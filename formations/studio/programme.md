# Formation Studio & Personnalisation low-code — programme (proposition)

Cours taagg-school.com : **Bloc 5 — Studio & Personnalisation low-code** (cours 234, programme
« Consultant fonctionnel Odoo »). Une capsule vidéo par grande procédure, rangée dans sa section,
à côté des fiches écrites existantes (publiées 1.1 à 6.1, brouillons 2802 à 2819).

Base de tournage : « Les Délices de Maïmouna » — Odoo 19 Enterprise, Studio installé, base **partagée**
avec les formations Comptabilité et E-business. Studio est absent d'Odoo Community (la version de la base
TAAGG) : toute la formation est **[E]**.

Capsules de **3 à 6 minutes**, même squelette que la Comptabilité : introduction · parties numérotées ·
3 pièges · récapitulatif · exercice. Voix de Babacar (clone ElevenLabs). Mêmes exemples que les fiches :
le « Type d'événement » et le nombre de convives sur les devis, le prix par convive, l'événement et
l'acompte sur le devis PDF, le livreur qui ne voit que ses livraisons.

Avancement : ☐ à écrire · 📝 scénario écrit · ✎ brouillon muet OK · 🎙 voix OK · ✅ publiée

## Les capsules

| Code | Section du cours | Capsule | Ce qu'on apprend | Écrans | Fiches liées | État |
|---|---|---|---|---|---|---|
| STU-01 | 1. Découvrir Studio | Ouvrir Studio et lire l'éditeur | l'icône Studio, ce que Studio fabrique (champs, vues, règles), les 5 zones de l'éditeur, Annuler / Fermer, le contexte (la vue qu'on regardait) | un devis, Studio | 1.1, 1.2, 2802, 2804 | ✅ 4:12 (publiée le 9/11) |
| STU-02 | 2. Champs et vues | Ajouter des champs : le type d'événement | champ Sélection « Type d'événement » (5 valeurs), champ Entier « Nombre de convives », invisible et obligatoire selon une condition, test sur un devis | Ventes › Devis | 2.1, 2805 | ✅ 4:31 (publiée le 9/11) |
| STU-03 | 2. Champs et vues | Choisir le bon lien entre deux fiches | Many2one « Livreur » et champ associé « Téléphone du client » sur le bon de livraison ; étiquettes « Allergènes » ; quand prendre des lignes (One2many) | Inventaire › Livraisons, Produits | 2806 | ✅ 4:29 (publiée le 9/11) |
| STU-04 | 2. Champs et vues | Ranger les écrans : la fiche et la liste | un onglet « Événement » sur le devis, une colonne dans la liste, un regroupement par type d'événement (kanban retiré : Studio 19 n'y propose pas les champs existants) | Ventes › Devis (3 vues) | 2.2, 2807 | ✅ 3:19 (publiée le 9/11) |
| STU-05 | 3. Automatiser | Un champ calculé : le prix par convive | vérifier le standard d'abord (Marges), champ Monétaire, dépendances et calcul en mode développeur, stocké ou non, contrôle 1 200 000 F / 150 = 8 000 | Devis, Paramètres › Technique › Champs | 3.2, 2810 | ✅ 3:56 (publiée le 9/11) |
| STU-06 | 3. Automatiser | Une règle d'automatisation : le mariage confirmé | QUAND / SI / ALORS, « Avant la mise à jour » et « Appliquer sur », champs surveillés, action « Créer une activité », test en 3 cas | Studio › Automatisations | 3.1, 2808, 2809, 2811 | ✅ 4:04 (publiée le 9/11) |
| STU-07 | 4. Rapports PDF | Le devis PDF : l'événement et les convives | ce qui relève de la mise en page (sans Studio) et ce qui relève du rapport ; insérer des champs avec « / » ; paragraphe d'acompte réservé aux mariages ; impression de contrôle | Studio › Rapports › Devis / Commande | 4.1, 2812, 2813 | ✅ 3:52 (publiée le 9/11) |
| STU-08 | 5. Sécurité et droits | Le livreur ne voit que ses livraisons | cacher n'est pas protéger (test de l'export) ; groupe « Livraison : Livreur », droits d'accès, règle d'enregistrement ; test avec le compte du livreur | Paramètres › Groupes, Règles | 5.1, 2814, 2815 | ☐ |
| STU-09 | 6. Synthèse | Du test à la production | le registre des personnalisations, la check-list de recette, Studio › Exporter (le .zip), Importer dans une autre base, ce qu'il faut sauvegarder avant | Studio (accueil) | 6.1, 2816, 2817 | ☐ |
| STU-10 | 6. Synthèse | Atelier : les 5 demandes de Maïmouna | présenter les 5 demandes de l'atelier et la bonne réponse à chacune (dont 2 sans Studio) ; à voir après avoir fait l'exercice | revue rapide des écrans des capsules 2 à 8 | 2818, 2819 | ☐ |

