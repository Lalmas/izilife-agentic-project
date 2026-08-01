#!/usr/bin/env python3
"""Point d'entrée sûr pour les agents et le planning iziLife."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
CATALOGUE_PATH = HERE / "catalogue.json"
DEFAULT_SCRIPTS_ROOT = HERE.parent
PRODUCTION_PHRASE = "JE_CONFIRME_PRODUCTION"


def load_catalogue() -> dict:
    with CATALOGUE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def scripts_root() -> Path:
    configured = os.environ.get("IZILIFE_AGENT_SCRIPTS_ROOT", "").strip()
    return Path(configured) if configured else DEFAULT_SCRIPTS_ROOT


def print_agents(catalogue: dict) -> None:
    current_group = None
    for key, agent in sorted(catalogue["agents"].items(), key=lambda item: (item[1]["group"], item[0])):
        if agent["group"] != current_group:
            current_group = agent["group"]
            print(f"\n{current_group}")
        availability = "OK" if (scripts_root() / agent["script"]).is_file() else "MANQUANT"
        print(f"  {key:<25} {agent['label']} [{agent['schedule']}] ({availability})")


def print_suites(catalogue: dict) -> None:
    for name, members in catalogue["suites"].items():
        print(f"\n{name}")
        for member in members:
            print(f"  - {member}: {catalogue['agents'][member]['label']}")


def print_planning(catalogue: dict) -> None:
    for block in catalogue["planning"]:
        print(f"\n{block['frequency'].upper()}")
        for job in block["jobs"]:
            print(f"  - {job}")
        print(f"  Note : {block['note']}")


def validate_environment(args: argparse.Namespace) -> bool:
    if args.env != "prod":
        return True
    if not args.execute:
        return True
    if args.confirm_production != PRODUCTION_PHRASE:
        print("PRODUCTION REFUSÉE : ajoutez --confirm-production JE_CONFIRME_PRODUCTION", file=sys.stderr)
        return False
    return True


def build_command(agent: dict, args: argparse.Namespace) -> list[str]:
    script = scripts_root() / agent["script"]
    if not script.is_file():
        raise FileNotFoundError(f"Script introuvable : {script}")

    command = [sys.executable, str(script), f"--env={args.env}"]
    command.extend(agent.get("arguments", []))
    scope = agent.get("scope", [])
    if "zone" in scope:
        command.append(f"--zone={args.zone}")
    if "city" in scope:
        command.append(f"--city={args.city or args.zone}")
    if "country" in scope:
        command.append(f"--country={args.country}")
    if agent.get("limit_option"):
        value = args.limit if args.limit is not None else agent.get("default_limit")
        if value is not None:
            command.extend([agent["limit_option"], str(value)])
    if agent.get("duration_option"):
        value = args.max_duration if args.max_duration is not None else agent.get("default_duration_minutes")
        if value is not None:
            command.extend([agent["duration_option"], str(value)])
    if "url" in agent.get("required_inputs", []):
        if not args.url:
            raise ValueError("Cet agent exige --url")
        command.extend(["--url", args.url])
    if not args.execute:
        command.append("--dry-run")
    return command


def redact_command(command: list[str]) -> str:
    return subprocess.list2cmdline(command)


def run_one(name: str, catalogue: dict, args: argparse.Namespace) -> int:
    agent = catalogue["agents"].get(name)
    if not agent:
        print(f"Agent inconnu : {name}", file=sys.stderr)
        return 2
    if not validate_environment(args):
        return 2
    try:
        command = build_command(agent, args)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    mode = "EXÉCUTION" if args.execute else "SIMULATION"
    print(f"\n[{mode}] {agent['label']} | zone={args.zone} | env={args.env}")
    print(redact_command(command))
    if args.preview:
        return 0

    logs = HERE / "logs"
    logs.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = logs / f"{stamp}_{name}_{args.env}_{args.zone}.log"
    started = time.monotonic()
    timeout_seconds = args.timeout_minutes * 60 if args.timeout_minutes else None
    with log_path.open("w", encoding="utf-8") as log:
        log.write(redact_command(command) + "\n\n")
        try:
            completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=timeout_seconds, check=False)
            code = completed.returncode
        except subprocess.TimeoutExpired:
            log.write("\nARRÊT : durée maximale du pilote dépassée.\n")
            code = 124
    elapsed = time.monotonic() - started
    print(f"Résultat={code} | durée={elapsed:.1f}s | journal={log_path}")
    return code


def main() -> int:
    catalogue = load_catalogue()
    parser = argparse.ArgumentParser(description="Centre de pilotage des agents iziLife")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("agents", help="Afficher tous les agents")
    sub.add_parser("suites", help="Afficher les regroupements")
    sub.add_parser("planning", help="Afficher le planning global")

    for action in ("run", "run-suite"):
        command = sub.add_parser(action)
        command.add_argument("name", help="Nom de l'agent ou de la suite")
        command.add_argument("--zone", default="global")
        command.add_argument("--city")
        command.add_argument("--country", default="FR")
        command.add_argument("--env", choices=["local", "staging", "prod"], default="staging")
        command.add_argument("--limit", type=int)
        command.add_argument("--max-duration", type=int, help="Limite comprise par l'agent, en minutes")
        command.add_argument("--timeout-minutes", type=int, default=120, help="Arrêt forcé par le pilote")
        command.add_argument("--url")
        command.add_argument("--execute", action="store_true", help="Autoriser les écritures ; sinon dry-run")
        command.add_argument("--confirm-production", default="")
        command.add_argument("--preview", action="store_true", help="Afficher seulement les commandes")
        command.add_argument("--continue-on-error", action="store_true")

    args = parser.parse_args()
    if args.action == "agents":
        print_agents(catalogue)
        return 0
    if args.action == "suites":
        print_suites(catalogue)
        return 0
    if args.action == "planning":
        print_planning(catalogue)
        return 0
    if args.action == "run":
        return run_one(args.name, catalogue, args)

    members = catalogue["suites"].get(args.name)
    if members is None:
        print(f"Suite inconnue : {args.name}", file=sys.stderr)
        return 2
    for member in members:
        code = run_one(member, catalogue, args)
        if code and not args.continue_on_error:
            print(f"Suite arrêtée après l'échec de {member}.", file=sys.stderr)
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
