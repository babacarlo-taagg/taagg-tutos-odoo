# Parcours « Consultant technique Odoo » — TAAGG School

Suivi du contenu des 5 blocs techniques du programme 10 (taagg-school.com).
Statut : programme **validé par Babacar le 21/11/2026** (fil rouge Baobab Livraison conservé). Bloc 1 rédigé, en brouillon sur le site, à relire.

## Repères

| Bloc | Cours | Sections déjà en ligne (vides) |
|---|---|---|
| 1 — Les fondations | 208 | 2698 Semaine 0 · 2700 Linux · 2702 Python · 2705 Bases de données · 2707 Git et environnement · 2711 Évaluation |
| 2 — Framework (backend) | 209 | 2714 Module · 2717 ORM · 2721 Logique métier · 2725 Héritage · 2728 Données · 2731 Tests · 2733 Évaluation |
| 3 — Interface et rapports | 210 | 2736 Vues · 2739 Rapports · 2741 Interface web · 2744 Évaluation |
| 4 — Intégrations et sécurité | 211 | 2747 API · 2750 Paiement mobile · 2752 Sécurité · 2755 Évaluation |
| 5 — Déploiement | 212 | 2758 Travailler proprement · 2761 Mettre en production · 2767 Surveiller · 2769 Projet tutoré · 2774 Évaluation |

**État trouvé le 21/11/2026.** Les cours ne sont pas vides : un squelette existe déjà (créé le 06/11/2026).
- Les sections sont publiées (donc potentiellement visibles), les leçons sont toutes en brouillon.
- Les leçons « article » contiennent seulement un objectif et « Contenu à préparer par le formateur TAAGG ».
- Les anciennes fiches « document » (1352 à 1363, créées le 08/10/2026) n'ont pas de texte.
- Chaque bloc a déjà un « Travail à rendre » et un grand quiz de fin de bloc (15 à 25 questions écrites).
- Le fil rouge choisi dans ce squelette est **Baobab Livraison** (module `baobab_livraison`).

**Méthode (validée).** On garde les sections existantes (pas de changement visible). On **remplit** les leçons
brouillon existantes (repère `♻ id`) et on **crée** les leçons manquantes (repère `＋`). Chaque leçon = une fiche
« article » d'environ 10 minutes : explication, code commenté, exercice, « À retenir », et 3 questions de quiz.
🎥 = leçon qui gagnerait à avoir une vidéo plus tard.

## Fil rouge : Baobab Livraison

Une petite société fictive de livraison à moto à Dakar. Les apprenants construisent son module Odoo de bloc en bloc :
- **Bloc 1** : un dépôt Git `baobab_livraison`, un script Python qui calcule le prix d'une course selon la zone, une base Odoo 20 qui tourne sur leur ordinateur.
- **Bloc 2** : le module : les courses (`baobab.course`), les zones et leurs tarifs (`baobab.zone`), les livreurs (contacts enrichis), les statuts, les calculs, le lien avec les ventes.
- **Bloc 3** : les écrans (formulaire, liste, kanban des courses), le bordereau PDF, la page « Suivre mon colis ».
- **Bloc 4** : l'API pour l'appli des livreurs, un paiement mobile simulé, les droits (un livreur ne voit que ses courses).
- **Bloc 5** : tests automatiques, mise en production avec Docker, sauvegardes, surveillance.

## Version enseignée et points de vigilance (vérifiés)

On enseigne **Odoo 20 Community** (version de la base TAAGG). Chaque leçon concernée porte un encadré
« Selon ta version » pour les clients restés en 18 ou 19. Points vérifiés le 21/11/2026 dans la documentation
officielle (odoo.com/documentation, pages 19.0 et master) et dans le code Odoo 20 de TAAGG :

