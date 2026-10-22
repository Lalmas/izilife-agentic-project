# Chantier Home et IndependentActions

Notes issues des tests manuels. Elles sont conservees ici sans les traiter pendant la validation de Sessions.

## Intentions et contenus a ajouter ou challenger

- Ajouter ou retrouver `Manger a l'exterieur`.
- Pouvoir exclure certaines propositions selon l'age.
- Matchs.
- Diffusions sportives.
- Verifier si `Plages` manque comme NavigationCategory principale entre staging et production.
- L'IA est tranchee comme intention `Stand-up & humour` ; elle conserve le lien
  vers le WTD large `Comedie`, qui rassemble les spectacles humoristiques.

## Campagne de validation Home

- Continuer a tester et valider toutes les IndependentActions.
- Tester chaque IA et verifier son lien.
- Valider manuellement la composition et l'ordre de `Maintenant`.
- Valider manuellement la composition et l'ordre de `Prochains jours`.
- Refaire la validation lorsque les Events et Spotlights seront assez alimentes pour juger le module.

## Bugs Vecu

- Le modal Vecu est trop large sur mobile, et egalement trop large sur PC.
- Le Vecu non cloture `Ares` est envoye mais le modal reste ouvert.

## Titres a changer

- `Idees pour maintenant ou plus tard`.
- `Pour les prochains jours`.

## Observations temporelles et de classement

### Test vers 17 h 45

- `Un concert en terrasse` arrive apres `Scene locale` et `S'amuser`, alors qu'on est deux heures apres `Boire un verre` : ordre a challenger.
- `Guinguette` devrait etre en position 3 pendant la periode adaptee.
- `Se poser au calme` ne doit pas finir trop bas : avant le coucher du soleil, parcs et lieux publics restent pertinents.
- `Une journee au lac` pour une personne seule parait peu adaptee ; probablement davantage famille.
- `Les meilleures terrasses` est vide et precede pourtant `Spots afterwork`.

### Test vers 6 h 22

- `Sortie velo` est peut-etre remontee a cause du contexte vacances/mercredi ; elle ne devrait pas etre en position 3 apres `Cafe croissant` et `Se poser`.
- `Escape game` est retire du profil solo. Il ne reviendra que lorsqu'un groupe
  public/Meetz disponible pourra etre garanti par la requete.
- Ordre observe dans `Maintenant` : Cafe croissant, Se poser au calme, Sortie velo, Escape game, Expo, Pique-niquer, Faire du sport, Spa et detente.
- `Balade matinale` est disponible a partir de 7 h et conserve la temporality
  stricte de la promenade.

### Prochains jours

- Redondances observees : Escapades, Detente Hotel, Une nuit insolite, Calais, Wissant, Moment de detente, Journee plage, Musee, Cours de danse, Dans l'eau.
- L'enchainement de plusieurs villes est problematique ; a reevaluer avec les Events et Spotlights.
- Clarifier la difference entre `Moment de detente` et `Spa et detente`.
- En ete, `Journee plage` doit remonter.

## Regle de travail

Chaque point sera challenge avec le testeur : constat du comportement, hypothese de classement ou de contenu, correction, nouveau test manuel, puis validation explicite.

---

# Etat reel HB / IA — audit du 13 octobre 2026

## Regles minimales validees pour les HB sensibles

