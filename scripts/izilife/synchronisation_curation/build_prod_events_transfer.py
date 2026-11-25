from __future__ import annotations

import csv
import hashlib
import html
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parent
MYSQL = Path(r"C:\xampp\mysql\bin\mysql.exe")
DB = "izilife2"
STAGING_EVENTS = ROOT / "staging_event_tmp_candidates_2026-10-27.csv"
STAGING_EXPERIENCES = ROOT / "staging_experience_tmp_candidates_2026-10-27.csv"
OUTPUT = ROOT / "insert_prod_events_experiences_representations_2026-10-27.sql"


def mysql_rows(query: str) -> list[dict[str, str | None]]:
    command = [
        str(MYSQL), "--xml", "--default-character-set=utf8mb4", "-u", "root",
        "-h", "127.0.0.1", "-P", "3306", "-D", DB, "-e", query,
    ]
    payload = subprocess.check_output(command)
    root = ET.fromstring(payload)
    rows: list[dict[str, str | None]] = []
    for row in root.findall("row"):
        item: dict[str, str | None] = {}
        for field in row.findall("field"):
            item[field.attrib["name"]] = None if field.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}nil") == "true" else field.text
        rows.append(item)
    return rows


def csv_rows(path: Path) -> list[dict[str, str | None]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        for key, value in list(row.items()):
            row[key] = None if value in (None, "", "NULL") else value
    return rows


def normalized_text(value: str | None) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def normalized_url(value: str | None) -> str:
    if not value:
        return ""
    try:
        parts = urlsplit(value.strip())
        query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                 if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid", "eventdate"}]
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), urlencode(query), ""))
    except ValueError:
        return value.strip().lower()


def is_test(row: dict[str, str | None]) -> bool:
    haystack = normalized_text(" ".join(str(row.get(key) or "") for key in ("title", "name", "representation_title")))
    return bool(re.search(r"(^| )(test|tests|qa)( |$)", haystack))


def completeness(row: dict[str, str | None]) -> int:
    return sum(1 for value in row.values() if value not in (None, "", "0", "NULL"))


def event_key(row: dict[str, str | None]) -> tuple[str, ...]:
    url = normalized_url(row.get("source_url"))
    fingerprint = (row.get("fingerprint") or row.get("file_fingerprint") or "").strip().lower()
    if url:
        return ("url", url)
    if fingerprint:
        return ("fingerprint", fingerprint)
    place = row.get("transfer_place_ref") or row.get("transfer_shop_ref") or row.get("place_string_id") or row.get("location_text") or row.get("place")
    return (
        "business", normalized_text(row.get("title")), str(row.get("start_date") or ""),
        str(row.get("start_hour") or "")[:5], normalized_text(place),
    )


def experience_key(row: dict[str, str | None]) -> tuple[str, ...]:
    url = normalized_url(row.get("source_url"))
    fingerprint = (row.get("fingerprint") or row.get("file_fingerprint") or "").strip().lower()
    if url:
        return ("url", url)
    if fingerprint:
        return ("fingerprint", fingerprint)
    return ("business", normalized_text(row.get("title")), normalized_text(row.get("transfer_city_ref") or row.get("city_string_id")))


def merge(rows: list[dict[str, str | None]], key_fn) -> tuple[list[dict[str, str | None]], int]:
    selected: dict[tuple[str, ...], dict[str, str | None]] = {}
    duplicates = 0
    for row in rows:
        if is_test(row):
            continue
        key = key_fn(row)
        if key in selected:
            duplicates += 1
            if completeness(row) > completeness(selected[key]):
                selected[key] = row
        else:
            selected[key] = row
    return list(selected.values()), duplicates


def sql(value: str | int | float | None) -> str:
    if value is None or value == "NULL" or value == "":
        return "NULL"
    value = str(value).replace("\\", "\\\\").replace("'", "''").replace("\x00", "")
    return "'" + value + "'"


def num(value: str | None, default: str = "NULL") -> str:
    if value is None or value == "":
        return default
    return str(value) if re.fullmatch(r"-?\d+(?:\.\d+)?", str(value)) else default


def lookup(table: str, column: str, value: str | None) -> str:
    if not value:
        return "NULL"
    return f"(SELECT id FROM `{table}` WHERE `{column}`={sql(value)} LIMIT 1)"


