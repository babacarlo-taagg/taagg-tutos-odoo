---
name: tuto-odoo-montage
description: Finaliser et publier un tutoriel vidéo Odoo TAAGG — générique, sous-titres, musique, contrôle qualité, version courte verticale, vignette, titre/description/chapitres YouTube, rangement sur Drive. Utiliser après le tournage d'un tuto, ou quand Babacar demande de retoucher, exporter, publier ou décliner une vidéo de tuto.
---

# Finition et publication d'un tuto

## Ce que `tuto.mjs` fait déjà

- Générique de début (4 s) : fond bleu TAAGG `#0B415B`, logo, `titre` en blanc, `sous_titre` en vert `#68C184`.
- Générique de fin (4 s) : `fin.message` + `fin.lien`.
- Sous-titres incrustés (2 lignes max) + fichier `.srt` séparé ; `--sans-sous-titres` pour une version propre.
- Musique de fond facultative (`musique:` dans le scénario, en boucle, volume 0,07, fondu final).
- Son normalisé à −16 LUFS, vidéo H.264 1920×1080 30 i/s, prête pour le web (`faststart`).
- `--remonter` refait uniquement le montage à partir du dernier tournage (rapide, aucun coût de voix).

Pour changer le générique pour toute la série : modifier `carton()` et `COULEURS` dans `tuto.mjs`,
puis `npm test` et regarder une image du générique avant de pousser.

## Contrôle qualité (obligatoire avant de livrer)

Extraire une image toutes les ~10 s et les regarder :
```bash
for t in 2 10 20 30 40; do ffmpeg -loglevel error -y -ss $t -i video.mp4 -frames:v 1 -vf scale=960:-1 t$t.png; done
```
Vérifier : le bon écran au bon moment ; curseur visible ; sous-titres lisibles et ne cachant pas
l'élément expliqué ; aucune donnée personnelle réelle ; aucun message d'erreur Odoo ; fin propre.
Écouter le début et la fin (`son.m4a` dans `sortie/<nom>/`).
Musique : uniquement des titres libres de droits (bibliothèque audio YouTube, Pixabay) — noter la source.

## Textes de publication (à livrer avec la vidéo)

- **Titre YouTube** (≤ 70 caractères) : verbe + objet + « dans Odoo » — « Créer un contact dans Odoo (en 1 minute) ».
- **Description** : 2 phrases sur ce qu'on apprend, puis les chapitres (`<titre>-chapitres.txt` ;
  YouTube exige 3 chapitres ou plus, de 10 s minimum, l'outil prévient sinon), puis le lien vers
  le tuto suivant et `taagg-gui.com`.
- **Sous-titres** : téléverser le `.srt` (langue Français) même si la vidéo est sous-titrée.
- **Vignette** 1280×720 : capture du moment clé + titre court en gros (3–4 mots) sur bandeau `#0B415B`.
  ```bash
  ffmpeg -ss 20 -i video.mp4 -frames:v 1 -vf "scale=1280:720,drawbox=y=ih-220:w=iw:h=220:color=0x0B415B@0.92:t=fill,drawtext=fontfile=/chemin/Inter-Bold.otf:text='Créer un contact':fontsize=92:fontcolor=white:x=60:y=h-170" vignette.png
  ```
- **Playlist** : ranger chaque épisode dans sa série (« Les bases d'Odoo », « Paramétrer Odoo »…).

## Version courte verticale (Reels, TikTok, statut WhatsApp)

Recadrer sur la zone utile en 9:16 et garder 30–60 s ; pour ce travail, utiliser la compétence
`montage-video` si elle est disponible, sinon :
```bash
ffmpeg -i video.mp4 -ss 4 -t 45 -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920" -c:a copy court.mp4
```
Ajuster le `crop` (position x) sur la zone où se passe l'action.

## Rangement

`sortie/` n'est pas dans Git. Ranger le MP4, le `.srt`, la vignette et les textes dans le dossier
Google Drive « Tutos Odoo / NN-sujet » (connecteur Google Drive si disponible), et garder le
scénario YAML dans ce dépôt : c'est lui qui permet de refaire la vidéo quand Odoo change d'apparence.
