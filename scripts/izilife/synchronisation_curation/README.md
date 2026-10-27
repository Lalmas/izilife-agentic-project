# Synchronisation intelligente de la curation iziLife

## Objectif

Réutiliser en staging puis en production les contenus réels déjà curatés en local ou staging, sans rappeler Google Places, Google Business ou un LLM pour reconstruire ce qui existe déjà.

Ce chantier est une synchronisation métier sélective. Ce n'est ni une réplication de base, ni un import SQL brut.

## Règles non négociables

1. La production reste prioritaire : une valeur déjà présente et valide n'est pas remplacée automatiquement.
2. Aucun identifiant numérique source n'est réutilisé comme identifiant destination.
3. Toute relation est reconstruite après résolution de la cible et des référentiels dans l'environnement destination.
4. Un établissement exclu, fermé, refusé, désactivé ou dépublié n'est jamais recréé ou réactivé automatiquement.
5. Les médias sont copiés, jamais déplacés. Un objet de stockage existant en production n'est jamais écrasé.
6. Aucun User, OTP, credential, paiement, réservation, achat, Grant ou historique transactionnel n'est exporté.
7. Les promotions et offres temporaires sont exclues : BPR, Happy Hour, C&T, Last Minute et négociations commerciales.
8. Une configuration EAP importée reste inactive ou en attente de validation commerciale tant que prix, devise, périmètre et relations n'ont pas été approuvés.
9. Les horaires sont importés uniquement lorsqu'ils existent dans la source. Aucun horaire n'est inventé.
10. Toute exécution commence par un plan en lecture seule. L'écriture nécessite une validation explicite du plan.

## Modes combinables

- `MEDIA_ONLY` : inventorie et importe uniquement les médias absents et leurs associations.
- `ENRICH_MISSING` : complète uniquement les champs simples et associations absents.
- `IMPORT_RELATED` : importe les objets métiers liés avec leurs dépendances.
- `CREATE_COMPLETE` : crée une Place ou un Shop absent, puis applique les autres modes autorisés.

Les modes sont sélectionnés par établissement. `CREATE_COMPLETE` n'est jamais implicite.

## Identité des établissements

Ordre de résolution proposé pour une Place ou un Shop :

1. `google_place_id` identique et unique, même si le type diffère entre environnements ;
2. type propre à l'environnement (`LOCAL_TYPE`, `STAGING_TYPE`, `PROD_TYPE`) et `place_string_id`/`shop_string_id` identique ;
3. alias validé dans le manifeste de synchronisation ;
4. rapprochement indicatif par nom normalisé, ville, adresse et coordonnées.

Le quatrième cas ne permet jamais une écriture automatique. Il produit un cas `AMBIGUOUS` à valider.

`unique_id` et les IDs numériques ne sont pas considérés comme portables entre environnements.

## Résolution des dépendances

Les référentiels globaux sont résolus par leur clé métier :

- `PlaceType.place_type_string_id` ;
- `ShopCategory.name_id` ;
- `Atmosphere.string_id` ;
- `ShopAndPlaceCharactTag.string_id` ;
- `EquipmentCategory.string_id` ;
- `ElementServiceType.string_id` ;
- `ExternalMediaSource.string_id` ;
- les autres référentiels par leur `string_id` vérifié dans le schéma courant.

Les objets appartenant à un établissement sont résolus par une clé naturelle reconstruite. Exemples :

- Link : cible destination + URL canonique ;
- média : cible destination + empreinte du fichier, puis chemin de stockage ;
- ProductCategory : cible destination + chemin hiérarchique de noms ;
- Product : cible destination + `unique_id` portable lorsqu'il est réellement stable, sinon SKU/référence externe, sinon nom + catégorie ;
- ProductOptionGroup : produit/catégorie destination + nom + règle de sélection ;
- Equipment : cible destination + catégorie + `unique_id`/`internal_id`/nom selon disponibilité ;
- EAP : cible destination + type + nom + prix + devise + périmètre ; toute collision incertaine est bloquée ;
- ElementService : cible destination + type + catégorie + nom.

Chaque résolveur doit retourner `MATCHED`, `MISSING` ou `AMBIGUOUS`, avec la preuve utilisée.

## Médias et stockage

Les clés S3 sont composées d'un préfixe métier et de `Media.integration_path`, par exemple :

- `statics/shops/<integration_path>` ;
- `statics/places/<integration_path>` ;
- `statics/products/<integration_path>` ;
- `statics/equipments/<integration_path>`.

