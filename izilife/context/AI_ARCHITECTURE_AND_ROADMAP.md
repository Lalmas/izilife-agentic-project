# Architecture IA iziLife et feuille de route

Dernière mise à jour : 23 octobre 2026.

## Objet du document

Ce document décrit la couche IA actuellement en place dans `izilife-admin` et `izilife`, les décisions prises pendant le chantier d'unification, les garanties déjà testées et les évolutions restant à réaliser.

Le principe directeur est le suivant : le code métier exprime une opération iziLife, tandis que le fournisseur IA reste un détail de transport. Un contrôleur, un modèle ou un service métier ne doit pas construire directement une requête OpenAI, Anthropic, Mistral, Kimi ou DeepSeek.

## État actuel

### Back-office `izilife-admin`

Le BO contient le cœur fonctionnel de l'IA.

- `AIClient_lib` est la façade unique appelée par les consommateurs.
- `AIProviderRegistry` construit les fournisseurs à la demande et conserve leurs instances.
- `AIWorkflow_lib` contient les opérations métier, les prompts et la normalisation des réponses.
- `OpenAI_lib` contient uniquement le transport OpenAI. Il utilise Responses API par défaut et conserve Chat Completions comme retour arrière explicite.
- `Claude_lib` contient le transport Anthropic et ses adaptations de format.
- `OpenAICompatible_lib` mutualise le transport Chat Completions utilisé par Mistral, Kimi et DeepSeek.
- `Mistral_lib`, `Kimi_lib` et `DeepSeek_lib` ne contiennent aucune logique métier iziLife.
- Aucun fallback automatique n'est autorisé. Une opération demandée à un fournisseur reste attachée à ce fournisseur et expose son échec.

Les principaux workflows BO unifiés sont :

- extraction d'événements depuis du texte, des pages ou des images ;
- extraction d'expériences ;
- extraction de produits, menus et quantités ;
- analyse d'actualités ;
- analyse des médias d'avis ;
- génération de certains textes métier ;
- traitement multi-ITEM du Hub de scraping.

Le Hub effectue deux niveaux de regroupement :

1. `HubRunnerService` forme des lots de contenus ;
2. le workflow IA redécoupe chaque lot selon son budget de tokens, appelle le fournisseur sélectionné et fusionne les résultats par `discovered_item_id`.

Un défaut historique a été corrigé dans ce mécanisme : la troncature d'un ITEM trop volumineux pouvait supprimer la structure de son en-tête et perdre silencieusement l'ITEM. L'en-tête est désormais conservé et seul le corps est tronqué.

### Front-office `izilife`

Le FO utilise la même organisation générale, mais reste volontairement plus léger :

- façade `AIClient_lib` ;
- registre `AIProviderRegistry` ;
- transports OpenAI, Claude, Mistral, Kimi et DeepSeek ;
- base commune `OpenAICompatible_lib` ;
- aucun workflow OCR ou scraping BO copié dans le FO.

Les trois usages IA réellement actifs dans le FO sont :

- modération textuelle des avis ;
- modération textuelle des vécus ;
- proposition, puis mémorisation en base, d'une description touristique lorsqu'un territoire n'en possède aucune.

Les prompts de ces usages restent dans leurs services métier respectifs. Ces services reçoivent maintenant la façade IA par injection, ce qui les rend testables sans réseau.

Le transport FO transmet réellement `max_tokens`, le mode JSON, la température et les timeouts. Avant l'unification, `max_tokens` était fourni par les services de modération mais ignoré par le transport OpenAI.

Dans le BO comme dans le FO, `OPENAI_API_TRANSPORT=responses` est la valeur par défaut. `OPENAI_API_TRANSPORT=chat_completions` permet un retour arrière temporaire sans toucher aux consommateurs ni aux prompts. Le transport Responses désactive le stockage fournisseur (`store=false`) et expose l'usage normalisé : entrée, sortie, total et entrée mise en cache.

### `izilife-partner-admin`

Ce projet reste volontairement différé. Son besoin actuel est plus petit, notamment la compréhension de messages texte ou vocaux. La couche commune devra y être diffusée seulement après stabilisation en production du BO et du FO.

## Duplication actuelle

Oui, une partie de l'infrastructure est actuellement dupliquée entre BO et FO :

- façade ;
- registre de fournisseurs ;
- transports ;
- résolution des variables d'environnement.

Cette duplication est temporaire et assumée afin de ne pas introduire simultanément un nouveau package partagé à quelques jours de la mise en production.

Ce qui n'est pas dupliqué :

