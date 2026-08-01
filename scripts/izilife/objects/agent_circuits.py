"""Agent Circuits — sources -> curate_circuits.xlsx -> insert direct draft/review."""
from __future__ import annotations
import argparse, json
from object_agent_common import *
OBJECT="circuits"
SRC_HEADERS=["status","source_url","source_type","city","city_string_id","notes","last_error","generated_at"]
CURATE_HEADERS=["status","title","circuit_string_id","description","short_description","source_url","source_name","city_string_id","scope_level","circuit_type_string_id","circuit_theme_string_id","sport_circuit_type_string_id","distance","distance_unity","duration","duration_unity","difficulty","steps_json","last_error","inserted_id"]
SYSTEM="""Tu extrais un circuit/parcours pour Izilife depuis une page. Retourne JSON strict: {"circuits":[...]}.
Champs circuit: title, circuit_string_id, description, short_description, source_url, source_name, city_string_id, scope_level, circuit_type_string_id, circuit_theme_string_id, sport_circuit_type_string_id, distance, distance_unity, duration, duration_unity, difficulty.
steps: [{position,title,description,address,latitude,longitude,object_type,object_string_id,action_hint}].
Si tu ne sais pas, null. Ne jamais inventer."""

def src_path(zone,env): return object_zone_dir(OBJECT,zone,env)/"sources_circuits.xlsx"
def curate_path(zone,env): return object_zone_dir(OBJECT,zone,env)/"curate_circuits.xlsx"

def init(zone,env):
    init_sheet(src_path(zone,env), SRC_HEADERS, [["pending","https://www.decathlon-outdoor.com/...","url",zone,zone,"", "", ""]])
    init_sheet(curate_path(zone,env), CURATE_HEADERS, [])

def append_curate(path, circuit):
    wb=openpyxl.load_workbook(path); ws=wb.active
    vals=[]
    for h in CURATE_HEADERS:
        if h=="status": vals.append("pending")
        elif h=="steps_json": vals.append(json.dumps(circuit.get("steps") or [], ensure_ascii=False))
        else: vals.append(circuit.get(h))
    ws.append(vals); wb.save(path)

def collect(zone,env,dry_run=False,max_items=20):
    sp=src_path(zone,env); cp=curate_path(zone,env)
    rows=[r for r in read_rows(sp) if str(r.get("status") or "pending").lower() in ("pending","todo","relancer")][:max_items]
    for r in rows:
        url=str(r.get("source_url") or "").strip(); log(f"→ {url}")
        try:
            text=fetch_clean_text(url)
            data=call_openai_json(SYSTEM, f"URL:{url}\nVille:{r.get('city_string_id') or zone}\nTexte:{text}")
            circuits=data.get("circuits") or []
            if dry_run:
                log(json.dumps(circuits,ensure_ascii=False,indent=2)[:3000]); continue
            for c in circuits:
                c.setdefault("source_url", url)
                c.setdefault("circuit_string_id", slugify(c.get("circuit_string_id") or c.get("title")))
                append_curate(cp,c)
            update_cell(sp,r["__row"],"status","done"); update_cell(sp,r["__row"],"generated_at",now_iso())
        except Exception as e:
            update_cell(sp,r["__row"],"status","error"); update_cell(sp,r["__row"],"last_error",str(e)[:500]); log(f"  ❌ {e}")

def insert(zone,env,dry_run=False,max_items=20):
    cp=curate_path(zone,env)
    rows=[r for r in read_rows(cp) if str(r.get("status") or "pending").lower() in ("pending","ready","relancer")][:max_items]
    for r in rows:
        payload={k:v for k,v in r.items() if not k.startswith("__")}
        payload["steps"] = json.loads(payload.get("steps_json") or "[]")
        if dry_run:
            log(json.dumps(payload,ensure_ascii=False,indent=2)[:3000]); continue
        resp=izilife_post("/scraper/agentUpsertCircuit", {"payload": json.dumps(payload,ensure_ascii=False)}, env)
        if resp.get("success"):
            update_cell(cp,r["__row"],"status","inserted"); update_cell(cp,r["__row"],"inserted_id",resp.get("id"))
        else:
            update_cell(cp,r["__row"],"status","error"); update_cell(cp,r["__row"],"last_error",str(resp)[:500])

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--zone",required=True); ap.add_argument("--env",default="prod",choices=["local","staging","prod"]); ap.add_argument("--init",action="store_true"); ap.add_argument("--collect",action="store_true"); ap.add_argument("--insert",action="store_true"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--max",type=int,default=20)
    a=ap.parse_args(); load_env()
    if a.init: init(a.zone,a.env)
    if a.collect: collect(a.zone,a.env,a.dry_run,a.max)
    if a.insert: insert(a.zone,a.env,a.dry_run,a.max)
