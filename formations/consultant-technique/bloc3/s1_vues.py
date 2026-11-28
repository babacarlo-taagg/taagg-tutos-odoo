"""Bloc 3 — Section « Les vues » (section 2736, cours 210).
Vues vérifiées sur Odoo 20.0 le 28/11/2026 : module de référence installé sur une base neuve (démonstration), chaque
vue ouverte dans Chromium (liste, kanban, formulaire, calendrier, pivot, graphique, recherche, fiche contact), filtres
cliqués et comptés, anciennes syntaxes essayées (<tree>, attrs, states) pour recopier les vrais messages d'erreur."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

FORMULAIRE = """<record id="view_baobab_course_form" model="ir.ui.view">
    <field name="name">baobab.course.form</field>
    <field name="model">baobab.course</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <button name="action_demarrer" type="object" string="Démarrer" class="btn-primary"
                        invisible="state != 'brouillon'"/>
                <button name="action_livrer" type="object" string="Livrée" class="btn-primary"
                        invisible="state != 'en_route'"/>
                <button name="action_annuler" type="object" string="Annuler"
                        invisible="state in ('livree', 'annulee')"/>
                <field name="state" widget="statusbar" statusbar_visible="brouillon,en_route,livree"/>
            </header>
            <sheet>
                <div class="oe_title">
                    <h1><field name="name" readonly="1"/></h1>
                </div>
                <group>
                    <group string="Client">
                        <field name="client_id"/>
                        <field name="zone_id"/>
                        <field name="date_course"/>
                    </group>
                    <group string="Colis">
                        <field name="poids"/>
                        <field name="currency_id" invisible="1"/>
                        <field name="prix"/>
                        <field name="etiquette_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
                    </group>
                </group>
                <notebook>
                    <page string="Livraison" name="livraison">
                        <group>
                            <field name="livreur_id"/>
                            <field name="date_livraison"/>
                        </group>
                    </page>
                    <page string="Consigne" name="consigne">
                        <field name="consigne" placeholder="Consigne pour le livreur…"/>
                    </page>
                </notebook>
            </sheet>
            <chatter/>
        </form>
    </field>
</record>"""

LISTE = """<record id="view_baobab_course_list" model="ir.ui.view">
    <field name="name">baobab.course.list</field>
    <field name="model">baobab.course</field>
    <field name="arch" type="xml">
        <list decoration-muted="state == 'annulee'" decoration-success="state == 'livree'"
              decoration-warning="state == 'en_route'">
            <field name="name"/>
            <field name="date_course"/>
            <field name="client_id"/>
            <field name="zone_id"/>
            <field name="livreur_id" optional="show"/>
            <field name="poids" optional="hide"/>
            <field name="currency_id" column_invisible="True"/>
            <field name="prix" sum="Total"/>
            <field name="state" widget="badge"
                   decoration-success="state == 'livree'" decoration-warning="state == 'en_route'"/>
        </list>
    </field>
</record>"""

RECHERCHE = """<record id="view_baobab_course_search" model="ir.ui.view">
    <field name="name">baobab.course.search</field>
    <field name="model">baobab.course</field>
    <field name="arch" type="xml">
        <search>
            <field name="name"/>
            <field name="client_id"/>
            <field name="livreur_id"/>
            <field name="zone_id"/>
            <filter name="aujourdhui" string="Courses du jour"
                    domain="[('date_course', '=', context_today().strftime('%Y-%m-%d'))]"/>
            <filter name="mes_courses" string="Mes courses"
                    domain="[('livreur_id.user_ids', 'in', [uid])]"/>
            <separator/>
            <filter name="a_livrer" string="À livrer" domain="[('state', 'in', ('brouillon', 'en_route'))]"/>
            <filter name="livrees" string="Livrées" domain="[('state', '=', 'livree')]"/>
            <group>
                <filter name="par_zone" string="Zone" context="{'group_by': 'zone_id'}"/>
                <filter name="par_statut" string="Statut" context="{'group_by': 'state'}"/>
                <filter name="par_jour" string="Jour" context="{'group_by': 'date_course:day'}"/>
            </group>
        </search>
    </field>
</record>"""

MENUS = """<record id="action_baobab_course" model="ir.actions.act_window">
    <field name="name">Courses</field>
    <field name="res_model">baobab.course</field>
    <field name="view_mode">list,kanban,form,calendar,pivot,graph</field>
    <field name="context">{'search_default_a_livrer': 1}</field>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">Enregistre ta première course</p>
        <p>Une course = un colis à livrer dans une zone de Dakar.</p>
    </field>
</record>
<record id="action_baobab_livreurs" model="ir.actions.act_window">
    <field name="name">Livreurs</field>
    <field name="res_model">res.partner</field>
    <field name="view_mode">list,form</field>
    <field name="domain">[('est_livreur', '=', True)]</field>
    <field name="context">{'default_est_livreur': True}</field>
</record>

<menuitem id="menu_baobab_root" name="Baobab Livraison" sequence="10"
          web_icon="baobab_livraison,static/description/icon.png"/>
