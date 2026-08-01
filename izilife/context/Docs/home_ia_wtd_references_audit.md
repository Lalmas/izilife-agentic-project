# Audit IA Home -> WTD et référentiels

Date de contrôle : 16 juillet 2026.

## Sources de vérité utilisées

1. Catalogue IA : `app/Helpers/home_layout_helper.php`.
2. Configuration d'activation : `app/Helpers/home_discovery_config_helper.php`.
3. WTD multi-objet : `app/Controllers/Whattodo.php`.
4. Référentiels attendus : `C:/xampp/htdocs/izilife-admin/statics/izilife_new_version`, notamment `01_navigation.sql`.
5. Base locale `izilife2`, utilisée seulement pour savoir ce qui a déjà été exécuté.

L'outil `php tools/audit_home_ia_references.php` refait la comparaison. `ABSENT / PREVU` signifie que la référence est définie dans les SQL mais pas encore installée dans la base locale.

## Contrat temporel corrigé

- `randonnee` apparaît dans Maintenant seulement si la météo est praticable et s'il reste au moins quatre heures avant le coucher du soleil. Son WTD est `sport/sport-running-rando`.
- `sunset` n'utilise plus de plage horaire saisonnière fixe. Il dépend du vrai coucher de soleil du jour et d'une météo ensoleillée ou chaude.
- La randonnée reste aussi disponible dans Prochains jours comme intention de préparation.

## État des intentions Maintenant

| Intentions | Destination WTD | État du référentiel |
|---|---|---|
| Petit-déjeuner, café, brunch, déjeuner, dîner, goûter | WTD alimentation existants | prêt |
| Pause rapide | `manger/manger-vite` | prêt ; alias corrigé, aucune NC `pause-rapide` à créer |
| Pique-niquer | `pique-niquer` | prêt |
| Manger en plein air | `manger/manger-plein-air` | défini dans `01_navigation.sql`, pas encore dans la base locale |
| Se balader, balade nocturne | `flaner` | prêt |
| Prendre l'air avec les enfants | `activites-enfants` | prêt |
| Visiter | `sortir/sorties-culturelles-et-artistiques` | prêt |
| Shopping, chiner | WTD existants | prêt |
| Boire un verre, terrasse, guinguette, rooftop | WTD existants | prêt |
| Apéro pique-nique | `boire/apero-pique-nique` | SQL complémentaire préparé |
| Jouer, comedy club, concert, cinéma | WTD existants | prêt |
| Danser | `danser` | prêt |
| Sortir la nuit | `sortir/sortir-nuit` | SQL complémentaire préparé ; requête métier à finaliser pendant le chantier WTD |
| Se détendre, faire du sport | WTD existants | prêt |
| Sortie vélo | `sport/sport-velo` | prêt |
| Randonnée | `sport/sport-running-rando` | prêt |
| Apéro plein air | `boire/apero-plein-air` | défini dans `01_navigation.sql`, pas encore dans la base locale |
| Petits concerts locaux | `live-sessions/live-sessions-petits-concerts` | prêt |
| Balade nature | `flaner/balades-nature` | prêt |
| Bord de l'eau | `flaner/flaner-au-bord-de-leau` | prêt |
| Coucher de soleil | `spotlights/spotlight-sunset` | prêt |
| Café cosy | `cafe-the` | prêt |
| Exposition | `art/art-musees-galeries/expositions` | prêt ; `expositions` est une sous-catégorie, pas une NC racine |
| Journée plage, après-midi plage, côte | `vacances` | NC définie dans `01_navigation.sql`, pas encore dans la base locale |
| Journée lac | `outdoor` | prêt |
| City trip | `escapades` | prêt |
| Week-end amoureux | `escapades/escapades-weekend` | prêt |
| Lieux à tester | `spotlights` | prêt |

## État des intentions Prochains jours

| Carte | Destination | État |
|---|---|---|
| Journée plage | `vacances` | NC prévue dans le SQL nouvelle version |
| Escapades | `escapades` | prêt |
| Hôtel | `dormir/hotels` | prêt ; aucune disponibilité résolue sur la Home |
| Parc d'attractions | `parcs-dattractions` | lien corrigé vers la NC existante |
| Parc aquatique | `s-evader/experiences-aquatiques` | prêt |
| Journée lac, grands parcs | `outdoor` | prêt |
| Nuit insolite | `dormir/logements-insolites` | prêt |
| Cours de danse | `danser/danse-ecoles-clubs` | lien corrigé vers la NC existante |
| Randonnée | `sport/sport-running-rando` | lien corrigé vers la NC existante |
| Meetz | `izilifeMeetz` | contrôleur existant ; carte toujours conditionnée par l'activation métier |

## Tags et LocalQuery

Les chaînes qui étaient utilisées comme de faux tags ont été retirées ou remplacées par les bons référentiels :

- `cosy` relève d'`Atmosphere`, pas de `ShopAndPlaceCharactTag` ;
- `guinguette` relève de la catégorie/navigation ;
- `sortie-a-velo` relève de l'intention, des hobbies et de la navigation ;
- `base-de-loisirs` a été remplacé par le vrai `PlaceType` `base-de-plein-air-et-de-loisirs` ;
- `journee-famille` devient le signal prévu `parfait-famille-journee` ;
- `romantique` devient le tag existant `cadre-romantique` ;
- les catégories d'événements ont été alignées sur les identifiants existants (`tournoi-de-beer-pong`, `spectacle-comedie`, `animation-enfant`, etc.).

Les tags Home encore absents de la base locale sont déjà définis dans `01_navigation.sql` : `lac`, `plage`, `parfait-sunset`, `parfait-week-end`, `parfait-vacances`, `parfait-couple`, `parfait-famille-journee` et `vaut-le-deplacement`.

LocalQuery sait maintenant appliquer ces tags aux quatre sources principales :

- `PlaceCharactTag` ;
- `ShopCharactTag` ;
- `EventCharactTag` ;
- `ExperienceCharactTag`.

## SQL complémentaire

Le fichier `docs/sql/2026_07_home_opportunities_navigation_tags.sql` contient les deux seules NavigationCategory réellement absentes des SQL admin :

- `apero-pique-nique`, enfant de `boire` ;
- `sortir-nuit`, enfant de `sortir`.

Tout le reste doit venir de `izilife-admin/statics/izilife_new_version/01_navigation.sql`. Il ne faut pas recréer ces lignes séparément : il suffit d'exécuter ou de reporter les portions encore non installées.
