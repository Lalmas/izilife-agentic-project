# AnnualCelebration, EAP et futur cashless

Dernière mise à jour : 29 juillet 2026

Ce document complète `eap-modele-catalogue-diffusion.md`.

## 1. AnnualCelebration comme source de modèles

`AnnualCelebration` (AC) possède déjà ses propres EAP via `annual_celebration_id`. Lors de la création d'un Event rattaché, le BO sait recopier ces EAP vers l'Event.

AC doit donc être traitée comme EventSerie :

```text
AnnualCelebration
└── EAP modèles
    └── édition Event
        └── EAP locaux vendus par l'Event
```

La copie doit conserver `is_variant_of` et inclure packs, tarifs groupés et dépendances, comme pour EventSerie.

## 2. Séparer droit d'accès et valeur cashless

Un EAP peut :

- vendre l'entrée à l'AC ou à une édition ;
- inclure un crédit initial ;
- donner droit à l'ouverture ou à l'activation d'un compte cashless ;
- inclure un support physique.

Mais l'EAP ne doit jamais porter le solde. Le solde appartient à un compte Wallet et évolue par écritures de ledger.

```text
EAP/Ticket
└── droit d'accès et éventuel crédit initial

WalletAccount AC
└── solde rechargeable et consommable
```

## 3. Compte cashless

Le socle existant comprend déjà `Wallet`, `WalletAccount`, `WalletOperation`, un ledger, des sous-soldes cash/izi et une dépense atomique.

Pour une AC, il faudra pouvoir créer un compte avec un scope explicite :

- `annual_celebration` pour un solde réutilisable d'une édition à l'autre si l'organisateur l'autorise ;
- `event` pour un solde limité à une édition ;
- éventuellement `partner` pour un réseau cashless permanent.

Les opérations attendues sont :

- recharge en ligne ;
- recharge sur place ;
- paiement cashless ;
- annulation/reversal ;
- remboursement ;
- transfert contrôlé entre supports ou comptes ;
- expiration ou report du solde selon la politique ;
- rapprochement et export organisateur.

Chaque opération doit être idempotente, atomique et traçable dans le ledger.

## 4. Avec ou sans support

Le compte cashless doit fonctionner sans support physique :

- compte IziLife ;
- QR code dynamique ou sécurisé ;
- application/web mobile.

Un support facultatif peut ensuite pointer vers le même compte :

- bracelet NFC/RFID ;
- carte ;
- badge ;
- QR code imprimé.

Le support n'est jamais le portefeuille. Il est un identifiant révocable et remplaçable donnant accès au compte.

Un compte peut avoir plusieurs supports successifs, mais un support actif ne doit pointer que vers un seul compte cashless.

## 5. Crédit initial vendu avec un EAP

Exemple : « Entrée + 20 € cashless ».

Après validation de la Transaction :

1. création des Tickets d'accès ;
2. obtention/création du WalletAccount scopé ;
3. création d'une opération de recharge liée à la Transaction ;
4. crédit atomique du sous-solde cash ;
5. éventuelle affectation d'un support.

Le montant d'accès et le montant rechargé doivent rester distincts dans le panier, la comptabilité, les remboursements et les frais.

## 6. État actuel et manques

Déjà présent :

- EAP sur AnnualCelebration ;
- copie des EAP vers un Event ;
- Wallet et comptes ;
- soldes cash/izi ;
- opérations et ledger ;
- consommation atomique ;
- attribution de crédits izi.

À construire plus tard :

- recharge monétaire cash ;
- scope AC/édition formalisé ;
- politique de validité/report/remboursement ;
- supports physiques et révocation ;
- paiement marchand/terminal ;
- mode déconnecté et resynchronisation si nécessaire ;
- back-office organisateur et rapprochement financier ;
- sécurité anti-rejeu et plafonds réglementaires.

## 7. Position dans la feuille de route

Le cashless ne bloque pas :

1. la stabilisation EAP Event ;
2. les modèles EventSerie/AnnualCelebration ;
3. l'installation EAP sur XP et Sessions ;
4. le scope multi-catégorie ;
5. le catalogue Partner minimal.

Il doit toutefois être pris en compte maintenant dans les contrats de copie et de fulfillment afin de ne pas confondre plus tard Ticket, avantage, recharge et solde.

Le chantier cashless sera ouvert après stabilisation du catalogue EAP/ES et du Wallet dans PayHub.

## 8. À transférer dans la conversation espace Partner

- configuration cashless par AnnualCelebration ou Event ;
- choix du scope du solde ;
- création d'EAP avec crédit initial ;
- politique de recharge, remboursement, expiration et report ;
- gestion des supports ;
- suivi des recharges, consommations et soldes ;
- exports et rapprochement ;
- droits des employés et opérateurs de caisse ;
- configuration des marchands/objets autorisés à consommer le solde.
