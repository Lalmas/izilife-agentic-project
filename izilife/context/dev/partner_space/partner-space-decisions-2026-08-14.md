# Partner Space et outils operationnels - decisions actives

Date : 14 aout 2026

Ce document fixe les decisions produit et techniques applicables au lancement du chantier. Il prime sur les notes plus anciennes en cas de contradiction.

## 1. Perimetre de code

- Code a modifier en priorite : `C:/xampp/htdocs/izilife-partner-admin`.
- Front public de reference : `C:/xampp/htdocs/izilife`.
- BO de reference et de configuration avancee : `C:/xampp/htdocs/izilife-admin`.
- Ne jamais lire un fichier `.env` ou assimile.
- Ne jamais appliquer de CSS generique sur `nav`, navbar, modal ou autre composant transversal sans scope explicite par conteneur et chaine d'identifiants/classes propre a la page.
- Toute evolution SQL est ajoutee a la fin de `izilife-admin/statics/izilife_new_version/021_Next_Improves.sql` apres verification du schema existant.
- Le projet utilise l'auto-routing CodeIgniter ; ne pas le desactiver. Chaque methode accessible doit donc etre protegee explicitement.

## 2. Strategie de lancement Partner Space

Le lancement vise un espace minimal, propre et utilisable par de vrais clients. Il ne s'agit ni d'exposer le BO complet ni de finaliser tous les objets avant la V2.

Ordre actif :

1. Stabiliser les fiches separees Place et Shop.
2. Retirer les boutons et fonctions BO inutiles au Partner.
3. Brancher les controllers et models des fonctions conservees avec controles d'appartenance server-side.
4. Refaire les horaires sous forme d'un formulaire hebdomadaire unique pour ajout et modification.
5. Conserver un formulaire separe pour les horaires exceptionnels.
6. Corriger les modals, selectpicker et comportements client-ready avec CSS strictement scope.
7. Reprendre Event et Experience avec la meme logique de fiche par sections.
8. Stabiliser rapidement reservation et menu digital, qui sont des priorites commerciales.
9. Exposer progressivement produits, EAP, services et paiement lorsque leur socle BO est valide.

Le BO peut continuer a creer et configurer les objets complexes pendant la premiere phase. Le Partner les voit et ne modifie que les donnees dont le parcours est securise et valide.

## 3. Place, Shop et revendication

- Pour le MVP, aucune creation de Place depuis le Partner Space.
- Les Places sont creees en BO, par import Google ou saisie interne.
- Le Partner peut rechercher et reclamer une Place existante.
- La revendication est examinee et validee en BO avant rattachement.
- Une fois rattachee, la Place est visible dans le Partner Space et ses champs autorises peuvent etre geres.
- Shop et Place restent deux objets et deux fiches distinctes.
- Le scope MVP repose sur `partner_id`.
- Le scope futur couvrira Network, chaine, secteur, ville, lieu et autres perimetres multi-etablissements, mais ne bloque pas le lancement.

## 4. Event et Experience

- Les controllers BO Event et Experience ne sont pas exposes tels quels au Partner.
- Ils doivent etre repris par petits parcours, avec auth PartnerEmployee et controle d'appartenance pour chaque lecture et mutation.
- Les fiches Partner seront separees par sections comme Place/Shop.
- Le Partner pourra creer ou proposer des Events selon le workflow de validation retenu.
- Les parcours avances restent temporairement gerables en BO tant que leur version Partner n'est pas blindee.

## 5. Horaires

- Supprimer l'edition JSON visible et l'ajout ligne par ligne comme UX principale.
- Fournir un formulaire unique representant toute la semaine.
- Le meme formulaire gere creation et modification.
- Chaque jour gere fermeture, premiere plage, coupure facultative et seconde plage.
- Les horaires exceptionnels restent un ecran/formulaire distinct.
- Le format interne existant peut etre conserve si le model le demande, mais il ne doit pas apparaitre au commercant.

## 6. Partner, Stripe et versements

- Un Partner peut exister sans compte Stripe et sans donnees bancaires completes.
- Stripe n'est pas requis pour creer ou gerer Place rattachee, Shop, Event, Experience, produits, EAP, services ou reservations.
- Ne pas imposer l'onboarding financier avant qu'il soit utile.
- izilife peut demander directement les justificatifs et le RIB puis effectuer des versements manuels.
- Les circuits a distinguer sont : Stripe automatise, versement manuel izilife, paiement externe/TPE, gratuite et versement bloque en attente de validation.
- L'industrialisation de la conformite entreprise, du RIB et des versements viendra ensuite.

