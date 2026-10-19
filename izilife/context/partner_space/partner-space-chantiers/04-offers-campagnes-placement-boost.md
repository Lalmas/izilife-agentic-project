# BRIEF À COPIER — Offers, Campagnes, Placement et Boost

Je lance le chantier **iziLife Offers / Campagnes / Placement / Boost** sur `izilife`, `izilife-admin` et `izilife-partner-admin`.

Avant de coder, audite l'intégralité des structures Offer, BPR, campagnes, placements, couvertures, médias, tracking, PayHub et anciens parcours User/Partner. Ne remplace pas les règles existantes avant de les avoir comprises.

## Objectif

Faire évoluer Offer et Campaign vers des coquilles éditoriales/commerciales cohérentes avec une couverture et des règles de ciblage, puis ouvrir un Boost simple acheté par le Partner et diffusé de façon explicitement sponsorisée.

## Frontières de domaine

- Le Catalogue décrit ce que propose normalement un objet.
- Une Offer porte une promotion, un avantage, un bon plan ou une opération commerciale.
- Une Campaign organise une diffusion dans le temps et sur des emplacements.
- Une BPR configure les règles d'éligibilité, de réduction ou de comportement.
- Un Placement représente une présence dans une zone de diffusion.
- Un Boost est un achat Partner qui finance ou active un placement.
- Une couverture/média illustre la coquille mais ne constitue pas la règle métier.

Ne pas fusionner ces concepts dans une seule table ou un seul écran artificiel.

## Offer

- Reprendre le menu et les pages Offer existants, actuellement jugés insuffisants.
- Donner à Offer une véritable coquille : titre, résumé, contenu, couverture, période, statut, ownership, organisateur/objet source et visibilité.
- Préparer les familles : Offer classique, spéciale, Happy Hour, étudiant, Last Minute et futures grosses opérations.
- Réutiliser les BPR existantes après audit.
- Une Offer peut cibler Place, Shop, Event, XP, EventSerie ou Page selon capacités.
- Elle peut aussi cibler des éléments de Catalogue : ElementMenu, catégorie, Product, EAP ou ElementService.
- Le ciblage ne transfère pas l'ownership de l'objet ciblé.
- Respecter partout la multi-catégorie.

## Campaign et placements

- Auditer puis refondre Campaign sans casser les campagnes externes existantes.
- Les campagnes d'ouverture restent exclusivement créées, administrées et attribuées par iziLife en BO. Elles ne sont pas créables par un Partner.
- Le système possède ou prévoit aussi des campagnes éditoriales iziLife telles que « Semaine de la Street Food », « Semaine de l'étudiant » et autres opérations thématiques.
- Préserver et auditer les types de Campaign existants, notamment `CelebrationDay`, plutôt que recréer une table parallèle.
- Un Event disposant d'une `Offer` éligible doit pouvoir être rattaché à une Edition d'AnnualCelebration, à une Campaign `CelebrationDay` ou à une autre Campaign créée par iziLife.
- Le Partner peut proposer ou sélectionner son Event/Offer pour une campagne ouverte aux contributions si iziLife l'autorise ; l'association définitive et la publication restent contrôlées/validées par iziLife.
- AnnualCelebration et ses Editions restent administrées par iziLife. Le Partner voit les grands événements et les rattachements qui concernent ses objets, sans créer l'AnnualCelebration.
- Permettre plusieurs emplacements/zones de diffusion configurables.
- Les remontées sponsorisées doivent toujours être étiquetées « Sponsorisé ».
- Préparer un swiper ou composant de campagne adapté au FO.
- Séparer sélection organique, règle éditoriale iziLife et placement payé.
- Conserver dates, budget/quantité, consommation, statut, cible et journal d'exécution.

## PARTNER_BOOST

- Ajouter un nouveau contexte PayHub Partner dédié au Boost.
- Le parcours doit rester simple et proche de l'achat User existant lorsque cela est pertinent.
- Le Partner choisit uniquement un objet qu'il possède ou organise et un placement auquel il est éligible.
- Le serveur revérifie ownership, statut/publicabilité, capacité, dates, prix et disponibilité du placement.
- Prévoir paiement, succès, échec, expiration, annulation, remboursement exceptionnel et webhook idempotent.
- Afficher au Partner le coût, la période, le statut, les impressions/couvertures/clics disponibles et les limites de son abonnement.
- Ne pas exposer dans le Partner Space les autres contextes PayHub destinés aux achats User.
- Les seuls achats Partner ouverts à ce stade restent `PARTNER_SUBSCRIPTION` et `PARTNER_BOOST`.

## Abonnement et entitlements

- Gratuit implicite et Pro payant, mais les règles de Boost sont testées par capacités.
- L'architecture reste multi-plan même s'il n'existe qu'un Pro aujourd'hui.
- Déterminer explicitement ce qui est inclus, limité, payant à l'acte ou interdit.
- Ne jamais coder `if plan == pro` dans les contrôleurs métier lorsque l'entitlement peut répondre directement.

## Tracking et finances

- Définir les événements de tracking avant d'afficher des performances.
- Distinguer couverture/impression, visibilité réelle, clic, ouverture de fiche, conversion et vente.
- Ne pas promettre une attribution que les données ne permettent pas de prouver.
- Le tableau Partner montre dépense, période, consommation, statut et métriques autorisées Gratuit/Pro.
- Transactions, commissions et remboursements utilisent PayHub ; ne pas construire un deuxième ledger dans Boost.

## Sécurité et modération

- Une Offer ou Campaign en brouillon ne peut pas devenir publiable par simple altération d'un ID ou statut envoyé par le Front.
- Les objets soumis à validation iziLife restent bloqués jusqu'à décision BO.
- Contrôler contenus, médias, dates, ownership, rôles et scopes multi-lieux.
- Toutes les mutations sont POST et protégées ; les webhooks sont signés et idempotents.

## Phasage

1. Audit Offer/BPR/Campaign/Placement/PayHub/tracking.
2. Modèle de coquille Offer et couverture.
3. Ciblage des objets et éléments Catalogue.
4. Rattachement Event/Offer aux Editions d'AnnualCelebration et Campaigns iziLife.
5. Refonte Campaign et zones de placement.
6. Affichage FO sponsorisé.
7. Contexte `PARTNER_BOOST` et paiement.
8. Cockpit Partner et métriques.
9. Last Minute et opérations avancées derrière capacités.

## Hors périmètre initial

- moteur publicitaire programmatique ;
- enchères temps réel ;
- génération automatique non validée d'une Offer ;
- comptabilité/facturation électronique complète ;
- attribution marketing sophistiquée sans données fiables.

## Livrables

- cartographie et arbitrage des structures existantes ;
- modèle Offer/Campaign/Placement/Boost ;
- contrat de ciblage BPR/Catalogue ;
- plan PayHub et webhooks ;
- écrans FO/BO/Partner ;
- tracking documenté ;
- tests ownership, IDOR, paiement idempotent et publication ;
- documentation des fonctions préparées mais désactivées.

## Décision — plusieurs mécaniques dans une Offer

Le Partner configure toujours une première mécanique comme auparavant. Elle crée ou met à jour le premier `BenefitPolicyRuleEffect`. Pour une Offer non opérationnelle, le Partner peut ajouter d'autres mécaniques puis affecter chaque catégorie ou élément précis à l'une d'elles. Avec un seul Effect, cette affectation est automatique.

Les opérations Cash & Trafic, Last Minute et collectives restent volontairement mono-Effect afin de conserver un prix d'achat, un panier et un snapshot de paiement non ambigus. Le serveur refuse également tout chevauchement produit/catégorie entre deux Effects.
