# Audit vérifié des agents iziLife — 13 novembre 2026

## Portée et niveau de preuve

Audit en lecture seule du dépôt `agentic_Workspace`, du manifeste
`deploy/cron/izilife-agents-prod.crontab`, des scripts et rapports sous
`scripts/izilife`, et des points d'intégration appelés dans
`C:\xampp\htdocs\izilife-admin`. Aucun agent ni aucune écriture de production
n'a été lancé.

Les statuts signifient :

- **livré disque** : commande et endpoint existent dans les arbres inspectés ;
- **planifié manifeste** : ligne active dans le crontab versionné ;
- **désactivé manifeste** : ligne commentée avec une raison explicite ;
- **ponctuel** : outil ciblé, sans justification pour un cron ;
- **déploiement non observé** : aucun accès au crontab installé ni au journal
  `/Users/lal/Library/Logs/izilife-cron.log` du Mac d'automatisation.

## Cartographie opérationnelle

| Agent / flux | Pourquoi métier | Entrée | Sortie / objets | Fréquence manifeste | Statut et prochaine action |
|---|---|---|---|---|---|
| Shotgun | Collecter les événements Shotgun de la ville demandée | Pages Shotgun, `--city`, cache des URL EventTmp | HTML vers `agentUploadEventSources`, puis EventTmp | jeudi et dimanche 21:30 | Livré disque, planifié. Le filtre géographique utilise localité/coordonnées et rejette le hors-ville. Déploiement réel à confirmer par journal serveur. |
| Curation Events | Traiter les liens saisis manuellement sans perdre médias ni cas ambigus | `curate_events.xlsx`, HTML/JSON-LD, Facebook/Instagram, images | EventTmp + médias + état Excel | quotidien 23:00 | Livré disque, planifié. Image conservée même si OCR vide/ambigu ; noyau manuel prioritaire. |
| Structures Event | Créer/mettre à jour séries, célébrations annuelles et parents récurrents | classeur de zone / file serveur | EventSerie, AnnualCelebration, parent de récurrence | quotidien 23:10 | Livré disque, planifié ; vérifier idempotence et rattachement des occurrences exceptionnelles en test réel. |
| Calendrier Event | Matérialiser/maintenir le calendrier des événements | objets et programmation existants | occurrences / calendrier | quotidien 23:20 | Livré disque, planifié ; déploiement non observé. |
| Validateur EventTmp | Publier les cas certains, laisser les ambigus en revue | file EventTmp, `scrapping_json`, analyse déjà stockée, références BO | Event, liens éditoriaux, rapport/revue | quotidien 23:35 | Livré disque et endpoints BO présents (`AgentEventValidator_model`). Planifié. Les tests de contrat existent ; exécution locale/staging/prod récente non démontrée par le seul dépôt. |
| Agrégateur territorial Event | Découvrir des sources territoriales sans doublonner | JSON de zone, JDS/InfoLocale/Ma Vie Lilloise/Meetup/HelloAsso, SQLite | candidats JSON/XLSX, nouveaux liens envoyés au Hub, éventuellement EVENT_GRAPH | dimanche 08:30 | Livré disque, planifié. État SQLite et rapports de smoke présents. Confirmer le JSON réellement déployé et le journal cron. |
| Paquets EVENT_GRAPH / inbox | Importer un graphe complet avec programmation | JSON dans `site_packages/inbox` | Event + série/célébration + programmation et autres paquets | quotidien 00:20 | Livré disque, planifié avec confirmation production. Les générateurs `site_event_package.py` et exemples EVENT_GRAPH existent. |
| Médias externes | Rattacher des médias distants pilotés | classeur de zone | médias via `agentAddExternalMedia` | quotidien 23:50 | Livré disque, planifié. |
| Pages | Créer/upserter des Pages éditoriales | `pages.xlsx`, résolution identité lieu | Page + médias | quotidien 00:10 | Livré disque, planifié ; utilise les candidats d'identité partagés. |
| Benefits / Offers / Brunch | Maintenir les offres et référentiels éditoriaux pilotés | classeurs de zone | bénéfices, offres spéciales, brunchs | quotidien 00:35 / 00:55 / 01:15 | Livrés disque, planifiés. Flux Excel idempotents ; déploiement non observé. |
| Media downloader | Télécharger les médias mis en file | file/cache média | fichiers locaux / état de téléchargement | quotidien 02:10 | Livré disque, planifié. |
| Media curator (`media_curation`) | Sélectionner et rattacher les médias admissibles | objets candidats, Instagram/cache | médias objet + rapport | quotidien 02:20 | Livré disque, planifié. Aussi inclus dans l'orchestrateur d'enrichissement : risque de double passage si celui-ci est activé sans coordination. |
| Référentiels territoriaux | Configurer territoires existants | classeur de zone | Territory | quotidien 02:35 | Livré disque, planifié. |
| Equipment / Escapade / Link / quartiers / rues | Alimenter les référentiels manuels | classeurs de zone | Equipment, EscapadeProposal, Link, CitySubdivision, Street | quotidien 03:05–04:25 | Livrés disque, planifiés. Ce sont des agents de classeur, pas des collecteurs autonomes. |
| Curate Places | Créer les lieux/commerces absents après résolution | `curate_places.xlsx`, identité iziLife/Google | PlaceTmp/Shop ou objet final, état Excel | quotidien 01:35 | Livré disque, planifié. Ne doit retirer une ligne que si TMP/objet existe réellement. |
| Chasseur de lieux | Découvrir puis insérer des POI | web/Google, zone/ville | candidats puis TMP | ancien planning semaine/week-end | Livré disque mais **désactivé manifeste**. Ne pas réactiver sans revoir budget, cache et tests réels. |
| Enrichisseur batch `enrichisseur.py` | Maintenance/fermeture et enrichissement générique | file BO, zone/ville | modifications de lieu, rapport | ancien planning 05:00/05:10 | Livré disque mais **désactivé manifeste** car IA payante sans plafond explicite. |
| Améliorateur intelligent | Proposer horaires, hobbies, caractéristiques, styles et données alimentaires | objets ciblés, JSON/cache Google, web, références BO | propositions JSON/XLSX, application contrôlée | cron 05:50 commenté | Livré disque ; **non planifiable actuellement** car `orchestrator.json` Drive validé manque. |
| Orchestrateur enrichissement | Enchaîner maintenance, horaires, médias, intelligent et contenu structuré | JSON `enabled_stages`, cible zone/ville | checkpoints + rapports de chaque sous-agent | non actif | Livré disque avec exemple et checkpoint local. Ne pas activer avant configuration Drive, verrou et prévention du double passage média/contenus. |
| Google Hours | Compléter les horaires en réutilisant les caches | cibles BO, cache Google, Playwright/API en dernier | horaires et rapport | seulement via orchestrateur / ciblé | Livré disque, non planifié seul. Vérifier quota mensuel et secret FO→BO en environnement déployé. |
| Enrichisseur de contenus | Créer menus, produits, services, EAP et équipements | sources web, cache, objets Place/Shop | objets structurés + médias | quotidien 06:30 | Livré disque, planifié. Correctif Wix `source_quality_image_url()` présent ; preuves locales La Braise 38 éléments. Déploiement réel à confirmer. |
| Validateur ExperienceTmp | Publier les expériences certaines et enrichir les champs manquants | ExperienceTmp, proposition stockée/fichier, références BO | Experience + pivots, revue/rapport | quotidien 05:30 | Livré disque, planifié. Préserve valeur+unité de durée dans les tests/artefacts ; cas ambigus restent en revue. |
| Agent territorial Experience | Collecter des expériences par zone | classeur `experiences.xlsx` ou ancien JSON | candidats/ExperienceTmp via endpoint territorial | non planifié | Livré disque, flux à la demande ; ne pas ajouter au cron sans pilotage et smoke serveur. |
| Transféreur de lieux | Convertir Place/Shop/Page/Equipment avec plan figé | `transfers.xlsx`, source/destination, plan | cible + dépendances, source archivée logiquement | quotidien 01:50 | Livré disque, planifié. `LocationTypeTransfer` BO et endpoints plan/apply présents. |
| ObjectConversion | Convertir Event/Experience/EventSerie et cas structurels | demande BO ou endpoints dédiés, mapping, double validation | cible, dépendances transférées, source archivée | via revue BO / file transfert | Livré disque. Contrôleur transactionnel, séparation demandeur/approbateur et audit présents. Casino/ECLIPSO doivent passer ici. |
| Spotlights / Tags / Activity proposals | Produire les référentiels aval après enrichissement | classeurs/objets enrichis | Spotlight, tags, propositions d'activité | quotidien 07:10–07:50 | Livrés disque, planifiés. `activité collective` ne doit jamais être un fallback générique. |
| Facebook | Collecter les événements Facebook | cookies/profil, ville | HTML/sources EventTmp | aucune ligne dans ce manifeste | Script livré mais **oublié du crontab versionné** malgré le guide qui le dit déjà autonome. Chercher le cron historique réellement installé avant toute correction. |
| Instagram via curation | Exploiter légende/carrousel et préserver l'image | ligne Excel + post Instagram | EventTmp/média/OCR local | inclus dans curation 23:00 | Livré disque. La première image est tamponnée même sans extraction exploitable ; pas d'agent Instagram autonome observé. |
| Scrapers Billetweb/Eventbrite/HelloAsso/Meetup | Collecter des plateformes événementielles | ville/zone/pages | sources vers EventTmp | non planifiés individuellement | Livrés disque mais couverts partiellement par agrégateur/curation. Éviter des crons doublons avant comparaison des sources. |
| Affiliation / compétitions / terrasses / circuits | Fonctions métier spécialisées | classeurs, URL, JSON | liens affiliés, calendriers, terrasses, Circuit | non planifiés | Livrés ou historiques selon le module ; usage à la demande. Nécessitent décision métier avant planification. |
| Audits/corrections datés | Rattraper doublons, taxonomie, prix, médias ou fermetures | listes/manifestes datés | rapports et mutations ciblées | jamais | **Ponctuels**. Garder comme preuves reproductibles, pas comme agents pérennes. |

