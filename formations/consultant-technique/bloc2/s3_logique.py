"""Bloc 2 — Section « La logique métier » (section 2721, cours 209).
Code et sorties vérifiés sur Odoo 20.0 le 27/11/2026 (module de référence, odoo-bin shell, méthode onchange)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

ACTIONS = """from odoo.exceptions import UserError

    def action_demarrer(self):
        for course in self:
            if course.state != "brouillon":
                raise UserError(self.env._("Seule une course en brouillon peut démarrer."))
            if not course.livreur_id:
                raise UserError(self.env._("Choisis un livreur avant de démarrer la course %s.", course.name))
        self.write({"state": "en_route"})

    def action_livrer(self):
        for course in self:
            if course.state != "en_route":
                raise UserError(self.env._("Seule une course en route peut être livrée."))
        self.write({"state": "livree", "date_livraison": fields.Datetime.now()})

    def action_annuler(self):
        if any(course.state == "livree" for course in self):
            raise UserError(self.env._("Une course livrée ne peut plus être annulée."))
        self.write({"state": "annulee"})"""

BOUTONS = """<header>
    <button name="action_demarrer" type="object" string="Démarrer" class="btn-primary" invisible="state != 'brouillon'"/>
    <button name="action_livrer" type="object" string="Livrée" class="btn-primary" invisible="state != 'en_route'"/>
    <button name="action_annuler" type="object" string="Annuler" invisible="state in ('livree', 'annulee')"/>
    <field name="state" widget="statusbar" statusbar_visible="brouillon,en_route,livree"/>
</header>"""

LECONS = [
# ---------------------------------------------------------------- 2.3.1
dict(code="2.3.1", id=1356, seq=31, minutes=10,
titre="Statuts et boutons d'action",
description="Faire avancer une course : brouillon, en route, livrée, avec des méthodes action_… et des boutons.",
html=fiche(
objectif="faire avancer une course de « Brouillon » à « Livrée » avec des boutons, et bloquer les étapes impossibles.",
intro="Une course suit un chemin : on la crée (brouillon), le livreur part (en route), il livre (livrée). Parfois on l'annule. Chaque étape est un bouton, et chaque bouton appelle une méthode Python.",
corps=[
("h", "Les méthodes d'action"),
("code", ACTIONS, "models/course.py"),
("liste", [
  "Une méthode appelée par un bouton est publique : son nom ne commence pas par <code>_</code>. Par convention : <code>action_…</code>.",
  "<code>self</code> peut contenir plusieurs courses (actions groupées depuis la liste) : on vérifie chacune, puis un seul <code>write</code>.",
  "<code>UserError</code> affiche un message clair à l'utilisateur et annule tout ce que la méthode avait commencé.",
]),
("h", "Les boutons dans l'écran (fichier fourni)"),
("p", "Les écrans s'apprennent au Bloc 3. Pour l'instant, recopie le fichier <code>views/baobab_course_views.xml</code> donné en entier à la fin de cette fiche. Voici sa partie haute :"),
("code", BOUTONS, "views/baobab_course_views.xml (extrait)"),
("liste", [
  "<code>name=\"action_demarrer\"</code> + <code>type=\"object\"</code> : le bouton appelle la méthode du même nom.",
  "<code>invisible=\"state != 'brouillon'\"</code> : le bouton n'apparaît qu'au bon moment.",
  "<code>widget=\"statusbar\"</code> : la barre des étapes en haut à droite.",
]),
("attention", "Cacher ne suffit pas", "Un bouton caché peut quand même être appelé (par l'API, par un autre programme). La vraie protection, ce sont les vérifications dans la méthode Python. On teste : sur une course en brouillon, <code>action_livrer()</code> donne <code>UserError: Seule une course en route peut être livrée.</code>"),
("version", "En Odoo 17 et suivants, on écrit directement <code>invisible=\"state != 'brouillon'\"</code>. En Odoo 16 et avant, on utilisait <code>attrs=\"{'invisible': [...]}\"</code> ou <code>states=\"brouillon\"</code> : ces attributs ne sont plus acceptés."),
],
exercice=[
("p", "Ajoute les trois méthodes et le fichier d'écran fourni. À l'écran : crée une course sans livreur et clique sur « Démarrer » (message attendu) ; choisis un contact comme livreur, démarre, puis livre. Vérifie que « Livrée le » est rempli et que le bouton « Annuler » a disparu."),
("code", """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Fourni au Bloc 2 : recopie ce fichier tel quel. On apprend à écrire les vues au Bloc 3. -->
    <record id="view_baobab_course_list" model="ir.ui.view">
        <field name="name">baobab.course.list</field>
        <field name="model">baobab.course</field>
        <field name="arch" type="xml">
            <list>
                <field name="name"/>
                <field name="date_course"/>
                <field name="client_id"/>
                <field name="zone_id"/>
                <field name="livreur_id"/>
                <field name="prix" sum="Total"/>
                <field name="state"/>
            </list>
        </field>
    </record>

    <record id="view_baobab_course_form" model="ir.ui.view">
        <field name="name">baobab.course.form</field>
        <field name="model">baobab.course</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <button name="action_demarrer" type="object" string="Démarrer" class="btn-primary" invisible="state != 'brouillon'"/>
                    <button name="action_livrer" type="object" string="Livrée" class="btn-primary" invisible="state != 'en_route'"/>
                    <button name="action_annuler" type="object" string="Annuler" invisible="state in ('livree', 'annulee')"/>
                    <field name="state" widget="statusbar" statusbar_visible="brouillon,en_route,livree"/>
                </header>
                <sheet>
                    <h1><field name="name"/></h1>
                    <group>
                        <group>
                            <field name="client_id"/>
                            <field name="zone_id"/>
                            <field name="poids"/>
                            <field name="prix"/>
                        </group>
                        <group>
                            <field name="date_course"/>
                            <field name="livreur_id"/>
                            <field name="etiquette_ids" widget="many2many_tags"/>
                            <field name="date_livraison"/>
                        </group>
                    </group>
                    <field name="consigne" placeholder="Consigne pour le livreur…"/>
                </sheet>
            </form>
        </field>
    </record>
