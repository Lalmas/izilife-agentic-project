# izilife - Roadmap priorisee Partner Space

Version de travail avant developpement. Ce document reformule et priorise les notes produit autour de l'espace Partner et des futures apps satellites.

## 1. Intention produit

L'espace Partner n'est pas un simple back-office adapte. Il doit devenir le cockpit des commercants, organisateurs et partenaires izilife. Il doit permettre de gerer leur presence, leurs lieux, leurs ventes, leurs reservations, leurs evenements, leurs produits, leurs avis et plus tard leurs messages et actions marketing.

L'ambition produit se rapproche d'un melange entre Google Business Profile, Deliveroo/Uber Eats, Tripadvisor, Shotgun et un assistant operationnel IA. La difference majeure avec le BO actuel est le scope: un partner et ses salaries ne doivent voir et modifier que ce qui leur appartient ou ce qui leur est explicitement autorise.

## 2. Surfaces produit a developper

### Priorite 1 - Partner Space

Application principale utilisee sur PC et mobile. Elle sert a administrer les objets metier du partner: lieux, shops, events, experiences, reservations, produits, services, paiements, employes et profil partner. C'est la priorite absolue.

### Priorite 2 - Kiosk tablette

Mini webapp tablette centree sur le live d'un lieu. Elle doit servir au commercant sur place pour gerer rapidement produits, paiements, evenements, activations/desactivations de services, commandes et etat operationnel du lieu.

### Priorite 3 - Event scanner / pod scanner

Webapp dediee au scan de tickets d'un event. L'objectif est de permettre la validation rapide des entrees, avec un format de donnees izilife controlable et difficilement reutilisable par un outil externe non autorise.

### Priorite 4 - Pad mobile de prise de commande

App ou webapp mobile/tablette pour prendre les commandes en salle, au comptoir, en terrasse ou sur event. Elle devient utile apres la base produits, menu digital, commandes et paiements.

### Socle transversal - WebSocket / notifications

Un serveur WebSocket generique sera necessaire pour notifier et synchroniser toutes les surfaces: front izilife, Partner Space, Kiosk, scanner, pad commande. Il ne faut pas le penser comme une feature isolee, mais comme une infrastructure partagee.

## 3. Decision de priorite actuelle

La priorite immediate n'est plus uniquement la gestion generique des objets. Il faut avancer plus tot sur la reservation et le menu digital pour les commerces, car ce sont des usages concrets et directement valorisables pour un partner.

Ordre recommande:

1. Stabiliser le Partner Space et le scope partner.
2. Lancer le socle commerce: lieu/shop, reservations, menu digital, produits.
3. Brancher paiements, PSP/Stripe et premiers flux de commande.
4. Ajouter EAP, services et objets vendables.
5. Reprendre events/experiences avec creation guidee et vente.
6. Ajouter temps reel, kiosk, scanner et pad mobile.
7. Ajouter presence en ligne, IA, voix et agents.

## 4. Phase 0 - Socle Partner Space

Objectif: disposer d'un espace propre, scoped partner, qui ne depend plus du fonctionnement BO sauf pour les parties explicitement reprises.

A faire:

- Authentification PartnerEmployee avec `partner_employee` et `partner_logged_in`.
- Navigation Partner Space propre.
- Profil partner et informations de base.
- Employes: invitation, choix mot de passe, roles, test des parcours.
- Controle des roles actuels, meme simple, avant d'ajouter des droits fins.
- Preparation du systeme de scope, sans bloquer le MVP.
- Verification que les anciens controllers/views/models BO ne restent pas accessibles ou utilises par erreur.

## 5. Phase 1 - Commerce: lieu, reservation, menu digital

Objectif: permettre a un commercant de gerer son lieu et ses reservations rapidement, puis d'afficher un menu digital exploitable.

### Lieu / Shop

- Voir mes lieux et mes shops.
- Ouvrir une fiche lieu/shop.
- Modifier les informations principales.
- Modifier horaires et horaires exceptionnels.
- Ajouter et gerer medias.
- Gerer les caracteristiques utiles.
- Valider ou corriger les informations ajoutees par des utilisateurs.
- Voir les avis du lieu et y repondre.

### Reservations

- Configurer simplement les reservations et privatisations.
- Ajouter une reservation manuellement.
- Lister les demandes et reservations.
- Gerer le delai minimum de reservation: par exemple 45 min, 1 h, etc.
- Gerer notifications SMS/push plus tard.
- Message personnalise: anniversaire, these, soiree entre amis, etc.
- Prevoir attribution de tables automatique ou manuelle.
- Gerer temps de rotation si attribution automatique.
- Gerer seuil maximum automatique: au-dela d'un nombre de personnes, basculer en appel ou demande.
- Permettre au partner de desactiver rapidement la reservation quand il est deborde.

