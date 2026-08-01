# IZILIFE - Contexte long projet

Date d'initialisation : 2026-07-02

Ce document sert de contexte de dÃ©part pour travailler sur l'ensemble du projet Izilife dans ce workspace. Il regroupe la vision produit, les rÃ¨gles de collaboration, l'architecture multi-apps, les objets mÃ©tier, les zones de code importantes et les prÃ©cautions Ã  respecter avant toute modification.

## RÃ¨gles immuables de travail

- Ne jamais lire, ouvrir, indexer, copier, rÃ©sumer ou modifier un fichier `.env`, `.env*`, `env` ou tout fichier assimilable Ã  des secrets.
- Ne jamais rechercher volontairement des secrets, tokens, mots de passe, clÃ©s API, credentials DB ou donnÃ©es privÃ©es.
- Ne jamais commencer Ã  modifier plusieurs zones du projet sans annoncer les fichiers et l'intention de modification.
- Le projet est vaste : toute intervention doit Ãªtre ciblÃ©e, prÃ©cÃ©dÃ©e d'une lecture locale du code concernÃ©, puis vÃ©rifiÃ©e.
- Ne pas toucher aux dossiers gÃ©nÃ©rÃ©s ou volumineux sauf nÃ©cessitÃ© : `system/`, `writable/`, `.git/`, `vendor/`, `node_modules/`, sessions publiques, archives legacy.
- Les apps partagent le mÃªme domaine mÃ©tier et probablement la mÃªme base MySQL ; les changements de schÃ©ma ou de contrat doivent Ãªtre pensÃ©s multi-apps.
- Les flux agents/scraping doivent rester en staging/tmp puis validation humaine avant production. Pas d'Ã©criture directe automatisÃ©e en prod.

## Source de contexte initiale

Sources prises en compte pour cette premiÃ¨re mise en contexte :

- `C:\Users\alcamara\Documents\agentic_Workspace\izilife\context\izilife-global.md`
- `C:\Users\alcamara\Documents\agentic_Workspace\izilife\context\Docs\Description izilife chat gpt.pdf`
- `C:\Users\alcamara\Documents\agentic_Workspace\izilife\context\Docs\ChatGPT Image 17 mai 2026, 09_37_17.png`
- Inventaire local non secret des apps :
  - `C:\xampp\htdocs\izilife`
  - `C:\xampp\htdocs\izilife-admin`
  - `C:\xampp\htdocs\izilife-partner-admin`
  - `C:\xampp\htdocs\izilife-partner`
- SchÃ©ma SQL :
  - `C:\xampp\htdocs\izilife-admin\statics\izilife_new_version`

## Vision produit

Izilife est une super-app locale et sociale pour dÃ©couvrir, choisir, rÃ©server et payer des sorties autour de soi. Le produit agrÃ¨ge lieux, commerces, Ã©vÃ©nements, expÃ©riences, bons plans, menus, services, offres et recommandations dans une interface gÃ©olocalisÃ©e.

La promesse centrale : retrouver toutes ses sorties, lieux utiles, activitÃ©s et bons plans autour de soi, avec une logique de ville et d'intention.

DiffÃ©renciation :

- mÃ©lange annuaire local + agenda + expÃ©riences + promos ;
- dÃ©couverte par intention : manger, boire, danser, se balader, bruncher, jouer, sortir, etc. ;
- dÃ©couverte par gÃ©olocalisation, catÃ©gories, hobbies, tags, atmosphÃ¨res, spotlights et sÃ©lections Ã©ditoriales ;
- capacitÃ© transactionnelle : rÃ©servation, paiement, QR code, menu, commande d'avance, avantages Izilife Plan.

## Applications du workspace

### Front public

Chemin : `C:\xampp\htdocs\izilife`

RÃ´le :

- interface publique utilisateur ;
- accueil et pages de dÃ©couverte ;
- pages Place, Shop, Event, Experience, Selection ;
- recherche par texte/catÃ©gorie/intention ;
- profils et comptes utilisateurs ;
- favoris, listes, agenda utilisateur, achats, droits d'usage ;
- Izilife Plan, bÃ©nÃ©fices, abonnements ;
- Meetz, booking et paiement cÃ´tÃ© utilisateur ;
- webhooks Stripe cÃ´tÃ© front.

