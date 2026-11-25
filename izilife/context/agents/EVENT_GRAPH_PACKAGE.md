# Paquet événementiel iziLife — contrat des conversations

Ce document décrit le contrat à utiliser lorsqu'une conversation reçoit un site, une page, un PDF, un post/carrousel social ou un événement iziLife existant et doit matérialiser un événement complexe.

## Séparation des responsabilités

- La conversation fait l'exploration intelligente : elle ouvre les sources, suit les pages utiles du même dossier, lit les PDF/images, recoupe les informations et décide de la structure métier.
- Elle ne remplit pas un tableur et ne lance pas un extracteur générique caché.
- Elle produit un unique JSON conforme à `izi.event.package.v1`.
- `POST /scraper/agentIngestEventPackage` valide, rapproche et insère ce JSON.
- Le contrôleur n'interprète jamais un site et n'appelle jamais un LLM.

Toujours conserver les URL ayant prouvé chaque objet. Ne jamais inventer une date, un lieu, un organisateur, un tarif ou une relation. Une information incertaine reste absente et doit être signalée dans `notes`.

## Choisir le paquet

### `EVENT_GRAPH`

Pour un dossier portant sur un événement structurant : festival, rendez-vous annuel, événement décliné en édition et programme.

- `EVENT_SERIE` : concept éditorial dont plusieurs éditions sont attendues (festival, salon, nocturne récurrente).
- `ANNUAL_CELEBRATION` : célébration calendaire/territoriale revenant annuellement (Braderie, marché de Noël, fête locale).
- Le paquet contient obligatoirement une première édition `ROOT_EDITION`.
- Si cette édition existe déjà dans iziLife, fournir `existing_ref` : elle est enrichie et rattachée, jamais dupliquée.

### `EDITORIAL_AGENDA`

Pour un carrousel, article « que faire », agenda de blogueur ou PDF contenant plusieurs événements indépendants.

- Chaque entrée est généralement `STANDALONE`.
- Les matchs sont ignorés : ils relèvent de l'objet `Match`.
- Une fiche déjà connue est enrichie seulement si les nouvelles données sont plus précises.
- `update_mode` vaut `ENRICH` par défaut : seuls ses champs vides sont complétés. Utiliser `OVERWRITE` uniquement lorsqu'une source officielle prouve qu'une valeur existante est fausse ou obsolète.
- Si plusieurs fiches peuvent correspondre, ne pas choisir arbitrairement : fournir une référence exacte ou laisser l'élément hors du paquet avec une note de revue.

## Relations à ne jamais confondre

- `ROOT_EDITION` : édition du `root` EventSerie/AnnualCelebration.
- `CHILD` + `parent_ref` : véritable LocalEvent du programme officiel, organisé par le même porteur ; il devient `LocalEvent.parent_id`.
- `OCCURRENCE` + `parent_ref` : autre séance/date du même événement ; elle devient `LocalEvent.is_another_date_of`, même lorsque le parent n'est pas récurrent. Ce n'est jamais un `CHILD`.
- `RELATED` + `related_to_ref` : événement tiers associé à une fête/édition, mais qui ne fait pas partie de son programme officiel. Il n'est jamais transformé en enfant.
- `programming[]` : ligne de programme légère (`EventProgrammation`), pas un LocalEvent autonome.
- `hourlies[]` : heures d'ouverture d'un événement réellement continu (`EventHourly`), par exemple une exposition du 1er au 31 ouverte de 10h à 18h. Une liste de représentations, séances ou ateliers datés utilise `OCCURRENCE`, jamais `hourlies`.

## Temporalité : ne jamais confondre durée et répétition

- `SINGLE_OCCURRENCE` : une seule séance ; début et fin décrivent sa durée réelle.
- `FINITE_OCCURRENCES` : liste finie de séances. La première est `STANDALONE`, les suivantes sont `OCCURRENCE`. Ne jamais étendre le parent de la première à la dernière date.
- `FIXED_RECURRENCE` : cadence stable explicitement annoncée, par exemple tous les samedis et dimanches de 15h à 19h. Utiliser une règle de récurrence, pas `hourlies`.
- `CONTINUOUS_SCHEDULE` : l'événement existe réellement pendant toute la période (exposition, foire, braderie) ; `hourlies` décrit alors ses ouvertures.

