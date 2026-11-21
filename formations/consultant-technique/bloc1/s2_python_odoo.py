"""Bloc 1 — Section « Python pour Odoo » (section 2702, cours 208).
Code testé avec Python 3.12 et Odoo 20.0 le 21/11/2026."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

LECONS = [
# ---------------------------------------------------------------- 1.2.1
dict(code="1.2.1", id=None, seq=31, minutes=10,
titre="Environnement virtuel et pip",
description="Isoler les bibliothèques Python d'un projet avec venv, les installer avec pip.",
html=fiche(
objectif="créer un environnement virtuel, y installer des bibliothèques avec pip et noter la liste dans requirements.txt.",
intro="Odoo a besoin d'une soixantaine de bibliothèques Python, dans des versions précises. Pour ne pas mélanger celles d'Odoo avec celles d'un autre projet (ou du système), on les range dans un <b>environnement virtuel</b>.",
corps=[
("h", "Le problème"),
("p", "Sur Ubuntu 24.04, essaie d'installer une bibliothèque directement :"),
("code", """pip install requests
error: externally-managed-environment
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install""", "Terminal"),
("p", "Ubuntu protège son propre Python : il refuse qu'on y ajoute des bibliothèques avec pip. La bonne solution est l'environnement virtuel."),
("h", "Créer et activer un environnement virtuel"),
("code", """sudo apt install python3-venv          # une seule fois
python3 -m venv ~/venv-odoo            # crée l'environnement dans ~/venv-odoo
source ~/venv-odoo/bin/activate        # l'active
(venv-odoo) awa@pc:~$                  # le nom apparaît devant l'invite
which python3
/home/awa/venv-odoo/bin/python3""", "Terminal"),
("p", "Tant que l'environnement est actif, <code>python3</code> et <code>pip</code> sont ceux de <code>~/venv-odoo</code>. Pour en sortir : <code>deactivate</code>."),
("h", "Installer avec pip"),
("code", """pip install requests                 # installer une bibliothèque
pip list                             # voir ce qui est installé
pip freeze > requirements.txt        # enregistrer la liste avec les versions
pip install -r requirements.txt      # tout réinstaller à partir de la liste""", "Terminal (environnement activé)"),
("astuce", "Odoo fait exactement ça", "Le dossier des sources d'Odoo contient un fichier <code>requirements.txt</code>. Pour installer Odoo, on fera : activer l'environnement, puis <code>pip install -r requirements.txt</code> (section Git et environnement)."),
("attention", "Un oubli classique", "Tu ouvres un nouveau terminal et Odoo dit <code>ModuleNotFoundError: No module named 'psycopg2'</code> ? L'environnement virtuel n'est pas activé. Relance <code>source ~/venv-odoo/bin/activate</code>."),
],
exercice=[
("p", "Crée l'environnement <code>~/venv-odoo</code> (on s'en resservira pour Odoo), active-le, installe <code>requests</code>, puis enregistre la liste dans <code>~/baobab/requirements-essai.txt</code>. Désactive l'environnement et vérifie avec <code>which python3</code> que tu es revenu au Python du système."),
],
retenir=[
  "Un environnement virtuel isole les bibliothèques d'un projet.",
  "<code>python3 -m venv chemin</code> pour créer, <code>source chemin/bin/activate</code> pour activer, <code>deactivate</code> pour sortir.",
  "<code>pip install -r requirements.txt</code> installe toutes les bibliothèques listées.",
  "<code>ModuleNotFoundError</code> au lancement d'Odoo : vérifie d'abord que l'environnement est activé.",
]),
quiz=[
("Sur Ubuntu 24.04, pip install refuse avec « externally-managed-environment ». Quelle est la bonne solution ?", [
  ("Créer et activer un environnement virtuel, puis refaire pip install", V, "Oui."),
  ("Lancer pip avec sudo", F, "Non : on risque de casser le Python du système."),
  ("Désinstaller Python", F, "Surtout pas : Ubuntu en a besoin."),
]),
("Quelle commande installe toutes les bibliothèques listées dans requirements.txt ?", [
  ("pip install -r requirements.txt", V, "Oui."),
  ("pip freeze requirements.txt", F, "Non : pip freeze affiche la liste, il n'installe rien."),
  ("python3 requirements.txt", F, "Non : ce n'est pas un script Python."),
]),
("Odoo affiche « No module named 'psycopg2' » dans un nouveau terminal. Que vérifier d'abord ?", [
  ("Que l'environnement virtuel est activé", V, "Oui : c'est l'oubli le plus fréquent."),
  ("Que PostgreSQL est éteint", F, "Non : l'erreur dit qu'une bibliothèque Python manque."),
  ("Que le port 8069 est libre", F, "Non, rien à voir."),
]),
]),

