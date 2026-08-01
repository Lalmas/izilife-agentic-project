# izilife — Architecture technique

> Charger aussi : izilife-global.md

## Framework & structure
- CodeIgniter 4 (PHP MVC)
- MySQL — tables principales + tables staging (ScrapingEventTmp…)
- Comptes service dans table `Employee` (is_service_account, service_scopes JSON)
- Déploiement : local XAMPP → staging OVH → prod OVH via SSH/Git

---

## Tables principales (confirmées par SQL)

### Objets géolocalisés
- `Place` — lieux physiques (adresse, coord, google_place_id, google_place_details JSON, ai_description)
- `Shop` — commerces/établissements (séparation legacy avec Place)
- `LocalEvent` — événements (event_place, event_shop, event_serie_id, is_izilife_organizer_event…)
- `Experience` — expériences/activités
- `Equipment` — équipements urbains et de lieux (bookable, privatisable, bookable_per_team…)
- `Circuit` + `CircuitStep` + `CircuitRouteFile` + `CircuitTrackPoint` — parcours géolocalisés
- `Selection` — sélections/coffrets éditoriaux

### Contenus liés
- `LocalHabit` — habitude locale (scope: PLACE/SHOP/EVENT/EXPERIENCE…, weather_contexts, moment_contexts)
- `HourlyContent` — créneaux horaires (shop_id ou place_id)
- `EventProgrammation` — programmation dans un event (line-up, artistes…)
- `EventOrganizers` / `ExperienceOrganizers` — organisateurs
- `EventParticipant` — participants

---

## Deals / Promos — 3 couches distinctes (à bien comprendre)

### 1. Offer — promos d'un lieu (place/shop/partner)
Table `Offer` avec `scope_level` (shop|place|partner) + `scope_id`

**Sans `special_campain_id`** → promo libre du lieu (réduction, deal maison)

**Avec `special_campain_id`** → promo typée (référence `SpecialCampain`) :
- `happy-hour` → alimente la section Happy Hour
- `promo-etudiante` → alimente la section Étudiants
- `avantage-izilife` → deal négocié par izilife affiché sur la fiche
- `avantage-izipay`, `ladies-night`

**`OfferTime`** → créneaux horaires de l'offre (jours + heures, pour HH notamment)

**`OfferAccessCode`** → code digital qui déverrouille une Offer

### 2. BenefitPolicyRule — avantages izilife plan (ne sont PAS des Offer)
N'appartiennent à aucun lieu. Ce sont les avantages négociés par izilife liés à un plan d'abonnement.
Ex : "abonnés izilife+ ont -20% dans tous les bars partenaires".
Gérés dans `BoBenefits` controller, via `BenefitPolicyRule_model`.

### 3. ExternalPromotion — codes promos externes (influenceurs / sites)
Codes promos d'influenceurs ou de sites externes qui sont des **Pages** izilife (via `page_id`).
Distinct de Offer — ce ne sont pas des promos de lieux.

---

## Campagnes — 3 types distincts

Table `Campain` avec `campain_type_id` (référence `CampainType`) :

**`campagne-izilife`** → campagne éditoriale izilife (ex : Semaine de la Street Food, Saint-Valentin)
- Regroupe lieux, events, promos dans une section thématique
- Liée optionnellement à une `CelebrationDay`
- `CampainParticipation` : qui participe (place, shop, event, event_serie…)

**`campagne-partenaire`** → campagne d'un lieu/partner (ex : promo d'ouverture d'un restaurant)
- Liée à `partner_id`, `place_id` ou `shop_id`

**`campagne-publicitaire`** → paid placement (géré via `Placement`)
- `Placement` = table unifiée ad + highlight (paid_ad | highlight | opening_pack | editorial)

---

## Calendar Intelligence — CelebrationDay & jours fériés

### CelebrationDay — concepts de calendrier
Fête, solde, journée mondiale, événement local. Pas automatiquement un jour férié.
Ex : Noël = global + fixe 25/12. "Noël est férié en France" = dans HolidayRule.

**Tables :**
- `CelebrationDay` — concept (fixed/computed/imported/manual, fixed_day + fixed_month)
- `CelebrationType` — fête | solde | journée mondiale | événement local
- `CalendarCelebrationFamily` — civil | religious | commercial | cultural | sport | school | izilife
- `HolidayRule` — "dans ce scope, ce concept est férié" (scope: country, division, city)
- `CalendarOccurrence` — occurrence datée pour une année (celebration | public_holiday | school_holiday | bridge | campaign_moment)
- `CalendarSource` — source (manual | computed | official_api | external_api | import_file)

**Règle agent :** un cron annuel (ou agent) génère les `CalendarOccurrence` de l'année suivante
depuis les `HolidayRule` (fixes ou calculées — ex : Pâques). Les jours fériés français de l'API
`service-public.fr` peuvent aussi alimenter ça.

**Lien avec Campain :** `Campain.celebration_id` → FK vers `CelebrationDay`. 
La campagne St Valentin est automatiquement planifiable à partir de ce référentiel.

---

## Compétitions sportives

- `Competition` — compétition (Ligue 1, Roland-Garros, NBA…) liée à un `Sport`
- `CompetitionEdition` — édition/saison (starts_at, ends_at, is_featured_home)
- `SportMatch` — match dans une édition (participant_1_name, participant_2_name, starts_at, phase_label)
- Saisie manuelle en début de saison ou début de compétition
- `is_featured_home` sur Edition et Match → mise en avant sur la home

