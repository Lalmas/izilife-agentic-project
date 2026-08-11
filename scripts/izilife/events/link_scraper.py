"""
link_scraper.py
---------------
Ingère un event depuis une URL directe (HelloAsso, Billetweb, Shotgun,
Eventbrite, Facebook Event unique...).
Détecte la plateforme, visite la page, envoie le HTML à izilife.

Usage :
    python link_scraper.py --env=local --city=lille --url="https://www.helloasso.com/associations/..."
    python link_scraper.py --env=local --city=lille --url="https://shotgun.live/fr/events/..."
    python link_scraper.py --env=local --city=lille --url="https://www.billetweb.fr/..." --dry-run

Cas d'usage :
    Un lieu partenaire envoie un lien → BO appelle ce script via exec() ou queue.
    Utilisable aussi en ligne de commande pour test rapide.

À activer quand l'espace partenaire sera développé.
"""

import os, sys, re, time, random, argparse, requests, json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

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

UPLOAD_PATH = "/scraper/agentUploadEventSources/{city_id}"

SCRIPTS_DIR = Path(__file__).parent

# Mapping domaine → profil cookies optionnel
COOKIES_MAP = {
    "facebook.com":   SCRIPTS_DIR / "profiles" / "facebook"   / "fb_cookies.json",
    "eventbrite.fr":  SCRIPTS_DIR / "profiles" / "eventbrite" / "eb_cookies.json",
    "meetup.com":     SCRIPTS_DIR / "profiles" / "meetup"     / "meetup_cookies.json",
}

# Mapping domaine → sélecteur d'attente
WAIT_SELECTOR_MAP = {
    "shotgun.live":       "h1",
    "helloasso.com":      "h1",
    "billetweb.fr":       "h1",
    "eventbrite.fr":      '[data-testid="event-title"], h1',
    "meetup.com":         "h1",
    "facebook.com":       '[data-testid="event-name"], h1',
    "weezevent.com":      "h1",
    "festik.net":         "h1",
}

DELAY = (2, 5)

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

def detect_platform(url: str) -> str:
    """Détecte la plateforme depuis l'URL."""
    domain = urlparse(url).netloc.lower().replace("www.", "")
    for key in COOKIES_MAP:
        if key in domain:
            return key
    # Détection par pattern URL
    if "shotgun.live" in domain:
        return "shotgun.live"
    if "helloasso" in domain:
        return "helloasso.com"
    if "billetweb" in domain:
        return "billetweb.fr"
    if "weezevent" in domain:
        return "weezevent.com"
    if "festik" in domain:
        return "festik.net"
    return domain  # inconnu mais on essaie quand même

def apply_stealth(page):
    if HAS_STEALTH:
        stealth_sync(page)
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['fr-FR', 'fr']});
        window.chrome = { runtime: {} };
    """)

def load_cookies(context, platform: str):
    cookies_path = COOKIES_MAP.get(platform)
    if cookies_path and cookies_path.exists():
        cookies = json.loads(cookies_path.read_text())
        context.add_cookies(cookies)
        log(f"  🍪 {len(cookies)} cookies chargés ({platform})")

def send_html(html, filename, base_url, city_id, verify_ssl, source_url):
    url = base_url + UPLOAD_PATH.format(city_id=city_id)
    try:
        r = requests.post(url,
                          files={"sources[]": (filename, html.encode("utf-8"), "text/html")},
                          data={"source_urls[]": source_url},
                          headers={"X-Agent-Token": AGENT_TOKEN},
                          verify=verify_ssl, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            log(f"  ✅ inserted={resp.get('inserted',0)} skipped={resp.get('skipped',0)}")
            return resp
        log(f"  ❌ HTTP {r.status_code} : {r.text[:200]}")
        return None
    except Exception as e:
        log(f"  ❌ {e}")
        return None

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env",     choices=ENVS.keys(), default="local")
    ap.add_argument("--city",    type=str, required=True)
    ap.add_argument("--url",     type=str, required=True, help="URL de l'event à ingérer")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    city_id    = resolve_city_id(args.city, base_url, verify_ssl)
    dry_run    = args.dry_run
    target_url = args.url.strip()

    platform = detect_platform(target_url)
    wait_sel  = WAIT_SELECTOR_MAP.get(platform, "h1")

    log(f"=== link_scraper.py — platform={platform}" + (" [DRY RUN]" if dry_run else "") + " ===")
    log(f"URL : {target_url}")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled",
                  "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]
        )
        context = browser.new_context()
        load_cookies(context, platform)
        page = context.new_page()
        apply_stealth(page)

        try:
            log("Chargement de la page...")
            page.goto(target_url, timeout=30000)
            try:
                page.wait_for_selector(wait_sel, timeout=15000)
            except:
                log(f"  ⚠️  Sélecteur '{wait_sel}' non trouvé — on continue quand même")
            sleep_random(*DELAY)

            html = page.content()
            title = page.title()
            log(f"  Titre : {title[:80]}")

            if dry_run:
                log(f"  [DRY RUN] HTML récupéré ({len(html)} chars) — pas d'envoi")
                browser.close()
                return

            # Construire le nom de fichier depuis l'URL
            slug = re.sub(r'[^a-z0-9\-]', '-', target_url.split('/')[-1].lower())[:60] or "event"
            filename = f"{platform.split('.')[0]}_{slug}.html"

            result = send_html(html, filename, base_url, city_id, verify_ssl, target_url)

            if result:
                sys.exit(0)
            else:
                sys.exit(1)

        except Exception as e:
            log(f"❌ Erreur fatale : {e}")
            browser.close()
            sys.exit(1)

        browser.close()

if __name__ == "__main__":
    main()
