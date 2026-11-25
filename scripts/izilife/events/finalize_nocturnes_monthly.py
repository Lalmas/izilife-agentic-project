#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os

import requests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="prod")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    bases = {
        "local": "https://localhost:4443/izilife-admin",
        "staging": "https://www.staging.izilife.co/izilife-admin",
        "prod": "https://www.izilife.co/izilife-admin",
    }
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN absent")
    package = {
        "schema_version": "izi.event.package.v1",
        "package_kind": "EDITORIAL_AGENDA",
        "publication": {"activate": True},
        "events": [{
            "client_ref": "nocturnes-1000-morceaux-monthly",
            "existing_ref": "f7603ab47c248116349877be8e613074",
            "relation": "STANDALONE",
            "update_mode": "OVERWRITE",
            "data": {
                "title": "Nocturnes « 1000 Morceaux »",
                "description": "Rendez-vous nocturne gratuit du LaM mêlant scène ouverte, performance contemporaine et DJ set.",
                "event_category_ref": "soiree",
                "start_date": "2026-11-04",
                "start_hour": "19:00",
                "end_date": "2026-11-04",
                "end_hour": "23:00",
                "city_ref": "villeneuve-d-ascq",
                "location_ref": "PLACE:lam-lille-metreopole-musee-dart-moderne",
                "source_url": "https://www.musee-lam.fr/fr/nocturnes-1000-morceaux",
                "is_free_event": True,
                "access_type_ref": "libre-et-gratuit",
            },
            "recurrence": {
                "rrule": "FREQ=MONTHLY;INTERVAL=1;BYDAY=1WE",
                "until_date": "2027-06-02",
                "horizon_days": 240,
            },
            "hourlies": [],
            "programming": [],
            "sources": [{"url": "https://www.musee-lam.fr/fr/nocturnes-1000-morceaux"}],
            "media": [],
        }],
    }
    response = requests.post(
        bases[args.env] + "/scraper/agentIngestEventPackage",
        data={"payload": json.dumps(package, ensure_ascii=False), "dry_run": "1" if args.dry_run else "0"},
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        timeout=180,
        verify=args.env != "local",
    )
    body = response.json()
    print(json.dumps(body, ensure_ascii=False, indent=2))
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
