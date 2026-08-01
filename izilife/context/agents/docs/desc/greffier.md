# Agent — Greffier

> Charger aussi : izilife-global.md, dev/agents-socle.md

## Rôle
Intégrer les lieux manquants détectés par l'Inspecteur.
Marquer comme fermés les lieux signalés.
Toujours via _tmp — jamais d'écriture directe en prod.

## Déclenchement
- Automatiquement après l'Inspecteur (cron enchaîné)
- Manuel : quand on veut intégrer un lot de nouveaux lieux

## Outils
- PHP + Google Places API (Place Details)
- 0 token Claude
- Méthode izilife : `postFetchAndStoreOnePlace()`

## Workflow
1. Lire la file "Manquants" depuis Google Sheets (onglet Inspecteur)
2. Pour chaque place_id :
   a. Vérifier si JSON déjà en cache (table google_place_json)
   b. Si absent → appeler Place Details → stocker JSON en cache
   c. Appeler `postFetchAndStoreOnePlace(place_id)` → insère en place_tmp
3. Pour les "Suspects fermés" validés humainement :
   a. Marquer le lieu comme fermé en place_tmp → validation → prod
4. Mettre à jour Google Sheets : statut "Traité" + id _tmp créé

## Règles
- Ne jamais écrire directement en prod
- Vérifier le cache JSON avant tout appel API
- Si `postFetchAndStoreOnePlace()` échoue → logger et passer au suivant
- Max 50 lieux par run (préserver le quota Places API)

## Cron OVH staging
```
0 2 * * 1  php /scripts/agents/greffier.php --max=50
```
