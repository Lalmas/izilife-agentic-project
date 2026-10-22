from __future__ import annotations
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offers"))
from offer_agent_common import create_workbook, drive_workspace_root, normalize_zone, process

FILE, SHEET = "terraces.xlsx", "Terrasses"
COLUMNS = [
    ("scope_type", "scope"), ("scope_ref", "scope"), ("name", "offer"),
    ("type_ref", "offer"), ("description", "offer"), ("capacity", "access"),
    ("is_rooftop", "access"), ("is_privatizable", "access"), ("hidden", "access"),
    ("source_url", "access"), ("status", "result"), ("notes", "result"), ("last_result", "result"),
]


def payload(row: dict) -> dict:
    item = {key: row.get(key) for key in ("name", "type_ref", "description", "capacity", "is_rooftop", "is_privatizable", "hidden")}
    return {
        "kind": "terrace",
        "scope_type": str(row.get("scope_type") or "").upper(),
        "scope_ref": row.get("scope_ref"),
        "source_url": str(row.get("source_url") or "").strip(),
        "item": item,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Ajout/upsert manuel de terrasses sur un lieu ou un commerce.")
    parser.add_argument("--zone", required=True)
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max", type=int, default=100)
    args = parser.parse_args()
    path = drive_workspace_root(args.env) / "izilife" / "terraces" / normalize_zone(args.zone) / FILE
    if args.init:
        example = {
            "scope_type": "SHOP", "scope_ref": "soultraincafe", "name": "Terrasse principale",
            "type_ref": "prive", "description": "", "capacity": "", "is_rooftop": "non",
            "is_privatizable": "non", "hidden": "non", "source_url": "",
            "status": "skip", "notes": "OUI/NON; type_ref accepte prive, espace-public, sur-une-rue-connue ou sur-une-place-connue. URL facultative de référence, les champs restent curatés manuellement.",
            "last_result": "",
        }
        create_workbook(path, SHEET, COLUMNS, example, {
            "scope_type": ["PLACE", "SHOP"],
            "type_ref": ["prive", "espace-public", "sur-une-rue-connue", "sur-une-place-connue"],
            "is_rooftop": ["oui", "non"], "is_privatizable": ["oui", "non"], "hidden": ["oui", "non"],
            "status": ["pending", "done", "error", "skip"],
        })
        return
    process(path, SHEET, args.env, "/scraper/agentIngestSiteItem", payload, args.dry_run, args.max)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("terraces", "terraces", main)