Exemples : « 3, 10, 17 novembre, 1er et 8 décembre, 9h30-11h30 » est une liste finie. « 4 novembre 14h30, 6 novembre 14h30, 7 novembre 16h30 » est aussi une liste finie, même si la source écrit « du 4 au 7 ». La période entre deux séances n'est pas la durée de l'événement.

## Références

Privilégier les références stables :

- `EVENT:<id|unique_id|event_string_id>`
- `PLACE:<string_id|unique_id|id>` / `SHOP:<string_id|unique_id|id>`
- catégories, villes, pages, partenaires, devises et types d'accès par leur `string_id` canonique.

Le rapprochement applique cet ordre : `existing_ref`, URL source déjà enregistrée, identifiant stable, puis titre + date + heure. Plusieurs résultats sur la dernière règle provoquent une erreur explicite.

## Forme minimale

```json
{
  "schema_version": "izi.event.package.v1",
  "package_kind": "EVENT_GRAPH",
  "publication": {"activate": true},
  "root": {
    "type": "EVENT_SERIE",
    "data": {
      "name": "Nom de la série",
      "string_id": "nom-de-la-serie",
      "event_category_ref": "festival"
    },
    "sources": [{"url": "https://exemple.fr", "kind": "OFFICIAL"}],
    "media": [{"image_url": "https://exemple.fr/cover.jpg", "is_principal": true}]
  },
  "events": [{
    "client_ref": "edition-2026",
    "relation": "ROOT_EDITION",
    "data": {
      "title": "Nom — édition 2026",
      "event_category_ref": "festival",
      "start_date": "2026-11-03",
      "start_hour": "10:00",
      "end_date": "2026-11-28",
      "end_hour": "18:00",
      "city_ref": "lille",
      "location_ref": "PLACE:palais-des-beaux-arts"
    },
    "hourlies": [{"date":"2026-11-03","opening_hour":"14:00","closing_hour":"18:00"}],
    "programming": [{
      "title": "Projection d'ouverture",
      "event_category_ref": "projection",
      "start_date": "2026-11-03",
      "start_hour": "19:30",
      "end_date": "2026-11-03",
      "end_hour": "21:30"
    }],
    "sources": [{"url":"https://exemple.fr/programme","kind":"OFFICIAL_PROGRAM"}],
    "media": [{"image_url":"https://exemple.fr/edition.jpg","is_principal":true}]
  }]
}
```

## Champs d'un événement

Chaque entrée de `events` accepte :

- `client_ref`, `relation`, `existing_ref`, `parent_ref`, `related_to_ref` ;
- `data` : `title`, descriptions, `event_category_ref`, dates/heures, `timezone_ref`, accès, prix de base, ville, adresse, coordonnées, `location_ref`, organisateur principal, statut ;
- `hourlies[]` ;
- `recurrence` : `rrule`, borne `until_date` facultative, `count_limit` facultatif et horizon ; uniquement pour `FIXED_RECURRENCE` ;
- `programming[]`, qui peut elle-même porter `access_prices[]` ;
- `access_prices[]` ;
- `organizers[]` (`PAGE`, `PARTNER`, `PLACE`, `SHOP`) ;
- `sources[]` ;
- `media[]` (`media_id` existant ou `image_url`).

`publication.activate=true` publie en une seule transaction la coquille, l'édition et tous les événements du paquet (`is_active=1`, `listable=1`), y compris ceux qui ont été rapprochés avec un objet existant. L'import ne peut atteindre cette étape que si les catégories obligatoires et toutes les références de lieux fournies ont été résolues. Sans ce drapeau, un nouvel événement reste inactif sauf `data.is_active=true`. Un tarif reste inactif et à confirmer sauf indication explicite.

Le schéma machine complet se trouve dans `event-package-v1.schema.json` dans ce dossier.

## Envoi

Envoyer le document JSON comme corps `application/json`, ou dans le champ POST `payload`, avec `X-Agent-Token`. Ajouter `dry_run=true` pour valider et simuler toute la transaction sans conserver d'écriture.

