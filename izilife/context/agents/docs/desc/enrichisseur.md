# Agent — Enrichisseur

> Charger aussi : izilife-global.md, dev/agents-socle.md

## Rôle
Améliorer les fiches de lieux dont le score de remplissage est insuffisant.
Aller chercher les informations manquantes sur le web.
Pousser un JSON enrichi via postIngestJson().

## Déclenchement
- Tous les soirs à 1h (cron PC local — nécessite navigateur)
- 40 à 50 lieux par run
- **Désactivé jusqu'au passage à Max 200€**
  (remplacé provisoirement par enrichissement manuel)

## Outils
- Claude in Chrome (CIC) — lit et comprend les pages web
- PHP local — pousse le JSON enrichi
- Google Photos API — URLs photos si manquantes

## Workflow
1. Récupérer 40-50 lieux avec score bas depuis la BDD
2. Pour chaque lieu :
   a. Lire le JSON Google Places en cache (déjà stocké)
   b. CIC visite : Google Maps + TripAdvisor + site du lieu (3-5 pages max)
   c. Extraire : description, tags, équipements, HH, ambiance, URLs photos
   d. Comparer avec ce qui est déjà en BDD — ne pas écraser ce qui est bon
   e. Construire le JSON diff (uniquement les champs à améliorer)
   f. Pusher via postIngestJson(type=place) → place_tmp
3. Marquer le lieu comme "traité" dans la file
4. Logger : nb lieux traités, score moyen avant/après

## Règles
- Un lieu traité est retiré de la file (ne repasse pas si score OK)
- Ne jamais écraser un champ déjà correctement rempli
- Si le lieu est en bord de mer → vérifier si tag "bord de mer" existe → l'ajouter
- Photos : passer les URLs dans le JSON, la méthode izilife gère l'upload
- Chaque appel CIC = 1 lieu = contexte remis à zéro

## JSON de sortie attendu
```json
{
  "type": "place",
  "source": "enrichisseur",
  "google_place_id": "ChIJ...",
  "fields": {
    "description": "...",
    "tags": ["bord de mer", "terrasse", "jazz"],
    "equipements": ["wifi", "terrasse", "parking"],
    "happy_hour": "Lun-Ven 17h-19h",
    "ambiance": "Cosy, lumière tamisée, clientèle 30-45 ans",
    "photos_urls": ["https://...", "https://..."]
  }
}
```

## Cron PC local
```
0 1 * * *  php /scripts/agents/enrichisseur.php --max=50
```