---

## Navigation

- `NavigationCategory` — arborescence de navigation (parent_id, active_month_from/to pour saisonnalité)
- `NavigationCategoryEntities` — quels types d'entités (`AppEntityType`) une catégorie affiche
- `AppEntityType` — shop | place | experience | event | circuit | session
- `UserTourismProfileType` — en famille | seul | en couple | entre amis | étudiant | touriste
- Catégories principales visibles : manger, boire, sortir, jouer, expériences, événements,
  happy-hour, deals, spotlights, nouveaux-lieux, escapades, terrasses (saisonnier)…

---

## Caractéristiques & Tags

- `ShopAndPlaceCharactTag` — tags (tag_types: PLACE/EVENT/EXPERIENCE/CAMPAIN/PARTNERS)
  - is_signal, signal_weight, usable_for_suggestion, usable_for_filter
- `PrincipalCharacteristics` — adapted_to_children, couples, groupes…
- `Hobby` + `HobbyCategory` — centres d'intérêt
- `TargetReason` — raisons de suggestion (HOBBY, OBJECT, ATMOSPHERE, TAG, LITTLE_ACTIVITY_OCCASION…)

---

## Référentiels de catégorisation

- `EventCategory` (arborescente, parent_id) — 130+ catégories
- `ActivityPrincipalCategory` — catégories d'activités
- `PlaceType`, `ShopCategory`
- `CircuitType`, `CircuitTheme`, `SportCircuitType`
- `EquipmentCategory`
- `ExperienceType`
- `SpecialCampain` — happy-hour | avantage-izilife | avantage-izipay | promo-etudiante | ladies-night
- `PromotionTarget` — tous | étudiants | membres | clients fidèles
- `PromotionMechanic` — réduction montant | pourcentage | X acheté Y offert | crédit | produit offert…

---

## Spotlight (moteur de règles)

- `SpotlightRule` + `SpotlightRuleCondition` + `SpotlightRuleEffect`
- `SpotlightTarget` + `TargetReason` + `TargetTourismProfile`

---

## Social / Communauté / Meetz

- `Community` + `CommunityMember`
- `UserGroup` + `UserGroupMember`
- `UserFollowing`, `UserFavorite`
- `Meetz*` — feature rencontres complète (MeetzEventCategory, MeetzZone, MeetzBooking, MeetzGroup…)

---

## Score de remplissage (completion score)

- Helper : `completion_score`
- Fonction : `LQ_refresh_completion_score($type, $id)`
- Types : place, shop, event, experience, equipment, circuit, selection
- Score bas → entre dans la file de l'Enrichisseur

---

## Controllers scrapping (Scraper.php)

### Méthodes autorisées aux agents (scope requis)
```
postScrapEventsFromBloggerWebsite($city_id, $type, $place_id)
postUploadEventImages($city_id, $type, $place_id)
postScrapExperiencesFromBloggerWebsite($city_id, $type, $place_id)
postUploadEventSources($city_id)
postUploadEventSourcesReplacement($city_id)
postFetchAndStoreOnePlace($city, $nextPageToken)     ← gère place, shop ET equipment
postFetchAndStorePlaces($city, $nextPageToken)
postAgentSuggestPlace($city)
postIngestJson()   ← À CRÉER (voir agents-socle.md)
```

### Méthodes INTERDITES aux agents
```
postClassifyPoi($city_id, $id)   ← humain uniquement (review + choix place/shop/equipment)
```

### Sécurité agents (implémentée)
```php
isServiceAccount()               // vérifie session employee + is_service_account
serviceHasScope(string $scope)   // lit service_scopes JSON
denyServiceAgentWithoutScope()   // 403 si compte service sans le bon scope
```

---

## Pipeline staging events/experiences (existant — NE PAS CASSER)

```
ScrapingEventTmp_model
  ->insert([...])
  ->urlRecentlyScraped($url, $days)
  ->fileRecentlyScraped($fingerprint, $days)
  ->rejectTmpEvent($tmpId, $bool)

ScrapingExperienceTmp_model
  ->insert([...])
  ->urlRecentlyScraped($url, $days)

ScrapingUnmappedPoi_model
  ->insert([...])   // lieux inconnus → classification manuelle via postClassifyPoi
```

---

## Libraries clés

```php
AIClient_lib          // client IA générique (switcher GPT/Claude)
OpenAI_lib            // client OpenAI
GooglePlace_lib       // Google Places API
Upload_lib            // upload médias
WebsiteParser_lib     // parser HTML
HtmlCleaner           // nettoyage HTML
BrightDataApiFetcher  // proxy scraping
EventSourceResolver
App\Libraries\Suggestions\*  // SuggestionEngine, CandidateNormalizer
```

---

## Variables d'environnement agents
```
LLM_PROVIDER=gpt          # gpt | claude | mistral
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_PLACES_API_KEY=...
GOOGLE_KEY_API=...
WHATSAPP_WEBHOOK_SECRET=...
AGENT_MODE=test            # test | production
```

---

## À créer

- `postIngestJson()` dans Scraper.php (voir agents-socle.md)
- Classe `App\Libraries\Agents\Agent` (voir agents-socle.md)
- Extension `postClassifyPoi()` pour supporter Equipment comme destination finale
- Agent CalendarOccurrence (cron annuel — génère occurrences depuis HolidayRule)
