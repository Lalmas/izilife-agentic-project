from pathlib import Path

root = Path(r"C:\xampp\htdocs\izilife-partner-admin")
changes = {
 "app/Views/partners/location_features.php": {
  "$l->place_type==='SHOP'?'Commerce':'Lieu'": "$l->place_type==='SHOP'?lang('PartnerStatic.location_shop'):lang('PartnerStatic.location_place')",
  "$f['active']?'Activée':'Activer'": "lang($f['active']?'PartnerStatic.feature_enabled':'PartnerStatic.feature_enable')",
 },
 "app/Views/partners/billing/index.php": {
  "?> · jusqu’au <?=": "?> · <?=esc(lang('PartnerStatic.until'))?> <?=",
  "<br>Délai de grâce jusqu’au <?=": "<br><?=esc(lang('PartnerStatic.grace_until'))?> <?=",
  "?>. Les nouvelles tentatives de paiement iziLife restent actives.": "?>. <?=esc(lang('PartnerStatic.payment_attempts_active'))?>",
  "$price->interval_unit==='year'?'annuel':'mensuel'": "$price->interval_unit==='year'?lang('PartnerStatic.annual'):lang('PartnerStatic.monthly')",
  "$price->interval_unit==='year'?'Deux mois offerts.':'Renouvellement mensuel.'": "$price->interval_unit==='year'?lang('PartnerStatic.two_months_free'):lang('PartnerStatic.monthly_renewal')",
  "?> crédits par période</p>": "?> <?=esc(lang('PartnerStatic.credits_per_period'))?></p>",
 },
 "app/Views/partners/billing/payment.php": {
  ">Montant à régler : <?=esc(number_format((float)$tx->amount,2,',',' '))?> €</p>": "><?=esc(lang('PartnerStatic.amount_due',[number_format((float)$tx->amount,2,',',' '),'€']))?></p>",
  "<strong><?=number_format($creditsReserved,0,',',' ')?> crédits iziLife réservés.</strong>": "<strong><?=esc(lang('PartnerStatic.credits_reserved',[number_format($creditsReserved,0,',',' ')]))?></strong>",
  "?' · Par défaut':''": "?' · '.lang('PartnerStatic.default_method'):''",
 },
 "app/Views/partners/campaigns/index.php": {
  "$m->moment_kind==='annual_edition'?'Fête locale':'Temps fort iziLife'": "$m->moment_kind==='annual_edition'?lang('PartnerStatic.local_festival'):lang('PartnerStatic.izilife_moment')",
 },
 "app/Views/partners/partner_places.php": {
  "<?= $totalCount ?> lieu<?= $totalCount > 1 ? 'x' : '' ?>": "<?= esc(lang($totalCount > 1 ? 'PartnerStatic.places_count' : 'PartnerStatic.place_count', [$totalCount])) ?>",
  "'label'=>'Booster '.$item->name": "'label'=>lang('PartnerStatic.boost_object', [$item->name])",
 },
 "app/Views/partners/requests/index.php": {
  "<?= esc($type) ?></option>": "<?= esc(partner_enum_label('request',$type)) ?></option>",
  "name=\"object_type\" required><?php foreach($object_types as $type): ?><option value=\"<?= esc($type) ?>\"><?= esc(partner_enum_label('request',$type)) ?>": "name=\"object_type\" required><?php foreach($object_types as $type): ?><option value=\"<?= esc($type) ?>\"><?= esc(partner_enum_label('object',$type)) ?>",
  "?:'Contenu indisponible'": "?:lang('PartnerStatic.content_unavailable')",
 },
 "app/Views/partners/offers/form.php": {
  "$editing?'Modifier l’offre':'Créer une offre'": "$editing?lang('PartnerStatic.edit_offer'):lang('PartnerStatic.create_offer')",
  "[['special','Spéciale','Happy Hour, étudiante…'],['classic','Classique','Promotion locale temporaire'],['operation','Opération','Cash ou Last Minute']]": "[['special',lang('PartnerStatic.special'),lang('PartnerStatic.special_help')],['classic',lang('PartnerStatic.classic'),lang('PartnerStatic.classic_help')],['operation',lang('PartnerStatic.operation'),lang('PartnerStatic.operation_help')]]",
  "['product'=>'Tous les produits','product_category'=>'Toutes les catégories','eap'=>'Tous les tarifs','service'=>'Tous les services','equipment'=>'Tous les équipements']": "['product'=>lang('PartnerStatic.all_products'),'product_category'=>lang('PartnerStatic.all_categories'),'eap'=>lang('PartnerStatic.all_prices'),'service'=>lang('PartnerStatic.all_services'),'equipment'=>lang('PartnerStatic.all_equipments')]",
  "[1=>'Lun',2=>'Mar',3=>'Mer',4=>'Jeu',5=>'Ven',6=>'Sam',7=>'Dim']": "[1=>lang('PartnerStatic.mon'),2=>lang('PartnerStatic.tue'),3=>lang('PartnerStatic.wed'),4=>lang('PartnerStatic.thu'),5=>lang('PartnerStatic.fri'),6=>lang('PartnerStatic.sat'),7=>lang('PartnerStatic.sun')]",
 },
 "app/Views/partners/offers/index.php": {
  "'label'=>'Booster '.$o->title": "'label'=>lang('PartnerStatic.boost_object', [$o->title])",
  "$special?'Spéciale':(((string)($o->offer_kind??'CLASSIC')==='OPERATION')?'Opération':'Classique')": "$special?lang('PartnerStatic.special'):(((string)($o->offer_kind??'CLASSIC')==='OPERATION')?lang('PartnerStatic.operation'):lang('PartnerStatic.classic'))",
 },
 "app/Views/partners/campaigns/show.php": {
  "?:'Contenu indisponible'": "?:lang('PartnerStatic.content_unavailable')",
  "esc($b->surface.' · '.$b->starts_at)": "esc(partner_enum_label('surface',$b->surface).' · '.$b->starts_at)",
 },
 "app/Views/partners/campaigns/participate_human.php": {
  ">Créer une offre</a>": "><?=esc(lang('PartnerStatic.create_offer'))?></a>",
  ">← Temps forts</a>": "><?=esc(lang('PartnerStatic.back_moments'))?></a>",
  ">Choisissez le contenu que vous souhaitez rattacher à ce temps fort.</p>": "><?=esc(lang('PartnerStatic.choose_moment_content'))?></p>",
  ">Participer avec une offre</h3>": "><?=esc(lang('PartnerStatic.join_with_offer'))?></h3>",
  ">Créez une nouvelle offre déjà rattachée, ou choisissez une offre existante.</p>": "><?=esc(lang('PartnerStatic.join_offer_help'))?></p>",
  ">Choisir une offre…</option>": "><?=esc(lang('PartnerStatic.choose_offer'))?></option>",
  ">Participer</button>": "><?=esc(lang('PartnerStatic.participate'))?></button>",
  ">Participer avec un événement</h3>": "><?=esc(lang('PartnerStatic.join_with_event'))?></h3>",
  ">Rattachez un événement que votre équipe organise.</p>": "><?=esc(lang('PartnerStatic.join_event_help'))?></p>",
  ">Choisir un événement…</option>": "><?=esc(lang('PartnerStatic.choose_event'))?></option>",
  ">Rattacher votre événement</h3>": "><?=esc(lang('PartnerStatic.attach_your_event'))?></h3>",
  ">L’événement sera associé à cette édition locale.</p>": "><?=esc(lang('PartnerStatic.attach_local_help'))?></p>",
  ">Rattacher</button>": "><?=esc(lang('PartnerStatic.attach'))?></button>",
 },
 "app/Views/partners/campaigns/participate.php": {
  ">← Temps forts</a>": "><?=esc(lang('PartnerStatic.back_moments'))?></a>",
  ">Choisissez un contenu existant ou créez une nouvelle offre pour ce temps fort.</p>": "><?=esc(lang('PartnerStatic.choose_or_create_content'))?></p>",
  ">Créer une offre pour ce temps fort</a>": "><?=esc(lang('PartnerStatic.create_offer_for_moment'))?></a>",
  ">Une offre</option>": "><?=esc(lang('PartnerStatic.one_offer'))?></option>",
  ">Un événement</option>": "><?=esc(lang('PartnerStatic.one_event'))?></option>",
  ">Offre — <?=": "><?=esc(lang('PartnerStatic.offer_prefix'))?> <?=",
  ">Événement — <?=": "><?=esc(lang('PartnerStatic.event_prefix'))?> <?=",
  ">Participer</button>": "><?=esc(lang('PartnerStatic.participate'))?></button>",
  ">Votre événement à rattacher à cette édition</label>": "><?=esc(lang('PartnerStatic.event_to_attach'))?></label>",
  ">Rattacher</button>": "><?=esc(lang('PartnerStatic.attach'))?></button>",
 },
 "app/Views/partners/operations/index.php": {
  ">Réservation n°<?=": "><?=esc(lang('PartnerStatic.booking_number'))?> <?=",
 },
 "app/Views/partners/analytics/human_index.php": {
  "?: 'Contenu indisponible'": "?: lang('PartnerStatic.content_unavailable')",
 },
 "app/Views/partners/reservation_management.php": {
  "?> — tables, privatisations et demandes</p>": "?> — <?=esc(lang('PartnerStatic.reservation_context_help'))?></p>",
  ">Réservations (<?=count($bookings)?>)</button>": "><?=esc(lang('PartnerStatic.bookings_count',[count($bookings)]))?></button>",
  ">Demandes (<?=count($requests)?>)</button>": "><?=esc(lang('PartnerStatic.requests_count',[count($requests)]))?></button>",
  "<?=esc($b->party_size)?> personne(s)": "<?=esc(lang('PartnerStatic.people_count',[$b->party_size]))?>",
  "$b->equipment_name?:'Table non attribuée'": "$b->equipment_name?:lang('PartnerStatic.table_unassigned')",
  "esc($c->confirmation_mode)": "esc(partner_enum_label('confirmation',$c->confirmation_mode))",
  "$c->automatic_resource_allocation?'allocation simple':'allocation manuelle'": "$c->automatic_resource_allocation?lang('PartnerStatic.simple_allocation'):lang('PartnerStatic.manual_allocation')",
  "$c->is_published?'Publiée sur iziLife':'Non publiée'": "$c->is_published?lang('PartnerStatic.published_izilife'):lang('PartnerStatic.not_published')",
  "$c->is_published?'Retirer du public':'Activer et publier'": "$c->is_published?lang('PartnerStatic.remove_public'):lang('PartnerStatic.enable_publish')",
  "$c->is_paused?'Réactiver':'Pause'": "$c->is_paused?lang('PartnerStatic.reactivate'):lang('PartnerStatic.pause')",
  "value=\"Réservation de table\"": "value=\"<?=esc(lang('PartnerStatic.booking_name_default'),'attr')?>\"",
  "value=\"Réserver une table\"": "value=\"<?=esc(lang('PartnerStatic.booking_public_default'),'attr')?>\"",
  "?' (principale)':''": "?' ('.esc(lang('PartnerStatic.principal')).')':''",
  "['capacity'=>'Capacité/créneau','min_party_size'=>'Minimum','max_party_size'=>'Maximum','min_booking_notice_minutes'=>'Préavis (minutes)']": "['capacity'=>lang('PartnerStatic.capacity_slot'),'min_party_size'=>lang('PartnerStatic.minimum'),'max_party_size'=>lang('PartnerStatic.maximum'),'min_booking_notice_minutes'=>lang('PartnerStatic.notice_minutes')]",
  "[1=>'Lun',2=>'Mar',3=>'Mer',4=>'Jeu',5=>'Ven',6=>'Sam',7=>'Dim']": "[1=>lang('PartnerStatic.mon'),2=>lang('PartnerStatic.tue'),3=>lang('PartnerStatic.wed'),4=>lang('PartnerStatic.thu'),5=>lang('PartnerStatic.fri'),6=>lang('PartnerStatic.sat'),7=>lang('PartnerStatic.sun')]",
 },
}

