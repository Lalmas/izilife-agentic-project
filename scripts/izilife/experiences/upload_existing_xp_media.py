#!/usr/bin/env python3
"""Upload verified local media to existing Experiences through the token endpoint."""
from __future__ import annotations

import argparse
import json
import mimetypes
from pathlib import Path

from site_experience_package import izilife_post


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=("local", "staging", "prod"), required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True,
                        help="JSON objet {experience_string_id: fichier_local}")
    parser.add_argument("--confirm-write", action="store_true")
    args = parser.parse_args()
    if not args.confirm_write:
        raise SystemExit("--confirm-write requis")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise SystemExit("manifest JSON invalide")
    results = []
    for scope_ref, filename in manifest.items():
        path = (args.directory / str(filename)).resolve()
        if not path.is_relative_to(args.directory.resolve()) or not path.is_file():
            raise SystemExit(f"média absent ou hors dossier: {filename}")
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        values = {
            "scope_type": "EXPERIENCE",
            "scope_ref": str(scope_ref),
            "destination_id": "",
            "belongs_to_scope": "oui",
            "rights_confirmed": "oui",
            "is_principal": "oui",
            "title": f"Illustration officielle {scope_ref}",
            "media_source": "getyourguide",
        }
        with path.open("rb") as handle:
            result = izilife_post(
                "/scraper/agentAddScopedMedia", values, args.env, timeout=240,
                files={"media": (path.name, handle, mime)},
            )
        results.append((scope_ref, result))
        print(scope_ref, "OK" if result.get("success") else result)
    return 0 if all(result.get("success") for _, result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
