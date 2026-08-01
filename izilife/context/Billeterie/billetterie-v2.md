# Billetterie IziLife V2 - contexte, état des lieux et feuille de route

Dernière mise à jour : 28 juillet 2026

## 1. Objet du chantier

Ce document est la référence de contexte du chantier billetterie IziLife V2.

L'objectif immédiat n'est pas de construire toutes les fonctions d'une billetterie mature. Il est de stabiliser ce qui existe déjà pour rendre la billetterie Event réellement utilisable, puis de permettre à quelques associations, lieux et organisateurs pilotes de configurer et exploiter leur billetterie depuis l'espace partenaire.

Le chantier avance progressivement : un périmètre fonctionnel est corrigé, testé et validé avant l'ouverture du suivant.

## 2. Modèle métier retenu

### 2.1 Objets IziLife

Les objets métier principaux sont notamment :

- Event ;
- Experience (XP) ;
- Place ;
- Shop ;
- Circuit.

Ces objets peuvent proposer différentes choses vendables ou réservables :

- un EAP ;
- un ElementService ;
- un Product avec un ou plusieurs Price.

ElementService n'est pas au même niveau que Event, Experience, Place, Shop ou Circuit. C'est une prestation rattachée à un objet.

### 2.2 EAP et Ticket

`ElementAccessPrice` (EAP) représente une offre ou un ticket d'accès configurable : adulte, enfant, gratuit sur réservation, pass, pack famille, etc.

Un EAP n'est pas une occurrence de billet déjà attribuée. Après validation de la réservation ou du paiement, le pipeline génère les occurrences `Ticket` correspondantes.

Exemple :

```text
Event
└── EAP « Entrée adulte »
    └── achat de deux accès
        ├── Ticket individuel 1
        └── Ticket individuel 2
```

### 2.3 ElementService et Product

- `ElementService` représente une prestation : service de coiffure, spa, traiteur, visite privée, etc. Cette prestation peut avoir un prix et pourra éventuellement déclencher une réservation.
- `Product` représente un produit ou une offre commerciale et utilise ses objets `Price`.

EAP, ElementService et Product peuvent partager des briques techniques (prix, disponibilité, panier et paiement), mais leurs identités et règles métier ne doivent pas être fusionnées.

## 3. Architecture de paiement retenue

Le tunnel historique `Event::pay()` est considéré comme mort fonctionnellement. Il ne doit plus recevoir de nouvelles évolutions.

Le tunnel de référence est :

```text
Payment::pay()
→ PayHub
→ EventBookingHandler::prepare()
→ transaction interne ou prestataire de paiement
→ EventBookingHandler::fulfill()
→ génération des Tickets
```

`EventBookingHandler` doit être l'autorité serveur pour :

- relire les EAP réels ;
- recalculer les montants ;
- recalculer les frais ;
- contrôler les limites par EAP et par utilisateur ;
- contrôler la capacité globale de l'Event ;
- refuser une réservation fermée ou épuisée ;
- créer les tickets après validation.

Le navigateur ne doit jamais être la source de vérité pour un prix, une disponibilité ou un état de réservation.

## 4. Compte IziLife

### Décision V2

Le compte IziLife reste obligatoire. Le produit est pensé comme un système intégré : billets, réservations, avantages et historique sont rattachés au compte de l'utilisateur.

La réservation sans compte n'est pas dans le périmètre de lancement.

### Porte de sortie future

L'architecture ne doit cependant pas empêcher définitivement un futur mode invité. Celui-ci pourrait un jour utiliser une identité de commande (email, nom, téléphone et lien sécurisé), puis permettre le rattachement ultérieur à un compte.

Ce sujet reste différé. Il ne faut pas aujourd'hui modifier `Transaction.sender_id`, la propriété des tickets ou l'authentification pour le supporter.

## 5. Mode de tarification

Le champ affiché historiquement comme « Gestion prix » correspond à un mode de calcul du prix. Il est utile et doit être conservé.

Nom recommandé dans l'interface : **Mode de tarification**.

Exemples existants :

- ticket unitaire ;
- prix par personne et par durée ;
- prix par équipement et par durée ;
- prix par personne à la journée ;
- prix par équipement à la journée ;
- abonnement récurrent ;
- adhésion.

Règles attendues :

