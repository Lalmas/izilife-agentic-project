"""Validate pending iziLife ExperienceTmp through the BO token endpoints."""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date, datetime
from html import unescape
from urllib.parse import urljoin
from pathlib import Path
from typing import Any

import requests

import sys
CORE_ROOT = Path(__file__).resolve().parents[2]
if str(CORE_ROOT) not in sys.path:
    sys.path.append(str(CORE_ROOT))
from core.paths import IZILIFE_ENVS, local_agent_workspace_root  # noqa: E402


def clean_html(value: str) -> str:
    value = re.sub(r"(?is)<(script|style|noscript).*?>.*?</\1>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()[:30000]


def fetch_text(url: str, verify: bool) -> str:
    if not re.match(r"^https?://", str(url or ""), re.I):
        return ""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; iziLifeExperienceValidator/1.0)"},
            timeout=25,
            verify=verify,
        )
        if response.status_code >= 400:
            return ""
        response.encoding = response.apparent_encoding or "utf-8"
        return clean_html(response.text)
    except requests.RequestException:
        return ""


def sanitize_expired_schedule(proposal: dict[str, Any]) -> dict[str, Any]:
    """Keep a stable Experience but never materialize an entirely expired schedule."""
    target = proposal.get("experience") if isinstance(proposal.get("experience"), dict) else proposal
    configuration = target.get("session_configuration")
    configurations = configuration if isinstance(configuration, list) else [configuration]
    parsed_dates: list[date] = []
    for item in configurations:
        if not isinstance(item, dict):
            continue
        for raw_date in item.get("dates") or []:
            # The LLM may return either a plain ISO date or a seasonal range
            # ({"start": ..., "end": ...}).  Inspect both bounds so an
            # entirely expired season cannot reach the SC/SCC materializer.
            values = (
                [raw_date.get("start"), raw_date.get("end")]
                if isinstance(raw_date, dict)
                else [raw_date]
            )
            for value in values:
                text = str(value or "").strip()[:10]
                try:
                    parsed_dates.append(date.fromisoformat(text))
                except ValueError:
                    continue
    # Des heures d'ouverture ou une simple plage horaire ne constituent pas
    # des séances. Sans configuration explicite, aucun SCC ne doit traverser.
    if not isinstance(configuration, (dict, list)):
        target["session_contents"] = []
        target["session_warnings"] = list(target.get("session_warnings") or []) + [
            "session_contents ignored without an explicit session_configuration"
        ]
    if parsed_dates and max(parsed_dates) < date.today():
        target["ignored_expired_schedule"] = {
            "session_configuration": configuration,
            "session_contents": target.get("session_contents") or [],
            "session_warnings": target.get("session_warnings") or [],
            "reason": "all_explicit_dates_expired",
        }
        # Explicit null/empty values also neutralize an old schedule already
        # present in raw_json when the production endpoint is one release behind.
        target["session_configuration"] = None
        target["session_contents"] = []
        target["session_warnings"] = []
    return proposal


def normalize_reference_lists(proposal: dict[str, Any]) -> dict[str, Any]:
    """Canonicalise catalogue objects before older deployed validators see them."""
    target = proposal.get("experience") if isinstance(proposal.get("experience"), dict) else proposal
    keys = {
        "language_string_ids": ("language_code_iso_639_1", "string_id", "id"),
        "hobby_string_ids": ("hobby_string_id", "string_id", "id"),
        "object_string_ids": ("object_string_id", "string_id", "id"),
        "occasion_string_ids": ("occasion_string_id", "string_id", "id"),
        "age_category_ids": ("id", "string_id"),
    }
    for key, candidates in keys.items():
        values = target.get(key)
        if not isinstance(values, list):
            continue
        normalized = []
        for value in values:
            if isinstance(value, dict):
                value = next((value.get(candidate) for candidate in candidates if value.get(candidate) not in (None, "")), None)
            if value not in (None, "") and value not in normalized:
                normalized.append(value)
        target[key] = normalized
    return proposal


