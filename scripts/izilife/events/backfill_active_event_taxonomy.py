"""One-shot taxonomy repair for future active LocalEvents.

Review is the default and performs no write.  Apply only fills currently empty
APC/sport/dance/music-style foreign keys; the server rejects every other field.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any

import requests
import urllib3

from core.paths import IZILIFE_ENVS, local_agent_workspace_root


def fetch_source_text(url: str, verify_ssl: bool) -> str:
    if not re.match(r"^https?://", str(url), re.I):
        return ""
    try:
        response = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0 (compatible; iziLifeEventBackfill/1.0)"},
            timeout=20, verify=verify_ssl,
        )
        if response.status_code >= 400:
            return ""
        text = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", " ", response.text)
        return re.sub(r"\s+", " ", unescape(re.sub(r"(?s)<[^>]+>", " ", text))).strip()[:24000]
    except requests.RequestException:
        return ""


class EventValidatorClient:
    def __init__(self, base_url: str, token: str, verify_ssl: bool):
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl
        self.headers = {"X-Agent-Token": token, "Content-Type": "application/json"}

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            self.base_url + path, headers=self.headers, json=payload,
            verify=self.verify_ssl, timeout=180,
        )
        try:
            body = response.json()
        except ValueError as exc:
            raise RuntimeError(f"HTTP {response.status_code}: réponse non JSON") from exc
        if response.status_code >= 400 or not body.get("success"):
            raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
        return body


class TaxonomyClient(EventValidatorClient):
    def candidates(self, limit: int, event_id: int | None = None) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {"limit": limit}
        if event_id:
            payload["event_id"] = event_id
        return self.post("/scraper/agentActiveEventTaxonomyCandidates", payload)["events"]

    def analyze(self, event: dict[str, Any], source_text: str) -> dict[str, Any]:
        return self.post("/scraper/agentAnalyzeActiveEventTaxonomy", {
            "event_id": int(event["id"]), "source_text": source_text,
        })["proposal"]

    def apply_taxonomy(self, event_id: int, proposal: dict[str, Any], dry_run: bool) -> dict[str, Any]:
        return self.post("/scraper/agentApplyActiveEventTaxonomy", {
            "event_id": event_id, "proposal": proposal, "dry_run": dry_run,
        })

    def quality_candidates(self, limit: int, event_id: int | None = None) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {"limit": limit}
        if event_id:
            payload["event_id"] = event_id
        return self.post("/scraper/agentActiveEventQualityCandidates", payload)["events"]

    def recover_representation_media(self, representation_id: int, dry_run: bool) -> dict[str, Any]:
        return self.post("/scraper/agentRecoverRepresentationMedia", {
            "representation_id": representation_id, "dry_run": dry_run,
        })

    def repair_event_pricing(self, event_id: int, dry_run: bool) -> dict[str, Any]:
        return self.post("/scraper/agentRepairActiveEventPricing", {
            "event_id": event_id, "dry_run": dry_run,
        })["result"]

    def archive_duplicate(self, duplicate_event_id: int, keeper_event_id: int, dry_run: bool) -> dict[str, Any]:
        return self.post("/scraper/agentArchiveDuplicateEvent", {
            "duplicate_event_id": duplicate_event_id,
            "keeper_event_id": keeper_event_id,
            "dry_run": dry_run,
        })["result"]


def has_occurrence_doubt(proposal: dict[str, Any]) -> bool:
    for doubt in proposal.get("doubts") or []:
        if isinstance(doubt, dict) and str(doubt.get("field") or "").lower() == "occurrences":
            return True
    return False


def _event_completeness(event: dict[str, Any]) -> int:
    """Only ranks duplicate candidates; it never decides identity by itself."""
    score = 0
    for field in ("description", "access_link", "scrapped_from", "scrapping_json"):
        if str(event.get(field) or "").strip():
            score += 1
    if event.get("basic_price") not in (None, ""):
        score += 1
    if int(event.get("event_media_count") or 0) > 0:
        score += 2
    return score


def build_duplicate_pairs(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse the symmetric audit output into actionable, linked pairs."""
    by_id = {int(row["id"]): row for row in events if row.get("id")}
    pairs: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for event in events:
        event_id = int(event.get("id") or 0)
        for candidate in (event.get("quality_evidence") or {}).get("duplicate_candidates") or []:
            candidate_id = int(candidate.get("event_id") or 0)
            key = tuple(sorted((event_id, candidate_id)))
            if event_id < 1 or candidate_id < 1 or key in seen:
                continue
            seen.add(key)
            other = by_id.get(candidate_id, {})
            conflicts = []
            for field in ("event_start_hour", "event_end_hour", "basic_price", "is_free_event", "access_link"):
                left, right = event.get(field), other.get(field)
                if left not in (None, "") and right not in (None, "") and str(left) != str(right):
                    conflicts.append(field)
            left_score, right_score = _event_completeness(event), _event_completeness(other)
            if right_score > left_score or (right_score == left_score and candidate_id < event_id):
                keeper, duplicate = other, event
            else:
                keeper, duplicate = event, other
            certainty = str(candidate.get("certainty") or "probable")
            pairs.append({
                "pair": list(key), "certainty": certainty, "similarity": candidate.get("similarity"),
                "data_conflicts": conflicts,
                "recommended_keeper": {"event_id": int(keeper.get("id") or 0), "title": keeper.get("title"),
                    "bo_url": keeper.get("bo_url"), "completeness_score": max(left_score, right_score)},
                "recommended_duplicate": {"event_id": int(duplicate.get("id") or 0), "title": duplicate.get("title"),
                    "bo_url": duplicate.get("bo_url")},
                "decision": "ready_to_archive_duplicate"
                    if certainty == "certain" and not conflicts else "manual_merge_required",
            })
    return pairs


