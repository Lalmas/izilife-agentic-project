#!/usr/bin/env python3
"""Curation Excel contrôlée des City et AdministrativeDivision iziLife."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offers"))
from offer_agent_common import drive_workspace_root, normalize_zone, post, scalar

FILE = "territories.xlsx"
CITY_COLUMNS = ["country","scope_ref","name","importance_score","ai_proposed_description","is_country_capital","is_country_principal_city","is_region_principal_city","is_department_principal_city","is_border_city","is_mountain_city","is_litoral_city","overtourism_indicator","source","confidence","manual_validation","status","notes","last_result"]
AD_COLUMNS = ["country","scope_ref","name","ai_proposed_description","is_mountain_division","is_litoral_division","source","confidence","manual_validation","status","notes","last_result"]

def add_validation(ws, column, values):
    idx=[c.value for c in ws[1]].index(column)+1; letter=openpyxl.utils.get_column_letter(idx)
    dv=DataValidation(type="list",formula1='"'+",".join(values)+'"',allow_blank=True); ws.add_data_validation(dv); dv.add(f"{letter}2:{letter}500")

def add_sheet(wb,title,columns,example):
    ws=wb.create_sheet(title); ws.append(columns); ws.append([example.get(c,"") for c in columns])
    for cell in ws[1]:
        cell.font=Font(bold=True,color="FFFFFF"); cell.fill=PatternFill("solid",fgColor="4472C4"); cell.alignment=Alignment(wrap_text=True)
        ws.column_dimensions[cell.column_letter].width=max(14,min(38,len(str(cell.value))+3))
    ws.freeze_panes="A2"; ws.auto_filter.ref=f"A1:{openpyxl.utils.get_column_letter(len(columns))}500"
    for field in [c for c in columns if c.startswith("is_")]: add_validation(ws,field,["oui","non"])
    add_validation(ws,"manual_validation",["oui","non"]); add_validation(ws,"status",["pending","done","skip","unmapped","error"])

def init(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): print(f"Existe déjà : {path}"); return
    wb=openpyxl.Workbook(); wb.remove(wb.active)
    add_sheet(wb,"Cities",CITY_COLUMNS,{"country":"FR","scope_ref":"lille","name":"Lille","importance_score":650,"is_region_principal_city":"oui","source":"validation éditoriale","confidence":1,"manual_validation":"non","status":"skip","notes":"Exemple : valider manuellement avant pending"})
    add_sheet(wb,"AdministrativeDivisions",AD_COLUMNS,{"country":"FR","scope_ref":"nord","name":"Nord","is_litoral_division":"oui","source":"validation éditoriale","confidence":1,"manual_validation":"non","status":"skip","notes":"Exemple : aucun héritage automatique vers les Cities"})
    refs=wb.create_sheet("Références"); refs.append(["Règle","Valeur"]); refs.append(["importance_score","Score mondial absolu de 0 à 1000, validé manuellement"]); refs.append(["description","La description humaine reste prioritaire; l'IA n'est qu'un fallback"]); refs.append(["rural/village","Hors insertion automatique : aucune estimation LLM"])
    wb.create_sheet("Unmapped").append(["sheet","row","scope_ref","reason"])
    wb.save(path); print(f"Créé : {path}")

def bool_or_blank(value):
    v=str(value or "").strip().lower()
    if not v:return None
    if v in {"oui","yes","true","1","x"}:return 1
    if v in {"non","no","false","0"}:return 0
    raise ValueError(f"Booléen invalide: {value}")

def payload(sheet,row):
    if str(row.get("manual_validation") or "").strip().lower() not in {"oui","yes","1","true"}: raise ValueError("manual_validation=oui obligatoire")
    result={"scope_type":"CITY" if sheet=="Cities" else "ADMINISTRATIVE_DIVISION","scope_ref":row.get("scope_ref")}
    allowed=CITY_COLUMNS if sheet=="Cities" else AD_COLUMNS
    for field in allowed:
        if field.startswith("is_"):
            value=bool_or_blank(row.get(field))
            if value is not None:result[field]=value
        elif field in {"importance_score","overtourism_indicator","ai_proposed_description","source","confidence"} and row.get(field) not in (None,""):result[field]=scalar(row[field])
    return result

def process(path,env,dry_run,maximum):
    wb=openpyxl.load_workbook(path); handled=created=skipped=errors=unmapped_count=0; unmapped_ws=wb["Unmapped"]
    for sheet_name in ("Cities","AdministrativeDivisions"):
        ws=wb[sheet_name]; headers=[str(c.value or "").strip() for c in ws[1]]; status_col=headers.index("status")+1; result_col=headers.index("last_result")+1
        for cells in ws.iter_rows(min_row=2):
            row={headers[i]:scalar(cells[i].value) for i in range(len(headers)) if headers[i]}
            if not any(v not in (None,"") for k,v in row.items() if k not in {"status","last_result"}):continue
            if str(row.get("status") or "pending").lower() in {"done","skip"}:skipped+=1;continue
            if handled>=maximum:break
            try:
                data=payload(sheet_name,row)
                if dry_run:print("[DRY RUN]",json.dumps(data,ensure_ascii=False));handled+=1;continue
                response=post(env,"/scraper/agentUpsertTerritory",data); ok=bool(response.get("success")); message=json.dumps(response,ensure_ascii=False)[:1000]
                if ok:ws.cell(cells[0].row,status_col,"done");created+=int(bool(response.get("created")))
                elif "introuvable" in str(response.get("error","")).lower():ws.cell(cells[0].row,status_col,"unmapped");unmapped_ws.append([sheet_name,cells[0].row,row.get("scope_ref"),response.get("error")]);unmapped_count+=1
                else:ws.cell(cells[0].row,status_col,"error");errors+=1
                ws.cell(cells[0].row,result_col,message);print("OK" if ok else "ERREUR",response)
            except Exception as exc:
                errors+=1;print("ERREUR",exc)
                if not dry_run:ws.cell(cells[0].row,status_col,"error");ws.cell(cells[0].row,result_col,str(exc)[:1000])
            handled+=1
    if not dry_run:wb.save(path)
    print(f"Traités: {handled}");print(f"Créés: {created}");print(f"Skippés: {skipped}");print(f"Unmapped: {unmapped_count}");print(f"Erreurs: {errors}")

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"geography"/normalize_zone(a.zone)/FILE
    init(path) if a.init else process(path,a.env,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("territories","geography",main)
