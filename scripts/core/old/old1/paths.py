from pathlib import Path
import os
import sys

# ─────────────────────────────────────────────
# CORE PATHS — source unique chemins/envs
# ─────────────────────────────────────────────

def normalize_zone(zone: str) -> str:
    zone = str(zone or "").strip().lower()
    return zone if zone.endswith("-zone") else f"{zone}-zone"

PROJECT_ROOT = Path(os.getenv(
    "AGENTIC_WORKSPACE_ROOT",
    Path.home() / "Documents" / "agentic_Workspace"
))

DRIVE_ROOT = Path(os.getenv("AGENTIC_DRIVE_ROOT", "G:/Mon Drive"))

# Drive partagé : fichiers Excel / zones / sources validées
WORKSPACE_BY_ENV = {
    "local":   "agentic_workspace_local",
    "staging": "agentic_workspace_staging",
    "prod":    "agentic_workspace",
}

# Espace local machine : cookies, images temporaires, html collectés, logs techniques
LOCAL_WORKSPACE_BY_ENV = {
    "local":   "izilife-agent-workspace-local",
    "staging": "izilife-agent-workspace-staging",
    "prod":    "izilife-agent-workspace",
}

IZILIFE_ENVS = {
    "local": {
        "base_url": os.getenv("IZILIFE_LOCAL_URL", "https://localhost:4443/izilife-admin"),
        "verify_ssl": False,
    },
    "staging": {
        "base_url": os.getenv("IZILIFE_STAGING_URL", "https://www.staging.izilife.co/izilife-admin"),
        "verify_ssl": True,
    },
    "prod": {
        "base_url": os.getenv("IZILIFE_PROD_URL", "https://www.izilife.co/izilife-admin"),
        "verify_ssl": True,
    },
}

ENV_GLOBAL  = PROJECT_ROOT / ".env"
ENV_IZILIFE = PROJECT_ROOT / "izilife" / ".env.izilife"
ENV_AGENCE  = PROJECT_ROOT / "agence" / ".env.agence"

def workspace_name(env_name: str = "prod") -> str:
    return WORKSPACE_BY_ENV.get(str(env_name or "prod").lower(), "agentic_workspace")

def local_workspace_name(env_name: str = "prod") -> str:
    return LOCAL_WORKSPACE_BY_ENV.get(str(env_name or "prod").lower(), "izilife-agent-workspace")

def workspace_root(env_name: str = "prod") -> Path:
    return DRIVE_ROOT / workspace_name(env_name)

def izilife_project_root() -> Path:
    return PROJECT_ROOT / "izilife"

def local_agent_workspace_root(env_name: str = "prod") -> Path:
    # Dossiers techniques locaux propres à izilife, séparés par environnement.
    # Ex: Documents/agentic_Workspace/izilife/izilife-agent-workspace-local
    return izilife_project_root() / local_workspace_name(env_name)

# ── PLACES ───────────────────────────────────

def izilife_places_zone(zone: str, env_name: str = "prod") -> Path:
    return workspace_root(env_name) / "izilife" / "places" / normalize_zone(zone)

# ── EVENTS ───────────────────────────────────

def izilife_events_zone(zone: str, env_name: str = "prod") -> Path:
    return workspace_root(env_name) / "izilife" / "events" / normalize_zone(zone)

def event_curate_file(zone: str, env_name: str = "prod") -> Path:
    return izilife_events_zone(zone, env_name) / "curate_events.xlsx"

def event_logs_dir(zone: str, env_name: str = "prod") -> Path:
    d = izilife_events_zone(zone, env_name) / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_source_dir(platform: str, zone: str, env_name: str = "prod") -> Path:
    # HTML collectés localement, pas sur Drive, pour éviter de polluer prod/staging/local entre eux.
    d = local_agent_workspace_root(env_name) / platform / normalize_zone(zone) / "events"
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_images_dir(zone: str, env_name: str = "prod") -> Path:
    d = local_agent_workspace_root(env_name) / "images" / normalize_zone(zone)
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_download_dir(zone: str, env_name: str = "prod", downloads: bool = True) -> Path:
    d = event_images_dir(zone, env_name) / ("downloads" if downloads else "")
    d.mkdir(parents=True, exist_ok=True)
    return d

def event_sent_log_file(env_name: str = "prod") -> Path:
    d = local_agent_workspace_root(env_name) / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d / "event_images_sent.txt"

# ── SOCIAL — laissé en prod par défaut pour l'instant ───────────────────

def izilife_social_zone(zone: str, env_name: str = "prod") -> Path:
    return workspace_root(env_name) / "izilife" / "social" / normalize_zone(zone)

# ── AGENCE ───────────────────────────────────

def agence_client(slug: str, env_name: str = "prod") -> Path:
    return workspace_root(env_name) / "agence" / "clients" / str(slug).strip()
