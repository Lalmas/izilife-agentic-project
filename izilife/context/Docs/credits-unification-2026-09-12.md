# Unification des unités iziLife — décision de lancement

## Convention

- La monnaie réelle (`EUR`, puis autres devises) reste portée par `Currency`, `Transaction` et les sous-soldes cash du Wallet.
- Les points iziLife sont gagnés par la participation et la fidélité globale. Ils servent également aux niveaux et badges.
- Les points sont cumulatifs à vie et ne sont pas dépensés. Des paliers peuvent offrir des crédits une seule fois lorsqu’ils sont franchis.
- Le crédit iziLife est l’unité marketing dépensable. Toute attribution, consommation, expiration ou annulation passe par `IziCreditAccount`, `IziCreditOperation`, `IziCreditLedgerEntry` et `IziCreditBucket`.
- Le taux de référence de lancement est de **10 crédits pour 1 EUR**. Il est versionné dans `IziCreditExchangeRate`.
- Un prix métier en crédits est toujours versionné dans `IziCreditPriceRule`. Le taux de référence n’est qu’un calcul par défaut.
- Il n’existe pas de score de contribution séparé : les points de participation alimentent les points de fidélité iziLife.
- Les points ne sont jamais convertibles directement en argent et ne sont pas transférables entre utilisateurs.
- L’inactivité ne retire aucun point, niveau, badge ou palier. L’activité récente sur 30/90/365 jours est un indicateur séparé sans effet punitif.
- La fidélité propre à un Partner est un futur système séparé et n’est pas configurée dans le cockpit économique iziLife.

## Legacy à ne plus alimenter

- `WalletAccount.balance_izi` (ancien pseudo-solde crédit exprimé en argent)
- `WalletLedgerEntry.sub_balance='izi'`
- `IziCreditLot` de l’ancien Wallet
- `MeetzUserCredit`, sauf lecture durant sa migration vers `IziCreditBucket`

## Vocabulaire UI

- `€` / devise : paiement réel.
- `iziCash` : argent réel rechargé et conservé chez le PSP, reflété dans le sous-solde cash.
- `crédits iziLife` : avantage interne séparé, offert selon une origine tracée. L’achat direct et l’acceptation par les commerçants sont futurs et désactivés.
- `points iziLife` : fidélité, participation et progression ; permanents, non dépensés, susceptibles de déclencher des crédits aux paliers.
- Ne jamais employer « points » et « crédits » comme synonymes.

## Valeurs au moment de la décision

- L’ancien fallback Partner était de 200 crédits/EUR, d’où 19 800 crédits pour 99 EUR.
- Aucun taux, prix ou barème de récompense iziCredit n’était actif dans la BDD locale.
- La BDD locale contenait 30 anciens points de participation, aucun solde `balance_izi` et aucun solde `IziCreditAccount`.

## Parcours de paiement cible

1. Afficher ensemble, mais sans les fusionner, le solde de crédits iziLife et le solde iziCash.
2. Si l’utilisateur l’autorise, appliquer les crédits disponibles et compatibles avec le contexte.
3. Compléter avec iziCash disponible dans la même devise.
4. Envoyer uniquement le reliquat au PSP/moyen de paiement principal.
5. Réserver chaque source avant le paiement, puis tout confirmer ou tout libérer de façon idempotente.

Le socle contient `TransactionFundingAllocation` pour tracer `IZI_CREDIT`, `CASH_WALLET` et `PSP`, mais ce parcours unifié n’est pas encore activé. `PayHub::applyWalletFunding()` est commenté et son ancien calcul privilégie le cash puis `WalletAccount.balance_izi`. Il ne doit pas être réactivé sans remplacement par `IziCreditAccount`/`IziCreditBucket` et sans ordre crédits → iziCash → PSP.

Les crédits offerts peuvent expirer au niveau du lot `IziCreditBucket.expires_at`. Le cash n’est jamais représenté par un crédit et reste sous garde du PSP.

## Usages commerciaux confirmés

- offrir des crédits aux influenceurs, ambassadeurs, bénévoles, photographes, power users, salariés, amis et famille, avec une origine et d’éventuelles restrictions traçables ;
- payer un abonnement User ou Partner sans paiement monétaire ;
- payer une participation à un MeetZ ou à un Event iziLife ;
- réduire ponctuellement une facture, avec une remise plafonnée à la commission iziLife lorsque la politique du contexte l’autorise.

Règle de couverture :

- MeetZ et réservation MeetZ : jusqu’à 100 % du prix, car ce sont des produits exclusifs iziLife ;
- Event ou XP sans bénéficiaire externe : jusqu’à 100 %, même payant, car la recette revient entièrement à iziLife ;
- Event, XP ou autre vente avec Partner/tiers rémunéré : couverture plafonnée à la commission iziLife ; la part du tiers reste payable en argent, sauf campagne explicitement financée par iziLife.

Une attribution offerte est un lot distinct. Elle peut donc être limitée à un abonnement, un Event/MeetZ, une campagne, un pays ou une période. Le plafond « commission iziLife » est une préparation future : aucun commerçant n’accepte actuellement les crédits.

## Configuration centrale

- `IzilifeUserParticipationActionType` : valeur en points de chaque action qualifiée ;
- `IziCreditExchangeRate` : valeur de référence crédit/devise ;
- `IziCreditPriceRule` : prix en crédits des abonnements et usages ; une règle ciblée surcharge une règle globale ;
- futur barème de paliers : seuil cumulé de points → attribution unique de crédits, sans conversion ni diminution des points.

Les abonnements payants actifs sont synchronisés automatiquement depuis `PlanPrice` et le taux actif. Les montants MeetZ, Event, XP, produit, service et Boost ne doivent pas être inventés : ils deviennent payables en crédits lorsqu’un prix global ou ciblé est activé.

## Garde-fou de lancement

La vente directe de crédits est désactivée par défaut avec la feature `IZI_CREDIT_PURCHASE`. Le premier lancement porte uniquement sur des crédits offerts, notamment en bonus d’une recharge iziCash, par palier de points ou par campagne. Ils sont non remboursables en argent, non transférables par défaut et limités par leurs lots/campagnes. L’acceptation par un Partner est elle aussi hors lancement.

Avant d’ouvrir l’achat, il faut valider avec le PSP et le conseil juridique : qualification de réseau limité, plafond de chargement, obligations de remboursement, cantonnement/protection des fonds, KYC/LCB-FT, traitement TVA/comptable, CGV et gestion des fonds non consommés. Si des Partners tiers acceptent une valeur achetée contre de l’argent, le simple fait de l’appeler « crédit » ne suffit pas à écarter le régime de la monnaie électronique.
