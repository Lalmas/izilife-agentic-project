#!/usr/bin/env python3
"""Qualifie les usages de restauration des Shops alimentaires, avec reprise Excel.

Les preuves fortes sont appliquées directement. Les propositions plausibles mais
non certaines alimentent « Autres validations ». Une absence de preuve reste
UNKNOWN et ne crée aucune demande vide.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import urllib3
from openpyxl import Workbook, load_workbook

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from intelligent_enricher import build_apply_payload, load_references, validate_proposal

BASE_URLS = {
    "local": ("https://localhost:4443/izilife-admin", False),
    "staging": ("https://www.staging.izilife.co/izilife-admin", True),
    "prod": ("https://www.izilife.co/izilife-admin", True),
}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
TAGS = {
    "consumption_onsite": {"YES": "consommation-sur-place", "NO": "sans-consommation-sur-place"},
    "restaurant_style": {
        "FAST": "repas-sur-le-pouce",
        "TABLE_SERVICE": "moment-repas-a-table",
        "MIXED": "restauration-mixte",
    },
}
HEADERS = ["shop_id", "shop_string_id", "name", "category", "consumption_onsite",
           "restaurant_style", "confidence", "evidence", "source_url", "decision",
           "validation_request_id", "error", "checked_at"]


class Api:
    def __init__(self, env: str):
        self.base, self.verify = BASE_URLS[env]
        token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
        if not token:
            raise RuntimeError("IZILIFE_AGENT_TOKEN ou AGENT_SECRET_TOKEN absent.")
        self.headers = {"X-Agent-Token": token, "Accept": "application/json"}

    def post(self, endpoint: str, payload: dict[str, Any], form: bool = False) -> dict[str, Any]:
        kwargs = {"data": {"payload": json.dumps(payload, ensure_ascii=False)}} if form else {"json": payload}
        response = requests.post(self.base + endpoint, headers=self.headers, verify=self.verify,
                                 timeout=180, **kwargs)
        try:
            body = response.json()
        except ValueError as exc:
            raise RuntimeError(f"Réponse non JSON HTTP {response.status_code}") from exc
        if response.status_code >= 400 or body.get("success") is False:
            raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
        return body

    def fields(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(self.base + endpoint, data=payload, headers=self.headers,
                                 verify=self.verify, timeout=180)
        try:
            body = response.json()
        except ValueError as exc:
            raise RuntimeError(f"Réponse non JSON HTTP {response.status_code}") from exc
        if response.status_code >= 400 or body.get("success") is False:
            raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
        return body


def workbook(path: Path):
    if path.exists():
        wb = load_workbook(path)
        ws, state = wb["Résultats"], wb["Pilotage"]
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "Résultats"
        ws.append(HEADERS)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = "A1:M1"
        state = wb.create_sheet("Pilotage")
        state.append(["next_after_id", "updated_at"])
        state.append([0, datetime.now().isoformat()])
    return wb, ws, state


def save_row(path: Path, wb, ws, state, row: list[Any], next_id: int) -> None:
    ws.append(row)
    state["A2"], state["B2"] = next_id, datetime.now().isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def proposed_signals(proposal: dict[str, Any], minimum: float, maximum: float = 1.01) -> dict[str, Any]:
    """Convertit une tranche de confiance vers le contrat Autres validations."""
    def selected(item: dict[str, Any]) -> bool:
        try:
            confidence = float(item.get("confidence") or 0)
        except (TypeError, ValueError):
            return False
        return minimum <= confidence < maximum

    return {
        "tags": [item for item in proposal.get("tags") or [] if selected(item)],
        "principal_characteristics": [
            {"name": item.get("field"), "value": item.get("value"),
             "confidence": item.get("confidence"), "evidence": item.get("evidence"),
             "source_url": item.get("source_url")}
            for item in proposal.get("principal_characteristics") or [] if selected(item)
        ],
        "editorial": [dict(item, type=family)
                      for family, items in (proposal.get("editorial") or {}).items()
                      for item in items if selected(item)],
    }


def normalize(proposal: dict[str, Any]) -> tuple[list[str], float, str, str]:
    onsite = str(proposal.get("consumption_onsite") or "UNKNOWN").upper()
    style = str(proposal.get("restaurant_style") or "UNKNOWN").upper()
    try:
        confidence = max(0.0, min(1.0, float(proposal.get("confidence") or 0)))
    except (TypeError, ValueError):
        confidence = 0.0
    if onsite not in {"YES", "NO", "UNKNOWN"}: onsite = "UNKNOWN"
    if style not in {"FAST", "TABLE_SERVICE", "MIXED", "UNKNOWN"}: style = "UNKNOWN"
    evidence = proposal.get("evidence") or []
    evidence_text = " | ".join(str(x.get("text") or "") for x in evidence if isinstance(x, dict)).strip(" |")
    source_url = next((str(x.get("url") or "") for x in evidence if isinstance(x, dict) and x.get("url")), "")
    tags = []
    if onsite in TAGS["consumption_onsite"]: tags.append(TAGS["consumption_onsite"][onsite])
    if style in TAGS["restaurant_style"]: tags.append(TAGS["restaurant_style"][style])
    # Une conclusion négative sans formulation explicite ne doit jamais muter la base.
    if onsite == "NO" and not re.search(r"uniquement|exclusivement|sans (?:salle|place)|à emporter seulement", evidence_text, re.I):
        tags = [tag for tag in tags if tag != "sans-consommation-sur-place"]
        onsite = "UNKNOWN"
    return tags, confidence, evidence_text, source_url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", choices=BASE_URLS, default="local")
    parser.add_argument("--max-id", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--resume-after", type=int,
                        help="Force ponctuellement le curseur de reprise (le classeur reprend ensuite la main).")
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-write", action="store_true")
    parser.add_argument("--auto-threshold", type=float, default=0.92)
    parser.add_argument("--review-threshold", type=float, default=0.60)
    args = parser.parse_args()
    if args.apply and not args.confirm_write:
        parser.error("--apply exige --confirm-write")
    api = Api(args.env)
    refs, _refs_env = load_references(args.env)
    wb, ws, state = workbook(args.workbook)
    after_id = args.resume_after if args.resume_after is not None else int(state["A2"].value or 0)
    inventory = api.post("/scraper/agentFoodCurationCandidates", {
        "after_id": after_id, "max_id": args.max_id, "limit": args.batch_size,
    })
    last_completed_id = after_id
    for item in inventory.get("items") or []:
        onsite = style = "UNKNOWN"
        confidence = 0.0
        evidence = source_url = decision = error = ""
        validation_id: Any = ""
        try:
            analysis = api.post("/scraper/agentAnalyzePlaceEditorial", {
                "scope_type": "SHOP", "scope_ref": item["shop_string_id"],
                "current_izilife": item, "official_pages": [],
                # Global food backfill: the explicitly enabled web search is
                # the source collector; obsolete URL columns are never crawled.
                "with_web_search": True,
            })
            proposal = validate_proposal(analysis.get("proposal") or {}, refs, [])
            all_items = list(proposal.get("tags") or [])
            all_items += list(proposal.get("principal_characteristics") or [])
            all_items += [entry for values in (proposal.get("editorial") or {}).values() for entry in values]
            confidence = max((float(entry.get("confidence") or 0) for entry in all_items), default=0.0)
            evidence = " | ".join(dict.fromkeys(str(entry.get("evidence") or "") for entry in all_items if entry.get("evidence")))
            source_url = next((str(entry.get("source_url") or "") for entry in all_items if entry.get("source_url")), "")
            tag_ids = {str(entry.get("string_id") or "") for entry in proposal.get("tags") or []}
            onsite = "YES" if "consommation-sur-place" in tag_ids else ("NO" if "sans-consommation-sur-place" in tag_ids else "UNKNOWN")
            style = ("MIXED" if "restauration-mixte" in tag_ids else
                     "TABLE_SERVICE" if "moment-repas-a-table" in tag_ids else
                     "FAST" if "repas-sur-le-pouce" in tag_ids else "UNKNOWN")
            apply_payload = build_apply_payload(proposal, "SHOP", item["shop_string_id"], args.auto_threshold)
            apply_payload["tags"] = [tag for tag in apply_payload["tags"] if tag not in set(item.get("current_tags") or [])]
            has_strong = bool(apply_payload["tags"] or apply_payload["principal_characteristics"] or
                              any(apply_payload["editorial"].values()))
            weak = proposed_signals(proposal, args.review_threshold, args.auto_threshold)
            has_weak = any(weak.values())
            if not has_strong and not has_weak:
                decision = "UNKNOWN_OR_ALREADY_DONE"
            elif args.apply:
                if has_strong:
                    api.post("/scraper/agentApplyTagsAndCharacts", apply_payload, form=True)
                if has_weak:
                    response = api.post("/scraper/agentSubmitEnrichment", {
                        "entity_type": "SHOP", "entity_id": int(item["id"]),
                        "agent_name": "food_usage_classifier",
                        "proposed_payload": {"_type": "EDITORIAL_SIGNALS", "signals": weak},
                        "source_url": source_url or None, "confidence_score": confidence,
                    })
                    validation_id = response.get("validation_request_id") or ""
                decision = "APPLIED_WITH_REVIEW" if has_strong and has_weak else ("APPLIED" if has_strong else "PENDING_REVIEW")
            elif has_strong:
                decision = "PROPOSED_STRONG"
            else:
                decision = "PROPOSED_FOR_REVIEW"
        except Exception as exc:
            error, decision = str(exc), "ERROR"
        # Une erreur ne doit jamais faire avancer le curseur : le prochain
        # lancement doit reprendre cet objet, et non le perdre définitivement.
        checkpoint_id = last_completed_id if decision == "ERROR" else int(item["id"])
        save_row(args.workbook, wb, ws, state, [
            item["id"], item["shop_string_id"], item["name"], item.get("category_ref"),
            onsite, style, confidence, evidence, source_url, decision, validation_id,
            error, datetime.now().isoformat(),
        ], checkpoint_id)
        print(f"SHOP #{item['id']} {item['shop_string_id']}: {decision}", flush=True)
        if decision == "ERROR":
            break
        last_completed_id = int(item["id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
