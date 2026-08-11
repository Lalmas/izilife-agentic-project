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

## Moteurs structurants Izilife

Izilife contient plusieurs moteurs transverses. Ils doivent etre compris comme des couches generiques reutilisables, pas comme des fonctionnalites isolees dans un controleur.

### PayHub et paiement par contexte

- Le paiement doit passer par le point d'entree unique `Payment::pay` / `payment/pay`.
- `Payment::pay` rentre dans `PayHub`, qui delegue selon le contexte metier : abonnement, achat, selection, booking futur, commande, etc.
- Le pipeline de paiement ne doit pas etre duplique dans chaque objet.
- Les offres internes type premiere periode offerte, operations internes, reduction interne, doivent passer par une couche `InternalOffer`/helper et modifier les montants/metadonnees sans creer de `Offer` metier.
- L'abonnement Izilife peut inclure une premiere periode offerte pendant un temps donne ; ce comportement appartient a l'offre interne / PayHub, pas au moteur Offer du lieu.

### Moteur de suggestion

- Le moteur de suggestion agrege signaux, categories, hobbies, tags, intentions, contexte utilisateur et raisons de suggestion.
- Il ne doit pas etre confondu avec le moteur de recherche classique.
- Les objets qui enrichissent la suggestion incluent Place, Shop, Event, Experience, Circuit, Selection, Equipment, LocalHabit, LocalTip, OutingIdea, Offers et signaux de completion.

### Moteur de construction d'accueil

- La home n'est pas une page statique : elle se construit selon un contexte.
- Signaux importants : heure, meteo, intention, ville/zone, profil touristique, saison, jours speciaux, ouvert maintenant, evenements proches, happy hours, avantages, selections.
- Les helpers `home_builder`, `home_layout`, `local_query_condition`, live resume et moteurs de requete locale doivent rester coherents avec cette logique.

### Moteur Benefit / Reward / Ledger / Redemption

Chantier prioritaire courant : finaliser le moteur d'avantages, recompenses, ledger et redemption.

Vision :

- Unifier abonnements, avantages, grants, rewards, jeux, missions, loyalty, discovery et historique.
- Toutes les consommations passent par un moteur unique : `BenefitEngine`.
- Le `BenefitLedger` est la verite metier : quotas, consommation, refus, historique, bucket, plan, grant.
- `ParticipationRewardEngine` devient le point d'entree des actions utilisateur : avis valide, photo, check-in, reservation, commande, evenement, ajout lieu, partage, etc.
- Les actions peuvent donner des points, debloquer badges, declencher RewardGame, creer BenefitGrant, puis rendre une BPR consommable.
- Les Plans utilisent directement `BenefitPolicyRule`; les jeux creent des Grants; les Grants consomment des BPR.
- Les controllers ne doivent pas contenir la logique metier de consommation.

Objets et notions importantes :

- `BenefitPolicyRule` : decrit le droit/avantage, conditions, targets, resume, mode de delivrance.
- `delivery_mode` : `onsite_redemption`, `online_order`, `promo_code`, `external_booking`, `display_only`.
- `usage_constraints_json` : jours, creneaux, horaires d'ouverture, blackout, limite horaire, etc.
- `BenefitLedger` : transactionnel, anti double clic, bucket temporel.
- `BenefitGrant` : droit gagne via jeu, mission, loyalty, affiliation, recommandation, discovery futur.
- `RewardGame` / `RewardGamePrize` : roue, jeu, recompense, stock/probabilite, creation de grant.
- `DiscoveryChoice` : discovery reste un produit configure via BPR.

UX validee pour les avantages/deals :

- Fiche lieu/shop : mini cards sans CTA interne.
- Deux sections : `Avantages Izilife` et `Offres du lieu`.
- Modal `Voir les offres` = premier vrai niveau d'action.
- Les mini cards ne consomment rien.
- Redemption seulement depuis modal ou page deal.
- Apres consommation : preuve + historique utilisateur.
- Futures pages `deals` et `deal` doivent pouvoir resoudre BPR plan, Offer, campagne future.

Regles de consommation attendues :

- Permanent : typiquement 1 fois par jour / user / lieu / regle.
- Anniversaire : 1 fois par an / user.
- Cadeau annuel : 1 fois par an.
- Offre-decouverte : bucket hebdomadaire.
- Grants : consommation compatible `grant_id`.

