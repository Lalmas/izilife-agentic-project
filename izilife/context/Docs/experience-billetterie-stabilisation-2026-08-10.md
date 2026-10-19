# Billetterie Experience — stabilisation du 10 août 2026

Le contrat BO complémentaire sur les contextes d'accès, la vente forcée sans
date et les XP à domicile est fixé dans
`docs/experience-access-pricing-home-rules-2026-08-11.md`.

## Contrats conservés

- Une opération à 0 € reste une vraie `Transaction` PayHub.
- La Transaction gratuite passe à `status = 2`, utilise `provider = internal`, puis exécute le fulfillment du contexte.
- Seule la résolution d'un PSP externe est évitée pour un montant nul.
- Une Experience informative ne peut pas être forcée dans le tunnel par un POST.
- Le resolver reste l'autorité pour `NO_DATE`, `ARRIVAL_DATE`, `SESSION` et `AFTER_PAYMENT`.
- Le serveur recalcule prix, composants de packs, limites, stocks et capacité.

## Modifications de ce lot

### PayHub et providers

- `ProviderResolver` ne renvoie plus `auto` ou `stripe` lorsqu'aucun provider n'est enregistré.
- Une vente payante sans provider retourne `NO_PROVIDER_ACTIVE` au contrôleur au lieu d'une page d'exception.
- L'aperçu du provider ne lève plus d'exception sur les écrans qui ne déclenchent pas encore de paiement.
- Les opérations gratuites ne cherchent ni compte PSP ni plan de split, mais conservent Transaction et fulfillment.
- Les frais XP payants sont calculés après résolution du provider réel ; Stripe n'est plus forcé dans le handler XP.

### OwnerChain

- `forExperience()` résout `meet_place`, `meet_shop`, `page_id`, puis `partner_id`.
- Place et Shop sont lus avec une table explicite afin de ne pas utiliser un modèle sans table par défaut.
- Les anciennes copies sous `Utils/Some_utils` ont été remises au même contrat pour éviter un comportement divergent si elles sont encore incluses par du code historique.

### Quantités et interface

- Le sélecteur et les tarifs sont regroupés dans un seul panneau compact ; chaque EAP conserve sa card individuelle.
- Le bouton Acheter/Réserver est désactivé quand la quantité totale vaut zéro ou quand le choix temporel est incomplet.
- Les métadonnées rendues avant affichage comprennent :
  - limite utilisateur déjà consommée ;
  - stock EAP global pour `NO_DATE` ;
  - stock EAP par occurrence pour `SESSION` ;
  - composition et admissions réelles des packs ;
  - capacité restante commune de la séance.
- Le navigateur contrôle la demande cumulée de tous les tarifs et composants.
- Un dépassement affiche le toast commun `showAlert` avec un texte de langue.
- Le serveur conserve tous les contrôles contre un POST forgé.

### Fulfillment

- `fulfilled_at` est désormais écrit dans la même transaction SQL que Booking et Ticket.
- Un échec annule donc à la fois les écritures métier et le marquage de fulfillment.
- Le verrou nommé sérialise le fulfillment d'une occurrence.
- Un retry d'une Transaction payée reste possible après rollback.
- Une Transaction déjà fulfillée reste idempotente.

## Validations réellement exécutées

- `php -l` sur le resolver, PayHub, handler XP, OwnerChain, contrôleur, modèle, vue, langue et tests XP : OK.
- `git diff --check` sur les fichiers touchés : OK.
- démarrage CodeIgniter avec `spark serve` et requête HTTP sur la home : HTTP 200, aucun marqueur fatal.
- test isolé du resolver vide : retourne bien `NO_PROVIDER_ACTIVE`.

Le dépôt ne fournit actuellement ni commande `spark test` ni binaire `vendor/bin/phpunit`. Les tests PHPUnit présents n'ont donc pas pu être exécutés localement dans ce lot.

## Recette manuelle ciblée

### SESSION payante

1. Ouvrir une XP payante avec plusieurs tarifs et une séance de capacité connue.
2. Vérifier que le bouton est désactivé avant sélection d'un tarif.
3. Choisir date puis séance.
4. Ajouter plusieurs tarifs : le bouton s'active dès la première unité.
5. Dépasser successivement limite utilisateur, stock EAP, composant de pack et capacité commune.
6. Vérifier un toast explicite à chaque refus.
7. Soumettre une combinaison valide, payer et vérifier Transaction, Booking et un Ticket par admission.

