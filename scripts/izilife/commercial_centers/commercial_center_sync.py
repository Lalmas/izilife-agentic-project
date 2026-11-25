"""Planifie puis synchronise automatiquement les commerces d'un centre.

Le plan est sans écriture. L'application exige son SHA-256 et une confirmation
supplémentaire en production. Les cartes marquées hors centre sont exclues.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


ENVIRONMENTS = {
    "local": ("https://localhost:4443/izilife-admin", False),
    "staging": ("https://www.staging.izilife.co/izilife-admin", True),
    "prod": ("https://www.izilife.co/izilife-admin", True),
}
RESOLVE_ENDPOINT = "/scraper/agentInternalDataV0ResolvePlace"
INSPECT_ENDPOINT = "/scraper/agentCurationSyncInspect"
IMPORT_ENDPOINT = "/scraper/agentFetchAndStoreOnePlace/{city}"
OFFICIAL_SHOP_ENDPOINT = "/scraper/agentCreateOfficialCommercialCenterShop"
CENTER_CITY = {"AUSHOPPING V2": "villeneuve-d-ascq", "LILLENIUM": "lille"}
CENTER_ADDRESS_MARKERS = {
    "AUSHOPPING V2": ("aushopping", "centre-commercial-v2", "cc-v2", "bd-de-valmy", "boulevard-de-valmy"),
    "LILLENIUM": ("lillenium", "faubourg-des-postes", "rue-simons", "genevieve-anthonioz-de-gaulle"),
}


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(c for c in value if not unicodedata.combining(c)).lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def official_category(row: dict[str, Any]) -> str:
    categories = {slug(str(value)) for value in row.get("source_categories") or []}
    name = slug(str(row.get("name") or ""))
    if "restaurant" in str(row.get("source_kind") or "").lower() or categories & {"restaurant", "restauration"}:
        return "restaurant"
    if categories & {"mode-femme", "mode-homme", "mode-enfant", "mode", "vetements"}:
        return "magasin-de-vetements"
    if categories & {"chaussures", "mode-chaussures"}:
        return "magasin-de-chaussures"
    if categories & {"beaute", "parfumerie"}:
        return "institut-de-beaute"
    if categories & {"bijoux", "bijouterie"}:
        return "bijouterie"
    if categories & {"optique", "sante-optique"} or "optical" in name or "optique" in name:
        return "opticien"
    return "boutique"


def plan_official_shop(api: Api, row: dict[str, Any], city: str, center_ref: str) -> dict[str, Any]:
    payload = {
        "name": row["name"], "city": city, "in_on_place_ref": center_ref,
        "source_url": row.get("source_url"), "category_string_id": official_category(row),
        "dry_run": True,
    }
    result = api.post(OFFICIAL_SHOP_ENDPOINT, payload)
    if result.get("success"):
        if result.get("status") == "already_attached":
            return {"action": "ALREADY_ATTACHED", "existing": result.get("item"), "official_plan": result}
        return {"action": "CREATE_OR_ATTACH_OFFICIAL", "official_plan": result, "category_string_id": payload["category_string_id"]}
    return {"action": "NO_CERTAIN_GOOGLE_MATCH", "official_error": result}


class Api:
    def __init__(self, env: str, timeout: int):
        token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
        if not token:
            raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
        self.base, self.verify = ENVIRONMENTS[env]
        self.timeout = timeout
        self.headers = {"X-Agent-Token": token, "Accept": "application/json"}

    def post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            self.base + endpoint, json=payload, headers=self.headers,
            timeout=self.timeout, verify=self.verify,
        )
        try:
            body = response.json()
        except ValueError:
            body = {"success": False, "error": response.text[:500] or "Réponse non JSON"}
        body["http_status"] = response.status_code
        return body


def belongs_to_center(name: str, address: str, city: str, center: str) -> bool:
    searchable = slug(f"{name} {address}")
    return slug(city) in slug(address) and any(marker in searchable for marker in CENTER_ADDRESS_MARKERS[center])


def choose_google_candidate(name: str, candidates: list[dict[str, Any]], city: str, center: str) -> dict[str, Any] | None:
    wanted = slug(name)
    scored = []
    for candidate in candidates:
        candidate_name = slug(str(candidate.get("name") or ""))
        address = slug(str(candidate.get("address") or ""))
        if not belongs_to_center(candidate_name, address, city, center):
            continue
        score = 100 if candidate_name == wanted else 0
        if wanted and (wanted in candidate_name or candidate_name in wanted):
            score = max(score, 90)
        if slug(city) in address:
            score += 5
        scored.append((score, candidate))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1] if scored and scored[0][0] >= 90 else None


def inspect_existing(api: Api, candidate: dict[str, Any], center_ref: str, center_id: int,
                     city: str, center: str) -> dict[str, Any]:
    scope_type = str(candidate.get("type") or "SHOP").upper()
    result = api.post(INSPECT_ENDPOINT, {
        "scope_type": scope_type, "scope_ref": candidate.get("string_id"),
    })
    identity = ((result.get("graph") or {}).get("identity") or {})
    if not belongs_to_center(
        str(identity.get("name") or candidate.get("name") or ""),
        " ".join(str(identity.get(field) or "") for field in ("address", "additional_address", "city_ref")),
        city,
        center,
    ):
        return {"action": "REJECT_EXISTING_OUTSIDE_CENTER", "existing": candidate, "identity": identity}
    parent = str(identity.get("in_on_place_ref") or identity.get("in_on_place") or "")
    if parent in {center_ref, str(center_id)}:
        action = "ALREADY_ATTACHED_PLACE" if scope_type == "PLACE" else "ALREADY_ATTACHED"
    elif parent not in {"", "0", "None"}:
        action = "CONFLICT_OTHER_CENTER"
    elif scope_type == "PLACE":
        action = "PLACE_REQUIRES_PARENT_REVIEW"
    else:
        action = "ATTACH_EXISTING"
    return {"action": action, "existing": candidate, "identity": identity}


def build_plan(inventory: dict[str, Any], api: Api, env: str, centers: set[str]) -> dict[str, Any]:
    actions = []
    selected_google_ids: dict[tuple[str, str], str] = {}
    center_ids: dict[str, int] = {}
    for center in centers:
        center_ref = "aushopping-v2" if center == "AUSHOPPING V2" else "lillenium"
        inspected = api.post(INSPECT_ENDPOINT, {"scope_type": "PLACE", "scope_ref": center_ref})
        identity = ((inspected.get("graph") or {}).get("identity") or {})
        center_ids[center] = int(identity.get("source_id") or identity.get("id") or 0)
        if not center_ids[center]:
            raise RuntimeError(f"Place centre introuvable: {center_ref}")
    for row in inventory.get("commerces") or []:
        center = str(row.get("center") or "")
        if center not in centers or not row.get("inside_center"):
            continue
        center_ref = str(row.get("center_scope_ref") or "")
        city = CENTER_CITY[center]
        top = (row.get("candidates") or [None])[0]
        decision = None
        if top and int(top.get("score") or 0) >= 100:
            decision = inspect_existing(api, top, center_ref, center_ids[center], city, center)
            if decision.get("action") == "REJECT_EXISTING_OUTSIDE_CENTER":
                decision = None
        if decision is None:
            resolution = api.post(RESOLVE_ENDPOINT, {
                "query": row["name"], "city": city, "continue_to_google": True,
            })
            if resolution.get("status") == "found" and (resolution.get("item") or {}).get("type") in {"SHOP", "PLACE"}:
                decision = inspect_existing(api, resolution["item"], center_ref, center_ids[center], city, center)
                if decision.get("action") == "REJECT_EXISTING_OUTSIDE_CENTER":
                    decision = plan_official_shop(api, row, city, center_ref)
                    decision["resolution"] = resolution
            elif resolution.get("status") == "google_candidates":
                selected = choose_google_candidate(row["name"], resolution.get("candidates") or [], city, center)
                if selected:
                    existing_by_google = api.post(RESOLVE_ENDPOINT, {
                        "google_place_id": selected.get("google_place_id"),
                    })
                    if existing_by_google.get("status") == "found" and (existing_by_google.get("item") or {}).get("type") in {"SHOP", "PLACE"}:
                        decision = inspect_existing(api, existing_by_google["item"], center_ref, center_ids[center], city, center)
                    else:
                        decision = {
                            "action": "CREATE_OR_ATTACH_GOOGLE", "google": selected,
                            "category_string_id": official_category(row),
                        }
                else:
                    decision = plan_official_shop(api, row, city, center_ref)
                    decision["resolution"] = resolution
            else:
                decision = plan_official_shop(api, row, city, center_ref)
                decision["resolution"] = resolution
        if decision.get("action") == "NO_CERTAIN_GOOGLE_MATCH":
            candidates = (decision.get("official_error") or {}).get("candidates") or []
            attached = [candidate for candidate in candidates if str(candidate.get("in_on_place") or "") == str(center_ids[center])]
            if len(attached) == 1:
                decision = {"action": "ALREADY_ATTACHED", "existing": attached[0]}
        google_id = str((decision.get("google") or {}).get("google_place_id") or "")
        duplicate_key = (center_ref, google_id)
        if google_id and duplicate_key in selected_google_ids:
            decision = {
                "action": "DUPLICATE_INVENTORY",
                "duplicate_of": selected_google_ids[duplicate_key],
                "google_place_id": google_id,
            }
        elif google_id:
            selected_google_ids[duplicate_key] = str(row["name"])
        actions.append({
            "center": center, "center_ref": center_ref, "city": city,
            "name": row["name"], "source_url": row.get("source_url"), **decision,
        })
    payload = {
        "format": "izilife-commercial-center-plan-v1", "env": env,
        "created_at": datetime.now().isoformat(), "centers": sorted(centers), "actions": actions,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["plan_hash"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def apply_plan(plan: dict[str, Any], api: Api) -> dict[str, Any]:
    results = []
    for action in plan.get("actions") or []:
        kind = action.get("action")
        if kind in {"ALREADY_ATTACHED", "ALREADY_ATTACHED_PLACE"}:
            results.append({"name": action["name"], "status": kind})
            continue
        if kind == "CREATE_OR_ATTACH_OFFICIAL":
            official_plan = action.get("official_plan") or {}
            payload = {
                "name": action["name"], "city": action["city"], "in_on_place_ref": action["center_ref"],
                "source_url": action.get("source_url"), "category_string_id": action.get("category_string_id") or "boutique",
                "dry_run": False, "confirm": "CREATE_OFFICIAL_COMMERCIAL_CENTER_SHOP",
                "plan_hash": official_plan.get("plan_hash"),
            }
            result = api.post(OFFICIAL_SHOP_ENDPOINT, payload)
            results.append({"name": action["name"], "status": "OK" if result.get("success") else "ERROR", "result": result})
            continue
        if kind not in {"ATTACH_EXISTING", "CREATE_OR_ATTACH_GOOGLE"}:
            results.append({"name": action["name"], "status": "SKIPPED", "reason": kind})
            continue
        payload = {"query": action["name"], "in_on_place_ref": action["center_ref"]}
        google = action.get("google") or {}
        if kind == "ATTACH_EXISTING" and (action.get("identity") or {}).get("google_place_id"):
            google = {"google_place_id": action["identity"]["google_place_id"]}
        if google.get("google_place_id"):
            payload["google_place_id_hint"] = google["google_place_id"]
            payload["destination"] = "SHOP"
            payload["category_string_id"] = action.get("category_string_id") or "boutique"
        result = api.post(IMPORT_ENDPOINT.format(city=action["city"]), payload)
        results.append({"name": action["name"], "status": "OK" if result.get("success") else "ERROR", "result": result})
    return {"format": "izilife-commercial-center-apply-v1", "plan_hash": plan["plan_hash"],
            "applied_at": datetime.now().isoformat(), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("--inventory", type=Path, required=True)
    plan_cmd.add_argument("--env", choices=ENVIRONMENTS, required=True)
    plan_cmd.add_argument("--center", action="append", choices=CENTER_CITY, required=True)
    plan_cmd.add_argument("--output", type=Path, required=True)
    plan_cmd.add_argument("--timeout", type=int, default=90)
    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("--plan", type=Path, required=True)
    apply_cmd.add_argument("--confirm", required=True)
    apply_cmd.add_argument("--confirm-production")
    apply_cmd.add_argument("--journal", type=Path, required=True)
    apply_cmd.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    if args.command == "plan":
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        plan = build_plan(inventory, Api(args.env, args.timeout), args.env, set(args.center))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        counts: dict[str, int] = {}
        for item in plan["actions"]:
            counts[item["action"]] = counts.get(item["action"], 0) + 1
        print(json.dumps({"plan_hash": plan["plan_hash"], "counts": counts, "output": str(args.output)}, ensure_ascii=False, indent=2))
        return 0
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if args.confirm != plan.get("plan_hash"):
        raise RuntimeError("Hash de confirmation différent du plan.")
    if plan.get("env") == "prod" and args.confirm_production != "I_CONFIRM_PRODUCTION_COMMERCIAL_CENTERS":
        raise RuntimeError("Confirmation production manquante.")
    journal = apply_plan(plan, Api(str(plan["env"]), args.timeout))
    args.journal.parent.mkdir(parents=True, exist_ok=True)
    args.journal.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
    errors = sum(item["status"] == "ERROR" for item in journal["results"])
    print(json.dumps({"errors": errors, "journal": str(args.journal)}, ensure_ascii=False))
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
