"""Bloc 1 — Section « Semaine 0 — Remise à niveau Python (facultatif) » (section 2698, cours 208).
Code testé avec Python 3.12 le 21/11/2026."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

LECONS = [
# ---------------------------------------------------------------- 1.0.1
dict(code="1.0.1", id=None, seq=11, minutes=10,
titre="Bienvenue : le parcours, Baobab Livraison et ta méthode de travail",
description="Ce que tu vas construire pendant les 5 blocs techniques, et comment travailler pour réussir.",
html=fiche(
objectif="savoir ce que tu vas construire et comment t'organiser pour suivre le parcours.",
intro="Bienvenue dans la partie technique du parcours ! Pendant cinq blocs, tu ne vas pas seulement lire du code : tu vas construire, pas à pas, un vrai module Odoo pour une entreprise.",
corps=[
("h", "Le fil rouge : Baobab Livraison"),
("p", "Baobab Livraison est une petite société (imaginaire) de livraison à moto à Dakar. Ses livreurs transportent des colis entre les quartiers : Plateau, Médina, Mermoz, Parcelles Assainies, jusqu'à Rufisque. Aujourd'hui, tout est noté dans un cahier et sur WhatsApp. Le gérant veut passer à Odoo."),
("p", "Ton travail, tout au long du parcours : lui construire le module <code>baobab_livraison</code>."),
("tableau", ["Bloc", "Ce que tu construis"], [
  ["1 — Fondations", "Ton poste de travail, un dépôt Git, un script Python qui calcule le prix d'une course, Odoo 20 qui tourne sur ton ordinateur"],
  ["2 — Framework", "Le module : les courses, les zones, les livreurs, les calculs, le lien avec les ventes"],
  ["3 — Interface", "Les écrans, le bordereau PDF, la page « Suivre mon colis »"],
  ["4 — Intégrations", "L'API de l'appli des livreurs, le paiement mobile, les droits d'accès"],
  ["5 — Déploiement", "Les tests, la mise en ligne, les sauvegardes, la surveillance"],
]),
("h", "Comment est construite chaque leçon"),
("liste", [
  "<b>Un objectif</b> en haut de page : ce que tu sais faire à la fin.",
  "<b>Une explication courte</b> avec du code commenté. Tape le code toi-même, ne le copie pas : c'est en tapant qu'on apprend.",
  "<b>Un exercice</b> qui fait avancer Baobab Livraison.",
  "<b>« À retenir »</b> : l'essentiel en quelques lignes, à relire avant le quiz.",
  "<b>Un quiz de 3 questions</b> pour vérifier que c'est compris.",
]),
("h", "Ta méthode de travail"),
("liste", [
  "Fixe-toi des créneaux réguliers : une heure par jour vaut mieux que sept heures le dimanche.",
  "Garde un carnet (papier ou fichier) : note les commandes nouvelles et les erreurs que tu as résolues.",
  "Quand tu bloques plus de 20 minutes : relis le message d'erreur en entier, cherche-le, puis pose ta question en commentaire sous la leçon, avec le message exact.",
  "Chaque bloc se termine par un travail à rendre : ne le laisse pas pour la dernière nuit.",
]),
("astuce", "Le bon réflexe", "Une erreur n'est pas un échec : c'est Odoo ou Python qui t'explique ce qui ne va pas. Les développeurs passent une bonne partie de leur temps à lire des messages d'erreur."),
("h", "Ce dont tu as besoin"),
("liste", [
  "Un ordinateur portable (8 Go de mémoire conseillés) sous Windows, Linux ou macOS.",
  "Une connexion Internet pour installer les outils (ensuite, tu peux travailler hors ligne).",
  "Un compte GitHub gratuit (on le crée dans la section Git).",
]),
("version", "Ce parcours utilise <b>Odoo 20 Community</b>, la version libre et gratuite. Beaucoup d'entreprises utilisent encore Odoo 17, 18 ou 19 : quand une chose change d'une version à l'autre, un encadré comme celui-ci te le signale."),
],
exercice=[
("p", "Ouvre ton carnet et écris : (1) les créneaux de la semaine où tu travailleras sur le parcours, (2) le système de ton ordinateur (Windows, Linux ou macOS) et sa mémoire (Windows : Paramètres → Système → Informations système)."),
("p", "Réfléchis aussi à cette question : chez Baobab Livraison, quelles informations faut-il noter pour chaque course ? Fais une liste. Tu la compareras au Bloc 2 avec les champs du modèle <code>baobab.course</code>."),
],
retenir=[
  "Tu construis un seul module, <code>baobab_livraison</code>, de bloc en bloc.",
  "Chaque leçon : objectif, explication, exercice, « À retenir », quiz de 3 questions.",
  "On travaille sur Odoo 20 Community ; les différences avec les versions précédentes sont signalées.",
  "Une erreur se lit en entier avant de demander de l'aide.",
]),
quiz=[
("Quel module vas-tu construire pendant le parcours ?", [
  ("baobab_livraison, pour une société de livraison à moto", V, "Oui : c'est le fil rouge des 5 blocs."),
  ("Le module Comptabilité d'Odoo", F, "Non : la comptabilité existe déjà dans Odoo. Toi, tu construis un module sur mesure."),
  ("Un site web de vente en ligne", F, "Non : le fil rouge est la gestion des courses de livraison."),
]),
("Quelle version d'Odoo utilise ce parcours ?", [
  ("Odoo 20 Community", V, "Oui. Les différences avec les versions 18 et 19 sont signalées dans les leçons."),
  ("Odoo 16 Enterprise", F, "Non : on travaille sur la version la plus récente, en édition Community (libre)."),
  ("N'importe laquelle, tout est identique", F, "Non : certaines choses changent d'une version à l'autre, d'où les encadrés « Selon ta version »."),
]),
("Tu bloques sur une erreur depuis 25 minutes. Que fais-tu en premier ?", [
  ("Je relis le message d'erreur en entier, puis je pose ma question avec le message exact", V, "Oui : le message exact permet qu'on t'aide vite."),
  ("J'abandonne la leçon", F, "Non : bloquer fait partie du métier. Lis l'erreur, cherche, puis demande."),
  ("Je réinstalle tout", F, "Rarement utile : comprends d'abord ce que dit l'erreur."),
]),
]),

# ---------------------------------------------------------------- 1.0.2
dict(code="1.0.2", id=2699, seq=12, minutes=10,
titre="Installer Python et écrire ton premier script",
description="Installer Python 3.12 et lancer un premier programme dans le terminal.",
html=fiche(
objectif="installer Python 3.12 et lancer ton premier script dans le terminal.",
intro="Odoo est écrit en Python. Avant d'écrire un module, il faut que Python soit installé et que tu saches lancer un fichier <code>.py</code>.",
corps=[
("h", "Quelle version installer ?"),
("p", "Odoo 20 demande <b>Python 3.12 ou plus récent</b>. Vérifie ce que tu as déjà dans un terminal :"),
("code", "python3 --version", "Terminal (Linux, macOS ou WSL)"),
("p", "Si tu vois <code>Python 3.12.3</code> ou un numéro plus grand, c'est bon. Sinon :"),
("liste", [
  "<b>Ubuntu 24.04</b> (ou WSL avec Ubuntu 24.04, qu'on installe dans la section Linux) : Python 3.12 est déjà là.",
  "<b>Windows</b> : on travaillera dans WSL (Linux dans Windows). En attendant, tu peux installer Python depuis python.org en cochant <i>Add Python to PATH</i>.",
  "<b>macOS</b> : installe Python 3.12 depuis python.org.",
]),
("version", "Odoo 19 acceptait Python 3.10. <b>Odoo 20 exige Python 3.12</b> au minimum : un serveur trop ancien ne pourra pas faire tourner Odoo 20."),
("h", "Ton premier script"),
("p", "Crée un dossier de travail et un fichier <code>premier.py</code> :"),
("code", """mkdir -p ~/baobab
cd ~/baobab
nano premier.py""", "Terminal"),
("p", "Dans l'éditeur, tape cette ligne, puis enregistre (Ctrl+O, Entrée) et quitte (Ctrl+X) :"),
("code", """print("Bonjour Baobab Livraison !")""", "premier.py"),
("p", "Lance-le :"),
("code", """python3 premier.py
Bonjour Baobab Livraison !""", "Terminal (la 2e ligne est ce qui s'affiche)"),
("p", "<code>print()</code> affiche du texte. Le texte entre guillemets s'appelle une <b>chaîne de caractères</b>."),
("h", "La console interactive"),
("p", "Tape seulement <code>python3</code> : tu entres dans une console où chaque ligne s'exécute tout de suite. Pratique pour essayer. Pour sortir : <code>exit()</code>."),
("code", """>>> 1500 * 3
4500
>>> exit()""", "Console Python"),
("attention", "Attention à l'indentation", "En Python, les espaces au début des lignes ont un sens. Une ligne décalée par erreur donne <code>IndentationError</code>. Règle : 4 espaces par niveau, jamais de tabulations mélangées."),
],
exercice=[
("p", "Écris un script <code>presentation.py</code> qui affiche trois lignes : le nom de la société (Baobab Livraison), sa ville (Dakar) et une phrase de ton choix. Lance-le."),
("p", "Puis, dans la console <code>python3</code>, calcule le prix de 12 courses à 1 500 F."),
],
retenir=[
  "Odoo 20 demande Python 3.12 ou plus : vérifie avec <code>python3 --version</code>.",
  "On lance un script avec <code>python3 nom_du_fichier.py</code>.",
  "<code>python3</code> seul ouvre une console pour essayer ; <code>exit()</code> pour sortir.",
  "En Python, l'indentation (4 espaces) fait partie du code.",
]),
quiz=[
("Quelle version minimale de Python faut-il pour Odoo 20 ?", [
  ("Python 3.12", V, "Oui. Odoo 19 acceptait encore 3.10."),
  ("Python 2.7", F, "Non : Python 2 n'est plus utilisé par Odoo depuis longtemps."),
  ("Python 3.8", F, "Non : trop ancien pour Odoo 20."),
]),
("Quelle commande lance le fichier premier.py ?", [
  ("python3 premier.py", V, "Oui."),
  ("run premier.py", F, "Cette commande n'existe pas."),
  ("print premier.py", F, "Non : print() est une fonction Python, pas une commande du terminal."),
]),
("Python affiche « IndentationError ». Que faut-il vérifier ?", [
  ("Les espaces au début des lignes", V, "Oui : en Python, l'indentation fait partie du code."),
  ("La connexion Internet", F, "Non, rien à voir."),
  ("La version d'Odoo", F, "Non : c'est une erreur de mise en forme du code Python."),
]),
]),

# ---------------------------------------------------------------- 1.0.3
dict(code="1.0.3", id=None, seq=13, minutes=10,
titre="Variables, nombres et textes",
description="Ranger des informations dans des variables, calculer un prix, afficher un message clair.",
html=fiche(
objectif="ranger des informations dans des variables, faire des calculs et afficher un message lisible.",
intro="Une course de Baobab Livraison, c'est un client, une zone, un prix, un poids. En Python, chaque information se range dans une <b>variable</b>.",
corps=[
("h", "Créer des variables"),
("code", """client = "Awa Diop"   # du texte (str)
zone = "Mermoz"
prix = 1500           # un nombre entier (int)
poids = 3.5           # un nombre à virgule (float) : on écrit un point, pas une virgule
livree = False        # vrai ou faux (bool) : True ou False