## Écarts, doublons et risques vérifiés

1. Le crontab du dépôt est modifié dans un worktree très sale et de nombreux
   agents récents sont encore non suivis par Git. Il ne constitue donc pas une
   preuve de livraison sur `develop` ni d'installation sur le Mac.
2. Facebook n'apparaît dans aucune ligne active du manifeste inspecté alors que
   le guide affirme que Facebook et Shotgun sont déjà autonomes. Il faut d'abord
   lire le crontab réellement installé et son journal avant d'ajouter une ligne.
3. `media_curator.py` et `enrichisseur_contenus.py` ont chacun un cron autonome,
   mais font aussi partie de l'orchestrateur d'enrichissement. L'activation de
   celui-ci sans exclusion créerait des passages redondants.
4. `enrichisseur.py`, le chasseur et l'améliorateur intelligent sont bien
   présents mais commentés. Les deux premiers sont bloqués par budget/plafond ;
   le dernier par l'absence du JSON Drive validé.
5. Les scrapers plateforme individuels existent mais ne sont pas planifiés. Les
   programmer sans matrice de sources ferait doublon avec agrégateur territorial
   et curation manuelle.
6. Les nombreux fichiers `*_prod_YYYYMMDD`, outils de correction, exports et
   journaux sont des rattrapages historiques. Ils ne doivent pas devenir des
   crons.
