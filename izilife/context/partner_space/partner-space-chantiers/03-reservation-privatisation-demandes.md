# BRIEF À COPIER — Réservation, Privatisation et Demandes

## État livré et décisions consolidées — 29 août 2026

- La réservation de table Place/Shop ne dépend pas de `ElementAccessAndBookingConf`. Une déclaration « Réservation de table » décrit le parcours mais ne l'active pas. L'affichage exige l'éligibilité métier, l'entitlement `TABLE_BOOKING`, puis une BC/BCC active, courante, publiée, non suspendue et exploitable.
- Exception de couverture : un contenu spécial Brunch actif et valide suffit à rendre sa BC activable sans couvrir les sept jours. Il exige toutefois jour(s), heure de début et heure de fin ; l'éligibilité considère aussi les catégories secondaires du lieu.
- Un parcours Equipment direct exige de la même façon l'entitlement `EQUIPMENT_BOOKING` et une BC/BCC publiée/non suspendue. Si un EABC existe, son `access_mean` et ses chemins d'accès restent une troisième porte : une BC seule ne peut pas contourner un ticket/pass ni un choix configuré après paiement.
- La portée BC est stricte : `ALL` signifie tout l'établissement ; sinon la catégorie principale ou secondaire est stockée explicitement dans `place_type_id` XOR `shop_category_id`. Le FO ne présente que les parcours publiés.
- Une Booking appartient à un `User` XOR un `BookingCustomer`. `BookingCustomer` est l'identité persistante d'un client sans compte, jamais le snapshot d'un User. Si l'e-mail invité existe dans `User`, connexion ou vérification d'identité obligatoire.
- Le créateur et la provenance sont orthogonaux au client : `created_by_*` et `origin_*` permettent une saisie Partner/Page ; `offer_id` conserve une provenance `Offer`. `SpecialCampain` reste réservé aux promotions spéciales du lieu (Happy Hour, étudiant, senior, etc.) et ne type pas les opérations. Le sous-typage futur des `Offer` de type `OPERATION` (collective, Last Minute, autres) appartient au chantier Offer ; Booking n'en duplique aucun champ.
- `booking_context`, `community_id`, `user_group_id` et `community_activity_id` portent les réservations personnelles, de groupe ou de Community. Le moteur Benefit existant résout la `BenefitPolicyRule` correspondante ; la Booking conserve `benefit_rule_id`. Les BPR groupe/community sont affichées informativement dans le tunnel et validées à la création.
- Une privatisation peut afficher un minimum de chiffre d'affaires/consommation porté par l'Equipment. Ce minimum n'est ni un prix encaissé ni un acompte en V1.
- Dans l'onglet Réserver du lieu, « réserver quelques tables », privatiser un Equipment/espace (salle, cave, terrasse…) et privatiser tout l'établissement sont des choix du même ensemble. En catégorie unique, seule la privatisation de l'établissement est proposée. En multi-catégorie avec gestion `commerces-separes`, le parcours de table peut aussi viser explicitement la catégorie ; cette cible reste distincte de l'établissement complet. La table physique éventuellement attribuée reste une ressource d'une Booking de table.
- Un Equipment réservé pour son usage propre (bowling, terrain, etc.) conserve en revanche son propre parcours BC/BCC et les effets éventuels d'EABC ; il ne doit jamais être traité comme une réservation de table.
- Pour un Equipment de loisir, la même catégorie peut publier soit une BC générique (le client choisit le créneau, avec allocation facultative d'une ressource du pool), soit plusieurs BC ciblant des Equipment explicites (Into The Wild, missions VR…), soit une combinaison. Le résumé groupe ces parcours ; il n'invente aucun comportement depuis la seule présence d'une catégorie.
- Le comportement n'est jamais codé depuis le nom Restaurant, Bar, Bowling ou VR. Le helper d'éligibilité s'appuie sur `EtablishmentType` et `BookableServiceProductType`; la BC/BCC publiée active ensuite le parcours. Une BC peut cibler plusieurs catégories via `BookingConfigurationCategory` : si Restaurant et Bar partagent horaires/capacité/règles, le FO affiche un seul parcours puis demande l'activité dans le tunnel. En `commerces-separes`, une catégorie sans rattachement explicite est exclue. Des BC distinctes produisent des entrées distinctes.
- V1 allocation automatique : une seule table active, compatible, de capacité suffisante et libre ; sinon aucune affectation. Aucun assemblage/recomposition/transfert multiressource.
- Les Equipment restent descriptifs sans abonnement. L'entitlement protège l'opération de réservation, pas l'existence de l'objet.
- `EquipmentInstance` est le futur inventaire physique d'un modèle mutualisé (chambres 101/102, etc.). Hôtel, cinéma, spectacle et placement sont préparés mais hors V1.
- Event peut posséder une BC/BCC propre, hériter explicitement en fallback de son Place/Shop, ou recevoir une BC/BCC via `EventSerie`. SCC/Session reste le calendrier d'occurrences et ne remplace jamais la capacité/allocation BCC.
- Le FO trace entrée, disponibilité, sélection du parcours/créneau, début d'identité, envoi, réussite et erreur. Le taux d'abandon se calcule entre entrée et réussite.
- Les réservations User apparaissent dans « Mes réservations » avec statut, participants, table, Benefit/Offer et QR signé. L'invité reçoit un lien privé de suivi.
- La demande simple/privatisation possède un fil iziLife Partner/client, statuts et notifications e-mail. Devis tarifé, paiement et acompte restent hors V1.

Je lance le chantier **iziLife Réservation / Privatisation / Demandes de devis** sur `izilife`, `izilife-admin` et `izilife-partner-admin`.

Le texte source « izilife — Décision d'architecture globale du moteur de réservation » fait partie du contexte obligatoire. Relis-le intégralement, puis audite les tables et implémentations actuelles avant de coder. Les décisions ci-dessous le mettent à jour.

## Objectif

Construire un moteur de réservation local multi-vertical, réutilisable pour Place, Shop, Equipment, Animation, Experience/XP et Event, puis fournir au Partner les outils d'exploitation correspondants.

Le moteur n'est ni un widget restaurant ni une copie de Privateaser. Il doit couvrir la table, le rendez-vous, l'activité, la séance, l'équipement, la journée, la privatisation et la demande de prestation à partir de configurations génériques.

## Principes non négociables

- Résolution par `from_type/from_id` et configuration effective, pas par grandes listes de catégories.
- Place et Shop restent séparés dans le legacy mais partagent les contrats du moteur.
- Multi-catégorie native.
- Le Front affiche ; le Back décide et recalcule.
- `BookingMethod`, `AccessBookingNeeded` et `AccessType` restent trois concepts distincts.
- `BookingStatus` et `TransactionStatus` sont deux workflows indépendants.
- Toutes les disponibilités et capacités sont recalculées côté serveur à la création.
- Chaque endpoint contrôle rôle, Partner, ownership, scope et entitlement.
- Le moteur peut être construit derrière une capacité désactivée ; son ouverture commerciale dépend du Foundation et de l'abonnement.

## Cible, scope et ownership

- Le contrat d'entrée commun reste `from_type/from_id`.
- `from_type/from_id` désigne la cible métier principale réellement réservée : `PLACE`, `SHOP`, `EQUIPMENT`, `ANIMATION`, `EXPERIENCE` ou `EVENT`.
- Une Booking ne possède qu'une seule cible métier principale. Les FK legacy restent temporairement disponibles pour compatibilité, mais le service de création garantit qu'une seule FK cible est renseignée.
- Le scope ne remplace pas la cible. Il décrit le périmètre opérationnel et d'autorisation. Exemple : une table est la cible `EQUIPMENT`, son lieu est le scope `PLACE`, et le Partner propriétaire du lieu fournit l'ownership.
- Le `BookingResolver` retourne une représentation canonique en mémoire contenant au minimum cible, famille BCC/SCC, configuration effective, scope opérationnel et Partner propriétaire.
- L'évolution éventuelle des configurations vers `scope_type/scope_id` doit être menée uniformément dans le BO et le Partner Space, avec période de compatibilité et contrôle anti-ambiguïté. Elle ne doit pas créer une seconde cible concurrente dans Booking.

### Multi-catégorie Place/Shop

- `unique-etablissement` signifie une exploitation commune : horaires, réservation, BC/BCC et parcours communs à toutes les catégories descriptives. La portée BO est explicitement « Tout l'établissement ».
- `commerces-separes` signifie une exploitation distincte dans un même lieu : chaque catégorie activée possède ses propres horaires et BC/BCC, y compris lorsqu'il s'agit de la catégorie principale.
- Le FO ne demande jamais de choisir parmi toutes les catégories du lieu. Il propose uniquement les parcours de réservation réellement activés et exploitables. S'il n'en existe qu'un, il l'ouvre directement.
- Une BC sans `place_type_id` ni `shop_category_id` signifie explicitement « Tout l'établissement » ; elle ne signifie jamais implicitement « catégorie principale ».
- Le BO et le Partner Space réutilisent le même contrat de référence de catégorie que les horaires : `ALL`, catégorie principale explicite ou catégorie secondaire validée dans le périmètre de l'objet.

## Accès, réservation et vente

Les notions suivantes restent orthogonales et doivent être résolues ensemble :

1. `AccessType` décrit la nature du droit d'accès : libre, gratuit sur réservation, payant, abonnement, adhésion, carte, accès par activité, etc.
2. La billetterie/paiement iziLife indique si iziLife exécute la vente ou l'inscription.
3. `AccessBookingNeeded` informe sur le besoin ou le conseil de réservation ; il ne suffit pas seul à piloter le moteur.
4. `BookingMethod` décrit la forme temporelle : sans réservation, jour seulement, jour et créneau.
5. `ElementAccessAndBookingConf` orchestre le parcours général : méthode, moment du choix temporel, réservation avant ou après paiement et délais.
6. BC/BCC ou SC/SCC décrivent disponibilités, capacités, durées, contraintes et acceptation effectives.
7. EAP et `ElementService` décrivent ce qui est vendu ou sélectionné et selon quel modèle de prix.

Le front reçoit une projection résolue de cette combinaison. Il ne déduit jamais le parcours à partir d'une catégorie, du seul `AccessType` ou de la seule présence d'un EAP.

Cas à préserver : restaurant sans EAP ; parc multi-activités avec EAP global ou partiel et date choisie maintenant ou plus tard ; lieu de loisirs combinant accès libre, carte de crédits et réservation d'un Equipment ; lieu sur abonnement ou adhésion avec réservation éventuelle d'une séance ou ressource.

## Deux familles de disponibilité derrière une API commune

### Place / Shop / Equipment / Animation

- `BookingContent` comme enveloppe de configuration.
- `BookingConfigurationContent` (BCC) comme règle effective.
- `BookingSlot` facultatif pour petit-déjeuner, déjeuner, brunch, dîner, soirée, etc.
- La BCC est prioritaire pour capacité, durée et disponibilité.

### Experience/XP / Event

- XP utilise `SessionConfiguration` et `SessionConfigurationContent` (SCC) comme récurrence.
- Event peut utiliser BC/BCC pour une réservation capacitaire (notamment table) et sa `EventSerie` peut porter cette configuration ; l'héritage depuis le lieu est seulement un fallback explicitement activé.
- Une occurrence standard reste virtuelle : SCC + date + heures.
- Une `Session` physique existe seulement pour une occurrence manuelle, modifiée, annulée ou administrée individuellement.
- Ne pas matérialiser toutes les occurrences futures.
- Une Booking peut cibler une occurrence SCC virtuelle sans `session_id`.

## Gestion des configurations dans le Partner Space

- Configurer BC/BCC pour les lieux, ressources et équipements possédés.
- Configurer SC/SCC pour XP et les occurrences événementielles qui relèvent réellement d'une séance ; configurer BC/BCC pour les réservations capacitaires Event/EventSerie.
- Créer des Sessions manuelles et des exceptions.
- Protéger modification/suppression lorsqu'il existe déjà des réservations.
- Fournir annulation, changement de capacité, déplacement et communication selon des workflows contrôlés.
- Distinguer « Mes événements » de « Dans mes lieux » : le second groupe est en lecture seule si le Partner n'est pas organisateur.
- La réservation de table est protégée par deux portes distinctes : entitlement `TABLE_BOOKING` accordé par `FeaturePlan`, puis activation/configuration opérationnelle sur tout l'établissement ou sur chaque catégorie lorsque la gestion est séparée.
- `FeaturePlan` accorde `TABLE_BOOKING` au titre de l'abonnement ; il ne faut pas créer une Feature de plan par catégorie. Le choix des catégories sur lesquelles le Partner exploite effectivement cette fonctionnalité appartient à la configuration locale.
- L'activation locale doit fonctionner aussi bien pour Place que pour Shop. L'existant possède `FeaturePlace`, mais pas `FeatureShop`, et `Feature.target_level` ne couvre actuellement que `global`, `partner` et `place` : ce manque doit être corrigé proprement, sans attribuer à Shop un faux entitlement permanent ni détourner le niveau Partner.
- `ElementAccessAndBookingConf` n'est pas requis pour activer la réservation de table. Il peut coexister sur le même lieu pour un parcours global d'accès, de ticket, de pass, de carte ou d'abonnement.

### Éligibilité métier des catégories

- Centraliser dans un helper commun Place/Shop la classification des parcours que peut proposer une catégorie.
- Le helper tient compte de `ShopCategory`, `PlaceType`, `EtablishmentType`, de leurs parents, de la catégorie principale, des catégories secondaires et du mode `unique-etablissement` / `commerces-separes`.
- Il sait notamment distinguer : réservation de table, séjour/nuitée, service réservable et loisir reposant sur un Equipment.
- `is_bookable_service_category` est un indice trop large pour signifier à lui seul « réservation de table » : Restaurant, Bowling et Escape Game peuvent être réservables tout en exigeant des parcours différents.
- Ce helper détermine uniquement la compatibilité métier. Il ne décide jamais qu'un parcours est publié : l'entitlement, la configuration effective, son activation et son caractère exploitable commandent seuls l'affichage FO.
- Le BO et le Partner Space doivent raccorder la gestion BC au même contrat de catégories que les horaires : `ALL`, catégorie principale explicitement référencée, ou catégorie secondaire appartenant réellement au Place/Shop, avec respect du XOR `place_type_id` / `shop_category_id`.

## Tables et équipements

- La réservation de table est un usage du moteur avec des équipements/ressources `table`, `zone`, `salle`, `terrasse`, `cave`, etc.
- L'allocation automatique d'une table ou ressource est désactivée par défaut et activée explicitement par le Partner dans sa configuration.
- En V1, l'allocation automatique affecte au plus une ressource compatible et libre. Si aucune ressource simple ne convient, la Booking reste sans affectation automatique et doit être traitée par le Partner.
- En V1, ne pas automatiser recomposition, assemblage, désassemblage ou transfert entre tables.
- En V2, permettre au Partner d'affecter/libérer une table, transférer une réservation vers une autre ressource libre et assembler plusieurs ressources. Toute composition bloque chacune des ressources d'origine.
- Une combinaison fréquente peut être enregistrée comme modèle, mais le verrouillage porte toujours sur les ressources d'origine.
- Permettre de désactiver temporairement une table ou ressource en un clic, avec période et motif.
- La configuration décide capacité, durée, nombre de personnes et règles d'acceptation.
- Ne pas coder `restaurant`, `bar` ou `salon-de-thé` dans le cœur du resolver ; ces catégories peuvent aider à proposer une configuration initiale.
- `Equipment` peut représenter un type mutualisé et commercial, par exemple « Chambre Deluxe ». `EquipmentInstance` représente alors chaque unité physique numérotée, par exemple « Chambre 101 ».
- Le moteur doit rester compatible avec les séjours et inventaires par type : arrivée, départ, voyageurs, quantité disponible et allocation éventuelle d'une instance physique.
- Les plans de salles, sièges de cinéma, théâtre, spectacle ou opéra relèvent d'un futur lot billetterie avec placement. Ils sont documentés mais exclus de la tranche réservation de table et de l'allocation Equipment V1.

## Réservation simple et séances

- Supporter jour seulement, jour + créneau et sans réservation requise.
- Parcours adaptable : service, équipement, date, heure, durée, quantité/personnes, notes.
- Experience/Event utilisent SCC/Session et les EAP associés lorsque paiement ou accès l'exige.
- Les achats, réservations et participants doivent être visibles dans le Partner Space de l'organisateur.
- Les modifications et annulations tiennent compte des ventes/réservations existantes et du workflow de remboursement.

## Mesures, capacité et tarification

- Le moteur ne fige pas tous les cas métier dans les seuls concepts personnes/unités.
- La configuration décrit les dimensions demandées, celles qui consomment la capacité, celles qui déterminent le prix et celles communiquées au Partner.
- Booking conserve les instantanés simples utiles, notamment le nombre réel de personnes lorsqu'il existe ; les dimensions additionnelles sont portées par des mesures/snapshots validés côté serveur.
- Exemples : personnes, adultes, enfants, groupes, unités, équipements, terrains, chambres, durée, jours, crédits, passages ou quantité tarifée.
- Une réservation privée de 6 à 10 personnes peut enregistrer 8 participants tout en facturant un prix fixe de groupe.
- EAP, `ElementService` et leurs modèles de prix restent les sources commerciales. Le resolver de disponibilité ne réimplémente pas leur calcul tarifaire.

## Exploitation Partner

- Vue calendrier/liste des réservations et demandes.
- Confirmation, confirmation automatique, refus, relance, annulation, absence, en cours, terminée.
- Configuration : sous un seuil X acceptation automatique ; à partir de X demande manuelle, si cette règle est compatible avec la capacité réelle.
- Pause globale ou par ressource/créneau.
- Bouton rapide pour arrêter temporairement les réservations.
- Préparer une commande texte future du type « Fais une réservation au nom de Tito sur Soultrain jeudi à 21 h 30 », mais aucune mutation IA sans prévisualisation et confirmation humaine.
- Une Booking peut rester sans ressource affectée lorsque l'allocation automatique est désactivée ou qu'aucune ressource simple ne convient.
- Le cockpit distingue disponibilité/capacité, état Booking, affectation de ressource et état du paiement.

## Client connecté ou invité

- Le FO accepte une réservation avec compte, création de compte pendant le parcours ou en invité.
- Un invité fournit au minimum nom, prénom, e-mail et téléphone selon la configuration.
- `BookingCustomer` représente exclusivement un client sans compte et peut être réutilisé par e-mail vérifié. Une Booking référence exactement un `User` ou un `BookingCustomer`, jamais les deux.
- Une réservation invitée dispose d'un lien non devinable et limité pour consultation, confirmation ou annulation.
- Une création de compte ultérieure peut rattacher la Booking après vérification de l'e-mail.

## Privatisation

- Privatisation d'un Equipment/zone et privatisation complète d'un Place/Shop restent distinctes.
- Une privatisation débute par défaut comme demande en attente.
- Elle peut inclure personnes, dates, horaires, espaces, équipements, nourriture et services.
- S'inspirer des bons parcours de Privateaser en les adaptant au modèle iziLife, sans en copier l'architecture.

## Nouveau domaine : Demand / Quote

Une demande de traiteur, de prestation ou de privatisation complexe n'est pas immédiatement une Booking ni une Transaction.

Prévoir un workflow propre :

1. demande client ;
2. qualification ;
3. échange Partner/client ;
4. proposition/devis ;
5. révision ;
6. acceptation/refus/expiration ;
7. conversion contrôlée vers Booking ;
8. acompte ou paiement éventuel ;
9. exécution et clôture.

Le Partner pourra ultérieurement réutiliser ses `ElementService`, équipements et tarifs préenregistrés dans la proposition. Ne pas mélanger le statut du devis avec BookingStatus ou TransactionStatus.

## Paiement

- La réservation gratuite doit pouvoir exister sans PSP.
- Paiement, acompte ou paiement après confirmation sont des stratégies distinctes.
- Le client achète/réserve depuis le FO ; le Partner consulte et traite dans son cockpit.
- PayHub fournit le moteur transactionnel commun lorsqu'un paiement est requis.
- Toute annulation doit déterminer séparément l'effet sur Booking, capacité, ticket, Transaction et remboursement.
- La consommation de capacité d'une demande en attente est configurable : blocage provisoire ou absence de blocage, avec durée en minutes, heures ou jours.
- Après confirmation nécessitant paiement ou acompte, la capacité peut être conservée pendant un délai configurable ; l'expiration libère ou réexamine la Booking selon la politique.
- Le Partner peut configurer une caution/acompte pour tous ou à partir d'un seuil de personnes, unités, montant ou autre mesure supportée.
- Le caractère remboursable, déductible du solde ou purement garantissant relève d'une politique de paiement distincte, activable progressivement.

## Contrat technique cible

- `BookingResolver(from_type, from_id)` ;
- resolver de disponibilités par famille BCC ou SCC/Session ;
- `AvailabilityDTO` commun ;
- endpoint availability ;
- endpoint create avec revalidation et protection de concurrence ;
- `booking_block` réutilisable dans page, fiche, modal ou sidebar ;
- Front sans logique métier par catégorie ;
- services de validation/création séparables sans surarchitecture prématurée.
- Les parcours Experience/EAP/Session servent de référence pour la philosophie générale du projet : résolution configurable, diversité des parcours et validation serveur. Leur HTML et leur logique embarquée dans les vues ne doivent pas être copiés pour Place/Shop.

## Mise à jour du phasage du texte source

La V0 technique peut être construite avant l'ouverture commerciale, mais elle ne doit pas simuler définitivement `can_use_booking_feature = true`. Le contrat d'entitlement Foundation doit être branché avant exposition publique.

Ordre recommandé :

1. Audit SQL et flux existants BC/BCC/SC/SCC/Session/Booking.
2. Statuts et invariants Booking/Transaction.
3. Resolver + DTO + disponibilité.
4. Tranche Place/Shop complète.
5. Equipment, tables et ressources composées.
6. XP/Event SCC et occurrences virtuelles.
7. Exploitation Partner et protections sur réservations existantes.
8. Privatisation simple.
9. Demand/Quote.
10. Paiement/acompte et tracking.

## Livrables

- cartographie de l'existant et écarts ;
- schéma des états Booking/Demand/Quote/Transaction ;
- contrats API/DTO ;
- plan SQL additif ;
- composants FO et écrans Partner/BO ;
- tests de capacité, concurrence, timezone et récurrence ;
- tests ownership/IDOR/rôles ;
- tests annulation avec et sans paiement ;
- documentation des capacités désactivées.