def local_event_tmps() -> list[dict[str, str | None]]:
    return mysql_rows("""
SELECT e.*, COALESCE(e.city_string_id,c.string_id) transfer_city_ref,
       p.place_string_id transfer_place_ref, s.shop_string_id transfer_shop_ref,
       ec.event_category_string_id transfer_category_ref,
       r.string_id transfer_representation_ref,
       ep.source_url transfer_endpoint_url, ep.label transfer_endpoint_label
FROM scraping_event_tmp e
LEFT JOIN City c ON c.id=e.city_id
LEFT JOIN Place p ON p.id=e.for_place_id
LEFT JOIN Shop s ON s.id=e.for_shop_id
LEFT JOIN EventCategory ec ON ec.id=e.auto_detected_category_id
LEFT JOIN Representation r ON r.id=e.representation_id
LEFT JOIN location_source_endpoint ep ON ep.id=e.endpoint_id
WHERE e.status='pending'
  AND (e.start_date IS NULL OR COALESCE(e.end_date,e.start_date)>=CURDATE())
ORDER BY e.id
""")


def local_experience_tmps() -> list[dict[str, str | None]]:
    return mysql_rows("""
SELECT x.*, COALESCE(x.city_string_id,c.string_id) transfer_city_ref,
       ep.source_url transfer_endpoint_url, ep.label transfer_endpoint_label
FROM scraping_experience_tmp x
LEFT JOIN City c ON c.id=x.city_id
LEFT JOIN location_source_endpoint ep ON ep.id=x.endpoint_id
WHERE x.status='pending'
ORDER BY x.id
""")


def event_tmp_insert(row: dict[str, str | None]) -> str:
    columns = [
        "title", "description", "start_date", "start_hour", "end_date", "end_hour", "basic_price",
        "is_free_event", "is_for_kids", "accessible_for_kids", "student_event", "event_in_all_city",
        "access_link", "source", "source_url", "raw_json", "status", "content_kind",
        "classification_confidence", "representation_key", "representation_title", "representation_id",
        "classification_reason", "location_text", "place", "place_string_id", "city_id", "city_string_id",
        "address", "employee_id", "local_image_path", "primary_image_url", "access_type_string_id",
        "access_booking_string_id", "scraping_type", "auto_detected_category_id", "auto_validated_at",
        "file_fingerprint", "for_place_id", "for_shop_id", "partner_id", "partner_employee_id", "hub_id",
        "endpoint_id", "discovered_item_id", "fingerprint"
    ]
    numeric = {"is_free_event", "is_for_kids", "accessible_for_kids", "student_event", "event_in_all_city", "classification_confidence"}
    values: list[str] = []
    for column in columns:
        if column in {"employee_id", "local_image_path", "partner_id", "partner_employee_id", "hub_id", "discovered_item_id"}:
            values.append("NULL")
        elif column == "city_id":
            values.append(lookup("City", "string_id", row.get("transfer_city_ref") or row.get("city_string_id")))
        elif column == "for_place_id":
            values.append(lookup("Place", "place_string_id", row.get("transfer_place_ref")))
        elif column == "for_shop_id":
            values.append(lookup("Shop", "shop_string_id", row.get("transfer_shop_ref")))
        elif column == "auto_detected_category_id":
            values.append(lookup("EventCategory", "event_category_string_id", row.get("transfer_category_ref")))
        elif column == "representation_id":
            values.append(lookup("Representation", "string_id", row.get("transfer_representation_ref")))
        elif column == "endpoint_id":
            endpoint = row.get("transfer_endpoint_url")
            values.append(lookup("location_source_endpoint", "source_url", endpoint))
        elif column in numeric:
            values.append(num(row.get(column), "0"))
        else:
            values.append(sql(row.get(column)))
    title = sql(row.get("title"))
    start_date = sql(row.get("start_date"))
    start_hour = sql((row.get("start_hour") or "")[:5] or None)
    source_url = sql(row.get("source_url"))
    fingerprint = sql(row.get("fingerprint") or row.get("file_fingerprint"))
    place_ref = lookup("Place", "place_string_id", row.get("transfer_place_ref"))
    shop_ref = lookup("Shop", "shop_string_id", row.get("transfer_shop_ref"))
    return f"""INSERT INTO scraping_event_tmp (`{'`,`'.join(columns)}`)
SELECT {','.join(values)}
WHERE NOT EXISTS (
  SELECT 1 FROM scraping_event_tmp d
  WHERE ({source_url} IS NOT NULL AND d.source_url={source_url})
     OR ({fingerprint} IS NOT NULL AND COALESCE(d.fingerprint,d.file_fingerprint)={fingerprint})
     OR (LOWER(TRIM(d.title))=LOWER(TRIM({title})) AND d.start_date <=> {start_date}
         AND LEFT(COALESCE(d.start_hour,''),5)=LEFT(COALESCE({start_hour},''),5)
         AND d.for_place_id <=> {place_ref} AND d.for_shop_id <=> {shop_ref})
);"""