for rel, replacements in changes.items():
    path = root / rel
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

reservation = root / "app/Views/partners/reservation_management.php"
text = reservation.read_text(encoding="utf-8")
marker = "<?php if($canEdit):?><script>"
if marker in text:
    text = text.split(marker, 1)[0] + """<?php if($canEdit):?>
<script>
document.addEventListener('DOMContentLoaded',()=>{
 const form=document.querySelector('form[action*=\"saveConfiguration\"]');if(!form)return;
 const submit=form.querySelector('button[type=\"submit\"],button.btn-primary');if(!submit)return;
 const labels=<?=json_encode(['special'=>lang('PartnerStatic.configuration_speciale_brunch_94f9116'),'start'=>lang('PartnerStatic.debut_f095531'),'end'=>lang('PartnerStatic.fin_4251065'),'formula'=>lang('PartnerStatic.formule_1bb7d65'),'menu'=>lang('PartnerStatic.menu_57f5f5e'),'buffet'=>lang('PartnerStatic.buffet_cdfeebf'),'mixed'=>lang('PartnerStatic.buffet_menu_2ba4ff1'),'price'=>lang('PartnerStatic.prix_adulte_e22241c'),'required'=>lang('PartnerStatic.reservation_obligatoire_2e9b6fc')],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?>;
 const wrap=document.createElement('div');wrap.className='col-12 border rounded p-3';wrap.innerHTML=`<label class=\"form-check\"><input class=\"form-check-input\" type=\"checkbox\" name=\"is_special_for_brunch\" value=\"1\"> ${labels.special}</label><div class=\"row g-3 mt-1 d-none\" data-brunch-fields><div class=\"col-md-3\"><label class=\"form-label\">${labels.start}</label><input class=\"form-control\" type=\"time\" name=\"brunch_time_from\"></div><div class=\"col-md-3\"><label class=\"form-label\">${labels.end}</label><input class=\"form-control\" type=\"time\" name=\"brunch_time_to\"></div><div class=\"col-md-3\"><label class=\"form-label\">${labels.formula}</label><select class=\"form-select\" name=\"brunch_service_type\"><option value=\"menu\">${labels.menu}</option><option value=\"buffet\">${labels.buffet}</option><option value=\"mixed\">${labels.mixed}</option></select></div><div class=\"col-md-3\"><label class=\"form-label\">${labels.price}</label><input class=\"form-control\" type=\"number\" min=\"0\" step=\"0.01\" name=\"brunch_price\"></div><div class=\"col-md-4\"><label class=\"form-check\"><input class=\"form-check-input\" type=\"checkbox\" name=\"brunch_reservation_required\" value=\"1\"> ${labels.required}</label></div></div>`;
 submit.closest('.col-12').before(wrap);const toggle=wrap.querySelector('[name=\"is_special_for_brunch\"]'),fields=wrap.querySelector('[data-brunch-fields]'),hours=form.querySelector('[name=\"hours\"]');const refresh=()=>{fields.classList.toggle('d-none',!toggle.checked);fields.querySelectorAll('input,select').forEach(x=>x.disabled=!toggle.checked);if(hours)hours.required=!toggle.checked};toggle.addEventListener('change',refresh);refresh();
});
</script>
<?php endif?>
"""
    reservation.write_text(text, encoding="utf-8")

