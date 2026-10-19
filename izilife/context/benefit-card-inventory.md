# Inventaire des cartes d'offres et avantages

## Objet

Ce document décrit le classement Front, l'identité visuelle et le comportement des cartes affichées dans le live resume, l'onglet **Bons plans**, les mini-cartes et les pages Offer.

Le porteur technique d'une règle (`plan` ou `offer`) ne suffit pas à choisir la rubrique. L'éligibilité publique de l'Offer est déterminante.

## Règle de classement

| Source | Contexte / éligibilité | Rubrique Front | Variante |
|---|---|---|---|
| BPR `owner_type=plan` | `application_context=special_brunch` | Avantages iziLife | Avantage Brunch, agrégé par plan |
| Offer + BPR | `application_context=special_brunch`, cible `all` | Offres du lieu | Offre Brunch publique |
| Offer + BPR | `application_context=special_brunch`, cible `izilife-subscribers` | Avantages iziLife | Avantage Brunch réservé aux abonnés |
| BPR `owner_type=plan` | autre temporalité Plan | Avantages iziLife | Carte de la temporalité correspondante |
| Offer classique publique | cible `all` | Offres du lieu | Carte Offer du lieu |
| Offer `OPERATION` | selon son type d'opération | Opérations | Carte opération |

Une Offer Brunch réservée aux abonnés reste techniquement une Offer du lieu, mais elle est volontairement présentée dans **Avantages iziLife**.

## Identité Brunch commune

Toutes les cartes Brunch utilisent la même identité :

| Usage | Fond | Bordure / badge | Texte d'accent | Icône |
|---|---|---|---|---|
| Mini-carte | `#FFF4E8` | `#F5B46B` | `#E67700` | 🥞 |
| Grande carte | `#E67700` | badge `#FFF4E8` | badge `#9A4B00` | 🥞 |

Les libellés distinguent le métier :

- BPR Plan Brunch : **Avantage Brunch** / **Avec votre abonnement iziLife**.
- Offer Brunch publique : **Offre Brunch** / **Proposée par le lieu**.
- Offer Brunch abonnés : **Avantage Brunch** / **Réservé aux abonnés iziLife**.

## Temporalités BPR Plan

| Clé | Libellé | Mini-carte (fond / bordure / accent) | Grande carte (fond / badge) | Icône | Particularité |
|---|---|---|---|---|---|
| `offre-permanente` | Offre permanente | `#F7EEE9` / `#E8B59F` / `#DE6A43` | `#F7EEE9` / `#F2D5C7` | ∞ | Variante permanente dédiée |
| `special-brunch` | Avantage Brunch | `#FFF4E8` / `#F5B46B` / `#E67700` | `#E67700` / `#FFF4E8` | 🥞 | Contexte autonome, jamais fusionné avec la temporalité Plan sous-jacente |
| `offre-cadeaux-ponctuels` | Offre cadeau | `#FDE9DE` / `#F29A73` / `#E85D35` | `#F29A73` / `#F8B79A` | 🎁 | Cadeau ponctuel |
| `anniversaire` | Offre anniversaire | `#EEE8FF` / `#9B84FF` / `#7A5AF8` | `#7A5AF8` / `#9B84FF` | 🎂 | Temporalité anniversaire adulte |
| `anniversaire-enfant-famille` | Anniversaire enfant | `#FFF3F8` / `#F7A8C8` / `#D63384` | `#D63384` / `#FFF3F8` | 👨‍👩‍👧 | Avantage famille |

`surprise` et `offre-decouverte` sont actuellement exclus du rendu principal par le builder. Leurs anciennes palettes restent visibles dans certains composants historiques mais ne doivent pas servir de fallback à une temporalité active.

## Offers du lieu et promos

