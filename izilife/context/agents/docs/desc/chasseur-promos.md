# Agent — Chasseur de promos & deals

> Charger aussi : izilife-global.md, dev/agents-socle.md, dev/architecture.md

## Rôle
Trouver et ingérer 3 types de contenus deals/promos distincts.
Comprendre la différence entre eux est critique — ils ne vont pas dans les mêmes tables.

---

## Les 3 types à gérer

### 1. Offers d'un lieu (happy hours, promos étudiantes, deals maison)
**Qui :** un lieu (place/shop) ou un partner
**Table :** `Offer` avec `scope_level` + `scope_id`
**Avec `special_campain_id` :**
- `happy-hour` → section Happy Hour (avec `OfferTime` pour les créneaux)
- `promo-etudiante` → section Étudiants
- `avantage-izilife` → deal négocié izilife sur la fiche du lieu
**Sans `special_campain_id`** → promo libre du lieu

**Sources :** sites des lieux, réseaux sociaux, scraping, partenaires
**Pipeline :** → `postIngestJson(type=offer)` → validation → Offer table

### 2. BenefitPolicyRule — plans izilife négociés
**Qui :** izilife directement, lié à un plan d'abonnement
**Pas un Offer.** N'appartient à aucun lieu spécifique.
**Gestion :** BoBenefits controller, `BenefitPolicyRule_model`
**Pipeline :** saisie via interface dédiée ou `postIngestJson(type=benefit_rule)`
**Ne pas confondre avec les Offers**

### 3. ExternalPromotion — codes promos influenceurs / sites externes
**Qui :** une Page izilife (influenceur, blog, site) via `page_id`
**Pas un Offer.** Code promo externe, pas lié à un lieu directement.
**Pipeline :** → `postIngestJson(type=external_promo)`

---

## Déclenchement
- Mardi et vendredi (cron OVH pour sites statiques)
- Ponctuel pour négociations et influenceurs
- WhatsApp partenaires → webhook → injection directe

## Outils
- PHP scraping (sites statiques) — 0 token
- CIC (sites dynamiques) — **désactivé jusqu'à Max 200€**
- Claude API : extraction structurée depuis texte brut

---

## JSON de sortie — Offer HH

```json
{
  "type": "offer",
  "source": "chasseur-promos",
  "special_campain": "happy-hour",
  "scope_level": "place",
  "scope_id": 42,
  "fields": {
    "title": "Happy Hour",
    "deal": "Cocktails à 5€",
    "is_active": 1,
    "times": [
      {"day_of_week": 1, "start_time": "17:00", "end_time": "20:00"},
      {"day_of_week": 2, "start_time": "17:00", "end_time": "20:00"}
    ]
  }
}
```

## JSON de sortie — External Promo (influenceur)

```json
{
  "type": "external_promo",
  "source": "chasseur-promos",
  "page_id": 123,
  "fields": {
    "code": "INFLUENCEUR20",
    "description": "-20% sur la commande",
    "url": "https://...",
    "end_date": "2025-12-31"
  }
}
```

## Cron OVH staging
```
0 10 * * 2,5  php /scripts/agents/chasseur-promos.php
```