- filtrer les choix selon le type d'objet ;
- présélectionner « Ticket unitaire » pour un Event ;
- masquer les notions de durée et d'équipement lorsqu'elles ne s'appliquent pas ;
- exploiter ce mode dans les calculs serveur ;
- ne pas confondre mode de tarification, type d'accès, EAP et variation tarifaire.

Pour un Event :

- type d'accès : payant, gratuit sur réservation, tarif libre, etc. ;
- EAP : adulte, enfant, pack famille, etc. ;
- mode de tarification : généralement ticket unitaire ;
- variation : réduction, groupe, palier, période ou catégorie.

## 6. État des réservations

### 6.1 Existant

`LocalEvent.registration_state` existe déjà et référence la table `RegistrationState` :

| ID | Valeur historique |
|---:|---|
| 1 | Ouvert |
| 2 | Fermé pour le moment |
| 3 | N'accepte plus de réservations |
| 4 | Complet |

Le BO propose déjà ce champ. Le front le consulte partiellement, mais les règles actuelles peuvent réafficher la billetterie malgré un arrêt manuel.

### 6.2 Évolution retenue

Le champ existant peut servir de base, mais il faut distinguer :

- **état configuré** : décision de l'organisateur ;
- **état effectif** : résultat calculé par le système.

Correspondance métier visée :

| État | Nature | Effet |
|---|---|---|
| Ouvert | manuel | réservations autorisées si une offre reste disponible |
| En pause | manuel | arrêt temporaire des nouvelles réservations |
| Clôturé | manuel ou date limite | aucune nouvelle réservation |
| Sold out | calculé | aucune offre vendable ne peut satisfaire une réservation |
| Liste d'attente | future | réservation directe fermée, inscription en attente possible |
| Pas encore ouvert | future/calculé | date d'ouverture non atteinte |

« Complet » ne doit pas être la seule source de vérité enregistrée. Le sold out doit être recalculé.

Priorité des règles :

```text
Event annulé ou inactif
→ indisponible

Réservations en pause ou clôturées
→ indisponible

Date d'ouverture non atteinte ou date de clôture dépassée
→ indisponible

Capacité globale atteinte ou aucune offre vendable
→ sold out

Sinon
→ ouvert
```

La même décision doit être appliquée dans le front, le BO, l'espace partenaire et `EventBookingHandler`.

## 7. Calcul de disponibilité attendu

### EAP simple

Un EAP est indisponible si :

- il est inactif ;
- sa quantité propre est épuisée ;
- la capacité globale de l'Event est épuisée ;
- l'état effectif de l'Event interdit les réservations ;
- les limites de l'utilisateur sont atteintes.

### Event

Un Event est sold out si :

- sa capacité globale est atteinte ; ou
- aucun EAP actif et vendable ne permet encore de réserver au moins une unité.

L'arrêt manuel et le sold out automatique doivent rester deux causes distinctes.

### Packs

Un pack est vendable uniquement si :

- le pack est actif ;
- sa propre limite permet l'achat ;
- la capacité globale permet tous les tickets réels du pack ;
- chacune des composantes requises possède encore une disponibilité suffisante.

Les capacités doivent utiliser `access_price_real_ticket_quantity`. Le nombre de packs achetés (`access_price_quantity`) ne représente pas le nombre réel de places consommées.

### Concurrence

Le contrôle front est seulement informatif. Le serveur doit refaire le contrôle au dernier moment et réserver les capacités de façon atomique afin d'éviter la survente lors de deux commandes simultanées.

## 8. Périmètre de validation avant lancement V2

Le lancement pilote repose sur six scénarios Event.

### 8.1 Event gratuit sur réservation

- EAP à 0 euro ;
- choix d'une quantité ;
- bouton « Réserver », jamais « Payer 0,00 € » ;
- aucun bloc de carte bancaire ;
- passage par la voie gratuite interne de PayHub ;
- transaction validée ;
- création du bon nombre de Tickets ;
- limites et sold out respectés.

### 8.2 Participation libre

À préciser fonctionnellement selon le type d'accès exact : accès sans réservation, ou participation/réservation sans paiement. La billetterie ne doit apparaître que si une réservation ou l'émission d'un ticket est requise.

### 8.3 Tarif par personne

