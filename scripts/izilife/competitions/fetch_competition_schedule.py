"""
fetch_competition_schedule.py
-----------------------------
Récupère le HTML d'une page de programme sportif avec Playwright
et l'envoie vers postImportCompetitionSchedule() de izilife.

Usage :
    python fetch_competition_schedule.py --edition=1 --env=local
    python fetch_competition_schedule.py --edition=1 --env=local --dry-run
    python fetch_competition_schedule.py --edition=1 --env=staging

Prérequis :
    pip install playwright requests
    python -m playwright install chromium
    Variable : IZILIFE_AGENT_TOKEN
"""

import os
import sys
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("pip install playwright && python -m playwright install chromium")
    sys.exit(1)

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
ENVS = {
    "local":   {"base_url": "https://localhost:4443/izilife-admin", "verify_ssl": False},
    "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify_ssl": True},
    "prod":    {"base_url": "https://www.izilife.co/izilife-admin", "verify_ssl": True},
}

AGENT_TOKEN = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()


# ─────────────────────────────────────────────
def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def fetch_html_with_playwright(url: str) -> str:
    """Ouvre la page avec Playwright et retourne le HTML rendu."""
    log(f"Playwright → {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

        page.set_extra_http_headers({
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            # Si networkidle timeout, on prend quand même ce qu'on a
            pass

        # Attendre un peu que le JS charge le contenu
        time.sleep(3)

        # Scroll pour forcer le lazy-load
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

        html = page.content()
        browser.close()
        log(f"HTML récupéré : {len(html)} caractères")
        return html

def send_html_to_izilife(html: str, edition_id: int, base_url: str, verify_ssl: bool) -> dict:
    """Envoie le HTML vers postImportCompetitionScheduleFromAgent()."""
    url = f"{base_url}/scraper/importCompetitionScheduleFromAgent/{edition_id}"
    try:
        r = requests.post(
            url,
            data={"html": html},
            headers={"X-Agent-Token": AGENT_TOKEN},
            verify=verify_ssl,
            timeout=120,
        )
        if r.status_code == 200:
            return r.json()
        else:
            return {"success": False, "error": f"HTTP {r.status_code} : {r.text[:300]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--edition", type=int, required=True, help="ID de l'édition CompetitionEdition")
    parser.add_argument("--env", choices=ENVS.keys(), default="local")
    parser.add_argument("--dry-run", action="store_true", help="Fetch HTML mais ne pas envoyer")
    parser.add_argument("--url", type=str, default=None, help="Override URL source (sinon prise depuis la BDD via l'API)")
    args = parser.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]

    log(f"=== fetch_competition_schedule.py — env={args.env} edition={args.edition}" + (" [DRY RUN]" if args.dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not args.dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    # Récupérer l'URL source depuis l'API izilife (ou override CLI)
    source_url = args.url
    if not source_url:
        info_url = f"{base_url}/scraper/editionSourceUrl/{args.edition}"
        try:
            r = requests.get(
                info_url,
                headers={"X-Agent-Token": AGENT_TOKEN},
                verify=verify_ssl,
                timeout=15,
            )
            if r.status_code == 200:
                data = r.json()
                source_url = data.get("source_url")
            else:
                log(f"❌ Impossible de récupérer l'URL source (HTTP {r.status_code})")
                sys.exit(1)
        except Exception as e:
            log(f"❌ Erreur récupération URL : {e}")
            sys.exit(1)

    if not source_url:
        log("❌ Aucune URL source configurée pour cette édition.")
        sys.exit(1)

    log(f"URL source : {source_url}")

    # Fetch avec Playwright
    html = fetch_html_with_playwright(source_url)

    if len(html) < 500:
        log("❌ HTML trop court — page probablement vide ou bloquée.")
        sys.exit(1)

    if args.dry_run:
        log(f"[DRY RUN] HTML récupéré ({len(html)} chars) — pas d'envoi.")
        log(f"Aperçu : {html[:500]}")
        return

    # Envoyer vers izilife
    log("Envoi vers izilife...")
    result = send_html_to_izilife(html, args.edition, base_url, verify_ssl)

    if result.get("success"):
        log(f"✅ {result.get('inserted', 0)} match(s) importé(s), {result.get('skipped', 0)} ignoré(s)")
    else:
        log(f"❌ Erreur : {result.get('error', 'inconnue')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