<menuitem id="menu_baobab_course" name="Courses" parent="menu_baobab_root"
          action="action_baobab_course" sequence="10"/>
<menuitem id="menu_baobab_config" name="Configuration" parent="menu_baobab_root" sequence="90"/>
<menuitem id="menu_baobab_zone" name="Zones" parent="menu_baobab_config"
          action="action_baobab_zone" sequence="10"/>
<menuitem id="menu_baobab_livreurs" name="Livreurs" parent="menu_baobab_config"
          action="action_baobab_livreurs" sequence="20"/>"""

KANBAN = """<record id="view_baobab_course_kanban" model="ir.ui.view">
    <field name="name">baobab.course.kanban</field>
    <field name="model">baobab.course</field>
    <field name="arch" type="xml">
        <kanban default_group_by="state" class="o_kanban_small_column">
            <field name="currency_id"/>
            <templates>
                <t t-name="card">
                    <div class="d-flex justify-content-between">
                        <field name="name" class="fw-bold"/>
                        <field name="prix" widget="monetary"/>
                    </div>
                    <field name="client_id"/>
                    <div class="text-muted">
                        <field name="zone_id"/> · <field name="poids"/> kg
                    </div>
                    <field name="etiquette_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
                </t>
            </templates>
        </kanban>
    </field>
</record>"""

ANALYSE = """<record id="view_baobab_course_calendar" model="ir.ui.view">
    <field name="name">baobab.course.calendar</field>
    <field name="model">baobab.course</field>
    <field name="arch" type="xml">
        <calendar date_start="date_course" mode="month" color="zone_id" quick_create="0">
            <field name="client_id"/>
            <field name="prix"/>
        </calendar>
    </field>
</record>

<record id="view_baobab_course_pivot" model="ir.ui.view">
    <field name="name">baobab.course.pivot</field>
    <field name="model">baobab.course</field>
    <field name="arch" type="xml">
        <pivot>
            <field name="zone_id" type="row"/>
            <field name="state" type="col"/>
            <field name="prix" type="measure"/>
        </pivot>
    </field>
</record>

<record id="view_baobab_course_graph" model="ir.ui.view">
    <field name="name">baobab.course.graph</field>
    <field name="model">baobab.course</field>
    <field name="arch" type="xml">
        <graph type="bar">
            <field name="zone_id"/>
            <field name="prix" type="measure"/>
        </graph>
    </field>
</record>"""

XPATH = """<record id="view_partner_form_baobab" model="ir.ui.view">
    <field name="name">res.partner.form.baobab</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='category_id']" position="after">
            <field name="est_livreur"/>
        </xpath>
    </field>
