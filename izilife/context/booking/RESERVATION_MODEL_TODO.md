# Réservations — décisions métier et TODO

## Contrat retenu pour `TABLE`

- `BookingConfiguration.min_party_size` et `max_party_size` bornent la taille d'une réservation individuelle.
- Le seuil d'auto-confirmation n'appartient pas à `BookingConfiguration` : il est porté par la configuration d'acceptation stockée dans sa table dédiée. Jusqu'à ce seuil iziLife peut confirmer automatiquement ; au-dessus et jusqu'au maximum de la BC, la demande reste possible mais doit être validée par le lieu.
- La politique est désormais matérialisée par `BookingAcceptancePolicy`, liée à la BC. Les colonnes historiques de `BookingConfiguration` restent temporairement synchronisées uniquement pour la compatibilité avec les anciennes écritures ; le résolveur lit la politique dédiée en priorité.
- Le lieu configure ces deux limites. `max_party_size` ne doit jamais être utilisé comme seuil implicite d'acceptation automatique.
- Une durée moyenne de 90 minutes est proposée par défaut dans le formulaire de configuration. Elle doit être visible, modifiable et explicitement enregistrée par le lieu ; le FO ne doit pas inventer silencieusement cette valeur.
- Pour `TABLE`, le champ `BookingConfigurationContent.duration` est présenté sous le libellé métier « Durée moyenne d'occupation ». Un restaurant ou un bar peut saisir 90, 120, 180 minutes, etc.
- Cette durée permet d'estimer une occupation et de produire des alertes intelligentes sur les plages qui se chevauchent.
- Pour `TABLE`, `max_people_per_slot` n'est pas utilisé : `online_capacity` est le seuil normal au-delà duquel la validation devient manuelle et `online_capacity_hard_limit` est le plafond absolu qui grise le créneau. Le calcul porte sur les réservations qui chevauchent la durée visible de la BCC.
- `max_people_per_slot` reste réservé aux parcours à départ fixe (`EQUIPMENT`, `SERVICE`, `STANDARD/FIXED_SLOT`) où chaque créneau possède sa propre jauge.
- La capacité générale de l'établissement reste une information distincte de la limite d'une réservation.
- « Réserver quelques tables » et les parcours de privatisation restent indépendants. Dépasser le maximum de la BC `TABLE` ne transforme jamais automatiquement la réservation en privatisation.

## Capacités et scopes

- Capacité physique globale : capacité totale du lieu, toutes zones confondues.
- Capacité d'une catégorie de réservation : capacité propre à une cible telle que Bar ou Restaurant dans une configuration multi-catégories.
- Capacité d'un service : capacité ouverte à la réservation pour Service 1 ou Service 2 ; elle peut être inférieure à la capacité physique de la catégorie.
- Exemple : lieu 300, Bar 100 sans services, Restaurant 100 avec deux services. La capacité Bar/Restaurant appartient au ciblage de catégorie de la BC ; la capacité éventuellement différente de chaque service appartient à sa BCC.
- La capacité proposée en ligne peut être inférieure à la capacité physique afin de conserver des places pour les clients sans réservation.
- À terme, priorité de lecture : capacité du service/BCC > capacité de la catégorie ciblée > capacité physique du lieu.

## Suspension et indisponibilités temporaires

- Conserver la possibilité de mettre les réservations en pause pour une journée entière.
- Ajouter la désactivation d'un ou plusieurs créneaux sélectionnés, sans suspendre toute la journée.
- Une indisponibilité doit cibler explicitement le lieu, une BC/BCC, un équipement ou une liste de créneaux, avec début, fin et motif facultatif.
- Le FO doit recalculer immédiatement les disponibilités et ne plus présenter les créneaux suspendus.

## Contrat à préparer pour `EQUIPMENT` et les loisirs

- La durée et la capacité simultanée redeviennent opérationnelles lorsque l'activité ou l'équipement possède une durée connue.
- Les valeurs de BC/BCC peuvent surcharger les valeurs générales de l'équipement.
- Priorité envisagée, à confirmer avant implémentation : `BookingSlot` > `BookingConfigurationContent` > `Equipment`.
- Une surcharge absente hérite de la valeur du niveau inférieur ; une valeur explicite ne doit jamais être confondue avec une capacité d'établissement.

