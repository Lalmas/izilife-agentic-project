# izilife — Contexte Réservation & Privatisation

## Objectif

Créer un module global de réservation réutilisable dans izilife, sans casser l’existant legacy.

Le module doit couvrir :

- réservation d’un Place ;
- réservation d’un Shop ;
- réservation d’un Equipment ;
- privatisation partielle ;
- privatisation complète ;
- demande de réservation avec validation manuelle ;
- future validation automatique selon seuils.

Stack cible :

- CodeIgniter 4
- PHP
- MySQL
- jQuery
- Ajax
- JavaScript

---

## Objets concernés

### Place

Lieu physique principal : restaurant, bar, musée, parc, salle, etc.

Un Place peut :

- être réservable ;
- proposer des créneaux ;
- contenir des Equipment ;
- être privatisable totalement ;
- être rattaché à une configuration de réservation active.

### Shop

Commerce / établissement, séparation legacy avec Place.

Un Shop peut :

- être réservable ;
- contenir des Equipment ;
- proposer des réservations ;
- proposer une privatisation complète.

Important : ne pas fusionner Place et Shop en base.

### Equipment

Objet rattaché à un Place ou Shop.

Exemples :

- table ;
- salle ;
- terrasse ;
- terrain ;
- chambre ;
- espace privatisable ;
- équipement urbain ;
- équipement interne au lieu.

Tous les Equipment ne sont pas réservables.

Un Equipment peut être :

- descriptif uniquement ;
- réservable ;
- privatisable ;
- soumis à validation manuelle ;
- soumis à capacité propre.

---

## Modèle fonctionnel

### BookingContent

BookingContent est le container de réservation d’un objet.

Règles :

- un seul BookingContent actif par objet ;
- peut avoir une période de validité ;
- contient une ou plusieurs configurations ;
- pilote l’affichage du module front.

### BookingConfigurationContent

BookingConfigurationContent contient la configuration effective.

Il peut définir :

- jours actifs ;
- horaires ;
- slots ;
- capacité ;
- limites ;
- règles spéciales ;
- variantes type brunch, dîner, privatisation, événement spécial.

La capacité finale doit être calculée avec :

- capacité du lieu ;
- capacité de l’équipement ;
- limite de BookingConfigurationContent ;
- réservations déjà existantes ;
- type de demande ;
- privatisation ou non.

### BookingSlot

BookingSlot représente un créneau nommé.

Exemples :

- brunch ;
- déjeuner ;
- dîner ;
- afterwork ;
- soirée ;
- privatisation journée ;
- privatisation soir.

Le slot aide le front, mais ne doit pas bloquer les réservations avec heure libre si la configuration l’autorise.

---

## Booking

Booking est la table transactionnelle principale.

Elle représente une demande ou réservation utilisateur.

Elle peut pointer vers :

- Place ;
- Shop ;
- Equipment ;
- Experience ;
- LocalEvent ;
- Animation ;
- Session ;
- BookingConfigurationContent ;
- BookingSlot ;
- ElementAccessPrice ;
- ElementService ;
- Product.

Attention : une réservation doit avoir une cible métier principale claire.

---

## Statuts

### V1

Toutes les réservations passent en :

- pending

Validation manuelle obligatoire.

### V2 prévue

Ajouter une validation automatique conditionnelle.

Statuts envisagés :

- pending ;
- confirmed ;
- refused ;
- cancelled ;
- auto_confirmed ;
- paid ;
- unpaid ;
- expired.

Point critique : éviter de mélanger statut de paiement et statut de réservation.

Recommandation : créer un référentiel BookingStatus dédié plutôt que réutiliser TransactionStatus à long terme.

---

## Parcours utilisateur

Depuis une page Place ou Shop :

1. Vérifier si l’objet est réservable.
2. Vérifier si l’abonnement réservation est actif.
3. Afficher le bouton “Réserver”.
4. Ouvrir le module de réservation.
5. Identifier les modes disponibles :
   - réservation simple ;
   - réservation de table ;
   - réservation d’équipement ;
   - privatisation partielle ;
   - privatisation complète.
6. L’utilisateur choisit :
   - date ;
   - heure ou slot ;
   - quantité / nombre de personnes ;
   - équipement si applicable ;
   - notes.
7. Création d’une Booking en pending.
8. Validation manuelle par le lieu / admin.

---

## Privatisation

Deux cas :

### Privatisation d’équipement

Champ :

- is_equipment_privatization = 1

Exemples :

- salle ;
- terrasse ;
- espace VIP ;
- terrain ;
- zone privatisable.

### Privatisation complète du lieu

Champ :

- is_full_place_privatization = 1

Dans ce cas, la réservation doit bloquer les autres disponibilités compatibles sur la même période.

---

## Règles de disponibilité

Le front ne doit pas calculer seul la disponibilité.

Le back doit résoudre :

- objet réservable ou non ;
- abonnement actif ou non ;
- BookingContent actif ;
- BookingConfigurationContent applicable ;
- BookingSlot disponible ;
- capacité restante ;
- conflits existants ;
- privatisation bloquante ;
- besoin de validation manuelle ;
- éventuelle éligibilité auto-confirmation.

---

## Règles de validation

### V1

Tout est pending.

### V2

Auto-confirmation possible si :

- quantité sous seuil ;
- pas de privatisation ;
- capacité disponible ;
- objet autorisé à auto-confirmer ;
- délai avant réservation suffisant ;
- paiement non requis ou transaction validée.

Validation manuelle obligatoire si :

- privatisation ;
- dépassement de seuil ;
- équipement sensible ;
- demande spéciale ;
- conflit potentiel ;
- montant important ;
- réservation groupe.

---

## Architecture front cible

Prévoir un module générique piloté par configuration.

### Blocs UI

- bouton réservation ;
- modal réservation ;
- choix date ;
- choix slot / heure ;
- choix quantité ;
- choix équipement ;
- choix privatisation ;
- formulaire notes ;
- résumé ;
- écran confirmation.

### Sous-composants logiques

- BookingTargetResolver ;
- AvailabilityResolver ;
- CapacityResolver ;
- SlotResolver ;
- PrivatizationResolver ;
- BookingPayloadBuilder ;
- BookingSubmitter.

---

## API mentale attendue

Le front doit pouvoir demander :

- cet objet est-il réservable ?
- quels modes sont disponibles ?
- quels jours sont ouverts ?
- quels créneaux sont disponibles ?
- quels équipements sont réservables ?
- quelle capacité reste disponible ?
- la privatisation est-elle possible ?
- la réservation sera-t-elle pending ou auto-confirmed ?
- quel payload envoyer ?

---

## Règles à ne pas casser

- Ne pas fusionner Place et Shop.
- Ne pas rendre tous les Equipment réservables.
- Ne pas confondre Booking et Session.
- Ne pas mélanger réservation et paiement.
- Ne pas gérer la disponibilité uniquement en front.
- Ne pas créer une Booking avec plusieurs cibles principales incohérentes.
- Garder une logique compatible legacy.
- Prévoir les futures Sessions pour Experience / Event.

---

## Décision V1

Pour démarrer proprement :

- module unique ;
- plusieurs modes internes ;
- Booking créée en pending ;
- validation manuelle ;
- pas d’auto-confirmation immédiate ;
- disponibilité calculée côté back ;
- front piloté par API ;
- pas de paiement bloquant au premier lot sauf besoin existant.