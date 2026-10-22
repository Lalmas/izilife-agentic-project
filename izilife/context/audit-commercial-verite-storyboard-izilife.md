# Audit commercial iziLife — contenu, vérité produit et storyboard

Date de consolidation : 20 octobre 2026  
Périmètre : présentation commerçants existante, FO iziLife, BO iziLife, Espace Partenaire, tests, dépôt SQL et décisions explicites de la conversation.

## 1. Cadre de vérité retenu

Le support général doit présenter ce qu’un commerce peut réellement montrer, administrer ou activer. Il ne doit contenir ni prix, ni promesse de fréquentation garantie, ni service abandonné.

Les décisions métier données dans la conversation priment sur les formulations anciennes :

- les abonnements utilisateurs à nommer sont **iziLife Pass** et **iziLife Prime** ;
- la prestation par laquelle iziLife choisirait une animation et mettrait le lieu en relation avec un prestataire est **abandonnée** ;
- **Last Minute est prévu au lancement** ;
- les parcours de **réservation et de privatisation sont prêts** ;
- les Sélections et les offres collectives restent présentées comme futures tant qu’une nouvelle décision métier ne les déclare pas lancées.

Le code distingue par ailleurs le socle commerçant `PARTNER_BASE` et la formule commerçant `PARTNER_PRIME`. Ces identifiants techniques ne doivent pas être confondus avec les abonnements utilisateurs iziLife Pass et iziLife Prime.

## 2. Audit éditorial de la présentation existante

### Diagnostic global

La présentation actuelle constitue un brouillon commercial de neuf slides. Elle donne une vue rapide de plusieurs idées mais ne peut pas servir de support de rendez-vous en l’état.

Points utiles à conserver :

- une entrée par les besoins du commerce ;
- la distinction entre présence, activation et conversion ;
- l’idée d’un premier test adapté au lieu ;
- les thèmes menu, réservation, offres, boosts, événements et sélections.

Points à corriger :

- plusieurs prix et niveaux de service ne sont pas validés ;
- des fonctions actives, futures et abandonnées apparaissent au même niveau ;
- des résultats commerciaux sont formulés comme des conséquences certaines ;
- le parcours réel de l’utilisateur et l’Espace Partenaire restent presque invisibles ;
- les slides reposent surtout sur des cartes de texte, sans preuve produit, photographie locale ou exemple d’usage ;
- le support ressemble à un catalogue d’options plus qu’à une démonstration de la valeur d’iziLife.

### Audit slide par slide

| Slide | Contenu actuel | Diagnostic | Décision pour le futur support |
|---|---|---|---|
| 1 | « Plus de visibilité. Plus de raisons de venir. » | Bonne intention, mais « transformer une présence locale en fréquentation » promet un résultat non démontré. | Recentrer la couverture sur la présence en ligne et la découverte dans les projets de sortie. Utiliser une scène locale réelle. |
| 2 | Socle gratuit, fiche, offres et services payants | Le socle gratuit est réel. La fiche, le menu digital et la gestion des retours clients sont confirmés. Les offres ne doivent pas être implicitement rangées dans le gratuit sans détail. | Conserver une slide sur le socle gratuit avec un inventaire exact et le quota média validé. Supprimer « accélèrent la fréquentation ». |
| 3 | Menu digital à 29,99 €, réservation et privatisation | Le prix doit disparaître. Le menu digital appartient au socle gratuit. Réservation et privatisation sont prêtes, mais méritent une explication séparée. | Faire deux slides : menu/catalogue, puis réservation/privatisation. |
| 4 | Boosts à 10 €, 20 € et 30 €+ | Le parcours de demande de boost existe. Les prix, durées, surfaces et intensités affichés ne sont pas validés. | Conserver le principe du boost sans prix. Expliquer qu’une mise en avant porte sur un contenu, une période et des emplacements définis. |
| 5 | Programme d’ouverture sur un mois | Ce programme n’est pas une fonction produit démontrée. Il peut servir de méthode commerciale, pas de promesse standardisée. | Retirer du cœur produit. Réutiliser éventuellement la logique dans la dernière slide comme proposition de premier test. |
| 6 | Member, Pass, Prime, roue iziLife, braderie | `Member` est obsolète. Les deux abonnements utilisateurs à employer sont iziLife Pass et iziLife Prime. La roue et la braderie ne sont pas établies comme offres permanentes. | Remplacer par une slide claire sur offres du lieu, avantages réservés aux membres et opérations ponctuelles. |
| 7 | Sélections et Meetz | Les Sélections disposent de briques techniques mais restent un produit futur dans le discours commercial. Meetz n’explique pas directement l’outillage quotidien du commerçant. | Présenter les Sélections dans une zone « à venir ». Sortir Meetz du support général, sauf besoin commercial spécifique. |
| 8 | iziLife choisit une animation et un prestataire | Service abandonné. La slide crée une promesse de prestation qui ne doit plus être faite. | Supprimer intégralement. Conserver seulement la capacité du lieu à publier et gérer ses propres événements. |
| 9 | Construction d’une formule et premier test | Bonne logique de conclusion. La mention du budget peut rester dans l’échange oral, mais le support demandé est sans prix. | Terminer sur un diagnostic du lieu, la mise à jour de la présence et le choix d’un premier usage à tester. |

