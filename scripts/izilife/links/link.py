from __future__ import annotations
import argparse,sys
from pathlib import Path
from urllib.parse import urlparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process,as_bool

FILE,SHEET="links.xlsx","Links"
COLUMNS=[("scope_type","scope"),("scope_ref","scope"),("url","offer"),("title","offer"),("source_type","offer"),("start_date","access"),("end_date","access"),("highlighted","access"),("is_official_website","access"),("order","bpr"),("status","result"),("notes","result"),("last_result","result")]

def source_type(url):
    host=(urlparse(str(url)).hostname or "").lower().removeprefix("www.")
    known={"privateaser.com":"privateaser","ubereats.com":"uber-eats","deliveroo.fr":"deliveroo","deliveroo.com":"deliveroo","dokaa.com":"dokaa","sundayapp.com":"sunday","instagram.com":"instagram","facebook.com":"facebook"}
    return next((label for domain,label in known.items() if host==domain or host.endswith("."+domain)),"website")

def payload(r):
    url=str(r.get("url") or "").strip(); detected=str(r.get("source_type") or "").strip() or source_type(url)
    return {"target_type":r.get("scope_type"),"target_string_id":r.get("scope_ref"),"url":url,"title":r.get("title") or detected,"start_date":r.get("start_date"),"end_date":r.get("end_date"),"highlighted":as_bool(r.get("highlighted")),"is_official_website":as_bool(r.get("is_official_website")),"order":r.get("order") or 0}

def main():
    ap=argparse.ArgumentParser(description="Ajout idempotent de Link depuis Excel.");ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"links"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"scope_type":"PLACE","scope_ref":"marche-de-wazemmes","url":"https://example.org/menu?lang=fr","title":"Menu officiel","source_type":"website","highlighted":"non","is_official_website":"oui","order":0,"status":"skip","notes":"Exemple : adapter puis mettre pending"}
        create_workbook(path,SHEET,COLUMNS,ex,{"scope_type":["PLACE","SHOP","PAGE","PARTNER","EVENT","EXPERIENCE","EVENT_SERIE","ANNUAL_CELEBRATION"],"highlighted":["oui","non"],"is_official_website":["oui","non"],"status":["pending","done","error","skip","unmapped"]});return
    process(path,SHEET,a.env,"/scraper/agentUpsertLink",payload,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("links","links",main)
