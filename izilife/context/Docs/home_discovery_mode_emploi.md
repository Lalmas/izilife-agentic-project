# Home contextuelle - mode d'emploi

## Fichier de configuration

Tous les interrupteurs editoriaux sont regroupes dans :

`app/Helpers/home_discovery_config_helper.php`

Les regles metier (heure, meteo, distance, calendrier) restent dans les helpers. La configuration sert a gerer l'affichage et le contenu sans modifier ces regles.

Le helper contient quatre registres :

- `home_discovery_now_intentions()` : toutes les IA du rail Maintenant ;
- `home_discovery_future_cards()` : intentions des prochains jours ;
- `home_discovery_settings()` : signaux, limites et interrupteurs globaux ;
- `home_discovery_feature_blocks()` : Meetz et futur bloc Selections.

## Activer ou masquer une carte

Dans `home_discovery_future_cards()`, modifier `enabled` :

```php
'future-randonnees' => [
    'enabled' => false,
],
```

- `true` : la carte peut apparaitre lorsque ses conditions sont remplies ;
- `false` : la carte est toujours masquee.

Interrupteurs globaux :

```php
'show_school_holidays' => true,
'show_bridges' => false,
'weekly_wheel_enabled' => false,
'show_spotlight_objects_now' => true,
'spotlight_now_radius_km' => 35,
'spotlight_now_limit' => 6,
```

## Modifier le texte, l'image ou le lien

```php
'future-cours-danse' => [
    'enabled' => true,
    'title' => 'Prendre un cours de danse',
    'description' => 'Cours et stages a decouvrir',
    'image' => 'sport.jpg',
    'internal_link' => 'whattodo/activity/danser/danser-cours-et-stage',
],
```

Les images des actions sont lues dans le repertoire CDN defini par `ACTIONS_MEDIAS_URL`, soit `statics/actions/`. Il suffit d'y deposer l'image puis d'indiquer son nom dans `image`.

## Carte Vacances

Elle se configure dans `home_discovery_school_holiday_card()` :

```php
return [
    'enabled' => true,
    'title' => 'Vacances',
    'description' => 'Des idees pour profiter des vacances',
    'use_period_name_as_description' => true,
    'image' => 'visit.jpg',
];
```

Avec `use_period_name_as_description = true`, le nom reel de la periode scolaire remplace la description. Passer la valeur a `false` pour afficher le texte manuel.

## Ajouter une nouvelle idee WTD

1. Ajouter sa production dans `home_future_actions()` dans `app/Helpers/home_highlight_helper.php`, avec un `string_id` unique et un `_score`.
2. Ajouter la meme cle dans `home_discovery_future_cards()` dans `home_discovery_config_helper.php`.
3. Definir `enabled`, `title`, `description`, `image` et `internal_link`.
4. Verifier que la route WTD renvoie bien une page.

Le `_score` determine l'ordre. `max_future_cards` limite le nombre total de cartes rendues.

## Meetz et Selections

Meetz est prepare avec `enabled = false`. Ne l'activer qu'apres branchement de la verification : feature active, ville Meetz active dans les 30 km et opportunite/slot disponible.

Le bloc `izilife-selections` est egalement prepare mais non rendu. Il devra lire les Selections actives et achetables avec un badge `Vendu par iziLife`.

## Actions generiques et objets directs

Les cartes `ACTION` ouvrent un WTD, qui resout ensuite les lieux, events, experiences, hotels ou escapades.

Le rail `Maintenant` injecte aussi directement les `EVENT` Spotlight du jour et les `EXPERIENCE` Spotlight dans le rayon configure. Ils conservent leur type reel et ouvrent leur fiche objet.

Les renderers savent egalement afficher `PLACE` et `SHOP`, mais leur injection Spotlight directe n'est pas activee dans ce rail pour le moment.

`A ne pas manquer` sait deja afficher ses highlights, campagnes et certains events selon ses producteurs propres.
