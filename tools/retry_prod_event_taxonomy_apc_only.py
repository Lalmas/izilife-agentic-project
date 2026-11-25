from __future__ import annotations
import json, os, sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\alcamara\Documents\agentic_Workspace\tmp\event-quality-one-shot\scripts")
from core.paths import IZILIFE_ENVS
from izilife.events.backfill_active_event_taxonomy import TaxonomyClient

report=Path(r"C:\Users\alcamara\Documents\agentic_Workspace\outputs\prod_event_taxonomy_llm_20261111.json")
data=json.loads(report.read_text(encoding="utf-8"));token=os.environ["IZILIFE_AGENT_TOKEN"]
env=IZILIFE_ENVS["prod"];client=TaxonomyClient(env["base_url"],token,env["verify_ssl"])
results=[]
for row in data.get("results",[]):
    if row.get("status")!="error" or float((row.get("proposal")or{}).get("confidence")or 0)<.90:continue
    proposal=dict(row["proposal"]);proposal.pop("event_category_ref",None)
    try:
        response=client.apply_taxonomy(int(row["event_id"]),proposal,False)
        results.append({"event_id":row["event_id"],"status":"applied_apc_only","updates":response.get("updates")or{}})
    except Exception as exc:results.append({"event_id":row["event_id"],"status":"error","error":str(exc)})
print(json.dumps(results,ensure_ascii=False))