</record>"""

LECONS = [
# ---------------------------------------------------------------- 3.1.1
dict(code="3.1.1", id=1358, seq=11, minutes=10,
titre="La vue formulaire",
description="Organiser la fiche d'une course : en-tête, titre, groupes, onglets et fil de discussion.",
html=fiche(
objectif="écrire toi-même le formulaire d'une course, bien rangé : en-tête avec boutons, titre, deux colonnes, onglets.",
intro="Au Bloc 2, tu as recopié un formulaire tout prêt. Maintenant, tu apprends à l'écrire. Une vue, c'est un fichier XML qui dit à Odoo <b>quels champs afficher et où</b>. Le code Python ne change pas.",
corps=[
("code", FORMULAIRE, "views/baobab_course_views.xml"),
("h", "Les briques du formulaire"),
("tableau", ["Balise", "Rôle"], [
  ["<code>&lt;record model=\"ir.ui.view\"&gt;</code>", "une vue est une fiche du modèle <code>ir.ui.view</code> ; <code>model</code> dit pour quel modèle"],
  ["<code>&lt;header&gt;</code>", "la barre du haut : boutons et barre d'étapes (<code>widget=\"statusbar\"</code>)"],
  ["<code>&lt;sheet&gt;</code>", "la « feuille » blanche au centre"],
  ["<code>&lt;div class=\"oe_title\"&gt;&lt;h1&gt;</code>", "le grand titre (la référence BL/2026/0001)"],
  ["<code>&lt;group&gt;</code> dans un <code>&lt;group&gt;</code>", "deux colonnes ; <code>string</code> donne un intertitre"],
  ["<code>&lt;notebook&gt;</code> + <code>&lt;page&gt;</code>", "des onglets"],
  ["<code>&lt;chatter/&gt;</code>", "le fil de discussion, après <code>&lt;/sheet&gt;</code>"],
]),
("p", "Un champ présent dans un <code>&lt;group&gt;</code> reçoit automatiquement son libellé (le <code>string</code> du champ Python). Hors d'un groupe (comme <code>consigne</code> dans l'onglet), il s'affiche sans libellé, sur toute la largeur."),
("astuce", "Le champ devise caché", "Pour afficher un montant (<code>prix</code>, de type Monetary), la vue doit aussi connaître sa devise : on ajoute <code>&lt;field name=\"currency_id\" invisible=\"1\"/&gt;</code>."),
("version", "Ce formulaire est écrit pour Odoo 17 et suivants : <code>invisible=\"state != 'brouillon'\"</code> directement sur le bouton, et <code>&lt;chatter/&gt;</code> (Odoo 18+). Les vieux tutoriels utilisent <code>attrs</code> et <code>states</code> : Odoo 20 les refuse (leçon 3.1.5)."),
],
exercice=[
("p", "Remplace le formulaire fourni au Bloc 2 par le tien : titre, groupes « Client » et « Colis », onglets « Livraison » et « Consigne ». Mets à jour le module (<code>-u</code>) et rafraîchis la page. Bonus : ajoute un troisième onglet « Historique » qui affiche <code>create_date</code> et <code>create_uid</code>."),
],
retenir=[
  "Une vue = une fiche <code>ir.ui.view</code> écrite en XML, chargée par le manifeste.",
  "<code>header</code> (boutons, étapes), <code>sheet</code> (contenu), <code>chatter</code> (fil).",
  "<code>group</code> dans <code>group</code> = deux colonnes ; <code>notebook</code>/<code>page</code> = onglets.",
  "Après un changement de vue : <code>-u</code> du module, puis rafraîchir le navigateur.",
]),
quiz=[
("Où place-t-on les boutons Démarrer, Livrée, Annuler ?", [
  ("Dans <header>", V, "Oui, avec la barre d'étapes."),
  ("Dans <notebook>", F, "Non : notebook contient les onglets."),
  ("Dans <chatter/>", F, "Non : c'est le fil de discussion."),
]),
("Comment obtenir deux colonnes de champs ?", [
  ("Deux <group> dans un <group>", V, "Oui."),
  ("Un attribut columns=\"2\" sur <sheet>", F, "Cet attribut n'existe pas."),
  ("Deux <page>", F, "Non : ça fait deux onglets."),
]),
("Tu modifies une vue XML. Que faut-il faire pour la voir ?", [
  ("Mettre à jour le module (-u) puis rafraîchir la page", V, "Oui : les vues sont chargées en base à la mise à jour."),
  ("Seulement rafraîchir la page", F, "Non : la vue en base n'a pas changé."),
  ("Vider le cache du navigateur", F, "Non : le problème est côté serveur."),
]),
]),

# ---------------------------------------------------------------- 3.1.2
dict(code="3.1.2", id=2934, seq=12, minutes=10,
titre="La vue liste",
description="Lister les courses avec un total, des couleurs par statut et des colonnes facultatives.",
html=fiche(
objectif="afficher les courses en liste, avec le total des prix, des couleurs selon le statut et des colonnes que l'utilisateur peut cacher.",
intro="La liste est souvent le premier écran que voit l'utilisateur. Une bonne liste se lit d'un coup d'œil : les courses en route en orange, les livrées en vert, le chiffre du jour en bas.",
corps=[
("code", LISTE, "views/baobab_course_views.xml"),
("tableau", ["Attribut", "Effet"], [
  ["<code>decoration-success=\"state == 'livree'\"</code>", "ligne en vert quand la condition est vraie (aussi <code>-warning</code> orange, <code>-danger</code> rouge, <code>-muted</code> gris, <code>-info</code>, <code>-bf</code> gras)"],
  ["<code>sum=\"Total\"</code>", "total de la colonne en bas de la liste (5 900 CFA sur la base de démonstration)"],
  ["<code>optional=\"show\"</code> / <code>\"hide\"</code>", "colonne que l'utilisateur peut afficher ou cacher (icône à droite des en-têtes)"],
  ["<code>column_invisible=\"True\"</code>", "colonne toujours cachée (la devise, utile au montant)"],
  ["<code>widget=\"badge\"</code>", "le statut dans une pastille colorée"],
]),
("p", "Les conditions s'écrivent comme en Python, avec les noms des champs : <code>state == 'livree'</code>, <code>poids &gt; 30</code>."),
("version", "<b>Odoo 17 et avant</b> : la liste s'écrivait <code>&lt;tree&gt;</code>. <b>Odoo 18 et suivants</b> : <code>&lt;list&gt;</code>. En Odoo 20, une vue <code>&lt;tree&gt;</code> est refusée : <code>Invalid view type: 'tree'. You might have used an invalid starting tag in the architecture. Allowed types are: list, form, graph, pivot, calendar, kanban, search, card, qweb, activity</code> (vérifié). Le <code>view_mode</code> des actions s'écrit aussi <code>list</code>, plus <code>tree</code>."),
],
exercice=[
("p", "Écris ta vue liste. Vérifie : le total en bas, la course en route en orange, la colonne Poids cachée par défaut que tu peux faire apparaître. Puis ajoute une décoration <code>decoration-danger</code> pour les colis de plus de 30 kg."),
],
retenir=[
  "Odoo 18+ : <code>&lt;list&gt;</code> ; <code>&lt;tree&gt;</code> est refusé en Odoo 20.",
  "<code>decoration-…</code> colore les lignes selon une condition.",
  "<code>sum</code> pour un total, <code>optional</code> pour une colonne facultative.",
  "<code>column_invisible</code> cache une colonne pour tout le monde.",
]),
quiz=[
("En Odoo 20, comment commence une vue liste ?", [
  ("<list>", V, "Oui."),
  ("<tree>", F, "C'était Odoo 17 et avant : Odoo 20 refuse la vue."),
  ("<table>", F, "Non : c'est du HTML, pas une vue Odoo."),
]),
("Comment afficher le total des prix en bas de la liste ?", [
  ("sum=\"Total\" sur le champ prix", V, "Oui."),
  ("total=\"True\" sur <list>", F, "Cet attribut n'existe pas."),
  ("Un champ calculé total", F, "Inutile : sum le fait."),
]),
("Que fait optional=\"hide\" sur une colonne ?", [
  ("La colonne est cachée par défaut, l'utilisateur peut l'afficher", V, "Oui."),
  ("La colonne n'existe plus", F, "Non."),
  ("La colonne est cachée pour tout le monde, toujours", F, "Non : ça, c'est column_invisible."),
]),
]),

# ---------------------------------------------------------------- 3.1.3
dict(code="3.1.3", id=2936, seq=13, minutes=10,
titre="La vue recherche : filtres et regroupements",
description="Créer les filtres « Courses du jour », « Mes courses », « À livrer » et les regroupements par zone.",
html=fiche(
objectif="offrir des filtres tout prêts (courses du jour, à livrer…) et des regroupements par zone, statut ou jour.",
intro="Le gérant de Baobab ne veut pas taper des domaines : il veut cliquer sur « Courses du jour » ou « À livrer ». C'est le rôle de la vue recherche.",
corps=[
("code", RECHERCHE, "views/baobab_course_views.xml"),
("tableau", ["Balise", "Effet"], [
  ["<code>&lt;field name=\"client_id\"/&gt;</code>", "on peut taper un nom de client dans la barre de recherche"],
  ["<code>&lt;filter domain=\"…\"/&gt;</code>", "un filtre tout prêt dans le menu Filtres"],
  ["<code>&lt;separator/&gt;</code>", "sépare des groupes de filtres : deux filtres du même groupe = OU, de deux groupes = ET"],
  ["<code>context=\"{'group_by': 'zone_id'}\"</code>", "un regroupement (menu Regrouper par) ; <code>date_course:day</code> regroupe par jour"],
]),
("h", "Deux variables utiles dans les domaines"),
("liste", [
  "<code>context_today()</code> : la date du jour de l'utilisateur.",
  "<code>uid</code> : l'utilisateur connecté. <code>[('livreur_id.user_ids', 'in', [uid])]</code> = les courses dont le livreur est l'utilisateur connecté (au Bloc 4, un livreur aura un compte).",
]),
("h", "Un filtre activé à l'ouverture"),
("p", "Dans l'action (leçon suivante), <code>'search_default_a_livrer': 1</code> active le filtre <code>a_livrer</code> dès l'ouverture : on a vérifié, la liste s'ouvre avec la facette « À livrer »."),
("astuce", "Tester un filtre", "Ouvre le menu Filtres, coche ton filtre et compte les lignes. Puis regarde le domaine réel : mode développeur, menu Filtres › <b>Filtre personnalisé…</b> le montre."),
],
exercice=[
("p", "Écris la vue recherche. Vérifie que « À livrer » est actif à l'ouverture, que « Courses du jour » ne montre que les courses d'aujourd'hui, et que le regroupement par Zone affiche un total par zone. Ajoute un filtre « Colis lourds » (plus de 30 kg)."),
],
retenir=[
  "<code>&lt;field&gt;</code> : recherche en tapant ; <code>&lt;filter&gt;</code> : filtre tout prêt.",
  "Même groupe = OU ; groupes séparés par <code>&lt;separator/&gt;</code> = ET.",
  "Regroupement : <code>context=\"{'group_by': 'champ'}\"</code>.",
  "<code>search_default_&lt;nom&gt;</code> dans l'action : filtre actif à l'ouverture.",
]),
quiz=[
("Comment créer un regroupement « par zone » ?", [
  ("<filter context=\"{'group_by': 'zone_id'}\"/>", V, "Oui."),
  ("<filter domain=\"[('zone_id', '!=', False)]\"/>", F, "Non : ça filtre, ça ne regroupe pas."),
  ("<group_by field=\"zone_id\"/>", F, "Cette balise n'existe pas."),
]),
("Deux filtres « À livrer » et « Livrées » sans séparateur entre eux, cochés tous les deux : résultat ?", [
  ("Les courses à livrer OU livrées", V, "Oui : dans un même groupe, c'est un OU."),
  ("Aucune course", F, "Ce serait le cas avec un ET."),
  ("Une erreur", F, "Non."),
]),
("Comment ouvrir la liste avec le filtre « À livrer » déjà actif ?", [
  ("'search_default_a_livrer': 1 dans le contexte de l'action", V, "Oui."),
  ("default=\"1\" sur le filtre", F, "Non."),
  ("Ce n'est pas possible", F, "Si."),
]),
]),

# ---------------------------------------------------------------- 3.1.4
dict(code="3.1.4", id=2738, seq=14, minutes=10,
titre="Actions et menus",
description="Créer le menu Baobab Livraison : une action par écran, des menus et un sous-menu Configuration.",
html=fiche(
objectif="relier tes vues aux menus : une action par écran, un menu principal avec son icône et un sous-menu Configuration.",
intro="Une vue ne s'affiche pas toute seule. Il faut une <b>action</b> (« ouvre les courses en liste, kanban… ») et un <b>menu</b> qui lance l'action.",
corps=[
("code", MENUS, "views/baobab_menus.xml"),
("h", "L'action de fenêtre"),
("tableau", ["Champ", "Rôle"], [
  ["<code>res_model</code>", "le modèle à afficher"],
  ["<code>view_mode</code>", "les vues proposées, dans l'ordre : la première s'ouvre d'abord"],
  ["<code>domain</code>", "un filtre permanent (les livreurs = les contacts avec <code>est_livreur</code>)"],
  ["<code>context</code>", "des réglages : filtre actif (<code>search_default_…</code>), valeur par défaut (<code>default_est_livreur</code>)"],
  ["<code>help</code>", "le message affiché quand la liste est vide"],
]),
("h", "Les menus"),
("liste", [
  "Un menu sans <code>parent</code> = une application sur la page d'accueil, avec son icône (<code>web_icon</code>, une image 256 × 256 dans <code>static/description/</code>).",
  "Un menu sans <code>action</code> = un sous-menu qui regroupe d'autres menus (Configuration).",
  "<code>sequence</code> règle l'ordre.",
]),
("attention", "L'ordre dans le manifeste", "Un menu appelle une action, qui doit déjà exister : le fichier des menus vient <b>après</b> celui des vues dans <code>data</code>. Sinon l'installation s'arrête sur un identifiant externe inconnu."),
("astuce", "Le contexte default_", "Grâce à <code>'default_est_livreur': True</code>, un contact créé depuis le menu Livreurs est automatiquement coché « Livreur Baobab ». C'est la même clé <code>default_</code> que dans la leçon sur le contexte (Bloc 2)."),
],
exercice=[
("p", "Réécris <code>baobab_menus.xml</code> : action des courses avec six vues et le filtre « À livrer », menu Configuration avec Zones et Livreurs, icône de l'application. Crée un livreur depuis le menu Livreurs et vérifie que la case est cochée."),
],
retenir=[
  "Action (<code>ir.actions.act_window</code>) : quel modèle, quelles vues, quel filtre.",
  "Menu (<code>menuitem</code>) : lance une action ; sans parent = application.",
  "<code>domain</code> filtre toujours ; <code>context</code> règle les valeurs par défaut et les filtres actifs.",
  "Les menus après les vues dans <code>data</code>.",
]),
quiz=[
("À quoi sert view_mode=\"list,kanban,form\" dans une action ?", [
  ("À choisir les vues proposées et celle qui s'ouvre en premier", V, "Oui : la première de la liste."),
  ("À créer les vues automatiquement", F, "Non : il faut les écrire (sinon Odoo fabrique des vues très simples)."),
  ("À trier les courses", F, "Non."),
]),
("Le menu « Livreurs » ne doit montrer que les livreurs. Où mettre cette règle ?", [
  ("Dans le domain de l'action", V, "Oui : [('est_livreur', '=', True)]."),
  ("Dans le menuitem", F, "Non : le menu ne fait que lancer l'action."),
  ("Dans la vue liste", F, "Non : une vue ne filtre pas les fiches."),
]),
("L'installation s'arrête : le menu appelle une action inconnue. Cause probable ?", [
  ("Le fichier des menus est avant celui des actions dans data", V, "Oui : l'ordre compte."),
  ("Il manque l'icône", F, "Non."),
  ("Le menu n'a pas de sequence", F, "Non : sequence est facultatif."),
]),
]),

# ---------------------------------------------------------------- 3.1.5
dict(code="3.1.5", id=2938, seq=15, minutes=10,
titre="Champs dynamiques : invisible, readonly, required, widgets",
description="Afficher, bloquer ou exiger un champ selon le statut, sans l'ancien attrs ; choisir le bon widget.",
html=fiche(
objectif="rendre un champ visible, modifiable ou obligatoire selon la situation, et choisir comment il s'affiche (widget).",
intro="Une course livrée ne doit plus changer de livreur. Une course en route doit avoir un livreur. La date de livraison n'a de sens qu'une fois livrée. Tout cela se règle dans la vue, avec une simple condition.",
corps=[
("code", """<field name="livreur_id" required="state == 'en_route'"
       readonly="state in ('livree', 'annulee')"/>
