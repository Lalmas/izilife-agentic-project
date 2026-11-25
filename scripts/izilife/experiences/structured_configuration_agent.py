#!/usr/bin/env python3
"""Agent d'extraction BookingConfiguration/SessionConfiguration.

PLACE, SHOP et EQUIPMENT produisent BookingConfiguration + Content ; EXPERIENCE
produit SessionConfiguration + SessionConfigurationContent. ``plan`` ne fait
qu'écrire le JSON. ``apply`` exige un environnement et --confirm-write.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from site_experience_package import izilife_post


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "apply"])
    parser.add_argument("--url", required=True)
    parser.add_argument("--target-type", required=True, choices=["PLACE", "SHOP", "EQUIPMENT", "EXPERIENCE"])
    parser.add_argument("--target-id", type=int)
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--confirm-write", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    apply = args.command == "apply"
    if apply and (not args.confirm_write or not args.target_id):
        raise SystemExit("apply exige --target-id et --confirm-write.")
    if not apply and args.confirm_write:
        raise SystemExit("--confirm-write n'est valable qu'avec apply.")
    payload = {"source_url": args.url, "target_type": args.target_type,
               "target_id": args.target_id, "apply": apply,
               "confirm_write": args.confirm_write}
    response = izilife_post(
        "/scraper/agentExtractStructuredConfiguration",
        {"payload": json.dumps(payload, ensure_ascii=False)}, args.env, timeout=300,
    )
    if not response.get("success"):
        raise SystemExit(response.get("error") or json.dumps(response, ensure_ascii=False))
    proposal = response["proposal"]
    output = args.output_dir or Path(__file__).with_name("reports") / "configurations"
    output.mkdir(parents=True, exist_ok=True)
    report = output / f"{args.target_type.lower()}_{datetime.now():%Y%m%d_%H%M%S}.json"
    report.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
