#!/usr/bin/env python3
"""Propose un enrichissement sourcé d'une fiche iziLife, sans écriture par défaut.

Ordre des sources : fiche iziLife, URLs officielles fournies, puis recherche web
OpenAI uniquement avec --with-web-search. La sortie est validée contre le
référentiel tags/references.json et peut alimenter tags_and_characts.xlsx.
L'application est explicite (--apply --confirm-write) et réutilise la route
déterministe AgentTagsAndCharacts du BO.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import requests
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

BASE_URLS = {
    "local": ("https://localhost:4443/izilife-admin", False),
    "staging": ("https://www.staging.izilife.co/izilife-admin", True),
    "prod": ("https://www.izilife.co/izilife-admin", True),
}
SCRIPT_ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = Path(__file__).resolve().parents[2]
if str(CORE_ROOT) not in sys.path: sys.path.insert(0, str(CORE_ROOT))
from core.place_resolution import PlaceIdentity
REFERENCES = SCRIPT_ROOT / "tags" / "references.json"
EDITORIAL_COLUMNS = ["Atmosphere", "MealType", "BarType", "MusicStyle", "DietType",
                     "DishOrigin", "KnowedMeal", "KnowedDrink", "Dance", "VisitMoment",
                     "VisitWeather", "PaiementMethod", "OrderMethod", "Sport", "Hobby",
                     "ObjectOnPublicPlace", "Occasion", "Animal", "AccessType", "AgeCategory"]


def normalized_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char)).casefold()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def canonical_source_url(value: str) -> str:
    return re.sub(r"[?#].*$", "", str(value or "").strip()).rstrip("/").casefold()


class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self._title = False
        self._ignored = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() in {"script", "style", "noscript", "svg"}:
            self._ignored += 1
        if tag.casefold() == "title":
            self._title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in {"script", "style", "noscript", "svg"} and self._ignored:
            self._ignored -= 1
        if tag.casefold() == "title":
            self._title = False

    def handle_data(self, data: str) -> None:
        if self._ignored:
            return
        if data.strip():
            self.parts.append(data)
            if self._title:
                self.title_parts.append(data)


def agent_token() -> str:
    token = (os.getenv("IZILIFE_AGENT_TOKEN") or os.getenv("AGENT_SECRET_TOKEN") or "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN ou AGENT_SECRET_TOKEN absent.")
    return token


def api_lookup(env: str, scope_type: str, scope_ref: str) -> dict[str, Any]:
    base_url, verify = BASE_URLS[env]
    response = requests.post(
        base_url + "/scraper/agentInternalDataV0Lookup",
        json={"items": [{"type": scope_type, "string_id": scope_ref}],
              "view": "full", "media_page_size": 10},
        headers={"X-Agent-Token": agent_token()}, verify=verify, timeout=120,
    )
    response.raise_for_status()
    items = response.json().get("items") or []
    if not items or items[0].get("status") != "found":
        raise RuntimeError(f"{scope_type} {scope_ref} absent de l'environnement {env}.")
    return items[0]


def prepare_google_enrichment(env: str, scope_type: str, scope_ref: str) -> dict[str, Any]:
    """Reuse stored Google JSON first and refresh reviews once per run."""
    base_url, verify = BASE_URLS[env]
    response = requests.post(
        base_url + "/scraper/agentPrepareGoogleEnrichment",
        json={"scope_type": scope_type, "scope_ref": scope_ref, "include_reviews": True},
        headers={"X-Agent-Token": agent_token()}, verify=verify, timeout=120,
    )
    data = response.json()
    if response.status_code >= 400 or not data.get("success"):
        raise RuntimeError(data.get("error") or f"Préparation Google refusée (HTTP {response.status_code}).")
    return data


def fetch_official(url: str) -> dict[str, str]:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 iziLifeEnricher/1.0"}, timeout=40)
    response.raise_for_status()
    parser = TextParser()
    parser.feed(response.text)
    title = re.sub(r"\s+", " ", " ".join(parser.title_parts)).strip()[:300]
    # Une page complète peut embarquer menus, footers et contenus masqués très
    # volumineux. Quinze mille caractères suffisent pour les preuves utiles et
    # évitent de payer/envoyer plusieurs fenêtres de contexte pour une fiche.
    text = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()[:15000]
    return {"url": response.url, "title": title, "text": text,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def load_references(env: str) -> tuple[dict[str, Any], str]:
    all_refs = json.loads(REFERENCES.read_text(encoding="utf-8"))
    if env in all_refs:
        return all_refs[env], env
    if "local" in all_refs:
        return all_refs["local"], "local"
    raise RuntimeError("Aucun référentiel disponible dans tags/references.json.")


def reference_index(refs: dict[str, Any]) -> dict[str, set[str]]:
    result = {
        "tags": {str(row.get("string_id") or "") for row in refs.get("tags", [])},
        "principal_characteristics": set(refs.get("principal_characteristics") or []),
    }
    for family, rows in (refs.get("editorial") or {}).items():
        result[family] = {str(row.get("string_id") or "") for row in rows}
    return result


def compact_references(scope_type: str, refs: dict[str, Any]) -> dict[str, Any]:
    """Réduit le référentiel au contrat utile sans perdre les choix autorisés."""
    scope = scope_type.upper()

    def allowed_for_scope(row: dict[str, Any]) -> bool:
        raw = str(row.get("scope_types") or row.get("tag_types") or "")
        return not raw or scope in {value.strip().upper() for value in raw.split(",")}

    def label(row: dict[str, Any]) -> str:
        string_id = str(row.get("string_id") or "").strip()
        name = str(row.get("name") or "").strip()
        return f"{string_id} | {name}" if name and name != string_id else string_id

    return {
        "tags": [label(row) for row in refs.get("tags", [])
                 if isinstance(row, dict) and allowed_for_scope(row)],
        "principal_characteristics": list(refs.get("principal_characteristics") or []),
        "editorial": {
            family: [label(row) for row in rows
                     if isinstance(row, dict) and allowed_for_scope(row)]
            for family, rows in (refs.get("editorial") or {}).items()
        },
    }


def compact_current_izilife(current: dict[str, Any]) -> dict[str, Any]:
    """Garde l'identité et l'état éditorial utiles, pas tout le graphe métier."""
    data = current.get("data") if isinstance(current.get("data"), dict) else {}
    graph = current.get("graph") if isinstance(current.get("graph"), dict) else {}
    identity_fields = (
        "id", "name", "string_id", "place_string_id", "shop_string_id",
        "primary_category_ref", "short_description", "description", "history",
        "address", "zip_code", "city_ref", "url_website", "url_facebook",
        "url_instagram", "is_active", "listable",
    )
    compact_graph = {
        key: graph.get(key)
        for key in ("ambiences", "characteristics", "other_categories", "equipment", "services")
        if graph.get(key)
    }
    shared_identity = PlaceIdentity.build(
        name=data.get("name", ""), string_id=data.get("string_id") or data.get("place_string_id") or data.get("shop_string_id") or "",
        address=data.get("address", ""), city=data.get("city_ref", ""),
        latitude=data.get("latitude"), longitude=data.get("longitude"),
        urls=[data.get("url_website", ""), data.get("url_facebook", ""), data.get("url_instagram", "")],
    )
    return {
        "type": current.get("type"),
        "status": current.get("status"),
        "identity": {key: data.get(key) for key in identity_fields if data.get(key) not in (None, "")},
        "canonical_identity": shared_identity.lookup_payload(),
        "counts": current.get("counts") or {},
        "editorial_state": compact_graph,
        "google_enrichment": current.get("google_enrichment") or {},
    }


def prompt_payload(scope_type: str, scope_ref: str, current: dict[str, Any],
                   pages: list[dict[str, str]], refs: dict[str, Any]) -> str:
    compact_refs = compact_references(scope_type, refs)
    payload = {
        "target": {"scope_type": scope_type, "scope_ref": scope_ref},
        "current_izilife": compact_current_izilife(current),
        "official_pages": [{"url": page["url"], "title": page["title"], "text": page["text"]}
                           for page in pages],
        "allowed_references": compact_refs,
    }
    return """Retourne uniquement du JSON. Propose seulement des valeurs démontrées par les sources.