### Conclusion de l’audit

La présentation actuelle ne doit pas être corrigée à la marge. Elle doit être reconstruite autour d’un fil narratif : **un utilisateur prépare une sortie, découvre un lieu, consulte ses informations et peut agir ; le commerçant maîtrise ces éléments depuis l’Espace Partenaire**.

## 3. Tableau de vérité commercial

Légende :

- **Actif** : fonction exploitable et administrable dans le produit.
- **Prêt** : fonction déclarée prête par la décision métier, même si son ouverture dépend encore d’une activation ou d’une configuration.
- **Lancement** : fonction prévue pour la remise en ligne.
- **Futur** : ne pas présenter comme disponible.
- **Abandonné** : supprimer des supports.
- **À confirmer** : contradiction ou condition commerciale non stabilisée.

| Fonction | Gratuit | Avec abonnement | Option / commission | Quota ou limite | État | Preuve principale | Formulation commerciale autorisée |
|---|---|---|---|---|---|---|---|
| Référencement d’un lieu | Oui, socle commerçant | Oui | Non établie | Aucun quota de fiche publié | Actif | PS `PartnerEntitlements.php`; SQL `021_Next_Improves.sql` lignes 2292-2316 | « Votre lieu dispose d’une présence structurée sur iziLife. » |
| Description, adresse, contacts et liens | Oui | Oui | Non établie | Selon les champs de la fiche | Actif | Contrôleurs `Place.php`, `Shop.php`, routes PS | « Vous gérez les informations utiles avant la venue. » |
| Horaires normaux et exceptionnels | Oui | Oui | Non | 5 configurations horaires par lieu dans le PS | Actif | `Hourly_model::MAX_HOURLIES_PER_OWNER = 5`; contrôleurs Place/Shop | « Vous gérez vos horaires habituels et vos exceptions. » Ne pas publier le plafond de 5 comme argument commercial sans nécessité. |
| Équipements, accessibilité, services et tarifs d’accès | Oui | Oui | Selon les produits configurés | Pas de quota commercial identifié | Actif | Contrôleurs Place/Shop et composants d’accès du PS | « Votre fiche précise les équipements, l’accessibilité, les services et les conditions d’accès. » |
| Photos et médias importés | Oui | Oui | Non | Gratuit : 5 médias par fiche. Pro : sans quota commercial pour la plupart des fiches. Limites structurelles : événement autonome 1 image, occurrence liée 2, offre 5. Ajout limité à 3 fichiers par envoi. | Actif | SQL `021_Next_Improves.sql` lignes 6030-6046 et 4073-4079 ; PS `Media.php` lignes 169-185 et 428-440 | « Le référencement gratuit comprend jusqu’à 5 médias par fiche. La formule supérieure étend la médiathèque. » Éviter « photos illimitées » sans préciser les exceptions de structure. |
| Publications Instagram intégrées | Oui, sous quota | Oui | Non | Gratuit : 5 sur une fiche lieu/commerce, 3 sur événement, expérience, série, célébration ou page. Maximum actif : 10 ou le quota inférieur. Pro : contradiction entre SQL illimité et contrôleur plafonné à 20. | Actif, quota Pro à corriger | SQL `021_Next_Improves.sql` lignes 4081-4084 ; PS `ScopedElement.php` lignes 274-325 | « Vous pouvez rattacher des publications Instagram à votre fiche. » Publier les quotas gratuits seulement. Ne pas annoncer le quota Pro avant correction. |
| Menu digital | Oui | Oui | Non | Aucun quota commercial identifié | Actif | `PartnerEntitlements.php` force `DIGITAL_MENU` à vrai ; SQL lignes 4089-4116 | « Le menu digital fait partie du socle gratuit. » |
| Catalogues, catégories et sous-catégories | Oui pour le socle publié | Capacités avancées selon configuration | Non établie | Aucun quota publié | Actif | Routes et contrôleurs `Product.php`, `ElementMenu.php`; tests catalogue PS | « Organisez vos produits dans un ou plusieurs menus ou catalogues. » |
| Produits, services, prix et disponibilités | Oui pour la présentation | Selon fonctions commerciales activées | Vente ou paiement selon le parcours | Règles propres au produit | Actif | Contrôleurs Product/ElementMenu et modèles de catalogue | « Présentez vos produits, services, prix et disponibilités. » |
| Produits signatures / produits du moment | Oui comme mise en valeur éditoriale | Selon administration | Non établie | Aucun quota validé | Actif, libellé commercial à cadrer | Modèle de catalogue et ciblage des offres | « Mettez en avant les produits qui représentent votre lieu ou répondent à un moment précis. » |
| Retours clients et réponse du lieu | Oui | Oui | Non | Aucun quota identifié | Actif | SQL `PARTNER_REVIEWS` activé pour Base et Pro ; `PartnerReview.php` | « Consultez les retours clients et répondez depuis l’Espace Partenaire. » Employer « retours clients », jamais « avis chauds ». |
| Statistiques de visibilité et d’interaction | Niveau de base à confirmer | Détail réservé à la formule commerçant supérieure | Non | Pas de quota | Actif avec niveaux | SQL `PARTNER_ANALYTICS_DETAILED` pour `PARTNER_PRIME` | « Suivez la visibilité et les interactions obtenues. Le niveau de détail dépend de la formule. » |
| Réservation de table | Non dans le mapping actuel du socle gratuit | Oui, formule commerçant supérieure, puis activation locale | Conditions propres au parcours | Bornes et capacités configurées par le lieu | Prêt | Décision conversation ; SQL lignes 4118-4123 ; PS `ReservationManagement.php`; FO `BookingQa.php` | « Activez la réservation lorsque la configuration de votre lieu est prête. » |
| Réservation de prestation ou d’équipement | À confirmer par formule | Selon droit et activation | Paiement possible selon configuration | Capacité par créneau | Prêt techniquement, droits à confirmer | PS `ReservationManagement.php`; fonctions `STANDARD_BOOKING`, `SERVICE_BOOKING`, `EQUIPMENT_BOOKING` | « iziLife peut gérer différents parcours de réservation selon l’activité du lieu. » Ne pas détailler les droits par formule avant validation commerciale. |
| Demande de privatisation | Liée à l’accès réservation du lieu | Oui selon configuration | Gratuité, paiement ou minimum de consommation configurables | Min/max de participants et durée métier | Prêt | Décision conversation ; FO `BookingQa.php`; tests de privatisation FO/PS | « Recevez et traitez des demandes de privatisation avec les conditions propres au lieu. » |
| Demande de devis | Selon le parcours de demande | Selon configuration | Conditions propres au lieu | Aucun quota publié | Prêt dans les demandes de service, périmètre à cadrer | `ServiceRequestService`, parcours de privatisation et configuration commerciale | « Recueillez les informations nécessaires à une demande particulière ou à une privatisation. » Éviter de promettre un moteur général de devis pour tous les produits. |
| Publication et gestion d’événements | Oui selon accès au PS | Oui | Billetterie et paiements selon configuration | Limites média propres aux événements | Actif | Routes PS `event/create`, mises à jour et programmation | « Publiez vos événements et leurs informations pratiques. » |
| Billetterie événement | Selon droit de la formule commerçant | Oui lorsque configurée | Vente et commission selon conditions à valider | Capacité globale, quotas par tarif et maximum par utilisateur | Actif techniquement | Test FO `EventTicketRulesSourceContractTest.php`; routes de paiement événement | « iziLife peut gérer la vente de billets lorsque la billetterie est activée. » Ne publier ni commission ni frais. |
| Offre habituelle du lieu | Oui pour création/présentation selon accès | Oui | Sans achat ou avec mécanique configurée | Période et cible définies par l’offre | Actif | PS `PartnerOffers.php`; FO pages offres et Deals | « Publiez une offre permanente ou ponctuelle adaptée à votre activité. » |
| Offre ciblée sur un produit ou une catégorie | Oui selon accès | Oui | Selon mécanique de l’offre | Produits et catégories explicitement ciblés | Actif | `OfferTargetResolver`, panier et formulaire PS | « Une offre peut concerner un produit, une catégorie ou une sélection précise. » |
| Avantages iziLife Pass / iziLife Prime | Côté client : non, abonnements payants | Deux abonnements utilisateurs | Avantage défini par le lieu et les règles de bénéfice | Quotas selon chaque règle | Actif | Décision conversation ; plans `USER_PASS` et `USER_PRIME`; moteur BPR et tests offres/avantages | « Le lieu peut proposer des avantages aux membres iziLife Pass et iziLife Prime. » Ne publier aucun pourcentage ni règle de cumul non validés. |
| Cash & Traffic | Non qualifié comme gratuit | Opération commerciale | Commission à valider | Durée, volume, cible et usage configurés | Actif sous le type technique `PROMOTIONAL_SALE`, nom commercial à confirmer | PS `PartnerOffers.php`; parcours d’achat et grants FO | « Une opération limitée dans le temps peut soutenir la vente d’un produit ou d’une sélection précise. » Utiliser le nom Cash & Traffic seulement après validation de sa correspondance avec `PROMOTIONAL_SALE`. |
| Last Minute | Non qualifié | Opération commerciale | Commission à valider | Un jour et une plage horaire ; capacité possible ; réservation possible | Prévu au lancement | Décision conversation ; PS `OfferFeatureFlags.php` et `PartnerOffers.php`; FO `LastMinuteFulfillmentResolver.php` | « Au lancement, Last Minute permettra de vendre une disponibilité à utiliser rapidement, sur le créneau défini. » |
| Offres collectives | Non | Non commercialisé | À définir | Paliers et fenêtre de déclenchement existent techniquement | Futur | Flags désactivés par défaut ; paiement collectif non pris en charge en production | « Les offres collectives sont prévues pour une phase ultérieure. » |
| Boost de visibilité | Non dans le socle Base actuel | Droit commerçant supérieur et/ou crédits | Achat en crédits ou en monnaie selon règle | Période, surface et budget définis par la demande | Actif sous validation | SQL `PARTNER_BOOST`; PS `PartnerBoost.php`; BO `PartnerBoostReview.php` | « Demandez la mise en avant d’un lieu, événement, produit ou offre pendant une période définie. » Aucun prix ni résultat garanti. |
| Sélection utilisable dans plusieurs lieux | Non | Produit séparé | Prix et contrats à valider | Variantes, paliers et participations existent dans le modèle | Futur commercialement | Routes FO/BO, modèles Selection et tests d’achat ; décision du brief | « Les Sélections multi-lieux font partie des services prévus pour plus tard. » |
| Parcours composé de plusieurs étapes | Non | Produit séparé | Prix et contrats à valider | Composition et participations par lieu | Futur commercialement | Modèles `SelectionComposition` et `SelectionParticipation` | « À terme, iziLife pourra composer une sortie en plusieurs étapes avec des lieux participants. » |
| Commande en ligne / click & collect | Non | Non | Non | Fonction explicitement fermée | Non disponible | `PartnerEntitlements.php`; SQL lignes 4125-4130 | Ne pas présenter dans le support général. |
| Organisation d’animations avec prestataire | Non | Non | Non | Sans objet | Abandonné | Décision conversation | Ne plus mentionner. Le lieu peut uniquement publier ses propres événements. |

