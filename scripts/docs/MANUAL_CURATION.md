# Curation manuelle déterministe

## Création Event

`scripts/izilife/events/ingest_manual_curate.py` lit `curate_events.xlsm`.

Priorité des données :

1. cellules Excel remplies ;
2. HTML, JSON-LD et données structurées du site ;
3. OCR/vision seulement pour les champs encore absents.

Si `title`, `description`, `start_date`, `event_category_ref` et le lieu sont déjà présents, une image Instagram est uniquement téléchargée comme média : aucun OCR/LLM n'est appelé. Le média doit être l'original Instagram ou un téléchargement iGram ; les captures et `og:image` sont interdits.

## Amélioration

Créer le classeur :

```powershell
python scripts/izilife/manual_improver.py manual_improver.xlsx --init
```

Onglets : `Lieux`, `Events`, `XP`. `target_ref` accepte une URL iziLife, un ID, un `string_id` ou un `unique_id`. Le script n'appelle jamais OpenAI.

## BO

URL : `/manualCuration`.

Configurer sur chaque serveur, sans versionner le secret :

```dotenv
MANUAL_CURATION_ACCESS_CODE="un-code-long-et-prive"
```

Le rapprochement accepte un ID/string_id exact, un nom normalisé ou un texte approché. Une correspondance floue n'est acceptée que si le meilleur résultat dépasse le seuil et se détache nettement du second ; sinon aucune écriture n'est faite.
