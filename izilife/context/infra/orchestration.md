# Infrastructure & orchestration agents

> Charger aussi : izilife-global.md, dev/agents-socle.md

## Deux cerveaux planificateurs

### OVH staging (cron)
Tout ce qui ne nécessite pas de navigateur :
```
0 1 * * 1    php /scripts/agents/inspecteur.php --ville=lille
0 2 * * 1    php /scripts/agents/greffier.php --max=50
0 9 * * 0    php /scripts/agents/chasseur-events.php --mode=full
0 10 * * 2,5 php /scripts/agents/chasseur-promos.php
0 8 * * 1    php /scripts/agents/redacteur-blog.php
```

### PC local (cron Linux)
Tout ce qui nécessite Chrome/CIC/Cowork :
```
0 1 * * *  php /scripts/agents/enrichisseur.php --max=50
0 9 * * 0  bash /scripts/lancer-cowork.sh chasseur-events
0 10 * * * bash /scripts/lancer-cowork.sh community-manager
```

## Pont OVH → PC local (futur)
Serveur Flask Python (~20 lignes) sur le PC local.
OVH appelle `http://pc-local:8080/lancer?agent=enrichisseur`
Flask déclenche le script CIC/Cowork correspondant.

## Google Sheets hub — onglets
- `Inspecteur` — rapport par ville (manquants/incomplets/fermés)
- `File_Greffier` — lieux à intégrer
- `File_Enrichisseur` — lieux à améliorer (score bas)
- `File_Events` — events détectés à valider
- `File_Promos` — promos détectées à valider
- `Planning_Social` — planning éditorial
- `Log_Agents` — log de tous les runs (date, agent, nb items, erreurs)

## PC fixe dédié (à acheter)
- Dell OptiPlex reconditionné
- 16 Go RAM min, 32 Go recommandé
- SSD 256 Go min
- Ethernet filaire obligatoire
- Ubuntu ou Windows + WSL2
- Allumé en permanence

## Contrainte actuelle
Pas de PC dédié → agents CIC/Cowork tournent sur le PC actuel,
manuellement ou avec les crons Windows/Linux existants.
OVH staging gère tout le reste.