## Composition horaire facultative d'une BCC

- Ne pas coder les notions « midi » ou « soir » : elles résultent uniquement des horaires configurés.
- Une BCC représente toujours un jour ou un groupe de jours partageant les mêmes règles générales. Un indicateur explicite `is_composable` active facultativement une composition ordonnée de segments horaires.
- `is_composable = 0` : comportement historique strict. La BCC porte elle-même toute la planification et aucun segment n'est consulté.
- `is_composable = 1` : la BCC conserve les règles communes — jours, durée, capacités, préavis, remplissage et autres contraintes — tandis que ses segments portent les différentes portions de planification de la journée.
- Ne pas introduire un nouvel enum concurrent `INTERVAL`, `FIXED_TIMES`, `SERVICE`. Chaque segment réutilise la même sémantique et les mêmes champs de planification que la BCC : `repetition_type`, `repetition_time`, unité de mesure, heures fixes, `have_multi_services`, `have_slots_in_services` et bornes horaires.
- Le code de résolution doit appeler le même interpréteur de planification pour une BCC simple et pour chaque segment d'une BCC composable ; seule la source des champs change.
- Exemple valide dans une seule BCC : deux services de 12 h à 14 h, des créneaux cadencés l'après-midi, puis des services de 18 h à 23 h.
- Ajouter une table enfant de composition, provisoirement nommée `BookingConfigurationContentSegment`, plutôt que dupliquer plusieurs BCC portant les mêmes jours, capacités, durée et préavis.
- Les heures fixes et services peuvent réutiliser `BookingSlot`, complété par un rattachement facultatif au segment. Les données historiques sans segment conservent leur comportement actuel.
- `Booking` conserve obligatoirement `booking_conf_content_id` et reçoit un identifiant de segment facultatif. La date, le début, la fin et l'éventuel `booking_slot_id` restent les valeurs contractuelles de la réservation ; supprimer ultérieurement un segment ne réécrit jamais les réservations existantes.
- L'action « supprimer » désactive le segment (`is_active = 0`) dès qu'il est référencé par une réservation ; aucune suppression physique en cascade n'est autorisée sur l'historique.
- Une BCC marquée composable doit posséder au moins un segment actif avant publication. À l'inverse, la présence accidentelle de segments inactifs ne modifie jamais une BCC non composable.
- Les segments actifs d'une BCC ne peuvent pas se chevaucher. Une fin égale au début du segment suivant est autorisée. Le serveur applique cette règle, indépendamment du JavaScript.
- Tous les segments restent intersectés avec les horaires et fermetures réelles de l'établissement. Ils ne peuvent jamais créer une disponibilité pendant une fermeture.
- Pour une date donnée, le FO résout la BCC puis ses segments dans l'ordre chronologique : pills générées pour une cadence, pills explicites pour des heures fixes, et libellés de services pour les segments de service.
- Le mode service concerne uniquement la présentation d'une réservation classique ou de tables ; il n'est pas présenté au client pour une privatisation du lieu ou d'un équipement.
- BO : le bouton « Composer les horaires », le modal et la liste ordonnée des segments sont branchés sur les BCC.
- PS : la même interaction métier est branchée dans ses composants propres, avec mutations POST/CSRF et contrôle serveur des chevauchements.
- Le cas courant ne montre pas cette complexité : tant que le partenaire n'active pas la composition avancée, il continue à configurer une BCC simple comme aujourd'hui.
- Une privatisation utilise sa propre heure de début. Tant que l'heure de fin n'est pas gérée, sa période d'occupation est estimée avec la constante métier de quatre heures, ni déduite de la fermeture ni configurable dans cette première version.

## TODO — occupation et exclusivité

- Introduire un état de disponibilité des équipements : libre, occupé, suspendu ou privatisé.
- La privatisation d'un équipement rend indisponibles les ressources qu'il contient pendant toute la période concernée, par exemple toutes les tables d'une salle.
- La privatisation de l'établissement rend indisponibles les parcours de réservation du lieu qui chevauchent sa période.
- Si une privatisation ne possède pas encore une période suffisamment précise, le lieu doit pouvoir appliquer l'indisponibilité à toute la journée.
- Les contrôles doivent être centralisés afin que le FO, le Partner Space et les futures sources de réservation réagissent au même état.
- Prévoir une hiérarchie explicite : privatisation du lieu > privatisation d'un espace > suspension manuelle > disponibilité BC/BCC > disponibilité des ressources.

