#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"offers"))
from offer_agent_common import create_workbook,drive_workspace_root,normalize_zone,process
from osm_geometry import enrich

FILE,SHEET="streets.xlsx","Streets"
COLUMNS=[("name","scope"),("street_ref","scope"),("city_ref","scope"),("place_type_ref","scope"),("address","access"),("zip_code","access"),("longitude","access"),("latitude","access"),("osm_refs","access"),("geometry_geojson","access"),("description","offer"),("members","offer"),("place_of_life","bpr"),("is_active","bpr"),("status","result"),("notes","result"),("last_result","result")]

def payload(r):
    return enrich({k:r.get(k) for k,_ in COLUMNS if k not in {"status","notes","last_result"} and r.get(k) not in (None,"")})

def main():
    ap=argparse.ArgumentParser(description="Création idempotente de rues connues et rattachement de commerces/lieux.")
    ap.add_argument("--zone",required=True);ap.add_argument("--env",choices=["local","staging","prod"],default="local");ap.add_argument("--init",action="store_true");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--max",type=int,default=100);a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"geography"/normalize_zone(a.zone)/FILE
    if a.init:
        ex={"name":"Rue exemple","street_ref":"rue-exemple-lille","city_ref":"lille","place_type_ref":"rue","address":"Rue exemple","zip_code":"59000","longitude":3.0,"latitude":50.0,"osm_refs":"way:123456, way:789012","members":"SHOP:soultraincafe, PLACE:lieu-exemple","place_of_life":"oui","is_active":"oui","status":"skip","notes":"Les références OSM sont fusionnées en LINESTRING/MULTILINESTRING. Rattachement additif via in_on_place."}
        create_workbook(path,SHEET,COLUMNS,ex,{"place_of_life":["oui","non"],"is_active":["oui","non"],"status":["pending","done","error","skip","unmapped"]});return
    process(path,SHEET,a.env,"/scraper/agentUpsertStreet",payload,a.dry_run,a.max)

if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]));from agent_excel_logger import run_logged;run_logged("streets","geography",main)
