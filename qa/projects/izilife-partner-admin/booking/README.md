# QA Partner Booking

Contrôler les droits Partner, la portée Place/Shop, BC/BCC, composition, politique d'acceptation, privatisation, publication/pause et consultation des réservations. Un Partner étranger doit recevoir un refus sans fuite de données.

Les scénarios PS de `qa/transverse/booking/browser-scenarios.json` constituent la procédure reproductible : création TABLE globale ou multicatégorie, BCC simple/composable, capacités, STANDARD, EQUIPMENT, privatisation, puis décision sur une demande. Chaque configuration doit être vérifiée à la fois dans l'interface et dans la base.
