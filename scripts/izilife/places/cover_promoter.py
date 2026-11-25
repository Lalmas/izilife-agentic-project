"""Promeut un média déjà rattaché en cover, sans duplication de fichier."""
from __future__ import annotations
import argparse,json,os,sys
from pathlib import Path
import requests
SCRIPTS=Path(__file__).resolve().parents[2];IZILIFE=Path(__file__).resolve().parents[1]
for root in (SCRIPTS,IZILIFE):
    if str(root) not in sys.path:sys.path.insert(0,str(root))
from core.paths import IZILIFE_ENVS
from objects.object_agent_common import load_env

def main():
    p=argparse.ArgumentParser();p.add_argument("--env",choices=["local","staging","prod"],default="local");p.add_argument("--target",action="append",default=[]);p.add_argument("--apply",action="store_true");p.add_argument("--confirm-production");a=p.parse_args();load_env()
    if a.apply and a.env=="prod" and a.confirm_production!="I_CONFIRM_PRODUCTION_COVERS":raise SystemExit("Production refusée sans confirmation explicite.")
    token=os.getenv("IZILIFE_AGENT_TOKEN","").strip();cfg=IZILIFE_ENVS[a.env];results=[]
    if not token and a.target:raise SystemExit("IZILIFE_AGENT_TOKEN manquant.")
    for target in a.target:
        if ":" not in target:raise SystemExit(f"Cible invalide: {target}")
        scope_type,scope_ref=target.split(":",1)
        response=requests.post(cfg["base_url"].rstrip("/")+"/scraper/agentPromoteExistingCover",json={"scope_type":scope_type.upper(),"scope_ref":scope_ref,"dry_run":not a.apply},headers={"X-Agent-Token":token},verify=cfg.get("verify_ssl",True),timeout=120)
        body=response.json();results.append({"target":target,"http":response.status_code,"result":body})
        if response.status_code>=400 or not body.get("success"):raise SystemExit(json.dumps(results,ensure_ascii=False))
    print(json.dumps({"success":True,"dry_run":not a.apply,"results":results},ensure_ascii=False))
if __name__=="__main__":main()
