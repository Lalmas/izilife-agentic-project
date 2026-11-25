"""Termine uniquement les lignes Event de Modifier, puis les contre-audite.

Le script exige les endpoints ciblés livrés le 2026-11-08. Chaque mutation est
idempotente et limitée à la temporalité ou au lieu explicitement demandé.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import requests


BASE = "https://www.izilife.co/izilife-admin"
TOKEN = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
HEADERS = {"X-Agent-Token": TOKEN, "Accept": "application/json"}
REPORT = Path(__file__).with_name("finish_modifier_events_prod_report.json")


def post(path: str, payload: dict) -> dict:
    response = requests.post(BASE + path, json=payload, headers=HEADERS, timeout=120)
    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError(f"{path}: HTTP {response.status_code}, réponse non JSON") from exc
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(f"{path}: HTTP {response.status_code}: {body}")
    return body


def main() -> None:
    if not TOKEN:
        raise SystemExit("IZILIFE_AGENT_TOKEN absent")
    results: list[dict] = []

    temporal = [
        {
            "event_ref": "f8f1209f95b3b396e8c82c7a9cbaf359",
            "start_date": "2026-01-24", "start_hour": "15:00",
            "end_date": "2026-01-24", "end_hour": "19:00",
            "rrule": "FREQ=WEEKLY;INTERVAL=1;BYDAY=SA,SU",
            "until_date": "2036-02-17", "future_occurrences": 4,
            "horizon_days": 90, "remove_event_hourly": True,
            "timezone_id": "Europe/Paris",
        },
        {
            "event_ref": "7d578ab0d8133a988186cd68ffe0614f",
            "start_date": "2026-11-07", "start_hour": "15:00",
            "end_date": "2026-11-07", "end_hour": "23:59",
            "rrule": "FREQ=MONTHLY;INTERVAL=1;BYDAY=1SA",
            "future_occurrences": 3, "horizon_days": 400,
            "remove_event_hourly": True,
            "timezone_id": "Europe/Paris",
        },
    ]
    for payload in temporal:
        results.append({"operation": "temporal", "ref": payload["event_ref"], "result": post("/scraper/agentCorrectEventTemporal", payload)})

    finite = {
        "event_ref": "dbd49d3cdf1ed8611fcbd5ded7e20d1c",
        "occurrences": [
            {"date": "2026-11-04", "start_hour": "14:30", "end_hour": "15:15"},
            {"date": "2026-11-06", "start_hour": "14:30", "end_hour": "15:15"},
            {"date": "2026-11-07", "start_hour": "16:30", "end_hour": "17:15"},
        ],
    }
    results.append({"operation": "finite_occurrences", "ref": finite["event_ref"], "result": post("/scraper/agentCorrectFiniteEventOccurrences", finite)})

    for event_ref in [
        "9fabb37d97235fb1bb59a4437879460c",
        "f005833e152fa18e30f3c7d8ef2010e2",
        "a4e4347690d3d7381a9878a324561603",
        "344108184c54ab7739e5f29701c15de4",
        "e29a380e1df630b91abee981199f9beb",
    ]:
        results.append({"operation": "move", "ref": event_ref, "result": post("/scraper/agentMoveEvent", {"event_ref": event_ref, "location_ref": "SHOP:labullecafe"})})

    conversions = [
        {
            "event_ref": "907a66348433fece981cd20b803c2e52",
            "experience_type_ref": "cours",
            "principal_activity_category_ref": "culture",
            "target_string_id": "cours-d-espagnol-iberica-seclin",
            "is_active": True,
        },
        {
            "event_ref": "f4f2fb4d2a4a361706164b7303dc5184",
            "experience_type_ref": "visite-guidee",
            "principal_activity_category_ref": "culture",
            "target_string_id": "lille-en-1913-entre-bourse-textiles-et-charbon",
            "is_active": True,
        },
    ]
    for payload in conversions:
        results.append({"operation": "event_to_experience", "ref": payload["event_ref"], "result": post("/scraper/agentEventToExperience", payload)})

    for event_ref in [
        "f8f1209f95b3b396e8c82c7a9cbaf359",
        "f7603ab47c248116349877be8e613074",
        "dbd49d3cdf1ed8611fcbd5ded7e20d1c",
        "7d578ab0d8133a988186cd68ffe0614f",
    ]:
        results.append({"operation": "audit", "ref": event_ref, "result": post("/scraper/agentInspectEventTemporal", {"event_ref": event_ref})})

    REPORT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"success": True, "operations": len(results), "report": str(REPORT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
