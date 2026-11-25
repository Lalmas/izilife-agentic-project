# Agrégateurs d'événements — JDS, InfoLocale et Ma Vie Lilloise

## Décision

JDS, InfoLocale et l'agenda de Ma Vie Lilloise ne sont pas configurés comme des endpoints ordinaires d'un Hub.

Les Hubs restent réservés en priorité aux sources officielles et directement responsables de leurs contenus : établissements, villes, offices, organisateurs et agendas officiels. JDS et InfoLocale sont des agrégateurs de couverture secondaire. Ils peuvent trouver des événements absents des Hubs, mais ils réécrivent les fiches et utilisent parfois un lien de billetterie ou d'affiliation différent de celui de la source officielle.

Ils seront traités par des adaptateurs spécialisés partageant le même moteur de rapprochement. Leur rôle est de compléter les manques, pas de devenir la source prioritaire d'un événement.

Pour Ma Vie Lilloise, cette décision concerne l'endpoint d'agenda `EVENT`, qui rassemble des événements provenant de nombreux lieux indépendants. Elle ne supprime pas automatiquement d'éventuels endpoints distincts portant un contenu éditorial original (`NEWS`, guide ou autre objet) : ceux-ci sont évalués séparément.

## Moteur territorial commun

Un seul moteur Python pilote plusieurs adaptateurs. Une configuration de zone définit le territoire, les villes, le rayon, la fenêtre de dates, la cadence, les limites et les sources actives. Les premiers adaptateurs sont JDS, InfoLocale et Ma Vie Lilloise. Fnac Spectacles et Ticketmaster pourront être ajoutés ensuite sans modifier le moteur commun.

Chaque adaptateur renvoie le même candidat brut : URL canonique, identifiant externe, titre, dates et heures visibles, lieu, adresse, ville, URL de billetterie, empreinte du contenu et source. Cette étape n'appelle pas le LLM.

Le classeur de pilotage et le journal distinguent au minimum : `DISCOVERED`, `KNOWN_SOURCE`, `MATCHED_OBJECT`, `AMBIGUOUS`, `NEW`, `SENT_TO_LLM`, `TMP_CREATED`, `ERROR`.

## Pipeline prévu

1. Découverte sans LLM par parseur déterministe, requête HTTP ou Playwright selon le site.
2. Conservation de l'URL de l'agrégateur, des identifiants visibles, des liens sortants de billetterie, du titre, de la date, de l'heure, du lieu et de la ville.
3. Déduplication avant LLM :
   - URL ou identifiant source déjà connu **pour la même date/séance** ;
   - URL de billetterie déjà rattachée à un Event, une Representation, une Experience ou un TMP ;
   - correspondance déterministe sur lieu, date, heure et titre normalisé ;
   - comparaison avec les objets publiés et les propositions TMP, toutes sources confondues.
4. Si la correspondance est certaine, rattacher la nouvelle source à l'objet existant sans créer un nouveau TMP.
5. Si plusieurs correspondances sont possibles, conserver le candidat pour validation sans fusion automatique.
6. Envoyer au LLM uniquement les candidats réellement nouveaux et suffisamment complets.

Le rapprochement doit être un service partagé avec le Hub et les autres collecteurs. Une empreinte connue par une autre source doit donc empêcher un second appel LLM, même si l'URL de l'agrégateur est différente. Une correspondance certaine rattache seulement une nouvelle `ContentSourceReference` à l'objet existant ; elle ne fusionne ni ne remplace ses données. Une URL commune à plusieurs séances n'est pas décisive seule : la date de l'Event ou d'une édition de la Representation doit aussi correspondre.

Une ressemblance de titre seule n'autorise jamais un rattachement. Deux séances différentes d'un même spectacle restent deux `LocalEvent`. Les sources et liens de billetterie sont conservés sans écraser les informations éditoriales ou les médias déjà validés.

## Couverture officielle et délai de grâce

La présence d'un lieu dans un Hub n'entraîne pas l'exclusion définitive d'un candidat JDS ou InfoLocale : l'endpoint officiel peut être incomplet ou temporairement en erreur.

Lorsqu'un candidat concerne un lieu couvert par un endpoint officiel actif :

- le candidat est découvert sans appel LLM ;
- un run récent du Hub officiel est vérifié en premier ;
- le rapprochement est rejoué après ce run ;
- seul un candidat encore absent peut poursuivre vers l'extraction.

Ce mécanisme donne la priorité aux sources officielles sans perdre un événement réellement manquant.

## Cadence proposée

- JDS Lille : collecte incrémentale hebdomadaire sur une fenêtre future bornée.
- Ma Vie Lilloise : collecte incrémentale hebdomadaire sur la même couverture lilloise.
- InfoLocale : collecte incrémentale hebdomadaire par territoire, avec un audit de couverture plus large mensuel.
- Une URL ou une empreinte déjà traitée reste idempotente et n'est pas renvoyée au LLM.

