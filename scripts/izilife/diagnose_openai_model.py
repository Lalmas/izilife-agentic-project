#!/usr/bin/env python3
"""Diagnostic minimal du modèle OpenAI configuré, sans afficher la clé."""
import json
import re
from pathlib import Path

import requests

text = Path(r"C:\xampp\htdocs\izilife-admin\.env").read_text(encoding="utf-8", errors="ignore")
match = re.search(r"(?mi)^\s*(?:openai\.apiKey|OPENAI_API_KEY)\s*=\s*['\"]?([^'\"\r\n#]+)", text)
if not match:
    raise RuntimeError("Clé OpenAI locale absente")

response = requests.post(
    "https://api.openai.com/v1/responses",
    headers={"Authorization": "Bearer " + match.group(1).strip(), "Content-Type": "application/json"},
    json={
        "model": "gpt-6-luna",
        "input": "Réponds uniquement en JSON valide avec la clé ok à true.",
        "store": False,
        "tools": [{"type": "web_search"}],
        "tool_choice": "auto",
        "max_output_tokens": 100,
    },
    timeout=60,
)
body = response.json()
print(json.dumps({
    "status": response.status_code,
    "error": body.get("error"),
    "response_status": body.get("status"),
    "incomplete_details": body.get("incomplete_details"),
    "output_types": [item.get("type") for item in body.get("output", [])],
    "usage": body.get("usage"),
}, ensure_ascii=False))
