#!/usr/bin/env python3
"""Paquet global Place/Equipment sourcé, sans dépendance Google Business."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from objects.object_agent_common import izilife_post,load_env,normalize_env

VERSION="izilife.location_package.v1"
KINDS={"EQUIPMENT_CATEGORY","PLACE","EQUIPMENT"}

def _url(value):
    parsed=urlparse(str(value or ""));return parsed.scheme in {"http","https"} and bool(parsed.netloc)

def issues(package):
    out=[]
    if package.get("schema_version")!=VERSION:out.append("schema_version incorrect")
    objects=package.get("objects")
    if not isinstance(objects,list):return out+["objects doit être une liste"]
    seen=set()
    for index,obj in enumerate(objects,1):
        prefix=f"objects[{index}]"
        if not isinstance(obj,dict) or obj.get("kind") not in KINDS:out.append(f"{prefix}: kind invalide");continue
        if obj.get("review_status") not in {"approved","needs_review","excluded"}:out.append(f"{prefix}: review_status invalide")
        if not _url(obj.get("source_url")):out.append(f"{prefix}: source_url officielle requise")
        key=(obj.get("kind"),obj.get("string_id") or obj.get("internal_id"))
        if key in seen:out.append(f"{prefix}: référence dupliquée")
        seen.add(key)
        if obj.get("kind")=="EQUIPMENT_CATEGORY" and not obj.get("string_id"):out.append(f"{prefix}: string_id requis")
        if obj.get("kind")=="PLACE" and not all(obj.get(x) not in (None,"") for x in ("string_id","name","place_type_ref","city_ref","address","latitude","longitude")):out.append(f"{prefix}: identité/type/adresse/coordonnées Place requises")
        if obj.get("kind")=="EQUIPMENT" and not all(obj.get(x) not in (None,"") for x in ("scope_type","scope_ref","category_ref","internal_id","name","city_ref","latitude","longitude")):out.append(f"{prefix}: scope/catégorie/identité/coordonnées Equipment requis")
        if obj.get("kind") in {"PLACE","EQUIPMENT"} and obj.get("review_status")=="approved" and obj.get("coordinate_status")!="verified":out.append(f"{prefix}: coordonnées non vérifiées")
        if obj.get("coordinate_conflict") and obj.get("review_status")=="approved":out.append(f"{prefix}: conflit de coordonnées encore ouvert")
        media=obj.get("media") or {}
        if media and (not _url(media.get("image_url")) or not _url(media.get("source_url"))):out.append(f"{prefix}: média officiel invalide")
    return out

def approved_package(package):
    return {**package,"objects":[{k:v for k,v in obj.items() if k not in {"media","review_status","coordinate_status","coordinate_evidence","coordinate_conflict"}}
        for obj in package["objects"] if obj.get("review_status")=="approved"]}

def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="command",required=True)
    for name in ("validate","plan","apply"):
        p=sub.add_parser(name);p.add_argument("--file",required=True)
        if name in {"plan","apply"}:p.add_argument("--env",choices=["local","staging","prod"],default="local")
        if name=="apply":p.add_argument("--confirm-write",action="store_true")
    args=ap.parse_args();path=Path(args.file);package=json.loads(path.read_text(encoding="utf-8"));problems=issues(package)
    if problems:print(json.dumps({"issues":problems},ensure_ascii=False,indent=2));raise SystemExit(1)
    approved=approved_package(package)
    if args.command=="validate":print(json.dumps({"objects":len(package["objects"]),"approved":len(approved["objects"]),"issues":[]},ensure_ascii=False));return
    load_env();env=normalize_env(args.env)
    if args.command=="apply" and not args.confirm_write:raise SystemExit("Écriture désactivée: préciser --confirm-write")
    result=izilife_post("/scraper/agentApplyLocationPackage",{"payload":json.dumps(approved,ensure_ascii=False),"dry_run":"1" if args.command=="plan" else "0"},env,timeout=180)
    if not result.get("success"):raise SystemExit(result.get("error",str(result)))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.command=="apply":
        by_ref={(o.get("kind"),o.get("string_id") or o.get("internal_id")):o for o in package["objects"]}
        for row in result.get("results",[]):
            obj=by_ref.get((row.get("kind"),row.get("string_id") or row.get("internal_id")))
            media=(obj or {}).get("media") or {}
            if media:
                target_id=row.get("id") or row.get("equipment_id")
                if not target_id:raise SystemExit(f"Image: identifiant cible absent dans {row}")
                cover=izilife_post("/scraper/agentAddRemoteCover",{"payload":json.dumps({"scope_type":row["kind"],"target_id":target_id,"image_url":media["image_url"],"title":obj.get("name")},ensure_ascii=False)},env,timeout=180)
                if not cover.get("success"):raise SystemExit(f"Image: {cover.get('error',cover)}")

if __name__=="__main__":main()