## Filtrage dynamique des cartes FO

- Les cartes sont recalculées dès que la date ou le nombre de participants change.
- Si le nombre est inférieur au minimum : afficher « Minimum X participants » et rendre la carte indisponible.
- S'il dépasse le maximum : afficher « Maximum X participants » et rendre la carte indisponible.
- Si les bornes sont respectées mais qu'aucune disponibilité n'existe : afficher « Indisponible à cette date ».
- Une carte indisponible ne doit pas ouvrir son formulaire ; les autres options restent évaluées indépendamment.
- Dans le détail d'une option, un créneau fermé, suspendu, complet ou devenu incompatible reste visible mais grisé, avec son motif si celui-ci est connu, et ne peut jamais être sélectionné.
- La première version du FO doit comprendre cet état d'indisponibilité sans attendre l'interface de suspension manuelle par journée ou par lots de créneaux.
- Employer « Privatisation gratuite » pour une privatisation sans frais de réservation, afin de ne pas confondre l'acte de privatiser avec une réservation de tables.

## Modèle candidat — privatisation

Une configuration de privatisation dédiée (`PrivatizationConfiguration`, nom définitif à valider) doit pouvoir cibler :

- l'établissement entier ;
- un équipement/espace privatisable, par exemple Salle Cosy ou Salle Principale.

Elle porte ses propres informations, indépendamment des BC de réservation :

- minimum et maximum de participants ;
- acte de privatisation gratuit ou payant ;
- éventuel minimum de consommation, total ou par personne ;
- devise ;
- publication, pause et disponibilité ;
- plus tard, durée ou heure de fin permettant de calculer l'exclusivité réelle.

Un équipement de type salle peut exister sans condition commerciale lorsqu'il sert seulement de préférence de placement dans « Réserver quelques tables ». Ses conditions de minimum, maximum et consommation ne s'appliquent que lorsqu'il est présenté comme option de privatisation.

## Conditions commerciales de `TABLE`

- Retenir un modèle simple pour la première version : « Réserver quelques tables » possède seulement un minimum, un maximum et un seuil d'auto-confirmation.
- Ne pas ajouter de tranches commerciales du type « 1–9 sans engagement, 10–20 avec minimum de consommation ». Leur combinaison avec les configurations globales, multi-catégories et catégories séparées rendrait le Partner Space inutilement complexe.
- Dans la plage autorisée par la BC, la demande de réservation de tables est gratuite et sans minimum de consommation. Le seuil d'auto-confirmation peut toutefois faire passer les groupes plus importants en validation manuelle.
- La capacité de la salle ou de la catégorie ne définit pas automatiquement le maximum d'une réservation individuelle.
- Un équipement Salle utilisé comme simple préférence de placement ne porte aucune condition commerciale.
- Les conditions commerciales restent propres aux privatisations : établissement entier ou équipement/espace explicitement privatisable.
- Le BO et le Partner Space doivent permettre de configurer, pour chaque privatisation, les bornes de participants, la gratuité ou le paiement de l'acte, l'éventuel minimum de consommation total ou par personne, la devise, la publication et la pause.
- Le ciblage multi-catégories reste porté par la BC : une configuration peut concerner le lieu, plusieurs catégories ensemble ou des catégories séparées, sans dupliquer des règles commerciales `TABLE` par tranche de participants.
- Le regroupement de catégories n'est proposé que pour mutualiser exactement le même parcours, les mêmes horaires et les mêmes règles. Exemple : une seule BC `TABLE` partagée par Bar et Restaurant, tandis que Loisir conserve sa propre BC `STANDARD` ou `EQUIPMENT`.
- Ce regroupement reste utile pour un établissement réellement mixte. Une BC `TABLE` globale convient si toutes les activités du lieu partagent ce parcours ; elle ne convient pas à Bar + Restaurant + Loisir, car elle rendrait implicitement le Loisir réservable comme une table. Dans ce cas, une seule BC `TABLE` ciblant Bar et Restaurant évite deux configurations dupliquées sans englober Loisir.
- Dès que deux catégories ont des horaires, capacités, services ou modes de réservation différents, elles doivent être séparées. « Regrouper » ne signifie jamais additionner leurs capacités ni fusionner implicitement leurs disponibilités.

