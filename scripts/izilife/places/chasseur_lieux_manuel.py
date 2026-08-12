#!/usr/bin/env python3
"""Chasse immédiate et exhaustive de catégories dans plusieurs villes."""
import argparse

from playwright.sync_api import sync_playwright

import chasseur_lieux as base


def parse_list(value):
    """Accepte une valeur unique ou une liste séparée par des virgules."""
    return [item.strip() for item in value.split(",") if item.strip()]


def hunt(playwright, city, category, label, args, env, vfile):
    city_id = base.resolve_city_id(city, env) if not args.dry_run else 0
    query = f"{category} à {city}"
    base.log(f"Chasse manuelle exhaustive : {query}")

    browser = playwright.chromium.launch(headless=False)
    try:
        page = browser.new_page(locale="fr-FR")
        base.apply_stealth(page)
        found = base.search_google_maps(page, query, max_results=10000) or []
    finally:
        browser.close()

    created = skipped = errors = 0
    for place in found:
        check = base.izilife_post(
            "/scraper/agentCheckPlace",
            {"name": place["nom"], "city_id": city_id},
            env,
        )
        if check and check.get("exists"):
            skipped += 1
            continue
        if args.dry_run:
            base.log(f"[DRY RUN] {place['nom']}")
            continue

        response = base.izilife_post(
            f"/scraper/agentFetchAndStoreOnePlace/{city}",
            {"city": city, "query": place["nom"]},
            env,
        )
        if response and response.get("success"):
            created += 1
            base.log(f"Créé : {place['nom']}")
        elif response and "déjà existant" in str(response.get("error", "")).lower():
            skipped += 1
        else:
            errors += 1
            base.log(f"Erreur : {place['nom']} — {response}")

    if not args.dry_run and errors == 0:
        base.mark_category_traitee(
            vfile, city, category, label, "manuel", len(found), created
        )

    base.log(
        f"Résultats {city} / {category} : {len(found)} | créés : {created} | "
        f"déjà présents : {skipped} | erreurs : {errors}"
    )
    return len(found), created, skipped, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zone", required=True)
    parser.add_argument("--city", required=True, help="Une ou plusieurs villes séparées par des virgules")
    parser.add_argument("--category", required=True, help="Une ou plusieurs catégories séparées par des virgules")
    parser.add_argument("--label", help="Libellé facultatif, avec une seule catégorie uniquement")
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="prod")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cities = parse_list(args.city)
    categories = parse_list(args.category)
    if not cities or not categories:
        parser.error("--city et --category doivent contenir au moins une valeur")
    if args.label and len(categories) != 1:
        parser.error("--label ne peut être utilisé qu'avec une seule catégorie")

    base.set_current_env(args.env)
    env = base.ENVS[args.env]
    vfile = base.get_villes_file(args.zone)
    if not vfile.exists():
        raise RuntimeError(f"Fichier introuvable : {vfile}")

    totals = [0, 0, 0, 0]
    with sync_playwright() as playwright:
        for city in cities:
            for category in categories:
                result = hunt(
                    playwright, city, category, args.label or category, args, env, vfile
                )
                totals = [a + b for a, b in zip(totals, result)]

    base.log(
        f"TOTAL {len(cities)} ville(s) × {len(categories)} catégorie(s) : "
        f"{totals[0]} trouvés | {totals[1]} créés | "
        f"{totals[2]} déjà présents | {totals[3]} erreurs"
    )


if __name__ == "__main__":
    main()
