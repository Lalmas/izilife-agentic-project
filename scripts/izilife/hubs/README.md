# Collecteur Hub local

Le navigateur local récupère les pages que l'hébergement izilife ne peut pas lire. Le serveur reste responsable des règles d'endpoint, du nettoyage, des lots LLM et de l'insertion dans les tables temporaires.

## Installation Windows ou macOS

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Le fichier `.env` doit exposer le même secret que les autres agents :

```text
AGENT_SECRET_TOKEN=...
```

## Lancement

```bash
python local_hub_collector.py --workbook local_hub_endpoints.xlsx --env ../../../../.env
```

Pour contrôler Chromium visuellement, ajouter `--headed`. Pour une seule source, ajouter `--only-endpoint 2`.
