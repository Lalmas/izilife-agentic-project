#!/usr/bin/env python3
"""Point d'entrée unique des paquets de curation issus de sites complexes.

Le lanceur détecte le contrat JSON puis délègue au moteur spécialisé :

- izilife.site_content.v1 : Services, EAP, Products et Equipment ;
- izilife.experience_site.v1 : Equipment, objets de lieu, Experiences,
  EAP, médias et séances ;
- izilife.circuit_site.v1 : Circuit, tracé GeoJSON et étapes ;
- izi.event.package.v1 : Event, EventSerie/AnnualCelebration racine, éditions,
  médias, organisateurs, sources et programmations ;
- izilife.site_bundle.v1 : liste ordonnée de plusieurs paquets.

Il ne collecte aucune page et n'appelle aucun LLM. Une écriture exige toujours
un environnement explicite et ``--confirm-write``.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
ENGINES = {
    "izilife.site_content.v1": ROOT / "places" / "site_content_package.py",
    "izilife.experience_site.v1": ROOT / "experiences" / "site_experience_package.py",
    "izilife.circuit_site.v1": ROOT / "circuits" / "site_circuit_package.py",
    "izi.event.package.v1": ROOT / "events" / "site_event_package.py",
    "izilife.location_package.v1": ROOT / "places" / "location_package.py",
}
BUNDLE_SCHEMA = "izilife.site_bundle.v1"


def _read(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Paquet illisible {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Paquet invalide {path}: objet JSON attendu")
    return value


def _package_paths(path: Path, package: dict) -> list[Path]:
    schema = package.get("schema_version")
    if schema != BUNDLE_SCHEMA:
        if schema not in ENGINES:
            raise RuntimeError(f"schema_version non pris en charge dans {path}: {schema!r}")
        return [path]

    entries = package.get("packages")
    if not isinstance(entries, list) or not entries:
        raise RuntimeError(f"Bundle invalide {path}: packages doit être une liste non vide")
    result = []
    for number, entry in enumerate(entries, 1):
        relative = entry.get("file") if isinstance(entry, dict) else entry
        if not isinstance(relative, str) or not relative.strip():
            raise RuntimeError(f"Bundle {path}, packages[{number}]: file requis")
        child = (path.parent / relative).resolve()
        if not child.is_file():
            raise RuntimeError(f"Bundle {path}, packages[{number}]: fichier absent {child}")
        child_schema = _read(child).get("schema_version")
        if child_schema not in ENGINES:
            raise RuntimeError(
                f"Bundle {path}, packages[{number}]: schéma non pris en charge {child_schema!r}"
            )
        result.append(child)
    return result


def _engine(path: Path) -> tuple[str, Path, dict]:
    package = _read(path)
    schema = package.get("schema_version")
    engine = ENGINES.get(schema)
    if engine is None:
        raise RuntimeError(f"Schéma non pris en charge dans {path}: {schema!r}")
    return schema, engine, package


def _run(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode:
        raise RuntimeError(f"Commande en échec ({completed.returncode}): {' '.join(command)}")


def _content_plan(path: Path, package: dict) -> None:
    objects = package.get("objects") if isinstance(package.get("objects"), list) else []
    kinds = Counter(str(row.get("kind")) for row in objects if isinstance(row, dict))
    statuses = Counter(str(row.get("review_status")) for row in objects if isinstance(row, dict))
    media = sum(
        len(row.get("media") or [])
        for row in objects
        if isinstance(row, dict) and isinstance(row.get("media") or [], list)
    )
    print(json.dumps({
        "file": str(path),
        "target": package.get("target"),
        "objects": len(objects),
        "kinds": dict(sorted(kinds.items())),
        "review_statuses": dict(sorted(statuses.items())),
        "media": media,
    }, ensure_ascii=False, indent=2))


def _content_issues(package: dict) -> list[str]:
    """Valide le contrat de contenu sans charger le client HTTP historique."""
    problems = []
    target = package.get("target") or {}
    if target.get("scope_type") not in {"PLACE", "SHOP"} or not target.get("scope_ref"):
        problems.append("target: PLACE/SHOP et scope_ref requis")
    objects = package.get("objects")
    if not isinstance(objects, list):
        return problems + ["objects doit être une liste"]
    allowed_kinds = {"element_service", "eap", "product", "equipment"}
    allowed_statuses = {"pending", "needs_review", "approved", "excluded"}
    for number, row in enumerate(objects, 1):
        prefix = f"objects[{number}]"
        if not isinstance(row, dict):
            problems.append(f"{prefix}: objet JSON attendu")
            continue
        item = row.get("item")
        if row.get("kind") not in allowed_kinds or not isinstance(item, dict) or not str(item.get("name") or "").strip():
            problems.append(f"{prefix}: kind ou item.name invalide")
        if row.get("review_status") not in allowed_statuses:
            problems.append(f"{prefix}: review_status invalide")
        source = urlparse(str(row.get("source_url") or ""))
        if source.scheme not in {"http", "https"} or not source.netloc:
            problems.append(f"{prefix}: source_url HTTP(S) requise")
        if row.get("kind") == "equipment" and isinstance(item, dict):
            if not str(item.get("category_ref") or "").strip():
                problems.append(f"{prefix}: category_ref Equipment requis")
            instances = item.get("instances") or []
            if not isinstance(instances, list):
                problems.append(f"{prefix}: instances Equipment doit être une liste")
            else:
                codes = []
                for position, instance in enumerate(instances, 1):
                    if not isinstance(instance, dict):
                        problems.append(f"{prefix}: instances[{position}] doit être un objet")
                        continue
                    code = str(instance.get("instance_code") or "").strip()
                    if not code:
                        problems.append(f"{prefix}: instances[{position}].instance_code requis")
                    else:
                        codes.append(code)
                if len(codes) != len(set(codes)):
                    problems.append(f"{prefix}: instance_code Equipment dupliqué")
        media = row.get("media") or []
        if not isinstance(media, list):
            problems.append(f"{prefix}: media doit être une liste")
    return problems


def _delegate(command: str, path: Path, env: str | None,
              confirm_write: bool, target_ref_override: str | None,
              confirm_production: str | None) -> None:
    schema, engine, package = _engine(path)
    if schema == "izilife.site_content.v1" and command in {"validate", "plan"}:
        # Ces commandes restent sans dépendance HTTP ni chargement de `requests`.
        problems = _content_issues(package)
        print(json.dumps({"file": str(path), "objects": len(package.get("objects") or []),
                          "issues": problems}, ensure_ascii=False, indent=2))
        if problems:
            raise RuntimeError(f"Paquet invalide {path}")
        if command == "validate":
            return
        _content_plan(path, package)
        return

    engine_command = command
    if command == "media-only" and schema != "izilife.site_content.v1":
        raise RuntimeError("media-only est réservé aux paquets izilife.site_content.v1")

    args = [sys.executable, str(engine)]
    if schema == "izilife.site_content.v1":
        args += [engine_command, "--file", str(path)]
    else:
        args += [engine_command, "--file", str(path)]

    if command in {"apply", "media-only"}:
        if not env or not confirm_write:
            raise RuntimeError("Écriture : --env explicite et --confirm-write requis")
        args += ["--env", env, "--confirm-write"]
        if env == "prod" and schema == "izi.event.package.v1":
            args += ["--confirm-production", confirm_production or ""]
        if target_ref_override:
            if schema != "izilife.experience_site.v1":
                raise RuntimeError("--target-ref-override est réservé aux paquets Experience")
            args += ["--target-ref-override", target_ref_override]
    elif command == "dry-run":
        if schema != "izi.event.package.v1" or not env:
            raise RuntimeError("dry-run est réservé au package Event et exige --env")
        args += ["--env", env]
    _run(args)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "plan", "dry-run", "apply", "media-only"])
    parser.add_argument("--file", required=True, type=Path,
                        help="Paquet JSON ou manifeste izilife.site_bundle.v1")
    parser.add_argument("--env", choices=["local", "staging", "prod"])
    parser.add_argument("--confirm-write", action="store_true")
    parser.add_argument("--confirm-production")
    parser.add_argument("--target-ref-override",
                        help="Cible de test locale d'un paquet Experience")
    args = parser.parse_args()

    source = args.file.resolve()
    package = _read(source)
    paths = _package_paths(source, package)
    if args.target_ref_override and len(paths) != 1:
        raise SystemExit("--target-ref-override exige un paquet unique")

    try:
        for number, path in enumerate(paths, 1):
            if len(paths) > 1:
                print(json.dumps({"package": number, "total": len(paths), "file": str(path)},
                                 ensure_ascii=False))
            _delegate(args.command, path, args.env, args.confirm_write,
                      args.target_ref_override, args.confirm_production)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
