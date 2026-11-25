"""Smoke test manuel, sans écriture ni API Google Places payante."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from core.place_resolution import MapsNameResolver


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--city", required=True)
    args = parser.parse_args()
    with MapsNameResolver() as resolver:
        resolver.resolve(args.name, args.city)
        print(json.dumps(asdict(resolver.last_result), ensure_ascii=False, indent=2), flush=True)
        return 0 if resolver.last_result.canonical_name else 2


if __name__ == "__main__":
    raise SystemExit(main())