## Portée des BC et configuration sans ambiguïté

- L'unicité de la configuration courante s'applique à toutes les cibles. Une cible peut conserver plusieurs BC en base pour les brouillons, l'historique ou la préparation d'une relève, mais une seule peut être `is_current = 1` et utilisable à un instant donné.
- Pour la cible établissement : une seule BC courante au total.
- Pour une catégorie : elle ne peut être couverte que par une seule BC courante ; deux BC courantes ne peuvent donc pas contenir la même catégorie, même si l'une cible un groupe de catégories.
- Pour un équipement : une seule BC courante par équipement. Plusieurs versions de sa configuration peuvent exister, mais elles ne sont jamais utilisables simultanément.
- Une BC courante n'est réellement proposée au FO que si elle est également active, publiée, non suspendue, dans sa période d'application et autorisée par le droit d'abonnement. `is_current` désigne la version retenue ; il ne remplace pas ces contrôles.
- Le choix de portée appartient à l'établissement entier, et non à chaque `booking_kind` : `GLOBAL` ou `BY_CATEGORY`.
- La cible « établissement » n'accepte qu'une seule `BookingConfiguration` active et courante au total, quel que soit son `booking_kind`, que le lieu soit mono-catégorie ou multi-catégories.
- Dès qu'une première BC est rattachée à une ou plusieurs catégories, l'établissement passe en mode `BY_CATEGORY`. Les BC de lieu/catégorie suivantes doivent alors posséder au moins une catégorie cible ; aucune BC active et courante directement rattachée au lieu ne peut coexister.
- Réciproquement, l'unique BC active et courante du lieu empêche le passage silencieux au mode catégoriel. Le partenaire doit engager explicitement la conversion de portée, avec contrôle ou réaffectation de cette BC.
- En mode `BY_CATEGORY`, plusieurs BC peuvent exister, mais leurs ensembles de catégories doivent être disjoints pour un même `booking_kind` : une catégorie ne peut appartenir qu'à une BC active/courante de ce type et de la même période d'application.
- Une catégorie non affectée n'est simplement pas réservable par ce parcours. Il n'est pas nécessaire de créer une configuration vide.
- Plusieurs natures de parcours restent possibles en mode catégoriel : une ou plusieurs BC `TABLE` et des BC `STANDARD`, chacune rattachée à sa ou ses catégories.
- Les BC `EQUIPMENT` ne sont pas comptées dans l'unicité de la cible établissement : elles ciblent un équipement identifié, conservent son `equipment_id` et utilisent les droits/accès de cet équipement. Elles peuvent donc coexister avec l'unique BC du lieu ou avec les BC catégorielles.
- L'interface ne présente pas une matrice. Dans le bloc « Réservation de table », le partenaire choisit d'abord « Une configuration pour tout le lieu » ou « Des configurations différentes selon les catégories ».
- En mode catégoriel, le bouton d'ajout crée une carte nommée d'après sa cible : « Réservation de table — Bar et Restaurant » ou, lorsque les règles diffèrent, « Réservation de table — Bar » et « Réservation de table — Restaurant ».
- Les catégories déjà utilisées par une carte ne sont plus proposées dans les autres cartes du même parcours. Une modification qui créerait un chevauchement est refusée côté serveur également.
- Au FO, une BC `TABLE` commune à plusieurs catégories reste une seule option publique intitulée « Réserver une table ». Les catégories ciblées servent à la résolution métier et ne doivent ni dupliquer la carte ni apparaître comme un choix technique dans le parcours.

## Nature du parcours et portée