### Tables et commandes a table

- Plan de tables simple: liste de tables, meme si certains bars ne l'utilisent pas.
- QR code par table.
- Cas bar/comptoir: le client peut commander sans table.
- Question au checkout: "Vous avez une table ?" oui/non.
- Possibilite de combiner des tables, par exemple table 1 + 2 pour creer une table de 8.
- Possibilite de figer des combinaisons.

### Menu digital / produits

- Gerer categories de produits.
- Ajouter/modifier produits.
- Gerer prix, disponibilite et options simples.
- Gerer allergenes et ingredients.
- Scanner un menu PDF pour creer une base produit avec IA plus tard.
- Traduire automatiquement les fiches produits pour les touristes plus tard.
- Generer descriptions produits via IA plus tard.

## 6. Phase 2 - Objets vendables: Products, EAP, Services

Objectif: clarifier ce qui est vendu, reservable, commandable ou simplement affiche.

Principes actuels:

- `Product`: produit au sens commerce/menu, distinct des tarifs d'acces.
- `ElementAccessPrice` / EAP: tarif, ticket, acces ou formule achetable pour un objet.
- `ElementService`: service offert ou vendu, parfois proche d'un EAP, parfois simple option non commandable.
- Services de reservation: slots ou services lies aux configurations de booking.

A gerer dans le Partner Space:

- Produits rattaches a un shop ou a un contexte event si besoin.
- EAP pour tickets, acces, formules, tarifs event/experience/place/equipment/animation.
- Services commandables et non commandables.
- Element News / promotions / happy hour / "en ce moment".
- Affichage front office degrade mais coherent pour lieu, event et experience.

## 7. Phase 3 - Events et Experiences

Objectif: permettre au partner de creer, vendre et suivre ses events et experiences sans devoir comprendre toute la complexite du modele izilife.

### Creation guidee

Un modal global de creation doit orienter le partner vers le bon type d'objet:

- Cours collectif recurrent toutes les semaines: Experience.
- Cours collectif ponctuel one-shot: Event.
- Evenement vendable avec tickets: Event.
- Activite continue ou sessionnable: Experience.
- Attraction/manège/parc: Animation selon l'historique du modele.
- Equipement ou ressource reservable: Equipment.

### Event

- Creer un event manuellement.
- Creer un event depuis lien Facebook plus tard.
- Creer un event depuis flyer avec OCR/IA plus tard.
- Configurer tickets et EAP.
- Activer la vente.
- Voir les reservations/ventes.
- Gerer remuneration simple ou multi-partner si necessaire.
- Gerer split paiement si plusieurs remunerations.
- Gerer objectifs de remplissage.
- Prevoir liste d'attente et tirage au sort plus tard.
- Gerer horaires specifiques des commerces pendant l'event.
- Ajouter produits d'un shop a un event.

### Experience

- Creer et modifier experience.
- Gerer sessions/recurrences.
- Gerer capacites, reservations et participants.
- Gerer le cas SCC: une occurrence recurrente devient session physique quand le partner agit dessus ou quand le BO a besoin de la materialiser.

## 8. Equipment et Animation

Equipment et Animation doivent rester separes techniquement pour respecter l'existant, mais l'UX partner doit masquer autant que possible cette complexite.

Historique:

- Animation a ete pensee pour les animations de foire, attractions, maneges, parcs d'attraction.
- Equipment est arrive ensuite pour les autres equipements ou ressources.

UX cible:

- Un seul espace ou modal de creation.
- Une union apparente des categories AnimationCategory et EquipmentCategory.
- Le systeme decide ensuite s'il cree un Equipment ou une Animation.
- Le partner gere l'objet sans devoir connaitre cette separation technique.

## 9. Paiement, PSP, Stripe et finances

Objectif: rendre les ventes possibles et comprehensibles.

A couvrir:

- Onboarding PSP/Stripe.
- Statut du compte de paiement.
- Conditions pour lancer une vente: partner onboarde, objet vendable, tickets/EAP configures, remuneration coherent.
- Event pret a vendre: tickets, capacite, paiement, split/remuneration si besoin.
- Finances partner: vision simple des ventes, paiements, remboursements et frais.
- Terminal/service account plus tard.
- Caisses et devices: cacher dans l'UX au debut, mais garder le terrain prepare.

## 10. Employes, roles, permissions et scope

