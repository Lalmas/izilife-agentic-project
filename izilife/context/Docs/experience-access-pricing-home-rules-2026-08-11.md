# XP — accès, tarifs, vente sans date et domicile

## Contrat retenu

Le moteur reste automatique. Une XP avec des sessions vendables continue à
proposer une session. Le domicile ne modifie pas ce choix.

`Experience.force_sale_without_date` est une surcharge monotone :

- `0` : le resolver décide à partir de l'accès et des sessions ;
- `1` : aucun choix de date pendant l'achat, même si des sessions existent.

La suite de l'achat est portée par `ExperienceBookingValidationType` : appel,
mail, rappel, consigne libre, ou ultérieurement choix d'une date dans iziLife.
La valeur `choisir-une-date-apres-achat` réutilise le parcours différé
`AFTER_PAYMENT` déjà présent ; ce nom technique reste interne et le BO affiche
uniquement « Choisir une date après l'achat ».

## Expérience à domicile

Le domicile est un lieu d'exécution, pas un mode de vente.

- `individual` et `private_group` sont autorisés ;
- `open_group` est interdit ;
- toute session à domicile est exclusive : la première réservation privatise
  le créneau, y compris lorsque le mode de participation est `individual` ;
- une ville de départ et un rayon strictement positif sont obligatoires ;
- pour une SESSION, l'adresse client est sélectionnée via la recherche OSM puis
  contrôlée côté serveur avant réservation/paiement ;
- pour une vente sans date, l'adresse est également sélectionnée et contrôlée
  avant l'achat ; seule la date reste à convenir ensuite avec l'organisateur ;
- l'adresse, la latitude et la longitude validées sont figées dans `Booking` ;
- le calcul Haversine compare ces coordonnées à celles de la ville de départ et
  refuse toute adresse au-delà du rayon configuré ;
- aucune division administrative ne borne le rayon, qui peut traverser une
  frontière.

Champs : `home_service_city_id` et `home_service_radius_km`.

## Contextes des référentiels

`AccessType.context_types` et `PriceModel.context_types` sont des `SET` fermés :
`PLACE`, `EVENT`, `EXPERIENCE`, `CIRCUIT`, `EQUIPMENT`, `ANIMATION`. `PLACE`
couvre Place et Shop.

Une valeur est proposée si son contexte contient l'objet courant. Un modèle de
prix doit en plus être `is_active = 1`. Event et Experience restent limités à
`ticket-unitaire` tant qu'un autre calcul n'est pas implémenté identiquement
dans le BO, le FO, le paiement et le fulfillment.

## Règles de commercialisation

Une vente forcée sans date requiert un mode de validation et un contact réel
quand ce mode implique le partenaire. Sans surcharge, le resolver conserve son
comportement automatique. Retirer la surcharge ne fabrique pas une session : si
la configuration restante est insuffisante, la vente doit rester bloquée.

PayHub ne décide aucune de ces règles. Il consomme le parcours déjà résolu et
ne gère que le paiement et la transaction associée.

## Participants

Les limites globales restent celles de l'XP. Un EAP peut uniquement les
resserrer avec `minimum_party_size` et `maximum_party_size`. La réservation
fige le nombre réel dans `Booking.party_size`. Tant que seul le ticket unitaire
est commercialisable sur XP, `party_size` correspond au nombre réel de places
calculé côté serveur et ne fait jamais confiance à une valeur libre du POST.

## Déploiement et rattrapage

Le SQL est exclusivement posé dans
`izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`. Il ajoute les
colonnes et contraintes, puis remet à niveau les lignes AccessType et PriceModel
existantes par `string_id`. Aucune migration CodeIgniter n'est utilisée.

Le fichier 021 doit être exécuté une seule fois sur une copie de la base avant
la recette. Les `UPDATE` de rattrapage sont rejouables ; les `ALTER TABLE`, comme
le reste de ce fichier de version, ne sont pas conçus pour être rejoués après
une application réussie.

## Matrice de recette fonctionnelle

- `individual` : aucun minimum/maximum de groupe sur l'XP ou l'EAP. Le nombre
  acheté est borné par le tarif et la capacité totale par la session.
- `private_group` : l'XP porte les bornes du groupe ; un EAP peut les resserrer.
- `open_group` : aucun minimum/maximum de groupe ; la session porte la capacité.
- `libre-et-gratuit` : information uniquement, sans EAP, Booking, Ticket ni
  transaction à zéro, même si un ancien `BookingNeeded` est incohérent.
- `gratuit-sur-reservation` avec billetterie iziLife : Booking et Ticket à zéro,
  transaction interne de traçabilité, sans résolution ni appel PSP.
- `payant` avec billetterie iziLife : au moins un EAP vendable ; choix de la date
  selon le parcours résolu.
- billetterie iziLife désactivée : sessions informatives, contact et lien externe
  affichables, aucun checkout iziLife.
- domicile : ville et rayon obligatoires uniquement lorsque
  `is_home_experience = 1`; ils sont ignorés et vidés sinon.