</odoo>""", "views/baobab_course_views.xml (fichier fourni ; ajoute-le dans data du manifeste, avant baobab_menus.xml)"),
],
retenir=[
  "Un statut = un champ <code>Selection</code> ; une étape = une méthode <code>action_…</code>.",
  "Un bouton <code>type=\"object\"</code> appelle la méthode qui porte son <code>name</code>.",
  "<code>UserError</code> : message à l'utilisateur, tout est annulé.",
  "Les vérifications se font en Python, pas seulement en cachant le bouton.",
]),
quiz=[
("Un bouton <button name=\"action_livrer\" type=\"object\"/> : que fait-il ?", [
  ("Il appelle la méthode Python action_livrer sur la fiche affichée", V, "Oui."),
  ("Il ouvre une nouvelle fenêtre", F, "Non : ce serait type=\"action\"."),
  ("Il change seulement la couleur du statut", F, "Non."),
]),
("Pourquoi vérifier le statut dans action_livrer alors que le bouton est caché ?", [
  ("Parce qu'une méthode peut être appelée autrement qu'avec le bouton", V, "Oui : par l'API ou par un autre programme."),
  ("Parce qu'Odoo l'exige pour installer le module", F, "Non."),
  ("Ce n'est pas utile", F, "Si : cacher un bouton ne protège rien."),
]),
("Que fait raise UserError(...) au milieu d'une méthode ?", [
  ("Affiche le message à l'utilisateur et annule les changements de la méthode", V, "Oui."),
  ("Écrit seulement dans le journal", F, "Non : l'utilisateur voit le message."),
  ("Arrête le serveur Odoo", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.3.2
dict(code="2.3.2", id=2722, seq=32, minutes=10,
titre="Les onchange",
description="Réagir pendant la saisie : le prix s'affiche dès qu'on choisit la zone, un avertissement pour les colis lourds.",
html=fiche(
objectif="réagir pendant que l'utilisateur remplit le formulaire, avant même qu'il enregistre.",
intro="Quand le réceptionniste choisit la zone Mermoz, le prix doit s'afficher tout de suite. Quand il tape 35 kg, Odoo doit le prévenir. Tout cela se passe <b>pendant la saisie</b>, avant l'enregistrement.",
corps=[
("h", "Bonne nouvelle : les champs calculés le font déjà"),
("p", "Le champ <code>prix</code> est calculé avec <code>@api.depends(\"zone_id.tarif\", \"poids\")</code>. Dans un formulaire, Odoo le recalcule <b>à chaque changement</b> de zone ou de poids, sans rien écrire de plus. Pour « proposer le tarif dès qu'on choisit la zone », la leçon sur les champs calculés suffit."),
("h", "@api.onchange : pour avertir ou proposer"),
("code", """@api.onchange("poids")
def _onchange_poids(self):
    if self.poids > 30:
        return {"warning": {
            "title": self.env._("Colis lourd"),
            "message": self.env._("Au-delà de 30 kg, prévois un livreur avec un tricycle."),
        }}""", "models/course.py"),
("p", "Quand l'utilisateur change le poids, Odoo appelle cette méthode sur la fiche en cours de saisie (pas encore enregistrée). Si elle renvoie un <code>warning</code>, une fenêtre s'affiche."),
("code", """{'value': {'prix': 7500.0},
 'warning': {'title': 'Colis lourd',
             'message': 'Au-delà de 30 kg, prévois un livreur avec un tricycle.',
             'type': 'dialog'}}""", "Réponse réelle d'Odoo 20 pour 35 kg à Mermoz : le prix recalculé + l'avertissement"),
("h", "Calculé ou onchange ?"),
("tableau", ["Besoin", "Outil"], [
  ["Une valeur toujours déduite d'autres champs (prix)", "champ calculé <code>compute</code>"],
  ["Un avertissement pendant la saisie", "<code>@api.onchange</code> + <code>warning</code>"],
  ["Une valeur proposée que l'utilisateur peut changer ensuite", "champ calculé avec <code>store=True, readonly=False</code> (méthode recommandée), ou un onchange"],
]),
("attention", "Un onchange ne protège pas", "Un onchange ne s'exécute que dans le formulaire. Une course créée par import ou par l'API ne passe pas par là. Pour une règle obligatoire, utilise une contrainte (<code>@api.constrains</code>)."),
("version", "Depuis Odoo 13, la documentation recommande les champs calculés plutôt que les onchange pour remplir des valeurs. Les onchange restent utiles pour les avertissements. Dans un onchange, <code>self</code> est une seule fiche, en mémoire."),
],
exercice=[
("p", "Ajoute l'onchange sur le poids et mets à jour. À l'écran, ouvre une nouvelle course, choisis Plateau puis Rufisque : le prix change sans enregistrer. Tape 35 kg : l'avertissement apparaît. Défi : ajoute un deuxième avertissement si la date de la course est dans le passé."),
],
retenir=[
  "Un champ calculé se met à jour tout seul pendant la saisie.",
  "<code>@api.onchange</code> sert surtout à afficher un avertissement.",
  "L'onchange ne tourne que dans le formulaire : jamais pour une règle obligatoire.",
  "Règle obligatoire → contrainte ; valeur déduite → champ calculé.",
]),
quiz=[
("Le prix se met-il à jour à l'écran quand on change la zone, avant d'enregistrer ?", [
  ("Oui, parce que c'est un champ calculé qui dépend de la zone", V, "Oui : Odoo recalcule pendant la saisie."),
  ("Non, il faut enregistrer d'abord", F, "Non."),
  ("Seulement si on écrit un onchange", F, "Non : le compute suffit."),
]),
("Une course est créée par l'API avec 40 kg. L'avertissement « Colis lourd » s'affiche-t-il ?", [
  ("Non : l'onchange ne tourne que dans le formulaire", V, "Oui."),
  ("Oui, toujours", F, "Non."),
  ("Oui, et la création est refusée", F, "Non : un onchange ne bloque rien."),
]),
("Pour interdire vraiment une date de course dans le passé, que choisir ?", [
  ("Une contrainte @api.constrains", V, "Oui : elle s'applique partout."),
  ("Un onchange avec un warning", F, "Non : il prévient seulement, et seulement dans le formulaire."),
  ("Cacher le champ", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.3.3
dict(code="2.3.4", id=2911, seq=34, minutes=10,
titre="Séquences et actions planifiées",
description="Numéroter les courses BL/2026/0001 et relancer chaque jour les courses en retard.",
html=fiche(
objectif="donner un numéro automatique à chaque course et programmer une tâche qui tourne chaque jour toute seule.",
intro="Chaque course doit avoir une référence lisible : BL/2026/0001, BL/2026/0002… Et chaque matin, Odoo doit repérer les courses « en route » depuis trop longtemps. Deux outils d'Odoo : les <b>séquences</b> et les <b>actions planifiées</b>.",
corps=[
("h", "1. La séquence"),
("code", """<?xml version="1.0" encoding="utf-8"?>
<odoo noupdate="1">
    <record id="seq_baobab_course" model="ir.sequence">
        <field name="name">Course de livraison</field>
        <field name="code">baobab.course</field>
        <field name="prefix">BL/%(year)s/</field>
        <field name="padding">4</field>
        <field name="company_id" eval="False"/>
    </record>