def experience_tmp_insert(row: dict[str, str | None]) -> str:
    columns = [
        "title", "experience_string_id", "experience_picture", "description", "short_description", "basic_price",
        "price_text", "minimal_age", "is_for_kids", "accessible_for_kids", "duration",
        "duration_measurement_unity_string_id", "minimal_number_of_people", "maximal_number_of_people",
        "experience_type_string_id", "experience_theme", "experience_theme2", "experience_theme3", "is_insolite",
        "is_nocturnal", "noise_level", "with_equipment", "equipment_gived", "equipment_text", "place_visit",
        "brand_text", "experience_in_all_city", "experience_access_type", "experience_booking_needed_for_access",
        "access_link", "phone_number", "city_id", "city_string_id", "source", "source_url", "raw_json", "status",
        "employee_id", "local_image_path", "file_fingerprint", "primary_image_url", "hub_id", "endpoint_id",
        "discovered_item_id", "fingerprint"
    ]
    numeric = {"basic_price", "minimal_age", "is_for_kids", "accessible_for_kids", "duration", "minimal_number_of_people", "maximal_number_of_people", "is_insolite", "is_nocturnal", "with_equipment", "equipment_gived", "place_visit", "experience_in_all_city"}
    values: list[str] = []
    for column in columns:
        if column in {"employee_id", "local_image_path", "hub_id", "discovered_item_id"}:
            values.append("NULL")
        elif column == "city_id":
            values.append(lookup("City", "string_id", row.get("transfer_city_ref") or row.get("city_string_id")))
        elif column == "endpoint_id":
            values.append(lookup("location_source_endpoint", "source_url", row.get("transfer_endpoint_url")))
        elif column in numeric:
            values.append(num(row.get(column), "0"))
        else:
            values.append(sql(row.get(column)))
    title = sql(row.get("title"))
    source_url = sql(row.get("source_url"))
    fingerprint = sql(row.get("fingerprint") or row.get("file_fingerprint"))
    city_ref = lookup("City", "string_id", row.get("transfer_city_ref") or row.get("city_string_id"))
    return f"""INSERT INTO scraping_experience_tmp (`{'`,`'.join(columns)}`)
SELECT {','.join(values)}
WHERE NOT EXISTS (
  SELECT 1 FROM scraping_experience_tmp d
  WHERE ({source_url} IS NOT NULL AND d.source_url={source_url})
     OR ({fingerprint} IS NOT NULL AND COALESCE(d.fingerprint,d.file_fingerprint)={fingerprint})
     OR (LOWER(TRIM(d.title))=LOWER(TRIM({title})) AND d.city_id <=> {city_ref})
);"""


def representation_rows() -> list[dict[str, str | None]]:
    return mysql_rows("""
SELECT r.*, ec.event_category_string_id representation_category_ref,
       p.place_string_id place_ref, s.shop_string_id shop_ref, c.string_id city_ref,
       at.string_id access_type_ref, ab.string_id booking_ref, cu.currency_code currency_ref
FROM Representation r
LEFT JOIN EventCategory ec ON ec.id=r.representation_category
LEFT JOIN Place p ON p.id=r.place_id
LEFT JOIN Shop s ON s.id=r.shop_id
LEFT JOIN City c ON c.id=r.default_city_id
LEFT JOIN AccessType at ON at.id=r.event_access_type
LEFT JOIN AccessBookingNeeded ab ON ab.id=r.event_booking_needed_for_access
LEFT JOIN Currency cu ON cu.id=r.basic_price_currency
WHERE LOCATE('test',LOWER(CONVERT(r.name USING utf8mb4)))=0
  AND LOCATE('qa ',LOWER(CONVERT(r.name USING utf8mb4)))=0
ORDER BY r.id
""")