payment = root / "app/Views/partners/billing/payment.php"
text = payment.read_text(encoding="utf-8")
marker = '<script src="https://js.stripe.com/v3/"></script>'
if marker in text:
    text = text.split(marker, 1)[0] + marker + """<script>
const stripe=Stripe(<?=json_encode($provider_public_key)?>),txUid=<?=json_encode($tx->unique_id)?>;let elements,paymentElement;
const messages=<?=json_encode(['unavailable'=>lang('PartnerStatic.stripe_form_unavailable'),'slow'=>lang('PartnerStatic.stripe_form_slow')],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)?>;
const showError=message=>{const element=document.getElementById('payment-error');element.textContent=message;element.classList.remove('d-none')};
async function post(url,data){const response=await fetch(url,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data)}),json=await response.json();if(!response.ok||!json.ok)throw new Error(json.error||'PAYMENT_FAILED');return json}
async function initialize(){const json=await post(<?=json_encode(base_url('payment/createIntent'))?>,{tx_uid:txUid});elements=stripe.elements({clientSecret:json.client_secret,loader:'auto'});paymentElement=elements.create('payment');paymentElement.on('ready',()=>{document.getElementById('pay-button').disabled=false});paymentElement.on('loaderror',event=>showError(event?.error?.message||messages.unavailable));paymentElement.mount('#payment-element');setTimeout(()=>{if(document.getElementById('pay-button').disabled)showError(messages.slow)},8000)}
document.getElementById('pay-button').addEventListener('click',async()=>{try{const result=await stripe.confirmPayment({elements,confirmParams:{return_url:<?=json_encode(base_url('payment/return?tx='))?>+encodeURIComponent(txUid)}});if(result.error)showError(result.error.message)}catch(error){showError(error.message)}});
document.querySelectorAll('.saved-method').forEach(button=>button.addEventListener('click',async()=>{try{const json=await post(<?=json_encode(base_url('payment/confirmSaved'))?>,{tx_uid:txUid,method_id:button.dataset.methodId});if(json.status==='requires_action'&&json.client_secret){const result=await stripe.handleCardAction(json.client_secret);if(result.error)return showError(result.error.message)}location.href=<?=json_encode(base_url('payment/return?tx='))?>+encodeURIComponent(txUid)}catch(error){showError(error.message)}}));
initialize().catch(error=>showError(error.message));
</script>
"""
    payment.write_text(text, encoding="utf-8")
