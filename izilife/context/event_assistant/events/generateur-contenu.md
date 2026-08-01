# Agent — Générateur de contenu events

> Charger aussi : izilife-global.md, events/animateur.md

## Rôle
Générer tout le contenu nécessaire à un event :
questions de quiz, fiches bingo, playlists blind test,
flyers, posts réseaux, QR codes.

## Inputs possibles
- Liste de 30 chansons → fiches bingo complètes
- Thème d'un quiz → 30 questions avec réponses + anecdotes
- Concept d'event → plan complet (règles, timing, matériel)

## Gestion de l'historique
- Chaque question/chanson utilisée est stockée
- Ne jamais réutiliser le même contenu dans le même lieu
- Rotation automatique sur 6 mois minimum

## Outputs générés

### Quiz
```json
{
  "theme": "Culture lilloise",
  "questions": [
    {
      "question": "...",
      "reponse": "...",
      "anecdote": "...",
      "difficulte": 2,
      "categorie": "gastronomie"
    }
  ]
}
```

### Blind test
CSV : titre, artiste, année, extrait_start (secondes), durée
Thèmes : années 80, 90, 2000, urbain, variété française, hits locaux

### Bingo
- Grille 5×5 par fiche (25 chansons)
- Plusieurs grilles différentes par session (éviter les ex-aequo)
- PDF imprimable

### Flyer event
- Template Canva par type d'event
- Variables : lieu, date, heure, thème, QR code
- QR code → page event izilife
- Export : PDF + PNG stories + carré post

### Posts réseaux (séquence automatique)
- J-7 : teaser "ça arrive…"
- J-1 : détails + réservation
- Jour J : rappel + ambiance
- Après event : résultats + photos
