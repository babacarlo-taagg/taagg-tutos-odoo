# Formation Comptabilité Odoo — programme

Base de tournage : « Les Délices de Maïmouna » — Odoo 19 Enterprise, plan comptable SYSCOHADA Sénégal,
francs CFA, TVA 18 % / 10 %, exercice 2025 clôturé et verrouillé.
Capsules d'environ 10 minutes, structure commune décrite dans la compétence `formation-odoo`.

> ⚠ Cette base est en **Enterprise**. Plusieurs capsules (rapprochement bancaire avancé, rapports
> SYSCOHADA, immobilisations, budgets, relances, emprunts, révision) n'existent pas dans Odoo Community
> (la version de la base TAAGG) : elles sont marquées **[E]**.

Avancement : ☐ à écrire · ✎ brouillon OK · 🎙 voix OK · ✅ publiée

## Parcours 1 — Mettre en place la comptabilité (paramétrage)

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| CPT-01 | Tour d’horizon de la Comptabilité | le tableau de bord, les journaux, les 6 menus et à quoi ils servent | Tableau de bord | 🎙 8:19 |
| CPT-02 | Les paramètres généraux | société, devise XOF, arrondis, présentation des factures, fonctions à activer | Configuration › Paramètres | 🎙 6:46 |
| CPT-03 | Le plan comptable SYSCOHADA | classes 1 à 9, lire un compte, créer un compte, groupes et étiquettes | Plan comptable (panneau des classes) | 🎙 6:10 |
| CPT-04 | Les journaux | ventes, achats, banque, caisse, opérations diverses ; créer un journal de caisse | Journaux | 🎙 5:58 |
| CPT-05 | Les taxes : la TVA au Sénégal | TVA 18 %, 10 %, exonérée ; créer une taxe, taxes par défaut, groupes de taxes | Taxes | 🎙 5:49 |
| CPT-06 | Positions fiscales | clients locaux / étrangers : remplacer automatiquement taxes et comptes | Positions fiscales | 🎙 6:00 |
| CPT-07 | Conditions de paiement et exercice fiscal | « 30 % à la commande, solde à 60 jours », escompte ; exercices fiscaux | Conditions de paiement, Exercices fiscaux | 🎙 6:00 |
| CPT-08 | Banque, caisse et moyens de paiement | relier un compte bancaire, modes de paiement, arrondi des paiements en espèces | Journaux, Modes de paiement | ☐ |
| CPT-09 | Produits et catégories : où va l'argent | comptes de produits et de charges par catégorie et par article | Catégories de produits, Produits | ☐ |

## Parcours 2 — Ventes et clients

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| CPT-10 | Créer et valider une facture client | lignes, taxes, échéance, validation, envoi, l'écriture générée | Clients › Factures clients | ☐ |
| CPT-11 | Avoirs et annulation | rectifier une erreur : avoir total ou partiel, remettre en brouillon | Clients › Avoirs | ☐ |
| CPT-12 | Encaisser un paiement client | paiement total, partiel, plusieurs factures, escompte | Clients › Paiements | ☐ |
| CPT-13 | Relancer les clients **[E]** | niveaux de relance, lettre et e-mail automatiques, échéancier clients | Niveaux de relance, Échéancier clients | ☐ |

## Parcours 3 — Achats et fournisseurs

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| CPT-14 | Saisir une facture fournisseur | saisie manuelle, numérisation d'une facture PDF, contrôle des taxes | Fournisseurs › Factures fournisseurs | ☐ |
| CPT-15 | Notes de crédit et payer les fournisseurs | avoir fournisseur, paiement unique et groupé, échéancier fournisseurs | Fournisseurs › Paiements | ☐ |
| CPT-16 | Notes de frais des employés | de la dépense à son remboursement et à l'écriture | Dépenses de l'employé | ☐ |

## Parcours 4 — Trésorerie

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| CPT-17 | Importer un relevé bancaire | import CSV / OFX / CAMT, saisie manuelle d'une ligne | Tableau de bord › Banque | ☐ |
| CPT-18 | Le rapprochement bancaire **[E]** | relier chaque ligne du relevé à une facture ou un paiement | Rapprochement | ☐ |
| CPT-19 | Modèles de rapprochement **[E]** | automatiser les frais bancaires, agios, commissions | Modèles de rapprochement | ☐ |
| CPT-20 | La caisse | encaissements et décaissements en espèces, contrôle de caisse | Journal de caisse | ☐ |
| CPT-21 | Les emprunts **[E]** | créer un emprunt, échéancier, écritures automatiques | Actif & passif › Emprunts | ☐ |