print(type(prix), type(poids), type(client), type(livree))""", "variables.py"),
("code", "<class 'int'> <class 'float'> <class 'str'> <class 'bool'>", "Résultat"),
("p", "Le signe <code>=</code> veut dire « ranger dans ». Tout ce qui suit <code>#</code> est un commentaire : Python l'ignore."),
("h", "Calculer"),
("code", """print(1500 * 2)      # 3000
print(7 / 2)         # 3.5  division normale
print(7 // 2)        # 3    division entière
print(7 % 2)         # 1    reste de la division
print(round(2.675, 2))  # 2.67 et non 2.68 !""", "Console Python"),
("attention", "Les nombres à virgule ne sont pas exacts", "<code>round(2.675, 2)</code> donne 2.67 : l'ordinateur range 2.675 comme 2.67499999… Pour l'argent, Odoo utilise ses propres règles d'arrondi (on les verra). Le franc CFA n'a pas de centimes : on travaille en nombres entiers."),
("h", "Afficher un message clair : les f-strings"),
("p", "Mets un <code>f</code> devant les guillemets et des variables entre accolades :"),
("code", """print(f"Course pour {client} à {zone} : {prix} F")
# Course pour Awa Diop à Mermoz : 1500 F

print(f"{1250000:,} F".replace(",", " "))
# 1 250 000 F   (séparateur de milliers à la française)""", "Console Python"),
("h", "Quelques outils sur le texte"),
("code", """print(client.upper())   # AWA DIOP
print(len(client))      # 8 caractères
print("10" + "5")       # 105 : on colle deux textes
print(int("10") + 5)    # 15 : int() transforme le texte en nombre""", "Console Python"),
("astuce", "Bien nommer ses variables", "Des noms clairs en minuscules avec des tirets bas : <code>prix_course</code>, <code>poids_colis</code>. Évite <code>x</code> ou <code>a1</code> : dans six mois, tu ne sauras plus ce qu'ils contiennent."),
],
exercice=[
("p", "Écris <code>course.py</code> : crée les variables d'une course (client, zone, prix de base 1 500 F, poids 7 kg). Calcule un supplément de 200 F par kilo au-delà de 5 kg, puis affiche :"),
("code", "Course pour Awa Diop (Mermoz) : 1900 F", "Résultat attendu"),
],
retenir=[
  "Une variable range une valeur : <code>prix = 1500</code>.",
  "Les types de base : <code>str</code> (texte), <code>int</code> (entier), <code>float</code> (à virgule), <code>bool</code> (True/False).",
  "<code>f\"...{variable}...\"</code> fabrique un message avec des valeurs.",
  "Les nombres à virgule ne sont pas exacts : attention aux arrondis d'argent.",
]),
quiz=[
("Que vaut 7 // 2 en Python ?", [
  ("3", V, "Oui : // fait une division entière."),
  ("3.5", F, "Non : c'est le résultat de 7 / 2."),
  ("1", F, "Non : c'est le reste, donné par 7 % 2."),
]),
("Quel est le type de la valeur 3.5 ?", [
  ("float", V, "Oui : un nombre à virgule."),
  ("int", F, "Non : int est pour les nombres entiers."),
  ("str", F, "Non : str est pour le texte, entre guillemets."),
]),
("prix = 1500. Qu'affiche print(f\"Total : {prix * 2} F\") ?", [
  ("Total : 3000 F", V, "Oui : le calcul entre accolades est fait avant l'affichage."),
  ("Total : {prix * 2} F", F, "Non : grâce au f devant les guillemets, Python remplace ce qui est entre accolades."),
  ("Total : 15001500 F", F, "Non : prix est un nombre, pas un texte."),
]),
]),

