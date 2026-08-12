"""Agent Brunch : une ligne Excel = un brunch complet pour un PLACE ou un SHOP."""
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offers"))
from offer_agent_common import *

FILE = "brunches.xlsx"
SHEET = "Brunchs"
COLUMNS = [
    ("scope_type","scope"),("scope_string_id","scope"),
    ("configuration_name","offer"),("configuration_description","offer"),
    ("days","offer"),("start_time","offer"),("end_time","offer"),("interval_minutes","offer"),
    ("min_booking_notice_minutes","access"),("max_people_per_slot","access"),("max_people_per_hour","access"),
    ("have_multi_services","access"),("have_slots_in_services","access"),
    ("service_type","bpr"),("price","bpr"),("child_price","bpr"),("price_type","bpr"),
    ("currency_code","bpr"),("included_items","bpr"),("description","bpr"),
    ("reservation_required","bpr"),("is_active","bpr"),
    ("status","result"),("last_result","result"),
]

def payload(r):
    return {
        "scope_type": str(r.get("scope_type") or "").lower(),
        "scope_string_id": r.get("scope_string_id"),
        "configuration_name": r.get("configuration_name") or "Brunch",
        "configuration_description": r.get("configuration_description"),
        "days": expand_days(r.get("days") or "sam-dim"),
        "start_time": normalize_time(r.get("start_time") or "11h00"),
        "end_time": normalize_time(r.get("end_time") or "15h00"),
        "interval_minutes": r.get("interval_minutes") or 30,
        "min_booking_notice_minutes": r.get("min_booking_notice_minutes"),
        "max_people_per_slot": r.get("max_people_per_slot"),
        "max_people_per_hour": r.get("max_people_per_hour"),
        "have_multi_services": as_bool(r.get("have_multi_services")),
        "have_slots_in_services": as_bool(r.get("have_slots_in_services")),
        "service_type": r.get("service_type") or "menu",
        "price": r.get("price"), "child_price": r.get("child_price"),
        "price_type": r.get("price_type") or "per_person",
        "currency_code": r.get("currency_code") or "EUR",
        "included_items": r.get("included_items"), "description": r.get("description"),
        "reservation_required": as_bool(r.get("reservation_required")),
        "is_active": r.get("is_active") if r.get("is_active") not in (None, "") else 1,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--zone",required=True)
    ap.add_argument("--env",choices=["local","staging","prod"],default="staging")
    ap.add_argument("--init",action="store_true")
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--max",type=int,default=100)
    a=ap.parse_args()
    path=drive_workspace_root(a.env)/"izilife"/"brunch"/normalize_zone(a.zone)/FILE
    if a.init:
        example={"scope_type":"SHOP","scope_string_id":"soultrain-cafe","configuration_name":"Brunch du dimanche",
            "configuration_description":"Brunch servi chaque week-end","days":"sam-dim","start_time":"11h00","end_time":"15h00",
            "interval_minutes":30,"min_booking_notice_minutes":120,"max_people_per_slot":20,"service_type":"mixed",
            "price":29.90,"child_price":14.90,"price_type":"per_person","currency_code":"EUR",
            "included_items":"Buffet salé et sucré, boissons chaudes","description":"Produits maison et options végétariennes.",
            "reservation_required":1,"is_active":1,"status":"skip","last_result":"EXEMPLE — copier puis mettre pending"}
        create_workbook(path,SHEET,COLUMNS,example,{"scope_type":["PLACE","SHOP"],"service_type":["menu","buffet","mixed"],
            "price_type":["per_person","per_child","fixed"],"reservation_required":["0","1"],"is_active":["0","1"],
            "status":["pending","done","error","skip"]})
        return
    process(path,SHEET,a.env,"/scraper/agentUpsertBrunch",payload,a.dry_run,a.max)

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("brunch", "brunch", main)
