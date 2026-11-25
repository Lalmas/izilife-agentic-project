"""OCR local et extraction déterministe de dates/heures d'affiches Event."""
from __future__ import annotations

import re
import shutil
from datetime import date, timedelta
from pathlib import Path

MONTHS = {
    "janvier": 1, "fevrier": 2, "février": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "aout": 8, "août": 8,
    "septembre": 9, "octobre": 10, "novembre": 11,
    "decembre": 12, "décembre": 12,
}
DATE_WORD_RE = re.compile(
    r"\b(?:lun(?:di)?|mar(?:di)?|mer(?:credi)?|jeu(?:di)?|ven(?:dredi)?|sam(?:edi)?|dim(?:anche)?)?\s*"
    r"(?P<day>[0-3]?\d)(?:er)?\s+(?P<month>" + "|".join(MONTHS) + r")"
    r"(?:\s+(?P<year>20\d{2}))?\b", re.I,
)
DATE_NUM_RE = re.compile(r"\b(?P<day>[0-3]?\d)[/.-](?P<month>0?\d|1[0-2])(?:[/.-](?P<year>20\d{2}|\d{2}))?\b")
TIME_RANGE_RE = re.compile(
    r"\b(?:de\s*)?(?P<start>[0-2]?\d\s*(?:h|H|:)\s*[0-5]?\d?)\s*"
    r"(?:a|à|-|–|—)\s*(?P<end>[0-2]?\d\s*(?:h|H|:)\s*[0-5]?\d?)\b", re.I,
)
TIME_RE = re.compile(r"\b(?P<hour>[0-2]?\d)\s*(?:h|H|:)\s*(?P<minute>[0-5]\d)?\b")


def extract_title_candidate(text: str) -> str:
    """Choisit seulement un titre suffisamment caractéristique.

    Une phrase ordinaire de légende (par exemple ``Avec les superbes``) ne doit
    jamais devenir le titre de l'événement. Les cellules Excel restent la
    source autoritaire quand aucun candidat fort n'est visible.
    """
    candidates = []
    for raw in str(text or "").splitlines():
        line = re.sub(r"\s+", " ", raw).strip(" -–—|•·")
        if len(line) < 4 or len(line) > 140:
            continue
        lowered = line.lower()
        if re.search(r"https?://|www\.|@[a-z0-9_.]+", lowered):
            continue
        if re.search(r"\b(?:agenda|programme|programmation|nos événements|ce mois-ci)\b", lowered):
            continue
        if DATE_WORD_RE.search(line) or DATE_NUM_RE.search(line) or TIME_RE.search(line):
            continue
        alpha = sum(char.isalpha() for char in line)
        if alpha < 4:
            continue
        words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", line)
        letters = [char for char in line if char.isalpha()]
        upper_ratio = sum(char.isupper() for char in letters) / max(1, len(letters))
        event_signal = bool(re.search(
            r"\b(?:soir[ée]e|party|festival|concert|stand\s*up|comedy|spectacle|atelier|"
            r"anniversaire|birthday|tournoi|march[ée]|brunch|jam|quiz|karaok[ée])\b",
            lowered,
        ))
        title_case = len(words) >= 2 and sum(word[:1].isupper() for word in words) >= max(2, len(words) // 2)
        score = (4 if event_signal else 0) + (2 if upper_ratio >= .55 else 0) + (1 if title_case else 0)
        if score >= 4:
            candidates.append((score, line))
    return max(candidates, default=(0, ""), key=lambda item: item[0])[1]


def is_strong_title(value: str) -> bool:
    """Indique si un titre peut être conservé sans validation humaine."""
    return bool(extract_title_candidate(str(value or "")))


def infer_event_category(text: str) -> str:
    """Retourne uniquement une catégorie prouvée par des mots explicites."""
    normalized = re.sub(r"\s+", " ", str(text or "")).lower()
    rules = (
        (r"\b(?:stand\s*-?up|comedy\s*club|humoriste|humour)\b", "stand-up"),
        (r"\b(?:concert|live\s+music|musique\s+live)\b", "concert"),
        (r"\b(?:march[ée]\s+de\s+no[eë]l)\b", "marche-de-noel"),
        (r"\b(?:atelier|workshop)\b", "atelier"),
    )
    for pattern, reference in rules:
        if re.search(pattern, normalized, re.I):
            return reference
    return ""


NIGHTLIFE_RE = re.compile(
    r"\b(?:soir[ée]e|night|afterwork|karaok[ée]|blind\s*test|block\s*party|"
    r"club|discoth[èe]que|dj\s*set|dancefloor|bar|bal|bamboche)\b",
    re.I,
)


def estimated_end_hour(start_hour: str, context: str = "") -> str:
    """Estime une fin contextuelle uniquement lorsqu'aucune fin n'est publiée.

    La valeur explicite de la source doit toujours gagner. Les vraies soirées
    sans horaire de fin passent à 02:00 (donc au lendemain); les autres bornes
    évitent que tous les événements ordinaires polluent le classement jusqu'à
    23:59.
    """
    try:
        hour = int(str(start_hour or "").split(":", 1)[0])
    except (TypeError, ValueError):
        return ""
    if hour >= 18 and NIGHTLIFE_RE.search(str(context or "")):
        return "02:00"
    if hour >= 19:
        return "23:59"
    if hour >= 16:
        return "19:00"
    return "18:00"


def _iso_date(day: str, month: int, year: str | None, today: date) -> str:
    parsed_year = int(year) if year else today.year
    if parsed_year < 100:
        parsed_year += 2000
    candidate = date(parsed_year, month, int(day))
    if not year and candidate < today:
        candidate = date(parsed_year + 1, month, int(day))
    return candidate.isoformat()


def _time(value: str) -> str | None:
    match = re.fullmatch(r"\s*([0-2]?\d)\s*(?:h|H|:)\s*([0-5]\d)?\s*", value)
    if not match:
        return None
    hour, minute = int(match.group(1)), int(match.group(2) or 0)
    return f"{hour:02d}:{minute:02d}" if hour <= 23 else None


def extract_event_fields(text: str, today: date | None = None) -> dict:
    """Extrait seulement les dates et heures non ambiguës, sans deviner."""
    today = today or date.today()
    normalized = re.sub(r"[ \t]+", " ", str(text or ""))
    dates: list[str] = []
    for match in DATE_WORD_RE.finditer(normalized):
        value = _iso_date(match.group("day"), MONTHS[match.group("month").lower()], match.group("year"), today)
        if value not in dates:
            dates.append(value)
    for match in DATE_NUM_RE.finditer(normalized):
        value = _iso_date(match.group("day"), int(match.group("month")), match.group("year"), today)
        if value not in dates:
            dates.append(value)

    ranges: list[tuple[str, str]] = []
    for match in TIME_RANGE_RE.finditer(normalized):
        start, end = _time(match.group("start")), _time(match.group("end"))
        if start and end and (start, end) not in ranges:
            ranges.append((start, end))
    isolated = []
    for match in TIME_RE.finditer(normalized):
        value = _time(match.group(0))
        if value and value not in isolated:
            isolated.append(value)

    result: dict[str, object] = {"ocr_text": normalized.strip(), "ambiguous": False, "reasons": []}
    if len(dates) == 1:
        result["start_date"] = dates[0]
    elif len(dates) > 1:
        result["ambiguous"] = True
        result["reasons"].append("multiple_dates")
        result["date_candidates"] = dates
    if len(ranges) == 1:
        result["start_hour"], result["end_hour"] = ranges[0]
    elif len(ranges) > 1:
        result["ambiguous"] = True
        result["reasons"].append("multiple_time_ranges")
        result["time_candidates"] = ranges
    elif len(isolated) == 1:
        result["start_hour"] = isolated[0]
    elif len(isolated) > 1:
        result["ambiguous"] = True
        result["reasons"].append("multiple_isolated_times")
        result["time_candidates"] = isolated
    return result


def ocr_image(path: Path) -> tuple[str, str]:
    """Essaie RapidOCR, PaddleOCR puis Tesseract, tous locaux."""
    try:
        from rapidocr_onnxruntime import RapidOCR  # type: ignore
        result, _ = RapidOCR()(str(path))
        chunks = [str(item[1]).strip() for item in (result or []) if len(item) > 1 and str(item[1]).strip()]
        if chunks:
            return "\n".join(chunks), "rapidocr"
    except (ImportError, RuntimeError, OSError, ValueError, TypeError):
        pass
    try:
        from paddleocr import PaddleOCR  # type: ignore
        engine = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, lang="fr")
        output = engine.predict(str(path))
        chunks = []
        for item in output:
            data = item.json() if callable(getattr(item, "json", None)) else {}
            chunks.extend((data.get("res", {}) if isinstance(data, dict) else {}).get("rec_texts", []) or [])
        if chunks:
            return "\n".join(str(value) for value in chunks if str(value).strip()), "paddleocr"
    except (ImportError, RuntimeError, OSError, ValueError):
        pass
    if shutil.which("tesseract"):
        try:
            import pytesseract  # type: ignore
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(path), lang="fra+eng")
            if text.strip():
                return text, "tesseract"
        except (ImportError, RuntimeError, OSError, ValueError):
            pass
    return "", ""