Certains anciens noms contiennent l'ID source (`sh_m_101_...`). Ce nombre n'est pas une foreign key : le nom peut être conservé, mais il ne doit jamais servir à résoudre la cible.

Procédure sûre :

1. lire les métadonnées source du média et le fichier source ;
2. calculer SHA-256 côté outil, même lorsque `Media.sha1_hash` est vide ;
3. rechercher en destination une association portant la même empreinte ;
4. vérifier l'existence de la clé dans le bucket destination ;
5. si la clé existe avec un contenu différent, bloquer avec `MEDIA_KEY_COLLISION` ;
6. sinon copier le flux dans le bucket destination sans supprimer la source ;
7. créer `Media` avec un nouvel ID destination ;
8. recréer le pivot (`PlaceMedias`, `ShopMedias`, `ProductMedias`, etc.) et les contextes/tags applicables ;
9. vérifier par lecture HTTP que le média est affichable.

Le transfert recommandé passe par un flux temporaire ou une URL source présignée et un endpoint d'import destination. La production ne doit pas connaître les credentials des buckets local ou staging.

## Architecture de l'outil ponctuel

L'outil peut rester un CLI ponctuel dans ce dossier. Il n'a pas besoin d'être un agent planifié.

### Backend `izilife-admin`

Deux capacités étroites sont nécessaires :

- export en lecture seule d'un graphe de curation par référence stable ;
- application idempotente d'une opération validée, avec résolution des IDs dans la destination.

L'export doit renvoyer des références métier et jamais demander au CLI d'interpréter des IDs source comme des IDs destination.

L'application doit accepter un `plan_id`, un hash du plan et une clé d'idempotence. Un plan modifié après validation est refusé.

### Classeur unique de pilotage

L'unité de travail n'est pas une ligne provenant d'un environnement : c'est une cible métier logique. Une même ligne peut donc déclarer des références différentes selon l'environnement :

```text
scope_key=soultrain
scope_type=SHOP
local_type=SHOP
staging_type=SHOP
local_ref=soultraincafe
staging_ref=soultrain-cafe
prod_ref=
```

`scope_key` est seulement la clé du dossier de synchronisation. Elle n'est jamais écrite en base.

Le classeur comporte les feuilles suivantes :

- `CIBLES` : références local/staging/prod et règles choisies par établissement ;
- `ETAT_DES_LIEUX` : existence et compteurs relus dans chaque environnement ;
- `PLAN` : opérations différentielles proposées ;
- `AMBIGUITES` : correspondances qui nécessitent une décision humaine ;
- `JOURNAL` : résultats des simulations et applications validées.

Colonnes de pilotage prévues dans `CIBLES` :

- `scope_key`, `scope_type`, `local_ref`, `staging_ref`, `prod_ref` ;
- `local_type`, `staging_type`, `prod_type`, car une même cible métier peut être une `PLACE` dans un environnement et un `SHOP` dans un autre ;
- `source_preference` : vide/`AUTO`, `LOCAL` ou `STAGING` ;
- `allow_create_prod` : `NON` par défaut ;
- `media`, `external_media`, `links`, `ambiences`, `characteristics`, `products`, `product_options`, `equipment`, `services`, `eap`, `hours` ;
- `notes`, `enabled`.

Pour chaque famille de contenu :

- cellule vide ou `AUTO` : le comparateur choisit les éléments manquants les plus fiables parmi local et staging ;
- `INCLUDE` : la famille est explicitement autorisée, toujours sans écraser une valeur production valide ;
- `EXCLUDE` : la famille est ignorée pour cet établissement ;
- `LOCAL` ou `STAGING` : seule cette source est utilisée pour cette famille.

Laisser une cellule vide signifie donc bien « laisse le script comparer ». Une exclusion explicite reste prioritaire sur le mode global.

`prod_ref` peut être renseigné manuellement lorsqu'il est connu. S'il est vide, l'auditeur cherche la fiche production à partir des identités local et staging, puis inscrit le candidat dans `ETAT_DES_LIEUX`. Il ne modifie jamais automatiquement `CIBLES`.

### CLI d'orchestration

Le CLI lit le classeur unique, compare simultanément local et staging à la destination, produit les feuilles de rapport et s'arrête par défaut.

Commandes prévues :

```text
audit     inventaire les sources, la destination et les correspondances
plan      génère les opérations proposées sans écrire
apply     applique un plan explicitement validé
verify    relit le backend, le BO et les URLs média après application
```

`apply --env=prod` devra exiger à la fois le fichier de plan validé, son hash et une confirmation explicite. Aucune commande par défaut ne doit cibler la production.

### Déroulement opérationnel par environnement

