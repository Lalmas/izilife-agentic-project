# Pages publiques des nouveaux objets

Toutes les pages sont fermées par défaut et répondent en 404 tant que leur contenu n'a pas été validé.

```dotenv
PUBLIC_CITY_PAGES_ENABLED=false
PUBLIC_COUNTRY_PAGES_ENABLED=false
PUBLIC_TERRITORY_PAGES_ENABLED=false
PUBLIC_LOCAL_HABIT_PAGES_ENABLED=false
PUBLIC_LOCAL_TIP_PAGES_ENABLED=false
PUBLIC_OUTING_IDEA_PAGES_ENABLED=false
PUBLIC_LOCAL_NEWS_ENABLED=false
```

URLs publiques (auto-routing classique du front, aucune route explicite) :

- `city/page/{city.string_id}`
- `country/page/{iso|nom}`
- `territory/page/{AdministrativeDivision.slug}`
- `localhabit/page/{LocalHabit.string_id|unique_id}`
- `localtip/page/{LocalTip.unique_id}`
- `outingidea/page/{OutingIdea.unique_id}`

Chaque objet conserve son contrôleur et sa méthode `page()` : City, Country et Territory ne partagent pas un contrôleur générique.

Une `EscapadeProposal` affichable est limitée à `CITY`, `ADMINISTRATIVE_DIVISION`, `PLACE` ou `SHOP`. Une division de type `intercommunality` est toujours exclue des escapades, même si une configuration erronée existe en base. `ANNUAL_CELEBRATION` et `EVENT_SERIE` doivent être proposés directement comme événements, sans enveloppe `EscapadeProposal`.

Les catalogues généraux `escapades` et `s-evader` montrent toutes les propositions actives et valides : le profil touristique courant et la météo immédiate ne doivent jamais vider entièrement ces catalogues. Les intentions spécialisées (par exemple `escapades-weekend-amoureux` ou `micro-aventures`) continuent d'appliquer leurs contraintes explicites de profil, météo ou type.

### Signalétique des destinations

Dans la première version, les `EscapadeProposalReason` sélectionnées dans le BO portent la signalétique éditoriale affichée sur les cartes City et AdministrativeDivision (`Mer`, `Plage`, `Montagne`, `Lac`, `Balade`, etc.). Elles déterminent également la variante du titre et de la description. Le libellé technique `Ville` ou `Territoire` n'est pas affiché comme pill.

Cette signalétique est pour le moment déclarative : une mauvaise sélection BO peut donc produire une information géographique fausse. La cible durable est de distinguer :

- les caractéristiques vérifiées portées par City/AdministrativeDivision et les relations spatiales (`is_litoral_city`, `is_mountain_city`, `is_rural_city`, présence ou traversée par une plage, un fleuve, un lac ou un massif) ;
- les raisons d'EscapadeProposal, qui sélectionneront seulement les angles éditoriaux autorisés par ces caractéristiques.

Lorsque cette validation sera branchée, EscapadeProposal ne pourra plus inventer seule une signalétique contradictoire.

### Composition des pages City et AD

Les pages réutilisent les composants existants, sans hero ni bibliothèque de
cards parallèle : en-tête simple, `show_object_header_gallery` avec tous les
médias, signalétiques géographiques, présentation, puis blocs de découverte
issus des builders Home. Les rails temporels de la Home ne sont pas repris et
un bloc vide n'est pas affiché.

La composition de départ est stable : manger, jouer, boire, dormir, cafés et
douceurs, événements, incontournables, expériences, puis selon les données
marchés/producteurs, zones commerçantes et services utiles. L'heure peut adapter
le libellé « manger/dîner », mais elle ne filtre pas les restaurants d'une petite
ville. Les boulangeries ont un poids secondaire dans « Cafés, pâtisseries &
salons de thé ».

Les variantes de profil servent surtout à personnaliser les activités (par
exemple jouer avec les enfants) et certaines expériences. Une variante spécialisée
n'est retenue qu'avec au moins six résultats ; sinon la rubrique générale prend
automatiquement le relais. Le profil enrichit ainsi une ville disposant d'une
offre abondante sans appauvrir une petite ville.