## 4. Contradictions et points à arbitrer avant un catalogue tarifaire

1. **Médias externes Pro** : le SQL met le quota à `NULL` pour signifier illimité, mais le contrôleur PS transforme `NULL` en plafond de 20 et limite les médias actifs à 10. Le support général peut annoncer l’intégration Instagram, mais pas un quota Pro précis.
2. **Last Minute en production** : la décision métier fixe un lancement. Le code conserve plusieurs verrous d’environnement, dont certains refusent les opérations en production. Le lancement nécessite donc une configuration et probablement un alignement du garde-fou FO.
3. **Cash & Traffic** : la mécanique `PROMOTIONAL_SALE` est active. Il reste à confirmer que Cash & Traffic constitue bien son nom commercial officiel et qu’aucune règle supplémentaire ne la distingue.
4. **Réservations autres que table** : les moteurs Standard, Service et Equipment existent. Le tableau des droits exacts par formule commerçant doit être figé avant le catalogue commercial.
5. **Demande de devis** : la privatisation et les demandes particulières sont prêtes. Un moteur universel de devis pour toute fiche ou tout produit n’est pas démontré.
6. **Billetterie** : le flux technique contrôle capacités, quotas et achats. Les conditions financières et le périmètre commercial restent à valider.
7. **Analytics** : le détail est associé à la formule commerçant supérieure. Les indicateurs exacts affichables dans une présentation doivent être sélectionnés sur des écrans réels.