Le même classeur est enrichi progressivement. Une ligne représente toujours le même établissement métier, même lorsque ses `string_id` diffèrent entre environnements.

**Étape 1 — local, disponible maintenant**

```powershell
python curation_sync.py prepare-env --workbook .\pilotage_sync_curation.xlsx --env local
python curation_sync.py audit --workbook .\pilotage_sync_curation.xlsx --envs local
```

`prepare-env` demande au backend toutes les Place et tous les Shop ayant un `google_place_id`, fusionne les résultats par `google_place_id` unique, renseigne `LOCAL_REF`, `LOCAL_NAME` et `LOCAL_TYPE`, puis ajoute les fiches locales absentes du classeur. Il ne modifie pas la base.

**Étape 2 — staging, après livraison des deux routes en staging**

```powershell
python curation_sync.py prepare-env --workbook .\pilotage_sync_curation.xlsx --env staging
python curation_sync.py audit --workbook .\pilotage_sync_curation.xlsx --envs local staging
```

La préparation staging complète `STAGING_REF`, `STAGING_NAME` et `STAGING_TYPE` sur les lignes déjà connues grâce au même `google_place_id`. Elle ajoute aussi les fiches réelles présentes en staging mais absentes du local. L'audit compare ensuite les graphes disponibles dans les deux sources. Un changement de type entre environnements est conservé sur la même ligne et n'est pas traité comme un doublon.

**Étape 3 — production en lecture seule, après livraison des routes**

```powershell
python curation_sync.py prepare-env --workbook .\pilotage_sync_curation.xlsx --env prod
python curation_sync.py audit --workbook .\pilotage_sync_curation.xlsx --envs local staging prod
```

Par défaut, la préparation production ne crée pas de ligne pour une fiche présente uniquement en production : elle recherche seulement les cibles déjà préparées et remplit `PROD_REF` et `PROD_NAME`. Les rapprochements absents ou douteux restent à confirmer manuellement. L'option `--include-unmatched-prod` existe pour un inventaire exceptionnel des fiches uniquement production, mais ne doit pas être utilisée pour le parcours normal.

**Étape 4 — plan puis import validé**

Le plan est calculé par le backend destination et ne réalise aucune écriture :

```powershell
python curation_sync.py plan --workbook .\pilotage_sync_curation.xlsx --env staging --output .\plan-staging.json
```

Une création de fiche absente reste explicite : ajouter `--allow-create`. En production, la ligne doit en plus porter `ALLOW_CREATE_PROD=OUI`.

Après relecture du JSON :

```powershell
python curation_sync.py apply --plan .\plan-staging.json --confirm CURATION_SYNC_APPLY
python curation_sync.py verify --plan .\plan-staging.json
```

La production possède un second verrou obligatoire :

```powershell
python curation_sync.py apply --plan .\plan-prod.json --confirm CURATION_SYNC_APPLY --confirm-production I_CONFIRM_PRODUCTION_IMPORT
```

Ne jamais lancer cette dernière commande sans validation manuelle du plan. Avant le premier `apply` de chaque environnement, exécuter manuellement `izilife-db/sql/curation_sync_journal.sql`.

Les routes nécessaires aux étapes 1 à 3 sont strictement en lecture seule :

- `agentCurationSyncListScopes` : inventaire paginé des Place/Shop qui possèdent un `google_place_id` ;
- `agentCurationSyncInspect` : lecture du graphe de curation d'une Place/Shop identifiée par son type et son `string_id`.

## Ordre d'import d'un graphe

1. résoudre ou créer la Place/Shop ;
2. résoudre les référentiels globaux ;
3. compléter les champs scalaires autorisés et les associations simples ;
4. importer les catégories de produits ;
5. importer les produits ;
6. importer groupes, valeurs et affectations d'options ;
7. importer équipements et leurs catégories/caractéristiques ;
8. importer services et dépendances ;
9. importer les EAP désactivés ou à valider et reconstruire leurs périmètres ;
10. importer les médias des objets déjà résolus ;
11. importer liens et médias externes ;
12. importer les horaires présents ;
13. vérifier les comptes et le rendu BO/FO.

Une transaction est utilisée par sous-graphe cohérent, pas pour le transfert complet de plusieurs établissements.

## Dry-run attendu

Chaque ligne du rapport contient au minimum :

- environnement et objet source ;
- type et référence stable de destination ;
- mode demandé ;
- action proposée : `CREATE`, `ENRICH`, `LINK`, `COPY_MEDIA`, `SKIP`, `BLOCK` ;
- clé naturelle utilisée ;
- valeur source et valeur destination résumées ;
- raison de la décision ;
- niveau de confiance ;
- dépendances ;
- clé d'idempotence ;
- exclusion éventuelle.

