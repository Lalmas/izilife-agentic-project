# API interne iziLife V0

La V0 du BO donne la priorité à **l'univers iziLife**. Elle permet à un outil iziLife local de lire les données curatées en staging ou en production. La consultation ne crée rien ; une route distincte de résolution peut importer un lieu manquant via Google Places. Les identifiants numériques renvoyés par les graphes de curation sont propres à la source et ne doivent jamais être réutilisés comme clés étrangères dans une autre base.

## Accès

La V0 utilise le secret agent existant `AGENT_SECRET_TOKEN`, défini hors dépôt dans l'environnement qui **sert** l'API, via l'en-tête `X-Agent-Token` en HTTPS. **La même clé autorise déjà des routes d'écriture** : réserver son accès aux outils iziLife de confiance. Le projet de jeton séparé `IZILIFE_INTERNAL_DATA_TOKEN` est mis de côté pour la V0. Il faudra créer ensuite un système sécurisé de génération et gestion des clés par **zone d'appel** (ex. lecture des lieux, lecture des événements, import Google), par outil et éventuellement par salarié, avec permissions, expiration, révocation et audit avant toute ouverture externe.

L'outil local doit conserver le jeton production dans son gestionnaire de secrets local, jamais dans un classeur ni dans Git. Le serveur de production conserve seul les clés Google. Les secrets staging et production doivent rester distincts.

## Routes

`POST /scraper/agentInternalDataV0Lookup` avec JSON :

```json
{"items":[{"type":"SHOP","string_id":"cryotera-pole-de-cryotherapie-lille"}],"include_graph":true}
```

La lecture peut être composée : `view=essential` renvoie l'identité, l'adresse,
la localisation, la catégorie principale et l'état ; `view=full` renvoie les
champs métier de la fiche et toutes les sections de curation. Pour cibler les
objets utiles, envoyer par exemple
`{"view":"essential","include":["services","eap","media","external_media"]}`.
Les sections disponibles sont `media`, `external_media`, `links`, `ambiences`,
`characteristics`, `other_categories`, `products`, `equipment`,
`equipment_media`, `services`, `eap` et `hours`.

`media` et `external_media` sont paginés en `{items,total,page,page_size}`.
`media_page` commence à 1 et `media_page_size` est plafonné à 10. La vue
complète exclut les champs de mot de passe, jeton et administration. L'ancien
`include_graph=true` garde son format pour les clients existants ; il n'est pas
paginé. Les IDs numériques restent propres à l'environnement source.

Types acceptés : `PLACE`, `SHOP`, `EVENT`, `EXPERIENCE`, `LOCAL_HABIT`. Maximum 100 références. Pour `PLACE` et `SHOP`, chaque entrée peut utiliser `google_place_id` à la place de `string_id`. La réponse indique `found`, `missing` ou `invalid`; pour Place et Shop, `include_graph` reprend l'export de curation existant (médias, liens, produits, horaires et autres relations déjà exportées). Pour les autres types, la V0 ne renvoie encore que les champs d'identité et d'état explicitement listés dans le contrôleur.

`POST /scraper/agentInternalDataV0FutureEvents` avec JSON :

```json
{"city_string_id":"lille","radius_km":10,"limit":50}
```

`radius_km=0` sélectionne la ville exacte. Un rayon de 0 à 100 km utilise les coordonnées de la ville et des événements. La réponse est limitée à 100 événements actifs, listables, dont la date de fin n'est pas passée, triés par date de début. Cette V0 ne reconstruit pas encore les relations complètes de chaque événement.

`POST /scraper/agentInternalDataV0ResolvePlace` avec JSON :

```json
{"city":"lille","name":"Cryotera","google_place_id":"identifiant-google-si-connu"}
```

Les entrées acceptées sont `unique_id`, `google_place_id`, `string_id`, `name` ou `query` ; `city` est le `string_id` de la ville et aide à départager. La route vérifie d'abord Place et Shop dans iziLife. Si plusieurs correspondances exactes ou partielles existent, elle renvoie `refine_search` et les candidats pour préciser la recherche, **sans appeler Google**. Elle contrôle aussi les noms partiels hors de la ville demandée avant de conclure à une absence. Si aucun candidat iziLife n'est trouvé, `name/query` et `city` sont requis : sans Google Place ID, une recherche Google renvoie seulement des candidats à choisir. Un second appel avec le Google Place ID retenu peut utiliser l'importeur BO existant. Une fiche non classable peut rester en `pending_review` plutôt que devenir une Place/Shop. Cette route peut consommer Google Places et **écrire dans l'environnement appelé** lors du second appel. Elle n'a pas été lancée en production dans ce chantier.

## Suite avant import automatique

1. Exposer des graphes contrôlés pour Event, Experience et LocalHabit ainsi que leur média, leurs dépendances et leurs références stables.
2. Ajouter un client local qui compare les graphes, résout les références dans la base cible et produit un plan `dry-run` avant tout import.
3. Renforcer la résolution Google avec verrou de concurrence/idempotence transactionnelle et journal des appels payants ; le parcours existant vérifie déjà les doublons avant import, mais les appels concurrents ne sont pas encore verrouillés dans cette V0.
4. Créer les clés par zone d'appel, salarié et outil, avec scopes lecture/import, expiration, révocation et audit, avant diffusion externe.

La base d'une autre cible n'est jamais interrogée directement par cette API. L'outil appelant choisit explicitement l'URL staging ou production et son jeton correspondant.
