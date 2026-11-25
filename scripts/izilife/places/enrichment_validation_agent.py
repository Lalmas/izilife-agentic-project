"""Valide automatiquement les demandes ENRICH de PLACE/SHOP.

Règle serveur :
- payload vide ou composé uniquement de confidence/confidence_score => REJECTED ;
- au moins une donnée métier non vide => application puis APPLIED/FAILED.

Le serveur recalcule toujours la règle. Le script ne peut pas forcer une décision.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests


def _ensure_core_import_path() -> None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "scripts" / "core" / "paths.py").exists():
            sys.path.insert(0, str(parent / "scripts"))
            return


_ensure_core_import_path()
try:
    from core.paths import IZILIFE_ENVS
except ImportError:
    IZILIFE_ENVS = {
        "local": {"base_url": "https://localhost:4443/izilife-admin", "verify_ssl": False},
        "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify_ssl": True},
        "prod": {"base_url": "https://www.izilife.co/izilife-admin", "verify_ssl": True},
    }


def has_business_changes(payload: Any, entity_type: str = "SHOP") -> bool:
    if not isinstance(payload, dict):
        return False
    scalar_allowed = {"short_description", "phone_number", "opening_hours_text"}
    if entity_type.upper() == "SHOP":
        scalar_allowed.add("website")
    for field, value in (payload.get("scalar") or {}).items():
        if field in scalar_allowed and str(value or "").strip():
            return True

    principal_allowed = {
        "have_terrace", "adapted_to_handicap", "can_drink_alcool",
        "sell_alcool", "play_music", "wifi", "can_eat_here",
    }
    for field, value in (payload.get("principal_characteristics") or {}).items():
        if field in principal_allowed and int(value or 0) == 1:
            return True

    for satellite_type, items in (payload.get("satellites") or {}).items():
        if not isinstance(items, list):
            continue
        if satellite_type in {"Atmosphere", "ShopAndPlaceCharactTag", "MealType", "BarType", "MusicStyle"}:
            if any(isinstance(item, dict) and str(item.get("string_id") or "").strip() for item in items):
                return True
        elif satellite_type == "Equipment":
            if any(isinstance(item, dict) and str(item.get("equipment_category_string_id") or "").strip() for item in items):
                return True
        elif satellite_type == "Terrace" and items:
            return True

    return any(str(value or "").strip() for value in ((payload.get("media") or {}).get("photo_references") or []))


class AgentApi:
    def __init__(self, env: dict[str, Any], token: str):
        self.base_url = str(env["base_url"]).rstrip("/")
        self.verify_ssl = bool(env.get("verify_ssl", True))
        self.headers = {"X-Agent-Token": token}

    def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            self.base_url + endpoint,
            data=data,
            headers=self.headers,
            verify=self.verify_ssl,
            timeout=120,
        )
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(f"HTTP {response.status_code}: réponse non JSON") from exc
        if response.status_code >= 400:
            raise RuntimeError(f"HTTP {response.status_code}: {payload.get('error', payload)}")
        return payload


def run(env_name: str, limit: int, city_id: int, dry_run: bool, request_id: int = 0) -> int:
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN non défini.")
    api = AgentApi(IZILIFE_ENVS[env_name], token)
    if request_id > 0:
        if dry_run:
            print(f"[DRY RUN] retraitement demandé pour #{request_id}")
            return 0
        result = api.post(
            "/scraper/agentProcessEnrichmentValidation",
            {"id": request_id, "retry_failed": 1},
        )
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result.get("success") else 1

    candidates = api.post(
        "/scraper/agentEnrichmentValidationCandidates",
        {"limit": limit, "city_id": city_id or ""},
    ).get("items", [])

    stats = {"found": len(candidates), "applied": 0, "rejected": 0, "failed": 0}
    print(f"{len(candidates)} demande(s) ENRICH à traiter — env={env_name}" + (" [DRY RUN]" if dry_run else ""))

    for item in candidates:
        request_id = int(item["id"])
        has_changes = bool(item.get("has_business_changes", has_business_changes(
            item.get("proposed_payload", {}), str(item.get("entity_type", "SHOP"))
        )))
        expected = "APPLIED" if has_changes else "REJECTED"
        label = f"#{request_id} {item.get('entity_type')}#{item.get('entity_id')}"
        if dry_run:
            print(f"[DRY RUN] {label} => {expected}")
            continue
        try:
            result = api.post("/scraper/agentProcessEnrichmentValidation", {"id": request_id})
            decision = str(result.get("decision", "FAILED"))
            if decision == "APPLIED":
                stats["applied"] += 1
            elif decision == "REJECTED":
                stats["rejected"] += 1
            else:
                stats["failed"] += 1
            print(f"{label} => {decision}")
        except Exception as exc:
            stats["failed"] += 1
            print(f"{label} => ERROR: {exc}", file=sys.stderr)
            print("Arrêt du lot au premier échec pour éviter une rafale de traitements invalides.", file=sys.stderr)
            break

    print(json.dumps(stats, ensure_ascii=False))
    return 1 if stats["failed"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validateur des demandes d'enrichissement PLACE/SHOP")
    parser.add_argument("--env", choices=IZILIFE_ENVS.keys(), default="local")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--city-id", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--request-id", type=int, default=0, help="Retraiter une demande précise, y compris FAILED")
    args = parser.parse_args()
    return run(args.env, max(1, min(200, args.limit)), max(0, args.city_id), args.dry_run, max(0, args.request_id))


if __name__ == "__main__":
    raise SystemExit(main())
