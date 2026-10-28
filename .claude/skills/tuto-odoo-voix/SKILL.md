---
name: tuto-odoo-voix
description: Choisir, régler et produire la voix off française des tutoriels vidéo Odoo (ElevenLabs, OpenAI, HeyGen, ou voix de Babacar enregistrée au micro), corriger une prononciation ou un rythme. Utiliser dès qu'il est question de voix, narration, prononciation, débit, clonage de voix ou enregistrement micro pour un tuto.
---

# La voix off des tutos

`tuto.mjs` produit une piste audio par étape, mesure sa durée, puis tourne l'écran à ce rythme.
Les pistes sont gardées en cache (`sortie/<nom>/voix/`) : modifier une phrase ne refait que celle-là.

## Les quatre moteurs (`--voix` ou `voix.moteur` dans le scénario)

| Moteur | Quand | Réglage dans `.env` |
|---|---|---|
| `elevenlabs` (défaut) | le plus naturel en français ; peut cloner la voix de Babacar | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (+ `ELEVENLABS_MODELE`, défaut `eleven_multilingual_v2`) |
| `openai` | bon et moins cher | `OPENAI_API_KEY`, `OPENAI_VOIX` (défaut `coral`) |
| `fichiers` | voix enregistrée au micro, ou produite ailleurs (HeyGen) | rien : déposer `scenarios/<nom>.voix/01.mp3`, `02.mp3`… (un fichier par étape, mp3/wav/m4a/ogg) |
| `muet` | brouillons et essais, gratuit | rien |

Ne jamais écrire de clé dans un fichier versionné : seulement dans `.env` (ignoré par Git).
Si la clé manque, l'outil le dit clairement : demander à Babacar de la mettre dans `.env`, ne pas la lui faire coller dans la conversation.

## Voix retenue : celle de Babacar (décision du 28 octobre 2026)

Les formations TAAGG utilisent **la voix de Babacar LO**, clonée dans ElevenLabs :
- échantillon nettoyé dans `voix-source/babacar-lo-echantillon.mp3` (3 min, jamais versionné : donnée personnelle) ;
- clonage : `node tuto.mjs cloner-voix voix-source/babacar-lo-echantillon.mp3 "Babacar LO"`
  (écrit `ELEVENLABS_VOICE_ID` dans `.env`) ;
- il faut `ELEVENLABS_API_KEY` dans `.env` et `api.elevenlabs.io` dans les domaines autorisés de l'environnement cloud.
- Voix clonée dans le compte : **« Babacar LO (naturel) »**, identifiant `YqeSIPMrI8Xhr78yPGXy`
  (à mettre dans `ELEVENLABS_VOICE_ID` ; la retrouver au besoin avec `GET /v2/voices?voice_type=personal`).
- Ce clone imite une parole naturelle : il glisse parfois un « euh » ou répète un mot (« tout le, tout le travail »).
  **Toujours vérifier par transcription** avant de livrer (voir « Contrôler la voix » plus bas).
- Nettoyage d'un nouvel enregistrement avant clonage :
  `ffmpeg -i brut.m4a -ac 1 -af "highpass=f=70,afftdn=nf=-30,loudnorm=I=-18:TP=-2:LRA=11,aresample=44100,alimiter=limit=0.7:level=false" echantillon.mp3`

## Choisir la voix (une fois pour toute la série)

- Même voix, même vitesse pour tous les épisodes d'une série.
- ElevenLabs : tester 2–3 voix françaises sur la même phrase d'accroche, faire choisir Babacar.
  Pour une voix « maison », Babacar enregistre 1 à 3 minutes propres et crée un clone dans
  ElevenLabs (Voices → Add voice) ; on récupère son identifiant dans `ELEVENLABS_VOICE_ID`.
- Vitesse : `voix.vitesse` entre 0,9 (paramétrage complexe) et 1,1 (gestes simples).

## Voix HeyGen (via le connecteur HeyGen de Claude)

Si Babacar préfère une voix de son compte HeyGen : `list_voices` (langue French) pour choisir,
puis **une** génération `create_speech` par étape avec le texte *dit* (après `prononciation`),
téléchargement de chaque `audio_url` dans `scenarios/<nom>.voix/NN.mp3`, puis `--voix fichiers`.
Une génération = un appel : demander l'accord avant de lancer toute la série.

## Enregistrer la voix de Babacar au micro

1. Générer d'abord un brouillon (`--brouillon`) et le lui envoyer avec le texte numéroté par étape.
2. Il enregistre une phrase par fichier (`01.m4a`, `02.m4a`…) avec son téléphone, dans une pièce
   calme, téléphone à 20 cm, sans musique de fond ; un petit blanc au début et à la fin suffit.
3. Nettoyer si besoin : `ffmpeg -i 01.m4a -af "highpass=f=80,afftdn=nf=-25,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse" 01.mp3`
4. Ranger dans `scenarios/<nom>.voix/` et lancer `--voix fichiers`.

## Contrôler la voix (obligatoire avant de livrer)

Faire retranscrire la piste finale par ElevenLabs (quelques centimes) et la comparer au texte :
```bash
ffmpeg -i sortie/<nom>/son.m4a -ac 1 -b:a 64k son.mp3
curl -sS -H "xi-api-key: $ELEVENLABS_API_KEY" -F model_id=scribe_v1 -F language_code=fra -F file=@son.mp3 \
  https://api.elevenlabs.io/v1/speech-to-text
```
Chercher : « euh », mots répétés, sigles mal dits, noms propres déformés. Pour refaire une seule phrase :
déplacer son fichier `sortie/<nom>/voix/NN-elevenlabs-*.mp3` (NN = numéro de l'étape, en partant de 1)
dans `sortie/<nom>/voix-ecartees/`, relancer `--seulement-voix`, retranscrire ce fichier, puis retourner la vidéo.

## Prononciation et rythme

- Règles connues : `TAAGG School: l'école Tag` (sinon on entend « Tax School »), `TAAGG: Tag`,
  `E-Business: i-business`, `eCommerce: e-commerce`, `FCFA: francs CFA`.

- `prononciation:` dans le scénario remplace un mot écrit par sa forme dite, **pour la voix seulement**
  (les sous-titres gardent l'orthographe) : `TAAGG: Tag`, `FCFA: francs CFA`, `CRM: cé-erre-èm`.
- Un mot mal lu ? Écouter avec `--seulement-voix`, ajouter la règle, relancer : seule la phrase concernée est refaite.
- Respiration entre étapes : `apres: 1.2` sur l'étape (défaut 0,6 s).
- Phrase trop longue pour les gestes ? La couper en deux étapes plutôt qu'accélérer la voix.
- Le son final est normalisé à −16 LUFS (norme YouTube/podcast) : pas besoin de régler le volume.
