# Accueil et recherche — contrat des signaux éditoriaux

## Objet

Ce document est destiné au chantier des requêtes de page d'accueil, de
recherche et de suggestion. Les agents enrichissent désormais les Places,
Shops, Events, Experiences et conteneurs événementiels avec davantage de
signaux. Les requêtes doivent les consommer sans refaire une classification à
partir du titre ou de la description.

Les règles essentielles sont les suivantes :

- ne jamais coder les IDs numériques des référentiels ; résoudre leurs
  `string_id` ;
- ne pas afficher les tags internes de curation comme des caractéristiques
  publiques ;
- un signal absent signifie « inconnu », pas « faux » ;
- un tag ou une caractéristique ne remplace pas les contraintes dures : objet
  actif, dates valides, ville, confidentialité, annulation, disponibilité ;
- les séances d'un même objet canonique ne doivent pas multiplier son poids
  éditorial dans les classements.

## 1. Niveaux de données

### 1.1 Nature métier

La nature principale est portée par `ActivityPrincipalCategory`. Elle permet de
rapprocher une activité stable et un événement ponctuel de même nature : sport,
danse, musique, science, jeu, art, artisanat, etc.

Colonnes principales :

| Objet | Colonne |
| --- | --- |
| `LocalEvent` | `principal_activity_category` |
| `Experience` | `principal_activity_category` |
| `Representation` | `principal_activity_category` |
| `EventSerie` | `principal_activity_category` |
| `AnnualCelebration` | `default_principal_activity_category` |

`ActivityPrincipalCategory` répond à « de quoi s'agit-il ? ». Le type répond à
« sous quelle forme ? » : cours, atelier, visite, séance de planétarium,
exposition, etc. Il ne faut pas confondre les deux.

Les référentiels détaillés `Sport`, `Dance`, `MusicStyle` et
`ArtisanTechnique` affinent la nature. Une référence détaillée absente ne doit
pas éliminer un objet qui possède une catégorie principale valable.

### 1.2 Caractéristiques principales

`PrincipalCharacteristics` peut cibler un Place, Shop, Event, Experience,
EventSerie, AnnualCelebration ou Representation selon sa colonne de portée.

Champs utiles pour la recommandation :

- `is_for_children` ;
- `adapted_to_children` ;
- `adapted_to_family` ;
- `adapted_to_family_with_children` ;
- `adapted_for_alone` ;
- `adapted_to_couple` ;
- `adapted_to_groups` ;
- `adapted_to_handicap` ;
- `adapted_to_strollers` ;
- `is_adapted_for_date` ;
- `minimal_age`, `age_start`, `age_end` ;
- les usages du lieu : `can_eat_here`, `can_work`, `have_terrace`, etc.

Attention : certaines colonnes historiques ont des valeurs par défaut
permissives. L'existence d'une ancienne ligne ne constitue pas seule une preuve
éditoriale récente. Pour les nouveaux classements, croiser les champs directs,
les âges, les tags consolidés et les caractéristiques.

### 1.3 Tags

Le référentiel commun est `ShopAndPlaceCharactTag`. Les pivots sont propres à
chaque type : `ShopCharactTag`, `PlaceCharactTag`, `EventCharactTag`,
`ExperienceCharactTag`, `RepresentationCharactTag`,
`EventSerieCharactTag`, `AnnualCelebrationCharactTag`.

Les colonnes du référentiel déterminent l'usage :

- `is_internal_curate=1` : ne pas afficher directement au public ;
- `usable_for_suggestion=1` : utilisable dans la recommandation ;
- `usable_for_filter=1` : utilisable comme filtre ou facette ;
- `is_signal=1` et `signal_weight` : signal pondérable ;
- `tag_types` : types d'objets compatibles.

Toujours joindre le référentiel par `charact_tag_id` puis filtrer par
`string_id`. Ne jamais figer son ID numérique dans le code.

### 1.4 Référentiels éditoriaux

Les agents peuvent aussi alimenter les pivots vers : `Hobby`,
`ObjectOnPublicPlace`, `Occasion`, `AgeCategory`, `Atmosphere`, `MealType`,
`BarType`, `MusicStyle`, `Dance`, `Sport`, `VisitMoment`, `VisitWeather`, etc.

Ces relations servent à expliquer et affiner un résultat. Elles ne doivent pas
remplacer `ActivityPrincipalCategory` lorsqu'elle est disponible.

## 2. Restauration : sur place et style de repas

Les cinq tags suivants sont internes à la curation, mais explicitement
utilisables pour la suggestion et les filtres :

- `consommation-sur-place` ;
- `sans-consommation-sur-place` ;
- `repas-sur-le-pouce` ;
- `moment-repas-a-table` ;
- `restauration-mixte`.

