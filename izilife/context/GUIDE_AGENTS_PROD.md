# Guide pratique des agents iziLife — lancement manuel en production

Pour l'installation Windows/Mac, les variables d'environnement, le crontab
général et l'inventaire compact des commandes, lire aussi
`LANCER_AGENTS_WINDOWS_MAC.md`.

Document de reprise : il explique quoi remplir, ce que fait chaque script et comment le lancer explicitement en production. Il décrit les scripts présents dans `C:\Users\alcamara\Documents\agentic_Workspace\scripts\izilife` au 25 octobre 2026. Il ne signifie pas que chaque parcours a été validé en production.

## 1. Règles de lancement

Ouvrir PowerShell et définir les chemins une fois :

```powershell
$py = 'C:\Users\alcamara\AppData\Local\Python\pythoncore-3.14-64\python.exe'
$root = 'C:\Users\alcamara\Documents\agentic_Workspace\scripts\izilife'
```

Le modèle de commande est :

```powershell
& $py "$root\CHEMIN\agent.py" --zone=lille --env=prod --dry-run
```

Enlève `--dry-run` uniquement quand tu as vérifié la cible, les lignes à traiter et le résultat simulé. Sans `--dry-run`, le script appelle l’API de production. Pour les agents qui lisent un classeur, l’agent traite normalement les lignes ayant le statut `pending`; `done`, `skip` ou les lignes vides ne sont pas une demande de création. Les agents font souvent un upsert, mais ne pars pas du principe qu’une relance est sans effet : vérifie le résultat dans le BO après un petit lot.

Les classeurs sont séparés par environnement sur le Drive synchronisé : local (`agentic_workspace_local`), staging (`agentic_workspace_staging`) et prod (`agentic_workspace`). Le script doit recevoir `--env=prod` pour lire le classeur prod et appeler l’API prod. `--zone=lille` sélectionne généralement le dossier `lille-zone`. Ne copie pas le classeur staging par-dessus celui de prod.

Options communes : `--init` crée un modèle s’il n’existe pas (il ne remplace normalement pas un classeur existant); `--dry-run` évite généralement l’écriture métier, mais son comportement dépend du script — il peut quand même lire des pages, lancer Playwright ou appeler un endpoint de préparation; `--max=N` borne les lignes, quand cette option est disponible. Pour les recherches Google/Playwright et l’IA, dry-run ne garantit pas l’absence de consommation externe. Les commandes ci-dessous sont des modèles prudents avec un petit plafond lorsqu’il existe.

## 2. Le parcours de curation à retenir

1. Choisir le bon agent et le bon environnement (`prod` seulement pour la production).
2. Ouvrir le classeur correspondant et remplir une ligne à la fois. Employer les `string_id`/références iziLife prévus par le champ, pas un ID numérique copié au hasard.
3. Laisser la ligne en `skip` pendant la préparation; la passer à `pending` lorsqu’elle est prête à être traitée.
4. Lancer d’abord en `--dry-run` lorsque l’option existe. Puis lancer un seul objet ou un petit `--max` sans `--dry-run`.
5. Lire `last_result`/le journal et vérifier le résultat dans le BO avant de poursuivre. Corriger une ligne `error` avant de la remettre en `pending`.

`scope_type` dit de quelle sorte d’objet il s’agit (par ex. `SHOP`, `EVENT`, `EXPERIENCE`); `scope_ref`/`scope_string_id` désigne généralement son `string_id`. Les colonnes `status`, `notes`, `last_result` servent au suivi, pas au contenu métier. Les champs finissant par `_ref` désignent habituellement un identifiant stable/référentiel iziLife.

## 3. Lieux — le groupe à manier avec le plus de prudence

### `places/createur_lieux.py` — ajout manuel d’un lieu nommé

Classeur `places\lille-zone\curate_places.xlsx`, onglet `Lieux`. Une ligne signifie « recherche ce commerce/lieu précis dans cette ville, puis crée-le s’il n’existe pas déjà ». Le script délègue la recherche Google Places et l’import au contrôleur PHP.

Le corps envoyé à `agentFetchAndStoreOnePlace` est du JSON. La route conserve aussi la compatibilité avec les anciens appels formulaire, sans tenter de décoder ces formulaires comme du JSON.

Colonnes : `NOM` (nom recherché), `VILLE` (obligatoirement le `City.string_id` iziLife, par exemple `marcq-en-baroeul`), `TYPE_IMPOSE` (`SHOP`, `PLACE`, `EQUIPMENT` ou vide si Google doit orienter le type), `CATEGORY_STRING_ID` (référence stable du référentiel cible, par exemple `restaurant` ou `musee`), `IN_ON_PLACE_REF` (`Place.string_id` facultatif du contenant, par exemple `aushopping-v2`), `NOTES` (mémo humain), `STATUT` (`pending`, `done`, `unmapped`, `error`, `skip`). `TYPE_IMPOSE` et `CATEGORY_STRING_ID` doivent être renseignés ensemble. Le classeur et la route n'utilisent pas d'identifiant numérique de catégorie : les IDs diffèrent entre local, staging et production et sont résolus par le backend de destination.

