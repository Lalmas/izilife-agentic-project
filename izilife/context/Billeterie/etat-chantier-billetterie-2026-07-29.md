# Billetterie, accès et avantages — état du chantier au 29 juillet 2026

## Modèle métier retenu

- Un EAP est un ticket ou droit d’accès. Le tarif libre Event utilise son formulaire propre et n’est pas un EAP.
- Un pack assemble au moins deux EAP simples distincts. Plusieurs exemplaires du même EAP relèvent du tarif groupé.
- La quantité d’un EAP est facultative : sans quantité, il consomme la capacité globale ; avec quantité, son quota propre est contrôlé en plus.
- Un pack ne crée pas de capacité et consomme ses composants via `access_price_real_ticket_quantity`.
- Event possède une capacité globale et un sold out calculé. Pause et clôture restent des décisions manuelles.
- Pour Experience, la capacité et le complet concernent le créneau ou l’occurrence, jamais toute l’Experience tant qu’un autre créneau est disponible.

## Event V2

`EventBookingHandler` est la source de vérité : recalcul du prix, tarifs groupés, packs, frais, capacité Event, quotas EAP, réservation gratuite sans PSP et verrou transactionnel.

Cas à valider manuellement avant mise en ligne : gratuit sur réservation, tarif libre, tarif libre minimum, EAP unitaire sans quota, EAP avec quota, tarif groupé, pack, pause, clôture et sold out calculé.

## Experience, Sessions et Booking

- `SessionConfiguration/SessionConfigurationContent` décrit le planning récurrent.
- `Session` représente une séance manuelle ou une exception matérialisée.
- `Booking` est la réservation réelle.
- EAP et le tunnel XP sont pilotés par `Experience.use_izilife_paiement` et `registration_state`, comme Event.
- Les XP existantes restent désactivées par défaut et une XP pilote doit être testée avant généralisation.

## Multi-catégorie

Le registre générique `ElementApplicationScope` a été retiré du modèle actif : il imposait une diffusion multiple à des éléments qui n’en ont pas besoin.

- EAP : fiche générale, toutes les catégories ou plusieurs catégories sélectionnées via ses liaisons dédiées.
- Hourly : un horaire global obligatoire comme repli, puis zéro ou une exception active par catégorie. Le FO n’affiche qu’un horaire lorsqu’il n’existe pas d’exception ; sinon il affiche le global et les exceptions par activité.
- Menu : appartient au lieu et, en gestion séparée, à une catégorie. La composition Menu ↔ ProductCategory reste à terminer dans le chantier Menu digital.
- Product et ElementService : général ou une catégorie métier.
- Offer : lieu entier ou une catégorie.
- BPR Plan : lieu entier ou catégories prévues par sa règle ; les autres BPR restent rattachées à leur Offer et à leurs cibles métier.

## Contraintes BPR et abonnement

Le BO BPR sait maintenant enregistrer dans `usage_constraints_json` :

- jours utilisables ;
- plusieurs plages horaires, globales ou par jours ;
- plages interdites ;
- heure limite ;
- mode de délivrance ;
- périmètre descriptif « Disponible pour : Restaurant | Bar ».

Une plage traversant minuit conserve le jour de service : lundi `17:00–02:00` autorise mardi 01:00 au titre du lundi. Les mêmes règles sont affichées sur les cartes/modal FO et appliquées par `BenefitEngine` à la redemption, y compris pour un code promotionnel externe.

Une heure limite du soir utilise une journée d’exploitation basculant à 06:00 par défaut : une limite à 23:00 reste donc dépassée à 00:30 et ne redevient disponible qu’au début de la journée d’exploitation suivante.

La preuve de réclamation reste utilisable une heure maximum. Le champ « Disponible pour » prépare le futur ciblage Menu/commande ; il est affiché mais ne bloque pas encore par catégorie tant que la redemption ne fournit pas de catégorie dans son contexte.

## Discipline de schéma

Les migrations de ce chantier et les chemins BPR touchés ne testent plus silencieusement l’existence de tables ou colonnes. Une base incomplète doit produire une erreur SQL visible pendant les tests.

## À ne pas déclarer terminé

- composition BO `ElementMenu` ↔ `ProductCategory` ;
- scope catégorie complet d’Offer et enforcement catégorie de BPR à la redemption ;
- validation navigateur de bout en bout de l’Experience pilote et de ses Sessions ;
- espace Partner et catalogue Partner, réservés à la conversation dédiée.
