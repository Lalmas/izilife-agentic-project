"""One-shot production repair for generic EventCategory and missing APC.

Stored exact references are applied first without AI. Remaining candidates can
then be analyzed once by the deployed validator. Every result is checkpointed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPTS = Path(r"C:\Users\alcamara\Documents\agentic_Workspace\tmp\event-quality-one-shot\scripts")
sys.path.insert(0, str(SCRIPTS))
from core.paths import IZILIFE_ENVS  # noqa: E402
from izilife.events.backfill_active_event_taxonomy import (  # noqa: E402
    TaxonomyClient, fetch_source_text, has_occurrence_doubt,
)

GENERIC_FORMATS = {
    "atelier", "workshop", "cours", "stage", "masterclass", "salon", "congres",
    "convention", "seminaire", "conference", "conference-debat", "table-ronde",
    "concours", "retraite", "sejour", "autre-festival",
}
REF_KEYS = (
    "event_category_ref", "event_category_string_id",
    "principal_activity_category_string_id", "sport_string_id",
    "dance_string_id", "music_style_string_id", "artisan_technique_string_id",
)


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def stored_proposal(event: dict[str, Any]) -> dict[str, Any]:
    raw = event.get("scrapping_json")
    try:
        parsed = json.loads(raw) if isinstance(raw, str) else (raw or {})
    except (TypeError, ValueError):
        parsed = {}
    result: dict[str, Any] = {}
    for obj in walk(parsed):
        for key in REF_KEYS:
            value = obj.get(key)
            if value not in (None, "", [], {}) and key not in result:
                result[key] = value
    if "event_category_ref" not in result and "event_category_string_id" in result:
        result["event_category_ref"] = result.pop("event_category_string_id")
    return result


def is_real_target(event: dict[str, Any]) -> bool:
    ref = str(event.get("event_category_string_id") or "").strip().lower()
    if ref == "rencontre":
        return True
    missing_apc = not event.get("principal_activity_category")
    return missing_apc and ref in GENERIC_FORMATS


def save(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("deterministic", "llm"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=Path, help="Rapport déterministe; en mode LLM, limite aux needs_llm.")
    parser.add_argument("--exclude", type=Path, action="append", default=[], help="Rapports LLM déjà exécutés; aucun rappel.")
    parser.add_argument("--min-confidence", type=float, default=.90)
    args = parser.parse_args()
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN absent")
    env = IZILIFE_ENVS["prod"]
    client = TaxonomyClient(env["base_url"], token, env["verify_ssl"])
    state = json.loads(args.output.read_text(encoding="utf-8")) if args.output.exists() else {
        "started_at": datetime.now().astimezone().isoformat(), "mode": args.mode,
        "results": [],
    }
    done = {int(row["event_id"]) for row in state["results"] if row.get("event_id")}
    candidates = [row for row in client.candidates(2000) if is_real_target(row)]
    if args.mode == "llm" and args.seed:
        seed = json.loads(args.seed.read_text(encoding="utf-8"))
        allowed = {int(row["event_id"]) for row in seed.get("results", []) if row.get("status") == "needs_llm"}
        candidates = [row for row in candidates if int(row["id"]) in allowed]
    if args.mode == "llm" and args.exclude:
        excluded: set[int] = set()
        for report in args.exclude:
            previous = json.loads(report.read_text(encoding="utf-8"))
            excluded |= {int(row["event_id"]) for row in previous.get("results", []) if row.get("event_id")}
        candidates = [row for row in candidates if int(row["id"]) not in excluded]
    state["candidate_count"] = len(candidates)
    for event in candidates:
        event_id = int(event["id"])
        if event_id in done:
            continue
        result = {"event_id": event_id, "title": event.get("title"), "status": "skipped"}
        try:
            if args.mode == "deterministic":
                proposal = stored_proposal(event)
                if not proposal:
                    result["status"] = "needs_llm"
                else:
                    result["proposal"] = proposal
                    response = client.apply_taxonomy(event_id, proposal, False)
                    result["updates"] = response.get("updates") or {}
                    result["status"] = "applied_stored" if result["updates"] else "needs_llm"
            else:
                proposal = client.analyze(event, fetch_source_text(str(event.get("scrapped_from") or ""), env["verify_ssl"]))
                result["proposal"] = proposal
                confidence = float(proposal.get("confidence") or 0)
                if confidence < args.min_confidence:
                    result["status"] = "low_confidence"
                elif has_occurrence_doubt(proposal):
                    result["status"] = "occurrence_blocked"
                else:
                    response = client.apply_taxonomy(event_id, proposal, False)
                    result["updates"] = response.get("updates") or {}
                    result["status"] = "applied_llm" if result["updates"] else "llm_no_change"
        except Exception as exc:
            result["status"] = "error"
            result["error"] = str(exc)
        state["results"].append(result)
        save(args.output, state)
        print(json.dumps({"event_id": event_id, "status": result["status"], "updates": result.get("updates", {})}, ensure_ascii=False), flush=True)
    state["finished_at"] = datetime.now().astimezone().isoformat()
    counts: dict[str, int] = {}
    for row in state["results"]:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    state["counts"] = counts
    save(args.output, state)
    print(json.dumps({"candidate_count": len(candidates), "counts": counts}, ensure_ascii=False), flush=True)
    return 1 if counts.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
