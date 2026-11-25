#!/usr/bin/env python3
"""Agent territorial automatisé d'expériences (dry-run par défaut).

Sa configuration JSON vit dans le Drive, par environnement et par zone. Elle
liste plusieurs sites génériques (ville, lieu, plateforme) et précise lesquels
sont actifs et si leur catalogue doit être découvert. Aucune écriture n'est
possible sans les deux options ``--ingest --confirm-write``.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
import openpyxl

from site_experience_package import izilife_post

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offers"))
from offer_agent_common import drive_workspace_root, normalize_zone


WORKBOOK_FILE = "experiences.xlsx"
SOURCES_SHEET = "Sources automatiques"


def workbook_path(env: str, zone: str) -> Path:
    return drive_workspace_root(env) / "izilife" / "experiences" / normalize_zone(zone) / WORKBOOK_FILE


def normalized_sources(config: dict) -> list[dict]:
    sources = []
    for item in config.get("sources") or []:
        if isinstance(item, str):
            item = {"url": item}
        if not isinstance(item, dict) or not item.get("enabled", True):
            continue
        url = str(item.get("url") or "").strip()
        if url:
            sources.append({
                "label": str(item.get("label") or url),
                "url": url,
                "discover": str(item.get("mode") or "catalog").lower() in {"catalog", "discover", "territorial"},
                "max_items": max(1, min(120, int(item.get("max_items") or config.get("max_items") or 24))),
            })
    # Compatibilité avec le premier format simple.
    if not sources:
        for url in dict.fromkeys(config.get("source_urls") or []):
            if str(url).strip():
                sources.append({"label": str(url), "url": str(url).strip(),
                                "discover": bool(config.get("discover", True)),
                                "max_items": max(1, min(120, int(config.get("max_items", 24))))})
    return sources


def workbook_sources(path: Path, default_city_ref: str) -> list[dict]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    if SOURCES_SHEET not in workbook.sheetnames:
        raise RuntimeError(f"Onglet absent dans {path.name}: {SOURCES_SHEET}")
    sheet = workbook[SOURCES_SHEET]
    headers = [str(cell.value or "").strip() for cell in sheet[1]]
    sources = []
    for cells in sheet.iter_rows(min_row=2, values_only=True):
        row = {headers[index]: cells[index] for index in range(min(len(headers), len(cells))) if headers[index]}
        if str(row.get("enabled") or "oui").strip().lower() not in {"1", "true", "yes", "oui", "y", "x"}:
            continue
        url = str(row.get("url") or "").strip()
        if not url:
            continue
        sources.append({
            "label": str(row.get("label") or url),
            "url": url,
            "city_ref": str(row.get("city_ref") or default_city_ref).strip(),
            "discover": str(row.get("mode") or "catalog").strip().lower() in {"catalog", "discover", "territorial"},
            "max_items": max(1, min(120, int(row.get("max_items") or 24))),
        })
    workbook.close()
    return sources


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zone", required=True)
    parser.add_argument("--workbook", type=Path, help="Surcharge du experiences.xlsx Drive")
    parser.add_argument("--config", type=Path, help="Ancien JSON, encore accepté pour compatibilité")
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--confirm-write", action="store_true")
    args = parser.parse_args()
    if args.ingest != args.confirm_write:
        raise SystemExit("Une écriture exige ensemble --ingest et --confirm-write.")

    source_file = args.config or args.workbook or workbook_path(args.env, args.zone)
    if not source_file.exists():
        raise SystemExit(f"Configuration territoriale absente : {source_file}")
    default_city_ref = args.zone.removesuffix("-zone")
    if args.config:
        config = json.loads(source_file.read_text(encoding="utf-8-sig"))
        sources = normalized_sources(config)
    else:
        config = {}
        sources = workbook_sources(source_file, default_city_ref)
    if not sources:
        raise SystemExit("Aucun site territorial actif dans la configuration.")
    totals = {key: 0 for key in ("sources", "failed", "empty_sources", "found", "new", "known", "inserted")}
    totals.update({"errors": [], "items": [], "source_results": []})
    for source in sources:
        payload = {
            "city_id": int(config.get("city_id") or 0),
            "city_ref": source.get("city_ref") or str(config.get("city_ref") or default_city_ref),
            "source_urls": [source["url"]],
            "max_items": source["max_items"],
            "discover": source["discover"],
            "ingest": args.ingest,
            "confirm_write": args.confirm_write,
            "refresh_known": bool(source.get("refresh_known", config.get("refresh_known", False))),
        }
        response = izilife_post(
            "/scraper/agentCollectTerritorialExperiences",
            {"payload": json.dumps(payload, ensure_ascii=False)}, args.env, timeout=900,
        )
        if not response.get("success"):
            result = {"sources": 1, "failed": 1, "errors": [{"url": source["url"], "error": response.get("error") or "Erreur API"}]}
        else:
            result = response["result"]
        totals["source_results"].append({"label": source["label"], "url": source["url"], **result})
        for key in ("sources", "failed", "empty_sources", "found", "new", "known", "inserted"):
            totals[key] += int(result.get(key) or 0)
        totals["errors"].extend(result.get("errors") or [])
        totals["items"].extend(result.get("items") or [])
    result = totals
    output = args.output_dir or source_file.parent / "reports"
    output.mkdir(parents=True, exist_ok=True)
    report = output / f"territorial_experiences_{datetime.now():%Y%m%d_%H%M%S}.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(report), **{k: result.get(k) for k in
          ("sources", "failed", "empty_sources", "found", "new", "known", "inserted")},
          "errors": result.get("errors") or []}, ensure_ascii=False, indent=2))
    return 0 if not result.get("failed") and not result.get("empty_sources") else 1


if __name__ == "__main__":
    sys.exit(main())