- `booking_kind` et portée sont deux axes indépendants.
- `STANDARD` ne signifie pas « rattaché au lieu ». Il signifie que le client réserve un créneau et un nombre de participants sans sélectionner ni allouer une table, un équipement, un service, une chambre ou un siège.
- Une BC `STANDARD` peut donc être l'unique BC active et courante directement rattachée au lieu en mode `GLOBAL`, ou être rattachée à une catégorie d'activité en mode `BY_CATEGORY`.
- Une BC `STANDARD` précise son mode d'accès aux créneaux : `ARRIVAL_TIME` lorsque l'heure choisie est une heure d'arrivée et que la présence est estimée pendant la durée de la BCC ; `FIXED_SLOT` lorsque chaque créneau possède sa propre jauge et est compté indépendamment.
- Ces deux valeurs ne sont jamais appelées « session ». Dans le modèle iziLife, les sessions restent réservées aux XP et au cinéma, avec `SessionConfiguration`, SCC et sessions manuelles.
- `TABLE` se comporte toujours comme une heure d'arrivée. Pour ce chantier, `EQUIPMENT` et `SERVICE` conservent une jauge par créneau. Aucun sélecteur générique « rolling/session » n'est exposé dans les BCC.
- `TABLE` décrit le parcours de réservation de tables ; `EQUIPMENT` décrit la réservation d'une ressource identifiée. Leur rattachement au lieu ou à une catégorie obéit séparément au mode de portée de l'établissement.

## Portée de la politique d'acceptation

- La table dédiée à l'acceptation, aujourd'hui limitée à l'établissement, doit évoluer pour cibler une `BookingConfiguration`.
- La relation attendue est une politique d'acceptation par BC, et non une politique par catégorie liée à cette BC.
- Une BC `TABLE` ciblant Bar et Restaurant possède donc une politique commune. Deux BC `TABLE` séparées pour Bar et Restaurant possèdent deux politiques indépendantes.
- Dans le BO et le Partner Space, cette politique apparaît dans le détail dépliable de la carte BC — le bloc ouvert par l'œil — avec le mode automatique, manuel ou selon seuil et la valeur du seuil.
- La résolution FO part toujours de la BC sélectionnée puis lit sa politique d'acceptation ; aucune politique globale d'établissement ne doit venir la surcharger implicitement.

## Modal — réservation de quelques tables

- Réutiliser exactement les composants date et participants de la page dans le modal.
- Toute modification dans le modal recalcule immédiatement les créneaux et l'état des cartes.
- Employer une alerte `info` ou `warning` lisible.
- Le créneau sélectionné reste visible et clairement actif dans la liste.
- Conserver les pills horaires ; afficher les suivantes progressivement si la liste est longue.
- Proposer la préférence de placement parmi les espaces éligibles (Salle 1, Salle 2, Terrasse, Cave avec tables, espace VIP), sans garantir contractuellement l'affectation.
- Uniformiser la hauteur du pays et du téléphone.
- Alimenter dynamiquement le placeholder et la validation du téléphone à partir du pays avec le mécanisme déjà utilisé à l'inscription.
- Afficher tous les pays ; le choix du canal SMS ou e-mail reste une décision du moteur OTP.
- Placer « Partager mes coordonnées avec cet établissement » sous les blocs d'identité avec une présentation compacte.
- Retirer le texte explicatif annonçant le code avant que l'étape OTP soit réellement atteinte.
- Placer le consentement marketing sous « Message à l'établissement (facultatif) ».

## Identité dans le modal

### Sans compte

- Saisie prénom, nom, e-mail, pays et téléphone.
- Validation OTP avec `AccountValidation` et le motif dédié à la réservation.
- Ne créer ou réutiliser `BookingCustomer` qu'après validation réussie.
- Si l'e-mail ou le téléphone appartient à un compte iziLife, demander une authentification.

### Avec un compte

