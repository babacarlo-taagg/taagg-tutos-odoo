"""Bloc 3 — Section « Les rapports » (section 2739, cours 210).
Vérifié sur Odoo 20.0 le 28/11/2026 : modèle QWeb rendu dans odoo-bin shell (sorties recopiées), bordereau imprimé en
PDF par le serveur avec wkhtmltopdf 0.12.6 d'Ubuntu (non patché), langue du client testée (fr_FR / en_US), pannes
reproduites (serveur web arrêté, plusieurs courses avec QT non patché, t-esc). Moteur Paper Muncher : lu dans le code,
non testé (binaire non disponible sur le poste d'essai)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

RAPPORT = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- 1. L'action : « Bordereau de livraison » dans le menu Actions des courses -->
    <record id="action_report_bordereau" model="ir.actions.report">
        <field name="name">Bordereau de livraison</field>
        <field name="model">baobab.course</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">baobab_livraison.report_bordereau</field>
        <field name="print_report_name">'Bordereau - %s' % object.name</field>
        <field name="binding_model_id" ref="model_baobab_course"/>
        <field name="binding_type">report</field>
    </record>

    <!-- 2. Le document d'une course -->
    <template id="report_bordereau_document">
        <t t-call="web.external_layout">
            <div class="page">
                <h2>Bordereau de livraison <span t-field="course.name"/></h2>
                <div class="row mt-4">
                    <div class="col-6">
                        <strong>Client</strong>
                        <div t-field="course.client_id"
                             t-options="{'widget': 'contact', 'fields': ['name', 'address', 'phone'], 'no_marker': True}"/>
                    </div>
                    <div class="col-6">
                        <strong>Zone :</strong> <span t-field="course.zone_id"/><br/>
                        <strong>Date :</strong> <span t-field="course.date_course"/><br/>
                        <strong>Livreur :</strong>
                        <span t-if="course.livreur_id" t-field="course.livreur_id"/>
                        <span t-else="">à désigner</span>
                    </div>
                </div>
                <table class="table table-sm mt-4">
                    <thead>
                        <tr><th>Poids</th><th>Étiquettes</th><th class="text-end">Prix</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span t-field="course.poids"/> kg</td>
                            <td><t t-out="', '.join(course.etiquette_ids.mapped('name')) or '—'"/></td>
                            <td class="text-end"><span t-field="course.prix"/></td>
                        </tr>
                    </tbody>
                </table>
                <p t-if="course.consigne"><strong>Consigne :</strong> <span t-field="course.consigne"/></p>
                <div class="row mt-5">
                    <div class="col-6">Signature du livreur :</div>
                    <div class="col-6">Signature du client :</div>
                </div>
            </div>
        </t>
    </template>

    <!-- 3. Le modèle appelé par l'action : une page par course, dans la langue du client -->
    <template id="report_bordereau">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="course">
                <t t-call="baobab_livraison.report_bordereau_document" t-lang="course.client_id.lang"/>
            </t>
        </t>
    </template>
</odoo>"""

