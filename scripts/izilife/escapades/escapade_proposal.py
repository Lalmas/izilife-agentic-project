from __future__ import annotations
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process

FILE,SHEET="escapade_proposals.xlsx","EscapadeProposals"
COLUMNS=[("scope_type","scope"),("scope_ref","scope"),("proposal_types","offer"),("editorial_title","offer"),("editorial_description","offer"),("profiles","offer"),("weather","offer"),("reason_refs","offer"),("start_month","access"),("end_month","access"),("priority","bpr"),("is_active","bpr"),("status","result"),("notes","result"),("last_result","result")]

def payload(r):return {k:r.get(k) for k in ["scope_type","scope_ref","proposal_types","editorial_title","editorial_description","profiles","weather","reason_refs","start_month","end_month","priority","is_active"]}

def main():
    ap=argparse.ArgumentParser(description="Curation massive des EscapadeProposal.");ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"escapades"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"scope_type":"CITY","scope_ref":"lille","proposal_types":"day_trip,city_trip","editorial_title":"Lille en une journée","editorial_description":"Une proposition éditoriale pour découvrir la ville à votre rythme.","profiles":"en-couple,en-famille,touriste","weather":"sunny,rainy","reason_refs":"visiter-la-ville,patrimoine","priority":10,"is_active":"oui","status":"skip","notes":"Exemple : adapter puis mettre pending"}
        create_workbook(path,SHEET,COLUMNS,ex,{"scope_type":["CITY","ADMINISTRATIVE_DIVISION","PLACE","SHOP","ANNUAL_CELEBRATION","EVENT_SERIE"],"is_active":["oui","non"],"status":["pending","done","error","skip","unmapped"]});return
    process(path,SHEET,a.env,"/scraper/agentUpsertEscapadeProposal",payload,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("escapade_proposals","escapades",main)
