# Sorties personnelles, visibilité, GPX et rémunération — 15 août 2026

## Décisions métier

- `CommunityActivity` est le domaine unique des activités sociales. Une activité peut être `PERSONAL`, `COMMUNITY` ou `USER_GROUP`.
- Une activité créée par un utilisateur hors communauté est toujours privée. Elle n'apparaît jamais sur les surfaces de découverte et reste accessible au créateur, aux invités ou par lien secret.
- Une sortie peut viser un lieu, un commerce, un événement ou une expérience iziLife, ou conserver une adresse libre (y compris un domicile).
- Le RSVP léger (`yes`, `maybe`, `no`) concerne l'organisation sociale. Dès qu'une réservation ou un billet iziLife porte la capacité ou le paiement, Booking/Ticket reste la source de vérité commerciale.
- La future feed de sorties et les outils d'organisation doivent enrichir `CommunityActivity`, sans créer un second domaine personnel concurrent.

## Visibilité Event / Experience

Les valeurs sont :

- `PUBLIC` : visible et ouvrable normalement ;
- `UNLISTED` : absent des résultats et surfaces de découverte, ouvrable par lien secret ;
- `MEMBERS_ONLY` : visible et ouvrable par les membres de la communauté ou du groupe ;
- `PRIVATE` : absent des surfaces, ouvrable uniquement par une autorisation personnelle ou un lien secret.

La publication (`is_active`), la visibilité et la billetterie sont trois notions distinctes. Un événement privé peut être gratuit avec RSVP, ou payant avec Booking/Ticket.

## Géométries Place / Equipment

`SpatialObjectGeometry` stocke une géométrie normalisée en GeoJSON et conserve son format source (`GPX`, `GEOJSON`, `KML`, `MANUAL`). Une ligne appartient exactement à un Place ou un Equipment. Le BO accepte les imports GPX, GeoJSON et KML, limite les fichiers à 10 Mo et ne permet pas les entités XML réseau.

## Rémunération EventSerie / AnnualCelebration

L'ordre de résolution est : Event direct, EventSerie, AnnualCelebration, puis lieu/commerce/page/partner/network. Une règle directe reste donc prioritaire. Le PayHub utilise cette chaîne pour calculer le plan ; l'activation réelle d'un split PSP demeure soumise au garde-fou fournisseur et à l'onboarding des comptes bénéficiaires.

## Déploiement

Les changements de schéma sont ajoutés uniquement à la fin de `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql`. Ils doivent être appliqués avant d'utiliser les nouveaux écrans. Aucun `ALTER` n'est lancé automatiquement par le FO ou le BO.
