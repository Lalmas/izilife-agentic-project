# Inventaire des intentions NavigationCategory

Source de verite structurelle : `izilife-admin/statics/izilife_new_version/01_navigation.sql`. 
etat de lecture : audit, pas validation metier. La presence d'un `case` WTD ne signifie pas que les sources, filtres, donnees et rendus sont valides.

`NavigationSubCategory` constitue actuellement un vocabulaire de filtres
reutilisables. Les ecrans choisissent les filtres pertinents avec
`Whattodo_model::getNavigationSubCategories([...])` puis chargent leur contenu
depuis `navigationsubcategorytab_helper.php`. L'absence de lignes dans
`NavigationSubCategoryContent` ne signifie donc pas que ces filtres sont
orphelins ; cette table de liaison n'est pas la source effective du branchement
historique. Leur maintien ou leur migration sera challenge categorie par
categorie, sans les traiter comme des routes NC autonomes.

## Legende

- `WTD explicite` : un `case` existe dans le nouveau builder de `Whattodo.php`.
- `Parent dynamique` : le parent est admis par le nouveau routage dynamique.
- `A tracer` : aucun `case` explicite detecte dans le nouveau builder ; un ancien circuit ou un autre branchement peut neanmoins exister.
- `Ajout tardif SQL` : ajoute par la seconde section SQL, actuellement avec `is_active = 0` dans le script.
- `A retirer de NC` : ne releve pas de l'ontologie des intentions.

## Hierarchie complete

### Manger (`manger`) — WTD explicite

- Cafe Croissant (`petit-dejeuner`) — A tracer
- Dejeuner (`dejeuner`) — A tracer
- Dener (`diner`) — A tracer
- Manger vite (`manger-vite`) — WTD explicite
- Sandwichs (`sandwichs`) — A tracer
- Street & Fast Food (`street-fast-foods`) — A tracer
- Restaurants (`restaurants`) — A tracer
- Food-trucks (`food-trucks`) — A tracer
- Gastronomie (`gastronomie`) — A tracer
- Manger pas cher (`manger-pas-cher`) — A tracer
- Manger en plein air (`manger-plein-air`) — A tracer

### Bruncher (`bruncher`) — WTD explicite

- Aucun enfant declare.

### Goeter (`gouter`) — A tracer

- Aucun enfant declare.

### Boire (`boire`) — WTD explicite

- En terrasse (`en-terrasse`) — A tracer
- Apero (`aperos`) — A tracer
- Boire & Jouer (`boire-et-jouer`) — A tracer
- Apero plein air (`apero-plein-air`) — A tracer
- Apero pique-nique (`apero-pique-nique`) — A tracer

### Cafe, The (`cafe-the`) — A tracer

- Cafes cosy (`cafes-cosy`) — WTD explicite

### Balades (`balades`) — WTD explicite

- En ville (`balades-en-ville`) — WTD explicite
- Culturelles (`balades-culturelles`) — WTD explicite
- Nature (`balades-nature`) — WTD explicite
- Au bord de l'eau (`balades-au-bord-de-l-eau`) — WTD explicite

### Sortir (`sortir`) — WTD explicite

- Art & Culture (`sorties-culturelles-et-artistiques`) — WTD explicite
- Cuisine (`sorties-autour-de-la-cuisine`) — WTD explicite
- Boissons (`sorties-autour-des-boissons`) — WTD explicite
- Cinema (`cinema`) — WTD explicite
- Casinos (`casinos-et-club-de-jeux`) — WTD explicite
- Spectacles (`spectacles`) — WTD explicite
- Concerts (`concerts`) — WTD explicite
- Festivals (`festivals`) — WTD explicite
- Theatre (`theatres`) — WTD explicite
- Sortir la nuit (`sortir-nuit`) — WTD explicite

