"""Smoke test read-only du lookup d'identité local iziLife."""
from __future__ import annotations

import argparse
import json
import os
import sys

import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from core.paths import IZILIFE_ENVS


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--name", required=True)
    parser.add_argument("--city", required=True)
    parser.add_argument("--address", default="")
    parser.add_argument("--latitude", type=float)
    parser.add_argument("--longitude", type=float)
    parser.add_argument("--url", action="append", default=[])
    args = parser.parse_args()
    if args.env != "local":
        raise SystemExit("Ce smoke test est volontairement limité à --env=local.")
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN absent.")
    cfg = IZILIFE_ENVS[args.env]
    payload = {"name": args.name, "city": args.city, "address": args.address,
               "latitude": args.latitude, "longitude": args.longitude, "urls": args.url}
    response = requests.post(
        cfg["base_url"].rstrip("/") + "/scraper/agentLocationIdentityCandidates",
        json=payload, headers={"X-Agent-Token": token, "Accept": "application/json"},
        verify=cfg.get("verify_ssl", True), timeout=30,
    )
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    return 0 if response.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
