# scripts/core/paths.py
from pathlib import Path
import os

PROJECT_ROOT = Path(os.getenv(
    "AGENTIC_WORKSPACE_ROOT",
    Path.home() / "Documents" / "agentic_Workspace"
))

DRIVE_ROOT = Path(os.getenv(
    "AGENTIC_DRIVE_ROOT",
    "G:/Mon Drive"
))

DATA_ROOT = DRIVE_ROOT / "agentic_workspace"

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

def izilife_places_zone(zone: str) -> Path:
    return DATA_ROOT / "izilife" / "places" / f"{zone}-zone"

def izilife_social_zone(zone: str) -> Path:
    return DATA_ROOT / "izilife" / "social" / zone

def agence_client(slug: str) -> Path:
    return DATA_ROOT / "agence" / "clients" / slug