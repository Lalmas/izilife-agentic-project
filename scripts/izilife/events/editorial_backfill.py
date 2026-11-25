"""Qualification éditoriale incrémentale des Experiences et Events actifs."""
from __future__ import annotations

import argparse, hashlib, html, json, os, re, sys
from pathlib import Path
from typing import Any
import requests

CORE_ROOT=Path(__file__).resolve().parents[2]
if str(CORE_ROOT) not in sys.path: sys.path.append(str(CORE_ROOT))
IZILIFE_ROOT=Path(__file__).resolve().parents[1]
if str(IZILIFE_ROOT) not in sys.path: sys.path.append(str(IZILIFE_ROOT))
from core.paths import IZILIFE_ENVS, normalize_env
from objects.object_agent_common import load_env

STATE = Path(__file__).resolve().parents[3] / "state" / "editorial_backfill.json"

def api(env: str, path: str, payload: dict[str, Any], timeout: int = 180) -> dict[str, Any]:
    cfg=IZILIFE_ENVS[env]; token=os.getenv("IZILIFE_AGENT_TOKEN","").strip()
    if not token: raise RuntimeError("IZILIFE_AGENT_TOKEN manquant")
    r=requests.post(cfg["base_url"].rstrip("/")+path,json=payload,headers={"X-Agent-Token":token},verify=cfg.get("verify_ssl",True),timeout=timeout)
    data=r.json()
    if not r.ok or not data.get("success"): raise RuntimeError(data.get("error",f"HTTP {r.status_code}"))
    return data

def source_text(url: str) -> str:
    if not url or not re.match(r"^https?://",url,re.I): return ""
    try:
        r=requests.get(url,headers={"User-Agent":"Mozilla/5.0 iziLife Editorial Agent/1.0"},timeout=35);r.raise_for_status()
        text=re.sub(r"<(script|style)[^>]*>.*?</\1>"," ",r.text,flags=re.I|re.S)
        return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",text))).strip()[:24000]
    except requests.RequestException: return ""

def load_state() -> dict[str, Any]:
    if not STATE.exists():
        return {kind: {"after_id": 0, "hashes": {}} for kind in (
            "EXPERIENCE", "EVENT", "EVENT_SERIE", "ANNUAL_CELEBRATION", "REPRESENTATION"
        )}
    return json.loads(STATE.read_text(encoding="utf-8"))

def save_state(state: dict[str, Any]) -> None:
    STATE.parent.mkdir(parents=True,exist_ok=True);STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")

def run(env: str, kind: str, maximum: int, dry_run: bool) -> None:
    state=load_state(); section=state.setdefault(kind,{"after_id":0,"hashes":{}}); processed=0
    initial_after_id = int(section.get("after_id", 0) or 0)
    while processed<maximum:
        result=api(env,"/scraper/agentEditorialBackfillCandidates",{"type":kind,"after_id":section.get("after_id",0),"limit":min(50,maximum-processed)})
        rows=result.get("objects",[])
        if not rows:
            if kind in {"EXPERIENCE", "EVENT_SERIE", "ANNUAL_CELEBRATION", "REPRESENTATION"}: section["after_id"]=0
            break
        for obj in rows:
            oid=int(obj["id"]); raw=json.dumps(obj,ensure_ascii=False,sort_keys=True); digest=hashlib.sha256(raw.encode()).hexdigest()
            if not dry_run:
                section["after_id"]=oid
            if section.setdefault("hashes",{}).get(str(oid))==digest: continue
            text=source_text(str(obj.get("source_url") or ""))
            proposal=api(env,"/scraper/agentAnalyzeEditorialObject",{"type":kind,"id":oid,"source_text":text}).get("proposal",{})
            if not dry_run:
                api(env,"/scraper/agentApplyEditorialObject",{"type":kind,"id":oid,"proposal":proposal})
                section["hashes"][str(oid)]=digest
                save_state(state)
            processed+=1
            print(json.dumps({"type":kind,"id":oid,"dry_run":dry_run,"proposal":proposal},ensure_ascii=False))
            if processed>=maximum: break
    if dry_run:
        section["after_id"] = initial_after_id
    else:
        save_state(state)
    print(json.dumps({"type":kind,"processed":processed,"next_after_id":section.get("after_id",0)},ensure_ascii=False))

def main() -> None:
    p=argparse.ArgumentParser();p.add_argument("--env",default="local",choices=["local","staging","prod"]);p.add_argument("--type",required=True,choices=["EVENT","EXPERIENCE","EVENT_SERIE","ANNUAL_CELEBRATION","REPRESENTATION"]);p.add_argument("--max",type=int,default=50);p.add_argument("--dry-run",action="store_true")
    a=p.parse_args();load_env();run(normalize_env(a.env),a.type,max(1,a.max),a.dry_run)

if __name__=="__main__":main()