- prix unitaire multiplié par le nombre de personnes ;
- quantité réelle égale au nombre de tickets ;
- montant recalculé côté serveur ;
- limites EAP, Event et utilisateur respectées.

### 8.4 Pack

- prix du pack multiplié par le nombre de packs ;
- nombre de Tickets issu de la composition ;
- capacité consommée selon les tickets réels ;
- refus si une composante ou l'Event ne peut plus accueillir le pack complet.

### 8.5 Tarif libre

- montant saisi par l'utilisateur ;
- aucune confusion avec un EAP inexistant ;
- règle explicite sur l'acceptation ou non de 0 euro ;
- montant et frais recalculés/validés côté serveur ;
- quantité de personnes contrôlée séparément du montant.

### 8.6 Tarif libre à partir de

- montant minimum configuré par personne ;
- impossibilité de descendre sous ce minimum ;
- quantité de personnes distincte du montant unitaire ;
- validation serveur du minimum ;
- calcul correct du total et des frais.

## 9. Matrice de tests obligatoire

Chaque scénario précédent doit être testé au minimum avec :

- utilisateur connecté ;
- quantité 0, 1, limite exacte et dépassement ;
- EAP actif puis inactif ;
- réservations ouvertes, en pause et clôturées ;
- capacité EAP disponible puis épuisée ;
- capacité Event disponible puis épuisée ;
- retour après authentification si nécessaire ;
- paiement réussi, annulé et refusé pour les cas payants ;
- double soumission ;
- deux réservations concurrentes sur la dernière place ;
- vérification de la Transaction ;
- vérification du nombre et du statut des Tickets ;
- vérification du mail de confirmation existant.

## 10. État technique constaté au démarrage

### Fonctionnel ou présent

- EAP Event ;
- tarifs groupés ;
- packs et compositions ;
- quantités et maxima par utilisateur ;
- calcul partiel des quantités restantes ;
- PayHub et `EventBookingHandler` ;
- voie interne pour les commandes gratuites ;
- génération d'occurrences `Ticket` dans `fulfill()` ;
- champ historique `registration_state` dans le BO.

### Corrigé pendant l'état des lieux

- crash de la vue tarif libre lorsque l'objet Event ne contient pas la propriété dynamique `is_sold_out` ;
- calcul local de repli à partir de la capacité globale pour cette vue.

### Corrigé dans le lot de stabilisation en cours

- le bouton utilise maintenant la sélection réelle : « Réserver » à 0 euro et « Payer » au-dessus de 0 ;
- le bloc « Enregistrer la carte » est masqué et désactivé lorsqu'aucun paiement n'est requis ;
- tarif libre et tarif libre à partir de utilisent désormais des minimums distincts ;
- le tarif libre virtuel est reconnu et validé explicitement par `EventBookingHandler` ;
- les EAP réels sont contrôlés et leurs prix sont recalculés depuis la base ;
- `canShowBilletterieForEvent()` respecte en priorité les états manuels fermés ;
- `EventBookingHandler` refuse les états pause, clôture et complet ;
- les quantités réelles des packs sont recalculées côté serveur depuis leur composition ;
- les compteurs globaux privilégient `access_price_real_ticket_quantity` ;
- le sold out global rend les EAP indisponibles lorsque la capacité Event est atteinte.

### Restant à valider ou à approfondir

- retest réel des six scénarios depuis la session navigateur authentifiée ;
- consommation détaillée des capacités des EAP inclus dans un pack ;
- protection atomique contre deux achats simultanés de la dernière place ;
- calcul central unique de l'état effectif, au-delà des protections ajoutées au front et au handler ;
- affichage d'un message dédié lorsque les réservations sont en pause ou clôturées.

## 11. Espace partenaire nécessaire au pilote

Avant de proposer la V2 à des associations, lieux et organisateurs pilotes, l'espace partenaire doit permettre :

- créer et modifier les EAP compatibles avec l'Event ;
- créer un ticket gratuit sur réservation ;
- créer un tarif par personne ;
- créer et composer un pack ;
- configurer un tarif libre et un tarif libre avec minimum ;
- définir les quantités et limites par utilisateur ;
- ouvrir, mettre en pause, reprendre et clôturer les réservations ;
- voir l'état effectif et la cause d'indisponibilité ;
- consulter réservations, ventes, quantités et chiffre d'affaires ;
- consulter et exporter les participants ;
- renvoyer une confirmation.