| Bloc | Definition minimale | Etat |
|---|---|---|
| `trendy_places` | Spotlights actifs et eligibles, tous objets supportes (lieu, commerce, evenement, experience). L'importance dans la ville signifie « incontournable », pas « tendance ». | Corrige ; affiche sous le titre **Tendances**. |
| `life_areas` | Lieux structurellement collectifs, ou objet explicitement cure avec `lieu-de-vie-local`. Une place connue ne suffit pas. | Corrige. |
| `solo_experiences` | Objets explicitement qualifies `bien-en-solo`. `is_insolite` n'est pas un signal solo. | Corrige. |
| `kids_activities_mixed` | Meme logique multi-objets stricte que le WTD Pour enfants : signaux enfants/famille, categories enfant, circuits accessibles. | Corrige ; « voir plus » vise `/activites-enfants`. |
| `unusual_activities` | Experience `is_insolite`, ou objet portant un tag explicite `insolite`, `lieu-insolite` ou `activite-insolite`. | Valide ; pas de deduction depuis la rarete ou la nouveaute. |
| `subscriber_promos` | Avantages d'abonnement proches. Les tags du profil courant remontent d'abord, sans supprimer les offres generiques. | Corrige : classement famille/couple/amis/solo/etudiant puis distance. |
| `romantic_places` | Lieux publics explicitement romantiques/date/intimistes. Les restaurants, bars et experiences ont leurs rails dedies. | Valide comme rail etroit ; ne pas en faire un fourre-tout multi-objets. |
| `cozy_cafes` | Cafe/salon de the/coffee-shop avec signal `cosy`, `ambiance-posee` ou `intimiste`. | Corrige. |

## Tous les HB effectivement demandes par profil

Les blocs ci-dessous sont ceux de `get_home_profile_blocks()`. Les blocs forces
`ideas_to_do`, `good_deals` et `subscriber_promos` s'ajoutent sur chaque Home.

- **Solo** : `sortir-nuit`, `trendy_bars`, `party_events`, `drinks_tonight`, `happy_hour`, `tonight_around`, `afterwork_spots`, `solo_experiences`, `local_concerts`, `standup_shows`, `trendy_places`, `best_terraces`, `places_to_play`, `new_places`, `life_areas`, `rainy_day_ideas`, `sunny_day_ideas`, `trendy_restaurants`, `sport_groups`, `dance_groups`, `good_deals`, `cities_to_discover_nearby`, puis les quatre blocs geographiques futurs.
- **Entre amis** : `sortir-nuit`, `party_events`, `trendy_bars`, `tonight_around`, `drinks_tonight`, `happy_hour`, `afterwork_spots`, `ou_drink_and_play`, `local_events`, `bars_terraces`, `places_to_play`, `local_concerts`, `sport_groups`, `dance_groups`, `weekend_events`, `street_food`, `good_deals`, `life_areas`, `unusual_activities`, `cities_to_discover_nearby`, puis les quatre blocs geographiques futurs.
- **Couple** : `romantic_bars`, `romantic_restaurants`, `date_ideas`, `wine_bars`, `romantic_places`, `romantic_walks`, `couple_experiences`, `couple_late_night_experiences`, `cozy_cafes`, `brunch_spots`, `weekend_events`, `sweet_spots`, `detente_couple`, `weekend_for_two`, `must_see`, `unusual_activities`, `cities_to_discover_nearby`, puis les quatre blocs geographiques futurs.
- **Etudiant** : `sortir-nuit`, `student_parties`, `student_bars`, `student_happy_hour`, `tonight_around`, `cheap_eats`, `student_promos`, `study_places`, `sport_groups`, `good_deals`, `street_food`, `life_areas`, `must_see`, `unusual_activities`, `cities_to_discover_nearby`, puis les quatre blocs geographiques futurs.
- **Famille** : `kids_activities_mixed`, `family_walks`, `creative_workshops`, `kids_sports`, `new_places`, `kids_snack`, `kids_restaurants`, `markets`, `sport_activities`, `family_weekend`, `unusual_activities`, `cities_to_discover_nearby`, puis les quatre blocs geographiques futurs.

### Blocs reellement non branches

`international_city_trips`, `major_cities_1h_2h`, `geographic_areas_to_explore`
et `country_international_cities` sont encore des placeholders vides. Ils ne
doivent pas etre presentes comme implementes. Les autres nombreux « manquants »
signales par l'ancien audit etaient des faux positifs : le routeur par defaut
fait volontairement correspondre plusieurs IDs de bloc a un meme builder.