Pour les `PLACE`/`SHOP`, un homonyme déjà présent dans une autre ville ne bloque plus la création : le backend utilise `<string_id-de-base>-<City.string_id>`. Avec `IN_ON_PLACE_REF`, il essaie ensuite des variantes déterministes issues du centre (`<base>-v2`, `<base>-<ville>-v2`, puis référence complète). Le cas ne passe en validation qu'après épuisement de ces variantes. Le `google_place_id` reste prioritaire pour reconnaître une fiche déjà existante.

```powershell
& $py "$root\places\createur_lieux.py" --zone=lille --city=lille --env=prod --dry-run
# après contrôle :
& $py "$root\places\createur_lieux.py" --zone=lille --city=lille --env=prod
```

### `places/chasseur_lieux.py` — collecte par catégories, puis insertion

Ce n’est pas le créateur d’un nom précis. Il parcourt le classeur de pilotage des villes/catégories, collecte des résultats Google Places dans `À créer`, puis peut insérer les lignes. Il existe deux phases : `--max-duration` borne la collecte; `--max-insert-duration` et `--max-insert` bornent séparément l’insertion. `--max-insert` vaut 20 par défaut ; les deux limites de durée valent `0` (pas de plafond). Fixe-les explicitement pour les essais.

Classeurs/fichiers : `izilife_villes.xlsx` (onglets `Villes`, `À créer`, `Catégories`) et `categories_lieux.json`. Dans `Villes`, renseigner/activer la ville et les paramètres de priorité; `Catégories` choisit les catégories de recherche et leur état actif; `À créer` conserve le résultat trouvé (`nom`, adresse, ville, `google_place_id`, catégorie/types Google, statut/date). Le script tient aussi à jour les statuts d’enrichissement et journaux.

`ville_slug` et `--city` contiennent obligatoirement un `City.string_id` iziLife. La « catégorie » du chasseur sert à former la recherche Google Maps ; elle ne force pas une `ShopCategory`, un `PlaceType` ou une `EquipmentCategory`. Le script envoie `destination` et `category_string_id` vides, puis le backend classe le résultat à partir de ses types Google et des référentiels de l’environnement cible. Seul `createur_lieux.py`, avec `TYPE_IMPOSE`, exige une catégorie métier explicite.

```powershell
& $py "$root\places\chasseur_lieux.py" --zone=lille --env=prod --city=lille --max-per-cat=5 --max-duration=180 --max-insert-duration=180 --max-insert=5 --dry-run
# collecte/insertion réelle seulement après inspection du classeur :
& $py "$root\places\chasseur_lieux.py" --zone=lille --env=prod --city=lille --max-per-cat=5 --max-duration=180 --max-insert-duration=180 --max-insert=5
```

`--collect-only` ne fait que collecter; `--insert-only` ne fait que traiter la file déjà collectée; ne pas les combiner. `--retry-errors` réessaie aussi les erreurs et doit être volontaire. `--max-per-cat` borne les fiches par catégorie, pas le nombre total de créations. `--dry-run` ne protège pas contre la collecte Google elle-même : il s’agit d’un mode d’écriture API, pas nécessairement d’un mode sans appels externes.

### `places/chasseur_lieux_manuel.py` — lancer une recherche ville + catégorie

Accélérateur de recherche manuelle par catégorie, non équivalent à `createur_lieux.py`. Aucun fichier d’entrée de curation par nom : tu fournis les critères dans la commande. `--city` est un `City.string_id`, y compris en dry-run. La catégorie sert uniquement à la recherche Google ; le classement métier final reste automatique. `--max-results` vaut par défaut 10 000; le parcours peut continuer tant que le scraper trouve des résultats (ce chiffre n’est pas une borne de temps). Il n’y a pas de `--max-duration`.

```powershell
& $py "$root\places\chasseur_lieux_manuel.py" --zone=lille --city=calais --category=restaurant --env=prod --max-results=5 --dry-run
```

Enlever `--dry-run` envoie les résultats au backend. Utiliser une zone de classeur valide, et une ville/catégorie précises. Ne pas démarrer une recherche large en production sans réduire/contrôler la portée.

### `places/enrichisseur.py` — améliorateur classique

Améliore des lieux déjà enregistrés (parcours classique, sans la curation Produits/Services/EAP de l’agent ++). Il utilise le classeur `ameliorateur.xlsx`, notamment l’onglet `Prioritaires`. Le classeur est à la fois une file de priorités d’enrichissement et un outil de maintenance manuelle pour les `PLACE`/`SHOP`.

Colonnes d’identification et de suivi : `string_id`, `type` (`PLACE`/`SHOP`), `notes`, `statut`, `last_result`. Colonnes de maintenance facultatives : `ferme_definitivement` (ancienne case conservée), `is_active`, `listable`, `closed_state_ref`, `is_new_in_city`, `opening_date`, `category_refs`, `primary_category_ref`, `other_category_refs`, `other_categories_mode`.

