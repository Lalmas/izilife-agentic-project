# Décisions Community / groupes / feed — 10 août 2026

Ce document remplace les décisions antérieures imposant un groupe `Général`.

## Hiérarchie

- Deux niveaux de `Community` au maximum : `C → SC`.
- Chaque Community, racine ou enfant, peut posséder des `UserGroup` plats : `C → G1/G2` ou `C → SC → G1/G2/G3`.
- Aucun groupe `Général` n'est créé automatiquement ni rendu obligatoire.
- Une sous-communauté possède sa propre identité, ses administrateurs, ses membres, son agenda et son éventuel Partner. Un groupe reste un espace interne de sa Community.

## Annonces et publications

- Chaque Community, y compris une sous-communauté, et chaque UserGroup possède son propre feed.
- Une publication cible exactement une Community **ou** un UserGroup.
- Le type `announcement` est publié par les administrateurs/modérateurs de la cible.
- Les membres autorisés de la cible peuvent commenter et réagir.
- Les autres publications peuvent partager une `CommunityActivity`, un Event, une Experience, un Place, un Shop ou une Page existants sans les dupliquer.
- Les commentaires sont plats, chronologiques et paginés/chargés progressivement. Il n'existe pas d'arbre récursif de réponses.

## Architecture sociale générique

- Il n'existe ni table `CommunityPost` ni table `SocialFeed`. `Post` porte directement `scope_level` et `scope_id` (`community` ou `user_group`).
- `owner_type/owner_id` dit qui publie. `scope_level/scope_id` est facultatif et indique une destination spéciale ; sans scope, le Post apparaît dans le feed propre de son owner.
- Une publication communautaire a toujours un User comme owner et une Community ou un UserGroup comme scope. Shop, Place, Page ou Partner publient uniquement dans leur propre feed avec un scope vide ; ils ne publient pas dans les communautés.
- `Post` reste générique et évolutif ; son type vient de `PostType` et les objets partagés passent par `PostReference`, sans ajouter une colonne par objet.
- Une fiche Community publique ne rend pas ses discussions publiques. `Post.visibility` vaut `members_only` par défaut ; l'ouverture doit être explicite.
- `ReviewReaction` reste dédiée aux avis et continue d'alimenter le front existant. Les autres réactions utilisent `ContentReaction(scope_level, scope_id)` ; les scopes sont ouverts explicitement et leur cible est validée par le modèle applicatif.
- Le registre initial de `ContentReaction` couvre Post/commentaire, LocalHabit, LocalTip, OutingIdea, ElementNewsPost, izi_news_item, Event, Experience, Place, Shop, Page, Community, UserGroup, CommunityActivity, AnnualCelebration et EventSerie. Il est extensible sans modifier le schéma SQL.
- `ElementNewsPost` reste un contenu éditorial de fiche et `izi_news_item` une actualité territoriale/curatée. Aucun des deux n'est fusionné avec les discussions sociales.

## Agenda

- L'agenda d'une Community agrège ses propres `CommunityActivity`, Event et Experience liés.
- Une vue de synthèse peut aussi présenter les contenus publics/autorisés de ses groupes et de ses sous-communautés, sans changer leur propriétaire.
- L'agenda d'un groupe reste filtré sur ce groupe.

## Référence WhatsApp

WhatsApp sert uniquement de référence pour la séparation `Community / Annonces / Groupes / Agenda`. L'interface iziLife conserve le design Page/Place/Shop existant et son fonctionnement web desktop/mobile ; elle ne copie ni l'apparence d'une messagerie ni son chargement temps réel intégral.