def fetch_images(url: str, verify: bool) -> list[str]:
    if not re.match(r"^https?://", str(url or ""), re.I):
        return []
    try:
        response=requests.get(url,headers={"User-Agent":"Mozilla/5.0 (compatible; iziLifeExperienceValidator/1.0)"},timeout=25,verify=verify)
        if response.status_code>=400:return []
        found=[]
        for pattern in (
            r'<meta[^>]+(?:property|name)=["\']og:image(?::url)?["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']og:image(?::url)?["\']',
            r'<meta[^>]+(?:property|name)=["\']twitter:image(?::src)?["\'][^>]+content=["\']([^"\']+)',
        ):
            for match in re.findall(pattern,response.text,re.I):
                candidate=urljoin(response.url,unescape(match).strip())
                if candidate not in found and re.match(r"^https?://",candidate,re.I):found.append(candidate)
        return found[:2]
    except requests.RequestException:return []


class Client:
    def __init__(self, base: str, token: str, verify: bool):
        self.base = base.rstrip("/")
        self.verify = verify
        self.headers = {"X-Agent-Token": token, "Content-Type": "application/json"}

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(self.base + path, headers=self.headers, json=payload, verify=self.verify, timeout=240)
        try:
            data = response.json()
        except ValueError:
            try:
                text = response.text.lstrip()
                data, end = json.JSONDecoder().raw_decode(text)
                suffix = text[end:].strip()
                if suffix:
                    print(f"AVERTISSEMENT réponse PHP après JSON ({path}): {suffix[:800]}", file=sys.stderr)
            except ValueError as exc:
                raise RuntimeError(f"HTTP {response.status_code}: réponse non JSON") from exc
        if response.status_code >= 400 or not data.get("success"):
            raise RuntimeError(str(data.get("error") or data.get("message") or data.get("title") or f"HTTP {response.status_code}"))
        return data