def complete_missing_fields(row: dict, image_path: Path, today: date | None = None) -> dict:
    """Complète une copie de la ligne sans écraser une cellule Excel."""
    completed = dict(row or {})
    if completed.get("title") and completed.get("description") and completed.get("start_date") and completed.get("start_hour") and completed.get("end_hour"):
        return completed
    text, engine = ocr_image(image_path)
    if not text:
        completed["local_ocr_status"] = "unavailable"
        return completed
    parsed = extract_event_fields(text, today=today)
    # L'OCR local ne décide plus des champs éditoriaux. Un titre, une
    # description ou une catégorie demandent une compréhension du visuel : ils
    # restent manquants afin que l'unique appel Luna les produise proprement.
    for key in ("start_date", "start_hour", "end_hour"):
        if parsed.get(key) and not str(completed.get(key) or "").strip():
            completed[key] = parsed[key]
    if completed.get("start_hour") and not completed.get("end_hour"):
        context = " ".join(str(completed.get(key) or "") for key in (
            "title", "description", "event_category_ref", "event_category_string_id",
        ))
        completed["end_hour"] = estimated_end_hour(completed["start_hour"], context)
        completed["end_hour_is_estimated"] = True
    if (completed.get("start_date") and completed.get("end_hour")
            and not str(completed.get("end_date") or "").strip()):
        completed["end_date"] = completed["start_date"]
        if (completed.get("end_hour_is_estimated")
                and str(completed.get("end_hour")) < str(completed.get("start_hour"))):
            completed["end_date"] = (
                date.fromisoformat(str(completed["start_date"])) + timedelta(days=1)
            ).isoformat()
    completed["local_ocr_status"] = "ambiguous" if parsed["ambiguous"] else "completed"
    completed["local_ocr_engine"] = engine
    completed["local_ocr_reasons"] = ",".join(parsed["reasons"])
    completed["local_ocr_text"] = text
    return completed