Selection canonique de la meilleure BPR par plan :

- La selection de la meilleure `BenefitPolicyRule` affichable/utilisable doit etre centralisee et commune au swiper, au modal, aux pages deal/deals et a la redemption.
- La regle canonique : pour une temporalite donnee, garder la meilleure regle dont `plan_rank <= user_plan_rank`.
- Ne jamais afficher ni consommer une regle au-dessus du rang du plan utilisateur.
- Non connecte / sans abonnement : afficher `USER_PASS` en priorite, sinon premier plan payant, sinon premier avantage disponible. Aucune redemption sans connexion : ouvrir `connexionNeedModal`.
- Connecte FREE : uniquement regles FREE ou regles all plans.
- Connecte PASS : prendre PASS si disponible, sinon FREE.
- Connecte PRIME : prendre PRIME si disponible, sinon PASS, sinon FREE.
- Cas critique PRIME sans BPR PRIME mais avec PASS : afficher/consommer PASS.
- Cas critique PASS sans BPR PASS mais avec FREE : afficher/consommer FREE.
- Cas critique FREE : ne jamais afficher/consommer PASS ou PRIME.
- Le helper existant `izilife_pick_best_rule_for_user_plan()` dans `live_resume_helper.php` est deja utilise par le swiper via `featured_advantages`; la meme logique doit alimenter le modal.
- Cote backend redemption, ne jamais faire confiance a un rule id choisi par le front sans verification. Le backend doit re-resoudre la meilleure BPR applicable avec : `user_id`, `scope_level`, `scope_id`, `temporality`, `plan_rank <= user_plan_rank`, `valid_from`, `valid_to`, `is_active = 1`.
- `BenefitEngine::canUseRule()` et `BenefitEngine::consumeRule()` doivent etre appeles sur CETTE regle resolue, pas sur la premiere BPR trouvee.
- Objectif technique probable : extraire/centraliser cette resolution dans un helper/service partage pour eviter divergence entre affichage et consommation.

## Booking Engine - reservation universelle

Le moteur de reservation doit etre un moteur multi-objet, pas un formulaire restaurant.

Objets compatibles :

- Place
- Shop
- Equipment
- Animation
- Experience
- Event

Principe central : le moteur connait seulement `from_type` et `from_id`. Il ne doit jamais coder un cas specifique restaurant, bar, coiffeur, massage, terrain ou hotel. Le comportement vient des configurations.

Deux familles sont fondamentales :

- `BookingConfiguration` / BCC pour Place, Shop, Equipment, Animation.
- `SessionConfiguration` / SCC pour Experience et Event.

Experience et Event ne doivent pas generer massivement des sessions physiques. Par defaut, le moteur reserve une occurrence virtuelle identifiee par :

- `from_type`
- `from_id`
- `session_conf_content_id`
- `booking_date`
- `booking_start_time`
- `booking_end_time`

Une `Session` physique n'est creee que si elle apporte une valeur metier : exception, changement d'horaire, salle, capacite, annulation, communication ciblee, pilotage BO.

Architecture cible :

```text
Booking controller Ajax
-> BookingResolver
-> AvailabilityResolver
-> BookingValidator
-> BookingCreator
-> BookingModel
```

Le front ne calcule jamais disponibilite, capacite, conflits, horaires ou creneaux. Il affiche ce que le back renvoie.

Decision front importante : construire un `Booking Block` universel avant une modal.

- `common_components/booking/booking_block.php` : composant principal reutilisable.
- `booking_modal.php` : wrapper optionnel qui embarque le block.
- `booking_page.php` : page dediee optionnelle.
- Meme JS, meme API, meme DTO.

DTO front attendu : `BookingAvailabilityDTO`.

Il doit dire explicitement :

- `can_book`
- `from_type`, `from_id`
- `mode`, `booking_method`, `source`
- champs requis : date, time, quantity, service, equipment
- droits : privatisation equipement, privatisation lieu complet
- `dates`, `slots`, `services`, `equipments`
- defaults et messages

V0 : toutes les reservations sont creees en attente / pending. Validation manuelle. Pas de paiement obligatoire au premier lot. L'auto-confirmation, acompte, caution, remboursement, waitlist, synchronisation calendrier, rappels, QR/check-in viendront plus tard sans reecrire le coeur.

## Catalogue commercial, menu digital et objets vendables

