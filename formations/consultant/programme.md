# Formation Posture & Méthodologie Consultant — capsules vidéo (proposition)

Cours taagg-school.com : **Bloc 6 — Posture & Méthodologie Consultant** (cours 235, programme
« Consultant fonctionnel Odoo »). Le bloc parle de méthode : les capsules montrent **les outils Odoo
qui servent au consultant** pour l'appliquer, sur le projet de démonstration des Délices de Maïmouna.
Chaque capsule est rangée dans la section du cours qu'elle illustre, à côté des fiches écrites
(9 fiches d'origine corrigées le 11/11, 21 fiches nouvelles publiées le 12/11, atelier 2850, quiz 2851).

Base de tournage : « Les Délices de Maïmouna » — Odoo 19 Enterprise, **partagée** avec les formations
Comptabilité, E-business et Studio. Applications utilisées, toutes déjà installées : Projet, Feuilles de
temps, Connaissances, Sondages, To-do, Paramètres › Utilisateurs.

Capsules de **3 à 5 minutes**, même squelette que Studio : introduction · parties numérotées ·
3 pièges · récapitulatif · exercice. Voix de Babacar (clone ElevenLabs), même vitesse.

Avancement : ☐ à écrire · 📝 scénario écrit · ✎ brouillon muet OK · 🎙 voix OK · ✅ publiée

## Les capsules

| Code | Section du cours | Capsule | Ce qu'on apprend | Écrans | Fiches liées | État |
|---|---|---|---|---|---|---|
| CON-01 | 2. Méthodologie | Piloter le déploiement dans Projet | un projet « Déploiement Odoo — Délices de Maïmouna » ; les 6 phases en **étapes** ; une tâche par livrable avec responsable et échéance ; la vue liste et le filtre « en retard » ; le client abonné au projet (montré, pas invité) | Projet | 2.1, 2836, 2839 || ✅ 3:07 (publiée le 12/11) |
| CON-02 | 2. Méthodologie | Le cahier des charges et les comptes-rendus dans Connaissances | un article « Projet Maïmouna » et ses sous-articles ; le compte-rendu d'atelier à partir de la trame ; un tableau d'exigences numérotées ; partager un article (bouton montré, aucune invitation envoyée) | Connaissances | 2.2, 2.3, 2836, 2838 || ✅ 3:12 (publiée le 13/11) |
| CON-03 | 2. Méthodologie | Combien coûtent les licences ? Lire sa base comme un acheteur | compter les utilisateurs internes et les comptes portail (gratuits) ; repérer ce qui impose le plan Custom : Studio installé, plusieurs sociétés ; où noter la date de renouvellement ; relever les prix sur odoo.com (montré en image fixe, pas filmé en direct) | Paramètres › Utilisateurs, Applications | 2830, 2831, 2832 || ✅ 3:13 (publiée le 13/11) |
| CON-04 | 3. Recette | Suivre la recette dans Projet | un projet « Recette » aux 5 étapes (Signalée → Clôturée) ; une tâche par anomalie, la gravité en étiquette, le testeur abonné ; distinguer anomalie, erreur de formation et nouvelle demande ; le filtre « gravité 1 ouvertes » avant de signer le PV | Projet | 3.1, 2840, 2841 || 🎙 3:09 (livrée, leçon 2855 en brouillon) |
| CON-05 | 3. Recette | Mesurer la formation et l'adoption avec Sondages | un questionnaire de 5 questions après formation ; le tester soi-même ; lire les résultats ; le bouton « Partager » montré sans rien envoyer | Sondages | 3.2, 2842, 2843 | ☐ |
| CON-06 | 4. Situations difficiles | Le temps passé contre le temps prévu : des faits pour l'avenant | heures prévues sur le projet et les tâches ; saisir des feuilles de temps ; le rapport « prévu / passé » ; s'en servir pour chiffrer une demande hors périmètre | Projet, Feuilles de temps | 4.1, 2844, 2845 | ☐ |
| CON-07 | 5. Outils | S'organiser au quotidien : To-do et activités | la liste To-do du consultant ; transformer les actions d'un compte-rendu en To-do et en activités ; la vue « mes activités » du matin | To-do, activités | 5.1, 2847, 2848 | ☐ |

**7 capsules ≈ 28 minutes.** Ordre de tournage proposé : CON-01 (elle crée le projet de démonstration
dont se servent CON-04, CON-06 et CON-07), puis CON-02, CON-04, CON-06, CON-07, CON-05, CON-03.

## Prudence sur la base partagée

- **Rien n'est changé dans les paramètres généraux** : on n'active pas les jalons ni les dépendances
  de tâches (désactivés pour toute la base) ; les phases sont des **étapes** du projet de démonstration.
- **Données existantes à ne pas toucher** : le projet « Ouverture boutique Almadies » (Babacar), les
  projets « Interne », les deux sondages modèles d'Odoo, les articles Connaissances existants.
- **Aucun e-mail ni invitation** : partage d'article, invitation au sondage et abonnement du client sont
  montrés, jamais validés. Le « client » abonné est le contact de démonstration Moussa Ndiaye.
- **Ce que chaque capsule crée, et que `formations/consultant/etat-depart.py` défera** (sur le modèle de
  celui de Studio ; l'accord permanent de Babacar couvre ces retraits) :

| Capsule | Créé à l'écran ou préparé par l'API |
|---|---|
| CON-01 | le projet « Déploiement Odoo — Délices de Maïmouna », ses étapes et ses tâches |
| CON-02 | l'article privé « Projet Délices de Maïmouna » et ses sous-articles (et tout article privé vide laissé par un essai) |
| CON-03 | rien (lecture seule) |
| CON-04 | le projet « Recette — Délices de Maïmouna » (préparé par l'API), ses étapes, ses tâches et les 5 étiquettes de la recette |
| CON-05 | le sondage « Formation Odoo — votre avis (formation) » et les réponses de test |
| CON-06 | l'employé « Formateur TAAGG » (nécessaire pour saisir du temps, archivé ensuite) et ses feuilles de temps sur le projet de démonstration |
| CON-07 | les To-do et activités du formateur créés à l'écran |

## Questions pour Babacar avant de tourner (réponses du 12/11 : flou au montage pour CON-03 ; employé « Formateur TAAGG » créé ; prix non filmés)

1. **CON-03 montre la liste des utilisateurs** : on y voit ton compte (nom et adresse e-mail). Je
   propose la vue regroupée par type (internes / portail) avec les adresses masquées par un flou au
   montage. D'accord, ou on crée deux comptes fictifs et on filtre sur eux ?
2. **CON-06 a besoin d'une fiche employé** pour le compte « Formateur TAAGG » (aucune aujourd'hui).
   Je la crée par l'API avant le tournage et je l'archive après : d'accord ?
3. **Les prix des licences** ne sont filmés nulle part (ils changent) : la capsule renvoie à odoo.com et
   à la fiche 2831. Si tu veux une image des prix du jour pour le Sénégal, envoie-moi une capture et je
   l'insère en image fixe, datée.

## Crédit de voix

Compte de secours : environ 109 000 caractères restants. 7 capsules ≈ 22 000 caractères, plus les
reprises. Avant chaque voix finale : crédit vérifié, consommation annoncée, accord de Babacar
(« c bon on peut générer »).