</odoo>""", "data/ir_sequence_data.xml"),
("p", "<code>%(year)s</code> devient l'année ; <code>padding</code> 4 donne 0001. <code>noupdate=\"1\"</code> : une mise à jour du module ne remet pas le compteur à zéro."),
("code", """@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get("name", "Nouveau") == "Nouveau":
            vals["name"] = self.env["ir.sequence"].next_by_code("baobab.course") or "Nouveau"
    return super().create(vals_list)""", "models/course.py"),
("p", "On complète la méthode <code>create</code> d'Odoo (on y revient dans la section sur l'héritage) : avant de créer, on demande le numéro suivant. Résultat : <code>BL/2026/0001</code>."),
("astuce", "Des trous dans la numérotation ?", "Un numéro pris n'est jamais rendu, même si la création échoue ensuite. Il peut donc manquer des numéros : c'est normal et voulu (deux utilisateurs ne reçoivent jamais le même)."),
("h", "2. L'action planifiée"),
("code", """@api.model
def _cron_relancer_retards(self):
    \"\"\"Tâche planifiée : une activité sur chaque course en route depuis avant-hier.\"\"\"
    limite = fields.Date.subtract(fields.Date.context_today(self), days=1)
    retards = self.search([("state", "=", "en_route"), ("date_course", "<", limite)])
    for course in retards:
        course.activity_schedule(
            "mail.mail_activity_data_todo",
            summary=self.env._("Course en retard"),
            note=self.env._("Appelle le livreur %s.", course.livreur_id.name or ""),
        )
    return retards""", "models/course.py"),
("code", """<record id="ir_cron_relancer_retards" model="ir.cron">
    <field name="name">Baobab : relancer les courses en retard</field>
    <field name="model_id" ref="model_baobab_course"/>
    <field name="state">code</field>
    <field name="code">model._cron_relancer_retards()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
