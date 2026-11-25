#!/usr/bin/env python3
"""Import JSON vérifié d'un équipement, d'expériences, EAP, médias et séances.

`validate` et `plan` n'appellent aucune API. `apply` écrit uniquement avec
--confirm-write et --env explicites ; les expériences et séances restent inactives.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import ssl
import sys
import uuid
from datetime import date
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

SCHEMA = "izilife.experience_site.v1"
BASE_URLS = {
    "local": ("IZILIFE_LOCAL_URL", "https://localhost:4443/izilife-admin"),
    "staging": ("IZILIFE_STAGING_URL", "https://www.staging.izilife.co/izilife-admin"),
    "prod": ("IZILIFE_PROD_URL", "https://www.izilife.co/izilife-admin"),
}


def load_env() -> str:
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN absent du processus")
    return token


def izilife_post(path: str, payload: dict, env: str, timeout: int = 120,
                 files: dict | None = None) -> dict:
    token = load_env()
    variable, default = BASE_URLS[env]
    url = os.getenv(variable, default).rstrip("/") + path
    headers = {"X-Agent-Token": token, "Accept": "application/json"}
    if files:
        boundary = "izilife-" + uuid.uuid4().hex
        parts = []
        for key, value in payload.items():
            parts.append((f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n").encode())
        for key, (filename, handle, mime) in files.items():
            parts.append((f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"; filename=\"{filename}\"\r\nContent-Type: {mime}\r\n\r\n").encode())
            parts.append(handle.read())
            parts.append(b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        body = b"".join(parts)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    else:
        body = urlencode(payload).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = Request(url, data=body, headers=headers, method="POST")
    context = ssl._create_unverified_context() if env == "local" else None
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        try:
            return json.loads(exc.read().decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {"success": False, "error": f"HTTP {exc.code}"}


def _url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _media_path(package_file: Path, media: dict) -> Path:
    relative = Path(str(media.get("local_file", "")))
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError("local_file doit être relatif au paquet")
    path = (package_file.parent / relative).resolve()
    if not path.is_relative_to(package_file.parent.resolve()):
        raise ValueError("local_file sort du répertoire du paquet")
    return path


def validate(package: dict, package_file: Path, require_files: bool = False) -> list[str]:
    errors = []
    if package.get("schema_version") != SCHEMA:
        errors.append("schema_version invalide")
    target = package.get("target") or {}
    if target.get("scope_type") not in {"PLACE", "SHOP"} or not target.get("scope_ref"):
        errors.append("target PLACE/SHOP et scope_ref requis")
    equipment = package.get("equipment")
    if equipment:
        for field in ("name", "internal_id", "category_ref"):
            if not equipment.get(field):
                errors.append(f"equipment.{field} requis")
    experiences = package.get("experiences")
    if not isinstance(experiences, list) or not experiences:
        return errors + ["experiences non vide requis"]
    for index, eap in enumerate(package.get("venue_eaps") or [], 1):
        if not eap.get("name") or eap.get("price") is None or not eap.get("access_type_ref") or not eap.get("price_model_ref"):
            errors.append(f"venue_eaps[{index}] incomplet")
    refs = set()
    for number, entry in enumerate(experiences, 1):
        prefix = f"experiences[{number}]"
        payload = entry.get("item") or {}
        for field in ("title", "experience_string_id", "city_ref", "description", "duration",
                      "experience_type_ref", "access_type_ref", "place_ref"):
            if not payload.get(field):
                errors.append(f"{prefix}.item.{field} requis")
        ref = payload.get("experience_string_id")
        if ref in refs:
            errors.append(f"{prefix}: experience_string_id dupliqué")
        refs.add(ref)
        if not _url(str(entry.get("source_url") or "")):
            errors.append(f"{prefix}.source_url HTTPS requis")
        for index, eap in enumerate(entry.get("eaps") or [], 1):
            for field in ("name", "price", "access_type_ref", "price_model_ref"):
                if eap.get(field) is None or eap.get(field) == "":
                    errors.append(f"{prefix}.eaps[{index}].{field} requis")
            try:
                if float(eap.get("price", -1)) < 0:
                    raise ValueError()
            except (ValueError, TypeError):
                errors.append(f"{prefix}.eaps[{index}].price invalide")
        for index, session in enumerate(entry.get("sessions") or [], 1):
            try:
                start = date.fromisoformat(session["start_date"])
                end = date.fromisoformat(session["end_date"])
                if start > end or not session.get("name"):
                    raise ValueError()
                for content in session["contents"]:
                    if not content.get("days") or not content.get("hours"):
                        raise ValueError()
                    if any(int(day) not in range(1, 8) for day in content["days"]):
                        raise ValueError()
            except (KeyError, ValueError, TypeError):
                errors.append(f"{prefix}.sessions[{index}] invalide")
    all_media = (equipment or {}).get("media", []) + [m for x in experiences for m in x.get("media", [])]
    for number, media in enumerate(all_media, 1):
        if not _url(str(media.get("source_url") or "")):
            errors.append(f"media[{number}].source_url HTTPS requis")
        try:
            file_path = _media_path(package_file, media)
            if require_files and not file_path.is_file():
                errors.append(f"media[{number}] absent: {file_path}")
        except ValueError as exc:
            errors.append(f"media[{number}]: {exc}")
    return errors


def _post(path: str, payload: dict, env: str) -> dict:
    result = izilife_post(path, {"payload": json.dumps(payload, ensure_ascii=False)}, env, timeout=180)
    if not result.get("success"):
        raise RuntimeError(f"{path}: {result.get('error', result)}")
    return result


def _upload(package_file: Path, media: dict, scope_type: str, scope_ref: str,
            env: str, destination_id: int | None = None) -> dict:
    path = _media_path(package_file, media)
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    values = {
        "scope_type": scope_type,
        "scope_ref": scope_ref if destination_id is None else "",
        "destination_id": str(destination_id or ""),
        "belongs_to_scope": "oui",
        "rights_confirmed": "oui",
        "is_principal": "oui" if media.get("role") == "cover" else "non",
        "title": media.get("title") or path.stem,
    }
    with path.open("rb") as handle:
        result = izilife_post("/scraper/agentAddScopedMedia", values, env, timeout=240,
                              files={"media": (path.name, handle, content_type)})
    if not result.get("success"):
        raise RuntimeError(f"média {path.name}: {result.get('error', result)}")
    return result


def apply(package: dict, package_file: Path, env: str, target_ref_override: str | None = None) -> list[dict]:
    problems = validate(package, package_file, require_files=True)
    if problems:
        raise RuntimeError("Paquet invalide: " + "; ".join(problems))
    load_env()
    target = package["target"]
    scope_type, scope_ref = target["scope_type"], target_ref_override or target["scope_ref"]
    parent = izilife_post("/scraper/agentGetPlaceByStringId",
                          {"string_id": scope_ref, "entity_type": scope_type}, env, timeout=60)
    if not parent.get("success"):
        raise RuntimeError(f"Fiche cible introuvable: {scope_type}/{scope_ref}")
    journal = []
    equipment = package.get("equipment")
    if equipment:
        item = {key: value for key, value in equipment.items() if key != "media"}
        item.update({"scope_type": scope_type, "scope_ref": scope_ref, "preserve_existing": 1})
        result = _post("/scraper/agentUpsertEquipment", item, env)
        journal.append({"kind": "equipment", "ref": item["internal_id"], "result": result})
        if package.get("object_on_public_place_ref"):
            if scope_type != "PLACE":
                raise RuntimeError("ObjectOnPublicPlace exige une cible PLACE")
            link = {"scope_type": "PLACE", "scope_ref": scope_ref, "operation": "ADD",
                    "editorial": {"ObjectOnPublicPlace": [package["object_on_public_place_ref"]]}}
            journal.append({"kind": "place_object", "result": _post("/scraper/agentApplyTagsAndCharacts", link, env)})
        for media in equipment.get("media", []):
            journal.append({"kind": "equipment_media", "ref": item["internal_id"],
                            "result": _upload(package_file, media, "EQUIPMENT", "", env,
                                              int(result["equipment_id"]))})
    for eap in package.get("venue_eaps") or []:
        price = dict(eap, is_active=0, need_to_be_confirmed_manually=1, preserve_existing=1)
        payload = {"kind": "eap", "scope_type": scope_type, "scope_ref": scope_ref,
                   "source_url": package.get("source_url"), "item": price}
        journal.append({"kind": "venue_eap", "name": price["name"],
                        "result": _post("/scraper/agentIngestSiteItem", payload, env)})
    for entry in package["experiences"]:
        item = dict(entry["item"])
        if target_ref_override and item.get("place_ref") == target["scope_ref"]:
            item["place_ref"] = target_ref_override
        item["source_url"] = entry["source_url"]
        item["source"] = "SITE_EXPERIENCE_PACKAGE"
        item["additional_image_urls"] = [
            media["source_url"] for media in entry.get("media", []) if media.get("source_url")
        ][:2]
        item["eaps"] = [
            dict(eap, is_active=0, need_to_be_confirmed_manually=1)
            for eap in entry.get("eaps", [])
        ]
        item["session_packages"] = []
        for session in entry.get("sessions", []):
            item["session_packages"].append({
                "session_configuration": {
                    "name": session.get("name") or "Sessions extraites",
                    "start_date": session.get("start_date"),
                    "end_date": session.get("end_date"),
                },
                "session_contents": [
                    {
                        "day_list": content.get("days") or [],
                        "hour_list": content.get("hours") or [],
                        "repetition_type": "FIXED_HOURS",
                    }
                    for content in session.get("contents", [])
                ],
                "session_warnings": [],
            })
        ref = item["experience_string_id"]
        journal.append({"kind": "experience", "ref": ref,
                        "result": _post("/scraper/agentStageExperience", item, env)})
    return journal


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "plan", "apply"])
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--env", choices=["local", "staging", "prod"])
    parser.add_argument("--confirm-write", action="store_true")
    parser.add_argument("--target-ref-override", help="Référence d'une fiche de test locale uniquement")
    args = parser.parse_args()
    package = json.loads(args.file.read_text(encoding="utf-8"))
    problems = validate(package, args.file, require_files=args.command == "apply")
    if problems:
        raise SystemExit("\n".join(problems))
    if args.command == "validate":
        print("Paquet valide :", len(package["experiences"]), "expériences")
    elif args.command == "plan":
        equipment_scoped_eaps = sum(
            1 for eap in package.get("venue_eaps") or [] if eap.get("equipment_refs")
        )
        experiences_on_equipment = sum(
            1 for entry in package["experiences"] if (entry.get("item") or {}).get("equipment_ref")
        )
        print(json.dumps({"target": package["target"], "equipment": bool(package.get("equipment")),
                          "experiences": len(package["experiences"]),
                          "eaps": sum(len(x.get("eaps", [])) for x in package["experiences"]),
                          "venue_eaps": len(package.get("venue_eaps") or []),
                          "equipment_scoped_eaps": equipment_scoped_eaps,
                          "experiences_on_equipment": experiences_on_equipment,
                          "sessions": sum(len(x.get("sessions", [])) for x in package["experiences"]),
                          "medias": len((package.get("equipment") or {}).get("media", [])) +
                          sum(len(x.get("media", [])) for x in package["experiences"])}, indent=2))
    else:
        if not args.env or not args.confirm_write:
            raise SystemExit("Écriture : --env explicite et --confirm-write requis")
        if args.target_ref_override and args.env != "local":
            raise SystemExit("--target-ref-override est réservé à --env local")
        journal = apply(package, args.file, args.env, args.target_ref_override)
        print(json.dumps(journal, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
