# Audit collaboratif WTD - Sessions

Statut : implementation technique terminee le 28/09/2026; validation fonctionnelle manuelle a faire avec le produit.

## Intention metier donnee par le produit

`Sessions` fait partie des espaces niches, comme Danser, Marches ou Sport. Il doit faire remonter des petits evenements musicaux locaux peu visibles ailleurs : petits concerts, jams, scenes ouvertes, programmations de collectifs et d'ecoles de musique, notamment dans les bars, restaurants, cafes et petites salles. Il ne doit pas devenir une copie des gros concerts et festivals.

Le parent `live-sessions` affiche par defaut des evenements et, lorsqu'elles existent, des experiences musicales. Il n'affiche pas directement les fiches permanentes des ecoles, collectifs ou etablissements. Ces objets servent a qualifier, organiser ou alimenter les editions affichables.

## NavigationCategory actuelle

- `live-sessions` : parent actif.
- `live-sessions-jams` : enfant actif.
- `live-sessions-petits-concerts` : enfant actif.
- `live-sessions-scenes-locales` : enfant actif.
- `live-sessions-collectifs` : enfant actif.
- `live-sessions-ecoles` : enfant actif, masque pour les profils enfant.
- `petits-concerts-locaux` : doublon supprime du SQL de navigation.

## Referentiels constates

### EventCategory

Existants : `concert`, `festival`, `jam-session`, `open-mic`, `scene-ouverte`.

Absents : `session-live`, `audition`. Leur creation n'est pas justifiee tant que le besoin ne peut pas etre couvert proprement par les categories existantes et les liens de programmation.

### Shop

La gestion multi-categorie existante a ete branchee dans `ShopSourceProvider` et `PlaceSourceProvider`. Elle controle la categorie principale puis `LocationOtherCategory`, uniquement lorsque le drapeau `is_multi_category_shop` ou `is_multi_category_place` est actif.

`cafe-concert` peut etre represente par un Cafe ou un Bar qualifie par `bien-pour-concerts`; `petite-salle-de-concert` n'a pas vocation a devenir une ShopCategory.

Le tag reel `bien-pour-concerts` existe pour qualifier les lieux. `concert` est une EventCategory et `live-music` ne correspond pas a un referentiel utile : ils ont ete retires des tags de la nouvelle requete Sessions. Le tag Event existant `scenes-izilife` couvre deja le besoin editorial de la sous-NC Scenes locales; aucun nouveau tag `scene-locale` n'est necessaire. La requete historique `concerts` exclut deja `scenes-izilife` ainsi que les trois indicateurs Izilife afin de laisser ces petits evenements au WTD Sessions. La nouvelle sous-NC Scenes locales reutilise maintenant exactement ces quatre signaux en inclusion.

### Page et Community

La PageCategory generique `association` existe. `association-musicale` a ete ajoutee a la fin de `021_Next_Improves.sql` comme enfant de `association`, puis appliquee a la BDD locale. `ecole-de-musique` reste un `PlaceType`. Le modele distingue donc l'acteur et son lieu : une association ou un collectif est une Page, tandis qu'une ecole de musique physique est un Place, meme lorsqu'elle est geree juridiquement par une association.

Une Page et un Place representant la meme structure peuvent coexister en etant relies au meme `Partner`. Dans la sous-NC Ecoles, la cible sera Place `ecole-de-musique` plus Page `association-musicale`, avec priorite au Place lorsqu'un site physique correspondant existe et Page en repli lorsqu'il n'existe pas.

Les Community n'appartiennent pas au besoin Sessions defini ici. Elles sont retirees de la cible fonctionnelle de cette intention; elles pourront rester pertinentes pour Sport, Danser et les usages de groupes.

## Cycle des evenements

LocalQuery `event` selectionne uniquement `LocalEvent`. Il ne retourne directement ni `EventSerie` ni `AnnualCelebration`, ce qui correspond au comportement attendu pour WTD.

Un `LocalEvent` peut etre :

- une edition liee a une `EventSerie`;
- une edition liee a une `AnnualCelebration`;
- un parent recurrent;
- une occurrence via `is_another_date_of`;
- un evenement simple.

Le provider filtre les editions encore disponibles par date et heure. L'option `inherit_editorial_from_event_family`, activee pour Sessions, fait aussi heriter les tags, styles musicaux et hobbies portes par `EventSerie`, `AnnualCelebration` ou le parent recurrent. Les objets serie/celebration ne sont toujours pas affiches directement.

## Definition implementee a tester

1. Parent : editions `jam-session`, `scene-ouverte`, `open-mic`; concerts seulement si le lieu porte `bien-pour-concerts` ou si l'evenement est Izilife/partenaire/organisateur/`scenes-izilife`; Experiences musicales en complement.
2. Jams : editions `jam-session`, `scene-ouverte`, `open-mic`.
3. Petits concerts : editions `concert` ou `scene-ouverte` qualifiees par un lieu `bien-pour-concerts` ou un signal local Izilife.
4. Scenes locales : editions `scene-ouverte`, `concert` ou `jam-session` portant un signal Izilife ou le tag `scenes-izilife`, directement ou par heritage.
5. Collectifs : Pages `association-musicale`.
6. Ecoles : Places `ecole-de-musique` et Pages `association-musicale`.

Les six URLs repondent en HTTP 200 sans erreur SQL. La BDD locale contient maintenant les cinq enfants actifs et la PageCategory `association-musicale`. La validation restante est manuelle : qualite des resultats reels, doublons eventuels Page/Place et pertinence de l'ordre avec des donnees musicales fraiches.