## 5. Storyboard détaillé du Support A — présentation générale sans prix

### Slide 1 — iziLife pour les commerces

**Message** : gérer sa présence en ligne et apparaître dans les projets de sortie.  
**Contenu** : logo, phrase courte, photographie réelle d’un moment local avant une sortie.  
**Visuel** : une rue animée, un restaurant ou un bar proche d’un lieu culturel. Pas de cartes UI.

### Slide 2 — Deux usages reliés

**Message** : l’utilisateur prépare sa sortie pendant que le lieu maîtrise les informations qui l’aident à choisir.  
**Contenu** : à gauche, recherche et préparation ; au centre, iziLife ; à droite, fiche et outils du lieu.  
**Preuve à montrer** : un écran réel de recherche ou de fiche, sans donnée sensible.

### Slide 3 — Avant la venue

**Message** : l’utilisateur consulte les informations utiles avant de se déplacer.  
**Contenu** : ambiance, horaires, adresse, accès, équipements, services, prix indicatifs, menu, événements et offres.  
**Visuel** : une fiche réelle annotée avec quatre ou cinq points maximum.

### Slide 4 — Le socle gratuit

**Message** : une présence exploitable dès le référencement gratuit.  
**Contenu** : informations du lieu, horaires, liens, menu digital, retours clients et jusqu’à 5 médias par fiche.  
**Note orale** : distinguer les médias importés des publications Instagram rattachées.

