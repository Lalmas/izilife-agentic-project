# IZILIFE — Architecture Fonctionnelle & Moteurs

# Vision Générale

Izilife n’est pas un simple réseau social, ni un simple annuaire local.

Le système mélange :

- découverte locale,
- recherche par intention,
- recommandations contextuelles,
- vie communautaire réelle,
- événements,
- escapades,
- réservations,
- acteurs locaux,
- temporalité culturelle.

Le principe central :

```txt
Tout doit pouvoir être relié au réel.
```

Il n’existe pas de logique purement virtuelle.

---

# Architecture Générale

Le système repose sur plusieurs moteurs séparés mais connectés.

```txt
Search
= recherche annuaire / catégories

Whattodo
= navigation par intention

HomeBuilder
= composition dynamique de l’accueil

SuggestionEngine
= recommandation contextuelle intelligente

LocalQueryEngine
= moteur SQL multi-sources commun
```

---

# 1. SEARCH

## Rôle

Search est le moteur :

```txt
annuaire / exploration par catégories
```

L’utilisateur cherche :

- un type de lieu,
- une activité,
- un commerce,
- une catégorie,
- un professionnel,
- un service,
- un acteur.

Exemples :

```txt
Restaurants
Bars
DJ
Artisans
Associations
Sport
Shopping
```

---

## Sources principales

Search utilise principalement :

```txt
DirectoryCategory
DirectoryCategoryGroup
DirectoryCategoryContents
```

---

## Fonctionnement

Search configure des sources pour :

```txt
Place
Shop
Page
Event
Experience
Community
...
```

Puis délègue au :

```txt
LocalQueryEngine
```

---

# 2. WHATTODO

## Rôle

Whattodo est :

```txt
la navigation par intention.
```

L’utilisateur ne cherche pas un objet.

Il cherche :

```txt
quoi faire.
```

Exemples :

```txt
Boire un verre
Bruncher
Faire du sport
Sortir ce soir
Se balader
Faire une escapade
Travailler
Découvrir la ville
```

---

## Différence avec Search

```txt
Search
→ “Je cherche une catégorie”

Whattodo
→ “Je cherche une intention”
```

---

## Architecture

Whattodo construit des configurations hybrides.

Le controller garde :

```txt
intelligence métier
fallbacks
subtilités produit
météo
heure
profil
priorités éditoriales
```

Le LocalQueryEngine reste :

```txt
un exécuteur SQL puissant.
```

---

## Important

Le système est volontairement hybride.

Il ne faut PAS déplacer toute l’intelligence dans le QB.

Architecture correcte :

```txt
Controller intelligent
→ construit une intention fine
→ configure des sources
→ LocalQueryEngine exécute
```

---

## Factorisation

Whattodo est progressivement factorisé.

Anciennes méthodes historiques :

```txt
beaucoup de logique métier directement dans le controller.
```

Nouvelle direction :

```php
$config = [...];
$results = $this->executeWtdQB($config);
```

---

# 3. HOMEBUILDER

## Rôle

HomeBuilder construit :

```txt
la page d’accueil dynamique.
```

Il compose :

- blocs objets,
- blocs éditoriaux,
- blocs héros,
- suggestions,
- campagnes,
- sections météo,
- sections temporelles,
- sections profil.

---

## Variables prises en compte

```txt
heure
météo
profil utilisateur
ville
saison
campagnes
celebrations
```

---

## Important

HomeBuilder n’est PAS un moteur de recherche.

C’est :

```txt
un moteur de composition éditoriale dynamique.
```

---

# 4. SUGGESTION ENGINE

## Rôle

Le moteur de suggestion est différent.

Il ne répond pas :

```txt
“quels objets existent ?”
```

Il répond :

```txt
“qu’est-ce qu’on devrait recommander maintenant ?”
```

---

## Exemple

```txt
Il fait beau
Il est 16h
Tu es proche du centre-ville
→ Va prendre un café en terrasse ici
```

---

## Pipeline

```txt
LocalSuggestionService
→ SuggestionCandidateProvider
→ CandidateNormalizer
→ SuggestionEngine
→ SuggestionRules
```

---

## Variables utilisées

```txt
météo
heure
distance
profil
historique
terrasse
saisonnalité
contexte
popularité
```

---

# 5. LOCALQUERYENGINE

# Rôle

Le LocalQueryEngine est :

```txt
le cœur SQL multi-sources.
```

---

## Fonction

Il :

- active des providers,
- génère des SELECT,
- assemble les requêtes,
- fait des UNION ALL,
- applique ranking,
- applique pagination.

---

## Ce qu’il N’EST PAS

Il n’est PAS :

```txt
le cerveau métier global.
```

Le controller garde l’intelligence produit.

---

## Sortie normalisée

Sortie volontairement legacy :

```php
id
name
string_id
type
weight
start_date
distance
```

---

## Providers

Le moteur repose sur des SourceProviders.

Exemples :

```txt
PlaceSourceProvider
ShopSourceProvider
EventSourceProvider
ExperienceSourceProvider
PageSourceProvider
CommunitySourceProvider
GroupSourceProvider
CitySourceProvider
AdministrativeDivisionSourceProvider
EventSerieSourceProvider
AnnualCelebrationSourceProvider
```

---

# OBJETS PRINCIPAUX

# PLACE

## Rôle

Lieux physiques.

Exemples :

```txt
parcs
monuments
cafés
musées
spots
terrasses
```

---

# SHOP

## Rôle

Commerce / établissement.

Exemples :

