# izilife — Contexte Réservation & Privatisation

## Mise à jour d'architecture — 25 août 2026

Les décisions ci-dessous complètent et, en cas de conflit, remplacent les simplifications V1 historiques du présent document.

### Accès et parcours

Le parcours effectif résulte de la combinaison orthogonale de `AccessType`, billetterie/paiement iziLife, `AccessBookingNeeded`, `BookingMethod`, `ElementAccessAndBookingConf`, BC/BCC ou SC/SCC, puis EAP/ElementService. Aucun de ces éléments ne doit absorber les responsabilités des autres. Le front consomme le résultat du resolver et ne déduit pas le parcours depuis une catégorie ou la seule présence d'un tarif.

La présence d'une BC/BCC ne suffit jamais : l'entitlement correspondant doit autoriser la capacité, le Partner doit avoir publié et non suspendu la configuration, puis EABC doit autoriser le chemin d'accès lorsqu'il s'agit d'un Equipment/loisir. `TABLE_BOOKING` reste indépendant d'EABC. Un comportement déclaré décrit l'interaction attendue ; il ne constitue jamais une activation et reste sans effet lorsque l'éligibilité, l'entitlement ou la configuration opérationnelle ne le justifient pas.

Le contrat opérationnel et les exemples sont détaillés dans `configuration-guide.md`.

`BookingConfigurationCategory` permet à une seule BC de servir plusieurs catégories sans dupliquer BCC, horaires ou capacité. La catégorie effectivement choisie est validée côté serveur puis enregistrée dans Booking. L'éligibilité métier vient de `EtablishmentType` et de ses `BookableServiceProductType` (`table-au-restaurant`, `objet-reservable`, `hebergement`, etc.), jamais du nom Restaurant/Bowling/VR. En mode `commerces-separes`, toute catégorie publiée doit être explicitement liée à une BC ; l'absence de lien l'exclut. Plusieurs catégories peuvent partager la même BC.

### Cible et scope

`from_type/from_id` désigne l'unique cible métier principale. Le scope décrit son contexte opérationnel et d'autorisation. Exemple : une table est une cible `EQUIPMENT`, son Place est le scope et le Partner du Place fournit l'ownership. Les FK Booking legacy sont conservées pendant la transition, avec invariant serveur imposant une seule FK cible.

### Allocation de ressources

- allocation automatique désactivée par défaut et activée explicitement par le Partner ;
- V1 : affectation automatique d'une seule ressource compatible et libre ; sinon Booking non affectée à traiter par le Partner ;
- V1 : aucun assemblage, désassemblage ou transfert manuel avancé ;
- V2 : affecter, libérer, transférer et assembler plusieurs ressources, en bloquant toutes les ressources d'origine.

### Mesures

Le moteur n'est pas limité aux personnes et unités. La configuration décrit les mesures collectées, capacitaires, tarifaires et opérationnelles : personnes, adultes/enfants, groupes, unités, durée, jours, chambres, terrains, crédits ou autres dimensions autorisées. Booking fige les valeurs validées utiles au Partner ; EAP et ElementService restent les autorités tarifaires.

### Client invité

Une réservation appartient à un `User` XOR un `BookingCustomer`. `BookingCustomer` est l'identité persistante du client sans compte ; il n'est jamais créé comme snapshot d'un User existant. Un e-mail déjà présent dans `User` impose connexion ou vérification d'identité. Créateur Partner/Page, origine Offer et identité cliente restent trois axes séparés.

### Catégorie, groupes, Community et Offer

- `place_type_id` XOR `shop_category_id` conserve la catégorie réellement réservée ; `NULL/NULL` signifie explicitement tout l'établissement.
- `booking_context` conserve `individual`, `user_group_booking` ou `community_booking`, avec les FK existantes `user_group_id`, `community_id`, `community_activity_id`.
- Le moteur réutilise les BPR `owner_type=booking`; il affiche la règle applicable et stocke `benefit_rule_id` sans recréer BenefitPolicy.
- `offer_id` relie la réservation à l'Offer d'origine. `SpecialCampain` ne type pas les opérations : il reste dédié aux promotions spéciales comme Happy Hour ou étudiant. Le futur sous-typage d'une `Offer` `OPERATION` (collective, Last Minute, etc.) sera défini dans le chantier Offer et ne sera pas recopié dans Booking.

### Event et EventSerie

Event/EventSerie peuvent porter une BC/BCC capacitaire propre. Une occurrence peut activer un fallback explicite vers la BC/BCC du Place/Shop hôte. SCC/Session reste une règle d'occurrence et ne remplace pas BCC pour les tables, ressources et capacités.

### Privatisation

Un Equipment privatisable peut définir un minimum de chiffre d'affaires/consommation et sa devise. Cette information est affichée avant la demande ; elle ne crée ni Transaction, ni acompte, ni devis tarifé dans la V1.

Sur un lieu de bouche, les options « réserver quelques tables », « privatiser cet Equipment/espace » et « privatiser tout l'établissement » partagent la même surface FO. Une catégorie unique ne produit pas une fausse privatisation de catégorie. En multi-catégorie `commerces-separes`, la catégorie ciblée est enregistrée et reste distincte de l'établissement complet. Un Equipment réservé pour son usage métier propre garde toutefois sa BC/BCC et son parcours EABC distincts.

### Attente, capacité et caution

Le blocage de capacité pendant l'attente, sa durée, le délai après confirmation et l'exigence d'une caution/acompte sont configurables. Une caution peut dépendre d'un seuil porté par une mesure et sa politique précise — remboursable, déductible ou garantie — reste distincte du statut Booking.

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
