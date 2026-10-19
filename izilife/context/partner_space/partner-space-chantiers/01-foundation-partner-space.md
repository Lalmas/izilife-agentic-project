# BRIEF À COPIER — Foundation Partner Space

Je poursuis le chantier **iziLife Partner Space Foundation**. Travaille sur l'ensemble du système :

- `izilife` : front-office public et espace utilisateur ;
- `izilife-admin` : back-office iziLife ;
- `izilife-partner-admin` : cockpit Partner.

Le Partner Space n'est pas un BO miniature. C'est un espace professionnel visible par des clients Partner, appelé à devenir le cockpit transversal d'iziLife pour des commerces, lieux, organisateurs, médias, collectivités, artistes, DJ, coachs et autres structures. Tous n'auront pas les mêmes objets ni les mêmes capacités.

## Objectif de cette conversation

Finir et stabiliser le socle permettant ensuite de lancer sans dette dangereuse les chantiers Réservation/Privatisation, Catalogue/Menu digital, paiement commercial, Boost et exploitation.

Avant toute modification, audite les trois projets et la base SQL existante. Distingue ce qui fonctionne réellement, ce qui est prototype, ce qui est codé en dur et ce qui manque. Ne crée pas une nouvelle structure si une structure correcte existe déjà.

N'implémente rien tant que je n'ai pas dit **Go**. Avant le Go, produis le diagnostic, les arbitrages nécessaires et le plan d'exécution précis.

## 1. Partner, identité et création

- Reprendre la page existante de création et de mise à jour des informations Partner.
- Revoir le processus de création d'un Partner.
- Un Partner doit pouvoir être créé sans PSP, sans IBAN et sans capacité de paiement.
- Séparer les états suivants : compte/cockpit Partner, identité légale, vérification/KYB, compte PSP, capacité d'encaissement, capacité de payout.
- SIRET, PSP et IBAN ne doivent pas bloquer l'accès au cockpit lorsque l'activité du Partner n'en a pas besoin.
- Préparer plusieurs types de Partner et des capacités extensibles. Ne pas ouvrir automatiquement toutes les fonctions à un DJ, un média, une collectivité, un commerce ou un organisateur.
- La décision finale « certaines Pages sont-elles gérées dans le Partner Space ou dans le User Space FO ? » reste ouverte. L'architecture ne doit pas rendre ce choix irréversible.

### Audit déjà identifié à confirmer dans le code

- La page Partner Banking affiche actuellement des lieux/comptes PSP factices codés dans la vue : ne pas les interpréter comme des données BDD.
- Remplacer ce prototype par les véritables objets possédés par le Partner courant.
- Auditer `PspAccount` : une seule portée d'entité cohérente doit être possible par compte.
- Vérifier les modèles bancaires non initialisés, les variables de vue incohérentes et les mutations effectuées en GET.
- L'écran IBAN brut doit être désactivé tant que stockage, chiffrement, masquage, rétention, logs, rôles et audit ne sont pas démontrés.
- Préférer l'onboarding hébergé par le PSP et ne conserver que l'identifiant fournisseur, le statut et des informations masquées.
- Le PIN visuel `TODO` n'est pas une protection des données bancaires.

## 2. Ownership, rôles et capacités

- Commencer par un RBAC simple et strict par rôle, sans importer pour le moment toute la complexité internationale/zones du BO.
- Rôles de base à auditer et stabiliser : Root/Owner/Admin/Manager/Staff.
- Le Staff ne doit presque rien muter par défaut.
- Chaque endpoint et chaque action doivent vérifier le Partner, le rôle, l'ownership explicite, le scope de l'objet et la capacité fonctionnelle.
- Le Partner ne modifie que les objets qu'il possède ou organise explicitement.
- Les objets accueillis dans ses lieux mais organisés par un tiers sont visibles en lecture seule.
- Les capacités sont testées par code fonctionnel, jamais en comparant directement le nom d'un abonnement.

## 3. Réclamations, attribution, don et transfert

