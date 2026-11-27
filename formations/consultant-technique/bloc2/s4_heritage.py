"""Bloc 2 — Section « L'héritage » (section 2725, cours 209).
Code vérifié sur Odoo 20.0 le 27/11/2026 : module baobab_livraison et module pont baobab_livraison_vente
(2 tests verts), exemples lus dans le code source d'Odoo 20."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

PARTENAIRE = """from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"          # pas de _name : on complète le modèle existant

    est_livreur = fields.Boolean("Livreur Baobab")
    course_livreur_ids = fields.One2many("baobab.course", "livreur_id", string="Courses livrées")
    nombre_courses = fields.Integer("Nombre de courses", compute="_compute_nombre_courses")

    @api.depends("course_livreur_ids")
    def _compute_nombre_courses(self):
        for partenaire in self:
            partenaire.nombre_courses = len(partenaire.course_livreur_ids)"""

VENTE = """from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    zone_livraison_id = fields.Many2one("baobab.zone", string="Zone de livraison")
    course_ids = fields.One2many("baobab.course", "commande_id", string="Courses")

    def action_confirm(self):
        resultat = super().action_confirm()          # 1. Odoo confirme la commande, comme d'habitude
        for commande in self.filtered("zone_livraison_id"):
            self.env["baobab.course"].create({       # 2. on ajoute notre comportement
                "client_id": commande.partner_shipping_id.id,
                "zone_id": commande.zone_livraison_id.id,
                "commande_id": commande.id,
                "consigne": self.env._("Livrer la commande %s", commande.name),
            })
        return resultat                              # 3. on renvoie le résultat d'origine"""

