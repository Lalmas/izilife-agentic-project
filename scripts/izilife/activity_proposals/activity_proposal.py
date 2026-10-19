from __future__ import annotations
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process
FILE,SHEET="activity_proposals.xlsx","ActivityProposals"
COLUMNS=[("scope_type","scope"),("scope_ref","scope"),("occasion_ref","offer"),("action_1","offer"),("action_2","offer"),("action_3","offer"),("title_template","offer"),("contextual_description","offer"),("special_activity_show","access"),("is_active","bpr"),("status","result"),("notes","result"),("last_result","result")]
def payload(r):return {k:r.get(k) for k in ["scope_type","scope_ref","occasion_ref","action_1","action_2","action_3","title_template","contextual_description","special_activity_show","is_active"]}
def main():
    ap=argparse.ArgumentParser(description="Propositions d'activité contextualisées par cible.");ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"activity-proposals"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"scope_type":"PLACE","scope_ref":"parc-de-la-dreve","occasion_ref":"date","action_1":"se-poser","action_2":"pique-niquer","title_template":"Se poser et pique-niquer au parc","contextual_description":"Une idée simple pour profiter du lieu.","is_active":"oui","status":"skip","notes":"occasion_ref peut rester vide pour une proposition générique."}
        create_workbook(path,SHEET,COLUMNS,ex,{"scope_type":["PLACE","SHOP","EVENT","EVENT_SERIE","EXPERIENCE","ANNUAL_CELEBRATION"],"is_active":["oui","non"],"status":["pending","done","error","skip"]});return
    process(path,SHEET,a.env,"/scraper/agentUpsertActivityProposal",payload,a.dry_run,a.max)
if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("activity_proposals","activity_proposals",main)