Ne transforme jamais une absence de preuve en false. Utilise exclusivement les string_id autorisés.
Chaque proposition porte confidence entre 0 et 1, source_url et evidence courte.
evidence doit être une citation exacte de la source, jamais une paraphrase. Une
absence de mention, une supposition ou un public « probablement » adapté n'est
pas une preuve. Une valeur 0 exige une interdiction ou négation explicite.
Schéma attendu: {"tags":[{"string_id":"...","confidence":0.9,"source_url":"...","evidence":"..."}],
"principal_characteristics":[{"field":"...","value":0|1,"confidence":0.9,"source_url":"...","evidence":"..."}],
"editorial":{"MusicStyle":[{"string_id":"...","confidence":0.9,"source_url":"...","evidence":"..."}]},
"warnings":[],"summary":"..."}.
DONNEES JSON:\n""" + json.dumps(payload, ensure_ascii=False)


def call_server_ai(env: str, scope_type: str, scope_ref: str, current: dict[str, Any],
                   pages: list[dict[str, str]], with_web_search: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    base_url, verify = BASE_URLS[env]
    response = requests.post(base_url + "/scraper/agentAnalyzePlaceEditorial", json={
        "scope_type": scope_type, "scope_ref": scope_ref,
        "current_izilife": compact_current_izilife(current),
        "official_pages": [{"url": p["url"], "title": p["title"], "text": p["text"]} for p in pages],
        "with_web_search": with_web_search,
        "manual_ai_request": True,
    }, headers={"X-Agent-Token": agent_token()}, verify=verify, timeout=240)
    data = response.json()
    if response.status_code >= 400 or not data.get("success"):
        raise RuntimeError(str(data.get("error") or f"HTTP {response.status_code}"))
    return data.get("proposal") or {}, {"provider": data.get("provider"), "web_search": with_web_search}


def evidence_rejection(item: dict[str, Any], pages: list[dict[str, str]],
                       require_explicit_negative: bool = False) -> str:
    if not pages:
        return ""
    evidence = normalized_text(str(item.get("evidence") or ""))
    source_url = canonical_source_url(str(item.get("source_url") or ""))
    weak = ("aucune mention", "non mentionne", "no mention", "not mentioned",
            "absence de", "semble", "probablement", "likely", "probably",
            "broad audience", "large public")
    if not evidence or any(marker in evidence for marker in weak):
        return "preuve absente ou déductive"
    source = next((page for page in pages if canonical_source_url(page.get("url", "")) == source_url), None)
    if source is None:
        return "source non collectée"
    if evidence not in normalized_text(source.get("text", "")):
        return "preuve non retrouvée mot pour mot dans la source"
    if require_explicit_negative:
        negative = (" pas ", " interdit", " uniquement", " reserve aux adultes",
                    " adulte uniquement", " sans ", " ne ")
        padded = f" {evidence} "
        if not any(marker in padded for marker in negative):
            return "valeur 0 sans négation explicite"
    return ""


def validate_proposal(proposal: dict[str, Any], refs: dict[str, Any],
                      pages: list[dict[str, str]] | None = None) -> dict[str, Any]:
    pages = pages or []
    allowed = reference_index(refs)
    accepted: dict[str, Any] = {"tags": [], "principal_characteristics": [],
                                "editorial": {}, "warnings": list(proposal.get("warnings") or []),
                                "rejected": [], "summary": proposal.get("summary") or ""}
    for item in proposal.get("tags") or []:
        reason = evidence_rejection(item, pages) if isinstance(item, dict) else "référence inconnue"
        if isinstance(item, dict) and item.get("string_id") in allowed["tags"] and not reason:
            accepted["tags"].append(item)
        else:
            accepted["rejected"].append({"kind": "tag", "item": item,
                                         "reason": reason or "référence inconnue"})
    for item in proposal.get("principal_characteristics") or []:
        valid = (isinstance(item, dict) and item.get("field") in allowed["principal_characteristics"]
                 and item.get("value") in {0, 1})
        reason = evidence_rejection(item, pages, item.get("value") == 0) if valid else "champ ou valeur invalide"
        if valid and not reason:
            accepted["principal_characteristics"].append(item)
        else:
            accepted["rejected"].append({"kind": "principal_characteristic", "item": item,
                                         "reason": reason})
    for family, items in (proposal.get("editorial") or {}).items():
        if family not in allowed:
            accepted["rejected"].append({"kind": "editorial", "family": family,
                                         "items": items, "reason": "famille inconnue"})
            continue
        for item in items or []:
            reason = evidence_rejection(item, pages) if isinstance(item, dict) else "référence inconnue"
            if isinstance(item, dict) and item.get("string_id") in allowed[family] and not reason:
                accepted["editorial"].setdefault(family, []).append(item)
            else:
                accepted["rejected"].append({"kind": "editorial", "family": family,
                                             "item": item, "reason": reason or "référence inconnue"})
    return accepted


def build_apply_payload(proposal: dict[str, Any], scope_type: str, scope_ref: str,
                        min_confidence: float = 0.8) -> dict[str, Any]:
    """Convertit une proposition validée en payload BO, sans valeur inventée."""
    def confident(item: dict[str, Any]) -> bool:
        try:
            return float(item.get("confidence", 0)) >= min_confidence
        except (TypeError, ValueError):
            return False

    return {
        "scope_type": scope_type,
        "scope_ref": scope_ref,
        "operation": "ADD",
        "tags": [item["string_id"] for item in proposal.get("tags") or [] if confident(item)],
        "principal_characteristics": {
            item["field"]: int(item["value"])
            for item in proposal.get("principal_characteristics") or [] if confident(item)
        },
        "editorial": {
            family: [item["string_id"] for item in items if confident(item)]
            for family, items in (proposal.get("editorial") or {}).items()
            if any(confident(item) for item in items)
        },
    }


def classify_restaurant(pages: list[dict[str, str]]) -> dict[str, Any] | None:
    """Classification prudente : uniquement sur une preuve explicite de la source."""
    text = "\n".join(str(page.get("text") or "") for page in pages)
    rules = [
        ("restaurant-gastronomique", [r"restaurant gastronomique", r"étoil[ée] michelin", r"menu dégustation"], ["a-table"]),
        ("restaurant-rapide", [r"restauration rapide", r"fast[- ]food", r"commande[rz]* au comptoir", r"borne de commande"], ["au-comptoir", "a-emporter"]),
        ("restaurant-rapide", [r"uniquement à emporter", r"exclusivement à emporter"], ["a-emporter"]),
        ("restaurant", [r"service à table", r"servi(?:e|s)? à table"], ["a-table"]),
    ]
    for category, patterns, methods in rules:
        for pattern in patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return {"primary_category_ref": category, "order_methods": methods,
                        "confidence": 0.95, "evidence": match.group(0)}
    return None


def category_apply(env: str, scope_ref: str, category_ref: str) -> dict[str, Any]:
    base_url, verify = BASE_URLS[env]
    response = requests.post(base_url + "/scraper/agentMaintainLocation",
        data={"payload":json.dumps({"scope_type":"SHOP","scope_ref":scope_ref,"primary_category_ref":category_ref})},
        headers={"X-Agent-Token":agent_token()},verify=verify,timeout=120)
    result=response.json()
    if response.status_code>=400 or not result.get("success"):raise RuntimeError(result.get("error") or f"Catégorie refusée HTTP {response.status_code}")
    return result


def review_required(proposal: dict[str, Any]) -> bool:
    """La confiance seule ne crée jamais une demande humaine."""
    return bool(proposal.get("rejected") or [w for w in proposal.get("warnings") or [] if "ambigu" in str(w).lower() or "inconn" in str(w).lower()])


def apply_enrichment(env: str, payload: dict[str, Any]) -> dict[str, Any]:
    base_url, verify = BASE_URLS[env]
    response = requests.post(
        base_url + "/scraper/agentApplyTagsAndCharacts",
        data={"payload": json.dumps(payload, ensure_ascii=False)},
        headers={"X-Agent-Token": agent_token()}, verify=verify, timeout=120,
    )
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Réponse BO non JSON (HTTP {response.status_code}).") from exc
    if response.status_code >= 400 or not result.get("success"):
        raise RuntimeError(result.get("error") or f"Application refusée (HTTP {response.status_code}).")
    return result


def cache_key(scope_type: str, scope_ref: str, current: dict[str, Any],
              pages: list[dict[str, str]], refs: dict[str, Any]) -> str:
    data = {"prompt_version": 3, "scope_type": scope_type, "scope_ref": scope_ref,
            "current": current, "page_hashes": [page["sha256"] for page in pages],
            "references_generated_at": refs.get("generated_at")}
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def write_excel(proposal: dict[str, Any], scope_type: str, scope_ref: str, path: Path) -> None:
    headers = ["scope_type", "scope_ref", "operation", "tags", "principal_characteristics",
               *EDITORIAL_COLUMNS, "status", "notes", "last_result"]
    principal = "|".join(f"{item['field']}={item['value']}" for item in proposal["principal_characteristics"])
    editorial = {family: "|".join(item["string_id"] for item in items)
                 for family, items in proposal["editorial"].items()}
    row = [scope_type, scope_ref, "ADD",
           "|".join(item["string_id"] for item in proposal["tags"]), principal,
           *[editorial.get(name, "") for name in EDITORIAL_COLUMNS],
           "pending", proposal.get("summary", ""), ""]
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Tags et caractéristiques"
    sheet.append(headers)
    sheet.append(row)
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for index in range(1, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(index)].width = 24
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", choices=BASE_URLS, default="local")
    parser.add_argument("--scope-type", choices=["PLACE", "SHOP"], required=True)
    parser.add_argument("--scope-ref", required=True)
    parser.add_argument("--source-url", action="append", default=[])
    parser.add_argument("--with-ai", action="store_true")
    parser.add_argument("--with-web-search", action="store_true")
    parser.add_argument("--proposal-json", type=Path,
                        help="Proposition JSON existante à valider sans appel IA.")
    parser.add_argument("--apply", action="store_true",
                        help="Applique les valeurs validées via AgentTagsAndCharacts.")
    parser.add_argument("--confirm-write", action="store_true",
                        help="Confirmation obligatoire avec --apply.")
    parser.add_argument("--min-confidence", type=float, default=0.8,
                        help="Confiance minimale pour une application (défaut: 0.8).")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("enrichment_reports"))
    args = parser.parse_args()
    if args.apply and not args.confirm_write:
        parser.error("--apply exige --confirm-write")
    if not 0 <= args.min_confidence <= 1:
        parser.error("--min-confidence doit être compris entre 0 et 1")
    if args.with_web_search:
        args.with_ai = True
    google_enrichment = prepare_google_enrichment(args.env, args.scope_type, args.scope_ref)
    current = api_lookup(args.env, args.scope_type, args.scope_ref)
    current["google_enrichment"] = google_enrichment
    refs, refs_env = load_references(args.env)
    pages = []
    source_errors = []
    # Ne jamais parcourir automatiquement Link ni les anciens champs URL de la
    # fiche. Le pilote choisit exactement les pages analysees avec --source-url.
    requested_urls = list(dict.fromkeys(
        str(url).strip() for url in args.source_url if str(url or "").strip()
    ))
    if args.with_ai and not requested_urls and not args.with_web_search:
        parser.error(
            "--with-ai exige au moins un --source-url, sauf si "
            "--with-web-search est explicitement active"
        )
    for url in requested_urls:
        try: pages.append(fetch_official(url))
        except Exception as exc: source_errors.append({"url": url, "error": str(exc)})
    key = cache_key(args.scope_type, args.scope_ref, current, pages, refs)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cache_path = args.output_dir / "cache" / f"{key}.json"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    meta: dict[str, Any] = {"cache_key": key, "references_env": refs_env, "analysis_only": not args.apply}
    if args.proposal_json:
        raw_proposal = json.loads(args.proposal_json.read_text(encoding="utf-8"))
        meta["source"] = "proposal_json"
    elif cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        raw_proposal = cached["proposal"]
        meta.update(cached.get("meta") or {})
        meta["cache_hit"] = True
    elif args.with_ai:
        raw_proposal, ai_meta = call_server_ai(
            args.env, args.scope_type, args.scope_ref, current, pages, args.with_web_search,
        )
        meta.update(ai_meta)
        meta["cache_hit"] = False
        cache_path.write_text(json.dumps({"proposal": raw_proposal, "meta": meta},
                                         ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        raw_proposal = {"tags": [], "principal_characteristics": [], "editorial": {},
                        "warnings": ["Aucune analyse IA demandée. Utiliser --with-ai ou --proposal-json."],
                        "summary": "État iziLife et pages officielles collectés, sans analyse payante."}
        meta["source"] = "deterministic_only"
    evidence_pages = list(pages)
    current_text = json.dumps(compact_current_izilife(current), ensure_ascii=False, default=str)
    evidence_pages.append({"url": "izilife://current", "title": "Fiche iziLife courante",
                           "text": current_text, "sha256": hashlib.sha256(current_text.encode("utf-8")).hexdigest()})
    validated = validate_proposal(raw_proposal, refs, evidence_pages)
    restaurant = classify_restaurant(pages) if args.scope_type == "SHOP" else None
    if restaurant:
        available_methods = reference_index(refs).get("OrderMethod", set())
        validated["editorial"].setdefault("OrderMethod", [])
        for method in restaurant["order_methods"]:
            if method in available_methods and not any(item.get("string_id") == method for item in validated["editorial"]["OrderMethod"]):
                validated["editorial"]["OrderMethod"].append({"string_id":method,"confidence":restaurant["confidence"],"source_url":pages[0]["url"],"evidence":restaurant["evidence"]})
    apply_payload = build_apply_payload(
        validated, args.scope_type, args.scope_ref, args.min_confidence,
    )
    apply_result = apply_enrichment(args.env, apply_payload) if args.apply else None
    category_result = category_apply(args.env,args.scope_ref,restaurant["primary_category_ref"]) if args.apply and restaurant else None
    result = {"schema_version": "izilife.enrichment.v1",
              "generated_at": datetime.now().isoformat(timespec="seconds"),
              "target": {"scope_type": args.scope_type, "scope_ref": args.scope_ref, "env": args.env},
              "sources": [{k: page[k] for k in ("url", "title", "sha256")} for page in pages],
              "current_izilife": current, "proposal": validated,
              "apply_payload": apply_payload, "apply_result": apply_result,
              "restaurant_classification": restaurant, "category_result": category_result,
              "review_required": review_required(validated), "source_errors": source_errors, "meta": meta}
    stem = f"{args.scope_type.lower()}_{args.scope_ref}_{datetime.now():%Y%m%d_%H%M%S}"
    json_path = args.output_dir / f"{stem}.json"
    xlsx_path = args.output_dir / f"{stem}.xlsx"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_excel(validated, args.scope_type, args.scope_ref, xlsx_path)
    print(json.dumps({"json": str(json_path), "xlsx": str(xlsx_path),
                      "accepted": {"tags": len(validated["tags"]),
                                   "principal_characteristics": len(validated["principal_characteristics"]),
                                   "editorial": sum(len(v) for v in validated["editorial"].values())},
                      "rejected": len(validated["rejected"]),
                      "analysis_only": not args.apply, "apply_result": apply_result},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
