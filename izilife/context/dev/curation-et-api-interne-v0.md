# Curation réutilisable et API interne iziLife V0

État du code au 29 octobre 2026. Vérifier les dépôts avant toute commande : ce document décrit les décisions et chemins, pas la preuve d'une livraison sur un environnement.

## Règle directrice

L'univers iziLife est consulté **avant** Google ou une IA. Une donnée réelle déjà curatée doit être réutilisée entre local, staging et production sans refaire une collecte payante. Une fiche existante en production reste prioritaire ; on complète seulement les données manquantes. On ne réutilise jamais les IDs numériques d'un autre environnement comme clés étrangères.

Pour rapprocher des Place/Shop entre environnements : Google Place ID unique, références stables propres à chaque environnement, puis nom + ville + adresse/coordonnées à confirmer en cas de doute. Le type Place/Shop peut varier entre environnements. `unique_id` sert à retrouver un objet **dans sa propre base** ; il n'est pas considéré portable entre bases. Une fiche exclue, fermée ou dépubliée ne doit pas être recréée ou réactivée par synchronisation.

Les médias sont copiés entre buckets et leurs associations recréées avec les IDs de destination ; les originaux ne sont pas déplacés. Les doublons, droits et chemins doivent être contrôlés. Les produits, options, horaires, caractéristiques, équipements, Services et EAP demandent la résolution de leurs dépendances. On n'invente pas d'horaires. On exclut les données personnelles, tests, transactions, promotions temporaires et négociations commerciales. Un EAP récupéré ne devient pas une vente active sans validation métier.

Voir `scripts/izilife/synchronisation_curation/README.md` pour les modes `MEDIA_ONLY`, `ENRICH_MISSING`, `IMPORT_RELATED`, `CREATE_COMPLETE`, le plan et le journal. La séquence de travail est : inventorier local, rapprocher staging, rapprocher production, puis simuler et vérifier avant import. Les transferts de production restent des lancements manuels distincts.

## Outils de curation récents

- `scripts/izilife/tags/tags_and_characts.py` : saisie manuelle de tags, caractéristiques principales 0/1, familles éditoriales et hobbies par `string_id`. Les cellules vides ne changent rien. Les onglets de référence sont propres à chaque environnement et se rafraîchissent explicitement. Voir `tags/README_tags_and_characts.md`.
- `scripts/izilife/places/site_content_package.py` : transforme une analyse de site complexe en paquet `izilife.site_content.v1`. `pending`/`needs_review` ne sont pas importés ; seul `approved` peut partir. `--analyze-only` de l'améliorateur peut appeler Playwright et l'IA sans écriture iziLife ; `--dry-run` du paquet et `apply` sont des opérations différentes. Voir `places/README_site_content_package.md`.
- Cryotera Lille : brouillon de 7 Services et 22 EAP, tous en attente de revue ; chaque tarif est lié à son Service. Les tarifs conseillés doivent être confirmés pour le centre et les droits des images vérifiés. Aucune importation n'est attestée par ce document.

## Services, EAP et SQL

Un EAP propre à un Service porte directement `ElementAccessPrice.service_id`. `LocationEAPUseForService(eap_id, service_id)` est réservée à la diffusion d'un EAP supérieur vers plusieurs Services. Le prix reste dans `ElementAccessPrice.price`. Un prix différent correspond à un EAP local distinct, éventuellement variante d'un modèle avec `is_variant_of`. Le prix `ElementService.price` peut être `NULL` pour « sur devis » ; `0` signifie gratuit seulement si la source l'affirme.

Les blocs SQL de `LocationEAPUseForService`, du prix Service nullable et de migration de l'ancienne table `EapPrice` sont dans `izilife-db/principal/021_Next_Improves.sql`. La migration transforme une liaison unique en propriété directe `ElementAccessPrice.service_id`, conserve uniquement les vraies diffusions multiples dans `LocationEAPUseForService`, puis supprime l'ancienne table une fois le FO/BO compatible déployé. Aucun nouveau fichier SQL structurel séparé n'est créé sans accord. Dans les modèles PHP, respecter **exactement la casse** des noms de tables du schéma, notamment sur Linux : `LocationEAPUseForService`, `ElementService`, `LocalEvent`, `Place`, `Shop`.

## API interne V0 du BO

Code : `izilife-admin/app/Controllers/InternalDataV0.php`, méthode de résolution dans `app/Controllers/Scraper.php`, routes dans `app/Config/Routes.php`.

La V0 utilise **le même** `AGENT_SECRET_TOKEN` que les routes agents, via `X-Agent-Token` en HTTPS. Ne pas mettre le secret dans Git ni un classeur. Puisqu'il autorise déjà des écritures, limiter la V0 aux outils iziLife internes. Plus tard : génération sécurisée de clés par zone d'appel (lecture lieux, lecture agenda, résolution/import Google), par outil et salarié, avec droits, expiration, révocation et journal d'accès. Aucune clé individuelle n'existe encore.

