#!/usr/bin/env python3
"""Pilote Excel unique des transferts, avec blocage explicite des capacités non sûres."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.paths import transfer_file

from location_transfer import post, PLAN_ENDPOINT, APPLY_ENDPOINT

TYPES = ["PLACE", "SHOP", "PAGE", "EQUIPMENT", "EVENT", "EXPERIENCE",
         "EVENT_SERIE", "ANNUAL_CELEBRATION", "REPRESENTATION"]
HEADERS = ["SOURCE_TYPE", "SOURCE_REF", "DESTINATION_TYPE", "DESTINATION_REF",
           "DESTINATION_MODE", "DESTINATION_NAME", "DESTINATION_CATEGORY_REF",
           "ACTIVATE_DESTINATION", "ACTION", "STATUS", "CAN_APPLY", "PLAN_HASH",
           "PLAN_JSON", "RESULT", "ERROR"]


def capability(source: str, destination: str) -> tuple[str, str]:
    if source in {"PLACE", "SHOP", "PAGE", "EQUIPMENT"} and destination in {"PLACE", "SHOP", "PAGE", "EQUIPMENT"}:
        return "AGENT_PLAN_APPLY", "Transaction, plan figé, journal idempotent, archivage source."
    if source in {"EVENT", "EXPERIENCE", "EVENT_SERIE", "ANNUAL_CELEBRATION", "REPRESENTATION"} and destination in {"EVENT", "EXPERIENCE", "EVENT_SERIE", "ANNUAL_CELEBRATION", "REPRESENTATION"}:
        return "BO_FOUR_EYES", "Demande BO, approbateur distinct, transfert puis archivage réversible."
    return "BLOCKED", "Relations métier non déclarées : conversion automatique interdite sans stratégie validée."


def init(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook(); ws = wb.active; ws.title = "Transferts"
    ws.append(HEADERS)
    ws.append(["SHOP", "", "PLACE", "", "EXISTING", "", "", "NON", "PLAN", "pending"])
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF"); cell.fill = PatternFill("solid", fgColor="1F4E78")
    ws.freeze_panes = "A2"; ws.auto_filter.ref = f"A1:O1000"
    widths = [18,28,22,28,20,30,28,22,14,16,14,68,28,38,38]
    for i, width in enumerate(widths, 1): ws.column_dimensions[chr(64+i)].width = width
    for col, values in (("A", TYPES), ("C", TYPES), ("E", ["EXISTING","CREATE"]),
                        ("H", ["OUI","NON"]), ("I", ["PLAN","APPLY"]),
                        ("J", ["pending","planned","blocked","done","error","skip"])):
        dv=DataValidation(type="list", formula1='"'+','.join(values)+'"'); ws.add_data_validation(dv); dv.add(f"{col}2:{col}1000")
    guide=wb.create_sheet("Matrice"); guide.append(["SOURCE", "DESTINATION", "CAPACITE", "GARANTIE"])
    for s in TYPES:
        for d in TYPES:
            mode, note = capability(s, d); guide.append([s,d,mode,note])
    for cell in guide[1]: cell.font=Font(bold=True,color="FFFFFF"); cell.fill=PatternFill("solid",fgColor="1F4E78")
    guide.freeze_panes="A2"; guide.auto_filter.ref=f"A1:D{guide.max_row}"
    for col,width in zip("ABCD",[24,24,22,85]): guide.column_dimensions[col].width=width
    wb.save(path)


def process(path: Path, env: str, allow_apply: bool) -> None:
    wb=load_workbook(path); ws=wb["Transferts"]
    columns={str(c.value):i+1 for i,c in enumerate(ws[1])}
    for row in range(2, ws.max_row+1):
        get=lambda key: str(ws.cell(row,columns[key]).value or "").strip()
        put=lambda key,value: ws.cell(row,columns[key],value)
        if get("STATUS").lower() not in {"", "pending"}: continue
        source,destination=get("SOURCE_TYPE").upper(),get("DESTINATION_TYPE").upper()
        if not source and not destination: continue
        mode,note=capability(source,destination)
        if mode != "AGENT_PLAN_APPLY":
            put("STATUS", "blocked" if mode == "BLOCKED" else "planned")
            put("RESULT", note); wb.save(path); continue
        try:
            payload={"source_type":source,"source_ref":get("SOURCE_REF"),"destination_type":destination,
                     "destination_ref":get("DESTINATION_REF"),"destination_mode":get("DESTINATION_MODE") or "EXISTING",
                     "destination_name":get("DESTINATION_NAME"),"destination_category_ref":get("DESTINATION_CATEGORY_REF"),
                     "activate_destination":get("ACTIVATE_DESTINATION").upper()=="OUI"}
            if get("ACTION").upper()=="APPLY":
                if not allow_apply:raise RuntimeError("APPLY exige l’option --apply.")
                plan=json.loads(get("PLAN_JSON") or "{}")
                if not plan.get("can_apply") or not get("PLAN_HASH"):raise RuntimeError("Un plan figé applicable est requis avant APPLY.")
                payload.update({"plan_hash":get("PLAN_HASH"),"confirm_apply":"LOCATION_TRANSFER_APPLY",
                    "idempotency_key":f"transfer:{env}:{source}:{get('SOURCE_REF')}:{destination}:{get('DESTINATION_REF')}:{get('PLAN_HASH')[:16]}"})
                result=post(env,APPLY_ENDPOINT,payload);put("STATUS","done");put("RESULT",json.dumps(result,ensure_ascii=False)[:3000]);put("ERROR","")
            else:
                plan=post(env,PLAN_ENDPOINT,payload)["plan"]
                put("CAN_APPLY","OUI" if plan.get("can_apply") else "NON"); put("PLAN_HASH",plan.get("plan_hash",""))
                put("PLAN_JSON",json.dumps(plan,ensure_ascii=False)); put("STATUS","planned" if plan.get("can_apply") else "blocked")
                put("RESULT",f"{len(plan.get('actions',[]))} actions, {len(plan.get('blockers',[]))} bloqueurs"); put("ERROR","")
        except Exception as exc:
            put("STATUS","error"); put("ERROR",str(exc))
        wb.save(path)


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=["init","plan","run"])
    parser.add_argument("--zone",required=True); parser.add_argument("--env",choices=["local","staging","prod"],default="local")
    parser.add_argument("--apply",action="store_true");parser.add_argument("--confirm-production")
    args=parser.parse_args(); path=transfer_file(args.zone,args.env)
    if args.apply and args.env=="prod" and args.confirm_production!="I_CONFIRM_PRODUCTION_TRANSFER":raise SystemExit("Production refusée sans confirmation dédiée.")
    if args.command=="init": init(path)
    else: process(path,args.env,args.apply)
    print(path)

if __name__ == "__main__": main()
