# Scripts Agent CM — Installation & Lancement

## Prérequis (PC local Windows)

```powershell
# Installer Python si pas déjà fait : https://python.org
pip install anthropic openpyxl openai
```

## Variables d'environnement (à faire une seule fois)

Dans PowerShell (en admin) :
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-xxxx", "User")
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY",    "sk-xxxx",     "User")
```
Redémarrer PowerShell après.

## Lancement

### izilife
```powershell
cd G:\Mon Drive\agentic_workspace\izilife\social\scripts
python cm_izilife.py
```

### Agence (client spécifique)
```powershell
python cm_agence.py --client nom_client
python cm_agence.py --list       # voir les clients configurés
```

## Workflow complet

1. Ouvrir planning_izilife.xlsx
2. Remplir les lignes (TYPE, VILLE, THÈME, DATA...) → statut "À faire"
3. Sauvegarder et fermer l'Excel
4. Lancer le script
5. Rouvrir l'Excel → les colonnes CAPTION et HASHTAGS sont remplies
6. Lire, ajuster si besoin → passer à "Validé"
7. Publier manuellement sur Instagram/Facebook

## Modifier le LLM (izilife)

Dans cm_izilife.py, ligne :
```python
LLM_PROVIDER = "claude"   # → changer en "openai" pour GPT-4o
```

## Ajouter un client agence

Dans cm_agence.py, section CLIENTS :
```python
"nom_client": {
    "excel"   : "planning_nom_client.xlsx",
    "context" : ["community-manager-nom_client.md"],
    "provider": "openai",   # openai si client ne paie pas forfait Max
    "compte"  : "@compte_instagram_client",
    "notes"   : "Description rapide du client",
},
```
Créer le dossier :
  G:\Mon Drive\agentic_workspace\clients\nom_client\
    ├── planning_nom_client.xlsx      (copie du template Excel)
    └── context\
          └── community-manager-nom_client.md

## Structure dossiers attendue

G:\Mon Drive\agentic_workspace\
  ├── izilife\
  │   └── social\
  │       ├── planning_izilife.xlsx
  │       └── scripts\
  │             ├── cm_izilife.py
  │             ├── cm_agence.py
  │             └── README.md
  ├── clients\
  │   └── [nom_client]\
  │       ├── planning_[nom_client].xlsx
  │       └── context\
  │             └── community-manager-[nom_client].md
  └── context\
      └── social\
          └── izilife\
                ├── izilife-social-strategy.md
                ├── community-manager.md
                └── planning-template.md
