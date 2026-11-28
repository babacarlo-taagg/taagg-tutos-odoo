"""Bloc 2 — Section « Le module » (section 2714, cours 209).
Code vérifié sur Odoo 20.0 (Python 3.12, PostgreSQL 16) le 27/11/2026 : module de référence baobab_livraison
installé sur une base neuve, 7 tests verts. Le module complet n'est pas dans ce dépôt public (c'est aussi un corrigé)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

ARBRE = """baobab_livraison/
├── __init__.py              ← importe le dossier models
├── __manifest__.py          ← la carte d'identité du module
├── models/
│   ├── __init__.py          ← importe chaque fichier de modèle
│   ├── zone.py
│   ├── course.py
│   └── res_partner.py
├── security/
│   └── ir.access.csv        ← qui a le droit de faire quoi
├── data/                    ← données chargées à l'installation
├── demo/                    ← données d'exemple (bases de test)
├── views/                   ← écrans et menus (Bloc 3)
└── tests/                   ← tests automatiques"""

MANIFESTE = """{
    "name": "Baobab Livraison",
    "summary": "Courses de livraison à moto : zones, tarifs, livreurs",
    "version": "20.0.1.0.0",
    "category": "Services",
    "author": "TAAGG School (exercice)",
    "website": "https://www.taagg-school.com",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.access.csv",
        "data/ir_sequence_data.xml",
        "data/baobab.zone.csv",
        "data/baobab_etiquette_data.xml",
        "data/ir_cron_data.xml",
        "views/baobab_course_views.xml",
        "views/baobab_menus.xml",
    ],
    "demo": [
        "demo/baobab_demo.xml",
    ],
    "application": True,
}"""

LECONS = [
# ---------------------------------------------------------------- 2.1.1
dict(code="2.1.1", id=2715, seq=11, minutes=10,
titre="Anatomie d'un module : manifeste, dossiers, données, dépendances",
description="Reconnaître chaque fichier et chaque dossier d'un module Odoo, et savoir à quoi il sert.",
html=fiche(
objectif="reconnaître chaque dossier et chaque fichier d'un module Odoo, et comprendre comment Odoo le lit.",
intro="Dans Odoo, tout est module : la Comptabilité, les Ventes, les Contacts… et bientôt Baobab Livraison. Un module, c'est simplement un dossier rangé d'une façon précise. Une fois cette organisation comprise, tu sauras lire n'importe quel module d'Odoo.",
corps=[
("h", "Le module Baobab Livraison, à la fin du Bloc 2"),
("code", ARBRE, "Arborescence du module"),
("h", "Les deux fichiers obligatoires"),
("liste", [
  "<b><code>__manifest__.py</code></b> : la carte d'identité. Nom, version, modules dont on dépend, liste des fichiers de données à charger. Sans lui, Odoo ne voit pas le dossier.",
  "<b><code>__init__.py</code></b> : il dit à Python quels fichiers de code importer. Celui de la racine importe le dossier <code>models</code>, qui a son propre <code>__init__.py</code>.",
]),
("code", """# baobab_livraison/__init__.py
from . import models

