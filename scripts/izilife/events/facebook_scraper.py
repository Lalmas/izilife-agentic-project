"""
facebook_scraper.py
-------------------
Scrape les events Facebook via Chrome + cookies existants.
Login auto depuis .env si cookies absents/expirés.
Mode interactif : tu configures ville/rayon/filtre, puis Entrée pour lancer.

Usage :
    python facebook_scraper.py --env=local --city=lille --dry-run
    python facebook_scraper.py --env=local --city=lille --max-events=100

Prérequis :
    pip install playwright requests playwright-stealth browser-cookie3 python-dotenv
    python -m playwright install chromium
    Variable : IZILIFE_AGENT_TOKEN

.env (dans scripts/izilife/events/) :
    FB_EMAIL=laleventorganizer@gmail.com
    FB_PASSWORD=ton_mdp
"""

import os
import sys
import re
import json
import time
import random
import argparse
import requests
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenv optionnel

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

try:
    import browser_cookie3
    HAS_COOKIE3 = True
except ImportError:
    HAS_COOKIE3 = False

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

AGENT_TOKEN          = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()

FB_EMAIL             = os.environ.get("FB_EMAIL", "")
FB_PASSWORD          = os.environ.get("FB_PASSWORD", "")
UPLOAD_PATH          = "/scraper/agentUploadEventSources/{city_id}"
FB_EVENTS_URL        = "https://www.facebook.com/events"
FB_LOGIN_URL         = "https://www.facebook.com/login"
DELAY_SCROLL         = (2, 4)
DELAY_BETWEEN_EVENTS = (3, 6)
COOKIES_FILE         = Path(__file__).parent / "profiles" / "facebook" / "fb_cookies.json"

CHROMIUM_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-notifications",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

# ─────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def resolve_city_id(city_slug: str, base_url: str, verify_ssl: bool) -> int:
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


def sleep_random(min_s: float, max_s: float):
    time.sleep(random.uniform(min_s, max_s))


