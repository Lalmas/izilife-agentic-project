# izilife — Animateur de lieux & organisateur d'events

> Charger aussi : izilife-global.md

## Rôle
Organiser des events dans des lieux pour :
1. Générer des revenus directs (animation)
2. Alimenter izilife en events (contenu)
3. Animer la communauté locale (cercle vertueux)

## Types d'events

### Events simples (dans les lieux, commission)
- Concert acoustique
- DJ set
- Soirée quiz standard
- Blind test musical

### Events signature izilife (plus chers, tu animes)
- **Quiz izilife** — questions locales, format équipes, vol de points
- **Blind test izilife** — format compétition, mélange de genres
- **Bingo musical** — fiches générées par agent
- **Tournoi fléchettes fun**
- **Beer pong compétition**
- **Soirée jeux de société**
- **Izilympic Games** — multi-épreuves fun retravaillé

### Format commun events signature
- Équipes mélangées (favoriser les rencontres)
- Système point/tension : vol de points, bonus, malus
- Différenciation forte — personne d'autre ne fait ce format

## Pipeline création event
1. Tu définis : type, lieu, date, thème
2. Agent génère : questions quiz / fiches bingo / playlist blind test
3. Agent crée l'event sur izilife (via EventOrganizer API)
4. Agent génère : flyer, posts réseaux, stories
5. Agent crée le QR code de l'event
6. Après l'event : posts résultats + photos

## EventOrganizer controller
- Endpoint : créer un event en tant qu'organisateur izilife
- Accessible via API avec compte de service
- Paramètres : lieu, date, type, description, image, prix, lien billetterie

## Revenus
- Commission sur les entrées (events simples)
- Forfait animation (events signature)
- Contenu izilife généré automatiquement à chaque event