Le catalogue n'est pas seulement un menu digital. C'est une page/moteur commercial generique qui presente ce qu'un objet peut proposer ou vendre.

Objectif : creer un moteur commercial generique capable de presenter, vendre et gerer n'importe quel element commercial Izilife sans creer un systeme restaurant, bowling, spa ou parking separe.

### Distinctions fondamentales

- `Catalogue` : page dynamique, pas une table SQL. Regroupe menus, produits, acces, services selon ce que possede l'objet.
- `Product` : objet commercial principal : burger, cocktail, location velo, bon cadeau, abonnement, produit boutique.
- `ProductCategory` : categories et sous-categories via `parent_id`; ne pas creer `ProductSubCategory`.
- `ElementMenu` / menu digital : conteneur de categories produits dans un contexte : menu restaurant, carte bar, brunch, menu enfant, menu event.
- `ElementAccessPrice` / EAP : acces vendu : entree bowling, pass journee, ticket parking, acces spa, abonnement, adhesion, licence.
- `ElementService` : service vendu : coiffure, pressing, livraison, traiteur, massage, impression, cours.
- `Offer` : promotions, happy hour, reduction, coupon, bon plan, campagne marketing. Offer reste separe du catalogue.

Le catalogue peut afficher :

- menus actifs ;
- categories/sous-categories ;
- produits simples/composes/groupes ;
- access prices ;
- services ;
- highlights/mises en avant ;
- disponibilites temporelles.

Il doit masquer les produits inactifs, indisponibles, categories vides, menus indisponibles, highlights expires.

### Product et menus

- Ne pas creer un objet specifique pour `PlatDuJour`, `FormuleMidi`, `CocktailDuMoment`, `MenuSoirSpecial`.
- Une formule midi est un `Product` compose avec slots (`ComposedProductSlot`, `ComposedProductSlotItem`) et disponibilite midi.
- Les menus sont des conteneurs d'affichage ; ils ne remplacent pas les categories.
- Les disponibilites doivent pouvoir s'appliquer a un produit, une categorie ou un menu.
- Les groupes de mise en avant doivent etre generiques : `ProductHighlightGroup`, `ProductHighlightItem`.
- Best-seller doit etre calcule plus tard, pas manuel.

### Sellable abstraction

`Sellable` n'est pas une table. C'est une couche d'abstraction pour normaliser :

- Product
- ElementAccessPrice
- ElementService

But : vues, panier, JS, composants communs.

Composants cibles :

```text
common_components/sellables/show_sellable_card.php
common_components/sellables/show_sellable_modal.php
common_components/sellables/show_sellable_resume.php
common_components/sellables/show_sellable_price.php
common_components/sellables/show_sellable_counter.php
common_components/sellables/show_sellable_badges.php
```

Regle : reutiliser le panier Phoenix. Ne pas repartir de zero. Migration progressive : Product -> AccessPrice Place/Shop -> Service -> Event plus tard.

Batch 1 courant cote catalogue : socle catalogue sans toucher Event ni panier. Preparer Place/Shop, models `ElementMenu_model`, methodes generiques dans `Product_model`, `ElementAccessPrice_model`, `ElementService_model`, puis vues catalogue ensuite.

### Multi-categories et lieux composites

Les lieux peuvent etre multi-categories via `LocationOtherCategory`, qui peut pointer vers des `PlaceType` ou `ShopCategory` secondaires.

- Si l'objet est un `Shop`, sa categorie principale vient de `ShopCategory` liee au shop.
- Si l'objet est un `Place`, sa categorie principale vient de `PlaceType` lie au place.
- Les autres categories sont secondaires et peuvent enrichir recherche/filtrage sans changer l'organisation interne.

Deux modes de gestion :

1. Categorie secondaire simple : le lieu reste un seul etablissement. La categorie sort dans les resultats/recherches, mais n'a pas d'impact fort sur la gestion.
2. Gestion comme entite differente : certaines categories/activites deviennent des sous-objets gerables avec leurs propres horaires, menus, produits, access prices, services, booking configs.

Exemple architectural important : complexe type Jost a Lille.

- Une `Place` hotel porte les chambres et la logique hotel.
- Un food court peut exister comme espace/lieu interne.
- Un bar peut appartenir au lieu/food court.
- Des kiosks peuvent etre des `Shop` avec `in_on_place` vers le food court.
- Le food court lui-meme peut etre dans la Place hotel.

