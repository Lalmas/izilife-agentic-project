"""
send_sources.py
---------------
Envoie les fichiers HTML sauvegardés vers postAgentUploadEventSources() d'izilife.
Auth par token statique — pas de session, pas de CSRF.

Usage :
    python send_sources.py --env=local --city=lille
    python send_sources.py --env=staging --city=lille --dry-run

Prérequis :
    pip install requests
    Variables d'environnement : IZILIFE_AGENT_TOKEN
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from datetime import datetime

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

# Token agent — définir avant de lancer :
#   Windows : $env:IZILIFE_AGENT_TOKEN="ton_secret"
#   Linux   : export IZILIFE_AGENT_TOKEN="ton_secret"
AGENT_TOKEN = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()


UPLOAD_PATH = "/scraper/agentUploadEventSources/{city_id}"

SOURCE_PLATFORMS = ["shotgun", "facebook", "helloasso", "eventbrite", "meetup", "billetweb"]

HTML_EXTENSIONS = {".html", ".htm"}

# ─────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def send_file(
    session: requests.Session,
    base_url: str,
    city_id: int,
    file_path: Path,
    verify_ssl: bool,
) -> bool:
    url = base_url + UPLOAD_PATH.format(city_id=city_id)
    try:
        with open(file_path, "rb") as f:
            files = {"sources[]": (file_path.name, f, "text/html")}
            r = session.post(url, files=files, verify=verify_ssl, timeout=30)

        if r.status_code == 200:
            data = r.json()
            log(f"  ✅ {file_path.name} → inserted={data.get('inserted',0)} skipped={data.get('skipped',0)}")
            if data.get('errors'):
                for err in data['errors']:
                    log(f"     ⚠️  {err}")
            return True
        else:
            log(f"  ❌ {file_path.name} → HTTP {r.status_code} : {r.text[:300]}")
            return False
    except Exception as e:
        log(f"  ❌ {file_path.name} → Erreur : {e}")
        return False


def collect_html_files(base_dir: Path) -> list:
    if not base_dir.exists():
        log(f"  ⚠️  Dossier introuvable : {base_dir}")
        return []
    return sorted([f for f in base_dir.iterdir() if f.suffix.lower() in HTML_EXTENSIONS and f.is_file()])


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env",     choices=ENVS.keys(), default="local")
    parser.add_argument("--city",    type=str, required=True)
    parser.add_argument("--dir",     type=str, default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    city_id    = resolve_city_id(args.city, base_url, verify_ssl)
    workspace  = Path(args.dir) if args.dir != "." else local_agent_workspace_root(args.env)
    dry_run    = args.dry_run

    log(f"=== send_sources.py — env={args.env} city={args.city}" + (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI":
        log("❌ IZILIFE_AGENT_TOKEN non défini. Lancer : $env:IZILIFE_AGENT_TOKEN='ton_secret'")
        sys.exit(1)

    all_files = []
    for platform in SOURCE_PLATFORMS:
        folder = event_source_dir(platform, args.city, args.env)
        files = collect_html_files(folder)
        log(f"  {folder} → {len(files)} fichier(s)")
        all_files.extend(files)

    if not all_files:
        log("Aucun fichier HTML trouvé.")
        sys.exit(0)

    log(f"Total : {len(all_files)} fichier(s)")

    if dry_run:
        for f in all_files:
            log(f"  [DRY RUN] {f.name}")
        sys.exit(0)

    session = requests.Session()
    session.headers.update({
        "User-Agent":    "izilife-agent/1.0",
        "X-Agent-Token": AGENT_TOKEN,
    })

    stats = {"ok": 0, "error": 0}
    for file_path in all_files:
        ok = send_file(session, base_url, city_id, file_path, verify_ssl)
        if ok:
            stats["ok"] += 1
        else:
            stats["error"] += 1

    log(f"\n=== Résultat : {stats['ok']} OK / {stats['error']} erreur(s) ===")


if __name__ == "__main__":
    main()