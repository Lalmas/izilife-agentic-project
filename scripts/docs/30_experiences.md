# 30 — Agent Expériences

## Flux

```text
sources_experiences.xlsx
  → collecte URL
  → LLM structure expérience
  → scraping_experience_tmp
  → validation humaine BO
```

## Commandes

```powershell
python scripts/izilife/objects/agent_experiences.py --zone=lille --env=local --init
python scripts/izilife/objects/agent_experiences.py --zone=lille --env=local --collect --dry-run
python scripts/izilife/objects/agent_experiences.py --zone=lille --env=local --collect --max=5
```
