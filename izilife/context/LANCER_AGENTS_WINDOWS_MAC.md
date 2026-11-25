# Lancer les agents iziLife — Windows et Mac

Ce document complète `GUIDE_AGENTS_PROD.md`. Il décrit l'installation commune,
les secrets et les commandes des agents planifiés dans
`deploy/cron/izilife-agents-prod.crontab`.

## 1. Secret commun et sécurité

Tous les agents HTTP utilisent le même en-tête `X-Agent-Token`. Le secret est lu
depuis `IZILIFE_AGENT_TOKEN` ou `AGENT_SECRET_TOKEN`. Ne jamais le mettre dans un
classeur Excel, le dépôt Git ou une commande conservée dans l'historique.

Variables habituelles :

```text
AGENT_SECRET_TOKEN=...
IZILIFE_AGENT_TOKEN=...
AGENTIC_DRIVE_ROOT=...
OPENAI_API_KEY=...
```

`IZILIFE_AGENT_TOKEN` et `AGENT_SECRET_TOKEN` peuvent contenir la même valeur.
Certains anciens agents ne lisent encore que `IZILIFE_AGENT_TOKEN`.

## 2. Sur ce PC Windows

Racine actuelle :

```powershell
$workspace = 'C:\Users\alcamara\Documents\agentic_Workspace'
$root = "$workspace\scripts\izilife"
$py = "$workspace\.venv_google_hours\Scripts\python.exe"
$envFile = "$root\.env.izilife"
```

Charger les variables du fichier dans le terminal courant avant un ancien agent
qui ne charge pas lui-même son `.env` :

```powershell
Get-Content -LiteralPath $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
        $pair = $line.Split('=', 2)
        [Environment]::SetEnvironmentVariable(
            $pair[0].Trim(), $pair[1].Trim().Trim('"').Trim("'"), 'Process'
        )
    }
}
if (-not $env:IZILIFE_AGENT_TOKEN -and $env:AGENT_SECRET_TOKEN) {
    $env:IZILIFE_AGENT_TOKEN = $env:AGENT_SECRET_TOKEN
}
```

Vérifier sans afficher le secret :

```powershell
if ($env:IZILIFE_AGENT_TOKEN) { 'Token chargé' } else { 'Token absent' }
```

Exemple Hub local :

```powershell
& $py "$root\hubs\local_hub_collector.py" `
  --workbook "$root\hubs\local_hub_endpoints.xlsx" `
  --env "$root\.env.izilife"
```

## 3. Sur le Mac

Installation initiale :

```bash
cd /Users/lal/izilife-agentic-project/scripts/izilife
python3 -m venv .venv
.venv/bin/python -m pip install -r hubs/requirements.txt
.venv/bin/python -m playwright install chromium
mkdir -p /Users/lal/Library/Logs
```

Créer `/Users/lal/izilife-agentic-project/scripts/izilife/.env`, renseigner les
secrets, puis protéger le fichier :

```bash
chmod 600 /Users/lal/izilife-agentic-project/scripts/izilife/.env
```

Pour un lancement manuel d'un ancien agent :

```bash
cd /Users/lal/izilife-agentic-project/scripts/izilife
set -a
source .env
set +a
export IZILIFE_AGENT_TOKEN="${IZILIFE_AGENT_TOKEN:-$AGENT_SECRET_TOKEN}"
```

Hub local manuel :

```bash
.venv/bin/python hubs/local_hub_collector.py \
  --workbook hubs/local_hub_endpoints.xlsx \
  --env .env
```

Test sans LLM ni EventTmp :

```bash
.venv/bin/python hubs/local_hub_collector.py \
  --workbook hubs/local_hub_endpoints.xlsx \
  --env .env --discover-only
```

## 4. Installer le crontab général sur le Mac

Toujours sauvegarder l'ancien crontab :

```bash
crontab -l > "$HOME/crontab.backup.$(date +%Y%m%d-%H%M%S)"
crontab /Users/lal/izilife-agentic-project/deploy/cron/izilife-agents-prod.crontab
crontab -l
tail -f /Users/lal/Library/Logs/izilife-cron.log
```

