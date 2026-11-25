from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import openpyxl

BASE = Path(r"C:\Users\alcamara\Documents\agentic_Workspace\outputs\prepare_intelligent_improver_20261112.py")
REPORT = Path(r"C:\Users\alcamara\Documents\agentic_Workspace\outputs\intelligent_improver_20261112\preparation_report.json")
TARGET = Path(r"G:\Mon Drive\agentic_workspace\izilife\places\lille-zone\ameliorateur.xlsx")

spec = importlib.util.spec_from_file_location("batch", BASE)
batch = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(batch)

payload = json.loads(REPORT.read_text(encoding="utf-8"))
resolved = []
for item in payload["unresolved"]:
    value = item["value"]
    preferred_type = ""
    ref = ""
    if ":" in value and value.split(":", 1)[0].upper() in {"SHOP", "PLACE"}:
        preferred_type, ref = value.split(":", 1)
        preferred_type, ref = preferred_type.strip().upper(), ref.strip()
    elif item["source_column"] == "I":
        ref = batch.norm(value).replace(" ", "-")
    if not ref:
        continue
    answer = batch.resolve_ref(ref, preferred_type)
    if answer:
        resolved.append(item | answer)

wb = openpyxl.load_workbook(TARGET)
ws = wb["Prioritaires"]
headers = [str(c.value or "").strip().lower() for c in ws[1]]
col = {name: idx + 1 for idx, name in enumerate(headers)}
existing = {
    (str(ws.cell(r, col["type"]).value or "").strip().upper(), str(ws.cell(r, col["string_id"]).value or "").strip())
    for r in range(2, ws.max_row + 1)
}
appended = []
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
    appended.append(item)
wb.save(TARGET)
print(json.dumps({"resolved": len(resolved), "appended": len(appended), "items": appended}, ensure_ascii=False, indent=2))
