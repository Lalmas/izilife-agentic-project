#!/usr/bin/env python3
"""One-shot Lille Tourism conversions; read-only unless --apply is explicit."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


MANIFEST = Path(__file__).with_name("lilletourism_wrong_type_conversions_20261110.json")
FORBIDDEN_IDS = {
    "target_category", "target_category_id", "equipment_category",
    "equipment_category_id", "equipment_parent_id",
}


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Manifeste vide.")
    for item in items:
        if not isinstance(item.get("experience_id"), int) or item["experience_id"] < 1:
            raise ValueError("experience_id invalide.")
        target = item.get("target_type")
        if target == "EVENT_SERIE" and not item.get("target_category_ref"):
            raise ValueError("target_category_ref obligatoire.")
        if target == "EQUIPMENT" and not item.get("equipment_category_ref"):
            raise ValueError("equipment_category_ref obligatoire.")
        if target not in {"EVENT_SERIE", "EQUIPMENT"}:
            raise ValueError(f"Cible interdite: {target}")
        if FORBIDDEN_IDS.intersection(item):
            raise ValueError("Les IDs de nomenclature ou de parent sont interdits.")
    return manifest


def payload(item: dict[str, Any], apply: bool) -> dict[str, Any]:
    result = {
        "source_type": "EXPERIENCE", "source_id": item["experience_id"],
        "target_type": item["target_type"], "apply": apply,
        "reason": "Correction Lille Tourisme: mauvais type d'objet importé",
    }
    for key in ("target_category_ref", "equipment_category_ref", "equipment_parent_type", "equipment_parent_ref"):
        if item.get(key):
            result[key] = item[key]
    return result


def run(base_url: str, token: str, manifest: dict[str, Any], apply: bool, timeout: int) -> list[dict[str, Any]]:
    url = base_url.rstrip("/") + "/scraper/agentExperienceConversion"
    results = []
    for item in manifest["items"]:
        entry = {"experience_id": item["experience_id"], "title": item.get("title"), "target_type": item["target_type"]}
        try:
            response = requests.post(url, headers={"X-Agent-Token": token}, json=payload(item, apply), timeout=timeout)
            body = response.json()
            if response.status_code >= 400 or body.get("success") is not True:
                raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
            entry["response"] = body
        except Exception as exc:
            entry["error"] = str(exc)
        results.append(entry)
        print(json.dumps(entry, ensure_ascii=False))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--base-url", default=os.getenv("IZILIFE_PROD_URL", "https://www.izilife.co/izilife-admin"))
    parser.add_argument("--token-env", default="IZILIFE_AGENT_TOKEN")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    token = os.getenv(args.token_env, "").strip()
    if not token:
        raise SystemExit(f"Variable {args.token_env} absente.")
    manifest = load_manifest(args.manifest)
    results = run(args.base_url, token, manifest, args.apply, args.timeout)
    mode = "apply" if args.apply else "audit"
    output = args.output or args.manifest.with_name(f"lilletourism_wrong_type_{mode}_{datetime.now():%Y%m%d_%H%M%S}.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(), "mode": mode,
        "manifest": str(args.manifest), "results": results,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Rapport: {output}")
    return 1 if any("error" in row for row in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
