#!/usr/bin/env python3
"""Copie sans réutiliser les IDs les médias de représentations entre environnements iziLife."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

import requests


ENVIRONMENTS = {
    "local": {"base_url": "https://localhost:4443/izilife-admin", "verify": False},
    "staging": {"base_url": "https://www.staging.izilife.co/izilife-admin", "verify": True},
    "prod": {"base_url": "https://www.izilife.co/izilife-admin", "verify": True},
}
DEFAULT_REFS = [
    "c-est-decide-je-deviens-une-connasse",
    "normal-n-existe-pas",
    "david-voinson-en-rodage",
    "ben-h-le-mec-en-rose",
    "cheri-on-se-dit-tout",
]


def post_json(env: str, endpoint: str, token: str, payload: dict) -> dict:
    cfg = ENVIRONMENTS[env]
    response = requests.post(
        cfg["base_url"] + endpoint,
        json=payload,
        headers={"X-Agent-Token": token, "Accept": "application/json"},
        timeout=120,
        verify=cfg["verify"],
    )
    try:
        body = response.json()
    except ValueError:
        body = {"success": False, "error": response.text[:500]}
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
    return body


def manifest(env: str, ref: str, token: str) -> list[dict]:
    return post_json(env, "/scraper/agentRepresentationMediaManifest", token, {"scope_ref": ref}).get("items") or []


def download(env: str, ref: str, media_id: int, token: str) -> tuple[bytes, str, str]:
    cfg = ENVIRONMENTS[env]
    response = requests.post(
        cfg["base_url"] + "/scraper/agentCurationSyncMediaDownload",
        json={"scope_type": "REPRESENTATION", "scope_ref": ref, "source_media_id": media_id},
        headers={"X-Agent-Token": token}, timeout=180, verify=cfg["verify"],
    )
    if response.status_code >= 400:
        raise RuntimeError(response.text[:500] or f"HTTP {response.status_code}")
    filename = requests.utils.unquote(response.headers.get("X-Original-Name", f"representation-{media_id}"))
    return response.content, response.headers.get("Content-Type", "application/octet-stream"), filename


def upload(env: str, ref: str, item: dict, content: bytes, mime: str, filename: str, token: str) -> dict:
    cfg = ENVIRONMENTS[env]
    response = requests.post(
        cfg["base_url"] + "/scraper/agentAddScopedMedia",
        data={
            "scope_type": "REPRESENTATION", "scope_ref": ref,
            "belongs_to_scope": "oui", "rights_confirmed": "oui",
            "is_principal": "oui" if int(item.get("is_principal") or 0) else "non",
            "media_role": item.get("media_role") or "gallery",
            "title": item.get("title") or "", "description": item.get("description") or "",
        },
        files={"media": (filename, content, mime)},
        headers={"X-Agent-Token": token, "Accept": "application/json"}, timeout=240, verify=cfg["verify"],
    )
    try:
        body = response.json()
    except ValueError:
        body = {"success": False, "error": response.text[:500]}
    if response.status_code >= 400 or not body.get("success"):
        raise RuntimeError(body.get("error") or f"HTTP {response.status_code}")
    return body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-env", choices=ENVIRONMENTS, default="local")
    parser.add_argument("--destination-env", choices=ENVIRONMENTS, default="prod")
    parser.add_argument("--ref", action="append", dest="refs")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-production")
    parser.add_argument("--journal")
    args = parser.parse_args()
    if args.apply and args.destination_env == "prod" and args.confirm_production != "I_CONFIRM_PRODUCTION_REPRESENTATION_MEDIA":
        raise RuntimeError("Production refusée sans --confirm-production I_CONFIRM_PRODUCTION_REPRESENTATION_MEDIA.")
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("IZILIFE_AGENT_TOKEN manquant.")

    report = {"created_at": datetime.now().isoformat(), "source": args.source_env, "destination": args.destination_env, "apply": args.apply, "representations": {}}
    failed = False
    for ref in args.refs or DEFAULT_REFS:
        entry = {"source": [], "destination_before": [], "operations": []}
        report["representations"][ref] = entry
        try:
            entry["source"] = manifest(args.source_env, ref, token)
            entry["destination_before"] = manifest(args.destination_env, ref, token)
            destination_hashes = {str(x.get("sha1_hash") or "").lower() for x in entry["destination_before"] if x.get("sha1_hash")}
            for item in entry["source"]:
                content = None
                mime = None
                filename = None
                source_hash = str(item.get("sha1_hash") or "").lower()
                if not source_hash:
                    content, mime, filename = download(args.source_env, ref, int(item["source_id"]), token)
                    source_hash = hashlib.sha1(content).hexdigest()
                if source_hash in destination_hashes:
                    entry["operations"].append({"source_id": item["source_id"], "status": "SKIP_DUPLICATE"})
                    continue
                if not args.apply:
                    entry["operations"].append({"source_id": item["source_id"], "status": "WOULD_COPY", "role": item.get("media_role")})
                    continue
                if content is None:
                    content, mime, filename = download(args.source_env, ref, int(item["source_id"]), token)
                actual = hashlib.sha1(content).hexdigest()
                expected = str(item.get("sha1_hash") or "").lower()
                if expected and expected != actual:
                    raise RuntimeError(f"SHA-1 différent pour {ref} media {item['source_id']}")
                result = upload(args.destination_env, ref, item, content, mime, filename, token)
                entry["operations"].append({"source_id": item["source_id"], "status": "COPIED" if result.get("created") else "SKIP_DUPLICATE", "destination_media_id": result.get("media_id"), "sha1": actual, "role": item.get("media_role")})
            if args.apply:
                entry["destination_after"] = manifest(args.destination_env, ref, token)
        except Exception as exc:
            failed = True
            entry["error"] = str(exc)

    output = Path(args.journal or f"journal-representation-media-{args.destination_env}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json").resolve()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Journal : {output}")
    for ref, entry in report["representations"].items():
        print(f"{ref}: source={len(entry['source'])}, opérations={len(entry['operations'])}, erreur={entry.get('error','aucune')}")
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