</record>""", "data/ir_cron_data.xml"),
("p", "Pour la voir et la tester : active le mode développeur, puis <b>Paramètres › Technique › Actions planifiées</b>, ouvre « Baobab : relancer les courses en retard » et clique sur <b>Exécuter manuellement</b>. Une course en route depuis 3 jours reçoit l'activité « Course en retard »."),
("attention", "Une méthode de cron doit être rapide et sûre", "Elle tourne sans personne devant l'écran : pas de fenêtre, pas de question. Cherche avec un domaine précis (pas toutes les courses), et teste-la d'abord avec « Exécuter manuellement »."),
],
exercice=[
("p", "Ajoute la séquence et l'action planifiée (pense au manifeste). Crée trois courses : elles doivent recevoir BL/2026/0001, 0002, 0003. Démarre une course datée d'il y a 3 jours, puis exécute l'action planifiée manuellement : l'activité apparaît sur la course."),
],
retenir=[
  "Séquence : <code>ir.sequence</code> avec un <code>code</code>, appelée par <code>next_by_code</code>.",
  "<code>noupdate=\"1\"</code> protège le compteur lors des mises à jour.",
  "Action planifiée : <code>ir.cron</code> qui appelle <code>model._ma_methode()</code>.",
  "Tester une action planifiée : « Exécuter manuellement ».",
]),
quiz=[
("Que donne le préfixe BL/%(year)s/ avec padding 4 pour la première course de 2026 ?", [
  ("BL/2026/0001", V, "Oui."),
  ("BL/%(year)s/1", F, "Non : %(year)s est remplacé par l'année."),
  ("BL/26/1", F, "Non : %(year)s donne l'année sur 4 chiffres et padding 4 complète avec des zéros."),
]),
("Pourquoi noupdate=\"1\" sur la séquence ?", [
  ("Pour qu'une mise à jour du module ne réinitialise pas la séquence", V, "Oui : le compteur continue."),
  ("Pour empêcher de créer des courses", F, "Non."),
  ("Pour que la séquence ne s'installe jamais", F, "Non : elle s'installe, puis n'est plus écrasée."),
]),
("Comment tester tout de suite une action planifiée quotidienne ?", [
  ("Paramètres › Technique › Actions planifiées, puis « Exécuter manuellement »", V, "Oui (mode développeur activé)."),
  ("Attendre le lendemain", F, "Ça marche, mais c'est long."),
  ("Redémarrer Odoo", F, "Non : redémarrer ne lance pas la tâche."),
]),
]),

# ---------------------------------------------------------------- 2.3.4
dict(code="2.3.5", id=2723, seq=35, minutes=10,
titre="Contexte, utilisateur, société et sudo",
description="Savoir qui agit, dans quelle langue, pour quelle société, et avec quels droits.",
html=fiche(
objectif="savoir qui exécute ton code, avec quels réglages et quels droits, grâce à <code>self.env</code>.",
intro="Le même code peut être lancé par l'administrateur, par un livreur, ou par une tâche planifiée. <code>self.env</code> (l'<b>environnement</b>) dit qui agit, dans quelle langue, pour quelle société.",
corps=[
("h", "Ce que contient self.env"),
("tableau", ["Expression", "Ce que c'est"], [
  ["<code>self.env.user</code>", "l'utilisateur qui agit (une fiche <code>res.users</code>)"],
  ["<code>self.env.company</code>", "la société active"],
  ["<code>self.env.context</code>", "un dictionnaire de réglages : langue, fuseau horaire…"],
  ["<code>self.env.su</code>", "<code>True</code> si on est en mode super-utilisateur (<code>sudo</code>)"],
  ["<code>self.env[\"baobab.zone\"]</code>", "accès à un autre modèle"],
]),
("code", """>>> env.user.name, env.uid, env.su
('OdooBot', 1, True)
>>> env.context
{'lang': 'en_US', 'tz': 'Europe/Brussels', 'uid': 1}""", "Terminal d'Odoo (base de test : la langue et le fuseau viennent de l'utilisateur)"),
("h", "with_context : changer un réglage"),
("code", """>>> c = env["baobab.course"].with_context(default_poids=8).create(
...     {"client_id": awa.id, "zone_id": mermoz.id})
>>> c.poids, c.prix
(8.0, 2100.0)""", "Une valeur par défaut passée par le contexte"),
("p", "Une clé <code>default_&lt;champ&gt;</code> dans le contexte donne une valeur par défaut. C'est ce que font les boutons « Créer » qui pré-remplissent un formulaire."),
("h", "with_user et sudo : les droits"),
("code", """>>> C = env["baobab.course"]
>>> C.with_user(portail).search_count([])
Traceback (most recent call last):
…
odoo.exceptions.AccessError: You are not allowed to access 'Course de livraison' (baobab.course) records.