def run(args: argparse.Namespace) -> dict[str, Any]:
    cfg = IZILIFE_ENVS[args.env]
    token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN ou AGENT_SECRET_TOKEN absent.")
    client = Client(cfg["base_url"], token, bool(cfg.get("verify_ssl", True)))
    staged: dict[str, Any] | None = None
    if args.stage_inactive:
        staged = client.post("/scraper/agentStageInactiveExperiences", {
            "after_id": args.after_id, "limit": args.limit,
        })
    query: dict[str, Any] = {"limit": args.limit}
    if args.tmp_id:
        query["tmp_id"] = args.tmp_id
    elif args.after_tmp_id:
        query["after_id"] = args.after_tmp_id
    rows = client.post("/scraper/agentExperienceValidatorCandidates", query).get("experiences", [])
    forced_proposal = json.loads(args.proposal_json) if args.proposal_json else None
    if args.proposal_file:
        saved = json.loads(Path(args.proposal_file).read_text(encoding="utf-8"))
        if isinstance(saved, dict) and isinstance(saved.get("experiences"), list):
            match = next((row for row in saved["experiences"] if int(row.get("tmp_id", 0)) == int(args.tmp_id or 0)), None)
            forced_proposal = (match or {}).get("proposal")
        else:
            forced_proposal = saved
        if not isinstance(forced_proposal, dict):
            raise RuntimeError("Le fichier ne contient aucune proposition pour ce tmp_id.")
    report: dict[str, Any] = {"environment": args.env, "mode": args.mode, "started_at": datetime.now().isoformat(), "staging": staged, "experiences": []}
    consecutive_provider_failures = 0
    ai_calls = 0
    for row in rows:
        entry: dict[str, Any] = {
            "tmp_id": int(row["id"]),
            "title": row.get("title"),
            "experience_type_string_id": row.get("experience_type_string_id"),
            "source_url": row.get("source_url"),
            "validation_blockers": list(row.get("validation_blockers") or []),
            "duration": row.get("duration"),
            "duration_measurement_unity_string_id": row.get("duration_measurement_unity_string_id"),
            "status": "pending",
        }
        try:
            blockers = list(row.get("validation_blockers") or [])
            proposal: dict[str, Any] = dict(forced_proposal or {})
            discovered_images: list[str] = []
            if not row.get("primary_image_url"):
                discovered_images=fetch_images(str(row.get("source_url") or ""),client.verify)
                if discovered_images:
                    proposal.setdefault("primary_image_url",discovered_images[0])
                    if len(discovered_images)>1:proposal.setdefault("additional_image_urls",discovered_images[1:2])
            if forced_proposal is None and (blockers or args.enrich_all):
                if not args.allow_ai:
                    entry["status"] = "needs_ai"
                    entry["error"] = "Analyse IA désactivée; utiliser --allow-ai avec un plafond explicite."
                    report["experiences"].append(entry)
                    continue
                source_text = fetch_text(str(row.get("source_url") or ""), client.verify)
                ai_calls += 1
                analysis = client.post("/scraper/agentAnalyzeExperienceTmp", {"tmp_id": int(row["id"]), "source_text": source_text})
                proposal = dict(analysis.get("proposal") or {})
                target = proposal.get("experience") if isinstance(proposal.get("experience"), dict) else proposal
                if discovered_images and not target.get("primary_image_url") and not target.get("additional_image_urls"):
                    target["primary_image_url"] = discovered_images[0]
                    if len(discovered_images)>1: target["additional_image_urls"] = discovered_images[1:2]
                entry["proposal"] = proposal
                entry["provider"] = analysis.get("provider")
            proposal = normalize_reference_lists(sanitize_expired_schedule(proposal))
            if args.override_experience_type:
                target = proposal.get("experience") if isinstance(proposal.get("experience"), dict) else proposal
                target["experience_type_string_id"] = args.override_experience_type
            if args.mode == "review":
                entry["status"] = "reviewed"
                consecutive_provider_failures = 0
            else:
                applied = client.post("/scraper/agentApplyExperienceValidation", {
                    "tmp_id": int(row["id"]), "proposal": proposal,
                    "validate": args.mode == "validate", "activate": True,
                })
                entry["application"] = applied
                validation = applied.get("validation") or {}
                entry["status"] = "validated" if validation.get("validated") else ("enriched" if not applied.get("blockers") else "needs_review")
                consecutive_provider_failures = 0
        except Exception as exc:  # one invalid row must not stop the backlog
            entry["status"] = "error"
            entry["error"] = str(exc)
            if "fournisseur IA n’a renvoyé aucune analyse" in str(exc):
                consecutive_provider_failures += 1
            else:
                consecutive_provider_failures = 0
        report["experiences"].append(entry)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        if consecutive_provider_failures >= 3:
            report["stopped_early"] = {
                "reason": "provider_unavailable",
                "after_tmp_id": int(row["id"]),
                "consecutive_failures": consecutive_provider_failures,
            }
            break
    report["ai_calls"] = ai_calls
    report["completed_at"] = datetime.now().isoformat()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validateur automatique ExperienceTmp")
    parser.add_argument("--env", choices=sorted(IZILIFE_ENVS), default="local")
    parser.add_argument("--mode", choices=("review", "apply", "validate"), default="review")
    parser.add_argument("--tmp-id", type=int)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--enrich-all", action="store_true", help="Analyse aussi les fiches sans blocker structurel afin d'ajouter les signaux éditoriaux")
    parser.add_argument("--allow-ai", action="store_true", help="Autorise explicitement les appels IA payants")
    parser.add_argument("--stage-inactive", action="store_true", help="Place d'abord les Experiences inactives dans ExperienceTmp")
    parser.add_argument("--after-id", type=int, default=0, help="Premier ID Experience à examiner pour --stage-inactive")
    parser.add_argument("--after-tmp-id", type=int, default=0, help="Reprend la file ExperienceTmp après cet ID")
    parser.add_argument("--proposal-json", help="Proposition JSON déjà relue; évite un appel IA pendant les tests locaux")
    parser.add_argument("--proposal-file", help="Rapport review ou fichier de proposition; évite un nouvel appel IA")
    parser.add_argument("--override-experience-type", help="Correction humaine explicite du type, sans refaire l’analyse LLM")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.output = args.output or local_agent_workspace_root(args.env) / "reports" / f"experience_validation_{datetime.now():%Y%m%d_%H%M%S}.json"
    report = run(args)
    counts: dict[str, int] = {}
    for row in report["experiences"]:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    print(json.dumps({"report": str(args.output), "counts": counts}, ensure_ascii=False))
    return 1 if counts.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
