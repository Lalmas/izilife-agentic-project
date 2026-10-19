# Points iziLife — inventaire et contrat d’intégration

Date de l’audit : 12 septembre 2026.

## Décision métier

Il existe un seul solde de points iziLife par utilisateur. Il regroupe :

- la fidélité d’usage : utilisation de l’application, visites qualifiées, réservations honorées, achats complétés et participations réelles ;
- la contribution : avis, notes, photos, vidéos, corrections, fiches, listes, publications et interactions utiles ;
- la progression : missions, niveaux et badges lisent ce même solde ;
- les paliers : certains seuils cumulés peuvent offrir des crédits iziLife une seule fois, sans débiter les points.

Un crédit iziLife est une valeur économique dépensable. Un point iziLife mesure d’abord l’usage et la contribution. Aucun code métier ne doit convertir lui-même une action en nombre de points.

Les points sont acquis à vie : ils ne diminuent ni après une récompense, ni après une période d’inactivité. Une maladie, un déplacement ou une contrainte personnelle ne doit jamais faire perdre un statut. L’activité récente est un indicateur séparé (`points_30d`, `points_90d`, `points_365d`, dernière activité qualifiée), utilisable pour les statistiques ou des messages adaptés, jamais pour retirer des droits.

## Porte d’entrée unique

Toute action qualifiée passe par :

```php
helper('izilife_participation');
izilife_participation_event([
    'user_id' => $userId,
    'action' => 'action-stable',
    'scope_level' => 'place',
    'scope_id' => $placeId,
    'object_type' => 'preuve_metier',
    'object_id' => $proofId,
]);
```

Contrat :

1. L’appelant donne l’action et la preuve métier, jamais un nombre de points.
2. `ParticipationRewardEngine` lit la valeur dans `IzilifeUserParticipationActionType`.
3. Il réserve une clé d’idempotence dans `IzilifeParticipationEventDedup`.
4. Il écrit l’historique dans `IzilifeUserParticipationPointHistory`.
5. Il met à jour `UserCurrentSocialThings.current_participation_point`.
6. Il avance les missions, la fidélité globale, les badges et les éventuelles récompenses.

Les recherches du 12 septembre 2026 ne trouvent aucune autre écriture applicative directe dans l’historique ou le solde. Les accès directs restants sont internes au moteur, ce qui est conforme.

`iz_apply_missions_and_loyalty()` est seulement un adaptateur de compatibilité vers cette porte d’entrée. Aucun nouveau code ne doit l’utiliser.

## Barème actuellement en base locale

| Action stable | Libellé | Points | Branchement constaté |
|---|---|---:|---|
| `commentaire` | Ancien commentaire / avis | 0 | conservé pour l’historique ; remplacé par `review-published` |
| `photo` | Ajout de photo | 3 | branché après ajout de médias à un avis |
| `video` | Ajout de vidéo | 5 | à brancher |
| `liste-publique` | Création de liste publique | 5 | à brancher dans `User_model` |
| `partage-liste` | Partage de liste | 2 | à brancher |
| `participation-event` | Participation à un événement | 5 | branché lors de la consommation effective d’une sélection |
| `event-hors-ville` | Participation hors ville | 7 | à brancher après présence prouvée |
| `correction-info` | Correction d’informations | 3 | à brancher après validation de la correction |
| `ajout-fiche` | Ajout d’un lieu ou d’une fiche | 10 | à brancher après publication/validation |
| `parrainage` | Parrainage utilisateur | 20 | à brancher après qualification du filleul |
| `notation-simple` | Note sans avis | 2 | à brancher après publication |
| `ajout-lieu-liste` | Ajout de lieu à une liste | 1 | à brancher |
| `media-event` | Ajout de média dans un événement | 3 | à brancher après validation/publication |
| `post-communaute` | Publication dans une communauté | 3 | à brancher après publication |
| `interaction` | Interaction sociale | 1 | aucune porte d’entrée active retrouvée ; les paiements et avantages en ont été retirés |
| `review-published` | Avis publié valide | 5 | préparé via preuve, mais aucun producteur actif retrouvé |
| `review-contextual` | Bonus d’avis contextuel | 3 | préparé via preuve, mais aucun producteur actif retrouvé |
| `review-useful` | Avis jugé utile | 2 | à brancher sur une qualification anti-abus |
| `visit-place` | Visite qualifiée d’un lieu | 2 | à brancher avec preuve et fenêtre anti-répétition |
| `visit-shop` | Visite qualifiée d’un commerce | 2 | à brancher, exclusivement de `visit-place` pour une même visite |
| `app-daily-use` | Utilisation quotidienne qualifiée | 1 | à brancher une fois par utilisateur et par jour |
| `booking-completed` | Réservation honorée/terminée | 5 | à brancher au changement d’état final, jamais à la création |
| `purchase-completed` | Achat complété | 5 | branché sur achats de sélection, billetterie Event et abonnement |
| `benefit-redeemed` | Avantage iziLife réellement utilisé | 3 | branché sur les deux parcours de consommation d’avantage |
| `izilife-campaign-visit` | Visite apportée par une campagne iziLife | 3 | bonus uniquement avec attribution campagne prouvée ; jamais pour une opération propre au lieu |
| `experience-completed` | Expérience terminée | 5 | à brancher sur preuve d’exécution |
| `meetz-completed` | Participation MeetZ terminée | 10 | à brancher sur présence prouvée |

