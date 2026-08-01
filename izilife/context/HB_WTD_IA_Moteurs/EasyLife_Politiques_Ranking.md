# EasyLife — Politiques de ranking communes

## Objectif

Ce document définit un vocabulaire simple et commun pour classer les résultats envoyés par :

- les Home Blocks ;
- les Navigation Categories et SubCategories de WTD ;
- la recherche par catégorie ;
- plus généralement, toutes les surfaces qui affichent des résultats multi-objets.

Le ranking intervient **après** les filtres. Il ne doit jamais remplacer ou neutraliser :

1. le type d’objet demandé ;
2. les catégories ;
3. `EtablishmentType` et son héritage ;
4. les conditions SQL ;
5. les contraintes géographiques ;
6. les contraintes temporelles ;
7. les profils, horaires, dates, météo et disponibilités.

## Chaîne de traitement commune

```text
1. Type d’objet
2. Catégories
3. EtablishmentType
4. Conditions SQL
5. Géographie
6. Temporalité et disponibilité
7. Calcul des scores
8. Politique de ranking
9. Limite et composition finale
```

## Scores

Les scores restent des signaux. Il ne faut pas créer une politique différente pour chaque score.

```text
quality_score =
    poids initial
  + completion
  + importance
  + nouveauté
  + spotlight
  + curation
  + extra
```

À terme, d’autres signaux peuvent être ajoutés sans créer une nouvelle stratégie :

- tag technique ;
- tag spécial rail ;
- compatibilité contextuelle ;
- popularité, lorsqu’elle sera fiable.

La distance ne doit pas être mélangée directement au `quality_score`. La politique choisit comment combiner qualité, distance et temps.

---

## 1. `distance_first`

### Usage

- autour de vous ;
- cafés ;
- bars ;
- restaurants ;
- commerces ;
- parcs ;
- services de proximité ;
- résultats WTD locaux.

### Ordre

```text
distance_band ASC
quality_score DESC
distance ASC
```

Exemple de couronnes :

```text
0–2 km
2–5 km
5–10 km
10–20 km
```

Cette stratégie évite qu’un objet d’Arras passe devant un objet pertinent de Lille ou Seclin uniquement grâce à un poids supérieur.

---

## 2. `score_in_radius`

### Usage

- meilleurs brunchs ;
- rooftops ;
- spas ;
- lieux romantiques ;
- bons cocktails ;
- escape games ;
- sélections locales où la qualité doit primer.

### Ordre

```text
quality_score DESC
distance ASC
```

Le rayon maximal reste obligatoire. Un excellent objet à 12 km peut passer devant un objet moyen à 2 km, mais aucun objet ne sort au-delà du rayon défini.

---

## 3. `score_global`

### Usage

Usage rare et explicite :

- incontournables ;
- plus beaux lieux ;
- destination exceptionnelle ;
- escapades ;
- grands rendez-vous ;
- lieux valant réellement le déplacement.

### Ordre

```text
quality_score DESC
distance ASC
```

La zone maximale est plus large que pour `score_in_radius`.

---

## 4. `event_temporal`

### Usage

- événements aujourd’hui ;
- événements ce soir ;
- concerts ce soir ;
- événements ce week-end ;
- événements dans les prochains jours.

### Mode `immediate`

```text
éligible aujourd’hui
encore disponible
heure de début ASC
distance_band ASC
quality_score DESC
```

### Mode `upcoming`

```text
date ASC
quality_score DESC
distance ASC
```

Configuration :

```php
'ranking' => [
    'strategy' => 'event_temporal',
    'event_mode' => 'immediate', // ou upcoming
],
```

---

## 5. `novelty_first`

### Usage

- nouvelles adresses ;
- nouveaux lieux ;
- ouvert récemment ;
- nouveautés locales.

### Ordre

```text
novelty_score DESC
quality_score DESC
distance ASC
```

Un seuil de qualité minimal doit rester obligatoire. La nouveauté seule ne suffit pas.

---

## 6. `serendipity`

### Usage

Uniquement pour quelques positions dans certains rails :

- à découvrir ;
- idées du moment ;
- autour de vous ;
- sélection hybride de la home.

Ce n’est pas un classement aléatoire complet.

```text
objets éligibles
seuil de qualité minimal
compatibilité avec le contexte
distance cohérente
favoriser les objets moins connus ou peu affichés
```

Recommandation : une ou deux cartes maximum dans un rail de dix. Le reste du rail conserve sa stratégie principale.

---

## Curation, Spotlight et sponsoring

Ces notions ne sont pas des politiques de ranking.

### Curation et Spotlight

Ils alimentent le `quality_score` :

- Spotlight ;
- tag spécial rail ;
- tag de curation ;
- objet important ;
- sélection manuelle.

Un bloc peut donc utiliser `distance_first` tout en accordant un bonus fort à un Spotlight.

### Sponsoring

Le sponsoring est une règle de composition :

```text
résultats naturels
+ nombre maximal d’objets sponsorisés
+ intercalage contrôlé
```

Il ne doit pas réordonner toute la requête naturelle. Un objet sponsorisé doit être signalé.

---

## Contrat minimal

```php
'ranking' => [
    'strategy' => 'distance_first',
    'distance_bands' => [2, 5, 10, 20],
    'event_mode' => null,
    'serendipity_slots' => 0,
],
```

Pour un événement ce soir :

```php
'ranking' => [
    'strategy' => 'event_temporal',
    'event_mode' => 'immediate',
    'distance_bands' => [5, 15, 30, 50],
],
```

Pour une sélection locale qualitative :

```php
'ranking' => [
    'strategy' => 'score_in_radius',
    'radius_km' => 30,
],
```

## Explicabilité attendue

Le mode debug doit pouvoir retourner :

```text
ranking_strategy
quality_score
distance_band
score_breakdown
matched_categories
matched_tags
spotlight_reason
geo_source
query_time
match_reasons
```

Cela permet de comprendre pourquoi un objet est sorti, sans changer le format normal utilisé par les renderers.
