# Conversions Event / Expérience / EventSerie

## Écrans BO à ne pas confondre

- `Propositions Event / XP` (`partnerContentProposalReview`) instruit de nouveaux
  objets proposés par un Partner. L'acceptation publie la proposition ; elle ne
  change pas la nature d'un objet existant.
- `Propositions EventSeries` (`eventSerieReview`) instruit les nouvelles séries
  proposées par les Partners.
- `Modifications avec réservations` (`partnerContentChangeReview`) traite les
  changements sur un Event ou une Expérience existante, notamment lorsqu'une
  réservation ou une vente impose une revue financière.
- `Conversions de type Event / XP / Série` (`objectConversion`) transforme un
  objet existant créé sous la mauvaise nature.

## Workflow de conversion

1. L'employé choisit la source, le type cible, les références nécessaires et un
   motif. La demande est créée sans modifier la source.
2. Un autre employé approuve ou rejette la demande. Le demandeur ne peut pas
   approuver sa propre demande.
3. L'approbation crée une cible inactive ou avec le statut repris par le modèle,
   mais ne purge pas encore la source.
4. Un employé autorisé contrôle la cible, coche la confirmation de purge et
   exécute la conversion.
5. Dans une même transaction, le BO transfère médias, EAP et pivots éditoriaux,
   supprime la source, puis marque la demande `EXECUTED`.

Une erreur annule la transaction et place la demande en `FAILED`. Un Event ou
une Expérience portant des réservations ou tickets ne peut pas être purgé par ce
parcours. Une EventSerie portant déjà des éditions n'est pas purgée
automatiquement.

Le comportement de suppression est volontaire pour ce workflow BO de correction
au démarrage : il traite une mauvaise saisie Partner avant exploitation réelle.
Le moteur agent Place/Shop suit une autre règle et conserve sa source désactivée
pour l'audit.

## Couverture locale du 1er novembre 2026

Trois fixtures `TEST-CODEX` ont été créées, approuvées dans le vrai écran BO,
puis exécutées avec les méthodes réelles du contrôleur :

- Event → Expérience ;
- Expérience → Event ;
- Event récurrent → EventSerie.

Pour les trois cas, le statut final était `EXECUTED`, la source avait disparu,
la cible existait et son pivot média contenait exactement une relation. Les
sources, cibles, demandes, événements d'audit et la commande temporaire de test
ont ensuite été supprimés. La base locale ne conserve aucune fixture
`TEST-CODEX` de ce test.

Le test permanent
`tests/ObjectConversionWorkflowSourceContractTest.php` verrouille les routes
POST, les permissions, la séparation demandeur/approbateur, la confirmation
explicite, l'ordre transfert → purge → `EXECUTED`, le rollback et les tables de
médias des trois familles. La page est protégée par `adminauth` et les trois
mutations par `adminauthcsrf`, en plus des contrôles de permissions du
contrôleur.

## Livraison et test staging

Après livraison d'`izilife-admin`, créer uniquement des fixtures désactivées et
sans réservation, refaire les trois conversions, vérifier les médias et nettoyer
les fixtures. Ne jamais utiliser un Event ou une Expérience commerciale réelle
pour un smoke test.

