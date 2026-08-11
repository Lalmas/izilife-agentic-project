"""
dealabs_scraper.py  v2
----------------------
Scrape Dealabs sur 4 axes :
  1. Offres à la une  → https://www.dealabs.com/
  2. Top codes promo  → https://www.dealabs.com/codes-promo/top20
  3. Codes par marque → https://www.dealabs.com/codes-promo  (toutes les marques)
  4. Page marque      → https://www.dealabs.com/groupe/{brand}

Envoie vers postAgentIngestPromo() → _ingestExternalPromo().

Usage :
    python dealabs_scraper.py --env=local --city=lille --dry-run
    python dealabs_scraper.py --env=local --city=lille --mode=all
    python dealabs_scraper.py --env=local --city=lille --mode=brands --brands="amazon,nike,shein,disneyland-paris"
    python dealabs_scraper.py --env=local --city=lille --mode=homepage
    python dealabs_scraper.py --env=local --city=lille --mode=top-codes
    python dealabs_scraper.py --env=local --city=lille --mode=all --min-temp=100

Modes :
    all          Tout scraper (défaut)
    homepage     Offres à la une seulement
    top-codes    Top 20 codes promo seulement
    brand-codes  Codes promo par marque (page /codes-promo)
    brands       Pages marque directes (--brands requis)

Prérequis :
    pip install playwright requests playwright-stealth
    python -m playwright install chromium
    Variable : IZILIFE_AGENT_TOKEN

SQL à exécuter UNE FOIS :
    INSERT INTO PromoSource (name, string_id, source_type, website_url, is_active) VALUES
    ('Dealabs', 'dealabs', 'manual_web', 'https://www.dealabs.com', 1);
"""

import os
import sys
import re
import time
import json
import random
import argparse
import requests
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("pip install playwright && python -m playwright install chromium")
    sys.exit(1)

try:
    from playwright_stealth import stealth_sync
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False

# ─────────────────────────────────────────────
# CONFIGURATION — envs via core.paths avec fallback local
# ─────────────────────────────────────────────

CORE_ROOT = Path(__file__).resolve().parents[2]
if str(CORE_ROOT) not in sys.path:
    sys.path.append(str(CORE_ROOT))
try:
    from core.paths import (
        IZILIFE_ENVS, normalize_zone, workspace_root, local_agent_workspace_root,
        event_curate_file, event_download_dir, event_source_dir, event_sent_log_file
    )
    ENVS = IZILIFE_ENVS
except Exception:
    def normalize_zone(zone: str) -> str:
        zone = str(zone or "").strip().lower()
        return zone if zone.endswith("-zone") else f"{zone}-zone"
    ENVS = {
        "local":   {"base_url": "https://localhost:4443/izilife-admin",          "verify_ssl": False},
        "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify_ssl": True},
        "prod":    {"base_url": "https://www.izilife.co/izilife-admin",          "verify_ssl": True},
    }
    def local_agent_workspace_root(env_name="prod"):
        suffix = {"local":"-local", "staging":"-staging", "prod":""}.get(env_name, "")
        return Path.home() / "Documents" / "agentic_Workspace" / "izilife" / f"izilife-agent-workspace{suffix}"
    def workspace_root(env_name="prod"):
        folder = {"local":"agentic_workspace_local", "staging":"agentic_workspace_staging", "prod":"agentic_workspace"}.get(env_name, "agentic_workspace")
        return Path(os.environ["AGENTIC_DRIVE_ROOT"]).expanduser() / folder
    def event_curate_file(zone, env_name="prod"):
        return workspace_root(env_name) / "izilife" / "events" / normalize_zone(zone) / "curate_events.xlsx"
    def event_download_dir(zone, env_name="prod", downloads=True):
        d = local_agent_workspace_root(env_name) / "images" / normalize_zone(zone) / ("downloads" if downloads else "")
        d.mkdir(parents=True, exist_ok=True)
        return d
    def event_source_dir(platform, zone, env_name="prod"):
        d = local_agent_workspace_root(env_name) / platform / normalize_zone(zone) / "events"
        d.mkdir(parents=True, exist_ok=True)
        return d
    def event_sent_log_file(env_name="prod"):
        d = local_agent_workspace_root(env_name) / "logs"
        d.mkdir(parents=True, exist_ok=True)
        return d / "event_images_sent.txt"

