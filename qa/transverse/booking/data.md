# Booking QA — données et règles

Le profil réel est `local.json`, ignoré par Git. Il résout toujours les objets par nom, référence publique ou e-mail avant de mémoriser leurs IDs locaux. Aucun ID local ne doit entrer dans un scénario partagé.

Les mutations QA utilisent un `run_id` de forme `booking-qa-YYYYMMDD-HHMMSS-<suffixe>`. Le nettoyage ne cible que les lignes portant ce marqueur ou leurs relations explicitement inventoriées.

La réservation TABLE/STANDARD/SERVICE/EQUIPMENT créée dans ce chantier est actuellement gratuite et n'appelle pas PayHub. Les tests Stripe, PSP et IziCredits ne deviennent applicables qu'après raccordement explicite de Booking au paiement. Ils ne doivent pas être validés par les anciens parcours Event, Experience ou Meetz.

Les émissions SMS/e-mail sont des effets externes. Les tests techniques vérifient la création d'`AccountValidation`, le canal choisi, le fallback et le contenu ; la réception réelle reste une validation manuelle.
