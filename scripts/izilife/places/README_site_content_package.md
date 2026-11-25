# Paquet JSON de curation de site

Un paquet sépare la collecte d'un site complexe de l'import BO. `enrichisseur_contenus.py --analyze-only` lit les URL avec Playwright et utilise l'analyse IA du BO : **il fait des requêtes externes et consomme des appels IA, mais n'écrit aucun objet iziLife**. `site_content_package.py from-analysis` convertit ensuite son rapport local sans nouvel appel. Le paquet peut également être rédigé manuellement après lecture d'un site.

## Contrat

```json
{
  "schema_version": "izilife.site_content.v1",
  "target": {"scope_type": "SHOP", "scope_ref": "cryotera-pole-de-cryotherapie-lille"},
  "objects": [
    {
      "kind": "element_service",
      "source_url": "https://cryotera.fr/prestations/suivi-en-nutrition",
      "item": {
        "name": "Suivi en nutrition",
        "description": "Accompagnement nutritionnel personnalisé.",
        "source_evidence": "Programme et suivi établi par un(e) nutritionnist(e) professionnel(le)"
      },
      "review_status": "pending",
      "media": [],
      "warnings": []
    }
  ]
}
```

`kind` reprend **exactement** le BO : `element_service`, `eap`, `product`, `equipment`. `item` reprend les champs de `agentAnalyzeSiteContent` et `agentIngestSiteItem`. Une URL source et une preuve textuelle permettent de revenir à la page. Les états sont `pending`, `needs_review`, `approved`, `excluded`. Seul `approved` part à l'import.

Le type `product` utilise déjà l'importeur produit complet du Scraper : produit, `ProductCategory` et chemins de catégories, prix et historique, groupes/options et leurs prix, attributs, image distante (`primary_image_url`) et, lorsqu'il est fourni, `ElementMenu` avec ses relations catégorie/produit. Il ne faut donc pas reconstruire un agent Product séparé pour chaque nouveau site.

Le champ `item.service_name` résout le Service par **nom exact dans le même établissement** et renseigne directement `ElementAccessPrice.service_id` dans la base cible. Il retire alors les propriétaires Place/Shop/Partner de cet EAP : le Service est son propriétaire métier. `LocationEAPUseForService` n'est pas utilisée pour ce cas ; elle est réservée aux EAP supérieurs diffusés vers des Services. Aucun ID source n'est réutilisé. Un pack peut préciser `pack_composition: [{"name":"Nom exact de l'EAP unitaire","quantity":5}]` ; l'EAP unitaire est créé avant le pack.

`media` décrit une image téléchargée localement avec `source_url`, `local_file`, `role` et `rights_confirmed`. Les sept visuels Cryotera (six prestations et bilan) sont conservés dans `cryotera_media/` ; les URL du site étant signées et potentiellement éphémères, l'import utilise ces fichiers locaux. Le BO ajoute l'image à `Media`, stocke le fichier dans le bucket de l'environnement, puis renseigne `ElementService.media_id` ou `ElementAccessPrice.media_id` **uniquement si aucun média n'existe déjà**. Les EAP liés réutilisent l'image de leur Service, sans 22 copies S3. Le script refuse l'écriture tant que `rights_confirmed` n'est pas `true` sur un objet approuvé. Pour Cryotera, le responsable iziLife a explicitement autorisé l'utilisation des visuels de leurs pages ; le paquet de test local porte donc `true`. Les sept médias ont été rattachés localement. Le bilan utilise une copie fidèle réduite à 1 920 × 1 280 px pour respecter la limite BO, sans remplacer l'original. Pour un `product`, le flux existant `primary_image_url` reste disponible ; l'import média local direct n'est pas encore implémenté pour Product/Equipment.

## Commandes

Depuis `scripts/izilife` :

```powershell
python places/site_content_package.py from-analysis --report CHEMIN/analyse_seule_enrichisseur.json --scope-type SHOP --scope-ref cryotera-pole-de-cryotherapie-lille --output CHEMIN/cryotera.json
python places/site_content_package.py validate --file CHEMIN/cryotera.json
```

Le point d'entrée recommandé pour les nouveaux sites est désormais le lanceur unique :

```powershell
python site_package.py validate --file CHEMIN/paquet.json
python site_package.py plan --file CHEMIN/paquet.json
python site_package.py apply --file CHEMIN/paquet.json --env local --confirm-write
```

Il détecte automatiquement les paquets de contenu (`Services`, `EAP`, `Products`, `Equipment`), les paquets Experience (`Equipment`, objets de lieu, `Experiences`, `EAP`, médias et séances) et les paquets Circuit (tracé GeoJSON et étapes). Un manifeste `izilife.site_bundle.v1` peut référencer plusieurs fichiers dans `packages`, afin de lancer un site comportant plusieurs graphes sans les fusionner artificiellement.

Après revue et confirmation des objets, l'écriture est une commande distincte :

```powershell
python places/site_content_package.py apply --file CHEMIN/cryotera.json --env local --confirm-write
```

Cette commande fait des upserts BO ; elle ne constitue pas un dry-run. Le `--dry-run` de l'améliorateur liste seulement les sources et ne scrape rien ; `--analyze-only` scrape et appelle l'IA. Cryotera a été importé en production sur demande explicite, puis contrôlé dans le BO et dans la base ; cela ne change pas la règle générale qui interdit toute écriture production sans validation ciblée.

Avant chaque écriture, le script vérifie la cible, la colonne `ElementAccessPrice.service_id` et la nullabilité du prix Service. Le paquet local contient 7 Services et 22 EAP propres à cinq Services. Après correction, les 22 EAP portent directement leur `service_id`, sans ligne de diffusion. Le même paquet a été envoyé via Scraper à `cryotera-pole-de-cryotherapie-lille` en production ; sa migration doit appliquer la même propriété directe. Aucun import staging n'a été exécuté.

## Cryotera

Les six pages prestation fournies permettent de préparer des Services. Le suivi en nutrition décrit un bilan et un programme, avec tarif sur devis. La page tarifs ne contient pas ses montants dans le HTML initial, mais ils apparaissent après le rendu JavaScript ; ils ont été relevés dans le navigateur. Le bilan offert est enregistré comme Service à 0 €, sans EAP commercial. Une machine mentionnée dans une prestation n'est pas automatiquement un `equipment` iziLife.

Le relevé dynamique de la page tarifs du 28/10/2026 donne **22 formules chiffrées** pour cinq prestations (séances, carnets et abonnements), plus le suivi en nutrition sur devis. Le bilan personnalisé offert est un Service séparé. Le brouillon initial `cryotera_lille_draft.json` reste en `pending`. Le paquet distinct `cryotera_lille_services_eap_approved.json` a servi à l'import du 29/10/2026, d'abord sans médias. Les montants sont présentés par le site comme des **tarifs conseillés** pour des centres indépendants. Les 22 EAP sont actifs depuis la demande explicite du 29/10/2026 ; `need_to_be_confirmed_manually` reste à 1. Le responsable iziLife a ensuite explicitement autorisé les sept visuels des pages Cryotera : ils ont été importés et rattachés aux Services, sans dupliquer une image par EAP.
