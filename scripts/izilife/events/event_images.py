"""
event_images.py
-------------------
Scanne un dossier local OU Google Drive (synchronisé) et envoie les images
vers postAgentUploadEventImages() d'izilife.

Usage :
    # Dossier local
    python event_images.py --env=local --city=lille --dir="C:/Users/alcamara/Pictures/instagram"

    # Google Drive synchronisé
    python event_images.py --env=local --city=lille --drive="G:/Mon Drive/agentic_workspace/izilife/events/lille-zone/images/instagram/2026-06"

    # Dry run
    python event_images.py --env=local --city=lille --dir="..." --dry-run

Prérequis :
    pip install requests
    Variable : IZILIFE_AGENT_TOKEN
"""

import os
import sys
import hashlib
import argparse
import requests
import time
from datetime import datetime
from pathlib import Path

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

AGENT_TOKEN  = os.environ.get("IZILIFE_AGENT_TOKEN", "METTRE_TOKEN_ICI")
CURRENT_ENV = "prod"

def set_current_env(env_name: str):
    global CURRENT_ENV
    CURRENT_ENV = str(env_name or "prod").lower()

UPLOAD_PATH  = "/scraper/agentUploadEventImages/{city_id}"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Fichier de tracking local des fingerprints déjà envoyés
SENT_LOG = None  # défini via core.paths selon --env

# Dossiers Google Drive par défaut (Windows)
DRIVE_DEFAULTS = []  # géré via core.paths selon --env

# ─────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_sent_fingerprints() -> set:
    sent_log = event_sent_log_file(CURRENT_ENV)
    if not sent_log.exists():
        return set()
    with open(sent_log, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_fingerprint(fingerprint: str):
    sent_log = event_sent_log_file(CURRENT_ENV)
    with open(sent_log, "a") as f:
        f.write(fingerprint + "\n")


def collect_images(folder: Path) -> list:
    if not folder.exists():
        log(f"  ⚠️  Dossier introuvable : {folder}")
        return []
    images = [
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images)


def collect_images_recursive(folder: Path) -> list:
    """Collecte récursivement toutes les images dans un dossier."""
    if not folder.exists():
        log(f"  ⚠️  Dossier introuvable : {folder}")
        return []
    images = [
        f for f in folder.rglob("*")
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images)


def send_image(image_path: Path, base_url: str, city_id: int, verify_ssl: bool) -> bool:
    """Envoie une image vers postAgentUploadEventImages()."""
    url = base_url + UPLOAD_PATH.format(city_id=city_id)

    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".png": "image/png", ".webp": "image/webp", ".gif": "image/gif"}
    mime = mime_map.get(image_path.suffix.lower(), "image/jpeg")

    try:
        with open(image_path, "rb") as f:
            files   = {"images[]": (image_path.name, f, mime)}
            headers = {"X-Agent-Token": AGENT_TOKEN}
            r = requests.post(url, files=files, headers=headers, verify=verify_ssl, timeout=60)

        if r.status_code == 200:
            log(f"  ✅ {image_path.name} → envoyé (HTTP 200)")
            return True
        elif r.status_code in (302, 301):
            log(f"  ✅ {image_path.name} → envoyé (redirect OK)")
            return True
        else:
            log(f"  ❌ {image_path.name} → HTTP {r.status_code} : {r.text[:200]}")
            return False
    except Exception as e:
        log(f"  ❌ {image_path.name} → Erreur : {e}")
        return False


def find_drive_folder() -> Path:
    """Dossier images local/env par défaut."""
    # args.city peut être un slug ou un id; pour auto-détection on utilise le libellé fourni.
    return None


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
    parser = argparse.ArgumentParser(description="Envoie les images Instagram vers izilife OCR")
    parser.add_argument("--env",       choices=ENVS.keys(), default="local")
    parser.add_argument("--city",      type=str, required=True)
    parser.add_argument("--dir",       type=str, default=None, help="Dossier local d'images")
    parser.add_argument("--drive",     type=str, default=None, help="Dossier Google Drive local synchronisé")
    parser.add_argument("--recursive", action="store_true", help="Parcourir récursivement")
    parser.add_argument("--dry-run",   action="store_true")
    args = parser.parse_args()
    set_current_env(args.env)

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    city_id    = resolve_city_id(args.city, base_url, verify_ssl)
    dry_run    = args.dry_run

    log(f"=== event_images.py — env={args.env} city={args.city}" + (" [DRY RUN]" if dry_run else "") + " ===")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    # Déterminer le dossier source
    folder = None

    if args.dir:
        folder = Path(args.dir)
        log(f"Source : dossier local → {folder}")
    elif args.drive:
        folder = Path(args.drive)
        log(f"Source : Google Drive → {folder}")
    else:
        folder = event_download_dir(str(args.city), CURRENT_ENV, downloads=False)
        log(f"Source : dossier images env auto → {folder}")

    # Collecter les images
    if args.recursive:
        images = collect_images_recursive(folder)
    else:
        images = collect_images(folder)

    log(f"Images trouvées : {len(images)}")

    if not images:
        log("Aucune image à traiter.")
        sys.exit(0)

    # Charger les fingerprints déjà envoyés
    sent = load_sent_fingerprints()
    log(f"Fingerprints déjà envoyés : {len(sent)}")

    stats = {"sent": 0, "skipped": 0, "errors": 0}

    for image_path in images:
        fingerprint = sha256_file(image_path)

        if fingerprint in sent:
            log(f"  SKIP {image_path.name} (déjà envoyé)")
            stats["skipped"] += 1
            continue

        size_kb = image_path.stat().st_size // 1024
        log(f"\n  📸 {image_path.name} ({size_kb} Ko)")

        if dry_run:
            log(f"  [DRY RUN] serait envoyé")
            continue

        ok = send_image(image_path, base_url, city_id, verify_ssl)

        if ok:
            save_fingerprint(fingerprint)

            # Déplacer dans loaded/
            loaded_dir = image_path.parent / "loaded"
            loaded_dir.mkdir(exist_ok=True)
            image_path.rename(loaded_dir / image_path.name)
            log(f"  📁 Déplacé dans loaded/")
            
            stats["sent"] += 1
        else:
            stats["errors"] += 1

        time.sleep(2)  # délai entre images

    log(f"\n=== Résultat ===")
    log(f"  Envoyées : {stats['sent']}")
    log(f"  Skippées : {stats['skipped']}")
    log(f"  Erreurs  : {stats['errors']}")


if __name__ == "__main__":
    main()
