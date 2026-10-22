from __future__ import annotations
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process

FILE,SHEET="equipments.xlsx","Equipments"
COLUMNS=[("scope_type","scope"),("scope_ref","scope"),("name","offer"),("category_ref","offer"),("internal_id","offer"),("description","offer"),("capacity","offer"),("instance_count","offer"),("instance_capacity","offer"),("instances_json","offer"),("characteristics_json","offer"),("localization_text","access"),("address","access"),("city_ref","access"),("longitude","access"),("latitude","access"),("exterior","bpr"),("is_privatisable","bpr"),("is_active","bpr"),("status","result"),("notes","result"),("last_result","result")]
CATEGORY_REF_ALIASES={"espace":"salle-restauration"}

def _json_object(value,label):
    if value in (None,""): return {} if label=="characteristics_json" else []
    if isinstance(value,(dict,list)): return value
    try: return json.loads(str(value))
    except json.JSONDecodeError as exc: raise ValueError(f"{label}: JSON invalide ({exc.msg})") from exc

def payload(r):
    data={k:r.get(k) for k in ["scope_type","scope_ref","name","category_ref","internal_id","description","capacity","instance_count","instance_capacity","localization_text","address","city_ref","longitude","latitude","exterior","is_privatisable","is_active"]}
    category_ref=str(data.get("category_ref") or "").strip()
    data["category_ref"]=CATEGORY_REF_ALIASES.get(category_ref,category_ref)
    data["instances"]=_json_object(r.get("instances_json"),"instances_json")
    data["characteristics"]=_json_object(r.get("characteristics_json"),"characteristics_json")
    return data

def main():
    ap=argparse.ArgumentParser(description="Ajout manuel idempotent d'Equipment, sans LLM.");ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"equipments"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"scope_type":"PLACE","scope_ref":"marche-de-wazemmes","name":"Salle principale","category_ref":"salle-restauration","internal_id":"salle-principale","capacity":50,"characteristics_json":'{"accessible-handicap": true, "wifi": true}',"instances_json":'[{"instance_code":"salle-1","name":"Salle principale","capacity":50}]',"exterior":"non","is_privatisable":"oui","is_active":"oui","status":"skip","notes":"Les clés characteristics_json sont les string_id autorisés pour la catégorie. Une clé absente ne supprime jamais une valeur BO."}
        create_workbook(path,SHEET,COLUMNS,ex,{"scope_type":["PLACE","SHOP","PAGE","PARTNER","EVENT","EVENT_SERIE","ANNUAL_CELEBRATION","CITY","ADMINISTRATIVE_DIVISION"],"exterior":["oui","non"],"is_privatisable":["oui","non"],"is_active":["oui","non"],"status":["pending","done","error","skip","unmapped"]});return
    process(path,SHEET,a.env,"/scraper/agentUpsertEquipment",payload,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("equipments","equipments",main)