- `closed_state_ref` accepte `ouvert`, `ferme-temporairement` ou `ferme-definitivement`. Une fermeture définitive force `is_active=0` et `listable=0` si ces deux champs ne sont pas explicitement renseignés. Une fermeture temporaire ne désactive pas automatiquement la fiche.
- Pour un nouveau lieu, renseigner `is_new_in_city=OUI` et `opening_date` au format `YYYY-MM-DD`.
- `category_refs` est la saisie recommandée pour les catégories : la première référence devient la catégorie principale, les suivantes deviennent secondaires. Pour un Shop, la première est obligatoirement recherchée dans `ShopCategory`; pour une Place, elle est obligatoirement recherchée dans `PlaceType`. Lors d'un changement, l'ancienne catégorie principale est conservée comme catégorie secondaire, comme dans le BO. `primary_category_ref` reste accepté pour compatibilité technique.
- `other_category_refs` accepte plusieurs `string_id` séparés par des virgules ou points-virgules. Les secondaires peuvent provenir indifféremment de `PlaceType` ou `ShopCategory`, quel que soit le type du lieu. Une référence présente dans les deux référentiels doit être préfixée par `PLACE:` ou `SHOP:` (par exemple `SHOP:patisserie`). `other_categories_mode` vaut `ADD`, `REPLACE` ou `REMOVE`; avec `REPLACE`, l'ancienne catégorie principale reste conservée si la principale change sur la même ligne.
- Dès qu'une colonne de maintenance est renseignée, la ligne est traitée par l'API de maintenance et ne lance ni Google ni Playwright. Une ligne sans action de maintenance reste une demande d'enrichissement classique.

Les anciens classeurs restent lisibles. Pour ajouter les nouvelles colonnes, utiliser explicitement `--upgrade-workbook`; la commande crée d'abord une copie `ameliorateur.backup-AAAAMMJJ-HHMMSS.xlsx`. Elle doit être exécutée séparément pour chaque environnement et ne fait aucune écriture métier :

```powershell
& $py "$root\places\enrichisseur.py" --zone=lille --env=local --upgrade-workbook
& $py "$root\places\enrichisseur.py" --zone=lille --env=staging --upgrade-workbook
# production : commande à lancer manuellement uniquement au moment choisi
& $py "$root\places\enrichisseur.py" --zone=lille --env=prod --upgrade-workbook
```

```powershell
& $py "$root\places\enrichisseur.py" --zone=lille --city=lille --env=prod --max=3 --dry-run
```

`--score-max` règle le seuil de sélection; `--type=SHOP` ou `--type=PLACE` filtre; `--priority-only` limite aux priorités du fichier. `--purge` déplace les lignes `done` vers les logs : ne l’ajouter que si tu veux réellement archiver ces lignes.

Pour une maintenance manuelle bornée, toujours utiliser `--priority-only`; les lignes de maintenance sont appliquées avant le parcours d'enrichissement et sont donc traitées sans recherche Google :

```powershell
& $py "$root\places\enrichisseur.py" --zone=lille --city=lille --env=prod --priority-only --max=1 --dry-run
```

### `places/enrichisseur_contenus.py` — améliorateur ++ (produits, services, EAP)

Classeur `enrichisseur_contenus.xlsx`, onglet `Sources`. Champs : `SCOPE_TYPE`/`SCOPE_REF` (objet à enrichir), `IMAGE_DIRECTORY` (photos locales), `URL_1..URL_10` (sources à analyser), `NOTES`, `LLM_INSTRUCTIONS`, `STATUS`, `LAST_RESULT`. Le traitement peut solliciter Playwright et le fournisseur IA configuré; par préférence actuelle, préciser `--llm-provider openai` pour éviter le fournisseur Claude.

```powershell
& $py "$root\places\enrichisseur_contenus.py" --zone=lille --env=prod --max=1 --llm-provider=openai --dry-run
```

`--analyze-only` analyse les sources sans appel d’écriture/upsert; `--scope-ref` et `--source-url` (répétables) restreignent le diagnostic; `--fixture-file` injecte des résultats de test. Sans `--analyze-only`/`--dry-run`, la ligne pending est destinée à importer/upserter les objets extraits (Products, Services, activités proposables selon les données reconnues).

Le BO classe et borne les référentiels injectés dans chaque prompt. Une erreur OpenAI `context_length_exceeded` est non relançable telle quelle : l’agent ne répète pas trois fois la même requête trop longue. Après livraison d’un correctif de référentiel, remettre explicitement la ligne en `retry` ou `pending` avant une nouvelle exécution.

## 4. Événements et dates

### `events/ingest_manual_curate.py` — curation manuelle par URL

Classeur `events\lille-zone\curate_events.xlsx`. Onglets par source : `Facebook`, `Shotgun`, `HelloAsso`, `Eventbrite`, `Meetup`, `Instagram`. Colonnes `url`, `status`, `notes`, `added_at`, `processed_at`. Tu ajoutes les liens que tu as sélectionnés; le script ouvre/traite les sources Playwright selon l’onglet et envoie les événements détectés pour validation/import. Facebook est un parcours manuel que tu déclenches toi-même; ne le confonds pas avec le scraper automatique Facebook.

```powershell
& $py "$root\events\ingest_manual_curate.py" --zone=lille --city=lille --sheet=Shotgun --env=prod --dry-run
```

`--sheet` accepte une source ou `all`. Pour garder le lancement déterministe et éviter d’embarquer Facebook involontairement, choisir explicitement l’onglet à traiter.

