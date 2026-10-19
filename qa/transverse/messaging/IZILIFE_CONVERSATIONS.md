# IziLife Conversations — socle transversal

## Intention

IziLife Conversations est le futur cœur de messagerie de la plateforme. Il ne
dépend ni de Booking ni de `ServiceRequestMessage`. Une conversation peut relier
des personnes et des entités IziLife dans un contexte métier précis ou sans
contexte :

- User ↔ User ;
- User ↔ Page, Shop, Place ou Event ;
- User ↔ établissement autour d’une Booking ;
- groupe ou support.

Booking est un premier consommateur, pas le propriétaire du chat.

## Séparation impérative avec Booking

La page d’une réservation reste la source de vérité métier.

- Côté client, elle affiche le statut et, lorsque la règle le permet, les
  actions **Annuler** et **Contacter le gérant**.
- Côté Partner Space, une demande en attente affiche **Accepter** et **Refuser**.
  Les autres actions dépendent ensuite du statut courant.
- `BookingStatusEvent` audite les transitions de statut.
- `BookingAttendanceIncident` audite les annulations tardives et absences.
- Le bouton **Contacter** ouvre la conversation liée à la Booking.

La conversation contextuelle peut afficher des bulles système synthétiques qui
racontent l'objet concerné (`BOOKING_CREATED`, acceptation, refus, annulation,
absence). Elles reflètent l'audit mais ne le remplacent pas. Les boutons et la
source de vérité du statut restent dans l'interface de réservation.

Une conversation directe sans contexte, ouverte par **Écrire** depuis la fiche
d'un établissement, ne reçoit aucune bulle métier. Une clé canonique calculée à
partir des deux acteurs garantit un seul fil durable User ↔ établissement,
indépendamment de celui qui reprend la conversation.

## Modèle de données

Le bloc canonique est à la fin de
`izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`.

- `IziConversation` : identité, nature, état et mode de chiffrement du fil.
- `IziConversationParticipant` : acteurs polymorphes (`USER`,
  `BOOKING_CUSTOMER`, `SHOP`, `PLACE`, `PAGE`, `EVENT`, etc.).
- `IziConversationContext` : zéro, un ou plusieurs contextes (`BOOKING`, `SHOP`,
  `PLACE`, etc.), avec un contexte principal.
- `IziConversationMessage` : messages serveur V1 ou ciphertext E2EE futur.
- `IziConversationMessageReceipt` : livraison et lecture.
- `IziConversationAttachment` : pièces jointes et métadonnées chiffrables.
- `IziConversationDevice` : clés publiques par appareil.
- `IziConversationKeyEnvelope` : clé de conversation chiffrée pour chaque
  appareil autorisé.

## Acteurs et représentation

Un acteur métier peut être une personne ou une entité. Le fait qu’un employé
Partner puisse parler pour un Shop ou un Place doit être contrôlé au point
d’entrée à partir de ses droits PS. Insérer un participant `SHOP` ne donne aucun
droit par lui-même à un employé.

Un invité Booking reste un `BOOKING_CUSTOMER`; la validation du lien privé de la
réservation est requise avant l’accès au chat. Il n’est jamais transformé en
`USER` par simple correspondance d’e-mail ou de téléphone.

## Chiffrement

La V1 peut fonctionner en `SERVER_MANAGED`. Le schéma prépare `E2EE` sans
prétendre que le chiffrement de bout en bout est déjà livré :

- clés d’identité par appareil ;
- enveloppe de clé de conversation par appareil et version ;
- ciphertext et nonce stockés sans corps lisible côté serveur ;
- rotation/révocation d’appareil possibles.

Une conversation E2EE refuse les corps serveur. La recherche plein texte,
modération et récupération multi-appareil devront être spécifiées avant
activation en production.

## API de domaine

`App\Libraries\Messaging\ConversationService` fournit la base commune :

- création d’une conversation, de ses participants et contextes ;
- message texte serveur ou payload E2EE ;
- idempotence via `client_message_id` ;
- contrôle strict de participation ;
- lecture et accusés ;
- appareil et enveloppe de clé.

Les contrôleurs FO et PS restent responsables de l’authentification, du CSRF,
des délégations d’entité et de l’exposition minimale des données.

## Premier branchement Booking

Une Booking confirmée automatiquement ne crée ni conversation Booking ni lien
de suivi. Une demande en attente crée une conversation contextuelle entre le
client (`USER` ou `BOOKING_CUSTOMER`) et l’établissement (`SHOP` ou `PLACE`).
Elle reçoit deux contextes : la Booking comme sujet principal et
l’établissement comme origine. Les changements importants peuvent y être
représentés par des bulles système non éditables. Depuis la fiche Booking, le
bouton **Contacter le gérant** ouvre cette conversation dans un modal/panneau JS ;
une future page autonome sera réservée à la route `chat/xxxxx`.

## Annulation tardive et no-show

Ce domaine est séparé du chat :

- l’annulation reste toujours possible ;
- à 60 minutes ou moins du début, elle crée un incident
  `LATE_CANCELLATION` ;
- après le début, le lieu peut déclarer `REPORTED_NO_SHOW`, plus pénalisant ;
- les incidents sont datés, attribués, motivables, contestables et annulables ;
- le score porte sur `USER` ou `BOOKING_CUSTOMER` ;
- une restriction est une décision distincte, temporaire et réversible.

La politique initiale est configurable dans `BookingAttendancePolicy` : fenêtre
de 365 jours, 1 point pour annulation tardive, 3 pour absence déclarée, blocage
temporaire de 30 jours à partir de 6 points. Ces valeurs sont une première règle
produit, pas des constantes cachées dans le PHP.

## Hors périmètre immédiat

- application mobile et push ;
- présence temps réel/WebSocket ;
- appels audio/vidéo ;
- chiffrement E2EE activé en production ;
- migration automatique de `ServiceRequestMessage` ;
- modération automatisée et pièces jointes exécutables.

