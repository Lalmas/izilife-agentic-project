from pathlib import Path
import os

# ─────────────────────────────────────────────
# CONVENTIONS
# ─────────────────────────────────────────────
# Utilisateur : --zone=lille, --city=lille, --env=local|staging|prod
# Dossiers zone internes : lille-zone
# Drive :
#   local   -> $AGENTIC_DRIVE_ROOT/agentic_workspace_local
#   staging -> $AGENTIC_DRIVE_ROOT/agentic_workspace_staging
#   prod    -> $AGENTIC_DRIVE_ROOT/agentic_workspace
# Local technique izilife :
#   local   -> Documents/agentic_Workspace/izilife/izilife-agent-workspace-local
#   staging -> Documents/agentic_Workspace/izilife/izilife-agent-workspace-staging
#   prod    -> Documents/agentic_Workspace/izilife/izilife-agent-workspace


def normalize_zone(zone: str) -> str:
    zone = str(zone or "").strip().lower()
    return zone if zone.endswith("-zone") else f"{zone}-zone"


PROJECT_ROOT = Path(os.getenv(
    "AGENTIC_WORKSPACE_ROOT",
    Path.home() / "Documents" / "agentic_Workspace"
))

_drive_root_value = os.getenv("AGENTIC_DRIVE_ROOT", "").strip()
DRIVE_ROOT = Path(_drive_root_value).expanduser() if _drive_root_value else None

ENV_GLOBAL = PROJECT_ROOT / ".env"
ENV_IZILIFE = PROJECT_ROOT / "izilife" / ".env.izilife"
ENV_AGENCE = PROJECT_ROOT / "agence" / ".env.agence"

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

WORKSPACE_BY_ENV = {
    "local": "agentic_workspace_local",
    "staging": "agentic_workspace_staging",
    "prod": "agentic_workspace",
}

LOCAL_AGENT_WORKSPACE_BY_ENV = {
    "local": "izilife-agent-workspace-local",
    "staging": "izilife-agent-workspace-staging",
    "prod": "izilife-agent-workspace",
}


def normalize_env(env_name: str | None) -> str:
    env_name = str(env_name or "prod").strip().lower()
    return env_name if env_name in WORKSPACE_BY_ENV else "prod"


def drive_workspace_root(env_name: str = "prod") -> Path:
    if DRIVE_ROOT is None:
        raise RuntimeError("AGENTIC_DRIVE_ROOT non défini : impossible de localiser Google Drive.")
    return DRIVE_ROOT / WORKSPACE_BY_ENV[normalize_env(env_name)]


def local_agent_workspace_root(env_name: str = "prod") -> Path:
    return PROJECT_ROOT / "izilife" / LOCAL_AGENT_WORKSPACE_BY_ENV[normalize_env(env_name)]


def izilife_places_zone(zone: str, env_name: str = "prod") -> Path:
    return drive_workspace_root(env_name) / "izilife" / "places" / normalize_zone(zone)


def izilife_events_zone(zone: str, env_name: str = "prod") -> Path:
    return drive_workspace_root(env_name) / "izilife" / "events" / normalize_zone(zone)


def izilife_event_images_zone(zone: str, env_name: str = "prod") -> Path:
    return local_agent_workspace_root(env_name) / "images" / normalize_zone(zone)


def izilife_social_zone(zone: str, env_name: str = "prod") -> Path:
    # Social reste prod-only dans la pratique, mais l'argument env permet de ne pas casser les imports.
    return drive_workspace_root(env_name) / "izilife" / "social" / normalize_zone(zone)


def agence_client(slug: str, env_name: str = "prod") -> Path:
    return drive_workspace_root(env_name) / "agence" / "clients" / str(slug).strip()


# Chemins communs utilisés par tous les agents événements.
def event_curate_file(zone: str, env_name: str = "prod") -> Path:
    return izilife_events_zone(zone, env_name) / "curate_events.xlsx"


def event_download_dir(zone: str, env_name: str = "prod", downloads: bool = True) -> Path:
    path = izilife_event_images_zone(zone, env_name)
    if downloads:
        path /= "downloads"
    path.mkdir(parents=True, exist_ok=True)
    return path


def event_source_dir(platform: str, zone: str, env_name: str = "prod") -> Path:
    path = local_agent_workspace_root(env_name) / str(platform).strip().lower() / normalize_zone(zone) / "events"
    path.mkdir(parents=True, exist_ok=True)
    return path


def event_sent_log_file(env_name: str = "prod") -> Path:
    path = local_agent_workspace_root(env_name) / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path / "event_images_sent.txt"
