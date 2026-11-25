"""Manual deterministic improver for places, shops, events and experiences.

The workbook is authoritative. No OpenAI/OCR call is made by this script.
Targets accept an iziLife URL, numeric id, string_id or unique_id.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import openpyxl
import requests
from openpyxl.worksheet.datavalidation import DataValidation

SHEETS = {
    "Lieux": "",
    "Events": "",
    "XP": "EXPERIENCE",
}
HEADERS = [
    "target_ref", "target_type", "update_mode", "status", "notes",
    "title", "name", "description", "short_description",
    "start_date", "start_hour", "end_date", "end_hour", "ticketing_url", "basic_price",
    "event_category_ref", "principal_activity_category_string_id",
    "sport_string_id", "dance_string_id", "music_style_string_id", "artisan_technique_string_id",
    "hobbies", "objects", "music_styles", "dances", "sports", "tags",
    "principal_characteristics", "processed_at", "result_json",
]


def init_workbook(path: Path) -> None:
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    for name in SHEETS:
        ws = wb.create_sheet(name); ws.append(HEADERS); ws.freeze_panes = "A2"; ws.auto_filter.ref = "A1:AD1"
        ws.column_dimensions["A"].width = 70; ws.column_dimensions["H"].width = 70
        for header in ws[1]:
            header.font = openpyxl.styles.Font(bold=True, color="FFFFFF")
            header.fill = openpyxl.styles.PatternFill("solid", fgColor="17365D")
        for column, values in {"B":"PLACE,SHOP,EVENT,EVENT_SERIE,ANNUAL_CELEBRATION,REPRESENTATION,EXPERIENCE", "C":"ENRICH,OVERWRITE", "D":"pending,done,error,skip"}.items():
            dv=DataValidation(type="list",formula1=f'"{values}"',allow_blank=True);ws.add_data_validation(dv);dv.add(f"{column}2:{column}1000")
    path.parent.mkdir(parents=True,exist_ok=True);wb.save(path)


def cell_value(value):
    if isinstance(value, datetime): return value.strftime("%Y-%m-%d %H:%M:%S")
    if hasattr(value, "strftime"): return value.strftime("%Y-%m-%d")
    return value


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument("workbook",type=Path);parser.add_argument("--base-url",default="http://localhost/izilife-admin/");parser.add_argument("--init",action="store_true");parser.add_argument("--dry-run",action="store_true");args=parser.parse_args()
    if args.init or not args.workbook.exists(): init_workbook(args.workbook)
    if args.init:return
    token=os.environ.get("IZILIFE_AGENT_TOKEN","").strip()
    if not args.dry_run and not token:raise RuntimeError("IZILIFE_AGENT_TOKEN non défini")
    wb=openpyxl.load_workbook(args.workbook)
    for sheet_name, default_type in SHEETS.items():
        if sheet_name not in wb.sheetnames:continue
        ws=wb[sheet_name];headers={str(c.value or "").strip():i+1 for i,c in enumerate(ws[1])}
        for row_idx in range(2,ws.max_row+1):
            get=lambda key: cell_value(ws.cell(row_idx,headers[key]).value) if key in headers else None
            if str(get("status") or "").lower()!="pending" or not str(get("target_ref") or "").strip():continue
            payload={key:get(key) for key in HEADERS if key not in {"status","notes","processed_at","result_json"} and get(key) not in (None,"")}
            payload["target_type"]=payload.get("target_type") or default_type
            if args.dry_run:result={"success":True,"dry_run":True,"payload":payload}
            else:
                response=requests.post(args.base_url.rstrip("/")+"/scraper/agentApplyManualCuration",json=payload,headers={"X-Agent-Token":token},timeout=60)
                result=response.json();response.raise_for_status()
            ws.cell(row_idx,headers["status"]).value="done" if result.get("success") else "error"
            ws.cell(row_idx,headers["processed_at"]).value=datetime.now().strftime("%Y-%m-%d %H:%M")
            ws.cell(row_idx,headers["result_json"]).value=json.dumps(result,ensure_ascii=False)[:32000]
            wb.save(args.workbook)


if __name__ == "__main__": main()