# ---------------------------------------------------------------- 1.2.2
dict(code="1.2.2", id=1352, seq=32, minutes=10,
titre="Classes et objets : lire « class Course(models.Model) »",
description="Comprendre les classes, les objets, self et les méthodes, pour lire un modèle Odoo.",
html=fiche(
objectif="comprendre ce que sont une classe, un objet, une méthode et <code>self</code>, pour pouvoir lire un modèle Odoo.",
intro="Dans Odoo, chaque type de fiche (un contact, une facture, une course de livraison) est décrit par une <b>classe</b> Python. Avant d'écrire ton premier modèle, il faut savoir lire une classe.",
corps=[
("h", "Une classe, des objets"),
("p", "Une <b>classe</b> est un moule. Les <b>objets</b> sont les gâteaux sortis du moule : ils ont tous la même forme, mais chacun a ses propres valeurs."),
("code", """class Course:
    \"\"\"Une course de livraison.\"\"\"
    TARIF_DE_BASE = 1000                 # attribut de classe : commun à toutes les courses

    def __init__(self, client, zone, poids=1.0):
        self.client = client             # attributs propres à chaque objet
        self.zone = zone
        self.poids = poids
        self.statut = "brouillon"

    def demarrer(self):                  # une méthode : une fonction de la classe
        self.statut = "en_route"


c1 = Course("Awa Diop", "Mermoz", 3.5)   # on crée un objet
c2 = Course("Moussa Ndiaye", "Plateau")
c1.demarrer()
print(c1.statut, c2.statut, c2.poids)    # en_route brouillon 1.0""", "classes.py"),
("liste", [
  "<code>__init__</code> est appelée automatiquement à la création de l'objet.",
  "<code>self</code> désigne <b>l'objet lui-même</b> : <code>self.statut</code>, c'est « le statut de cette course-ci ».",
  "Une <b>méthode</b> est une fonction définie dans la classe ; on l'appelle avec un point : <code>c1.demarrer()</code>.",
]),
("h", "Et dans Odoo ?"),
("p", "Voici un vrai modèle Odoo 20 (on l'écrira au Bloc 2). Tu peux déjà le lire :"),
("code", """from odoo import api, fields, models


class BaobabCourse(models.Model):          # la classe hérite de models.Model
    _name = "baobab.course"                # nom technique du modèle
    _description = "Course de livraison"

    client = fields.Char(required=True)    # un champ = une colonne en base
    poids = fields.Float()
    prix = fields.Integer(compute="_compute_prix")

    @api.depends("poids")
    def _compute_prix(self):
        for course in self:                # self contient PLUSIEURS courses
            course.prix = 1000 + max(0, int(course.poids) - 5) * 200""", "models/course.py (testé sous Odoo 20)"),
("attention", "La grande différence", "En Python classique, <code>self</code> est un seul objet. Dans Odoo, <code>self</code> est un <b>ensemble de fiches</b> (un « recordset ») : 0, 1 ou plusieurs courses. C'est pour cela qu'on écrit presque toujours <code>for course in self:</code>."),
],
exercice=[
("p", "Ajoute à la classe <code>Course</code> une méthode <code>livrer(self)</code> qui passe le statut à <code>\"livree\"</code>, et une méthode <code>est_lourde(self)</code> qui renvoie <code>True</code> si le poids dépasse 5 kg. Crée trois courses, livre-en une, et affiche le statut et le résultat de <code>est_lourde()</code> pour chacune."),
],
retenir=[
  "Une classe est un moule, un objet est une fiche créée à partir du moule.",
  "<code>__init__</code> initialise l'objet ; <code>self</code> désigne l'objet lui-même.",
  "Un modèle Odoo est une classe qui hérite de <code>models.Model</code>, avec des champs <code>fields.…</code>.",
  "Dans Odoo, <code>self</code> peut contenir plusieurs fiches : on boucle avec <code>for … in self</code>.",
]),
quiz=[
("Dans une méthode de classe Python, que désigne self ?", [
  ("L'objet sur lequel la méthode est appelée", V, "Oui."),
  ("La classe mère", F, "Non : pour la classe mère, on utilise super()."),
  ("Le fichier Python", F, "Non."),
]),
("Quelle méthode est appelée automatiquement quand on crée un objet ?", [
  ("__init__", V, "Oui."),
  ("__repr__", F, "Non : __repr__ sert à afficher l'objet."),
  ("demarrer", F, "Non : c'est une méthode ordinaire, qu'on appelle soi-même."),
]),
("Pourquoi écrit-on souvent « for course in self: » dans une méthode Odoo ?", [
  ("Parce que self peut contenir plusieurs fiches", V, "Oui : self est un recordset."),
  ("Parce que Python l'oblige dans toutes les méthodes", F, "Non : c'est propre à Odoo."),
  ("Pour ralentir le programme", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 1.2.3
dict(code="1.2.3", id=None, seq=33, minutes=10,
titre="Héritage de classes et super()",
description="Réutiliser une classe existante et la compléter sans la recopier : la base de _inherit dans Odoo.",
html=fiche(
objectif="créer une classe qui hérite d'une autre, remplacer une méthode et garder son comportement d'origine avec <code>super()</code>.",
intro="Toute la force d'Odoo repose sur une idée : on ne modifie jamais le code d'origine, on le <b>complète</b>. Cette idée vient de l'héritage de classes, que tu vas voir en Python pur.",
corps=[
("h", "Hériter d'une classe"),
("code", """class CourseExpress(Course):
    \"\"\"Une course urgente : le livreur part tout de suite.\"\"\"

    def demarrer(self):
        super().demarrer()          # 1. on garde ce que fait la classe mère
        print(f"Express ! Le livreur part tout de suite pour {self.client}")  # 2. on ajoute


c3 = CourseExpress("Fatou Sarr", "Rufisque")
c3.demarrer()
print(c3.statut)                    # en_route : le travail de la classe mère est fait
print(isinstance(c3, Course))       # True : une CourseExpress EST une Course""", "Python (suite de classes.py)"),
("p", "<code>CourseExpress</code> récupère tout ce que sait faire <code>Course</code> (son <code>__init__</code>, ses attributs) et <b>remplace</b> la méthode <code>demarrer</code>."),
("h", "super() : ne pas casser l'existant"),
("p", "Sans la ligne <code>super().demarrer()</code>, le statut ne passerait plus à <code>en_route</code> : on aurait remplacé le comportement au lieu de le compléter."),
("attention", "Le bug le plus courant dans Odoo", "Quand on surcharge une méthode d'Odoo (par exemple <code>create</code> ou <code>action_confirm</code>), oublier <code>super()</code> ou oublier de <code>return</code> son résultat casse le fonctionnement standard. Règle : on appelle <code>super()</code> et on renvoie ce qu'il renvoie."),
("code", """def demarrer(self):
    resultat = super().demarrer()   # on récupère le résultat
    # ... notre ajout ...
    return resultat                 # et on le renvoie""", "Le bon modèle à suivre"),
("h", "Le lien avec Odoo"),
("p", "Dans Odoo, on écrira par exemple :"),
("code", """class ResPartner(models.Model):
    _inherit = "res.partner"        # on complète le modèle Contact existant
    est_livreur = fields.Boolean()""", "Aperçu du Bloc 2"),
("p", "Le mécanisme est un peu différent (Odoo assemble toutes les extensions d'un même modèle), mais l'esprit est le même : ajouter sans recopier, et appeler <code>super()</code>."),
],
exercice=[
("p", "Crée une classe <code>CourseFragile(Course)</code> dont l'<code>__init__</code> appelle <code>super().__init__(client, zone, poids)</code> puis ajoute un attribut <code>self.consigne = \"Manipuler avec soin\"</code>. Vérifie qu'une course fragile a bien un client, un statut <code>brouillon</code> et une consigne."),
],
retenir=[
  "<code>class Fille(Mere):</code> : la fille récupère tout ce que sait faire la mère.",
  "Redéfinir une méthode la remplace ; <code>super().methode()</code> appelle celle de la mère.",
  "Toujours appeler <code>super()</code> et renvoyer son résultat quand on surcharge une méthode d'Odoo.",
  "Dans Odoo, <code>_inherit</code> applique cette idée : compléter sans recopier.",
]),
quiz=[
("Que fait super().demarrer() dans la méthode demarrer d'une classe fille ?", [
  ("Il exécute la méthode demarrer de la classe mère", V, "Oui : on garde le comportement d'origine."),
  ("Il relance le programme", F, "Non."),
  ("Il supprime la méthode de la classe mère", F, "Non."),
]),
("On surcharge create dans Odoo mais on oublie super(). Que se passe-t-il ?", [
  ("Le comportement standard de create n'est plus exécuté", V, "Oui : on a remplacé au lieu de compléter."),
  ("Rien, Odoo appelle super() tout seul", F, "Non : c'est à toi de l'appeler."),
  ("Odoo refuse d'installer le module", F, "Non : il s'installe, mais il ne marche plus correctement."),
]),
("c3 est une CourseExpress, qui hérite de Course. Que renvoie isinstance(c3, Course) ?", [
  ("True", V, "Oui : une CourseExpress est aussi une Course."),
  ("False", F, "Non : l'héritage fait de c3 une Course."),
  ("Une erreur", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 1.2.4
dict(code="1.2.4", id=None, seq=34, minutes=10,
titre="Ce qu'Odoo utilise partout : décorateurs, compréhensions, *args et **kwargs",
description="Les écritures Python qu'on croise à chaque ligne du code d'Odoo.",
html=fiche(
objectif="reconnaître et comprendre les décorateurs, les compréhensions de liste et <code>*args</code> / <code>**kwargs</code>.",
intro="En ouvrant le code d'Odoo, tu verras des <code>@api.depends</code>, des <code>[x for x in …]</code> et des <code>**kwargs</code> partout. Ce ne sont pas des choses compliquées : ce sont des raccourcis.",
corps=[
("h", "Les décorateurs : @quelque_chose"),
("p", "Un décorateur s'écrit juste au-dessus d'une fonction et lui ajoute un comportement, sans toucher à son code :"),
("code", """import functools

def journaliser(fonction):
    @functools.wraps(fonction)
    def enveloppe(*args, **kwargs):
        print(f"→ appel de {fonction.__name__} avec {args} {kwargs}")
        return fonction(*args, **kwargs)
    return enveloppe

@journaliser
def prix(zone, poids=1, express=False):
    base = {"Plateau": 1000, "Mermoz": 1500}[zone]
    return base * 2 if express else base

print(prix("Mermoz", 3, express=True))
# → appel de prix avec ('Mermoz', 3) {'express': True}
# 3000""", "outils.py"),
("p", "Tu n'auras presque jamais à écrire un décorateur. Mais tu en <b>utiliseras</b> : <code>@api.depends(\"poids\")</code> dit à Odoo « recalcule ce champ quand le poids change », <code>@api.constrains</code> « vérifie cette règle à l'enregistrement »."),
("h", "Les compréhensions : une boucle en une ligne"),
("code", """courses = [{"client": "Awa", "zone": "Mermoz", "poids": 3.5},
           {"client": "Moussa", "zone": "Plateau", "poids": 8},
           {"client": "Fatou", "zone": "Mermoz", "poids": 12}]

clients = [c["client"] for c in courses]                  # ['Awa', 'Moussa', 'Fatou']
lourdes = [c["client"] for c in courses if c["poids"] > 5]  # ['Moussa', 'Fatou']
par_client = {c["client"]: c["zone"] for c in courses}    # un dictionnaire
total = sum(c["poids"] for c in courses)                  # 23.5""", "Python"),
("p", "<code>sorted(courses, key=lambda c: c[\"poids\"], reverse=True)</code> trie par poids décroissant : <code>lambda</code> est une petite fonction sans nom, écrite sur place."),
("h", "*args et **kwargs : des paramètres en nombre variable"),
("code", """def creer_course(client, *zones, **options):
    print(client, zones, options)

creer_course("Awa", "Mermoz", "Plateau", express=True, note="fragile")
# Awa ('Mermoz', 'Plateau') {'express': True, 'note': 'fragile'}

valeurs = {"client": "Ibou", "zone": "Médina"}
def resume(client, zone):
    return f"{client} → {zone}"
print(resume(**valeurs))       # Ibou → Médina : le dictionnaire est « déplié »""", "Python"),
("liste", [
  "<code>*args</code> récupère les valeurs sans nom dans un tuple.",
  "<code>**kwargs</code> récupère les valeurs nommées dans un dictionnaire.",
  "Dans Odoo, les méthodes surchargées s'écrivent souvent <code>def write(self, vals)</code> ou avec <code>**kwargs</code> pour transmettre tout à <code>super()</code>.",
]),
("astuce", "Dans Odoo", "Odoo fournit aussi ses propres outils qui ressemblent à des compréhensions : <code>courses.mapped(\"client\")</code>, <code>courses.filtered(lambda c: c.poids &gt; 5)</code>. On les verra au Bloc 2."),
],
exercice=[
("p", "À partir de la liste <code>courses</code> ci-dessus : (1) avec une compréhension, fais la liste des courses de la zone Mermoz ; (2) calcule le poids moyen ; (3) trie les clients par ordre alphabétique. Chaque réponse doit tenir en une ligne."),
],
retenir=[
  "Un décorateur <code>@…</code> ajoute un comportement à une fonction ; Odoo en utilise beaucoup (<code>@api.depends</code>, <code>@api.constrains</code>).",
  "<code>[x for x in liste if condition]</code> : une boucle et un filtre en une ligne.",
  "<code>lambda c: c[\"poids\"]</code> : une petite fonction sans nom.",
  "<code>*args</code> = valeurs sans nom, <code>**kwargs</code> = valeurs nommées.",
]),
quiz=[
("Que renvoie [c[\"client\"] for c in courses if c[\"poids\"] > 5] avec les courses de la leçon ?", [
  ("['Moussa', 'Fatou']", V, "Oui : seules ces deux courses dépassent 5 kg."),
  ("['Awa', 'Moussa', 'Fatou']", F, "Non : la condition if retire Awa (3,5 kg)."),
  ("23.5", F, "Non : c'est le poids total."),
]),
("Dans def f(*args, **kwargs), que contient kwargs ?", [
  ("Les valeurs passées avec un nom, dans un dictionnaire", V, "Oui."),
  ("Les valeurs passées sans nom, dans une liste", F, "Non : c'est args (un tuple)."),
  ("Le nom de la fonction", F, "Non."),
]),
("À quoi sert @api.depends(\"poids\") au-dessus d'une méthode Odoo ?", [
  ("À dire à Odoo de recalculer le champ quand le poids change", V, "Oui : c'est un décorateur fourni par Odoo."),
  ("À supprimer le champ poids", F, "Non."),
  ("À rendre le poids obligatoire", F, "Non : pour cela on écrit required=True sur le champ."),
]),
]),

# ---------------------------------------------------------------- 1.2.5
dict(code="1.2.5", id=2703, seq=35, minutes=10,
titre="Les dates, les nombres et le texte en Python (fuseau de Dakar, F CFA, accents)",
description="Éviter les pièges classiques : heures décalées, arrondis faux, accents.",
html=fiche(
objectif="manipuler des dates avec le bon fuseau horaire, arrondir correctement un montant et traiter du texte avec accents.",
intro="Trois sources de bugs reviennent sans cesse chez les clients : une livraison affichée avec une heure de décalage, un total faux d'un franc, un nom « MÃ©dina » à l'écran. Voici comment les éviter.",
corps=[
("h", "Les dates"),
("code", """from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

aujourd_hui = date(2026, 11, 21)
echeance = aujourd_hui + timedelta(days=30)
print(echeance.strftime("%d/%m/%Y"))          # 21/12/2026
print((echeance - aujourd_hui).days)          # 30

depart = datetime(2026, 11, 21, 9, 30, tzinfo=ZoneInfo("Africa/Dakar"))
print(depart.astimezone(ZoneInfo("Europe/Paris")).strftime("%H:%M"))   # 10:30
print(datetime.strptime("21/11/2026 14:05", "%d/%m/%Y %H:%M"))      # texte → date""", "dates.py"),
("p", "Dakar est à l'heure UTC toute l'année (pas d'heure d'été). Mais un client à Paris, à Abidjan ou à Douala ne voit pas la même heure."),
("astuce", "Dans Odoo", "Dans Odoo (toutes versions récentes, 20 compris), les champs Date et Heure sont <b>enregistrés en UTC</b>, sans fuseau. Odoo les convertit au fuseau de l'utilisateur seulement à l'affichage. Règle : dans ton code, travaille en UTC ; pour afficher une heure locale dans un document, utilise <code>fields.Datetime.context_timestamp(record, valeur)</code>."),
("h", "Les nombres et l'argent"),
("code", """print(0.1 + 0.2)              # 0.30000000000000004
print(0.1 + 0.2 == 0.3)       # False !
print(round(2.5), round(3.5)) # 2 4 : Python arrondit au pair le plus proche

from decimal import Decimal, ROUND_HALF_UP
print(Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))  # 2.68""", "Python"),
("p", "Ne compare jamais deux montants à virgule avec <code>==</code>. Odoo fournit ses propres outils, qui respectent les règles d'arrondi de la devise :"),
("code", """from odoo.tools import float_compare, float_round
float_round(2.675, precision_digits=2)               # 2.68
float_compare(0.1 + 0.2, 0.3, precision_digits=2)   # 0 = égaux""", "Dans Odoo 20 (testé)"),
("astuce", "Le franc CFA", "Le franc CFA n'a pas de centimes : dans Odoo, la devise XOF est réglée sans décimale. Pour un affichage à la française : <code>f\"{1234567:,}\".replace(\",\", \" \") + \" F CFA\"</code> donne <code>1 234 567 F CFA</code>."),
("h", "Le texte et les accents"),
("code", """nom = "Médina"
print(len(nom), len(nom.encode("utf-8")))   # 6 caractères, mais 7 octets
print(nom.lower() == "medina")              # False : é n'est pas e
print(" Awa  Diop ".strip())                # 'Awa  Diop' : espaces du bord retirés
print("awa diop".title())                   # 'Awa Diop'""", "Python"),
("p", "Python 3 et Odoo travaillent en <b>UTF-8</b> : les accents marchent, à condition que tes fichiers soient enregistrés en UTF-8 (c'est le cas par défaut dans VS Code). Les « Ã© » à l'écran viennent presque toujours d'un fichier CSV enregistré dans un autre encodage."),
],
exercice=[
("p", "Écris une fonction <code>date_limite(date_course)</code> qui renvoie la date de la course + 2 jours, au format <code>jj/mm/aaaa</code>. Puis écris <code>prix_ttc(prix_ht)</code> qui ajoute 18 % de TVA et renvoie un entier arrondi au franc supérieur à partir de 0,5 (utilise <code>Decimal</code> et <code>ROUND_HALF_UP</code>). Teste avec 1 525 F HT (résultat attendu : 1 800 F)."),
],
retenir=[
  "Utilise <code>zoneinfo</code> pour les fuseaux ; Dakar = UTC toute l'année.",
  "Odoo enregistre les dates-heures en UTC et convertit seulement à l'affichage.",
  "Ne compare pas des nombres à virgule avec <code>==</code> ; dans Odoo, utilise <code>float_compare</code> et <code>float_round</code>.",
  "Tout en UTF-8 : les accents posent problème surtout dans les fichiers CSV importés.",
]),
quiz=[
("Comment Odoo enregistre-t-il un champ Datetime en base ?", [
  ("En UTC, sans fuseau horaire", V, "Oui : la conversion se fait à l'affichage, selon le fuseau de l'utilisateur."),
  ("À l'heure de Dakar", F, "Non : toujours en UTC."),
  ("À l'heure de l'ordinateur du développeur", F, "Non."),
]),
("Que renvoie 0.1 + 0.2 == 0.3 en Python ?", [
  ("False", V, "Oui : les nombres à virgule ne sont pas exacts. D'où float_compare dans Odoo."),
  ("True", F, "Non : 0.1 + 0.2 vaut 0.30000000000000004."),
  ("Une erreur", F, "Non : Python répond simplement False."),
]),
("Un client voit « MÃ©dina » après un import CSV. Quelle est la cause la plus probable ?", [
  ("Le fichier CSV n'était pas enregistré en UTF-8", V, "Oui : réenregistre-le en UTF-8 avant l'import."),
  ("Odoo ne gère pas les accents", F, "Non : Odoo gère très bien l'UTF-8."),
  ("Le fuseau horaire est faux", F, "Non, rien à voir."),
]),
]),

# ---------------------------------------------------------------- 1.2.6
dict(code="1.2.6", id=2704, seq=36, minutes=10,
titre="Les erreurs et le débogage : lire une trace d'erreur, utiliser pdb",
description="Lire une trace d'erreur de bas en haut et arrêter le programme pour regarder dedans.",
html=fiche(
objectif="lire une trace d'erreur Python et arrêter un programme avec <code>breakpoint()</code> pour inspecter les variables.",
intro="Une trace d'erreur (« traceback ») fait peur la première fois. En réalité, elle te dit exactement ce qui s'est passé et où. Il suffit de savoir la lire.",
corps=[
("h", "Un programme qui plante"),
("code", """TARIFS = {"Plateau": 1000, "Mermoz": 1500}

def prix_course(zone, poids):
    prix = TARIFS[zone]
    if poids > 5:
        prix += (poids - 5) * 200
    return prix

def total_journee(courses):
    total = 0
    for zone, poids in courses:
        total += prix_course(zone, poids)
    return total

print(total_journee([("Mermoz", 3), ("Yoff", 2)]))""", "bug.py"),
("code", """Traceback (most recent call last):
  File "/home/awa/baobab/bug.py", line 15, in <module>
    print(total_journee([("Mermoz", 3), ("Yoff", 2)]))
  File "/home/awa/baobab/bug.py", line 12, in total_journee
    total += prix_course(zone, poids)
  File "/home/awa/baobab/bug.py", line 4, in prix_course
    prix = TARIFS[zone]
           ~~~~~~^^^^^^
KeyError: 'Yoff'""", "Résultat"),
("h", "Lire de bas en haut"),
("liste", [
  "<b>La dernière ligne</b> dit quoi : <code>KeyError: 'Yoff'</code>, la clé « Yoff » n'existe pas dans un dictionnaire.",
  "<b>Juste au-dessus</b>, où : fichier <code>bug.py</code>, ligne 4, dans <code>prix_course</code>.",
  "<b>En remontant</b>, le chemin suivi : la ligne 15 a appelé <code>total_journee</code>, qui a appelé <code>prix_course</code>.",
]),
("astuce", "Dans Odoo", "Les traces d'Odoo sont plus longues, car elles traversent le code d'Odoo lui-même. Cherche la dernière ligne, puis remonte jusqu'à la première ligne qui parle de <b>ton</b> module (<code>baobab_livraison/…</code>) : c'est là qu'il faut regarder."),
("h", "Arrêter le programme pour regarder : breakpoint()"),
("p", "Ajoute <code>breakpoint()</code> juste avant la ligne suspecte :"),
("code", """def prix_course(zone, poids):
    breakpoint()            # le programme s'arrête ici
    prix = TARIFS[zone]""", "bug.py"),
("p", "Relance le script : tu entres dans le débogueur <b>pdb</b>."),
("tableau", ["Commande pdb", "Effet"], [
  ["<code>p zone</code>", "afficher une variable"],
  ["<code>n</code>", "exécuter la ligne suivante"],
  ["<code>s</code>", "entrer dans la fonction appelée"],
  ["<code>c</code>", "continuer jusqu'au prochain arrêt"],
  ["<code>q</code>", "quitter"],
]),
("attention", "Ne l'oublie pas dans ton code", "Un <code>breakpoint()</code> oublié bloque Odoo en production. Retire-le avant chaque commit. Dans la section Git et environnement, on verra le débogueur de VS Code, plus confortable et sans risque d'oubli."),
("h", "Les erreurs que tu croiseras le plus"),
("tableau", ["Erreur", "Signifie souvent"], [
  ["<code>KeyError</code>", "clé absente d'un dictionnaire"],
  ["<code>AttributeError</code>", "attribut ou méthode qui n'existe pas (faute de frappe ?)"],
  ["<code>TypeError</code>", "mauvais type, ou mauvais nombre de paramètres"],
  ["<code>IndentationError</code> / <code>SyntaxError</code>", "code mal écrit : deux-points, parenthèse, espaces"],
  ["<code>ModuleNotFoundError</code>", "bibliothèque non installée ou environnement virtuel non activé"],
]),
],
exercice=[
("p", "Recopie <code>bug.py</code>, lance-le et lis la trace. Ajoute <code>breakpoint()</code> dans <code>prix_course</code>, relance, et avec <code>p zone</code> puis <code>c</code>, trouve à quel tour de boucle l'erreur arrive. Corrige ensuite la fonction pour qu'une zone inconnue lève une <code>ValueError</code> avec un message clair (comme dans la leçon 1.0.6)."),
],
retenir=[
  "Une trace se lit de bas en haut : quoi (dernière ligne), puis où, puis le chemin.",
  "Dans Odoo, remonte jusqu'à la première ligne qui parle de ton module.",
  "<code>breakpoint()</code> arrête le programme ; <code>p</code>, <code>n</code>, <code>c</code>, <code>q</code> dans pdb.",
  "Retire tout <code>breakpoint()</code> avant de committer.",
]),
quiz=[
("Dans une trace d'erreur Python, où lit-on le type d'erreur ?", [
  ("À la dernière ligne", V, "Oui : par exemple KeyError: 'Yoff'."),
  ("À la première ligne", F, "Non : la première ligne dit seulement « Traceback (most recent call last) »."),
  ("Dans le journal de PostgreSQL", F, "Non."),
]),
("Dans pdb, quelle commande affiche la valeur de la variable zone ?", [
  ("p zone", V, "Oui."),
  ("print zone", F, "Presque : dans pdb, la commande courte est p."),
  ("c zone", F, "Non : c continue l'exécution."),
]),
("Que signifie souvent AttributeError ?", [
  ("On utilise un attribut ou une méthode qui n'existe pas, souvent une faute de frappe", V, "Oui."),
  ("Le serveur est éteint", F, "Non."),
  ("Une clé manque dans un dictionnaire", F, "Non : c'est KeyError."),
]),
]),
]