def representation_insert(row: dict[str, str | None]) -> str:
    fields = ["name", "string_id", "is_online", "is_active", "is_for_kids", "is_accessible_for_kids", "is_all_public", "minimal_age", "is_tour", "default_event_in_all_city", "default_address", "default_address_complement", "default_zip_code", "default_latitude", "default_longitude", "access_on_booking", "access_text", "access_link", "is_free_event", "basic_price", "description", "saving_default_language"]
    numeric = {"is_online", "is_active", "is_for_kids", "is_accessible_for_kids", "is_all_public", "minimal_age", "is_tour", "default_event_in_all_city", "default_latitude", "default_longitude", "access_on_booking", "is_free_event", "basic_price", "saving_default_language"}
    columns = fields + ["unique_id", "representation_category", "place_id", "shop_id", "default_city_id", "event_access_type", "event_booking_needed_for_access", "basic_price_currency", "cover_picture", "poster_picture"]
    values = [num(row.get(f), "0") if f in numeric else sql(row.get(f)) for f in fields]
    values += [
        "REPLACE(UUID(),'-','')",
        lookup("EventCategory", "event_category_string_id", row.get("representation_category_ref")),
        lookup("Place", "place_string_id", row.get("place_ref")),
        lookup("Shop", "shop_string_id", row.get("shop_ref")),
        lookup("City", "string_id", row.get("city_ref")),
        lookup("AccessType", "string_id", row.get("access_type_ref")),
        lookup("AccessBookingNeeded", "string_id", row.get("booking_ref")),
        lookup("Currency", "currency_code", row.get("currency_ref")),
        "NULL", "NULL",
    ]
    return f"INSERT INTO Representation (`{'`,`'.join(columns)}`) SELECT {','.join(values)} WHERE NOT EXISTS (SELECT 1 FROM Representation d WHERE d.string_id={sql(row.get('string_id'))});"


def local_events() -> list[dict[str, str | None]]:
    return mysql_rows("""
SELECT le.*, r.string_id representation_ref, ec.event_category_string_id event_category_ref,
       pac.string_id principal_activity_ref, p.place_string_id place_ref, s.shop_string_id shop_ref,
       c.string_id city_ref, at.string_id access_type_ref, ab.string_id booking_ref, cu.currency_code currency_ref
FROM LocalEvent le
JOIN Representation r ON r.id=le.representation_id
LEFT JOIN EventCategory ec ON ec.id=le.event_category
LEFT JOIN ActivityPrincipalCategory pac ON pac.id=le.principal_activity_category
LEFT JOIN Place p ON p.id=COALESCE(le.event_place,le.place_id)
LEFT JOIN Shop s ON s.id=COALESCE(le.event_shop,le.shop_id)
LEFT JOIN City c ON c.id=le.city_id
LEFT JOIN AccessType at ON at.id=le.event_access_type
LEFT JOIN AccessBookingNeeded ab ON ab.id=le.event_booking_needed_for_access
LEFT JOIN Currency cu ON cu.id=le.basic_price_currency
WHERE le.event_start_date>=CURDATE()
  AND LOCATE('test',LOWER(CONVERT(CONCAT_WS(' ',r.name,le.title) USING utf8mb4)))=0
  AND LOCATE('qa ',LOWER(CONVERT(CONCAT_WS(' ',r.name,le.title) USING utf8mb4)))=0
ORDER BY le.event_start_date,le.event_start_hour,le.id
""")