Le résumé présente : objets créés, objets enrichis, médias à copier, associations à reconstruire, doublons évités, exclusions et ambiguïtés.

## Audit initial du code — 26 octobre 2026

Constats vérifiés :

- le backend possède déjà le SDK AWS S3 et `Upload_lib` sait écrire dans le bucket de l'environnement courant ;
- les préfixes de stockage sont centralisés dans `app/Config/Constants.php` ;
- les routes agents savent déjà ajouter des médias, liens et médias externes ;
- `agentAddScopedMedia` déduplique par empreinte SHA-1 dans le scope destination, mais renomme le fichier lors de l'upload ;
- aucune route actuelle n'exporte le graphe métier complet d'une Place/Shop ;
- aucune route actuelle ne réalise une copie inter-buckets en conservant et vérifiant la clé ;
- `agentGetPlaceByStringId` ne renvoie que la fiche de base et le cache Google ;
- le schéma possède des identifiants métier sur une partie importante des référentiels ;
- plusieurs objets enfants ont des `unique_id`, mais leur portabilité entre environnements doit être vérifiée avant utilisation ;
- les anciens médias pilotes ont souvent `Media.sha1_hash` vide : l'outil devra recalculer une empreinte réelle ;
- la résolution actuelle d'`EVENT_SERIE` dans `_agentResolveTarget` vise `event_serie_string_id`, alors que le schéma local expose `EventSerie.string_id` : ce point devra être corrigé avant d'inclure EventSerie.

## Pilotes identifiés en local

| Type | Référence locale vérifiée | Médias | Links | Médias externes | Ambiances | Produits | Catégories produit | Groupes options | Équipements | EAP | Services | Horaires |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SHOP | `soultraincafe` | 10 | 0 | 2 | 0 | 75 | 13 | 2 | 2 | 0 | 0 | 3 |
| SHOP | `disco-volante-lille` | 1 | 3 | 1 | 3 | 24 | 10 | 1 | 2 | 0 | 0 | 2 |
| SHOP | `don-vito` | 1 | 0 | 0 | 0 | 60 | 4 | 0 | 0 | 0 | 0 | 1 |
| PLACE | `hun` | 0 | 0 | 0 | 0 | 6 | 4 | 0 | 14 | 5 | 1 | 0 |
| PLACE | `follow-park-lille` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 14 | 0 | 1 |

`Les Essentielles` est un salon de coiffure. La référence fournie pour la recherche inter-environnements est `l-essenti-elles-coiffure-et-beaute`.

## Avancement au 26 octobre 2026

1. Le classeur unique existe et contient les identités séparées local/staging/production.
2. Les deux routes de lecture et le CLI `prepare-env`/`audit` existent localement, sans route d'écriture.
3. L'inventaire local contient 285 Place/Shop ayant un `google_place_id` ; aucune collision locale de `google_place_id` n'a été détectée.
4. Les cinq pilotes locaux identifiés sont audités. `Les Essentielles` doit être recherchée avec `l-essenti-elles-coiffure-et-beaute` et ses variantes de nom.
5. La livraison staging permettra l'étape 2 sans recommencer le travail local.
6. Le plan différentiel, l'import idempotent et le transfert média authentifié sont implémentés localement ; ils doivent être livrés et testés en staging avant toute utilisation en production.
7. Experience et EventSerie seront traités ensuite, avec leurs propres dépendances et après correction du résolveur EventSerie.

## État d'implémentation

Le premier lot en lecture seule est disponible localement :

- `pilotage_sync_curation.xlsx` contient les cibles, l'état des lieux, le futur plan, les ambiguïtés et le journal ;
- `curation_sync.py audit` lit les cibles et remplit l'état des lieux ;
- `POST /scraper/agentCurationSyncInspect` exporte le graphe éditorial d'une Place ou d'un Shop sans écriture ;
- cinq pilotes locaux sont résolus ; la recherche de `Les Essentielles` dispose maintenant de la référence `l-essenti-elles-coiffure-et-beaute`.

Exécution locale vérifiée :

```powershell
python .\synchronisation_curation\curation_sync.py audit `
  --workbook .\synchronisation_curation\pilotage_sync_curation.xlsx `
  --envs local
```

Les audits staging et production nécessitent d'abord la livraison des routes dans ces environnements. `audit` et `plan` ne déclenchent aucun import.

## Fichiers à livrer

Dans `izilife-admin` :

