#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offers"))
from offer_agent_common import create_workbook, drive_workspace_root, normalize_zone, process

FILE, SHEET = "event_calendar.xlsx", "Calendar"
COLUMNS = [
    ("scope_type", "scope"), ("scope_ref", "scope"), ("operation", "scope"),
    ("title", "offer"), ("start_date", "access"), ("start_hour", "access"),
    ("end_date", "access"), ("end_hour", "access"),
    ("date_from", "access"), ("date_to", "access"), ("reason", "offer"),
    ("is_active", "bpr"), ("listable", "bpr"),
    ("status", "result"), ("notes", "result"), ("last_result", "result"),
]


def payload(row):
    return {key: row.get(key) for key, _ in COLUMNS
            if key not in {"status", "notes", "last_result"} and row.get(key) not in (None, "")}


def main():
    parser = argparse.ArgumentParser(description="Maintenance idempotente des dates d'événements.")
    parser.add_argument("--zone", required=True)
    parser.add_argument("--env", choices=["local", "staging", "prod"], default="local")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max", type=int, default=100)
    args = parser.parse_args()
    path = drive_workspace_root(args.env) / "izilife" / "events" / normalize_zone(args.zone) / FILE
    if args.init:
        example = {
            "scope_type": "EVENT_SERIE", "scope_ref": "serie-string-id",
            "operation": "ADD_DATE", "title": "", "start_date": "2026-12-01",
            "start_hour": "19:00", "end_date": "2026-12-01", "end_hour": "23:00",
            "is_active": "oui", "listable": "oui", "status": "skip",
            "notes": "EVENT utilise unique_id. EVENT_SERIE et ANNUAL_CELEBRATION utilisent leur string_id.",
        }
        validations = {
            "scope_type": ["EVENT", "EVENT_SERIE", "ANNUAL_CELEBRATION"],
            "operation": ["ADD_DATE", "CANCEL_DATE", "CANCEL_PERIOD", "POSTPONE_EVENT", "CLOSE_RECURRENCE"],
            "is_active": ["oui", "non"], "listable": ["oui", "non"],
            "status": ["pending", "done", "error", "skip", "unmapped"],
        }
        create_workbook(path, SHEET, COLUMNS, example, validations)
        return
    process(path, SHEET, args.env, "/scraper/agentApplyEventCalendar", payload, args.dry_run, args.max)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent_excel_logger import run_logged
    run_logged("event_calendar", "events", main)