This operation is allowed for the following groups:
	- Sales / User: Own Documents Only
…
>>> C.with_user(portail).sudo().search_count([])
3""", "Un utilisateur du portail n'a aucun droit sur les courses ; sudo() passe outre"),
("liste", [
  "<code>with_user(u)</code> : agir à la place de l'utilisateur <code>u</code>, avec ses droits.",
  "<code>sudo()</code> : ignorer les droits d'accès pour cette opération.",
]),
("attention", "sudo() avec prudence", "<code>sudo()</code> ouvre toutes les portes. Utilise-le pour une opération précise et justifiée (par exemple : écrire dans un journal technique que l'utilisateur ne peut pas lire), jamais pour « faire disparaître » une erreur de droits. Une erreur de droits se corrige dans <code>ir.access.csv</code>."),
("version", "En Odoo 20, l'environnement s'utilise comme dans les versions 17 à 19. Rappel : dans <code>odoo-bin shell</code>, tu es OdooBot avec <code>env.su = True</code> ; pour tester comme un vrai utilisateur, utilise <code>with_user</code>."),
],
exercice=[
("p", "Dans le terminal d'Odoo : (1) affiche la société active et sa devise ; (2) crée une course avec <code>with_context(default_poids=12)</code> et vérifie son prix ; (3) compte les courses en tant que l'utilisateur de démonstration (<code>login = \"demo\"</code>), puis en tant qu'un utilisateur du portail, et explique la différence."),
],
retenir=[
  "<code>self.env</code> : l'utilisateur, la société, le contexte, l'accès aux modèles.",
  "<code>with_context(...)</code> : changer un réglage (langue, valeur par défaut…).",
  "<code>with_user(u)</code> : agir avec les droits de <code>u</code>.",
  "<code>sudo()</code> : sans contrôle des droits. Rarement, et pour une raison précise.",
]),
quiz=[
("Que donne self.env.user ?", [
  ("L'utilisateur qui exécute le code", V, "Oui."),
  ("Le client de la course", F, "Non : c'est client_id."),
  ("L'administrateur, toujours", F, "Non : celui qui agit."),
]),
("with_context(default_poids=8).create({...}) sans préciser le poids : quel poids ?", [
  ("8 kg", V, "Oui : la clé default_poids sert de valeur par défaut (vérifié : prix 2 100 F à Mermoz)."),
  ("1 kg, la valeur par défaut du champ", F, "Non : le contexte passe avant."),
  ("Une erreur", F, "Non."),
]),
("Un utilisateur reçoit une erreur de droits sur les courses. La bonne correction ?", [
  ("Ajouter le droit qui manque dans ir.access.csv pour son groupe", V, "Oui."),
  ("Mettre sudo() partout dans le code", F, "Non : c'est ouvrir toutes les portes à tout le monde."),
  ("Lui donner le mot de passe administrateur", F, "Surtout pas."),
]),
]),

# ---------------------------------------------------------------- 2.3.5
dict(code="2.3.3", id=2724, seq=33, minutes=10,
titre="Discussion, activités et suivi des changements",
description="Ajouter le chatter aux courses : messages, activités et historique des changements de statut.",
html=fiche(
objectif="donner aux courses un fil de discussion, des activités et un historique automatique des changements.",
intro="Sous chaque devis Odoo, il y a un fil : les messages, les activités à faire, l'historique (« Statut : Brouillon → En route »). C'est le <b>chatter</b>. Tu peux l'offrir à tes courses en trois lignes.",
corps=[
("h", "1. Hériter de mail.thread et mail.activity.mixin"),
("code", """class BaobabCourse(models.Model):
    _name = "baobab.course"
    _description = "Course de livraison"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    client_id = fields.Many2one("res.partner", string="Client", required=True, tracking=True)
    livreur_id = fields.Many2one("res.partner", string="Livreur", tracking=True, ...)
    state = fields.Selection([...], string="Statut", default="brouillon", tracking=True)""", "models/course.py"),
("liste", [
  "<code>mail.thread</code> : les messages et le suivi des changements.",
  "<code>mail.activity.mixin</code> : les activités (appeler, relancer…).",
  "Le module doit dépendre de <code>mail</code> : <code>\"depends\": [\"base\", \"mail\"]</code>.",
  "<code>tracking=True</code> : chaque changement de ce champ est noté dans le fil.",
]),
("h", "2. Afficher le fil dans le formulaire"),
("code", """<form>
    <sheet>
        ...
    </sheet>
    <chatter/>
