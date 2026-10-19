from __future__ import annotations
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process
FILE,SHEET="tags.xlsx","Tags"
COLUMNS=[("scope_type","scope"),("scope_ref","scope"),("tag_ref","offer"),("operation","access"),("status","result"),("notes","result"),("last_result","result")]
def payload(r):return {"scope_type":r.get("scope_type"),"scope_ref":r.get("scope_ref"),"tag_ref":r.get("tag_ref"),"operation":r.get("operation") or "ADD"}
def main():
    ap=argparse.ArgumentParser(description="Affecter ou retirer des tags existants sur des objets iziLife.");ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"tags"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"scope_type":"PLACE","scope_ref":"parc-de-la-dreve","tag_ref":"parfait-pour-un-date","operation":"ADD","status":"skip","notes":"Le tag doit déjà exister dans ShopAndPlaceCharactTag."}
        create_workbook(path,SHEET,COLUMNS,ex,{"scope_type":["PLACE","SHOP","EVENT","EVENT_SERIE","EXPERIENCE","ANNUAL_CELEBRATION"],"operation":["ADD","REMOVE"],"status":["pending","done","error","skip"]});return
    process(path,SHEET,a.env,"/scraper/agentApplyTag",payload,a.dry_run,a.max)
if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("tags","tags",main)
