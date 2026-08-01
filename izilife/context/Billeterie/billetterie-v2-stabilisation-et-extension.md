# Billetterie V2 — stabilisation Event et extension Booking

Dernière mise à jour : 29 juillet 2026

Ce document complète `billetterie-v2.md`. Il consigne les corrections de clôture du tunnel Event et fixe les limites d'architecture avant la duplication vers Experience et les Sessions.

## 1. Modèle métier

Les objets principaux sont `Event`, `Experience`, `Place`, `Shop` et `Circuit`.

Ils peuvent porter des propositions de natures différentes :

- `ElementAccessPrice` (EAP) : offre/tarif donnant un droit d'accès et produisant des `Ticket` ;
- `ElementService` : prestation rattachée à un objet, avec son propre prix et éventuellement une réservation ;
- `Product`, vendu avec ses objets `Price`.

Un EAP, un ElementService et un Product peuvent employer les mêmes briques de prix, panier, paiement et Booking sans être confondus ni placés au même niveau que les objets principaux.

## 2. État Event après stabilisation

Le tunnel unique est `Payment::pay()` → `PayHub` → `EventBookingHandler::prepare()` → paiement interne/PSP → `fulfill()`.

Corrections posées :

- retour normalisé sans duplication `/izilife/izilife` ;
- EAP gratuit : bouton `Réserver`, carte masquée, frais PSP strictement nuls ;
- tarif libre et tarif libre à partir de distingués et validés serveur ;
- prix EAP et tarifs groupés recalculés serveur ;
- quantité réelle des packs recalculée depuis leur composition ;
- disponibilité des composants d'un pack contrôlée avant la transaction ;
- capacité Event, capacité EAP et maximum utilisateur contrôlés serveur ;
- verrou Event pendant le contrôle et l'insertion de la transaction ;
- transactions de paiement en cours récentes retenues pendant 15 minutes dans la capacité ;
- pause et clôture prioritaires dans le FO et le handler.

Le test navigateur authentifié reste la validation fonctionnelle finale pour chaque scénario.

## 3. État de réservation

`LocalEvent.registration_state` reste le champ de commande de l'organisateur :

- `1` : ouvert ;
- `2` : en pause ;
- `3` : clôturé.

L'ancien état manuel `4 = Complet` n'est plus proposé dans le BO. `Complet` est un résultat calculé, affiché comme tel dans le BO et le FO.

Ordre de décision :

1. Event inactif/annulé : indisponible.
2. Pause/clôture manuelle : indisponible.
3. Fenêtre de vente fermée : indisponible.
4. Capacité globale atteinte : complet.
5. Aucun EAP actif satisfaisable, y compris les packs : complet.
6. Sinon : ouvert.

Le sold out ne doit jamais écraser l'intention manuelle enregistrée.

## 4. Protection de capacité

Pour chaque tentative, le serveur doit :

1. prendre un verrou logique sur l'Event ;
2. relire les ventes terminées et les transactions en cours non expirées ;
3. recalculer le panier ;
4. vérifier chaque EAP et chaque composant de pack ;
5. insérer la transaction en cours ;
6. libérer le verrou.

La réservation temporaire expire actuellement après 15 minutes. Un futur job devra marquer explicitement les transactions abandonnées/expirées ; la fenêtre temporelle reste la protection de repli.

## 5. `ElementAccessAndBookingConf`

Cette configuration ne représente ni un EAP ni une réservation. C'est la règle d'orchestration qui explique comment un utilisateur accède à une cible (`Place`, `Shop`, `Experience`, `Equipment`, etc.).

Elle doit pouvoir décider :

- accès libre, achat seul, réservation seule, ou achat + réservation ;
- `BookingConfigurationContent` à utiliser ;
- choix du créneau **avant** l'achat, **après** l'achat, ou absent ;
- confirmation instantanée ou manuelle ;
- capacité partagée ou privatisation d'une ressource ;
- taille du groupe et consommation réelle de capacité.

Valeurs conceptuelles à formaliser avant XP :

- `access_flow`: `FREE`, `BUY_ONLY`, `BOOK_ONLY`, `BOOK_THEN_BUY`, `BUY_THEN_BOOK` ;
- `slot_timing`: `NONE`, `BEFORE_PURCHASE`, `AFTER_PURCHASE` ;
- `capacity_mode`: `PER_PERSON`, `SHARED_SLOT`, `PRIVATE_RESOURCE` ;
- `booking_configuration_content_id` ;
- règles de taille minimale/maximale de groupe.

Exemples :

- restaurant/salon de thé : `BOOK_ONLY`, sans EAP obligatoire ;
- bowling privatisé pour huit : une unité vendue bloque toute la ressource ;
- activité de huit places partagées : chaque personne consomme une place ;
- carte d'accès : `BUY_ONLY` ;
- Experience avec session : choix du créneau avant paiement, puis EAP ;
- pass utilisable plus tard : achat d'abord, choix du créneau après.

`EligibilityResolver` peut exposer les actions possibles, mais la décision finale doit provenir d'un resolver de parcours unique, utilisé par le FO et les handlers serveur.

## 6. `LocationOtherCategory`

Une `LocationOtherCategory` est un sous-périmètre fonctionnel du même `Place` ou `Shop`. Elle ne crée pas trois lieux ni trois commerces.

Lorsque `is_multi_category_* = 1` et que `multi_category_management_type` indique une gestion séparée, les modules concernés doivent demander une catégorie :

- EAP ;
- horaires (`Hourly`) ;
- menus ;
- ElementServices ;
- BenefitPolicyRule ;
- Offer ;
- BookingConfiguration/ressources si nécessaire.

Le principe commun est un scope :

```text
owner_type + owner_id + location_other_category_id nullable
```

`location_other_category_id = NULL` signifie configuration commune à tout le lieu. Une valeur signifie configuration propre à la catégorie. Le resolver doit appliquer une règle explicite d'héritage : spécifique d'abord, puis commun si le module l'autorise.

La table actuelle doit recevoir un identifiant primaire stable avant d'être référencée par ces modules, ainsi qu'une contrainte garantissant qu'une ligne appartient soit à un Place, soit à un Shop.

## 7. Ordre de suite recommandé

1. Retester manuellement les six scénarios Event.
2. Corriger les erreurs fonctionnelles remontées par ces tests.
3. Porter la gestion Event minimale dans l'espace partenaire : EAP, pause/reprise/clôture, réservations, ventes et chiffre.
4. Extraire un service commun de disponibilité et de parcours.
5. Brancher Experience + Sessions en réutilisant ce service et `EventBookingHandler` comme référence, sans copier ses erreurs historiques.
6. Ajouter le scope `LocationOtherCategory` module par module.
7. Brancher ensuite ElementService sur Booking selon ses propres règles métier.

## 8. Matrice de clôture Event

Pour chacun : gratuit sur réservation, participation libre, par personne, pack, tarif libre, tarif libre à partir de :

- sélection et libellé du bouton ;
- absence/présence correcte de la carte ;
- montant net, frais et total ;
- transaction et nombre de Tickets ;
- limite EAP, Event et utilisateur ;
- pause et clôture ;
- sold out calculé ;
- double clic et deux navigateurs sur la dernière place ;
- retour réussi, annulé et refusé sans duplication du préfixe d'application.
