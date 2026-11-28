# Formation Point de Vente (caisse) — capsules vidéo (proposition)

Cours taagg-school.com : **Bloc 7 — Canal direct : POS, E-commerce & Site Web** (cours 236). Les capsules
illustrent la section « 1. Point de Vente (POS) » : fiches 1.1 à 1.4 corrigées le 21/11, fiches 1.5 à 1.8
publiées le 21/11, atelier 2892 et quiz 2893 publiés le 28/11. L'e-commerce et le site web sont déjà couverts par
les vidéos EB de la formation E-Business (reprises dans le cours, leçons 2869 à 2876).

Base de tournage : « Les Délices de Maïmouna » — Odoo 19 Enterprise, **partagée** avec les formations
Comptabilité, E-business, Studio et Consultant. Point de Vente installé le 17/11 (avec la connexion des employés
en caisse et la fidélité ; **sans** le mode restaurant).

Fil rouge : Maïmouna ouvre un **comptoir de vente** dans sa pâtisserie de la Médina (le même que dans l'atelier
2892). Capsules de **3 à 5 minutes**, même squelette que Studio et Consultant : introduction · parties numérotées ·
3 pièges · récapitulatif · exercice. Voix de Babacar (clone ElevenLabs), même vitesse.

Avancement : ☐ à écrire · 📝 scénario écrit · ✎ brouillon muet OK · 🎙 voix OK · ✅ publiée

## Les capsules

| Code | Capsule | Ce qu'on apprend | Écrans | Fiches liées | État |
|---|---|---|---|---|---|
| POS-01 | Créer la caisse et ses modes de paiement | le point de vente « Comptoir Médina » ; les modes Espèces, Wave, Orange Money, chacun relié à **son** journal ; les réglages utiles (taxes, connexion des employés, écart maximum autorisé) | Point de Vente › Configuration | 1.2, 1.8 | ✅ 3:29 (publiée le 28/11, leçon 2933, 3 questions) |
| POS-02 | Préparer les produits pour la caisse | la case « Disponible dans le PdV » ; 3 catégories de caisse (Boissons, Pâtisseries, Snacks) ; la taxe « 18 % TTC » ; le suivi du stock pour les jus seulement ; vérifier dans la caisse | Ventes › Produits, la caisse | 1.2 | ☐ |
| POS-03 | Une matinée de caisse : ouvrir et encaisser | l'ouverture avec un fond de caisse de 25 000 F ; une vente en espèces et la monnaie rendue ; un paiement partagé espèces + Wave ; une remise de 10 % sur une ligne ; une sortie d'espèces de 2 000 F pour les sachets | la caisse | 1.5, 1.6 | ☐ |
| POS-04 | Retour, facture et fermeture de la caisse | rembourser un jus depuis la vente d'origine ; une facture pour un client professionnel ; fermer la caisse : comptage, écart de −500 F expliqué, clôture | la caisse, Point de Vente › Sessions | 1.5, 1.6 | ☐ |
| POS-05 | Les chiffres du soir et le contrôle des écarts | la liste des sessions et leurs écarts ; l'analyse des commandes par jour, produit, mode de paiement et vendeuse ; enregistrer deux vues en favoris pour Maïmouna | Point de Vente › Rapports | 1.7 | ☐ |
| POS-06 | Rapprocher Wave avec la caisse | l'encaissement Wave créé à la clôture ; une ligne de relevé Wave ; le rapprochement et les frais de l'opérateur en charge | Comptabilité › Wave Comptoir | 1.8 | ☐ (à confirmer : question 3) |

**5 ou 6 capsules ≈ 22 à 26 minutes.** Ordre de tournage imposé : POS-01 → POS-06 (chaque capsule part de ce que
la précédente a créé). Le mode restaurant (fiche 1.3) et le matériel (fiche 1.4) ne sont pas filmés : pas de
restaurant installé ni d'imprimante sur la base.

## Prudence sur la base partagée

- **Aucun produit existant n'est touché** (beaucoup sont à 1 F, données d'un autre exercice) : la capsule POS-02
  travaille sur **9 produits propres au comptoir**, absents de la base aujourd'hui : Jus de bissap, Jus de bouye,
  Jus de gingembre (33 cl, 500 F), Part de fraisier, Part d'opéra (1 500 F), Beignet, Fataya (250 F),
  Thiakry (pot, 750 F), Croissant du comptoir (350 F). Prix TTC, taxe existante « 18 % TTC ».
- **Journaux propres** : « Espèces Comptoir », « Wave Comptoir », « Orange Money Comptoir ». Les journaux existants
  « Caisse boutique » et « Wave » de la formation Comptabilité ne sont pas utilisés.
- **Vendeuses** : les fiches employées existantes (Awa CISSE, Fatou NDIAYE) servent à la connexion en caisse,
  sans être modifiées ; le code de caisse n'est pas montré.
- **Aucun e-mail** : facture et ticket ne sont pas envoyés ; le client professionnel est un contact de démonstration.
- **Ce que chaque capsule crée, et que `formations/pos/etat-depart.py` défera** (accord permanent de Babacar) :

| Capsule | Créé à l'écran ou préparé par l'API |
|---|---|
| POS-01 | le point de vente « Comptoir Médina », ses 3 modes de paiement et les 3 journaux « Comptoir » |
| POS-02 | les 9 produits du comptoir et les 3 catégories de caisse |
| POS-03 | la session du jour, ses ventes et la sortie d'espèces |
| POS-04 | le remboursement, la facture du client professionnel, la clôture (écritures comptables) |
| POS-05 | 2 filtres favoris du formateur |
| POS-06 | la ligne de relevé Wave et son rapprochement |

## Questions pour Babacar avant de tourner

1. **Droits du compte « Formateur TAAGG »** : il n'a aujourd'hui aucun droit sur le Point de Vente (le compte API
   non plus). Je lui ajoute le groupe « Point de Vente / Administrateur » par l'API, et je le retire après la
   formation. D'accord ?
2. **La clôture d'une session passe des écritures en comptabilité** (ventes, TVA, encaissements), dans la société
   des Délices de Maïmouna partagée avec la formation Comptabilité. Une session clôturée ne se supprime pas
   proprement. Je propose de **laisser ces écritures** (quelques dizaines de milliers de F, dans les journaux
   « Comptoir » à part, libellées « Comptoir Médina ») : elles sont cohérentes avec l'histoire de Maïmouna. Sinon,
   on arrête POS-04 avant le bouton « Clôturer » (la fermeture est montrée, pas validée).
3. **POS-06 (rapprochement Wave)** touche la Comptabilité : on la garde, ou la fiche 1.8 suffit et on renvoie à
   la capsule banque de la formation Comptabilité ?
4. **Mode restaurant** : on l'installe pour une capsule POS-07 (plan de salle, « Commander »), ou on s'en tient à la
   fiche 1.3 ?

## Crédit de voix

Compte « Babacar LO » (voix IPPenh…, clé fournie le 28/11, à supprimer après la formation) : 84 811 caractères avant POS-01. 6 capsules ≈ 19 000 caractères, plus les reprises.
Avant chaque voix finale : crédit vérifié, consommation annoncée, accord de Babacar (« c bon on peut générer »).
