#!/usr/bin/env python3
"""Valide, planifie et ingère un package Event/EventSerie/AnnualCelebration."""
from __future__ import annotations
import argparse,json,os,sys
from collections import Counter
from datetime import date
from pathlib import Path
import requests

SCRIPTS=Path(__file__).resolve().parents[2]
if str(SCRIPTS) not in sys.path:sys.path.insert(0,str(SCRIPTS))
from core.paths import IZILIFE_ENVS
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from objects.object_agent_common import load_env

def read(path):
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict):raise RuntimeError("Objet JSON attendu.")
    return value

def issues(package):
    out=[]
    if package.get("schema_version")!="izi.event.package.v1":out.append("schema_version invalide")
    kind=str(package.get("package_kind") or "").strip().upper()
    if kind not in {"EVENT_GRAPH","EDITORIAL_AGENDA"}:out.append("package_kind doit être EVENT_GRAPH ou EDITORIAL_AGENDA")
    root=package.get("root")
    if root is not None:
        if not isinstance(root,dict) or root.get("type") not in {"EVENT_SERIE","ANNUAL_CELEBRATION"}:out.append("root.type doit être EVENT_SERIE ou ANNUAL_CELEBRATION")
        elif not str((root.get("data") or {}).get("name") or "").strip():out.append("root.data.name requis")
    events=package.get("events")
    if not isinstance(events,list) or not events:out.append("events doit être une liste non vide")
    else:
        refs=[]
        for index,event in enumerate(events,1):
            if not isinstance(event,dict):out.append(f"events[{index}] objet attendu");continue
            data=event.get("data") or {};ref=str(event.get("client_ref") or "").strip();refs.append(ref)
            if not ref:out.append(f"events[{index}].client_ref requis")
            if not str(data.get("title") or "").strip():out.append(f"events[{index}].data.title requis")
            if not str(data.get("description") or "").strip():out.append(f"events[{index}].data.description requis")
            if not str(data.get("event_category_ref") or "").strip():out.append(f"events[{index}].data.event_category_ref requis")
            if not (event.get("existing_ref") or data.get("start_date")):out.append(f"events[{index}].data.start_date requis pour création")
            hourlies=event.get("hourlies") or []
            try:
                start=date.fromisoformat(str(data.get("start_date")))
                end=date.fromisoformat(str(data.get("end_date") or data.get("start_date")))
            except (TypeError, ValueError):
                start=end=None
            if start is not None and end is not None and (end-start).days>=7 and hourlies:
                weekly=[row for row in hourlies if isinstance(row,dict) and row.get("day_id") is not None and not row.get("date")]
                dated=[row for row in hourlies if isinstance(row,dict) and row.get("date")]
                if not weekly:out.append(f"events[{index}].hourlies: un événement long exige une base hebdomadaire day_id")
                for hourly_index,row in enumerate(hourlies,1):
                    if isinstance(row,dict) and row.get("date") and row.get("override") is not True:
                        out.append(f"events[{index}].hourlies[{hourly_index}]: une date sur un événement long doit être marquée override=true")
            for media in event.get("media") or []:
                if not isinstance(media,dict) or not str(media.get("image_url") or "").startswith(("http://","https://")):out.append(f"events[{index}].media image_url invalide")
        if len(refs)!=len(set(refs)):out.append("client_ref dupliqué")
        root_editions=sum(1 for event in events if isinstance(event,dict) and str(event.get("relation") or "").upper()=="ROOT_EDITION")
        if kind=="EVENT_GRAPH" and root is None:out.append("EVENT_GRAPH exige root")
        if kind=="EVENT_GRAPH" and root_editions!=1:out.append("EVENT_GRAPH exige exactement une ROOT_EDITION")
        if kind=="EDITORIAL_AGENDA" and (root is not None or root_editions):out.append("EDITORIAL_AGENDA interdit root et ROOT_EDITION")
    return out

def plan(package,path):
    events=package.get("events") or [];relations=Counter(str(e.get("relation") or "STANDALONE") for e in events if isinstance(e,dict))
    media=sum(len(e.get("media") or []) for e in events if isinstance(e,dict))
    return {"file":str(path),"root_type":(package.get("root") or {}).get("type"),"events":len(events),"relations":dict(relations),"media":media,"organizers":len(package.get("organizers") or []),"sources":sum(len(e.get("sources") or []) for e in events if isinstance(e,dict))}

def apply(package,env,dry_run):
    token=os.getenv("IZILIFE_AGENT_TOKEN","").strip()
    if not token:raise RuntimeError("IZILIFE_AGENT_TOKEN manquant")
    cfg=IZILIFE_ENVS[env];response=requests.post(cfg["base_url"].rstrip("/")+"/scraper/agentIngestEventPackage",data={"payload":json.dumps(package,ensure_ascii=False),"dry_run":"1" if dry_run else "0"},headers={"X-Agent-Token":token},verify=cfg.get("verify_ssl",True),timeout=180)
    try:body=response.json()
    except ValueError as exc:raise RuntimeError(f"Réponse non JSON HTTP {response.status_code}") from exc
    if response.status_code>=400 or not body.get("success"):raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
    print(json.dumps(body,ensure_ascii=False,indent=2))

def main():
    p=argparse.ArgumentParser();p.add_argument("command",choices=["validate","plan","dry-run","apply"]);p.add_argument("--file",type=Path,required=True);p.add_argument("--env",choices=["local","staging","prod"]);p.add_argument("--confirm-write",action="store_true");p.add_argument("--confirm-production");a=p.parse_args();load_env();package=read(a.file);problems=issues(package)
    print(json.dumps({"file":str(a.file),"issues":problems},ensure_ascii=False,indent=2))
    if problems:raise SystemExit(2)
    if a.command=="validate":return
    if a.command=="plan":print(json.dumps(plan(package,a.file),ensure_ascii=False,indent=2));return
    if a.command=="dry-run":
        if not a.env:raise SystemExit("dry-run exige --env")
        apply(package,a.env,True);return
    if not a.env or not a.confirm_write:raise SystemExit("apply exige --env et --confirm-write")
    if a.env=="prod" and a.confirm_production!="I_CONFIRM_PRODUCTION_EVENT_PACKAGE":raise SystemExit("Production refusée sans confirmation dédiée")
    apply(package,a.env,False)
if __name__=="__main__":main()
