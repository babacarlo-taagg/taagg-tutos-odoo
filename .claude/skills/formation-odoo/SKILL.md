---
name: formation-odoo
description: Concevoir et produire une formation Odoo complète en capsules vidéo d'environ 10 minutes (un module Odoo couvert fonctionnalité par fonctionnalité, paramétrage par paramétrage) — programme, découpage, préparation des données de démo, écriture et tournage de chaque capsule, suivi de l'avancement. Utiliser dès que Babacar parle de « formation », « capsules », « parcours », « programme », « série » ou veut couvrir tout un module (Comptabilité, Ventes, Stock…).
---

# Formation Odoo en capsules de 10 minutes

Une formation = un dossier `formations/<module>/` :

```
formations/comptabilite/
  programme.md              le plan : parcours, capsules, objectifs, état d'avancement
  CPT-01-tour-d-horizon.yaml  une capsule = un scénario tuto.mjs
  CPT-02-parametres.yaml
  …
```

Chaque capsule se tourne avec la chaîne habituelle (compétence `tuto-odoo`) :
`node tuto.mjs formations/comptabilite/CPT-02-parametres.yaml --brouillon`, puis la version finale.

## 1. Le programme (avant tout tournage)

- Partir de **ce qui est installé dans la base de tournage** (lire les modules et le paramétrage par
  l'API, voir plus bas), pas de la documentation générale d'Odoo.
- Ordre : d'abord le **paramétrage** (ce qu'on règle une fois), puis l'**usage quotidien**, puis la
  **clôture et les rapports**. Chaque capsule ne s'appuie que sur les précédentes.
- Une capsule = **un objectif** qu'on peut nommer en une phrase (« Paramétrer les taxes de vente et
  d'achat »). Si l'objectif ne tient pas en 10 min, couper en deux capsules ; si une capsule fait
  moins de 6 min, la fusionner.
- Code court par capsule (`CPT-07`) : il sert de nom de fichier, de titre YouTube et de repère.
- Faire valider le programme par Babacar avant d'écrire les capsules ; tenir l'avancement dans
  `programme.md` (à écrire → brouillon OK → voix OK → publiée).

## 2. La structure d'une capsule de 10 min

≈ 1 400 mots dits, 50 à 80 étapes. Toujours le même squelette, pour que l'apprenant se repère :

| Moment | Durée | Contenu |
|---|---|---|
| Accroche | 30 s | ce qu'on saura faire à la fin, pourquoi c'est utile pour l'entreprise |
| Rappel | 20 s | où on en est dans la formation (capsule précédente) |
| Parties 1 à 3 (ou 4) | 2–3 min chacune | une `partie:` par grand geste ; le bandeau s'affiche 5 s |
| Pièges fréquents | 1 min | 2 ou 3 erreurs classiques et comment les éviter |
| Récapitulatif | 40 s | 3 à 5 points à retenir, à dire lentement |
| Exercice | 20 s | une consigne à refaire seul dans sa base (« créez la taxe TVA 10 % achats ») |

- Le texte suit `tuto-odoo-scenario` (phrases courtes, vouvoiement, libellés exacts de l'écran),
  avec **une phrase de « pourquoi » pour chaque paramètre** : un paramétrage sans sa raison ne s'apprend pas.
- Vocabulaire comptable : le dire en français courant la première fois
  (« le lettrage, c'est-à-dire relier une facture à son paiement »), puis garder le mot juste.
- Exemples tirés de l'entreprise de la base (Les Délices de Maïmouna, montants en francs CFA,
  TVA sénégalaise 18 %, plan SYSCOHADA), jamais d'exemples européens.
- Les montants se disent en entier : « cent-dix-huit mille francs CFA » (ajouter `FCFA: francs CFA`
  et les sigles dans `prononciation`).

## 3. Préparer les données de chaque capsule

La base de tournage est partagée et chaque tournage la modifie (une facture créée reste créée).
- En tête de chaque scénario, noter en commentaire **l'état de départ** attendu
  (« un client Awa Diop existe, aucune facture brouillon »).
- Préparer ou remettre cet état **par l'API** avant le tournage (JSON-RPC avec `ODOO_LOGIN_API` +
  `ODOO_CLE_API` du `.env`, base `edu-correction-les-delices-de-maimouna`), jamais à la main à l'écran.
  Préférer archiver ou annuler plutôt que supprimer.
- Ranger cette remise à zéro dans `formations/<module>/etat-depart.py` (une fonction par capsule,
  exemple : `python3 formations/comptabilite/etat-depart.py CPT-02`) et la lancer avant chaque tournage,
  brouillon compris.
- Les noms tapés à l'écran doivent être nouveaux à chaque tournage (sinon doublons) : prévoir un
  suffixe ou nettoyer avant de retourner.
- L'exercice 2025 est verrouillé : toutes les pièces filmées sont datées de l'exercice en cours.
- Ne pas modifier un paramètre que les capsules suivantes supposent : si une capsule change un
  réglage pour la démonstration, elle le remet à la fin (hors caméra, par l'API).

## 4. Produire la série

1. Brouillon muet de chaque capsule (gratuit) → corriger jusqu'à ce que tout passe.
2. Envoyer à Babacar le brouillon + le texte pour relecture ; corriger.
3. Voix (compétence `tuto-odoo-voix`) : même voix et même vitesse pour toute la formation.
   Budget : une capsule ≈ 9 000 caractères de voix ; vérifier le crédit ElevenLabs avant de lancer la série.
4. Version finale, contrôle qualité et textes de publication (compétence `tuto-odoo-montage`),
   playlist « Formation Comptabilité Odoo », titres `CPT-07 · Paramétrer les taxes`.
5. Mettre à jour l'avancement dans `programme.md` et pousser.

Pour chaque capsule, le texte à faire relire se tire du scénario : une ligne numérotée par étape,
les titres de partie en intertitres, et le nombre de caractères (≈ 15 caractères par seconde de voix).