Le partenaire ne doit pas accéder à des options de tarification incompatibles avec l'objet Event.

## 12. Ordre des chantiers

### Lot 1 - Stabilisation Event

1. Corriger l'interface gratuit/payant.
2. Distinguer tarif libre et tarif libre à partir de.
3. Centraliser l'état effectif des réservations.
4. Appliquer cet état dans `EventBookingHandler`.
5. Centraliser capacités EAP, Event et packs.
6. Tester les six scénarios de lancement.

### Lot 2 - Espace partenaire pilote

1. Configuration des six scénarios.
2. Pause, reprise et clôture.
3. Réservations, ventes, participants et chiffre d'affaires.
4. Contrôle des droits par partenaire et par objet.

### Lot 3 - Livraison et exploitation du ticket

- ticket web mobile ;
- QR code ;
- ticket PDF et envoi par email ;
- renvoi de confirmation ;
- contrôle et validation ;
- transfert et annulation.

Le PDF est souhaitable pour une vraie billetterie, mais il ne bloque pas la correction initiale du tunnel Event si le ticket et la confirmation sont déjà accessibles autrement.

### Chantiers suivants

- vente d'Experience avec intégration au futur chantier Booking ;
- vente sur Place, Shop ou Circuit selon les cas métier ;
- chantier menu digital autour de Product et Price ;
- ElementService après stabilisation de Booking et des règles de vente/réservation ;
- amélioration continue des EAP : liste d'attente, variantes/paliers, tarifs réduits, pass multijours, diffusion, consommations et produits inclus, abonnements et adhésions ;
- adresse secrète et notifications programmées ;
- import et transfert de tickets.

## 13. Critères de lancement pilote

La V2 Event est lançable auprès de premiers partenaires si :

- les six scénarios sont configurables et passent la matrice de tests ;
- aucun montant ou prix envoyé par le navigateur n'est accepté sans recalcul serveur ;
- aucune réservation n'est possible pendant une pause ou après clôture ;
- aucune survente simple ou concurrente n'est possible ;
- les transactions gratuites n'appellent aucun prestataire de paiement ;
- les transactions payantes et gratuites génèrent les bons Tickets ;
- le partenaire peut gérer ses offres et suivre réservations, ventes et chiffre d'affaires ;
- les erreurs sont compréhensibles pour le client et l'organisateur.

## 14. Journal d'avancement

| Date | État | Élément |
|---|---|---|
| 2026-07-28 | Fait | Premier audit du flux Event/EAP, front et BO |
| 2026-07-28 | Fait | Identification de la cause du bouton gratuit désactivé |
| 2026-07-28 | Fait | Correction du crash `is_sold_out` sur la vue tarif libre |
| 2026-07-28 | Fait, à retester | Correction effective du bouton « Réserver » et masquage de la carte |
| 2026-07-28 | Fait, à retester | Séparation tarif libre / tarif libre à partir de |
| 2026-07-28 | Fait, à retester | Prise en charge V2 de l'identifiant virtuel du tarif libre |
| 2026-07-28 | Fait | Recalcul serveur des prix EAP et des quantités réelles de packs |
| 2026-07-28 | Fait | Priorité des états manuels fermés dans le front et le handler |
| 2026-07-28 | À faire | Service central d'état et de disponibilité |
| 2026-07-28 | À faire | Sécurisation correspondante dans `EventBookingHandler` |
| 2026-07-28 | À faire | Matrice de tests des six scénarios |
| 2026-07-28 | À faire | Périmètre partenaire minimal du pilote |

## 15. Principes à préserver

- Le compte IziLife reste le parcours nominal de la V2.
- `EventBookingHandler` est le tunnel Event de référence.
- Le serveur est l'autorité pour les prix, frais, états et capacités.
- Une réservation gratuite est une vraie commande à montant nul, pas un faux paiement.
- Un EAP produit des Tickets ; une Transaction ne remplace pas un Ticket.
- L'état manuel et le sold out calculé restent distincts.
- Les briques communes peuvent être mutualisées sans confondre EAP, ElementService et Product.
- Event est stabilisé avant la généralisation aux autres objets.
