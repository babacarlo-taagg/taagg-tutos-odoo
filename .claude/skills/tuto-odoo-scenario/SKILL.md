---
name: tuto-odoo-scenario
description: Écrire le scénario YAML d'un tutoriel vidéo Odoo (texte de la voix off + gestes à l'écran, étape par étape) pour l'outil tuto.mjs. Utiliser pour rédiger, corriger ou découper un tuto Odoo, trouver le bon sélecteur d'un bouton ou d'un champ Odoo (19 ou 20), ou quand un brouillon échoue sur une action.
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
  - partie: "2. Créer une taxe"             # bandeau en haut à droite pendant 5 s (+ chapitre YouTube)
    texte: Créons maintenant notre propre taxe.
    actions:
      - bouton: Nouveau
```

## Actions disponibles

| Action | Effet |
|---|---|
| `aller: /odoo/contacts` | ouvre une adresse (relative à `ODOO_URL`) |
| `menu: Ventes > Commandes > Devis` | écran d'accueil → clique l'appli → puis chaque menu du haut |
| `ouvrir_menu: Configuration` | déplie un menu du haut sans rien choisir (pour faire visiter son contenu) |
| `survoler_texte: Plan comptable` | pointe le curseur sur un texte visible (d'abord dans le menu déplié) |
| `surligner_texte: Non payé` + `duree: 3` | cadre vert autour d'un texte visible |
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

## Mode terminal (filmer des commandes Linux, Python, Git…)

Pour les leçons techniques (parcours « Consultant technique Odoo ») qui se passent dans un terminal et non dans Odoo.
Exemple complet : `scenarios/02-terminal-premiers-pas.yaml`.

```yaml
titre: Se déplacer dans le terminal
mode: terminal                  # au lieu de filmer Odoo, filme un faux terminal Linux
terminal:
  utilisateur: awa              # invite affichée : awa@baobab:~$
  machine: baobab
  titre: Terminal — awa@baobab  # facultatif (barre du haut)
  dossier: ~/essai              # facultatif : dossier où lancer les commandes « executer » ;
                                # par défaut un dossier d'essai vide, recréé à chaque tournage
```

| Action (mode terminal) | Effet |
|---|---|
| `commande: ls -l` + `executer: oui` | tape la commande lettre par lettre, la **lance pour de vrai** (bash, dans le dossier d'essai) et affiche son vrai résultat ; les `cd` font évoluer l'invite |
| `commande: pwd` + `sortie: /home/awa` | tape la commande et affiche le résultat écrit dans le scénario (rien n'est lancé) ; `erreur: oui` l'affiche en rouge |
| `afficher: "texte"` | affiche des lignes sans commande (ex. journal qui défile) |
| `surligner_ligne: scripts` + `duree: 2` | cadre vert autour de la dernière ligne de résultat qui contient ce texte |
| `editeur: {fichier: tarifs.py, contenu: "…"}` | ouvre un éditeur façon nano et y tape le contenu ; `deja: "…"` = texte déjà présent (affiché d'un coup) ; `taille: 16` = police plus petite pour un long fichier (≈ 22 lignes visibles en taille 20, 28 en taille 16) ; `enregistrer: oui` écrit aussi le fichier (pour l'exécuter ensuite) |
| `fermer_editeur: oui` | referme l'éditeur (le mettre au début de l'étape suivante pour laisser lire le fichier) |
| `effacer: oui` | vide l'écran (comme `clear`) |
| `invite: "(Pdb)"` | change l'invite (débogueur, `psql` : `baobab_sql=>`, PowerShell : `PS C:\Users\awa>`) ; `invite: normale` revient à `awa@baobab:~$` |
| `fenetre: Windows PowerShell` | change le titre de la fenêtre |
| `delai: 40` | (sur `commande` ou `editeur`) millisecondes par lettre tapée |
| `attendre`, `touche` | comme en mode Odoo |

Règles :
- **Préférer `executer: oui`** : le résultat affiché est alors le vrai, jamais inventé. Utiliser `sortie` seulement pour
  ce qui ne peut pas tourner sur la machine de tournage (`sudo …`, `apt install`, chemins de l'apprenant comme `/home/awa`).
- Jamais de `sudo`, de commande qui modifie la machine, ni de secret dans une commande « executer ».
- Le dossier d'essai et la sortie montrent le compte de l'apprenant (`awa awa` dans `ls -l`), pas celui du serveur.
- Les actions d'Odoo (`menu`, `bouton`, `champ`…) sont refusées en mode terminal.
- L'écran affiche environ 115 caractères par ligne et 20 lignes au-dessus des sous-titres : au-delà, la ligne passe à la suivante (comme dans un vrai terminal).
- Si Playwright ne trouve pas son navigateur : `TUTO_CHROMIUM=/chemin/vers/chrome node tuto.mjs …`.

## Trouver les bons noms (Odoo 19 et 20, mêmes repères)

- `node tuto.mjs explorer <chemin>` liste les **champs techniques** (`name — Nom (o_field_char)`),
  les boutons, onglets et menus, et enregistre `sortie/explorer.png`. Toujours partir de là.
- La base de tournage est en Odoo 19 **Enterprise** (Studio, Documents, Paie… installés) : l'interface diffère un peu de la Community 20 de TAAGG ; toujours vérifier avec `explorer`.
- Avec la clé API, `fields_get` sur le modèle donne la liste exacte des champs et leur type.
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

## Visiter un menu (capsules « tour d'horizon »)

```yaml
- texte: Le menu Clients regroupe les factures, les avoirs et les paiements.
  actions:
    - ouvrir_menu: Clients
    - survoler_texte: Factures clients
    - survoler_texte: Avoirs
- texte: Ouvrons les factures clients.
  actions:
    - cliquer: '.o-dropdown--menu .dropdown-item:has-text("Factures clients")'
```
Les textes sont cherchés « contenant » (sans tenir compte des majuscules) : choisir un texte qui
n'apparaît qu'une fois à l'écran. Retour en arrière : `cliquer: '.breadcrumb-item a:has-text("Factures clients")'`.

## Quand le brouillon échoue

Lancer avec `TUTO_TRACE=1` pour voir l'heure et la durée de chaque action.


L'outil s'arrête sur l'étape fautive et enregistre `erreur-etape-N.png`. Causes habituelles :
1. Le bouton porte un autre libellé → relancer `explorer` sur cette page.
2. L'élément n'est pas encore affiché → ajouter `attendre: 1` avant, ou passer par l'onglet qui le contient.
3. Plusieurs éléments correspondent → préciser le sélecteur (`.modal .btn-primary` plutôt que `.btn-primary`).
4. Les données de la base de démo ont changé (fiche déjà créée) → nettoyer la base ou changer le nom tapé.