- Ne pas quitter le modal.
- Reprendre le formulaire de connexion existant dans une version compacte : « Pas de compte encore ? Créer un compte », e-mail, mot de passe, affichage/masquage du mot de passe, mot de passe oublié et bouton de connexion.
- Ne pas afficher « Se souvenir de moi » dans le tunnel de réservation.
- Ouvrir « Créer un compte » dans un nouvel onglet afin de ne pas perdre le tunnel en cours.
- Conserver le parcours d'inscription existant dans ce nouvel onglet : saisie des coordonnées, création de la demande, puis validation de l'e-mail et du téléphone avec les codes `AccountValidation` de raison `signup`.
- L'inscription n'ouvre actuellement aucune session et sa page finale renvoie vers la connexion. Ne pas inventer de retour automatique vers le tunnel dans la première version : l'utilisateur revient dans l'onglet de réservation, dont le modal et les choix sont restés intacts, puis se connecte dans le formulaire AJAX.
- Afficher e-mail et mot de passe dans le modal et authentifier en AJAX avec protections anti-bruteforce, CSRF, limitation de débit et réponses non énumérantes.
- Ne pas appeler tel quel le parcours de connexion qui redirige aujourd'hui vers la page précédente. Le modal utilise un endpoint AJAX dédié, tout en réemployant le même service d'authentification, les mêmes contrôles de sécurité et la même création de session.
- Version 1 du endpoint AJAX : authentification par e-mail et mot de passe, sans OTP de connexion.
- Version 2 : faire évoluer ce même parcours pour accepter une identification d'abord par téléphone ou par e-mail, puis demander le code OTP/MFA lorsque la politique du compte l'exige. Cette évolution ne doit pas modifier le parcours invité ni celui de l'inscription.
- Une connexion AJAX réussie renvoie un résultat JSON et laisse le modal ouvert ; elle remplace localement le formulaire par les coordonnées du compte sans navigation ni redirection intermédiaire.
- Après succès, remplacer le formulaire de connexion par les coordonnées du compte et le message « Vous êtes connecté avec votre compte iziLife ».
- L'authentification ouvre réellement la session utilisateur par AJAX, sans quitter ni fermer le modal. Le tunnel conserve date, participants, option et créneau.
- Régénérer l'identifiant de session après authentification et réutiliser les protections normales du compte ; ne jamais extraire les informations personnelles d'un compte sans établir cette session authentifiée.
- Après soumission réussie de la réservation, effectuer la redirection POST/Redirect/GET vers la page de confirmation ou de suivi ; la session ouverte reste active.
- Lorsque la MFA utilisateur sera activée, insérer une étape de code dans ce même flux en réutilisant le mécanisme MFA existant côté Partner, adapté au compte utilisateur.

## Modal — privatisation

- Réutiliser les mêmes composants date et participants.
- Initialiser les participants au minimum de la configuration sélectionnée.
- Ne jamais permettre de descendre sous le minimum ni de dépasser le maximum.
- Pour une privatisation d'équipement, proposer les heures compatibles avec les horaires du lieu sous forme de pills.
- Pour une privatisation globale, proposer provisoirement un sélecteur par pas de 30 minutes, borné par les horaires du lieu.
- Conserver le statut de demande soumise à validation tant que le modèle d'acceptation et de période finale n'est pas terminé.
- Une demande en attente ne bloque aucune disponibilité. Ne pas déduire la fin de la privatisation depuis l'heure de fermeture : le client peut partir avant.
- Première approximation retenue : une privatisation acceptée utilise une durée estimée fixe de quatre heures, définie dans une constante métier, tant que l'heure de fin réelle n'est pas gérée.
- Une privatisation acceptée de l'établissement bloque tous ses parcours de réservation sur cette période. Une privatisation acceptée d'un espace bloque cet espace et les ressources qu'il contient.
- Le reste des informations d'identité, partage, message et OTP est commun au modal de réservation.

## Conflits entre réservations d'un client

- Centraliser le contrôle dans un service extensible aux réservations, privatisations, Meetz et futurs parcours.
- Dans un même établissement, refuser un chevauchement réel ; une réservation successive reste possible si les périodes ne se chevauchent pas.
- Contrôler d'abord les chevauchements temporels établis à partir des périodes réelles ou estimées.
- Ajouter un garde-fou anti-abus volontairement large entre établissements différents : au-delà de 100 km, interdire une seconde réservation sur la même plage ou lorsqu'il existe moins de deux heures entre la fin estimée de R1 et le début de R2.
- Ne pas chercher à modéliser précisément le transport dans cette première version. Une réservation distante reste possible dès que ce délai large est respecté, ce qui laisse notamment la place aux déplacements en train ou en avion.
- Ce garde-fou vise les abus et les risques de non-présentation ; un futur paiement ou dépôt de garantie pourra compléter cette protection sans remplacer les contrôles de cohérence.
- Ne pas raisonner uniquement avec l'écart entre les deux heures de début : chaque parcours doit fournir une durée estimée ou une fin métier.
- Pour la première version d'une privatisation sans heure de fin, utiliser la constante métier de quatre heures plutôt que toute l'amplitude d'ouverture du lieu. Cela permet, par exemple, une privatisation de parc suivie d'un restaurant le soir.
- Le contrôle ne doit pas dépendre uniquement de la session : il doit fonctionner après résolution sécurisée du compte ou du `BookingCustomer`.