Le modele doit rester modelable : un environnement global unique peut contenir des sous-entites commerciales distinctes. Ne pas forcer une structure plate.

### Event et panier proteges

- Event possede deja une billetterie avancee : tickets gratuits, tarifs libres, packs, jauges, limite utilisateur, paiement PSP, generation ticket.
- Le chantier Catalogue ne doit rien casser cote Event.
- SQL additive uniquement : nouvelles tables, colonnes NULL, index, FK, string_id. Pas de renommage destructif.
- Referentiels a proteger : `PriceModel`, `ElementAccessType`, `ElementServiceType`, `UserSpecificReductionCategory`.
## Architecture agentique externe - agentic_Workspace

Chemin racine : `C:\Users\alcamara\Documents\agentic_Workspace`

Ce dossier fait partie de la vision globale Izilife. Il ne contient pas seulement de la documentation : c'est la couche agentique qui doit alimenter, enrichir et prolonger le BO PHP. Le BO reste le systeme metier central, mais les agents Python, les fichiers Drive/XLSX, les inputs/outputs et les scripts sociaux forment une deuxieme architecture autour de lui.

### Role dans l'architecture Izilife

- Alimenter le projet sans tout saisir manuellement dans le BO.
- Collecter et structurer des lieux, events, experiences, circuits, pages, liens, medias externes, local tips, local habits.
- Envoyer les donnees au BO via endpoints agents proteges, staging ou fichiers de validation.
- Gerer les sources semi-automatiques : sites de mairies, influenceurs locaux, OpenAgenda, Shotgun, Facebook, Eventbrite, Meetup, HelloAsso, Billetweb, pages web, images Instagram/Facebook.
- Produire la presence reseaux sociaux Izilife via planning, templates, Drive, outputs et validation humaine.
- Servir de base a l'agence CM, puis a une version agentique de l'espace partner.

### Structure observee

- `agentic_Workspace\izilife\context` : contexte produit, dev, social, agents, docs, schemas, strategie.
- `agentic_Workspace\izilife\izilife-agent-workspace` : workspace agent principal par zones/sources.
- `agentic_Workspace\izilife\izilife-agent-workspace-local` : workspace local d'execution/curation.
- `agentic_Workspace\izilife\izilife-agent-workspace-staging` : workspace staging avant validation/prod.
- `agentic_Workspace\scripts` : scripts Python agents, coeur commun, docs techniques.
- `agentic_Workspace\agence` : logique community manager agence par client.
- `agentic_Workspace\wordpress` : activite annexe sites/clients, a garder separee sauf besoin explicite.

### Scripts Python et alimentation du BO

Les scripts Python sont une couche d'automatisation autour du BO :

- `scripts\izilife\places` : chasseurs/createurs/enrichisseurs de lieux.
- `scripts\izilife\events` : scrapers et ingestion events : Facebook, Shotgun, Eventbrite, Meetup, HelloAsso, Billetweb, liens, images, curation manuelle.
- `scripts\izilife\objects` : agents pour pages, outing ideas, local tips, local habits, links, external media, experiences, circuits.
- `scripts\izilife\deals` : deals/promos externes.
- `scripts\izilife\competitions` : recuperation planning competitions.
- `scripts\izilife\social\cm_izilife.py` : community manager Izilife.
- `scripts\agence\cm_agence.py` : moteur agence derive de la logique CM Izilife.
- `scripts\core\paths.py` : chemins, environnements, zones, workspaces.

Regle d'architecture : les agents ne remplacent pas le BO. Ils preparent, collectent, structurent et poussent vers le BO ou vers une zone de validation. Les secrets restent cote local/serveur, jamais dans Drive/XLSX.

### Drive, XLSX, CSV et systeme hybride

Le systeme n'est pas seulement code -> DB. Il est hybride :

- Google Drive contient les fichiers de travail : Excel/XLSX, inputs, outputs, logs, images, templates.
- Les XLSX servent de planning, files de curation, sources d'objets, suivi de statut.
- Le CSV pourra etre une alternative selon les besoins, mais le modele actuel est oriente XLSX.
- Les scripts lisent Drive/inputs, appellent LLM/parsers/scrapers, puis ecrivent outputs/logs ou appellent le BO.
- Les donnees non fiables ou issues de sources difficiles doivent rester en staging/curation avant validation humaine.