Le WTD Cinema couvre actuellement les cinemas physiques, les Events de
projection/cinema et les Experiences qualifiees cinema/film. La table
`MovieDiffusion` existe dans le schema catalogue, mais son provider LocalQuery
est volontairement reporte a un chantier ulterieur : les seances deviendront
alors une quatrieme source sans remplacer les trois sources actuelles.

### Jouer (`jouer`) — A tracer

- Bars — jeux & Cafes ludiques (`bars-a-jeux-et-cafes-ludiques`) — A tracer
- Flechettes, billard, baby-foot (`flechettes-billard-babyfoot`) — A tracer
- Laser Game & Paintball (`laser-game-paintball`) — A tracer
- Bowling (`bowlings`) — A tracer
- Arcade & Realite virtuelle (`arcade-et-vr`) — A tracer
- Escape games (`escape-games`) — A tracer
- Aires de jeux & ludotheques (`aires-de-jeux`) — A tracer
- Karting & simulateurs (`karting-simulateurs`) — A tracer
- Parcs deattractions (`parcs-dattractions`) — A tracer
- `skateparks-et-trampolines` retire : melangeait deux intentions et son ancien
  moteur renvoyait presque tous les loisirs indoor.

### S'evader (`s-evader`) — WTD explicite

- Escapades week-end (`escapades-weekend`) — WTD explicite
- Micro-aventures (`micro-aventures`) — WTD explicite
- Lieux insolites (`lieux-insolites`) — WTD explicite
- En pleine nature (`en-pleine-nature`) — WTD explicite
- Sejours bien-etre (`sejour-bien-etre`) — WTD explicite
- `roadtrips-et-circuits` retire : doublon de `circuits` et
  `outdoor-circuits`, sans moteur propre.
- Retraites & silence (`retraites-et-silence`) — WTD explicite

### Travailler (`travailler`) — actif, moteur historique

- Aucun enfant declare.

### Sport (`sport`) — WTD explicite

- Diffusions sportives (`diffusions-sportives`) — WTD explicite
- Communautes & Groupes (`sport-communautes`) — WTD explicite
- Clubs, dojos, salles (`sport-clubs-dojos`) — WTD explicite
- evenements (`sport-evenements-niches`) — WTD explicite
- Entraenements (`sport-entrainements`) — WTD explicite
- `sport-disciplines` retire : les disciplines restent un filtre transversal
  de Sport, pas une destination WTD.
- equipements (`sport-equipements`) — WTD explicite
- Running & Rando (`sport-running-rando`) — WTD explicite
- Fitness & Cross training (`sport-fitness-cross-training`) — WTD explicite
- Velo (`sport-velo`) — WTD explicite
- Sports de raquette (`sport-raquette`) — WTD explicite
- Sports de combat (`sport-combat`) — WTD explicite
- Escalade & Accrobranche (`sport-escalade-accrobranche`) — WTD explicite

### Danser (`danser`) — WTD explicite

- Communautes & groupes (`danse-communautes`) — WTD explicite
- ecoles & clubs (`danse-ecoles-clubs`) — WTD explicite
- evenements (`danse-evenements-niches`) — WTD explicite

### Se detendre (`se-detendre`) — WTD explicite

- Spas detente (`se-detendre-spas-detente`) — WTD explicite
- Hammams & saunas (`se-detendre-hammams-saunas`) — WTD explicite
- Massages relax (`se-detendre-massages-relax`) — WTD explicite
- Yoga & slow (`se-detendre-yoga-doux`) — WTD explicite
- Lieux calmes (`se-detendre-lieux-calmes`) — WTD explicite
- Journee deconnexion (`se-detendre-journee-detox`) — WTD explicite, inactive tant que les signaux editoriaux ne sont pas alimentes

### Soins & Beaute (`prendre-soin-de-soi`) — WTD explicite

