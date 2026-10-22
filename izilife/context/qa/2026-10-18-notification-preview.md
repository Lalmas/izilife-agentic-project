# Aperçu QA des emails et SMS

## Comportement

- En production, l'interception, les routes et le composant visuel n'existent pas.
- En local/staging manuel, le message final est capturé avant SES/Twilio. L'écran suivant affiche le destinataire, l'objet et le contenu exact, puis propose **Ne pas envoyer** ou **Envoyer**.
- L'envoi réel non-production est limité à `IZILIFE_QA_NOTIFICATION_ALLOWLIST` (destinataires séparés par des virgules).
- En test automatisé, toute la préparation métier reste exécutée. L'OTP reste donc enregistré normalement et le vrai contenu construit est capturé, mais aucun transport externe et aucun modal ne sont déclenchés.

## Tests techniques

Une commande CLI utilise `IZILIFE_QA_NO_NOTIFICATIONS=1` et peut lire `QaNotificationRecorder::all()` dans son processus.

Un scénario Playwright envoie les en-têtes :

- `X-IziLife-QA-Mode: automated`
- `X-IziLife-QA-Run: <identifiant-du-run>`

Le serveur écrit alors chaque notification au format JSONL dans `writable/qa-notifications/<identifiant-du-run>.jsonl`. Ces fichiers sont temporaires et supprimés automatiquement après 24 heures.

La capture ne remplace jamais l'enregistrement métier du code de validation en base.

