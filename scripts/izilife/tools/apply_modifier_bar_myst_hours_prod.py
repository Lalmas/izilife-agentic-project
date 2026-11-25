from __future__ import annotations

import json
import os

import requests


def main() -> None:
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN absent")
    days = [
        {"day_id": 1, "closing_day": 1},
        {"day_id": 2, "closing_day": 0, "opening_hour": "18:00", "closure_hour": "01:00"},
        {"day_id": 3, "closing_day": 0, "opening_hour": "18:00", "closure_hour": "01:00"},
        {"day_id": 4, "closing_day": 0, "opening_hour": "18:00", "closure_hour": "01:00"},
        {"day_id": 5, "closing_day": 0, "opening_hour": "18:30", "closure_hour": "02:00"},
        {"day_id": 6, "closing_day": 0, "opening_hour": "18:30", "closure_hour": "02:00"},
        {"day_id": 7, "closing_day": 1},
    ]
    response = requests.post(
        "https://www.izilife.co/izilife-admin/scraper/agentApplyGoogleHours",
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        json={"scope_type": "SHOP", "scope_ref": "bar-myst", "days": days},
        timeout=60,
    )
    body = response.json()
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(f"HTTP {response.status_code}: {body}")
    print(json.dumps(body, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