Points d'entrÃ©e observÃ©s :

- routes dÃ©clarÃ©es dans `app\Config\Routes.php` :
  - `/` -> `Home::getIndex`
  - `l/{slug}` -> `LocationResolver::bySlug`
  - `webhooks/stripe` -> `Webhooks\Stripe::index`
  - `user/purchases*` -> usages/achats utilisateur
  - `que-faire*` -> `Whattodo::activity`
- beaucoup de surface est probablement portÃ©e par auto-routing / conventions de contrÃ´leurs.

ContrÃ´leurs majeurs :

- `Home.php` : accueil, profil touristique, page d'entrÃ©e.
- `Whattodo.php` : moteur "que faire" par intention, catÃ©gories et sources.
- `Search.php` : recherche par catÃ©gorie, texte, rÃ©sultats.
- `Place.php` : page lieu, agenda, autour, expÃ©riences, avis, photos, liens, tabs.
- `Shop.php` : page commerce, menu, agenda, Ã©quipements, avis, autour, liens.
- `Event.php` : page event, programme, tickets, paiement, intÃ©rÃªts, avis.
- `Experience.php` : page expÃ©rience, photos, avis, liens.
- `IzilifeSelection.php` : sÃ©lections/coffrets, participations, avis, filtres.
- `IzilifePlan.php` : abonnement, changement de plan, consommation de bÃ©nÃ©fices.
- `IzilifeMeetz.php` : onboarding Meetz, planning, booking, paiement, prÃ©fÃ©rences.
- `User.php` : authentification, inscription, profil, favoris, listes, agenda, achats, abonnements.

Vues structurantes observÃ©es :

- `app\Views\layouts`
- `app\Views\places`, `shops`, `events`, `experiences`, `selections`
- `app\Views\search`, `swipers`, `zooming_swipers`, `overflow_swipers`
- `app\Views\users`, `benefits`, `cart`, `payment`, `subscription`
- `app\Views\meetz`

Note technique : le `composer.json` du front indique encore `codeigniter/framework` avec PHP `>=5.3.7`, alors que la structure locale ressemble Ã  CodeIgniter 4 (`app\Config`, `BaseController`, `spark`, namespace CI4 dans plusieurs zones). Ã€ vÃ©rifier avant toute intervention Composer.

### Back-office principal

Chemin : `C:\xampp\htdocs\izilife-admin`

RÃ´le :

- coeur de la gestion ;
- CRUD et enrichissement des objets mÃ©tier ;
- gestion Place, Shop, Event, Experience, Equipment, Animation, Product, EAP, ElementService ;
- partenaires, PSP, rÃ©munÃ©rations, paiements, Stripe onboarding ;
- scraping, agents, validation humaine, imports Google/agenda/sports ;
- rÃ©fÃ©rentiels et configurations ;
- campagnes, avantages, plans, promos, newsletters, spotlight.

Routes dÃ©clarÃ©es :

- `/` -> `Exploitation::getIndex`
- `stripe/webhook` -> `StripeWebhook::index`
- groupe `psp/onboarding/*` -> `PspOnboarding`

ContrÃ´leurs majeurs :

