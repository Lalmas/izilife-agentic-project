# Partner Space Controller Inventory

Projet scanne: `C:/xampp/htdocs/izilife-partner-admin`

Regle de scan:

- `PARTNER_SPACE`: contient `partner_employee` ou `partner_logged_in`, sans marqueur BO.
- `BO_LEGACY`: contient `employee/logged_in` ou redirections BO, sans marqueur partner.
- `MIXTE`: contient les deux familles.
- `NEUTRE`: aucun marqueur session detecte.

Important: aucun `.env` n'a ete ouvert.

> Mise a jour du 15 aout 2026 : cet inventaire conserve l'historique du nettoyage de juin, mais son comptage n'est plus l'etat courant du repertoire. Des controllers et vues ont depuis ete recopies pour les chantiers suivants et l'autorouting est de nouveau actif. Ne pas utiliser les listes quantitatives ci-dessous comme une validation de securite actuelle.

## Etat courant valide : socle Place / Shop

- `Place.php` est reduit aux listes, affichages scopes, modification des champs autorises et horaires habituels/exceptionnels.
- `Shop.php` est reduit aux affichages scopes, modification des champs autorises et horaires habituels/exceptionnels.
- `Media.php`, `Offer.php` et `ScopedElement.php` protegent chaque mutation par session Partner et appartenance `partner_id` de la cible.
- Les vues Place/Shop actives ne chargent plus la pile de modales ni les requetes du BO.
- Les actions Google, produits, equipements, attractions, services, news et autres parcours non MVP ne sont plus rendues dans ces fiches.
- L'oeil de la liste ouvre la derniere section consultee et l'ancre de son bloc.
- Les routes de mutation de ce socle sont des routes POST generees par l'autorouting ameliore ; le retrait d'un media n'existe plus en GET.
- L'autorouting reste un risque transversal pour les autres controllers recopies. Chaque prochain chantier doit reduire son controller avant de considerer l'objet expose au Partner.

## Constat critique

`app/Config/Routing.php` contient:

```php
public bool $autoRoute = true;
```

Donc meme si `app/Config/Routes.php` expose peu de routes explicites, les controllers presents dans `app/Controllers` peuvent etre accessibles par autorouting.

Routes explicites actuellement vues:

- `/` -> `Welcome::getIndex`
- `stripecallback/stripe/partner/*` -> `StripeCallback`
- `stripecallback/stripe/place/*` -> `StripeCallback`
- `stripecallback/stripe/shop/*` -> `StripeCallback`
- `psp/onboarding/*` -> `PspOnboarding`

## Synthese

- `PARTNER_SPACE`: 1 controller
- `MIXTE`: 4 controllers
- `BO_LEGACY`: 29 controllers
- `NEUTRE`: 4 controllers

## Controllers Partner Space

- `Welcome.php`

## Controllers Mixtes

Ces fichiers contiennent deja du `partner_employee/partner_logged_in`, mais gardent aussi des restes BO.

- `Employee.php`
- `Exploitation.php`
- `Partner.php`
- `PspOnboarding.php`

## Controllers BO Legacy

Ces fichiers utilisent encore `employee/logged_in`, `employee/connexion` ou equivalent BO, sans marqueur partner.

- `Art.php`
- `Booking.php`
- `Campain.php`
- `Circuit.php`
- `City.php`
- `Configuration.php`
- `ContentProgram.php`
- `Country.php`
- `CronScript.php`
- `Equipment.php`
- `Event.php`
- `Experience.php`
- `Home.php`
- `Newsletter.php`
- `Numbers.php`
- `Page.php`
- `Place.php`
- `Product.php`
- `Question.php`
- `Representation.php`
- `Scraper.php`
- `Search.php`
- `Session.php`
- `Shop.php`
- `StripeCallback.php`
- `Transaction.php`
- `User.php`
- `Util.php`
- `Warehouse.php`

Note: `StripeCallback.php` est BO_LEGACY au scan mais il est explicitement route par `Routes.php`; il doit etre traite a part.

