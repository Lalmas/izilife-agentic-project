#!/usr/bin/env python3
"""Valide, planifie et soumet un circuit extrait d'un site officiel.

La collecte reste séparée de l'import : ``validate`` et ``plan`` ne font
aucune requête externe. ``apply`` exige un GeoJSON local déjà collecté et
crée une demande de validation BO via l'entrée générique Scraper.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

SCHEMA = "izilife.circuit_site.v1"


def _http_url(value: object) -> bool:
    parsed = urlparse(str(value or ""))
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _read(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("Objet JSON attendu")
    return value


def _geometry_file(package_path: Path, package: dict) -> Path | None:
    route = package.get("route") or {}
    local_file = str(route.get("local_file") or "").strip()
    return (package_path.parent / local_file).resolve() if local_file else None


def _point_count(value: object) -> int:
    if not isinstance(value, dict):
        return 0
    if value.get("type") == "FeatureCollection":
        return sum(_point_count(row) for row in value.get("features") or [])
    if value.get("type") == "Feature":
        return _point_count(value.get("geometry"))
    coordinates = value.get("coordinates")
    if value.get("type") == "Point":
        return 1 if isinstance(coordinates, list) else 0
    if value.get("type") == "LineString":
        return len(coordinates or [])
    if value.get("type") == "MultiLineString":
        return sum(len(line or []) for line in coordinates or [])
    return 0


def issues(package_path: Path, package: dict) -> list[str]:
    problems: list[str] = []
    if package.get("schema_version") != SCHEMA:
        problems.append("schema_version incorrect")
    circuit = package.get("circuit")
    if not isinstance(circuit, dict):
        return problems + ["circuit doit être un objet"]
    for field in ("title", "circuit_string_id", "circuit_type_string_id", "city_string_id"):
        if not str(circuit.get(field) or "").strip():
            problems.append(f"circuit.{field} requis")
    if circuit.get("review_status") not in {"pending", "needs_review", "approved", "excluded"}:
        problems.append("circuit.review_status invalide")
    if not _http_url(circuit.get("source_url")):
        problems.append("circuit.source_url HTTP(S) requise")
    steps = circuit.get("steps")
    if not isinstance(steps, list) or not steps:
        problems.append("circuit.steps doit être une liste non vide")
    else:
        for number, step in enumerate(steps, 1):
            if not isinstance(step, dict) or not str(step.get("title") or "").strip():
                problems.append(f"circuit.steps[{number}].title requis")
                continue
            if step.get("object_type", "manual_point") not in {
                "place", "shop", "equipment", "event", "experience", "art_piece", "manual_point"
            }:
                problems.append(f"circuit.steps[{number}].object_type invalide")
            for field in ("latitude", "longitude"):
                try:
                    float(step.get(field))
                except (TypeError, ValueError):
                    problems.append(f"circuit.steps[{number}].{field} invalide")
    route = package.get("route")
    if not isinstance(route, dict) or route.get("format") != "geojson":
        problems.append("route.format=geojson requis")
    else:
        if not _http_url(route.get("source_url")):
            problems.append("route.source_url HTTP(S) requise")
        path = _geometry_file(package_path, package)
        if path is None or not path.is_file():
            problems.append(f"route.local_file absent: {path}")
        else:
            try:
                geometry = _read(path)
                if geometry.get("type") not in {"Feature", "FeatureCollection", "LineString", "MultiLineString"}:
                    problems.append("route.local_file ne contient pas un GeoJSON de tracé")
            except (OSError, json.JSONDecodeError, RuntimeError) as exc:
                problems.append(f"route.local_file invalide: {exc}")
    return problems


def plan(package_path: Path, package: dict) -> dict:
    geometry_path = _geometry_file(package_path, package)
    geometry = _read(geometry_path) if geometry_path and geometry_path.is_file() else {}
    animals = package.get("observed_animals") if isinstance(package.get("observed_animals"), list) else []
    statuses: dict[str, int] = {}
    for row in animals:
        status = str(row.get("review_status") or "") if isinstance(row, dict) else "invalid"
        statuses[status] = statuses.get(status, 0) + 1
    return {
        "file": str(package_path),
        "circuit": package.get("circuit", {}).get("title"),
        "review_status": package.get("circuit", {}).get("review_status"),
        "steps": len(package.get("circuit", {}).get("steps") or []),
        "route_points": _point_count(geometry),
        "observed_animals": len(animals),
        "animal_review_statuses": statuses,
        "writes": False,
    }


def apply(package_path: Path, package: dict, env: str) -> dict:
    # Le client HTTP historique charge requests/openpyxl. Le chargement reste
    # volontairement tardif pour que validate/plan fonctionnent sans ces deps.
    import sys
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from objects.object_agent_common import izilife_post, load_env, normalize_env

    errors = issues(package_path, package)
    if errors:
        raise RuntimeError("Paquet invalide:\n" + "\n".join(errors))
    circuit = package["circuit"]
    if circuit["review_status"] != "approved":
        raise RuntimeError("Le circuit doit être approved avant soumission")
    geometry_path = _geometry_file(package_path, package)
    geometry = _read(geometry_path)
    fields = {
        "title": circuit["title"],
        "circuit_string_id": circuit["circuit_string_id"],
        "circuit_type_string_id": circuit["circuit_type_string_id"],
        "circuit_theme_string_id": circuit.get("circuit_theme_string_id"),
        "sport_circuit_type_string_id": circuit.get("sport_circuit_type_string_id"),
        "city_string_id": circuit["city_string_id"],
        "description": circuit.get("description"),
        "distance": circuit.get("distance_km"),
        "distance_measurement_unity_string_id": "km",
        "duration": circuit.get("duration_minutes"),
        "duration_measurement_unity_string_id": "m",
        "is_loop": 1 if circuit.get("is_loop") else 0,
        "route_shape_type": "geojson",
        "route_geometry": json.dumps(geometry, ensure_ascii=False, separators=(",", ":")),
        "route_point_count": _point_count(geometry),
        "route_source_url": package["route"]["source_url"],
        "start_address": circuit.get("start_address"),
        "start_longitude": circuit.get("start_longitude"),
        "start_latitude": circuit.get("start_latitude"),
        "source_name": circuit.get("source_name") or "site-officiel",
        "source_url": circuit["source_url"],
        "source_image_url": circuit.get("source_image_url"),
        "external_id": str(circuit.get("external_id") or "") or None,
        "steps": circuit["steps"],
    }
    payload = {"type": "circuit", "source": "site-circuit-package", "fields": fields}
    load_env()
    response = izilife_post(
        "/scraper/agentIngestJson",
        {"payload": json.dumps(payload, ensure_ascii=False)},
        normalize_env(env),
        timeout=180,
    )
    if not response.get("success"):
        raise RuntimeError(str(response.get("error") or response))
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "plan", "apply"])
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--env", choices=["local", "staging", "prod"])
    parser.add_argument("--confirm-write", action="store_true")
    args = parser.parse_args()

    package_path = args.file.resolve()
    package = _read(package_path)
    errors = issues(package_path, package)
    if args.command == "validate":
        print(json.dumps({"file": str(package_path), "issues": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1 if errors else 0)
    if errors:
        raise SystemExit("Paquet invalide:\n" + "\n".join(errors))
    if args.command == "plan":
        print(json.dumps(plan(package_path, package), ensure_ascii=False, indent=2))
        return
    if not args.env or not args.confirm_write:
        raise SystemExit("Écriture : --env explicite et --confirm-write requis")
    print(json.dumps(apply(package_path, package, args.env), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