- Hygiene & Beaute (`hygiene-et-beaute`) — WTD explicite
- Spas (`spas-hammams-et-saunas`) — WTD explicite
- Massages (`massages`) — WTD explicite
- Meditation (`meditation`) — WTD explicite
- Coiffure (`coiffure`) — WTD explicite
- Barbers (`barbers`) — WTD explicite
- Onglerie (`onglerie`) — WTD explicite
- Instituts (`instituts-esthetique`) — WTD explicite
- Soins visage (`soins-visage`) — WTD explicite, curation `soin-visage` requise
- Soins corps (`soins-corps`) — WTD explicite, curation `soin-corps` ou `modelage` requise
- epilation (`epilation`) — WTD explicite
- Maquillage (`maquillage`) — WTD explicite, categorie inactive
- Medecines douces (`medecines-douces`) — WTD explicite, categorie inactive

### Dormir (`dormir`) — WTD explicite

- Hotels (`hotels`) — WTD explicite, source `PlaceType` uniquement : `hotel`, `residence-hoteliere`
- Chambres d'hotes (`chambre-dhotes`) — WTD explicite, source `PlaceType` uniquement : `chambre-hotes`
- Gites (`gites`) — WTD explicite, source `PlaceType` uniquement : `gite`
- Campings (`campings`) — WTD explicite, source `PlaceType` uniquement : `camping`
- Insolites (`logements-insolites`) — WTD explicite et actif : types de lieux
  `hebergement-insolite`, `cabane`, `bulle`, `dome`, `yourte`, `roulotte`,
  `tiny-house`, `lodge`, avec repli strict sur les lieux `is_for_sleep`
  portant le tag structure `insolite`. Les Experiences simplement marquees
  `is_insolite` sont exclues, car ce signal couvre aussi des activites sans
  hebergement.

Les six routes Dormir ont ete testees en HTTP 200 sans erreur applicative le
4 octobre 2026. La base locale ne contient toutefois encore aucune fiche
`Place` rattachee a ces types d'hebergement : le branchement est operationnel,
mais les resultats dependront de la curation/import des lieux.

### Experiences (`experiences`) — A tracer

- Artistiques (`experiences-artistiques`) — A tracer
- Culturelles (`experiences-culturelles`) — A tracer
- Urbaines (`experiences-urbaines`) — A tracer
- Nature (`experiences-en-nature`) — A tracer
- Aquatiques (`experiences-aquatiques`) — A tracer
- Aeriennes (`experiences-aeriennes`) — A tracer
- Sportives (`experiences-sportives`) — A tracer
- Neige (`experiences-avec-neige`) — A tracer
- Pilotage (`experiences-de-pilotage`) — A tracer

### evenements (`evenements`) — A tracer

- Festifs (`evenements-festifs`) — A tracer
- Culturels (`evenements-culturels`) — A tracer
- etudiants (`soirees-etudiantes`) — A tracer
- Cinema (`evenements-cinema`) — A tracer
- Theetre (`theatre`) — WTD explicite
- Humour & Comedy clubs (`humour-et-comedy-clubs`) — WTD explicite
- Spectacles (`evenements-spectacles`) — A tracer
- Mode (`evenements-mode`) — A tracer
- Sportifs (`evenements-sportifs`) — A tracer
- Alimentaires (`evenements-alimentaires`) — A tracer
- Rencontres (`evenements-de-rencontres`) — A tracer
- Braderies & Brocantes (`evenements-marches-braderies-brocantes`) — A tracer
- Autres (`autres-evenements`) — A tracer

### Marches (`marches`) — WTD explicite

- Aucun enfant declare.

### Tendances (`spotlights`) — WTD explicite

- En bord deeau (`spotlight-en-bord-deau`) — WTD explicite
- Rooftops (`spotlight-rooftops`) — WTD explicite
- Romantique (`spotlight-romantique`) — WTD explicite
- Sunset (`spotlight-sunset`) — WTD explicite
- Nouveaux (`spotlight-nouveaux`) — WTD explicite
- Terrasses (`spotlight-terrasses`) — WTD explicite
- Secrets (`spotlight-secrets`) — WTD explicite
- En famille (`spotlight-famille`) — WTD explicite

