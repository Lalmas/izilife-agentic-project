# Chantier futur — paiements, fulfillment et nettoyage Stripe historique

## Statut du document

- Document de cadrage pour un chantier **postérieur à la mise en production**.
- Il ne demande aucune refonte immédiate des paiements.
- Priorité actuelle : tester les comportements existants dans les trois applications et ne corriger que les défauts reproductibles.

## Applications concernées aujourd'hui

Le monde iziLife repose actuellement sur trois applications autonomes qui partagent la même base de données :

- `izilife` : Front Office (FO) ;
- `izilife-admin` : Back Office (BO) ;
- `izilife-partner-admin` : Partner Space (PS).

Il ne faut pas créer maintenant de quatrième composant partagé ni déplacer du code entre ces dépôts. Une future bibliothèque `izilife-libs` pourra réunir les briques réellement communes, après stabilisation et mise en production.

## Modèle métier à préserver

### Abonnement utilisateur actuel

Le parcours de référence est :

`IzilifePlan → Plan → PlanPrice → PayHub → Subscription iziLife`

La gestion du plan actif se fait depuis `user/plan`. Les abonnements iziLife sont des objets métier internes. Ils ne reposent pas sur Stripe Billing Subscription.

### Abonnement Partner actuel

Le renouvellement Partner utilise des paiements ponctuels, notamment des `PaymentIntent` confirmés en `off_session`, puis prolonge la ligne `Subscription` iziLife. Il faut conserver :

- les périodes internes ;
- le renouvellement automatique interne ;
- la période de grâce ;
- la consommation ou la libération des crédits ;
- les moyens de paiement enregistrés ;
- les événements métier internes.

À terme, le modèle `Subscription` pourra également porter des Memberships ou de nouveaux abonnements. Son nom et son existence ne constituent donc pas du legacy.

## Idempotence et fulfillment existants

L'idempotence existe déjà. Le chantier futur ne doit pas repartir de zéro ni ajouter un registre global sans anomalie démontrée.

### FO

Le FO dispose d'un `Transaction_model::claimFulfillment()` atomique. Il réclame une transaction payée dont `fulfilled_at` est encore nul. Les handlers métier utilisent ensuite cette réclamation pour empêcher un double effet.

### PS

Le PS verrouille actuellement la transaction avec `SELECT ... FOR UPDATE`, réalise le traitement métier dans la même transaction SQL, puis renseigne `fulfilled_at` et le statut final. Un rollback annule l'ensemble si le traitement échoue.

Cette mécanique ne doit pas être remplacée par celle du FO. Une future uniformisation peut seulement extraire cette mécanique dans une méthode nommée `claimFulfillment()` au niveau du modèle PS, tout en conservant :

- le `FOR UPDATE` ;
- la transaction SQL englobante ;
- les validations métier avant écriture ;
- le rollback intégral ;
- l'écriture finale de `fulfilled_at`.

L'objectif serait une convention de nom commune, pas une implémentation identique.

### BO

Le BO journalise notamment les événements PSP par `provider_event_id`. Il ne doit pas exécuter un fulfillment métier appartenant au FO ou au PS. Cette séparation doit être vérifiée par les tests avant toute modification.

## Stratégie de tests préalable

Pour chaque contexte de paiement réel — billetterie, expérience, Offer/opération, Selection, abonnement User, abonnement Partner, renouvellement, Boost et commande Hub — exécuter :

1. succès du paiement ;
2. webhook reçu avant le retour navigateur ;
3. retour navigateur reçu avant le webhook ;
4. rejeu deux ou trois fois du même événement PSP ;
5. montant, devise, propriétaire ou contexte falsifié ;
6. paiement échoué ;
7. paiement annulé ;
8. remboursement ;
9. panne simulée au milieu du fulfillment ;
10. rejeu après correction de la panne.

Après chaque cas, vérifier en base qu'il n'existe qu'un seul effet métier attendu : transaction finalisée, commande, billet, accès, abonnement, allocation de crédits ou Boost.

Si ces tests passent, ne pas modifier le mécanisme avant la mise en production.

## Nettoyage de l'ancien Stripe Billing

Le nettoyage vise uniquement les anciens parcours Stripe Billing (`invoice.*`, `customer.subscription.*`, objets Stripe Subscription), jamais le système `Subscription` métier iziLife.

### Éléments actuels à conserver

- `IzilifePlan`, `Plan`, `PlanPrice` et PayHub ;
- `checkoutCompleted()` ;
- `paymentIntentSucceeded()` ;
- `paymentIntentFailed()` ;
- les renouvellements ponctuels `off_session` ;
- les colonnes et objets métier encore utiles aux futurs Memberships/Subscriptions ;
- toute méthode BO/PS appelée `createSubscription()` qui crée ou configure en réalité un compte PSP/Stripe Connect.

### Éléments candidats legacy à confirmer

- ancien contrôleur FO `Subscription` ;
- anciennes vues `Views/subscription/*` ;
- ancienne branche User affichant `users/user_subscription` ;
- anciens liens `subscription/choose_option` ;
- handlers `invoicePaid()` et `invoiceFailed()` ;
- handler `subscriptionChanged()` basé sur une Stripe Subscription ;
- recherche d'une souscription par `provider_subscription_id` lorsqu'elle ne sert qu'à Stripe Billing ;
- anciens événements `invoice.*` et `customer.subscription.*` dans le webhook BO.

### Méthode de neutralisation

Ne rien supprimer à l'aveugle.

1. Rechercher toutes les références statiques et dynamiques.
2. Vérifier les routes explicites et l'éventuel auto-routing.
3. Tester que les parcours actuels n'utilisent pas le code candidat.
4. Ajouter temporairement un commentaire clair aux méthodes ambiguës : rôle réel, parcours appelant et statut legacy éventuel.
5. Si nécessaire, journaliser leur invocation pendant une période d'observation.
6. Neutraliser uniquement les entrées confirmées inutilisées.
7. Rejouer toute la campagne de paiements.
8. Supprimer définitivement lors d'un chantier ultérieur, avec migration de colonnes séparée si elle est réellement nécessaire.

Un commentaire est préférable à une suppression lorsque le rôle n'est pas démontré. Une méthode `createSubscription()` liée à l'onboarding PSP ne doit pas être renommée ou supprimée dans ce chantier.

## Future bibliothèque `izilife-libs`

Après stabilisation, `izilife-libs` pourra accueillir les contrats véritablement communs :

- conventions de statuts de transaction ;
- interfaces de fulfillment ;
- validation commune des événements PSP ;
- objets de valeur paiement, montant et devise ;
- outils de tests de rejeu et d'idempotence ;
- journalisation et corrélation techniques.

Elle ne devra pas absorber les règles métier propres au FO, au BO ou au PS. Chaque application conservera ses handlers et ses responsabilités.

## Critères d'ouverture du chantier

Le chantier ne commence qu'après :

- livraison et stabilisation de la version actuelle ;
- campagne de tests Stripe complète sur staging ;
- inventaire confirmé des routes et appels legacy ;
- sauvegarde et plan de retour arrière ;
- séparation claire entre nettoyage Stripe Billing, uniformisation du fulfillment et création de `izilife-libs`.

## Règle de décision

Si le comportement actuel est correct et résiste aux rejeux, à la concurrence et aux pannes simulées, il reste inchangé avant la mise en production. Toute évolution doit répondre à un défaut reproduit ou à un chantier post-production explicitement planifié.
