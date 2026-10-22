# Brief de reprise — WTD et Activity Engine

## État mis à jour au 4 octobre 2026

Le chantier **Idées date** est terminé. Le prochain travail peut reprendre sur
un autre WTD sans rouvrir sa conception.

Marchés et Pour enfants disposent déjà de leurs définitions dédiées. Comédie
est recentré sur les éditions Event (`stand-up-et-one-man-show`,
`spectacle-comedie`, `improvisation`) et accepte le Hobby `comedy-club` porté
par l'Event ou sa famille ; aucun faux lieu « Comedy club » n'est créé.
Nouveaux lieux est déjà filtré par date d'ouverture et trié des ouvertures les
plus récentes vers les plus anciennes.

Art possède cinq parcours explicites : expositions/vernissages, musées et
galeries, street-art, ateliers, puis boutiques d’art et créateurs. Le parent
agrège Places, Events, Experiences et Shops. Musique inclut également les
Events `release-party` dans son moteur actuel.

Une Experience n'entre dans Art que si son activité principale ou un thème
secondaire est explicitement artistique (`art`, `artisanat`, `sculpture`,
`peinture`, `dessin`, `street-art`, `calligraphie`, `photographie`). Son type
seul (`visite-guidee`, `atelier`, `cours`, `stage`) ne suffit jamais. Les thèmes
génériques `culture` et `architecture` ne constituent pas une preuve Art.

Dans le tiroir du parent Deals, seuls `deals-izilife-plus` et
`promo-etudiante` restent proposés. `codes-promos` est une ancienne source
externe ; Happy hour garde son WTD spécialisé au lieu de doubler l’intention
dans Deals. Les routes historiques restent compatibles.

La documentation de référence détaillée est
`app/Libraries/LocalQuery/ACTIVITY_ENGINE.md`.

## Modèle retenu

- `GOOD_FOR` / « Parfait pour » qualifie éditorialement une cible et contribue
  à son éligibilité ou son score. Ce n'est jamais une activité.
- `TargetActivityProposal` décrit une proposition concrète sur une cible : une
  à trois `IndependentAction` ordonnées, un titre et une description propres.
- Une proposition peut appartenir à une `LittleActivityOccasion` (`date`,
  `en-couple`...) ou être globale avec `little_activity_occasion_id = NULL`.
- Avec une occasion demandée, le moteur filtre strictement dessus. Sans
  occasion, il examine toutes les propositions puis les classe selon
  `requested_actions`.
- La meilleure proposition est déterminée par pertinence, pas simplement par
  l'ordre de création.

## Présentations

- `editorial` : présentation contextuelle homogène pour tout le rail.
- `suggestion` : la proposition gagnante remplace uniquement le titre sur
  l'image ; la carte standard et tous ses contenus restent intacts.
- `none` : moteur utilisé sans modification visuelle.
- Les rendus spécialisés (`BRUNCH`, `TOILET`, etc.) restent prioritaires.

En mode `suggestion`, l'activité principale n'est pas répétée dans le modal.
Le bouton **Voir d’autres activités** est au pied de la carte, après les
contenus standards, et ouvre seulement les alternatives.

## WTD Idées date — terminé

- Activity Engine activé en mode `editorial`.
- Occasions : `date` et `en-couple`.
- Éligibilité forte : tags directs prévus, raison Spotlight
  `GOOD_FOR/LITTLE_ACTIVITY_OCCASION`, ou proposition compatible.
- Les signaux faibles romantiques ne suffisent pas seuls.
- Cas validés : Kok Piraat, La Luck, Dream Away Lille, Canal de Seclin.
- Une destination `perfect_for` ne rend pas automatiquement la cible Tendance.

## WTD Flâner — premier test générique

- Activity Engine activé en mode `suggestion`.
- Aucune occasion sociale imposée.
- Pas d'injection de cibles configurées : seules les cartes organiques du WTD
  sont enrichies.
- Actions recherchées : `se-poser`, `se-balader`, `pique-niquer`,
  `apero-pique-nique`, `sortie-velo`.
- Parc de la Drève : Parfait pour / Hobby / Se poser, destination
  `perfect_for`, proposition globale « Se poser et pique-niquer au Parc de la
  Drève ».
- Canal de Seclin : proposition globale « Flâner et pique-niquer au bord du
  Canal de Seclin » ; ses propositions Date restent aussi classables dans un
  appel générique.

## Règle pour le prochain WTD

Avant activation, choisir explicitement :

1. rail éditorial homogène ou cartes standards enrichies ;
2. occasion précise ou recherche générique par actions ;
3. injection ou non des cibles uniquement configurées ;
4. liste de `requested_actions` et données de test ;
5. comportement attendu des rendus spécialisés déjà présents.

Tester d'abord deux ou trois cibles, dont une sans proposition, une avec une
proposition et une avec plusieurs alternatives.
