# Reprise QA — Offres, paiements, grants et redeems

Date prévue : 30/09/2026 au matin

## Objectif

Valider de bout en bout les offres achetables, les Last Minute, les grants quantifiés, les avantages d’abonnement et les contraintes horaires avant de reprendre les chantiers Home Builder / IA Offers / Deals.

## État fonctionnel au 29/09 au soir

- Une commande reste unique et crée un grant par ligne consommable réellement identique (cible, effet, validité et contexte).
- La quantité achetée est portée par `BenefitGrant.max_uses_total`; le consommé est la somme de `BenefitLedger.bucket_count`.
- Un grant reste actif tant qu’il possède une quantité restante et passe à `consumed` uniquement lorsque son solde atteint zéro.
- Les BPR d’abonnement restent virtuelles et continuent d’utiliser leur moteur de quotas actuel : aucun grant quantifié n’est créé pour elles.
- L’échéance à 30 jours se termine à `23:59:59`.
- Un paiement annulé ne crée ni achat, ni grant, ni événement `earn`.
- Les retours succès et annulation doivent rester sur la fiche de l’offre avec le toast correspondant.
- « Mes avantages » est maintenant une liste compacte, une ligne par grant.
- La page du grant acheté et sa preuve reviennent vers « Mes avantages ».
- Une preuve issue d’un avantage d’abonnement utilisé depuis un lieu revient vers la fiche du lieu.
- La preuve demande explicitement de ne pas fermer la page avant validation par le commerçant.
- Un grant d’opération achetée repasse au redeem par les contraintes de sa BPR et par l’ouverture réelle du lieu, horaires exceptionnels compris.
- Un grant Last Minute n’est utilisable que le jour choisi et à l’intérieur du créneau exact enregistré au paiement ; l’expiration reste calée sur la fin de ce créneau.

## Préconditions du matin

1. Vérifier MariaDB et Apache.
2. Noter l’heure locale exacte du test.
3. Vérifier les horaires normaux et exceptionnels du commerce cible.
4. Vérifier la configuration brunch séparément dans `BookingConfigurationContent`.
5. Garder sous la main les identifiants de l’offre, de la BPR, des Effects, du commerce et de l’utilisateur.

## Matrice de tests

### 1. Paiement d’une Last Minute existante

- Effectuer un paiement réussi.
- Résultat UI attendu : retour sur la fiche Last Minute et toast vert.
- Résultat BDD attendu :
  - transaction `status = 2`, fournisseur `succeeded` ;
  - un `OfferPurchase` payé ;
  - une ligne `OfferPurchaseItem` par produit acheté ;
  - un `BenefitGrant` par ligne consommable avec `max_uses_total = quantité` ;
  - un événement `BenefitLedger earn` par grant, avec la quantité dans `bucket_count`.
- Vérifier la date d’utilisation et sa plage horaire, pas une plage de dates.
- Vérifier que la date est bien la date d’utilisation du coupon : achat aujourd’hui possible pour utilisation demain.
- Avant le début du créneau (par exemple le matin pour une offre de 18 h à 22 h) : redeem refusé avec grant intact.
- Pendant le créneau, lieu fermé : redeem refusé ; pendant le créneau et lieu ouvert : redeem autorisé.
- Après la fin du créneau : redeem refusé comme expiré.

### 2. Annulation et refus de paiement

Faire au moins deux scénarios distincts :

- annulation volontaire depuis Stripe ;
- paiement refusé/échoué par le fournisseur.

Pour chacun :

- retour attendu sur la fiche de l’offre ;
- toast rouge, jamais de toast vert ;
- conservation des paramètres GET de la fiche ;
- transaction conservée pour audit avec statut/provider_status cohérent ;
- aucun `OfferPurchase`, aucun grant, aucun `earn`, aucun fulfillment.

Répéter un refus sur l’autre contexte de paiement prévu (« CéT ») afin de confirmer que la correction générique PayHub ne casse pas ce flux.

### 3. Nouvelle Last Minute avec réservation obligatoire

- Créer la Last Minute depuis le BO puis refaire depuis le PS.
- Sélectionner le bon jour d’utilisation.
- Pour une expérience : sélectionner une ou plusieurs sessions existantes.
- Pour un événement : reprendre le jour et les horaires de l’événement ; si l’événement couvre plusieurs jours, choisir un jour compris dans sa plage.
- Aller jusqu’au paiement sans nécessairement confirmer au premier passage.
- Vérifier le contrat de fulfillment, la capacité et le lien entre quantité achetée et réservation.
- Vérifier que l’utilisateur ne peut pas payer une configuration invalide ou expirée.

### 4. Redeem d’un grant acheté

- Tenter le redeem hors horaire : refus attendu et grant toujours actif.
- Tenter dans l’horaire autorisé : choisir une quantité comprise entre 1 et le restant, puis produire une seule preuve.
- Pour une opération Last Minute, distinguer explicitement : avant le créneau, dans le créneau avec lieu fermé, dans le créneau avec lieu ouvert, puis après le créneau.
- Vérifier la page de preuve, le QR/code, l’expiration de la preuve et le bouton « Retour à mes avantages ».
- Vérifier qu’après un redeem partiel, le grant reste actif et que son solde diminue exactement de la quantité choisie.
- Vérifier qu’après consommation du dernier exemplaire, le grant passe à `consumed`.
- Rafraîchir et retenter le même grant : aucune double consommation.

### 5. Redeem d’un avantage d’abonnement