### Slide 5 — L’Espace Partenaire

**Message** : le commerçant garde la main sur les informations et les activations de son lieu.  
**Contenu** : mettre à jour la fiche, gérer les horaires, publier les contenus, suivre les demandes et répondre aux retours.  
**Visuel** : capture réelle du tableau de bord ou montage de deux écrans maximum.

### Slide 6 — Photos, ambiance et Instagram

**Message** : montrer le lieu tel qu’il se vit.  
**Contenu** : médiathèque, image de couverture et publications Instagram rattachées.  
**Garde-fou** : ne pas annoncer le quota Pro des médias externes avant correction de la contradiction.

### Slide 7 — Menus et catalogues

**Message** : rendre l’offre compréhensible avant la visite.  
**Contenu** : plusieurs menus ou univers, catégories, produits, services, prix, disponibilités et produits mis en avant.  
**Visuel** : écran réel d’un catalogue comportant des catégories.

### Slide 8 — Réservations et privatisations

**Message** : recevoir une réservation ou une demande particulière depuis la fiche du lieu.  
**Contenu** : réservation de table, parcours adaptés à certaines prestations, privatisation et informations nécessaires à la demande.  
**Garde-fou** : ne pas promettre que tous les types de lieux disposent du même parcours.

### Slide 9 — Événements et billetterie

