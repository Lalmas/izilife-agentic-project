#!/usr/bin/env python3
"""Audit or apply the Lille Tourism Experience conversions through the agent API.

The default mode is read-only.  ``--apply`` must be supplied explicitly and the
server remains responsible for the transaction, dependency transfer and source
archival.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path(__file__).with_name(
    "lilletourism_wrong_type_conversions_20261110.json"
)
DEFAULT_ENDPOINT = "/scraper/agentExperienceConversion"


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Le manifeste ne contient aucune conversion.")
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Chaque conversion doit être un objet JSON.")
        if not isinstance(item.get("experience_id"), int) or item["experience_id"] < 1:
            raise ValueError("experience_id invalide.")
        target = item.get("target_type")
        if target not in {"EVENT_SERIE", "EQUIPMENT"}:
            raise ValueError(f"Cible interdite: {target!r}")
        if target == "EVENT_SERIE" and not item.get("target_category_ref"):
            raise ValueError("target_category_ref est obligatoire pour EVENT_SERIE.")
        if target == "EQUIPMENT" and not item.get("equipment_category_ref"):
            raise ValueError("equipment_category_ref est obligatoire pour EQUIPMENT.")
        forbidden = {
            "target_category",
            "target_category_id",
            "equipment_category",
            "equipment_category_id",
            "equipment_parent_id",
        }
        present = sorted(forbidden.intersection(item))
        if present:
            raise ValueError(
                "Les IDs de nomenclature/parent sont interdits: " + ", ".join(present)
            )
    return data


def build_payload(item: dict[str, Any], apply: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "source_type": "EXPERIENCE",
        "source_id": item["experience_id"],
        "target_type": item["target_type"],
        "apply": apply,
        "reason": "Correction Lille Tourisme: mauvais type d'objet importé",
    }
    for key in (
        "target_category_ref",
        "equipment_category_ref",
        "equipment_parent_type",
        "equipment_parent_ref",
    ):
        if item.get(key):
            payload[key] = item[key]
    return payload


def post_json(url: str, token: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Agent-Token": token,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"API inaccessible: {exc.reason}") from exc
    result = json.loads(body)
    if not isinstance(result, dict):
        raise RuntimeError("Réponse API JSON inattendue.")
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--base-url", default="https://www.izilife.co/izilife-admin")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--token-env", default="IZILIFE_AGENT_TOKEN")
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    manifest = load_manifest(args.manifest)
    token = os.environ.get(args.token_env, "").strip()
    if not token:
        raise SystemExit(f"Variable {args.token_env} absente.")
    url = args.base_url.rstrip("/") + "/" + args.endpoint.lstrip("/")
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "apply" if args.apply else "audit",
        "manifest": str(args.manifest),
        "endpoint": url,
        "results": [],
    }
    exit_code = 0
    for item in manifest["items"]:
        payload = build_payload(item, args.apply)
        entry = {
            "experience_id": item["experience_id"],
            "title": item.get("title"),
            "target_type": item["target_type"],
        }
        try:
            response = post_json(url, token, payload, args.timeout)
            entry["response"] = response
            if response.get("success") is not True:
                exit_code = 1
        except Exception as exc:  # keep a complete four-item journal
            entry["error"] = str(exc)
            exit_code = 1
        report["results"].append(entry)
        print(json.dumps(entry, ensure_ascii=False))
    report_path = args.report or args.manifest.with_name(
        f"lilletourism_wrong_type_{report['mode']}_{datetime.now():%Y%m%d_%H%M%S}.json"
    )
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Rapport: {report_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