- `POST scraper/agentInternalDataV0Lookup` : consultation sans Google, 1 à 100 références Place, Shop, LocalEvent (`EVENT`), Experience ou LocalHabit. Pour Place/Shop, `include_graph=true` reprend le graphe de curation existant ; les autres types ne donnent aujourd'hui qu'un résumé.
- `POST scraper/agentInternalDataV0FutureEvents` : événements actifs/listables futurs par `city_string_id`, rayon de 0 à 100 km et limite de 100. Rayon 0 = ville exacte.
- `POST scraper/agentInternalDataV0ResolvePlace` : cherche **d'abord dans iziLife** par Google Place ID, `unique_id`, `string_id` ou nom exact, avec ville pour départager. Des correspondances multiples ou partielles donnent `refine_search` et une liste à préciser, sans Google. Si aucun candidat iziLife n'est trouvé, nom et ville sont obligatoires. Une recherche Google par nom propose des résultats, sans import immédiat ; l'appel suivant avec le Google Place ID choisi peut passer par l'importeur BO. Cette route peut consommer Google Places et écrire dans **l'environnement appelé** ; un type non mappé peut rester en `pending_review`.

### Références des homonymes

À la création d'une `Place` ou d'un `Shop`, iziLife conserve le slug de base s'il est libre. Si ce slug existe déjà dans une autre ville, la référence créée est `<slug>-<City.string_id>`. Quand `in_on_place_ref` est fourni, les collisions restantes sont résolues avec la référence du contenant (`<slug>-v2`, `<slug>-<ville>-v2`, puis référence complète). La validation manuelle n'intervient qu'après épuisement de ces variantes. Les fiches existantes ne sont pas renommées automatiquement et la reconnaissance par `google_place_id` reste prioritaire.

La consultation et la résolution sont distinctes pour rendre visibles les coûts et l'écriture. L'outil client choisit l'URL et le secret de staging ou production ; la clé Google reste côté serveur. Aucun appel de la nouvelle route n'a été lancé en production dans ce travail.

### Incident enrichisseur Seclin du 28 octobre 2026

`places/enrichisseur.py` appelle `scraper/agentAnalyzeContent` avec OpenAI et le mode JSON. Le transport `OpenAI_lib` envoyait la consigne « JSON » dans `instructions` mais pas dans `input` de l'API Responses. OpenAI répondait HTTP 400 : `Response input messages must contain the word 'json'`. Le transport ajoute désormais la consigne JSON au message utilisateur quand `json_mode` est actif. Cette correction est dans `izilife-admin/app/Libraries/OpenAI_lib.php` et couverte par `tests/AIClientFacadeContractTest.php`. Elle nécessite une livraison BO dans l'environnement où tourne l'enrichisseur ; elle ne répare pas à elle seule les lignes Seclin échouées. Relancer manuellement seulement les lignes en erreur après vérification du classeur et du résultat BO.

### Coût des appels IA et cache

Le Hub regroupe déjà jusqu'à dix fiches par appel IA, tronque le texte de chaque fiche à environ 2 500 tokens et évite normalement de retraiter une URL déjà ingérée. Il peut néanmoins reprendre à chaque passage les découvertes en état `ERROR`. Un endpoint `run_every=ALWAYS` est éligible à chaque lancement ; `P1W` et `P1M` sont disponibles dans le BO pour les sources moins mouvantes.

Le cache de préfixe OpenAI est automatique sur les modèles compatibles, mais deux prompts Hub plaçaient l'heure courante dès le début et invalidaient la partie commune à chaque appel. L'heure est désormais après les consignes stables, juste avant les items. `OpenAI_lib` accepte une `prompt_cache_key` stable par workflow ; le Hub et les deux enrichisseurs en fournissent une. Cela peut réduire les **tokens d'entrée facturés** sur des appels rapprochés, pas le nombre d'appels Google, Playwright, Twilio ou OpenAI. Le gain réel doit être mesuré via `usage.input_tokens_details.cached_tokens` et le tableau de bord API, par modèle et par workflow. Aucun taux de cache ni économie chiffrée n'est garanti avant mesure sur les appels déployés.

Limites connues : les graphes complets Event, Experience et LocalHabit ne sont pas exposés ; pas de clé individuelle ni de verrou distribué pour empêcher deux imports Google concurrents ; pas encore de journal des coûts Google. La V0 ne suffit donc pas à un import automatique complet de tous les objets.

## Livraison

Pour cette V0 et Cryotera, les projets touchés sont `izilife-admin` (routes, contrôleurs, modèle), `izilife-db` (blocs de schéma à appliquer de façon ciblée sur bases existantes) et `scripts/izilife` (paquet JSON, tags, documentation). Le FO n'est pas modifié par ces nouvelles routes. Après livraison, vérifier l'authentification, les résultats de lecture, les cas ambigus et un import Google sur un environnement de test avant tout emploi en production.