### Nouveaux (`nouveaux-lieux`) — WTD explicite

- Aucun enfant declare.

### Izilife + (`izilife-plus`) — WTD explicite

- Aucun enfant declare.

### Art (`art`) — WTD explicite

- Expositions (`expositions`) — WTD explicite : expositions, vernissages et événements Art & Culture
- Musees & Galeries (`art-musees-galeries`) — WTD explicite : lieux culturels et galeries
- Street-art (`art-street-art`) — WTD explicite : œuvres, événements et expériences street-art
- Ateliers (`art-ateliers`) — WTD explicite : ateliers événementiels, expériences de type atelier/cours/stage qualifiées par un thème artistique, et ateliers d’art
- Boutiques d’art & createurs (`art-artisans`) — WTD explicite : galeries-boutiques, ateliers d’art et créateurs

### Escapades (`escapades`) — WTD explicite

- City trips (`escapades-city-trip`) — WTD explicite
- Week-end en amoureux (`escapades-weekend-amoureux`) — WTD explicite

### Deals (`deals`) — WTD explicite

- Izilife+ (`deals-izilife-plus`) — WTD explicite
- Codes promos (`codes-promos`) — route historique conservée, retirée du tiroir Deals
- Happy hour (`deals-happy-hour`) — route compatible conservée, retirée du tiroir au profit du WTD spécialisé `happy-hour`
- Promo etudiante (`promo-etudiante`) — WTD explicite

### Courses (`courses`) — WTD explicite

- Aucun enfant `NavigationCategory`. Le filtre historique Hypermarches et
  supermarches reste une `NavigationSubCategory`; ne pas creer un doublon NC.

- Aucun enfant declare.

### Portefeuille (`wallet`) — A tracer

- Aucun enfant declare.

### Payer (`payer`) — A tracer

- Aucun enfant declare.

### Transfert (`transfert`) — A tracer

- Aucun enfant declare.

### Jeux (`jeux`) — A tracer

- Aucun enfant declare.

### Happy hour (`happy-hour`) — WTD explicite

- Aucun enfant declare.

### Social (`rencontres`) — retire

L'ancien brouillon renvoyait des parcs d'attractions et des trampolines. Le
parcours social reel reste MeetZ et ne doit pas etre duplique comme intention
WTD.

### Idees date (`sorties-premier-rendez-vous`) — WTD explicite

- Aucun enfant declare.

### Pour enfants (`activites-enfants`) — A tracer

- Aucun enfant declare.

### Jobs (`jobs`) — A tracer

- Aucun enfant declare.

### Au quotidien (`au-quotidien`) — A tracer

- Toilettes (`toilettes`) — A tracer
- Se garer (`se-garer`) — A tracer
- Station service (`station-services`) — A tracer
- Distributeurs de billets (`distributeurs-de-billets`) — A tracer
- Transports (`transports`) — A tracer

### equipements (`equipements`) — A tracer

- Aucun enfant declare.

### Shopping (`shopping`) — WTD explicite

- Mode & Accessoires (`shopping-mode-accessoires`) — A tracer
- Beaute (`shopping-beaute`) — A tracer
- Maison & Deco (`shopping-maison-deco`) — A tracer
- Librairies (`shopping-librairies`) — A tracer
- Cadeaux & Idees originales (`shopping-cadeaux`) — A tracer

### Chiner (`chiner`) — WTD explicite

- Brocantes & vide-greniers (`brocantes-et-vide-greniers`) — WTD explicite
- Marches aux puces (`marches-aux-puces`) — WTD explicite
- Friperies & vintage (`friperies-et-vintage`) — WTD explicite
- Ressourceries (`ressourceries`) — WTD explicite
- Artisanat local (`artisanat-local`) — WTD explicite
- Salons & foires (`salons-et-foires`) — WTD explicite

