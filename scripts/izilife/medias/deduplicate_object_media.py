from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests

SCRIPTS = Path(__file__).resolve().parents[2]
IZILIFE = Path(__file__).resolve().parents[1]
for root in (SCRIPTS, IZILIFE):
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

from core.paths import IZILIFE_ENVS
from objects.object_agent_common import load_env


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--target", action="append", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-production")
    args = parser.parse_args()
    load_env()
    if args.apply and args.env == "prod" and args.confirm_production != "I_CONFIRM_PRODUCTION_MEDIA_DEDUP":
        raise SystemExit("Production refusée sans confirmation explicite.")
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN manquant.")
    config = IZILIFE_ENVS[args.env]
    results = []
    for target in args.target:
        if ":" not in target:
            raise SystemExit(f"Cible invalide: {target}")
        scope_type, scope_ref = target.split(":", 1)
        response = requests.post(
            config["base_url"].rstrip("/") + "/scraper/agentDeduplicateObjectMedia",
            json={"scope_type": scope_type.upper(), "scope_ref": scope_ref, "dry_run": not args.apply},
            headers={"X-Agent-Token": token},
            verify=config.get("verify_ssl", True),
            timeout=180,
        )
        body = response.json()
        results.append({"target": target, "http": response.status_code, "result": body})
        if response.status_code >= 400 or not body.get("success"):
            raise SystemExit(json.dumps(results, ensure_ascii=False))
    print(json.dumps({"success": True, "dry_run": not args.apply, "results": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
