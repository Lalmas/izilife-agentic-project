#!/usr/bin/env python3
"""Audit, planification et import sélectif de la curation iziLife.

`audit` et `plan` sont sans écriture. `apply` exige un plan figé, son hash serveur,
une clé d'idempotence et des confirmations explicites, renforcées en production.
"""

from __future__ import annotations

import argparse
from copy import copy
import hashlib
import json
import mimetypes
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import urllib3
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


ENVIRONMENTS = {
    "local": {"base_url": "https://localhost:4443/izilife-admin", "verify_ssl": False},
    "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify_ssl": True},
    "prod": {"base_url": "https://www.izilife.co/izilife-admin", "verify_ssl": True},
}
INSPECT_ENDPOINT = "/scraper/agentCurationSyncInspect"
LIST_SCOPES_ENDPOINT = "/scraper/agentCurationSyncListScopes"
PLAN_ENDPOINT = "/scraper/agentCurationSyncPlan"
APPLY_ENDPOINT = "/scraper/agentCurationSyncApply"
MEDIA_DOWNLOAD_ENDPOINT = "/scraper/agentCurationSyncMediaDownload"
MEDIA_UPLOAD_ENDPOINT = "/scraper/agentAddScopedMedia"
LOCATION_MAINTENANCE_ENDPOINT = "/scraper/agentMaintainLocation"
TARGET_HEADERS = [
    "SCOPE_KEY", "SCOPE_TYPE", "LOCAL_REF", "STAGING_REF", "PROD_REF",
    "SOURCE_PREFERENCE", "ALLOW_CREATE_PROD", "MEDIA", "EXTERNAL_MEDIA", "LINKS",
    "AMBIENCES", "CHARACTERISTICS", "PRODUCTS", "PRODUCT_OPTIONS", "EQUIPMENT",
    "SERVICES", "EAP", "HOURS", "ENABLED", "NOTES", "LOCAL_NAME", "GOOGLE_PLACE_ID",
    "STAGING_NAME", "PROD_NAME",
    "LOCAL_TYPE", "STAGING_TYPE", "PROD_TYPE",
]
INVENTORY_HEADERS = [
    "SCOPE_KEY", "ENV", "REQUESTED_TYPE", "REQUESTED_REF", "EXISTS", "RESOLVED_TYPE",
    "RESOLVED_REF", "NAME", "GOOGLE_PLACE_ID", "MATCH_METHOD", "MATCH_STATUS",
    "IS_ACTIVE", "LISTABLE", "CLOSED_STATE", "MEDIA", "EXTERNAL_MEDIA", "LINKS",
    "AMBIENCES", "CHARACTERISTICS", "PRODUCTS", "PRODUCT_CATEGORIES", "PRODUCT_OPTIONS",
    "EQUIPMENT", "SERVICES", "EAP", "HOURS", "AUDITED_AT", "MESSAGE",
]
AMBIGUITY_HEADERS = [
    "SCOPE_KEY", "ENV", "OBJECT_TYPE", "SOURCE_REFERENCE", "CANDIDATE_REFERENCE",
    "REASON", "EVIDENCE", "REQUIRED_DECISION", "STATUS",
]


@dataclass
class Target:
    scope_key: str
    scope_type: str
    refs: dict[str, str]
    types: dict[str, str]
    row: dict[str, Any]


def normalize(value: Any) -> str:
    return str(value or "").strip()


def enabled(value: Any) -> bool:
    return normalize(value).upper() not in {"NON", "NO", "0", "FALSE"}


def table_rows(sheet, header_row: int = 4) -> list[dict[str, Any]]:
    headers = [normalize(cell.value).upper() for cell in sheet[header_row]]
    rows: list[dict[str, Any]] = []
    for values in sheet.iter_rows(min_row=header_row + 1, values_only=True):
        row = {headers[index]: value for index, value in enumerate(values) if index < len(headers) and headers[index]}
        if any(value not in (None, "") for value in row.values()):
            rows.append(row)
    return rows


def load_targets(workbook_path: Path, selected: set[str]) -> list[Target]:
    wb = load_workbook(workbook_path, read_only=True, data_only=False)
    try:
        rows = table_rows(wb["CIBLES"])
    finally:
        wb.close()
    targets = []
    for row in rows:
        key = normalize(row.get("SCOPE_KEY"))
        if not key or not enabled(row.get("ENABLED")) or (selected and key not in selected):
            continue
        targets.append(Target(
            scope_key=key,
            scope_type=normalize(row.get("SCOPE_TYPE")).upper(),
            refs={env: normalize(row.get(f"{env.upper()}_REF")) for env in ENVIRONMENTS},
            types={env: normalize(row.get(f"{env.upper()}_TYPE") or row.get("SCOPE_TYPE")).upper() for env in ENVIRONMENTS},
            row=row,
        ))
    return targets


