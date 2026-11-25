#!/usr/bin/env python3
"""Finalise et vérifie les fiches côtières local/staging vers production."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import requests

from curation_sync import (
    APPLY_ENDPOINT,
    LOCATION_MAINTENANCE_ENDPOINT,
    PLAN_ENDPOINT,
    Inspector,
    ENVIRONMENTS,
)


COASTAL_LOCAL_CITY_IDS = {259, 260, 261, 262, 263, 845, 1538}
REPORT_DIR = Path(__file__).resolve().parent


def maintain(api: Inspector, payload: dict) -> dict:
    cfg = ENVIRONMENTS["prod"]
    response = requests.post(
        cfg["base_url"] + LOCATION_MAINTENANCE_ENDPOINT,
        data={"payload": json.dumps(payload, ensure_ascii=False)},
        headers={"X-Agent-Token": api.token, "Accept": "application/json"},
        timeout=api.timeout,
        verify=cfg["verify_ssl"],
    )
    try:
        result = response.json()
    except ValueError:
        result = {"success": False, "error": response.text[:500]}
    result["http_status"] = response.status_code
    return result


def by_google(items: list[dict]) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    for item in items:
        google_id = str(item.get("google_place_id") or "").strip()
        if google_id:
            result.setdefault(google_id, []).append(item)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN manquant")

    api = Inspector(token, args.timeout)
    local = api.list_google_scopes("local")
    prod = api.list_google_scopes("prod")
    prod_google = by_google(prod)
    coastal = [
        item for item in local
        if int(item.get("city_id") or 0) in COASTAL_LOCAL_CITY_IDS
        and str(item.get("is_active")) == "1"
        and str(item.get("listable")) == "1"
    ]
    report = {
        "created_at": datetime.now().isoformat(),
        "apply": args.apply,
        "source_count": len(coastal),
        "existing": [],
        "missing": [],
        "actions": [],
        "collisions": [],
    }
    collision_plan = {
        "format": "izilife-curation-plan-v1",
        "created_at": datetime.now().isoformat(),
        "destination_env": "prod",
        "targets": {},
    }

    for source in coastal:
        google_id = str(source.get("google_place_id") or "").strip()
        matches = prod_google.get(google_id, [])
        if matches:
            preferred = next(
                (item for item in matches if item.get("scope_ref") == source.get("scope_ref")),
                matches[0],
            )
            report["existing"].append({"source": source, "destination": preferred, "duplicates": matches[1:]})
            if args.apply and (str(preferred.get("is_active")) != "1" or str(preferred.get("listable")) != "1"):
                result = maintain(api, {
                    "scope_type": preferred["scope_type"],
                    "scope_ref": preferred["scope_ref"],
                    "is_active": "1",
                    "listable": "1",
                })
                report["actions"].append({"action": "ACTIVATE", "scope": preferred, "result": result})
            continue

        # Une fiche peut déjà exister par référence après un ancien import qui n'a
        # pas conservé le Google Place ID. On la recherche avant toute création.
        prod_by_ref = api.inspect("prod", {
            "scope_type": source["scope_type"],
            "scope_ref": source["scope_ref"],
        })
        graph = prod_by_ref.get("graph") if prod_by_ref.get("match_status") == "MATCHED" else None
        if graph:
            identity = graph.get("identity") or {}
            destination_google = str(identity.get("google_place_id") or "").strip()
            if destination_google and destination_google != google_id:
                source_result = api.inspect("local", {
                    "scope_type": source["scope_type"],
                    "scope_ref": source["scope_ref"],
                })
                source_graph = source_result.get("graph") or {}
                city_ref = str((source_graph.get("identity") or {}).get("city_ref") or "").strip()
                destination_ref = f"{source['scope_ref']}-{city_ref}"
                collision = {
                    "source": source,
                    "occupied_destination": identity,
                    "destination_ref": destination_ref,
                }
                report["collisions"].append(collision)
                if args.apply:
                    # Cette fiche homonyme était inactive avant cette opération :
                    # annule l'activation erronée, sans toucher à ses autres données.
                    reverted = maintain(api, {
                        "scope_type": identity["scope_type"],
                        "scope_ref": identity["scope_ref"],
                        "is_active": "0",
                        "listable": "0",
                    })
                    report["actions"].append({"action": "REVERT_COLLISION", "scope": identity, "result": reverted})
                unique_result = api.inspect("prod", {
                    "scope_type": source["scope_type"],
                    "scope_ref": destination_ref,
                })
                if unique_result.get("match_status") == "MATCHED":
                    unique_identity = (unique_result.get("graph") or {}).get("identity") or {}
                    report["existing"].append({"source": source, "destination": unique_identity, "match": "collision_ref"})
                    if args.apply:
                        activated = maintain(api, {
                            "scope_type": unique_identity["scope_type"],
                            "scope_ref": unique_identity["scope_ref"],
                            "is_active": "1",
                            "listable": "1",
                        })
                        report["actions"].append({"action": "ACTIVATE_COLLISION_TARGET", "scope": unique_identity, "result": activated})
                    continue
                payload = {
                    "destination_type": source["scope_type"],
                    "destination_ref": destination_ref,
                    "allow_create": True,
                    "policies": {
                        "media": "INCLUDE", "external_media": "INCLUDE", "links": "INCLUDE",
                        "ambiances": "INCLUDE", "characteristics": "INCLUDE", "products": "INCLUDE",
                        "product_options": "INCLUDE", "equipment": "INCLUDE", "services": "INCLUDE",
                        "eap": "INCLUDE", "hours": "INCLUDE",
                    },
                    "graph": source_graph,
                }
                planned = api.post("prod", PLAN_ENDPOINT, payload)
                collision_plan["targets"][destination_ref] = {
                    "status": "PLANNED" if (planned.get("plan") or {}).get("can_apply") else "ERROR",
                    "source_origins": {name: "local" for name in payload["policies"]},
                    "source_scopes": {"local": source_graph.get("identity") or {}},
                    "payload": payload,
                    "server_plan": planned.get("plan"),
                    "error": planned.get("error"),
                }
                continue
            report["existing"].append({"source": source, "destination": identity, "match": "scope_ref"})
            if args.apply:
                result = maintain(api, {
                    "scope_type": identity["scope_type"],
                    "scope_ref": identity["scope_ref"],
                    "is_active": "1",
                    "listable": "1",
                })
                report["actions"].append({"action": "ACTIVATE", "scope": identity, "result": result})
            continue

        report["missing"].append(source)
        if not args.apply:
            continue
        source_result = api.inspect("local", {
            "scope_type": source["scope_type"],
            "scope_ref": source["scope_ref"],
        })
        source_graph = source_result.get("graph") or {}
        payload = {
            "destination_type": source["scope_type"],
            "destination_ref": source["scope_ref"],
            "allow_create": True,
            "policies": {
                "media": "INCLUDE", "external_media": "INCLUDE", "links": "INCLUDE",
                "ambiances": "INCLUDE", "characteristics": "INCLUDE", "products": "INCLUDE",
                "product_options": "INCLUDE", "equipment": "INCLUDE", "services": "INCLUDE",
                "eap": "INCLUDE", "hours": "INCLUDE",
            },
            "graph": source_graph,
        }
        planned = api.post("prod", PLAN_ENDPOINT, payload)
        plan = planned.get("plan") or {}
        if not plan.get("can_apply"):
            report["actions"].append({"action": "CREATE_BLOCKED", "scope": source, "result": planned})
            continue
        payload.update({
            "plan_hash": plan["plan_hash"],
            "confirm_apply": "CURATION_SYNC_APPLY",
            "idempotency_key": f"prod:coastal:{source['scope_type']}:{source['scope_ref']}:{plan['plan_hash'][:24]}",
        })
        created = api.post("prod", APPLY_ENDPOINT, payload)
        report["actions"].append({"action": "CREATE", "scope": source, "result": created})
        if created.get("success"):
            activated = maintain(api, {
                "scope_type": source["scope_type"],
                "scope_ref": source["scope_ref"],
                "is_active": "1",
                "listable": "1",
            })
            report["actions"].append({"action": "ACTIVATE_CREATED", "scope": source, "result": activated})

    suffix = "apply" if args.apply else "audit"
    output = REPORT_DIR / f"coastal-prod-{suffix}-{datetime.now():%Y%m%d-%H%M%S}.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    plan_output = None
    if collision_plan["targets"]:
        plan_output = REPORT_DIR / f"coastal-prod-collisions-plan-{datetime.now():%Y%m%d-%H%M%S}.json"
        plan_output.write_text(json.dumps(collision_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "report": str(output),
        "source_count": len(coastal),
        "existing": len(report["existing"]),
        "missing": len(report["missing"]),
        "actions": len(report["actions"]),
        "collisions": len(report["collisions"]),
        "collision_plan": str(plan_output) if plan_output else None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