| Clé | Fond grande carte | Badge | Icône | Usage |
|---|---|---|---|---|
| `brunch` | `#E67700` | `#FFF4E8`, texte `#9A4B00` | 🥞 | Offer Brunch publique |
| `happy-hour` | `#16A66A` | `#B8F1D5`, texte `#075C3A` | 🍹 | Happy Hour |
| `operation` | `#E58A16` | `#FFF3DF`, texte `#8A4B00` | ⚡ | Opération commerciale |
| `promo-etudiante` | `#2563EB` | `#93C5FD` | 🎓 | Promo étudiante |
| `promo-senior` | `#7C3AED` | `#C4B5FD` | 👵 | Promo senior |
| `promo-enfant` | `#059669` | `#A7F3D0`, texte `#065F46` | 🧒 | Promo enfant |
| `promo-lyceens` | `#0F766E` | `#CCFBF1`, texte `#115E59` | 🎒 | Promo lycéens |
| `place-offers` / `offer-classic` | `#2E8B57` | `#7EC8A0` | 🏷️ | Offre classique du lieu |

Mini-cartes correspondantes :

| Type | Fond | Bordure | Accent |
|---|---|---|---|
| Brunch | `#FFF4E8` | `#F5B46B` | `#E67700` |
| Offre classique du lieu | `#ECFDF3` | `#8DD5AC` | `#2E8B57` |
| Étudiante | `#EAF7FF` | `#A6E1FF` | `#12A6D9` |
| Senior | `#F5F3FF` | `#C4B5FD` | `#7C3AED` |
| Enfant | `#ECFDF5` | `#A7F3D0` | `#059669` |
| Lycéens | `#F0FDFA` | `#5EEAD4` | `#0F766E` |

## Autres familles de cartes

| Type | Fond | Bordure / badge | Accent | Icône |
|---|---|---|---|---|
| Politique d'accès iziLife | `#EEF4FF` | `#BFD4FF` | `#3D73DD` | ⚡ |
| Offre classique du lieu | `#2E8B57` | `#7EC8A0` | blanc | 🏷️ |

Les missions, programmes de fidélité, campagnes et concours sont produits par des builders distincts et ne partagent pas la carte BPR Plan.

## CTA et navigation

- Une carte BPR/Offer disposant d'un détail ouvre le modal d'action via `js-offer-card` / `js-offer-action`.
- Une Offer du lieu utilise **Voir l'offre** ; elle ne présente pas l'action **Utiliser**.
- Une carte ciblant des produits peut proposer le lien produits correspondant.
- Le contexte Brunch n'autorise pas la carte avantage à devenir la page Brunch : la page Brunch et son `ElementMenu` restent la source du menu et des produits.
- Sur une page Brunch, les cartes associées apparaissent sous **Offres valables sur ce brunch**.

## Fichiers de référence

- Construction et classement : `app/Helpers/live_resume_helper.php`
- Chargement des Offers et de leur cible : `app/Models/CampainsAndOffers/Offer_model.php`
- Grande carte BPR Plan : `app/Views/common_components/advantages/_advantage_card_plan_based.php`
- Grande carte Offer : `app/Views/common_components/advantages/_advantage_card_offer_list.php`
- Carte simple : `app/Views/common_components/advantages/_advantage_card_simple.php`
- Mini-cartes : `app/Views/common_components/advantages/show_search_advantage_swiper.php`
- Composition de l'onglet Bons plans : `app/Views/benefits/deals_page.php`

## Invariants de non-régression

1. `special_brunch` est un contexte d'application, pas une campagne Anniversaire ni une Special Offer générique.
2. L'icône Brunch est toujours 🥞.
3. Une Offer Brunch `all` reste dans **Offres du lieu**.
4. Une Offer Brunch `izilife-subscribers` est déplacée dans **Avantages iziLife**.
5. Une BPR Plan Brunch reste dans **Avantages iziLife** et conserve ses lignes par abonnement.
6. Une temporalité connue doit avoir un thème explicite ; elle ne doit jamais tomber silencieusement sur le fallback cadeau.