## Administration BO et Partner Space

- Ne pas restructurer la navigation ni les vues générales du BO dans ce chantier. Compléter les cartes et formulaires BC/BCC existants avec les paramètres manquants.
- Le BO et le PS restent deux applications et deux expériences distinctes : l'alignement demandé porte sur les données, les validations et les capacités d'administration, jamais sur une reproduction des vues du PS dans le BO.
- Le BO doit permettre à l'équipe iziLife de créer, cibler et configurer intégralement les BC/BCC à la place du partenaire pendant les premiers mois : mêmes paramètres métier disponibles, avec une ergonomie d'administration propre au BO.
- Dans le formulaire BO de création/modification d'une BC, permettre une cible établissement ou une sélection d'une ou plusieurs catégories éligibles. Une sélection multiple crée une seule BC commune aux catégories choisies ; elle ne duplique pas la BC.
- Ajouter dans le BO, comme dans le PS, toute la configuration de privatisation : participants minimum/maximum, acte gratuit ou payant, minimum de consommation total ou par personne, montant, devise, publication, pause et future période d’occupation.
- Faire évoluer dans les deux interfaces la table dédiée à la politique d’acceptation : rattachement à la BC, confirmation automatique, manuelle ou selon seuil, sans recopier provisoirement ces champs dans `BookingConfiguration`.
- Toute nouvelle règle de réservation ajoutée pendant le chantier devra être administrable et validée de manière cohérente dans le BO et le PS ; aucun paramètre ne doit exister uniquement dans une interface ni être inventé silencieusement par le FO.
- Phase ultérieure : faire évoluer la fonction de pause existante au lieu de créer un second système, puis ajouter la fermeture d'une journée et la sélection de plusieurs créneaux à suspendre.
- Exposer les mêmes min/max et conditions de privatisation dans le BO et le PS.
- La capacité globale, la capacité par catégorie et la capacité par service doivent être identifiables et ne jamais partager un libellé ambigu.
- Les termes BC, BCC et noms de colonnes restent techniques et ne sont pas montrés au partenaire.

## Ordre de réalisation après validation du modèle

1. stabiliser les tables et règles de priorité ;
2. aligner BO et Partner Space ;
3. exposer un résolveur FO unique pour capacités, bornes, services et indisponibilités ;
4. rendre les cartes dynamiques selon date et participants ;
5. uniformiser les modales ;
6. brancher connexion AJAX, OTP invité et futurs contrôles MFA ;
7. tester les conflits, indisponibilités et privatisations ; la gestion opérationnelle des pauses par journée ou lots de créneaux vient dans une phase ultérieure.

## Décisions stabilisées pour cette version

- La durée de 90 minutes est préremplie, visible et modifiable ; elle n'est jamais inventée silencieusement par le FO.
- La capacité normale et le plafond absolu sont distincts pour `TABLE` et `STANDARD/ARRIVAL_TIME` : dépasser la première force la validation manuelle, dépasser le second rend le créneau indisponible.
- Dépasser `BC.max_party_size` rend l'option indisponible et peut orienter visuellement vers la demande particulière, sans conversion automatique.
- La capacité physique du lieu reste une donnée propre au lieu. Les capacités ouvertes à iziLife appartiennent à la BCC et ne remplacent pas cette capacité physique.
- Une BCC composable présente ses parties dans l'ordre, avec leur libellé. Les parties réutilisent les cadences, heures fixes et services existants ; aucun nouveau vocabulaire « session » n'est introduit.
- `SERVICE` désigne une prestation identifiée et conserve une jauge par créneau ; le vocabulaire de service de restauration dans `TABLE` ne change pas son `booking_kind`.
- Les suspensions opérationnelles par journée ou sélection multiple de créneaux restent une phase ultérieure. Dès cette version, le FO sait afficher toute indisponibilité résolue en grisé, sans soumission possible.