- `Place.php` : gestion complÃ¨te lieux, Google enrichissement, mÃ©dias, horaires, Ã©quipements, booking conf, intÃ©rÃªts, zones internes.
- `Shop.php` : gestion complÃ¨te commerces, lieux itinÃ©rants, horaires, repas, Ã©quipements, booking conf, caractÃ©ristiques, mÃ©dias.
- `Event.php` : gestion complÃ¨te Ã©vÃ©nements, programmation, dates, rÃ©currences, tarifs, participants, animations, mÃ©dias.
- `Experience.php` : gestion expÃ©riences, sessions, accÃ¨s, mÃ©dias, hobbies.
- `Partner.php` : gestion partenaires.
- `Scraper.php` : orchestration scraping, validation requests, endpoints agents, enrichissements, imports.
- `Product.php` : produits, prix, options, composÃ©s.
- `AccessPrice.php` : ElementAccessPrice / EAP, tarifs d'entrÃ©e, packs, prix groupÃ©s, liens catÃ©gories/Ã©quipements.
- `ElementService.php` : services proposÃ©s, catÃ©gories, options, attributs, bundles.
- `Equipment.php` : Ã©quipements, booking conf, mÃ©dias.
- `Animation.php` : animations/attractions rattachÃ©es Ã  des objets, booking conf.
- `PspOnboarding.php` : onboarding PSP/Stripe pour entitÃ©s.

Vues structurantes observÃ©es :

- `app\Views\layouts`
- `places`, `shops`, `events`, `experiences`, `equipments`, `animations`
- `products`, `element_service`, `bo_benefits`, `bo_access_policy`, `bo_plans`
- `partners`, `psp`, `remunerations`, `transactions`
- `scraping`, `review_moderation`, `spotlights`
- `bo_sport_competition`, `bo_celebration_day`, `bo_external_promo`

### Espace partner admin

Chemin : `C:\xampp\htdocs\izilife-partner-admin`

RÃ´le :

- interface admin cÃ´tÃ© partenaire ;
- version restreinte/filtrÃ©e de la gestion BO ;
- accÃ¨s partner sur ses shops, places, events, experiences, employÃ©s et PSP ;
- forte rÃ©utilisation ou copie de structures BO avec restrictions par partner.

Routes dÃ©clarÃ©es :

- `/` -> `Welcome::getIndex`
- callbacks Stripe partner/place/shop
- groupe `psp/onboarding/*` -> `PspOnboarding`

ContrÃ´leurs majeurs observÃ©s :

- `Welcome.php` : entrÃ©e partner.
- `Place.php` : liste/show des lieux du partner, sections normalisÃ©es.
- `Shop.php` : show des commerces du partner.
- `Event.php` : CRUD Ã©vÃ©nement partner, contrÃ´le d'appartenance partner, tarifs, organisateurs, horaires, mÃ©dias, participants, rÃ©munÃ©rations, rÃ©currences.
- `Experience.php` : CRUD expÃ©rience partner, sessions, accÃ¨s, mÃ©dias, langues, hobbies.
- `Employee.php` : employÃ©s partner, login, MFA/2FA, reset password, scopes.
- `PspOnboarding.php` : onboarding PSP/Stripe.

Vues structurantes observÃ©es :

- `layouts`
- `places`, `shops`, `events`, `experiences`
- `partners`, `employees`, `psp`
- beaucoup de vues BO recopiÃ©es/adaptÃ©es, y compris `common_components`.

### Front partner pro futur

Chemin prÃ©vu : `C:\xampp\htdocs\izilife-partner`

Ã‰tat observÃ© : dossier existant mais vide au moment de l'analyse.

RÃ´le prÃ©vu :

- futur front professionnel partenaire ;
- probablement interface publique/produit destinÃ©e aux partenaires, distincte de l'espace admin partner.

## ModÃ¨le mÃ©tier principal

### Objets geolocalises et editoriaux

- `Place` : lieu physique, adresse, coordonnees, typologie, ville/division, equipements, agenda, avis, medias, acces.
- `Shop` : commerce/etablissement. Separation legacy avec `Place`; un shop peut posseder des places, horaires, menus, offres, caracteristiques.
- `LocalEvent` / Event : evenement lie a un lieu, shop, organisateur, association, mairie ou autre acteur.
- `EventSerie` : serie d'evenements, logique de regroupement editorial/agenda autour de plusieurs occurrences ou evenements lies.
- `AnnualCelebration` / `CelebrationDay` : fetes, moments annuels, marronniers, jours speciaux et occurrences calendaires.
- `Experience` : activite/experience, souvent insolite ou reservable, avec acces, sessions, langues, etapes.
- `Equipment` : equipements de ville ou de lieux, parfois reservables/vivables : table, terrain, salle, chambre, etc.
- `Animation` : attractions/animations, separation legacy ; comportement proche d'equipement sur plusieurs flux, avec particularites.
- `Circuit` + `CircuitStep` : parcours touristiques/sportifs/localises, avec types, themes, etapes, traces et destinations.
- `Selection` : selection/coffret editorial, compose d'objets, de participations, de jours/actions, d'achats et de droits d'usage.
- `LocalHabit` : habitude locale rattachee a un objet ; micro-contenu qui donne du contexte culturel/local.
- `LocalTip` : bon plan local.
- `OutingIdea` : idee de sortie qui peut completer les objets principaux dans la decouverte.
### Objets utilisateur et social graph

