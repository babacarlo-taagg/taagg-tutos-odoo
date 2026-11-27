"""Bloc 2 — Section « Le modèle (ORM) » (section 2717, cours 209).
Code et sorties vérifiés sur Odoo 20.0 le 27/11/2026 (module de référence, base de test, odoo-bin shell)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

ZONE = """from odoo import fields, models


class BaobabZone(models.Model):
    _name = "baobab.zone"                  # nom technique : table baobab_zone
    _description = "Zone de livraison"     # nom lisible
    _order = "tarif, name"                 # tri par défaut

    name = fields.Char("Zone", required=True)
    tarif = fields.Monetary("Tarif de base", required=True, currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency", string="Devise", required=True,
        default=lambda self: self.env.company.currency_id,
    )
    active = fields.Boolean(default=True)"""

CHAMPS_COURSE = """class BaobabCourse(models.Model):
    _name = "baobab.course"
    _description = "Course de livraison"
    _order = "date_course desc, id desc"

    name = fields.Char("Référence", required=True, readonly=True, copy=False, default="Nouveau")
    poids = fields.Float("Poids (kg)", default=1.0)
    date_course = fields.Date("Date", required=True, default=fields.Date.context_today)
    state = fields.Selection(
        [("brouillon", "Brouillon"), ("en_route", "En route"),
         ("livree", "Livrée"), ("annulee", "Annulée")],
        string="Statut", required=True, default="brouillon",
    )
    consigne = fields.Text("Consigne")
    date_livraison = fields.Datetime("Livrée le", readonly=True, copy=False)"""

LECONS = [
# ---------------------------------------------------------------- 2.2.1
dict(code="2.2.1", id=1355, seq=21, minutes=10,
titre="Premier modèle : les zones de livraison",
description="Écrire le modèle baobab.zone, l'installer et créer des zones depuis le terminal d'Odoo.",
html=fiche(
objectif="écrire ton premier modèle, <code>baobab.zone</code>, et y créer des fiches depuis le terminal d'Odoo.",
intro="Un <b>modèle</b>, c'est la description d'un type de fiche : ses informations (les champs) et son comportement (les méthodes). Odoo s'occupe du reste : il crée la table dans PostgreSQL et sait lire et écrire les fiches. C'est ce qu'on appelle l'ORM.",
corps=[
("h", "Le modèle des zones"),
("code", ZONE, "models/zone.py"),
("liste", [
  "<code>_name</code> : le nom technique, avec des points. Odoo crée la table <code>baobab_zone</code>.",
  "<code>_description</code> : le nom affiché (obligatoire en pratique : Odoo avertit s'il manque).",
  "Chaque <code>fields.Quelquechose(...)</code> devient une colonne de la table.",
  "Odoo ajoute tout seul <code>id</code>, <code>create_date</code>, <code>create_uid</code>, <code>write_date</code>, <code>write_uid</code>.",
]),
("p", "N'oublie pas <code>from . import zone</code> dans <code>models/__init__.py</code>, puis mets à jour le module (<code>-u</code>). Le droit d'accès vient dans deux leçons : en attendant, on travaille dans le terminal d'Odoo, qui a tous les droits."),
("h", "Créer des zones depuis le terminal d'Odoo"),
("code", """python3 odoo-bin shell -c ~/baobab/odoo.conf""", "Terminal : ouvrir le terminal d'Odoo"),
("code", """>>> Zone = env["baobab.zone"]
>>> z = Zone.create({"name": "Mermoz", "tarif": 1500})
>>> z.name, z.tarif
('Mermoz', 1500.0)
>>> env.cr.commit()        # enregistre pour de bon dans la base""", "Terminal d'Odoo (Python)"),
("p", "<code>env</code> donne accès à tous les modèles. <code>env.cr.commit()</code> valide l'enregistrement : sans lui, en quittant le terminal, tout est annulé (pratique pour faire des essais)."),
("astuce", "Qui suis-je dans ce terminal ?", "Dans <code>odoo-bin shell</code>, tu travailles en tant qu'<b>OdooBot</b>, le super-utilisateur : aucune règle de droit ne s'applique. Pratique pour tester, mais ce n'est pas ce que verra un vrai utilisateur."),
("version", "Le tri par défaut <code>_order</code> et le champ <code>active</code> (archivage) fonctionnent de la même façon depuis de nombreuses versions. En Odoo 20, le champ <code>tarif</code> est un <code>Monetary</code> : il s'affiche avec la devise de la société (XOF pour une société sénégalaise)."),
],
exercice=[
("p", "Écris <code>models/zone.py</code>, installe-le avec <code>-u</code>, puis dans le terminal d'Odoo crée les six zones : Plateau 1 000, Médina 1 000, Mermoz 1 500, Parcelles Assainies 2 000, Pikine 2 500, Rufisque 3 000. Valide avec <code>env.cr.commit()</code>. Vérifie dans <code>psql</code> : <code>SELECT name, tarif FROM baobab_zone;</code>"),
],
retenir=[
  "Un modèle = une classe qui hérite de <code>models.Model</code>, avec un <code>_name</code>.",
  "Odoo crée la table (<code>baobab.zone</code> → <code>baobab_zone</code>) et les colonnes.",
  "<code>odoo-bin shell</code> ouvre un terminal Python dans Odoo ; <code>env.cr.commit()</code> enregistre.",
  "Dans ce terminal, tu es OdooBot : aucun droit ne t'arrête.",
]),
quiz=[
("Quelle table PostgreSQL Odoo crée-t-il pour le modèle baobab.zone ?", [
  ("baobab_zone", V, "Oui : les points deviennent des tirets bas."),
  ("zone", F, "Non : la table garde tout le nom technique."),
  ("baobab.zone", F, "Non : un point n'est pas permis dans un nom de table."),
]),
("Dans odoo-bin shell, que se passe-t-il si tu quittes sans env.cr.commit() ?", [
  ("Les fiches créées sont annulées", V, "Oui : rien n'est enregistré pour de bon."),
  ("Elles sont enregistrées quand même", F, "Non."),
  ("Odoo plante", F, "Non : il annule simplement."),
]),
("Quels champs Odoo ajoute-t-il tout seul à chaque modèle ?", [
  ("id, create_date, create_uid, write_date, write_uid", V, "Oui."),
  ("name et active", F, "Non : ceux-là, c'est toi qui les déclares."),
  ("Aucun", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.2.2
dict(code="2.2.2", id=2915, seq=22, minutes=10,
titre="Les types de champs",
description="Texte, nombres, dates, montants, listes de choix : choisir le bon type de champ.",
html=fiche(
objectif="choisir le bon type de champ pour chaque information d'une course de livraison.",
intro="Une course a une référence, un poids, une date, un statut, une consigne… Chaque information a son type de champ. Bien choisir le type, c'est éviter des calculs faux et des écrans peu pratiques.",
corps=[
("code", CHAMPS_COURSE, "models/course.py (premiers champs de la course)"),
("h", "Les types les plus utiles"),
("tableau", ["Type", "Pour…", "Exemple Baobab"], [
  ["<code>Char</code>", "un texte court", "la référence BL/2026/0001"],
  ["<code>Text</code>", "un texte long", "la consigne pour le livreur"],
  ["<code>Integer</code>", "un nombre entier", "un nombre de colis"],
  ["<code>Float</code>", "un nombre à virgule", "le poids : 3,5 kg"],
  ["<code>Monetary</code>", "un montant, avec sa devise", "le tarif, le prix"],
  ["<code>Boolean</code>", "oui / non", "est-ce un livreur ?"],
  ["<code>Date</code> / <code>Datetime</code>", "une date / une date et une heure", "date de la course / heure de livraison"],
  ["<code>Selection</code>", "un choix dans une liste fixe", "le statut"],
]),
("h", "Les options qu'on retrouve partout"),
("liste", [
  "<code>string</code> (le premier texte) : le libellé affiché.",
  "<code>required=True</code> : obligatoire.",
  "<code>default=…</code> : valeur proposée à la création. Une fonction est appelée à chaque création : <code>fields.Date.context_today</code> donne la date du jour de l'utilisateur.",
  "<code>readonly=True</code> : non modifiable à l'écran.",
  "<code>copy=False</code> : la valeur n'est pas recopiée quand on duplique la fiche (une référence doit rester unique).",
  "<code>help=\"…\"</code> : une bulle d'aide au survol.",
]),
("h", "Monetary : un montant a toujours une devise"),
("p", "Un champ <code>Monetary</code> a besoin d'un champ devise (<code>currency_field</code>). Il respecte alors les règles d'arrondi de la devise : le franc CFA (XOF) n'a pas de centimes."),
("attention", "Les noms techniques", "Une fois installés chez un client, les noms des champs ne se changent plus à la légère (il faut un script de migration). Choisis des noms clairs dès le départ : <code>poids</code>, <code>date_course</code>, pas <code>x1</code> ou <code>champ2</code>."),
("version", "Ces types de champs existent depuis longtemps et se déclarent de la même façon en Odoo 18, 19 et 20. Nouveauté interne d'Odoo 20 : les champs Binary (fichiers) manipulent un objet <code>BinaryValue</code> au lieu de texte en base64."),
],
exercice=[
("p", "Crée <code>models/course.py</code> avec les champs ci-dessus, ajoute l'import et mets à jour le module. Dans le terminal d'Odoo, crée une course sans préciser la date ni le statut, et vérifie qu'elle a bien la date du jour et le statut <code>brouillon</code>."),
],
retenir=[
  "Char/Text pour le texte, Integer/Float pour les nombres, Monetary pour l'argent.",
  "Selection pour une liste de choix fixe (statut).",
  "<code>required</code>, <code>default</code>, <code>readonly</code>, <code>copy</code>, <code>help</code> : les options courantes.",
  "Des noms de champs clairs dès le départ : ils sont difficiles à changer ensuite.",
]),
quiz=[
("Quel type de champ pour le prix d'une course ?", [
  ("Monetary", V, "Oui : un montant avec sa devise et ses règles d'arrondi."),
  ("Char", F, "Non : on ne pourrait pas faire de calcul."),
  ("Boolean", F, "Non : c'est un oui/non."),
]),
("Pourquoi copy=False sur la référence de la course ?", [
  ("Pour qu'une copie de la course n'ait pas la même référence", V, "Oui : une référence doit rester unique."),
  ("Pour interdire de lire la référence", F, "Non."),
  ("Pour rendre le champ obligatoire", F, "Non : c'est required=True."),
]),
("default=fields.Date.context_today sur date_course : que se passe-t-il ?", [
  ("Une nouvelle course prend la date du jour de l'utilisateur", V, "Oui : la fonction est appelée à chaque création."),
  ("La date ne peut plus être modifiée", F, "Non : c'est seulement une valeur proposée."),
  ("Toutes les courses ont la date d'installation du module", F, "Non : la fonction est appelée à chaque création."),
]),
]),

# ---------------------------------------------------------------- 2.2.3
dict(code="2.2.3", id=2916, seq=23, minutes=10,
titre="Les relations : Many2one, One2many, Many2many",
description="Relier une course à son client, à sa zone, à ses étiquettes.",
html=fiche(
objectif="relier les courses aux clients, aux zones et aux étiquettes avec les trois types de relations.",
intro="Une course appartient à un client et à une zone ; une zone a plusieurs courses ; une course peut porter plusieurs étiquettes (Fragile, Urgent). Ce sont les trois relations d'Odoo.",
corps=[
("h", "Many2one : « plusieurs courses → un client »"),
("code", """client_id = fields.Many2one("res.partner", string="Client", required=True)
zone_id = fields.Many2one("baobab.zone", string="Zone", required=True)
livreur_id = fields.Many2one("res.partner", string="Livreur")   # complété en 2.4.1""", "models/course.py"),
("p", "Dans la base, c'est une colonne <code>client_id</code> qui contient l'<code>id</code> du client, avec une clé étrangère. Par convention, le nom finit par <code>_id</code>."),
("h", "One2many : « une zone → plusieurs courses »"),
("code", """course_ids = fields.One2many("baobab.course", "zone_id", string="Courses")""", "models/zone.py"),
("p", "C'est l'autre côté du Many2one <code>zone_id</code> : aucune colonne n'est créée, Odoo cherche les courses dont <code>zone_id</code> pointe vers cette zone. Nom par convention : <code>…_ids</code>."),
("h", "Many2many : « plusieurs courses ↔ plusieurs étiquettes »"),
("code", """# models/etiquette.py
class BaobabEtiquette(models.Model):
    _name = "baobab.etiquette"
    _description = "Étiquette de course"

    name = fields.Char("Étiquette", required=True)
    color = fields.Integer("Couleur")

# models/course.py
etiquette_ids = fields.Many2many("baobab.etiquette", string="Étiquettes")""", "Deux modèles reliés"),
("p", "Odoo crée une table de liaison : ici <code>baobab_course_baobab_etiquette_rel</code> (vérifié sur Odoo 20)."),
("h", "Lire et remplir une relation"),
("code", """>>> c = env["baobab.course"].search([("poids", "<", 5)], limit=1)
>>> c.zone_id.name, c.zone_id.tarif        # on « traverse » la relation avec un point
('Mermoz', 1500.0)
>>> c.etiquette_ids.mapped("name")
['Fragile']
>>> urgent = env["baobab.etiquette"].search([("name", "=", "Urgent")])
>>> c.etiquette_ids = [Command.link(urgent.id)]   # ajouter une étiquette
>>> c.etiquette_ids.mapped("name")
['Fragile', 'Urgent']""", "Terminal d'Odoo"),
("astuce", "Command", "Pour modifier un One2many ou un Many2many, on utilise <code>Command</code> : <code>Command.link(id)</code> ajoute, <code>Command.unlink(id)</code> retire, <code>Command.set([ids])</code> remplace tout, <code>Command.create({...})</code> crée et relie. Dans un fichier Python : <code>from odoo.fields import Command</code>."),
],
exercice=[
("p", "Ajoute le modèle <code>baobab.etiquette</code> (nouveau fichier, import, mise à jour), puis les champs <code>client_id</code>, <code>zone_id</code>, <code>livreur_id</code> et <code>etiquette_ids</code> à la course, et <code>course_ids</code> à la zone. Dans le terminal d'Odoo, crée une course pour Mermoz avec l'étiquette Fragile, puis affiche <code>zone.course_ids</code> pour la zone Mermoz."),
],
retenir=[
  "Many2one (<code>…_id</code>) : une colonne qui pointe vers une autre fiche.",
  "One2many (<code>…_ids</code>) : l'autre côté d'un Many2one, sans colonne.",
  "Many2many (<code>…_ids</code>) : une table de liaison.",
  "On traverse une relation avec un point : <code>course.zone_id.tarif</code>.",
]),
quiz=[
("Une course a un seul client, un client a plusieurs courses. Quel champ sur la course ?", [
  ("Un Many2one vers res.partner", V, "Oui : client_id."),
  ("Un One2many vers res.partner", F, "Non : le One2many est de l'autre côté (sur le client)."),
  ("Un Many2many", F, "Non : une course n'a qu'un client."),
]),
("Un champ One2many crée-t-il une colonne dans la table ?", [
  ("Non : il s'appuie sur le Many2one de l'autre modèle", V, "Oui."),
  ("Oui, une colonne par fiche liée", F, "Non."),
  ("Oui, une table de liaison", F, "Non : c'est le cas du Many2many."),
]),
("Comment ajouter l'étiquette e à la course c sans retirer les autres ?", [
  ("c.etiquette_ids = [Command.link(e.id)]", V, "Oui : link ajoute sans toucher aux autres."),
  ("c.etiquette_ids = [Command.set([e.id])]", F, "Non : set remplace toute la liste."),
  ("c.etiquette_ids = e.name", F, "Non : une relation attend des fiches, pas un texte."),
]),
]),

# ---------------------------------------------------------------- 2.2.4
dict(code="2.2.4", id=2917, seq=24, minutes=10,
titre="Le droit minimum pour voir son modèle (ir.access.csv)",
description="Donner aux utilisateurs le droit de lire et modifier les courses : le fichier ir.access.csv d'Odoo 20.",
html=fiche(
objectif="donner aux utilisateurs le droit d'utiliser tes modèles, avec le fichier <code>security/ir.access.csv</code>.",
intro="Ton modèle existe, tu le manipules dans le terminal… mais pour un vrai utilisateur, il est invisible. Dans Odoo, tout est interdit par défaut : il faut donner des droits.",
corps=[
("h", "Sans droit : rien du tout"),
("p", "On a installé un modèle sans aucun droit : Odoo 20 l'installe <b>sans le moindre avertissement</b>, puis l'administrateur lui-même reçoit :"),
("code", """AccessError : You are not allowed to access 'Chose' (essai.chose) records.
No group currently allows this operation.""", "Odoo 20, vérifié le 27/11/2026"),
("h", "Le fichier ir.access.csv"),
("code", """id,name,model_id,group_id/id,operation,domain
access_baobab_zone_user,Zones : utilisateurs,baobab.zone,base.group_user,crud,
access_baobab_etiquette_user,Étiquettes : utilisateurs,baobab.etiquette,base.group_user,crud,
access_baobab_course_user,Courses : utilisateurs,baobab.course,base.group_user,crud,""", "security/ir.access.csv"),
("tableau", ["Colonne", "Signification"], [
  ["<code>id</code>", "identifiant unique de la ligne"],
  ["<code>name</code>", "description lisible"],
  ["<code>model_id</code>", "le nom technique du modèle : <code>baobab.course</code>"],
  ["<code>group_id/id</code>", "le groupe concerné : <code>base.group_user</code> = tous les utilisateurs internes"],
  ["<code>operation</code>", "les lettres des opérations permises : <b>c</b>réer, <b>r</b>ead (lire), <b>u</b>pdate (modifier), <b>d</b>elete (supprimer). <code>crud</code> = tout, <code>r</code> = lecture seule"],
  ["<code>domain</code>", "facultatif : limiter le droit à certaines fiches (Bloc 4)"],
]),
("p", "Ajoute <code>\"security/ir.access.csv\"</code> <b>en premier</b> dans la liste <code>data</code> du manifeste, puis <code>-u</code>."),
("version", "C'est le grand changement d'Odoo 20. <b>Avant (Odoo 18 et 19)</b> : fichier <code>security/ir.model.access.csv</code>, modèle <code>ir.model.access</code>, colonnes <code>id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink</code>, et des règles séparées (<code>ir.rule</code>) pour limiter aux bonnes fiches. <b>Odoo 20</b> : un seul fichier <code>ir.access.csv</code>, modèle <code>ir.access</code>, qui réunit les droits et les règles. Le modèle <code>ir.model.access</code> n'existe plus : un ancien fichier empêche la base de démarrer."),
("astuce", "Pour la suite", "Ici, tout le monde a tous les droits sur les courses. Au Bloc 4, on créera les groupes Livreur et Responsable, et un livreur ne verra que ses propres courses (colonne <code>domain</code>)."),
],
exercice=[
("p", "Crée <code>security/ir.access.csv</code> pour tes trois modèles, ajoute-le au manifeste et mets à jour. Ajoute aussi le fichier des menus ci-dessous (après <code>ir.access.csv</code> dans <code>data</code>). Connecte-toi en admin : le menu Baobab Livraison apparaît et tu peux créer une zone à l'écran. Odoo fabrique tout seul des écrans simples ; les vrais écrans arrivent à la leçon « Statuts et boutons d'action »."),
("code", """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Fourni au Bloc 2 sans explication détaillée : les vues, actions et menus sont l'objet du Bloc 3. -->
    <record id="action_baobab_course" model="ir.actions.act_window">
        <field name="name">Courses</field>
        <field name="res_model">baobab.course</field>
        <field name="view_mode">list,form</field>
    </record>
    <record id="action_baobab_zone" model="ir.actions.act_window">
        <field name="name">Zones</field>
        <field name="res_model">baobab.zone</field>
        <field name="view_mode">list,form</field>
    </record>
    <menuitem id="menu_baobab_root" name="Baobab Livraison" sequence="10"/>
    <menuitem id="menu_baobab_course" name="Courses" parent="menu_baobab_root" action="action_baobab_course" sequence="10"/>
    <menuitem id="menu_baobab_zone" name="Zones" parent="menu_baobab_root" action="action_baobab_zone" sequence="20"/>
</odoo>""", "views/baobab_menus.xml (fichier fourni : les menus s'apprennent au Bloc 3)"),
],
retenir=[
  "Dans Odoo, tout est interdit par défaut : un modèle sans droit est invisible.",
  "Odoo 20 : <code>security/ir.access.csv</code>, colonnes <code>id,name,model_id,group_id/id,operation,domain</code>.",
  "<code>operation</code> : c, r, u, d (<code>crud</code> = tout).",
  "Odoo 18-19 : <code>ir.model.access.csv</code> + <code>ir.rule</code>. À ne pas mélanger.",
]),
quiz=[
("En Odoo 20, quel fichier donne les droits d'accès d'un module ?", [
  ("security/ir.access.csv", V, "Oui : modèle ir.access."),
  ("security/ir.model.access.csv", F, "Non : c'était le fichier d'Odoo 18 et 19."),
  ("__manifest__.py", F, "Non : le manifeste liste le fichier, il ne contient pas les droits."),
]),
("Dans la colonne operation, que veut dire r ?", [
  ("Lecture seule (read)", V, "Oui."),
  ("Supprimer", F, "Non : c'est d (delete)."),
  ("Tout", F, "Non : tout s'écrit crud."),
]),
("Un modèle installé sans aucun droit : que voit l'administrateur ?", [
  ("Une erreur « You are not allowed to access… »", V, "Oui : même l'administrateur est bloqué, seul le super-utilisateur passe."),
  ("Toutes les fiches, comme d'habitude", F, "Non : tout est interdit par défaut."),
  ("Un avertissement à l'installation", F, "Non : Odoo 20 n'avertit pas à l'installation."),
]),
]),

# ---------------------------------------------------------------- 2.2.5
dict(code="2.2.5", id=2718, seq=25, minutes=10,
titre="Lire, créer, modifier, chercher : search, create, write, les domaines",
description="Les quatre gestes de l'ORM et l'art d'écrire un domaine de recherche.",
html=fiche(
objectif="créer, chercher, modifier et supprimer des fiches avec l'ORM, et écrire des domaines de recherche.",
intro="Tout le code d'Odoo repose sur quelques méthodes de base. On les essaie dans le terminal d'Odoo sur les courses de démonstration : deux courses d'Awa Diop, une pour Mermoz (3,5 kg) et une pour Rufisque (12 kg).",
corps=[
("h", "Les gestes de base"),
("code", """C = env["baobab.course"]
c = C.create({"client_id": awa.id, "zone_id": mermoz.id, "poids": 2})   # créer
C.search([("poids", ">", 5)])                                           # chercher
C.search_count([("zone_id.tarif", ">=", 1500)])                         # compter
c.write({"poids": 4})            # modifier (ou simplement : c.poids = 4)
c.unlink()                       # supprimer""", "Terminal d'Odoo"),
("h", "Les domaines : la langue des filtres"),
("p", "Un domaine est une liste de conditions <code>(champ, opérateur, valeur)</code> :"),
("code", """[("poids", ">", 5)]                                  # plus de 5 kg
[("state", "=", "brouillon"), ("poids", ">", 5)]     # ET (par défaut)
["|", ("state", "=", "en_route"), ("state", "=", "livree")]   # OU, écrit avant
[("state", "in", ["en_route", "livree"])]            # même chose, plus lisible
[("zone_id.tarif", ">=", 1500)]                      # en traversant une relation
[("client_id.name", "ilike", "awa")]                 # contient, sans tenir compte des majuscules""", "Exemples de domaines"),
("code", """>>> C.search_count([("zone_id.tarif", ">=", 1500)])
2
>>> C.search([("state", "=", "brouillon")], order="prix desc", limit=1).name
'BL/2026/0002'
>>> C.search_read([("poids", ">", 5)], ["name", "prix"])
[{'id': 2, 'name': 'BL/2026/0002', 'prix': 4400.0}]""", "Résultats réels sur la base de démonstration"),
("h", "Écrire un domaine en Python : Domain"),
("code", """from odoo.fields import Domain

d = Domain("poids", ">", 5) & Domain("state", "=", "brouillon")
print(d)                           # ['&', ('poids', '>', 5), ('state', '=', 'brouillon')]
C.search(d).mapped("name")         # ['BL/2026/0002']""", "Odoo 20"),
("version", "La classe <code>Domain</code> existe depuis Odoo 18.1 : elle permet de combiner des conditions avec <code>&amp;</code> et <code>|</code>. Les listes classiques restent valables partout. En Odoo 20, on l'importe avec <code>from odoo.fields import Domain</code>, comme dans le module Ventes."),
("attention", "search ne renvoie pas une liste Python", "<code>search</code> renvoie un <b>recordset</b> (un ensemble de fiches), même s'il n'y en a qu'une ou aucune. On le parcourt avec une boucle ou on utilise ses outils (leçon suivante)."),
],
exercice=[
("p", "Dans le terminal d'Odoo, écris les domaines qui trouvent : (1) les courses de plus de 3 kg en brouillon ; (2) les courses des zones Plateau ou Médina ; (3) les courses dont le client contient « diop ». Puis passe toutes les courses de Mermoz à 2 kg avec un seul <code>write</code>."),
],
retenir=[
  "<code>create</code>, <code>search</code>, <code>search_count</code>, <code>write</code>, <code>unlink</code>.",
  "Un domaine = liste de <code>(champ, opérateur, valeur)</code> ; ET par défaut, <code>\"|\"</code> pour OU.",
  "On traverse les relations : <code>zone_id.tarif</code>.",
  "<code>search</code> renvoie un recordset, pas une liste.",
]),
quiz=[
("Que renvoie C.search([(\"poids\", \">\", 5)]) ?", [
  ("Un recordset des courses de plus de 5 kg", V, "Oui."),
  ("Le nombre de courses de plus de 5 kg", F, "Non : c'est search_count."),
  ("Une liste de dictionnaires", F, "Non : c'est search_read."),
]),
("Comment écrire « statut en route OU livrée » ?", [
  ("[(\"state\", \"in\", [\"en_route\", \"livree\"])]", V, "Oui (ou avec \"|\" devant les deux conditions)."),
  ("[(\"state\", \"=\", \"en_route\"), (\"state\", \"=\", \"livree\")]", F, "Non : sans \"|\", c'est un ET, donc impossible."),
  ("[(\"state\", \"or\", \"en_route\", \"livree\")]", F, "Non : cet opérateur n'existe pas."),
]),
("Quel domaine trouve les courses dont la zone coûte au moins 1 500 F ?", [
  ("[(\"zone_id.tarif\", \">=\", 1500)]", V, "Oui : on traverse la relation avec un point."),
  ("[(\"tarif\", \">=\", 1500)]", F, "Non : la course n'a pas de champ tarif."),
  ("[(\"zone_id\", \">=\", 1500)]", F, "Non : zone_id contient un id, pas un tarif."),
]),
]),

# ---------------------------------------------------------------- 2.2.6
dict(code="2.2.6", id=2919, seq=26, minutes=10,
titre="Les recordsets : boucles, mapped, filtered, sorted",
description="Travailler sur plusieurs fiches à la fois avec les outils de l'ORM.",
html=fiche(
objectif="manipuler des ensembles de fiches avec <code>mapped</code>, <code>filtered</code>, <code>sorted</code> et <code>ensure_one</code>.",
intro="Dans Odoo, on ne manipule presque jamais une fiche seule : <code>self</code>, le résultat d'un <code>search</code>, une relation… sont des <b>recordsets</b>, des ensembles de 0, 1 ou plusieurs fiches. Ils ont leurs propres outils.",
corps=[
("code", """>>> courses = env["baobab.course"].search([])
>>> courses
baobab.course(2, 1)
>>> len(courses)
2
>>> courses.mapped("poids")                        # récupérer un champ de chaque fiche
[12.0, 3.5]
>>> courses.mapped("client_id.name")              # à travers une relation : sans doublon
['Awa Diop']
>>> courses.filtered(lambda c: c.poids > 5).mapped("name")   # garder certaines fiches
['BL/2026/0002']
>>> courses.sorted("poids").mapped("poids")       # trier
[3.5, 12.0]
>>> sum(courses.mapped("prix"))
5900.0""", "Terminal d'Odoo (base de démonstration)"),
("h", "Les outils à connaître"),
("tableau", ["Outil", "Effet"], [
  ["<code>for c in courses:</code>", "parcourir chaque fiche"],
  ["<code>mapped(\"champ\")</code>", "liste des valeurs ; recordset sans doublon si le champ est une relation"],
  ["<code>filtered(lambda c: …)</code>", "garder les fiches qui respectent la condition (en Python, sans requête SQL)"],
  ["<code>sorted(\"champ\")</code>", "trier ; <code>reverse=True</code> pour l'ordre inverse"],
  ["<code>a | b</code>, <code>a &amp; b</code>, <code>a - b</code>", "réunir, garder les communs, retirer"],
  ["<code>browse(id)</code>", "récupérer une fiche par son id"],
  ["<code>ensure_one()</code>", "lève une erreur si l'ensemble ne contient pas exactement une fiche"],
]),
("h", "Dans une méthode : toujours penser « plusieurs »"),
("code", """def action_demarrer(self):
    for course in self:          # self peut contenir 1 ou 50 courses (sélection dans la liste)
        ...
    self.write({"state": "en_route"})   # un seul write pour toutes : plus rapide""", "models/course.py"),
("attention", "L'erreur classique", "Écrire <code>self.poids</code> dans une méthode qui peut recevoir plusieurs courses donne l'erreur <code>Expected singleton</code>. Boucle avec <code>for course in self</code>, ou appelle <code>self.ensure_one()</code> si la méthode ne doit traiter qu'une fiche."),
("astuce", "filtered ou search ?", "Pour chercher dans toute la base, utilise <code>search</code> (une requête SQL, rapide). Pour trier un ensemble que tu as déjà en main, <code>filtered</code>."),
],
exercice=[
("p", "Dans le terminal d'Odoo : (1) calcule le chiffre d'affaires des courses livrées ; (2) la liste des zones (sans doublon) où Awa Diop a des courses (indice : <code>mapped(\"zone_id\")</code> renvoie un recordset sans doublon) ; (3) la course la plus lourde."),
],
retenir=[
  "Un recordset = 0, 1 ou plusieurs fiches ; <code>self</code> en est un.",
  "<code>mapped</code>, <code>filtered</code>, <code>sorted</code> : les trois outils du quotidien.",
  "« Expected singleton » : on a traité plusieurs fiches comme une seule.",
  "<code>search</code> pour la base, <code>filtered</code> pour un ensemble déjà chargé.",
]),
quiz=[
("Que renvoie courses.mapped(\"client_id.name\") ?", [
  ("La liste des noms des clients des courses, sans doublon", V, "Oui : à travers une relation, mapped passe par un recordset de clients, sans doublon."),
  ("Le nombre de clients", F, "Non : il faudrait len(...)."),
  ("Les courses triées par client", F, "Non : c'est sorted."),
]),
("L'erreur « Expected singleton » signifie…", [
  ("qu'on a lu un champ sur un ensemble de plusieurs fiches comme si c'était une seule", V, "Oui : il faut boucler ou appeler ensure_one()."),
  ("que la fiche n'existe pas", F, "Non."),
  ("que le champ n'existe pas", F, "Non : ce serait une AttributeError."),
]),
("Pour trouver toutes les courses de Rufisque dans la base, que préférer ?", [
  ("search avec un domaine", V, "Oui : une seule requête SQL."),
  ("search([]) puis filtered", F, "Ça marche, mais on charge toutes les courses de la base : lent."),
  ("browse avec tous les id", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.2.7
dict(code="2.2.7", id=2719, seq=27, minutes=10,
titre="Les champs calculés, liés et enregistrés ; les dépendances",
description="Calculer le prix d'une course automatiquement, à partir de la zone et du poids.",
html=fiche(
objectif="calculer automatiquement le prix d'une course avec un champ calculé, et comprendre <code>@api.depends</code> et <code>store</code>.",
intro="Le prix d'une course ne se tape pas : il se calcule à partir du tarif de la zone et du poids. C'est exactement le rôle d'un <b>champ calculé</b>. On y retrouve ta fonction <code>prix_course</code> du Bloc 1.",
corps=[
("code", """import math

from odoo import api, fields, models

POIDS_INCLUS = 5          # kg compris dans le tarif de la zone
SUPPLEMENT_PAR_KG = 200   # F CFA par kilo entamé au-delà


class BaobabCourse(models.Model):
    _name = "baobab.course"
    # ...
    currency_id = fields.Many2one(related="zone_id.currency_id")
    prix = fields.Monetary("Prix", compute="_compute_prix", store=True, currency_field="currency_id")

    @api.depends("zone_id.tarif", "poids")
    def _compute_prix(self):
        for course in self:
            prix = course.zone_id.tarif
            if course.poids > POIDS_INCLUS:
                prix += math.ceil(course.poids - POIDS_INCLUS) * SUPPLEMENT_PAR_KG
            course.prix = prix""", "models/course.py"),
("h", "Les trois ingrédients"),
("liste", [
  "<code>compute=\"_compute_prix\"</code> : le nom de la méthode qui calcule.",
  "<code>@api.depends(\"zone_id.tarif\", \"poids\")</code> : <b>quand</b> recalculer. Si le poids change, ou si le tarif de la zone change, Odoo recalcule.",
  "La méthode <b>boucle sur self</b> et donne une valeur à chaque fiche, même 0 : une fiche oubliée provoque une erreur.",
]),
("h", "store=True : calculé une fois, enregistré"),
("tableau", ["", "Sans store (par défaut)", "Avec store=True"], [
  ["Dans la base", "pas de colonne : recalculé à chaque affichage", "une colonne, mise à jour quand une dépendance change"],
  ["Recherche, tri, total", "impossible (ou à programmer)", "possible : <code>search([(\"prix\", \">\", 2000)])</code>, total dans la liste"],
  ["Coût", "calcul à chaque lecture", "calcul seulement quand une dépendance change"],
]),
("p", "Le prix doit pouvoir être trié et totalisé : on le stocke. Résultat sur la base de démonstration : 1 500 F pour 3,5 kg à Mermoz, 4 400 F pour 12 kg à Rufisque."),
("h", "Le champ lié (related)"),
("p", "<code>currency_id = fields.Many2one(related=\"zone_id.currency_id\")</code> : la course reprend la devise de sa zone, sans rien calculer. Un <code>related</code> est un raccourci vers un champ d'une fiche reliée."),
("attention", "Le @api.depends oublié", "Sans <code>\"zone_id.tarif\"</code> dans <code>@api.depends</code>, changer le tarif d'une zone ne mettrait <b>pas</b> à jour le prix des courses déjà enregistrées. Liste toujours tout ce que ton calcul lit."),
],
exercice=[
("p", "Ajoute le champ <code>prix</code> et sa méthode, puis mets à jour le module. Vérifie : une course de 7,2 kg à Mermoz coûte 2 100 F. Change le tarif de Mermoz à 1 600 F à l'écran, puis rouvre la course : le prix doit passer à 2 200 F."),
],
retenir=[
  "<code>compute=</code> + une méthode qui boucle sur <code>self</code> et remplit chaque fiche.",
  "<code>@api.depends</code> liste tout ce que le calcul lit, y compris à travers les relations.",
  "<code>store=True</code> pour pouvoir chercher, trier, totaliser.",
  "<code>related=</code> : un raccourci vers le champ d'une fiche reliée.",
]),
quiz=[
("À quoi sert @api.depends(\"zone_id.tarif\", \"poids\") ?", [
  ("À dire à Odoo de recalculer le prix quand le poids ou le tarif de la zone change", V, "Oui."),
  ("À rendre ces champs obligatoires", F, "Non."),
  ("À trier les courses", F, "Non."),
]),
("Pourquoi store=True sur le prix ?", [
  ("Pour pouvoir le chercher, le trier et le totaliser dans la liste", V, "Oui : il devient une colonne de la table."),
  ("Pour qu'il ne soit plus jamais recalculé", F, "Non : il est recalculé quand une dépendance change."),
  ("Pour le rendre modifiable à la main", F, "Non."),
]),
("Une course de 7,2 kg dans une zone à 1 500 F : quel prix avec la règle de la leçon ?", [
  ("2 100 F", V, "Oui : 3 kilos entamés au-delà de 5 kg, 200 F chacun (vérifié par un test automatique)."),
  ("1 940 F", F, "Non : on compte les kilos entamés, pas 2,2 kg."),
  ("1 500 F", F, "Non : le poids dépasse 5 kg."),
]),
]),

# ---------------------------------------------------------------- 2.2.8
dict(code="2.2.8", id=2720, seq=28, minutes=10,
titre="Les contraintes et les valeurs par défaut",
description="Interdire les données absurdes : contraintes SQL avec models.Constraint, contraintes Python avec @api.constrains.",
html=fiche(
objectif="empêcher les données absurdes avec deux types de contraintes, et proposer de bonnes valeurs par défaut.",
intro="Un poids négatif, deux zones « Mermoz », un client choisi comme livreur… Ces erreurs ne doivent jamais entrer dans la base. Odoo offre deux protections complémentaires.",
corps=[
("h", "1. La contrainte de base de données : models.Constraint"),
("code", """class BaobabZone(models.Model):
    _name = "baobab.zone"
    # ...
    _nom_unique = models.Constraint("UNIQUE(name)", "Cette zone existe déjà.")
    _tarif_positif = models.Constraint("CHECK(tarif >= 0)", "Le tarif ne peut pas être négatif.")


class BaobabCourse(models.Model):
    _name = "baobab.course"
    # ...
    _poids_positif = models.Constraint("CHECK(poids > 0)", "Le poids doit être supérieur à zéro.")""", "models/zone.py et models/course.py"),
("p", "C'est PostgreSQL lui-même qui vérifie : impossible de contourner la règle, même en important des données. On l'utilise pour les règles simples (unicité, signe d'un nombre)."),
("version", "<b>Odoo 18.1 et suivants</b> : on écrit <code>models.Constraint</code> comme attribut du modèle. <b>Avant</b> : une liste <code>_sql_constraints = [(\"nom\", \"CHECK(...)\", \"message\")]</code>. Attention, en <b>Odoo 20</b>, <code>_sql_constraints</code> est <b>ignoré</b> : Odoo écrit seulement dans le journal <code>Model attribute '_sql_constraints' is no longer supported, please define models.Constraint on the model.</code> Une ancienne contrainte recopiée d'un tutoriel Odoo 17 ne protège donc plus rien."),
("h", "2. La contrainte Python : @api.constrains"),
("code", """from odoo.exceptions import ValidationError

@api.constrains("livreur_id")
def _check_livreur(self):
    for course in self:
        if course.livreur_id and not course.livreur_id.est_livreur:
            raise ValidationError(self.env._("%s n'est pas un livreur.", course.livreur_id.name))""", "models/course.py"),
("p", "Pour les règles qui demandent de la logique (lire une autre fiche, comparer des dates). Odoo l'appelle à la création et à chaque modification des champs listés, et annule l'enregistrement si une erreur est levée."),
("h", "Les valeurs par défaut"),
("code", """poids = fields.Float("Poids (kg)", default=1.0)
date_course = fields.Date("Date", required=True, default=fields.Date.context_today)
currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)""", "Trois façons"),
("p", "Une valeur fixe, une fonction d'Odoo, ou une <code>lambda</code> appelée à chaque création (ici : la devise de la société de l'utilisateur)."),
("astuce", "self.env._(…)", "Les messages affichés à l'utilisateur passent par <code>self.env._(\"…\")</code> : ils pourront être traduits. C'est la forme utilisée dans le code d'Odoo 20."),
],
exercice=[
("p", "Ajoute les trois <code>models.Constraint</code> (la contrainte sur le livreur viendra à la leçon 2.4.1, quand les contacts sauront dire qui est livreur). Mets à jour, puis essaie à l'écran : une zone en double, un tarif négatif, un poids à 0. Note les messages. Puis essaie dans le terminal d'Odoo de créer une course avec <code>poids=-2</code> : quelle erreur obtiens-tu ?"),
],
retenir=[
  "<code>models.Constraint(\"CHECK(...)\" ou \"UNIQUE(...)\", \"message\")</code> : règle vérifiée par PostgreSQL.",
  "<code>@api.constrains</code> + <code>ValidationError</code> : règle en Python.",
  "Odoo 20 ignore <code>_sql_constraints</code> : seulement un avertissement dans le journal.",
  "<code>default=</code> : valeur fixe, fonction ou <code>lambda</code>.",
]),
quiz=[
("En Odoo 20, comment déclarer « le poids doit être positif » au niveau de la base ?", [
  ("_poids_positif = models.Constraint(\"CHECK(poids > 0)\", \"…\")", V, "Oui."),
  ("_sql_constraints = [(\"poids_positif\", \"CHECK(poids > 0)\", \"…\")]", F, "Non : en Odoo 20 c'est ignoré, avec un simple avertissement dans le journal."),
  ("poids = fields.Float(positive=True)", F, "Cette option n'existe pas."),
]),
("Quand préférer @api.constrains à models.Constraint ?", [
  ("Quand la règle demande de la logique, par exemple lire une autre fiche", V, "Oui : vérifier que le livreur est bien un livreur."),
  ("Pour vérifier qu'un nom est unique", F, "Non : UNIQUE dans models.Constraint suffit et c'est plus sûr."),
  ("Jamais, c'est déprécié", F, "Non : @api.constrains est bien vivant."),
]),
("default=lambda self: self.env.company.currency_id : quand la lambda est-elle appelée ?", [
  ("À chaque création de fiche", V, "Oui : la devise de la société de l'utilisateur à ce moment-là."),
  ("Une seule fois, à l'installation du module", F, "Non : c'est justement pour ça qu'on met une fonction."),
  ("À chaque affichage", F, "Non."),
]),
]),
]
