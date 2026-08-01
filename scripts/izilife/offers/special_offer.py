"""Agent Offer spéciale : une ligne Excel = Offer + horaires/code + sa BPR."""
import argparse
from offer_agent_common import *

FILE="special_offers.xlsx"; SHEET="Offres"
COLUMNS=[
    ("scope_type","scope"),("scope_string_id","scope"),
    ("special_campain_string_id","offer"),("title","offer"),("deal","offer"),("note","offer"),
    ("promotion_mechanic_string_id","offer"),("offer_hours","offer"),("start_date","offer"),("end_date","offer"),("priority","offer"),("is_active","offer"),
    ("offer_access_code","access"),("code_start_date","access"),("code_end_date","access"),("max_total_uses","access"),("max_uses_per_user","access"),
    ("bpr_benefit_resume","bpr"),("bpr_promotion_mechanic_string_id","bpr"),("bpr_value_int","bpr"),("bpr_currency","bpr"),("bpr_x_qty","bpr"),("bpr_y_qty","bpr"),
    ("bpr_benefit_target","bpr"),("bpr_on_izilife_object","bpr"),("bpr_delivery_mode","bpr"),("bpr_external_promotion_code","bpr"),
    ("bpr_usable_days","bpr"),("bpr_access_hours","bpr"),("bpr_blackout_hours","bpr"),("bpr_last_use_time","bpr"),
    ("bpr_opening_hours_required","bpr"),("bpr_allow_if_opening_hours_unknown","bpr"),("bpr_valid_from","bpr"),("bpr_valid_to","bpr"),("bpr_priority","bpr"),("bpr_is_active","bpr"),
    ("status","result"),("last_result","result")]

def payload(r):
    benefit={"benefit_resume":r.get("bpr_benefit_resume"),"promotion_mechanic_string_id":r.get("bpr_promotion_mechanic_string_id"),"value_int":r.get("bpr_value_int") or 0,
        "currency":r.get("bpr_currency") or 1,"x_qty":r.get("bpr_x_qty"),"y_qty":r.get("bpr_y_qty"),"benefit_target":"product" if r.get("bpr_promotion_mechanic_string_id")=="produit-offert" else (r.get("bpr_benefit_target") or "all"),
        "on_izilife_object":r.get("bpr_on_izilife_object") or "selections","delivery_mode":r.get("bpr_delivery_mode") or "onsite_redemption",
        "external_promotion_code":r.get("bpr_external_promotion_code") or r.get("offer_access_code"),"usage_constraints":constraints(r,"bpr_"),
        "valid_from":r.get("bpr_valid_from"),"valid_to":r.get("bpr_valid_to"),"priority":r.get("bpr_priority") or 100,"is_active":r.get("bpr_is_active") if r.get("bpr_is_active") not in (None,"") else 1}
    return {"scope_type":str(r.get("scope_type") or "").lower(),"scope_string_id":r.get("scope_string_id"),"special_campain_string_id":r.get("special_campain_string_id"),
        "title":r.get("title"),"deal":r.get("deal"),"note":r.get("note"),"promotion_mechanic_string_id":r.get("promotion_mechanic_string_id"),
        "times":parse_schedules(r.get("offer_hours") or ""),"start_date":r.get("start_date"),"end_date":r.get("end_date"),"priority":r.get("priority") or 0,
        "is_active":r.get("is_active") if r.get("is_active") not in (None,"") else 1,"offer_access_code":r.get("offer_access_code"),"code_start_date":r.get("code_start_date"),
        "code_end_date":r.get("code_end_date"),"max_total_uses":r.get("max_total_uses"),"max_uses_per_user":r.get("max_uses_per_user"),"benefit_policy_rule":benefit}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--zone",required=True); ap.add_argument("--env",choices=["local","staging","prod"],default="staging"); ap.add_argument("--init",action="store_true"); ap.add_argument("--dry-run",action="store_true"); ap.add_argument("--max",type=int,default=100); a=ap.parse_args()
    path=workbook_path(a.env,a.zone,FILE)
    if a.init:
        example={"scope_type":"SHOP","scope_string_id":"soultrain-cafe","special_campain_string_id":"happy-hour","title":"Happy Hour","deal":"-20% sur une sélection","note":"Sur présentation de l'app iziLife","promotion_mechanic_string_id":"reduction-pourcentage","offer_hours":"lun-mer: 17h00-20h00 & jeu-ven: 18h00-22h00 & sam-dim: 16h00-23h00","priority":10,"is_active":1,"bpr_benefit_resume":"-20% sur une sélection","bpr_promotion_mechanic_string_id":"reduction-pourcentage","bpr_value_int":20,"bpr_currency":1,"bpr_benefit_target":"all","bpr_on_izilife_object":"selections","bpr_delivery_mode":"onsite_redemption","bpr_priority":100,"bpr_is_active":1,"status":"skip","last_result":"EXEMPLE — copier la ligne puis mettre pending"}
        create_workbook(path,SHEET,COLUMNS,example,{"scope_type":["PLACE","SHOP","PARTNER","EVENT","EVENT_SERIE","EXPERIENCE"],"special_campain_string_id":["happy-hour","promo-etudiante","promo-senior","promo-enfant","promo-ado"],"promotion_mechanic_string_id":["reduction-montant","reduction-pourcentage","x-achete-y-offert","credit-offert","produit-offert","tous-les-produits-a","tels-produits-a"],"bpr_promotion_mechanic_string_id":["reduction-montant","reduction-pourcentage","x-achete-y-offert","credit-offert","produit-offert","tous-les-produits-a","tels-produits-a"],"bpr_delivery_mode":["onsite_redemption","promo_code"],"status":["pending","done","error","skip"]}); return
    process(path,SHEET,a.env,"/scraper/agentCreateSpecialOffer",payload,a.dry_run,a.max)
if __name__=="__main__": main()
