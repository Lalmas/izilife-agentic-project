import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://www.labraiseseclin.com/menu"
CATEGORIES = [
    ("entrees", BASE + "?location=Location+1"),
    *[(slug, BASE + f"?location=Location+1&menu={slug}") for slug in (
        "grillades", "ribs", "poissons", "burgers", "pates", "salades",
        "desserts", "boissons", "alcools", "vins", "spiritueux", "formules-midi"
    )],
]

def main():
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="fr-FR")
        for category, url in CATEGORIES:
            print(f"CATEGORY {category}", flush=True)
            page.goto(url, wait_until="commit", timeout=25000)
            page.wait_for_timeout(2500)
            for _ in range(5):
                page.mouse.wheel(0, 2500)
                page.wait_for_timeout(180)
            images = page.locator("img").evaluate_all(r"""imgs => imgs.map(img => {
              let owner=img.parentElement, best='';
              for(let i=0; owner && i<10; i++, owner=owner.parentElement){
                const text=(owner.innerText||'').trim();
                if(text && text.length<1200){ best=text; if(/[€$£]/.test(text)) break; }
              }
              return {alt:(img.alt||'').trim(), url:img.currentSrc||img.src||'', width:img.naturalWidth||0,
                height:img.naturalHeight||0, context:best.slice(0,1000)};
            }).filter(x => /^https?:\/\//i.test(x.url) && x.width >= 200 && x.height >= 150 && x.alt)""")
            for item in images:
                item.update(category=category, source_url=url)
                rows.append(item)
        browser.close()
    unique = {}
    for row in rows:
        key = (row["category"], row["alt"].casefold(), row["url"].split("?")[0])
        unique[key] = row
    out = Path(__file__).with_name("menu_images.json")
    out.write_text(json.dumps(list(unique.values()), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"count": len(unique), "output": str(out)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