# ---------------------------------------------------------------- 1.0.4
dict(code="1.0.4", id=None, seq=14, minutes=10,
titre="Listes et dictionnaires",
description="Ranger plusieurs valeurs : la liste des zones, le dictionnaire des tarifs.",
html=fiche(
objectif="ranger plusieurs valeurs dans une liste ou un dictionnaire, et les retrouver.",
intro="Baobab Livraison livre dans plusieurs zones, chacune avec son tarif. Pour ranger des collections de valeurs, Python a deux outils indispensables : la <b>liste</b> et le <b>dictionnaire</b>. Tu les retrouveras partout dans Odoo.",
corps=[
("h", "La liste : des valeurs dans l'ordre"),
("code", """zones = ["Plateau", "Médina", "Mermoz"]
print(zones[0])      # Plateau  (on compte à partir de 0)
print(zones[-1])     # Mermoz   (le dernier)
print(len(zones))    # 3
zones.append("Rufisque")   # ajouter à la fin
print("Mermoz" in zones)   # True""", "Console Python"),
("h", "Le dictionnaire : une clé, une valeur"),
("p", "Un dictionnaire associe une <b>clé</b> à une <b>valeur</b>, comme un répertoire : le nom de la zone donne son tarif."),
("code", """tarifs = {"Plateau": 1000, "Médina": 1000, "Mermoz": 1500}
print(tarifs["Mermoz"])          # 1500
tarifs["Rufisque"] = 3000        # ajouter ou modifier
print(tarifs.get("Yoff"))        # None : la clé n'existe pas
print(tarifs.get("Yoff", 0))     # 0 : valeur par défaut
print(list(tarifs.keys()))       # ['Plateau', 'Médina', 'Mermoz', 'Rufisque']""", "Console Python"),
("attention", "KeyError", "<code>tarifs[\"Yoff\"]</code> provoque l'erreur <code>KeyError: 'Yoff'</code> si la clé n'existe pas. Utilise <code>.get()</code> quand tu n'es pas sûr."),
("h", "Combiner les deux : une liste de courses"),
("p", "Une course a plusieurs informations : c'est un dictionnaire. Plusieurs courses : une liste de dictionnaires."),
("code", """courses = [
    {"client": "Awa Diop", "zone": "Mermoz", "poids": 3.5},
    {"client": "Moussa Ndiaye", "zone": "Plateau", "poids": 8},
]
print(courses[1]["zone"])   # Plateau""", "Console Python"),
("astuce", "Pourquoi c'est important pour Odoo", "Quand Odoo crée un enregistrement, tu lui donnes un dictionnaire : <code>{\"name\": \"Course 1\", \"poids\": 3.5}</code>. Et le fichier <code>__manifest__.py</code> d'un module est… un grand dictionnaire. Tu le verras au Bloc 2."),
],
exercice=[
("p", "Dans <code>zones.py</code>, crée le dictionnaire des tarifs de Baobab Livraison : Plateau 1 000 F, Médina 1 000 F, Mermoz 1 500 F, Parcelles Assainies 2 000 F, Rufisque 3 000 F. Affiche le tarif de Parcelles Assainies, puis le nombre de zones."),
("p", "Bonus : ajoute la zone Pikine à 2 500 F et affiche la liste des noms de zones."),
],
retenir=[
  "Liste : <code>[a, b, c]</code>, ordonnée, on compte à partir de 0.",
  "Dictionnaire : <code>{clé: valeur}</code>, on retrouve une valeur par sa clé.",
  "<code>.get(clé, défaut)</code> évite l'erreur <code>KeyError</code>.",
  "Odoo utilise des dictionnaires partout : pour créer des fiches, dans le manifeste…",
]),
quiz=[
("zones = [\"Plateau\", \"Médina\", \"Mermoz\"]. Que vaut zones[1] ?", [
  ("Médina", V, "Oui : on compte à partir de 0, donc [1] est le deuxième élément."),
  ("Plateau", F, "Non : Plateau est zones[0]."),
  ("Mermoz", F, "Non : Mermoz est zones[2] (ou zones[-1])."),
]),
("Quelle instruction donne 0 si la zone Yoff n'existe pas dans tarifs ?", [
  ("tarifs.get(\"Yoff\", 0)", V, "Oui : .get() renvoie la valeur par défaut si la clé manque."),
  ("tarifs[\"Yoff\"]", F, "Non : cela provoque une erreur KeyError."),
  ("tarifs.append(\"Yoff\")", F, "Non : append() sert aux listes, et n'ajoute pas de tarif."),
]),
("Quelle structure convient le mieux pour associer chaque zone à son tarif ?", [
  ("Un dictionnaire", V, "Oui : la zone est la clé, le tarif la valeur."),
  ("Une liste", F, "Une liste range des valeurs dans l'ordre, sans les associer à un nom."),
  ("Une chaîne de caractères", F, "Non : un texte ne permet pas de retrouver un tarif par zone."),
]),
]),