Ils forment deux décisions indépendantes.

| Consommation | Style | Tags |
| --- | --- | --- |
| Sur place | repas posé | `consommation-sur-place`, `moment-repas-a-table` |
| Sur place | rapide | `consommation-sur-place`, `repas-sur-le-pouce` |
| Sur place | deux usages prouvés | `consommation-sur-place`, `restauration-mixte` |
| Emporter uniquement | rapide | `sans-consommation-sur-place`, `repas-sur-le-pouce` |
| Emporter uniquement | indéterminé | `sans-consommation-sur-place` |
| Preuves insuffisantes | indéterminé | aucun tag |

### 2.1 Interprétation dans l'accueil

- « Se poser pour un repas » : exiger `moment-repas-a-table` ou
  `restauration-mixte`. Le simple `can_eat_here=1` ne suffit pas.
- « Manger rapidement » : `repas-sur-le-pouce`.
- « Manger sur place » : `consommation-sur-place`.
- « À emporter » : le tag `sans-consommation-sur-place` permet une sélection
  stricte ; l'existence d'un service de livraison ou d'emporter ne prouve pas
  l'absence de salle.
- `restauration-mixte` signifie que les deux usages sont démontrés. Il ne doit
  pas être transformé en deux fiches.

Priorité future : services structurés explicites > tags consolidés > catégorie
du Shop. Une catégorie `restaurant` ne permet jamais à elle seule de conclure
service à table ou restauration rapide.

## 3. Enfants, parents, familles et couples

### 3.1 Différences à conserver

- `is_for_kids=1` sur Event/Experience : contenu conçu pour les enfants ;
- `accessible_for_kids=1` : enfants acceptés, sans être nécessairement le
  public principal ;
- `is_for_children=1` / `adapted_to_children=1` : signal éditorial enfant ;
- `adapted_to_family=1` : adapté à une famille au sens large ;
- `adapted_to_family_with_children=1` : sortie adaptée à un parent avec
  enfant ;
- `adapted_to_couple=1` : adapté à deux personnes ;
- `is_adapted_for_date=1` : preuve plus précise pour une sortie en amoureux.

Ne pas assimiler « accessible aux enfants » à « activité pour enfants ».

### 3.2 Décisions recommandées

#### Bloc « Pour les enfants »

Condition forte : objet actif et au moins l'une des preuves suivantes :

- champ direct `is_for_kids=1` ;
- caractéristique `is_for_children=1` ;
- caractéristique `adapted_to_children=1` accompagnée d'un âge, d'une
  `AgeCategory` ou d'un tag enfant ;
- catégorie ou source explicitement destinée aux enfants.

#### Bloc « À faire avec les enfants »

Utiliser :

- `adapted_to_family_with_children=1` ; ou
- `accessible_for_kids=1` avec `adapted_to_family=1` ; ou
- tag `kids-friendly` avec une preuve d'âge compatible.

Un contenu peut apparaître dans ce bloc sans être conçu exclusivement pour les
enfants.

#### Bloc « En couple »

Préférer `is_adapted_for_date=1`. À défaut, utiliser
`adapted_to_couple=1` seulement avec un autre signal compatible : ambiance,
occasion, repas à table, visite, bien-être, spectacle, etc. Ne pas utiliser un
ancien booléen isolé comme preuve suffisante.

### 3.3 Âges

Appliquer les contraintes `minimal_age`, `age_start`, `age_end` et les pivots
`PublicAge` après la sélection éditoriale. Une fiche « famille » incompatible
avec l'âge demandé doit être exclue.

## 4. Experiences

Une Experience est une offre stable ou réservable : cours, atelier, visite,
jeu de piste, séance de planétarium, exposition durable, etc. Un Event est une
occurrence datée. Une exposition durable avec des sessions reste donc une
Experience, même si le mot « exposition » est utilisé dans son titre.

Champs utiles :

- `experience_type` : forme de l'expérience ;
- `principal_activity_category` : nature ;
- `is_for_kids`, `accessible_for_kids`, `minimal_age` ;
- durée, prix, accès, réservation et lieu de rendez-vous ;
- `sport_id`, `dance_id`, `music_style_id`, `artisan_technique_id` ;
- caractéristiques, tags, hobbies, objets, occasions et âges associés.

Les créneaux de l'Experience sont portés par `SessionConfiguration` et
`SessionConfigurationContent`. Les tarifs commerciaux proposés par les agents
peuvent être des `ElementAccessPrice` inactifs tant qu'ils ne sont pas validés.

Une Experience active ne doit pas être écartée parce qu'elle n'a pas encore de
SC/SCC ou d'EAP. Ces données améliorent la présentation et la réservation, pas
son identité éditoriale.

## 5. Events et objets canoniques

Les données éditoriales stables appartiennent au conteneur canonique :

