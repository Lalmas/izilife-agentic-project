# BRIEF À COPIER — Wallet & Crédits iziLife

Je lance le chantier transversal **iziLife Wallet & Crédits** sur `izilife`, `izilife-admin` et `izilife-partner-admin`.

Avant toute modification, audite le SQL, PayHub, Transaction, les abonnements User et Partner, les crédits MeetZ, les remboursements, cadeaux/claims, prorata d'abonnement, Event/XP/EAP et toutes les colonnes `wallet_id` ou logiques de crédit existantes. L'objectif n'est pas de généraliser aveuglément les anciennes implémentations, mais d'en extraire les invariants utiles sans casser les parcours actifs.

## Objectif

Construire un ledger commun, auditable et multi-contexte pour représenter :

- un Wallet User ;
- un Wallet Partner lorsque nécessaire ;
- des crédits iziLife ;
- des crédits restreints à un contexte ou un objet ;
- des avoirs/remboursements ;
- des cadeaux et compensations ;
- des mouvements liés à Event, XP, EAP, Booking, abonnement, Boost et futurs achats.

Le Wallet ne doit pas devenir une simple colonne `balance` modifiée directement. Le solde est la conséquence de mouvements immuables et rapprochables.

## Décisions structurantes

- Séparer argent réel, crédit promotionnel, avoir de remboursement, cadeau, crédit MeetZ et éventuels points non monétaires.
- Ne jamais mélanger un crédit monétaire avec un entitlement d'abonnement ou une Feature.
- Définir devise, montant en unité mineure, propriétaire, source, contexte, restrictions, expiration et état de chaque crédit.
- Une écriture validée n'est pas modifiée ou supprimée : une correction produit une écriture inverse/compensatrice.
- Toute consommation est atomique, idempotente et protégée contre la double dépense.
- PayHub reste le moteur de paiement ; Wallet est un moyen de financement/compensation et un ledger, pas un second PSP.
- `BookingStatus`, `TransactionStatus`, statut du crédit et statut du mouvement restent distincts.
- Le Partner ne peut jamais créditer arbitrairement son propre Wallet ou celui d'un User.
- Les opérations manuelles BO exigent rôle, motif, référence, initiateur et audit.

## Modèle conceptuel à auditer puis stabiliser

- `Wallet` : propriétaire polymorphe contrôlé, devise, statut.
- `WalletEntry` ou mouvement : crédit/débit, montant, nature, contexte, référence métier, idempotency key, dates.
- `CreditGrant`/lot logique : origine, valeur initiale, restant, restrictions, priorité d'utilisation, expiration.
- `WalletAllocation` : ventilation d'un débit entre plusieurs lots de crédit.
- `WalletHold` éventuel : réservation temporaire avant confirmation d'un paiement ou d'une Booking.
- Liens explicites vers Transaction, remboursement, Booking, EAP, abonnement, Boost ou geste commercial.

Ne crée pas obligatoirement ces noms/tables : commence par confronter ce modèle aux structures SQL existantes.

## Contextes

Prévoir sans tout ouvrir immédiatement :

- achat FO Event/XP/EAP ;
- réservation/acompte ;
- remboursement en argent ou en avoir selon règle et consentement ;
- cadeau/claim ;
- MeetZ et récupération des crédits existants ;
- prorata/changement d'abonnement ;
- compensation SAV ;
- abonnement Partner ;
- `PARTNER_BOOST` ;
- commande future.

Chaque crédit peut être universel ou restreint : domaine User/Partner, type d'achat, objet, Partner émetteur, campagne, dates ou zone. Une restriction est vérifiée côté serveur au moment du devis puis à nouveau à la consommation.

## Paiement mixte

- Supporter crédit seul, PSP seul et crédit + PSP.
- Réserver/consommer le crédit de façon atomique avec la transaction.
- En cas d'échec PSP, timeout ou webhook tardif, libérer ou réconcilier correctement le crédit.
- Les remboursements ventilent la part PSP et la part Wallet selon une politique explicite.
- Aucun montant négatif, dépassement de solde ou arrondi flottant : utiliser les unités mineures et une devise explicite.

## Expiration et réclamations

- Définir les crédits expirables et non expirables.
- Prévoir notifications avant expiration, sans les rendre bloquantes pour la première tranche.
- Une réclamation peut placer un mouvement ou un remboursement en examen sans réécrire l'historique.
- Préparer le décalage entre transaction, contestation, remboursement et futurs documents financiers.

## Interfaces

### User Space FO

- solde disponible expliqué ;
- détail par type de crédit et expiration ;
- historique lisible ;
- application au checkout ;
- origine et restrictions compréhensibles.

### Partner Space

- uniquement les mouvements et impacts qui concernent le Partner ;
- aucune exposition des mécanismes internes ou Wallets d'autres acteurs ;
- lecture des ventes, crédits/remboursements affectant ses prévisions et commissions ;
- actions limitées aux workflows explicitement autorisés.

### BO

- recherche, rapprochement et audit ;
- attribution/compensation manuelle contrôlée ;
- annulation par mouvement inverse ;
- gestion des expirations et incidents ;
- vision des références PayHub/Transaction/Booking.

## Sécurité et comptabilité technique

- Contrôles ownership/IDOR sur chaque Wallet et mouvement.
- Aucun endpoint client ne choisit librement le propriétaire, le montant ou la nature comptable.
- Idempotency keys obligatoires pour callbacks et créations sensibles.
- Transactions SQL et verrouillage adaptés à la concurrence.
- Journal technique sans données bancaires sensibles.
- Ne pas appeler « facture » un historique Wallet.
- Préparer les exports et la facturation électronique future, mais ne pas construire maintenant clôtures Z ou comptabilité complète.

## Phasage

1. Audit de toutes les implémentations de crédits et Wallet existantes.
2. Taxonomie des valeurs et matrice des contextes/restrictions.
3. Contrat du ledger et règles d'idempotence.
4. Migration/compatibilité des crédits existants, particulièrement MeetZ et prorata.
5. Consultation BO et User.
6. Paiement mixte sur un seul parcours pilote.
7. Remboursement/avoir et réconciliation.
8. Extension contrôlée à Event/XP/EAP, Booking, Partner Subscription et Boost.

## Hors périmètre initial

- monnaie électronique transférable entre utilisateurs ;
- retrait libre d'un Wallet User vers un compte bancaire ;
- crypto-actifs ;
- comptabilité générale ;
- clôtures Z et facture électronique complète ;
- marketplace de crédits entre Partners.

## Livrables

- audit SQL/code et inventaire des crédits existants ;
- glossaire argent/crédit/avoir/point/entitlement ;
- matrice contexte × propriétaire × restriction × expiration ;
- modèle de ledger et invariants ;
- plan SQL/migration compatible ;
- contrats PayHub et remboursement ;
- écrans FO/BO/Partner nécessaires ;
- tests concurrence, double dépense, idempotence, arrondis, expiration, remboursement et IDOR ;
- documentation des contextes préparés mais désactivés.

