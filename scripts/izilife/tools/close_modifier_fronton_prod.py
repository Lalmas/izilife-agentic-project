from __future__ import annotations

import json
import os

import requests


def main() -> None:
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN absent")
    payload = {
        "scope_type": "SHOP",
        "scope_ref": "le-fronton-citi",
        "primary_category_ref": "salle-de-sport",
        "closed_state_ref": "ferme-definitivement",
        "is_active": "0",
        "listable": "0",
    }
    response = requests.post(
        "https://www.izilife.co/izilife-admin/scraper/agentMaintainLocation",
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        data={"payload": json.dumps(payload, ensure_ascii=False)},
        timeout=60,
    )
    body = response.json()
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(f"HTTP {response.status_code}: {body}")
    print(json.dumps(body, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
