import json, re
from pathlib import Path
from openpyxl import Workbook

ROOT = Path(__file__).parent
rows = json.loads((ROOT / "menu_images.json").read_text(encoding="utf-8"))
ignored = {"IMG_9552.jpeg", "Produit laitier"}
seen = set()
source_url = "https://www.labraiseseclin.com/menu"
sources = {source_url: []}

for row in rows:
    name = row["alt"].strip()
    if name in ignored:
        continue
    key = re.sub(r"\W+", " ", name.casefold()).strip()
    if key in seen:
        continue
    seen.add(key)
    lines = [line.strip() for line in row.get("context", "").splitlines() if line.strip()]
    price_index = next((i for i, line in enumerate(lines[1:], 1) if re.fullmatch(r"\d+(?:[,.]\d+)?\s*€", line)), None)
    description = " ".join(lines[1:price_index]) if price_index is not None else ""
    price = None
    if price_index is not None:
        price = float(re.sub(r"[^\d,.]", "", lines[price_index]).replace(",", "."))
    source_image = row["url"]
    if "/v1/" in source_image:
        base, tail = source_image.split("/v1/", 1)
        filename = tail.rsplit("/", 1)[-1]
        source_image = f"{base}/v1/fill/w_1200,h_1200,al_c,q_90,enc_auto/{filename}"
    item = {
        "name": name,
        "description": description,
        # Demander à Wix une variante haute résolution téléchargeable. L'URL
        # source nue est refusée par leur CDN et la miniature 300x300 par le BO.
        "primary_image_url": source_image,
        "raw_source_url": row["source_url"],
    }
    if price is not None:
        item.update(price=price, currency_code="EUR")
    sources[source_url].append({"kind": "product", "item": item})

(ROOT / "fixture.json").write_text(json.dumps({"sources": sources}, ensure_ascii=False, indent=2), encoding="utf-8")

wb = Workbook()
ws = wb.active
ws.title = "Enrichissement"
headers = ["SCOPE_TYPE", "SCOPE_REF", "URL_1", "STATUS", "LAST_RESULT"]
ws.append(headers)
for url in sources:
    ws.append(["SHOP", "la-braise", url, "pending", ""])
wb.save(ROOT / "la_braise_images.xlsx")
print(json.dumps({"products": len(seen), "sources": len(sources)}, ensure_ascii=False))
