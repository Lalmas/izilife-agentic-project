"""
meetup_scraper.py
-----------------
Scrape les events Meetup pour une ville et envoie vers izilife.
Pattern identique à shotgun_scraper.py.

Usage :
    python meetup_scraper.py --env=local --city=lille --dry-run
    python meetup_scraper.py --env=local --city=lille --zone=lille --pages=5

Note :
    Meetup nécessite souvent une session authentifiée pour voir tous les events.
    Créer profiles/meetup/meetup_cookies.json si nécessaire.
    À tester quand l'espace partenaire sera développé.
"""

import os, sys, re, time, random, argparse, requests, json
from datetime import datetime
from pathlib import Path

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

AGENT_TOKEN  = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()

UPLOAD_PATH  = "/scraper/agentUploadEventSources/{city_id}"
COOKIES_PATH = Path(__file__).parent / "profiles" / "meetup" / "meetup_cookies.json"

# Meetup : recherche par ville avec paramètres géo
ZONES = {
    "lille":    "https://www.meetup.com/fr-FR/find/?location=fr--lille&source=EVENTS",
    "paris":    "https://www.meetup.com/fr-FR/find/?location=fr--paris&source=EVENTS",
    "lyon":     "https://www.meetup.com/fr-FR/find/?location=fr--lyon&source=EVENTS",
    "bordeaux": "https://www.meetup.com/fr-FR/find/?location=fr--bordeaux&source=EVENTS",
}

DELAY_PAGES  = (3, 6)
DELAY_EVENTS = (2, 5)

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
        window.chrome = { runtime: {} };
    """)

def load_cookies(context):
    if COOKIES_PATH.exists():
        cookies = json.loads(COOKIES_PATH.read_text())
        context.add_cookies(cookies)
        log(f"  🍪 {len(cookies)} cookies Meetup chargés")

def extract_event_urls(html: str) -> list:
    """Extrait les URLs d'events Meetup."""
    # Meetup : /fr-FR/{group-slug}/events/{id}/
    patterns = re.findall(
        r'href=["\']((https://www\.meetup\.com)?/fr-FR/[^"\'?\s]+/events/\d+/?)["\']',
        html
    )
    seen = {}
    for path, base in patterns:
        url = path if path.startswith('http') else f"https://www.meetup.com{path}"
        seen[url.split('?')[0].rstrip('/')] = True
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

    env     = ENVS[args.env]
    city_id = resolve_city_id(args.city, env["base_url"], env["verify_ssl"])
    dry_run = args.dry_run
    log(f"=== meetup_scraper.py — zone={args.zone}" + (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    stats = {"found": 0, "inserted": 0, "skipped": 0, "errors": 0}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
                                    args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context()
        load_cookies(context)
        page = context.new_page()
        apply_stealth(page)

        all_event_urls = []
        for page_num in range(1, args.pages + 1):
            # Meetup utilise le scroll infini — on scroll pour charger plus
            url = ZONES[args.zone]
            if page_num == 1:
                log(f"\nPage initiale : {url}")
                try:
                    page.goto(url, timeout=30000)
                    try:
                        page.wait_for_selector('[data-testid="event-card"], .event-listing', timeout=12000)
                    except:
                        pass
                    sleep_random(*DELAY_PAGES)
                except Exception as e:
                    log(f"  ❌ {e}")
                    break
            else:
                # Scroll pour charger plus d'events
                log(f"\nScroll {page_num}...")
                try:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    sleep_random(2, 4)
                except:
                    pass

            urls = extract_event_urls(page.content())
            new_urls = [u for u in urls if u not in all_event_urls]
            log(f"  → {len(new_urls)} nouvelles URLs")
            if not new_urls and page_num > 1:
                log("  → Plus de nouveaux events, arrêt")
                break
            all_event_urls.extend(new_urls)

        stats["found"] = len(all_event_urls)
        log(f"\n📋 {len(all_event_urls)} URLs uniques")

        if dry_run:
            [log(f"  [DRY] {u}") for u in all_event_urls]
            browser.close()
            return

        for i, event_url in enumerate(all_event_urls, 1):
            parts = event_url.rstrip('/').split('/')
            slug  = f"{parts[-3]}_{parts[-1]}" if len(parts) >= 3 else parts[-1]
            log(f"\n[{i}/{len(all_event_urls)}] {event_url}")
            try:
                page.goto(event_url, timeout=30000)
                try:
                    page.wait_for_selector("h1", timeout=10000)
                except:
                    pass
                sleep_random(*DELAY_EVENTS)
                ok = send_html(page.content(), f"meetup_{slug}.html",
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
