# Road to production — agents iziLife

État de référence au 5 novembre 2026. Ce document remplace la roadmap générale
pour le chantier de mise en production des agents.

## Objectif

Les agents doivent fonctionner depuis le Mac d'automatisation, sans ChatGPT et
sans intervention quotidienne. Le BO PHP reste le système métier : les scripts
Python collectent, structurent et appellent ses endpoints protégés.

Chaque exécution doit être :

- idempotente ;
- reprise après interruption sans retraiter les lignes terminées ;
- séparée par environnement et par zone ;
- explicite sur `done`, `skipped`, `needs_review` et `error` ;
- observable dans les journaux et dans `pilotage_global.xlsx` ;
- sans identifiant de base codé en dur.

## Décisions d'architecture

### 1. Pilotage

Il existe deux familles distinctes :

1. Les agents à données éditoriales manuelles sont pilotés par un classeur de
   zone : Pages, lieux à créer, curation manuelle, transferts,
   enrichissements ciblés et médias.
2. Les agents de pipeline n'ont pas de classeur métier : Hub, scrapers,
   rapprochements et validateur EventTmp. Ils parcourent la file serveur et
   produisent seulement un rapport d'exécution et une liste d'actions humaines.

Le classeur ne doit jamais être utilisé comme file technique quand une table
TMP existe déjà dans le BO.

### 2. Résolution Google partagée

Créer un service Python partagé dans `core` qui encapsule la recherche gratuite
Playwright et renvoie une preuve structurée : nom canonique, Google Place ID,
adresse, coordonnées, état d'activité et URL source.

Ce service sera utilisé par `createur_lieux.py`, `agent_pages.py`, les agents de
validation et les enrichisseurs. Il ne crée aucun objet et ne décide jamais de
la catégorie métier.

Ordre obligatoire pour un lieu ou une Page :

1. rechercher dans iziLife par string_id, Google Place ID et nom/adresse ;
2. confirmer gratuitement l'existence et le vrai nom avec Playwright ;
3. rejeter les établissements définitivement fermés ;
4. appeler Google Places payant uniquement si une création doit réellement
   être matérialisée.

### 3. Pages

`Page` reste une destination du validateur de POI et conserve également son
agent `pages.xlsx` pour les ajouts éditoriaux manuels. Les deux flux utilisent
le même endpoint d'upsert et le même anti-doublon par Google Place ID,
string_id, URL et réseaux sociaux.

L'agent Pages ne crée jamais de `PlaceTmp` : il upsert directement une `Page`.
Seul le validateur de POI peut choisir `PAGE` comme destination d'un POI déjà
présent dans sa propre file TMP.

L'agent Pages doit accepter un simple nom + ville : le résolveur partagé cherche
le nom canonique et le Google Place ID avant l'upsert.

### 4. Transferts et modifications

Ne pas mélanger les deux opérations :

- le modificateur change catégorie, statut, fermeture et données d'un objet de
  même type ;
- le transféreur crée une cible d'un autre type, transfère médias et relations,
  vérifie les usages commerciaux, puis désactive ou purge la source dans une
  transaction.

Le moteur général devra couvrir `PLACE`, `SHOP`, `PAGE`, `EQUIPMENT`, `EVENT`,
`EVENT_SERIE` et `EXPERIENCE`. Le socle actuel est fragmenté entre
`LocationTypeTransfer` (Place/Shop) et `ObjectConversion` (Event/XP/Serie). Un
classeur unique de transferts pilotera le moteur général ; aucune copie de
logique métier ne sera implémentée dans Python.

### 5. Validation automatique des événements

Le validateur EventTmp est un agent de pipeline sans Excel de pilotage. Il
traite la file EventTmp alimentée par les collecteurs existants. Il ne modifie
ni leurs agents ni leurs crons. Facebook et Shotgun sont déjà autonomes et
planifiés : ils sont hors du chantier prioritaire.

Il applique successivement :

1. filtres de date et exclusions éditoriales ;
2. normalisation déterministe des accès et horaires ;
3. résolution iziLife de la ville et du lieu ;
4. contrôle catégorie, description, image, prix et doublon ;
5. validation des seuls événements suffisamment complets ;
6. rapport unique des éléments restant à arbitrer.

Les représentations restent hors validation automatique. Un événement non
résolu mais géocodé peut être publié à son adresse ; le lieu manquant est envoyé
à la file de création sans bloquer l'événement.

Le validateur ne relance pas un LLM lorsque le Hub a déjà enregistré son analyse
dans EventTmp. L'IA intervient uniquement sur un champ réellement absent ou
ambigu et réutilise le résultat lors des passes suivantes.

### 6. Agrégateur territorial

`territorial_aggregator.py` existe avec état SQLite et rapprochement. Sa
configuration reste volontairement en JSON dans le Drive, classée par zone.
Chaque zone déclare les sources locales qui lui sont propres et les URL filtrées
des plateformes numériques (par exemple Meetup/HelloAsso avec leur filtre
territorial). Au lancement, l'agent charge uniquement le JSON de la zone et
exécute les connecteurs activés. Aucun classeur Excel n'est requis. Facebook et
Shotgun restent dans leurs agents et crons actuels ; leur éventuel rattachement
territorial futur ne fait pas partie de cette priorité.