- séances d'une `Representation` → lire les tags, médias, caractéristiques,
  activité, sport/danse/musique depuis `Representation` ;
- éditions d'une `EventSerie` → lire depuis `EventSerie` ;
- éditions d'une `AnnualCelebration` → lire depuis `AnnualCelebration` ;
- occurrences d'un Event récurrent → lire depuis le premier Event récurrent ;
- Event avec `is_another_date_of` → lire depuis l'Event pointé ;
- `parent_id` désigne une programmation autonome : le CHILD conserve ses
  propres données et ne doit pas être confondu avec une simple autre date.

Les `LocalEvent` enfants restent nécessaires pour les dates, heures, lieux et
accès. Ils ne doivent pas dupliquer le poids de leur Representation/Serie dans
une sélection éditoriale.

### 5.1 Résolution canonique conceptuelle

Pour une ligne `LocalEvent e` :

1. si `representation_id` est renseigné, le canon éditorial est la
   Representation ;
2. sinon si `event_serie_id` est renseigné, le canon est l'EventSerie ;
3. sinon si `annual_celebration_id` est renseigné, le canon est
   l'AnnualCelebration ;
4. sinon si `is_another_date_of` est renseigné, remonter vers ce LocalEvent ;
5. sinon si l'Event est une occurrence générée d'un récurrent, remonter vers le
   premier Event récurrent ;
6. sinon le LocalEvent est son propre canon.

La déduplication des résultats doit utiliser une clé canonique composée du type
et de l'ID, tout en conservant la prochaine occurrence comme date affichée.

## 6. Algorithme de classement recommandé

### Étape A — contraintes dures

Filtrer d'abord : activité/listabilité selon le type, ville et périmètre,
dates, annulation, confidentialité, disponibilité et exclusions métier.

### Étape B — canon et déduplication

Résoudre l'objet canonique, puis garder la meilleure ou la prochaine occurrence
de chaque canon. Ne pas additionner dix fois les mêmes tags pour dix séances.

### Étape C — compatibilité

Appliquer les contraintes d'âge, public, accessibilité, horaire, prix et
distance. Une incompatibilité dure exclut le résultat.

### Étape D — score éditorial

Ordre conseillé :

1. correspondance `ActivityPrincipalCategory` ;
2. Sport/Dance/MusicStyle/Hobby/Occasion correspondant à la requête ;
3. caractéristiques principales explicitement consolidées ;
4. tags avec `usable_for_suggestion=1`, pondérés par `signal_weight` ;
5. proximité, disponibilité temporelle et fraîcheur ;
6. catégorie générale comme rappel, jamais comme preuve unique d'un usage
   précis.

### Étape E — diversité

Limiter la répétition d'un même canon, lieu, catégorie ou organisateur. La
diversité intervient après la compatibilité, jamais pour réintroduire un objet
incompatible.

## 7. Priorité et contradictions

Priorité générale :

1. donnée structurée explicitement validée ;
2. champ direct de l'objet ;
3. caractéristique principale consolidée ;
4. tag interne de curation appliqué ;
5. relation éditoriale de référentiel ;
6. catégorie générale ;
7. inférence textuelle : interdite dans les requêtes, responsabilité des
   agents.

En cas de contradiction, ne pas choisir silencieusement le signal positif. Par
exemple `sans-consommation-sur-place` contredit `can_eat_here=1` : exclure le
cas des sélections strictes et le faire remonter en audit de données.

## 8. Points à tester dans les requêtes

- un kebab avec quelques tables : sur place + sur le pouce ;
- une friterie uniquement à emporter : sans sur place + sur le pouce ;
- une brasserie : moment repas à table ;
- une Experience conçue pour enfants versus seulement accessible aux enfants ;
- une sortie famille avec enfant ;
- une sortie couple avec et sans preuve `date` ;
- plusieurs séances d'une même Representation : une seule carte canonique ;
- plusieurs dates liées par `is_another_date_of` : une seule identité avec la
  prochaine date ;
- un CHILD avec `parent_id` : carte autonome ;
- une EventSerie et une AnnualCelebration : classification lue sur leur racine ;
- une Experience sans SC/SCC : toujours trouvable si elle est active et
  compatible ;
- un tag interne : utilisé pour le score mais jamais affiché comme libellé FO.

## 9. Évolutions de référentiels

Les annuaires `MusicStyle`, `Dance` et `Sport` doivent encore être enrichis.
Les requêtes doivent donc rester tolérantes à leur absence et toujours pouvoir
retomber sur `ActivityPrincipalCategory`.

Le type Experience `seance-planetarium` existe. Le type générique
`exposition` doit être ajouté séquentiellement au référentiel avant de
reclasser les expositions stables du Forum des Sciences.