Pour Instagram, l’agent tente d’abord les médias publics exposés par la publication elle-même, puis utilise iGram et les autres services comme secours. Une panne DNS ou l’absence de résultat de ces services ne doit donc plus être le premier chemin d’échec; une publication privée ou protégée peut néanmoins rester impossible à récupérer.

### Scrapers de source, différents de la curation URL

Les scrapers parcourent une source pour une ville; ils ne signifient pas que chaque résultat est éditorialement validé. `--max-events=0` signifie illimité pour plusieurs de ces scripts : fournir une limite. Options habituelles : `--env`, `--city`, `--zone`, `--pages`, `--max-events`, `--dry-run`.

```powershell
& $py "$root\events\shotgun_scraper.py" --city=lille --env=prod --pages=1 --max-events=5 --dry-run
& $py "$root\events\facebook_scraper.py" --city=lille --env=prod --max-events=5 --dry-run
& $py "$root\events\billetweb_scraper.py" --city=lille --zone=lille --env=prod --pages=1 --max-events=5 --dry-run
& $py "$root\events\eventbrite_scraper.py" --city=lille --zone=lille --env=prod --pages=1 --max-events=5 --dry-run
& $py "$root\events\helloasso_scraper.py" --city=lille --zone=lille --env=prod --pages=1 --max-events=5 --dry-run
```

Facebook automatique reste un outil distinct que tu as indiqué lancer manuellement. Meetup est marqué « pas besoin » dans les consignes précédentes; HelloAsso/Eventbrite sont optionnels selon le besoin. `link_scraper.py` prend une URL précise via `--url`; il ne remplace pas le classeur de curation. `send_sources.py` est annoncé comme remplacé par Playwright; ne pas l’utiliser pour une nouvelle procédure. `instagram/saved_collections.py` est destiné à être retiré plus tard.

### `events/event_structures.py` — coquilles EventSerie / AnnualCelebration / récurrent

Classeur `events\lille-zone\event_structures.xlsx`, onglet `Structures`. Une ligne par objet parent/coquille. Types `EVENT_SERIE`, `ANNUAL_CELEBRATION` ou `RECURRENT_EVENT`. Identifiants métier : `string_id` pour les structures; `unique_id` pour l’événement récurrent LocalEvent. Champs d’identité/texte : `object_type`, `string_id`, `unique_id`, `name`, `description`, `event_category_ref`. Propriétaire/lieu : `partner_ref`, `page_ref`, `location_ref`, `default_location_ref`, `default_address`, `default_address_complement`, `default_zip_code`, `default_city`, `default_city_ref`, coordonnées, `scope_ref`. Réglages d’objet/visibilité : `is_active`, `listable`, `celebration_day_ref`, `can_be_linked_by_others`, `is_internal`, `news_visibility_days_before`, indicateurs de série iziLife. Accès/prix : `access_type_ref`, `booking_needed_ref`, `access_on_booking`, `access_text`, `access_link`, `basic_price`, `currency_ref`. Catégories : `principal_activity_category_ref`, `default_event_category_ref`. Première occurrence : `first_title`, `first_start_date/hour`, `first_end_date/hour`. Récurrence : `start_date/hour`, `end_date/hour`, `recurrence_frequency`, `recurrence_interval`, `recurrence_days`, `recurrence_month_day`, `recurrence_until`, `recurrence_rrule`, `timezone_id`, `horizon_days`, `count_limit`. Enfin `status`, `notes`, `last_result`.

```powershell
& $py "$root\events\event_structures.py" --zone=lille --env=prod --max=1 --dry-run

### Dossier événementiel intelligent — JSON conversationnel

Pour un site/PDF/carrousel décrivant un événement complexe ou plusieurs événements éditoriaux, ne pas utiliser le classeur `event_structures.xlsx`. La conversation chargée du dossier suit obligatoirement [le contrat EVENT_GRAPH_PACKAGE](agents/EVENT_GRAPH_PACKAGE.md), produit un document `izi.event.package.v1`, puis l'envoie à `POST /scraper/agentIngestEventPackage`. Le BO matérialise en une transaction la série ou célébration, sa première édition, les LocalEvent enfants ou liés, `EventHourly`, `EventProgrammation`, tarifs, organisateurs, caractéristiques, sources et médias. `dry_run=true` valide et rapproche le paquet sans conserver d'écriture.
```

Pour un récurrent quotidien/hebdomadaire/etc., renseigner la fréquence et les bornes, plutôt que créer manuellement chaque occurrence. Le classeur permet de préparer beaucoup de lignes, mais commence avec `--max=1` et vérifie l’objet parent et ses occurrences générées.

### `events/event_calendar.py` — nouvelle date, report, annulation, clôture

Classeur `events\lille-zone\event_calendar.xlsx`, onglet `Calendar`. Colonnes `scope_type`, `scope_ref`, `operation`, `title`, `start_date`, `start_hour`, `end_date`, `end_hour`, `date_from`, `date_to`, `reason`, `is_active`, `listable`, `status`, `notes`, `last_result`. `scope_type` accepte `EVENT`, `EVENT_SERIE`, `ANNUAL_CELEBRATION`; `EVENT` se référence par `unique_id`, les structures par `string_id`. Opérations reconnues par le modèle : `ADD_DATE`, `CANCEL_DATE`, `CANCEL_PERIOD`, `POSTPONE_EVENT`, `CLOSE_RECURRENCE`.

