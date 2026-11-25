# Brief — extraire des sites complexes pour iziLife

À coller dans une conversation dédiée quand une prestation, une carte, un tarif ou un équipement est difficile à extraire automatiquement.

## Objectif

Lire les pages fournies, extraire les informations utiles **une seule fois**, puis produire un paquet JSON vérifiable pour le BO iziLife. La conversation réalise l'analyse ; l'outil local importe ensuite les objets approuvés. Ne pas appeler à nouveau Google Places ou un LLM si l'information est déjà présente dans iziLife, son cache ou le paquet validé.

## Entrées à fournir

- URL du site et des pages pertinentes ; établissement cible `PLACE` ou `SHOP` avec son `string_id` et son environnement.
- Ce que l'on cherche : Services, EAP et leurs tarifs/variantes, Products et catégories/options, Equipment, liens, horaires, images et preuves.
- Consignes métier propres au lieu, exclusions, langues, date de consultation et éventuels droits d'utilisation des images.

## Travail demandé à la conversation

1. Vérifier d'abord ce qui existe dans iziLife et les référentiels BO ; ne pas inventer de type, catégorie, colonne ou référence.
2. Lire les pages et relever pour chaque donnée sa source exacte et une preuve courte. Distinguer prix fixe, prix conseillé, devis, gratuit et tarif variable. Ne jamais remplacer une valeur inconnue par zéro.
3. Relier chaque EAP au Service qui porte réellement ce tarif. Séparer les séances, carnets, abonnements et options selon le modèle BO. Laisser les EAP commerciaux inactifs et à confirmer avant vente.
4. Distinguer Equipment réel, Service, produit et simple variante commerciale. Ne pas créer une machine ou un équipement parce qu'il est seulement mentionné dans une description.
5. Lister les URL des images et le rôle voulu. Ne pas télécharger ni importer une image sans droit de réutilisation confirmé ; préserver `rights_confirmed=false` tant que ce point est inconnu.
6. Produire le contrat adapté : `izilife.site_content.v1` pour Services/EAP/Products/Equipment, `izilife.experience_site.v1` pour Experiences et séances, ou `izilife.circuit_site.v1` pour un parcours avec tracé et étapes. Utiliser `pending` ou `needs_review` pour les doutes ; seul `approved` est importable. Ne pas mélanger artificiellement ces graphes dans un même objet.
7. Donner un tableau final : objets proposés, tarifs confirmés, doutes, images, exclusions et questions ciblées. Ne lancer aucun import de production depuis cette conversation.

## Contrat et vérification

Référence : `scripts/izilife/places/README_site_content_package.md`. Le lanceur commun est `scripts/izilife/site_package.py` ; il délègue aux moteurs de contenu, d'Experience et de Circuit. Le flux Product existant couvre déjà catégories, options, tarifs, images distantes et `ElementMenu`. `--analyze-only` de l'améliorateur peut encore coûter des appels externes et IA ; le paquet JSON relu localement n'en coûte pas. Vérifier le paquet avec `validate` avant tout `apply`. Cryotera Lille est un exemple de contenu commercial ; la Citadelle documente le cas des circuits et lieux vivants.

## Maîtrise des coûts

Éviter plusieurs analyses IA de la même page. Lire d'abord le HTML et le rendu Playwright, sélectionner les sections métier, dédupliquer par URL canonique et hash du contenu, puis n'envoyer au modèle que les passages nécessaires. Réutiliser le JSON approuvé pour les environnements suivants ; les IDs et médias doivent être remappés dans chaque destination. Compter séparément les appels ChatGPT/Codex de cette conversation, les appels API OpenAI du BO, Google Places, ScrapingBee, Twilio et le stockage.