Le modele utilisateur n'est pas seulement compte/authentification. Plusieurs petites briques se greffent sur les objets principaux et doivent rester visibles dans le contexte :

- `Favorite` / favoris : favoris multi-objets, y compris circuits selon le front.
- Listes utilisateur : listes, items de listes, sauvegarde d'objets, collections personnelles.
- `to_try` / statuts d'objet : objets a essayer, deja faits, ou autres etats personnels de decouverte.
- Agenda utilisateur : evenements sauvegardes, liens calendrier, export ICS.
- Follow : suivi d'objets, pages, users ou entites selon les cas.
- `Review` : avis sur Place, Shop, Event, Experience, Selection et potentiellement autres objets.
- Achats et droits : `SelectionPurchase`, `SelectionEntitlement`, `SelectionRedemption`, usages avec QR/signature.
- Meetz profile/preferences : preferences, onboarding, ville, zones, booking et contraintes de planning.

Ces objets sont souvent petits mais structurants : ils transforment l'annuaire en produit personnel/social. Avant de modifier une page objet, verifier les greffes favoris/listes/to_try/reviews/agenda/Meetz/achats.

### Meetz

Meetz est une verticale complete du produit, pas une simple page :

- onboarding utilisateur, profil, preferences et ville Meetz ;
- zones, plannings, overrides, occurrences et conflits horaires ;
- choix d'evenements, booking, paiement, confirmation, succes ;
- integration a `User` lors de l'inscription/connexion via application de l'onboarding en attente ;
- tables et vues dediees dans `meetz` cote front et BO.

Quand une modification touche `User`, paiement, agenda, city/location ou evenements, verifier si Meetz consomme indirectement la meme donnee.
### Commerce, paiement, rÃ©servation

- `Product` : produits au sens mÃ©tier, hors tarifs/services.
- `ElementAccessPrice` / EAP : tarifs d'entrÃ©e ou accÃ¨s Ã  events, lieux, expÃ©riences ; achat avec ou sans rÃ©servation.
- `ElementService` : services proposÃ©s, avec prix ou devis. Certains peuvent se comporter comme des EAP, d'autres non.
- `BookingConfiguration`, contenus, slots et sessions : rÃ¨gles de rÃ©servation.
- `Transaction`, `PayoutJob`, PSP/Stripe : paiement, onboarding, reversements.
- QR code : cas d'usage menus, consultation, commande d'avance, parcours sur place.

### Partner, network, PSP

- `Partner` : entitÃ© entreprise Ã  laquelle rattacher lieux, events, PSP et flux d'argent.
- `Network` : chaÃ®ne ou rÃ©seau type McDo/BK rattachÃ© Ã  un partner, pouvant contenir des restaurants/shops.
- Gestion descendante : partner -> networks/shops/places/events/PSP selon les cas.
- L'espace partner doit filtrer strictement les objets par appartenance partner.

### Deals, promos, plans

Trois couches distinctes Ã  ne pas confondre :

- `Offer` + `OfferTime` : promotions d'un lieu/shop, happy hour, promo Ã©tudiante, avantage Izilife rattachÃ© Ã  campagne.
- `BenefitPolicyRule` / `BoBenefits` : avantages Izilife Plan nÃ©gociÃ©s, pas nÃ©cessairement liÃ©s Ã  un lieu.
- `ExternalPromotion` : codes promos externes/influenceurs/sites via `page_id`.