```powershell
& $py "$root\events\event_calendar.py" --zone=lille --env=prod --max=1 --dry-run
```

### `events/event_images.py` — images locales/Drive pour événements

Pas de classeur de lignes : commande avec `--city` et un dossier source `--dir` ou `--drive`; `--recursive` étend aux sous-dossiers; `--dry-run` prévisualise.

```powershell
& $py "$root\events\event_images.py" --city=lille --env=prod --drive='G:\Mon Drive\agentic_workspace\izilife\events\lille-zone\images' --dry-run
```

Sans `--recursive`, ne suppose pas que les sous-dossiers seront parcourus. Le traitement peut envoyer les images au backend pour reconnaissance/attachement; inspecte d’abord le dossier choisi.

### `competitions/fetch_competition_schedule.py` — éditions et matchs

Le fichier `competitions\competition-planning.xlsx`, onglet `Éditions`, est le pilotage : une ligne par compétition/édition à synchroniser, pas une ligne par match. Colonnes : `active` (Oui/Non), `competition_string_id`, `season_label`, `edition_name`, `starts_at`, `ends_at`, `schedule_source_url`, `import_mode` (`AUTO`, `FORCE`, `SKIP`). Les dates vides laissent les dates déjà au BO. Le script prépare l’édition puis récupère/import les matchs depuis la source configurée; les matchs ne sont donc pas saisis un par un dans l’Excel.

```powershell
& $py "$root\competitions\fetch_competition_schedule.py" --env prod --dry-run
```

`--competition=ligue-1` cible une seule compétition; `--season` et `--url` la précisent. `--file` choisit un Excel/CSV; `--all` ignore le fichier et prend le plan du BO; éviter `--all` si le classeur est la configuration que tu veux piloter. `--force` force une relecture. `SKIP` prépare l’édition sans charger de matchs. Le classeur modèle est dans le dossier du script, donc la commande `--init` n’utilise pas le Drive; vérifier le chemin du fichier avant d’initialiser une copie de prod.

## 5. Créations et curation d’objets

### `experiences/experience.py` — expérience saisie manuellement

Classeur `experiences\lille-zone\experiences.xlsx`, onglet `Experiences`. Une ligne par expérience. Colonnes : `title`, `experience_string_id`, `city_ref`, `description`, `short_description`, `experience_type_ref`, `experience_theme`, `principal_activity_category_ref`, `access_type_ref`, `booking_needed_ref`, `access_link`, `price_text`, `basic_price`, `duration`, `duration_measurement_unity_id`, `place_ref`, `shop_ref`, `phone_number`, `exterior`, `with_equipment`, `equipment_gived`, `is_nocturnal`, `noise_level`, `participation_mode`, `minimal_age`, `minimal_number_of_people`, `maximal_number_of_people`, `is_for_kids`, `accessible_for_kids`, `is_insolite`, `experience_in_all_city`, `place_visit`, `source_url`, `status`, `notes`, `last_result`. Références `_ref`/`_id` doivent correspondre aux référentiels BO; `place_ref`/`shop_ref` rattachent l’expérience si elle n’est pas à l’échelle de toute la ville.

```powershell
& $py "$root\experiences\experience.py" --zone=lille --env=prod --max=1 --dry-run
```

### `terraces/terraces.py` — terrasse sur Place/Shop

Classeur `terraces\lille-zone\terraces.xlsx`, onglet `Terrasses`. Colonnes : `scope_type`, `scope_ref`, `name`, `type_ref`, `description`, `capacity`, `is_rooftop`, `is_privatizable`, `hidden`, `source_url`, `status`, `notes`, `last_result`. Le type est parmi `prive`, `espace-public`, `sur-une-rue-connue`, `sur-une-place-connue`; l’URL est une inspiration, les champs restent curatés manuellement.

```powershell
& $py "$root\terraces\terraces.py" --zone=lille --env=prod --max=1 --dry-run
```

### `agent_pages.py` — pages/personnes/organisations iziLife