- les gros prompts et workflows OCR/scraping restent uniquement dans le BO ;
- le FO ne dépend pas du moteur de Hub ;
- les services métier propres au FO restent dans le FO.

Les fichiers ne sont donc pas nécessairement identiques octet par octet. Le BO possède une interface plus large et des utilitaires de découpage spécifiques. La cible finale est un noyau partagé, pas la copie du moteur métier complet dans chaque application.

## Configuration des fournisseurs

La variable canonique est :

```text
AI_DEFAULT_PROVIDER=openai
```

Les anciens noms restent temporairement acceptés pour compatibilité, notamment `AI_DEFAULT_ENTITY`.

Fournisseurs enregistrés :

```text
openai
claude
mistral
kimi
deepseek
```

Alias acceptés :

```text
gpt       -> openai
anthropic -> claude
moonshot  -> kimi
```

Le choix explicite d'un fournisseur se fait par la façade :

```php
$ai->with('mistral')->chat($prompt, $options);
```

L'absence de clé ou l'échec d'un fournisseur ne doit jamais provoquer silencieusement un appel chez un autre fournisseur.

## Niveau de validation actuel

OpenAI Responses a été testé réellement dans le BO avec :

- deux images de menus ;
- une affiche d'événement ;
- les workflows produits, quantités et événement.

Après la bascule, un smoke test Responses a extrait 24 produits du menu Don Vito et un événement complet de l'affiche Battle Blindtest (date du 23 octobre 2026, 20 h, La Mousse Touch). Les tests de transport couvrent aussi le décodage Responses, le JSON structuré, la vision, `store=false`, les compteurs d'usage et le retour arrière Chat Completions.

Mistral, Kimi et DeepSeek ont été testés avec des transports HTTP simulés. Ces tests vérifient :

- la sélection du fournisseur ;
- l'URL et l'authentification construites ;
- le modèle texte ou vision ;
- les messages système et utilisateur ;
- `max_tokens`, température, timeouts et mode JSON ;
- le format des images ;
- le passage des workflows par la façade ;
- l'absence de fallback ;
- le découpage et la fusion des lots du Hub.

Ces tests ne prouvent pas encore l'authentification réelle, la disponibilité des modèles sur les comptes, la qualité métier, la latence, les coûts ou les particularités de quota de chaque fournisseur.

Les fournisseurs autres qu'OpenAI doivent rester désactivés en production jusqu'à un smoke test réel texte, JSON et vision avec leurs clés.

## Ce qui reste à faire dans le BO

### Priorité 1 — stabilisation et observabilité

1. Ajouter une mesure uniforme par appel : fournisseur, modèle, workflow, durée, statut, tokens d'entrée, tokens de sortie, tokens mis en cache et coût estimé.
2. Définir une corrélation entre un appel IA, un run de scraping et les ITEM concernés, sans journaliser de données personnelles ni les clés.
3. Ajouter des fixtures représentatives et des tests de non-régression des schémas JSON pour les événements, expériences, produits, quantités, actualités et médias d'avis.
4. Valider en réel Mistral, Kimi, DeepSeek et Claude avec de petits jeux de données contrôlés.
5. Nettoyer la configuration résiduelle : faire de `AI_DEFAULT_PROVIDER` la seule source canonique puis retirer les anciens alias après migration des environnements.

### Priorité 2 — réduction des coûts OpenAI

1. Responses API est désormais le transport OpenAI par défaut ; conserver temporairement Chat Completions comme retour arrière sélectionnable.
2. Comparer les résultats et coûts des deux transports sur les mêmes fixtures avant de supprimer le retour arrière.
3. Exploiter le cache de prompts lorsque le fournisseur le permet, en gardant des préfixes système stables.
4. Éviter de renvoyer des référentiels constants dans chaque requête lorsque ceux-ci peuvent être versionnés, condensés ou mis en cache.
5. Enregistrer les informations d'usage retournées par les API au lieu de dépendre uniquement d'estimations locales.
6. Ajuster les modèles par workflow seulement après mesure : modèle peu coûteux pour classification/modération simple, modèle plus robuste pour extraction complexe.
7. Étudier le traitement Batch pour les travaux non synchrones et volumineux.

### Priorité 3 — contrats et capacités

Les méthodes anticipées `embeddings()` et `runAgent()` ont été retirées du contrat BO : aucun consommateur ne les appelait et elles imposaient de fausses capacités à tous les fournisseurs. Elles seront réintroduites sous forme de capacités séparées seulement lorsqu'un besoin réel apparaîtra.

La cible est de remplacer ce contrat uniforme trop large par des capacités déclarées, par exemple :

