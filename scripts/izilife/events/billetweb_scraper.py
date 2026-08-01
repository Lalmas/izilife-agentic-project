"""
billetweb_scraper.py
--------------------
Scrape les events Billetweb pour une ville et envoie vers izilife.
Pattern identique à shotgun_scraper.py.

Usage :
    python billetweb_scraper.py --env=local --city=lille --dry-run
    python billetweb_scraper.py --env=local --city=lille --zone=lille --pages=5

À tester quand l'espace partenaire sera développé.
"""

import os, sys, re, time, random, argparse, requests
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

ENVS = {
    "local":   {"base_url": "https://localhost:4443/izilife-admin",          "verify_ssl": False},
    "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify_ssl": True},
    "prod":    {"base_url": "https://www.izilife.co/izilife-admin",          "verify_ssl": True},
}

AGENT_TOKEN = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()

UPLOAD_PATH = "/scraper/agentUploadEventSources/{city_id}"

# Billetweb : recherche par ville
ZONES = {
    "lille":    "https://www.billetweb.fr/multi_event.php?filter_city=Lille",
    "paris":    "https://www.billetweb.fr/multi_event.php?filter_city=Paris",
    "lyon":     "https://www.billetweb.fr/multi_event.php?filter_city=Lyon",
    "bordeaux": "https://www.billetweb.fr/multi_event.php?filter_city=Bordeaux",
}

DELAY_PAGES  = (3, 5)
DELAY_EVENTS = (2, 4)

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
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

def extract_event_urls(html: str) -> list:
    """Extrait les URLs d'events Billetweb."""
    # Billetweb : URLs type /event-slug ou /shop/{id}/{slug}
    patterns = re.findall(
        r'href=["\']((https://www\.billetweb\.fr)?/(?:shop/[^"\'?\s]+|[a-z0-9][a-z0-9\-]{3,80}))["\']',
        html
    )
    seen = {}
    for path, base in patterns:
        url = path if path.startswith('http') else f"https://www.billetweb.fr{path}"
        # Filtrer les pages non-event (multi_event, inscription, etc.)
        if any(x in url for x in ['multi_event', 'inscription', 'connexion', 'contact']):
            continue
        if len(url) > 30:  # URL assez longue pour être un event
            seen[url.split('?')[0]] = True
    return list(seen.keys())

def send_html(html, filename, base_url, city_id, verify_ssl, source_url=""):
    url = base_url + UPLOAD_PATH.format(city_id=city_id)
    try:
        r = requests.post(url,
                          files={"sources[]": (filename, html.encode("utf-8"), "text/html")},
                          data={"source_urls[]": source_url} if source_url else {},
                          headers={"X-Agent-Token": AGENT_TOKEN},
                          verify=verify_ssl, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            log(f"  ✅ {filename} → inserted={resp.get('inserted',0)}")
            return resp.get("inserted", 0) > 0
        log(f"  ❌ HTTP {r.status_code} : {r.text[:200]}")
        return False
    except Exception as e:
        log(f"  ❌ {e}")
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env",     choices=ENVS.keys(), default="local")
    ap.add_argument("--city",    type=str, required=True)
    ap.add_argument("--zone",    choices=ZONES.keys(), default="lille")
    ap.add_argument("--pages",   type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    set_current_env(args.env)

    env      = ENVS[args.env]
    dry_run  = args.dry_run
    log(f"=== billetweb_scraper.py — zone={args.zone}" + (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    stats = {"found": 0, "inserted": 0, "skipped": 0, "errors": 0}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
                                    args=["--disable-blink-features=AutomationControlled"])
        page = browser.new_page()
        apply_stealth(page)

        all_event_urls = []
        for page_num in range(1, args.pages + 1):
            url = ZONES[args.zone] + f"&page={page_num}"
            log(f"\nPage {page_num} : {url}")
            try:
                page.goto(url, timeout=30000)
                try:
                    page.wait_for_selector('.event, .card, article', timeout=10000)
                except:
                    pass
                sleep_random(*DELAY_PAGES)
                urls = extract_event_urls(page.content())
                log(f"  → {len(urls)} URLs")
                if not urls:
                    log("  → Vide, arrêt")
                    break
                all_event_urls.extend(urls)
            except Exception as e:
                log(f"  ❌ {e}")

        all_event_urls = list(dict.fromkeys(all_event_urls))
        stats["found"] = len(all_event_urls)
        log(f"\n📋 {len(all_event_urls)} URLs uniques")

        if dry_run:
            [log(f"  [DRY] {u}") for u in all_event_urls]
            browser.close()
            return

        for i, event_url in enumerate(all_event_urls, 1):
            slug = event_url.rstrip('/').split('/')[-1]
            log(f"\n[{i}/{len(all_event_urls)}] {event_url}")
            try:
                page.goto(event_url, timeout=30000)
                try:
                    page.wait_for_selector("h1", timeout=10000)
                except:
                    pass
                sleep_random(*DELAY_EVENTS)
                ok = send_html(page.content(), f"billetweb_{slug}.html",
                               env["base_url"], city_id, env["verify_ssl"], event_url)
                stats["inserted" if ok else "skipped"] += 1
            except Exception as e:
                log(f"  ❌ {e}")
                stats["errors"] += 1

        browser.close()

    log(f"\n=== Résultat : trouvés={stats['found']} insérés={stats['inserted']} "
        f"skippés={stats['skipped']} erreurs={stats['errors']}")

if __name__ == "__main__":
    main()
