---
name: tuto-odoo-illustrations
description: Ajouter des images aux tutos et capsules vidéo Odoo TAAGG quand l'écran Odoo ne suffit pas à faire comprendre une idée — schémas avec texte (étapes, flèches, montants en francs CFA) faits en HTML aux couleurs TAAGG, et images d'ambiance générées par IA (scènes du Sénégal et d'Afrique de l'Ouest, sans texte). Utiliser dès qu'une capsule parle d'un parcours client, d'un tunnel de vente, d'un circuit d'argent, d'une comparaison, ou quand Babacar parle d'« illustration », « schéma », « image », « visuel » pour un tuto.
---

# Illustrer une capsule

L'écran Odoo montre **où cliquer**. Une illustration montre **ce qui se passe derrière** : le chemin
d'un client sur la boutique, l'argent d'un paiement Wave qui arrive sur le compte, deux options côte à côte.

## 1. Quand illustrer

- **Au plus 1 image par minute de vidéo** (une capsule de 10 min : 10 images maximum, souvent 3 à 6).
- Seulement si l'image **explique** quelque chose que l'écran Odoo ne montre pas :
  un enchaînement (le client commande → paie → est livré), une idée abstraite (le tunnel de vente),
  un circuit (où va l'argent), une comparaison (Wave manuel ou Flutterwave), un ordre de grandeur.
- **Jamais pour décorer** : si la voix est compréhensible sans l'image, pas d'image.
- Typiquement : l'accroche (une image d'ambiance qui pose la situation), le passage d'une idée
  difficile (un schéma), le récapitulatif (un schéma des 3 à 5 points). Le reste du temps : l'écran Odoo.
- Une image reste à l'écran **le temps de la phrase qui l'explique** (5 à 15 s), pas plus.

## 2. Deux sortes d'images

### a) Schémas avec du texte — HTML aux couleurs TAAGG → PNG 1920×1080

Le texte doit être **exact** (libellés, montants, orthographe) : on ne le confie jamais à une IA d'images.

1. Copier `ressources/schema-modele.html` dans `formations/<module>/images/<code>-<sujet>.html`.
2. Écrire le contenu avec les classes de `ressources/schema.css` : `h1` (+ `small` pour la phrase-clé),
   `.rangee` de `.carte` reliées par des `.fleche`, `.carte.forte` pour le résultat, `.chiffre`, `.bandeau`.
   Icônes : petits SVG dessinés dans la page (pas d'emoji, pas d'image téléchargée).
3. Capturer : `node tuto.mjs schema formations/<module>/images/<fichier>.html` → même nom en `.png`.
4. Regarder le PNG (outil Read) avant de l'utiliser.

Règles de dessin :
- Couleurs TAAGG seulement : bleu `#0B415B`, vert `#68C184`, orange `#F2A541` pour un seul point fort.
- Police Inter, **28 px minimum** pour tout texte (lisible sur téléphone), 3 à 5 blocs au plus, 12 mots au plus par bloc.
- **Laisser libre la bande du bas (200 px)** : les sous-titres s'y affichent (`schema.css` le fait déjà).
- Montants en francs CFA écrits comme au Sénégal : `25 000 F CFA` (espace des milliers), jamais d'euros.
- Libellés Odoo recopiés exactement de l'écran (« Ajouter au panier », « Commandes »).
- Exemples tirés de l'entreprise de la formation (Les Délices de Maïmouna, clients fictifs Awa Diop, Moussa Ndiaye…).

### b) Images d'ambiance — générées par IA, **sans aucun texte**

Pour poser une situation : la commerçante qui reçoit une commande, le client qui paie avec son téléphone,
le livreur à moto dans Dakar.

- Outil : connecteur **ElevenLabs** de Claude (`creative_generate_image`), qui génère des images.
  fal.ai est possible aussi si une clé `FAL_KEY` est dans `.env` (pas le cas au 28/10/2026).
- Modèle par défaut : `gpt-image-2.5-sunburst` (bon et peu cher) ; `bytedance-seedream-5-pro`
  si le rendu photo n'est pas assez réaliste.
