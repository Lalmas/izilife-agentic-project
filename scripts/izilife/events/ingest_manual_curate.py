"""
ingest_manual_curate.py
-----------------------
Curation manuelle — lit curate_events.xlsx depuis Google Drive par zone
et dispatche vers le bon handler selon l'onglet.

Onglets Excel : Facebook | Shotgun | HelloAsso | Eventbrite | Meetup | Instagram

Colonnes : url | status | target_type | target_string_id | organizer_is_location |
           organizer_type | organizer_string_id | description | start_date | start_hour |
           end_date | end_hour | event_category_ref | ticketing_url |
           is_free_event | auto_validate | notes | added_at | processed_at
Status   : pending → done | error | skip

Usage :
    python ingest_manual_curate.py --zone=lille --env=local --city=lille --dry-run
    python ingest_manual_curate.py --zone=lille --env=local --city=lille
    python ingest_manual_curate.py --zone=lille --env=local --city=lille --sheet=Facebook
    python ingest_manual_curate.py --zone=lille --env=local --city=lille --init

Prérequis :
    pip install playwright requests playwright-stealth openpyxl
    python -m playwright install chromium
    Variable : IZILIFE_AGENT_TOKEN
"""

import os
import sys

import re
import json
import hashlib
import time
import random
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
# Credentials must be provided by the shell/process environment. Do not load
# local .env files here: manual curation is also used in staging/prod runs.

try:
    import openpyxl
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    print("pip install openpyxl")
    sys.exit(1)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

try:
    from playwright_stealth import stealth_sync
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False

# ─────────────────────────────────────────────
# CHEMINS — cross-platform Windows / Linux
# ─────────────────────────────────────────────

def get_drive_root() -> Path:
    value = os.environ.get("AGENTIC_DRIVE_ROOT", "").strip()
    if not value:
        raise RuntimeError("AGENTIC_DRIVE_ROOT non défini.")
    return Path(value).expanduser()
    # Ancienne détection conservée temporairement mais désormais inaccessible.
    """Retourne la racine Google Drive selon l'OS."""
    if sys.platform == "win32":
        # Google Drive for Desktop sur Windows
        candidates = [
            Path(value),
            Path.home() / "Google Drive",
            Path.home() / "Mon Drive",
        ]
    else:
        # Linux / Mac
        candidates = [
            Path.home() / "GoogleDrive",
            Path.home() / "Google Drive",
            Path.home() / "gdrive",
            Path(value),
        ]

    for p in candidates:
        if p.exists():
            return p

    # Fallback — dossier local si Drive pas trouvé
    fallback = Path(__file__).parent.parent.parent.parent / "izilife-agent-workspace" / "curate"
    fallback.mkdir(parents=True, exist_ok=True)
    print(f"⚠️  Google Drive non trouvé — fallback local : {fallback}")
    return fallback


def get_curate_file(zone: str) -> Path:
    """Retourne le chemin du fichier Excel pour une zone/env."""
    canonical = event_curate_file(zone, CURRENT_ENV)
    if canonical.exists():
        return canonical
    macro_enabled = canonical.with_suffix(".xlsm")
    return macro_enabled if macro_enabled.exists() else canonical


def get_download_dir(zone: str) -> Path:
    """Retourne l'ancien dossier de téléchargement intermédiaire."""
    return event_download_dir(zone, CURRENT_ENV, downloads=True)


def get_image_dir(zone: str) -> Path:
    """
    Retourne directement le dossier racine des images de la zone.
    Exemple : images/lille-zone/
    """
    return event_download_dir(zone, CURRENT_ENV, downloads=False)


def get_cookies_path(platform: str) -> Path:
    """Retourne le chemin des cookies pour une plateforme."""
    scripts_dir = Path(__file__).parent
    return scripts_dir / "profiles" / platform / f"{platform}_cookies.json"


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
    from izilife.events.local_event_ocr import complete_missing_fields, estimated_end_hour, extract_event_fields, extract_title_candidate, infer_event_category, is_strong_title
    from core.location_identity import resolve_location
except Exception:
    def normalize_zone(zone: str) -> str:
        zone = str(zone or "").strip().lower()
        return zone if zone.endswith("-zone") else f"{zone}-zone"
    ENVS = {
        "local":   {"base_url": "https://localhost:4443/izilife-admin",          "verify_ssl": False},
        "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify_ssl": True},
        "prod":    {"base_url": "https://www.izilife.co/izilife-admin",          "verify_ssl": True},
    }
    from izilife.events.local_event_ocr import complete_missing_fields, estimated_end_hour, extract_event_fields, extract_title_candidate, infer_event_category, is_strong_title
    from core.location_identity import resolve_location
    def local_agent_workspace_root(env_name="prod"):
        suffix = {"local":"-local", "staging":"-staging", "prod":""}.get(env_name, "")
        return Path.home() / "Documents" / "agentic_Workspace" / "izilife" / f"izilife-agent-workspace{suffix}"
    def workspace_root(env_name="prod"):
        folder = {"local":"agentic_workspace_local", "staging":"agentic_workspace_staging", "prod":"agentic_workspace"}.get(env_name, "agentic_workspace")
        return get_drive_root() / folder
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

FB_EMAIL    = os.environ.get("FB_EMAIL", "")
FB_PASSWORD = os.environ.get("FB_PASSWORD", "")
UPLOAD_PATH = "/scraper/agentUploadEventSources/{city_id}"
IMAGE_PATH  = "/scraper/agentUploadEventImages/{city_id}"

WAIT_SELECTORS = {
    "shotgun.live":   "h1",
    "helloasso.com":  "h1",
    "billetweb.fr":   "h1",
    "eventbrite.fr":  '[data-testid="event-title"], h1',
    "meetup.com":     "h1",
    "facebook.com":   "h1",
    "weezevent.com":  "h1",
    "festik.net":     "h1",
}

FB_LOGIN_URL = "https://www.facebook.com/login"

IGRAM_SITES = [
    {
        "name": "igram.world",
        "url": "https://igram.world/fr1/",
        "input_sel": "input[type='text']",
        "result_timeout": 90000,
    },
    {
        "name": "snapinsta.app",
        "url": "https://snapinsta.app/fr",
        "input_sel": "input[type='text']",
        "btn_sel": "button[type='submit']",
        "wait_sel": "a[href*='.jpg'], a[download]",
        "result_timeout": 30000,
    },
    {
        "name": "instafinsta.com",
        "url": "https://instafinsta.com",
        "input_sel": "input[name='url'], input[type='text']",
        "btn_sel": "button[type='submit']",
        "wait_sel": "a[download], a[href*='.jpg']",
        "result_timeout": 30000,
    },
]

SHEET_HANDLERS = {
    "Facebook":   "html",
    "Shotgun":    "html",
    "HelloAsso":  "html",
    "Eventbrite": "html",
    "Meetup":     "html",
    "Instagram":  "instagram",
}

DELAY = (2, 5)

# ─────────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────────

def log(msg: str):
    line=f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    try:print(line)
    except UnicodeEncodeError:print(line.encode(sys.stdout.encoding or "utf-8","replace").decode(sys.stdout.encoding or "utf-8"))


def sleep_random(mn=2, mx=5):
    time.sleep(random.uniform(mn, mx))


