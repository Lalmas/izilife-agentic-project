"""Classifie et importe les POI Google laissés sans destination par iziLife.

Le serveur garde le dernier mot : les catégories doivent déjà exister et
l'import réutilise strictement le circuit du BO. Les catégories manquantes
sont seulement consignées dans un rapport pour faire évoluer le référentiel.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.parse import quote_plus
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

# Les noms Google peuvent contenir des caractères absents de la page de codes
# Windows courante. Le journal ne doit jamais interrompre un lot métier.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CORE_ROOT = Path(__file__).resolve().parents[2]
if str(CORE_ROOT) not in sys.path:
    sys.path.append(str(CORE_ROOT))
from core.paths import IZILIFE_ENVS, local_agent_workspace_root  # noqa: E402
from core.place_resolution import PlaceIdentity, normalize_url  # noqa: E402


class PoiValidatorClient:
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
            # Compatibility with deployed legacy importers that print opening
            # hours before the agent controller emits its final JSON response.
            json_start = (response.text or "").rfind("{")
            if json_start >= 0:
                try:
                    body = json.loads(response.text[json_start:])
                except ValueError:
                    body = None
                if isinstance(body, dict):
                    if response.status_code >= 400 or not body.get("success"):
                        raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
                    return body
            preview = re.sub(r"\s+", " ", response.text or "").strip()[:500]
            raise RuntimeError(
                f"HTTP {response.status_code}: réponse non JSON"
                + (f" — {preview}" if preview else "")
            ) from exc
        if response.status_code >= 400 or not body.get("success"):
            raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
        return body

    def candidates(self, limit: int, city_id: int | None, poi_id: int | None,
                   after_id: int | None = None) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {"limit": limit}
        if city_id:
            payload["city_id"] = city_id
        if poi_id:
            payload["poi_id"] = poi_id
        if after_id:
            payload["after_id"] = after_id
        return self.post("/scraper/agentPoiValidatorCandidates", payload)["pois"]

    def analyze(self, poi_id: int, source_text: str = "") -> dict[str, Any]:
        return self.post("/scraper/agentAnalyzePoi", {
            "poi_id": poi_id, "source_text": source_text,
        })

    def apply(self, poi_id: int, proposal: dict[str, Any]) -> dict[str, Any]:
        return self.post("/scraper/agentApplyPoiValidation", {
            "poi_id": poi_id, "proposal": proposal,
        })


def report_path(env_name: str) -> Path:
    folder = local_agent_workspace_root(env_name) / "places_validator"
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return folder / f"validate_unmapped_pois-{stamp}.json"


def source_url(poi: dict[str, Any]) -> str:
    try:
        details = json.loads(str(poi.get("json_payload") or "{}"))
    except (TypeError, ValueError):
        details = {}
    for key in ("googleMapsUri", "google_maps_uri", "websiteUri", "website", "url"):
        value = str(details.get(key) or "").strip()
        if re.match(r"^https?://", value, re.I):
            identity = PlaceIdentity.build(name=poi.get("name", ""), address=poi.get("address", ""),
                                           city=poi.get("city_name", ""), urls=[value])
            urls = sorted(identity.website_urls | identity.social_urls)
            return urls[0] if urls else normalize_url(value)
    return ""


def google_maps_url(poi: dict[str, Any]) -> str:
    existing = source_url(poi)
    if "google." in existing and "/maps" in existing:
        return existing
    query = " ".join(str(poi.get(key) or "").strip()
                     for key in ("name", "address", "city_name")).strip()
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(query)


def browser_text(url: str) -> str:
    """Fallback explicite de rodage, jamais utilisé automatiquement en production."""
    if not url:
        return ""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            page.wait_for_timeout(1_000)
            return re.sub(r"\s+", " ", page.locator("body").inner_text()).strip()[:18000]
        finally:
            browser.close()


def validate_proposal(proposal: dict[str, Any], minimum: float) -> tuple[bool, str]:
    action = str(proposal.get("action") or "").upper()
    if action not in {"IMPORT", "IGNORE", "CATEGORY_MISSING"}:
        return False, "action_invalide"
    if float(proposal.get("confidence") or 0) < minimum:
        return False, "confiance_insuffisante"
    if [item for item in (proposal.get("doubts") or []) if item]:
        return False, "doutes"
    if action == "IMPORT" and (
        str(proposal.get("destination") or "").upper() not in {"PLACE", "SHOP", "EQUIPMENT", "PAGE"}
        or not str(proposal.get("category_string_id") or "").strip()
    ):
        return False, "categorie_incomplete"
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=sorted(IZILIFE_ENVS), default="local")
    parser.add_argument("--mode", choices=("review", "apply"), default="review")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--city-id", type=int)
    parser.add_argument("--poi-id", type=int)
    parser.add_argument("--after-id", type=int,
                        help="Reprendre strictement après cet ID sans rejouer le début du lot.")
    parser.add_argument("--min-confidence", type=float, default=.85)
    parser.add_argument("--checkpoint-every", type=int, default=10)
    parser.add_argument("--no-browser-fallback", action="store_true",
                        help="Désactive la vérification Google Maps locale des seuls cas ambigus.")
    args = parser.parse_args()

    config = IZILIFE_ENVS[args.env]
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise SystemExit("IZILIFE_AGENT_TOKEN manquant")
    base_url = str(config["base_url"]).rstrip("/")
    verify_ssl = bool(config.get("verify_ssl", True))
    client = PoiValidatorClient(base_url, token, verify_ssl)
    path = report_path(args.env)
    report: dict[str, Any] = {
        "environment": args.env, "mode": args.mode, "started_at": datetime.now().isoformat(),
        "items": [], "missing_categories": [], "summary": {},
    }
    candidates = client.candidates(args.limit, args.city_id, args.poi_id, args.after_id)
    counters = {"reviewed": 0, "imported": 0, "ignored": 0,
                "category_missing": 0, "manual": 0, "errors": 0}

    def checkpoint() -> None:
        report["summary"] = counters.copy()
        report["updated_at"] = datetime.now().isoformat()
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for index, poi in enumerate(candidates, 1):
        entry: dict[str, Any] = {"poi_id": int(poi["id"]), "name": poi.get("name"),
                                 "city": poi.get("city_name"), "google_types": poi.get("google_types")}
        try:
            ambiguous = not bool(poi.get("deterministic_proposal"))
            evidence = (browser_text(google_maps_url(poi))
                        if ambiguous and not args.no_browser_fallback else "")
            analysis = client.analyze(int(poi["id"]), evidence)
            proposal = analysis["proposal"]
            entry["proposal"] = proposal
            counters["reviewed"] += 1
            valid, reason = validate_proposal(proposal, args.min_confidence)
            action = str(proposal.get("action") or "").upper()
            if action == "CATEGORY_MISSING":
                counters["category_missing"] += 1
                missing = {
                    "poi_id": int(poi["id"]), "name": poi.get("name"), "city": poi.get("city_name"),
                    "destination": proposal.get("destination"),
                    "proposed_category_name": proposal.get("proposed_category_name"),
                    "proposed_category_string_id": proposal.get("proposed_category_string_id"),
                    "evidence": proposal.get("evidence"),
                }
                report["missing_categories"].append(missing)
                entry["status"] = "category_missing"
            elif not valid:
                counters["manual"] += 1
                entry.update(status="manual", reason=reason)
            elif args.mode == "review":
                entry["status"] = "review"
            else:
                result = client.apply(int(poi["id"]), proposal)
                entry.update(status=result.get("status", "applied"), result=result)
                if action == "IGNORE":
                    counters["ignored"] += 1
                else:
                    counters["imported"] += 1
        except Exception as exc:  # continue le lot, mais conserve la cause exacte
            counters["errors"] += 1
            entry.update(status="error", error=str(exc))
        report["items"].append(entry)
        print(f"[{index}/{len(candidates)}] {entry['name']} -> {entry.get('status')}", flush=True)
        if index % max(1, args.checkpoint_every) == 0:
            checkpoint()
    report["finished_at"] = datetime.now().isoformat()
    checkpoint()
    print(f"Rapport: {path}")
    print(json.dumps(counters, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