def filter_quality_events(events: list[dict[str, Any]], focus: str) -> list[dict[str, Any]]:
    """Expose the consolidated audit as distinct one-shot operational agents."""
    if focus == "all":
        return events
    reason_sets = {
        "duplicates": {"probable_semantic_duplicate"},
        "representation-media": {
            "representation_media_recoverable_from_event_tmp", "representation_media_missing",
        },
        "paid-without-link": {"paid_without_access_link"},
        "false-free": {
            "false_free_with_commercial_evidence", "free_without_explicit_evidence",
        },
        "pricing": {
            "false_free_with_commercial_evidence", "free_without_explicit_evidence",
            "paid_without_access_link", "paid_or_unknown_without_price_and_link",
        },
    }
    wanted = reason_sets[focus]
    return [row for row in events if wanted.intersection(row.get("quality_reasons") or [])]


def run(args: argparse.Namespace) -> dict[str, Any]:
    env = IZILIFE_ENVS[args.env]
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN non défini.")
    if not env["verify_ssl"]:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    client = TaxonomyClient(env["base_url"], token, env["verify_ssl"])
    report: dict[str, Any] = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "environment": args.env, "mode": args.mode, "events": [],
        "quality_events": [], "duplicate_pairs": [], "duplicate_actions": [],
        "media_recovery": [], "pricing_recovery": [], "ai_calls": 0,
        "one_shot_agents": {
            "future_active_event_taxonomy": not args.quality_only,
            "local_event_duplicates": args.quality_focus in ("all", "duplicates"),
            "representation_media_from_event_tmp": args.quality_focus in ("all", "representation-media"),
            "paid_without_access_link": args.quality_focus in ("all", "pricing", "paid-without-link"),
            "false_free_events": args.quality_focus in ("all", "pricing", "false-free"),
        },
    }
    if not args.taxonomy_only:
        # Deterministic/read-only first: no LLM call and no mutation. The report
        # carries EventTmp image evidence, duplicate candidates and pricing facts.
        quality_events = client.quality_candidates(args.limit, args.event_id)
        report["quality_events"] = filter_quality_events(quality_events, args.quality_focus)
        report["duplicate_pairs"] = build_duplicate_pairs(report["quality_events"])
        for pair in report["duplicate_pairs"]:
            if pair["decision"] != "ready_to_archive_duplicate":
                continue
            try:
                report["duplicate_actions"].append(client.archive_duplicate(
                    int(pair["recommended_duplicate"]["event_id"]),
                    int(pair["recommended_keeper"]["event_id"]),
                    not (args.mode == "apply" and args.apply_duplicates),
                ))
            except Exception as exc:
                report["duplicate_actions"].append({
                    "status": "error", "pair": pair["pair"], "error": str(exc),
                })
        seen_representations: set[int] = set()
        for event in report["quality_events"]:
            reasons = event.get("quality_reasons") or []
            representation_id = int(event.get("representation_id") or 0)
            if representation_id < 1 or representation_id in seen_representations:
                continue
            if "representation_media_recoverable_from_event_tmp" not in reasons:
                continue
            seen_representations.add(representation_id)
            try:
                report["media_recovery"].append(client.recover_representation_media(
                    representation_id, args.mode != "apply"
                ))
            except Exception as exc:
                report["media_recovery"].append({
                    "success": False, "representation_id": representation_id, "error": str(exc),
                })
        pricing_reasons = {
            "false_free_with_commercial_evidence", "free_without_explicit_evidence",
            "paid_without_access_link", "paid_or_unknown_without_price_and_link",
        }
        seen_pricing_events: set[int] = set()
        for event in report["quality_events"]:
            event_id = int(event.get("id") or 0)
            reasons = set(event.get("quality_reasons") or [])
            if event_id < 1 or event_id in seen_pricing_events or not pricing_reasons.intersection(reasons):
                continue
            seen_pricing_events.add(event_id)
            try:
                report["pricing_recovery"].append(client.repair_event_pricing(
                    event_id, args.mode != "apply"
                ))
            except Exception as exc:
                report["pricing_recovery"].append({
                    "status": "error", "event_id": event_id, "error": str(exc),
                })
    if args.quality_only:
        return report
    for event in client.candidates(args.limit, args.event_id):
        row: dict[str, Any] = {
            "event_id": int(event["id"]), "title": event.get("title"),
            "reasons": event.get("taxonomy_reasons") or [], "status": "candidate",
        }
        try:
            if not args.allow_ai:
                row["status"] = "needs_ai_review"
                report["events"].append(row)
                continue
            source_text = fetch_source_text(str(event.get("scrapped_from") or ""), env["verify_ssl"])
            proposal = client.analyze(event, source_text)
            report["ai_calls"] += 1
            row["proposal"] = proposal
            confidence = float(proposal.get("confidence") or 0)
            if confidence < args.min_confidence:
                row["status"] = "low_confidence"
            elif has_occurrence_doubt(proposal):
                row["status"] = "manual_occurrence_review"
            else:
                result = client.apply_taxonomy(int(event["id"]), proposal, args.mode != "apply")
                row["result"] = result
                row["status"] = "applied" if args.mode == "apply" else "dry_run"
        except Exception as exc:  # keep the batch auditable
            row["status"] = "error"
            row["error"] = str(exc)
        report["events"].append(row)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Rattrapage ponctuel taxonomie LocalEvent")
    parser.add_argument("--env", choices=sorted(IZILIFE_ENVS), default="local")
    parser.add_argument("--mode", choices=("review", "apply"), default="review")
    parser.add_argument("--event-id", type=int)
    parser.add_argument("--limit", type=int, default=2000)
    parser.add_argument("--allow-ai", action="store_true")
    parser.add_argument("--taxonomy-only", action="store_true",
                        help="Ignore l'audit terrain doublons/tarifs/médias.")
    parser.add_argument("--quality-only", action="store_true",
                        help="Exécute seulement les agents ponctuels qualité, sans taxonomie ni appel LLM.")
    parser.add_argument("--quality-focus", choices=(
                            "all", "duplicates", "representation-media", "paid-without-link",
                            "false-free", "pricing",
                        ),
                        default="all", help="Limite l'agent qualité ponctuel à un chantier nommé.")
    parser.add_argument("--apply-duplicates", action="store_true",
                        help="Avec --mode apply, archive seulement les doublons certains sans conflit.")
    parser.add_argument("--min-confidence", type=float, default=0.90)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.output = args.output or (local_agent_workspace_root(args.env) / "reports" /
                                  f"active_event_taxonomy_{datetime.now():%Y%m%d_%H%M%S_%f}_{args.quality_focus}.json")
    report = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    counts: dict[str, int] = {}
    for row in report["events"]:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    quality_counts: dict[str, int] = {}
    for row in report["quality_events"]:
        for reason in row.get("quality_reasons") or []:
            quality_counts[reason] = quality_counts.get(reason, 0) + 1
    print(json.dumps({"report": str(args.output), "counts": counts,
                      "quality_counts": quality_counts,
                      "duplicate_pairs": len(report["duplicate_pairs"]),
                      "duplicate_actions": len(report["duplicate_actions"]),
                      "media_recovery": len(report["media_recovery"]),
                      "pricing_recovery": len(report["pricing_recovery"]),
                      "one_shot_agents": report["one_shot_agents"]}, ensure_ascii=False))
    return 1 if counts.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
