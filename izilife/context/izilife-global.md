# izilife — Contexte global

## Vision produit
App web géolocalisée qui réunit tous les lieux, events, expériences,
bons plans, promos et codes promos d'une ville.
Promesse : retrouve toutes tes sorties et bons plans autour de toi.

Différenciation : mélange lieux + agenda + expériences locales + promos
dans une seule interface, avec moteurs par intention, annuaire, suggestion
et approche découverte (nouveaux lieux, spotlights, niches).

Statut : v2 en cours de finalisation. Lancement le 1er juin.

## Fondateur
Entrepreneur solo. Organise des events (quiz, blind test, Izilympics…)
pour financer la startup. Activités parallèles : agence com réseaux sociaux,
création sites WordPress.

---

## Objets métier (confirmés par tables.sql)

### Objets géolocalisés principaux
- **Place** — lieux physiques (restaurants, bars, musées, parcs…)
- **Shop** — commerces/établissements (séparation legacy avec Place)
- **LocalEvent** — événements (dans lieux/shops ou par organisateurs)
- **Experience** — expériences/activités (cours, visites, ateliers…)
- **Equipment** — équipements urbains et de lieux (tables, terrains, bornes…)
- **Circuit** + **CircuitStep** — parcours géolocalisés (touristiques, sportifs)
- **Selection** — sélections/coffrets éditoriaux

### Contenus éditoriaux liés
- **LocalHabit** — habitude locale d'un lieu/event/experience
- **ShopAndPlaceCharactTag** — tags caractéristiques (terrasse, rooftop, kids-friendly…)
- **EventProgrammation** — line-up dans un event (artistes, DJs…)

### Deals / Promos (3 couches distinctes — ne pas confondre)
- **Offer** (avec OfferTime) — promos d'un lieu : HH, promo étudiante, avantage izilife (special_campain_id)
- **BenefitPolicyRule** — avantages izilife plan négocié, PAS lié à un lieu (dans BoBenefits)
- **ExternalPromotion** — codes promos d'influenceurs/sites via page_id (Pages izilife)

### Campagnes (3 types)
- **Campain ** — éditoriale izilife liée à une CelebrationDay (St Valentin, Street Food…)
- **Campain ** — campagne d'un lieu/partner
- **Campain ** — paid ads via Placement

### Calendrier
- **CelebrationDay** — concept de fête/date (Noël, St Valentin, jours fériés…)
- **HolidayRule** — "dans ce scope, ce concept est férié" (par pays/division/ville)
- **CalendarOccurrence** — occurrence datée pour une année (générée par agent annuel)

### Compétitions sportives
- **Competition** + **CompetitionEdition** + **SportMatch** — saisie manuelle en début de saison

### Référentiels
- **EventCategory** (arborescente, 130+ catégories)
- **ActivityPrincipalCategory**, **PlaceType**, **ShopCategory**
- **CircuitType**, **CircuitTheme**, **SportCircuitType**
- **Hobby** + **HobbyCategory** (centres d'intérêt)

### Social / Communauté
- **Community**, **UserGroup** — communautés et groupes
- **Meetz** — feature rencontres (MeetzEventCategory, MeetzZone, MeetzBooking…)

### Moteurs
- **SpotlightRule** + conditions + effects — moteur de règles de mise en avant
- **TargetReason** — raisons de suggestion (HOBBY, TAG, ATMOSPHERE…)
- Score de remplissage (completion_score) sur Place, Shop, Event, Experience, Equipment, Circuit

---

## Stack technique
- **Framework** : CodeIgniter 4 (PHP MVC)
- **BDD** : MySQL — tables principales + tables staging (ScrapingEventTmp…)
- **Hébergement** : OVH mutualisé (staging + prod), SSH disponible
- **Local** : Windows + XAMPP (dev PHP)
- **IA** : OpenAI_lib (actuel), AIClient_lib (générique), Claude API (variable à activer)
- **Scraping** : BrightDataApiFetcher, WebsiteParser_lib, HtmlCleaner
- **Outils agents** : Claude Code, Claude in Chrome (CIC), Cowork
- **Hub données** : Google Sheets (planning + file de tâches agents)
- **Versioning** : Git (local → OVH)

---

## Contraintes actuelles
- Abonnement Claude Pro 20€/mois (pas encore Max 200€)
- Pas de PC fixe dédié agents (prévu — Dell OptiPlex reconditionné)
- CIC et Cowork : construits et testés, **désactivés en production** jusqu'à Max 200€
- Google Places API : free tier ~28 000 requêtes/mois — ne jamais relancer une ville déjà scannée
- OVH mutualisé : SSH disponible mais pas npm/node → Claude Code tourne en local uniquement

---

## Architecture agents — règles immuables
1. Tout agent = un `.md` (cerveau) + un script PHP (bras) + `postIngestJson()` (sortie)
2. Tout passe par staging/tmp → validation humaine → prod. **Jamais d'écriture directe.**
3. 0 token pour la structure (Places API, crons, parsing HTML statique)
4. Tokens uniquement pour l'intelligence (CIC, OCR, génération)
5. Switcher GPT / Claude / Mistral = 1 variable `LLM_PROVIDER`
6. Chaque appel LLM est **indépendant** (pas de contexte qui grossit en boucle)
7. Le `.md` = prompt système fixe injecté à chaque appel

---

## Sécurité agents (implémentée dans Scraper.php)
- Comptes service : `is_service_account` + `service_scopes` JSON dans `Employee`
- `isServiceAccount()` + `serviceHasScope($scope)` + `denyServiceAgentWithoutScope($scope)`
- Filtre global : agents bloqués sur toutes les méthodes sauf celles listées
- Staging avant prod, toujours — validation humaine sur tout ce qui vient des agents

---

## Priorités du moment
1. Équipe agents opérationnelle pour le 1er juin ← priorité absolue
2. Fix bugs & requêtes SQL nouvelles sections (staging)
3. Méthode `postIngestJson()` + classe `Agent` PHP (tuyau commun)
4. Curation manuelle contenu lancement
5. Agents réseaux sociaux (posture fédérateur)
6. Agent événements & animation

---

## Organisation des conversations Claude
- Toujours charger ce fichier en premier
- Puis charger le(s) .md correspondant au chantier (voir README.md)
- Une conversation par chantier — ne pas mélanger
# Décisions structurelles V2 confirmées le 9 août 2026

- La création manuelle des Place, Shop, Event et Experience part de leur liste BO ; la ville obligatoire est choisie dans le formulaire.
- `city_id` reste le cœur de l'architecture de recherche. Il n'est jamais synthétisé depuis `AdministrativeDivision.city_id`.
- Une Experience peut avoir des lieux de séance dans des villes voisines sans changer sa ville cœur.
- Les Community forment l'arbre d'antennes. Les UserGroup sont des subdivisions internes terminales, sans sous-groupes ni versement propre.
- Une Community a toujours un administrateur User ; son Partner juridique/financier reste facultatif.