### NO_DATE payante

1. Ouvrir une dégustation sans date.
2. Vérifier l'absence de sélecteur temporel.
3. Vérifier le stock EAP global et les packs.
4. Payer puis vérifier Transaction et Tickets, sans Booking daté.
5. Vérifier le texte de validation/prise de contact dans les métadonnées du droit.

### Gratuit sur réservation

1. Choisir une séance et un EAP à 0 €.
2. Vérifier qu'aucun provider externe n'est demandé.
3. Vérifier la création d'une Transaction `status = 2`, `provider = internal`.
4. Vérifier Booking et Tickets gratuits.

### RSVP

1. Tester invité, utilisateur connecté non membre et membre.
2. Vérifier que la billetterie iziLife désactive le RSVP concurrent.
3. Pour un membre, enregistrer Oui/Peut-être/Non et vérifier toast et persistance par occurrence.

### Fulfillment et retry

1. Exécuter deux fois le fulfillment d'une Transaction payée : aucune duplication.
2. Provoquer une exception métier avant commit : aucun Booking/Ticket partiel et `fulfilled_at` reste NULL.
3. Corriger la cause et relancer : fulfillment complet possible.

### Aucun provider actif

1. Utiliser une XP payante sans provider enregistré.
2. Vérifier le retour sur la fiche avec toast d'indisponibilité, sans exception technique.
3. Vérifier qu'une XP gratuite continue de créer Transaction et fulfillment dans le même environnement.

### Préparation SQL et protections BO

1. Restaurer une copie d'une base existante, puis exécuter intégralement
   `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql` une fois.
2. Vérifier le rattrapage `context_types` des AccessType et PriceModel existants.
3. Vérifier qu'Event et XP ne proposent que `ticket-unitaire` et qu'un POST forgé
   avec un PriceModel désactivé ou hors contexte est refusé.
4. Sur un Event mono-jour, vérifier l'absence des champs Pass. Sur un Event
   multi-jour, vérifier l'exclusion mutuelle 1 jour/plusieurs jours et la borne
   du nombre de jours côté serveur.
5. Vérifier les listes contextuelles PLACE (Place et Shop), EVENT, EXPERIENCE,
   CIRCUIT, EQUIPMENT et ANIMATION.

### SESSION à domicile

1. Configurer une XP domicile avec une ville de départ et un rayon, en mode
   `individual`, puis refaire le scénario en `private_group`.
2. Vérifier que `open_group` empêche la commercialisation.
3. Sélectionner une séance : l'adresse d'intervention devient obligatoire.
4. Choisir une suggestion OSM située dans le rayon : la réservation doit passer
   et figer adresse, ville rapprochée, latitude et longitude dans Booking.
5. Essayer une adresse sans suggestion, sans coordonnées, puis hors rayon : le
   serveur doit refuser avant paiement, même avec un POST forgé.
6. Vérifier qu'un rayon frontalier accepte une adresse étrangère réellement
   située dans le cercle.

### Vente sans date et choix après achat

1. Activer `force_sale_without_date` sur une XP avec sessions : aucun choix de
   date ne doit apparaître avant l'achat.
2. Avec un mode de contact, vérifier le texte et les coordonnées du contact ;
   sans contact valide, la XP ne doit pas être commercialisable.
3. Avec « Choisir une date après l'achat », acheter puis ouvrir le droit depuis
   Mes réservations, choisir la séance et vérifier la consommation atomique du
   droit. Pour une XP domicile, vérifier l'adresse et le rayon à cette étape.
4. Désactiver la surcharge et vérifier que le resolver revient au comportement
   automatique sans transformer implicitement le domicile en NO_DATE.

### Limites de participants

1. Poser un minimum/maximum global sur l'XP puis des bornes EAP plus étroites.
2. Vérifier qu'un EAP ne peut pas élargir les bornes globales.
3. Tester sous le minimum, dans la plage et au-dessus du maximum.
4. Vérifier `Booking.party_size` et confirmer qu'une valeur `party_size` forgée
   dans le POST n'écrase pas le calcul serveur issu des tickets.