7. Le dépôt contient des clones de déploiement et des `old_scripts`; ils ne sont
   pas des sources canoniques. La source active est `scripts/izilife` et le BO
   XAMPP inspecté.

## Garanties confirmées dans le code

- Shotgun résout la ville demandée et filtre les événements hors zone par
  localité/coordonnées ; Lille n'est plus imposée aux événements d'autres villes.
- La curation Instagram conserve une première image en EventTmp incomplet quand
  OCR/LLM n'extrait rien ; l'OCR ambigu ne force pas de valeur.
- Les validateurs EventTmp/ExperienceTmp réutilisent les propositions fournies
  ou stockées et séparent revue/application.
- Les conversions BO sont transactionnelles, auditées et archivent la source au
  lieu de la supprimer physiquement.
- L'URL Wix 300×300 est transformée en variante 1200×1200 par
  `source_quality_image_url()` avant import produit.
- Les endpoints agents sont déclarés dans `izilife-admin/app/Config/Routes.php`
  et protégés par la famille de contrôles `X-Agent-Token` testée dans le BO.

## Ce qui reste non prouvé

- installation du crontab versionné sur le Mac ;
- dernières exécutions et codes retour de chaque agent en production ;
- état courant des deux événements désactivés et des 38 médias La Braise en BDD
  production (les artefacts locaux corroborent l'historique, mais aucun nouvel
  accès production n'a été effectué pendant cet audit) ;
- présence et contenu des fichiers Drive de pilotage réellement utilisés.

## Prochaine action sûre

Récupérer en lecture seule sur le Mac d'automatisation : `crontab -l`, les 300
dernières lignes de `izilife-cron.log`, la liste des fichiers JSON/classeurs de
pilotage Drive et les versions de code déployées. Comparer ensuite ces quatre
preuves au manifeste du dépôt avant toute activation, correction ou relance.

## Complément : architecture réelle côté BO (`Scraper.php`)

Le premier audit centré sur les scripts était insuffisant. Le fichier
`izilife-admin/app/Controllers/Scraper.php` fait 14 512 lignes et 808 951
octets. Il est une partie du moteur métier, pas seulement une façade HTTP.

### Couches observées

1. **Collecte vers les tampons** : `postAgentUploadEventSources`,
   `postAgentUploadEventImages`, `_ingestEvent`, `_ingestExperience` et les
   modèles `ScrapingEventTmp_model` / `ScrapingExperienceTmp_model` conservent
   HTML, JSON normalisé, URL source, image locale et état de revue.
2. **Routeur JSON générique** : `postIngestJson` délègue à `_ingestOneItem`,
   qui accepte Event, Experience, Place, Equipment, Offer, ExternalPromo,
   Circuit, Product, SportMatch et CalendarOccurrence. Ce routeur n'offre pas
   les mêmes garanties riches que les paquets spécialisés.
3. **Graphes spécialisés** : `postAgentIngestEventPackage` délègue à
   `AgentEventPackage_model` pour une transaction EventSerie /
   AnnualCelebration / LocalEvent / programmation / prix / médias /
   organisateurs / sources / récurrence. Les paquets Place/Shop, Experience et
   Circuit ont leurs moteurs dédiés.
4. **Validation** : les endpoints EventTmp, ExperienceTmp, POI et
   `validation_request` délèguent principalement aux modèles `Agent*Validator`.
   Les analyses et les applications sont séparées, mais une part importante de
   l'orchestration et des prompts reste dans le contrôleur.
5. **Enrichissement des lieux** : Google/cache, analyse éditoriale, horaires,
   fermeture, contenu de site et médias sont des flux différents. Ils passent
   par `GoogleBusinessEnrichment_model`, `AgentOpeningHours_model`,
   `AgentLocationMaintenance_model`, `AgentSiteContent_model` et
   `AgentScopedMedia_model`.
6. **Catalogue commercial** : `importProductsToDbDirect` et ses helpers gèrent
   encore directement dans `Scraper.php` les Product, catégories, prix,
   packaging, attributs, options, inventaire, médias et `ElementMenu`. Ce bloc
   est donc critique pour toute extraction JSON de carte/menu.

### Contrats d'écriture à distinguer

| Besoin | Point d'entrée canonique | Comportement |
|---|---|---|
| Source événement simple | `agentUploadEventSources` | Crée/complète un EventTmp ; validation ultérieure. |
| Image/affiche événement | `agentUploadEventImages` | OCR/analyse puis EventTmp, avec tampon image possible. |
| Graphe événement complet | `agentIngestEventPackage` | Transaction riche avec racine, éditions, occurrences, programmation, prix et relations. |
| Expérience collectée | `agentStageExperience` | Passe toujours par ExperienceTmp ; l'ancien `agentUpsertExperience` est désormais un alias de staging. |
| Contenu Place/Shop approuvé | `agentIngestSiteItem` | Equipment via modèle, Product via importeur direct, autres contenus via `AgentSiteContent_model`. |
| Image de menu produit | `agentIngestProductImage` | OCR IA, extraction quantités, puis import direct de Product. Cette route écrit réellement et n'est pas un simple analyseur. |
| Analyse d'un site | `agentAnalyzeSiteContent` | Enrichit d'abord le contexte Google/cache, sélectionne les référentiels, puis produit une analyse structurée. |
| Conversion Place/Shop/Page/Equipment | `LocationTypeTransfer` | plan/apply, copie contrôlée, source archivée logiquement. |
| Conversion Event/XP/Série | `ObjectConversion` | workflow BO distinct avec demande, double regard et transaction. Le code actuel doit primer sur les notes historiques parlant de purge physique. |

### Objets et relations importantes pour les futurs JSON

- **Événement** : `LocalEvent` est l'occurrence ou l'événement concret ;
  `EventSerie` et `AnnualCelebration` sont des coquilles éditoriales ;
  `Representation` groupe des séances ; `is_another_date_of` relie les dates ;
  `RecurrenceRule` porte une cadence ; `EventHourly` décrit les ouvertures d'un
  événement continu, jamais une liste de séances ; `EventProgrammation` est une
  ligne de programme légère.
- **Expérience** : `ExperienceTmp` est le tampon canonique de tous les
  producteurs. L'objet final conserve valeur et unité de durée, type, accès,
  réservation, activité principale, langues, occasions, publics, hobbies et
  pivots éditoriaux. Les sessions sont un flux séparé.
- **Lieu** : Place et Shop restent deux familles legacy. Une salle ou un
  Equipment interne est un enfant/rattachement et ne doit pas bloquer la
  résolution du lieu principal. Page représente plutôt une personne,
  organisation ou marque éditoriale.
- **Catalogue** : Product est l'objet vendu ; ProductCategory organise ;
  ElementMenu sélectionne et ordonne des catégories/produits ; un produit
  composé utilise les slots existants. ElementService décrit un service ;
  ElementAccessPrice décrit un droit/tarif. `NULL` n'est ni gratuit ni zéro.
- **Sources** : `ContentSourceReference` normalise et mémorise les URL déjà
  associées. `scrapping_json` / `raw_json` sont des caches métier à réutiliser,
  pas des champs jetables.
- **Médias** : `AgentScopedMedia_model` résout le scope, déduplique par hash et
  rattache selon le pivot propre à l'objet. Le téléchargement, l'analyse et le
  rattachement sont trois opérations différentes.

### Sécurité et limites structurelles

- Les pages BO de revue utilisent session + `adminauth`/CSRF. Les routes
  `scraper/agent*` sont exemptées du CSRF global mais chaque méthode doit appeler
  `_checkAgentToken()` et vérifier `X-Agent-Token`.
- Les routes sont très nombreuses et la présence dans `Routes.php` ne suffit
  pas : il faut vérifier dans chaque méthode l'appel au token, le mode dry-run,
  la transaction et le statut HTTP.
- Plusieurs anciennes documentations disent « tout passe par TMP » ou « jamais
  d'écriture directe ». Ce n'est plus universellement vrai : les upserts de
  référentiels, médias, Products, Services/EAP et paquets approuvés écrivent
  directement. La règle correcte est désormais : collecte incertaine vers TMP ;
  paquet approuvé ou action déterministe vers un endpoint d'écriture explicite.
- `Scraper.php` mélange encore transport, prompts, résolution, import et logique
  catalogue. Toute modification doit donc être accompagnée d'un test du modèle
  appelé et d'un test de contrat de route, pas seulement d'un lint du contrôleur.

### Sources de vérité retenues

En cas de contradiction, ordre de confiance : code courant du contrôleur et des
modèles, schéma SQL courant `izilife-db/principal`, tests exécutables, puis docs
datées. Les documents `izilife-global.md` et anciens guides restent utiles pour
le vocabulaire produit mais contiennent des règles dépassées, notamment
« aucune écriture directe » et certaines descriptions de purge.
