# Home contextuelle V2 - etat et reste a faire

La reference produit est `docs/home_hb_mds_opportunites_v2.md`.

## Decisions figees

- Les stories sont mises de cote.
- La home conserve trois rails : `A ne pas manquer`, `Des idees pour maintenant`, `Dans les prochains jours`.
- Spotlight nourrit `Maintenant` ou `Prochains jours`, jamais automatiquement `A ne pas manquer`.
- Une `EventSerie` Spotlight doit transmettre le signal a ses events enfants.
- Une `AnnualCelebration` n'a pas besoin de Spotlight ; ses editions locales sont les gros events du territoire.
- Les vacances et ponts appartiennent uniquement a `A ne pas manquer`.
- Vacances est active ; Ponts reste masque par interrupteur.
- Une action generique peut ouvrir un WTD sans resoudre ses objets sur la home.
- `Week-end hotel` ne verifie pas la disponibilite des hotels sur la home ; le WTD en est responsable.

## Ce qui existe

- `app/Helpers/home_highlight_helper.php` construit les mises en avant, les vacances et les idees futures de base.
- `app/Helpers/calendar_signal_helper.php` lit le contexte calendrier.
- `app/Libraries/Home/HomeHorizonResolver.php` arbitre `Maintenant`, `Prochains jours` ou masque.
- `app/Helpers/home_builder_helper.php` branche les rails de la home.
- `docs/sql/2026_07_home_opportunities_navigation_tags.sql` prepare les tags et navigations a valider/appliquer.
- Les actions territoriales deja ajoutees restent activables progressivement selon leur WTD et leurs donnees.
- Le rail `Dans les prochains jours` produit maintenant : journee plage, escapades, hotel, parc d'attractions, parc aquatique, journee lac et grands parcs.
- Les liens WTD escapades, hotels, attractions, aquatique et outdoor ont ete verifies en local.
- Vacances n'est plus produite dans ce rail ; elle reste dans `A ne pas manquer`.

## Reste a faire prioritaire

1. Faire heriter le Spotlight `EVENT_SERIE` aux `Event.event_serie_id` sans dupliquer les cibles.
2. Faire remonter automatiquement les editions d'`AnnualCelebration` comme gros events locaux dans `A ne pas manquer`.
3. Finaliser le classement des events du jour : actif, a venir, termine, annule, explicitement complet ou acces ouvert.
4. Completer les donnees ou tags manquants dans les WTD ; la home ne doit pas compenser une base vide.
5. Utiliser un temps de trajet reel lorsqu'il existe, avec estimation par distance uniquement en repli.
6. Valider les tags des lieux concrets, notamment Pres du Hem, Citadelle, plages, lacs, grands parcs et spots sunset.
7. Verifier le rendu mobile et reduire les espaces inutiles sans toucher au header, aux menus, au dropdown ni a la bottom nav.

## Interrupteurs temporaires

Dans `app/Helpers/home_highlight_helper.php` :

- `home_highlight_show_school_holidays()` : `true` ;
- `home_highlight_show_bridges()` : `false` ;
- `home_weekly_wheel_is_enabled()` : `false`.

## Hors perimetre immediat

- Reprendre les stories.
- Reconstruire un MDS etendu generaliste.
- Ajouter un moteur de temps de trajet externe complet.
- Activer la roue avant la vraie methode d'eligibilite utilisateur.
