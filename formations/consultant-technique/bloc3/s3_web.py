"""Bloc 3 — Section « L'interface web » (section 2741, cours 210).
Vérifié sur Odoo 20.0 le 28/11/2026 (OWL 3.0.0-alpha.50) : exports d'OWL lus dans le navigateur, compteur monté et
cliqué dans Chromium (écriture OWL 3, puis écriture OWL 2 pour recopier l'erreur), widget « baobab_etapes » affiché
dans le formulaire avant et après « Démarrer », page /suivre-mon-colis et portail /my/courses testés dans le
navigateur et par deux tests HttpCase verts."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

COMPTEUR = """import { Component, proxy, xml } from "@odoo/owl";

export class Compteur extends Component {
    static template = xml`
        <div class="compteur">
            <span t-out="this.etat.valeur"/> colis
            <button t-on-click="() => this.ajouter()">+1</button>
        </div>`;

    setup() {
        this.etat = proxy({ valeur: 0 });   // l'état : quand il change, l'écran se redessine
    }

    ajouter() {
        this.etat.valeur++;
    }
}"""

WIDGET_JS = """import { Component, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const ETAPES = ["brouillon", "en_route", "livree"];

export class EtapesField extends Component {
    static template = "baobab_livraison.EtapesField";
    props = useProps(standardFieldProps);

    get statut() {
        return this.props.record.data[this.props.name];
    }
    get numero() {
        return ETAPES.indexOf(this.statut) + 1;
    }
    get pourcentage() {
        return Math.round((this.numero / ETAPES.length) * 100);
    }
}

registry.category("fields").add("baobab_etapes", {
    component: EtapesField,
    supportedTypes: ["selection"],
});"""

WIDGET_XML = """<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="baobab_livraison.EtapesField">
        <div class="o_baobab_etapes w-100">
            <t t-if="this.statut === 'annulee'">
                <span class="badge text-bg-secondary">Course annulée</span>
            </t>
            <t t-else="">
                <div>Étape <t t-out="this.numero"/> sur 3</div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar" role="progressbar"
                         t-att-style="'width: ' + this.pourcentage + '%; background-color: #68C184;'"/>
                </div>
            </t>
        </div>
    </t>
</templates>"""

CONTROLEUR = """from odoo import http
from odoo.http import request


class SuiviColis(http.Controller):

    @http.route("/suivre-mon-colis", type="http", auth="public", website=True, sitemap=True)
    def suivre_mon_colis(self, reference="", **kw):
        course = request.env["baobab.course"]
        if reference:
            # Visiteur anonyme : on cherche avec sudo(), mais on n'affiche que le statut, la zone et la date.
            course = course.sudo().search([("name", "=", reference.strip().upper())], limit=1)
        return request.render("baobab_livraison_site.suivi_colis", {
            "reference": reference,
            "course": course,
        })"""

PAGE = """<template id="suivi_colis" name="Suivre mon colis">
    <t t-call="website.layout">
        <div class="container py-5" style="max-width: 640px;">
            <h1 style="color: #0B415B;">Suivre mon colis</h1>
            <p>Tape la référence écrite sur ton bordereau (exemple : BL/2026/0001).</p>
            <form action="/suivre-mon-colis" method="get" class="d-flex gap-2 mb-4">
                <input type="text" name="reference" class="form-control" t-att-value="reference"
                       placeholder="BL/2026/0001" required="required"/>
                <button type="submit" class="btn btn-primary">Chercher</button>
            </form>
            <t t-if="reference and not course">
                <div class="alert alert-warning">Aucune course ne porte la référence <t t-out="reference"/>.</div>
            </t>
            <t t-if="course">
                <div class="card">
                    <div class="card-body">
                        <h2 class="h4" t-out="course.name"/>
                        <p class="mb-1"><strong>Statut :</strong> <span t-field="course.state"/></p>
                        <p class="mb-1"><strong>Zone :</strong> <t t-out="course.zone_id.name"/></p>
                        <p class="mb-0"><strong>Date :</strong> <span t-field="course.date_course"/></p>
                    </div>
                </div>
            </t>
        </div>
    </t>
</template>"""

PORTAIL_PY = """from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class BaobabPortal(CustomerPortal):

    def _prepare_portal_counter_values(self, counter):
        if counter == "course_count":
            partner = request.env.user.partner_id
            return "baobab.course", [("client_id", "child_of", partner.commercial_partner_id.id)], "read"
        return super()._prepare_portal_counter_values(counter)

    @http.route("/my/courses", type="http", auth="user", website=True)
    def portal_mes_courses(self, **kw):
        partner = request.env.user.partner_id
        courses = request.env["baobab.course"].search(
            [("client_id", "child_of", partner.commercial_partner_id.id)])
        values = self._prepare_portal_layout_values()
        values.update({"courses": courses, "page_name": "courses"})
        return request.render("baobab_livraison_site.portal_mes_courses", values)"""

LECONS = [
# ---------------------------------------------------------------- 3.3.1
dict(code="3.3.1", id=1360, seq=31, minutes=10,
titre="OWL : composant, modèle, état",
description="Comprendre l'interface web d'Odoo 20 : des composants OWL 3, leur modèle et leur état.",
html=fiche(
objectif="comprendre comment est construite l'interface d'Odoo : des composants OWL, chacun avec un modèle et un état.",
intro="Tout ce que tu vois dans Odoo (la liste, le formulaire, chaque champ, chaque bouton) est un <b>composant OWL</b> : une classe JavaScript, un modèle XML qui dit quoi afficher, et un état qui, quand il change, redessine l'écran.",
corps=[
("code", COMPTEUR, "Un compteur OWL 3 (testé dans Odoo 20 : 0 colis, deux clics, 2 colis)"),
("tableau", ["Élément", "Rôle"], [
  ["<code>class … extends Component</code>", "le composant"],
  ["<code>static template</code>", "son modèle : du XML avec les directives QWeb (<code>t-out</code>, <code>t-if</code>, <code>t-foreach</code>…) et <code>t-on-click</code> pour les événements"],
  ["<code>setup()</code>", "la préparation, à la place du constructeur"],
  ["<code>proxy({...})</code>", "un état « réactif » : modifier <code>this.etat.valeur</code> redessine le composant"],
  ["<code>this.</code> dans le modèle", "le modèle lit tout à partir du composant : <code>this.etat.valeur</code>, <code>this.ajouter()</code>"],
]),
("version", "<b>Odoo 20 utilise OWL 3</b> (version 3.0.0-alpha.50, vérifiée dans le navigateur). Ce qui change par rapport à OWL 2 (Odoo 17 à 19) : <code>useState</code> et <code>useRef</code> n'existent plus (on utilise <code>proxy</code> et des <code>signal</code>) ; les propriétés se déclarent avec <code>props = useProps(...)</code> au lieu de <code>static props</code> ; dans les modèles, on écrit <code>this.</code> devant tout. Un modèle à l'ancienne (<code>t-out=\"etat.valeur\"</code>) plante : <code>TypeError: Cannot read properties of undefined (reading 'valeur')</code> (vérifié). Méfie-toi des tutoriels OWL d'avant 2026."),
("h", "Comment Odoo charge ton JavaScript"),
("code", """"assets": {
    "web.assets_backend": [
        "baobab_livraison/static/src/etapes/*",
    ],
},""", "__manifest__.py : les fichiers .js et .xml du dossier sont ajoutés à l'interface"),
("liste", [
  "Les fichiers sont dans <code>static/src/</code>. Le <code>.js</code> s'importe avec <code>@odoo/owl</code>, <code>@web/…</code> (modules d'Odoo).",
  "Le composant se branche par un <b>registre</b> : <code>registry.category(\"fields\")</code> pour un widget de champ, <code>\"actions\"</code> pour un écran complet…",
  "Après un changement : <code>-u</code> du module, puis rafraîchir. En développement, ajoute <code>?debug=assets</code> à l'adresse pour avoir des fichiers lisibles dans les outils du navigateur.",
]),
],
exercice=[
("p", "Ouvre Odoo avec <code>?debug=assets</code>, puis les outils de développement du navigateur (F12), onglet Console. Tape <code>odoo.loader.modules.get(\"@odoo/owl\").useState</code> puis <code>….proxy</code> : le premier vaut <code>undefined</code>, le second est une fonction. Ensuite, explique en trois phrases ce que fait chaque ligne du compteur."),
],
retenir=[
  "L'interface d'Odoo = des composants OWL : classe + modèle + état.",
  "Odoo 20 = OWL 3 : <code>proxy</code> pour l'état, <code>useProps</code> pour les propriétés, <code>this.</code> dans les modèles.",
  "Les fichiers JS/XML sont déclarés dans <code>assets</code> du manifeste.",
  "Un composant se branche dans un registre.",
]),
quiz=[
("En Odoo 20, comment déclarer l'état d'un composant ?", [
  ("this.etat = proxy({ valeur: 0 })", V, "Oui (OWL 3)."),
  ("this.etat = useState({ valeur: 0 })", F, "C'était OWL 2 : useState n'existe plus en Odoo 20."),
  ("static etat = { valeur: 0 }", F, "Non : ce ne serait pas réactif."),
]),
("Dans un modèle OWL 3, comment afficher la valeur de l'état ?", [
  ("<span t-out=\"this.etat.valeur\"/>", V, "Oui."),
  ("<span t-out=\"etat.valeur\"/>", F, "Écriture OWL 2 : en Odoo 20, erreur « Cannot read properties of undefined »."),
  ("<span>{{ etat.valeur }}</span>", F, "Ce n'est pas la syntaxe de QWeb."),
]),
("Où déclare-t-on les fichiers JavaScript d'un module ?", [
  ("Dans la clé assets du manifeste (web.assets_backend)", V, "Oui."),
  ("Dans data", F, "Non : data charge du XML de données et de vues."),
  ("Dans un fichier JS à la racine, chargé automatiquement", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 3.3.2
dict(code="3.3.2", id=2742, seq=32, minutes=10,
titre="Un petit composant : le suivi d'une course",
description="Créer un widget de champ OWL 3 qui affiche l'avancement de la course et se met à jour tout seul.",
html=fiche(
objectif="créer ton propre widget : une barre « Étape 2 sur 3 » qui suit le statut de la course et se met à jour seule.",
intro="Le livreur aime voir où en est la course. On crée un <b>widget de champ</b> : un composant OWL qui remplace l'affichage normal du champ <code>state</code> dans le formulaire.",
corps=[
("code", WIDGET_JS, "static/src/etapes/etapes_field.js"),
("code", WIDGET_XML, "static/src/etapes/etapes_field.xml"),
("code", """<field name="state" widget="baobab_etapes" string="Avancement"/>""", "Dans le formulaire (onglet Livraison)"),
("liste", [
  "<code>props = useProps(standardFieldProps)</code> : le widget reçoit, comme tous les champs, la fiche (<code>record</code>) et le nom du champ (<code>name</code>).",
  "<code>this.props.record.data[this.props.name]</code> : la valeur actuelle du statut.",
  "Les <code>get</code> calculent ce qu'il faut afficher ; le modèle les lit avec <code>this.</code>.",
  "<code>registry.category(\"fields\").add(\"baobab_etapes\", …)</code> donne le nom utilisé dans <code>widget=\"…\"</code>.",
]),
("p", "Résultat vérifié : sur une course en brouillon, « Étape 1 sur 3 » ; on clique sur Démarrer, et la barre passe aussitôt à « Étape 2 sur 3 » (aux deux tiers, en vert #68C184), sans recharger la page. Le composant se redessine parce que la fiche, qu'il lit, a changé."),
("attention", "Une erreur dans le JS = écran vide", "Une faute de frappe dans un fichier JS peut bloquer toute l'interface. Garde la console du navigateur ouverte (F12) pendant que tu développes : l'erreur y est écrite avec le nom du fichier et la ligne."),
],
exercice=[
("p", "Crée les deux fichiers, déclare-les dans <code>assets</code>, ajoute le widget au formulaire. Mets à jour et vérifie : Étape 1, puis 2 après Démarrer, 3 après Livrée. Ajoute ensuite : en vert le texte « Livrée ! » quand la course est livrée, à la place de « Étape 3 sur 3 »."),
],
retenir=[
  "Widget de champ = composant OWL + <code>registry.category(\"fields\")</code>.",
  "La valeur du champ : <code>this.props.record.data[this.props.name]</code>.",
  "Dans la vue : <code>widget=\"nom_du_widget\"</code>.",
  "Console du navigateur ouverte pendant le développement.",
]),
quiz=[
("Comment un widget de champ lit-il la valeur du champ ?", [
  ("this.props.record.data[this.props.name]", V, "Oui."),
  ("this.env.course.state", F, "Non."),
  ("Avec un appel au serveur à chaque fois", F, "Inutile : la fiche est déjà chargée."),
]),
("Quel nom met-on dans widget=\"…\" dans la vue ?", [
  ("Celui donné dans registry.category(\"fields\").add(…)", V, "Oui : baobab_etapes."),
  ("Le nom de la classe JavaScript", F, "Non."),
  ("Le nom du fichier", F, "Non."),
]),
("Pourquoi la barre passe-t-elle à « Étape 2 » sans recharger la page après Démarrer ?", [
  ("Le composant lit la fiche ; la fiche change, OWL redessine le composant", V, "Oui."),
  ("Le navigateur recharge en cachette", F, "Non."),
  ("Grâce à une action planifiée", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 3.3.3
dict(code="3.3.3", id=2743, seq=33, minutes=10,
titre="Une page du site : « Suivre mon colis »",
description="Un contrôleur et un modèle QWeb public : le client tape sa référence et voit où en est sa course.",
html=fiche(
objectif="créer une page publique du site où le client tape sa référence et voit le statut de sa course, sans voir de données personnelles.",
intro="Un client appelle trois fois par jour : « Où est mon colis ? ». Donnons-lui une page sur le site. On la met dans un petit module à part, <code>baobab_livraison_site</code>, qui dépend de <code>website</code> et de <code>baobab_livraison</code> (comme le module pont des ventes au Bloc 2).",
corps=[
("h", "1. Le contrôleur : une adresse web"),
("code", CONTROLEUR, "baobab_livraison_site/controllers/main.py"),
("tableau", ["Paramètre de la route", "Rôle"], [
  ["<code>\"/suivre-mon-colis\"</code>", "l'adresse"],
  ["<code>type=\"http\"</code>", "renvoie une page (<code>\"jsonrpc\"</code> pour des données)"],
  ["<code>auth=\"public\"</code>", "ouverte aux visiteurs non connectés (<code>\"user\"</code> : connectés seulement)"],
  ["<code>website=True</code>", "page du site : menu, langue, thème"],
]),
("p", "Le paramètre <code>reference</code> vient du formulaire (<code>?reference=BL/2026/0001</code>). <code>request.render</code> remplit le modèle QWeb avec les valeurs données."),
("h", "2. Le modèle de la page"),
("code", PAGE, "baobab_livraison_site/views/suivi_templates.xml"),
("p", "<code>website.layout</code> ajoute l'en-tête et le pied de page du site. Le menu « Suivre mon colis » se crée avec une fiche <code>website.menu</code> (url <code>/suivre-mon-colis</code>, parent <code>website.main_menu</code>)."),
("attention", "sudo() et données personnelles", "Un visiteur n'a aucun droit sur les courses : on cherche avec <code>sudo()</code>. C'est justifié ici, mais alors <b>c'est toi</b> qui protèges : la page n'affiche que la référence, le statut, la zone et la date, <b>jamais</b> le nom, le téléphone ou l'adresse du client. Un test automatique le vérifie (le nom du client n'apparaît pas dans la page)."),
("attention", "Une référence se devine", "Les références se suivent : quelqu'un qui connaît BL/2026/0001 peut essayer BL/2026/0002, 0003… et voir le statut des courses des autres. C'est pourquoi la page ne montre rien de personnel. La vraie protection : un <b>code de suivi secret</b> imprimé sur le bordereau et demandé en plus de la référence. C'est une des demandes du travail à rendre."),
("p", "Vérifié : <code>bl/2026/0001</code> tapé en minuscules trouve bien BL/2026/0001 (grâce à <code>.upper()</code>) ; une référence inconnue affiche « Aucune course ne porte la référence BL/2026/9999 »."),
],
exercice=[
("p", "Crée le module <code>baobab_livraison_site</code> (manifeste, <code>controllers/</code>, modèle, menu). Installe-le, ouvre <code>/suivre-mon-colis</code> sans être connecté et cherche une course. Puis écris un test <code>HttpCase</code> qui vérifie que le nom du client n'apparaît pas dans la page."),
],
retenir=[
  "Une page = un contrôleur (<code>@http.route</code>) + un modèle QWeb (<code>website.layout</code>).",
  "<code>auth=\"public\"</code> : visiteurs ; <code>auth=\"user\"</code> : connectés.",
  "<code>sudo()</code> sur une page publique : n'afficher que le strict nécessaire.",
  "Un module à part qui dépend de <code>website</code>.",
]),
quiz=[
("Quelle route ouvre une page aux visiteurs non connectés ?", [
  ("@http.route(\"/suivre-mon-colis\", type=\"http\", auth=\"public\", website=True)", V, "Oui."),
  ("@http.route(..., auth=\"user\")", F, "Non : il faut être connecté."),
  ("@http.route(..., type=\"jsonrpc\")", F, "Non : ça renvoie des données, pas une page."),
]),
("La page publique cherche la course avec sudo(). Que faut-il surveiller ?", [
  ("N'afficher aucune donnée personnelle du client", V, "Oui : sudo ouvre tout, c'est la page qui protège."),
  ("Rien, sudo() suffit", F, "Non : sudo() enlève justement les protections."),
  ("Mettre auth=\"user\"", F, "La page serait alors fermée aux clients non connectés."),
]),
("Quel modèle QWeb ajoute l'en-tête et le pied de page du site ?", [
  ("website.layout", V, "Oui."),
  ("web.external_layout", F, "Non : c'est l'en-tête des rapports PDF."),
  ("portal.portal_layout", F, "Non : c'est la mise en page de « Mon compte »."),
]),
]),

# ---------------------------------------------------------------- 3.3.4
dict(code="3.3.4", id=2941, seq=34, minutes=10,
titre="Le portail client",
description="Le client connecté voit toutes ses courses dans « Mon compte », et seulement les siennes.",
html=fiche(
objectif="permettre au client connecté de voir toutes ses courses dans « Mon compte », et seulement les siennes.",
intro="La page publique montre une course à la fois. Les boutiques clientes de Baobab veulent plus : la liste de toutes leurs courses. Odoo a pour cela le <b>portail</b> : un espace « Mon compte » pour les clients, avec des droits très limités.",
corps=[
("h", "1. Le droit de lecture, limité à ses courses"),
("code", """id,name,model_id,group_id/id,operation,domain
access_baobab_course_portal,Courses : le client voit les siennes,baobab.course,base.group_portal,r,"[('client_id', 'child_of', [user.commercial_partner_id.id])]"
access_baobab_zone_portal,Zones : lecture portail,baobab.zone,base.group_portal,r,""", "baobab_livraison_site/security/ir.access.csv"),
("p", "C'est la colonne <code>domain</code> d'Odoo 20 : le groupe Portail peut <b>lire</b> (<code>r</code>) les courses, mais seulement celles de sa société (<code>child_of</code> : la société et ses contacts). Le module Ventes d'Odoo 20 fait exactement pareil pour les commandes."),
("version", "<b>Odoo 18 et 19</b> : la même chose demandait deux fichiers : une ligne dans <code>ir.model.access.csv</code> (droit de lecture) et une règle <code>ir.rule</code> en XML (le domaine). <b>Odoo 20</b> : une seule ligne dans <code>ir.access.csv</code>."),
("h", "2. La page /my/courses"),
("code", PORTAIL_PY, "baobab_livraison_site/controllers/main.py (suite)"),
("p", "La recherche se fait <b>sans</b> <code>sudo()</code> : ce sont les droits du client qui filtrent. Le modèle de la page appelle <code>portal.portal_layout</code> et <code>portal.portal_table</code> pour avoir le style de « Mon compte »."),
("h", "3. La carte dans « Mon compte »"),
("code", """<odoo noupdate="1">
    <record id="portal_entry_mes_courses" model="portal.entry">
        <field name="name">Mes courses</field>
        <field name="description">Suivre mes livraisons Baobab</field>
        <field name="url">/my/courses</field>
        <field name="placeholder_count">course_count</field>
        <field name="category">client_category</field>
        <field name="sequence" eval="60"/>
    </record>
</odoo>""", "baobab_livraison_site/data/portal_entry_data.xml"),
("p", "La carte ne s'affiche que si le client a au moins une course : Odoo appelle <code>_prepare_portal_counter_values(\"course_count\")</code> pour compter."),
("version", "<b>Nouveau en Odoo 20</b> : les cartes de « Mon compte » sont des fiches <code>portal.entry</code> (c'est ainsi que le module Ventes déclare « Your Orders »). Avant, on héritait du modèle <code>portal.portal_my_home</code> avec un <code>xpath</code> et on surchargeait <code>_prepare_home_portal_values</code>."),
("p", "Vérifié : Awa Diop, utilisatrice du portail, voit la carte « Mes courses » et ses deux courses ; un test automatique vérifie qu'un client ne voit pas la course d'un autre client. Et si elle tente d'ouvrir l'interface interne, Odoo la renvoie vers <code>/my</code>."),
],
exercice=[
("p", "Ajoute le droit portail, la page <code>/my/courses</code> et la carte. Crée un utilisateur Portail pour Awa Diop (Contacts › Awa Diop › menu Actions (⋮) › Donner accès au portail, ou dans le terminal d'Odoo), connecte-toi avec son compte dans une fenêtre privée : la carte « Mes courses » apparaît. Écris le test qui prouve qu'elle ne voit pas les courses des autres."),
],
retenir=[
  "Portail = utilisateurs du groupe <code>base.group_portal</code>, droits très limités.",
  "Odoo 20 : droit + domaine dans une ligne d'<code>ir.access.csv</code>.",
  "Page portail sans <code>sudo()</code> : les droits filtrent.",
  "Odoo 20 : une carte de « Mon compte » = une fiche <code>portal.entry</code>.",
]),
quiz=[
("Comment limiter un client du portail à ses propres courses en Odoo 20 ?", [
  ("Une ligne ir.access.csv pour base.group_portal avec un domain sur client_id", V, "Oui."),
  ("Filtrer dans le modèle QWeb de la page", F, "Non : la page n'est pas une protection, les droits si."),
  ("Une règle ir.rule seule, sans droit d'accès", F, "C'était la moitié de la méthode d'Odoo 18-19."),
]),
("Pourquoi la page /my/courses cherche-t-elle sans sudo() ?", [
  ("Pour que les droits du client filtrent les courses", V, "Oui : avec sudo(), il verrait tout."),
  ("Parce que sudo() est interdit dans un contrôleur", F, "Non : on l'utilise pour la page publique."),
  ("Pour aller plus vite", F, "Non."),
]),
("En Odoo 20, comment ajoute-t-on une carte dans « Mon compte » ?", [
  ("Une fiche portal.entry (url, compteur, catégorie)", V, "Oui."),
  ("Un menuitem", F, "Non : les menus sont pour l'interface interne."),
  ("Une page du site", F, "Non."),
]),
]),
]
