# Agent affiliation iziLife

GetYourGuide utilise un fichier contrôlé par zone :

```powershell
python affiliate_agent.py --provider getyourguide --zone lille --env local --init
python affiliate_agent.py --provider getyourguide --zone lille --env local
```

Ticketmaster part automatiquement des Event futurs rattachés aux Place/Shop actifs de `PlaceEventAffiliationSearch` :

```powershell
python affiliate_agent.py --provider ticketmaster --zone lille --env local --dry-run --max 20
python affiliate_agent.py --provider ticketmaster --zone lille --env local --max 20
```

`--visible` ouvre Chromium pendant la recherche. Un résultat sous le seuil `--min-score` reste à vérifier dans le fichier Excel et n'est pas inséré.

Variables requises : `AGENTIC_DRIVE_ROOT` et `IZILIFE_AGENT_TOKEN` (ou `AGENT_SECRET_TOKEN`).
