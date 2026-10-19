# Validation des agents iziLife — production

Cette procédure ne commence qu'après une campagne staging entièrement verte et
la livraison du même code en production.

## Principe

Les scripts sont lancés localement, mais utilisent les classeurs du Drive de
production, les API de production et la base de production. Les données de test
doivent être nouvelles, connues et limitées à 1–5 objets. Une relance d'une ligne
déjà terminée valide l'idempotence ; elle ne remplace pas un test de création.

Le runner ne lit ni ne modifie aucun `.env`. Les variables nécessaires sont
chargées dans le terminal par l'opérateur.

## Campagne contrôlée

Audit sans écriture :

```powershell
python tests/staging_smoke.py --target-env prod --prepare --max 5
```

Après vérification des lignes `pending`, exécution réelle :

```powershell
python tests/staging_smoke.py --target-env prod --allow-prod --prepare --run --online --event-search --media --max 5
```

Le runner refuse les écritures de production sans `--allow-prod`. Contrôler le
rapport PASS/FAIL, puis les objets dans la base et le BO. Aucun cron n'est
installé tant qu'une erreur, une route absente, un `unmapped` inattendu ou une
donnée incohérente subsiste.

## Installation du planning sur le Mac agents

Le fichier versionné est
`deploy/cron/izilife-agents-prod.crontab`. Il contient notamment les agents
calendrier d'événements, territorial, quartiers, rues, Equipment,
EscapadeProposal, Améliorateur++, Spotlight, Tags et ActivityProposal.

Après validation production :

```bash
crontab -l > "$HOME/crontab.backup.$(date +%Y%m%d-%H%M%S)"
crontab /Users/lal/izilife-agentic-project/deploy/cron/izilife-agents-prod.crontab
crontab -l
```

La première commande conserve une sauvegarde horodatée. La dernière permet de
comparer immédiatement le planning installé au fichier livré.