**Message** : publier ce qui se passe dans le lieu et permettre l’achat lorsque la billetterie est activée.  
**Contenu** : informations, dates, programmation, capacité, tarifs et billets.  
**Garde-fou** : aucune offre d’organisation d’animation ou de mise en relation avec un prestataire.

### Slide 10 — Trois familles d’offres

**Message** : le lieu choisit le type d’avantage adapté à son objectif.  
**Contenu** : offres habituelles du lieu ; avantages réservés aux membres iziLife Pass et iziLife Prime ; opérations commerciales limitées dans le temps.  
**Visuel** : trois exemples concrets, sans pourcentage imposé.

### Slide 11 — Autour d’un concert

**Message** : iziLife fait découvrir un commerce dans le contexte réel d’une sortie.  
**Contenu** : fin de journée, concert prévu, recherche autour de la salle, comparaison de restaurants, avantage membre proposé par l’un d’eux.  
**Visuel** : mini-parcours chronologique avec carte locale et restaurant voisin.  
**Garde-fou** : les pourcentages éventuels restent des exemples oraux tant qu’ils ne correspondent pas à une offre validée.

### Slide 12 — Cash & Traffic

**Message** : soutenir la vente d’un produit ou d’une courte sélection pendant une campagne limitée.  
**Contenu** : cible de l’offre, période de vente, quantité disponible, achat puis utilisation dans les conditions définies.  
**Garde-fou** : ne montrer ni remise type, ni commission, ni durée standard.

### Slide 13 — Last Minute au lancement

**Message** : proposer une disponibilité qui doit être utilisée rapidement.  
**Contenu** : jour, plage horaire, capacité disponible et éventuel lien avec une réservation, un événement ou une expérience.  
**Visuel** : exemple d’un créneau restant le jour même, sans prix.

### Slide 14 — Boosts de visibilité

**Message** : mettre temporairement en avant le contenu qui compte pour le lieu.  
**Contenu** : lieu, événement, offre ou produit ; période ; emplacements ; demande soumise à validation.  
**Garde-fou** : aucun tarif, aucune portée garantie et aucun engagement de fréquentation.

### Slide 15 — Services prévus pour plus tard

**Message** : identifier clairement ce qui ne fait pas encore partie de l’offre disponible.  
**Contenu** : offres collectives et Sélections multi-lieux ou en plusieurs étapes.  
**Visuel** : deux concepts simples portant chacun la mention « à venir ».

### Slide 16 — Le premier test adapté au lieu

**Message** : commencer par un usage concret et mesurable.  
**Contenu** : diagnostic de la présence actuelle, choix du besoin prioritaire, mise en place du premier usage, observation des interactions.  
**Appel à l’action** : convenir du lieu, du contenu à mettre à jour et du premier test. Aucun prix.

## 6. Recommandation de narration orale

Le rendez-vous ne doit pas commencer par les abonnements ni par une liste de fonctions. Il doit suivre cette logique :

1. comprendre comment le commerce veut être trouvé et à quels moments ;
2. montrer ce que l’utilisateur voit avant de venir ;
3. montrer comment le commerçant garde ces informations à jour ;
4. présenter les actions possibles, de la réservation aux offres ;
5. illustrer la découverte contextuelle avec le concert ;
6. choisir un premier usage à tester.

## 7. Validation demandée avant création du PowerPoint

Avant de fabriquer le support final, valider :

- l’expression commerciale « Cash & Traffic » pour la mécanique `PROMOTIONAL_SALE` ;
- le traitement du quota Pro des publications Instagram ;
- le niveau de détail à montrer pour les formules commerçants, sans prix ;
- les captures réelles à utiliser pour le FO et l’Espace Partenaire ;
- le maintien de 16 slides ou la fusion des slides 6 et 7 pour revenir à 15.