## Parcours 5 — Opérations comptables

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| CPT-22 | Écritures d'opérations diverses | saisir une OD, extourner, dupliquer | Pièces comptables | ☐ |
| CPT-23 | Le lettrage | relier factures et paiements, lettrage manuel, comptes non lettrés | Clôture › Lettrer | ☐ |
| CPT-24 | Immobilisations et amortissements **[E]** | modèles d'immobilisations, créer une immobilisation, tableau d'amortissement, cession | Immobilisations, Modèles d'immobilisations | ☐ |
| CPT-25 | Charges et produits constatés d'avance **[E]** | étaler une charge ou un produit sur plusieurs mois | Écritures de régularisation | ☐ |
| CPT-26 | Factures à recevoir et à émettre **[E]** | régularisations de fin de période liées aux achats et ventes | Révision › Achats / Ventes | ☐ |
| CPT-27 | Comptabilité analytique | dimensions, comptes analytiques, modèles de répartition | Comptabilité analytique | ☐ |
| CPT-28 | Les budgets **[E]** | créer un budget, suivre le réalisé, rapport de budget | Budget analytique, Rapport de budget | ☐ |

## Parcours 6 — Fiscalité, clôture et rapports

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| CPT-29 | La déclaration de TVA **[E]** | rapport de taxes, clôture de la période de TVA, écriture de TVA à payer | Déclarations fiscales | ☐ |
| CPT-30 | Balance et grands livres **[E]** | lire la balance, le grand livre général et partenaires, filtrer, exporter | Grands livres | ☐ |
| CPT-31 | Les états financiers SYSCOHADA **[E]** | bilan, compte de résultat, flux de trésorerie, rapport Syscohada | Analyse › Syscohada, Comptes annuels | ☐ |
| CPT-32 | Contrôles et révision **[E]** | audit du journal, contrôles, dossiers de travail, piste d'audit | Révision | ☐ |
| CPT-33 | Clôturer l'exercice | dates de verrouillage, sécuriser les écritures, report à nouveau | Clôture | ☐ |

**33 capsules ≈ 5 h 30 de formation.**

## Journal de production

- **CPT-01** (28 octobre 2026) : version finale avec la voix de Babacar LO (clone ElevenLabs
  « Babacar LO (naturel) », vitesse 1,0), 8 min 19 s, 44 étapes, ≈ 7 700 caractères de voix.
  Contrôle qualité fait (images clés, synchro voix et image, son à −16 LUFS). À publier.
- **CPT-02** (28 octobre 2026) : version finale, 6 min 46 s, 40 étapes, ≈ 5 800 caractères de voix.
  Change la base (on garde ces réglages pour la suite) : adresse « Rue 22, Médina, Dakar », mise en page
  des documents « Bold », montant des factures en toutes lettres. Retourner : `python3 formations/comptabilite/etat-depart.py CPT-02` d'abord.
  Contrôle qualité fait (images clés, synchro, −16 LUFS, prononciation NINEA / XOF / SYSCOHADA vérifiée). À publier.
- **CPT-03** (28 octobre 2026) : version finale, 6 min 10 s, 40 étapes, ≈ 5 500 caractères de voix.
  Crée le compte 702110 « Ventes de pâtisseries » (gardé). Le menu « Groupes de comptes » n'existe qu'en mode
  développeur dans cette base : les classes sont montrées avec le panneau de gauche du plan comptable.
  Contrôle qualité fait. À publier.
- **CPT-04** (29 octobre 2026) : version finale, 5 min 58 s, 36 étapes, ≈ 5 300 caractères de voix.
  Crée le journal « Caisse boutique » (Espèces, préfixe CAI) et son compte 571001, créé par Odoo : un journal
  Espèces n'accepte que des comptes « Banque et espèces », et le 571100 du plan est en « Actifs circulants ».
  Gardés pour CPT-08 et CPT-20. Contrôle qualité fait. À publier.
- **CPT-05** (31 octobre 2026) : version finale, 5 min 49 s, 35 étapes, ≈ 5 000 caractères de voix.
  Crée la taxe de vente « 18% TTC » par duplication de « 18% » (gardée). Une phrase (étape 20) a été
  régénérée : la voix clonée avait ajouté un « euh » (repéré par la transcription de contrôle).
- **Mise en ligne** (31 octobre 2026) : CPT-01 à CPT-05 déposées sur Drive et ajoutées en brouillon dans le cours
  taagg-school.com « Bloc 4 — Finance & RH », section « Module comptabilité » (une leçon vidéo + une fiche
  article par capsule). Les liens Drive des vidéos se collent à la main (le connecteur n'a pas le droit).
- **CPT-06** (31 octobre 2026) : version finale, 6 min 00 s, 39 étapes, ≈ 5 000 caractères de voix.
  Odoo 19 : la règle de remplacement est portée par la taxe (champs Position fiscale et Remplace).
  Démonstration avec le client « Pâtisserie de Banjul » (Gambie), retiré par etat-depart.py. CPT-01 à CPT-05 publiées.
- **CPT-07** (31 octobre 2026) : version finale, 6 min 00 s, 36 étapes, ≈ 5 200 caractères de voix.
  Crée la condition « 50 % à la commande, solde à 30 jours », la pose sur la Boutique Les Almadies et montre
  une facture brouillon coupée en deux versements de 59 000 F ; tout est remis à zéro par etat-depart.py.

## Ordre de tournage proposé

1. CPT-01 (pilote : valide le ton, la voix et la durée de 10 min).
2. Parcours 1 dans l'ordre (le paramétrage conditionne tout le reste).
3. Parcours 2 et 3, puis 4, 5, 6.
