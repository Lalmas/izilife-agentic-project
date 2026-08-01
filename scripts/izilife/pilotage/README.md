# Centre de pilotage des agents iziLife

Ce dossier fournit un point d’entrée Python unique pour inventorier, tester et
lancer les agents iziLife par zone. Chaque agent reste dans son fichier spécialisé.

Le pilote est portable : il fonctionne avec Python 3 sur Windows ou Linux. Il ne
dépend d’aucun fichier `.cmd`, PowerShell ou Bash.

## Commandes

Depuis `scripts/izilife` sous Linux :

```bash
python3 pilotage/izilife_agents.py agents
python3 pilotage/izilife_agents.py suites
python3 pilotage/izilife_agents.py planning
```

Sous Windows, utiliser `python` ou le lanceur Python installé :

```powershell
python pilotage\izilife_agents.py agents
py -3 pilotage\izilife_agents.py agents
```

Afficher un test sans rien lancer :

```bash
python3 pilotage/izilife_agents.py run lieux-chasseur --zone lille --city lille --preview
```

Faire le dry-run staging d’un agent :

```bash
python3 pilotage/izilife_agents.py run lieux-chasseur --zone lille --city lille
```

Autoriser un petit test avec écriture dans staging :

```bash
python3 pilotage/izilife_agents.py run lieux-chasseur --zone lille --city lille --limit 5 --execute
```

Afficher le regroupement hebdomadaire complet :

```bash
python3 pilotage/izilife_agents.py run-suite hebdomadaire-all --zone lille --city lille --preview
```

## Sécurité

- `staging` est l’environnement par défaut ;
- sans `--execute`, les agents utilisent leur dry-run ;
- la production exige `--execute --confirm-production JE_CONFIRME_PRODUCTION` ;
- les tâches sont exécutées une par une ;
- une suite s’arrête à la première erreur par défaut ;
- toujours tester chaque agent séparément avant le regroupement hebdomadaire.

## Séparation PC local / serveur

Ce pilote commande uniquement les agents Python présents sur le PC local, qu’il
soit sous Windows ou Linux.

Les Commands PHP et les hubs restent exécutés sur le serveur. Ils figurent dans le
Sheet de planning global, mais ne sont pas exécutables depuis ce pilote Python.

Les webhooks Stripe restent hors planning et ne sont jamais appelés par le pilote.

## Fichiers

- `izilife_agents.py` : pilote Python portable ;
- `catalogue.json` : annuaire des agents et regroupements Python ;
- `logs/` : journaux créés pendant les exécutions.

Le chemin des scripts peut être remplacé avec `IZILIFE_AGENT_SCRIPTS_ROOT`.