Cette logique est essentielle : elle evite de tout alimenter manuellement dans le BO, tout en gardant un filet humain sur les sources fragiles.

### Hub de sources locales

Le hub permet de regrouper par zone les sources facilement exploitables :

- sites de mairies ;
- offices, agendas locaux, OpenAgenda ;
- petits influenceurs et medias locaux ;
- sites d'associations, collectifs, lieux, salles ;
- sources web simples a scraper automatiquement.

Pour les sources difficiles ou semi-fermees comme Facebook, Shotgun, images Instagram, stories, captures ou pages peu structurables, les agents doivent fonctionner avec curation manuelle partielle. Le but est de capter ce que les scrapers classiques ne savent pas fiabiliser seuls, puis de transformer ces donnees en objets Izilife exploitables.

Lien avec le BO : cette logique recoupe `Scraper.php`, les endpoints agents, les tables staging et les methodes d'import/validation deja presentes dans `izilife-admin`.

### Social Izilife

La presence sociale est une extension du produit, pas le produit lui-meme. Izilife reste l'agregateur ; Instagram/Facebook/TikTok/terrain doivent ramener vers le site.

Le moteur `cm_izilife` travaille par zone avec :

- planning XLSX ;
- inputs manuels ;
- templates Canva ou locaux ;
- outputs captions/slides/posts ;
- types de posts : agenda, tops, decouvertes, histoire locale, humour local, escapades, pepites, events Izilife.

Regle importante : l'agent ne choisit pas arbitrairement qui merite d'etre dans un top. Le fondateur fournit les listes/infos importantes ; l'agent met en forme, structure, reformule et produit.

### Agence CM

Le dossier `agence` et `scripts\agence` portent une version agence du community manager :

- meme logique que CM Izilife, mais par client ;
- un planning par client ;
- un contexte de marque par client ;
- inputs/outputs/templates separes ;
- ton, offres, contraintes et hashtags propres au client ;
- interdiction d'inventer offres, prix, dates, lieux ou temoignages.

Vision : quand `cm_izilife` sera solide, il sert de base a `cm_agence` pour gerer la presence de clients externes. Cette logique agence est aussi une prefiguration de services pro pour commerçants/partenaires.

### Vers un espace partner agentique

Cette architecture agentique doit inspirer une future version agentique de l'espace partner :

- aider un commercant/lieu/partenaire a gerer sa presence locale depuis un point unique ;
- centraliser messages, avis, Google Business Profile/GMB, Facebook, Instagram, evenements, liens, medias ;
- permettre de partager un event depuis Izilife vers les reseaux ;
- permettre au partner de fournir un lien Facebook/Shotgun/site, puis laisser un agent extraire les infos via LLM et creer une proposition d'event dans Izilife ;
- transformer les methodes actuelles de scraping/curation en workflows accessibles aux partenaires, avec validation et garde-fous.

Objectif produit long terme : le partner admin ne doit pas seulement etre un formulaire BO reduit. Il peut devenir un assistant de presence locale : collecte, creation, diffusion, reponse, enrichissement, suivi, tout en gardant Izilife comme base metier centrale.

### Regles de securite pour cette couche

- Ne jamais lire ni exposer `.env`, `.env.*`, `env`, providers secrets, tokens API, credentials Drive ou comptes sociaux.
- Les secrets restent hors Drive et hors XLSX.
- Les XLSX/plannings ne doivent pas contenir providers/modeles/cles.
- Toute source externe non fiable passe par staging/curation.
- Toute automatisation qui ecrit dans Izilife doit passer par endpoints agents scopes ou validation humaine.
- Ne pas confondre workspace agentique, BO PHP et Drive : ce sont trois couches qui collaborent, pas une seule base de code.

## Precision UX - avantages, deal action modal et blocs de gain

### Modal global vs modal d'action ciblé
Depuis les fiches live (`place_live_resume`, et par extension `shop_live_resume` / `event_live_resume`), le clic sur une carte avantage ne doit pas ouvrir uniquement le modal global "toutes les offres".

Le comportement cible est de partir de la meilleure BPR/deal deja resolue pour l'utilisateur et d'ouvrir un modal d'action centre sur cette opportunite.