- Scènes du **Sénégal et d'Afrique de l'Ouest** : rues et boutiques de Dakar, marchés, quartiers, intérieurs
  simples ; **personnages africains**, habillés comme au quotidien à Dakar.
- **Aucune vraie marque ni vraie personne** : pas de logo Wave, Orange, Odoo… ; écrans de téléphone
  flous ou vus de dos ; pas de visage de personnalité.
- **Aucun texte dans l'image** (enseignes, écrans, emballages) : l'IA écrit mal et on ne peut pas corriger.
- **Même style pour toute la formation** : reprendre mot pour mot le « style commun » ci-dessous
  à la fin de chaque demande, et garder les mêmes personnages récurrents décrits pareil.

Style commun (formation E-Business) :
> Photorealistic documentary photo, Dakar, Senegal, natural warm daylight, soft shallow depth of field,
> realistic everyday clothing, authentic West African setting, 16:9 framing, no text, no letters,
> no logos, no brand names, phone screens blurred or facing away.

Personnages récurrents (E-Business) :
- **Maïmouna** : pâtissière sénégalaise d'environ 35 ans, foulard coloré, tablier blanc, dans sa petite pâtisserie.
- **Awa** : cliente d'environ 25 ans, étudiante, commande depuis son téléphone.
- **Ibou** : livreur d'environ 30 ans, casque, moto, sac isotherme.

Après génération : choisir la meilleure des variantes, la recadrer en 1920×1080
(`ffmpeg -i in.png -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" out.png`),
la regarder (mains, visages, aucun texte parasite) et noter dans `images/README.md` : fichier, modèle,
demande (prompt) utilisée, date.

## 3. Rangement, noms, validation

```
formations/<module>/images/
  eb-01-parcours-client.html   source d'un schéma (versionnée : on peut corriger le texte)
  eb-01-parcours-client.png    l'image utilisée dans la vidéo
  eb-01-ambiance-commande.png  image IA (déjà recadrée)
  README.md                    liste des images IA : modèle, prompt, date, validée oui/non
```

- Nom : `<code capsule en minuscules>-<sujet court>.png` (`eb-03-pages-confiance.png`).
- Les PNG sont légers (≈ 100–500 Ko) : ils vont dans Git avec le scénario, pour pouvoir refaire la vidéo.
- **Babacar valide toutes les images avant le tournage final** : les envoyer avec le brouillon muet
  (planche ou fichiers), et noter « validée » dans `README.md` après son accord.

## 4. Dans le scénario

```yaml
- texte: >
    Voici le chemin de votre cliente : elle découvre un gâteau, le met dans son panier,
    choisit la livraison, paie, et reçoit sa confirmation.
  actions:
    - illustration: images/eb-01-parcours-client.png   # relatif au fichier du scénario
      zoom: 1.04        # léger zoom avant pendant l'affichage (1 = immobile ; défaut 1,06)
                        # sans « duree » : l'image reste jusqu'à la fin de la phrase, puis s'efface
```
`duree: 6` fixe un temps d'affichage précis ; l'action suivante de l'étape reprend ensuite sur l'écran Odoo.
Les schémas chargés de texte : `zoom: 1` ou `1.03` (le texte doit rester net) ; les images d'ambiance : 1,06 à 1,10.

## 5. Coûts (à annoncer avant de lancer une série)

Prix relevés le 28/10/2026 sur le connecteur ElevenLabs, pour **4 variantes** d'une même image :

| Modèle | Crédits | Prix | ≈ F CFA |
|---|---|---|---|
| `gpt-image-2.5-sunburst` | ≈ 760 | ≈ 0,14 $ | ≈ 80 F |
| `bytedance-seedream-5-pro` | ≈ 3 300 | ≈ 0,60 $ | ≈ 350 F |

- Toujours estimer d'abord (`estimate_only: true`), puis annoncer à Babacar le total de la série
  (nombre d'images × prix) et **attendre son accord** avant de générer.
- Ne jamais relancer une génération pour « réessayer » : chaque appel est facturé.
- Les schémas HTML sont gratuits.
