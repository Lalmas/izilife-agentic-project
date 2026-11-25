#!/usr/bin/env python3
"""Copie les médias d'une campagne entre environnements sans réutiliser les IDs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

import requests

ENVS = {
    "local": ("https://localhost:4443/izilife-admin", False),
    "staging": ("https://www.staging.izilife.co/izilife-admin", True),
    "prod": ("https://www.izilife.co/izilife-admin", True),
}


def manifest(env: str, ref: str, token: str) -> list[dict]:
    base, verify = ENVS[env]
    r = requests.post(base + "/scraper/agentCampaignMediaManifest", json={"scope_ref": ref}, headers={"X-Agent-Token": token}, timeout=120, verify=verify)
    body = r.json()
    if r.status_code >= 400 or not body.get("success"): raise RuntimeError(body.get("error") or f"HTTP {r.status_code}")
    return body.get("items") or []


def download(env: str, ref: str, media_id: int, token: str) -> tuple[bytes, str, str]:
    base, verify = ENVS[env]
    r = requests.post(base + "/scraper/agentCurationSyncMediaDownload", json={"scope_type":"CAMPAIGN","scope_ref":ref,"source_media_id":media_id}, headers={"X-Agent-Token":token}, timeout=180, verify=verify)
    if r.status_code >= 400: raise RuntimeError(r.text[:500] or f"HTTP {r.status_code}")
    return r.content, r.headers.get("Content-Type","application/octet-stream"), requests.utils.unquote(r.headers.get("X-Original-Name",f"campaign-{media_id}"))


def upload(env: str, ref: str, item: dict, content: bytes, mime: str, filename: str, token: str) -> dict:
    base, verify = ENVS[env]
    r = requests.post(base + "/scraper/agentAddScopedMedia", data={"scope_type":"CAMPAIGN","scope_ref":ref,"belongs_to_scope":"oui","rights_confirmed":"oui","is_principal":"oui" if int(item.get("is_principal") or 0) else "non","title":item.get("title") or "","description":item.get("description") or ""}, files={"media":(filename,content,mime)}, headers={"X-Agent-Token":token,"Accept":"application/json"}, timeout=240, verify=verify)
    body = r.json()
    if r.status_code >= 400 or not body.get("success"): raise RuntimeError(body.get("error") or f"HTTP {r.status_code}")
    return body


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--source-env",choices=ENVS,default="staging");p.add_argument("--destination-env",choices=ENVS,default="prod");p.add_argument("--ref",default="musees-gratuits-les-1er-dimanches-du-mois");p.add_argument("--apply",action="store_true");p.add_argument("--confirm-production");p.add_argument("--journal");a=p.parse_args()
    if a.apply and a.destination_env=="prod" and a.confirm_production!="I_CONFIRM_PRODUCTION_CAMPAIGN_MEDIA": raise RuntimeError("Confirmation production manquante.")
    token=os.getenv("IZILIFE_AGENT_TOKEN","").strip()
    if not token: raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    source=manifest(a.source_env,a.ref,token); destination=manifest(a.destination_env,a.ref,token); hashes={str(x.get("sha1_hash") or "").lower() for x in destination if x.get("sha1_hash")}; operations=[]
    for item in source:
        if item.get("sha1_hash") and str(item["sha1_hash"]).lower() in hashes: operations.append({"source_id":item["source_id"],"status":"SKIP_DUPLICATE"});continue
        if not a.apply: operations.append({"source_id":item["source_id"],"status":"WOULD_COPY"});continue
        content,mime,filename=download(a.source_env,a.ref,int(item["source_id"]),token); actual=hashlib.sha1(content).hexdigest(); expected=str(item.get("sha1_hash") or "").lower()
        if expected and expected!=actual: raise RuntimeError(f"SHA-1 source différent pour media {item['source_id']}")
        result=upload(a.destination_env,a.ref,item,content,mime,filename,token); operations.append({"source_id":item["source_id"],"status":"COPIED" if result.get("created") else "SKIP_DUPLICATE","destination_media_id":result.get("media_id"),"sha1":actual})
    report={"created_at":datetime.now().isoformat(),"source_env":a.source_env,"destination_env":a.destination_env,"campaign_ref":a.ref,"source_count":len(source),"destination_before_count":len(destination),"operations":operations}
    out=Path(a.journal or f"journal-campaign-media-{a.destination_env}-{datetime.now():%Y%m%d-%H%M%S}.json").resolve();out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8");print(f"Journal : {out}");print(json.dumps(report,ensure_ascii=False));return 0


if __name__=="__main__": raise SystemExit(main())
