---
name: tuto-odoo
description: Fabriquer un tutoriel vidéo Odoo avec voix off (capture d'écran animée + voix + sous-titres + générique TAAGG), de la demande à la vidéo publiable. Utiliser dès que Babacar demande un tuto, une vidéo explicative, une démo ou une formation sur Odoo (utilisation ou paramétrage), ou dit « filme », « montre comment », « vidéo pour expliquer ».
---

# Tuto vidéo Odoo — de la demande à la vidéo

Chaîne complète, dans ce dépôt (`taagg-tutos-odoo`) :

```
scénario YAML  ──►  1. voix  ──►  2. tournage (navigateur piloté)  ──►  3. montage (ffmpeg)  ──►  MP4 1080p + .srt + chapitres
```

L'outil est `tuto.mjs`. Il calcule d'abord la durée de chaque phrase dite, puis rejoue les gestes
dans Odoo en attendant que la voix ait fini : la voix et l'image sont toujours synchronisées.

## Étapes à suivre

1. **Comprendre la demande** (une question au plus si c'est flou) : quel geste Odoo, pour qui
   (équipe TAAGG, école partenaire, tuteur…), quelle longueur (viser 1 à 4 min ; au-delà, faire une série).
2. **Préparer** (une seule fois par machine) :
   ```bash
   npm install                      # playwright + yaml
   cp .env.exemple .env             # puis remplir ODOO_* et la clé de voix
   ```
   Il faut aussi `ffmpeg` et un Chromium (`npx playwright install chromium` si absent).
   Dans une session Claude dans le cloud, Chromium est déjà là : ne pas lancer `playwright install`.
   Dans le cloud, ce Chromium est plus récent que celui attendu par Playwright : mettre
   `CHROMIUM_CHEMIN=/opt/pw-browsers/chromium` dans `.env` (sinon « Executable doesn't exist »).
   Les réglages peuvent aussi venir des variables d'environnement de l'environnement cloud
   (`ODOO_URL`, `ODOO_BASE`, `ODOO_LOGIN`, `ODOO_MOT_DE_PASSE`, `ODOO_LOGIN_API`, `ODOO_CLE_API`,
   `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `CHROMIUM_CHEMIN`) : `tuto.mjs` les lit en priorité.
   Vérifier la connexion : `node tuto.mjs explorer /odoo`.
3. **Repérer les écrans** : `node tuto.mjs explorer /odoo/contacts/new` liste les boutons, champs
   (nom technique + libellé), onglets et menus de la page, et enregistre `sortie/explorer.png`.
   Lire la capture pour voir l'écran réel. Répéter pour chaque écran du tuto.
4. **Écrire le scénario** dans `scenarios/NN-sujet.yaml` → suivre la compétence `tuto-odoo-scenario`.
   Faire relire le texte à Babacar **avant** de payer la voix (montrer seulement les phrases dites).
5. **Brouillon** (gratuit, voix muette, sans générique) pour vérifier que tous les gestes passent :
   ```bash
   node tuto.mjs scenarios/NN-sujet.yaml --brouillon
   ```
   En cas d'échec, l'outil dit quelle étape/action a raté et enregistre `sortie/<nom>/erreur-etape-N.png` :
   regarder la capture, corriger le sélecteur, relancer.
6. **Voix** → compétence `tuto-odoo-voix`. Pour écouter avant de tourner :
   `node tuto.mjs scenarios/NN-sujet.yaml --seulement-voix` (les voix sont gardées en cache :
   seule une phrase modifiée est refacturée).
7. **Vidéo finale** :
   ```bash
   node tuto.mjs scenarios/NN-sujet.yaml               # voix du scénario (elevenlabs par défaut)
   node tuto.mjs scenarios/NN-sujet.yaml --voix openai
   node tuto.mjs scenarios/NN-sujet.yaml --remonter    # refait seulement le montage (sous-titres, générique, musique)
   ```
8. **Contrôler avant de livrer** : extraire 5–6 images (`ffmpeg -nostdin -ss <t> -i video.mp4 -frames:v 1 t.png` ;
   les temps des étapes sont dans `sortie/<nom>/prise.json`, + 4 s de générique dans la version finale),
   les regarder (curseur visible, bon écran au bon moment, sous-titres lisibles, aucune donnée
   personnelle réelle), et vérifier la durée. Corriger puis relivrer.
   Synchro : le premier sous-titre et le début de la voix (`silencedetect`) doivent coïncider, de même la fin.
   Prononciation des sigles : transcrire les pistes concernées (`sortie/<nom>/voix/NN-elevenlabs-*.mp3`)
   avec l'API speech-to-text d'ElevenLabs (`model_id=scribe_v1`) et vérifier que le mot est reconnu.
9. **Livrer** → compétence `tuto-odoo-montage` (textes YouTube, vignette, version courte verticale).

## Fichiers produits (`sortie/<nom-du-scenario>/`)

| Fichier | À quoi il sert |
|---|---|
| `<titre>.mp4` | la vidéo finale 1920×1080, son normalisé (−16 LUFS) |
| `<titre>.srt` | sous-titres séparés, à téléverser sur YouTube |
| `<titre>-chapitres.txt` | chapitres à coller dans la description YouTube |
| `voix/` | une piste par étape (cache) |
| `prise.json`, `brut/` | le tournage, réutilisé par `--remonter` |

`sortie/` n'est pas versionné : la vidéo finale se range sur Google Drive (dossier « Tutos Odoo »)
ou se publie directement.

## Règles

- **Jamais la base de production avec de vraies personnes.** Filmer une base de démonstration
  (ex. `taagg_tuto`, copie sans données personnelles, remplie avec des noms fictifs : Awa Diop,
  Moussa Ndiaye, Ibou Fall…). Si seule la production est disponible, s'arrêter et le dire.
- Le compte utilisé pour filmer doit être en **français** (Préférences → Langue) pour que l'écran
  corresponde à la voix.
- Un tuto = un seul objectif (« créer un contact », « paramétrer les taxes »). Si la demande
  en contient plusieurs, proposer une série numérotée.
- Ne jamais montrer de mot de passe ni de clé à l'écran : la connexion se fait hors caméra.
- Vérifier l'outil après toute modification de `tuto.mjs` : `npm test` (faux Odoo local).