LECONS = [
# ---------------------------------------------------------------- 3.2.1
dict(code="3.2.1", id=1359, seq=21, minutes=10,
titre="QWeb : la langue des modèles",
description="t-if, t-foreach, t-out, t-field, t-set, t-call : les directives pour fabriquer des PDF et des pages web.",
html=fiche(
objectif="lire et écrire un modèle QWeb : conditions, boucles, affichage de valeurs.",
intro="Les bordereaux PDF, les pages du site, le portail, les e-mails : tout cela est fabriqué avec <b>QWeb</b>, le langage de modèles d'Odoo. C'est du HTML, avec des attributs qui commencent par <code>t-</code>.",
corps=[
("code", """<ul>
    <li t-foreach="courses" t-as="c" t-attf-class="ligne-#{c_index}">
        <t t-out="c.name"/>
        <t t-if="c.poids &gt; 5">lourd</t>
        <t t-elif="c.poids &gt; 2">moyen</t>
        <t t-else="">léger</t>
        <t t-if="c_last">(dernière)</t>
    </li>
</ul>
<t t-set="total" t-value="sum(courses.mapped('prix'))"/>
<p>Total : <t t-out="total"/></p>""", "Un petit modèle QWeb"),
("code", """<ul><li class="ligne-0">BL/2026/0001 moyen </li><li class="ligne-1">BL/2026/0002 lourd (dernière)</li></ul><p>Total : 5900.0</p>""", "Résultat réel sur la base de démonstration (Odoo 20)"),
("tableau", ["Directive", "Rôle"], [
  ["<code>t-if</code>, <code>t-elif</code>, <code>t-else</code>", "afficher selon une condition (écrire <code>&amp;gt;</code> pour « plus grand que » : c'est du XML)"],
  ["<code>t-foreach</code> + <code>t-as</code>", "répéter pour chaque élément ; variables offertes : <code>c_index</code> (0, 1…), <code>c_first</code>, <code>c_last</code>"],
  ["<code>t-out</code>", "afficher une valeur, en protégeant les caractères HTML"],
  ["<code>t-field</code>", "afficher un champ d'une fiche, formaté selon son type (date, montant avec devise, contact…)"],
  ["<code>t-set</code> + <code>t-value</code>", "créer une variable"],
  ["<code>t-att-xxx</code>, <code>t-attf-xxx</code>", "calculer un attribut HTML ; <code>t-attf</code> mélange texte et <code>#{…}</code>"],
  ["<code>t-call</code>", "insérer un autre modèle (l'en-tête de la société, la mise en page)"],
]),
("h", "t-out ou t-field ?"),
("p", "<code>t-out=\"course.prix\"</code> affiche <code>1500.0</code> ; <code>t-field=\"course.prix\"</code> affiche <code>1 500 CFA</code> avec la devise et le format du pays. Dans un rapport, pour un champ de fiche, prends <code>t-field</code>."),
("version", "<b>Piège d'Odoo 20</b> : <code>t-esc</code> et <code>t-raw</code>, partout dans les tutoriels d'avant Odoo 15, n'affichent <b>plus rien</b>, sans erreur. Seul le journal le signale : <code>Unknown directives or unused attributes: {'t-esc'}</code> (vérifié). Remplace-les par <code>t-out</code>."),
],
exercice=[
("p", "Dans le terminal d'Odoo, crée un petit modèle QWeb qui liste les courses avec leur zone, et « (livrée) » pour celles qui le sont. Rends-le avec <code>env[\"ir.qweb\"]._render(…)</code>. Puis remplace un <code>t-out</code> par <code>t-esc</code> et observe : la valeur disparaît."),
],
retenir=[
  "QWeb = HTML + attributs <code>t-</code>.",
  "<code>t-if</code>/<code>t-elif</code>/<code>t-else</code>, <code>t-foreach</code>/<code>t-as</code>, <code>t-set</code>, <code>t-call</code>.",
  "<code>t-field</code> pour un champ formaté, <code>t-out</code> pour une valeur.",
  "Odoo 20 : <code>t-esc</code> et <code>t-raw</code> n'affichent plus rien.",
]),
quiz=[
("Quelle directive affiche un montant avec sa devise, au format du pays ?", [
  ("t-field=\"course.prix\"", V, "Oui."),
  ("t-out=\"course.prix\"", F, "Non : t-out affiche 1500.0, sans devise."),
  ("t-esc=\"course.prix\"", F, "Non : en Odoo 20, t-esc n'affiche plus rien."),
]),
("Dans t-foreach=\"courses\" t-as=\"c\", comment savoir si on est sur la dernière course ?", [
  ("c_last", V, "Oui (et c_index, c_first)."),
  ("c.last", F, "Non : ce serait un champ last de la course."),
  ("loop.last", F, "C'est la syntaxe d'autres langages (Jinja), pas de QWeb."),
]),
("Un ancien modèle utilise t-esc. Que se passe-t-il en Odoo 20 ?", [
  ("La valeur ne s'affiche pas, avec un avertissement dans le journal", V, "Oui : remplace par t-out."),
  ("Ça marche comme avant", F, "Non."),
  ("Le module refuse de s'installer", F, "Non : c'est justement le piège, aucune erreur."),
]),
]),

# ---------------------------------------------------------------- 3.2.2
dict(code="3.2.2", id=2935, seq=22, minutes=10,
titre="Premier rapport PDF : le bordereau de livraison",
description="Créer le bordereau de livraison et l'imprimer depuis le menu Actions d'une course.",
html=fiche(
objectif="créer le bordereau de livraison d'une course et l'imprimer en PDF depuis Odoo.",
intro="Le livreur part avec un bordereau papier : référence, client, zone, poids, prix, et deux cases pour les signatures. Un rapport Odoo, c'est deux choses : une <b>action</b> (l'entrée du menu Actions) et un <b>modèle QWeb</b> (le contenu).",
corps=[
("code", RAPPORT, "report/baobab_course_report.xml (à ajouter dans data du manifeste)"),
("h", "L'action ir.actions.report"),
("tableau", ["Champ", "Rôle"], [
  ["<code>report_type</code>", "<code>qweb-pdf</code> pour un PDF (<code>qweb-html</code> pour l'afficher dans le navigateur)"],
  ["<code>report_name</code>", "le modèle QWeb à utiliser : <code>module.id_du_template</code>"],
  ["<code>print_report_name</code>", "le nom du fichier PDF : <code>Bordereau - BL/2026/0001.pdf</code>"],
  ["<code>binding_model_id</code> + <code>binding_type</code>", "ajoute le rapport au menu <b>Actions</b> (⋮) des courses"],
]),
("p", "Dans le modèle, Odoo fournit <code>docs</code> : les courses à imprimer. <code>web.html_container</code> prépare la page, <code>web.external_layout</code> ajoute l'en-tête et le pied de page de la société."),
("version", "<b>Odoo 20</b> : le champ <code>report_file</code>, présent dans presque tous les anciens exemples, n'existe plus. Le laisser bloque l'installation : <code>ValueError: Invalid field 'report_file' in 'ir.actions.report'</code> (vérifié). Supprime simplement la ligne."),
("h", "Imprimer"),
("p", "Ouvre une course, clique sur le bouton <b>⋮</b> (Actions) à côté de la référence, puis sur <b>Bordereau de livraison</b> (vérifié en Odoo 20 : le menu affiche Bordereau de livraison, Dupliquer, Supprimer). Pour tester plus vite pendant que tu écris, ouvre dans le navigateur <code>/report/html/baobab_livraison.report_bordereau/1</code> : la version HTML de la course n° 1, sans passer par le moteur PDF."),
("attention", "Il faut un moteur PDF", "Odoo ne fabrique pas le PDF lui-même : il confie le HTML à un programme, en général <b>wkhtmltopdf</b>. S'il manque, Odoo affiche « Unable to find the PDF engine on this system. The report will be shown in html. » (leçon 3.2.4)."),
],
exercice=[
("p", "Crée le fichier du rapport, ajoute-le au manifeste, mets à jour. Imprime le bordereau d'une course. Vérifie le nom du fichier, puis la version HTML par l'adresse <code>/report/html/…</code>. Ajoute ensuite une ligne « Étiquettes » qui affiche « Fragile » en gras quand la course porte cette étiquette."),
],
retenir=[
  "Un rapport = une action <code>ir.actions.report</code> + un modèle QWeb.",
  "<code>docs</code> = les fiches à imprimer ; <code>web.external_layout</code> = en-tête et pied de page.",
  "<code>binding_model_id</code> met le rapport dans le menu Actions (⋮) de la fiche.",
  "Odoo 20 : pas de <code>report_file</code>.",
]),
quiz=[
("Comment le bordereau apparaît-il dans le menu Actions (⋮) des courses ?", [
  ("Grâce à binding_model_id et binding_type=\"report\" dans l'action", V, "Oui."),
  ("Grâce à un bouton dans la vue formulaire", F, "Possible aussi, mais ce n'est pas le menu Actions."),
  ("Automatiquement pour tout modèle QWeb", F, "Non."),
]),
("Dans le modèle du rapport, que contient la variable docs ?", [
  ("Les fiches à imprimer", V, "Oui : une ou plusieurs courses."),
  ("La documentation d'Odoo", F, "Non."),
  ("Le PDF déjà fabriqué", F, "Non."),
]),
("Un vieil exemple contient <field name=\"report_file\">. Que fait Odoo 20 ?", [
  ("Il refuse l'installation : le champ n'existe plus", V, "Oui (vérifié) : supprime la ligne."),
  ("Il l'ignore", F, "Non."),
  ("Il s'en sert comme nom du PDF", F, "Non : c'est print_report_name."),
]),
]),

# ---------------------------------------------------------------- 3.2.3
dict(code="3.2.3", id=2740, seq=23, minutes=10,
titre="Mise en page, logo, en-tête de la société, traductions",
description="Un bordereau aux couleurs de la société, dans la langue du client.",
html=fiche(
objectif="donner au bordereau l'en-tête de la société et l'imprimer dans la langue du client.",
intro="Un bordereau professionnel porte le logo et l'adresse de Baobab, et parle la langue du client. Bonne nouvelle : une grande partie se règle sans code.",
corps=[
("h", "1. L'en-tête de la société : sans code"),
("p", "<code>web.external_layout</code> reprend les réglages de la société : <b>Paramètres</b> › section Sociétés › <b>Configurer la mise en page du document</b>. On y choisit le modèle de mise en page, le logo, les couleurs (bleu TAAGG #0B415B, par exemple), la police et le texte du pied de page. Tous les rapports qui appellent <code>web.external_layout</code> en profitent."),
("attention", "Pas d'en-tête sur ton PDF ?", "Avec le wkhtmltopdf d'Ubuntu (non « patché »), l'en-tête et le pied de page sont <b>ignorés</b> : le journal affiche <code>The switch --header-html, is not support using unpatched qt, and will be ignored.</code> (vérifié). Odoo recommande la version 0.12.6.1 « with patched qt » (paquets sur github.com/wkhtmltopdf/packaging). Voir la leçon suivante."),
("h", "2. La langue du client : t-lang"),
("code", """<template id="report_bordereau">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="course">
            <t t-call="baobab_livraison.report_bordereau_document" t-lang="course.client_id.lang"/>
        </t>
    </t>
</template>""", "On sépare le document (une course) de la boucle, et on appelle le document dans la langue du client"),
("p", "Résultat vérifié : avec un client en français, la date s'imprime <code>28/11/2026</code> ; avec un client en anglais, <code>11/28/2026</code>. Les libellés traduits (statuts, textes du modèle) suivent aussi, à condition qu'une traduction existe."),
("h", "3. Les traductions du module"),
("code", """python3 odoo-bin i18n export -c ~/baobab/odoo.conf baobab_livraison""", "Terminal (odoo.conf doit contenir db_name) : crée baobab_livraison/i18n/baobab_livraison.pot"),
("p", "Le fichier <code>.pot</code> liste tous les textes à traduire (112 entrées pour notre module : libellés des champs, menus, textes du bordereau, messages d'erreur). On le copie en <code>i18n/en.po</code> pour l'anglais, on remplit les <code>msgstr</code>, et Odoo charge la traduction à la mise à jour du module. Les textes Python sont traduits s'ils passent par <code>self.env._(\"…\")</code>."),
("version", "<b>Odoo 20</b> : l'export se fait avec la commande <code>odoo-bin i18n export</code> (sous-commandes <code>import</code>, <code>export</code>, <code>loadlang</code>). Les tutoriels d'avant utilisent <code>--i18n-export=fichier.po --modules=…</code>."),
],
exercice=[
("p", "Configure la mise en page du document (logo, couleur #0B415B), puis sépare ton bordereau en deux modèles avec <code>t-lang</code>. Mets un client en anglais, imprime : la date change de format. Enfin exporte le <code>.pot</code> de ton module et compte les entrées."),
],
retenir=[
  "En-tête, logo, couleurs : Paramètres › Configurer la mise en page du document.",
  "<code>t-lang=\"course.client_id.lang\"</code> : le document dans la langue du client.",
  "<code>odoo-bin i18n export</code> crée le <code>.pot</code> ; une langue = un fichier <code>.po</code>.",
  "En-tête absent du PDF : wkhtmltopdf non patché.",
]),
quiz=[
("Où règle-t-on le logo et les couleurs des documents imprimés ?", [
  ("Paramètres › Configurer la mise en page du document", V, "Oui : web.external_layout les reprend."),
  ("Dans chaque modèle QWeb", F, "Non : c'est commun à tous les rapports."),
  ("Dans le manifeste", F, "Non."),
]),
("Comment imprimer chaque bordereau dans la langue de son client ?", [
  ("t-call du document avec t-lang=\"course.client_id.lang\"", V, "Oui."),
  ("Changer la langue de l'utilisateur avant d'imprimer", F, "Fastidieux, et faux pour plusieurs clients."),
  ("Ce n'est pas possible", F, "Si."),
]),
("Ton PDF sort sans en-tête de société, et le journal parle de « unpatched qt ». Pourquoi ?", [
  ("Le wkhtmltopdf installé n'est pas la version patchée : il ignore en-têtes et pieds de page", V, "Oui."),
  ("Le modèle n'appelle pas web.html_container", F, "Non : le corps sortirait quand même, le message vise l'en-tête."),
  ("La société n'a pas de logo", F, "Le message du journal dit autre chose."),
]),
]),

# ---------------------------------------------------------------- 3.2.4
dict(code="3.2.4", id=2937, seq=24, minutes=10,
titre="Quand le PDF ne sort pas : pannes courantes",
description="Diagnostiquer le moteur PDF d'Odoo 20 : wkhtmltopdf absent, PDF sans style, impression groupée, t-esc.",
html=fiche(
objectif="savoir diagnostiquer un PDF qui ne sort pas, ou qui sort mal, chez un client.",
intro="« Le bouton Imprimer ne marche pas ! » C'est un appel classique. Dans 9 cas sur 10, la cause est dans cette fiche. Toutes ces pannes ont été reproduites sur Odoo 20.",
corps=[
("h", "Le moteur PDF en Odoo 20"),
("p", "Odoo 20 range les moteurs dans des modules à part : <code>base_report_wkhtmltox</code> (wkhtmltopdf, installé automatiquement, moteur par défaut) et <code>base_report_paper_muncher</code> (Paper Muncher, le nouveau moteur maison d'Odoo, à installer avec son programme, version 0.6 ou plus). Le moteur par défaut est noté dans le paramètre système <code>report.pdf_engine_default</code>."),
("tableau", ["Symptôme", "Cause", "Solution"], [
  ["« Unable to find the PDF engine on this system. The report will be shown in html. »", "wkhtmltopdf n'est pas installé sur le serveur", "<code>sudo apt install wkhtmltopdf</code>, ou mieux la version 0.12.6.1 patchée"],
  ["« You need to start Odoo with at least two workers to print a pdf version of the reports. »", "Odoo tourne avec <code>workers = 1</code>", "<code>workers = 0</code> (développement) ou 2 et plus (production)"],
  ["Le PDF sort sans mise en page (texte brut) ; journal : <code>Exit with code 1 due to network error: ConnectionRefusedError</code>", "wkhtmltopdf n'arrive pas à télécharger les styles depuis Odoo (serveur web arrêté, mauvaise adresse <code>web.base.url</code>, pare-feu)", "vérifier <code>web.base.url</code>, ou fixer <code>report.url</code> (paramètre système) à une adresse que le serveur joint lui-même, par ex. <code>http://localhost:8069</code>"],
  ["Pas d'en-tête ni de pied de page ; journal : <code>--header-html, is not support using unpatched qt</code>", "wkhtmltopdf non patché (celui d'Ubuntu)", "installer 0.12.6.1 « with patched qt »"],
  ["Imprimer plusieurs courses d'un coup : « Tentative de conversion de plusieurs documents dans wkhtmltopdf avec une version non patchée de QT »", "même cause", "même solution (ou imprimer une à une)"],
  ["Des valeurs manquent dans le PDF, sans erreur", "<code>t-esc</code> / <code>t-raw</code> dans le modèle", "remplacer par <code>t-out</code>"],
  ["Les codes-barres (<code>/report/barcode/…</code>) ne s'affichent pas ; journal : <code>RenderPMError: cannot import desired renderPM backend rlPyCairo</code>", "installation depuis les sources sous Linux : le complément de dessin de reportlab manque (le fichier <code>requirements.txt</code> ne l'installe que sous Windows)", "dans l'environnement virtuel d'Odoo : <code>pip install rl-renderPM==4.0.3</code>, puis redémarrer Odoo (vérifié)"],
]),
("h", "La méthode"),
("liste", [
  "<b>Regarder la version HTML</b> : <code>/report/html/&lt;report_name&gt;/&lt;id&gt;</code>. Si le HTML est faux, le problème est dans le modèle QWeb ; s'il est juste, c'est le moteur PDF.",
  "<b>Lire le journal d'Odoo</b> au moment de l'impression : les messages de wkhtmltopdf y sont recopiés.",
  "<b>Vérifier la version</b> : <code>wkhtmltopdf --version</code> doit afficher « (with patched qt) ».",
]),
("astuce", "Paper Muncher", "Paper Muncher est le moteur PDF écrit par Odoo, présenté comme le successeur de wkhtmltopdf (projet sur odoo.github.io/paper-muncher). En Odoo 20, il faut installer son programme sur le serveur puis le module <code>base_report_paper_muncher</code> ; chaque rapport peut alors choisir son moteur (type « PDF (Paper Muncher) »). Nous ne l'avons pas encore testé : à vérifier sur le serveur du client avant de le proposer."),
],
exercice=[
("p", "Provoque deux pannes sur ta base de test : (1) arrête le serveur web et imprime depuis le terminal d'Odoo avec <code>env[\"ir.actions.report\"]._render_qweb_pdf(\"baobab_livraison.action_report_bordereau\", [1])</code> : regarde le journal et le PDF obtenu ; (2) sélectionne deux courses dans la liste et imprime-les ensemble. Pour chacune, note le message et la solution."),
],
retenir=[
  "Odoo 20 : moteur PDF dans un module (wkhtmltopdf par défaut, Paper Muncher en option).",
  "D'abord la version HTML, ensuite le journal, enfin <code>wkhtmltopdf --version</code>.",
  "PDF sans style = les styles ne sont pas téléchargés (<code>web.base.url</code>, <code>report.url</code>).",
  "En-têtes absents et impression groupée refusée = wkhtmltopdf non patché.",
]),
quiz=[
("Le PDF sort en texte brut, sans mise en page. Que regardes-tu d'abord ?", [
  ("Le journal : wkhtmltopdf n'a pas pu télécharger les styles (web.base.url, report.url)", V, "Oui."),
  ("La langue du client", F, "Aucun rapport."),
  ("Le nombre de champs du modèle", F, "Non."),
]),
("Comment savoir si le problème vient du modèle QWeb ou du moteur PDF ?", [
  ("Ouvrir la version HTML : /report/html/<report_name>/<id>", V, "Oui : HTML juste = moteur en cause."),
  ("Réinstaller Odoo", F, "Non."),
  ("Supprimer le rapport", F, "Non."),
]),
("Imprimer deux courses ensemble échoue, une seule fonctionne. Cause la plus probable ?", [
  ("wkhtmltopdf non patché", V, "Oui (message vérifié sur Odoo 20)."),
  ("Une des deux courses n'a pas de prix", F, "Non."),
  ("Le rapport n'a pas de binding", F, "Non : il ne serait pas dans le menu du tout."),
]),
]),
]
