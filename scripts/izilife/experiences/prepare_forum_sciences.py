#!/usr/bin/env python3
"""Transforme l'inventaire vérifié du Forum en paquet d'import générique.

L'option --download récupère uniquement les images du site officiel. Elle ne
contacte pas iziLife et ne crée aucun objet en base.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from urllib.request import Request, urlopen

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "forum_sciences_draft.json"
OUTPUT = HERE / "forum_sciences_package.json"
MEDIA_DIR = HERE / "forum_sciences_media"
PLANETARIUM_URL = "https://forumdepartementaldessciences.fr/activites/le-planetarium/"
TARIFF_URL = "https://forumdepartementaldessciences.fr/informations-pratiques/ouverture-et-tarifs/"


def media_entry(url: str, stem: str, role: str = "cover") -> dict:
    extension = Path(urlparse(url).path).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise ValueError(f"Format image non prévu : {url}")
    return {"source_url": url, "local_file": f"forum_sciences_media/{stem}{extension}", "role": role}


def eap(name: str, price: float, conditions: str) -> dict:
    return {"name": name, "price": price, "currency": "EUR",
            "access_type_ref": "experience", "price_model_ref": "ticket-unitaire",
            "conditions_description": conditions}


def build(source: dict) -> dict:
    target = source["target"]
    equipment = source["equipment"]
    media = []
    for index, candidate in enumerate(equipment["media_candidates"]):
        media.append(media_entry(candidate["url"], f"planetarium-{index+1}", candidate["role"]))
    result = {
        "schema_version": "izilife.experience_site.v1",
        "source_url": TARIFF_URL,
        "target": {"scope_type": target["scope_type"], "scope_ref": target["scope_ref"]},
        "equipment": {"name": equipment["name"], "internal_id": equipment["internal_id"],
                      "category_ref": equipment["category_ref"], "capacity": equipment["capacity"],
                      "description": "Dôme de projection du Forum départemental des sciences ; 114 sièges et 4 emplacements PMR.",
                      "media": media},
        "object_on_public_place_ref": "planetarium",
        "venue_eaps": [
            {"name": "Planétarium — adulte", "price": 9,
             "currency": "EUR", "access_type_ref": "equipement", "price_model_ref": "ticket-unitaire",
             "equipment_refs": ["planetarium"], "conditions_description": "Tarif adulte du planétarium."},
            {"name": "Planétarium — 13 à 18 ans", "price": 8,
             "currency": "EUR", "access_type_ref": "equipement", "price_model_ref": "ticket-unitaire",
             "equipment_refs": ["planetarium"], "conditions_description": "Justificatif d'âge requis."},
            {"name": "Planétarium — enfant jusqu'à 12 ans", "price": 4,
             "currency": "EUR", "access_type_ref": "equipement", "price_model_ref": "ticket-unitaire",
             "equipment_refs": ["planetarium"], "conditions_description": "Jusqu'à 12 ans."},
            {"name": "Planétarium — tarif réduit", "price": 8,
             "currency": "EUR", "access_type_ref": "equipement", "price_model_ref": "ticket-unitaire",
             "equipment_refs": ["planetarium"], "conditions_description": "Sur présentation d'un justificatif éligible."},
            {"name": "Forum des Sciences — Pass tribu, 1 activité", "price": 25,
             "currency": "EUR", "access_type_ref": "lieu", "price_model_ref": "ticket-unitaire",
             "conditions_description": "4 personnes ; une activité au choix. À confirmer avant vente."},
            {"name": "Forum des Sciences — Pass tribu, 2 activités", "price": 35,
             "currency": "EUR", "access_type_ref": "lieu", "price_model_ref": "ticket-unitaire",
             "conditions_description": "4 personnes ; deux activités. À confirmer avant vente."},
        ],
        "experiences": [],
        "notes": ["Séances non importées : grille scolaire et vacances avec exceptions non modélisées de façon sûre.",
                  "Billetterie en ligne indiquée indisponible ; EAP inactifs et à confirmer.",
                  "Tarifs scolaires et groupes exclus à la demande de l'utilisateur."],
    }
    for row in source["experiences"]:
        planetarium = row["group"] == "planetarium"
        if planetarium:
            prices = []  # Accès mutualisé : EAP du lieu limités à l'équipement planétarium.
            basic_price = 4
            experience_type = "seance-planetarium"
            principal_activity_category = "astronomie"
        else:
            adult = row["adult_price"]
            child = row["child_price"]
            prices = [eap(row["title"] + " — adulte", adult, "Tarif adulte de l'activité.")]
            prices.append(eap(row["title"] + " — enfant", child,
                              "Enfant jusqu'à 12 ans ; gratuit uniquement si le prix indiqué est 0 €."))
            basic_price = adult
            if row["group"] == "workshop":
                experience_type = "atelier"
            elif row["group"] == "exhibition":
                experience_type = "exposition"
            else:
                experience_type = "jeu-de-piste"
            principal_activity_category = "science"
        item = {
            "title": row["title"], "experience_string_id": row["string_id"],
            "city_ref": target["city"], "place_ref": target["scope_ref"],
            "description": row["description"], "short_description": row["description"],
            "duration": row["duration_minutes"], "duration_measurement_unity_id": 2,
            "minimal_age": row.get("minimum_age"),
            "experience_type_ref": experience_type, "access_type_ref": "acces-payant",
            "principal_activity_category_ref": principal_activity_category,
            "basic_price": basic_price,
            "price_text": ("Accès par les tarifs Planétarium du Forum ; réservation par téléphone conseillée."
                           if planetarium else "Tarifs selon âge et conditions ; réservation par téléphone conseillée."),
            "phone_number": source["phone"], "place_visit": 1,
            "accessible_for_kids": 1,
        }
        if planetarium:
            item["equipment_ref"] = "planetarium"
        result["experiences"].append({
            "source_url": row.get("source_url") or PLANETARIUM_URL,
            "item": item, "eaps": prices,
            "media": [media_entry(row["cover_candidate"], row["string_id"])],
            "sessions": [],
        })
    return result


def download(package: dict) -> None:
    MEDIA_DIR.mkdir(exist_ok=True)
    entries = package["equipment"]["media"] + [m for x in package["experiences"] for m in x["media"]]
    for entry in entries:
        path = HERE / entry["local_file"]
        if path.is_file() and path.stat().st_size:
            resize_for_bo(path)
            print("EXISTS", path.name)
            continue
        url = entry["source_url"]
        if urlparse(url).hostname != "forumdepartementaldessciences.fr":
            raise RuntimeError(f"Hôte image inattendu: {url}")
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=45) as response:
            if not response.headers.get("content-type", "").startswith("image/"):
                raise RuntimeError(f"La source ne renvoie pas une image: {url}")
            body = response.read(12 * 1024 * 1024 + 1)
        if len(body) > 12 * 1024 * 1024:
            raise RuntimeError(f"Image trop lourde: {url}")
        path.write_bytes(body)
        resize_for_bo(path)
        print("SAVED", path.name, len(body))


def resize_for_bo(path: Path) -> None:
    """Réduction fidèle à la limite BO 2000 px ; l'original reste sur le site source."""
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source)
        if image.width <= 2000 and image.height <= 2000 and path.stat().st_size <= 5 * 1024 * 1024:
            return
        image.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
        if path.suffix.lower() in {".jpg", ".jpeg"}:
            image.convert("RGB").save(path, format="JPEG", quality=88, optimize=True)
        else:
            image.save(path, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    package = build(json.loads(SOURCE.read_text(encoding="utf-8")))
    OUTPUT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PREPARED", OUTPUT, "experiences=", len(package["experiences"]))
    if args.download:
        download(package)


if __name__ == "__main__":
    main()
