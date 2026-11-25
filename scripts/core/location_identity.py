"""Résolution déterministe Place/Shop via l'endpoint partagé iziLife."""
from __future__ import annotations

import os
import requests


def resolve_location(base_url: str, verify_ssl: bool, *, name: str = "",
                     urls: list[str] | None = None, city: str = "") -> dict | None:
    token = os.getenv("IZILIFE_AGENT_TOKEN", "").strip()
    if not token or (not str(name).strip() and not urls):
        return None
    response = requests.post(
        base_url.rstrip("/") + "/scraper/agentLocationIdentityCandidates",
        json={"name": str(name).strip(), "urls": list(urls or []), "city": str(city).strip()},
        headers={"X-Agent-Token": token}, verify=verify_ssl, timeout=30,
    )
    response.raise_for_status()
    candidates = [item for item in response.json().get("candidates", [])
                  if item.get("type") in {"PLACE", "SHOP"}]
    if not candidates:
        return None
    candidates.sort(key=lambda item: float(item.get("score") or 0), reverse=True)
    best = candidates[0]
    score = float(best.get("score") or 0)
    gap = score - float(candidates[1].get("score") or 0) if len(candidates) > 1 else score
    social_exact = "url" in (best.get("reasons") or [])
    if not social_exact and (score < .90 or gap < .08):
        return None
    if social_exact and score < .92:
        return None
    return best
