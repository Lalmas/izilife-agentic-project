# 31 — Agent Circuits

## Flux

```text
sources_circuits.xlsx
  → collecte URL randonnée / Decathlon Outdoor / autre
  → curate_circuits.xlsx
  → insertion directe Circuit + CircuitStep
```

## Raison du curate

Les circuits sont structurants et comportent des étapes. On garde une étape de curation pour éviter des inserts sales.

## Commandes

```powershell
python scripts/izilife/objects/agent_circuits.py --zone=lille --env=local --init
python scripts/izilife/objects/agent_circuits.py --zone=lille --env=local --collect --dry-run
python scripts/izilife/objects/agent_circuits.py --zone=lille --env=local --collect
python scripts/izilife/objects/agent_circuits.py --zone=lille --env=local --insert --dry-run
python scripts/izilife/objects/agent_circuits.py --zone=lille --env=local --insert
```
