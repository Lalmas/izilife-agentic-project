# TVA Partner — V1 France et évolution future

## Périmètre immédiat

La V1 couvre uniquement les achats Partner facturés par iziLife : abonnement Partner et Boost. Les prix `PlanPrice.amount` et les budgets de Boost sont considérés HT.

Un même `PartnerTaxQuoteService` est utilisé par les écrans et par le PayHub. L'écran affiche HT, TVA, TTC ou la mention d'exonération. Le PayHub recalcule le devis côté serveur, stocke son snapshot dans `Transaction.meta.fiscal_snapshot`, puis transmet au PSP le reste TTC réellement dû.

Une seule configuration métier subsiste : `IZILIFE_COMPANY_IS_MICRO_ENTERPRISE=1|0`.

Pour 2026, le code applique automatiquement les seuils officiels des prestations de services : dépassement de 37 500 € l'année précédente, ou dépassement de 41 250 € pendant l'année courante. Un partenaire hors France est bloqué avec un message clair dans cette V1.

## Audit de l'existant

- Abonnement : `PlanPrice` → `PayHub::startSubscription()` → `Transaction` → provider.
- Boost : budget HT → `PayHub::startBoost()` → `BoostRequest` + `Transaction` → provider.
- `Transaction.amount` reste le montant monétaire transmis au PSP ; le détail fiscal historique est dans `meta.fiscal_snapshot`.
- `PartnerTransactionFinancialSnapshot` décrit les commissions/frais/net dus au Partner et ne doit pas être détourné pour la TVA d'une vente iziLife.
- `FinancialDocument` et `FinancialDocumentLine` préparent déjà la future facturation et pourront consommer le snapshot fiscal sans recalculer l'historique.

## Projet fiscal ultérieur

Le futur moteur devra ajouter une configuration fiscale administrable et historisée en base, le suivi du CA iziLife (revenus plateforme et revenus externes déclarés), les règles B2B internationales, la facture électronique, les avoirs/remboursements et la migration contrôlée des snapshots JSON vers un référentiel fiscal dédié.