```txt
restaurants
bars
boutiques
salons
```

---

# PAGE

## IMPORTANT

Une Page n’est PAS juste une page sociale.

Certaines Pages deviennent :

```txt
de vrais objets métier.
```

---

## Exemples

```txt
DJ
Artiste
Association
Coach
Artisan
Photographe
Office de tourisme
Marque
```

---

## Structure

La nature métier est portée par :

```txt
PageCategory
```

---

## Capacités

Les capacités viennent notamment de :

```txt
sell_products
sell_services
receive_bookings
create_events
create_experiences
```

---

## Conséquence

Page doit être une vraie source affichable.

Donc :

```txt
PageSourceProvider
```

---

# CITY

## Rôle

Une ville peut devenir :

```txt
un objet de destination.
```

---

## Cas d’usage

```txt
escapades
balades
week-end
visite
voyage local
```

---

## Important

Une ville peut être :

```txt
ville voisine
métropole étrangère
destination touristique
```

---

# ADMINISTRATIVE DIVISION

## Rôle

Territoire plus large.

Exemples :

```txt
région
province
zone
territoire
```

---

# COMMUNITY

# IMPORTANT

Une Community n’est PAS un groupe Facebook.

C’est :

```txt
une identité collective réelle.
```

---

## Rôle

Une Community peut gérer :

```txt
agenda
sorties
réservations
membres
événements privés
mur
sondages
organisation réelle
```

---

## Structure

```txt
Community
= identité / réseau

Group
= organisation opérationnelle interne
```

---

## Décision importante

Il n’existe PAS de Group sans Community.

Donc :

```sql
community_id NOT NULL
```

---

## Architecture correcte

```txt
Page
= acteur / entité

Community
= réseau humain

Group
= cellule opérationnelle
```

---

## Exemple

```txt
Page :
Association Running Lyon

Community :
Communauté Running Lyon

Groups :
- Débutants
- Trail
- Fractionné
```

---

## SQL

En SQL :

```txt
UserGroup
```

Dans le code métier :

```txt
Group
```

Même logique que :

```txt
LocalEvent
→ Event
```

---

# EVENT

## Rôle

Occurrence datée concrète.

Exemples :

```txt
concert du 14 juin
soirée du vendredi
atelier demain
```

---

# EVENTSERIE

## Rôle

Concept récurrent / franchise événementielle.

---

## Exemples

```txt
Afterwork Sunset
Marché des Créateurs
Soirées Salsa Latina
Run Club Adidas
```

---

## Relation

```txt
EventSerie
→ plusieurs LocalEvent
```

---

# ANNUALCELEBRATION

## IMPORTANT

AnnualCelebration n’est PAS un simple marronnier calendrier.

C’est :

```txt
un gros événement territorial récurrent.
```

---

## Exemples

```txt
Braderie de Lille
Marché de Noël de Strasbourg
Fête des Lumières
Festival d’Avignon
```

---

## Important

Le marketing principal est porté par :

```txt
AnnualCelebration
```

pas par chaque occurrence.

---

# CELEBRATIONDAY

## Rôle

Date culturelle / calendrier.

---

## Exemples

```txt
Nouvel An Chinois
Halloween
Saint-Valentin
Fête de la Musique
```

---

# CAMPAIN

## IMPORTANT

Il n’existe PAS de CelebrationCampaign.

Le système utilise :

```txt
Campain
```

avec :

```txt
celebration_day_id
```

---

## Structure

```txt
CelebrationDay
→ Campain
```

---

## Exemple correct

```txt
CelebrationDay :
Nouvel An Chinois

Campain :
Campagne Nouvel An Chinois 2027

AnnualCelebration :
Festivités Nouvel An Chinois Paris 13e

LocalEvent :
Défilé officiel
```

---

# ESCAPADEPROPOSAL

## IMPORTANT

EscapadeProposal n’est PAS un objet affichable.

C’est :

```txt
une logique éditoriale de proposition.
```

---

## Rôle

EscapadeProposal décide :

```txt
quoi proposer
pourquoi
sur quelle cible
```

---

## Les vraies cibles affichées sont

```txt
Place
Shop
City
AdministrativeDivision
```

---

## Donc

Le provider doit sortir :

```txt
l’objet cible enrichi
```

et PAS :

```txt
EscapadeProposal brut.
```

---

# PROVIDERS

## Philosophie

Chaque source métier importante doit avoir :

```txt
un vrai provider dédié.
```

---

## À éviter

Les gros SkeletonProviders génériques.

---

## Direction correcte

```txt
PageSourceProvider
CommunitySourceProvider
GroupSourceProvider
CitySourceProvider
AdministrativeDivisionSourceProvider
EventSerieSourceProvider
AnnualCelebrationSourceProvider
```

---

# RANKING

## Important

Le futur danger principal du système :

```txt
cohérence du ranking multi-objets.
```

---

## Les objets mélangés deviennent très différents

```txt
Place
Shop
Page
Community
Group
Event
EventSerie
AnnualCelebration
City
Escapade
```

Le ranking devra rester cohérent selon :

```txt
intention
contexte
heure
météo
distance
popularité
profil
saisonnalité
```

---

# CONCLUSION

Izilife repose sur :

```txt
un moteur local multi-objets contextualisé.
```

Ce n’est :

- ni un réseau social,
- ni un annuaire,
- ni une app événementielle,
- ni un moteur de réservation,
- ni un guide touristique.

C’est :

```txt
un système hybride de découverte locale intelligente.
```