### Flener (`flaner`) — WTD explicite

- Espaces verts (`espaces-verts`) — WTD explicite
- Places & Lieux vivants (`places-et-lieux-vivants`) — WTD explicite
- Bords de leeau (`flaner-au-bord-de-leau`) — WTD explicite
- Marches & Brocantes (`marches-et-brocantes`) — WTD explicite
- Cours cachees & squares (`cours-cachees-et-squares`) — WTD explicite
- Terrasses tranquilles (`terrasses-tranquilles`) — WTD explicite
- Centres & Zones commerciaux agreables (`centres-et-zones-commerciaux`) — WTD explicite
- Flaner en ville (`flaner-en-villes`) — WTD explicite
- Balade nocturne (`balade-nocturne`) — WTD explicite et actif : places, rues,
  quartiers, zones pietonnes, quais et canaux urbains ; aucun parc, jardin,
  foret, plage ou lac.

### Aider (`aider`) — WTD explicite

- Aucun enfant declare.

### Comedie (`comedie`) — WTD explicite

- Aucun enfant declare.

### Sessions (`live-sessions`) — WTD explicite

- Jams (`live-sessions-jams`) — WTD explicite
- Petits concerts (`live-sessions-petits-concerts`) — WTD explicite
- Scenes locales izilife (`live-sessions-scenes-locales`) — WTD explicite
- Collectifs (`live-sessions-collectifs`) — WTD explicite
- ecoles (`live-sessions-ecoles`) — WTD explicite
- Petits concerts locaux (`petits-concerts-locaux`) — A tracer, Ajout tardif SQL

### Terrasses (`terrasses`) — WTD explicite

- Rooftops (`rooftops`) — WTD explicite
- Guinguettes (`guinguettes`) — WTD explicite

### Activites nautiques (`activites-nautiques`) — WTD explicite

- Aucun enfant declare.

### Plages (`plages`) — WTD explicite

- Aucun enfant declare.

### Sunset (`sunset`) — WTD explicite

- Aucun enfant declare.

### etudiants (`etudiants`) — WTD explicite

- Soirees (`etudiants-soirees`) — WTD explicite
- Offres etudiantes (`etudiants-offres`) — WTD explicite
- Lieux adaptes (`etudiants-lieux`) — WTD explicite
- Events campus (`etudiants-campus`) — WTD explicite

### Se rafraechir (`se-rafraichir`) — WTD explicite

- Parcs & ombre (`parcs-et-ombres`) — WTD explicite
- Lieux climatises (`lieux-climatises`) — WTD explicite
- Piscines & baignade (`piscines-et-baignade`) — WTD explicite
- Terrasses fraeches (`terrasses-fraiches`) — WTD explicite
- Glaces & boissons fraeches (`glaces-et-boissons-fraiches`) — WTD explicite
- Brumisateurs & fontaines (`brumisateurs-et-fontaines`) — WTD explicite
- Activites indoor (`activites-indoor`) — WTD explicite
- Avec enfants (`plan-canicule-enfants`) — WTD explicite

### Pique-niquer (`pique-niquer`) — WTD explicite

- Aucun enfant declare.

### Outdoor (`outdoor`) — WTD explicite

- — pied (`outdoor-a-pied`) — WTD explicite
- Running (`outdoor-running`) — WTD explicite
- — velo (`outdoor-velo`) — WTD explicite
- Spots (`outdoor-spots`) — WTD explicite
- Circuits (`outdoor-circuits`) — WTD explicite

### Mis en avant (`mis-en-avant`) — WTD explicite

- Aucun enfant declare.

### Events Izilife (`events-izilife`) — WTD explicite

- Aucun enfant declare.

### Series Izilife (`izilife-event-series`) — WTD explicite

- Aucun enfant declare.