La Home reste centrée sur la position GPS ou la ville configurée par
l'utilisateur. Une page City injecte seulement pendant son rendu les coordonnées
de la ville affichée ; une page AD injecte son périmètre. La session,
`search_filters` et la préférence de localisation ne sont jamais modifiés. Le
profil touristique courant continue de choisir les variantes famille, couple,
solo, étudiant ou touriste.

`locality_build_geographic_context()` fournit le contrat commun City/AD :
`features`, `feature_keys` et `crossings`. `crossings` prépare le futur
raccordement aux relations structurées « bordée/traversée par un lac, un fleuve
ou un canal ». La vérité vient d'abord des champs de la localité
(`is_litoral_city`, `is_mountain_city`, `is_rural_city`, etc.). Les raisons
d'EscapadeProposal sont encore acceptées comme complément éditorial, avec une
source explicitement marquée `escapade_proposal`.

`locality_feature_emoji()` centralise les emojis des cards et des pages pour
reprendre le langage visuel des signalétiques Terrasses.

La météo n'est appelée ni sur les cards de destination ni sur les pages City/AD.
Le fournisseur et `CityWeatherCache` restent disponibles pour les autres moteurs,
mais le chantier localités ne consomme aucun appel WeatherAPI.

`City.is_active` n'est pas un critère d'éligibilité pour les nouvelles pages, les listes territoriales ou les escapades. Ce champ représente le lancement éditorial global d'une ville ; une ville non lancée peut déjà regrouper des lieux et être explicitement ciblée par une proposition. L'ouverture publique de la page City reste pilotée par `PUBLIC_CITY_PAGES_ENABLED` et l'existence d'une proposition reste pilotée par `EscapadeProposal.is_active`.

## Choix du format d'escapade

Une configuration BO correspond à une destination et peut porter plusieurs formats. Le formulaire accepte donc plusieurs choix parmi :

- `micro_escape`
- `half_day_trip`
- `day_trip`
- `weekend_trip`
- `city_trip`

Le format affiché dépend du point d'entrée :

- dans WTD, la définition de l'intention demande le ou les formats admissibles et le résultat LocalQuery transporte le `proposal_id` ainsi que le `proposal_type` effectivement retenu jusqu'à la carte ;
- une IndependentAction exprime une envie et ouvre le parcours WTD : c'est donc WTD qui choisit le format selon l'intention ;
- un HomeBloc dédié demande explicitement son format (`half_day_trips`, `day_trips`, `weekend_city_trips`) ;
- dans le catalogue générique, sans durée demandée, le helper prend le premier format disponible selon l'ordre de présentation `day_trip`, `half_day_trip`, `micro_escape`, `city_trip`, `weekend_trip`.

Une destination peut donc conserver une seule configuration multiformat. L'index simple `(scope_level, scope_id)` permet également plusieurs configurations lorsque des périodes, profils ou contextes éditoriaux distincts le justifient.

Les poids de raisons ne font pas partie du pilotage actuel : les raisons sélectionnées servent de contenu éditorial, sans classement administré par poids.

## Circuits et road-trips

Un `Circuit` est un parcours local tracé, touristique ou sportif (marche, course, vélo, etc.). Ce n'est jamais un road-trip. Les circuits restent proposés dans les intentions `Balades` et `Outdoor`.

Les road-trips sont entièrement hors périmètre pour le moment : aucun type d'EscapadeProposal, aucun provider, aucune intention WTD et aucun lien avec `Circuit` ou le futur objet d'itinéraire. La NavigationCategory historique `roadtrips-et-circuits`, redondante et ambiguë, est désactivée.

## Mise en navigation

City, Country, Territory, LocalHabit, LocalTip et OutingIdea utilisent la pile de navigation des fiches publiques. Leur activation reste indépendante grâce aux variables d'environnement ci-dessus.
