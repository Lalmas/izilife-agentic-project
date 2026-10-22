import pathlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')

root = pathlib.Path(r"C:\xampp\htdocs\izilife-partner-admin")
files = [
 "app/Views/partners/billing/index.php", "app/Views/partners/billing/payment.php",
 "app/Views/partners/boost_configure.php", "app/Views/partners/finance/index.php",
 "app/Views/partners/location_features.php", "app/Views/partners/offers/form.php",
 "app/Views/partners/offers/index.php", "app/Views/partners/partner_boost_index.php",
 "app/Views/partners/partner_places.php", "app/Views/partners/reservation_management.php",
 "app/Views/partners/settings_banking.php", "app/Views/common_components/izi_credit_payment_modal.php",
 "app/Views/common_components/partner_boost_button.php", "app/Views/common_components/qr_code_and_link.php",
 "app/Views/partners/campaigns/index.php", "app/Views/partners/campaigns/show.php",
 "app/Views/partners/campaigns/participate.php", "app/Views/partners/campaigns/participate_human.php",
 "app/Views/partners/requests/index.php", "app/Views/partners/operations/index.php",
]
problems=[]
for rel in files:
    source=(root/rel).read_text(encoding="utf-8-sig")
    source=re.sub(r"<script[\s\S]*?</script>","",source,flags=re.I)
    source=re.sub(r"<style[\s\S]*?</style>","",source,flags=re.I)
    source=re.sub(r"<\?(?:php|=)[\s\S]*?\?>","",source)
    for match in re.finditer(r">\s*([^<>]+?)\s*<",source):
        value=match.group(1).strip()
        if re.search(r"[A-Za-zÀ-ÿ]",value): problems.append((rel,value))
    for match in re.finditer(r'(?:placeholder|title|aria-label)="([^"]*[A-Za-zÀ-ÿ][^"]*)"',source):
        problems.append((rel,match.group(1)))
for rel,value in problems: print(f"{rel}: {value}")
print(f"STATIC_TEXT_PROBLEMS={len(problems)}")