- Tester une BPR abonnement après la nouvelle structure BPR/Effects.
- Tester hors horaire puis dans l’horaire.
- Vérifier le titre/résumé BPR et les Effects appliqués.
- Vérifier les quotas (par jour, par lieu, par personne selon la règle).
- Vérifier la preuve et le retour vers la fiche du lieu.
- Confirmer qu’aucun chemin legacy ne lit les anciennes colonnes au lieu de `BenefitPolicyRuleEffect`.

### 6. Horaires normaux et exceptionnels

Test en quatre temps sur le même commerce :

1. horaire normal fermé, sans exception : redeem refusé ;
2. ajouter une ouverture exceptionnelle couvrant l’heure actuelle : redeem autorisé ;
3. mettre une fermeture exceptionnelle alors que l’horaire normal est ouvert : redeem refusé ;
4. retirer l’exception : retour au comportement de l’horaire normal.

Résultat technique attendu : les redeems classiques de grants et d’abonnements utilisent `Hourly_model::get*CurrentHourlyContents()`, qui ajoute les exceptions, puis `hourly_is_open_now()`, qui donne priorité à l’exception du jour.

### 7. Offre spéciale brunch

- Sans configuration brunch active/valide : redeem refusé.
- Avec un jour brunch mais hors plage brunch : redeem refusé.
- Dans la plage brunch : redeem autorisé.
- Vérifier que le refus est compréhensible pour l’utilisateur.

Règle attendue : le brunch exige simultanément un jour/créneau autorisé par `BookingConfigurationContent` + `BookingSlot` (`is_special_for_brunch = 1`) et un lieu ouvert. Une fermeture exceptionnelle du lieu bloque donc le redeem. Une ouverture exceptionnelle ne crée jamais, à elle seule, un créneau brunch absent de la configuration brunch.

## Contrôles BDD après chaque paiement

Relever la transaction concernée puis contrôler :

```sql
SELECT id, unique_id, status, provider_status, fulfilled_at
FROM Transaction
WHERE izilife_scope = 'IZILIFE_OFFERS'
ORDER BY id DESC LIMIT 5;

SELECT id, transaction_id, offer_id, status, quantity, grant_id
FROM OfferPurchase
ORDER BY id DESC LIMIT 5;

SELECT id, purchase_id, target_type, target_id, label, quantity
FROM OfferPurchaseItem
ORDER BY id DESC LIMIT 20;

SELECT id, source_id, source_reward_type, source_reward_id,
       benefit_kind, status, max_uses_total, expires_at
FROM BenefitGrant
ORDER BY id DESC LIMIT 20;

SELECT id, event_type, result, deny_reason, grant_id,
       bucket_count, payment_tx_id, created_at
FROM BenefitLedger
ORDER BY id DESC LIMIT 30;
```

## Ce qui peut être testé en backstage

- Préflight BDD avant/après chaque scénario.
- Vérification automatique qu’un refus ou une annulation ne produit aucun fulfillment.
- Vérification d’un grant par ligne identique et de `max_uses_total` par rapport aux quantités achetées.
- Tests des contraintes BPR avec une date/heure injectée, sans attendre l’heure réelle.
- Tests de la date et du créneau Last Minute injectés : avant, dedans et après la fenêtre.
- Tests des horaires normaux et exceptionnels avec un `DateTime` injecté.
- Tests des créneaux brunch issus des BCC/BookingSlot.
- Contrôle de non-régression des BPR abonnement et de leurs Effects.
- Contrôle des URL de retour et des métadonnées `return_url` / `cancel_url`.

## Ce qui doit rester manuel

- Le vrai parcours Stripe et ses écrans d’annulation/refus.
- Le ressenti des toasts et des redirections dans le navigateur.
- Le parcours BO/PS de création Last Minute avec autocomplete, sessions et événements multi-jours.
- L’expérience commerçant de validation du code/QR.
- La lisibilité mobile des listes, pages de grant et preuves.

La stratégie la plus sûre est hybride : préparer et contrôler automatiquement les états et invariants en backstage, puis effectuer manuellement les parcours externes et visuels.

## Chantiers suivants, après validation

### Deals

- Ajouter/brancher le rail Deals.
- Afficher dans Deals les offres pertinentes déjà exposées dans What To Do.
- Définir le classement et les exclusions (Brunch, Happy Hour, Last Minute, permanent, temporaire).

### Home Builder et IA Offers

- Ajouter la Home Builder restante.
- Faire converger IA Offers vers Deals (non commencé).
- Conserver un resolver unique pour éviter des règles différentes entre cards WTD, rails Deals et grandes fiches.

## Critères de sortie

- Aucun toast vert sur un paiement annulé/refusé.
- Aucun fulfillment sans paiement confirmé.
- Un grant par ligne consommable identique, avec la quantité achetée dans `max_uses_total`.
- Un redeem consomme exactement la quantité choisie et ne peut jamais dépasser le restant.
- Deux redeems concurrents ne peuvent pas surconsommer le même grant.
- Les contraintes BPR abonnement continuent de fonctionner.
- Les exceptions horaires gagnent sur l’horaire normal pour les redeems classiques.
- Un Last Minute est refusé avant son heure de début, après sa fin et lorsque le lieu est fermé.
- Un brunch est accepté uniquement si le créneau brunch et l’ouverture du lieu sont tous les deux valides.
- Le comportement brunch est démontré et sa relation avec les exceptions générales est décidée.
- Les retours des pages de grant/preuve sont cohérents avec leur origine.