La rétention de quatorze jours utilisée pour les fichiers de curation ne suffit pas à ce chantier : les URLs, identifiants externes et références de source validées doivent rester connus durablement. L'empreinte de contenu peut, elle, avoir une durée limitée afin de permettre la détection d'une vraie modification.

La fréquence exacte, les limites de pagination et la fenêtre de dates seront fixées après un premier inventaire en mode analyse seule.

## État du code existant

Le backend possède déjà plusieurs briques utiles :

- `location_discovered_item` déduplique les découvertes d'un endpoint par empreinte ;
- `ContentSourceReference` normalise et mémorise les URLs de source et de billetterie des objets validés ;
- le Hub évite déjà un appel LLM lorsqu'une URL de page ou une billetterie connue est retrouvée dans la fiche collectée ;
- `LlmIngestor` et `ProposalReconciler` éliminent certains doublons après extraction.

La lacune à combler est un rapprochement commun, avant LLM et entre toutes les sources, lorsque JDS, InfoLocale et la source officielle utilisent des URLs différentes.

## Hors périmètre immédiat

- Aucun collecteur n'est lancé en production pendant la conception.
- Aucun événement publié n'est fusionné ou supprimé automatiquement.
- Fnac Spectacles et Ticketmaster ne sont pas ajoutés automatiquement à ce chantier. Leurs liens servent d'abord d'identifiants de rapprochement. Une collecte directe de billetterie constituera un chantier séparé.

## Implémentation locale

Le moteur opérateur est `scripts/izilife/events/territorial_aggregator.py` et sa
première configuration est
`scripts/izilife/events/territorial_sources/lille-zone.json`.

Il sait maintenant :

- collecter JDS Lille et InfoLocale sans LLM ;
- extraire les objets JSON-LD `Event`, leurs horaires, lieux et billetteries ;
- découvrir les pages de détail du même domaine ;
- cibler la page InfoLocale de Lille au lieu de parcourir aveuglément l'agenda national ;
- lire la ville réelle dans `location.address.addressLocality`, y compris le format objet propre à InfoLocale, et refuser un candidat national sans ville fiable ;
- convertir les dates ISO classiques et le format compact InfoLocale `YYYYMMDDTHHMMSS` ;
- retenter avec Playwright lorsqu'une page JDS répond sans données exploitables ;
- canoniser les URLs et supprimer leurs paramètres de suivi ;
- garder deux séances du même spectacle distinctes par date et heure ;
- mémoriser durablement URL + empreinte dans SQLite ;
- envoyer les lots de 100 au rapprochement BO `agentMatchEventCandidates` ;
- produire un rapport JSON et Excel avec `KNOWN_SOURCE`, `MATCHED_OBJECT`,
  `MATCHED_TMP`, `AMBIGUOUS`, `NEW`, `INVALID` ou `ERROR` ;
- n'envoyer au pipeline LLM existant que les pages `NEW`, uniquement avec
  `--send-new-to-scraper --confirm-write`.

Ma Vie Lilloise est collectée hors Hub depuis son agenda public
`https://www.mavielilloise.fr/evenements-lille/c/0`. Les motifs de fiches détail
proviennent de l'ancien endpoint local ; le retrait de l'endpoint Hub évite que
les mêmes pages entrent directement dans le pipeline LLM.

Analyse sans écriture :

```powershell
python scripts/izilife/events/territorial_aggregator.py `
  --env staging --config scripts/izilife/events/territorial_sources/lille-zone.json
```

Le contrôleur et le modèle de rapprochement sont prêts localement dans
`izilife-admin`, mais doivent être livrés avant l'appel staging/production. Le
collecteur n'a pas été lancé en production dans ce chantier.

## Vérifications du 31 octobre 2026

- six tests unitaires passent : canonisation, distinction des séances, extraction JSON-LD, ville réelle, priorité aux fiches détail et format de date InfoLocale ;
- un inventaire réseau réel JDS a produit 19 candidats sans erreur ;
- un inventaire réseau réel InfoLocale Lille limité à dix fiches a produit dix candidats Lille structurés, sans erreur ;
- ces essais ont utilisé `--no-api-match` : aucun LLM, aucun EventTmp et aucune écriture iziLife.

## Vérifications locales du 1er novembre 2026

- un passage réseau réel borné a produit 29 candidats : 25 JDS et 4 InfoLocale,
  sans erreur et sans appel LLM ;
- le second passage identique a classé les 29 candidats `KNOWN_SOURCE` : aucun
  candidat n'a été renvoyé au LLM ni transformé en EventTmp ;
- le rapport ne conserve plus le HTML brut des pages et pèse environ 24 Ko au
  lieu de plusieurs mégaoctets ;
- les six tests unitaires restent verts ;
- un test transactionnel local confirme qu'une URL connue et la même date
  retrouvent l'Event, tandis que la même URL avec une autre date reste distincte ;
- après activation de Ma Vie Lilloise, un passage réel borné a produit 54
  candidats : 38 JDS, 8 InfoLocale et 8 Ma Vie Lilloise, sans erreur, sans LLM
  et sans écriture iziLife ;
- le second passage identique a classé les 54 candidats `KNOWN_SOURCE`.

