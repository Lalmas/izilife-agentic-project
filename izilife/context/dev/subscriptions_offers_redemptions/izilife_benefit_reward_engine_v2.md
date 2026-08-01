# Izilife - Benefit & Reward Engine V2

## Vision

Ce document décrit le moteur unique de gestion des droits, récompenses et avantages d'Izilife.

Objectifs :

- Unifier les abonnements, Grants, Rewards, Discovery, jeux, missions, loyalty...
- Réutiliser un seul moteur de consommation.
- Ne jamais dupliquer la logique métier.
- Préparer les futures évolutions sans casser l'existant.

---

# Architecture

```
Action utilisateur
        │
        ▼
ParticipationRewardEngine
        │
        ├── Participation Points
        ├── Badges
        ├── RewardGame
        ├── BenefitGrant
        └── Notifications (plus tard)
                    │
                    ▼
BenefitPolicyRule
        │
        ▼
BenefitEngine
        │
        ▼
BenefitLedger
        │
        ▼
Redemption
```

---

# Les moteurs

## ParticipationRewardEngine

Point d'entrée UNIQUE.

Le code métier n'ajoute jamais directement des points, grants ou récompenses.

Exemple :

```php
ParticipationRewardEngine::dispatch([
    'user_id'=>$userId,
    'action'=>'review_validated',
    'scope_level'=>'place',
    'scope_id'=>$placeId,
    'object_type'=>'review',
    'object_id'=>$reviewId,
    'meta'=>[]
]);
```

Le moteur :

- ajoute les points
- met à jour les badges
- vérifie un RewardGame actif
- crée un BenefitGrant si nécessaire
- retourne les actions UX

Retour :

```php
[
    "points"=>10,
    "badge"=>null,
    "reward"=>[
        "type"=>"wheel",
        "url"=>"..."
    ]
]
```

Le moteur ne fait jamais de redirection.

---

# Participation

Actions :

- avis validé
- photo validée
- vidéo
- check-in
- réservation
- commande
- événement
- ajout lieu
- partage
- etc.

Chaque action peut :

- donner des points
- déclencher un jeu
- créer un Grant
- débloquer un badge

---

# Points

Tables existantes :

- IzilifeUserParticipationActionType
- IzilifeUserParticipationPointHistory

Conserver.

Le ledger des points est indépendant du BenefitLedger.

---

# Badges

Conserver :

- UserBadge
- UserBadgeUnlock
- UserCurrentSocialThings

Le moteur décide des déblocages.

---

# RewardGame

Nouvelles tables.

RewardGame

- scope_level
- scope_id
- trigger_action_type_id
- game_type
- config_json
- is_active

RewardGamePrize

- reward_game_id
- benefit_rule_id
- probability_weight
- stock_limit
- is_active

Exemple :

Avis validé

↓

Roue

↓

BenefitGrant

↓

BenefitPolicyRule

↓

BenefitLedger

---

# BenefitGrant

Le Grant représente un droit gagné.

Origines possibles :

- jeu
- mission
- loyalty
- affiliation
- recommandation
- achat futur
- Discovery futur

Le Plan classique ne passe PAS par Grant.

Exception :

si Prime possède X cadeaux utilisables.

---

# BenefitPolicyRule

Le BPR décrit :

- ce que possède le user
- les produits
- catégories
- équipements
- services
- conditions
- résumé

Ajouter :

delivery_mode

Valeurs :

- onsite_redemption
- online_order
- promo_code
- external_booking
- display_only

Ajouter :

usage_constraints_json

Exemple :

{
    "opening_hours_required": true,
    "usable_days":[1,2,3,4,5,6,7],
    "time_windows":[
        {
            "start":"12:00",
            "end":"14:00"
        }
    ],
    "blackout_windows":[
        {
            "start":"01:00",
            "end":"02:00"
        }
    ],
    "last_use_time":"23:00",
    "allow_if_opening_hours_unknown":true
}

---

# BenefitEngine

Point d'entrée unique.

Fonctions :

- canUse()
- consume()
- history()

Toutes les consommations passent ici.

---

# BenefitLedger

Le Ledger est la vérité métier.

Il gère :

- quotas
- consommation
- refus
- historique
- bucket
- Grant
- Plan

Toutes les consommations sont transactionnelles.

Aucun double clic possible.

---

# InternalOffer

Nouveau helper.

Responsable de :

- première année offerte
- opérations internes
- réductions internes

Ne crée jamais d'Offer.

Il modifie uniquement :

- original_amount
- final_amount
- metadata

Le pipeline PayHub reste inchangé.

---

# Redemption Plan

Flow :

Objet

↓

BPR Plan

↓

BenefitEngine::canUse()

↓

Modal

↓

BenefitEngine::consume()

↓

BenefitLedger

↓

Preuve

↓

Historique

---

# Delivery Mode

Le bouton dépend du BPR.

onsite_redemption

↓

Utiliser

online_order

↓

Commander

promo_code

↓

Copier le code

external_booking

↓

Réserver

display_only

↓

Voir

---

# Discovery

Discovery reste un produit à 5€.

Le contenu est configuré via une BPR type discovery.

Le commerçant choisit :

- produits
- catégories

Le choix utilisateur :

DiscoveryChoice

↓

BenefitPolicyRule

↓

BenefitLedger

Plus tard :

- roue
- surprise
- activités
- spa
- etc.

---

# Commande en ligne

Si :

- commande Izilife active
- BPR possède des targets

↓

Commander

La remise sera appliquée dans le pipe de commande.

---

# Historique utilisateur

Afficher :

- date
- heure
- lieu
- offre
- plan
- Grant
- statut

---

# QR

QR public

↓

plan/use/{string_id}

QR sécurisé

↓

plus tard

Scanner universel Izilife.

---

# Roadmap V3

Participation

- Missions
- Loyalty
- Affiliation
- Parrainage

Reward

- Calendrier de l'avent
- Roue
- Coffrets

Discovery

- Food
- Activité
- Bien-être

Commande

- Application automatique

Scanner

- Universel

Analytics

- Utilisation
- Conversion
- Performance

---

# Plan de développement

## Phase 0

- delivery_mode
- usage_constraints_json
- DiscoveryChoice
- InternalOfferHelper

---

## Phase 1

InternalOffer

PayHub

Abonnement gratuit

---

## Phase 2

BenefitEngine

BenefitLedger

Redemption

Historique

---

## Phase 3

Live Resume

UI

Modal

QR

---

## Phase 4

Discovery

RewardGame

Grant

---

## Phase 5

ParticipationRewardEngine

Points

Badges

Jeux

---

## Phase 6

Commande

Promo Code

External Booking

---

## Règles

- Une offre permanente active par lieu.
- Les Plans utilisent directement les BPR.
- Les jeux créent des Grants.
- Les Grants consomment des BPR.
- Toutes les consommations passent par BenefitLedger.
- Toute action métier passe par ParticipationRewardEngine.
- Aucune logique métier dans les contrôleurs.
- Réutiliser les helpers et composants existants.
- Ne jamais casser le fonctionnement actuel.