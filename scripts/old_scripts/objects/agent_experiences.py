"""Agent Expériences — source sheet -> scraping_experience_tmp.
Usage:
  python agent_experiences.py --zone=lille --env=local --init
  python agent_experiences.py --zone=lille --env=local --collect --dry-run
  python agent_experiences.py --zone=lille --env=local --collect --max=5
"""
from __future__ import annotations
import argparse, json, os
from pathlib import Path
from object_agent_common import *

OBJECT = "experiences"
HEADERS = ["status","source_url","source_type","city","city_string_id","notes","last_error","tmp_id","generated_at"]

SYSTEM = """Tu structures des expériences pour Izilife. Retourne uniquement JSON.
Une expérience est une activité structurée : visite, atelier, dégustation, jeu de piste, balade, cours, stage, croisière.
Ignore les simples billets d'entrée sans expérience.
Format: {"experiences":[{...}]}.
Champs: title, experience_string_id, description, short_description, price_text, basic_price, minimal_age, is_for_kids, accessible_for_kids, duration, duration_measurement_unity_string_id, minimal_number_of_people, maximal_number_of_people, experience_type_string_id, experience_theme, experience_theme2, experience_theme3, is_insolite, is_nocturnal, noise_level, with_equipment, equipment_gived, equipment_text, place_visit, brand_text, experience_in_all_city, experience_access_type, experience_booking_needed_for_access, access_link, phone_number, city_string_id, primary_image_url.
Ne jamais inventer. Mets null si absent."""

def sheet_path(zone, env):
    return object_zone_dir(OBJECT, zone, env) / "sources_experiences.xlsx"

def init(zone, env):
    init_sheet(sheet_path(zone, env), HEADERS, [["pending","https://example.com/experience","url",zone,zone,"", "", "", ""]])

def analyze_url(url, city):
    text = fetch_clean_text(url)
    return call_openai_json(SYSTEM, f"URL: {url}\nVille: {city}\nTexte:\n{text}")

def submit(exp, row, env, source_url):
    payload = dict(exp)
    payload.setdefault("source", "agent_experiences")
    payload.setdefault("source_url", source_url)
    payload.setdefault("raw_json", json.dumps(exp, ensure_ascii=False))
    return izilife_post("/scraper/agentSubmitExperienceTmp", {"payload": json.dumps(payload, ensure_ascii=False)}, env)

def collect(zone, env, dry_run=False, max_items=20):
    path = sheet_path(zone, env)
    rows = [r for r in read_rows(path) if str(r.get("status") or "pending").lower() in ("pending","todo","relancer")]
    rows = rows[:max_items]
    for r in rows:
        url = str(r.get("source_url") or "").strip()
        if not url: continue
        log(f"→ {url}")
        try:
            data = analyze_url(url, r.get("city_string_id") or zone)
            exps = data.get("experiences") or []
            if dry_run:
                log(json.dumps(exps[:2], ensure_ascii=False, indent=2)[:3000])
                update_cell(path, r["__row"], "status", "dry_ok")
                continue
            inserted=[]
            for exp in exps:
                resp = submit(exp, r, env, url)
                if resp.get("success"):
                    inserted.append(str(resp.get("id") or resp.get("tmp_id") or "ok"))
                else:
                    raise RuntimeError(resp.get("error") or str(resp))
            update_cell(path, r["__row"], "status", "done")
            update_cell(path, r["__row"], "tmp_id", ",".join(inserted))
            update_cell(path, r["__row"], "generated_at", now_iso())
        except Exception as e:
            log(f"  ❌ {e}")
            update_cell(path, r["__row"], "status", "error")
            update_cell(path, r["__row"], "last_error", str(e)[:500])

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--zone", required=True)
    ap.add_argument("--env", default="prod", choices=["local","staging","prod"])
    ap.add_argument("--init", action="store_true")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max", type=int, default=20)
    args=ap.parse_args(); load_env()
    if args.init: init(args.zone,args.env)
    if args.collect: collect(args.zone,args.env,args.dry_run,args.max)