### Coups de ceur (`coups-de-coeur`) — WTD explicite

- Aucun enfant declare.

### Grands RDV annuels (`grands-rdv-annuels`) — WTD explicite

- Aucun enfant declare.

### Vacances (`vacances`) — WTD explicite, Ajout tardif SQL

- Vacances avec enfants (`vacances-avec-enfants`) — WTD explicite, Ajout tardif SQL
- Escapades vacances (`vacances-escapades`) — WTD explicite, Ajout tardif SQL
- Parcs et attractions (`vacances-parcs-attractions`) — WTD explicite, Ajout tardif SQL
- Journee plage (`vacances-journee-plage`) — WTD explicite, Ajout tardif SQL
- Experiences vacances (`vacances-experiences`) — WTD explicite, Ajout tardif SQL
- Lieux frais (`vacances-lieux-frais`) — WTD explicite, Ajout tardif SQL
- Journee nature (`vacances-journee-nature`) — WTD explicite, Ajout tardif SQL

## Corrections structurelles appliquees

- `planning-opportunity` a ete retire de `01_navigation.sql`, avec tous ses enfants `planning-*`. Une opportunite de planning est une temporalite/un signal de presentation, pas une NavigationCategory.

## Regle de cleture proposee

Une grande intention n'est `validee` qu'apres contrele des six niveaux : hierarchie NC, route, definition WTD, providers LocalQuery, correspondance reelle avec la BDD, puis rendu/resultats sur donnees reelles. IA et HomeBloc sont contreles comme des entrees vers la meme intention, sans imposer qu'ils aient exactement la meme composition editoriale.

## État réel du chantier au 30/09/2026

- **Sport** : implémentation et cadrage traités.
- **Danser** : implémentation et cadrage traités.
- **Sessions** : implémentation technique terminée ; validation fonctionnelle
  manuelle produit encore à faire sur des données musicales fraîches. Voir
  `docs/wtd_sessions_audit.md`.
- **Idées date** : implémentation, Activity Engine, présentation éditoriale et
  tests de cibles terminés. Voir
  `app/Libraries/LocalQuery/ACTIVITY_ENGINE.md`.
- **Flâner** : premier branchement générique de l'Activity Engine ajouté et
  testé ; ce travail ne remplace pas encore une validation métier complète de
  toute la famille Flâner.
- **Marchés** : définition LocalQuery dédiée validée (marchés et halles
  permanents, éditions de marchés, sans brocantes ni vide-greniers).
- **Pour enfants** : définition multi-source dédiée en place avec signaux
  familiaux forts et temporalité des événements.
- **Art** : définition multi-source en place ; sa validation produit détaillée
  reste distincte de l'implémentation technique.
- **Comédie** : définition recentrée sur les Events de stand-up, spectacles
  comiques et improvisation. `comedy-club` est un Hobby d'Event ou de sa
  famille, jamais un type de lieu public.
- **Nouveaux lieux** : définition technique en place, triée par
  `is_new_in_city` puis `opening_date` décroissante.

## File de validation métier restante

1. Validation sur donnees reelles de Sortir et de chacun de ses enfants.
2. Validation sur donnees reelles de Se detendre ; alimenter les signaux de
   deconnexion avant d'activer `se-detendre-journee-detox`.
3. Validation sur donnees reelles de Soins & Beaute ; les soins visage/corps
   dependent volontairement de leur curation dediee.
4. Revoir les sous-categories historiques de Courses.
5. Recurer les hebergements existants dans les nouveaux `PlaceType` ; la
   taxonomie et le WTD `logements-insolites` sont actifs, mais la base locale
   ne contient encore aucun lieu correctement classe. `Les Nids de Chlorofil`
   est actuellement un Shop `accrobranche` et son Experience est classee
   `degustation` : ne pas la faire remonter par recherche textuelle.
6. Concevoir les signaux nocturnes avant d'activer `balade-nocturne`.