## 7. Lien de paiement generique

`IziPayPublicPaymentLink` doit evoluer comme un outil large proche d'un Stripe Payment Link, et non comme un objet reserve aux Events.

Cas a couvrir :

- montant fixe ou montant libre ;
- acompte ou service ponctuel ;
- liste facultative de produits, tarifs ou services ;
- destinataire connu ou paiement invite ;
- rattachement facultatif a Partner, Shop, Place, Event, Booking, commande, Product, EAP ou ElementService ;
- lien a usage unique ou reutilisable, avec expiration facultative.

Un paiement invite impose au moins un email ou un telephone. L'interface encourage la validation des deux. La creation d'un compte izilife ne doit pas etre obligatoire pour payer.

## 8. Identites humaines, comptes operationnels et appareils

Ne pas figer la nouvelle architecture sur les champs historiques `PartnerEmployee.is_service_account` et `service_account_type` simplement parce qu'ils existent. Rien n'etant encore branche, le schema peut etre refondu proprement.

Separation cible :

- `PartnerEmployee` : personne permanente ou temporaire, avec roles et permissions.
- Compte operationnel : identite limitee de scanner, caisse ou autre fonction, partageable si le contexte l'exige.
- Appareil : kiosk, terminal ou pad physique/logique, avec identite technique propre.
- Affectation : rattachement borne d'un compte ou appareil a un Partner, Shop, Place, Event ou fonction.
- Session : connexion concrete d'un navigateur/telephone/tablette.
- Journal : auteur humain ou compte operationnel, appareil/session, scope, action et date.

Les noms de tables definitifs seront choisis apres audit complet du schema avant tout ALTER/CREATE.

## 9. Kiosk

- Application web/PWA complete et separee du Partner Space.
- Le Partner Space configure ; le kiosk exploite le lieu en temps reel.
- Une identite technique unique est attribuee a chaque appareil et rattachee a un lieu/shop.
- Activation depuis le Partner Space avec QR ou code temporaire.
- L'appareil reste connecte durablement comme une tablette Deliveroo/Uber Eats.
- La persistance repose sur des jetons courts renouveles par une credencial d'appareil revocable, pas sur un mot de passe partage ou un cookie permanent illimite.
- Plusieurs personnes peuvent utiliser le kiosk pendant le service.
- Les actions courantes ne necessitent pas une reconnexion humaine permanente.
- Les actions sensibles exigent un PIN personnel, une reauthentification ou une validation superieure.
- Le Partner Space permet de suspendre/revoquer immediatement un appareil.
- Le kiosk n'accede jamais a l'administration complete du Partner.

## 10. Scanner et caisse Event

- Application web complete et separee du Partner Space.
- Le concept metier est un compte scanner, pas l'ajout d'un appareil scanner.
- Deux modes sont obligatoires : compte scanner operationnel partage et PartnerEmployee personnel avec permission scanner.
- Un compte scanner est cree au niveau du Partner puis affecte a un ou plusieurs Events ; une creation directement depuis l'Event peut preconfigurer cette affectation.
- Le compte peut etre reutilise sur de prochains Events sans obtenir automatiquement de nouveaux acces.
- La connexion du telephone par QR temporaire genere depuis le Partner Space est le parcours privilegie.
- Chaque telephone recoit une session distincte et revocable.
- L'autorisation Event expire automatiquement apres une marge configurable.
- Le scanner ne voit ni statistiques, ni donnees financieres globales, ni configuration Partner/Event.

Fonctions operationnelles :

- scanner et valider un ticket ;
- rechercher manuellement une inscription ;
- identifier un billet deja utilise, annule ou invalide ;
- creer une inscription sur place ;
- enregistrer un paiement realise sur TPE externe ;
- generer et envoyer un lien de paiement izilife ;
- rattacher l'achat a un compte izilife existant ou permettre un paiement invite.

## 11. Securite minimale non negociable

- Autorisation verifiee cote serveur pour chaque objet et chaque mutation.
- Refus par defaut hors scope.
- Aucun secret Partner partage avec un benevole ou stocke dans un QR durable.
- QR d'activation a usage unique, fortement aleatoire, expire rapidement et limite en tentatives.
- Une session par appareil/navigateur, jamais un meme token copie sur plusieurs telephones.
- Rotation et revocation des sessions et credencials d'appareil.
- Journalisation des scans, ventes, annulations, remboursements, changements de disponibilite et actions sensibles.
- Donnees personnelles minimales dans les interfaces operationnelles.
- Aucune statistique dans le scanner.