AGENT_TOKEN = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()

UPLOAD_PATH = "/scraper/agentIngestPromo/{city_id}"

DEALABS_BASE = "https://www.dealabs.com"

# Marques par défaut — grandes enseignes / loisirs / mode
DEFAULT_BRANDS = [
    "amazon",
    "nike",
    "adidas",
    "shein",
    "uniqlo",
    "auchan",
    "carrefour",
    "disneyland-paris",
    "zara",
    "h-m",
    "decathlon",
    "fnac",
    "cdiscount",
    "booking-com",
    "sncf",
    "airbnb",
    "spotify",
    "netflix",
]

# Délais anti-bot (secondes)
DELAY_PAGES = (3, 6)
DELAY_ITEMS = (0.5, 1.5)

# ─────────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────────

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def sleep_random(mn: float, mx: float):
    time.sleep(random.uniform(mn, mx))


def apply_stealth(page):
    if HAS_STEALTH:
        stealth_sync(page)
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['fr-FR', 'fr']});
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        window.chrome = { runtime: {} };
    """)


def parse_discount(text: str) -> tuple:
    """
    Extrait (discount_value, discount_type) depuis un label de remise.
    Ex : "30% DE REMISE" → (30.0, 'percent')
         "5€ DE REMISE"  → (5.0, 'amount')
         "GRATUIT"       → (0.0, 'free_product')
         "ENVOI OFFERT"  → (0.0, 'free_shipping')
         "81€ BILLET"    → (81.0, 'fixed_price')
    """
    if not text:
        return None, 'deal'
    t = text.strip().upper()

    if 'GRATUIT' in t or 'FREE' in t:
        return 0.0, 'free_product'
    if 'ENVOI OFFERT' in t or 'LIVRAISON' in t and 'OFFERT' in t:
        return 0.0, 'free_shipping'

    m = re.search(r'(\d+[\.,]?\d*)\s*%', t)
    if m:
        return float(m.group(1).replace(',', '.')), 'percent'

    m = re.search(r'(\d+[\.,]?\d*)\s*[€$£]', t)
    if m:
        return float(m.group(1).replace(',', '.')), 'amount'

    return None, 'deal'


def parse_temperature(text: str) -> float | None:
    """Extrait la température (popularité) depuis un texte."""
    if not text:
        return None
    m = re.search(r'[\-−]?(\d+[\.,]?\d*)', text.replace('\u2212', '-'))
    if m:
        return float(m.group(0).replace(',', '.').replace('−', '-'))
    return None


def build_promo(title, description, landing_url, code, discount_value,
                discount_type, store, promo_kind='deal',
                scope_level='online', start_at=None, end_at=None,
                temperature=None, brand=None) -> dict:
    return {
        'source_string_id': 'dealabs',
        'owner_type':       'izilife',
        'promo_kind':       promo_kind,
        'scope_level':      scope_level,
        'title':            title,
        'description':      description,
        'landing_url':      landing_url,
        'code':             code,
        'discount_type':    discount_type or 'deal',
        'discount_value':   discount_value,
        'currency':         'EUR',
        'start_at':         start_at,
        'end_at':           end_at,
        'priority':         0,
        # champs enrichis — ignorés si absent côté PHP
        '_meta_store':      store,
        '_meta_temperature':temperature,
        '_meta_brand':      brand,
    }


def send_promo(promo: dict, base_url: str, city_id: int,
               verify_ssl: bool, dry_run: bool) -> bool:
    if dry_run:
        title = (promo.get('title') or '')[:60]
        code  = f" [{promo['code']}]" if promo.get('code') else ''
        disc  = f" {promo['discount_value']}{promo['discount_type']}" if promo.get('discount_value') else ''
        log(f"    [DRY] {title}{code}{disc}")
        return True

    url = base_url + UPLOAD_PATH.format(city_id=city_id)
    try:
        r = requests.post(url, json=promo,
                          headers={"X-Agent-Token": AGENT_TOKEN,
                                   "Content-Type": "application/json"},
                          verify=verify_ssl, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            if resp.get('skipped'):
                log(f"    ↩️  Doublon : {(promo.get('title') or '')[:50]}")
            else:
                log(f"    ✅ {(promo.get('title') or '')[:50]} → id={resp.get('id','?')}")
            return True
        else:
            log(f"    ❌ HTTP {r.status_code} : {r.text[:200]}")
            return False
    except Exception as e:
        log(f"    ❌ Erreur : {e}")
        return False


# ─────────────────────────────────────────────
# PARSERS DEALABS
# ─────────────────────────────────────────────

def _get_text(el, selector: str) -> str | None:
    """Raccourci : cherche un sélecteur dans un élément et retourne son texte."""
    try:
        node = el.query_selector(selector)
        return node.inner_text().strip() if node else None
    except:
        return None


def _get_attr(el, selector: str, attr: str) -> str | None:
    try:
        node = el.query_selector(selector)
        return node.get_attribute(attr) if node else None
    except:
        return None


def _abs_url(href: str | None) -> str | None:
    if not href:
        return None
    if href.startswith('http'):
        return href
    return DEALABS_BASE + href


# ── 1. Offres à la une (/  ou  /hot) ─────────────────────────────────────

def parse_homepage(page) -> list:
    """
    Scrape la liste des deals sur la page d'accueil Dealabs.
    Retourne une liste de dicts prêts pour build_promo().
    """
    log("  → parse_homepage()")
    results = []
    try:
        page.wait_for_selector('article', timeout=12000)
    except:
        log("  ⚠️  Timeout attente articles")

    articles = page.query_selector_all('article')
    log(f"  → {len(articles)} articles")

    for art in articles:
        try:
            # ── Titre ──────────────────────────────────────────────────────
            title = (
                _get_text(art, '[class*="thread-title"]') or
                _get_text(art, 'h2') or
                _get_text(art, 'h3') or
                _get_text(art, '[class*="cept-tt"]')
            )
            if not title:
                continue

            # ── Lien ───────────────────────────────────────────────────────
            href = (
                _get_attr(art, 'a[href*="/deals/"]', 'href') or
                _get_attr(art, 'a[href*="/hot/"]', 'href') or
                _get_attr(art, 'a[href]', 'href')
            )
            url = _abs_url(href)

            # ── Prix / remise ──────────────────────────────────────────────
            price_text = (
                _get_text(art, '[class*="thread-price"]') or
                _get_text(art, '[class*="price"]') or
                _get_text(art, '[class*="cept-tp"]')
            )
            disc_val, disc_type = parse_discount(price_text)

            # ── Description ────────────────────────────────────────────────
            desc = (
                _get_text(art, '[class*="thread-description"]') or
                _get_text(art, 'p')
            )

            # ── Marchand ───────────────────────────────────────────────────
            store = (
                _get_text(art, '[class*="merchant"]') or
                _get_text(art, '[class*="store"]')
            )

            # ── Température ────────────────────────────────────────────────
            temp_text = (
                _get_text(art, '[class*="vote-temp"]') or
                _get_text(art, '[class*="temperature"]') or
                _get_text(art, '[class*="cept-heat-score"]')
            )
            temp = parse_temperature(temp_text)

            results.append(dict(
                title=title, description=desc, landing_url=url,
                code=None, discount_value=disc_val, discount_type=disc_type,
                store=store, temperature=temp, brand=store,
                promo_kind='deal', scope_level='online',
            ))
        except:
            continue

    return results


# ── 2. Top codes promo (/codes-promo/top20) ───────────────────────────────

def parse_top_codes(page) -> list:
    """
    Scrape /codes-promo/top20.
    Les items sont des cards avec remise + titre + code éventuel.
    """
    log("  → parse_top_codes()")
    results = []
    try:
        page.wait_for_selector('[class*="coupons"], article, [class*="coupon"]', timeout=12000)
    except:
        pass

    # Dealabs affiche les codes dans des cards — plusieurs sélecteurs possibles
    cards = (
        page.query_selector_all('[class*="coupon-card"]') or
        page.query_selector_all('[class*="coupons"] li') or
        page.query_selector_all('article') or
        page.query_selector_all('[class*="thread"]')
    )
    log(f"  → {len(cards)} cards")

    for card in cards:
        try:
            title = (
                _get_text(card, '[class*="title"]') or
                _get_text(card, 'h2') or _get_text(card, 'h3') or
                _get_text(card, 'strong') or _get_text(card, 'p')
            )
            if not title:
                continue

            # Remise affichée en gros (ex: "30% DE REMISE", "5€ DE REMISE")
            badge_text = (
                _get_text(card, '[class*="badge"]') or
                _get_text(card, '[class*="discount"]') or
                _get_text(card, '[class*="amount"]') or
                _get_text(card, '[class*="percent"]')
            )
            disc_val, disc_type = parse_discount(badge_text or title)

            # Code promo éventuel
            code = (
                _get_text(card, '[class*="code"]') or
                _get_text(card, 'code') or
                _get_attr(card, '[data-code]', 'data-code')
            )
            # Nettoyer le code (parfois "Code : AMAZON5")
            if code:
                m = re.search(r'[A-Z0-9]{4,}', code.upper())
                code = m.group(0) if m else None

            href = (
                _get_attr(card, 'a[href*="/codes-promo/"]', 'href') or
                _get_attr(card, 'a[href]', 'href')
            )
            url = _abs_url(href)

            # Marque = depuis l'URL ou le titre
            brand = None
            if url:
                m = re.search(r'/codes-promo/([^/?#]+)', url)
                brand = m.group(1) if m else None

            # Date expiration
            exp_text = _get_text(card, '[class*="expire"]') or _get_text(card, '[class*="valid"]')
            end_at = None
            if exp_text:
                m = re.search(r'(\d{2})/(\d{2})/(\d{4})', exp_text)
                if m:
                    end_at = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"

            results.append(dict(
                title=title, description=None, landing_url=url,
                code=code, discount_value=disc_val, discount_type=disc_type,
                store=brand, temperature=None, brand=brand,
                promo_kind='code_promo' if code else 'deal',
                scope_level='online', end_at=end_at,
            ))
        except:
            continue

    return results


# ── 3. Codes promo par marque (/codes-promo) ─────────────────────────────

def parse_brand_codes_listing(page) -> list:
    """
    Scrape /codes-promo : la liste des marques avec leurs meilleures offres.
    Chaque bloc = une marque avec 1-4 offres visibles.
    """
    log("  → parse_brand_codes_listing()")
    results = []
    try:
        page.wait_for_selector('[class*="merchant"], [class*="brand"], article', timeout=12000)
    except:
        pass

    # Blocs marque — Dealabs utilise une grille avec des sections par brand
    sections = page.query_selector_all('[class*="merchant-block"], [class*="brand-block"], section')
    if not sections:
        sections = page.query_selector_all('article')
    log(f"  → {len(sections)} sections marques")

    for section in sections:
        try:
            # Nom de la marque
            brand_name = (
                _get_text(section, '[class*="merchant-name"]') or
                _get_text(section, '[class*="brand-name"]') or
                _get_text(section, 'h2') or _get_text(section, 'h3')
            )

            # Offres dans cette section
            offers = section.query_selector_all('[class*="offer"], [class*="coupon"], li, [class*="deal"]')
            if not offers:
                offers = [section]  # toute la section = une offre

            for offer in offers:
                title = (
                    _get_text(offer, '[class*="title"]') or
                    _get_text(offer, 'p') or
                    _get_text(offer, 'span')
                )
                if not title and brand_name:
                    title = brand_name  # fallback
                if not title:
                    continue

                badge = (
                    _get_text(offer, '[class*="badge"]') or
                    _get_text(offer, '[class*="discount"]') or
                    _get_text(offer, '[class*="amount"]')
                )
                disc_val, disc_type = parse_discount(badge or '')

                code_text = (
                    _get_text(offer, '[class*="code"]') or
                    _get_text(offer, 'code')
                )
                code = None
                if code_text:
                    m = re.search(r'[A-Z0-9]{4,}', code_text.upper())
                    code = m.group(0) if m else None

                href = _get_attr(offer, 'a[href]', 'href')
                url  = _abs_url(href)

                exp_text = _get_text(offer, '[class*="expire"]')
                end_at = None
                if exp_text:
                    m = re.search(r'(\d{2})/(\d{2})/(\d{4})', exp_text)
                    if m:
                        end_at = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"

                results.append(dict(
                    title=title, description=None, landing_url=url,
                    code=code, discount_value=disc_val, discount_type=disc_type,
                    store=brand_name, temperature=None, brand=brand_name,
                    promo_kind='code_promo' if code else 'deal',
                    scope_level='online', end_at=end_at,
                ))
        except:
            continue

    return results


# ── 4. Page marque directe (/groupe/{brand}) ─────────────────────────────

def parse_brand_page(page, brand_slug: str) -> list:
    """
    Scrape la page dédiée à une marque sur Dealabs.
    Ex : /groupe/amazon, /groupe/disneyland-paris
    """
    log(f"  → parse_brand_page({brand_slug})")
    results = []
    try:
        page.wait_for_selector('article, [class*="thread"], [class*="coupon"]', timeout=12000)
    except:
        pass

    # Articles de deals
    articles = page.query_selector_all('article')
    # Cards de codes promo (zone codes promo en haut de page)
    code_cards = page.query_selector_all('[class*="coupon"], [class*="code-card"]')

    all_items = list(code_cards) + list(articles)
    log(f"  → {len(all_items)} items ({len(code_cards)} codes + {len(articles)} deals)")

    for item in all_items:
        try:
            # ── Type de l'item ──────────────────────────────────────────────
            is_code = bool(item.query_selector('[class*="code"]') or
                          item.query_selector('code'))

            # ── Titre ──────────────────────────────────────────────────────
            title = (
                _get_text(item, '[class*="title"]') or
                _get_text(item, '[class*="thread-title"]') or
                _get_text(item, 'h2') or _get_text(item, 'h3') or
                _get_text(item, 'p')
            )
            if not title:
                continue

            # ── Badge remise ───────────────────────────────────────────────
            badge = (
                _get_text(item, '[class*="badge"]') or
                _get_text(item, '[class*="discount"]') or
                _get_text(item, '[class*="thread-price"]') or
                _get_text(item, '[class*="price"]') or
                _get_text(item, '[class*="amount"]')
            )
            disc_val, disc_type = parse_discount(badge or '')

            # ── Code promo ─────────────────────────────────────────────────
            code_text = (
                _get_text(item, '[class*="code"]') or
                _get_text(item, 'code')
            )
            code = None
            if code_text:
                m = re.search(r'[A-Z0-9]{4,}', code_text.upper())
                code = m.group(0) if m else None

            # ── Lien ───────────────────────────────────────────────────────
            href = (
                _get_attr(item, 'a[href*="/deals/"]', 'href') or
                _get_attr(item, 'a[href*="/hot/"]', 'href') or
                _get_attr(item, 'a[href*="/codes-promo/"]', 'href') or
                _get_attr(item, 'a[href]', 'href')
            )
            url = _abs_url(href)

            # ── Description ────────────────────────────────────────────────
            desc = (
                _get_text(item, '[class*="description"]') or
                _get_text(item, 'p')
            )

            # ── Température ────────────────────────────────────────────────
            temp_text = (
                _get_text(item, '[class*="vote-temp"]') or
                _get_text(item, '[class*="temperature"]') or
                _get_text(item, '[class*="heat"]')
            )
            temp = parse_temperature(temp_text)

            # ── Expiration ─────────────────────────────────────────────────
            exp_text = _get_text(item, '[class*="expire"]') or _get_text(item, '[class*="valid"]')
            end_at = None
            if exp_text:
                m = re.search(r'(\d{2})/(\d{2})/(\d{4})', exp_text)
                if m:
                    end_at = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"

            results.append(dict(
                title=title, description=desc, landing_url=url,
                code=code, discount_value=disc_val, discount_type=disc_type,
                store=brand_slug, temperature=temp, brand=brand_slug,
                promo_kind='code_promo' if (is_code or code) else 'deal',
                scope_level='online', end_at=end_at,
            ))
        except:
            continue

    return results


# ─────────────────────────────────────────────
# RUNNER PRINCIPAL
# ─────────────────────────────────────────────

def process_results(raw_items: list, seen_urls: set,
                    base_url: str, city_id: int, verify_ssl: bool,
                    dry_run: bool, min_temp: float | None) -> dict:
    """Filtre, déduplique, envoie."""
    stats = {"found": 0, "sent": 0, "skipped": 0, "errors": 0, "filtered": 0}

    for item in raw_items:
        url = item.get('landing_url')

        # ── Déduplique par URL ─────────────────────────────────────────────
        if url and url in seen_urls:
            stats["skipped"] += 1
            continue
        if url:
            seen_urls.add(url)

        # ── Filtre température minimale ────────────────────────────────────
        if min_temp is not None:
            temp = item.get('temperature')
            if temp is not None and temp < min_temp:
                stats["filtered"] += 1
                continue

        stats["found"] += 1

        promo = build_promo(
            title=item['title'],
            description=item.get('description'),
            landing_url=item.get('landing_url'),
            code=item.get('code'),
            discount_value=item.get('discount_value'),
            discount_type=item.get('discount_type'),
            store=item.get('store'),
            promo_kind=item.get('promo_kind', 'deal'),
            scope_level=item.get('scope_level', 'online'),
            end_at=item.get('end_at'),
            temperature=item.get('temperature'),
            brand=item.get('brand'),
        )

        ok = send_promo(promo, base_url, city_id, verify_ssl, dry_run)
        if ok:
            stats["sent"] += 1
        else:
            stats["errors"] += 1

        sleep_random(*DELAY_ITEMS)

    return stats




def resolve_city_id(city_slug: str, base_url: str, verify_ssl: bool) -> int:
    """Résout le city_id depuis le string_id (ex: 'lille' → 1)."""
    url = f"{base_url}/scraper/cityByStringId/{city_slug}"
    try:
        r = requests.get(url, headers={"X-Agent-Token": AGENT_TOKEN},
                         verify=verify_ssl, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('success') and data.get('city'):
                city_id = int(data['city']['id'])
                log(f"Ville résolue : {city_slug} → city_id={city_id}")
                return city_id
    except Exception as e:
        log(f"  ⚠️  Erreur résolution ville : {e}")
    log(f"❌ Ville introuvable : {city_slug}")
    sys.exit(1)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env",       choices=ENVS.keys(), default="local")
    ap.add_argument("--city",      type=str, required=True)
    ap.add_argument("--mode",      choices=["all", "homepage", "top-codes",
                                            "brand-codes", "brands"],
                    default="all")
    ap.add_argument("--brands",    type=str, default=None,
                    help="Slugs séparés par virgule : amazon,nike,shein")
    ap.add_argument("--min-temp",  type=float, default=None,
                    help="Ne garder que les deals avec température ≥ N")
    ap.add_argument("--dry-run",   action="store_true")
    args = ap.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    dry_run    = args.dry_run
    city_id    = resolve_city_id(args.city, base_url, verify_ssl)
    min_temp   = args.min_temp

    brands = [b.strip() for b in args.brands.split(',')] if args.brands else DEFAULT_BRANDS
    mode   = args.mode

    tag = " [DRY RUN]" if dry_run else ""
    log(f"=== dealabs_scraper v2 — env={args.env} city={args.city} city_id={city_id} mode={mode}{tag} ===")
    if min_temp is not None:
        log(f"Filtre température ≥ {min_temp}°")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    seen_urls = set()
    total     = {"found": 0, "sent": 0, "skipped": 0, "errors": 0, "filtered": 0}

    def add(s):
        for k in total:
            total[k] += s.get(k, 0)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                " AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/125.0.0.0 Safari/537.36",
            ]
        )
        page = browser.new_page()
        apply_stealth(page)

        # ── Homepage ────────────────────────────────────────────────────────
        if mode in ("all", "homepage"):
            log(f"\n{'='*55}")
            log("OFFRES À LA UNE  →  https://www.dealabs.com/")
            log(f"{'='*55}")
            try:
                page.goto(DEALABS_BASE + "/", timeout=30000)
                sleep_random(*DELAY_PAGES)
                items = parse_homepage(page)
                add(process_results(items, seen_urls, base_url,
                                    args.city, verify_ssl, dry_run, min_temp))
            except Exception as e:
                log(f"❌ Homepage : {e}")

        # ── Top codes promo ─────────────────────────────────────────────────
        if mode in ("all", "top-codes"):
            log(f"\n{'='*55}")
            log("TOP CODES PROMO  →  /codes-promo/top20")
            log(f"{'='*55}")
            try:
                page.goto(DEALABS_BASE + "/codes-promo/top20", timeout=30000)
                sleep_random(*DELAY_PAGES)
                items = parse_top_codes(page)
                add(process_results(items, seen_urls, base_url,
                                    args.city, verify_ssl, dry_run, min_temp))
            except Exception as e:
                log(f"❌ Top codes : {e}")

        # ── Codes promo listing ─────────────────────────────────────────────
        if mode in ("all", "brand-codes"):
            log(f"\n{'='*55}")
            log("CODES PROMO PAR MARQUE  →  /codes-promo")
            log(f"{'='*55}")
            try:
                page.goto(DEALABS_BASE + "/codes-promo", timeout=30000)
                sleep_random(*DELAY_PAGES)
                items = parse_brand_codes_listing(page)
                add(process_results(items, seen_urls, base_url,
                                    args.city, verify_ssl, dry_run, min_temp))
            except Exception as e:
                log(f"❌ Brand codes listing : {e}")

        # ── Pages marque directes ───────────────────────────────────────────
        if mode in ("all", "brands"):
            for brand in brands:
                log(f"\n{'='*55}")
                log(f"MARQUE  →  /groupe/{brand}")
                log(f"{'='*55}")
                try:
                    page.goto(DEALABS_BASE + f"/groupe/{brand}", timeout=30000)
                    sleep_random(*DELAY_PAGES)
                    items = parse_brand_page(page, brand)
                    add(process_results(items, seen_urls, base_url,
                                        args.city, verify_ssl, dry_run, min_temp))
                except Exception as e:
                    log(f"❌ Marque {brand} : {e}")

        browser.close()

    log(f"\n{'='*55}")
    log("RÉSULTAT FINAL")
    log(f"{'='*55}")
    log(f"  Trouvés  : {total['found']}")
    log(f"  Envoyés  : {total['sent']}")
    log(f"  Doublons : {total['skipped']}")
    log(f"  Filtrés  : {total['filtered']}")
    log(f"  Erreurs  : {total['errors']}")


if __name__ == "__main__":
    main()
