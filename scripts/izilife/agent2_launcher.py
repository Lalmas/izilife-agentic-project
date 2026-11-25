#!/usr/bin/env python3
"""Lanceur manuel Agent 2 : séquence allowlistée, checkpoints et rapports JSON."""
from __future__ import annotations
import argparse,json,subprocess,sys
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent
if str(ROOT.parent) not in sys.path:sys.path.insert(0,str(ROOT.parent))
from core.paths import drive_workspace_root

def save_checkpoint(path,state):
    temporary=path.with_suffix(path.suffix+".tmp")
    temporary.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
    temporary.replace(path)

def safe_exists(path):
    try:return path.exists()
    except OSError:return False

def stages(args):
    py=sys.executable;common=[]
    zone_key=args.zone if args.zone.endswith("-zone") else f"{args.zone}-zone"
    enrichment_config=getattr(args,"enrichment_config",None) or drive_workspace_root(args.env)/"izilife"/"enrichment"/zone_key/"orchestrator.json"
    if args.task in {"all","curate-places"}:common.append(("curate_places",[py,str(ROOT/"places"/"createur_lieux.py"),"--zone",args.zone,"--env",args.env,"--city",args.city]+([] if args.apply else ["--dry-run"])))
    if args.task in {"all","pages"}:common.append(("pages",[py,str(ROOT/"agent_pages.py"),"--zone",args.zone,"--env",args.env,"--max",str(args.maximum)]+([] if args.apply else ["--dry-run"])))
    if args.task in {"all","event-improver"}:common.append(("event_improver",[py,str(ROOT/"events"/"improve_existing_events.py"),"--zone",args.zone,"--env",args.env,"--max",str(args.maximum)]+([] if args.apply else ["--dry-run"])))
    if args.task in {"all","manual-events"}:common.append(("manual_events",[py,str(ROOT/"events"/"ingest_manual_curate.py"),"--zone",args.zone,"--env",args.env,"--city",args.city]+([] if args.apply else ["--dry-run"])))
    if args.task in {"all","territorial"}:common.append(("territorial",[py,str(ROOT/"events"/"territorial_aggregator.py"),"--config",str(args.territorial_config or ROOT/"events"/"territorial_sources"/f"{args.zone}-zone.json"),"--env",args.env,"--max-links",str(args.maximum),"--output-dir",str(args.report_dir/"territorial")]+(["--send-new-to-scraper","--confirm-write"] if args.apply else ["--no-api-match"])))
    if args.task in {"all","external-content"}:common.append(("external_content",[py,str(ROOT/"offers"/"external_content_agent.py"),"--zone",args.zone,"--env",args.env,"--max",str(args.maximum)]+([] if args.apply else ["--dry-run"])))
    if args.task in {"all","enrichment"}:
        cmd=[py,str(ROOT/"places"/"enrichment_orchestrator.py"),"--zone",args.zone,"--city",args.city,"--env",args.env,"--max",str(args.maximum)]
        if safe_exists(enrichment_config):cmd += ["--config",str(enrichment_config)]
        if getattr(args,"restart",False):cmd += ["--restart"]
        common.append(("enrichment",cmd+(["--apply"] if args.apply else [])))
    if args.task in {"all","transfers"}:common.append(("transfers",[py,str(ROOT/"commercial_centers"/"transfer_pilot.py"),"run","--zone",args.zone,"--env",args.env]+(["--apply"] if args.apply else [])))
    if args.task=="site-package":
        if not args.file:raise SystemExit("site-package exige --file")
        common.append(("site_package",[py,str(ROOT/"site_package.py"),"apply" if args.apply else "plan","--file",str(args.file)]+(["--env",args.env,"--confirm-write"] if args.apply else [])))
    if args.apply and args.env=="prod":
        if args.confirm_production!="I_CONFIRM_PRODUCTION_AGENT2":raise SystemExit("Production refusée sans confirmation globale dédiée.")
        for _,cmd in common:
            if "enrichment_orchestrator.py" in " ".join(cmd):cmd += ["--confirm-production","I_CONFIRM_PRODUCTION_ENRICHMENT"]
            if "transfer_pilot.py" in " ".join(cmd):cmd += ["--confirm-production","I_CONFIRM_PRODUCTION_TRANSFER"]
            if "site_package.py" in " ".join(cmd):cmd += ["--confirm-production","I_CONFIRM_PRODUCTION_EVENT_PACKAGE"]
    return common

def main():
    p=argparse.ArgumentParser();p.add_argument("task",choices=["all","curate-places","pages","event-improver","manual-events","territorial","external-content","enrichment","transfers","site-package"]);p.add_argument("--env",choices=["local","staging","prod"],default="local");p.add_argument("--zone",default="lille");p.add_argument("--city",default="lille");p.add_argument("--file",type=Path);p.add_argument("--territorial-config",type=Path);p.add_argument("--enrichment-config",type=Path);p.add_argument("--max",dest="maximum",type=int,default=20);p.add_argument("--apply",action="store_true");p.add_argument("--confirm-production");p.add_argument("--plan",action="store_true");p.add_argument("--restart",action="store_true");p.add_argument("--report-dir",type=Path,default=ROOT/"launcher_reports");a=p.parse_args();a.report_dir.mkdir(parents=True,exist_ok=True)
    specs=stages(a)
    if a.plan:print(json.dumps([{"stage":name,"command":cmd} for name,cmd in specs],ensure_ascii=False,indent=2));return
    checkpoint=a.report_dir/f"checkpoint_{a.env}_{a.zone}_{a.task}.json";state={"completed":[],"runs":[]} if a.restart or not checkpoint.exists() else json.loads(checkpoint.read_text(encoding="utf-8"))
    for index,(name,cmd) in enumerate(specs,1):
        if name in state["completed"]:print(f"[{index}/{len(specs)}] SKIP {name}");continue
        print(f"[{index}/{len(specs)}] START {name}",flush=True);proc=subprocess.run(cmd,text=True,capture_output=True);state["runs"].append({"stage":name,"at":datetime.now().isoformat(),"returncode":proc.returncode,"stdout":proc.stdout[-10000:],"stderr":proc.stderr[-10000:]})
        save_checkpoint(checkpoint,state)
        if proc.returncode:raise SystemExit(f"Échec {name}; voir {checkpoint}")
        state["completed"].append(name);save_checkpoint(checkpoint,state)
    print(json.dumps({"success":True,"completed":state["completed"],"checkpoint":str(checkpoint)},ensure_ascii=False))
if __name__=="__main__":main()