## 12. Socle Place / Shop cloture le 15 aout 2026

Le premier workflow Partner Place/Shop est considere branche pour le perimetre MVP suivant :

- liste unique des Places et Shops rattaches au `partner_id` connecte ;
- fiches distinctes et URLs distinctes ;
- sections Informations, Dates et horaires, Medias, Offres et promotions, Liens ;
- oeil depuis la liste ouvrant la derniere section consultee pour l'objet ;
- ancre de section et bloc automatiquement ouvert sur la fiche ;
- modification des champs Partner autorises ;
- formulaire hebdomadaire unique pour creation et modification des horaires ;
- ajout, modification et suppression des horaires exceptionnels ;
- gestion limitee d'images avec controles techniques communs ;
- offres et liens scopes a l'objet et au Partner ;
- filtrage des liens commerciaux interdits, y compris apres resolution des raccourcisseurs ; Shotgun reste explicitement autorise ;
- aucune action Google, equipement, attraction, service, news, produit ou autre fonction BO dans ces vues MVP ;
- retrait d'un media uniquement en POST et redirections de retour limitees au domaine Partner.

La creation d'une Place reste hors Partner : revendication puis validation BO. Le prochain chantier fonctionnel est Event puis Experience. Les Annual Celebrations restent gerees en BO au premier passage.

## 13. Socle Event / Experience branche le 15 aout 2026

Le workflow Partner minimal Event/Experience reprend l'architecture validee pour Place/Shop :

- listes limitees aux objets appartenant directement au Partner, explicitement organises par lui ou accueillis dans ses Places/Shops ;
- distinction stricte entre droit de voir un objet accueilli et droit de le modifier ;
- modification reservee au Partner proprietaire ou a un organisateur explicite Partner/Place/Shop ;
- creation Event et Experience dans le Partner Space sans condition Stripe ;
- toute creation Partner est inactive et transmise au BO pour validation avant publication ;
- Event : sections Informations, Dates, Acces, Medias et Liens ;
- Experience : sections Informations, Acces, Medias et Liens ;
- annulation Event uniquement en POST ;
- maximum de deux images pour un Event et six pour une Experience ;
- couverture/principale synchronisee avec la fiche ;
- liens filtres par la protection commune contre les domaines interdits et leurs raccourcisseurs ;
- oeil de liste, derniere section consultee et ouverture automatique du bon bloc conserves ;
- toutes les mutations exposees par ces deux controllers sont en POST ;
- les anciennes methodes BO ne sont plus auto-routees depuis les controllers Event/Experience Partner.

Les Events recurrents existants sont visibles dans ce socle, mais la configuration de recurrence n'est pas exposee dans le MVP afin de ne pas importer le workflow BO complexe sans validation metier. Les Annual Celebrations restent gerees en BO au premier passage.

## 14. Pages, profils et transactions

La frontiere cible reste a valider lors du chantier Page :

- le FO peut porter une edition legere du profil public par son proprietaire ;
- le Partner Space devient obligatoire des qu'il existe une equipe, des permissions, un Event gere, un encaissement, un lien de tipping/paiement ou une activite commerciale ;
- ne pas imposer maintenant une limite d'un seul `PartnerEmployee` aux Pages Artiste/DJ : managers, agences et delegations rendent cette regle trop rigide ;
- la bonne contrainte devra venir de roles/scopes et eventuellement du plan Partner, apres audit Page/PartnerEmployee.

## 15. Vague fonctionnelle suivante

Apres validation manuelle du socle Place/Shop/Event/Experience :

- blinder et finaliser en BO les Produits, EAP, Services, tarifs et configurations de reservation avant ouverture de leur creation Partner ;
- permettre d'abord au Partner de consulter les objets prepares et valides en BO ;
- menu digital et suivi catalogue/produits ;
- reservations, privatisations, BCC, SCC, sessions manuelles et equipements reservables ;
- liens de paiement et tipping generiques ;
- abonnement Partner et activation progressive des fonctions ;
- applications separees kiosk et scanner/caisse Event ;
- integration operationnelle future des MeetZ et Selections au kiosk.