class Inspector:
    def __init__(self, token: str, timeout: int = 60):
        self.token = token
        self.timeout = timeout
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def inspect(self, env: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.post(env, INSPECT_ENDPOINT, payload)

    def post(self, env: str, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        cfg = ENVIRONMENTS[env]
        try:
            response = requests.post(
                cfg["base_url"] + endpoint,
                json={k: v for k, v in payload.items() if v not in (None, "", 0)},
                headers={"X-Agent-Token": self.token, "Accept": "application/json"},
                timeout=self.timeout,
                verify=cfg["verify_ssl"],
            )
            try:
                body = response.json()
            except ValueError:
                body = {"success": False, "error": response.text[:500] or "Réponse non JSON"}
            if response.status_code >= 400:
                body.setdefault("success", False)
                body.setdefault("error", f"HTTP {response.status_code}")
            body["http_status"] = response.status_code
            return body
        except requests.RequestException as exc:
            return {"success": False, "error": str(exc), "http_status": None}

    def list_google_scopes(self, env: str) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        offset = 0
        while True:
            result = self.post(env, LIST_SCOPES_ENDPOINT, {"limit": 500, "offset": offset})
            if not result.get("success"):
                raise RuntimeError(f"Inventaire {env} impossible: {result.get('error', 'erreur inconnue')}")
            page = result.get("items") or []
            items.extend(page)
            offset += len(page)
            if not page or offset >= int(result.get("total") or 0):
                break
        return items

    def download_media(self, env: str, scope_type: str, scope_ref: str, source_media_id: int, object_type: str | None = None, source_object_id: int | None = None) -> tuple[bytes, str, str]:
        cfg = ENVIRONMENTS[env]
        payload={"scope_type": scope_type, "scope_ref": scope_ref, "source_media_id": source_media_id}
        if object_type: payload["object_type"]=object_type
        if source_object_id: payload["source_object_id"]=source_object_id
        response = requests.post(cfg["base_url"] + MEDIA_DOWNLOAD_ENDPOINT, json=payload, headers={"X-Agent-Token": self.token}, timeout=self.timeout, verify=cfg["verify_ssl"])
        if response.status_code >= 400:
            try: error = response.json().get("error")
            except ValueError: error = response.text[:300]
            raise RuntimeError(f"Téléchargement média {env} impossible: {error}")
        return response.content, response.headers.get("Content-Type", "application/octet-stream"), requests.utils.unquote(response.headers.get("X-Original-Name", f"media-{source_media_id}"))

    def upload_media(self, env: str, scope_type: str, scope_ref: str, media: dict[str, Any], content: bytes, mime: str, filename: str, destination_id: int | None = None) -> dict[str, Any]:
        cfg = ENVIRONMENTS[env]
        data={"scope_type": scope_type,"scope_ref": scope_ref,"belongs_to_scope": "oui","rights_confirmed": "oui","is_principal": "oui" if int(media.get("is_principal") or 0) else "non","title": media.get("title") or "","description": media.get("description") or ""}
        if destination_id:
            data["destination_id"]=str(destination_id); data["scope_ref"]=""
        response = requests.post(cfg["base_url"] + MEDIA_UPLOAD_ENDPOINT, data=data, files={"media": (filename, content, mime)}, headers={"X-Agent-Token": self.token,"Accept":"application/json"}, timeout=max(self.timeout, 180), verify=cfg["verify_ssl"])
        try: body = response.json()
        except ValueError: body = {"success":False,"error":response.text[:500]}
        if response.status_code >= 400 or not body.get("success"): raise RuntimeError(body.get("error") or f"Upload média HTTP {response.status_code}")
        return body


def explicit_audit(inspector: Inspector, target: Target, env: str) -> dict[str, Any]:
    ref = target.refs[env]
    scope_type = target.types[env]
    if not scope_type:
        return {"success": False, "match_status": "BLOCKED", "error": f"{env.upper()}_TYPE/SCOPE_TYPE manquant"}
    if not ref:
        return {"success": True, "match_status": "NOT_REQUESTED", "graph": None, "candidates": []}
    return inspector.inspect(env, {"scope_type": scope_type, "scope_ref": ref})


def discover_prod(inspector: Inspector, target: Target, source_results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    explicit_result: dict[str, Any] | None = None
    if target.refs["prod"]:
        explicit_result = explicit_audit(inspector, target, "prod")
        explicit_identity = ((explicit_result.get("graph") or {}).get("identity") or {})
        if (
            explicit_result.get("match_status") == "MATCHED"
            and str(explicit_identity.get("is_active")) == "1"
            and str(explicit_identity.get("listable")) == "1"
        ):
            return explicit_result
    attempts: list[tuple[str, dict[str, Any]]] = []
    seen: set[tuple[str, str]] = set()
    if explicit_result:
        explicit_identity = ((explicit_result.get("graph") or {}).get("identity") or {})
        explicit_google_id = normalize(explicit_identity.get("google_place_id"))
        explicit_ref = normalize(explicit_identity.get("scope_ref"))
        explicit_type = normalize(explicit_identity.get("scope_type")).upper() or target.types["prod"]
        for scope_type in dict.fromkeys((explicit_type, "SHOP" if explicit_type == "PLACE" else "PLACE")):
            if explicit_google_id and (scope_type, "google", explicit_google_id) not in seen:
                seen.add((scope_type, "google", explicit_google_id))
                attempts.append((f"prod_ref:{scope_type}:google_place_id", {"scope_type": scope_type, "google_place_id": explicit_google_id}))
            if explicit_ref and (scope_type, "ref", explicit_ref) not in seen:
                seen.add((scope_type, "ref", explicit_ref))
                attempts.append((f"prod_ref:{scope_type}:scope_ref", {"scope_type": scope_type, "scope_ref": explicit_ref}))
    for source_env in ("staging", "local"):
        graph = source_results.get(source_env, {}).get("graph")
        identity = graph.get("identity", {}) if isinstance(graph, dict) else {}
        google_id = normalize(identity.get("google_place_id"))
        source_ref = normalize(identity.get("scope_ref"))
        source_type = target.types[source_env]
        for scope_type in dict.fromkeys((source_type, "SHOP" if source_type == "PLACE" else "PLACE")):
            if google_id and (scope_type, "google", google_id) not in seen:
                seen.add((scope_type, "google", google_id))
                attempts.append((f"{source_env}:{scope_type}:google_place_id", {"scope_type": scope_type, "google_place_id": google_id}))
            if source_ref and (scope_type, "ref", source_ref) not in seen:
                seen.add((scope_type, "ref", source_ref))
                attempts.append((f"{source_env}:{scope_type}:scope_ref", {"scope_type": scope_type, "scope_ref": source_ref}))

    matches: dict[str, dict[str, Any]] = {}
    candidates: list[dict[str, Any]] = []
    errors: list[str] = []
    if explicit_result and explicit_result.get("match_status") == "MATCHED" and isinstance(explicit_result.get("graph"), dict):
        identity = explicit_result["graph"].get("identity", {})
        key = f"{identity.get('scope_type')}:{identity.get('scope_ref')}"
        matches[key] = explicit_result | {"discovery_evidence": "prod_ref_explicit"}
    for evidence, payload in attempts:
        result = inspector.inspect("prod", payload)
        if not result.get("success"):
            errors.append(f"{evidence}: {result.get('error', 'erreur')}")
            continue
        graph = result.get("graph")
        if result.get("match_status") == "MATCHED" and isinstance(graph, dict):
            identity = graph.get("identity", {})
            key = f"{identity.get('scope_type')}:{identity.get('scope_ref')}"
            matches[key] = result | {"discovery_evidence": evidence}
        for candidate in result.get("candidates") or []:
            candidates.append(candidate | {"discovery_evidence": evidence})
    active_matches = {
        key: value for key, value in matches.items()
        if str((value.get("graph") or {}).get("identity", {}).get("is_active")) == "1"
        and str((value.get("graph") or {}).get("identity", {}).get("listable")) == "1"
    }
    if len(active_matches) == 1:
        return next(iter(active_matches.values()))
    if len(active_matches) > 1:
        matches = active_matches
    if len(matches) == 1:
        return next(iter(matches.values()))
    if len(matches) > 1:
        return {"success": True, "match_status": "AMBIGUOUS", "match_method": None, "graph": None, "candidates": [m["graph"]["identity"] | {"discovery_evidence": m["discovery_evidence"]} for m in matches.values()]}
    if errors and not candidates:
        return {"success": False, "match_status": "UNAVAILABLE", "graph": None, "candidates": [], "error": " | ".join(errors)}
    return {"success": True, "match_status": "AMBIGUOUS" if candidates else "MISSING", "graph": None, "candidates": candidates}


def inventory_row(target: Target, env: str, result: dict[str, Any], audited_at: datetime) -> list[Any]:
    graph = result.get("graph") if isinstance(result, dict) else None
    identity = graph.get("identity", {}) if isinstance(graph, dict) else {}
    counts = graph.get("counts", {}) if isinstance(graph, dict) else {}
    status = normalize(result.get("match_status")) or ("ERROR" if not result.get("success") else "MISSING")
    return [
        target.scope_key, env.upper(), target.types[env], target.refs[env], "OUI" if graph else "NON",
        identity.get("scope_type"), identity.get("scope_ref"), identity.get("name"), identity.get("google_place_id"),
        result.get("match_method"), status, identity.get("is_active"), identity.get("listable"), identity.get("closed_state_ref"),
        counts.get("media"), counts.get("external_media"), counts.get("links"), counts.get("ambiences"), counts.get("characteristics"),
        counts.get("products"), counts.get("product_categories"), counts.get("product_options"), counts.get("equipment"), counts.get("services"),
        counts.get("eap"), counts.get("hours"), audited_at, result.get("error") or result.get("discovery_evidence"),
    ]


def ambiguity_rows(target: Target, env: str, result: dict[str, Any]) -> list[list[Any]]:
    if result.get("match_status") not in {"AMBIGUOUS", "BLOCKED", "UNAVAILABLE"}:
        return []
    candidates = result.get("candidates") or [None]
    rows = []
    for candidate in candidates:
        candidate = candidate or {}
        candidate_ref = normalize(candidate.get("scope_ref"))
        evidence = {
            "name": candidate.get("name"),
            "google_place_id": candidate.get("google_place_id"),
            "city_id": candidate.get("city_id"),
            "method": candidate.get("match_method"),
            "discovery_evidence": candidate.get("discovery_evidence"),
        }
        rows.append([
            target.scope_key, env.upper(), target.types[env], target.refs[env], candidate_ref,
            result.get("error") or result.get("match_status"), json.dumps(evidence, ensure_ascii=False),
            "Renseigner la référence exacte ou exclure la cible", "À VALIDER",
        ])
    return rows


def clear_and_write(sheet, headers: list[str], rows: list[list[Any]], table_name: str) -> None:
    header_row = 4
    max_row = max(sheet.max_row, header_row + 1)
    for row in sheet.iter_rows(min_row=header_row + 1, max_row=max_row, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.value = None
            cell.fill = PatternFill(fill_type=None)
            cell.font = Font(name="Arial", size=10, color="1F2937")
            cell.alignment = Alignment(vertical="center")
    for index, header in enumerate(headers, 1):
        sheet.cell(header_row, index, header)
    write_rows = rows or [[None] * len(headers)]
    for row_index, values in enumerate(write_rows, header_row + 1):
        for column_index, value in enumerate(values, 1):
            cell = sheet.cell(row_index, column_index, value)
            cell.font = Font(name="Arial", size=10, color="1F2937")
            wrap = headers[column_index - 1] in {"NAME", "GOOGLE_PLACE_ID", "MESSAGE", "EVIDENCE", "REQUIRED_DECISION", "VALIDATION_NOTE"}
            cell.alignment = Alignment(vertical="top", wrap_text=wrap)
        sheet.row_dimensions[row_index].height = 42 if any(headers[i] in {"MESSAGE", "EVIDENCE", "REQUIRED_DECISION"} and values[i] for i in range(min(len(values), len(headers)))) else 24
    table = sheet.tables[table_name]
    table.ref = f"A{header_row}:{get_column_letter(len(headers))}{header_row + len(write_rows)}"


def update_workbook(path: Path, inventory: list[list[Any]], ambiguities: list[list[Any]]) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.stem}.backup-{stamp}{path.suffix}")
    shutil.copy2(path, backup)
    wb = load_workbook(path)
    clear_and_write(wb["ETAT_DES_LIEUX"], INVENTORY_HEADERS, inventory, "SyncInventory")
    clear_and_write(wb["AMBIGUITES"], AMBIGUITY_HEADERS, ambiguities, "SyncAmbiguities")
    wb.save(path)
    wb.close()
    return backup


def reconcile_audit_report(path: Path, report: dict[str, Any], env: str, authorize_missing_prod: bool = False) -> tuple[Path, int, int]:
    """Recopie uniquement les correspondances certaines d'un audit dans CIBLES."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.stem}.backup-{stamp}{path.suffix}")
    shutil.copy2(path, backup)
    wb = load_workbook(path)
    sheet = wb["CIBLES"]
    headers = [normalize(cell.value).upper() for cell in sheet[4]]
    index = {header: position + 1 for position, header in enumerate(headers) if header}
    required = {"SCOPE_KEY", f"{env.upper()}_REF", f"{env.upper()}_TYPE", f"{env.upper()}_NAME"}
    if authorize_missing_prod:
        required.add("ALLOW_CREATE_PROD")
    missing = sorted(required.difference(index))
    if missing:
        wb.close()
        raise RuntimeError(f"Colonnes CIBLES manquantes: {', '.join(missing)}")
    rows = {
        normalize(sheet.cell(row, index["SCOPE_KEY"]).value): row
        for row in range(5, sheet.max_row + 1)
        if normalize(sheet.cell(row, index["SCOPE_KEY"]).value)
    }
    updated = 0
    authorized = 0
    for key, environments in (report.get("targets") or {}).items():
        result = (environments or {}).get(env) or {}
        identity = (result.get("graph") or {}).get("identity") or {}
        row = rows.get(normalize(key))
        if not row:
            continue
        if authorize_missing_prod and env == "prod" and result.get("match_status") == "MISSING":
            source = next(
                (
                    (environments.get(source_env) or {}).get("graph") or {}
                    for source_env in ("staging", "local")
                    if (environments.get(source_env) or {}).get("match_status") == "MATCHED"
                ),
                {},
            )
            source_identity = source.get("identity") or {}
            safe = (
                str(source_identity.get("is_active")) == "1"
                and str(source_identity.get("listable")) == "1"
                and not source_identity.get("closed_state")
                and bool(source_identity.get("google_place_id"))
            )
            if safe and normalize(sheet.cell(row, index["ALLOW_CREATE_PROD"]).value).upper() != "OUI":
                sheet.cell(row, index["ALLOW_CREATE_PROD"], "OUI")
                authorized += 1
            if safe:
                source_type = normalize(source_identity.get("scope_type")).upper()
                if source_type and normalize(sheet.cell(row, index["PROD_TYPE"]).value).upper() != source_type:
                    sheet.cell(row, index["PROD_TYPE"], source_type)
                    updated += 1
        if result.get("match_status") != "MATCHED" or not identity.get("scope_ref"):
            continue
        values = {
            f"{env.upper()}_REF": identity.get("scope_ref"),
            f"{env.upper()}_TYPE": identity.get("scope_type"),
            f"{env.upper()}_NAME": identity.get("name"),
        }
        changed = False
        for header, value in values.items():
            cell = sheet.cell(row, index[header])
            if normalize(cell.value) != normalize(value):
                cell.value = value
                changed = True
        updated += int(changed)
    wb.save(path)
    wb.close()
    return backup, updated, authorized


def run_reconcile_report(args: argparse.Namespace) -> int:
    workbook = Path(args.workbook).expanduser().resolve()
    report_path = Path(args.report).expanduser().resolve()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    backup, updated, authorized = reconcile_audit_report(workbook, report, args.env, args.authorize_missing_prod)
    print(f"Lignes complétées depuis l'audit {args.env}: {updated}")
    print(f"Créations production autorisées dans le classeur: {authorized}")
    print(f"Classeur : {workbook}")
    print(f"Sauvegarde : {backup}")
    return 0


def prepare_environment_workbook(path: Path, scopes: list[dict[str, Any]], env: str, add_unmatched: bool) -> tuple[Path, int, int, int]:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.stem}.backup-{stamp}{path.suffix}")
    shutil.copy2(path, backup)
    wb = load_workbook(path)
    sheet = wb["CIBLES"]
    headers = [normalize(cell.value).upper() for cell in sheet[4]]
    missing_headers = [header for header in TARGET_HEADERS if header not in headers]
    if missing_headers:
        wb.close()
        raise RuntimeError(f"Colonnes CIBLES manquantes: {', '.join(missing_headers)}")
    index = {header: position + 1 for position, header in enumerate(headers) if header}
    ref_header = f"{env.upper()}_REF"
    name_header = f"{env.upper()}_NAME"
    type_header = f"{env.upper()}_TYPE"
    rows_by_identity: dict[tuple[str, str], int] = {}
    rows_by_google: dict[str, list[int]] = {}
    used_keys: set[str] = set()
    for row_number in range(5, sheet.max_row + 1):
        key = normalize(sheet.cell(row_number, index["SCOPE_KEY"]).value)
        scope_type = normalize(sheet.cell(row_number, index["SCOPE_TYPE"]).value).upper()
        env_ref = normalize(sheet.cell(row_number, index[ref_header]).value)
        google_id = normalize(sheet.cell(row_number, index["GOOGLE_PLACE_ID"]).value)
        if key:
            used_keys.add(key)
        if scope_type and env_ref:
            rows_by_identity[(scope_type, env_ref)] = row_number
        if google_id:
            rows_by_google.setdefault(google_id, []).append(row_number)

    created = 0
    updated = 0
    skipped = 0
    template_row = 5
    for scope in scopes:
        scope_type = normalize(scope.get("scope_type")).upper()
        env_ref = normalize(scope.get("scope_ref"))
        google_id = normalize(scope.get("google_place_id"))
        name = normalize(scope.get("name"))
        google_matches = rows_by_google.get(google_id, []) if google_id else []
        row_number = google_matches[0] if len(google_matches) == 1 else rows_by_identity.get((scope_type, env_ref))
        if row_number:
            updated += 1
        else:
            if not add_unmatched:
                skipped += 1
                continue
            row_number = sheet.max_row + 1
            for column in range(1, len(headers) + 1):
                source = sheet.cell(template_row, column)
                target = sheet.cell(row_number, column)
                if source.has_style:
                    target._style = copy(source._style)
                target.number_format = source.number_format
                target.alignment = copy(source.alignment)
                target.protection = copy(source.protection)
            key = env_ref
            if key in used_keys:
                key = f"{scope_type.lower()}-{env_ref}"
            suffix = 2
            base_key = key
            while key in used_keys:
                key = f"{base_key}-{suffix}"
                suffix += 1
            used_keys.add(key)
            defaults = {
                "SCOPE_KEY": key, "SCOPE_TYPE": scope_type, ref_header: env_ref,
                "SOURCE_PREFERENCE": "AUTO", "ALLOW_CREATE_PROD": "NON", "ENABLED": "OUI",
                "NOTES": f"Ajout automatique depuis l'inventaire {env}",
            }
            for policy in ["MEDIA","EXTERNAL_MEDIA","LINKS","AMBIENCES","CHARACTERISTICS","PRODUCTS","PRODUCT_OPTIONS","EQUIPMENT","SERVICES","EAP","HOURS"]:
                defaults[policy] = "AUTO"
            for header, value in defaults.items():
                sheet.cell(row_number, index[header], value)
            created += 1
        sheet.cell(row_number, index["SCOPE_TYPE"], scope_type)
        sheet.cell(row_number, index[ref_header], env_ref)
        sheet.cell(row_number, index[name_header], name)
        sheet.cell(row_number, index[type_header], scope_type)
        if not normalize(sheet.cell(row_number, index["GOOGLE_PLACE_ID"]).value):
            sheet.cell(row_number, index["GOOGLE_PLACE_ID"], google_id)
        rows_by_identity[(scope_type, env_ref)] = row_number
        if google_id:
            rows_by_google.setdefault(google_id, [])
            if row_number not in rows_by_google[google_id]:
                rows_by_google[google_id].append(row_number)

    populated = []
    for row_number in range(5, sheet.max_row + 1):
        if normalize(sheet.cell(row_number, index["SCOPE_KEY"]).value):
            populated.append([sheet.cell(row_number, column).value for column in range(1, len(headers) + 1)])
    original_max_row = sheet.max_row
    for row_number in range(5, original_max_row + 1):
        for column in range(1, len(headers) + 1):
            sheet.cell(row_number, column).value = None
    for offset, values in enumerate(populated, start=5):
        for column, value in enumerate(values, start=1):
            target = sheet.cell(offset, column, value)
            source = sheet.cell(template_row, column)
            if source.has_style:
                target._style = copy(source._style)
            target.number_format = source.number_format
            target.alignment = copy(source.alignment)
            target.protection = copy(source.protection)

    validation_ranges = {
        "B": "B5:B2000", "F": "F5:F2000", "G": "G5:G2000",
        "H": "H5:R2000", "S": "S5:S2000",
    }
    for validation in sheet.data_validations.dataValidation:
        current = str(validation.sqref)
        for prefix, target_range in validation_ranges.items():
            if current.startswith(prefix + "5"):
                validation.sqref = target_range
                break

    last_row = 4 + len(populated)
    sheet.tables["SyncTargets"].ref = f"A4:{get_column_letter(len(headers))}{last_row}"
    sheet.auto_filter.ref = sheet.tables["SyncTargets"].ref
    wb.save(path)
    wb.close()
    return backup, created, updated, skipped


def run_prepare_local(args: argparse.Namespace) -> int:
    args.env = "local"
    args.include_unmatched_prod = False
    return run_prepare_environment(args)


def run_prepare_environment(args: argparse.Namespace) -> int:
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    workbook_path = Path(args.workbook).expanduser().resolve()
    if not workbook_path.is_file():
        raise RuntimeError(f"Classeur introuvable: {workbook_path}")
    inspector = Inspector(token, args.timeout)
    env = args.env
    scopes = inspector.list_google_scopes(env)
    add_unmatched = env != "prod" or bool(args.include_unmatched_prod)
    backup, created, updated, skipped = prepare_environment_workbook(workbook_path, scopes, env, add_unmatched)
    print(f"Scopes {env} avec google_place_id : {len(scopes)}")
    print(f"Lignes créées : {created}")
    print(f"Lignes complétées : {updated}")
    print(f"Lignes ignorées car absentes des cibles : {skipped}")
    print(f"Classeur : {workbook_path}")
    print(f"Sauvegarde : {backup}")
    return 0


def run_audit(args: argparse.Namespace) -> int:
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    workbook_path = Path(args.workbook).expanduser().resolve()
    if not workbook_path.is_file():
        raise RuntimeError(f"Classeur introuvable: {workbook_path}")
    selected = set(args.scope or [])
    targets = load_targets(workbook_path, selected)
    inspector = Inspector(token, args.timeout)
    audited_at = datetime.now()
    inventory: list[list[Any]] = []
    ambiguities: list[list[Any]] = []
    json_result: dict[str, Any] = {"audited_at": audited_at.isoformat(), "targets": {}}
    requested_envs = list(dict.fromkeys(args.envs))

    for target in targets:
        print(f"[{target.scope_key}] audit")
        results: dict[str, dict[str, Any]] = {}
        for env in ("local", "staging"):
            if env in requested_envs:
                results[env] = explicit_audit(inspector, target, env)
        if "prod" in requested_envs:
            results["prod"] = discover_prod(inspector, target, results)
        for env in requested_envs:
            result = results.get(env) or {"success": True, "match_status": "NOT_REQUESTED", "graph": None, "candidates": []}
            inventory.append(inventory_row(target, env, result, audited_at))
            ambiguities.extend(ambiguity_rows(target, env, result))
            print(f"  {env}: {result.get('match_status', 'ERROR')}")
        json_result["targets"][target.scope_key] = results

    backup = update_workbook(workbook_path, inventory, ambiguities)
    report_path = Path(args.json_report).resolve() if args.json_report else workbook_path.with_name(f"audit-{audited_at.strftime('%Y%m%d-%H%M%S')}.json")
    report_path.write_text(json.dumps(json_result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"Classeur mis à jour : {workbook_path}")
    print(f"Sauvegarde : {backup}")
    print(f"Rapport JSON : {report_path}")
    return 0


FAMILY_COLUMNS = {
    "media": "MEDIA", "external_media": "EXTERNAL_MEDIA", "links": "LINKS",
    "ambiences": "AMBIENCES", "characteristics": "CHARACTERISTICS",
    "products": "PRODUCTS", "product_options": "PRODUCT_OPTIONS",
    "equipment": "EQUIPMENT", "services": "SERVICES", "eap": "EAP", "hours": "HOURS",
}


def policy(value: Any) -> str:
    value = normalize(value).upper() or "AUTO"
    return value if value in {"AUTO", "INCLUDE", "EXCLUDE", "LOCAL", "STAGING"} else "AUTO"


def source_order(target: Target, family: str) -> list[str]:
    family_policy = policy(target.row.get(FAMILY_COLUMNS.get(family, "")))
    preference = policy(target.row.get("SOURCE_PREFERENCE"))
    forced = family_policy if family_policy in {"LOCAL", "STAGING"} else preference
    return [forced.lower()] if forced in {"LOCAL", "STAGING"} else ["staging", "local"]


def family_size(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if not isinstance(value, dict):
        return int(bool(value))
    if "items" in value or "categories" in value:
        return sum(len(value.get(key) or []) for key in (
            "items", "categories", "option_groups", "option_values",
            "option_assignments", "media",
        ))
    if "sets" in value or "content" in value:
        return len(value.get("sets") or []) + len(value.get("content") or [])
    return sum(family_size(item) for item in value.values())


def choose_family_source(target: Target, family: str, available: dict[str, dict[str, Any]]) -> str | None:
    ordered = [env for env in source_order(target, family) if env in available]
    if not ordered:
        return None
    if len(ordered) == 1:
        return ordered[0]
    # En AUTO, prendre la source réellement la plus riche. L'ordre conserve
    # la préférence staging uniquement en cas d'égalité exacte.
    return max(ordered, key=lambda env: family_size(available[env].get(family)))


def exclude_test_products(graph: dict[str, Any]) -> None:
    """Retire les produits de test et leurs dépendances du graphe transférable."""
    products = graph.get("products")
    if not isinstance(products, dict):
        return

    marker = re.compile(r"(?:^|[^a-z0-9])test(?:[^a-z0-9]|$)", re.IGNORECASE)
    categories = products.get("categories") or []
    excluded_categories = {
        int(category["source_id"])
        for category in categories
        if category.get("source_id") and marker.search(normalize(category.get("name")))
    }
    changed = True
    while changed:
        changed = False
        for category in categories:
            source_id = int(category.get("source_id") or 0)
            parent_id = int(category.get("source_parent_id") or 0)
            if source_id and parent_id in excluded_categories and source_id not in excluded_categories:
                excluded_categories.add(source_id)
                changed = True

    excluded_products: set[int] = set()
    for item in products.get("items") or []:
        searchable = " ".join(normalize(item.get(field)) for field in ("name", "internal_sku", "external_reference"))
        category_id = int(item.get("source_category_id") or 0)
        if marker.search(searchable) or category_id in excluded_categories:
            excluded_products.add(int(item.get("source_id") or 0))

    products["categories"] = [x for x in categories if int(x.get("source_id") or 0) not in excluded_categories]
    products["items"] = [x for x in products.get("items") or [] if int(x.get("source_id") or 0) not in excluded_products]
    products["media"] = [x for x in products.get("media") or [] if int(x.get("source_product_id") or 0) not in excluded_products]

    assignments = [
        x for x in products.get("option_assignments") or []
        if int(x.get("source_product_id") or 0) not in excluded_products
        and int(x.get("source_category_id") or 0) not in excluded_categories
    ]
    products["option_assignments"] = assignments
    used_groups = {int(x.get("source_group_id") or 0) for x in assignments}
    products["option_groups"] = [x for x in products.get("option_groups") or [] if int(x.get("source_id") or 0) in used_groups]
    products["option_values"] = [x for x in products.get("option_values") or [] if int(x.get("source_group_id") or 0) in used_groups]


def build_source_graph(target: Target, results: dict[str, dict[str, Any]], destination_env: str) -> tuple[dict[str, Any] | None, dict[str, str]]:
    # Un environnement destination ne doit jamais être utilisé comme sa propre
    # source : cela recopierait notamment ses médias historiques sans SHA-1.
    available = {env: result.get("graph") for env, result in results.items() if env != destination_env and isinstance(result.get("graph"), dict)}
    if not available:
        return None, {}
    identity_env = next((env for env in source_order(target, "identity") if env in available), next(iter(available)))
    graph = json.loads(json.dumps(available[identity_env]))
    origins = {"identity": identity_env}
    for family in FAMILY_COLUMNS:
        if family == "product_options":
            continue
        chosen = choose_family_source(target, family, available)
        if chosen:
            graph[family] = json.loads(json.dumps(available[chosen][family]))
            if family == "equipment":
                graph["equipment_media"] = json.loads(json.dumps(available[chosen].get("equipment_media", [])))
            origins[family] = chosen
    exclude_test_products(graph)
    return graph, origins


def build_plan_payload(target: Target, destination_env: str, graph: dict[str, Any], allow_create: bool) -> dict[str, Any]:
    destination_ref = target.refs[destination_env] or normalize(graph.get("identity", {}).get("scope_ref"))
    destination_type = target.types[destination_env] or normalize(graph.get("identity", {}).get("scope_type"))
    policies = {}
    for family, column in FAMILY_COLUMNS.items():
        value = policy(target.row.get(column))
        policies[family] = "EXCLUDE" if value == "EXCLUDE" else "INCLUDE" if value == "INCLUDE" else "AUTO"
    return {"destination_type": destination_type,"destination_ref": destination_ref,"allow_create": allow_create,"policies": policies,"graph": graph}


def run_plan(args: argparse.Namespace) -> int:
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token: raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    workbook = Path(args.workbook).expanduser().resolve()
    targets = load_targets(workbook, set(args.scope or []))
    inspector = Inspector(token, args.timeout)
    report: dict[str, Any] = {"format":"izilife-curation-plan-v1","created_at":datetime.now().isoformat(),"destination_env":args.env,"targets":{}}
    for target in targets:
        source_results = {env: explicit_audit(inspector, target, env) for env in ("local","staging") if target.refs[env]}
        graph, origins = build_source_graph(target, source_results, args.env)
        if not graph:
            report["targets"][target.scope_key] = {"status":"BLOCKED","error":"Aucun graphe source disponible"}; continue
        allow_create = bool(args.allow_create) and (args.env != "prod" or normalize(target.row.get("ALLOW_CREATE_PROD")).upper() in {"OUI","YES","1","TRUE"})
        payload = build_plan_payload(target, args.env, graph, allow_create)
        response = inspector.post(args.env, PLAN_ENDPOINT, payload)
        source_scopes = {env: (result.get("graph") or {}).get("identity", {}) for env, result in source_results.items() if isinstance(result.get("graph"), dict)}
        item = {"status":"PLANNED" if response.get("success") else "ERROR","source_origins":origins,"source_scopes":source_scopes,"payload":payload,"server_plan":response.get("plan"),"error":response.get("error")}
        report["targets"][target.scope_key] = item
        print(f"[{target.scope_key}] {item['status']} -> {payload['destination_type']}:{payload['destination_ref']}")
    output = Path(args.output).expanduser().resolve()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"Plan : {output}\nSHA-256 fichier : {digest}")
    return 0


def run_apply(args: argparse.Namespace) -> int:
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token: raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    if args.confirm != "CURATION_SYNC_APPLY": raise RuntimeError("Utiliser --confirm CURATION_SYNC_APPLY.")
    plan_path = Path(args.plan).expanduser().resolve()
    report = json.loads(plan_path.read_text(encoding="utf-8"))
    env = normalize(report.get("destination_env")).lower()
    if env not in {"local","staging","prod"}: raise RuntimeError("Environnement du plan invalide.")
    if env == "prod" and args.confirm_production != "I_CONFIRM_PRODUCTION_IMPORT": raise RuntimeError("Production refusée sans --confirm-production I_CONFIRM_PRODUCTION_IMPORT.")
    inspector = Inspector(token, args.timeout)
    journal = {"format":"izilife-curation-apply-v1","plan":str(plan_path),"plan_sha256":hashlib.sha256(plan_path.read_bytes()).hexdigest(),"applied_at":datetime.now().isoformat(),"destination_env":env,"targets":{}}
    for key, item in report.get("targets", {}).items():
        server_plan = item.get("server_plan") or {}
        if item.get("status") != "PLANNED" or not server_plan.get("can_apply"):
            journal["targets"][key] = {"status":"SKIPPED","reason":item.get("error") or server_plan.get("blocked")}; continue
        payload = dict(item["payload"])
        payload.update({"plan_hash":server_plan["plan_hash"],"confirm_apply":"CURATION_SYNC_APPLY","idempotency_key":f"{env}:{key}:{server_plan['plan_hash'][:32]}"})
        result = inspector.post(env, APPLY_ENDPOINT, payload)
        entry: dict[str, Any] = {"status":"APPLIED" if result.get("success") else "ERROR","backend":result,"media":[]}
        if result.get("success") and payload.get("policies",{}).get("media") != "EXCLUDE":
            source_env = item.get("source_origins",{}).get("media")
            source_identity = item.get("source_scopes",{}).get(source_env,{})
            source_ref = source_identity.get("scope_ref")
            source_type = source_identity.get("scope_type")
            if source_env and source_ref and source_type:
                for media in payload.get("graph",{}).get("media",[]):
                    try:
                        content, mime, filename = inspector.download_media(source_env, source_type, source_ref, int(media["source_id"]))
                        actual = hashlib.sha1(content).hexdigest()
                        expected = normalize(media.get("sha1_hash"))
                        if expected and actual.lower() != expected.lower(): raise RuntimeError(f"SHA-1 source différent ({actual} != {expected})")
                        uploaded = inspector.upload_media(env, payload["destination_type"], payload["destination_ref"], media, content, mime, filename)
                        check, _, _ = inspector.download_media(env, payload["destination_type"], payload["destination_ref"], int(uploaded["media_id"]))
                        if hashlib.sha1(check).hexdigest() != actual: raise RuntimeError("Contrôle média destination différent après upload")
                        entry["media"].append({"source_id":media["source_id"],"sha1":actual,"result":uploaded})
                    except Exception as exc:
                        entry["media"].append({"source_id":media.get("source_id"),"error":str(exc)})
                        entry["status"] = "PARTIAL"
        if result.get("success"):
            maps = (result.get("result") or {}).get("_maps", {})
            related_sets = [
                ("PRODUCT", "products", payload.get("graph",{}).get("products",{}).get("media",[]), "source_product_id", maps.get("products",{})),
                ("EQUIPMENT", "equipment", payload.get("graph",{}).get("equipment_media",[]), "source_equipment_id", maps.get("equipment",{})),
            ]
            for object_type, family, media_items, source_fk, destination_map in related_sets:
                if payload.get("policies",{}).get(family) == "EXCLUDE": continue
                source_env = item.get("source_origins",{}).get(family)
                source_identity = item.get("source_scopes",{}).get(source_env,{})
                for media in media_items:
                    source_object_id=int(media.get(source_fk) or 0)
                    destination_id=destination_map.get(str(source_object_id), destination_map.get(source_object_id))
                    if not source_env or not destination_id:
                        entry["media"].append({"object_type":object_type,"source_id":media.get("source_id"),"error":"Correspondance objet destination absente"}); entry["status"]="PARTIAL"; continue
                    try:
                        content,mime,filename=inspector.download_media(source_env,source_identity.get("scope_type"),source_identity.get("scope_ref"),int(media["source_id"]),object_type,source_object_id)
                        actual=hashlib.sha1(content).hexdigest(); expected=normalize(media.get("sha1_hash"))
                        if expected and actual.lower()!=expected.lower(): raise RuntimeError("SHA-1 source différent")
                        uploaded=inspector.upload_media(env,object_type,"",media,content,mime,filename,int(destination_id))
                        check,_,_=inspector.download_media(env,payload["destination_type"],payload["destination_ref"],int(uploaded["media_id"]),object_type,int(destination_id))
                        if hashlib.sha1(check).hexdigest()!=actual: raise RuntimeError("Contrôle média destination différent après upload")
                        entry["media"].append({"object_type":object_type,"source_id":media["source_id"],"destination_id":destination_id,"sha1":actual,"result":uploaded})
                    except Exception as exc:
                        entry["media"].append({"object_type":object_type,"source_id":media.get("source_id"),"error":str(exc)}); entry["status"]="PARTIAL"
        journal["targets"][key] = entry
        print(f"[{key}] {entry['status']}")
    output = Path(args.journal or plan_path.with_name(f"apply-{env}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")).resolve()
    output.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Journal : {output}")
    return 0 if all(x.get("status") in {"APPLIED","SKIPPED"} for x in journal["targets"].values()) else 2


def run_verify(args: argparse.Namespace) -> int:
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token: raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    report = json.loads(Path(args.plan).expanduser().resolve().read_text(encoding="utf-8"))
    env = normalize(report.get("destination_env")).lower(); inspector = Inspector(token,args.timeout); failed=0
    for key,item in report.get("targets",{}).items():
        payload=item.get("payload") or {}; result=inspector.inspect(env,{"scope_type":payload.get("destination_type"),"scope_ref":payload.get("destination_ref")})
        ok=result.get("success") and result.get("match_status")=="MATCHED"; failed += 0 if ok else 1
        counts=(result.get("graph") or {}).get("counts",{}); print(f"[{key}] {'OK' if ok else 'ERREUR'} {counts}")
    return 1 if failed else 0


def run_media_move_plan(args: argparse.Namespace) -> int:
    """Prépare sans écriture une copie de médias entre deux fiches Place/Shop."""
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    inspector = Inspector(token, args.timeout)
    source = inspector.inspect(args.source_env, {
        "scope_type": args.source_type,
        "scope_ref": args.source_ref,
    })
    destination = inspector.inspect(args.destination_env, {
        "scope_type": args.destination_type,
        "scope_ref": args.destination_ref,
    })
    if source.get("match_status") != "MATCHED":
        raise RuntimeError(f"Fiche source introuvable: {args.source_type}:{args.source_ref}")
    if destination.get("match_status") != "MATCHED":
        raise RuntimeError(f"Fiche destination introuvable: {args.destination_type}:{args.destination_ref}")
    source_graph = source.get("graph") or {}
    destination_graph = destination.get("graph") or {}
    destination_hashes = {
        normalize(media.get("sha1_hash")).lower()
        for media in destination_graph.get("media") or []
        if normalize(media.get("sha1_hash"))
    }
    media = []
    for item in source_graph.get("media") or []:
        sha1 = normalize(item.get("sha1_hash")).lower()
        media.append({
            "source_id": int(item["source_id"]),
            "sha1_hash": sha1 or None,
            "title": item.get("title"),
            "description": item.get("description"),
            "is_principal": int(item.get("is_principal") or 0),
            "action": "SKIP_DUPLICATE" if sha1 and sha1 in destination_hashes else "COPY",
        })
    plan = {
        "format": "izilife-media-move-plan-v1",
        "created_at": datetime.now().isoformat(),
        "source": {"env": args.source_env, "type": args.source_type, "ref": args.source_ref},
        "destination": {"env": args.destination_env, "type": args.destination_type, "ref": args.destination_ref},
        "close_source_after_verified_copy": bool(args.close_source),
        "media": media,
    }
    output = Path(args.output).expanduser().resolve()
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Plan média : {output}")
    print(f"À copier : {sum(x['action'] == 'COPY' for x in media)} ; doublons évités : {sum(x['action'] == 'SKIP_DUPLICATE' for x in media)}")
    return 0


def run_media_move_apply(args: argparse.Namespace) -> int:
    """Copie les médias, les relit, puis ferme éventuellement l'ancienne fiche."""
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")
    if args.confirm != "MEDIA_MOVE_APPLY":
        raise RuntimeError("Utiliser --confirm MEDIA_MOVE_APPLY.")
    plan_path = Path(args.plan).expanduser().resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("format") != "izilife-media-move-plan-v1":
        raise RuntimeError("Format de plan média invalide.")
    source = plan["source"]
    destination = plan["destination"]
    if "prod" in {source["env"], destination["env"]} and args.confirm_production != "I_CONFIRM_PRODUCTION_MEDIA_MOVE":
        raise RuntimeError("Production refusée sans --confirm-production I_CONFIRM_PRODUCTION_MEDIA_MOVE.")
    inspector = Inspector(token, args.timeout)
    journal = {
        "format": "izilife-media-move-apply-v1",
        "plan": str(plan_path),
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
        "applied_at": datetime.now().isoformat(),
        "media": [],
        "source_closed": False,
    }
    failed = False
    for media in plan.get("media") or []:
        if media.get("action") != "COPY":
            journal["media"].append({"source_id": media.get("source_id"), "status": media.get("action")})
            continue
        try:
            content, mime, filename = inspector.download_media(
                source["env"], source["type"], source["ref"], int(media["source_id"])
            )
            actual = hashlib.sha1(content).hexdigest()
            expected = normalize(media.get("sha1_hash")).lower()
            if expected and actual.lower() != expected:
                raise RuntimeError(f"SHA-1 source différent ({actual} != {expected})")
            uploaded = inspector.upload_media(
                destination["env"], destination["type"], destination["ref"], media,
                content, mime, filename,
            )
            check, _, _ = inspector.download_media(
                destination["env"], destination["type"], destination["ref"], int(uploaded["media_id"])
            )
            if hashlib.sha1(check).hexdigest() != actual:
                raise RuntimeError("Contrôle SHA-1 destination différent après copie")
            journal["media"].append({"source_id": media["source_id"], "status": "COPIED_VERIFIED", "sha1": actual, "result": uploaded})
        except Exception as exc:
            failed = True
            journal["media"].append({"source_id": media.get("source_id"), "status": "ERROR", "error": str(exc)})
    if plan.get("close_source_after_verified_copy"):
        if failed:
            journal["close_error"] = "Fermeture refusée car au moins une copie média a échoué."
        elif source["env"] != destination["env"]:
            journal["close_error"] = "Fermeture refusée entre environnements différents; fermer explicitement la fiche dans son environnement."
            failed = True
        elif source["type"] not in {"PLACE", "SHOP"}:
            journal["close_error"] = "Fermeture disponible uniquement pour PLACE/SHOP."
            failed = True
        else:
            result = inspector.post(source["env"], LOCATION_MAINTENANCE_ENDPOINT, {
                "scope_type": source["type"], "scope_ref": source["ref"],
                "closed_state_ref": "ferme-definitivement", "is_active": "0", "listable": "0",
            })
            if not result.get("success"):
                failed = True
                journal["close_error"] = result.get("error") or "Fermeture source échouée"
            else:
                journal["source_closed"] = True
                journal["close_result"] = result
    output = Path(args.journal or plan_path.with_name(f"media-move-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")).resolve()
    output.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Journal média : {output}")
    return 2 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synchronisation sélective de la curation iziLife")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Audit strictement en lecture seule des backends")
    audit.add_argument("--workbook", required=True)
    audit.add_argument("--envs", nargs="+", choices=list(ENVIRONMENTS), default=["local", "staging", "prod"])
    audit.add_argument("--scope", action="append", help="Limiter à un ou plusieurs SCOPE_KEY")
    audit.add_argument("--timeout", type=int, default=60)
    audit.add_argument("--json-report")
    audit.set_defaults(func=run_audit)
    prepare = sub.add_parser("prepare-local", help="Ajoute toutes les Place/Shop locales ayant un google_place_id")
    prepare.add_argument("--workbook", required=True)
    prepare.add_argument("--timeout", type=int, default=60)
    prepare.set_defaults(func=run_prepare_local)
    prepare_env = sub.add_parser("prepare-env", help="Fusionne l'inventaire d'un environnement dans CIBLES")
    prepare_env.add_argument("--workbook", required=True)
    prepare_env.add_argument("--env", required=True, choices=list(ENVIRONMENTS))
    prepare_env.add_argument("--include-unmatched-prod", action="store_true", help="Ajoute aussi les fiches uniquement présentes en production")
    prepare_env.add_argument("--timeout", type=int, default=60)
    prepare_env.set_defaults(func=run_prepare_environment)
    reconcile = sub.add_parser("reconcile-report", help="Recopie les correspondances certaines d'un rapport d'audit dans CIBLES")
    reconcile.add_argument("--workbook", required=True)
    reconcile.add_argument("--report", required=True)
    reconcile.add_argument("--env", required=True, choices=list(ENVIRONMENTS))
    reconcile.add_argument("--authorize-missing-prod", action="store_true", help="Passe à OUI les créations prod absentes, actives, listables, non fermées et dotées d'un Google Place ID")
    reconcile.set_defaults(func=run_reconcile_report)
    plan = sub.add_parser("plan", help="Construit un plan différentiel sans écriture")
    plan.add_argument("--workbook", required=True)
    plan.add_argument("--env", required=True, choices=["local","staging","prod"])
    plan.add_argument("--output", required=True)
    plan.add_argument("--scope", action="append")
    plan.add_argument("--allow-create", action="store_true", help="Autorise CREATE_COMPLETE; en prod ALLOW_CREATE_PROD doit aussi valoir OUI")
    plan.add_argument("--timeout", type=int, default=90)
    plan.set_defaults(func=run_plan)
    apply_cmd = sub.add_parser("apply", help="Applique un plan figé et transfère les médias")
    apply_cmd.add_argument("--plan", required=True)
    apply_cmd.add_argument("--confirm", required=True)
    apply_cmd.add_argument("--confirm-production")
    apply_cmd.add_argument("--journal")
    apply_cmd.add_argument("--timeout", type=int, default=180)
    apply_cmd.set_defaults(func=run_apply)
    verify = sub.add_parser("verify", help="Relit les cibles après application")
    verify.add_argument("--plan", required=True)
    verify.add_argument("--timeout", type=int, default=90)
    verify.set_defaults(func=run_verify)
    media_plan = sub.add_parser("media-move-plan", help="Planifie la copie des médias d'une fiche vers une autre sans écriture")
    media_plan.add_argument("--source-env", required=True, choices=list(ENVIRONMENTS))
    media_plan.add_argument("--source-type", required=True, choices=["PLACE", "SHOP"])
    media_plan.add_argument("--source-ref", required=True)
    media_plan.add_argument("--destination-env", required=True, choices=list(ENVIRONMENTS))
    media_plan.add_argument("--destination-type", required=True, choices=["PLACE", "SHOP"])
    media_plan.add_argument("--destination-ref", required=True)
    media_plan.add_argument("--close-source", action="store_true", help="Prévoit la fermeture après copie vérifiée, uniquement dans le même environnement")
    media_plan.add_argument("--output", required=True)
    media_plan.add_argument("--timeout", type=int, default=90)
    media_plan.set_defaults(func=run_media_move_plan)
    media_apply = sub.add_parser("media-move-apply", help="Applique un plan média figé et vérifie chaque fichier")
    media_apply.add_argument("--plan", required=True)
    media_apply.add_argument("--confirm", required=True)
    media_apply.add_argument("--confirm-production")
    media_apply.add_argument("--journal")
    media_apply.add_argument("--timeout", type=int, default=180)
    media_apply.set_defaults(func=run_media_move_apply)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
