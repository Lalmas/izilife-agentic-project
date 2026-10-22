#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process
from osm_geometry import enrich

FILE,SHEET="city_subdivisions.xlsx","Subdivisions"
COLUMNS=[("name","scope"),("subdivision_ref","scope"),("city_ref","scope"),("division_type_ref","scope"),("parent_ref","scope"),("internal_code","scope"),("zip_code","access"),("other_zip_codes","access"),("longitude","access"),("latitude","access"),("osm_refs","access"),("geometry_geojson","access"),("is_verified","bpr"),("is_active","bpr"),("status","result"),("notes","result"),("last_result","result")]

def payload(r):
    data={k:r.get(k) for k,_ in COLUMNS if k not in {"status","notes","last_result"} and r.get(k) not in (None,"")}
    try:
        return enrich(data)
    except Exception as exc:
        data.pop("geometry_geojson",None)
        data.pop("geometry_source_provider",None)
        print(f"AVERTISSEMENT: subdivision créée sans géométrie OSM ({exc})")
        return data

def main():
    ap=argparse.ArgumentParser(description="Upsert de quartiers, secteurs ou arrondissements dans une ville iziLife existante.")
    ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"geography"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"name":"Quartier exemple","subdivision_ref":"quartier-exemple-lille","city_ref":"lille","division_type_ref":"quartier","longitude":3.0,"latitude":50.0,"osm_refs":"relation:123456","is_verified":"non","is_active":"oui","status":"skip","notes":"La ville doit déjà exister. La relation OSM est facultative : si elle est absente ou indisponible, la subdivision est créée sans géométrie."}
        create_workbook(path,SHEET,COLUMNS,ex,{"division_type_ref":["quartier","secteur","arrondissement"],"is_verified":["oui","non"],"is_active":["oui","non"],"status":["pending","done","error","skip","unmapped"]});return
    process(path,SHEET,a.env,"/scraper/agentUpsertCitySubdivision",payload,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("city_subdivisions","geography",main)
