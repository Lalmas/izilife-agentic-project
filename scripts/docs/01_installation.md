# 01 — Installation

## Dépendances Python

```powershell
pip install openpyxl requests python-dotenv anthropic openai pillow
```

Selon les agents :

```powershell
pip install beautifulsoup4 lxml
```

## Emplacement recommandé

```text
C:\Users\<user>\Documents\agentic_Workspace\scripts\
```

## Secrets

Créer :

```text
scripts/.env
```

Exemple :

```env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
IZILIFE_AGENT_TOKEN=
CANVA_API_KEY=
GOOGLE_API_KEY=
```

Ce fichier reste local/serveur. Il ne doit jamais être placé sur le Drive.