## Controllers Neutres

Ces fichiers n'ont pas de marqueur session detecte, mais restent accessibles si l'autorouting reste actif.

- `BaseController.php`
- `DataInsert.php`
- `Location.php`
- `Script.php`

Note: `BaseController.php` est structurel et ne doit pas etre archive comme un controller legacy ordinaire.

## Premiere action de nettoyage logique

Pour rendre le projet clean sans perte immediate:

1. Desactiver l'autorouting dans `app/Config/Routing.php`.
2. Mettre hors de `app/Controllers` les controllers BO legacy non explicitement routes.
3. Garder temporairement:
   - `BaseController.php`
   - `Welcome.php`
   - `Employee.php`
   - `Partner.php`
   - `PspOnboarding.php`
   - `StripeCallback.php`
4. Traiter ensuite les mixtes un par un pour enlever les restes `employee/logged_in`.

## Etat apres nettoyage du 2026-06-29

Action effectuee:

- `app/Config/Routing.php`: `public bool $autoRoute = false;`
- 31 controllers ont ete deplaces vers:
  - `C:/xampp/htdocs/izilife-partner-admin/_legacy_bo_controllers_2026-06-29`

Controllers restant dans `app/Controllers`:

- `BaseController.php`
- `Employee.php`
- `Exploitation.php`
- `Partner.php`
- `PspOnboarding.php`
- `StripeCallback.php`
- `Welcome.php`

Classement apres nettoyage:

- `PARTNER_SPACE`: `Welcome.php`
- `MIXTE`: `Employee.php`, `Exploitation.php`, `Partner.php`, `PspOnboarding.php`
- `BO_LEGACY` conserve car explicitement route: `StripeCallback.php`
- `NEUTRE`: `BaseController.php`

Restes BO detectes dans les fichiers conserves:

- `Employee.php`: references a `employee`/roles BO autour de certaines methodes de gestion historique.
- `Exploitation.php`: contient encore plusieurs gardes `employee/logged_in`; non route explicitement.
- `Partner.php`: reste une reference `Employee_model`.
- `PspOnboarding.php`: `launch/open/status` utilisent le guard partner, mais `setCurrent/deactivate` utilisent encore le guard BO et redirigent vers `employee/connexion`.
- `StripeCallback.php`: conserve car route par `Routes.php`; a relire separement.

## Etat apres nettoyage Models / Views du 2026-06-29

Action effectuee:

- 19 models non instancies par les controllers actifs ont ete deplaces vers:
  - `C:/xampp/htdocs/izilife-partner-admin/_legacy_bo_models_2026-06-29`
- 259 fichiers de vues BO ont ete deplaces vers:
  - `C:/xampp/htdocs/izilife-partner-admin/_legacy_bo_views_2026-06-29`

Models restants dans `app/Models`:

- `Category_model.php`
- `ContentProgram_model.php`
- `Country_model.php`
- `Employee_model.php`
- `Partner_model.php`
- `Place_model.php`
- `PspAccount_model.php`
- `PspEventLog_model.php`
- `Shop_model.php`
- `User_model.php`
- `Utils_model.php`
- `Validation_model.php`

Racine active de `app/Views`:

- `2fa_code_choose.php`
- `choose_password.php`
- `common_components`
- `emails`
- `employees`
- `errors`
- `exploitation`
- `layouts`
- `onboarding_validation_message.php`
- `partner_space_some_js_scripts.php`
- `partners`
- `psp`
- `psp_onboarding_feedback.php`
- `reset_password_choose.php`
- `reset_password_login_check.php`
- `sign_in.php`
- `user`

Deux vues minimales ont ete ajoutees pour supprimer des erreurs de vue manquante deja presentes:

- `app/Views/partners/partner_resume_home.php`: appelee par `Partner::getIndex()`.
- `app/Views/user/edit.php`: fallback legacy appele par une branche restante de `Employee.php`.

Verification:

- `NO_MISSING_MODELS`
- `NO_MISSING_VIEWS`
