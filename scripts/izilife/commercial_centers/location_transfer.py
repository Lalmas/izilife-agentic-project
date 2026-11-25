#!/usr/bin/env python3
"""Planifie/applique une conversion contrôlée Place/Shop dans un environnement.

Le backend résout toutes les fiches et catégories par string_id. Aucun ID d'un
autre environnement n'est accepté par cet opérateur.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import urllib3


ENVS = {
    "local": {"base_url": "https://localhost:4443/izilife-admin", "verify": False},
    "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify": True},
    "prod": {"base_url": "https://www.izilife.co/izilife-admin", "verify": True},
}
PLAN_ENDPOINT = "/scraper/agentLocationTransferPlan"
APPLY_ENDPOINT = "/scraper/agentLocationTransferApply"


def post(env: str, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN est absent.")
    cfg = ENVS[env]
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.post(
        cfg["base_url"] + endpoint,
        json=payload,
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        timeout=180,
        verify=cfg["verify"],
    )
    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Réponse non JSON (HTTP {response.status_code}): {response.text[:500]}") from exc
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
    return body


def save_report(report_dir: Path, env: str, source_type: str, source_ref: str, payload: dict[str, Any]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = report_dir / f"location-transfer-{env}-{source_type.lower()}-{source_ref}-{stamp}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["plan", "apply"])
    parser.add_argument("--env", choices=ENVS, required=True)
    parser.add_argument("--source-type", choices=["PLACE", "SHOP", "PAGE", "EQUIPMENT"], required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--destination-type", choices=["PLACE", "SHOP", "PAGE", "EQUIPMENT"], required=True)
    parser.add_argument("--destination-ref", required=True)
    parser.add_argument("--destination-mode", choices=["EXISTING", "CREATE"], default="EXISTING")
    parser.add_argument("--destination-name")
    parser.add_argument("--destination-category-ref",
                        help="Référence stable de la catégorie destination; requise pour CREATE inter-type.")
    parser.add_argument("--activate-destination", action="store_true")
    parser.add_argument("--plan-file", type=Path)
    parser.add_argument("--confirm-production", action="store_true")
    parser.add_argument("--report-dir", type=Path, default=Path(__file__).with_name("reports"))
    args = parser.parse_args()

    payload = {
        "source_type": args.source_type,
        "source_ref": args.source_ref.strip(),
        "destination_type": args.destination_type,
        "destination_ref": args.destination_ref.strip(),
        "destination_mode": args.destination_mode,
        "destination_name": (args.destination_name or "").strip(),
        "destination_category_ref": (args.destination_category_ref or "").strip(),
        "activate_destination": args.activate_destination,
    }
    if args.command == "plan":
        result = post(args.env, PLAN_ENDPOINT, payload)
        path = save_report(args.report_dir, args.env, args.source_type, args.source_ref, result)
        print(json.dumps(result["plan"], ensure_ascii=False, indent=2))
        print(f"Rapport: {path}")
        return 0 if result["plan"].get("can_apply") else 2

    if not args.plan_file or not args.plan_file.exists():
        raise RuntimeError("--plan-file est requis pour apply.")
    if args.env == "prod" and not args.confirm_production:
        raise RuntimeError("--confirm-production est obligatoire pour une écriture en production.")
    frozen = json.loads(args.plan_file.read_text(encoding="utf-8"))
    plan = frozen.get("plan", frozen)
    if not plan.get("can_apply"):
        raise RuntimeError("Le plan figé contient des bloqueurs.")
    payload.update({
        "plan_hash": plan["plan_hash"],
        "confirm_apply": "LOCATION_TRANSFER_APPLY",
        "idempotency_key": (
            f"location-transfer:{args.env}:{args.source_type}:{payload['source_ref']}:"
            f"{args.destination_type}:{payload['destination_ref']}:{plan['plan_hash'][:16]}"
        ),
    })
    result = post(args.env, APPLY_ENDPOINT, payload)
    path = save_report(args.report_dir, args.env, args.source_type, args.source_ref, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Rapport: {path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        raise SystemExit(1)