LECONS = [
# ---------------------------------------------------------------- 2.4.1
dict(code="2.4.1", id=1357, seq=41, minutes=10,
titre="_inherit : ajouter un champ à un modèle existant",
description="Marquer un contact comme livreur sans toucher au code d'Odoo : l'héritage classique.",
html=fiche(
objectif="ajouter des champs à un modèle d'Odoo (les contacts) sans modifier son code, avec <code>_inherit</code>.",
intro="Les livreurs de Baobab sont des contacts Odoo : ils ont un nom, un téléphone, une adresse. Il manque juste une case « Livreur Baobab ». On ne touche <b>jamais</b> au code d'Odoo : on le complète depuis notre module. C'est l'<b>héritage</b>, la compétence n° 1 du développeur Odoo.",
corps=[
("code", PARTENAIRE, "models/res_partner.py"),
("p", "Maintenant que les contacts savent dire qui est livreur, on complète la course : le champ livreur ne propose que les livreurs, et la contrainte de la leçon 2.2.8 refuse un contact qui n'en est pas un."),
("code", """livreur_id = fields.Many2one(
    "res.partner", string="Livreur", tracking=True,
    domain=[("est_livreur", "=", True)],     # ne propose que les livreurs
)

@api.constrains("livreur_id")
def _check_livreur(self):
    for course in self:
        if course.livreur_id and not course.livreur_id.est_livreur:
            raise ValidationError(self.env._("%s n'est pas un livreur.", course.livreur_id.name))""", "models/course.py (compléments)"),
("liste", [
  "<code>_inherit = \"res.partner\"</code> <b>sans</b> <code>_name</code> : on complète le modèle des contacts. Pas de nouvelle table : les colonnes sont ajoutées à <code>res_partner</code>.",
  "Tous les modules voient les nouveaux champs : un contact a maintenant <code>est_livreur</code>, partout dans Odoo.",
  "Le Many2one <code>livreur_id</code> de la course utilise <code>domain=[(\"est_livreur\", \"=\", True)]</code> : seuls les livreurs sont proposés.",
]),
("h", "Pourquoi ne jamais modifier le code d'Odoo ?"),
("p", "Parce qu'à la prochaine mise à jour d'Odoo, tes changements seraient écrasés. Avec l'héritage, ton module reste à part : Odoo se met à jour, ton module continue de s'appliquer par-dessus."),
("h", "Afficher le champ"),
("p", "Pour voir la case dans la fiche contact, il faut aussi hériter de la vue (une ligne <code>xpath</code>) : c'est le sujet du Bloc 3. En attendant, vérifie dans le terminal d'Odoo :"),
("code", """>>> ibou = env["res.partner"].search([("name", "=", "Ibou Fall")])
>>> ibou.est_livreur, ibou.nombre_courses
(True, 1)""", "Terminal d'Odoo (données de démonstration)"),
("attention", "_name + _inherit, c'est autre chose", "Si tu écris à la fois <code>_name = \"baobab.course\"</code> et <code>_inherit = [\"mail.thread\"]</code>, tu crées un <b>nouveau</b> modèle qui reprend les champs et méthodes de <code>mail.thread</code>. Sans <code>_name</code> (ou avec le même nom), tu <b>complètes</b> le modèle existant. C'est le même mot-clé pour deux usages."),
("version", "Ce mécanisme est identique d'Odoo 8 à Odoo 20. C'est aussi lui qu'Odoo utilise en interne : le module Ventes ajoute des champs aux contacts exactement de cette façon."),
],
exercice=[
("p", "Crée <code>models/res_partner.py</code> (et l'import), mets à jour. Dans le terminal d'Odoo, coche <code>est_livreur</code> sur un contact, puis crée une course en le choisissant comme livreur. Ajoute le <code>domain</code> et la contrainte <code>_check_livreur</code> à la course. Essaie ensuite avec un contact qui n'est pas livreur : quelle erreur ?"),
],
retenir=[
  "<code>_inherit</code> sans <code>_name</code> : on complète un modèle existant.",
  "Les nouveaux champs vont dans la table existante (<code>res_partner</code>).",
  "On ne modifie jamais le code d'Odoo : on l'étend depuis son module.",
  "<code>_name</code> + <code>_inherit</code> d'un autre modèle : nouveau modèle qui reprend ses fonctions.",
]),
quiz=[
("Pour ajouter le champ est_livreur aux contacts, que faut-il écrire ?", [
  ("_inherit = \"res.partner\" et le champ, dans ton module", V, "Oui."),
  ("Modifier le fichier res_partner.py d'Odoo", F, "Jamais : tout serait perdu à la mise à jour."),
  ("Créer un modèle baobab.livreur avec _name", F, "Possible, mais on perdrait tout ce qu'un contact sait faire."),
]),
("Où est enregistrée la valeur de est_livreur ?", [
  ("Dans une nouvelle colonne de la table res_partner", V, "Oui."),
  ("Dans une nouvelle table baobab_livreur", F, "Non."),
  ("Nulle part, elle est calculée", F, "Non : c'est un champ Boolean normal."),
]),
("Pourquoi le champ livreur de la course ne propose-t-il que les livreurs ?", [
  ("Grâce au domain [(\"est_livreur\", \"=\", True)] sur le Many2one", V, "Oui."),
  ("Grâce à la contrainte _check_livreur", F, "Non : la contrainte refuse après coup ; le domain filtre la liste proposée."),
  ("Par hasard", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.4.2
dict(code="2.4.2", id=None, seq=42, minutes=10,
titre="Surcharger une méthode avec super()",
description="Ajouter une règle à create ou à la suppression sans casser le comportement d'Odoo.",
html=fiche(
objectif="modifier le comportement d'une méthode d'Odoo (créer, supprimer, confirmer) en ajoutant ton code avant ou après l'original.",
intro="Tu veux un numéro automatique à la création, ou interdire de supprimer une course livrée. Ces actions existent déjà dans Odoo. On ne les réécrit pas : on les <b>surcharge</b>, c'est-à-dire qu'on ajoute notre code et qu'on appelle l'original avec <code>super()</code>.",
corps=[
("h", "Le modèle à suivre : create"),
("code", """@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:                       # AVANT : on prépare les valeurs
        if vals.get("name", "Nouveau") == "Nouveau":
            vals["name"] = self.env["ir.sequence"].next_by_code("baobab.course") or "Nouveau"
    return super().create(vals_list)             # puis Odoo crée, comme d'habitude""", "models/course.py"),
("liste", [
  "Même nom, mêmes paramètres que la méthode d'origine.",
  "<code>super().create(vals_list)</code> appelle la version d'Odoo (et celles des autres modules installés).",
  "On <b>renvoie</b> ce que renvoie <code>super()</code> : ici, les courses créées.",
  "<code>@api.model_create_multi</code> : <code>create</code> reçoit une <b>liste</b> de dictionnaires (on peut créer plusieurs fiches d'un coup).",
]),
("h", "Les deux erreurs qui cassent tout"),
("tableau", ["Oubli", "Conséquence"], [
  ["Ne pas appeler <code>super()</code>", "le comportement d'Odoo (et des autres modules) est perdu : ici, aucune course ne serait créée"],
  ["Ne pas faire <code>return</code>", "la méthode renvoie <code>None</code> : le code d'Odoo qui l'appelait attend des fiches et plante"],
]),
("h", "Interdire une suppression : @api.ondelete"),
("code", """@api.ondelete(at_uninstall=False)
def _unlink_sauf_livree(self):
    if any(course.state == "livree" for course in self):
        raise UserError(self.env._("Une course livrée ne peut pas être supprimée."))""", "models/course.py"),
("p", "Pour bloquer une suppression, Odoo recommande <code>@api.ondelete</code> plutôt que de surcharger <code>unlink</code>. <code>at_uninstall=False</code> : la règle ne s'applique pas quand on désinstalle le module (sinon la désinstallation serait bloquée). Le module Ventes fait pareil pour les commandes confirmées (<code>_unlink_except_draft_or_cancel</code>)."),
("code", """>>> course.state
'livree'
>>> course.unlink()
odoo.exceptions.UserError: Une course livrée ne peut pas être supprimée.""", "Résultat réel"),
("version", "<code>@api.model_create_multi</code> est la forme normale de <code>create</code> depuis Odoo 13 ; <code>@api.ondelete</code> existe depuis Odoo 14. Dans de vieux modules, tu verras <code>create(self, vals)</code> avec un seul dictionnaire, ou des <code>unlink</code> surchargés."),
],
exercice=[
("p", "Ajoute la règle <code>@api.ondelete</code>. Livre une course puis essaie de la supprimer (à l'écran : Action › Supprimer). Puis, pour voir l'erreur classique, enlève le <code>return</code> devant <code>super().create(...)</code>, redémarre et enregistre une nouvelle course à l'écran : Odoo affiche une erreur <code>AttributeError: 'NoneType' object has no attribute 'web_read'</code> (il attendait la course créée et a reçu <code>None</code>). Remets le <code>return</code>."),
],
retenir=[
  "Surcharger = même nom de méthode + ton code + <code>super()</code> + <code>return</code>.",
  "Code avant <code>super()</code> : préparer ; code après : réagir au résultat.",
  "<code>create</code> reçoit une liste de valeurs (<code>@api.model_create_multi</code>).",
  "Bloquer une suppression : <code>@api.ondelete(at_uninstall=False)</code>.",
]),
quiz=[
("Dans ta surcharge de create, tu oublies d'appeler super(). Que se passe-t-il ?", [
  ("Le comportement d'origine est perdu : la fiche n'est pas créée par Odoo", V, "Oui : c'est super() qui fait le vrai travail."),
  ("Rien, Odoo l'appelle tout seul", F, "Non."),
  ("Odoo refuse d'installer le module", F, "Non : l'erreur n'apparaît qu'à l'usage."),
]),
("Pourquoi écrire return super().create(vals_list) et pas seulement super().create(vals_list) ?", [
  ("Parce que le code qui appelle create attend les fiches créées", V, "Oui."),
  ("C'est une question de style", F, "Non : sans return, la méthode renvoie None."),
  ("Pour créer la fiche deux fois", F, "Non."),
]),
("Pour interdire de supprimer une course livrée, la méthode conseillée en Odoo 20 ?", [
  ("Une méthode décorée par @api.ondelete(at_uninstall=False)", V, "Oui."),
  ("Une contrainte models.Constraint", F, "Non : les contraintes vérifient les valeurs, pas les suppressions."),
  ("Cacher le bouton Supprimer", F, "Non : ce n'est pas une protection."),
]),
]),

# ---------------------------------------------------------------- 2.4.3
dict(code="2.4.3", id=2726, seq=43, minutes=10,
titre="Héritage par délégation et mixins",
description="Reconnaître _inherits (un utilisateur est un contact) et les mixins comme mail.thread.",
html=fiche(
objectif="reconnaître les deux autres formes d'héritage d'Odoo : la délégation (<code>_inherits</code>) et les mixins.",
intro="Tu connais <code>_inherit</code> pour compléter un modèle. Odoo a deux autres façons de réutiliser du code. Tu les écriras rarement, mais tu les croiseras partout dans le code d'Odoo : il faut savoir les lire.",
corps=[
("h", "1. La délégation : _inherits (avec un s)"),
("code", """class ResUsers(models.Model):
    _name = 'res.users'
    _inherits = {'res.partner': 'partner_id'}""", "odoo/addons/base/models/res_users.py (ligne 176, Odoo 20)"),
("p", "Un utilisateur <b>est</b> un contact, avec en plus un identifiant de connexion et des droits. Chaque utilisateur a sa propre fiche contact (<code>partner_id</code>), et lit ou écrit ses champs comme les siens :"),
("code", """>>> u = env["res.users"].create({"name": "Moussa Fall", "login": "moussa"})
>>> u.partner_id.name            # un contact a été créé automatiquement
'Moussa Fall'
>>> u.name = "Moussa Ndiaye"     # écrire sur l'utilisateur...
>>> u.partner_id.name            # ...écrit sur le contact
'Moussa Ndiaye'""", "Terminal d'Odoo"),
("p", "Même chose pour les articles : <code>product.product</code> (une variante, « T-shirt rouge taille M ») délègue à <code>product.template</code> (le modèle « T-shirt »)."),
("h", "2. Les mixins : des briques prêtes à l'emploi"),
("p", "Un mixin est un modèle « abstrait » (sans table) qui apporte des champs et des méthodes. On l'ajoute avec <code>_inherit</code> :"),
("tableau", ["Mixin", "Ce qu'il apporte"], [
  ["<code>mail.thread</code>", "le fil de messages et le suivi des changements"],
  ["<code>mail.activity.mixin</code>", "les activités"],
  ["<code>portal.mixin</code>", "un lien pour que le client voie la fiche sur le portail"],
  ["<code>image.mixin</code>", "une image en plusieurs tailles"],
]),
("h", "Résumé des trois héritages"),
("tableau", ["Écriture", "Effet", "Exemple"], [
  ["<code>_inherit = \"x\"</code> sans <code>_name</code>", "compléter le modèle x (même table)", "livreur sur les contacts"],
  ["<code>_name = \"y\"</code> + <code>_inherit = [\"x\"]</code>", "nouveau modèle y qui reprend x", "courses + <code>mail.thread</code>"],
  ["<code>_inherits = {\"x\": \"x_id\"}</code>", "y est relié à une fiche x et partage ses champs", "utilisateur → contact"],
]),
("astuce", "Pour Baobab ?", "Faut-il un modèle « livreur » qui délègue à <code>res.partner</code> ? Non : une simple case <code>est_livreur</code> suffit. Garde <code>_inherits</code> pour les cas où l'objet a vraiment beaucoup de données propres (comme un utilisateur)."),
],
exercice=[
("p", "Dans le code d'Odoo (<code>~/odoo</code>), cherche avec <code>grep -rn \"_inherits = \" addons/hr/models/</code> quel modèle des Ressources humaines utilise la délégation, et vers quel modèle. Puis, avec <code>grep -ln \"mail.thread\" addons/account/models/*.py</code>, trouve trois fichiers de la Comptabilité qui utilisent le mixin <code>mail.thread</code>."),
],
retenir=[
  "<code>_inherits</code> (avec s) : délégation, un modèle « contient » une fiche d'un autre modèle.",
  "Un utilisateur a sa fiche contact : écrire <code>u.name</code> écrit sur le contact.",
  "Un mixin (<code>mail.thread</code>…) : une brique ajoutée avec <code>_inherit</code>.",
  "Au quotidien : <code>_inherit</code>. <code>_inherits</code> : rarement.",
]),
quiz=[
("Dans Odoo, res.users utilise _inherits = {'res.partner': 'partner_id'}. Cela veut dire…", [
  ("Chaque utilisateur est relié à sa fiche contact et en partage les champs", V, "Oui."),
  ("Les utilisateurs et les contacts sont dans la même table", F, "Non : deux tables, reliées par partner_id."),
  ("Les contacts peuvent se connecter", F, "Non."),
]),
("Qu'est-ce qu'un mixin comme mail.thread ?", [
  ("Un modèle sans table qui apporte des champs et méthodes à ceux qui l'héritent", V, "Oui."),
  ("Un module à installer à part", F, "Non : il vient du module mail, on l'utilise avec _inherit."),
  ("Une vue", F, "Non."),
]),
("Quel héritage pour ajouter le champ est_livreur aux contacts ?", [
  ("_inherit = \"res.partner\"", V, "Oui : on complète le modèle."),
  ("_inherits = {\"res.partner\": \"partner_id\"}", F, "Non : ce serait créer un nouveau modèle relié."),
  ("Un mixin", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.4.4
dict(code="2.4.4", id=2727, seq=44, minutes=10,
titre="Étendre les ventes",
description="Un module pont : quand une commande de vente est confirmée, la course de livraison se crée toute seule.",
html=fiche(
objectif="relier Baobab Livraison au module Ventes : une commande confirmée crée automatiquement sa course.",
intro="Baobab vend aussi des colis pour des boutiques. Quand la boutique confirme une commande avec une zone de livraison, la course doit se créer seule. On va <b>étendre</b> la méthode de confirmation des ventes.",
corps=[
("h", "Un module pont"),
("code", """{
    "name": "Baobab Livraison — Ventes",
    "summary": "Une commande de vente confirmée crée sa course de livraison",
    "version": "20.0.1.0.0",
    "category": "Sales",
    "author": "TAAGG School (exercice)",
    "license": "LGPL-3",
    "depends": ["sale", "baobab_livraison"],
    "data": ["views/sale_order_views.xml"],
}""", "baobab_livraison_vente/__manifest__.py"),
("p", "Pourquoi un deuxième module ? Pour que les clients de Baobab sans le module Ventes puissent installer <code>baobab_livraison</code> seul. Le module pont dépend des deux et ne s'installe que s'ils sont là."),
("h", "Surcharger action_confirm"),
("code", VENTE, "baobab_livraison_vente/models/sale_order.py"),
("code", """class BaobabCourse(models.Model):
    _inherit = "baobab.course"

    commande_id = fields.Many2one("sale.order", string="Commande", readonly=True)""", "baobab_livraison_vente/models/course.py"),
("liste", [
  "On appelle d'abord <code>super().action_confirm()</code> : la commande est confirmée normalement (stock, factures…).",
  "Puis on crée une course pour chaque commande qui a une zone (<code>filtered(\"zone_livraison_id\")</code>).",
  "Le client de la course est l'adresse de livraison de la commande (<code>partner_shipping_id</code>).",
  "On renvoie <code>resultat</code> : Odoo peut en avoir besoin (ouvrir une fenêtre, par exemple).",
]),
("p", "Pour le champ « Zone de livraison » dans le devis, un petit fichier d'héritage de vue est fourni (expliqué au Bloc 3) :"),
("code", """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Fourni au Bloc 2 : l'héritage de vues (xpath) est expliqué au Bloc 3. -->
    <record id="view_order_form_baobab" model="ir.ui.view">
        <field name="name">sale.order.form.baobab</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="arch" type="xml">
            <field name="partner_id" position="after">
                <field name="zone_livraison_id"/>
            </field>
        </field>
    </record>
</odoo>""", "baobab_livraison_vente/views/sale_order_views.xml (fichier fourni)"),
("attention", "Lire le code avant de surcharger", "Avant de surcharger une méthode d'Odoo, lis-la dans le code source (<code>addons/sale/models/sale_order.py</code>) : que renvoie-t-elle ? Que fait-elle sur plusieurs commandes ? On ne surcharge bien que ce qu'on a compris."),
],
exercice=[
("p", "Crée le module <code>baobab_livraison_vente</code> (manifeste, <code>models/</code>, vue fournie), installe-le avec <code>-i baobab_livraison_vente</code> (le module Ventes s'installe avec). Crée un devis pour Awa Diop, zone Médina, confirme-le : une course apparaît dans Baobab Livraison avec la consigne « Livrer la commande S0000… ». Un devis sans zone ne doit rien créer."),
],
retenir=[
  "Un module pont relie deux modules sans les rendre dépendants l'un de l'autre.",
  "Surcharge d'une action : <code>resultat = super()...</code>, ton code, <code>return resultat</code>.",
  "On peut ajouter des champs dans les deux sens (<code>sale.order</code> et <code>baobab.course</code>).",
  "Lire la méthode d'origine avant de la surcharger.",
]),
quiz=[
("Pourquoi mettre l'extension des ventes dans un module à part ?", [
  ("Pour que baobab_livraison puisse s'installer sans le module Ventes", V, "Oui."),
  ("Parce qu'Odoo interdit deux _inherit dans un module", F, "Non."),
  ("Pour aller plus vite", F, "Non."),
]),
("Dans action_confirm, pourquoi appeler super() en premier ?", [
  ("Pour que la commande soit vraiment confirmée avant de créer la course", V, "Oui : on ajoute notre comportement après celui d'Odoo."),
  ("Parce que super() doit toujours être sur la première ligne", F, "Non : on peut aussi préparer des choses avant."),
  ("Pour annuler la confirmation", F, "Non."),
]),
("Une commande confirmée sans zone de livraison : que fait notre code ?", [
  ("Rien de plus : filtered(\"zone_livraison_id\") l'écarte", V, "Oui (vérifié par un test automatique)."),
  ("Il crée une course sans zone", F, "Non : la zone est obligatoire sur la course."),
  ("Il bloque la confirmation", F, "Non."),
]),
]),
]
