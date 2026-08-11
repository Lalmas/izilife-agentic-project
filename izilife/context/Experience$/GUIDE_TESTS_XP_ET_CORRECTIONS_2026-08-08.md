# Guide de test — Experience, billetterie et corrections associées

Dernière mise à jour : 8 août 2026.

Ce guide complète le PDF de recette existant. Il décrit les changements ajoutés ou précisés pendant la reprise du chantier.

## 1. SQL du chantier

La structure générale existe déjà. Ne rejouer aucun gros script de construction.

Les évolutions réellement nouvelles sont regroupées à la fin de :

`izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`

Les colonnes `access_mean`, `occupancy_mode` et les champs BPR étaient déjà présentes dans `020_New_Entities.sql` : elles n'ont pas été dupliquées. Le bloc ajouté à `021_Next_Improves.sql` contient `participation_mode`, le rattachement minimal Event/Experience à Community/UserGroup et la table `CommunityRSVP`.

## 2. Parcours Experience à tester

### A. Experience informative gratuite

Configuration : `Libre & Gratuit`, aucune billetterie iziLife, planning récurrent.

Attendu :

- aucun formulaire, aucun compteur et aucun achat à 0 € ;
- résumé lisible de la récurrence dans « Séances / Réservation » ;
- cartes des prochaines séances ;
- cartes de tarifs informatives si des tarifs externes sont renseignés ;
- contact ou lien externe ;
- aucune création de Transaction, Ticket ou Booking.

### B. Experience payante externe

Configuration : prix payant mais `use_izilife_paiement = 0`.

Attendu :

- comportement informatif ;
- horaires, lieu et tarifs visibles ;
- aucun checkout iziLife ;
- lien externe autorisé si présent ;
- une requête POST forgée vers PayHub doit être refusée.

### C. Achat `NO_DATE`

Configuration : billetterie iziLife, réservation non requise.

Attendu :

- aucun calendrier et aucune séance à choisir ;
- EAP affichés directement ;
- paiement interne normal ;
- création d'une Transaction et des Tickets ;
- aucun Booking daté.

Cas « une seule Experience » : mettre un unique EAP avec `maximum_quantity_per_user = 1`.

Attendu : l'EAP est présélectionné à une unité et aucun compteur `- / +` n'est affiché. Le serveur refuse une quantité supérieure.

### D. Date d'arrivée

Configuration : `ARRIVAL_DATE`.

Attendu :

1. calendrier seul ;
2. après sélection du jour, affichage des EAP ;
3. réservation/paiement ;
4. Booking portant le jour choisi.

### E. Séance avant paiement

Configuration : disponibilité `SESSION`, choix avant paiement.

Attendu :

1. choix de la date ;
2. affichage des séances de ce jour seulement ;
3. choix d'une séance ;
4. affichage des EAP seulement après la séance ;
5. réservation/paiement.

Une date dont toutes les séances sont pleines doit être indiquée « Complet » et désactivée. Une séance pleine doit rester visible, grisée/rouge et non sélectionnable. Vérifier aussi le refus serveur si la dernière place est prise dans un autre navigateur avant validation.

### F. Achat puis planification

Configuration : choix après paiement avec délai positif et unité.

Attendu :

- achat immédiat de l'EAP ;
- Transaction et Tickets créés sans Booking ;
- QR masqué tant que la planification n'est pas faite ;
- bouton « Choisir ma date » dans « Mes réservations » ;
- écran date puis séance si la disponibilité est `SESSION`, ou calendrier seul pour `ARRIVAL_DATE` ;
- création du Booking et rattachement des Tickets après validation ;
- refus après l'échéance ;
- refus d'une séance située après l'échéance.

## 3. Gratuit sur réservation iziLife

Attendu :

- EAP à 0 € ;
- aucune ouverture PSP ;
- Transaction à montant nul pour tracer l'opération ;
- Booking si une capacité/date/séance est réservée ;
- Ticket gratuit et QR code ;
- apparition dans « Mes activités/réservations ».

## 4. Sessions récurrentes et exceptions

Créer une configuration courante, puis tester :

- activation d'une configuration ne couvrant que certains jours, par exemple mardi et jeudi ;
- refus d'une configuration sans aucun horaire actif ;
- jours fixes avec une heure unique ;
- plusieurs heures explicites ;
- répétition par intervalle entre une heure de début et de fin ;
- configuration temporaire sur une plage de dates avec nouvelle récurrence ;
- période temporaire ne contenant aucune séance ;
- retour automatique à la récurrence courante après la période ;
- Session matérialisée modifiant une occurrence SCC ;
- Session `status = 0` annulant une occurrence ;
- deux occurrences parallèles de sources différentes au même horaire.

