# Incident BO production — agrégations Analytics

Le BO de production ne pouvait plus initialiser correctement les sessions. L'erreur visible dans `BaseHandler::fail()` sur `ini_set(session.save_path)` était secondaire.

`SHOW FULL PROCESSLIST` a révélé plusieurs requêtes issues de `Analytics_model` actives depuis plusieurs centaines à plusieurs centaines de milliers de secondes. Le calcul `COUNT(DISTINCT ...)` utilisait une sous-requête corrélée vers `UserUuid` pour chaque ligne de `user_events`. La série principale était également exécutée deux fois par chargement du dashboard.

Corrections retenues :

- identité statistique calculée depuis `user_id`, `cust_uniq_id` ou `session_id` déjà persistés ;
- suppression de la sous-requête corrélée `UserUuid` ;
- calcul de la série une seule fois, partagé entre `series` et `daily` ;
- remplacement de `DATE(action_date) = CURDATE()` par une plage indexable ;
- ajout de l'index `idx_user_events_date_identity`.

`BlockServiceAccountFromHumanUi` déclenche la session en premier dans la pile, mais n'est pas l'origine des requêtes lentes. Le handler de session reste le handler SQL et aucune configuration FO/BO n'a été modifiée.