Autres modules liÃ©s :

- `IzilifePlan` : abonnements utilisateurs, consommation, preuves, historiques.
- `BoAccessPolicy`, `BoBenefits`, `BoLoyalty`, `BoMissions`, `BoExternalPromo`.

### Calendrier, Ã©vÃ©nements, sports

- `CelebrationDay`, `HolidayRule`, `CalendarOccurrence` : calendrier Ã©ditorial/fÃ©riÃ© par scope gÃ©ographique.
- `EventDate`, `Representation`, `EventProgrammation`, rÃ©currences.
- `Competition`, `CompetitionEdition`, `SportMatch` : compÃ©titions sportives et calendriers.

### RÃ©fÃ©rentiels et configuration

RÃ©fÃ©rentiels importants vus dans le contexte global et le SQL :

- `ShopCategory`, `PlaceType`, `EventCategory`, `ActivityPrincipalCategory`
- `CircuitType`, `CircuitTheme`, `SportCircuitType`
- `ExperienceType`, `ExperienceStepActionType`
- `SelectionCategory`, `SelectionTheme`
- `Hobby`, `HobbyCategory`
- `Currency`, `AccessType`, unitÃ©s de mesure, booking configuration types
- `City`, `AdministrativeDivision`, `Country`, `Department`

### Moteurs

- `SpotlightRule`, conditions, actions, schedules : moteur de mise en avant.
- `TargetReason` : raisons de suggestion.
- Completion score sur objets principaux : Place, Shop, Event, Experience, Equipment, Circuit.
- Moteurs de recherche/intention : `Whattodo`, `Search`, helpers de query locale.

## SchÃ©ma SQL

Le schÃ©ma principal se trouve dans :

`C:\xampp\htdocs\izilife-admin\statics\izilife_new_version`

Fichiers structurants observÃ©s :

- `000_Some_Basics.sql` : rÃ©fÃ©rentiels de base, horaires, accÃ¨s, transactions, EAP, ElementService, devises, UTM.
- `0010_izilife.sql` et `0010_izilife_o.sql` : gros socle historique, objets principaux, gÃ©ographie, users, events, places, shops, Ã©quipements.
- `0011_Place_Shop_Event_Experience_Circuit_Conf.sql` : configuration des objets principaux.
- `001100_calendar_intelligence.sql` : calendrier intelligent.
- `00110_Campain.sql` : campagnes.
- `0012_transport.sql` : transports.
- `0013_Competition.sql` et `0013_sport_competition_rebuild.sql` : sport/compÃ©titions.
- `0020_Add_Some_FK.sql` : clÃ©s Ã©trangÃ¨res.
- `011_regions_departments_cities_configuration.sql`, `030_insert_cities_FR*.sql`, `04_insert_cities_BE*.sql` : gÃ©ographie.
- `019_Book_Movie_Serie_Catalog.sql`, `020_New_Entities.sql`, `021_Translation.sql`, `translation.sql`.
- `App_Internal_Security.sql` : sÃ©curitÃ© interne app.

Attention : plusieurs fichiers SQL contiennent de trÃ¨s gros inserts de donnÃ©es. Pour analyser la structure, privilÃ©gier `CREATE TABLE`, `ALTER TABLE`, indexes et FKs avant de lire les dumps complets.

## Agents, scraping et IA

Contexte global :

- Tout agent = un fichier `.md` comme cerveau + un script PHP comme bras + `postIngestJson()` comme sortie.
- Tout passe par staging/tmp -> validation humaine -> prod.
- ZÃ©ro token pour la structure : Places API, crons, parsing HTML statique.
- Tokens uniquement pour intelligence : CIC, OCR, gÃ©nÃ©ration.
- Switch provider par `LLM_PROVIDER`.
- Chaque appel LLM indÃ©pendant ; pas de contexte cumulatif incontrÃ´lÃ©.
- Le `.md` de l'agent doit Ãªtre un prompt systÃ¨me fixe injectÃ© Ã  chaque appel.

Code observÃ© :

