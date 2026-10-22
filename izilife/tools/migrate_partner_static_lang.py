import hashlib, html, pathlib, re, sys, unicodedata

ROOT = pathlib.Path(r"C:\xampp\htdocs\izilife-partner-admin")
FILES = [
    "app/Views/partners/billing/index.php", "app/Views/partners/billing/payment.php",
    "app/Views/partners/boost_configure.php", "app/Views/partners/partner_boost_index.php",
    "app/Views/partners/finance/index.php", "app/Views/partners/location_features.php",
    "app/Views/partners/offers/form.php", "app/Views/partners/offers/index.php",
    "app/Views/partners/partner_places.php", "app/Views/partners/reservation_management.php",
    "app/Views/partners/settings_banking.php", "app/Views/common_components/izi_credit_payment_modal.php",
    "app/Views/common_components/partner_boost_button.php", "app/Views/common_components/qr_code_and_link.php",
    "app/Views/partners/campaigns/index.php", "app/Views/partners/campaigns/show.php",
    "app/Views/partners/requests/index.php", "app/Views/partners/operations/index.php",
]
LANG = ROOT / "app/Language/fr/PartnerStatic.php"
entries = {}

def key_for(value):
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")[:48] or "text"
    key = slug + "_" + hashlib.sha1(value.encode()).hexdigest()[:7]
    entries[key] = value
    return key

def translatable(value):
    value = html.unescape(value.strip())
    return bool(value and re.search(r"[A-Za-zÀ-ÿ]", value) and not re.fullmatch(r"[A-Z0-9_./:+ -]+", value))

def replace_text(match):
    raw = match.group(1)
    if "__PHP_" in raw or not translatable(raw): return match.group(0)
    lead = raw[:len(raw)-len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
    value = html.unescape(raw.strip())
    return ">" + lead + "<?= esc(lang('PartnerStatic.%s')) ?>" % key_for(value) + trail + "<"

def migrate(path):
    source = path.read_text(encoding="utf-8-sig")
    php = []
    def protect(m):
        php.append(m.group(0)); return "__PHP_%d__" % (len(php)-1)
    protected = re.sub(r"<\?(?:php|=)[\s\S]*?\?>", protect, source)
    protected = re.sub(r">([^<>]+)<", replace_text, protected)
    for attr in ("placeholder", "title", "aria-label"):
        pattern = re.compile(r'(%s=")([^"]+)(")' % attr)
        def repl(m):
            value = html.unescape(m.group(2).strip())
            if not translatable(value): return m.group(0)
            return m.group(1) + "__PHP_%d__" % len(php) + m.group(3)
        old_len=len(php)
        # Attribute PHP blocks are appended while replacing.
        def repl2(m):
            value=html.unescape(m.group(2).strip())
            if not translatable(value): return m.group(0)
            php.append("<?= esc(lang('PartnerStatic.%s'), 'attr') ?>" % key_for(value))
            return m.group(1)+"__PHP_%d__"%(len(php)-1)+m.group(3)
        protected=pattern.sub(repl2,protected)
    for i, block in enumerate(php): protected=protected.replace("__PHP_%d__"%i,block)
    path.write_text(protected, encoding="utf-8", newline="")

for rel in FILES:
    path=ROOT/rel
    if path.exists(): migrate(path)

lines=["<?php", "return ["]
for key,value in sorted(entries.items()):
    escaped=value.replace("\\","\\\\").replace("'","\\'")
    lines.append("    '%s' => '%s',"%(key,escaped))
lines.append("];\n")
LANG.write_text("\n".join(lines),encoding="utf-8",newline="")
print(f"Migrated {len(FILES)} views, {len(entries)} static strings")