</form>""", "views/baobab_course_views.xml : ajoute la ligne &lt;chatter/&gt; juste après &lt;/sheet&gt;"),
("version", "<code>&lt;chatter/&gt;</code> s'écrit ainsi depuis Odoo 18. En Odoo 17 et avant, on écrivait <code>&lt;div class=\"oe_chatter\"&gt;</code> avec trois champs (<code>message_follower_ids</code>, <code>activity_ids</code>, <code>message_ids</code>). Tu le verras encore dans de vieux modules."),
("h", "3. Écrire dans le fil depuis le code"),
("code", """course.message_post(body=self.env._("Le client a appelé : livraison après 17 h."))
course.activity_schedule(
    "mail.mail_activity_data_todo",
    summary=self.env._("Course en retard"),
    note=self.env._("Appelle le livreur %s.", course.livreur_id.name or ""),
)""", "Poster un message, créer une activité"),
("p", "C'est exactement ce que fera l'action planifiée de la leçon suivante : sur une course en retard, l'activité « Course en retard » apparaît dans le fil, et l'utilisateur la voit dans son menu d'activités."),
("astuce", "Ne suis pas tout", "Mets <code>tracking=True</code> sur les champs importants pour le métier (statut, client, livreur), pas sur tous : un fil rempli de petits changements devient illisible."),
],
exercice=[
("p", "Ajoute l'héritage, <code>mail</code> dans les dépendances, <code>tracking=True</code> sur le statut, le client et le livreur, et la ligne <code>&lt;chatter/&gt;</code> dans le formulaire. Mets à jour. Démarre une course : le fil affiche le changement de statut. Écris un message, puis programme une activité « Appeler le client » pour demain."),
],
retenir=[
  "<code>_inherit = [\"mail.thread\", \"mail.activity.mixin\"]</code> + dépendance <code>mail</code>.",
  "<code>tracking=True</code> : historique automatique des changements du champ.",
  "<code>&lt;chatter/&gt;</code> dans le formulaire (Odoo 18 et suivants).",
  "<code>message_post</code> et <code>activity_schedule</code> pour écrire dans le fil depuis le code.",
]),
quiz=[
("Que faut-il pour que le changement de statut apparaisse dans le fil ?", [
  ("tracking=True sur le champ state, et le modèle qui hérite de mail.thread", V, "Oui."),
  ("Un message_post dans chaque action", F, "Possible, mais tracking=True le fait tout seul."),
  ("Rien, c'est automatique pour tous les champs", F, "Non : seulement pour les champs suivis."),
]),
("En Odoo 20, comment afficher le fil sous un formulaire ?", [
  ("<chatter/> après </sheet>", V, "Oui : depuis Odoo 18."),
  ("<div class=\"oe_chatter\"> avec trois champs", F, "C'était la forme d'Odoo 17 et avant."),
  ("Rien à faire", F, "Non : Odoo génère un formulaire sans fil si tu n'en écris pas."),
]),
("Ton module utilise mail.thread. Quelle dépendance ajouter au manifeste ?", [
  ("mail", V, "Oui."),
  ("web", F, "Non : mail.thread vient du module mail."),
  ("sale", F, "Non."),
]),
]),
]