def apply_stealth(page):
    if HAS_STEALTH:
        stealth_sync(page)
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        Object.defineProperty(navigator, 'languages', {get: () => ['fr-FR', 'fr']});
        window.chrome = { runtime: {} };
    """)


def get_facebook_cookies() -> list:
    """Charge les cookies Facebook depuis fichier JSON ou browser-cookie3."""
    if COOKIES_FILE.exists():
        try:
            with open(COOKIES_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
            cookies = [
                {"name": c.get("name",""), "value": c.get("value",""),
                 "domain": c.get("domain", ".facebook.com"), "path": c.get("path", "/")}
                for c in raw if c.get("name") and c.get("value")
            ]
            log(f"Cookies chargés depuis {COOKIES_FILE.name} : {len(cookies)}")
            return cookies
        except Exception as e:
            log(f"Erreur lecture cookies JSON : {e}")

    if HAS_COOKIE3:
        try:
            jar = browser_cookie3.chrome(domain_name=".facebook.com")
            cookies = [{"name": c.name, "value": c.value,
                        "domain": c.domain or ".facebook.com", "path": c.path or "/"}
                       for c in jar]
            log(f"Cookies Facebook lus depuis Chrome : {len(cookies)}")
            return cookies
        except Exception as e:
            log(f"browser-cookie3 : {e}")

    log("⚠️  Aucun cookie trouvé")
    return []


def login_facebook(page) -> bool:
    """Login automatique depuis .env si FB_EMAIL et FB_PASSWORD définis."""
    if not FB_EMAIL or not FB_PASSWORD:
        return False

    log(f"Tentative login auto : {FB_EMAIL}")
    try:
        page.goto(FB_LOGIN_URL, timeout=30000)
        sleep_random(2, 3)

        page.fill('#email', FB_EMAIL)
        sleep_random(0.5, 1)
        page.fill('#pass', FB_PASSWORD)
        sleep_random(0.5, 1)
        page.click('[name="login"]')
        sleep_random(4, 6)

        # Vérifier si connecté
        if "login" not in page.url and "checkpoint" not in page.url:
            log("✅ Login auto réussi")
            return True
        else:
            log("⚠️  Login auto échoué (2FA ou erreur)")
            return False
    except Exception as e:
        log(f"  ❌ Erreur login : {e}")
        return False


def clean_facebook_title_suffix(html: str) -> str:
    """Retire uniquement le suffixe final Facebook des titres HTML/OG."""
    return re.sub(
        r"\s*\|\s*Facebook\s*(?=(?:</title>|[\"']))",
        "",
        html,
        flags=re.IGNORECASE,
    )


def send_html(
    html: str,
    filename: str,
    base_url: str,
    city_id: int,
    verify_ssl: bool,
    source_url: str = ""
) -> dict:
    url = base_url + UPLOAD_PATH.format(city_id=city_id)
    html = clean_facebook_title_suffix(html)

    try:
        files = {
            "sources[]": (
                filename,
                html.encode("utf-8"),
                "text/html"
            )
        }

        headers = {
            "X-Agent-Token": AGENT_TOKEN,
            "Accept": "application/json",
        }

        postdata = {
            "source_urls[]": source_url
        } if source_url else {}

        response = requests.post(
            url,
            files=files,
            data=postdata,
            headers=headers,
            verify=verify_ssl,
            timeout=120
        )

        content_type = response.headers.get("Content-Type", "")
        response_preview = response.text[:3000]

        if response.status_code != 200:
            log(f"  ❌ {filename} → HTTP {response.status_code}")
            log(f"     Content-Type : {content_type}")
            log(f"     Réponse : {response_preview}")

            return {
                "success": False,
                "inserted": 0,
                "skipped": 0,
                "errors": [
                    f"HTTP {response.status_code}"
                ],
            }

        try:
            data = response.json()
        except ValueError as exception:
            log(f"  ❌ {filename} → réponse non JSON")
            log(f"     Content-Type : {content_type}")
            log(f"     Erreur JSON : {exception}")
            log(f"     Réponse : {response_preview}")

            return {
                "success": False,
                "inserted": 0,
                "skipped": 0,
                "errors": [
                    "Réponse serveur non JSON"
                ],
            }

        inserted = int(data.get("inserted", 0) or 0)
        skipped = int(data.get("skipped", 0) or 0)

        errors = data.get("errors", [])
        diagnostics = data.get("diagnostics", []) or []

        if isinstance(errors, str):
            errors = [errors]

        if data.get("error"):
            errors.append(str(data["error"]))

        success = bool(data.get("success", True))

        if not success or errors:
            log(
                f"  ❌ {filename} → échec API "
                f"(inserted={inserted}, skipped={skipped})"
            )

            for error in errors:
                log(f"     ↳ {error}")

            log(
                "     JSON complet : "
                + json.dumps(
                    data,
                    ensure_ascii=False,
                    default=str
                )[:3000]
            )

            return {
                **data,
                "success": False,
                "inserted": inserted,
                "skipped": skipped,
                "errors": errors,
            }

        for diag in diagnostics:
            if diag.get("duplicate"):
                log(f"     DOUBLON: {diag.get('reason')} id={diag.get('duplicate_id')}")
                continue
            log(
                "     AUTO-VALIDATION: "
                f"score={diag.get('score', 0)} | "
                f"ville={'OK' if diag.get('city_found') else 'NON'} | "
                f"lieu={'OK' if diag.get('place_found') else 'NON'} | "
                f"categorie={'OK' if diag.get('category_found') else 'NON'} | "
                f"organisateur={'OK' if diag.get('organizer_found') else 'NON'} | "
                f"resultat={'VALIDÉ' if diag.get('auto_validated') else 'EN ATTENTE'} | "
                f"raison={diag.get('reason', '')}"
            )

        if inserted > 0:
            log(
                f"  ✅ {filename} → "
                f"inserted={inserted} skipped={skipped}"
            )
        elif skipped > 0:
            log(
                f"  ⚠️ {filename} → "
                f"inserted={inserted} skipped={skipped}"
            )
        else:
            log(f"  ❌ {filename} → aucun résultat retourné")
            log(
                "     JSON complet : "
                + json.dumps(
                    data,
                    ensure_ascii=False,
                    default=str
                )[:3000]
            )

        return {
            **data,
            "success": inserted > 0 or skipped > 0,
            "inserted": inserted,
            "skipped": skipped,
            "errors": errors,
        }

    except requests.Timeout:
        log(f"  ❌ {filename} → timeout API")

        return {
            "success": False,
            "inserted": 0,
            "skipped": 0,
            "errors": [
                "Timeout API"
            ],
        }

    except requests.RequestException as exception:
        log(f"  ❌ {filename} → erreur HTTP : {exception}")

        return {
            "success": False,
            "inserted": 0,
            "skipped": 0,
            "errors": [
                str(exception)
            ],
        }

    except Exception as exception:
        log(f"  ❌ {filename} → erreur inattendue : {exception}")

        return {
            "success": False,
            "inserted": 0,
            "skipped": 0,
            "errors": [
                str(exception)
            ],
        }


def extract_event_urls(page) -> list:
    urls = page.evaluate("""
        () => {
            const links = document.querySelectorAll('a[href*="/events/"]');
            const found = new Set();
            links.forEach(l => {
                const match = l.href.match(/facebook\\.com\\/events\\/(\\d{10,})/);
                if (match) found.add('https://www.facebook.com/events/' + match[1]);
            });
            return Array.from(found);
        }
    """)
    return urls or []


def scroll_and_collect(page, max_events: int) -> list:
    all_urls = set()
    scrolls  = 0

    while len(all_urls) < max_events and scrolls < 30:
        urls     = extract_event_urls(page)
        new_urls = set(urls) - all_urls
        if new_urls:
            log(f"  +{len(new_urls)} URLs ({len(all_urls) + len(new_urls)} total)")
            all_urls.update(new_urls)
        if len(all_urls) >= max_events:
            break
        try:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        except:
            page.keyboard.press("End")
        sleep_random(*DELAY_SCROLL)
        try:
            btn = page.locator('text="Voir plus"').first
            if btn.is_visible(timeout=1500):
                btn.click()
                sleep_random(1, 2)
        except:
            pass
        scrolls += 1

    return list(all_urls)[:max_events]


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env",        choices=ENVS.keys(), default="local")
    parser.add_argument("--city",       type=str, default="lille")
    parser.add_argument("--max-events", type=int, default=50)
    parser.add_argument("--dry-run",    action="store_true")
    args = parser.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    city_id    = resolve_city_id(args.city, base_url, verify_ssl)
    dry_run    = args.dry_run

    log(f"=== facebook_scraper.py — env={args.env} city={args.city} max={args.max_events}" +
        (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    cookies = get_facebook_cookies()
    stats   = {"found": 0, "inserted": 0, "skipped": 0, "errors": 0}

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            channel="chrome",
            args=CHROMIUM_ARGS,
        )
        context = browser.new_context(locale="fr-FR")

        if cookies:
            context.add_cookies(cookies)
            log(f"✅ {len(cookies)} cookies injectés")

        page = context.new_page()
        apply_stealth(page)

        # ── Phase 1 : Connexion ───────────────────────────────────
        log(f"\nOuverture de {FB_EVENTS_URL} ...")
        page.goto(FB_EVENTS_URL, timeout=30000)
        sleep_random(3, 5)

        # Si non connecté — tenter login auto, sinon mode interactif
        if "login" in page.url or "checkpoint" in page.url:
            log("⚠️  Non connecté — tentative login auto...")
            logged_in = login_facebook(page)

            if not logged_in:
                # Mode interactif — attendre connexion manuelle
                print("")
                print("=" * 60)
                print("  ❌ Login auto échoué ou 2FA requis.")
                print("  Connecte-toi manuellement dans Chrome.")
                print("  Quand tu es connecté → appuie sur ENTREE")
                print("=" * 60)
                input("")
                page.goto(FB_EVENTS_URL, timeout=30000)
                sleep_random(2, 3)

                if "login" in page.url:
                    log("❌ Toujours non connecté. Abandonne.")
                    browser.close()
                    sys.exit(1)

        log("✅ Facebook connecté")

        try:
            page.keyboard.press("Escape")
            sleep_random(1, 2)
        except:
            pass

        # ── Phase 2 : Mode interactif — configuration ─────────────
        print("")
        print("=" * 60)
        print("  Chrome ouvert sur Facebook Events.")
        print("  Configure maintenant dans Chrome :")
        print("  1. Localisation → Lille, rayon 31 km")
        print("  2. Filtre : Cette semaine / Semaine prochaine")
        print("  3. Scrolle pour charger plus d'events si besoin")
        print("")
        print("  Quand tu es prêt → appuie sur ENTREE ici")
        print("=" * 60)
        input("")

        # ── Phase 3 : Collecte des URLs ───────────────────────────
        log(f"Collecte des URLs (max {args.max_events})...")
        event_urls    = scroll_and_collect(page, args.max_events)
        stats["found"] = len(event_urls)
        log(f"\n📋 {len(event_urls)} URLs trouvées")

        if dry_run:
            for u in event_urls:
                log(f"  [DRY RUN] {u}")
            browser.close()
            return

        # ── Phase 4 : Visiter chaque event et envoyer ─────────────
        for i, event_url in enumerate(event_urls, 1):
            match    = re.search(r"/events/(\d+)", event_url)
            filename = f"fb_{match.group(1) if match else i}.html"
            log(f"\n[{i}/{len(event_urls)}] {event_url}")

            try:
                page.goto(event_url, timeout=30000)
                try:
                    page.wait_for_selector("h1", timeout=10000)
                except:
                    pass
                sleep_random(*DELAY_BETWEEN_EVENTS)

                html   = page.content()
                result = send_html(html, filename, base_url, city_id, verify_ssl,
                                   source_url=event_url)

                if result.get("inserted", 0) > 0:
                    stats["inserted"] += 1
                elif result.get("skipped", 0) > 0:
                    stats["skipped"] += 1
                else:
                    stats["errors"] += 1

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
