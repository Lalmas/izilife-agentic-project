#!/usr/bin/env python3
"""Construit un inventaire sans écriture des commerces et services de centres.

Le script ne contacte aucune API et ne modifie aucune base. Il transforme les
captures HTML/JSON officielles et un export read-only des scopes iziLife en un
JSON normalise, destine au classeur de validation humaine.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any


def clean_html(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value or "", flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.lower().replace("&", " et ").replace("'", " ")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def canonical(value: str, center: str = "") -> str:
    words = slugify(value).split("-")
    ignored = {"centre", "commercial", "cc"}
    if center == "LILLENIUM":
        ignored |= {"lillenium", "lille"}
    elif center == "AUSHOPPING V2":
        ignored |= {"aushopping", "v2", "villeneuve", "ascq", "d"}
    return "-".join(word for word in words if word and word not in ignored)


def parse_lillenium_shops(work_dir: Path) -> list[dict[str, Any]]:
    posts = json.loads((work_dir / "lillenium_posts.json").read_text(encoding="utf-8-sig"))
    tags_path = work_dir / "lillenium_tags.json"
    tag_slugs = {
        int(tag["id"]): str(tag.get("slug") or "")
        for tag in (json.loads(tags_path.read_text(encoding="utf-8-sig")) if tags_path.exists() else [])
    }
    rows: list[dict[str, Any]] = []
    for post in posts:
        url = str(post.get("link") or "")
        if "/boutiques/" not in url:
            continue
        title = clean_html(((post.get("title") or {}).get("rendered") or Path(url.rstrip("/")).name))
        tags = [tag_slugs.get(int(tag_id), str(tag_id)) for tag_id in post.get("tags") or []]
        kind = "RESTAURANT" if any(tag in {"restauration", "gourmandises"} for tag in tags) else "BOUTIQUE"
        rows.append({
            "center": "LILLENIUM",
            "center_scope_type": "PLACE",
            "center_scope_ref": "lillenium",
            "source_kind": kind,
            "name": title,
            "source_slug": str(post.get("slug") or Path(url.rstrip("/")).name),
            "source_url": url,
            "source_categories": tags,
            "inside_center": True,
            "source_status": str(post.get("status") or "publish"),
        })
    return sorted(rows, key=lambda row: (row["source_kind"], row["name"].casefold()))


def parse_aushopping_cards(path: Path, kind: str) -> list[dict[str, Any]]:
    source = path.read_text(encoding="utf-8", errors="replace")
    starts = list(re.finditer(r'<div\s+class="js-filter-card shop-card[^"]*"', source, flags=re.I))
    rows: list[dict[str, Any]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(source)
        block = source[start.start():end]
        fields = {
            key: re.search(rf'{key}="([^"]*)"', block, flags=re.I)
            for key in ("data-filter-name", "data-filter-univers", "data-filter-localisation")
        }
        link = re.search(r'<a href="([^"]+)" class="grid">', block, flags=re.I)
        name = re.search(r'<h2>\s*(.*?)\s*</h2>', block, flags=re.I | re.S)
        if not link or not name or not all(fields.values()):
            continue
        location = fields["data-filter-localisation"].group(1)
        rows.append({
            "center": "AUSHOPPING V2",
            "center_scope_type": "PLACE",
            "center_scope_ref": "aushopping-v2",
            "source_kind": kind,
            "name": clean_html(name.group(1)),
            "source_slug": fields["data-filter-name"].group(1),
            "source_url": "https://v2.aushopping.com" + link.group(1),
            "source_categories": [item for item in fields["data-filter-univers"].group(1).split(",") if item],
            "inside_center": "dans-le-centre" in location.split(","),
            "source_status": "publish",
        })
    return sorted(rows, key=lambda row: (not row["inside_center"], row["name"].casefold()))


def section_text(block: str, marker: str) -> str:
    match = re.search(marker + r"(?P<body>.*)", block, flags=re.I | re.S)
    return clean_html(match.group("body")) if match else ""


def parse_v2_services(path: Path) -> list[dict[str, Any]]:
    source = path.read_text(encoding="utf-8", errors="replace")
    starts = list(re.finditer(r'<li class="services-item js-grid-item">', source, flags=re.I))
    rows: list[dict[str, Any]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(source)
        block = source[start.start():end]
        title_match = re.search(r'<span class="services-item-title">\s*(.*?)\s*</span>', block, flags=re.I | re.S)
        id_match = re.search(r'href="#panel-([^"]+)"', block, flags=re.I)
        if not title_match:
            continue
        title = clean_html(title_match.group(1))
        description = section_text(block, r'<div class="services-item-content">')
        rows.append({
            "center": "AUSHOPPING V2",
            "center_scope_type": "PLACE",
            "center_scope_ref": "aushopping-v2",
            "source_kind": "SERVICE_CC",
            "name": title,
            "source_slug": id_match.group(1) if id_match else slugify(title),
            "source_url": "https://v2.aushopping.com/services#" + (id_match.group(1) if id_match else slugify(title)),
            "description": description[:1000],
            "inside_center": True,
            "source_status": "publish",
        })
    return rows


def parse_lillenium_services(path: Path) -> list[dict[str, Any]]:
    source = path.read_text(encoding="utf-8", errors="replace")
    ignored = {
        "nos services", "famille", "stationnement", "détente", "pratique",
        "explorer", "horaires & infos", "contacts & infos", "suivez-nous",
    }
    matches = list(re.finditer(r'<h2[^>]*>(.*?)</h2>', source, flags=re.I | re.S))
    rows: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        title = clean_html(match.group(1))
        if not title or title.casefold() in ignored:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else min(len(source), match.end() + 2500)
        description = clean_html(source[match.end():end])
        rows.append({
            "center": "LILLENIUM",
            "center_scope_type": "PLACE",
            "center_scope_ref": "lillenium",
            "source_kind": "SERVICE_CC",
            "name": title,
            "source_slug": slugify(title),
            "source_url": "https://www.lillenium-lille.com/nos-services/#" + slugify(title),
            "description": description[:1000],
            "inside_center": True,
            "source_status": "publish",
        })
    return rows


TARGET_CITY_REFS = {
    "LILLENIUM": "lille",
    "AUSHOPPING V2": "villeneuve-d-ascq",
}


def match_commerce(
    row: dict[str, Any],
    scopes: list[dict[str, Any]],
    inspected: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    center = row["center"]
    source_name = slugify(row["name"])
    source_base = canonical(row["name"], center)
    target_city_ref = TARGET_CITY_REFS[center]
    candidates: list[dict[str, Any]] = []
    for scope in scopes:
        if str(scope.get("scope_type")) != "SHOP":
            continue
        prod_name = str(scope.get("name") or "")
        prod_ref = str(scope.get("scope_ref") or "")
        prod_norm = str(scope.get("_normalized_name") or slugify(prod_name))
        prod_base = str(scope.get("_canonical_by_center", {}).get(center) or canonical(prod_name + " " + prod_ref, center))
        score = 0
        reason = ""
        if source_name == prod_norm or source_name == slugify(prod_ref):
            score, reason = 100, "nom/référence exact"
        elif source_base and source_base == canonical(prod_name, center):
            score, reason = 94, "nom exact après retrait du centre"
        elif source_base and (source_base in prod_base or prod_base in source_base) and min(len(source_base), len(prod_base)) >= 4:
            score, reason = 82, "nom contenu après normalisation"
        else:
            source_tokens, prod_tokens = set(source_base.split("-")), set(prod_base.split("-"))
            union = source_tokens | prod_tokens
            similarity = len(source_tokens & prod_tokens) / len(union) if union else 0
            if similarity >= 0.75:
                score, reason = round(similarity * 85), "forte proximité de nom"
        if not score:
            continue
        identity = inspected.get(prod_ref) or {}
        city_ref = str(identity.get("city_ref") or "")
        if city_ref == target_city_ref:
            score += 4
            reason += ", ville cible"
        elif city_ref:
            # Un homonyme situé dans une autre ville ne doit jamais être proposé
            # automatiquement comme commerce du centre.
            score -= 35
            reason += f", autre ville ({city_ref})"
        marker = "lillenium" if center == "LILLENIUM" else "v2"
        if marker in (prod_norm + "-" + slugify(prod_ref)):
            score += 3
            reason += ", centre mentionné"
        candidates.append({
            "score": min(score, 107),
            "reason": reason,
            "type": "SHOP",
            "name": prod_name,
            "string_id": prod_ref,
            "source_id": scope.get("source_id"),
            "city_ref": city_ref,
            "is_active": scope.get("is_active"),
            "listable": scope.get("listable"),
        })
    candidates.sort(key=lambda item: (-item["score"], item["name"].casefold()))
    top = candidates[:3]
    if not top:
        status = "ABSENT_A_CONFIRMER"
    elif top[0]["score"] >= 100 and (len(top) == 1 or top[0]["score"] - top[1]["score"] >= 8):
        status = "EXISTANT_A_RATTACHER"
    elif top[0]["score"] >= 92 and (len(top) == 1 or top[0]["score"] - top[1]["score"] >= 8):
        status = "PROBABLE_A_VALIDER"
    else:
        status = "AMBIGU_A_REVOIR"
    base_refs = {slugify(row["name"]), slugify(row.get("source_slug") or "")}
    if center == "LILLENIUM":
        base_refs |= {f"{ref}-lillenium" for ref in tuple(base_refs) if ref}
        base_refs |= {f"{ref}-lille-lillenium" for ref in tuple(base_refs) if ref and "lillenium" not in ref}
    else:
        base_refs |= {f"{ref}-v2" for ref in tuple(base_refs) if ref}
        base_refs |= {f"{ref}-villeneuve-d-ascq-v2" for ref in tuple(base_refs) if ref and "v2" not in ref}
        base_refs |= {f"{ref}v2" for ref in tuple(base_refs) if ref and "v2" not in ref}
    return {"match_status": status, "candidates": top, "lookup_refs": sorted(ref for ref in base_refs if ref)}


OBJECT_REFS = {
    "nurserie": ("OBJECT_ON_PUBLIC_PLACE", "nurserie"),
    "pret-de-poussette": ("OBJECT_ON_PUBLIC_PLACE", "pret-de-poussette"),
    "doudou-perdu": ("OBJECT_ON_PUBLIC_PLACE", "doudou-perdu"),
    "parking-gratuit": ("OBJECT_ON_PUBLIC_PLACE", "parking-gratuit"),
    "bornes-electriques": ("OBJECT_ON_PUBLIC_PLACE", "borne-electrique"),
    "vehicules-electrique": ("OBJECT_ON_PUBLIC_PLACE", "borne-electrique"),
    "parking-2-roues": ("OBJECT_ON_PUBLIC_PLACE", "parking-2-roues"),
    "bibliotheque-partagee": ("OBJECT_ON_PUBLIC_PLACE", "bibliotheque-partagee"),
    "espace-detente": ("OBJECT_ON_PUBLIC_PLACE", "espace-detente"),
    "aire-de-jeux": ("OBJECT_ON_PUBLIC_PLACE", "aire-de-jeux"),
    "moment-enfants": ("OBJECT_ON_PUBLIC_PLACE", "aire-de-jeux"),
    "vinted-go": ("OBJECT_ON_PUBLIC_PLACE", "vinted-go"),
    "amazon-locker": ("OBJECT_ON_PUBLIC_PLACE", "amazon-locker"),
    "consignes": ("OBJECT_ON_PUBLIC_PLACE", "consigne"),
    "photomaton": ("OBJECT_ON_PUBLIC_PLACE_A_COMPLETER", "photomaton"),
    "wifi-gratuit": ("OBJECT_ON_PUBLIC_PLACE", "wifi"),
    "wifi": ("OBJECT_ON_PUBLIC_PLACE", "wifi"),
    "distributeur-billets": ("OBJECT_ON_PUBLIC_PLACE", "distributeur-de-billet"),
    "distributeur-de-billets": ("OBJECT_ON_PUBLIC_PLACE", "distributeur-de-billet"),
    "recyclage-piles": ("OBJECT_ON_PUBLIC_PLACE", "recyclage-piles"),
    "point-recyclage": ("OBJECT_ON_PUBLIC_PLACE", "recyclage-piles"),
    "batteries-nomades": ("OBJECT_ON_PUBLIC_PLACE", "borne-de-recharge-pour-telephone"),
    "defibrillateurs": ("OBJECT_ON_PUBLIC_PLACE", "defibrilateur"),
    "ascenseurs": ("OBJECT_ON_PUBLIC_PLACE", "ascenseur"),
    "escalators": ("OBJECT_ON_PUBLIC_PLACE", "escalator"),
    "toilettes": ("OBJECT_ON_PUBLIC_PLACE_A_PRECISER", "toilettes-gratuites"),
    "toilettes-pmr": ("OBJECT_ON_PUBLIC_PLACE_A_PRECISER", "toilettes-gratuites"),
    "manege": ("OBJECT_ON_PUBLIC_PLACE", "manege"),
    "change-bebe": ("OBJECT_ON_PUBLIC_PLACE", "change-bebe"),
    "accueil-du-centre-commercial": ("OBJECT_ON_PUBLIC_PLACE", "reception"),
}


def classify_service(row: dict[str, Any]) -> dict[str, Any]:
    ref = OBJECT_REFS.get(slugify(row["source_slug"])) or OBJECT_REFS.get(slugify(row["name"]))
    if ref:
        return {"proposed_object_type": ref[0], "proposed_ref": ref[1], "match_status": "REFERENTIEL_TROUVE"}
    return {"proposed_object_type": "A_CLASSER", "proposed_ref": "", "match_status": "REFERENTIEL_A_CONFIRMER"}


def build(work_dir: Path) -> dict[str, Any]:
    scopes_path = work_dir / "prod-scopes-current.json"
    if not scopes_path.exists():
        scopes_path = work_dir / "prod_scopes_2026-10-30.json"
    scopes = json.loads(scopes_path.read_text(encoding="utf-8-sig"))
    ref_lookup_path = work_dir / "prod_ref_lookup_2026-10-30.json"
    if ref_lookup_path.exists():
        known_refs = {(str(scope.get("scope_type")), str(scope.get("scope_ref"))) for scope in scopes}
        for result in json.loads(ref_lookup_path.read_text(encoding="utf-8-sig")):
            data = result.get("data") or {}
            key = (str(result.get("type") or "SHOP"), str(result.get("string_id") or ""))
            if result.get("status") != "found" or key in known_refs:
                continue
            scopes.append({
                "scope_type": key[0],
                "scope_ref": key[1],
                "name": data.get("name") or key[1],
                "source_id": None,
                "google_place_id": data.get("google_place_id"),
                "city_id": data.get("city_id"),
                "is_active": data.get("is_active"),
                "listable": data.get("listable"),
            })
            known_refs.add(key)
    inspect_path = work_dir / "prod_candidate_inspect_2026-10-30.json"
    inspected = {}
    if inspect_path.exists():
        inspected = {
            str(item.get("scope_ref")): item.get("identity") or {}
            for item in json.loads(inspect_path.read_text(encoding="utf-8-sig"))
            if item.get("success")
        }
    commerces = (
        parse_lillenium_shops(work_dir)
        + parse_aushopping_cards(work_dir / "v2_magasins.html", "BOUTIQUE")
        + parse_aushopping_cards(work_dir / "v2_restaurants.html", "RESTAURANT")
    )
    # La page restaurants reprend parfois une fiche déjà présente dans magasins.
    deduped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in commerces:
        key = (row["center"], slugify(row["name"]), row["source_url"])
        deduped[key] = row
    commerces = list(deduped.values())
    # Les exports de production contiennent plusieurs milliers de scopes. Ces
    # normalisations sont invariantes pour tout l'inventaire et ne doivent pas
    # être recalculées pour chaque enseigne officielle.
    for scope in scopes:
        if str(scope.get("scope_type")) != "SHOP":
            continue
        prod_name = str(scope.get("name") or "")
        prod_ref = str(scope.get("scope_ref") or "")
        scope["_normalized_name"] = slugify(prod_name)
        scope["_canonical_by_center"] = {
            center: canonical(prod_name + " " + prod_ref, center)
            for center in TARGET_CITY_REFS
        }
    for row in commerces:
        row.update(match_commerce(row, scopes, inspected))
        if row["candidates"]:
            identity = inspected.get(str(row["candidates"][0]["string_id"])) or {}
            row["current_in_on_place"] = identity.get("in_on_place")
            if row["center"] == "LILLENIUM" and str(identity.get("in_on_place") or "") == "82":
                row["match_status"] = "DEJA_RATTACHE"
            elif row["center"] == "LILLENIUM" and identity.get("in_on_place") not in (None, "", 0, "0"):
                row["match_status"] = "RATTACHE_A_UN_AUTRE_LIEU"
    services = parse_lillenium_services(work_dir / "lillenium_services.html") + parse_v2_services(work_dir / "v2_services.html")
    for row in services:
        row.update(classify_service(row))
    return {
        "generated_at": date.today().isoformat(),
        "write_performed": False,
        "centers": [
            {"name": "Lillenium", "scope_type": "PLACE", "scope_ref": "lillenium", "model_status": "OK"},
            {"name": "Aushopping V2", "scope_type": "PLACE", "scope_ref": "aushopping-v2", "model_status": "OK"},
        ],
        "commerces": sorted(commerces, key=lambda row: (row["center"], not row["inside_center"], row["name"].casefold())),
        "services": sorted(services, key=lambda row: (row["center"], row["name"].casefold())),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = build(args.work_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "commerces": len(payload["commerces"]),
        "services": len(payload["services"]),
        "output": str(args.output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
