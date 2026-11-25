"""
shotgun_scraper.py
------------------
Scrape les events Shotgun Lille avec Playwright et envoie vers izilife.

Usage :
    python shotgun_scraper.py --env=local --city=lille --dry-run
    python shotgun_scraper.py --env=local --city=lille --pages=5

Prérequis :
    pip install playwright requests
    python -m playwright install chromium
    Variable : IZILIFE_AGENT_TOKEN
"""

import os
import sys
import re
import time
import random
import argparse
import requests
import json
import html as html_lib
import unicodedata
import math
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("pip install playwright && python -m playwright install chromium")
    sys.exit(1)

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

AGENT_TOKEN          = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()

UPLOAD_PATH          = "/scraper/agentUploadEventSources/{city_id}"
PENDING_PATH         = "/scraper/agentEventValidatorCandidates"
SHOTGUN_CITY_BASE    = "https://shotgun.live/fr/cities/{city_slug}"
DELAY_BETWEEN_PAGES  = (2, 4)
DELAY_BETWEEN_EVENTS = (3, 6)
CITY_CENTERS = {
    "lille": (50.62925, 3.057256),
}
MAX_CITY_RADIUS_KM = 60.0

# ─────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────

def log(msg: str):
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


def sleep_random(min_s: float, max_s: float):
    time.sleep(random.uniform(min_s, max_s))


def extract_event_urls(html: str) -> list:
    """Extrait les URLs d'events depuis une page listing Shotgun rendue par Playwright."""
    patterns = re.findall(
        r'href=["\'](?:https://shotgun\.live)?(/fr/(events|festivals)/([a-z0-9][a-z0-9\-]{2,80}))["\']',
        html
    )
    seen = {}
    for path, typ, slug in patterns:
        seen[f"https://shotgun.live{path}"] = True
    return list(seen.keys())


def normalize_place_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def extract_event_locations(page_html: str) -> list:
    """Retourne ville et coordonnées des lieux Event/MusicEvent déclarés en JSON-LD."""
    locations = []
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        page_html or "",
        flags=re.I | re.S,
    )

    def visit(value):
        if isinstance(value, dict):
            event_type = str(value.get("@type") or "").lower()
            location = value.get("location") if event_type in {"event", "musicevent"} else None
            if isinstance(location, dict):
                address = location.get("address") if isinstance(location.get("address"), dict) else {}
                geo = location.get("geo") if isinstance(location.get("geo"), dict) else {}
                locality = html_lib.unescape(str(address.get("addressLocality") or "")).strip()
                try:
                    latitude = float(geo.get("latitude"))
                    longitude = float(geo.get("longitude"))
                except (TypeError, ValueError):
                    latitude = longitude = None
                if locality or (latitude is not None and longitude is not None):
                    locations.append({"locality": locality, "latitude": latitude, "longitude": longitude})
            for key, child in value.items():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for block in blocks:
        try:
            visit(json.loads(html_lib.unescape(block).strip()))
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
    unique = {}
    for location in locations:
        key = (location["locality"], location["latitude"], location["longitude"])
        unique[key] = location
    return list(unique.values())


def extract_event_localities(page_html: str) -> list:
    return list(dict.fromkeys(
        location["locality"] for location in extract_event_locations(page_html) if location["locality"]
    ))


def distance_km(first: tuple, second: tuple) -> float:
    lat1, lon1 = map(math.radians, first)
    lat2, lon2 = map(math.radians, second)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    value = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))


def event_matches_city(page_html: str, city_slug: str) -> tuple:
    """Accepte la ville ou sa zone proche; refuse une localisation lointaine explicite."""
    locations = extract_event_locations(page_html)
    localities = [location["locality"] for location in locations if location["locality"]]
    if not locations:
        return True, localities
    expected = normalize_place_name(city_slug)
    if any(normalize_place_name(city) == expected for city in localities):
        return True, localities
    center = CITY_CENTERS.get(expected)
    if center:
        for location in locations:
            if location["latitude"] is None or location["longitude"] is None:
                continue
            if distance_km(center, (location["latitude"], location["longitude"])) <= MAX_CITY_RADIUS_KM:
                return True, localities
    return False, localities