La période temporaire applicable doit toujours prendre la priorité, même si elle est vide. La configuration spécifique la plus récemment mise à jour gagne lorsque plusieurs périodes se chevauchent.

## 5. Capacités, limites et groupes

Tester séparément :

- capacité de Session manuelle ;
- `max_capacity` d'un SCC ;
- mode `PRIVATE_GROUP` : la première réservation rend le créneau complet ;
- `Experience.participation_mode = individual` avec minimum et maximum par réservation ;
- `private_group` avec taille minimale/maximale ;
- `open_group`, dont la capacité réelle reste celle de la séance ;
- `maximum_quantity_per_user` d'un EAP ;
- deux navigateurs tentant la dernière place.

## 6. Packs Experience

Tester :

- pack composé d'au moins deux EAP simples ;
- quantité consommée = nombre de packs × quantité de chaque composant ;
- stock propre du pack ;
- stock de chaque composant ;
- `maximum_quantity_per_user` limitant le nombre de packs ;
- ordre stable des tarifs groupés ;
- création d'un Ticket par admission réelle, avec métadonnées du pack.

## 7. Fulfillment et reprise

Attendu :

- une transaction non payée ne peut pas être réclamée ;
- `fulfilled_at` protège contre un double fulfillment ;
- si la transaction SQL Booking/Ticket échoue, toutes les écritures métier sont annulées ;
- le paiement reste validé ;
- `fulfilled_at` est libéré pour permettre une reprise contrôlée ;
- un nouvel appel peut terminer le fulfillment sans doubler les Tickets.

## 8. BO central et partenaire

Dans chacun des deux BO :

- ouvrir une Experience ;
- ouvrir le bloc « Parcours de vente » directement dans la fiche, sans bouton vers une page séparée ;
- vérifier que les deux champs de billetterie restent dans « Informations principales » ;
- choisir un lieu de séance par son nom via l'autocomplétion Place/Shop ;
- saisir une adresse ponctuelle et vérifier le remplissage de latitude/longitude après sélection d'une adresse française ;
- enregistrer moyen d'accès et méthode de réservation ;
- vérifier que le choix après paiement exige un délai positif et une unité ;
- vérifier qu'un identifiant AccessMean ou BookingMethod forgé est refusé ;
- créer/modifier un EAP Experience ;
- vérifier les règles gratuit/informatif ;
- créer un pack et vérifier que le contexte Experience est conservé.

Aucune route explicite n'est nécessaire pour ces écrans.

## 9. Autres corrections à retester

### Navigation

- bureau : navigation supérieure toujours visible ;
- mobile : navigation masquée à l'arrivée, swiper d'intentions collé en haut, navigation flottante révélée au premier scroll.

### What To Do

- ouvrir une catégorie parente, par exemple « Boire » ;
- ouvrir une sous-catégorie, par exemple « Apéro » ;
- vérifier que « Boire » reste visuellement sélectionné.

### Home, campagnes et Placement

- vérifier les blocs utilisant `Placement` et l'absence de requête vers l'ancienne table Sponsorship ;
- campagne « musées gratuits le premier dimanche » visible dix jours avant ;
- visible le dimanche concerné ;
- absente dès le lundi ;
- tester une campagne sans récurrence avec ses dates statiques.

### BenefitPolicyRule

- règle avec plusieurs valeurs « Disponible pour » ;
- choix de catégorie obligatoire pendant une utilisation sur place ;
- catégorie autorisée acceptée ;
- catégorie forgée refusée côté serveur ;
- contraintes de jours, heures, plages interdites et heure limite toujours appliquées.

## 10. Éléments encore à livrer avant clôture complète de la mission

### CommunityRSVP

Le PDF place explicitement le RSVP dans la mission. Son SQL minimal est défini à la fin de `021_Next_Improves.sql`. Le FO vérifie maintenant l'adhésion existante et propose Oui / Non / Peut-être sur les occurrences. Un visiteur non connecté est renvoyé vers la connexion ; un utilisateur connecté peut rejoindre une communauté active et revendiquée, puis rejoindre ses groupes. Une communauté inactive ou non revendiquée reste visible à titre informatif, sans adhésion ni RSVP.

Contrat retenu pour la suite :

- `members_only` : adhésion et éventuelle approbation avant RSVP ;
- `join_to_attend` : Experience publiquement visible, adhésion obligatoire pour participer ;
- `guests_allowed` : RSVP invité sans accès aux contenus privés.

