#!/usr/bin/env python3
"""Planifie puis applique une conversion Shop -> Place dans un seul environnement.

Le script ne transporte aucun identifiant entre environnements. Les deux objets
sont résolus par string_id par le backend cible. `plan` est toujours en lecture
seule; `apply` exige le hash exact retourné par ce plan.
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
PLAN_ENDPOINT = "/scraper/agentShopToPlacePlan"
APPLY_ENDPOINT = "/scraper/agentShopToPlaceApply"


def post(env: str, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    cfg = ENVS[env]
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN est absent.")
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


def save_report(report_dir: Path, env: str, source: str, payload: dict[str, Any]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = report_dir / f"shop-to-place-{env}-{source}-{stamp}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["plan", "apply"])
    parser.add_argument("--env", choices=ENVS, required=True)
    parser.add_argument("--source-shop-ref", required=True)
    parser.add_argument("--destination-place-ref", required=True)
    parser.add_argument("--plan-file", type=Path)
    parser.add_argument("--activate-destination", action="store_true",
                        help="Active et rend listable la Place au moment de l'application.")
    parser.add_argument("--confirm-production", action="store_true")
    parser.add_argument("--report-dir", type=Path, default=Path(__file__).with_name("reports"))
    args = parser.parse_args()

    base = {
        "source_shop_ref": args.source_shop_ref.strip(),
        "destination_place_ref": args.destination_place_ref.strip(),
        "activate_destination": args.activate_destination,
    }
    if args.command == "plan":
        result = post(args.env, PLAN_ENDPOINT, base)
        path = save_report(args.report_dir, args.env, args.source_shop_ref, result)
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
    payload = base | {
        "plan_hash": plan["plan_hash"],
        "confirm_apply": "SHOP_TO_PLACE_APPLY",
        "idempotency_key": f"shop-to-place:{args.env}:{base['source_shop_ref']}:{base['destination_place_ref']}:{plan['plan_hash'][:16]}",
    }
    result = post(args.env, APPLY_ENDPOINT, payload)
    path = save_report(args.report_dir, args.env, args.source_shop_ref, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Rapport: {path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        raise SystemExit(1)