def apply_stealth(page):
    if HAS_STEALTH:
        stealth_sync(page)
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['fr-FR', 'fr']});
        window.chrome = { runtime: {} };
    """)


def detect_domain(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www.", "")


def load_cookies(context, platform: str):
    path = get_cookies_path(platform)
    if path.exists():
        cookies = json.loads(path.read_text())
        valid   = [c for c in cookies if c.get("name") and c.get("value")]
        context.add_cookies(valid)
        log(f"  🍪 {len(valid)} cookies chargés ({platform})")
    else:
        log(f"  ⚠️  Cookies non trouvés : {path}")


MANUAL_EVENT_FIELDS = (
    "title", "description", "target_type", "target_string_id",
    "organizer_is_location", "organizer_type", "organizer_string_id",
    "start_date", "start_hour", "end_date", "end_hour",
    "event_category_ref", "principal_activity_category_string_id",
    "sport_string_id", "dance_string_id", "music_style_string_id",
    "artisan_technique_string_id", "hobbies", "objects", "music_styles", "dances",
    "sports", "tags", "principal_characteristics", "ticketing_url", "access_type_string_id",
    "access_booking_string_id", "basic_price", "is_free_event",
    "auto_validate", "source_account", "source_name", "location_name",
    "venue_name", "venue_url", "location_url", "instagram_url", "facebook_url",
    "instagram_content_mode",
)


def event_is_past(row: dict, today=None) -> bool:
    """Ignore une fiche dont la dernière date explicite est déjà passée."""
    today = today or datetime.now().date()
    value = row.get("end_date") or row.get("start_date")
    if not value:
        return False
    if hasattr(value, "date") and not isinstance(value, str):
        value = value.date() if hasattr(value, "hour") else value
    if isinstance(value, str):
        try:
            value = datetime.strptime(value[:10], "%Y-%m-%d").date()
        except ValueError:
            return False
    return value < today


def deterministic_description(row: dict) -> str:
    title = str(row.get("title") or "").strip()
    date = excel_value(row.get("start_date"))
    start = excel_value(row.get("start_hour"))
    end = excel_value(row.get("end_hour"))
    venue = str(row.get("target_string_id") or "").replace("-", " ").strip()
    if not title or not date:
        return ""
    schedule = f" le {date}"
    if start:
        schedule += f" à {start}" if not end else f" de {start} à {end}"
    location = f" à {venue}" if venue else ""
    return f"{title}{schedule}{location}."


def inferred_end_date(start_date, start_hour, end_hour):
    """Une fin après minuit appartient au lendemain."""
    if not start_date or not end_hour:
        return start_date
    try:
        base = start_date.date() if hasattr(start_date, "hour") else start_date
        if isinstance(base, str):
            base = datetime.strptime(base[:10], "%Y-%m-%d").date()
        start_minutes = None
        if start_hour:
            sh, sm = map(int, str(start_hour)[:5].split(":"))
            start_minutes = sh * 60 + sm
        eh, em = map(int, str(end_hour)[:5].split(":"))
        if start_minutes is not None and eh * 60 + em <= start_minutes:
            base += timedelta(days=1)
        return base.isoformat()
    except (TypeError, ValueError):
        return start_date


def excel_value(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    if hasattr(value, 'hour') and hasattr(value, 'minute'):
        return value.strftime('%H:%M')
    if hasattr(value, 'strftime'):
        return value.strftime('%Y-%m-%d')
    text = str(value or "").strip()
    if text.lower() in {'oui', 'yes', 'vrai', 'true', '1'}:
        return 'true'
    if text.lower() in {'non', 'no', 'faux', 'false', '0'}:
        return 'false'
    return text


def manual_event_payload(row: dict | None, source_url: str,
                         image_path: Path | None = None) -> dict:
    row = dict(row or {})
    if row.get("start_hour") and not row.get("end_hour"):
        row["end_hour"] = estimated_end_hour(row["start_hour"])
        row["end_hour_is_estimated"] = True
    if row.get("start_date") and row.get("end_hour") and not row.get("end_date"):
        row["end_date"] = inferred_end_date(row["start_date"], row.get("start_hour"), row["end_hour"])
    if image_path is not None:
        core_complete = all(str(row.get(key) or "").strip() for key in
                            ("title", "description", "start_date",
                             "event_category_ref", "target_string_id"))
        if core_complete:
            row["local_ocr_status"] = "skipped_manual_core_complete"
            log("  ℹ️ OCR local inutile : noyau éditorial déjà fourni")
        else:
            row = complete_missing_fields(row, image_path)
            if row.get("local_ocr_status") == "completed":
                log("  ✅ OCR local : date/horaires non ambigus ajoutés avant envoi")
            elif row.get("local_ocr_status") == "ambiguous":
                log(f"  ℹ️ OCR local ambigu ({row.get('local_ocr_reasons')}), aucune supposition")
    payload = {key: excel_value(row.get(key)) for key in MANUAL_EVENT_FIELDS}
    line_ai_choice = str(row.get("use_llm_if_missing") or "").strip().lower()
    # Pour curate_events, Luna est autorisé par défaut dès que le noyau manque.
    # Une valeur explicite non/false/0 conserve toutefois un coupe-circuit local.
    payload["manual_ai_request"] = line_ai_choice not in {"non", "no", "false", "faux", "0"}
    payload = {key: value for key, value in payload.items() if value != ""}
    payload["source_url"] = source_url
    return payload


def send_html(html: str, filename: str, base_url: str, city_id: int,
              verify_ssl: bool, source_url: str, row: dict | None = None) -> bool:
    if event_is_past(row or {}):
        log("  ℹ️ Date explicite passée : source ignorée avant envoi")
        return True
    url = base_url + UPLOAD_PATH.format(city_id=city_id)
    try:
        r = requests.post(
            url,
            files={"sources[]": (filename, html.encode("utf-8"), "text/html")},
            data={
                "source_urls[]": source_url,
                "manual_event_json": json.dumps(
                    manual_event_payload(row, source_url), ensure_ascii=False
                ),
            },
            headers={"X-Agent-Token": AGENT_TOKEN},
            verify=verify_ssl, timeout=30
        )
        if r.status_code == 200:
            resp = r.json()
            log(f"  ✅ inserted={resp.get('inserted',0)} skipped={resp.get('skipped',0)}")
            return True
        log(f"  ❌ HTTP {r.status_code} : {r.text[:200]}")
        return False
    except Exception as e:
        log(f"  ❌ Erreur envoi : {e}")
        return False


def send_image(image_path: Path, base_url: str, city_id: int, verify_ssl: bool,
               row: dict | None = None, source_url: str = "",
               allow_image_only_tmp: bool = False) -> bool:
    if event_is_past(row or {}):
        log("  ℹ️ Date explicite passée : image ignorée avant envoi")
        return True
    url  = base_url + IMAGE_PATH.format(city_id=city_id)
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png",  "webp": "image/webp"}.get(
                image_path.suffix.lstrip(".").lower(), "image/jpeg")
    row = row or {}
    data = manual_event_payload(row, source_url, image_path)
    # Ne jamais transformer arbitrairement la premiere phrase promotionnelle
    # en titre. Si Excel ne fournit pas le titre, l'unique analyse initiale
    # Luna reçoit l'image et le contexte pour le déterminer.
    # Une ligne ajoutée manuellement au classeur constitue une demande
    # d'insertion. La validation automatique est donc active par défaut ;
    # l'utilisateur peut toujours la désactiver explicitement avec « non ».
    if not str(row.get("auto_validate") or "").strip():
        data["auto_validate"] = "true"
    if allow_image_only_tmp:
        # Une première image réellement téléchargée ne doit jamais être perdue
        # lorsque l'OCR/LLM ne parvient pas à en extraire un événement. Le BO
        # créera alors un EventTmp incomplet avec son local_image_path.
        data["allow_image_only_tmp"] = "true"
    try:
        with open(image_path, "rb") as f:
            r = requests.post(url,
                              files={"images[]": (image_path.name, f, mime)},
                              data=data, headers={"X-Agent-Token": AGENT_TOKEN},
                              verify=verify_ssl, timeout=60)
        if r.status_code == 200:
            payload = r.json()
            diagnostics = payload.get("diagnostics") or []
            for diagnostic in diagnostics:
                if diagnostic.get("auto_validated"):
                    log(f"  ✅ LocalEvent #{diagnostic.get('local_event_id')} créé et activé")
                else:
                    log(f"  ℹ️ TMP #{diagnostic.get('tmp_id')} conservé : {diagnostic.get('reason')}")
            if payload.get("errors"):
                log(f"  ❌ OCR : {payload['errors']}")
                return False
            log("  ✅ Image originale envoyée avec les champs OCR locaux")
            return bool(payload.get("inserted") or payload.get("skipped"))
        log(f"  ❌ HTTP {r.status_code} : {r.text[:150]}")
        return False
    except Exception as e:
        log(f"  ❌ Erreur envoi image : {e}")
        return False


def send_event_flyers(image_paths: list[Path], base_url: str, city_id: int,
                      verify_ssl: bool, row: dict, source_url: str) -> bool:
    """Envoie plusieurs flyers comme médias d'un seul Event."""
    if not image_paths:
        return False
    data = manual_event_payload(row, source_url, image_paths[0])
    data["auto_validate"] = data.get("auto_validate") or "true"
    data["single_event_media_group"] = "true"
    handles = []
    try:
        files = []
        for path in image_paths:
            handle = open(path, "rb")
            handles.append(handle)
            mime = {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png","webp":"image/webp"}.get(path.suffix.lstrip(".").lower(),"image/jpeg")
            files.append(("images[]", (path.name, handle, mime)))
        response = requests.post(base_url + IMAGE_PATH.format(city_id=city_id), files=files,
                                 data=data, headers={"X-Agent-Token": AGENT_TOKEN},
                                 verify=verify_ssl, timeout=120)
        if response.status_code == 200:
            log(f"  ✅ {len(image_paths)} flyer(s) rattaché(s) au même Event")
            return True
        log(f"  ❌ HTTP {response.status_code} : {response.text[:300]}")
        return False
    finally:
        for handle in handles:
            handle.close()


def selected_event_flyers(local_files: list[Path], row: dict) -> list[Path]:
    """Sélection des médias d'un carrousel ordinaire (un seul Event)."""
    raw = str(row.get("img_index") or row.get("included_img_indexes") or "").strip()
    indexes = [int(value) for value in re.findall(r"\d+", raw)] or [1]
    excluded = {int(value) for value in re.findall(r"\d+", str(row.get("excluded_img_indexes") or ""))}
    return [local_files[index-1] for index in indexes
            if 1 <= index <= len(local_files) and index not in excluded]


def carousel_event_rows(local_files: list[Path], row: dict) -> list[tuple[Path, dict]]:
    """Sépare seulement les carrousels où chaque flyer décrit un Event autonome."""
    requested_index = str(row.get("img_index") or row.get("image_index") or "").strip()
    if requested_index:
        try:
            index = int(requested_index)
        except ValueError:
            log(f"  ❌ img_index invalide : {requested_index}")
            return []
        if index < 1 or index > len(local_files):
            log(f"  ❌ img_index {index} hors carrousel (1..{len(local_files)})")
            return []
        if event_is_past(row):
            log("  ℹ️ Événement daté passé : slide ignorée")
            return []
        log(f"  ✅ Carrousel manuel : slide {index}/{len(local_files)} sélectionnée")
        return [(local_files[index - 1], dict(row))]
    if len(local_files) <= 1:
        return [(local_files[0], row)] if local_files and not event_is_past(row) else []
    event_specific = {"title", "description", "start_date", "start_hour", "end_date", "end_hour"}
    candidates = []
    included = {int(value) for value in re.findall(r"\d+", str(row.get("included_img_indexes") or ""))}
    excluded = {int(value) for value in re.findall(r"\d+", str(row.get("excluded_img_indexes") or row.get("ignored_img_indexes") or ""))}
    planning_mode = str(row.get("instagram_content_mode") or "").strip().upper() == "PLANNING_INSTAGRAM"
    # Mode sûr par défaut : une publication Instagram contenant plusieurs
    # médias ne doit pas déclencher l'OCR ni la création de plusieurs Events
    # sans demande explicite. img_index sélectionne une slide (traité plus
    # haut) ; included_img_indexes est le seul opt-in pour plusieurs slides.
    if not included and not (planning_mode and excluded):
        if event_is_past(row):
            log("  ℹ️ Événement daté passé : première slide ignorée")
            return []
        first = dict(row)
        first["img_index"] = 1
        first["detected_img_indexes"] = "1"
        log(f"  ℹ️ Carrousel de {len(local_files)} médias : première slide seulement (mode sûr)")
        return [(local_files[0], first)]
    detected = []
    for slide_index, path in enumerate(local_files, start=1):
        if (included and slide_index not in included) or slide_index in excluded:
            continue
        base = {key: value for key, value in row.items() if key not in event_specific}
        parsed = complete_missing_fields(base, path)
        if (parsed.get("local_ocr_status") == "completed" and parsed.get("start_date")
                and parsed.get("title") and not event_is_past(parsed)):
            parsed["img_index"] = slide_index
            candidates.append((path, parsed))
            detected.append(slide_index)
    row["detected_img_indexes"] = ",".join(map(str, detected))
    if candidates:
        log(f"  ✅ Carrousel : {len(candidates)} flyer(s) Event autonome(s), couvertures/agendas ignorés")
        return candidates
    # Carrousel illustrant une seule fiche manuelle : une seule création, jamais
    # une fiche dupliquée par image. Le premier média original suffit ici.
    if row.get("title") and row.get("start_date"):
        log("  ℹ️ Carrousel mono-Event : une seule création depuis le premier média")
        return [(local_files[0], row)]
    # Même si les diapositives ne permettent pas d'identifier un événement
    # automatiquement, ne perdons pas un média réellement téléchargé. Une
    # seule image est envoyée au BO comme EventTmp incomplet ; l'utilisateur
    # peut alors renseigner le titre dans le modal de validation. Les autres
    # diapositives ne sont pas envoyées afin de ne créer aucun doublon.
    fallback = dict(row)
    fallback["local_ocr_status"] = "ambiguous_carousel_manual_review"
    fallback["detected_img_indexes"] = ""
    log("  ℹ️ Carrousel ambigu : première image conservée pour validation manuelle")
    return [(local_files[0], fallback)]


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


# ─────────────────────────────────────────────
# EXCEL
# ─────────────────────────────────────────────

def read_pending_rows(sheet) -> list:
    headers = [str(c.value).strip().lower() if c.value else "" for c in sheet[1]]
    rows    = []
    for row_idx, row in enumerate(sheet.iter_rows(min_row=2), start=2):
        values = {headers[i]: (cell.value or "") for i, cell in enumerate(row) if i < len(headers)}
        status = str(values.get("status", "")).strip().lower()
        url    = str(values.get("url", "")).strip()
        if status == "pending" and url.startswith("http"):
            values["row_idx"] = row_idx
            values["url"] = url
            rows.append(values)
    return rows


def ensure_curate_columns(workbook) -> bool:
    """Ajoute les champs de curation sans déplacer ni réécrire les colonnes existantes."""
    required = [
        "target_type", "target_string_id", "organizer_is_location", "organizer_type",
        "organizer_string_id", "description", "start_date", "start_hour", "end_date",
        "end_hour", "event_category_ref", "principal_activity_category_string_id",
        "sport_string_id", "dance_string_id", "music_style_string_id",
        "artisan_technique_string_id", "hobbies", "objects", "music_styles", "dances",
        "sports", "tags", "principal_characteristics",
        "ticketing_url", "access_type_string_id", "access_booking_string_id", "basic_price",
        "is_free_event", "auto_validate", "title", "source_account", "source_name",
        "location_name", "venue_name", "venue_url", "location_url", "instagram_url",
        "facebook_url", "img_index",
        "included_img_indexes", "excluded_img_indexes", "detected_img_indexes",
        "inspection_result", "use_llm_if_missing",
    ]
    changed = False
    for sheet_name in SHEET_HANDLERS:
        if sheet_name not in workbook.sheetnames:
            continue
        sheet = workbook[sheet_name]
        headers = [str(cell.value or "").strip().lower() for cell in sheet[1]]
        if sheet_name == "Instagram" and "instagram_content_mode" not in headers:
            # Colonne métier visible immédiatement après l'URL. Les cellules
            # restent vides : vide = publication Instagram normale.
            url_index = headers.index("url") if "url" in headers else 0
            sheet.insert_cols(url_index + 2)
            sheet.cell(row=1, column=url_index + 2).value = "instagram_content_mode"
            headers.insert(url_index + 1, "instagram_content_mode")
            changed = True
        if "image_index" in headers and "img_index" not in headers:
            legacy_index = headers.index("image_index")
            sheet.cell(row=1, column=legacy_index + 1).value = "img_index"
            headers[legacy_index] = "img_index"
            changed = True
        if "ignored_img_indexes" in headers and "excluded_img_indexes" not in headers:
            legacy_index = headers.index("ignored_img_indexes")
            sheet.cell(row=1, column=legacy_index + 1).value = "excluded_img_indexes"
            headers[legacy_index] = "excluded_img_indexes"
            changed = True
        for header in required:
            if header not in headers:
                sheet.cell(row=1, column=sheet.max_column + 1).value = header
                headers.append(header)
                changed = True
    return changed


def configure_curate_selectors(workbook) -> None:
    """Sélecteurs et formats conservés dans Excel/Google Sheets."""
    lists = {
        'status': '"pending,split,done,error,skip"',
        'target_type': '"PLACE,SHOP,EQUIPMENT"',
        'organizer_is_location': '"oui,non"',
        'organizer_type': '"PAGE,PARTNER"',
        'is_free_event': '"oui,non"',
        'auto_validate': '"oui,non"',
        'use_llm_if_missing': '"non,oui"',
    }
    for sheet_name in SHEET_HANDLERS:
        if sheet_name not in workbook.sheetnames:
            continue
        ws = workbook[sheet_name]
        headers = {str(c.value or '').strip().lower(): c.column_letter for c in ws[1]}
        # Évite d'empiler les mêmes validations à chaque passage de la cron.
        ws.data_validations.dataValidation = []
        for name, formula in lists.items():
            if name not in headers:
                continue
            validation = DataValidation(type='list', formula1=formula, allow_blank=True)
            validation.error = 'Choisir une valeur dans la liste.'
            validation.errorTitle = 'Valeur invalide'
            ws.add_data_validation(validation)
            validation.add(f'{headers[name]}2:{headers[name]}1000')
        for name, fmt in [('start_date', 'dd/mm/yyyy'), ('end_date', 'dd/mm/yyyy'),
                          ('start_hour', 'hh:mm'), ('end_hour', 'hh:mm')]:
            if name not in headers:
                continue
            column = headers[name]
            for row in range(2, 1001):
                ws[f'{column}{row}'].number_format = fmt


def update_row(sheet, row_idx: int, status: str):
    headers = [str(c.value).strip().lower() if c.value else "" for c in sheet[1]]
    try:
        status_col    = headers.index("status") + 1
        processed_col = headers.index("processed_at") + 1
        sheet.cell(row=row_idx, column=status_col).value     = status
        sheet.cell(row=row_idx, column=processed_col).value  = datetime.now().strftime('%Y-%m-%d %H:%M')
    except ValueError:
        pass


def create_excel_template(zone: str):
    curate_file = get_curate_file(zone)
    curate_file.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    headers  = [
        "url", "instagram_content_mode", "status", "notes", "added_at", "processed_at", "target_type",
        "target_string_id", "organizer_is_location", "organizer_type", "organizer_string_id",
        "title", "description", "start_date", "start_hour", "end_date", "end_hour",
        "event_category_ref", "ticketing_url", "is_free_event", "auto_validate",
        "principal_activity_category_string_id", "sport_string_id", "dance_string_id",
        "music_style_string_id", "artisan_technique_string_id", "hobbies", "objects",
        "music_styles", "dances", "sports", "tags", "principal_characteristics",
        "access_type_string_id", "access_booking_string_id", "basic_price", "source_account",
        "source_name", "location_name", "venue_name", "venue_url", "location_url",
        "instagram_url", "facebook_url",
        "img_index", "included_img_indexes", "excluded_img_indexes",
        "detected_img_indexes", "inspection_result", "use_llm_if_missing",
    ]
    examples = {
        "Facebook":   "https://www.facebook.com/events/123456789",
        "Shotgun":    "https://shotgun.live/fr/events/mon-event",
        "HelloAsso":  "https://www.helloasso.com/associations/asso/evenements/event",
        "Eventbrite": "https://www.eventbrite.fr/e/mon-event-123456",
        "Meetup":     "https://www.meetup.com/fr-FR/groupe/events/123456789/",
        "Instagram":  "https://www.instagram.com/p/ABC123DEF/",
    }

    for sheet_name in SHEET_HANDLERS.keys():
        ws = wb.create_sheet(sheet_name)
        ws.append(headers)
        example = {header: "" for header in headers}
        example.update({"url": examples.get(sheet_name, ""), "status": "pending", "notes": "exemple", "added_at": datetime.now().strftime('%Y-%m-%d')})
        ws.append([example[header] for header in headers])
        ws.column_dimensions['A'].width = 70
        ws.column_dimensions['B'].width = 12
        ws.column_dimensions['C'].width = 28
        ws.column_dimensions['D'].width = 70

    configure_curate_selectors(wb)
    wb.save(curate_file)
    log(f"✅ Fichier créé : {curate_file}")


# ─────────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────────

def login_facebook(page) -> bool:
    """Login automatique Facebook depuis .env."""
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
        if "login" not in page.url and "checkpoint" not in page.url:
            log("✅ Login auto réussi")
            return True
        log("⚠️  Login auto échoué (2FA ou erreur)")
        return False
    except Exception as e:
        log(f"  ❌ Erreur login : {e}")
        return False


def handle_html(page, row: dict, base_url: str, city_id: int,
                verify_ssl: bool, dry_run: bool) -> bool:
    url      = row["url"]
    domain   = detect_domain(url)
    wait_sel = next((v for k, v in WAIT_SELECTORS.items() if k in domain), "h1")

    log(f"  [{domain}] {url}")

    if dry_run:
        log(f"  [DRY RUN] serait envoyé")
        return True

    try:
        page.goto(url, timeout=30000)
        try:
            page.wait_for_selector(wait_sel, timeout=12000)
        except:
            pass
        sleep_random(2, 5)

        html     = page.content()
        slug     = re.sub(r'[^a-z0-9\-]', '-', url.split('/')[-1].lower())[:50] or "event"
        prefix   = domain.split('.')[0]
        filename = f"{prefix}_{slug}.html"

        return send_html(html, filename, base_url, city_id, verify_ssl, url, row)

    except Exception as e:
        log(f"  ❌ {e}")
        return False



def _visible_indexes(locator):
    visible = []
    try:
        count = locator.count()
    except Exception:
        return visible
    for index in range(count):
        try:
            if locator.nth(index).is_visible():
                visible.append(index)
        except Exception:
            pass
    return visible


def _save_playwright_image_response(response, local_path: Path) -> bool:
    try:
        body = response.body()
        content_type = (response.headers.get("content-type") or "").lower()
        if not body or "image/" not in content_type:
            return False
        local_path.write_bytes(body)
        return True
    except Exception:
        return False


def extract_instagram_context(page) -> dict:
    """Lit la légende et le compte depuis la page Instagram déjà ouverte."""
    context = {"description": "", "source_account": "", "source_name": ""}
    try:
        description = page.locator("meta[property='og:description']").first.get_attribute("content") or ""
        # Instagram préfixe parfois la vraie légende par ses métriques, selon
        # la langue de la session. Ce préfixe social ne doit jamais devenir
        # le titre ou la description métier de l'événement.
        if re.match(r"^\s*\d+[\s\d.,]*\s+(?:likes?|mentions? J’aime)", description, re.I):
            quoted = re.search(r'[:]\s*[\"“](.*)[\"”]\.?\s*$', description, re.S)
            if quoted:
                description = quoted.group(1)
        description = re.sub(r"^.*?on Instagram:\s*[\"“]?", "", description, flags=re.I)
        context["description"] = description.strip(' \"”')
    except Exception:
        pass
    try:
        title = page.locator("meta[property='og:title']").first.get_attribute("content") or ""
        source_name = re.sub(r"\s+on Instagram:.*$", "", title, flags=re.I).strip(' "“”')
        if source_name:
            context["source_name"] = source_name
        account = re.search(r"@([A-Za-z0-9._]+)", title)
        if account:
            context["source_account"] = account.group(1).lower()
    except Exception:
        pass
    return context


def should_use_instagram_caption(row: dict) -> bool:
    """Ignore la légende globale uniquement pour un planning découpé en slides."""
    content_mode = str(row.get("instagram_content_mode") or "").strip().upper()
    return content_mode != "PLANNING_INSTAGRAM"


def validate_instagram_planning_selection(row: dict) -> tuple[bool, str]:
    """Un agenda Instagram ne peut jamais choisir ses slides implicitement."""
    content_mode = str(row.get("instagram_content_mode") or "").strip().upper()
    if content_mode != "PLANNING_INSTAGRAM":
        return True, ""
    selection = any(str(row.get(field) or "").strip() for field in (
        "img_index", "image_index", "included_img_indexes",
        "excluded_img_indexes", "ignored_img_indexes",
    ))
    if selection:
        return True, ""
    return False, (
        "PLANNING_INSTAGRAM exige img_index, included_img_indexes "
        "ou excluded_img_indexes : sélection des slides obligatoire"
    )


def resolve_instagram_location(row: dict, base_url: str, verify_ssl: bool,
                               post_url: str) -> None:
    if str(row.get("target_string_id") or "").strip():
        return
    account = str(row.get("source_account") or "").strip().lstrip("@")
    name = str(row.get("source_name") or row.get("location_name") or "").strip()
    urls = [post_url]
    if account:
        urls.insert(0, f"https://www.instagram.com/{account}/")
    try:
        match = resolve_location(base_url, verify_ssl, name=name or account, urls=urls)
    except Exception as exc:
        log(f"  ℹ️ Résolution du lieu indisponible : {exc}")
        return
    if not match:
        log("  ℹ️ Aucun lieu iziLife résolu avec une confiance suffisante")
        return
    row["target_type"] = match["type"]
    row["target_string_id"] = match["string_id"]
    row["organizer_is_location"] = row.get("organizer_is_location") or "oui"
    log(f"  ✅ Lieu résolu : {match['type']} {match['name']} ({match['score']:.2f})")

def handle_igram_consent(page, appearance_timeout: int = 15000) -> bool:
    """
    Attend l'apparition différée du CMP Google Funding Choices puis le refuse.
    `locator.is_visible()` ne sert pas d'attente fiable : on utilise `wait_for()`.
    """
    consent_root = page.locator(".fc-consent-root").first

    try:
        log("  ⏳ Attente éventuelle du consentement igram...")
        consent_root.wait_for(
            state="visible",
            timeout=appearance_timeout
        )
    except Exception:
        log("  ℹ️ Aucun consentement igram affiché")
        return False

    log("  🍪 Fenêtre de consentement igram détectée")

    # Le texte et les classes internes peuvent varier : on cible d'abord
    # tous les boutons du CMP puis on filtre leur libellé.
    buttons = consent_root.locator("button")

    deadline = time.time() + 10

    while time.time() < deadline:
        try:
            count = buttons.count()
        except Exception:
            count = 0

        for index in range(count):
            button = buttons.nth(index)

            try:
                if not button.is_visible():
                    continue

                label = " ".join(
                    filter(
                        None,
                        [
                            button.inner_text(timeout=1000).strip(),
                            (button.get_attribute("aria-label") or "").strip(),
                            (button.get_attribute("title") or "").strip(),
                        ]
                    )
                ).lower()
            except Exception:
                continue

            if any(
                expected in label
                for expected in (
                    "refuser",
                    "tout refuser",
                    "refuser tout",
                    "continuer sans accepter",
                )
            ):
                button.scroll_into_view_if_needed()
                button.click(force=True, timeout=5000)

                try:
                    consent_root.wait_for(
                        state="hidden",
                        timeout=10000
                    )
                except Exception:
                    # Certains CMP retirent l'overlay mais conservent brièvement
                    # la racine dans le DOM.
                    page.wait_for_timeout(1000)

                log("  🍪 Consentement igram refusé")
                return True

        page.wait_for_timeout(500)

    # Dernier secours : croix en haut à droite.
    close_selectors = [
        "button.fc-close",
        "button[aria-label*='fermer' i]",
        "button[aria-label*='close' i]",
        "[role='button'][aria-label*='fermer' i]",
        "[role='button'][aria-label*='close' i]",
    ]

    for selector in close_selectors:
        try:
            close_button = consent_root.locator(selector).first
            close_button.wait_for(state="visible", timeout=1500)
            close_button.click(force=True, timeout=3000)
            page.wait_for_timeout(1000)
            log("  🍪 Fenêtre de consentement igram fermée")
            return True
        except Exception:
            pass

    log("  ⚠️ Bouton Refuser du CMP introuvable")
    return False


def close_igram_ad_popup(page) -> bool:
    """Ferme uniquement l'interstitiel publicitaire, jamais son bouton Ouvrir."""
    selectors = [
        "text=Fermer",
        "[aria-label='Fermer' i]",
        "[aria-label='Close' i]",
        "[title='Fermer' i]",
        "[title='Close' i]",
    ]

    for scope in [page, *page.frames]:
        for selector in selectors:
            try:
                close_button = scope.locator(selector).first
                if close_button.is_visible(timeout=250):
                    close_button.click(force=True, timeout=1500)
                    page.wait_for_timeout(500)
                    log("  ✅ Publicité interstitielle fermée")
                    return True
            except Exception:
                pass

    if "google_vignette" in page.url:
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
        except Exception:
            pass

    return False


def download_from_igram_world(
    page,
    instagram_url: str,
    image_dir: Path,
    pid: str
) -> list:
    """
    Parcours igram.world comme un utilisateur :
      1. ouvrir la page d'accueil française ;
      2. traiter le consentement différé ;
      3. cliquer sur Photo ;
      4. coller l'URL Instagram ;
      5. cliquer sur le premier bouton Télécharger ;
      6. attendre le résultat ;
      7. récupérer directement le href du bouton final ;
      8. enregistrer l'image dans images/<zone>/.
    """
    page.goto(
        "https://igram.world/fr1/",
        wait_until="domcontentloaded",
        timeout=30000
    )

    # Le CMP est absent pendant une session déjà initialisée. Une attente longue
    # répétée pour chaque post ralentit inutilement les campagnes Instagram.
    handle_igram_consent(page, appearance_timeout=1500)

    consent_root = page.locator(".fc-consent-root").first
    try:
        consent_root.wait_for(state="hidden", timeout=3000)
    except Exception:
        if consent_root.is_visible():
            raise RuntimeError(
                "Le bandeau de consentement igram bloque toujours la page"
            )

    # Accéder à l'outil Photo depuis la page d'accueil.
    photo_link = page.locator(
        "a[href*='/fr1/photo'], "
        "a:has-text('Photo'), "
        "button:has-text('Photo')"
    ).first

    try:
        photo_link.wait_for(state="visible", timeout=15000)
        photo_link.click()
        page.wait_for_load_state("domcontentloaded", timeout=30000)
    except Exception:
        # Secours pragmatique si le menu change.
        page.goto(
            "https://igram.world/fr1/photo",
            wait_until="domcontentloaded",
            timeout=30000
        )

    # Le CMP peut parfois réapparaître après la navigation interne.
    handle_igram_consent(page, appearance_timeout=700)

    input_box = page.locator(
        "form.search-form input[type='text'], "
        "input[type='text']"
    ).first

    input_box.wait_for(state="visible", timeout=15000)
    input_box.fill(instagram_url)

    sleep_random(1, 2)

    # Premier bouton Télécharger : submit du formulaire.
    submit_button = page.locator(
        "form.search-form button.search-form__button[type='submit'], "
        "form.search-form button[type='submit']"
    ).first

    submit_button.wait_for(state="visible", timeout=15000)
    try:
        submit_button.click(timeout=8000)
    except Exception as click_error:
        # iGram/Google interstitial ads can intercept the normal click while
        # leaving the form button visible. Close the ad and submit the form.
        closed = close_igram_ad_popup(page)
        try:
            submit_button.click(force=True, timeout=5000)
            log("  ✅ Soumission iGram via clic de secours" + (" après fermeture de la publicité" if closed else " malgré le recouvrement publicitaire"))
        except Exception:
            raise click_error

    log("  ⏳ URL envoyée à igram.world, attente du résultat...")

    # Le résultat réel contient un ou plusieurs liens .button__download.
    # Une publication simple en expose un ; un carrousel en expose plusieurs.
    result_links = page.locator(
        ".output-list a.button__download[href], "
        ".output-component a.button__download[href], "
        ".search-result a.button__download[href], "
        "a.button__download[href]"
    )

    hrefs = []
    for _ in range(20):
        close_igram_ad_popup(page)
        try:
            if result_links.count() and result_links.first.is_visible(timeout=250):
                break
        except Exception:
            pass
        page.wait_for_timeout(1000)

    # Attendre que le nombre de diapositives soit stable avant de les lire.
    previous_count = -1
    stable_rounds = 0
    for _ in range(12):
        count = result_links.count()
        stable_rounds = stable_rounds + 1 if count == previous_count and count > 0 else 0
        previous_count = count
        if stable_rounds >= 2:
            break
        page.wait_for_timeout(500)

    for index in range(result_links.count()):
        href = result_links.nth(index).get_attribute("href")
        if href and href.startswith("http") and href not in hrefs:
            hrefs.append(href)

    if not hrefs:
        log("  ⚠️ Le bouton de téléchargement du résultat n'est pas apparu")
        close_igram_ad_popup(page)
        candidates = page.locator(
            ".output-list img, .output-list video, "
            ".output-component img, .output-component video, "
            ".search-result img, .search-result video"
        ).evaluate_all(r"""
            elements => elements.map(el => ({
                src: el.currentSrc || el.src || '',
                width: el.naturalWidth || el.videoWidth || 0,
                height: el.naturalHeight || el.videoHeight || 0,
                context: `${el.alt || ''} ${el.className || ''} ${el.closest('a,article,section,div')?.className || ''}`.toLowerCase()
            })).filter(item =>
                /^https?:\/\//i.test(item.src)
                && item.width >= 300
                && item.height >= 300
                && !/(logo|avatar|icon|favicon|advert|publicit|banner|doubleclick|googleads)/i.test(`${item.src} ${item.context}`)
            ).sort((a, b) => (b.width * b.height) - (a.width * a.height))
        """)
        if not candidates:
            log("  ⚠️ Aucune grande image de résultat exploitable")
            return []
        hrefs = list(dict.fromkeys(item["src"] for item in candidates))
        log(
            f"  ✅ {len(hrefs)} média(s) de résultat détecté(s) directement"
        )

    log(f"  ✅ Résultat igram.world prêt : {len(hrefs)} média(s)")
    output_dir = image_dir / f"carousel_{pid}" if len(hrefs) > 1 else image_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    hashes = set()
    for index, href in enumerate(hrefs):
        response = page.request.get(href, headers={"Referer": page.url}, timeout=90000)
        if not response.ok:
            log(f"  ⚠️ Diapo #{index + 1} : HTTP {response.status}")
            continue
        body = response.body()
        digest = hashlib.sha256(body).hexdigest()
        if not body or digest in hashes:
            continue
        hashes.add(digest)
        content_type = (response.headers.get("content-type") or "").lower()
        suffix = ".png" if "png" in content_type else ".webp" if "webp" in content_type else ".jpg"
        local_path = output_dir / f"ig_{pid}_{index}{suffix}"
        local_path.write_bytes(body)
        if local_path.stat().st_size < 10_000:
            local_path.unlink(missing_ok=True)
            log(f"  ⚠️ Diapo #{index + 1} suspecte, ignorée")
            continue
        saved.append(local_path)
        log(f"  📥 Diapo #{index + 1} : {local_path} ({local_path.stat().st_size // 1024} Ko)")
    return saved


def download_from_instagram_page(page, instagram_url: str, image_dir: Path,
                                 pid: str) -> list[Path]:
    """Secours direct : télécharge les grandes images visibles du post public."""
    page.goto(instagram_url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)
    urls: list[str] = []
    for _ in range(10):
        candidates = page.locator("article img").evaluate_all(r"""
            images => images.map(img => ({
                src: img.currentSrc || img.src || '',
                width: img.naturalWidth || 0,
                height: img.naturalHeight || 0,
                alt: (img.alt || '').toLowerCase()
            })).filter(item =>
                /^https?:\/\//i.test(item.src)
                && item.width >= 300 && item.height >= 300
                && !/(photo de profil|profile picture|avatar)/i.test(item.alt)
            ).sort((a,b) => (b.width*b.height)-(a.width*a.height))
        """)
        for item in candidates:
            if item["src"] not in urls:
                urls.append(item["src"])
        next_button = page.locator(
            "article button[aria-label='Next'], article button[aria-label='Suivant']"
        ).last
        try:
            if not next_button.is_visible(timeout=500):
                break
            next_button.click()
            page.wait_for_timeout(900)
        except Exception:
            break
    if not urls:
        log("  ⚠️ Instagram direct : aucune image publique exploitable")
        return []
    output_dir = image_dir / f"carousel_{pid}" if len(urls) > 1 else image_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    hashes: set[str] = set()
    for index, media_url in enumerate(urls):
        response = page.request.get(media_url, headers={"Referer": instagram_url}, timeout=90000)
        if not response.ok:
            continue
        body = response.body()
        digest = hashlib.sha256(body).hexdigest()
        if len(body) < 10_000 or digest in hashes:
            continue
        hashes.add(digest)
        content_type = (response.headers.get("content-type") or "").lower()
        suffix = ".png" if "png" in content_type else ".webp" if "webp" in content_type else ".jpg"
        path = output_dir / f"ig_{pid}_direct_{index}{suffix}"
        path.write_bytes(body)
        saved.append(path)
    if saved:
        log(f"  ✅ Instagram direct : {len(saved)} média(s) original(aux) récupéré(s)")
    return saved


def handle_instagram(page, row: dict, base_url: str, city_id: int,
                     verify_ssl: bool, dry_run: bool, zone: str,
                     inspect_only: bool = False) -> bool:
    url = row["url"]
    log(f"  [INSTAGRAM] {url}")

    if dry_run:
        log("  [DRY RUN] serait téléchargé et envoyé")
        return True

    image_dir = get_image_dir(zone)
    post_id = re.search(r'/p/([A-Za-z0-9_-]+)', url)
    pid = post_id.group(1) if post_id else "unknown"

    # La page Instagram sert uniquement à récupérer son contexte éditorial.
    # `og:image` est une vignette potentiellement recadrée et ne doit jamais
    # devenir le média de l'événement. Le média est obligatoirement obtenu par
    # un vrai téléchargement depuis un bouton de téléchargement.
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    instagram_context = extract_instagram_context(page)
    planning_valid, planning_error = validate_instagram_planning_selection(row)
    if not planning_valid:
        row["inspection_result"] = json.dumps({
            "source": "instagram", "error": planning_error,
        }, ensure_ascii=False)
        log(f"  ❌ {planning_error}")
        return False
    indexed_slide = bool(str(row.get("img_index") or row.get("image_index") or "").strip())
    # Un carrousel ordinaire peut partager une légende utile avec la slide
    # sélectionnée. PLANNING_INSTAGRAM désigne au contraire une légende-agenda
    # globale, qui ne doit jamais polluer les événements extraits slide par slide.
    use_instagram_caption = should_use_instagram_caption(row)
    for key, value in instagram_context.items():
        if key == "description" and not use_instagram_caption:
            continue
        current = str(row.get(key) or "").strip()
        replace_social_prefix = key == "description" and re.match(r"^\d+[\s\d.,]*\s+(?:likes?|mentions?)", current, re.I)
        if value and (not current or replace_social_prefix):
            row[key] = value
    # La légende est du texte : les règles locales peuvent en extraire dates et
    # heures sans OCR et sans LLM, avant même le téléchargement du média.
    caption = str(row.get("description") or "") if use_instagram_caption else ""
    if caption:
        caption_fields = extract_event_fields(caption)
        for key in ("start_date", "start_hour", "end_hour"):
            if caption_fields.get(key) and not str(row.get(key) or "").strip():
                row[key] = caption_fields[key]
        if row.get("start_date") and row.get("end_hour") and not row.get("end_date"):
            row["end_date"] = inferred_end_date(row["start_date"], row.get("start_hour"), row["end_hour"])
        elif row.get("start_date") and row.get("end_hour") and str(row.get("end_date"))[:10] == str(row.get("start_date"))[:10]:
            row["end_date"] = inferred_end_date(row["start_date"], row.get("start_hour"), row["end_hour"])
        # La légende ne fournit que les faits déterministes (dates/heures).
        # Titre, description éditoriale et catégorie restent à Excel ou à Luna.
        if row.get("start_hour") and not row.get("end_hour"):
            row["end_hour"] = estimated_end_hour(row["start_hour"])
            row["end_hour_is_estimated"] = True
    resolve_instagram_location(row, base_url, verify_ssl, url)
    if inspect_only and "/reel/" in url and all(str(row.get(key) or "").strip() for key in
                            ("title", "start_date", "start_hour", "target_string_id")):
        row["inspection_result"] = json.dumps({
            "source": "instagram_caption",
            "title": row.get("title"), "start_date": excel_value(row.get("start_date")),
            "start_hour": excel_value(row.get("start_hour")), "end_hour": excel_value(row.get("end_hour")),
            "end_hour_is_estimated": bool(row.get("end_hour_is_estimated")),
            "target_type": row.get("target_type"), "target_string_id": row.get("target_string_id"),
            "media_downloaded": False, "ocr_used": False,
        }, ensure_ascii=False)
        log("  ✅ Légende suffisante : inspection terminée sans OCR ni téléchargement média")
        return True
    for igram in IGRAM_SITES:
        log(f"  Tentative via {igram['name']}...")

        try:
            if igram["name"] == "igram.world":
                local_files = download_from_igram_world(
                    page,
                    url,
                    image_dir,
                    pid
                )

                if not local_files:
                    log("  ⚠️ igram.world : aucun fichier récupéré")
                    continue

                planning_mode = str(row.get("instagram_content_mode") or "").strip().upper() == "PLANNING_INSTAGRAM"
                if not planning_mode and not inspect_only:
                    flyers = selected_event_flyers(local_files, row)
                    if not flyers:
                        log("  ❌ Aucun flyer sélectionné dans le carrousel")
                        return False
                    return send_event_flyers(flyers, base_url, city_id, verify_ssl, row, url)

                if inspect_only:
                    inspections = []
                    for local_path, event_row in carousel_event_rows(local_files, row):
                        payload = manual_event_payload(event_row, url, local_path)
                        payload["image_file"] = local_path.name
                        payload["img_index"] = event_row.get("img_index")
                        inspections.append(payload)
                    row["_inspection_candidates"] = inspections
                    if len(inspections) == 1:
                        for key, value in inspections[0].items():
                            if key in MANUAL_EVENT_FIELDS and value and not str(row.get(key) or "").strip():
                                row[key] = value
                    row["inspection_result"] = json.dumps(inspections, ensure_ascii=False)
                    log(f"  ✅ Inspection seule : {len(inspections)} candidat(s), aucun envoi serveur")
                    return bool(inspections)

                ok = False

                for image_index, (local_path, event_row) in enumerate(
                    carousel_event_rows(local_files, row)
                ):
                    log(
                        f"  📤 Envoi OCR : {local_path.name} "
                        f"({local_path.stat().st_size // 1024} Ko)"
                    )

                    if send_image(
                        local_path, base_url, city_id, verify_ssl, event_row, url,
                        allow_image_only_tmp=image_index == 0,
                    ):
                        ok = True

                if ok:
                    return True

                continue

            # Sites de secours : on conserve le flux générique,
            # mais les images restent également à la racine de la zone.
            page.goto(
                igram["url"],
                wait_until="domcontentloaded",
                timeout=30000
            )

            sleep_random(2, 3)

            page.locator(
                igram["input_sel"]
            ).first.fill(url)

            sleep_random(1, 2)

            page.locator(
                igram["btn_sel"]
            ).first.click()

            try:
                page.wait_for_selector(
                    igram["wait_sel"],
                    timeout=igram.get("result_timeout", 30000)
                )
            except Exception:
                log(f"  ⚠️ {igram['name']} : pas de résultat")
                continue

            img_urls = page.evaluate("""
                () => Array.from(document.querySelectorAll(
                    'a[href*=".jpg"], a[href*=".jpeg"], '
                    + 'a[href*=".png"], a[href*=".webp"], a[download]'
                ))
                .map(a => a.href)
                .filter(h => h.startsWith('http'))
            """)

            if not img_urls:
                log(f"  ⚠️ {igram['name']} : aucune image")
                continue

            log(f"  → {len(img_urls)} image(s)")
            ok = False

            for i, img_url in enumerate(img_urls):
                try:
                    response = page.request.get(
                        img_url,
                        timeout=30000
                    )

                    content_type = (
                        response.headers.get("content-type") or ""
                    ).lower()

                    suffix = (
                        ".png" if "png" in content_type
                        else ".webp" if "webp" in content_type
                        else ".jpg"
                    )

                    fname = f"ig_{pid}_{i}{suffix}"
                    local_path = image_dir / fname

                    if not _save_playwright_image_response(
                        response,
                        local_path
                    ):
                        continue

                    log(
                        f"  📥 Image enregistrée : {fname} "
                        f"({local_path.stat().st_size // 1024} Ko)"
                    )

                    if send_image(
                        local_path, base_url, city_id, verify_ssl, row, url,
                        allow_image_only_tmp=i == 0,
                    ):
                        ok = True

                except Exception as exc:
                    log(f"  ⚠️ image {i} : {exc}")

            if ok:
                return True

        except Exception as exc:
            log(f"  ⚠️ {igram['name']} : {exc}")
            continue

    log("  Tentative directe depuis la page Instagram...")
    try:
        local_files = download_from_instagram_page(page, url, image_dir, pid)
        if local_files:
            planning_mode = str(row.get("instagram_content_mode") or "").strip().upper() == "PLANNING_INSTAGRAM"
            if not planning_mode and not inspect_only:
                flyers = selected_event_flyers(local_files, row)
                return bool(flyers) and send_event_flyers(flyers, base_url, city_id, verify_ssl, row, url)
            if inspect_only:
                inspections = [manual_event_payload(event_row, url, local_path)
                               for local_path, event_row in carousel_event_rows(local_files, row)]
                row["inspection_result"] = json.dumps(inspections, ensure_ascii=False)
                return bool(inspections)
            ok = False
            for image_index, (local_path, event_row) in enumerate(carousel_event_rows(local_files, row)):
                ok = send_image(local_path, base_url, city_id, verify_ssl, event_row, url,
                                allow_image_only_tmp=image_index == 0) or ok
            if ok:
                return True
    except Exception as exc:
        log(f"  ⚠️ Instagram direct : {exc}")
    log("  ❌ Aucun téléchargement original Instagram/iGram disponible")
    return False


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Curation manuelle izilife")
    parser.add_argument("--zone",     type=str, required=True,
                        help="Zone cible : lille, valenciennes, dunkerque, paris, ...")
    parser.add_argument("--env",      choices=ENVS.keys(), default="local")
    parser.add_argument("--city",     type=str, required=False, default="lille")
    parser.add_argument("--sheet",    type=str, default="all",
                        help="Onglet : Facebook|Shotgun|HelloAsso|Eventbrite|Meetup|Instagram|all")
    parser.add_argument("--file", type=str, default="",
                        help="Classeur explicite à inspecter/traiter")
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--inspect-only", action="store_true",
                        help="Instagram : complète Excel localement sans créer d'Event/TMP")
    parser.add_argument("--max", type=int, default=0,
                        help="Nombre maximal de lignes à traiter (0 = toutes)")
    parser.add_argument("--init",     action="store_true",
                        help="Créer le fichier Excel template pour la zone")
    args = parser.parse_args()
    set_current_env(args.env)

    if args.init:
        create_excel_template(args.zone)
        log(f"Lance : python ingest_manual_curate.py --zone={args.zone} --env={args.env} --city=lille --dry-run")
        return

    env        = ENVS[args.env]
    base_url   = env["base_url"]
    verify_ssl = env["verify_ssl"]
    dry_run    = args.dry_run
    zone       = args.zone.lower().strip()

    curate_file = Path(args.file) if args.file else get_curate_file(zone)

    city_id = resolve_city_id(args.city, base_url, verify_ssl)

    log(f"=== ingest_manual_curate.py — zone={zone} env={args.env} city={args.city}" +
        (" [DRY RUN]" if dry_run else "") + " ===")
    log(f"Fichier : {curate_file}")

    if AGENT_TOKEN == "METTRE_TOKEN_ICI" and not dry_run:
        log("❌ IZILIFE_AGENT_TOKEN non défini.")
        sys.exit(1)

    if not curate_file.exists():
        log(f"❌ Fichier introuvable : {curate_file}")
        log(f"   Lance : python ingest_manual_curate.py --zone={zone} --init")
        sys.exit(1)

    wb = openpyxl.load_workbook(
        curate_file,
        keep_vba=curate_file.suffix.lower() == ".xlsm",
    )
    ensure_curate_columns(wb)
    configure_curate_selectors(wb)
    wb.save(curate_file)
    log("✅ Colonnes et sélecteurs de curation événementielle vérifiés")

    sheets_to_process = (
        [s for s in SHEET_HANDLERS.keys() if s in wb.sheetnames]
        if args.sheet.lower() == "all"
        else [args.sheet] if args.sheet in wb.sheetnames else []
    )

    if not sheets_to_process:
        log(f"❌ Onglet(s) introuvable(s). Disponibles : {wb.sheetnames}")
        sys.exit(1)

    all_rows = {}
    for sheet_name in sheets_to_process:
        rows = read_pending_rows(wb[sheet_name])
        if args.max > 0:
            rows = rows[:args.max]
        if rows:
            all_rows[sheet_name] = rows
            log(f"  {sheet_name} : {len(rows)} URLs pending")

    if not all_rows:
        log("✅ Aucune URL pending.")
        return

    if sync_playwright is None:
        raise RuntimeError("Playwright requis pour traiter les URLs : pip install playwright && python -m playwright install chromium")

    log(f"\nTotal : {sum(len(r) for r in all_rows.values())} URLs")

    stats = {"done": 0, "errors": 0}

    with sync_playwright() as p:

        needs_chrome = any(s in all_rows for s in ["Facebook", "Instagram"])
        launch_args  = {"headless": False,
                        "args": ["--disable-blink-features=AutomationControlled",
                                 "--disable-notifications"]}
        if needs_chrome:
            launch_args["channel"] = "chrome"

        browser = p.chromium.launch(**launch_args)
        context = browser.new_context(locale="fr-FR")

        if "Facebook" in all_rows:
            load_cookies(context, "facebook")

        page = context.new_page()
        apply_stealth(page)

        # Vérifier connexion Facebook si nécessaire
        if "Facebook" in all_rows:
            page.goto("https://www.facebook.com", timeout=30000)
            sleep_random(2, 3)
            if "login" in page.url or "checkpoint" in page.url:
                log("⚠️  Facebook non connecté — tentative login auto...")
                logged_in = login_facebook(page)
                if not logged_in:
                    print("")
                    print("=" * 60)
                    print("  Connecte-toi manuellement dans Chrome.")
                    print("  Quand tu es connecté → appuie sur ENTREE")
                    print("=" * 60)
                    input("")
                    if "login" in page.url:
                        log("❌ Toujours non connecté — onglet Facebook ignoré")
                        all_rows.pop("Facebook", None)
            else:
                log("✅ Facebook connecté")

        for sheet_name, rows in all_rows.items():
            handler_type = SHEET_HANDLERS.get(sheet_name, "html")
            ws           = wb[sheet_name]

            log(f"\n{'='*50}")
            log(f"Onglet : {sheet_name} ({len(rows)} URLs)")
            log(f"{'='*50}")

            for row in rows:
                log(f"\n  → {row['url'][:80]}")

                if handler_type == "instagram":
                    ok = handle_instagram(page, row, base_url, city_id,
                                          verify_ssl, dry_run, zone, args.inspect_only)
                else:
                    ok = handle_html(page, row, base_url, city_id,
                                     verify_ssl, dry_run)

                if args.inspect_only:
                    headers = {str(c.value or "").strip().lower(): c.column for c in ws[1]}
                    for key in (*MANUAL_EVENT_FIELDS, "img_index", "included_img_indexes", "excluded_img_indexes",
                                "detected_img_indexes", "inspection_result"):
                        if key in headers and row.get(key) not in (None, ""):
                            ws.cell(row["row_idx"], headers[key], row[key])
                    for key in row.get("_clear_fields", []):
                        if key in headers:
                            ws.cell(row["row_idx"], headers[key], "")
                    candidates = row.get("_inspection_candidates") or []
                    indexed_candidates = [candidate for candidate in candidates if candidate.get("img_index")]
                    if indexed_candidates:
                        existing = {
                            (str(ws.cell(r, headers["url"]).value or "").strip(),
                             str(ws.cell(r, headers["img_index"]).value or "").strip())
                            for r in range(2, ws.max_row + 1)
                        }
                        for candidate in indexed_candidates:
                            key = (str(row["url"]).strip(), str(candidate["img_index"]))
                            if key in existing:
                                continue
                            values = {name: "" for name in headers}
                            for name in ("target_type", "target_string_id", "organizer_is_location",
                                         "organizer_type", "organizer_string_id", "event_category_ref",
                                         "is_free_event", "auto_validate", "use_llm_if_missing"):
                                values[name] = row.get(name, "")
                            values.update(candidate)
                            values.update({"url": row["url"], "status": "pending",
                                           "notes": "Généré automatiquement depuis le carrousel",
                                           "inspection_result": json.dumps(candidate, ensure_ascii=False)})
                            ws.append([values.get(str(cell.value or "").strip().lower(), "") for cell in ws[1]])
                            existing.add(key)
                        ws.cell(row["row_idx"], headers["status"], "split")
                        ws.cell(row["row_idx"], headers["notes"],
                                "Carrousel inspecté : lignes Event générées automatiquement")
                    wb.save(curate_file)
                elif not dry_run:
                    new_status = "done" if ok else "failed"
                    update_row(ws, row["row_idx"], new_status)
                    wb.save(curate_file)

                stats["done" if ok else "errors"] += 1
                sleep_random(2, 4)

        browser.close()

    log(f"\n=== Résultat ===")
    log(f"  Traités : {stats['done']}")
    log(f"  Erreurs : {stats['errors']}")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("curate_manuel_events", "events", main)