<field name="date_livraison" invisible="not date_livraison"/>""", "Onglet Livraison du formulaire"),
("tableau", ["Attribut", "Effet quand la condition est vraie"], [
  ["<code>invisible=\"…\"</code>", "le champ (ou le bouton, le groupe, la page) disparaît"],
  ["<code>readonly=\"…\"</code>", "le champ est affiché mais non modifiable"],
  ["<code>required=\"…\"</code>", "le champ devient obligatoire pour enregistrer"],
]),
("p", "La condition utilise les champs de la fiche, <b>présents dans la vue</b> (ici <code>state</code>, affiché dans l'en-tête). Elle est réévaluée à chaque modification, en direct."),
("version", "<b>Odoo 16 et avant</b> : <code>attrs=\"{'invisible': [('state', '=', 'livree')]}\"</code> et <code>states=\"…\"</code> sur les boutons. <b>Depuis Odoo 17</b>, Odoo 20 compris, c'est refusé à l'installation : <code>Since 17.0, the \"attrs\" and \"states\" attributes are no longer used.</code> (message réel). Pour un ancien module : transformer chaque <code>attrs</code> en attributs directs."),
("attention", "La vue ne protège pas", "<code>readonly</code> dans la vue empêche de modifier <b>à l'écran</b>, pas par l'API ni par le code. Une règle obligatoire se met en Python (contrainte, vérification dans l'action), comme au Bloc 2."),
("h", "Les widgets : changer l'affichage"),
("tableau", ["Widget", "Pour"], [
  ["<code>statusbar</code>", "la barre d'étapes d'un champ Selection"],
  ["<code>badge</code>", "une pastille de couleur (statut dans une liste)"],
  ["<code>many2many_tags</code>", "des étiquettes ; <code>options=\"{'color_field': 'color'}\"</code> pour les couleurs"],
  ["<code>monetary</code>", "un montant avec sa devise"],
  ["<code>boolean_toggle</code>", "un interrupteur au lieu d'une case"],
  ["<code>image</code>", "une photo"],
]),
],
exercice=[
("p", "Ajoute les trois règles sur <code>livreur_id</code> et <code>date_livraison</code>. Vérifie : sur une course livrée, le livreur est grisé ; sur une course en route, effacer le livreur empêche d'enregistrer (champ en rouge) ; la date de livraison n'apparaît qu'une fois livrée. Essaie ensuite <code>attrs</code> pour voir l'erreur d'Odoo 20."),
],
retenir=[
  "<code>invisible</code>, <code>readonly</code>, <code>required</code> + une condition Python.",
  "Les champs de la condition doivent être dans la vue.",
  "<code>attrs</code> et <code>states</code> sont refusés depuis Odoo 17.",
  "La vue ne protège pas : les vraies règles restent en Python.",
]),
quiz=[
("Comment rendre le livreur obligatoire seulement quand la course est en route ?", [
  ("required=\"state == 'en_route'\" sur le champ", V, "Oui."),
  ("attrs=\"{'required': [('state', '=', 'en_route')]}\"", F, "Refusé depuis Odoo 17."),
  ("required=True dans le champ Python", F, "Non : il serait obligatoire tout le temps."),
]),
("Un module Odoo 16 contient attrs=\"{'invisible': ...}\". Que fait Odoo 20 à l'installation ?", [
  ("Il refuse la vue avec un message sur attrs", V, "Oui : « Since 17.0, the attrs and states attributes are no longer used »."),
  ("Il l'accepte et l'ignore", F, "Non."),
  ("Il la convertit tout seul", F, "Non : c'est à toi de la réécrire."),
]),
("readonly=\"state == 'livree'\" empêche-t-il de changer le livreur par l'API ?", [
  ("Non : la vue ne protège que l'écran", V, "Oui : pour une vraie règle, il faut du Python."),
  ("Oui, partout", F, "Non."),
  ("Oui, sauf pour l'administrateur", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 3.1.6
dict(code="3.1.6", id=2737, seq=16, minutes=10,
titre="La vue kanban",
description="Le tableau des courses par statut : des cartes qu'on déplace d'une colonne à l'autre.",
html=fiche(
objectif="afficher les courses en cartes, rangées en colonnes par statut, comme un tableau de suivi.",
intro="Le matin, le gérant veut voir d'un coup d'œil : combien de courses en brouillon, combien en route ? La vue kanban range les courses en colonnes, une carte par course.",
corps=[
("code", KANBAN, "views/baobab_course_views.xml"),
("liste", [
  "<code>default_group_by=\"state\"</code> : une colonne par statut (Brouillon, En route…).",
  "<code>&lt;t t-name=\"card\"&gt;</code> : le contenu d'une carte. On y met des <code>&lt;field&gt;</code> et un peu de HTML (classes Bootstrap : <code>d-flex</code>, <code>fw-bold</code>, <code>text-muted</code>).",
  "Les champs nécessaires mais non affichés (la devise du prix) sont déclarés avant <code>&lt;templates&gt;</code>.",
  "Déplacer une carte d'une colonne à l'autre <b>change le statut</b> : pratique, mais attention, cela contourne les boutons et leurs vérifications.",
]),
("version", "<b>Odoo 18 et suivants</b> : la carte s'appelle <code>t-name=\"card\"</code>. <b>Odoo 17 et avant</b> : <code>t-name=\"kanban-box\"</code> avec beaucoup plus de HTML (<code>oe_kanban_global_click</code>…). En Odoo 20, plus aucun module d'Odoo n'utilise <code>kanban-box</code> (vérifié dans le code) : écris <code>card</code>."),
("attention", "Glisser une carte contourne tes contrôles", "Essai réel : on glisse la course de Rufisque, <b>sans livreur</b>, de Brouillon vers En route. Odoo accepte et note « Brouillon → En route » dans le fil, alors que le bouton Démarrer l'aurait refusée. Le glisser écrit directement le champ <code>state</code>, sans appeler <code>action_demarrer</code>. Pour l'empêcher : <code>records_draggable=\"0\"</code> sur <code>&lt;kanban&gt;</code>, ou un contrôle en Python sur l'écriture du statut."),
("p", "À savoir : pour un champ Selection, Odoo n'affiche que les colonnes qui contiennent au moins une course (plus celles vidées pendant la session). Sur une base neuve, seule la colonne Brouillon apparaît."),
],
exercice=[
("p", "Ajoute la vue kanban et <code>kanban</code> dans le <code>view_mode</code> de l'action. Ouvre-la : deux colonnes sur la base de démonstration. Démarre une course avec son bouton (pour faire apparaître la colonne En route), puis glisse une course sans livreur dans cette colonne et regarde le fil de discussion. Puis ajoute <code>records_draggable=\"0\"</code> et vérifie qu'on ne peut plus glisser."),
],
retenir=[
  "Kanban = cartes en colonnes ; <code>default_group_by</code> choisit les colonnes.",
  "Odoo 18+ : <code>&lt;t t-name=\"card\"&gt;</code>.",
  "Glisser une carte modifie le champ de regroupement, sans passer par les boutons.",
  "<code>records_draggable=\"0\"</code> pour l'interdire.",
]),
quiz=[
("Comment avoir une colonne par statut ?", [
  ("default_group_by=\"state\" sur <kanban>", V, "Oui."),
  ("Une <page> par statut", F, "Non : page sert aux onglets du formulaire."),
  ("Un filtre par statut", F, "Non."),
]),
("En Odoo 20, comment s'appelle le modèle de la carte ?", [
  ("<t t-name=\"card\">", V, "Oui, depuis Odoo 18."),
  ("<t t-name=\"kanban-box\">", F, "C'était Odoo 17 et avant."),
  ("<card>", F, "Non."),
]),
("Glisser une course de « Brouillon » à « En route » appelle-t-il action_demarrer ?", [
  ("Non : seul le champ state est modifié", V, "Oui (vérifié : une course sans livreur passe en route). D'où records_draggable=\"0\" ou un contrôle en Python."),
  ("Oui, toujours", F, "Non."),
  ("Oui, si le bouton est visible", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 3.1.7
dict(code="3.1.7", id=2939, seq=17, minutes=10,
titre="Calendrier, pivot et graphique",
description="Voir les courses par jour, et le chiffre d'affaires par zone et par statut.",
html=fiche(
objectif="donner au gérant trois vues d'analyse : le calendrier des courses, un tableau croisé et un graphique par zone.",
intro="« Combien a rapporté Rufisque ce mois-ci ? » Pas besoin d'Excel : Odoo a ses propres vues d'analyse. Trois balises suffisent.",
corps=[
("code", ANALYSE, "views/baobab_course_views.xml"),
("tableau", ["Vue", "Attributs clés"], [
  ["<code>calendar</code>", "<code>date_start</code> : le champ date ; <code>color</code> : une couleur par zone ; <code>mode</code> : month, week ou day ; <code>quick_create=\"0\"</code> : clic sur un jour = vrai formulaire"],
  ["<code>pivot</code>", "<code>type=\"row\"</code> en lignes, <code>type=\"col\"</code> en colonnes, <code>type=\"measure\"</code> la valeur additionnée"],
  ["<code>graph</code>", "<code>type</code> = bar, line ou pie ; un champ de regroupement et une mesure"],
]),
("p", "N'oublie pas d'ajouter <code>calendar,pivot,graph</code> au <code>view_mode</code> de l'action. Sur la base de démonstration, le pivot montre Mermoz 1 500 CFA et Rufisque 4 400 CFA."),
("astuce", "Des mesures stockées", "Le pivot et le graphique additionnent des champs <b>stockés</b>. C'est pour cela que le prix a <code>store=True</code> (Bloc 2) : un champ calculé non stocké ne peut pas servir de mesure."),
("version", "Ces trois vues s'écrivent de la même façon en Odoo 18, 19 et 20. Pour des tableaux de bord plus riches, Odoo Enterprise propose Tableurs et Tableaux de bord ; en Community, le pivot s'exporte en Excel avec le bouton de téléchargement."),
],
exercice=[
("p", "Ajoute les trois vues. Dans le pivot, ajoute le regroupement par jour en lignes sous la zone. Dans le graphique, passe en camembert. Crée deux courses de plus pour voir les chiffres bouger."),
],
retenir=[
  "Calendrier : <code>date_start</code> obligatoire.",
  "Pivot : <code>row</code>, <code>col</code>, <code>measure</code>.",
  "Graphique : <code>type=\"bar|line|pie\"</code>.",
  "Les mesures doivent être des champs stockés.",
]),
quiz=[
("Quel attribut est indispensable dans une vue calendrier ?", [
  ("date_start", V, "Oui : le champ date qui place la fiche dans le calendrier."),
  ("color", F, "Facultatif."),
  ("mode", F, "Facultatif : month par défaut… à régler selon ton besoin."),
]),
("Dans un pivot, comment additionner les prix ?", [
  ("<field name=\"prix\" type=\"measure\"/>", V, "Oui."),
  ("<field name=\"prix\" sum=\"Total\"/>", F, "Non : sum sert dans la vue liste."),
  ("<field name=\"prix\" type=\"row\"/>", F, "Non : ça ferait une ligne par prix."),
]),
("Pourquoi un champ calculé non stocké ne peut-il pas être une mesure du pivot ?", [
  ("Parce que le pivot additionne dans la base, où ce champ n'existe pas", V, "Oui."),
  ("Parce qu'il est en lecture seule", F, "Non."),
  ("Il le peut", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 3.1.8
dict(code="3.1.8", id=2940, seq=18, minutes=10,
titre="Hériter d'une vue avec xpath",
description="Ajouter la case « Livreur Baobab » dans la fiche contact d'Odoo, sans toucher à sa vue.",
html=fiche(
objectif="ajouter ton champ dans un écran d'Odoo (la fiche contact) sans modifier la vue d'origine, grâce à l'héritage de vue.",
intro="Au Bloc 2, tu as ajouté le champ <code>est_livreur</code> aux contacts. Il manque la case dans la fiche contact. Comme pour le Python, on ne touche jamais à la vue d'Odoo : on <b>hérite</b> de la vue.",
corps=[
("code", XPATH, "views/res_partner_views.xml"),
("liste", [
  "<code>inherit_id</code> : la vue qu'on complète (<code>base.view_partner_form</code>, la fiche contact).",
  "<code>xpath expr=\"//field[@name='category_id']\"</code> : l'endroit visé, ici le champ Étiquettes.",
  "<code>position</code> : <code>after</code> (après), <code>before</code> (avant), <code>inside</code> (dedans), <code>replace</code> (remplacer), <code>attributes</code> (changer un attribut).",
]),
("code", """<field name="category_id" position="after">
    <field name="est_livreur"/>
