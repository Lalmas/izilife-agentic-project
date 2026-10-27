#!/usr/bin/env python3
"""Planifie et transfère les objets éditoriaux hors Place/Shop.

Le plan fusionne local puis staging par clé métier; staging gagne en cas de clé
identique. Toute proposition contenant le mot isolé "test" est exclue.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re
from datetime import datetime
from pathlib import Path
from typing import Any
import requests, urllib3

ENVS={"local":("https://localhost:4443/izilife-admin",False),"staging":("https://www.staging.izilife.co/izilife-admin",True),"prod":("https://www.izilife.co/izilife-admin",True)}
EXPORT="/scraper/agentExportCurationExtras"
UPSERT={"escapade_proposals":"/scraper/agentUpsertEscapadeProposal","activity_proposals":"/scraper/agentUpsertActivityProposal","territories":"/scraper/agentUpsertTerritory","campaigns":"/scraper/agentUpsertPublicCampaign"}
TEST=re.compile(r"(?:^|[^a-z0-9])test(?:[^a-z0-9]|$)",re.I)

class Api:
 def __init__(self,token:str,timeout:int):self.h={"X-Agent-Token":token,"Accept":"application/json"};self.timeout=timeout;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 def post(self,env:str,path:str,payload:dict[str,Any],form=False)->dict[str,Any]:
  base,verify=ENVS[env];kw={"data":{"payload":json.dumps(payload,ensure_ascii=False)}} if form else {"json":payload}
  r=requests.post(base+path,headers=self.h,timeout=self.timeout,verify=verify,**kw)
  try:b=r.json()
  except ValueError:b={"success":False,"error":r.text[:500]}
  if r.status_code>=400:b.setdefault("error",f"HTTP {r.status_code}")
  return b

def searchable(item):return " ".join(str(item.get(k) or "") for k in ("editorial_title","editorial_description","title_template","contextual_description","special_activity_show"))
def key(family,item):
 if family=="escapade_proposals":return (item.get("scope_type"),item.get("scope_ref"),item.get("proposal_types"),item.get("start_month"),item.get("end_month"))
 if family=="activity_proposals":return (item.get("scope_type"),item.get("scope_ref"),item.get("occasion_ref"),item.get("action_1"))
 if family=="territories":return (item.get("scope_type"),item.get("scope_ref"))
 return (item.get("string_id"),)

def plan(args):
 token=os.getenv("IZILIFE_AGENT_TOKEN","").strip()
 if not token:raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
 api=Api(token,args.timeout);merged={x:{} for x in UPSERT};excluded=[]
 for env in args.sources:
  response=api.post(env,EXPORT,{"kind":"ALL"})
  if not response.get("success"):raise RuntimeError(f"Export {env}: {response.get('error')}")
  data=response.get("data") or {}
  for family in merged:
   for item in data.get(family) or []:
    if family in {"escapade_proposals","activity_proposals"} and TEST.search(searchable(item)):
     excluded.append({"env":env,"family":family,"source_id":item.get("source_id"),"reason":"mot test"});continue
    if family=="campaigns" and item.get("string_id") not in set(args.campaign or []):continue
    clean={k:v for k,v in item.items() if k!="source_id"};merged[family][key(family,clean)]={"source_env":env,"payload":clean}
 out={"format":"izilife-curation-extras-plan-v1","created_at":datetime.now().isoformat(),"destination_env":args.destination,"sources":args.sources,"families":{f:list(v.values()) for f,v in merged.items()},"excluded":excluded}
 path=Path(args.output).resolve();path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8");print(f"Plan: {path}");print(json.dumps({f:len(v) for f,v in out['families'].items()},ensure_ascii=False));return 0

def apply(args):
 token=os.getenv("IZILIFE_AGENT_TOKEN","").strip()
 if not token:raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
 if args.confirm!="CURATION_EXTRAS_APPLY":raise RuntimeError("Utiliser --confirm CURATION_EXTRAS_APPLY.")
 p=Path(args.plan).resolve();plan=json.loads(p.read_text(encoding="utf-8"));env=plan["destination_env"]
 if env=="prod" and args.confirm_production!="I_CONFIRM_PRODUCTION_EXTRAS":raise RuntimeError("Confirmation production manquante.")
 api=Api(token,args.timeout);journal={"format":"izilife-curation-extras-apply-v1","plan_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"applied_at":datetime.now().isoformat(),"destination_env":env,"items":[]};failed=False
 for family,items in plan.get("families",{}).items():
  for item in items:
   payload=item["payload"]
   if family=="campaigns" and payload.get("scope_level")!="global" and not payload.get("scope_ref"):
    result={"success":False,"error":"Campagne bloquée: scope sans référence stable."}
   else:result=api.post(env,UPSERT[family],payload,form=family!="campaigns")
   ok=bool(result.get("success"));failed|=not ok;journal["items"].append({"family":family,"key":key(family,payload),"source_env":item["source_env"],"status":"APPLIED" if ok else "ERROR","result":result})
 out=Path(args.journal or p.with_name(f"extras-{env}-{datetime.now():%Y%m%d-%H%M%S}.json")).resolve();out.write_text(json.dumps(journal,ensure_ascii=False,indent=2),encoding="utf-8");print(f"Journal: {out}");return 2 if failed else 0

def main():
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="command",required=True)
 p=sub.add_parser("plan");p.add_argument("--sources",nargs="+",choices=ENVS,default=["local","staging"]);p.add_argument("--destination",required=True,choices=ENVS);p.add_argument("--campaign",action="append",default=[]);p.add_argument("--output",required=True);p.add_argument("--timeout",type=int,default=90);p.set_defaults(func=plan)
 a=sub.add_parser("apply");a.add_argument("--plan",required=True);a.add_argument("--confirm",required=True);a.add_argument("--confirm-production");a.add_argument("--journal");a.add_argument("--timeout",type=int,default=90);a.set_defaults(func=apply)
 args=ap.parse_args();return args.func(args)
if __name__=="__main__":raise SystemExit(main())
