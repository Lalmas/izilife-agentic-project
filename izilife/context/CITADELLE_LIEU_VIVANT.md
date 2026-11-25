# Parc de la Citadelle — lieu vivant de référence

## Décision de modélisation

Le Parc de la Citadelle est un `PLACE` conteneur et un cas de référence pour les
lieux vivants iziLife. Sa richesse ne doit pas être aplatie dans une seule
description. Elle se construit avec :

- les lieux et commerces réellement autonomes situés dans le parc ;
- les équipements physiques du parc ;
- les circuits et leurs étapes ;
- la faune observable ;
- les associations, cours, expériences et événements qui y vivent ;
- les informations pratiques et saisonnières, sans écraser les contenus déjà
  validés.

La cible historique identifiée dans le SQL est `PLACE/parc-de-la-citadelle`.
La fiche `PLACE/la-citadelle-de-lille` désigne la Citadelle fortifiée et ne doit
pas être confondue avec le parc.

## Circuit officiel préparé

La page officielle « Incontournables du patrimoine » expose des données
structurées : identifiant source `658`, durée 35 minutes, distance affichée
4 km, tracé GeoJSON officiel et 12 points d'intérêt ordonnés avec coordonnées,
textes et images. Le GeoJSON indique toutefois `Longueur_metres=1587,8538` : le
paquet reste `needs_review` jusqu'au choix de la distance métier à conserver.

Ces douze points sont des `CircuitStep`. Ils ne deviennent pas automatiquement
douze `Equipment`. La règle est :

- point purement patrimonial ou point d'observation : `manual_point` ;
- fiche iziLife autonome déjà existante : rattachement `place` ou `shop` ;
- équipement : seulement si une ressource physique réutilisable est réellement
  décrite et que sa catégorie existe ;
- œuvre : `art_piece` si elle est effectivement modélisée comme telle.

Dans le paquet actuel, Quartier Libre est rattaché au `SHOP/lequartierlibre`.
Les onze autres points restent des `manual_point` pour éviter les faux objets.

Fichiers :

- bundle du site : `scripts/izilife/circuits/citadelle/citadelle_bundle.json` ;
- équipement sportif : `scripts/izilife/circuits/citadelle/citadelle_equipment_package.json` ;
- paquet : `scripts/izilife/circuits/citadelle/citadelle_package.json` ;
- tracé : `scripts/izilife/circuits/citadelle/incontournables_du_patrimoine.geojson` ;
- moteur : `scripts/izilife/circuits/site_circuit_package.py` ;
- lanceur commun : `scripts/izilife/site_package.py`.

Commandes sans écriture :

```powershell
python scripts/izilife/site_package.py validate --file scripts/izilife/circuits/citadelle/citadelle_package.json
python scripts/izilife/site_package.py plan --file scripts/izilife/circuits/citadelle/citadelle_package.json
python scripts/izilife/site_package.py plan --file scripts/izilife/circuits/citadelle/citadelle_bundle.json
```

Une soumission exige `--env` et `--confirm-write`. Elle crée d'abord une demande
de validation BO ; elle ne publie pas automatiquement le circuit.

## Faune : référentiel proposé, non injecté

La table `Animal` actuelle est plate et mélange espèces précises et libellés
génériques. Il serait contre-productif d'y copier toute la liste naturaliste.
La proposition est hybride : conserver quelques familles utiles à la découverte
et ajouter seulement des espèces reconnaissables ou emblématiques.

Le paquet contient 19 propositions `pending` issues de la page officielle. Le
moteur circuit ne les écrit pas. Avant ajout SQL et association à la Place, il
faut trancher la liste finale et, si nécessaire, l'évolution hiérarchique du
référentiel.

La cible recommandée reste un référentiel hybride : les familles utiles à la
recherche (`oiseaux`, `chauves-souris`, `grenouilles`, etc.) et seulement les
espèces réellement reconnaissables ou emblématiques. Une copie exhaustive de
chaque espèce dans la table plate actuelle produirait surtout du bruit. Il ne
faut pas non plus rattacher simultanément une famille et toutes ses espèces tant
que `Animal` ne possède pas de hiérarchie explicite.

## Mobilier sportif

La page officielle confirme un ensemble de six modules sur la plaine
Grimonprez. Le référentiel existant est `EquipmentCategory/cage-street-workout`.
Le paquet les modélise comme **un Equipment avec six EquipmentInstance**, pas
comme six fiches autonomes :

- double cardio jambes ;
- double cardio et musculaire jambes ;
- double fessiers dorsaux ;
- double abdominaux dorsaux ;
- double bras pectoraux ;
- double bras.

Le paquet reste `needs_review` parce que la page donne la zone (« plaine
Grimonprez »), mais aucune coordonnée précise. Il ne doit pas hériter en silence
du point central du parc. Une fois le point validé, le passage à `approved`
permettra l'upsert idempotent de l'équipement et de ses six instances.

## Autres contenus repérés

- les boucles de 1, 2, 3, 4, 5 et 7,5 km sont des `Circuit`, pas des
  `Equipment` ;
- les parcours d'orientation sont également des `Circuit`. Les 60 balises sont
  un dispositif commun ; elles ne doivent pas devenir 60 fiches sans besoin
  d'usage ou de maintenance clairement identifié ;
- les activités nautiques et l'accrobranche sont portés par des opérateurs ou
  lieux autonomes. Ils pourront être liés au parc, mais ne doivent pas être
  transformés automatiquement en équipements possédés par le parc.

## Séparation collecte / import

- `validate` et `plan` ne font aucun appel externe ;
- le GeoJSON collecté est conservé localement avec son URL source ;
- le paquet utilise les `string_id` des référentiels, jamais les IDs d'un
  environnement ;
- l'import BO résout les références et crée le circuit en brouillon ;
- le `circuit_string_id` stable empêche une seconde création identique ;
- aucun agent ni aucune écriture production n'est lancé par cette préparation.

## Suite du lieu vivant

Les prochaines sources pourront ajouter, sans reconstruire ce socle : boucles
sportives, parcours d'orientation, lieux internes, associations, cours,
expériences et événements. Chaque type garde son propre contrat métier ; le
`PLACE` sert de contexte, pas de table fourre-tout. Le site officiel fournit le
socle physique et patrimonial ; les associations, cours et événements devront
ensuite alimenter la vie du lieu avec leur propre provenance et leurs périodes
de validité.