</field>""", "Écriture courte, même effet"),
("h", "Trouver le bon endroit"),
("liste", [
  "Active le mode développeur, ouvre une fiche contact, puis l'icône du mode développeur (le petit insecte) › <b>Afficher : Form</b> : tu vois le nom de la vue (<code>base.view_partner_form</code>) et son XML.",
  "Vise un élément stable : un <code>field</code> par son <code>name</code>, une <code>page</code> ou un <code>group</code> par son <code>name</code>.",
  "Un <code>xpath</code> qui ne trouve rien bloque l'installation : le message donne l'expression fautive.",
]),
("code", """<xpath expr="//field[@name='phone']" position="attributes">
    <attribute name="required">est_livreur</attribute>
</xpath>""", "Changer un attribut : le téléphone obligatoire pour un livreur"),
("attention", "replace avec prudence", "<code>position=\"replace\"</code> supprime l'élément d'Odoo : un autre module qui s'y accroche plantera. Préfère <code>attributes</code> (par exemple <code>invisible</code>)."),
],
exercice=[
("p", "Ajoute la case Livreur Baobab après les étiquettes de la fiche contact, puis rends le téléphone obligatoire pour un livreur. Vérifie dans Configuration › Livreurs : la case est cochée sur Ibou Fall."),
],
retenir=[
  "Héritage de vue : <code>inherit_id</code> + <code>xpath</code> (ou l'écriture courte).",
  "Positions : after, before, inside, replace, attributes.",
  "Trouver la vue : mode développeur › Vue : Formulaire.",
  "On évite <code>replace</code> ; on préfère <code>attributes</code>.",
]),
quiz=[
("Comment ajouter un champ dans la fiche contact sans modifier la vue d'Odoo ?", [
  ("Une vue avec inherit_id=\"base.view_partner_form\" et un xpath", V, "Oui."),
  ("Copier toute la vue contact dans ton module", F, "Non : elle ne suivrait plus les mises à jour d'Odoo."),
  ("Modifier le fichier XML d'Odoo", F, "Jamais."),
]),
("Quelle position change seulement un attribut d'un élément existant ?", [
  ("attributes", V, "Oui."),
  ("replace", F, "Non : replace remplace tout l'élément."),
  ("inside", F, "Non : inside ajoute à l'intérieur."),
]),
("Ton xpath ne trouve pas l'élément visé. Que se passe-t-il ?", [
  ("L'installation ou la mise à jour s'arrête avec un message", V, "Oui."),
  ("Le champ est ajouté à la fin", F, "Non."),
  ("Rien, la vue est ignorée sans rien dire", F, "Non."),
]),
]),
]
