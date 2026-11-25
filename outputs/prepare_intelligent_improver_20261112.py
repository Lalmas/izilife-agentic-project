from __future__ import annotations

import json
import os
import re
import shutil
import unicodedata
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import openpyxl
import requests


SOURCE = Path(r"C:\Users\alcamara\AppData\Local\Packages\sandbox.{d59ce699-2cf2-4dd8-bfce-0c0769eebb89}\AC\Temp\browser-use\exports\Curation - Démarchage.xlsm-d1747791-1fd5-4a1e-b8e9-c0c61da5c8f2.xlsx")
INVENTORY = Path(r"G:\Mon Drive\inventaire_maps_seclin_alentours.xlsx")
TARGET = Path(r"G:\Mon Drive\agentic_workspace\izilife\places\lille-zone\ameliorateur.xlsx")
REPORT_DIR = Path(r"C:\Users\alcamara\Documents\agentic_Workspace\outputs\intelligent_improver_20261112")
BASE_URL = "https://www.izilife.co/izilife-admin"


def norm(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def post(path: str, payload: dict) -> tuple[int, dict]:
    token = os.environ.get("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN absent")
    response = requests.post(
        BASE_URL + path,
        json=payload,
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        timeout=60,
    )
    try:
        body = response.json()
    except Exception:
        body = {"error": response.text[:500]}
    return response.status_code, body


def resolve_ref(ref: str, preferred_type: str = "") -> dict | None:
    code, body = post("/scraper/agentInternalDataV0ResolvePlace", {"string_id": ref})
    if code == 200 and body.get("success"):
        item = body.get("item") or {}
        entity_type = str(item.get("type") or "").upper()
        if entity_type in {"SHOP", "PLACE"} and (not preferred_type or entity_type == preferred_type):
            return {"type": entity_type, "string_id": item.get("string_id") or ref, "name": item.get("name", ""), "method": "string_id"}
    return None


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    src = openpyxl.load_workbook(SOURCE, data_only=True)["Lieux Clean, Cur (Hor, Ph, ..)"]
    raw: list[dict] = []
    for row in range(2, src.max_row + 1):
        value = src.cell(row, 9).value
        if value not in (None, ""):
            raw.append({"source_column": "I", "source_row": row, "value": str(value).strip()})
    for row in range(2, src.max_row + 1):
        value = src.cell(row, 8).value
        if value not in (None, ""):
            raw.append({"source_column": "H", "source_row": row, "value": str(value).strip()})

    inv = openpyxl.load_workbook(INVENTORY, data_only=True)["Inventaire"]
    headers = [str(cell.value or "").strip() for cell in inv[1]]
    pos = {name: idx + 1 for idx, name in enumerate(headers)}
    by_name: dict[str, list[dict]] = defaultdict(list)
    by_ref: dict[str, list[dict]] = defaultdict(list)
    for row in range(2, inv.max_row + 1):
        name = str(inv.cell(row, pos["NOM"]).value or "").strip()
        ref = str(inv.cell(row, pos["IZILIFE_STRING_ID"]).value or "").strip()
        entity_type = str(inv.cell(row, pos["IZILIFE_TYPE"]).value or "").strip().upper()
        item = {
            "inventory_row": row,
            "name": name,
            "google_place_id": str(inv.cell(row, pos["GOOGLE_PLACE_ID"]).value or "").strip(),
            "type": entity_type,
            "string_id": ref,
        }
        if name:
            by_name[norm(name)].append(item)
        if ref:
            by_ref[ref].append(item)

    resolved: list[dict] = []
    unresolved: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for target in raw:
        value = target["value"]
        preferred_type = ""
        ref = ""
        if ":" in value and value.split(":", 1)[0].upper() in {"SHOP", "PLACE"}:
            preferred_type, ref = value.split(":", 1)
            preferred_type = preferred_type.upper().strip()
            ref = ref.strip()
        elif re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
            ref = value

        answer = resolve_ref(ref, preferred_type) if ref else None
        if not answer and not ref:
            slug_candidate = norm(value).replace(" ", "-")
            answer = resolve_ref(slug_candidate)
            if answer:
                answer["method"] = "derived_string_id"

        candidates = by_name.get(norm(value), [])
        if not answer and len({(c["type"], c["string_id"]) for c in candidates if c["type"] in {"SHOP", "PLACE"} and c["string_id"]}) == 1:
            c = next(c for c in candidates if c["type"] in {"SHOP", "PLACE"} and c["string_id"])
            answer = resolve_ref(c["string_id"], c["type"])
            if answer:
                answer["method"] = "inventory_string_id"

        if not answer and candidates:
            google_ids = list(dict.fromkeys(c["google_place_id"] for c in candidates if c["google_place_id"]))
            found = []
            for google_id in google_ids:
                code, body = post("/scraper/agentInternalDataV0ResolvePlace", {"google_place_id": google_id})
                item = body.get("item") if code == 200 and body.get("success") else None
                if item and item.get("type") in {"SHOP", "PLACE"} and item.get("string_id"):
                    found.append((item["type"], item["string_id"], item.get("name", "")))
            found = list(dict.fromkeys(found))
            if len(found) == 1:
                answer = {"type": found[0][0], "string_id": found[0][1], "name": found[0][2], "method": "google_place_id"}

        if not answer:
            code, body = post("/scraper/agentInternalDataV0ResolvePlace", {"query": value})
            item = body.get("item") if code == 200 and body.get("success") else None
            if item and item.get("type") in {"SHOP", "PLACE"} and item.get("string_id"):
                answer = {"type": item["type"], "string_id": item["string_id"], "name": item.get("name", ""), "method": "exact_name"}

        if not answer:
            unresolved.append(target | {"inventory_candidates": candidates})
            continue
        key = (answer["type"], answer["string_id"])
        if key in seen:
            continue
        seen.add(key)
        resolved.append(target | answer)

    backup = TARGET.with_name(f"{TARGET.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}{TARGET.suffix}")
    shutil.copy2(TARGET, backup)
    wb = openpyxl.load_workbook(TARGET)
    ws = wb["Prioritaires"]
    target_headers = [str(cell.value or "").strip().lower() for cell in ws[1]]
    col = {name: idx + 1 for idx, name in enumerate(target_headers)}
    existing = {
        (str(ws.cell(row, col["type"]).value or "").strip().upper(), str(ws.cell(row, col["string_id"]).value or "").strip())
        for row in range(2, ws.max_row + 1)
    }
    appended = 0
    for item in resolved:
        key = (item["type"], item["string_id"])
        if key in existing:
            continue
        row = ws.max_row + 1
        ws.cell(row, col["string_id"], item["string_id"])
        ws.cell(row, col["type"], item["type"])
        ws.cell(row, col["notes"], f"Curation-Démarchage {item['source_column']}{item['source_row']} — {item['value']}")
        ws.cell(row, col["statut"], "pending")
        existing.add(key)
        appended += 1
    wb.save(TARGET)

    report = {
        "source_count": len(raw),
        "resolved_unique": len(resolved),
        "unresolved_count": len(unresolved),
        "appended": appended,
        "backup": str(backup),
        "target": str(TARGET),
        "resolved": resolved,
        "unresolved": unresolved,
    }
    (REPORT_DIR / "preparation_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("source_count", "resolved_unique", "unresolved_count", "appended", "backup", "target")}, ensure_ascii=False, indent=2))
    if unresolved:
        print("UNRESOLVED")
        for item in unresolved:
            print(f"{item['source_column']}{item['source_row']}\t{item['value']}")


if __name__ == "__main__":
    main()
