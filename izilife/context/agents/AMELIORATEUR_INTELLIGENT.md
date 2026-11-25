# Améliorateur intelligent de fiches

## Décision

Le nouvel outil ne remplace pas l'importeur de sites complexes. Le projet possède déjà :

- `places/enrichisseur_contenus.py` pour collecter et analyser des pages ;
- `site_package.py` et les paquets JSON pour importer Services, EAP, Products, Equipment, Experiences, médias et circuits ;
- `tags/tags_and_characts.py` et `tags/references.json` pour appliquer tags, `PrincipalCharacteristics` et familles éditoriales par références stables.

La nouvelle brique doit produire une proposition de curation sémantique plus riche, sourcée et vérifiable. L'import reste déterministe via les routes Scraper existantes.

## Sources et priorité

1. API interne iziLife : état actuel et données déjà connues ;
2. site officiel de l'établissement ;
3. Google/Maps seulement pour les informations absentes ;
4. Instagram et autres réseaux lorsqu'ils sont accessibles et utiles ;
5. aucune valeur n'est déduite sans preuve : `unknown` reste distinct de `false`.

## Sortie

Le résultat est un JSON de proposition contenant :

- cible `scope_type` et `scope_ref` ;
- sources consultées et date de collecte ;
- tags avec leur famille et leur `string_id` ;
- champs `PrincipalCharacteristics` proposés avec valeur, confiance et preuve ;
- caractéristiques éditoriales (`MusicStyle`, `Dance`, `Sport`, `Hobby`, `ObjectOnPublicPlace`, etc.) ;
- éventuels liens, médias, équipements, Services, EAP et produits déjà compatibles avec le contrat de paquet ;
- avertissements, ambiguïtés et éléments refusés.

Chaque proposition conserve l'URL et un court élément de preuve. Une référence absente de `tags/references.json` reste en revue et n'est jamais inventée.

## Deux usages distincts

### Workflow interactif Codex

Adapté aux fiches importantes et difficiles. Codex navigue, comprend les pages et prépare le JSON ou le classeur de validation. Cet usage consomme les limites du compte ChatGPT/Codex connecté, pas directement la clé API du BO.

### Agent Python par lot

Adapté à un grand volume et aux lancements planifiés. Il utilise Playwright, puis une API de modèle pour l'analyse structurée. Il doit tronçonner et dédupliquer le contenu avant appel, utiliser le cache de prompt et écrire d'abord un rapport `analysis-only`.

Le workflow interactif sert de V0 pour stabiliser le contrat. Le batch n'est construit qu'après plusieurs fiches validées, afin de ne pas automatiser une taxonomie encore mouvante.

## Implémentation locale

`scripts/izilife/places/intelligent_enricher.py` matérialise la V0 par lot.
Pour une fiche, il :

1. lit d'abord la vue complète de l'API interne iziLife ;
2. collecte les pages officielles fournies et les tronque à 15 000 caractères ;
3. ne lance aucune IA par défaut ;
4. avec `--with-ai`, demande un JSON structuré ;
5. avec `--with-web-search`, autorise aussi l'outil de recherche web du modèle ;
6. compacte les référentiels par scope avant l'appel et rejette toute référence
   absente de `tags/references.json` ;
7. exige une courte citation exacte de la page collectée : une absence de
   mention, une supposition ou une valeur `0` sans négation explicite est
   rejetée ;
8. met en cache la proposition selon la fiche, les empreintes de pages et la
   version des référentiels ;
9. écrit un rapport JSON sourcé et un classeur compatible avec
   `tags_and_characts.py` ;
10. reste en analyse seule par défaut ; l'application exige simultanément
   `--apply --confirm-write`, filtre les propositions sous `--min-confidence`
   et réutilise la route déterministe `agentApplyTagsAndCharacts`.

Collecte et état iziLife sans coût IA :

```powershell
python scripts/izilife/places/intelligent_enricher.py `
  --env prod --scope-type SHOP --scope-ref ma-fiche `
  --source-url https://site-officiel.example/
```

Analyse payante bornée, toujours sans écriture iziLife :

```powershell
python scripts/izilife/places/intelligent_enricher.py `
  --env prod --scope-type SHOP --scope-ref ma-fiche `
  --source-url https://site-officiel.example/ --with-ai --with-web-search
```

Application explicite d'une proposition déjà contrôlée :

```powershell
python scripts/izilife/places/intelligent_enricher.py `
  --env local --scope-type SHOP --scope-ref ma-fiche `
  --source-url https://site-officiel.example/ `
  --apply --confirm-write --min-confidence 0.8
```

`OPENAI_API_KEY` est requis seulement pour les deux options IA. Le modèle peut
être changé par `OPENAI_ENRICHER_MODEL`. Les appels n'ont pas été lancés pendant
le développement.

Le 31 octobre 2026, le mode déterministe a été testé en lecture seule sur
`SHOP cryotera-pole-de-cryotherapie-lille` avec la fiche production et le site
officiel. Il a généré le JSON et le classeur d'analyse sans appel IA, sans coût
OpenAI et sans écriture iziLife. Le test de rejet des références inconnues passe
également.

Ce test ne signifie pas que Cryotera a été enrichi. Il prouve seulement que la
chaîne sait retrouver la fiche iziLife, collecter le site officiel, utiliser le
cache, conserver les preuves et refuser les références inconnues. La proposition
déterministe ne contenait aucun tag ou caractéristique accepté : rien n'a été
appliqué. Un enrichissement réel exige l'analyse IA ou une curation manuelle,
puis une validation séparée avant l'import Scraper.

Le 1er novembre 2026, le chemin d'écriture a été testé localement sur une fiche
`TEST-CODEX` avec un tag, une `PrincipalCharacteristics` et une `Atmosphere` :
le premier passage a créé les trois relations, le second passage identique a
renvoyé `changed: []`, puis la fiche et toutes ses relations de test ont été
supprimées. Ce test valide l'idempotence de l'import déterministe.

Une analyse IA réelle a ensuite été exécutée sur `SHOP cryotera-test-local` et
la page officielle Pressothérapie. Le premier essai a révélé un prompt de
64 855 tokens et deux déductions sans preuve ; aucune valeur n'a été appliquée.
Après compactage et ajout du contrôle de citation, le même essai consomme
13 225 tokens, ne propose plus de valeur non prouvée et reste en analyse seule.
Les tests permanents couvrent aussi le rejet de « no mention » comme fausse
preuve et la réduction des données envoyées au modèle.

## Sécurité métier

- aucune écriture pendant la recherche ;
- validation humaine du paquet avant appel Scraper ;
- résolution des références dans l'environnement cible ;
- aucun ID local/staging copié vers production ;
- journal des valeurs créées, ajoutées, ignorées et bloquées ;
- un objet existant n'est pas remplacé sans instruction explicite.