Etats attendus :
- Non connecte : ouvrir le modal existant de connexion obligatoire avant toute redemption ou action sensible.
- Connecte sans abonnement actif : proposer `Prendre l'abonnement` et `Voir les produits` / `Voir le deal` quand la page sera branchee.
- Connecte avec abonnement actif : entrer dans le processus de redemption avec `Utiliser en caisse`; action secondaire possible vers `Commander en ligne` / `Voir le deal`, mais cette destination peut rester non branchee au depart.

La page `deal/{id|slug|key}` ne doit pas etre la source de verite de la redemption. Elle doit resolvere l'offre/BPR pour affichage et preparation catalogue, mais la consommation effective doit refaire la resolution backend canonique.

### Pages deals / deal a preparer
Preparer des routes/pages minimales pour :
- Place : liste deals et fiche deal.
- Shop : liste deals et fiche deal.
- Event : a prevoir ensuite si necessaire.

Au depart, ces pages peuvent etre structurelles et peu visibles, car le flux principal reste le modal d'action. Leur role est de reprendre le contenu du modal en page dediee, puis de brancher plus tard les produits, targets, EAP, ElementService, RewardGame, Grants et Missions.

### Blocs live resume autour du moteur de gain
Le terme "hooks" signifie ici des entrees fonctionnelles visibles et preparees dans le live resume, pas seulement des callbacks techniques.

Blocs a prevoir autour du moteur unique de participation/gain :
- Jeu / RewardGame : roulette, de, tir au but ou autre mecanique configuree; peut demander une action comme avis, scan menu, participation ou autre preuve avant gain.
- Fidelite : affichage de progression vers la prochaine recompense locale du lieu.
- Cadeaux / Grants : mise en avant des avantages deja acquis par l'utilisateur, par exemple reductions, produits offerts ou offres actives.
- Missions : missions globales Izilife ou locales que l'utilisateur peut faire avancer via ce lieu.

Ces blocs doivent rester raccordables au Benefit/Reward/Ledger/ParticipationRewardEngine sans que le front choisisse arbitrairement la regle consommee.

## Mise à jour contexte - 2026-07-04 - Roue Izilife, opportunités et analytics

### Décisions Reward / opportunités

- L'ancienne logique "Offre découverte" sort de la V2. Elle ne doit plus être exposée dans le live resume, les modals d'avantages ou les nouveaux flux de reward. Les anciennes données peuvent rester en base le temps d'une migration, mais elles ne doivent plus porter l'expérience produit.
- La fidélité Izilife globale est abandonnée côté UX V2 : Izilife garde son moteur de points, badges, missions, grants et participation. Les programmes de fidélité visibles doivent être locaux : lieu, commerce, page, partenaire, éventuellement event/experience plus tard.
- Les programmes de fidélité commerçants doivent être simplifiés : objectif fixe lisible, progression simple, récompense claire. Les mécaniques complexes sont plutôt portées par Mission / MissionObjective.
- Le bloc `place_live_resume` doit présenter les opportunités sous forme de rail compact : Roulette / Jeux / Concours / Missions / Cadeaux / Fidélité locale. Les détails s'ouvrent ensuite dans un bottom sheet mobile ou un panneau/modal compact desktop.

### Roue Izilife pérenne

La Roue Izilife est une fonctionnalité permanente, pas une campagne de juillet ou une offre ponctuelle. Elle possède son propre moteur global.

Principe métier :

- Izilife négocie avec des commerçants des lots récurrents : produit offert, cadeau, réduction, points, etc.
- Le commerçant configure une dotation récurrente, par exemple `10 cocktails offerts par semaine`, et le moteur réinitialise le stock selon la période.
- Un lot peut aussi être limité par dates (`valid_from` / `valid_to`) pour un produit saisonnier ou une opération courte.
- Quand le user tourne la roue, le backend choisit d'abord un lot disponible dans le pool, puis génère un grant précis : produit X chez lieu Y, avec expiration et conditions.
- La consommation du lot passe ensuite par le flux de claim/proof/consume des grants, pas par une BenefitPolicyRule plan.

Familles de jeux à distinguer :

- `izilife_wheel` : roue globale permanente Izilife.
- `seasonal` : jeux saisonniers, potentiellement reliés à `AnnualCelebration` / `CelebrationDay` : Noël, Saint-Valentin, braderie, été, rentrée.
- `campaign` : jeux rattachés à une campagne via `campaign_id`.
- `local` : jeux locaux attachés à un shop/place/event/experience.