- `app/Controllers/CurationSync.php` ;
- `app/Models/Agents/CurationSyncExport_model.php` ;
- `app/Models/Agents/CurationSyncImport_model.php` ;
- `app/Models/Agents/AgentScopedMedia_model.php` ;
- `app/Libraries/Upload_lib.php` ;
- les routes `agentCurationSyncInspect`, `agentCurationSyncListScopes`, `agentCurationSyncPlan`, `agentCurationSyncApply` et `agentCurationSyncMediaDownload` ;
- l'évolution de `agentAddScopedMedia` pour les médias Product/Equipment.

Dans `izilife-db` : `sql/curation_sync_journal.sql`, à exécuter manuellement.

## Copier les médias d'une ancienne fiche vers une nouvelle

Le plan est toujours sans écriture. Il compare les empreintes SHA-1 et marque les
fichiers déjà présents comme `SKIP_DUPLICATE` :

```powershell
python .\curation_sync.py media-move-plan `
  --source-env local --source-type PLACE --source-ref embranchement-de-seclin `
  --destination-env local --destination-type PLACE --destination-ref canal-de-seclin `
  --output .\plan-medias-embranchement-canal.json
```

Ajouter `--close-source` au plan permet de fermer définitivement l'ancienne fiche,
mais seulement lorsque source et destination sont dans le même environnement et
uniquement après vérification de toutes les copies. L'application exige un plan figé :

```powershell
python .\curation_sync.py media-move-apply `
  --plan .\plan-medias-embranchement-canal.json `
  --confirm MEDIA_MOVE_APPLY
```

Si la source ou la destination est en production, ajouter explicitement
`--confirm-production I_CONFIRM_PRODUCTION_MEDIA_MOVE`. Les originaux ne sont jamais
déplacés ni supprimés du bucket source.

## Propositions, territoires et campagne publique

`curation_extras_sync.py` fusionne local et staging par références stables et exclut
automatiquement les EscapadeProposal/ActivityProposal contenant le mot isolé
`test`. Le plan est sans écriture :

```powershell
python .\curation_extras_sync.py plan --sources local staging --destination prod `
  --campaign musees-gratuits-premier-dimanche --output .\plan-extras-prod.json
```

L'application production exige :

```powershell
python .\curation_extras_sync.py apply --plan .\plan-extras-prod.json `
  --confirm CURATION_EXTRAS_APPLY `
  --confirm-production I_CONFIRM_PRODUCTION_EXTRAS
```

Une campagne dont le scope source ne possède pas de référence stable est bloquée :
aucun identifiant numérique local/staging n'est réutilisé en production.

Dans l'espace agents : ce dossier et son classeur de pilotage.

L'import couvre les champs éditoriaux manquants, catégories secondaires, ambiances, caractéristiques, liens, médias externes, produits, catégories et options, équipements, services, EAP et horaires. Les médias Place/Shop/Product/Equipment transitent en flux authentifié, sont recalculés en SHA-1 et dédupliqués dans leur objet destination. Les promotions, utilisateurs et transactions ne figurent dans aucun export.

## Nettoyage préalable de production — 26 octobre 2026

Ce nettoyage a été exécuté manuellement et contrôlé dans la base de production avant la synchronisation de curation.

- les fiches explicitement listées comme obsolètes ont été rendues inactives et non listables, sans suppression ;
- les six enregistrements Grand Scène historiques sont non listables, dont les trois fiches actives fermées ;
- `jost-food-court` est la fiche JOST conservée ; elle possède maintenant les catégories secondaires `hotel` et `bar`, 3 médias et 10 hobbies ; `jost-hotel` et `jost-lille` sont inactives et non listables ;
- `acropolis-bowling-seclin` est la seule fiche Acropolis conservée ; elle reste active/listable, possède 18 médias, les catégories secondaires `bar`, `salle-d-arcade`, `salle-de-billard` et 6 hobbies pertinents ; `laser-game` et `parc-de-loisirs` ont été explicitement exclus ;
- `hall-u-need` (SHOP 1263) est la fiche Hall U Need conservée ; elle possède 32 médias, 10 hobbies, 2 catégories secondaires et 4 caractéristiques éditoriales ; ses `PrincipalCharacteristics` ont été fusionnées de façon additive ; l'ancienne PLACE `hun` est inactive et non listable ;
- aucune ligne n'a été supprimée et aucun fichier média n'a été déplacé.

Le fichier de retour arrière des statuts se trouve dans `rollback_prod_cleanup_2026-10-26.sql`. Les relations ajoutées pendant les consolidations doivent être auditées avant un éventuel retrait : ne pas lancer de suppression globale.