Objectif: permettre a plusieurs salaries d'utiliser le Partner Space sans exposer tout le compte partner.

Court terme:

- Owner/admin/manager/staff selon roles existants.
- Invitation par email.
- Choix mot de passe.
- Modification profil employee: numero, mail, informations de base.
- Tests des parcours: ajout, transfert, conflit, annulation.

Moyen terme:

- Permissions par fonction: reservation, produits, events, finance, employes, settings.
- Scope par lieu/shop/event.
- Obligation de scope pour certains managers.
- Affichage automatique du perimetre d'acces.

Long terme:

- Partners multi-lieux en France ou Europe.
- Responsables par region, ville, network, shop ou type d'objet.

## 11. Temps reel, Kiosk, scanner, pad

Ces apps doivent etre pensees apres le socle commerce, mais leurs besoins influencent les choix techniques.

### WebSocket generique

- Notifications reservation.
- Notification commande.
- Paiement valide/echec.
- Ticket scanne.
- Changement de statut d'un event ou d'un service.
- Synchronisation Partner Space, FO, Kiosk, scanner et pad.

### Kiosk tablette

- Gerer le lieu en live.
- Activer/desactiver reservation, commande, menu, services.
- Voir commandes/paiements.
- Gerer produits disponibles.
- Gerer events du lieu.

### Scanner event

- Connexion partner/employee.
- Liste des events accessibles.
- Scan ticket.
- Validation offline/online a definir.
- Format QR/code izilife specifique.
- Historique des scans.

### Pad commande

- Prise de commande mobile.
- Table, comptoir, terrasse, event.
- Paiement ou envoi en cuisine/bar selon flux futur.

## 12. Presence en ligne et IA

Vision long terme: centraliser la presence en ligne du partner.

Modules envisages:

- Google Business Profile.
- Instagram.
- Facebook.
- WhatsApp.
- Avis Google/Tripadvisor/izilife.
- Messages entrants.
- Analyse et reponse assistee par IA.
- Creation de posts et flyers.
- Import d'event depuis Facebook.
- OCR flyer vers event.
- Generation de descriptions.
- Traduction automatique des objets et produits.
- Interface agentique type chat izilife.
- Commandes vocales: creer reservation, event, produit, description, image.

Exemple d'usage prioritaire a garder en tete:

Le commercant recoit un appel pour une reservation de 9 personnes. Il clique sur le micro et dit: "cree une reservation pour 9 personnes au nom de X le jour Y a Z heures". Le systeme reconnait la voix, cree la reservation et prepare la notification.

## 13. Priorisation MVP

### MVP A - Partner Space commerce

1. Auth partner employee propre.
2. Liste et fiche lieu/shop.
3. Edition informations, horaires, medias.
4. Reservation simple: config, ajout manuel, liste.
5. Menu digital: categories, produits, prix, disponibilite.
6. PSP/Stripe statut minimal.
7. Navigation mobile/desktop exploitable.

### MVP B - Reservation avancee et commande

1. Tables et QR codes.
2. Commande a table ou sans table.
3. Activation/desactivation rapide quand le lieu est deborde.
4. Notifications de reservation/commande.
5. Paiement lie au flux.

### MVP C - Events/Experiences vendables

1. Creation guidee Event vs Experience.
2. Tickets/EAP.
3. Activation vente.
4. Reservations/participants.
5. Scanner basique.

### MVP D - Apps satellites

1. Kiosk tablette lieu live.
2. Pad commande mobile.
3. Scanner event complet.
4. WebSocket generalise et durci.

### MVP E - IA et presence en ligne

1. Import event par lien/flyer.
2. Menu PDF vers produits.
3. Descriptions et traductions.
4. Reponses aux avis.
5. Commandes vocales.
6. Agent marketing/post/flyer.

## 14. Points a ne pas oublier

- Le Partner Space doit cacher la complexite du BO, pas la recopier.
- Les objets izilife sont multi-domaines: Place, Shop, Event, Experience, Circuit, Equipment, Animation, Product, EAP, ElementService, Booking, Review.
- Les parcours doivent partir des intentions du commercant: vendre, reserver, afficher, publier, encaisser, repondre, gerer le live.
- Le BO reste la source de nombreuses fonctions, mais l'UX partner doit etre adaptee.
- Les vieux controllers BO ne doivent pas redevenir la surface utilisateur par accident.
- Les features caisses/devices/terminal peuvent etre preparees mais cachees tant qu'elles ne sont pas pretes.
- La reservation et le menu digital sont maintenant prioritaires avant une couverture complete de tous les objets.
