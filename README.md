# Tutos vidéo Odoo — TAAGG

Fabrique des tutoriels vidéo Odoo **avec voix off** à partir d'un simple scénario texte :
la voix explique, le curseur montre, les sous-titres et le générique TAAGG sont ajoutés automatiquement.

```
scénario YAML ──► voix (ElevenLabs / OpenAI / micro) ──► tournage dans Odoo ──► montage ──► MP4 1080p + .srt + chapitres
```

## Démarrer

```bash
npm install
cp .env.exemple .env          # adresse Odoo de démonstration + clé de voix
npm test                      # essai complet sur un faux Odoo local, voix muette
```
Il faut Node 18+, `ffmpeg`, et Chromium (`npx playwright install chromium`).

## Faire un tuto

```bash
node tuto.mjs explorer /odoo/contacts/new                  # repérer boutons et champs d'un écran
node tuto.mjs scenarios/01-creer-un-contact.yaml --brouillon   # vérifier les gestes (gratuit)
node tuto.mjs scenarios/01-creer-un-contact.yaml --seulement-voix   # écouter la voix
node tuto.mjs scenarios/01-creer-un-contact.yaml           # vidéo finale → sortie/
node tuto.mjs scenarios/01-creer-un-contact.yaml --remonter    # refaire seulement le montage
```

Options : `--voix elevenlabs|openai|fichiers|muet`, `--sans-sous-titres`, `--visible` (voir le navigateur).

## Compétences Claude (`.claude/skills/`)

| Compétence | Rôle |
|---|---|
| `tuto-odoo` | chef d'orchestre : de la demande à la vidéo livrée |
| `tuto-odoo-scenario` | écrire le scénario : pédagogie, texte pour l'oreille, actions, sélecteurs Odoo 20 |
| `tuto-odoo-voix` | choisir et produire la voix (ElevenLabs, OpenAI, HeyGen, micro), prononciation |
| `tuto-odoo-montage` | contrôle qualité, générique, version verticale, vignette, textes YouTube |
| `formation-odoo` | formation complète en capsules de 10 min : programme, structure, données de démo, série |

Il suffit de demander à Claude, dans ce dépôt : « Fais-moi un tuto sur la création d'un devis ».

## Règle d'or

On filme une **base de démonstration**, jamais la production avec de vraies données d'élèves.
