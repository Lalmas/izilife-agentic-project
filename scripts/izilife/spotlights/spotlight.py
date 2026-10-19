from __future__ import annotations
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process

FILE,SHEET="spotlights.xlsx","Spotlights"
COLUMNS=[("scope_type","scope"),("scope_ref","scope"),("city_ref","scope"),("editorial_title","offer"),("editorial_description","offer"),("theme","offer"),("target_spotlight","access"),("target_perfect_for","access"),("target_today","access"),("target_next_days","access"),("rail_editorial_reason","access"),("rail_configuration_json","access"),("reasons_json","offer"),("start_date","access"),("end_date","access"),("priority","bpr"),("base_weight","bpr"),("publication_status","bpr"),("status","result"),("notes","result"),("last_result","result")]

def as_bool(value):
    return int(str(value or "").strip().lower() in {"1","true","yes","oui","y","x"})

def payload(r):
    destinations = [as_bool(r.get(name)) for name in ("target_spotlight","target_perfect_for","target_today","target_next_days")]
    if not any(destinations): raise ValueError("Au moins une destination doit être activée.")
    return {"target_type":str(r.get("scope_type") or "").upper(),"target_string_id":r.get("scope_ref"),"city_string_id":r.get("city_ref"),"editorial_title":r.get("editorial_title"),"editorial_description":r.get("editorial_description"),"theme":r.get("theme"),"spotlight":destinations[0],"perfect_for":destinations[1],"rail_today":destinations[2],"rail_future":destinations[3],"rail_reason":r.get("rail_editorial_reason"),"rail_configuration_json":r.get("rail_configuration_json"),"reasons_json":r.get("reasons_json"),"start_date":r.get("start_date"),"end_date":r.get("end_date"),"priority":r.get("priority") or 0,"base_weight":r.get("base_weight") or 1,"status":r.get("publication_status") or "DRAFT"}

def main():
    ap=argparse.ArgumentParser(description="Une ligne par objet, avec trois colonnes de destination."); ap.add_argument("--zone",required=True); ap.add_argument("--env",choices=["local","staging","prod"],default="staging"); ap.add_argument("--init",action="store_true"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--max",type=int,default=100); a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"spotlights"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"scope_type":"PLACE","scope_ref":"marche-de-wazemmes","city_ref":"lille","editorial_title":"Le marché incontournable","editorial_description":"Une sélection éditoriale locale.","theme":"sorties","target_spotlight":"oui","target_perfect_for":"non","target_today":"oui","target_next_days":"oui","reasons_json":"","priority":10,"base_weight":1,"publication_status":"DRAFT","status":"skip","notes":"reasons_json est optionnel. Vide = aucune raison GOOD_FOR/WHY créée.","last_result":""}
        yes_no=["oui","non"]
        create_workbook(path,SHEET,COLUMNS,ex,{"scope_type":["PLACE","SHOP","EVENT","EVENT_SERIE","EXPERIENCE"],"target_spotlight":yes_no,"target_perfect_for":yes_no,"target_today":yes_no,"target_next_days":yes_no,"publication_status":["DRAFT","PUBLISHED","ARCHIVED"],"status":["pending","done","error","skip"]}); return
    process(path,SHEET,a.env,"/scraper/agentUpsertSpotlight",payload,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); from agent_excel_logger import run_logged; run_logged("spotlights","spotlights",main)
