# Templates .env — NE JAMAIS METTRE SUR GOOGLE DRIVE

## 1. .env global (C:\Users\alcamara\Documents\agentic_Workspace\.env)
# Clés API — partagées par tous les scripts
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
CANVA_API_KEY=

## 2. .env.izilife (C:\Users\alcamara\Documents\agentic_Workspace\izilife\.env.izilife)
# Config moteurs izilife — commune à toutes les zones
LLM_PROVIDER=claude
IMAGE_ENGINE=gpt
IMAGE_LLM=gpt
CLAUDE_MODEL=claude-sonnet-4-6
OPENAI_MODEL=gpt-4o
IMAGE_MODEL=gpt-image-1

## 3. .env.agence (C:\Users\alcamara\Documents\agentic_Workspace\agence\.env.agence)
# Config moteurs agence — commune à tous les clients
LLM_PROVIDER=openai
IMAGE_ENGINE=gpt
IMAGE_LLM=gpt
OPENAI_MODEL=gpt-4o
IMAGE_MODEL=gpt-image-1

## 4. .env.override (optionnel — dans dossier zone ou client LOCAL si override nécessaire)
# Override pour une zone/client spécifique
# Ex: client qui a ses propres tokens
# LLM_PROVIDER=claude
# ANTHROPIC_API_KEY=sk-ant-client-xxx