- Il n'y a pas de création libre de Place/Shop par le Partner.
- Créer le module transversal de demandes Partner et le workflow BO contrôlé pour : réclamation d'une fiche, attribution, don, transfert de propriété et futures modifications sensibles.
- Préparer les scopes : Place, Shop, Page, Equipment, EventSerie, AnnualCelebration et autres objets pertinents après audit.
- Circuit : préparer la possibilité sans l'activer tant que sa gestion BO n'est pas éprouvée.
- Le BO doit pouvoir créer une demande interne et rattacher un Partner à un Place/Shop sans contourner le workflow, sauf éventuelle attribution initiale lors de la création ; ce point doit être arbitré après audit du processus actuel.
- Conserver historique, initiateur, ancien/nouveau propriétaire, justificatifs, décision, motif, dates et journal d'audit.

## 4. Place / Shop

Reprendre le socle, il n'est pas considéré terminé.

- Densité visuelle proche du BO, avec CSS strictement limité au Partner Space.
- Adresse et téléphone affichés en lecture seule ; changement ultérieur par procédure.
- Email complet uniquement pour Owner/Admin/Manager autorisés, masqué ou absent pour Staff ; modification future par demande avec vérification.
- Liens sociaux et site uniquement dans le module Links.
- Catégories et multi-catégories visibles, prises en compte partout, mais non modifiables par le Partner pour le moment.
- Informations popup store seulement si pertinentes.
- Une seule image de couverture, conforme au FO actuel.
- Autocomplete unifié « Lieu » pour l'emplacement dans/sur un autre lieu.
- Toilettes, accès toilettes, minimum éventuel, type d'accès, réservation et tarif de base à zéro conservés dans une section adaptée.
- Préparer les procédures de changement d'adresse, téléphone, email, propriétaire, sans nécessairement toutes les ouvrir immédiatement.

## 5. Horaires

- Conserver l'architecture `Hourly` + `HourlyContent` existante.
- Supporter plusieurs Hourly par objet et par contexte/catégorie : général, restaurant, horaires d'été, d'hiver, saisonniers, actifs/inactifs, etc.
- Afficher une ligne ou card par Hourly avec action Ajouter/Modifier selon l'existence de son contenu.
- Le formulaire hebdomadaire reste unique : modification des sept jours puis enregistrement global, pas de validation ligne par ligne.
- Conserver fermeture, première plage, pause et seconde plage.
- Gérer les horaires exceptionnels récents, qui remplacent la semaine habituelle.
- Réutiliser les helpers BO/FO existants pour les libellés et résumés ; ne pas concaténer un résumé artisanal incorrect.
- Auditer et corriger les méthodes Partner Hourly utilisant des variables de colonne ou catégorie non définies.

## 6. Event, XP et EventSerie

- Finaliser la gestion Partner des Event et XP existants, sans casser la billetterie Event actuelle.
- Entrée de création guidée commune permettant d'orienter vers Event classique, Event récurrent, EventSerie ou XP activité collective.
- Les autres types de XP peuvent être une branche du même parcours si le code et l'UX le permettent ; ne pas créer un second moteur sans audit.
- Un Event organisé par le Partner est administrable ; un Event seulement accueilli dans un de ses lieux est consultable en détail mais non modifiable.
- Finaliser EAP Event/XP, BC/BCC, SC/SCC, Sessions, annulations/modifications, participants, réservations et contraintes lorsqu'il existe déjà des achats ou réservations.
- Préserver les contrats commerciaux Event existants avant toute factorisation générique.

### EventSerie

- Création via le parcours guidé commun.
- État draft/instruction modifiable immédiatement.
- Soumission : email interne vers `contact@izilife.co`.
- Analyse différée toutes les cinq minutes, inspirée du pipeline Review, capable ultérieurement d'OCR et d'analyse texte/LLM.
- Validation humaine dans une page BO dédiée.
- Inactive et non publiable avant acceptation.
- Aucune Edition ne peut être créée avant acceptation et activation de l'EventSerie.
- AnnualCelebration reste créée en BO mais est visible dans « Grands événements » du Partner.