def local_event_insert(row: dict[str, str | None]) -> str:
    fields = ["title", "local_event_official_name", "local_event_official_string_id", "event_string_id", "is_online_event", "listable", "multiple_places", "event_in_all_city", "is_active", "is_degraded_mode", "is_tour", "event_start_date", "event_start_hour", "event_end_date", "event_end_hour", "is_nocturnal", "time_on_place", "number_of_tickets", "is_recurrent_event", "recurrent_day", "recurrent_until", "kill_recurrency", "is_alive_representation", "minimal_age", "student_event", "only_for_students", "is_for_kids", "accessible_for_kids", "event_cancelled", "event_reported", "is_free_event", "access_on_booking", "access_text", "access_link", "show_external_booking_link", "basic_price", "address", "address_complement", "longitude", "latitude", "zip_code", "city", "event_brand_text", "phone_number", "description", "saving_default_language", "scrapped_from", "scrapping_json", "reserved_for", "secret_address", "access_conditions_text", "visibility_mode"]
    text_fields = {"title", "local_event_official_name", "local_event_official_string_id", "event_string_id", "event_start_date", "event_start_hour", "event_end_date", "event_end_hour", "recurrent_until", "access_text", "access_link", "address", "address_complement", "city", "event_brand_text", "phone_number", "description", "scrapped_from", "scrapping_json", "access_conditions_text", "visibility_mode"}
    columns = fields + ["unique_id", "representation_id", "event_category", "principal_activity_category", "event_place", "event_shop", "place_id", "shop_id", "city_id", "event_access_type", "event_booking_needed_for_access", "basic_price_currency", "cover_picture", "created_by_user", "created_by_page", "partner_id", "page_id"]
    values = [sql(row.get(f)) if f in text_fields else num(row.get(f), "NULL") for f in fields]
    place = lookup("Place", "place_string_id", row.get("place_ref"))
    shop = lookup("Shop", "shop_string_id", row.get("shop_ref"))
    values += [
        "REPLACE(UUID(),'-','')", lookup("Representation", "string_id", row.get("representation_ref")),
        lookup("EventCategory", "event_category_string_id", row.get("event_category_ref")),
        lookup("ActivityPrincipalCategory", "string_id", row.get("principal_activity_ref")),
        place, shop, place, shop, lookup("City", "string_id", row.get("city_ref")),
        lookup("AccessType", "string_id", row.get("access_type_ref")),
        lookup("AccessBookingNeeded", "string_id", row.get("booking_ref")),
        lookup("Currency", "currency_code", row.get("currency_ref")),
        "NULL", "NULL", "NULL", "NULL", "NULL",
    ]
    rep = lookup("Representation", "string_id", row.get("representation_ref"))
    title = sql(row.get("title")); date = sql(row.get("event_start_date")); hour = sql((row.get("event_start_hour") or "")[:5])
    return f"""INSERT INTO LocalEvent (`{'`,`'.join(columns)}`)
SELECT {','.join(values)}
WHERE NOT EXISTS (SELECT 1 FROM LocalEvent d WHERE
  ({sql(row.get('event_string_id'))} IS NOT NULL AND d.event_string_id={sql(row.get('event_string_id'))})
  OR (d.representation_id <=> {rep} AND LOWER(TRIM(d.title))=LOWER(TRIM({title}))
      AND d.event_start_date={date} AND LEFT(d.event_start_hour,5)=LEFT({hour},5))
);"""


def main() -> None:
    local_events_tmp = local_event_tmps()
    staging_events_tmp = csv_rows(STAGING_EVENTS)
    events, event_duplicates = merge(local_events_tmp + staging_events_tmp, event_key)

    local_experiences_tmp = local_experience_tmps()
    staging_experiences_tmp = csv_rows(STAGING_EXPERIENCES)
    experiences, experience_duplicates = merge(local_experiences_tmp + staging_experiences_tmp, experience_key)

    representations = [row for row in representation_rows() if not is_test(row)]
    future_events = [row for row in local_events() if not is_test(row)]

    header = f"""-- Reprise unique local/staging vers production, générée le 2026-10-27.
-- Idempotent : aucune mise à jour, aucun effacement, aucun ID source réutilisé.
-- EventTmp candidats uniques: {len(events)} (doublons source éliminés: {event_duplicates}).
-- ExperienceTmp candidats uniques: {len(experiences)} (doublons source éliminés: {experience_duplicates}).
-- Representations hors tests: {len(representations)}; LocalEvent futurs liés: {len(future_events)}.
START TRANSACTION;
SET @transfer_started_at = NOW();
"""
    sections = [header]
    sections += ["\n-- REPRESENTATIONS", *(representation_insert(row) for row in representations)]
    sections += ["\n-- LOCAL EVENTS FUTURS LIES AUX REPRESENTATIONS", *(local_event_insert(row) for row in future_events)]
    sections += ["\n-- EVENT TMP", *(event_tmp_insert(row) for row in events)]
    sections += ["\n-- EXPERIENCE TMP", *(experience_tmp_insert(row) for row in experiences)]
    sections += ["\nCOMMIT;\n"]
    OUTPUT.write_text("\n".join(sections), encoding="utf-8")
    print(f"output={OUTPUT}")
    print(f"event_tmp local={len(local_events_tmp)} staging={len(staging_events_tmp)} unique={len(events)} duplicates={event_duplicates}")
    print(f"experience_tmp local={len(local_experiences_tmp)} staging={len(staging_experiences_tmp)} unique={len(experiences)} duplicates={experience_duplicates}")
    print(f"representations={len(representations)} future_local_events={len(future_events)}")


if __name__ == "__main__":
    main()
