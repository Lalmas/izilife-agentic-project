#!/usr/bin/env python3
"""Chasse immédiate et exhaustive d'une catégorie dans une ville."""
import argparse
from playwright.sync_api import sync_playwright
import chasseur_lieux as base


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zone", required=True)
    parser.add_argument("--city", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--label")
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="prod")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    base.set_current_env(args.env)
    env = base.ENVS[args.env]
    vfile = base.get_villes_file(args.zone)
    if not vfile.exists():
        raise RuntimeError(f"Fichier introuvable : {vfile}")
    city_id = base.resolve_city_id(args.city, env) if not args.dry_run else 0
    query = f"{args.category} à {args.city}"
    base.log(f"Chasse manuelle exhaustive : {query}")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page(locale="fr-FR")
        base.apply_stealth(page)
        found = base.search_google_maps(page, query, max_results=10000) or []
        browser.close()
    created = skipped = errors = 0
    for place in found:
        check = base.izilife_post("/scraper/agentCheckPlace", {"name": place["nom"], "city_id": city_id}, env)
        if check and check.get("exists"):
            skipped += 1
            continue
        if args.dry_run:
            base.log(f"[DRY RUN] {place['nom']}")
            continue
        response = base.izilife_post(f"/scraper/agentFetchAndStoreOnePlace/{args.city}", {"city": args.city, "query": place["nom"]}, env)
        if response and response.get("success"):
            created += 1
            base.log(f"Créé : {place['nom']}")
        elif response and "déjà existant" in str(response.get("error", "")).lower():
            skipped += 1
        else:
            errors += 1
            base.log(f"Erreur : {place['nom']} — {response}")
    if not args.dry_run and errors == 0:
        base.mark_category_traitee(vfile, args.city, args.category, args.label or args.category, "manuel", len(found), created)
    base.log(f"Résultats : {len(found)} | créés : {created} | déjà présents : {skipped} | erreurs : {errors}")


if __name__ == "__main__":
    main()