Décision d'architecture : ne pas transformer chaque lot de roue en BPR. Pour la roue, utiliser un pool de lots (`RewardGamePrizePool`) + stock périodique + `BenefitGrant` généré au gain. BPR reste pour les avantages d'abonnement, promos structurées et règles de bénéfices.

### Moteur JS de jeux

Besoin futur confirmé : un module front générique de jeux capable de gérer plusieurs mécaniques avec une configuration commune : roue, dés, fléchettes, tir au but, scratch, snake/simple game, etc.

Approche cible :

- Le backend décide le résultat gagnant et renvoie une configuration signée ou une résolution serveur.
- Le module JS ne décide jamais le gain réel ; il anime seulement l'expérience et affiche le résultat validé.
- Le même contrat doit accepter : nombre de cases, labels, couleurs, assets, durée, easing, comportement mobile/desktop, callbacks de fin, état déjà joué, état non connecté, état non éligible.
- Le moteur doit rester réutilisable pour roue globale, jeux saisonniers, jeux de campagne et jeux locaux.

### Analytics / DataTaker

`trackOnce()` est la bonne base V2 : un événement analytique important doit être dédupliqué par clé et TTL. On évite de recréer l'ancien problème de 70 lignes pour une seule visite.

Règle : BenefitLedger / grants restent la source de vérité métier pour les consommations et récompenses. `user_events` reste analytics comportemental : home, recherche, catégorie, fiche objet, menu, catalogue, agenda, QR scan, deal view, etc.

### Offres flash / invendus / achat anticipé

La logique type TooGoodToGo ne doit pas entrer dans la roue V2. Elle mérite son propre flux transactionnel.

Piste produit retenue : plutôt qu'un clone direct d'invendus, Izilife peut porter un moteur d'offres flash / dernière minute :

- un restaurateur ou bar peut publier une offre limitée pour demain, ce soir ou un créneau précis ;
- stock limité, conditions simples, éventuellement paiement en ligne plus tard ;
- utile pour remplir un service, écouler certains produits, pousser une soirée calme ou créer une offre de dernière minute.

À distinguer plus tard :

- offres flash / dernière minute : promotion courte, souvent sans panier anti-gaspi strict ;
- invendus alimentaires : flux plus contraint, retrait à horaire précis, paiement et stock précis ;
- achat anticipé : réduction si achat à l'avance ;
- achat groupé : prix dégressif si assez de participants sur un jour donné.

## Mise à jour contexte - 2026-07-04 - Home Builder, LocalQuery, Suggestions et requêtes V2

Objectif du prochain chantier : finaliser en une journée les requêtes et blocs d'accueil de la V2, en s'appuyant sur l'existant plutôt qu'en réécrivant les contrôleurs.

### Home Builder
La page d'accueil est maintenant pilotée par `buildHomePage($profile, $weather, $hour, $weekPart)` dans `app/Helpers/home_builder_helper.php`. Elle part du catalogue `get_home_blocks_catalog()` (`home_layout_helper.php`), applique le bloc contextuel selon l'heure, injecte les blocs "maintenant", les blocs utilisateur si connecté, filtre par météo/temporalité, puis injecte les blocs spéciaux (Selection, Meetz, abonnement, contenus, promos) via `HB_get_special_blocks_pool()`.

`app_request_helper.php` sert de fabrique de conditions SQL et de définitions de blocs : horaires, météo, open now, événements aujourd'hui/ce soir/week-end, expériences disponibles, catégories enfants/sport/danse/sorties, terrasses, bons plans, etc. Le prochain travail doit surtout ajuster les mappings bloc -> LocalQuery/config, pas repartir de zéro.

### LocalQuery V6
`app/Libraries/LocalQuery` est le moteur de requête multi-objet configurable. Il prend `sources`, `context`, `ranking`, `pagination`, construit des requêtes par provider, puis les assemble en `UNION ALL`. Sortie legacy volontaire : `id, name, string_id, type, weight, start_date, distance`.

Providers enregistrés actuellement : `place`, `shop`, `event`, `experience`, `equipment`, `circuit`, `local_tip`, `local_habit`, `outing_idea`, `selection`, `page`, `association`, `promo`, `external_promo`, `escapade_proposal`, `community`, `annual_celebration`, plus quelques skeletons (`user_list`, `meetz_slot`, `city`, `administrative_division`, `escapade`). `TerraceSourceProvider` est importé mais pas encore enregistré.