### 7. Caractéristiques éditoriales des événements

Tous les extracteurs doivent produire le même bloc éditorial lorsque la source
le prouve : `MusicStyle`, `Dance`, `Sport` et autres référentiels existants.
Le LLM ne crée pas de libellé libre : il choisit dans les références actives du
BO. Les pivots sont matérialisés avec l'événement ou sa représentation.

### 8. Enrichissement des lieux

Les agents existants ont des responsabilités différentes :

- `enrichisseur.py` : file batch, maintenance et fermeture ;
- `google_hours_agent.py` : collecte spécialisée des horaires ;
- `intelligent_enricher.py` : analyse et propositions éditoriales ;
- `enrichisseur_contenus.py` : produits, services, équipements et EAP issus de
  sources web ;
- agents médias : téléchargement et rattachement des médias sélectionnés.

Ils doivent être orchestrés sous un même pipeline, pas fusionnés dans un gros
script. Les références déjà connues et à forte confiance sont appliquées
automatiquement. Seules une nouvelle référence ou une ambiguïté réelle créent
une demande de validation. Une proposition ne contenant que `confidence` ne
doit jamais créer de travail humain.

Pour la restauration, ajouter une classification éditoriale stable permettant
au minimum de distinguer service à table, gastronomique, restauration rapide
et principalement à emporter.

### 9. Extraction complète depuis un site

Le routeur `site_package.py` et les moteurs existent déjà pour :

- contenu de Place/Shop ;
- Experience ;
- Circuit ;
- paquet événementiel riche via le contrôleur Scraper.

Le moteur Place/Shop est responsable du graphe structurel. Les produits,
services, équipements et EAP détaillés restent la responsabilité de
`enrichisseur_contenus.py`, qui peut être appelé après le paquet. Il ne faut pas
dupliquer leur extraction dans plusieurs agents.

## État réel du crontab actuel

Les agents et crons Facebook/Shotgun existants ne sont pas modifiés. Le seul
ajout prioritaire de cette phase est le validateur EventTmp. L'agent territorial
multi-plateformes sera ajouté au pilotage dans une phase ultérieure.

La cible est une commande orchestratrice unique avec verrou anti-chevauchement :

```text
collecteurs et crons existants inchangés
  -> file EventTmp
  -> validateur EventTmp
  -> rapport/alerte uniquement si action requise ou erreur
```

## Ordre de finalisation

### P0 — événements automatiques

- [ ] Ne modifier ni Facebook, ni Shotgun, ni leurs crons.
- [ ] Finaliser le validateur EventTmp avec verrou, code retour et checkpoints.
- [ ] Finaliser le validateur EventTmp et son rapport synthétique.
- [ ] Tester le validateur sur une vraie file EventTmp en local, puis staging,
      puis production.
- [ ] Ajouter l'extraction et l'insertion des caractéristiques éditoriales.
- [ ] Laisser les représentations et les expériences en validation humaine.

### P0 — lieux nécessaires aux événements

- [ ] Extraire le résolveur Playwright partagé dans `core`.
- [ ] Terminer les deux phases de `createur_lieux.py`.
- [ ] Garantir qu'une ligne `unmapped` n'est retirée du classeur que si le TMP
      BO ou l'objet final existe réellement.
- [ ] Rattacher automatiquement les événements après création du lieu.

### P1 — pilotage territorial et Pages

- [ ] Initialiser et valider le JSON Drive de chaque zone avec ses sources
      locales et ses URL de plateformes filtrées.
- [ ] Faire utiliser le résolveur partagé par l'agent Pages.
- [ ] Ajouter Pages à l'anti-doublon Google Place ID de tous les imports.

### P1 — enrichisseur intelligent

- [ ] Créer l'orchestrateur des quatre sous-agents d'enrichissement.
- [ ] Appliquer automatiquement les références connues à forte confiance.
- [ ] Ne créer une ValidationRequest que pour une décision humaine réelle.
- [ ] Ajouter horaires, fermeture, description de référence et médias choisis.
- [ ] Ajouter la classification de restauration.

### P2 — transferts

- [ ] Étendre le moteur transactionnel aux objets Place/Shop/Page/Equipment et
      Event/Experience/EventSerie.
- [ ] Transférer médias, pivots éditoriaux, dépendances et rattachements.
- [ ] Ajouter le classeur de pilotage et les modes plan/apply.
- [ ] Ajouter les conversions depuis les files TMP dans les modals BO.

### P2 — paquets de site

- [ ] Ajouter un classeur de pilotage des URL et du type de paquet.
- [ ] Vérifier le plan/apply pour Place/Shop, Experience et Event riche.
- [ ] Chaîner l'enrichisseur de contenus après un paquet Place/Shop.

## Critères de mise en production

Un agent n'entre dans le crontab que si :

- son `--help` fonctionne dans le même environnement Python que le cron ;
- un smoke test local et staging est vert ;
- le mode production exige une confirmation explicite dans sa configuration ;
- une seconde exécution ne crée aucun doublon ;
- une interruption peut reprendre au dernier checkpoint ;
- le rapport contient les compteurs et les raisons d'échec ;
- aucun secret, chemin Windows ou ID de base n'est codé dans le script.