# baobab_livraison/models/__init__.py
from . import zone
from . import etiquette
from . import course
from . import res_partner""", "Les deux __init__.py"),
("attention", "L'oubli le plus courant", "Tu crées <code>models/course.py</code> mais tu oublies la ligne <code>from . import course</code> : Odoo ne lit jamais ton fichier, et ton modèle n'existe pas. Aucune erreur, juste rien. Premier réflexe quand « ça n'apparaît pas » : vérifier les <code>__init__.py</code>."),
("h", "Deux mondes : le Python et les données"),
("tableau", ["Type de fichier", "Comment Odoo le charge", "Exemples"], [
  ["Python (<code>.py</code>)", "par les <code>import</code> des <code>__init__.py</code>", "modèles, champs, logique"],
  ["Données (<code>.xml</code>, <code>.csv</code>)", "par la liste <code>data</code> du manifeste, <b>dans l'ordre</b>", "droits, séquences, zones, écrans, menus"],
  ["Démonstration", "par la liste <code>demo</code>, seulement si on la demande", "clients et courses d'exemple"],
]),
("astuce", "Où trouver des exemples", "Le code d'Odoo lui-même est la meilleure école : ouvre <code>~/odoo/addons/sale/</code> et retrouve exactement la même organisation, en plus grand."),
("version", "Le fichier des droits s'appelle <code>security/ir.access.csv</code> en Odoo 20. En Odoo 18 et 19, c'était <code>security/ir.model.access.csv</code>, avec d'autres colonnes. On le voit en détail dans la section « Le modèle »."),
],
exercice=[
("p", "Ouvre <code>~/odoo/addons/sale/</code> dans VS Code. Retrouve : (1) le fichier qui dit de quels modules dépend Ventes ; (2) le fichier Python qui définit les commandes (<code>sale.order</code>) ; (3) le fichier qui liste les droits d'accès. Note les chemins dans ton carnet."),
],
retenir=[
  "Un module = un dossier avec au minimum <code>__manifest__.py</code> et <code>__init__.py</code>.",
  "Le Python est chargé par les <code>import</code> ; les fichiers XML et CSV par la liste <code>data</code> du manifeste.",
  "Un fichier Python oublié dans un <code>__init__.py</code> n'est jamais lu, sans message d'erreur.",
  "Les sous-dossiers habituels : models, security, data, demo, views, tests.",
]),
quiz=[
("Quel fichier est la « carte d'identité » d'un module Odoo ?", [
  ("__manifest__.py", V, "Oui : nom, version, dépendances, fichiers de données."),
  ("__init__.py", F, "Non : __init__.py dit seulement quels fichiers Python importer."),
  ("models.py", F, "Non : il contient du code, pas la description du module."),
]),
("Tu as créé models/course.py mais ton modèle n'apparaît pas. Quelle est la cause la plus probable ?", [
  ("La ligne from . import course manque dans models/__init__.py", V, "Oui : sans cet import, Python ne lit jamais le fichier."),
  ("PostgreSQL est trop ancien", F, "Non : rien à voir."),
  ("Le module n'a pas de dossier demo", F, "Non : le dossier demo est facultatif."),
]),
("Comment Odoo charge-t-il un fichier XML de données ?", [
  ("Parce qu'il est listé dans la clé data du manifeste", V, "Oui, et dans l'ordre de la liste."),
  ("Automatiquement, dès qu'il est dans le dossier du module", F, "Non : un fichier non listé est ignoré."),
  ("Par un import dans __init__.py", F, "Non : les import servent au Python seulement."),
]),
]),

# ---------------------------------------------------------------- 2.1.2
dict(code="2.1.2", id=2912, seq=12, minutes=10,
titre="Le manifeste ligne par ligne",
description="Écrire le __manifest__.py de Baobab Livraison et comprendre chaque clé.",
html=fiche(
objectif="écrire le manifeste de Baobab Livraison et comprendre le rôle de chaque clé.",
intro="Le manifeste est un dictionnaire Python. Odoo le lit avant tout le reste : c'est lui qui décide si le module s'affiche, ce qu'il faut installer avant lui, et quels fichiers charger.",
corps=[
("code", MANIFESTE, "baobab_livraison/__manifest__.py (version finale du Bloc 2)"),
("h", "Les clés, une par une"),
("tableau", ["Clé", "Rôle"], [
  ["<code>name</code>, <code>summary</code>", "le nom et la phrase affichés dans Applications"],
  ["<code>version</code>", "<b>20.0</b> (version d'Odoo) + <b>1.0.0</b> (version de ton module). On l'augmente à chaque livraison chez le client."],
  ["<code>category</code>", "la famille d'applications (Services, Ventes…)"],
  ["<code>author</code>, <code>website</code>", "qui a écrit le module"],
  ["<code>license</code>", "la licence : <code>LGPL-3</code> pour un module libre"],
  ["<code>depends</code>", "les modules à installer <b>avant</b> le tien"],
  ["<code>data</code>", "les fichiers XML et CSV chargés à chaque installation et mise à jour, <b>dans l'ordre</b>"],
  ["<code>demo</code>", "les données d'exemple, chargées seulement si on le demande"],
  ["<code>application</code>", "<code>True</code> : le module apparaît comme une vraie application, avec son icône"],
]),
("h", "depends : la chaîne des dépendances"),
("p", "Notre module a besoin des contacts (<code>base</code>) et de la discussion et des activités (<code>mail</code>). Si tu utilises un modèle d'un autre module sans le déclarer dans <code>depends</code>, l'installation échoue ou, pire, marche chez toi par hasard et plante chez le client."),
("h", "data : l'ordre compte"),
("p", "Les droits d'accès d'abord, puis les données, puis les écrans, et les menus en dernier : un menu pointe vers une action, qui doit déjà exister quand Odoo lit le menu."),
("attention", "Les avertissements à ne pas ignorer", "Sans <code>author</code> ou <code>license</code>, Odoo 20 écrit dans le journal : <code>Missing `author` key in manifest</code> ou <code>Missing `license` key in manifest, defaulting to LGPL-3</code>. Le module s'installe quand même, mais un module propre n'a aucun avertissement."),
("version", "La version du module commence toujours par la version d'Odoo : <code>20.0.1.0.0</code> pour Odoo 20, <code>18.0.1.0.0</code> pour Odoo 18. C'est elle qui déclenche les scripts de migration (section « Les données »)."),
],
exercice=[
("p", "Dans <code>~/baobab/addons/baobab_livraison/</code>, crée le manifeste de la première version : name, summary, version <code>20.0.1.0.0</code>, author (ton nom), license, <code>depends</code> avec seulement <code>base</code>, et <code>data</code> vide (<code>[]</code>). Les autres clés arriveront au fil du bloc."),
],
retenir=[
  "Le manifeste est un dictionnaire Python lu en premier par Odoo.",
  "<code>version</code> = version d'Odoo + version du module : <code>20.0.1.0.0</code>.",
  "<code>depends</code> liste tout ce dont le module a besoin.",
  "<code>data</code> est chargé dans l'ordre : droits, données, écrans, menus.",
]),
quiz=[
("Que signifie la version 20.0.1.0.0 ?", [
  ("Version 1.0.0 du module, pour Odoo 20", V, "Oui."),
  ("Version 20 du module", F, "Non : 20.0 est la version d'Odoo."),
  ("Le module a 20 fichiers", F, "Non."),
]),
("Ton module utilise le modèle sale.order. Que dois-tu ajouter au manifeste ?", [
  ("\"sale\" dans depends", V, "Oui : le module Ventes doit être installé avant le tien."),
  ("\"sale.order\" dans data", F, "Non : data liste des fichiers XML ou CSV."),
  ("Rien, Odoo le trouve tout seul", F, "Non : sans dépendance déclarée, l'installation peut échouer chez le client."),
]),
("Pourquoi les menus sont-ils en dernier dans la liste data ?", [
  ("Parce qu'un menu pointe vers une action qui doit déjà exister", V, "Oui : les fichiers sont chargés dans l'ordre."),
  ("Parce qu'Odoo trie les fichiers par ordre alphabétique", F, "Non : il respecte l'ordre de la liste."),
  ("C'est seulement une habitude, sans effet", F, "Non : un mauvais ordre provoque une erreur à l'installation."),
]),
]),

# ---------------------------------------------------------------- 2.1.3
dict(code="2.1.3", id=2716, seq=13, minutes=10,
titre="Créer le module baobab_livraison et l'installer",
description="Créer le dossier du module, le faire connaître à Odoo et l'installer.",
html=fiche(
objectif="créer le module Baobab Livraison, le faire voir à Odoo et l'installer dans ta base.",
intro="Place à la pratique : on crée le module, on dit à Odoo où il se trouve, et on l'installe. Pour l'instant il est presque vide, mais il apparaîtra dans Applications.",
corps=[
("h", "1. Créer le dossier"),
("code", """mkdir -p ~/baobab/addons/baobab_livraison/models
cd ~/baobab/addons/baobab_livraison
touch __init__.py models/__init__.py""", "Terminal"),
("p", "Écris le <code>__manifest__.py</code> de la leçon précédente, et dans <code>__init__.py</code> la ligne <code>from . import models</code>."),
("version", "La commande <code>odoo-bin scaffold</code> crée un module tout prêt. Attention, en Odoo 20 elle génère encore l'ancien fichier <code>security/ir.model.access.csv</code> : s'il est activé dans le manifeste, Odoo 20 refuse de démarrer la base (<code>KeyError: 'ir.model.access'</code>). Pour apprendre, on crée donc le module à la main."),
("h", "2. Dire à Odoo où chercher"),
("p", "Ajoute ton dossier au chemin des modules, dans <code>~/baobab/odoo.conf</code> :"),
("code", "addons_path = /home/awa/odoo/addons,/home/awa/baobab/addons", "~/baobab/odoo.conf (remplace awa par ton nom)"),
("h", "3. Installer"),
("code", """cd ~/odoo
source ~/venv-odoo/bin/activate
python3 odoo-bin -c ~/baobab/odoo.conf -i baobab_livraison --stop-after-init""", "Terminal"),
("p", "<code>-i baobab_livraison</code> installe le module ; <code>--stop-after-init</code> arrête Odoo juste après. Relance ensuite Odoo normalement et va dans <b>Applications</b> : retire le filtre « Applications » et cherche « Baobab ». Ton module est installé."),
("astuce", "Par l'écran", "Tu peux aussi installer depuis Odoo : mode développeur, <b>Applications</b> → <b>Mettre à jour la liste des Apps</b>, puis bouton <b>Activer</b> sur ton module."),
("h", "4. Les écrans fournis pour le Bloc 2"),
("p", "Pour voir et manipuler tes courses pendant le Bloc 2, tu recopieras deux fichiers d'écrans tout prêts : <code>views/baobab_course_views.xml</code> (liste et formulaire) et <code>views/baobab_menus.xml</code> (menus). Les menus sont donnés en entier dans la leçon « Le droit minimum pour voir son modèle », les écrans dans la leçon « Statuts et boutons d'action ». On apprend à les écrire au Bloc 3 : pour l'instant, recopie-les tels quels."),
("attention", "Un module qui n'apparaît pas", "Vérifie dans l'ordre : le dossier est bien dans un chemin de <code>addons_path</code> ; le nom du dossier ne contient ni espace ni tiret (<code>baobab_livraison</code>, pas <code>baobab-livraison</code>) ; le manifeste est un dictionnaire Python valide ; tu as mis à jour la liste des Apps."),
],
exercice=[
("p", "Crée le module, ajoute ton dossier à <code>addons_path</code>, installe-le avec <code>-i</code>. Dans le journal, retrouve la ligne <code>Loading module baobab_livraison</code>. Puis committe le module dans ton dépôt Git <code>baobab_livraison</code> (Bloc 1) : à partir de maintenant, chaque étape du Bloc 2 = un commit."),
],
retenir=[
  "Un module se place dans un dossier listé dans <code>addons_path</code>.",
  "<code>-i nom_du_module</code> installe ; <code>--stop-after-init</code> arrête Odoo après.",
  "Par l'écran : mode développeur, Mettre à jour la liste des Apps, puis Activer.",
  "En Odoo 20, attention au fichier de droits généré par <code>scaffold</code> : c'est l'ancien format.",
]),
quiz=[
("Quelle option installe le module baobab_livraison au démarrage d'Odoo ?", [
  ("-i baobab_livraison", V, "Oui."),
  ("-u baobab_livraison", F, "Non : -u met à jour un module déjà installé."),
  ("--save baobab_livraison", F, "Non : --save enregistre le fichier de configuration."),
]),
("Ton module n'apparaît pas dans Applications. Que vérifies-tu en premier ?", [
  ("Que son dossier est dans addons_path et que la liste des Apps a été mise à jour", V, "Oui."),
  ("Que tu as assez de données de démonstration", F, "Non, rien à voir."),
  ("Que le port 8069 est libre", F, "Non : Odoo tourne, c'est le module qu'il ne voit pas."),
]),
("En Odoo 20, que se passe-t-il si tu actives l'ancien fichier ir.model.access.csv créé par scaffold ?", [
  ("Odoo refuse de démarrer la base : le modèle ir.model.access n'existe plus", V, "Oui : en Odoo 20, les droits passent par ir.access."),
  ("Rien, Odoo le convertit tout seul", F, "Non : on l'a vérifié, la base ne démarre plus."),
  ("Les droits sont donnés à tout le monde", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.1.4
dict(code="2.1.4", id=2913, seq=14, minutes=10,
titre="Mettre à jour un module : quand redémarrer, quand faire -u",
description="Savoir exactement quoi faire après chaque modification pour qu'Odoo en tienne compte.",
html=fiche(
objectif="savoir, après chaque modification, s'il faut redémarrer Odoo, mettre à jour le module, ou les deux.",
intro="« J'ai changé mon code et rien ne change ! » C'est la phrase la plus entendue chez les débutants. La règle est simple, une fois qu'on sait ce qu'Odoo garde en mémoire et ce qu'il garde dans la base.",
corps=[
("h", "La règle"),
("tableau", ["Tu as modifié…", "Il faut…"], [
  ["Le corps d'une méthode Python (un calcul, un message)", "<b>Redémarrer</b> Odoo (ou laisser <code>--dev=reload</code> le faire)"],
  ["Un champ : ajouté, supprimé, renommé, changé de type", "Redémarrer <b>et</b> mettre à jour : <code>-u baobab_livraison</code>"],
  ["Un fichier XML ou CSV (écran, menu, données, droits)", "Mettre à jour : <code>-u baobab_livraison</code>"],
  ["Le manifeste (nouvelle dépendance, nouveau fichier dans data)", "Mettre à jour : <code>-u baobab_livraison</code>"],
  ["Un nouveau module", "Mettre à jour la liste des Apps, puis installer (<code>-i</code>)"],
]),
("h", "Pourquoi ?"),
("liste", [
  "Le code Python est lu <b>au démarrage</b> : un redémarrage suffit pour une méthode.",
  "Les champs correspondent à des <b>colonnes</b> dans PostgreSQL : seule la mise à jour crée ou modifie ces colonnes.",
  "Les fichiers XML et CSV sont <b>copiés dans la base</b> à l'installation : seule la mise à jour les recopie.",
]),
("h", "Ce qui arrive si on oublie -u"),
("p", "On a ajouté un champ <code>remarque</code> au modèle, puis seulement redémarré Odoo :"),
("code", """ERROR: column baobab_course.remarque does not exist
psycopg2.errors.UndefinedColumn: column baobab_course.remarque does not exist""", "Odoo 20, vérifié le 27/11/2026"),
("p", "Après <code>-u baobab_livraison</code>, la colonne est créée et tout fonctionne."),
("code", "python3 odoo-bin -c ~/baobab/odoo.conf -u baobab_livraison --stop-after-init", "Terminal : mettre à jour le module"),
("astuce", "Le bon rythme de travail", "Pendant que tu écris une méthode : <code>--dev=reload</code>, Odoo redémarre tout seul à chaque enregistrement. Dès que tu touches un champ ou un fichier XML : <code>-u</code>. Dans le doute, <code>-u</code> ne fait jamais de mal sur ta base de test."),
("attention", "Pas sur la base d'un client sans précaution", "Sur ta base de développement, <code>-u</code> à volonté. Chez un client, une mise à jour se prépare : sauvegarde, essai sur une copie, puis mise à jour. On le verra au Bloc 5."),
],
exercice=[
("p", "Ajoute un champ <code>essai = fields.Char()</code> à un modèle de ton module. Redémarre Odoo sans <code>-u</code> et ouvre la liste : observe l'erreur dans le journal. Puis lance <code>-u baobab_livraison</code> et vérifie que tout remarche. Enfin, retire le champ et remets à jour."),
],
retenir=[
  "Méthode Python modifiée : redémarrer.",
  "Champ ajouté ou modifié, fichier XML ou CSV, manifeste : <code>-u nom_du_module</code>.",
  "« column … does not exist » = tu as oublié <code>-u</code>.",
  "Chez un client, une mise à jour se prépare (sauvegarde, essai sur une copie).",
]),
quiz=[
("Tu as seulement corrigé un calcul dans une méthode Python. Que faut-il faire ?", [
  ("Redémarrer Odoo", V, "Oui : le code Python est relu au démarrage (ou automatiquement avec --dev=reload)."),
  ("Réinstaller le module", F, "Inutile."),
  ("Rien, c'est immédiat même sans redémarrage", F, "Non : sans --dev=reload, Odoo garde l'ancien code en mémoire."),
]),
("Le journal dit « column baobab_course.remarque does not exist ». Que s'est-il passé ?", [
  ("Un champ a été ajouté sans mettre à jour le module (-u)", V, "Oui : la colonne n'a pas été créée dans PostgreSQL."),
  ("PostgreSQL est en panne", F, "Non : il répond, il dit justement que la colonne manque."),
  ("Le module n'a pas de manifeste", F, "Non."),
]),
("Tu as modifié un fichier XML de menus. Que faut-il faire ?", [
  ("Mettre à jour le module avec -u", V, "Oui : les fichiers XML sont copiés dans la base à la mise à jour."),
  ("Seulement redémarrer", F, "Non : le XML déjà copié dans la base ne change pas."),
  ("Vider le cache du navigateur", F, "Non."),
]),
]),
]