| Sujet | Odoo 18 | Odoo 19 | Odoo 20 | Source |
|---|---|---|---|---|
| Droits d'accès | `security/ir.model.access.csv` (perm_read…) + `ir.rule` | idem | `security/ir.access.csv`, modèle `ir.access`, colonnes `id,name,model_id,group_id/id,operation,domain` : droits et règles réunis (introduit en Online 19.4) | tutoriel Server Framework 101 ch. 4 (19.0 et master) ; changelog ORM master ; base TAAGG |
| Paramètres système | `get_param` | `get_param` | `get_str` / `get_int` (nouvelle API en Online 19.1) | changelog ORM ; code TAAGG |
| API externe | XML-RPC / JSON-RPC | + API **JSON-2** (`/json/2/<modèle>/<méthode>`, clé d'API en `bearer`), nouvelle en 19.0 | XML-RPC / JSON-RPC dépréciés ; service `db` retiré en 20 ; `common` et `object` retirés prévus en Odoo 22 | page External API (19.0 et master) |
| Contrôleurs JSON | `type='json'` renommé `type='jsonrpc'` (Online 18.1) | `jsonrpc` | `jsonrpc` | changelog ORM |
| Contraintes | `_sql_constraints` → contraintes et index déclarés comme attributs du modèle (Online 18.1) | idem | idem | changelog ORM |
| Regroupements | `read_group` déprécié (18.2) → `_read_group` / `formatted_read_group` | idem | idem | changelog ORM |
| Raccourcis | — | `record._cr`, `_context`, `_uid` dépréciés → `env.cr`, `env.context`, `env.uid` | idem ; `request` retiré du code des modèles, `env.website` (Online 19.4) | changelog ORM |
| Données de démo | plus chargées par défaut (Online 18.3) | idem | idem | changelog ORM |
| Vues | `<list>` et `<chatter/>` ; plus de `attrs` (`invisible="…"` directement) | idem | idem | page View architectures (master) |
| Champs binaires | base64 | base64 | `BinaryValue` (Online 19.3, 20.0) | changelog ORM |
| Python / PostgreSQL | — | Python ≥ 3.10, PostgreSQL ≥ 13 | Python ≥ 3.12, PostgreSQL ≥ 16 | page Installation depuis les sources (19.0 et master) |

À vérifier au moment d'écrire les leçons concernées (pas encore lu) : moteur de rapports PDF en 20
(« modularize reporting engines / paper-muncher », Online 19.4), OWL (version et syntaxe), Odoo.sh, image Docker officielle.
Règle : aucun code dans une fiche sans l'avoir fait tourner sur un Odoo 20 de test.

---

## Bloc 1 — Les fondations (cours 208)

Objectif du bloc : avoir un poste de travail prêt et les bases pour lire et écrire du code Odoo.

### Section « Semaine 0 — Remise à niveau Python (facultatif) » (2698)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 1.0.1 | Bienvenue : le parcours, Baobab Livraison et ta méthode de travail | Savoir ce que tu vas construire et comment t'organiser | ✅ 2894 |
| 1.0.2 | Installer Python et écrire ton premier script | Lancer un script `.py` dans le terminal | ✅ 2699 🎥 |
| 1.0.3 | Variables, nombres et textes | Calculer un prix et afficher un message | ✅ 2895 |
| 1.0.4 | Listes et dictionnaires | Ranger les zones de livraison et leurs tarifs | ✅ 2896 |
| 1.0.5 | Conditions et boucles | Appliquer un tarif selon la zone, parcourir des courses | ✅ 2897 |
| 1.0.6 | Les fonctions | Écrire `prix_course(zone, poids)` réutilisable | ✅ 2898 |

### Section « Linux et le terminal » (2700)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 1.1.1 | Pourquoi Linux ? Installer Ubuntu ou WSL sous Windows | Avoir un terminal Linux qui marche | ✅ 1353 🎥 |
| 1.1.2 | Se déplacer et manipuler des fichiers | `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm` sans peur | ✅ 2701 |
| 1.1.3 | Chercher et lire : `cat`, `less`, `grep`, `tail -f` | Retrouver une erreur dans un journal | ✅ 2899 |
| 1.1.4 | Utilisateurs, droits, `sudo` et paquets `apt` | Installer un logiciel, comprendre « Permission denied » | ✅ 2900 |
| 1.1.5 | Processus et ports | Régler « le port 8069 est déjà utilisé » | ✅ 2901 |

### Section « Python pour Odoo » (2702)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 1.2.1 | Environnement virtuel et `pip` | Isoler les dépendances d'un projet | ✅ 2902 |
| 1.2.2 | Classes et objets | Lire `class Course(models.Model)` et comprendre `self` | ✅ 1352 |
| 1.2.3 | Héritage de classes et `super()` | Comprendre ce que fera `_inherit` | ✅ 2903 |
| 1.2.4 | Ce qu'Odoo utilise partout : décorateurs, compréhensions, `*args`/`**kwargs` | Lire `@api.depends(...)` sans être perdu | ✅ 2904 |
| 1.2.5 | Dates, nombres et texte (fuseau de Dakar, F CFA, accents) | Éviter les erreurs classiques de dates et d'arrondis | ✅ 2703 |
| 1.2.6 | Les erreurs et le débogage | Lire une trace d'erreur, utiliser `pdb` | ✅ 2704 🎥 |

### Section « Les bases de données » (2705)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 1.3.1 | Installer PostgreSQL, créer un utilisateur et une base | Se connecter avec `psql` | ✅ 2905 🎥 |
| 1.3.2 | Lire des données : `SELECT`, `WHERE`, `ORDER BY` | Interroger une table de courses | ✅ 1354 |
| 1.3.3 | Écrire et relier : `INSERT`, `UPDATE`, `DELETE`, jointures | Relier courses et zones | ✅ 2906 |
| 1.3.4 | Comment Odoo range ses données | Retrouver un modèle Odoo dans PostgreSQL (lecture seule !) | ✅ 2706 |

### Section « Git et l'environnement » (2707)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 1.4.1 | Git : dépôt, commit, historique | Créer le dépôt `baobab_livraison` et faire ses premiers commits | ✅ 2708 🎥 |
| 1.4.2 | Branches et fusion | Travailler sur une branche sans casser le reste | ✅ 2907 |
| 1.4.3 | GitHub : envoyer, récupérer, demande de fusion, `.gitignore` | Publier son dépôt sans jamais y mettre de mot de passe | ✅ 2908 |
| 1.4.4 | Installer Odoo 20 Community depuis les sources | Avoir Odoo qui démarre sur ton ordinateur | ✅ 2709 🎥 |
| 1.4.5 | Variante : Odoo avec Docker | Lancer Odoo + PostgreSQL avec `docker compose` | ✅ 2909 🎥 |
| 1.4.6 | Lancer Odoo : fichier de configuration, base de test, mode développeur, journaux | Démarrer, créer une base, activer le mode développeur | ✅ 2710 |
| 1.4.7 | L'éditeur de code : VS Code et son débogueur | Mettre un point d'arrêt dans Odoo | ✅ 2910 🎥 |

### Section « Évaluation » (2711)
- ♻ 2712 Travail à rendre : le dépôt Baobab Livraison et le script de tarifs (à rédiger)
- ♻ 2713 Quiz : les fondations (20 questions existantes, à relire et ajuster au contenu)

## Bloc 2 — Architecture du framework (cours 209)

Objectif : un module `baobab_livraison` installable, avec ses modèles, ses calculs et son lien avec les ventes.

### « Le module » (2714)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 2.1.1 | Anatomie d'un module | Reconnaître chaque dossier et fichier | ♻ 2715 |
| 2.1.2 | Le manifeste ligne par ligne | Écrire `__manifest__.py` (version, dépendances, data, démo, licence) | ＋ |
| 2.1.3 | Créer `baobab_livraison` et l'installer | Voir son module dans Applications | ♻ 2716 🎥 |
| 2.1.4 | Mettre à jour un module : quand redémarrer, quand faire `-u` | Ne plus se demander pourquoi « ça ne change pas » | ＋ |

### « Le modèle (ORM) » (2717)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 2.2.1 | Premier modèle : `baobab.course` | `_name`, `_description`, premiers champs | ♻ 1355 |
| 2.2.2 | Les types de champs | Char, Text, Integer, Float, Monetary, Date, Datetime, Boolean, Selection | ＋ |
| 2.2.3 | Les relations : Many2one, One2many, Many2many | Relier courses, zones et livreurs | ＋ |
| 2.2.4 | Le droit minimum pour voir son modèle | Premier `ir.access.csv` (20) / `ir.model.access.csv` (18-19) | ＋ |
| 2.2.5 | Chercher, créer, modifier : `search`, `create`, `write`, domaines | Manipuler les courses depuis le shell Odoo | ♻ 2718 🎥 |
| 2.2.6 | Les recordsets : boucles, `mapped`, `filtered`, `sorted` | Travailler sur plusieurs fiches d'un coup | ＋ |
| 2.2.7 | Champs calculés, liés et enregistrés | Calculer le prix d'une course | ♻ 2719 |
| 2.2.8 | Contraintes et valeurs par défaut | Interdire un poids négatif (`models.Constraint`, `@api.constrains`) | ♻ 2720 |

### « La logique métier » (2721)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 2.3.1 | Statuts et boutons d'action | Brouillon → en route → livrée, avec des méthodes `action_…` | ♻ 1356 |
| 2.3.2 | Les onchange | Proposer le tarif dès qu'on choisit la zone | ♻ 2722 |
| 2.3.3 | Séquences et actions planifiées | Numéroter les courses, relancer les courses en retard | ＋ |
| 2.3.4 | Contexte, utilisateur, société et `sudo` | Savoir qui agit et avec quels droits | ♻ 2723 |
| 2.3.5 | Discussion, activités et suivi des changements | Ajouter le chatter aux courses | ♻ 2724 |

### « L'héritage » (2725)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 2.4.1 | `_inherit` : ajouter un champ à un modèle existant | Marquer un contact comme livreur | ♻ 1357 |
| 2.4.2 | Surcharger une méthode avec `super()` | Ajouter une règle à `create` sans casser Odoo | ＋ |
| 2.4.3 | Héritage par délégation et mixins | Savoir quand utiliser `_inherits` et `mail.thread` | ♻ 2726 |
| 2.4.4 | Étendre les ventes | Une commande confirmée crée une course | ♻ 2727 |

### « Les données » (2728)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 2.5.1 | Fichiers de données XML et CSV, identifiants externes | Charger les zones de Dakar avec le module | ♻ 2729 |
| 2.5.2 | Données de démonstration et `noupdate` | Préparer une base de test réaliste | ＋ |
| 2.5.3 | Scripts de migration du module (pré et post) | Changer un champ sans perdre les données | ♻ 2730 |

### « Les tests » (2731)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 2.6.1 | Écrire un premier test | Vérifier le calcul du prix avec `TransactionCase` | ♻ 2732 |
| 2.6.2 | Lancer ses tests et lire le résultat | `--test-tags`, comprendre un test qui échoue | ＋ |

### « Évaluation » (2733) : ♻ 2734 travail à rendre · ♻ 2735 quiz (25 questions existantes à relire)

## Bloc 3 — Interface et rapports (cours 210)

Objectif : des écrans clairs, un bordereau PDF et une page web « Suivre mon colis ».

### « Les vues » (2736)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 3.1.1 | La vue formulaire | Organiser la fiche course (groupes, onglets, en-tête) | ♻ 1358 🎥 |
| 3.1.2 | La vue liste (`<list>`, ex-`<tree>`) | Lister les courses, totaux, couleurs | ＋ |
| 3.1.3 | La vue recherche : filtres et regroupements | « Mes courses du jour », regrouper par zone | ＋ |
| 3.1.4 | Actions et menus | Créer le menu Baobab Livraison | ♻ 2738 |
| 3.1.5 | Champs dynamiques : `invisible`, `readonly`, `required`, widgets | Remplacer l'ancien `attrs` | ＋ |
| 3.1.6 | La vue kanban | Le tableau des courses par statut | ♻ 2737 🎥 |
| 3.1.7 | Calendrier, pivot et graphique | Voir l'activité par jour et par zone | ＋ |
| 3.1.8 | Hériter d'une vue avec `xpath` | Ajouter un champ dans la fiche contact | ＋ |

### « Les rapports » (2739)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 3.2.1 | QWeb : la langue des modèles | `t-if`, `t-foreach`, `t-out`, `t-field` | ♻ 1359 |
| 3.2.2 | Premier rapport PDF : le bordereau de livraison | Imprimer une course depuis le bouton Imprimer | ＋ 🎥 |
| 3.2.3 | Mise en page, logo, en-tête de la société, traductions | Un bordereau propre en français | ♻ 2740 |
| 3.2.4 | Quand le PDF ne sort pas : pannes courantes | Diagnostiquer le moteur PDF (à vérifier en 20) | ＋ |

### « L'interface web » (2741)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 3.3.1 | OWL : composant, modèle, état | Comprendre l'interface web d'Odoo | ♻ 1360 |
| 3.3.2 | Un petit composant : le suivi d'une course | Afficher un compteur qui se met à jour | ♻ 2742 |
| 3.3.3 | Une page du site : « Suivre mon colis » | Contrôleur + modèle QWeb public | ♻ 2743 🎥 |
| 3.3.4 | Le portail client | Le client voit ses courses dans « Mon compte » | ＋ |

### « Évaluation » (2744) : ♻ 2745 travail à rendre · ♻ 2746 quiz (20 questions existantes)

## Bloc 4 — Intégrations et sécurité (cours 211)

Objectif : ouvrir le module à l'appli des livreurs et au paiement mobile, sans ouvrir de faille.

### « Les API » (2747)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 4.1.1 | Les API d'Odoo : JSON-2 et les anciennes XML-RPC / JSON-RPC | Choisir la bonne API selon la version | ♻ 1361 |
| 4.1.2 | Créer une clé d'API et faire un premier appel JSON-2 | Lire les courses depuis un script Python | ＋ 🎥 |
| 4.1.3 | Créer et modifier des données depuis l'extérieur | Créer une course depuis un autre logiciel | ＋ |
| 4.1.4 | Créer ses propres adresses web (contrôleurs HTTP) | L'API de l'appli des livreurs | ♻ 2748 |
| 4.1.5 | Recevoir un webhook | Vérifier la signature, ne pas traiter deux fois | ＋ |
| 4.1.6 | Appeler un service extérieur : délais, erreurs, nouvelles tentatives | Ne pas bloquer Odoo quand le service est en panne | ♻ 2749 |
| 4.1.7 | Envoyer des e-mails automatiques | Modèle d'e-mail « Votre colis est livré » | ＋ |

### « Le paiement mobile » (2750)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 4.2.1 | Comment marche un paiement mobile | Demande, confirmation, notification, remboursement | ♻ 1363 |
| 4.2.2 | Exercice : un faux service de paiement | Payer une course et la marquer payée | ♻ 2751 |
| 4.2.3 | Échecs, doublons et rapprochement | Que faire quand la confirmation n'arrive jamais | ＋ |

### « La sécurité » (2752)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 4.3.1 | Groupes d'utilisateurs | Créer « Livreur » et « Responsable » | ＋ |
| 4.3.2 | Droits d'accès : `ir.access` (20) et `ir.model.access` (18-19) | Qui peut lire, créer, modifier, supprimer | ♻ 1362 |
| 4.3.3 | Restreindre par fiche : un livreur ne voit que ses courses | Domaine dans `ir.access` (20) / `ir.rule` (18-19) | ＋ |
| 4.3.4 | Protéger un champ ou un bouton | `groups="…"` sur les champs et les boutons | ＋ |
| 4.3.5 | Les erreurs de sécurité les plus courantes | `sudo` mal placé, données exposées par une API, injection SQL | ♻ 2753 |
| 4.3.6 | Données personnelles : ce que demande la loi sénégalaise | Les obligations du développeur (CDP) | ♻ 2754 |

### « Évaluation » (2755) : ♻ 2756 travail à rendre · ♻ 2757 quiz (20 questions existantes)

## Bloc 5 — Déploiement (cours 212)

Objectif : mettre le module en production, le faire évoluer et le surveiller sans casser la base du client.

### « Travailler proprement » (2758)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 5.1.1 | Développement, test, production : trois bases, trois règles | Ne jamais essayer sur la base du client | ＋ |
| 5.1.2 | Les règles d'une équipe : branches, demandes de fusion, relecture | Travailler à plusieurs sur un module | ♻ 2759 |
| 5.1.3 | La qualité automatique : style, vérificateurs, tests à chaque envoi | Lancer les tests sur GitHub à chaque envoi | ♻ 2760 🎥 |
| 5.1.4 | Aller plus loin dans les tests | Tester une adresse web et un parcours d'écran | ＋ |

### « Mettre en production » (2761)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 5.2.1 | Les hébergements : Odoo Online, Odoo.sh, serveur avec Docker | Conseiller le client selon son besoin | ♻ 2762 |
| 5.2.2 | Odoo.sh : branches, préproduction, production | Déployer en poussant sur une branche | ＋ 🎥 |
| 5.2.3 | Déployer avec Docker sur un serveur Linux | Base, Odoo, serveur web, nom de domaine | ♻ 2763 🎥 |
| 5.2.4 | Réglages de production : HTTPS, workers, limites, mot de passe maître | Un serveur qui tient la charge et reste fermé | ＋ |
| 5.2.5 | Sauvegarder et restaurer | Le geste qui sauve, et le tester | ♻ 2764 🎥 |
| 5.2.6 | Mettre à jour un module en production | Sauvegarde, test, mise à jour, retour arrière | ♻ 2765 |
| 5.2.7 | Migrer vers une nouvelle version d'Odoo | Préparer un passage 18 → 19 → 20 | ♻ 2766 |

### « Surveiller » (2767)
| # | Leçon | Objectif | Fiche |
|---|---|---|---|
| 5.3.1 | Les journaux, les lenteurs et les erreurs : trouver la cause | Lire les journaux de production | ♻ 2768 |
| 5.3.2 | Rendre Odoo plus rapide | Requêtes lentes, index, champs enregistrés, profileur | ＋ |
| 5.3.3 | Être prévenu avant le client | Alertes, suivi des erreurs, espace disque | ＋ |

### « Projet tutoré » (2769) : ♻ 2770 à 2773 (à rédiger après les blocs)
### « Évaluation » (2774) : ♻ 2775 soutenance · ♻ 2776 quiz (15 questions existantes)

---

## Vidéos du Bloc 1 (mode terminal de tuto.mjs)

Scénarios dans `videos/`. Tutoiement (public TAAGG School). Sorties à l'écran : soit lancées pour de vrai pendant le
tournage (`executer: oui`), soit copiées de vrais essais (Ubuntu 24.04, Odoo 20.0, PostgreSQL 16.15, Docker odoo:20).
État : ☐ à écrire · ✎ brouillon OK · 🎙 voix OK · ✅ publiée sur la fiche

| Scénario | Leçon (fiche) | Contenu | État |
|---|---|---|---|
| `CT1-02-premier-script` | 1.0.2 (2699) | version de Python, nano, premier script, console | ✎ |
| `CT1-11-ubuntu-wsl` | 1.1.1 (1353) | PowerShell `wsl --install` (sans résultat inventé), apt update, versions | ✎ |
| `scenarios/02-terminal-premiers-pas` | 1.1.2 (2701) | pwd, mkdir, cd, ls -l, nano, python3 (exemple de l'outil) | ✎ |
| `CT1-26-debogage` | 1.2.6 (2704) | vraie trace d'erreur, lecture de bas en haut, séance pdb | ✎ |
| `CT1-31-postgresql` | 1.3.1 (2905) | installation, createuser, psql, CREATE/INSERT/SELECT | ✎ |
| `CT1-41-git` | 1.4.1 (2708) | config, init, status, add, commit, log, diff | ✎ |
| `CT1-44-installer-odoo` | 1.4.4 (2709) | apt, git clone, venv, pip, premier démarrage d'Odoo 20 | ✎ |
| `CT1-45-docker` | 1.4.5 (2909) | compose.yaml, up, ps, version, journal, down | ✎ |
| — | 1.4.7 VS Code | interface graphique : enregistrement d'écran par Babacar | ☐ |

Restent à décider : la voix (ElevenLabs ou voix clonée de Babacar) avant la version finale (crédits ElevenLabs).

## Volume

| Bloc | Leçons | dont à créer | Questions de quiz (3 par leçon) |
|---|---|---|---|
| 1 | 28 | 17 | 84 |
| 2 | 26 | 10 | 78 |
| 3 | 16 | 8 | 48 |
| 4 | 16 | 8 | 48 |
| 5 | 14 | 6 | 42 |
| **Total** | **100** | **49** | **300** |

## Avancement

| Bloc | Programme | Fiches rédigées | Quiz | Montré à Babacar | Publié |
|---|---|---|---|---|---|
| 1 | validé 21/11 | 28 / 28 (brouillon) | 28 / 28 | à faire | non |
| 2 | validé 21/11 | 0 / 26 | 0 / 26 | — | — |
| 3 | validé 21/11 | 0 / 16 | 0 / 16 | — | — |
| 4 | validé 21/11 | 0 / 16 | 0 / 16 | — | — |
| 5 | validé 21/11 | 0 / 14 | 0 / 14 | — | — |

## Journal
- 21/11/2026 : état des lieux des cours 208 à 212, vérification des versions dans la documentation officielle, proposition de programme.
- 21/11/2026 : Babacar valide le programme et le fil rouge Baobab Livraison ; Bloc 1 lancé.
- 21-22/11/2026 : Bloc 1 rédigé (28 fiches + 84 questions), tout en brouillon. Code vérifié sur un vrai Odoo 20.0
  (sources + Python 3.12 + PostgreSQL 16, et image Docker odoo:20 + postgres:16). Sources des fiches : `bloc1/*.py`,
  gabarit : `outils/fiche.py`, identifiants : `outils/ids_bloc1.json`. Les 3 anciennes fiches « document » vides
  (1352, 1353, 1354) sont devenues des articles. ✅ = fiche rédigée (avec son identifiant sur le site).

## Bloc 1 — reste à faire avant publication
- Relecture par Babacar.
- Non testé ici, à tester sur un PC Windows : installation de WSL (1.1.1) et interface de VS Code (1.4.7).
- ~~Rédiger le « Travail à rendre » (2712) et relire le grand quiz (2713)~~ : fait le 22/11 (voir journal).
- Préciser aux apprenants comment envoyer le lien de leur dépôt au formateur (e-mail ? formulaire ?).
- Les sections sont publiées mais les leçons sont en brouillon : rien n'est visible des apprenants tant qu'on ne publie pas.
- 22/11/2026 : « Travail à rendre » 2712 rédigé (script CSV, requêtes SQL, règles Git, barème sur 20), en brouillon.
  Corrigé testé, **gardé hors du dépôt** (dépôt public) et transmis à Babacar. Quiz 2713 relu : 20 questions justes et
  conformes aux fiches ; explication ajoutée à la question 19 (redémarrer / mettre à jour, vérifié sur Odoo 20).