**10 capsules ≈ 45 minutes.** STU-10 est facultative : elle peut rester un exercice écrit (fiche 2818).

## Ordre de tournage

1. **STU-02 en pilote** : c'est le geste de base de Studio. Elle valide le ton, la durée et le nettoyage.
2. STU-01, puis STU-03 à STU-08 dans l'ordre : chacune s'appuie sur les champs des précédentes
   (le type d'événement sert à STU-04, 05, 06 et 07 ; le livreur de STU-03 sert à STU-08).
3. STU-09 et STU-10 en dernier.

## Prudence sur la base partagée

- **Écrans utilisés** : devis de Ventes, bons de livraison, produits (étiquettes « Allergènes » seulement),
  paramètres techniques. **Jamais** les factures, les paiements, les journaux ni les relevés.
- **Pas de changement de la mise en page de la société** dans STU-07 : la capsule CPT-02 la filme.
  STU-07 la montre sans y toucher et ne modifie que le rapport « Devis / Commande ».
- **Produits** : la capsule CPT-09 filme la fiche produit. Le champ « Allergènes » est retiré juste après
  le tournage de STU-03, sinon on le met ailleurs (question 3 ci-dessous).
- **Ce que chaque capsule crée, et que `etat-depart.py` défera, et rien d'autre** (liste à montrer
  à Babacar avant toute suppression) :

| Capsule | Créé à l'écran |
|---|---|
| STU-01 | rien (visite seulement) |
| STU-02 | champs `x_studio_type_evenement`, `x_studio_nombre_de_convives` sur les devis + leur place dans la vue formulaire |
| STU-03 | champs `x_studio_livreur`, `x_studio_telephone_du_client` (livraisons), `x_studio_allergenes` + le modèle des allergènes (produits) |
| STU-04 | l'onglet « Événement », la colonne, la carte kanban, le filtre enregistré |
| STU-05 | champ `x_studio_prix_par_convive` |
| STU-06 | la règle « Mariage confirmé → dégustation » et les activités qu'elle a créées |
| STU-07 | les modifications Studio du rapport Devis / Commande |
| STU-08 | groupe « Livraison : Livreur », ses droits et sa règle, l'utilisateur de test |
| STU-09 | le fichier exporté (sur l'ordinateur, rien dans la base) |

  Les noms techniques exacts sont relevés au tournage et notés en tête de chaque scénario.
- Chaque capsule tourne sur des fiches de démonstration (devis « Mariage » d'un client d'exemple,
  livraisons de démonstration). Les noms tapés à l'écran prennent un suffixe pour éviter les doublons.

## Questions pour Babacar avant de tourner

1. **Amadou FALL n'est pas un utilisateur** (seulement un employé). Pour STU-06, l'activité va
   **au vendeur du devis**, sans créer de compte, ce qui suit aussi le conseil de la fiche 2809 :
   un rôle plutôt qu'un nom. Ou bien on crée un compte « Amadou FALL » de démonstration ?
2. **STU-08 a besoin d'un compte de test « Modou GUEYE (livreur) »**. Un utilisateur interne de plus
   sur la base de tournage : d'accord ? Il est archivé (pas supprimé) par `etat-depart.py`.
3. **Allergènes sur la fiche produit** (filmée par CPT-09), retirés juste après le tournage : d'accord,
   ou préférez-vous montrer les étiquettes ailleurs (par exemple « Préférences » sur le contact client) ?
4. **STU-10** : capsule vidéo, ou on laisse l'atelier en exercice écrit ?

## Crédit de voix

Environ 3 000 caractères restants jusqu'au 17 novembre ; une capsule de 4 à 5 minutes en demande
3 500 à 5 000. D'ici là : scénarios et brouillons muets seulement. Avant chaque voix finale : crédit
vérifié, consommation annoncée, et l'accord de Babacar (« c bon on peut générer »).
