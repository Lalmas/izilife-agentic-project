"""Saisie manuelle des tags et caractéristiques, sans collecte externe."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offers"))
from offer_agent_common import create_workbook, drive_workspace_root, normalize_zone, post, process

FILE = "tags_and_characts.xlsx"
SHEET = "Tags et caractéristiques"
EDITORIAL = ["Atmosphere", "MealType", "BarType", "MusicStyle", "DietType", "DishOrigin",
             "KnowedMeal", "KnowedDrink", "Dance", "VisitMoment", "VisitWeather",
             "PaiementMethod", "OrderMethod", "Sport", "Hobby", "ObjectOnPublicPlace",
             "Occasion", "Animal", "AccessType", "AgeCategory"]
COLUMNS = [("scope_type", "scope"), ("scope_ref", "scope"), ("operation", "access"),
           ("tags", "offer"), ("principal_characteristics", "offer")]
COLUMNS += [(name, "offer") for name in EDITORIAL]
COLUMNS += [("status", "result"), ("notes", "result"), ("last_result", "result")]
REFERENCES = Path(__file__).with_name("references.json")


def split_refs(value):
    if value is None or str(value).strip() == "":
        return []
    return list(dict.fromkeys(part.strip() for part in str(value).replace("\n", "|").split("|") if part.strip()))


def payload(row):
    principal = {}
    for token in split_refs(row.get("principal_characteristics")):
        if "=" in token:
            name, value = (part.strip() for part in token.split("=", 1))
        else:
            name, value = (token[1:].strip(), "0") if token.startswith("-") else (token, "1")
        if value not in {"0", "1"}:
            raise ValueError(f"Valeur 0/1 attendue pour {name}")
        principal[name] = int(value)
    editorial = {name: refs for name in EDITORIAL if (refs := split_refs(row.get(name)))}
    return {"scope_type": row.get("scope_type"), "scope_ref": row.get("scope_ref"),
            "operation": row.get("operation") or "ADD", "tags": split_refs(row.get("tags")),
            "principal_characteristics": principal, "editorial": editorial}


def update_reference_sheets(path, data, source_env=None, target_env=None):
    if not path.exists():
        return
    wb = openpyxl.load_workbook(path)
    if "Références" in wb:
        del wb["Références"]
    meta = wb.create_sheet("Références", 1)
    meta.append(["Environnement du classeur", target_env or source_env or "inconnu"])
    meta.append(["Référentiel lu sur", source_env or "inconnu"])
    meta.append(["Dernière lecture", data.get("generated_at", "")])
    meta.append(["Statut", "À actualiser après livraison BO" if source_env != target_env else "Référentiel de cet environnement"])
    meta.column_dimensions["A"].width = 32
    meta.column_dimensions["B"].width = 56
    catalog = {"Tags": (["string_id", "name", "tag_types"], data.get("tags", [])),
               "PrincipalCharacteristics": (["field", "value"],
                                            [{"field": name, "value": "0 ou 1"} for name in data.get("principal_characteristics", [])])}
    for name, rows in data.get("editorial", {}).items():
        catalog[name] = (["string_id", "name", "scope_types"], rows)
    for name, (headers, rows) in catalog.items():
        if name in wb:
            del wb[name]
        ws = wb.create_sheet(name)
        ws.append(headers)
        for row in rows:
            ws.append([row.get(key, "") for key in headers])
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{openpyxl.utils.get_column_letter(len(headers))}{max(2, ws.max_row)}"
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="4472C4")
        for col in range(1, len(headers) + 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 34
    wb.save(path)


def main():
    ap = argparse.ArgumentParser(description="Tags et caractéristiques manuels, sans Google/IA.")
    ap.add_argument("--zone", required=True)
    ap.add_argument("--env", choices=["local", "staging", "prod"], required=True)
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--refresh-references", action="store_true", help="Lit les référentiels du BO et actualise les onglets.")
    ap.add_argument("--refresh-all-zones", action="store_true", help="Avec --refresh-references, actualise tous les classeurs de l'environnement.")
    ap.add_argument("--dry-run", action="store_true", help="Affiche les payloads, sans appel BO ni écriture du classeur.")
    ap.add_argument("--max", type=int, default=100)
    args = ap.parse_args()
    if args.refresh_all_zones and not args.refresh_references:
        ap.error("--refresh-all-zones exige --refresh-references")
    path = drive_workspace_root(args.env) / "izilife" / "tags" / normalize_zone(args.zone) / FILE
    if args.init or (args.refresh_references and not args.refresh_all_zones and not path.exists()):
        created = not path.exists()
        create_workbook(path, SHEET, COLUMNS,
                        {},
                        {"scope_type": ["PLACE", "SHOP", "EVENT", "EVENT_SERIE", "EXPERIENCE", "ANNUAL_CELEBRATION"],
                         "operation": ["ADD", "REMOVE"], "status": ["pending", "done", "error", "skip"]})
        legacy = path.with_name("tags.xlsx")
        if created and legacy.exists():
            old = openpyxl.load_workbook(legacy, read_only=True, data_only=True)
            if "Tags" in old:
                source = old["Tags"]
                header = [cell.value for cell in source[1]]
                new = openpyxl.load_workbook(path)
                target = new[SHEET]
                for values in source.iter_rows(min_row=2, values_only=True):
                    row = dict(zip(header, values))
                    if not row.get("scope_ref") or not row.get("tag_ref"):
                        continue
                    target.append([row.get("scope_type"), row.get("scope_ref"), row.get("operation") or "ADD",
                                   row.get("tag_ref"), "", *([""] * len(EDITORIAL)), row.get("status") or "pending",
                                   row.get("notes"), row.get("last_result")])
                new.save(path)
            old.close()
        if REFERENCES.exists():
            all_cached = json.loads(REFERENCES.read_text(encoding="utf-8"))
            cached = all_cached.get(args.env) or all_cached.get("local")
            if cached:
                update_reference_sheets(path, cached, args.env if args.env in all_cached else "local", args.env)
    if args.refresh_references:
        response = post(args.env, "/scraper/agentTagsAndCharactsReferences", {})
        if not response.get("success"):
            raise RuntimeError(response.get("error") or "Référentiels indisponibles")
        data = response["data"]
        current = json.loads(REFERENCES.read_text(encoding="utf-8")) if REFERENCES.exists() else {}
        current[args.env] = data
        REFERENCES.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        targets = (drive_workspace_root(args.env) / "izilife" / "tags").glob(f"*-zone/{FILE}") if args.refresh_all_zones else [path]
        updated = []
        for target in targets:
            update_reference_sheets(target, data, args.env, args.env)
            updated.append(str(target))
        print(f"Référentiels {args.env} : {data['generated_at']} ; {len(updated)} classeur(s) actualisé(s)")
    if not (args.init or args.refresh_references):
        process(path, SHEET, args.env, "/scraper/agentApplyTagsAndCharacts", payload, args.dry_run, args.max)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("tags_and_characts", "tags", main)