```text
text
vision
json
embeddings
responses
agent
audio
```

Un workflow doit vérifier la capacité requise avant l'appel et retourner une erreur métier explicite si le fournisseur choisi ne la possède pas.

### Priorité 4 — package partagé `izilife-libs`

Lorsque BO et FO auront tourné de manière stable :

1. créer un package partagé versionné ;
2. y déplacer l'interface fournisseur, le registre, les erreurs normalisées et les transports ;
3. conserver les workflows métier dans leur application lorsqu'ils ne sont pas réellement partagés ;
4. ajouter des tests de compatibilité pour chaque application ;
5. migrer `izilife-partner-admin` vers ce package ;
6. supprimer seulement ensuite les copies locales.

Le package partagé ne doit pas contenir de contrôleurs, de modèles CodeIgniter ni de règles métier spécifiques au Hub.

### Priorité 5 — routage, sans fallback implicite

Un routeur pourra ultérieurement choisir un fournisseur selon :

- la capacité nécessaire ;
- le coût observé ;
- la qualité mesurée sur le workflow ;
- la latence ;
- la résidence ou sensibilité des données ;
- la disponibilité d'un modèle open-weight interne.

Ce routage doit être explicite, observable et configurable. Il ne doit pas devenir un fallback silencieux masquant une panne ou changeant la qualité d'un traitement sans trace.

## Évolutions métier envisagées

Ces fonctions ne doivent être ajoutées que lorsqu'un besoin produit réel existe :

- création ou amélioration de descriptions ;
- traduction de contenus ;
- transformation d'un message ou audio partenaire en brouillon de réservation, événement, produit ou prestation ;
- enrichissement contrôlé de lieux depuis plusieurs sources ;
- détection de doublons d'événements ;
- contrôles de qualité des contenus avant publication ;
- modération de contenus textuels ou visuels ;
- assistant conversationnel Muse ;
- investigation d'incidents ou d'attaques en lecture seule ;
- exécution future sur un modèle open-weight interne.

La majorité de ces usages sont des appels stateless et relèvent de la Responses API ou d'un équivalent fournisseur. Un agent persistant ne se justifie que lorsqu'il faut conserver un véritable état de travail, utiliser plusieurs outils de façon autonome ou conduire une investigation en plusieurs étapes.

## Règles d'architecture pour les futurs développements

1. Aucun contrôleur ne construit une requête HTTP vers un fournisseur IA.
2. Aucun prompt métier ne vit dans une classe de transport.
3. Un nouveau besoin métier devient un service ou un workflow nommé.
4. Un fournisseur ne connaît ni les tables, ni les entités, ni les règles iziLife.
5. Les réponses structurées sont validées avant écriture en base.
6. Une erreur IA ne doit jamais publier ou modifier silencieusement une donnée sensible.
7. Les appels synchrones sont réservés aux parcours où l'utilisateur attend réellement le résultat.
8. Les traitements longs ou massifs deviennent des jobs idempotents et reprenables.
9. Les clés restent dans l'environnement et ne sont jamais journalisées.
10. Tout changement de modèle, de prompt ou de fournisseur est mesuré sur des fixtures avant déploiement.

## Ordre recommandé des prochains chantiers

1. Mettre en production l'architecture actuelle avec OpenAI uniquement.
2. Observer erreurs, latences et stabilité sans changer les prompts.
3. Ajouter la comptabilité tokens/coûts et les fixtures d'évaluation.
4. Mesurer l'usage et le cache du transport Responses déjà actif, puis réduire les coûts.
5. Retirer le retour arrière Chat Completions après la période de validation.
6. Valider réellement un fournisseur alternatif à la fois.
7. Créer `izilife-libs` et supprimer la duplication.
8. Diffuser la couche dans `izilife-partner-admin`.
9. Ajouter les nouvelles fonctions métier seulement selon leur valeur produit.
10. Ajouter plus tard un routeur mesuré et le fournisseur open-weight interne.

## Critères de fin du chantier d'infrastructure

Le socle IA pourra être considéré complètement industrialisé lorsque :

- les trois applications consommeront le même package de transport versionné ;
- chaque workflow possédera des fixtures et un schéma de sortie validé ;
- les tokens, coûts, latences et erreurs seront mesurés ;
- Chat Completions et Responses pourront être comparés sans modifier les consommateurs, puis l'ancien transport pourra être retiré ;
- au moins un fournisseur alternatif aura passé des tests réels ;
- les capacités non supportées seront déclarées explicitement ;
- le changement de fournisseur ou de modèle ne nécessitera aucune modification des contrôleurs.
