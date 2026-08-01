# Chantier — Stack IA privé izilife

> Charger avec izilife-global.md pour le contexte projet.
> Objectif : comprendre, choisir et installer un stack IA maison
> pour remplacer progressivement les APIs payantes (Claude, GPT, OCR...).

---

## Contexte

Fondateur solo d'izilife. Utilise actuellement :
- Claude API / GPT API → génération texte agents
- OCR externe → lecture de documents
- Recherche sémantique → pas encore en place

Objectif à terme : tout faire tourner sur un serveur dédié loué chez un
hébergeur (pas à domicile). Zéro token, données privées, coût fixe mensuel.

---

## Questions à explorer dans cette conversation

1. C'est quoi exactement un LLM open source ? Comment ça tourne ?
2. Quelle différence entre Llama, Deepseek, Qwen, Mistral ?
3. C'est quoi Ollama ? Comment on installe un LLM en 10 minutes ?
4. C'est quoi un GPU et pourquoi c'est important pour un LLM ?
5. Héberger où ? OVH, Hetzner, Vast.ai, RunPod... quelles différences ?
6. C'est quoi l'OCR ? Tesseract vs PaddleOCR vs Surya ?
7. C'est quoi les embeddings et la recherche vectorielle ?
8. C'est quoi Whisper et à quoi ça sert ?
9. Comment brancher tout ça aux scripts Python existants ?
10. Roadmap réaliste : quand basculer de l'API vers le local ?

---

## Stack cible (à valider et installer progressivement)

```
Serveur loué (VPS GPU chez Hetzner / Vast.ai / RunPod)
  ├── Ollama           → faire tourner les LLM open source
  │     Modèles cibles : Llama3, Deepseek, Qwen, Mistral
  ├── OCR local        → Tesseract (simple) ou PaddleOCR (précis)
  ├── Whisper          → transcription audio (open source OpenAI)
  └── Qdrant / Chroma  → recherche vectorielle / sémantique
```

---

## Ce qui existe déjà (ne pas réinventer)

- Scripts Python agents CM : cm_izilife.py, cm_agence.py
  Déjà prévu LLM_PROVIDER switchable → brancher Ollama = changer l'URL
- izilife stack : CI4 PHP, MySQL, OVH mutualisé
- PC local Windows (alcamara) + OptiPlex agents (à venir)
- Google Drive monté en G:\ pour les fichiers partagés

---

## Priorités d'apprentissage suggérées

Étape 1 : Installer Ollama en local sur le PC Windows
  → Télécharger un modèle (ex: llama3:8b ou deepseek-r1:7b)
  → Faire un appel depuis Python
  → Voir que c'est exactement la même chose que l'API Claude/GPT

Étape 2 : Comprendre les différences entre modèles
  → Llama (Meta), Deepseek (Chine), Qwen (Alibaba), Mistral (France)
  → Lequel est le mieux pour la génération de posts en français ?

Étape 3 : Choisir un hébergeur GPU
  → Comparer Hetzner (serveur dédié), Vast.ai (GPU à la demande),
    RunPod (simple, bien documenté)
  → Installer Ollama sur le VPS

Étape 4 : Brancher les scripts existants sur Ollama
  → Changer 3 lignes dans cm_izilife.py
  → Tester la qualité vs Claude API

Étape 5 : OCR et recherche vectorielle
  → À faire quand les besoins concrets arrivent

---

## Vision long terme

Ce stack privé devient le moteur IA d'izilife.
Les commerces qui s'inscrivent sur la plateforme utilisent ce moteur
mutualisé (ou filent leur propre clé API).
Coût fixe serveur = partagé entre tous les utilisateurs.
Plus izilife grandit, plus le coût par utilisateur baisse.