# ---------------------------------------------------------------- 1.0.5
dict(code="1.0.5", id=None, seq=15, minutes=10,
titre="Conditions et boucles",
description="Prendre une décision avec if, répéter une action avec for.",
html=fiche(
objectif="faire prendre une décision à ton programme (if) et répéter une action sur plusieurs courses (for).",
intro="Un colis lourd paie un supplément ; à la fin de la journée, on additionne toutes les courses. Pour cela, il faut savoir décider et répéter.",
corps=[
("h", "Décider : if, elif, else"),
("code", """poids = 8
if poids > 5:
    print("Colis lourd : supplément")
elif poids > 2:
    print("Colis moyen")
else:
    print("Petit colis")""", "Python"),
("p", "Les deux-points <code>:</code> et le décalage de 4 espaces sont obligatoires. Comparaisons possibles : <code>==</code> (égal), <code>!=</code> (différent), <code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code>. On combine avec <code>and</code>, <code>or</code>, <code>not</code>."),
("attention", "= ou == ?", "<code>=</code> range une valeur ; <code>==</code> compare. <code>if zone = \"Mermoz\":</code> est une erreur de syntaxe."),
("h", "Répéter : la boucle for"),
("code", """tarifs = {"Plateau": 1000, "Médina": 1000, "Mermoz": 1500, "Rufisque": 3000}

for zone, prix in tarifs.items():
    if prix >= 1500:
        print(f"{zone} est une zone éloignée ({prix} F)")""", "Python"),
("code", """Mermoz est une zone éloignée (1500 F)
Rufisque est une zone éloignée (3000 F)""", "Résultat"),
("h", "Additionner les courses de la journée"),
("code", """courses = [
    {"client": "Awa Diop", "zone": "Mermoz"},
    {"client": "Moussa Ndiaye", "zone": "Plateau"},
    {"client": "Fatou Sarr", "zone": "Rufisque"},
]
total = 0
for course in courses:
    total = total + tarifs[course["zone"]]
print("Chiffre du jour :", total, "F")   # Chiffre du jour : 5500 F""", "Python"),
("p", "<code>range(1, 4)</code> donne les nombres 1, 2, 3 : pratique pour répéter un nombre de fois connu."),
("astuce", "Dans Odoo", "Tu écriras souvent <code>for course in self:</code> : une boucle sur les fiches sélectionnées. C'est exactement la même boucle."),
],
exercice=[
("p", "Reprends la liste <code>courses</code> ci-dessus et ajoute un poids à chaque course (3, 8 et 12 kg). Écris une boucle qui affiche, pour chaque course, le client et « supplément » si le poids dépasse 5 kg. À la fin, affiche combien de colis lourds il y a eu."),
],
retenir=[
  "<code>if / elif / else</code> pour décider ; deux-points et indentation obligatoires.",
  "<code>==</code> compare, <code>=</code> range.",
  "<code>for élément in collection:</code> répète pour chaque élément.",
  "<code>.items()</code> parcourt un dictionnaire clé et valeur ensemble.",
]),
quiz=[
("Quel symbole sert à tester si deux valeurs sont égales ?", [
  ("==", V, "Oui."),
  ("=", F, "Non : = range une valeur dans une variable."),
  ("=>", F, "Ce n'est pas un opérateur Python."),
]),
("poids = 4. Qu'affiche le code if poids > 5 … elif poids > 2 … else … de la leçon ?", [
  ("Colis moyen", V, "Oui : 4 n'est pas > 5, mais 4 > 2."),
  ("Colis lourd : supplément", F, "Non : 4 n'est pas plus grand que 5."),
  ("Petit colis", F, "Non : le test elif poids > 2 est vrai, le else n'est pas atteint."),
]),
("À quoi sert tarifs.items() dans une boucle for ?", [
  ("À parcourir chaque zone avec son tarif", V, "Oui : on obtient la clé et la valeur à chaque tour."),
  ("À trier les zones par prix", F, "Non : items() ne trie pas."),
  ("À ajouter une zone", F, "Non : on ajoute avec tarifs[\"zone\"] = prix."),
]),
]),

