#!/usr/bin/env python3
"""Consomme les paquets JSON déposés dans le dossier Drive de l'environnement.

Les fichiers restent dans l'inbox. Leur empreinte SHA-256 est enregistrée dans
le workspace technique afin qu'un paquet déjà appliqué ne soit jamais rejoué.
Un fichier modifié reçoit une nouvelle empreinte et peut donc être retraité.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = ROOT.parent
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

from core.paths import drive_workspace_root, local_agent_workspace_root


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"files": {}}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {"files": {}}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--inbox", type=Path)
    parser.add_argument("--max", type=int, default=20)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-production")
    parser.add_argument("--retry-errors", action="store_true")
    args = parser.parse_args()

    if args.apply and args.env == "prod" and args.confirm_production != "I_CONFIRM_PRODUCTION_PACKAGE_INBOX":
        raise SystemExit("Production refusée sans confirmation dédiée.")

    inbox = args.inbox or (
        drive_workspace_root(args.env) / "izilife" / "site_packages" / "inbox"
    )
    inbox.mkdir(parents=True, exist_ok=True)
    state_path = (
        local_agent_workspace_root(args.env) / "state" / "site_package_inbox.json"
    )
    state = load_state(state_path)
    files_state = state.setdefault("files", {})
    candidates = sorted(path for path in inbox.glob("*.json") if path.is_file())
    counters = {"found": len(candidates), "processed": 0, "skipped": 0, "done": 0, "error": 0}

    for path in candidates:
        if counters["processed"] >= max(0, args.max):
            break
        fingerprint = digest(path)
        previous = files_state.get(str(path), {})
        if previous.get("sha256") == fingerprint and (
            previous.get("status") == "done" or
            (previous.get("status") == "error" and not args.retry_errors)
        ):
            counters["skipped"] += 1
            continue

        command = [sys.executable, str(ROOT / "site_package.py")]
        if args.apply:
            command += [
                "apply", "--file", str(path), "--env", args.env, "--confirm-write",
            ]
            if args.env == "prod":
                command += ["--confirm-production", "I_CONFIRM_PRODUCTION_EVENT_PACKAGE"]
        else:
            command += ["plan", "--file", str(path)]

        completed = subprocess.run(command, text=True, capture_output=True)
        counters["processed"] += 1
        status = "done" if completed.returncode == 0 else "error"
        counters[status] += 1
        files_state[str(path)] = {
            "sha256": fingerprint,
            "status": status,
            "processed_at": datetime.now().isoformat(),
            "returncode": completed.returncode,
            "stdout": completed.stdout[-5000:],
            "stderr": completed.stderr[-5000:],
        }
        save_state(state_path, state)

    print(json.dumps({"inbox": str(inbox), "state": str(state_path), **counters}, ensure_ascii=False))
    return 1 if counters["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