Le BO « Économie & fidélité iziLife » est la source unique pour modifier ces valeurs. Le barème SQL installe les valeurs de lancement sans saisie manuelle ; les modifications ultérieures ne changent jamais l’historique déjà acquis.

## Branchements actuels vérifiés

- `Review_model::attachReviewMedia` : `photo`, preuve = avis et médias créés.
- `User` (consommation de sélection) : `participation-event`, preuve = participation consommée.
- `SelectionPurchaseHandler` : `purchase-completed`, preuve = achat créé après paiement.
- `EventBookingHandler` : `purchase-completed`, preuve = transaction de billetterie finalisée.
- `PlanSubscriptionHandler` : `purchase-completed`, preuve = souscription créée après paiement.
- `IzilifePlan` (deux parcours) : `benefit-redeemed`, preuve = règle ou attribution consommée.
- `review_evidence_helper` : producteur générique idempotent prêt, mais sans appelant actif lors de cet audit.
- `RewardGame` appelle directement les méthodes de jeu du même moteur ; ce n’est pas une seconde mécanique de points.

## Endroits prioritaires à brancher ensuite

1. Visites `Place` et `Shop` : ne récompenser qu’une visite qualifiée, avec fenêtre anti-répétition ; une simple impression ou un survol ne compte pas.
2. Réservations : déclencher `booking-completed` lors de l’état honoré/terminé, pas lors de la demande ni de la confirmation.
3. Achat d’Offer : `OfferPurchaseHandler` finalise des achats mais n’émet pas encore `purchase-completed`.
4. Avis et notes : choisir une seule action de base (`review-published` ou `notation-simple`) puis ajouter les bonus contextuel/utile sans doubler l’avis de base.
5. Listes : création publique, partage et ajout de lieu sont présents dans les modèles mais pas reliés au moteur.
6. Contributions éditoriales : correction, ajout de fiche, médias Event et posts doivent attendre validation/publication.
7. Usage quotidien : une preuve journalière déterministe est nécessaire pour empêcher le rechargement de page de multiplier les gains.
8. Parrainage : récompenser sur événement qualifiant décidé (compte vérifié ou première action/premier paiement), jamais sur simple saisie d’un code.

## Garde-fous avant activation des valeurs

- Toute action doit fournir un `object_type` et un `object_id` stables pour l’idempotence.
- Les visites et usages récurrents nécessitent une clé par période, pas l’identifiant aléatoire d’un événement analytics.
- Une action annulée ou remboursée devra produire une écriture compensatoire ; ne jamais effacer l’historique.
- Les changements de barème ne sont pas rétroactifs : l’historique conserve le nombre attribué à la date de l’action.
- L’inactivité ne déclenche aucune expiration de points, baisse de niveau ou reprise de récompense.
- Les points ne doivent être accordés qu’après la transaction métier réussie et validée.
- Aucun contrôleur, modèle ou handler ne doit écrire directement dans les tables de points.
- Un contenu utilisateur ne rapporte rien tant que sa modération n’est pas `APPROVED` et `is_active=1`. Un rejet, une suspension, une injure, du spam ou un média pornographique ne rapporte aucun point et peut déclencher la sanction du compte.
- Une utilisation de promotion validée compte comme visite qualifiée. Le bonus `izilife-campaign-visit` exige en plus une campagne iziLife attribuable ; impression, survol, clic et campagne propre au commerçant ne suffisent pas.

## Matrice de validation décidée

| Famille | Preuve qui déclenche | Ce qui ne rapporte jamais |
|---|---|---|
| Avis | `moderation_status=APPROVED` et `is_active=1` | brouillon, pending, suspendu, rejeté, supprimé, injurieux, spam ou pornographique |
| Photo/vidéo | média publié et modéré, rattaché à un objet actif | upload seul, doublon, contenu refusé |
| Correction/fiche | validation BO puis publication effective | proposition, auto-enregistrement ou refus |
| Visite | preuve forte : avantage validé, billet scanné, réservation honorée ou signal de présence qualifié | impression, survol, ouverture de page, géolocalisation passive seule |
| Promo du lieu | utilisation validée : visite + `benefit-redeemed` | affichage ou clic |
| Campagne iziLife | visite validée + attribution de campagne : ajoute `izilife-campaign-visit` | opération propre au lieu sans campagne iziLife |
| Réservation | statut final honoré/terminé | création, confirmation, annulation, refus, no-show |
| Achat | paiement complété puis délai d’annulation métier atteint, ou compensation si remboursement ultérieur | tentative, pending, échec, fraude, remboursement total |
| Event/XP/MeetZ | billet/présence consommée ou exécution terminée | intéressé, « j’y vais », simple inscription ou no-show |
| Usage quotidien | première action authentifiée et qualifiée du jour | rafraîchissement de page, tâche automatique, trafic anonyme |
| Parrainage | filleul qualifié selon la règle active, une seule fois | code saisi, compte non vérifié ou auto-parrainage |

## Paliers de lancement

Les seuils sont absolus et chaque attribution porte la clé idempotente `izi-point-milestone:{user}:{seuil}`. Les gains successifs sont : 50→5, 100→5, 250→15, 500→25, 1 000→50, 2 500→150, 5 000→250 et 10 000→500 crédits. Atteindre 10 000 points donne donc 1 000 crédits cumulés sans retirer aucun point.

## Dette de nommage connue

Les tables historiques conservent les noms `ParticipationPoint` et le champ `current_participation_point`. Ils représentent désormais le solde unique de points iziLife. Les renommer en base n’est pas nécessaire au lancement et créerait un risque de migration sans bénéfice métier.
