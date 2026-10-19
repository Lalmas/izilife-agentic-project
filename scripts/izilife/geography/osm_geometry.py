from __future__ import annotations
import json
import urllib.parse
import urllib.request

_CACHE: dict[str, str] = {}

def enrich(payload: dict) -> dict:
    refs = str(payload.get("osm_refs") or "").strip()
    if not refs or payload.get("geometry_geojson"):
        return payload
    if refs in _CACHE:
        payload["geometry_geojson"] = _CACHE[refs]
        return payload
    osm_ids = []
    for raw in refs.replace(";", ",").split(","):
        raw = raw.strip()
        if not raw:
            continue
        kind, separator, identifier = raw.partition(":")
        prefixes = {"node":"N", "way":"W", "relation":"R"}
        if not separator or kind.lower() not in prefixes or not identifier.isdigit():
            raise ValueError(f"Référence OSM invalide: {raw} (attendu way:123, relation:456 ou node:789)")
        osm_ids.append(prefixes[kind.lower()] + identifier)
    if not osm_ids:
        return payload
    query = urllib.parse.urlencode({"osm_ids": ",".join(osm_ids), "format":"jsonv2", "polygon_geojson":1})
    request = urllib.request.Request("https://nominatim.openstreetmap.org/lookup?" + query, headers={"User-Agent":"iziLife-agent/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        rows = json.load(response)
    geometries = [row.get("geojson") for row in rows if isinstance(row.get("geojson"), dict)]
    if len(geometries) != len(osm_ids):
        raise ValueError(f"OSM n'a retourné que {len(geometries)} géométrie(s) pour {len(osm_ids)} référence(s).")
    geometry = _merge(geometries)
    encoded = json.dumps(geometry, ensure_ascii=False, separators=(",", ":"))
    _CACHE[refs] = encoded
    payload["geometry_geojson"] = encoded
    payload.setdefault("geometry_source_provider", "OSM")
    return payload

def _merge(geometries: list[dict]) -> dict:
    if len(geometries) == 1:
        return geometries[0]
    types = {str(g.get("type")) for g in geometries}
    if types <= {"LineString", "MultiLineString"}:
        lines = []
        for geometry in geometries:
            coordinates = geometry["coordinates"]
            lines.extend(coordinates if geometry["type"] == "MultiLineString" else [coordinates])
        return {"type":"MultiLineString", "coordinates":lines}
    if types <= {"Polygon", "MultiPolygon"}:
        polygons = []
        for geometry in geometries:
            coordinates = geometry["coordinates"]
            polygons.extend(coordinates if geometry["type"] == "MultiPolygon" else [coordinates])
        return {"type":"MultiPolygon", "coordinates":polygons}
    raise ValueError("Les références OSM ne forment pas une géométrie homogène.")
