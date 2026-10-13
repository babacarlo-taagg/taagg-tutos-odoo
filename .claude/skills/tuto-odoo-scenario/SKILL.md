---
name: tuto-odoo-scenario
description: Écrire le scénario YAML d'un tutoriel vidéo Odoo (texte de la voix off + gestes à l'écran, étape par étape) pour l'outil tuto.mjs. Utiliser pour rédiger, corriger ou découper un tuto Odoo, trouver le bon sélecteur d'un bouton ou d'un champ Odoo 20, ou quand un brouillon échoue sur une action.
---

# Écrire un scénario de tuto Odoo

Un scénario = un fichier `scenarios/NN-sujet.yaml`. Modèle complet : `scenarios/01-creer-un-contact.yaml`.

## Structure pédagogique (toujours la même)

1. **Accroche** (1 étape, ~8 s) : ce qu'on va savoir faire à la fin. « Dans ce tutoriel, nous allons voir… »
2. **Chemin** : où on va dans Odoo (appli, menu).
3. **Les gestes** : une étape par idée, un geste principal par étape.
4. **Le résultat** : montrer que ça a marché (enregistrement, la fiche apparaît dans la liste).
5. **Conclusion** (1 étape) : rappel en une phrase + annonce du tuto suivant.

## Écrire pour l'oreille

- Phrases courtes (≤ 20 mots), vouvoiement, présent, voix active : « Cliquez sur Nouveau. »
- **Dire ce qu'on voit au moment où on le voit** : le texte d'une étape est dit *pendant* ses actions.
- Nommer les boutons exactement comme à l'écran (libellés Odoo en français), sans jargon technique
  (pas de « many2one », « enregistrement », « vue formulaire » → « la liste », « la fiche »).
- Expliquer le **pourquoi** d'un paramétrage en une phrase (« Ce réglage évite de… »).
- Chiffres et sigles écrits comme ils doivent être dits, ou ajoutés dans `prononciation`.
- 1 minute de vidéo ≈ 150 mots de texte.

## Format

```yaml
titre: Paramétrer les taxes de vente        # générique de début + nom du fichier
sous_titre: Comptabilité — épisode 3        # sous le titre (facultatif)
depart: /odoo                               # page ouverte avant la première étape
ecran: [1600, 900]                          # taille du navigateur (agrandi en 1080p : texte bien lisible)
voix: {moteur: elevenlabs, vitesse: 1.0}    # elevenlabs | openai | fichiers | muet
prononciation: {TAAGG: Tag, FCFA: "francs CFA", TVA: "té-vé-a"}
musique: ../musiques/douce.mp3              # facultatif, relatif au scénario
volume_musique: 0.07
fin: {message: "À vous de jouer !", lien: taagg-gui.com}

etapes:
  - chapitre: Ouvrir la configuration       # facultatif → chapitre YouTube (3 minimum, 10 s minimum chacun)
    texte: Ouvrez l'application Comptabilité, puis le menu Configuration.
    apres: 0.6                              # silence après la phrase (s), défaut 0,6
    actions:
      - menu: Comptabilité > Configuration > Taxes
```

## Actions disponibles

| Action | Effet |
|---|---|
| `aller: /odoo/contacts` | ouvre une adresse (relative à `ODOO_URL`) |
| `menu: Ventes > Commandes > Devis` | écran d'accueil → clique l'appli → puis chaque menu du haut |
| `bouton: Nouveau` | clique le bouton qui porte ce libellé |
| `cliquer_texte: Notes internes` | clique le premier élément qui affiche exactement ce texte (`exact: false` pour « contient ») |
| `cliquer: '<sélecteur>'` | clique un sélecteur Playwright (`.o_form_button_save`, `text=Archiver`, `button:has-text("Confirmer")`) |
| `champ: name` + `taper: Awa Diop` | tape lettre par lettre dans le champ technique `name` (`entree: true` pour valider) |
| `choisir: {champ: country_id, valeur: Sénégal}` | liste déroulante ou champ relié : tape puis choisit dans la liste |
| `cocher: is_company` | coche une case |
| `onglet: Notes internes` | ouvre un onglet de la fiche |
| `rechercher: Awa` | tape dans la barre de recherche + Entrée |
| `enregistrer: oui` | clique l'icône Enregistrer de la fiche |
| `surligner: '<sélecteur>'` / `surligner_champ: email` + `duree: 2` | cadre vert + fond assombri autour de l'élément |
| `survoler: '<sélecteur>'` | déplace le curseur dessus (pour pointer sans cliquer) |
| `touche: Escape` | appuie sur une touche |
| `defiler: 400` ou `defiler: '<sélecteur>'` | fait défiler la page |
| `attendre: 1.5` | pause (secondes) |

Le curseur glisse comme une main, chaque clic fait une onde verte : pas besoin d'en rajouter.

## Trouver les bons noms (Odoo 20)

- `node tuto.mjs explorer <chemin>` liste les **champs techniques** (`name — Nom (o_field_char)`),
  les boutons, onglets et menus, et enregistre `sortie/explorer.png`. Toujours partir de là.
- Champs : le nom technique est l'attribut `name` de `.o_field_widget` (stable, ne dépend pas de la langue).
- Repères Odoo 20 utiles : `.o_form_button_save` (enregistrer), `.o_form_button_cancel` (annuler),
  `.o_list_button_add` / `bouton: Nouveau`, `.o_searchview_input`, `.o_notebook .nav-link`,
  `.o_app` (icônes de l'accueil), `.o_menu_sections` (menus du haut), `.o-autocomplete--dropdown-item`,
  `.o_statusbar_buttons button` (boutons de la barre d'état : Confirmer, Annuler…),
  `.o_cp_action_menus` (engrenage Actions), `.modal-footer .btn-primary` (valider une fenêtre).
- Un **paramètre** se trouve souvent dans Paramètres (`aller: /odoo/settings`) : utiliser
  `rechercher` n'y marche pas, préférer `cliquer_texte` sur le titre de la section puis `surligner`.
- Modules TAAGG (`taagg_*`) : les noms de champs sont dans le dépôt `babacarlo-taagg/taagg-odoo`
  (`addons/<module>/models/*.py`, vues dans `views/*.xml`).

## Quand le brouillon échoue

L'outil s'arrête sur l'étape fautive et enregistre `erreur-etape-N.png`. Causes habituelles :
1. Le bouton porte un autre libellé → relancer `explorer` sur cette page.
2. L'élément n'est pas encore affiché → ajouter `attendre: 1` avant, ou passer par l'onglet qui le contient.
3. Plusieurs éléments correspondent → préciser le sélecteur (`.modal .btn-primary` plutôt que `.btn-primary`).
4. Les données de la base de démo ont changé (fiche déjà créée) → nettoyer la base ou changer le nom tapé.