### Conversion d'objets

- Préparer dans le BO un workflow global, transactionnel et audité pour les conversions Event, XP et EventSerie.
- Exemples : Event vers XP avec purge contrôlée de l'ancien objet ; XP activité collective vers Event ; Event vers EventSerie ; EventSerie vers Event ou XP.
- Pas de boutons qui réécrivent directement plusieurs tables. Utiliser analyse, prévisualisation, validation, exécution atomique, journal et stratégie de reprise.

## 7. Paiement, abonnement et transactions Partner

- Gratuit implicite et Pro payant.
- Pro mensuel : 100 euros ; annuel : 1 000 euros, soit deux mois offerts.
- Architecture multi-plan conservée pour un éventuel second niveau futur.
- Prévoir promotion/essai, renouvellement, changement mensuel/annuel, résiliation immédiate ou fin de période, échec, remboursement exceptionnel, facture et webhooks Stripe.
- Après échec : grâce de sept jours avec retries ; le BO peut prolonger manuellement avec motif et audit.
- Multi-établissement préparé.
- Séparer `IZILIFE_USER` et `IZILIFE_PARTNER` dans Feature/entitlements. Les features User inutiles ne doivent pas être exposées au Partner.
- Un Partner n'achète pas ses propres Event/XP/EAP dans le Partner Space.
- Les seuls contextes d'achat Partner à ouvrir pour le moment sont `PARTNER_SUBSCRIPTION` et `PARTNER_BOOST`.
- PayHub peut rester le moteur commun mais ses contextes User inutiles ne sont pas affichés dans le Partner Space.

### Transactions et chiffres

- Exposer au Partner les ventes de ses Event/XP/EAP : chiffre prévisionnel, annulations possibles, commissions, remboursements et couvertures pertinentes.
- Le statut Booking et le statut Transaction restent deux workflows distincts.
- Les chiffres détaillés et analytics avancés sont Pro ; une synthèse limitée reste disponible gratuitement.
- Préparer le chemin vers facture électronique, exports et clôtures Z, sans construire ces fonctions maintenant : ce n'est pas la priorité.

## 8. Médias, ExternalMedia et Equipment

- Adapter le nouveau module média du BO : recherche, filtres, pagination, titre, provenance, ownership, objet et statut.
- Une galerie en cards reste acceptable comme sélecteur local, mais pas comme médiathèque de 50 à 200 médias.
- Le Partner n'ajoute et ne sélectionne que les médias lui appartenant.
- Même règle pour `ExternalMedia`, avec une UX plus légère puisque le volume actif attendu est faible.
- Les limites sont pilotées ensuite par abonnement/capacité.
- Créer la gestion Partner des Equipment vivants lui appartenant, avec scope par lieu.
- Ne pas ouvrir pour le moment l'association Partner d'Equipment à Event, XP ou Page sans décision explicite.

## 9. Ce que Foundation doit préparer sans ouvrir artificiellement

- produits et `ElementMenu` ;
- `ElementService` ;
- EAP génériques ;
- moteur de réservation et privatisation ;
- commande en ligne ;
- acompte et paiement iziLife ;
- Boost et placements ;
- actualités/publications selon le type de Partner ;
- gestion de Pages officielles ;
- facturation électronique et exports futurs.

## Livrables attendus après le Go

1. Audit documenté des trois projets et du SQL.
2. Matrice rôles × capacités × objets × actions.
3. Modèle d'ownership et de demandes/transferts.
4. Plan SQL additif et compatible.
5. Correction progressive des modules dans l'ordre des dépendances.
6. Tests d'IDOR, ownership, rôle, CSRF, mutations GET et scopes multi-lieux.
7. Vérifications fonctionnelles FO/BO/Partner et absence de régression Event.
8. Documentation des capacités laissées désactivées.