La ligne Hub local est fournie à 23 h 30 mais reste commentée par sécurité.
Le validateur EventTmp conserve son horaire de 23 h 35. Après validation
manuelle, décommenter volontairement la ligne Hub ; elle lit uniquement les
lignes `enabled` de `hubs/local_hub_endpoints.xlsx`.

## 5. Commandes manuelles des agents planifiés

Depuis `scripts/izilife`, préfixer chaque commande par `.venv/bin/python` sur Mac
ou `& $py` sous PowerShell.

& 'C:\Users\alcamara\Documents\agentic_Workspace\.venv_google_hours\Scripts\python.exe' .\medias\media_curator.py --zone=lille --env=prod --max=500

### Événements

```text
hubs/local_hub_collector.py --workbook hubs/local_hub_endpoints.xlsx --env .env
events/shotgun_scraper.py --env=prod --city=lille
events/ingest_manual_curate.py --zone=lille --env=prod
events/event_structures.py --zone=lille --env=prod --max=100
events/event_calendar.py --zone=lille --env=prod --max=100
events/validate_event_tmp.py --env=prod --mode=validate --zone=lille --limit=100 --allow-ai
events/territorial_aggregator.py --config=events/territorial_sources/lille-zone.json --env=prod --max-links=100 --output-dir=REPORTS --send-new-to-scraper --confirm-write
```

### Médias, contenus et offres

```text
agent_external_media.py --zone=lille --env=prod
agent_pages.py --zone=lille --env=prod
site_package_inbox.py --env=prod --max=20 --apply --retry-errors --confirm-production=I_CONFIRM_PRODUCTION_PACKAGE_INBOX
offers/izilife_subscription_benefit.py --zone=lille --env=prod
offers/special_offer.py --zone=lille --env=prod
brunch/brunch.py --zone=lille --env=prod
media_downloader.py --env=prod
medias/media_curator.py --zone=lille --env=prod --max=500
```

### Lieux et enrichissement

```text
places/createur_lieux.py --zone=lille --city=lille --env=prod
places/google_hours_agent.py --env=prod --apply --confirm-production I_CONFIRM_PRODUCTION_HOURS --max=100
places/enrichisseur_contenus.py --zone=lille --env=prod --max=40
experiences/validate_experience_tmp.py --env=prod --mode=validate --limit=100 --allow-ai
```

`google_hours_agent.py` ouvre Chromium en mode visible. Ne pas le mettre dans le
crontab tant que le Mac n'a pas une session graphique stable.

### Référentiels et transferts

```text
geography/classificateur_territoires.py --zone=lille --env=prod --max=100
equipments/equipment.py --zone=lille --env=prod --max=100
escapades/escapade_proposal.py --zone=lille --env=prod --max=100
links/link.py --zone=lille --env=prod --max=100
geography/city_subdivisions.py --zone=lille --env=prod --max=100
geography/streets.py --zone=lille --env=prod --max=100
commercial_centers/transfer_pilot.py run --zone=lille --env=prod --apply --confirm-production=I_CONFIRM_PRODUCTION_TRANSFER
spotlights/spotlight.py --zone=lille --env=prod --max=100
tags/tags.py --zone=lille --env=prod --max=100
activity_proposals/activity_proposal.py --zone=lille --env=prod --max=100
```

## 6. Ajouter un nouvel agent Python

1. Placer le script sous `scripts/izilife/<domaine>/`.
2. Utiliser `X-Agent-Token` et accepter `IZILIFE_AGENT_TOKEN` ou
   `AGENT_SECRET_TOKEN`.
3. Prévoir `--env`, une limite (`--max`) et si possible `--dry-run`.
4. Si un Excel pilote l'agent, stocker la configuration sans aucun secret.
5. Tester manuellement sur un seul objet.
6. Ajouter ensuite une ligne au crontab, avec `cd`, `|| exit 1`, journal START/END,
   code retour et redirection vers `izilife-cron.log`.
7. Espacer les agents qui utilisent Playwright ou un LLM.

Modèle :

```cron
MM HH * * * /bin/zsh -lic 'cd /Users/lal/izilife-agentic-project/scripts/izilife || exit 1; echo "\n===== START NOM $(date) ====="; .venv/bin/python domaine/agent.py --env=prod --max=100; rc=$?; echo "===== END NOM rc=$rc $(date) ====="; exit $rc' >> /Users/lal/Library/Logs/izilife-cron.log 2>&1
```