## Audit exhaustif des IndependentActions et de leur destination WTD

### Ancien moteur encore assume

- Manger : `prendre-un-petit-dejeuner`, `dejeuner`, `pause-rapide`, `diner`, `manger-plein-air`.
- Cafe / gouter / boire : `boire-un-cafe`, `manger-une-glace`, `gouter`, `boire-un-verre`, `apero-pique-nique`, `apero-plein-air`.
- Jouer : `jouer`, `jeux-de-societe`, `escape-game`, `parcs-aires-jeux`, `parc-attractions`.

Ces liens sont valides mais restent sur les familles historiques que le planning
a volontairement placees apres les NC prioritaires.

### Nouveau moteur ou branche WTD explicite

- Sorties : `visiter`, `soiree-festive`, `discotheque`, `comedy-club`, `concert-ce-soir`, `petits-concerts-locaux`, `theatre-spectacles`, `soirees-etudiantes`, `voir-un-film`, `sortir-nuit`.
- Flaner / outdoor : `se-balader`, `balade-nocturne`, `se-poser`, `sortie-velo`, `randonnee`, `balade-nature`, `marcher-bord-eau`, `sunset`.
- Detente / sport / danse : `se-detendre`, `spa-detente`, `faire-du-sport`, `cours-danse`.
- Art et culture : `expo`, `musees`.
- Eau et vacances : `journee-plage`, `journee-lac`, `balade-cote-cet-apres-midi`, `apres-midi-plage`, `parc-aquatique`.
- Escapades / dormir : `escapades`, `hotel`, `nuits-insolites`, `city-trip`, `weekend-amoureux`, `grands-parcs`.
- Autres : `bruncher`, `boire-un-verre-en-terrasse`, `aller-en-guinguette`, `rooftop-ce-soir`, `cafe-cosy`, `lieux-a-tester`.

### Liens errones corriges par cet audit

- `se-balader` : `/flaner` (et non `/flaner/balade-nocturne`).
- `balade-nocturne` : `/flaner/balade-nocturne` (et non `/flaner`).
- `parc-aquatique` : `/experiences/experiences-aquatiques` ; le parent reel est `experiences`.
- `lieux-a-tester` : `/nouveaux-lieux` (et non l'ancien `/nouveaux`).
- Les routes GET WTD a un, deux et trois segments sont maintenant explicites ; cela corrige notamment le 404 de `/dormir` avec l'auto-routing desactive.

## Tags consommes pendant ce chantier

Les 28 signaux controles sont :

`parfait-pour-un-date`, `parfait-couple`, `soiree-romantique`, `spot-calme`,
`spot-pour-se-poser`, `ambiance-posee`, `lieu-silencieux`, `cosy`, `retraite`,
`deconnexion`, `detox-digitale`, `soin-visage`, `soin-corps`, `modelage`,
`maquillage`, `naturopathie`, `reflexologie`, `sophrologie`, `bien-avec-enfants`,
`spectacle-enfants`, `parfait-famille-journee`, `super-vue`,
`parfait-pour-une-balade`, `lieu-iconique`, `lieu-de-vie-local`,
`bien-en-solo`, `insolite`, `intimiste`.

Les 11 tags reellement necessaires sont ajoutes dans une section distincte a la fin de
`0212_Tag_Hobby_And_Other.sql`, et nulle part dans `New_Entities` ni dans
`021_Next_Improves.sql` : `lieu-silencieux`, `retraite`, `deconnexion`,
`detox-digitale`, `soin-visage`, `soin-corps`, `modelage`, `maquillage`,
`naturopathie`, `reflexologie`, `sophrologie`.

`cosy` n'est volontairement pas recree comme tag : c'est deja une valeur de
`Atmosphere`, desormais lue comme telle par les moteurs. De meme, les Events
`retraite` utilisent l'`EventCategory` existante ; le tag homonyme ne sert qu'a
la curation des lieux et experiences.