- BO : `Scraper.php` porte une grosse partie des endpoints agents et scraping.
- Helpers/libraries BO : `ai_helper.php`, `calendar_intelligence_helper.php`, `scraper_helper.php`, `OpenAI_lib.php`, `Claude_lib.php`, `AIClient_lib.php`, `BrightData_lib.php`, `WebsiteParser_lib.php`, `Scraping/*`.
- SÃ©curitÃ© agents mentionnÃ©e : comptes service avec `is_service_account`, `service_scopes`, contrÃ´les de scope et filtre global.

RÃ¨gle : ne jamais brancher un agent directement sur la prod sans staging, validation et garde-fous de scope.

## Zones legacy et dette Ã  respecter

- `Shop` et `Place` sont sÃ©parÃ©s historiquement : ne pas fusionner mentalement sans vÃ©rifier les usages.
- `Equipment` et `Animation` sont sÃ©parÃ©s historiquement : ils peuvent se ressembler mais n'ont pas forcÃ©ment les mÃªmes comportements.
- Plusieurs fichiers `_o`, `_old`, `old_*`, `_legacy_bo_*_2026-06-29` existent. Ils sont utiles pour comprendre l'historique mais ne doivent pas Ãªtre modifiÃ©s sauf demande explicite.
- Le partner-admin semble contenir de nombreuses copies/adaptations du BO ; les correctifs doivent Ãªtre propagÃ©s consciemment, pas mÃ©caniquement.
- Les routes dÃ©clarÃ©es sont peu nombreuses ; avant de supprimer ou renommer une mÃ©thode de contrÃ´leur, vÃ©rifier les liens dans les vues, formulaires et auto-routing.

## MÃ©thode recommandÃ©e pour les prochains chantiers

1. Relire ce document.
2. Identifier l'app concernÃ©e : front, BO, partner-admin ou futur partner-front.
3. Lire uniquement les contrÃ´leurs/modÃ¨les/vues concernÃ©s.
4. Exclure systÃ©matiquement `.env*`, `env`, secrets, `writable/`, `system/`, `ThirdParty/`, sessions et archives si non nÃ©cessaires.
5. Annoncer les fichiers qui vont Ãªtre modifiÃ©s.
6. Modifier petit, vÃ©rifier localement avec lint/test adaptÃ©.
7. Si la logique touche un objet partagÃ©, vÃ©rifier les impacts sur les trois apps.
8. Mettre Ã  jour ce contexte si une rÃ¨gle mÃ©tier importante est dÃ©couverte.

## Commandes de vÃ©rification utiles

Exemples Ã  adapter selon le fichier modifiÃ© :

```powershell
& 'C:\xampp\php\php.exe' -l 'C:\xampp\htdocs\izilife\app\Controllers\Place.php'
& 'C:\xampp\php\php.exe' -l 'C:\xampp\htdocs\izilife-admin\app\Controllers\Place.php'
& 'C:\xampp\php\php.exe' -l 'C:\xampp\htdocs\izilife-partner-admin\app\Controllers\Place.php'
```

Pour inventorier sans secrets :

```powershell
rg --files -g '!**/.env*' -g '!**/env' -g '!**/writable/**' -g '!**/.git/**' -g '!**/vendor/**' -g '!**/node_modules/**'
```

## Ã‰tat de cette initialisation

Cette premiÃ¨re passe est une cartographie longue, pas un audit complet. Elle a volontairement Ã©vitÃ© :

- lecture de fichiers d'environnement ;
- lecture exhaustive des dumps SQL de donnÃ©es ;
- analyse complÃ¨te de tous les fichiers `system/` et `ThirdParty/`;
- modifications de code applicatif.

Ã€ complÃ©ter dans les prochains chantiers :

- carte dÃ©taillÃ©e des modÃ¨les et relations par objet ;
- cartographie des vues/formulaires critiques ;
- cartographie des endpoints agents et sÃ©curitÃ© ;
- inventaire des schÃ©mas SQL par tables rÃ©ellement actives ;
- stratÃ©gie pour le futur `izilife-partner`.