# ---------------------------------------------------------------- 1.0.6
dict(code="1.0.6", id=None, seq=16, minutes=10,
titre="Les fonctions",
description="Écrire prix_course(zone, poids), une fonction réutilisable qui gère aussi les erreurs.",
html=fiche(
objectif="écrire une fonction réutilisable qui calcule le prix d'une course et signale les erreurs.",
intro="Le calcul du prix sert partout : au téléphone, sur le bordereau, dans l'appli. Plutôt que de le recopier, on l'écrit une seule fois dans une <b>fonction</b>.",
corps=[
("h", "Définir une fonction"),
("code", """import math

TARIFS = {"Plateau": 1000, "Médina": 1000, "Mermoz": 1500,
          "Parcelles Assainies": 2000, "Rufisque": 3000}
POIDS_INCLUS = 5         # kg compris dans le prix de base
SUPPLEMENT_PAR_KG = 200  # F par kilo entamé au-delà


def prix_course(zone, poids):
    \"\"\"Renvoie le prix d'une course en F CFA.\"\"\"
    if zone not in TARIFS:
        raise ValueError(f"Zone inconnue : {zone}")
    prix = TARIFS[zone]
    if poids > POIDS_INCLUS:
        kilos_en_plus = math.ceil(poids - POIDS_INCLUS)  # 2,2 kg en plus = 3 kilos entamés
        prix = prix + kilos_en_plus * SUPPLEMENT_PAR_KG
    return prix""", "tarifs.py"),
("liste", [
  "<code>def</code> définit la fonction ; <code>zone</code> et <code>poids</code> sont ses <b>paramètres</b>.",
  "<code>return</code> renvoie le résultat à celui qui a appelé la fonction.",
  "Le texte entre triples guillemets (docstring) explique ce que fait la fonction.",
  "Les noms en MAJUSCULES sont des <b>constantes</b> : des réglages qu'on ne modifie pas dans le programme.",
  "<code>import math</code> donne accès à <code>math.ceil()</code>, qui arrondit vers le haut.",
]),
("h", "Appeler la fonction"),
("code", """print(prix_course("Mermoz", 3))      # 1500
print(prix_course("Mermoz", 7.2))    # 2100  (3 kilos entamés x 200 F)
print(prix_course("Rufisque", 12))   # 4400""", "Python"),
("h", "Signaler une erreur et la rattraper"),
("p", "<code>raise ValueError(...)</code> arrête le calcul avec un message clair. Celui qui appelle peut rattraper l'erreur avec <code>try / except</code> :"),
("code", """try:
    prix_course("Yoff", 2)
except ValueError as erreur:
    print("Erreur :", erreur)     # Erreur : Zone inconnue : Yoff""", "Python"),
("astuce", "Dans Odoo", "Odoo fonctionne pareil : quand une règle n'est pas respectée, le code lève une erreur (<code>ValidationError</code> ou <code>UserError</code>) et Odoo affiche le message à l'utilisateur."),
],
exercice=[
("p", "Ajoute à <code>tarifs.py</code> une fonction <code>en_francs(montant)</code> qui renvoie par exemple <code>\"4 400 F\"</code> (avec un espace pour les milliers). Puis écris une boucle qui affiche le prix de chacune de ces courses : Mermoz 3 kg, Plateau 8 kg, Rufisque 12 kg, Yoff 2 kg (cette dernière doit afficher un message d'erreur sans arrêter le programme)."),
("p", "Garde bien ce fichier : c'est la première pièce du travail à rendre du Bloc 1."),
],
retenir=[
  "<code>def nom(paramètres):</code> définit une fonction ; <code>return</code> renvoie le résultat.",
  "Une fonction s'écrit une fois et s'utilise partout.",
  "<code>raise</code> signale une erreur ; <code>try / except</code> la rattrape.",
  "Les constantes (MAJUSCULES) regroupent les réglages en haut du fichier.",
]),
quiz=[
("Que renvoie prix_course(\"Plateau\", 6.5) avec les règles de la leçon ?", [
  ("1400", V, "Oui : 1 000 F + 2 kilos entamés (1,5 kg arrondi au-dessus) x 200 F."),
  ("1300", F, "Non : 1,5 kg au-delà donne 2 kilos entamés avec math.ceil."),
  ("1000", F, "Non : le poids dépasse 5 kg, il y a un supplément."),
]),
("À quoi sert le mot-clé return ?", [
  ("À renvoyer le résultat de la fonction", V, "Oui."),
  ("À afficher le résultat à l'écran", F, "Non : c'est print() qui affiche."),
  ("À recommencer la fonction", F, "Non."),
]),
("Comment éviter que le programme s'arrête quand une zone est inconnue ?", [
  ("En entourant l'appel de try / except ValueError", V, "Oui : l'erreur est rattrapée et le programme continue."),
  ("En supprimant le raise de la fonction", F, "Non : on perdrait le message qui explique le problème."),
  ("En mettant la zone en majuscules", F, "Non, cela ne change rien au problème."),
]),
]),
]
