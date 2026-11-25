# Agents 5 — file post-livraison

Cette liste regroupe les opérations à poursuivre après confirmation de la livraison en staging/production. Elle ne vaut pas autorisation d'écriture en production en dehors des opérations déjà demandées.

## État du code

- Déjà livré et exploité : résolution de `category_string_id`, correction du champ principal des médias Experience et rendu FO Services/EAP Cryotera.
- Prêt localement mais **à livrer dans `izilife-admin`** : résolution globale des collisions de `string_id` Place/Shop, y compris les variantes déterministes basées sur `City.string_id` et `in_on_place`.
- Prêt dans les scripts locaux : `createur_lieux.py` accepte `IN_ON_PLACE_REF` sous forme de `Place.string_id`.
- Prêts localement mais **à livrer dans `izilife-admin`** : transfert générique
  Place/Shop (`LocationTypeTransfer`), rapprochement territorial avant LLM
  (`EventDiscovery`) et leurs routes agent authentifiées.
- Prêts dans les scripts locaux : opérateur Place/Shop, collecteur territorial
  JDS/InfoLocale et améliorateur intelligent avec analyse par défaut et écriture
  uniquement sous double confirmation.

## À exécuter ou vérifier après livraison

1. Régénérer l'inventaire Aushopping V2/Lillenium avec la règle de ville et de contenant, puis traiter les commerces encore absents, probables ou ambigus après validation.

## Opérations terminées

- LaM production : la fiche cible `lam-lille-metropole-musee-d-art-moderne-d-art-contemporain-et-d-art-brut` a conservé ses dix médias et ses pointeurs image. Sa description longue a été complétée depuis l'ancienne fiche et ses `PrincipalCharacteristics` ont été enrichies sans supprimer ses valeurs. L'ancienne fiche `lam-lille-metreopole-musee-dart-moderne` est inactive et non listable. Aucun média, fichier de bucket ni Google Place ID n'a été déplacé.
- Cryotera : Services, EAP, images et affichage FO finalisés.
- Forum des Sciences : les treize expériences, leurs EAP et leurs images principales sont finalisés.
- Aushopping V2 : conversion Shop vers Place appliquée en production. La Place est active/listable avec ses onze médias ; l'ancien Shop est purgé, inactif et non listable.
- Centres commerciaux : vingt Shops confirmés ont été rattachés à Aushopping V2 et un Shop confirmé à Lillenium. Les correspondances ambiguës ou situées dans une autre ville n'ont pas été modifiées.
- `createur_lieux` : Ripaille (`SHOP ripaille`, Marcq-en-Barœul) et Le Fresnoy (`PLACE le-fresnoy-studio-national-des-arts-contemporains`, Tourcoing) sont créés, actifs, visibles au FO et portent leur image principale.

## Chantiers suivants

- Collecteurs spécialisés JDS, InfoLocale et Ma Vie Lilloise : moteur développé et testé
  unitairement et sur JDS, InfoLocale et Ma Vie Lilloise en lecture seule ; il reste à livrer
  la route de rapprochement, puis à exécuter un premier inventaire staging sans
  envoi LLM. Voir `AGREGATEURS_EVENTS_JDS_INFOLOCALE.md`.
- Agent générique d'extraction de sites complexes vers JSON normalisé et import Scraper.
- Centres commerciaux : poursuivre la validation des commerces absents, probables ou ambigus. Leur création reste interdite sans confirmation. Lillenium est déjà une Place et ne nécessite pas de conversion.
- Transfert transactionnel et journalisé Place/Shop : les six directions
  (création ou fusion) ont été testées localement, ainsi que l'idempotence, les
  médias, les liens et la purge logique. Il reste à livrer puis à valider un plan
  staging sur une fiche désactivée avant tout nouvel apply distant. Voir
  `TRANSFERT_SHOP_VERS_PLACE.md`.
- Améliorateur intelligent avec preuves et sortie JSON déterministe : V0
  développée et testée sur Cryotera en lecture seule. L'application déterministe
  a aussi été testée localement sur une fixture : premier passage créateur,
  second passage sans changement, puis fixture supprimée. Aucun appel IA payant
  n'a été effectué. Voir
  `AMELIORATEUR_INTELLIGENT.md`.
- BO conversions Event / XP / EventSerie : les trois parcours ont été approuvés
  puis exécutés localement sur des fixtures `TEST-CODEX`. Les sources ont été
  purgées après transfert, chaque média est arrivé une seule fois sur la cible,
  les statuts sont passés à `EXECUTED`, puis toutes les fixtures et journaux de
  test ont été supprimés. Les libellés BO distinguent maintenant proposition,
  modification avec réservations et conversion de type ; les routes sont
  explicitement protégées par authentification et CSRF. Voir
  `CONVERSIONS_EVENT_XP_SERIE.md`.

