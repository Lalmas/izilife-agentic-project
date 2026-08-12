from __future__ import annotations
import argparse, json
from object_agent_common import *
OBJECT="outing_ideas"
ROUTE="/scraper/agentUpsertOutingIdeas"
HEADERS=["status","title","string_id","scope_level","scope_string_id","city","city_string_id","description","short_description","priority","source_url","owner_type","notes","last_error","inserted_id"]
def path(zone,env): return object_zone_dir(OBJECT,zone,env)/f"{OBJECT}.xlsx"
def init(zone,env): init_sheet(path(zone,env), HEADERS, [["pending","Titre exemple","titre-exemple","CITY","",zone,zone,"Description","Résumé","10","","izilife","","", ""]])
def run(zone,env,dry_run=False,max_items=50):
    p=path(zone,env); rows=[r for r in read_rows(p) if str(r.get("status") or "pending").lower() in ("pending","todo","relancer")][:max_items]
    for r in rows:
        payload={k:v for k,v in r.items() if not k.startswith("__")}; payload.setdefault("owner_type","izilife"); payload.setdefault("string_id",slugify(payload.get("title")))
        if dry_run: log(json.dumps(payload,ensure_ascii=False,indent=2)); continue
        try:
            resp=izilife_post(ROUTE, {"payload":json.dumps(payload,ensure_ascii=False)}, env)
            if resp.get("success"): update_cell(p,r["__row"],"status","done"); update_cell(p,r["__row"],"inserted_id",resp.get("id"))
            else: raise RuntimeError(resp.get("error") or str(resp))
        except Exception as e: update_cell(p,r["__row"],"status","error"); update_cell(p,r["__row"],"last_error",str(e)[:500]); log(f"❌ {e}")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--zone",required=True); ap.add_argument("--env",default="prod",choices=["local","staging","prod"]); ap.add_argument("--init",action="store_true"); ap.add_argument("--insert",action="store_true"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--max",type=int,default=50)
    a=ap.parse_args(); load_env();
    if a.init: init(a.zone,a.env)
    if a.insert: run(a.zone,a.env,a.dry_run,a.max)