def send_html(html: str, filename: str, base_url: str, city_id: int,
              verify_ssl: bool, source_url: str = "") -> bool:
    """Envoie un HTML vers postAgentUploadEventSources()."""

    url = base_url + UPLOAD_PATH.format(city_id=city_id)

    try:
        files = {
            "sources[]": (
                filename,
                html.encode("utf-8"),
                "text/html"
            )
        }

        headers = {
            "X-Agent-Token": AGENT_TOKEN
        }

        postdata = {
            "source_urls[]": source_url
        } if source_url else {}

        r = requests.post(
            url,
            files=files,
            data=postdata,
            headers=headers,
            verify=verify_ssl,
            timeout=30
        )

        print("\n" + "=" * 80)
        print("POST :", url)
        print("HTTP :", r.status_code)
        print("Content-Type :", r.headers.get("Content-Type"))
        print("=" * 80)
        print(r.text[:5000])
        print("=" * 80 + "\n")

        if r.status_code != 200:
            log(f"❌ HTTP {r.status_code}")
            return False

        try:
            resp = r.json()
        except Exception as e:
            log(f"❌ Réponse non JSON : {e}")
            return False

        inserted = resp.get("inserted", 0)
        skipped = resp.get("skipped", 0)

        log(f"✅ {filename} → inserted={inserted} skipped={skipped}")

        for err in resp.get("errors", []):
            log(f"   ⚠️ {err}")

        return inserted > 0

    except Exception as e:
        log(f"❌ {filename} → Exception : {e}")
        return False


def pending_source_urls(base_url: str, city_id: int, verify_ssl: bool) -> set:
    """Charge les URL déjà présentes dans EventTmp afin d'éviter une réinsertion."""
    try:
        response = requests.post(
            base_url + PENDING_PATH,
            headers={"X-Agent-Token": AGENT_TOKEN, "Content-Type": "application/json"},
            json={"city_id": city_id, "limit": 2000, "include_representations": True},
            verify=verify_ssl,
            timeout=180,
        )
        response.raise_for_status()
        body = response.json()
        if not body.get("success"):
            raise RuntimeError(body.get("error") or "Réponse EventTmp invalide")
        return {
            str(event.get("source_url") or "").strip()
            for event in body.get("events", [])
            if str(event.get("source_url") or "").strip()
        }
    except Exception as exc:
        log(f"  ⚠️ Prélecture EventTmp impossible : {exc}")
        return set()

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env",     choices=ENVS.keys(), default="local")
    parser.add_argument("--city",    type=str, required=True)
    parser.add_argument("--pages",   type=int, default=5)
    parser.add_argument("--max-events", type=int, default=0, help="Nombre maximal d'événements à traiter. 0 = illimité.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--headful", action="store_true", help="Affiche Chromium (headless par défaut).")
    args = parser.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    city_id    = resolve_city_id(args.city, base_url, verify_ssl)
    dry_run    = args.dry_run

    log(f"=== shotgun_scraper.py — env={args.env} city={args.city} pages={args.pages}" + (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    stats = {"found": 0, "inserted": 0, "skipped": 0, "errors": 0}
    known_tmp_urls = pending_source_urls(base_url, city_id, verify_ssl) if not dry_run else set()
    log(f"EventTmp déjà connus par URL : {len(known_tmp_urls)}")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=not args.headful,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

        # ── Phase 1 : Listing ─────────────────────────────────────
        all_event_urls = []

        for page_num in range(1, args.pages + 1):
            listing_url = f"{SHOTGUN_CITY_BASE.format(city_slug=args.city)}?page={page_num}"
            log(f"\nPage listing {page_num}/{args.pages} : {listing_url}")

            try:
                page.goto(listing_url, timeout=30000)
                try:
                    page.wait_for_selector('a[href*="/fr/events/"], a[href*="/fr/festivals/"]', timeout=15000)
                except:
                    pass
                sleep_random(*DELAY_BETWEEN_PAGES)

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

        # Dédupliquer
        all_event_urls = list(dict.fromkeys(all_event_urls))
        if args.max_events > 0: all_event_urls = all_event_urls[:args.max_events]
        stats["found"] = len(all_event_urls)
        log(f"\n📋 Total URLs uniques : {len(all_event_urls)}")

        if dry_run:
            for u in all_event_urls:
                log(f"  [DRY RUN] {u}")
            browser.close()
            return

        # ── Phase 2 : Visiter chaque event ───────────────────────
        for i, event_url in enumerate(all_event_urls, 1):
            slug     = event_url.split("/")[-1]
            filename = f"shotgun_{slug}.html"

            log(f"\n[{i}/{len(all_event_urls)}] {event_url}")

            if event_url in known_tmp_urls:
                log("  ⏭️  URL déjà présente dans EventTmp")
                stats["skipped"] += 1
                continue

            try:
                page.goto(event_url, timeout=30000)
                try:
                    page.wait_for_selector("h1", timeout=15000)
                except:
                    pass
                sleep_random(*DELAY_BETWEEN_EVENTS)

                html = page.content()
                city_ok, localities = event_matches_city(html, args.city)
                if not city_ok:
                    log(f"  ⏭️  Hors {args.city} : villes déclarées={localities}")
                    stats["skipped"] += 1
                    continue
                ok   = send_html(html, filename, base_url, city_id, verify_ssl, source_url=event_url)

                if ok:
                    stats["inserted"] += 1
                    known_tmp_urls.add(event_url)
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
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("shotgun_events", "events", main)
