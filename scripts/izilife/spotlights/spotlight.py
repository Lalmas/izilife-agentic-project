from __future__ import annotations
import argparse,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process

FILE,SHEET="spotlights.xlsx","Spotlights"
COLUMNS=[("target_type","scope"),("target_string_id","scope"),("city_string_id","scope"),("description","offer"),("theme","offer"),("destinations","access"),("start_date","access"),("end_date","access"),("priority","bpr"),("base_weight","bpr"),("publication_status","bpr"),("status","result"),("last_result","result")]

def payload(r):
    raw={re.sub(r"[^a-z0-9]+","-",x.strip().lower()).strip("-") for x in re.split(r"[,;&|]+",str(r.get("destinations") or "")) if x.strip()}
    aliases={"classique":"spotlight","aujourdhui":"today","aujourd-hui":"today","prochains-jours":"future","prochain":"future"}; d={aliases.get(x,x) for x in raw}
    if not d or d-{"spotlight","today","future"}: raise ValueError("destinations invalide: spotlight, aujourdhui, prochains-jours")
    return {"target_type":str(r.get("target_type") or "").upper(),"target_string_id":r.get("target_string_id"),"city_string_id":r.get("city_string_id"),"description":r.get("description"),"theme":r.get("theme"),"spotlight":int("spotlight" in d),"rail_today":int("today" in d),"rail_future":int("future" in d),"start_date":r.get("start_date"),"end_date":r.get("end_date"),"priority":r.get("priority") or 0,"base_weight":r.get("base_weight") or 1,"status":r.get("publication_status") or "DRAFT"}

def main():
    ap=argparse.ArgumentParser(description="Une ligne par objet; destinations combinées dans une cellule."); ap.add_argument("--zone",required=True); ap.add_argument("--env",choices=["local","staging","prod"],default="staging"); ap.add_argument("--init",action="store_true"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--max",type=int,default=100); a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"spotlights"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"target_type":"PLACE","target_string_id":"soultrain-cafe","city_string_id":"lille","description":"À ne pas manquer.","theme":"sorties","destinations":"spotlight,aujourdhui,prochains-jours","priority":10,"base_weight":1,"publication_status":"DRAFT","status":"skip","last_result":"EXEMPLE — copier puis mettre pending"}
        create_workbook(path,SHEET,COLUMNS,ex,{"target_type":["PLACE","SHOP","EVENT","EVENT_SERIE","EXPERIENCE"],"destinations":["spotlight","aujourdhui","prochains-jours","spotlight,aujourdhui","spotlight,prochains-jours","spotlight,aujourdhui,prochains-jours"],"publication_status":["DRAFT","PUBLISHED","ARCHIVED"],"status":["pending","done","error","skip"]}); return
    process(path,SHEET,a.env,"/scraper/agentUpsertSpotlight",payload,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); from agent_excel_logger import run_logged; run_logged("spotlights","spotlight",main)
