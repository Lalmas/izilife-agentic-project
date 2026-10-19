"""Agent avantages iziLife : une ligne Excel = un Effect Plan dans une BPR de temporalité."""
import argparse
from offer_agent_common import *

FILE="izilife_subscription_benefits.xlsx"; SHEET="Avantages abonnements"
COLUMNS=[("scope_type","scope"),("scope_string_id","scope"),("plan_string_id","bpr"),("plan_temporality_string_id","bpr"),("bpr_title","bpr"),("effect_label","effect"),("benefit_resume","legacy"),
    ("promotion_mechanic_string_id","bpr"),("value_int","bpr"),("currency","bpr"),("x_qty","bpr"),("y_qty","bpr"),("benefit_target","bpr"),("on_izilife_object","bpr"),("application_context","bpr"),("include_brunch","bpr"),
    ("delivery_mode","access"),("external_promotion_code","access"),("available_for","access"),("usable_days","access"),("access_hours","access"),("access_schedule","access"),("blackout_hours","access"),("last_use_time","access"),
    ("opening_hours_required","access"),("allow_if_opening_hours_unknown","access"),("valid_from","bpr"),("valid_to","bpr"),("priority","bpr"),("is_active","bpr"),
    ("status","result"),("last_result","result")]

def short_title(value):
    title=str(value or "").strip()
    if not title or len(title)>50:
        raise ValueError("Le titre court de la mécanique est obligatoire et limité à 50 caractères.")
    return title

def payload(r):
    return {"scope_type":str(r.get("scope_type") or "").lower(),"scope_string_id":r.get("scope_string_id"),"plan_string_id":r.get("plan_string_id"),
        "plan_temporality_string_id":r.get("plan_temporality_string_id"),"bpr_title":r.get("bpr_title") or "Avantages abonnés iziLife","effect_label":short_title(r.get("effect_label") or r.get("benefit_resume")),"promotion_mechanic_string_id":r.get("promotion_mechanic_string_id"),
        "value_int":r.get("value_int") or 0,"currency":r.get("currency") or 1,"x_qty":r.get("x_qty"),"y_qty":r.get("y_qty"),"benefit_target":"product" if r.get("promotion_mechanic_string_id")=="produit-offert" else (r.get("benefit_target") or "all"),
        "on_izilife_object":r.get("on_izilife_object") or "selections","application_context":r.get("application_context") or None,"include_brunch":r.get("include_brunch") or 0,"delivery_mode":r.get("delivery_mode") or "onsite_redemption","external_promotion_code":r.get("external_promotion_code"),
        "usage_constraints":constraints(r),"valid_from":r.get("valid_from"),"valid_to":r.get("valid_to"),"priority":r.get("priority") or 100,"is_active":r.get("is_active") if r.get("is_active") not in (None,"") else 1}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--zone",required=True); ap.add_argument("--env",choices=["local","staging","prod"],default="staging"); ap.add_argument("--init",action="store_true"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--max",type=int,default=100); a=ap.parse_args()
    path=workbook_path(a.env,a.zone,FILE)
    if a.init:
        example={"scope_type":"SHOP","scope_string_id":"soultrain-cafe","plan_string_id":"USER_PASS","plan_temporality_string_id":"anniversaire","bpr_title":"Avantages abonnés iziLife","effect_label":"-10% sur la carte","promotion_mechanic_string_id":"reduction-pourcentage","value_int":10,"currency":1,"benefit_target":"all","on_izilife_object":"selections","delivery_mode":"promo_code","external_promotion_code":"ANNIV10","usable_days":"lun-dim","access_hours":"12h00-14h00 & 18h00-22h00","priority":100,"is_active":1,"status":"skip","last_result":"EXEMPLE — copier la ligne puis mettre pending"}
        create_workbook(path,SHEET,COLUMNS,example,{"scope_type":["GLOBAL","PLACE","SHOP","PARTNER","PAGE","EVENT","EVENT_SERIE","EXPERIENCE"],"plan_temporality_string_id":["offre-permanente","anniversaire","offre-cadeaux-ponctuels","anniversaire-enfant-famille"],"promotion_mechanic_string_id":["reduction-montant","reduction-pourcentage","reduction-montant-facture","reduction-pourcentage-facture","x-achete-y-offert","credit-offert","produit-offert","tels-produits-a"],"application_context":["","special_brunch"],"include_brunch":[0,1],"delivery_mode":["onsite_redemption","promo_code"],"status":["pending","done","error","skip"]}); return
    process(path,SHEET,a.env,"/scraper/agentCreateSubscriptionBenefit",payload,a.dry_run,a.max)
if __name__=="__main__":
    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("izilife_subscription_benefits", "offers", main)
