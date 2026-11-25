"""Pilote séquentiellement les briques existantes d'enrichissement avec reprise."""
from __future__ import annotations
import argparse,json,subprocess,sys
from datetime import datetime
from pathlib import Path

HERE=Path(__file__).resolve().parent

def command_specs(args,config):
    out=Path(args.report_dir); maxv=str(args.max)
    enabled=set(config.get("enabled_stages") or ["maintenance_content","google_hours","media_curation","intelligent","structured_content"])
    specs=[]
    if "maintenance_content" in enabled:
        specs.append(("maintenance_content",[sys.executable,str(HERE/"enrichisseur.py"),"--zone",args.zone,"--env",args.env,"--city",args.city,"--max",maxv]+([] if args.apply else ["--dry-run"])))
    if "google_hours" in enabled:
        hours_python=str(config.get("google_hours_python") or sys.executable)
        hours=[hours_python,str(HERE/"google_hours_agent.py"),"--env",args.env,"--max",maxv,"--output",str(out/"google_hours.json")]
        if args.config and config.get("intelligent_targets"):
            hours += ["--targets-file",str(args.config)]
        if args.apply:
            hours += ["--apply"]+(["--confirm-production","I_CONFIRM_PRODUCTION_HOURS"] if args.env=="prod" else [])
        specs.append(("google_hours",hours))
    if "media_curation" in enabled:
        specs.append(("media_curation",[sys.executable,str(HERE.parent/"medias"/"media_curator.py"),"--zone",args.zone,"--env",args.env,"--max",maxv]+([] if args.apply else ["--dry-run"])))
    for index,target in enumerate(config.get("intelligent_targets",[]),1):
        if "intelligent" not in enabled: break
        cmd=[sys.executable,str(HERE/"intelligent_enricher.py"),"--env",args.env,"--scope-type",target["scope_type"],"--scope-ref",target["scope_ref"],"--min-confidence",str(target.get("min_confidence",.8)),"--output-dir",str(out/"intelligent")]
        for url in target.get("source_urls",[]):cmd += ["--source-url",url]
        if target.get("with_ai"):cmd.append("--with-ai")
        if target.get("with_web_search"):cmd.append("--with-web-search")
        if args.apply:cmd += ["--apply","--confirm-write"]
        specs.append((f"intelligent_{index}_{target['scope_ref']}",cmd))
    if "structured_content" in enabled:
        specs.append(("structured_content",[sys.executable,str(HERE/"enrichisseur_contenus.py"),"--zone",args.zone,"--env",args.env,"--max",maxv]+([] if args.apply else ["--dry-run"])))
    cover_targets=config.get("cover_targets",[])
    if cover_targets:
        cmd=[sys.executable,str(HERE/"cover_promoter.py"),"--env",args.env]
        for target in cover_targets:cmd += ["--target",f"{target['scope_type']}:{target['scope_ref']}"]
        if args.apply:cmd += ["--apply"]+(["--confirm-production","I_CONFIRM_PRODUCTION_COVERS"] if args.env=="prod" else [])
        specs.append(("promote_existing_covers",cmd))
    return specs

def main():
    p=argparse.ArgumentParser();p.add_argument("--zone",required=True);p.add_argument("--city",required=True);p.add_argument("--env",choices=["local","staging","prod"],default="local");p.add_argument("--config",type=Path);p.add_argument("--report-dir",type=Path,default=HERE/"orchestrator_reports");p.add_argument("--max",type=int,default=20);p.add_argument("--apply",action="store_true");p.add_argument("--confirm-production");p.add_argument("--plan",action="store_true");p.add_argument("--restart",action="store_true");a=p.parse_args()
    if a.apply and a.env=="prod" and a.confirm_production!="I_CONFIRM_PRODUCTION_ENRICHMENT":raise SystemExit("Production refusée sans confirmation explicite.")
    cfg=json.loads(a.config.read_text(encoding="utf-8")) if a.config else {};a.report_dir.mkdir(parents=True,exist_ok=True);checkpoint=a.report_dir/f"checkpoint_{a.env}_{a.zone}.json"
    state={"completed":[],"runs":[]} if a.restart or not checkpoint.exists() else json.loads(checkpoint.read_text(encoding="utf-8"))
    specs=command_specs(a,cfg)
    if a.plan:print(json.dumps([{"stage":n,"command":c} for n,c in specs],ensure_ascii=False,indent=2));return
    for name,cmd in specs:
        if name in state["completed"]:print(f"SKIP {name} (checkpoint)");continue
        print(f"START {name}");proc=subprocess.run(cmd,text=True,capture_output=True)
        record={"stage":name,"at":datetime.now().isoformat(),"returncode":proc.returncode,"stdout":proc.stdout[-5000:],"stderr":proc.stderr[-5000:]};state["runs"].append(record)
        if proc.returncode!=0:
            checkpoint.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
            if cfg.get("continue_on_error"):
                print(f"ERROR {name}: {proc.stderr[-800:]}")
                continue
            raise SystemExit(f"Échec {name}: {proc.stderr[-800:]}")
        state["completed"].append(name);checkpoint.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"success":True,"completed":state["completed"],"checkpoint":str(checkpoint)},ensure_ascii=False))
if __name__=="__main__":main()