Config normalisée par source : catégories, conditions, signal_filters, availability, terrace, spotlight, newness, popup, offers, promo, itinerant, age, price, types, natures, activity_principal_categories, themes, action_types, little_activity_occasions, campain, annual_celebration, sport_competition, extra_score. Rankings disponibles : relevance, distance, completion, newest, spotlight, weight, event_date.

Score interne typique : poids éditorial + completion_score + importance locale + nouveauté + spotlight + extra_score - distance. Il faut donc alimenter `completion_score`, `importance_in_city`, `is_new_in_city`, `Spotlight/SpotlightRule`, catégories et signaux.

### Whattodo / Search
`Whattodo` et `Search` utilisent déjà LocalQuery via `executeWtdQB()` et `executeSearchQB()`. `Whattodo` a déjà du tracking `trackOnce('search_intent_view', ...)`, avec déduplication et merge des pages vues. Les sections `s-evader`, `live-sessions`, `sport`, `danser` existent partiellement et doivent être stabilisées par des packs de requêtes LocalQuery. Il faut migrer progressivement les intentions et catégories : ne pas casser les anciens chemins si une branche legacy marche mieux.

`Search` contient encore beaucoup de mapping legacy par catégorie, mais `buildSearchSourcesFromCurrentState()` prépare déjà `place/shop/event/experience/selection/circuit/...` pour LocalQuery. La stratégie V2 : transformer chaque intention ou catégorie prioritaire en config LocalQuery testée, puis basculer par petits lots.

### Suggestions
`app/Libraries/Suggestions` est le moteur de suggestion pré/post-intention. `LocalSuggestionService` prépare le contexte (ville, GPS, heure, météo, vacances, coucher de soleil), récupère des candidats proches, puis `SuggestionEngine` applique `LocalSuggestionRules`. Les règles couvrent déjà : balade, prendre l'air, coucher de soleil, pique-nique, boire, café, manger, jouer, danse, famille, nouveautés, expériences disponibles, spectacles, apéro, terrasse, etc.

Le rôle de Suggestions n'est pas de remplacer Whattodo : Whattodo/Search sortent les résultats principaux ; Suggestions ajoute la couche "pourquoi maintenant" et les propositions contextuelles (météo, heure, sunset, profil, pré/post-intention).

### Priorités du prochain chantier
1. Auditer `NavCategory` et stabiliser les nouveaux pôles : `s-evader`, `live-sessions`, `sport`, `danser`, éventuellement `jouer`, `famille`, `bons-plans`.
2. Écrire les packs LocalQuery prioritaires : manger maintenant, boire/afterwork, sortir ce soir, événements aujourd'hui, week-end, sport, danser, s'évader, live sessions, bons plans, pluie/soleil, coucher de soleil.
3. Alimenter SQL/config : `Spotlight`, `SpotlightRule`, `EscapadeProposal`, `AnnualCelebration`, poids de catégories, completion_score, importance locale.
4. Ajuster `home_layout_helper` pour l'ordre des blocs par heure/météo/profil : petit-déj, lunch, goûter, afterwork, dîner, nuit, pluie, soleil, week-end.
5. Brancher `trackOnce()` avec parcimonie : Home, Whattodo, Search texte/catégorie, fiche objet, menu/catalogue/agenda. Pas de ligne à chaque pagination ou onglet.

Attention : vérifier le mapping `BenefitPolicyRule` utilisé dans `LocalSpecialConditions::offerCondition()` (`target_type/target_id`) vs le modèle BPR actuel (`scope_level/scope_id`) avant de s'appuyer dessus pour les offres. Ne jamais lire les `.env` ; les flags `env()` existent dans le code mais ne doivent pas être inspectés directement.
# Correctif d'architecture — 9 août 2026

Ne jamais interpréter `AdministrativeDivision.city_id` comme une ville-centre universelle. La hiérarchie administrative dépend du pays et peut se poursuivre sous la ville ; les intercommunalités disposent de leur liste propre de villes. Pour Place, Shop, Event et Experience, une vraie ligne `City` explicitement choisie reste obligatoire. Voir les documents Experience et Communautés pour le contrat complet.
