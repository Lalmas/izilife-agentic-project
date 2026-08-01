"""
helloasso_scraper.py
--------------------
Scrape les events HelloAsso pour une ville et envoie vers izilife.
Pattern identique à shotgun_scraper.py.

Usage :
    python helloasso_scraper.py --env=local --city=lille --dry-run
    python helloasso_scraper.py --env=local --city=lille --zone=lille --pages=5

Prérequis :
    pip install playwright requests playwright-stealth
    python -m playwright install chromium
    Variable : IZILIFE_AGENT_TOKEN

Note :
    Le parser PHP parseHelloAssoHtmlSource() est déjà dans WebsiteParser_lib.php.
    Ce script se contente d'envoyer le HTML brut.
    À tester quand l'espace partenaire sera développé.
"""

import os
import sys
import re
import time
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
        return Path("G:/Mon Drive") / folder
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

UPLOAD_PATH = "/scraper/agentUploadEventSources/{city_id}"

# Zones HelloAsso — adapter selon les villes couvertes
ZONES = {
    "lille":    "https://www.helloasso.com/associations?location=Lille&type=evenement",
    "paris":    "https://www.helloasso.com/associations?location=Paris&type=evenement",
    "lyon":     "https://www.helloasso.com/associations?location=Lyon&type=evenement",
    "bordeaux": "https://www.helloasso.com/associations?location=Bordeaux&type=evenement",
}

DELAY_PAGES  = (3, 6)
DELAY_EVENTS = (2, 5)

# ─────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

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


def sleep_random(mn, mx):
    time.sleep(random.uniform(mn, mx))

def apply_stealth(page):
    if HAS_STEALTH:
        stealth_sync(page)
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['fr-FR', 'fr']});
    """)

def extract_event_urls(html: str) -> list:
    """Extrait les URLs d'events HelloAsso depuis une page listing."""
    # HelloAsso : /evenements/{slug} ou /associations/{asso}/evenements/{slug}
    patterns = re.findall(
        r'href=["\']((https://www\.helloasso\.com)?/associations/[^"\']+/evenements/[^"\'?\s]+)["\']',
        html
    )
    seen = {}
    for path, base in patterns:
        url = path if path.startswith('http') else f"https://www.helloasso.com{path}"
        # Exclure les pages associations (garder seulement les events)
        if '/evenements/' in url:
            seen[url.split('?')[0]] = True
    return list(seen.keys())

def send_html(html, filename, base_url, city_id, verify_ssl, source_url=""):
    url = base_url + UPLOAD_PATH.format(city_id=city_id)
    try:
        files   = {"sources[]": (filename, html.encode("utf-8"), "text/html")}
        headers = {"X-Agent-Token": AGENT_TOKEN}
        data    = {"source_urls[]": source_url} if source_url else {}
        r = requests.post(url, files=files, data=data, headers=headers,
                          verify=verify_ssl, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            log(f"  ✅ {filename} → inserted={resp.get('inserted',0)} skipped={resp.get('skipped',0)}")
            return resp.get("inserted", 0) > 0
        else:
            log(f"  ❌ HTTP {r.status_code} : {r.text[:200]}")
            return False
    except Exception as e:
        log(f"  ❌ Erreur : {e}")
        return False

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env",     choices=ENVS.keys(), default="local")
    ap.add_argument("--city",    type=str, required=True)
    ap.add_argument("--zone",    choices=ZONES.keys(), default="lille")
    ap.add_argument("--pages",   type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    city_id    = resolve_city_id(args.city, base_url, verify_ssl)
    dry_run    = args.dry_run
    listing_base = ZONES[args.zone]

    log(f"=== helloasso_scraper.py — env={args.env} city={args.city} zone={args.zone}" +
        (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    stats = {"found": 0, "inserted": 0, "skipped": 0, "errors": 0}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()
        apply_stealth(page)

        # ── Phase 1 : Listing ─────────────────────────────────────
        all_event_urls = []

        for page_num in range(1, args.pages + 1):
            # HelloAsso pagination : paramètre page
            url = f"{listing_base}&page={page_num}"
            log(f"\nPage listing {page_num}/{args.pages} : {url}")

            try:
                page.goto(url, timeout=30000)
                try:
                    page.wait_for_selector('a[href*="/evenements/"]', timeout=12000)
                except:
                    pass
                sleep_random(*DELAY_PAGES)

                html = page.content()
                urls = extract_event_urls(html)
                log(f"  → {len(urls)} URLs trouvées")

                if not urls:
                    log("  → Page vide, arrêt")
                    break

                all_event_urls.extend(urls)

            except Exception as e:
                log(f"  ❌ Erreur page {page_num} : {e}")
                continue

        all_event_urls = list(dict.fromkeys(all_event_urls))
        stats["found"] = len(all_event_urls)
        log(f"\n📋 Total URLs uniques : {len(all_event_urls)}")

        if dry_run:
            for u in all_event_urls:
                log(f"  [DRY RUN] {u}")
            browser.close()
            return

        # ── Phase 2 : Visiter chaque event ───────────────────────
        for i, event_url in enumerate(all_event_urls, 1):
            slug     = event_url.rstrip('/').split('/')[-1]
            filename = f"helloasso_{slug}.html"
            log(f"\n[{i}/{len(all_event_urls)}] {event_url}")

            try:
                page.goto(event_url, timeout=30000)
                try:
                    page.wait_for_selector("h1", timeout=12000)
                except:
                    pass
                sleep_random(*DELAY_EVENTS)

                html = page.content()
                ok   = send_html(html, filename, base_url, city_id, verify_ssl, event_url)
                if ok:
                    stats["inserted"] += 1
                else:
                    stats["skipped"] += 1

            except Exception as e:
                log(f"  ❌ Erreur : {e}")
                stats["errors"] += 1

        browser.close()

    log(f"\n=== Résultat ===")
    log(f"  Trouvés  : {stats['found']}")
    log(f"  Insérés  : {stats['inserted']}")
    log(f"  Skippés  : {stats['skipped']}")
    log(f"  Erreurs  : {stats['errors']}")

if __name__ == "__main__":
    main()
