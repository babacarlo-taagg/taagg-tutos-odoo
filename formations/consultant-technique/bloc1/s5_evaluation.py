"""Bloc 1 — Section « Évaluation » (section 2711, cours 208) : travail à rendre (2712).
Corrigé testé avec Python 3.12 le 22/11/2026 ; il n est PAS dans ce dépôt (dépôt public) : transmis à Babacar."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

ZONES = """zone,tarif
Plateau,1000
Médina,1000
Mermoz,1500
Parcelles Assainies,2000
Rufisque,3000
Pikine,2500"""

COURSES = """client,zone,poids
Awa Diop,Mermoz,3
Moussa Ndiaye,Plateau,8
Fatou Sarr,Rufisque,12
Ibou Fall,Yoff,2
Khady Ba,Pikine,5.5"""

RESULTAT = """Awa Diop — Mermoz — 1 500 F
Moussa Ndiaye — Plateau — 1 600 F
Fatou Sarr — Rufisque — 4 400 F
Ibou Fall — Yoff — erreur : zone inconnue : Yoff
Khady Ba — Pikine — 2 700 F
Total : 10 200 F (4 courses)"""

LECONS = [
dict(code="1.5.1", id=2712, seq=61, minutes=180,
titre="Travail à rendre : le dépôt Baobab Livraison et le script de tarifs",
description="Le projet de fin de Bloc 1 : un dépôt GitHub propre, un script qui calcule les courses à partir de fichiers CSV, une base Odoo 20 qui démarre.",
html=fiche(
duree="environ 3 h",
titre_exercice="Comment rendre ton travail",
objectif="montrer que ton poste de travail est prêt et que tu sais utiliser Python, SQL et Git sur un vrai petit projet.",
intro="Le gérant de Baobab Livraison veut un premier outil : chaque soir, il exporte la liste des courses du jour dans un fichier, et il veut savoir combien chaque course doit coûter. Tu vas lui livrer ce script, proprement rangé dans un dépôt Git, avec Odoo 20 prêt pour la suite.",
corps=[
("h", "Ce que tu dois livrer"),
("tableau", ["Pièce", "Contenu"], [
  ["1. Le dépôt GitHub <code>baobab_livraison</code>", "Le script, les deux fichiers CSV, un <code>README.md</code>, un <code>.gitignore</code>, un historique propre"],
  ["2. Le script <code>tarifs.py</code>", "Il lit les tarifs et les courses dans deux fichiers CSV et affiche le prix de chaque course et le total"],
  ["3. Le fichier <code>requetes.sql</code>", "Trois requêtes SQL sur la base <code>baobab_sql</code>"],
  ["4. La preuve qu'Odoo 20 tourne", "Une capture d'écran de ta base <code>baobab_dev</code> avec l'application Contacts installée"],
]),
("h", "1. Les deux fichiers de données"),
("p", "Crée ces deux fichiers à la racine de ton dépôt, en UTF-8 :"),
("code", ZONES, "zones.csv"),
("code", COURSES, "courses.csv"),
("h", "2. Le script tarifs.py"),
("p", "Reprends ton script de la leçon « Les fonctions » et fais-le évoluer :"),
("liste", [
  "Les tarifs ne sont plus écrits dans le code : le script les lit dans <code>zones.csv</code>.",
  "Les mêmes règles qu'avant : 5 kg compris, puis 200 F par kilo entamé au-delà.",
  "Une zone inconnue affiche un message d'erreur clair, <b>sans arrêter</b> le script.",
  "À la fin : le total des courses calculées et leur nombre.",
  "Le script se lance ainsi : <code>python3 tarifs.py zones.csv courses.csv</code>.",
]),
("p", "Pour lire un fichier CSV, Python fournit le module <code>csv</code>. Voici comment parcourir les lignes de <code>zones.csv</code> :"),
("code", """import csv

with open("zones.csv", encoding="utf-8", newline="") as fichier:
    for ligne in csv.DictReader(fichier):     # chaque ligne est un dictionnaire
        print(ligne["zone"], int(ligne["tarif"]))""", "Exemple (à adapter)"),
("p", "Pour récupérer les noms de fichiers donnés après <code>tarifs.py</code> : <code>import sys</code>, puis <code>sys.argv[1]</code> et <code>sys.argv[2]</code>."),
("p", "Avec les fichiers ci-dessus, ton script doit afficher exactement :"),
("code", RESULTAT, "Résultat attendu"),
("h", "3. Les requêtes SQL"),
("p", "Dans un fichier <code>requetes.sql</code>, écris trois requêtes sur la base <code>baobab_sql</code> de la section « Les bases de données » :"),
("liste", [
  "le nom et le tarif des zones à plus de 1 000 F, du plus cher au moins cher ;",
  "pour chaque course : le client, le nom de la zone et le tarif (avec un <code>JOIN</code>) ;",
  "le nombre de courses par zone, y compris les zones sans course.",
]),
("h", "4. Les règles du dépôt"),
("liste", [
  "Au moins <b>6 commits</b>, chacun avec un message clair qui dit ce qu'il fait.",
  "Au moins <b>une branche</b> fusionnée dans <code>main</code> (par exemple pour la lecture des CSV).",
  "Un <code>.gitignore</code> : aucun fichier <code>.env</code>, <code>.conf</code> ou <code>__pycache__</code> dans le dépôt.",
  "Un <code>README.md</code> qui explique en quelques lignes à quoi sert le script et comment le lancer.",
]),
("attention", "Aucun secret", "Ton dépôt ne doit contenir aucun mot de passe : ni celui d'Ubuntu, ni le mot de passe maître d'Odoo, ni ton jeton GitHub. Un dépôt avec un secret perd tous les points de la ligne « Git »."),
("h", "Comment tu seras évalué (sur 20)"),
("tableau", ["Critère", "Points"], [
  ["Le script donne exactement le résultat attendu", "6"],
  ["Le code est lisible : fonctions, constantes, noms clairs, commentaires utiles", "3"],
  ["La zone inconnue est gérée sans arrêter le script", "2"],
  ["Les trois requêtes SQL sont justes", "3"],
  ["Git : commits clairs, branche fusionnée, <code>.gitignore</code>, aucun secret", "4"],
  ["Odoo 20 tourne (capture d'écran)", "2"],
]),
],
exercice=[
("liste", [
  "Rends ton dépôt GitHub public, ou invite ton formateur dans le dépôt.",
  "Ajoute dans le dépôt un dossier <code>preuves/</code> avec la capture d'écran d'Odoo.",
  "Envoie le lien de ton dépôt à ton formateur <b>avant l'atelier de la semaine 4</b> : la correction est faite pendant cet atelier.",
]),
("astuce", "Avant d'envoyer", "Clone ton propre dépôt dans un autre dossier (<code>git clone … essai</code>) et lance le script depuis ce clone. S'il marche là, il marchera chez ton formateur."),
],
retenir=[
  "Quatre pièces : le dépôt, le script, les requêtes SQL, la preuve qu'Odoo tourne.",
  "Résultat attendu : 4 courses calculées, 10 200 F, et une erreur propre pour Yoff.",
  "Pas de secret dans le dépôt.",
  "Lien à envoyer au formateur avant l'atelier de la semaine 4.",
]),
quiz=[]),
]