Le bouton « Rejoindre le groupe » ne doit pas encore créer une adhésion : ce workflow sera branché avec la gestion complète des communautés.

### Tests supplémentaires — horaires, exceptions et modèles

1. XP informative sans communauté : vérifier que la phrase « Le mardi et le jeudi à 19:00 » et le lieu s'affichent, mais pas la liste de dates jusqu'en novembre.
2. XP avec billetterie iziLife : vérifier date, séance, puis EAP ; les dates/séances complètes doivent être désactivées.
3. XP liée à un groupe : membre connecté = cartes avec Oui / Peut-être / Non ; anonyme = bouton Participer ; connecté non membre = message pour rejoindre.
4. BO, configuration temporaire : créer une configuration date-à-date, l'activer et vérifier qu'elle remplace la courante uniquement pendant cette période.
5. BO, contenu SCC, bouton calendrier barré : annuler une occurrence, puis déplacer une autre. Vérifier que l'origine disparaît, que le déplacement apparaît et que la récurrence suivante revient normalement.
6. BO, bouton « Déclinaison locale » : créer « Blabla Run – Paris ». Vérifier que la nouvelle XP est inactive, sans séances, lieux, tarifs ni communauté, mais conserve descriptions et taxonomies.
7. Sur une XP multi-lieux, vérifier que le lieu précis vient de la Session/SCC. `meet_place`/`meet_shop` ne doivent servir qu'aux anciennes XP sans lieu opérationnel.

### Géolocalisation Circuit

Un circuit n'est pas remonté dans une ville uniquement parce que sa trace GPX la traverse. La règle reste fondée sur son point de départ. Aucun élargissement géographique n'est inclus dans ce lot.

### PSP split

Le split au moment du paiement reste désactivé. `split_plan` est uniquement conservé comme photographie comptable pour un traitement ultérieur.
# Tests ajoutés le 9 août 2026

1. Depuis chaque liste BO Place, Shop, Event et Experience, cliquer sur `Ajouter` sans passer par une ville.
2. Vérifier qu'une ville tapée mais non sélectionnée est refusée.
3. Sélectionner Lille et créer l'objet ; contrôler que `city_id`, `city` et `zip_code` correspondent à la ligne City de Lille.
4. Modifier la ville : annuler d'abord l'alerte et vérifier qu'aucune sauvegarde ne part, puis confirmer et contrôler la mise à jour cohérente.
5. Pour une Experience Lille avec `locations_by_session`, créer une SCC à Seclin : l'Experience doit rester rattachée à Lille et la carte de cette séance doit afficher Seclin.
6. Créer une Community avec un administrateur choisi par autocomplétion : contrôler la création de `Général` et les deux adhésions.
7. Rattacher une Experience à un groupe : le FO doit afficher un seul organisateur, sous la forme `Groupe · Community`.
# Recette Communauté Test / Blabla Run

1. Exécuter la partie nouvelle de `021_Next_Improves.sql`, notamment
   `CommunityRSVP`, `CommunityActivity`, `SessionRecurrenceOverride`, les ALTER
   de Community, puis le jeu de test final.
2. Vérifier dans le BO que `Communauté Test` possède `Général`, que le user 2 est
   membre accepté et que Blabla Run est rattachée à ce groupe.
3. Ouvrir `/community/page/communaute-test` déconnecté : fiche, liens et agenda
   sont visibles, mais le RSVP demande la connexion.
4. Connecté avec le user 2 : répondre Oui, Peut-être puis Non sur une occurrence
   Blabla Run et vérifier l'upsert dans CommunityRSVP, sans doublon.
5. Avec un autre user : rejoindre la communauté, vérifier le toast et l'ajout à
   Général si la politique est `open`; tester l'état en attente avec `request`.
6. Désactiver la communauté : la page informative reste visible, adhésion et
   RSVP disparaissent.
7. Créer une pause SCC datée : les occurrences disparaissent de la fiche XP et
   de l'agenda communautaire. La récurrence reprend après la période.
8. Créer une pause annuelle juillet–août : aucune occurrence n'est affichée sur
   ces mois, y compris l'année suivante.
9. Déplacer une occurrence sans Booking : aucune Session métier inutile.
10. Déplacer/annuler une occurrence avec Booking et l'option de matérialisation :
    vérifier Session, disparition/déplacement, puis courriel aux inscrits.
11. Activer la billetterie iziLife sur l'XP : elle doit reprendre la priorité et
    les contrôles RSVP ne doivent plus être proposés.