Classeur `pages\lille-zone\pages.xlsx`, onglet `Pages`; dossiers de médias associés sous `pages\lille-zone\medias\`. Champs : `NOM`, `CATEGORIE`, `EMAIL`, `TELEPHONE`, `DESCRIPTION`, `LIEN_1..LIEN_8`, `MEDIA_DIRECTORY_NAME`. Catégorie attend une valeur PageCategory `string_id` (ex. `association`, `artiste-groupe`, `organisateur-d-evenements`), pas son libellé affiché. Les liens peuvent aussi alimenter la description manquante; les images/vidéos du sous-dossier nommé sont téléversées à la création.

```powershell
& $py "$root\agent_pages.py" --zone=lille --env=prod --max=1 --dry-run
```

### `agent_external_media.py` — liens sociaux/vidéo vers un objet

Classeur `ambiance\lille-zone\ambiance.xlsx`, onglet `Ambiances`. `TARGET_REF` (string_id ciblé), `TARGET_TYPE` (`PAGE`, `PLACE`, `SHOP`, `EVENT`, `EVENT_SERIE`, `ANNUAL_CELEBRATION`, `EXPERIENCE`), `SOURCE` (`AUTO`, instagram, tiktok, youtube, facebook, website), `LIEN_1..LIEN_8`. Chaque lien valide est associé séparément; les doublons sont ignorés.

```powershell
& $py "$root\agent_external_media.py" --zone=lille --env=prod --max=5 --dry-run
```

### `medias/media_curator.py` — téléverser/associer des fichiers média

Classeur `medias\lille-zone\media_curation.xlsx`, onglet initial `Medias`; médias locaux dans `medias\lille-zone\sources\`. Colonnes : `SCOPE_TYPE`, `SCOPE_REF`, `MEDIA_GROUP` (`SIMPLE`, `CAROUSEL`, `BEFORE`, `AFTER`), `SOURCE_TYPE` (`INSTAGRAM`, `DIRECTORY`), `SOURCE_URLS`, `URL_1..URL_10`, `DIRECTORY_NAME`, `TITLE`, `DESCRIPTION`, `PRINCIPAL`, `RIGHTS_CONFIRMED`, `BELONGS_TO_SCOPE`, `STATUS`, `LAST_RESULT`, `OWNER_PAGE_STRING_ID`, `TAG_REFS`. Le scope peut notamment être `PLACE`, `SHOP`, `PAGE`, `EVENT`, `EVENT_SERIE`, `ANNUAL_CELEBRATION`, `EXPERIENCE`, `CITY`, `ADMINISTRATIVE_DIVISION`, `TERRACE`. Ici `DIRECTORY_NAME`/`URL_n` désigne les fichiers/sources du groupe, tandis que `OWNER_PAGE_STRING_ID` est destiné à la propriété Page si le média n’appartient pas directement au scope. N’utilise pas le mode propriétaire Page sans vérifier son fonctionnement BO/API dans la version déployée.

```powershell
& $py "$root\medias\media_curator.py" --zone=lille --env=prod --max=1 --dry-run
```

### `media_downloader.py` — télécharger des images Instagram via iGram

Classeur `medias\medias_igram.xlsx`, onglet `Medias`; l’onglet `Logs` est le journal. C’est un téléchargeur, pas un importateur d’objet iziLife. En-têtes de file : `URL`, `Type`, `Etat`. `Type` accepte `photo`, `carousel`, `story`, `reel` (des alias français sont reconnus); `Etat` vide, `pending`, `retry` ou `error` autorise le téléchargement. Le journal ajoute `URL`, `Type`, `Etat`, `Traité le`, `Nb fichiers`, `Fichiers`, `Message`. Ce script n’a pas `--zone`; `--env=prod` choisit le répertoire Drive prod.

```powershell
& $py "$root\media_downloader.py" --env=prod --max=1 --dry-run
```

`--max=0` signifie toutes les lignes en attente; pour une reprise, préciser un nombre borné. `--root` remplace explicitement le dossier de travail médias. Le téléchargement vers le dossier n’attache pas à lui seul l’image à un scope : c’est le travail du curateur média.

## 6. Éditorial, offres et configuration d’objets

### `spotlights/spotlight.py` — Spotlight classique, éditorial et rails

Classeur `spotlights\lille-zone\spotlights.xlsx`, onglet `Spotlights`. Identité/cible : `scope_type`, `scope_ref`, `city_ref`; éditorial : `editorial_title`, `editorial_description`, `theme`; destinations : `target_spotlight`, `target_perfect_for`, `target_today`, `target_next_days`, `rail_editorial_reason`, `rail_configuration_json`, `reasons_json`; période/priorité : `start_date`, `end_date`, `priority`, `base_weight`, `publication_status`; suivi : `status`, `notes`, `last_result`.

Pour chaque raison `GOOD_FOR`, cinq groupes de colonnes `good_for_1_...` à `good_for_5_...` permettent de saisir type/référence, poids, titre/texte et contexte propre : `type`, `ref`, `weight`, `editorial_title`, `editorial_description`, `days_of_week`, `visit_moments`, `start_month`, `end_month`, `visit_weathers`. Le script convertit les champs de contexte en JSON; pas besoin d’écrire du JSON à la main pour ces contextes. `days_of_week` = 1 lundi à 7 dimanche; listes séparées par virgules; moments et météo sont des `string_id`; les deux mois doivent être fournis ensemble. Le JSON vide vaut null. Ne mets pas de contexte sur WHY. `rail_configuration_json` reste le réglage du Spotlight classique : ne le change pas pour configurer un `GOOD_FOR`.

```powershell
& $py "$root\spotlights\spotlight.py" --zone=lille --env=prod --max=1 --dry-run
```

### `activity_proposals/activity_proposal.py` — activités proposables avec contexte

Classeur `activity-proposals\lille-zone\activity_proposals.xlsx`, onglet `ActivityProposals`. Colonnes : `scope_type`, `scope_ref`, `occasion_ref`, `action_1..action_3`, `title_template`, `contextual_description`, `days_of_week`, `visit_moments`, `start_month`, `end_month`, `visit_weathers`, `special_activity_show`, `is_active`, `status`, `notes`, `last_result`. Les cinq champs contexte sont convertis en `context_json` automatiquement avec les mêmes règles que Spotlight : jours 1–7, listes string_id de moments/météos, mois début/fin obligatoires ensemble; contexte vide = null.

```powershell
& $py "$root\activity_proposals\activity_proposal.py" --zone=lille --env=prod --max=1 --dry-run
```

### `offers/special_offer.py` — Offre + BenefitPlanReward + Effect

Classeur `offers\lille-zone\special_offers.xlsx`, onglet `Offres`. Cible : `scope_type`, `scope_string_id`; éventuellement `special_campain_string_id`. Offre : `title`, `deal`, `note`, `promotion_mechanic_string_id`, `offer_hours`, `start_date`, `end_date`, `priority`, `is_active`, `offer_access_code`, `code_start_date`, `code_end_date`, `max_total_uses`, `max_uses_per_user`. Récompense/effet : `bpr_title`, `effect_label`, `bpr_benefit_resume`, `bpr_promotion_mechanic_string_id`, `bpr_value_int`, `bpr_currency`, `bpr_x_qty`, `bpr_y_qty`, `bpr_benefit_target`, `bpr_on_izilife_object`, `bpr_delivery_mode`, `bpr_external_promotion_code`, règles d’utilisation `bpr_usable_days`, `bpr_access_hours`, `bpr_blackout_hours`, `bpr_last_use_time`, `bpr_opening_hours_required`, `bpr_allow_if_opening_hours_unknown`, dates de validité, priorité/actif et suivi.

```powershell
& $py "$root\offers\special_offer.py" --zone=lille --env=prod --max=1 --dry-run
```

### `offers/izilife_subscription_benefit.py` — récompense attachée à un plan

Classeur `izilife_subscription_benefits.xlsx`, onglet `Avantages abonnements`. Champs : `scope_type`, `scope_string_id`, `plan_string_id`, `plan_temporality_string_id`; titre et libellés `bpr_title`, `effect_label`, `benefit_resume`; mécanique et valeur `promotion_mechanic_string_id`, `value_int`, `currency`, `x_qty`, `y_qty`, `benefit_target`; contexte `on_izilife_object`, `application_context`, `include_brunch`; livraison/code `delivery_mode`, `external_promotion_code`; contraintes `available_for`, `usable_days`, `access_hours`, `access_schedule`, `blackout_hours`, `last_use_time`, `opening_hours_required`, `allow_if_opening_hours_unknown`; `valid_from`, `valid_to`, `priority`, `is_active`, `status`, `last_result`.

```powershell
& $py "$root\offers\izilife_subscription_benefit.py" --zone=lille --env=prod --max=1 --dry-run
```

### `brunch/brunch.py` — créneaux et formule de brunch d’un Place/Shop

Classeur `brunch\lille-zone\brunches.xlsx`, onglet `Brunchs`. Identifie l’objet par `scope_type`, `scope_string_id`; formule par `configuration_name`, `configuration_description`; service par `days`, `start_time`, `end_time`, `interval_minutes`; capacité/réservation par `min_booking_notice_minutes`, `max_people_per_slot`, `max_people_per_hour`, `have_multi_services`, `have_slots_in_services`; offre par `service_type`, `price`, `child_price`, `price_type`, `currency_code`, `included_items`, `description`, `reservation_required`, `is_active`; suivi `status`, `last_result`.

```powershell
& $py "$root\brunch\brunch.py" --zone=lille --env=prod --max=1 --dry-run
```

### `equipments/equipment.py` — équipement louable/rattaché à un scope

Classeur `equipments\lille-zone\equipments.xlsx`, onglet `Equipments`. Colonnes : `scope_type`, `scope_ref`, `name`, `category_ref`, `internal_id`, `description`, `capacity`, `instance_count`, `instance_capacity`, `instances_json`, `characteristics_json`, `localization_text`, `address`, `city_ref`, `longitude`, `latitude`, `exterior`, `is_privatisable`, `is_active`, `status`, `notes`, `last_result`. Les deux champs JSON doivent être des objets/listes JSON valides; les clés de caractéristiques sont des string_id autorisés de la catégorie.

```powershell
& $py "$root\equipments\equipment.py" --zone=lille --env=prod --max=1 --dry-run
```

### `escapades/escapade_proposal.py` — proposition éditoriale d’escapade

Classeur `escapades\lille-zone\escapade_proposals.xlsx`, onglet `EscapadeProposals`. `scope_type`, `scope_ref`, `proposal_types`, `editorial_title`, `editorial_description`, `profiles`, `weather`, `reason_refs`, `start_month`, `end_month`, `priority`, `is_active`, `status`, `notes`, `last_result`. Listes de types/profils/météo/raisons attendent des références prévues par le BO; les mois sont 1–12.

```powershell
& $py "$root\escapades\escapade_proposal.py" --zone=lille --env=prod --max=1 --dry-run
```

### `tags/tags.py` — ajouter/retirer un tag existant

Classeur `tags\lille-zone\tags.xlsx`, onglet `Tags`. `scope_type`, `scope_ref`, `tag_ref`, `operation` (`ADD` par défaut ou `REMOVE`), `status`, `notes`, `last_result`. Le tag doit déjà exister dans le référentiel BO.

```powershell
& $py "$root\tags\tags.py" --zone=lille --env=prod --max=1 --dry-run
```

### `links/link.py` — liens attachés à un objet

Classeur `links\lille-zone\links.xlsx`, onglet `Links`. `scope_type`, `scope_ref`, `url`, `title`, `source_type` (déduit du domaine si vide), `start_date`, `end_date`, `highlighted`, `is_official_website`, `order`, `status`, `notes`, `last_result`.

```powershell
& $py "$root\links\link.py" --zone=lille --env=prod --max=1 --dry-run
```

## 7. Géographie

### `geography/classificateur_territoires.py`

Classeur `territories.xlsx`, deux onglets `Cities` et `AdministrativeDivisions`. Ce n’est pas l’agent de quartiers ou de rues : il classe les territoires existants. Colonnes communes : `country`, `scope_ref`, `name`, `source`, `confidence`, `manual_validation`, `status`, `notes`, `last_result`; villes ont aussi `importance_score`, `ai_proposed_description`, indicateurs capitale/ville principale/frontière/montagne/littoral/surtourisme; divisions ont `ai_proposed_description`, `is_mountain_division`, `is_litoral_division`.

```powershell
& $py "$root\geography\classificateur_territoires.py" --zone=lille --env=prod --max=1 --dry-run
```

### `geography/city_subdivisions.py` — quartiers/subdivisions d’une ville

Classeur `city_subdivisions.xlsx`, une ligne par subdivision et ville. Colonnes `name`, `subdivision_ref`, `city_ref`, `division_type_ref`, `parent_ref`, `internal_code`, `zip_code`, `other_zip_codes`, `longitude`, `latitude`, `osm_refs`, `geometry_geojson`, `is_verified`, `is_active`, `status`, `notes`, `last_result`. La géométrie OSM est facultative : renseigner `geometry_geojson`/`osm_refs` seulement si disponible; l’objet quartier et sa géométrie sont distincts des vraies rues.

```powershell
& $py "$root\geography\city_subdivisions.py" --zone=lille --env=prod --max=1 --dry-run
```

### `geography/streets.py` — objets Place représentant des rues connues

Classeur `streets.xlsx`. Colonnes `name`, `street_ref`, `city_ref`, `place_type_ref`, `address`, `zip_code`, `longitude`, `latitude`, `osm_refs`, `geometry_geojson`, `description`, `members`, `place_of_life`, `is_active`, `status`, `notes`, `last_result`. Ce n’est pas la table des vraies rues; l’agent crée/alimente des objets iziLife représentant une rue ou un lieu de vie lié à une rue. Géométrie et OSM sont optionnels selon les données disponibles.

```powershell
& $py "$root\geography\streets.py" --zone=lille --env=prod --max=1 --dry-run
```

## 8. Inventaire complémentaire — scripts qui ne sont pas des classeurs CRUD

- `events/link_scraper.py` : ingestion d’une URL d’événement fournie par `--url`, avec `--city`, `--env`, option `--dry-run`. Utile pour un lien ponctuel, mais la curation manuelle est le classeur `ingest_manual_curate.py`.
- `events/shotgun_scraper.py`, `facebook_scraper.py`, `billetweb_scraper.py`, `eventbrite_scraper.py`, `helloasso_scraper.py`, `meetup_scraper.py` : collecte par source; préférer les commandes bornées de la section événements. Meetup est non prioritaire; Facebook est manuel selon ta procédure.
- `events/send_sources.py` : ancien flux remplacé par Playwright; ne pas planifier.
- `instagram/saved_collections.py` : outil à retirer plus tard selon ta consigne; ne pas inclure dans la reprise prod.
- `geography/osm_geometry.py` : utilitaire géométrie OSM; pas un flux de curation général à lancer sans besoin précis.
- `test_api.py`, `tests/*`, `agent_excel_logger.py`, `objects/object_agent_common.py`, `offers/offer_agent_common.py` : tests/bibliothèques de support, pas des agents métier à lancer comme campagnes.

## 9. À propos du cron

Tu veux piloter manuellement et te réapproprier les classeurs : ces commandes sont faites pour un lancement à la demande. Ne lance pas un cron général pendant cette phase de reprise. Une tâche planifiée reprendrait des lignes `pending` sans que tu sois devant le fichier; elle ne remplace pas une revue de contenu ni le contrôle du BO.

# Agent horaires Google Maps

Script :
`C:\Users\alcamara\Documents\agentic_Workspace\scripts\izilife\places\google_hours_agent.py`

Le script inventorie uniquement les Place/Shop actifs et listables qui possèdent un
`google_place_id` mais aucun enregistrement `Hourly`. Il consulte Google Maps avec
Playwright, transforme les sept jours vers le format iziLife (`lundi=1` à
`dimanche=7`) et produit toujours un rapport JSON.

Analyse/collecte externe sans écriture :

```powershell
python google_hours_agent.py --env=staging --headless --max=100
```

Écriture staging :

```powershell
python google_hours_agent.py --env=staging --headless --max=100 --apply
```

Production (confirmation renforcée) :

```powershell
python google_hours_agent.py --env=prod --headless --max=100 --apply `
  --confirm-production I_CONFIRM_PRODUCTION_HOURS
```

Un lancement sans `--apply` reste un dry-run d'écriture, mais effectue réellement
des navigations Google Maps. Une fermeture n'est appliquée que si Google affiche
explicitement « Fermé temporairement » ou « Fermé définitivement ». Une absence
d'horaires ne ferme jamais une fiche.

