"""Bloc 4 — Section « Les API » (section 2747, cours 211).
Vérifié sur Odoo 20.0 le 28/11/2026 : appels JSON-2 avec une vraie clé d'API (curl et script Python, sorties
recopiées), ancien XML-RPC (avertissement du journal, service db supprimé), API de l'appli des livreurs testée avec curl
et par des tests HttpCase, webhook signé envoyé par un faux opérateur, e-mail « colis livré » généré (mail.mail)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

SCRIPT = """import os

import requests

ODOO = "http://localhost:8069"
CLE = os.environ["ODOO_CLE_API"]          # la clé n'est jamais écrite dans le code
ENTETES = {
    "Authorization": f"bearer {CLE}",
    "X-Odoo-Database": "baobab_dev",      # utile si le serveur a plusieurs bases
}


def appeler(modele, methode, **arguments):
    reponse = requests.post(f"{ODOO}/json/2/{modele}/{methode}", headers=ENTETES, json=arguments, timeout=10)
    reponse.raise_for_status()
    return reponse.json()


courses = appeler("baobab.course", "search_read",
                  domain=[("state", "in", ["brouillon", "en_route"])],
                  fields=["name", "zone_id", "prix", "state"])
for course in courses:
    print(course["name"], course["zone_id"][1], course["prix"], course["state"])"""

API_LIVREUR = """from odoo import http
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.http import request

CHAMPS_PUBLIES = ["name", "date_course", "state", "poids", "consigne"]


class ApiLivreur(http.Controller):
    \"\"\"API de l'appli des livreurs : chaque appel porte la clé d'API du livreur (portée « baobab_livreur »).\"\"\"

    def _course_en_json(self, course):
        valeurs = course.read(CHAMPS_PUBLIES)[0]
        valeurs["date_course"] = str(valeurs["date_course"])
        valeurs["zone"] = course.zone_id.name
        valeurs["client"] = course.client_id.name
        valeurs["adresse"] = course.client_id.contact_address or ""
        valeurs["telephone"] = course.client_id.phone or ""
        return valeurs

    @http.route("/api/livreur/courses", type="http", auth="bearer", bearer_scope="baobab_livreur",
                methods=["GET"], csrf=False)
    def mes_courses(self, **kw):
        # Pas de sudo() : les droits du livreur (ir.access) ne lui laissent voir que ses courses.
        courses = request.env["baobab.course"].search([("state", "in", ["brouillon", "en_route"])])
        return request.make_json_response([self._course_en_json(c) for c in courses])

    @http.route("/api/livreur/courses/<int:course_id>/livrer", type="http", auth="bearer",
                bearer_scope="baobab_livreur", methods=["POST"], csrf=False)
    def livrer(self, course_id, **kw):
        course = request.env["baobab.course"].browse(course_id)
        try:
            course.action_livrer()
        except (AccessError, MissingError):
            return request.make_json_response({"erreur": "Course introuvable."}, status=404)
        except UserError as erreur:
            return request.make_json_response({"erreur": str(erreur)}, status=409)
        return request.make_json_response(self._course_en_json(course))"""

PORTEE = """from odoo import fields, models


class ResUsersApikeysDescription(models.TransientModel):
    _inherit = "res.users.apikeys.description"

    # Une portée à part : une clé « Appli des livreurs » ne sert qu'à l'API /api/livreur/...
    scope = fields.Selection(selection_add=[("baobab_livreur", "Appli des livreurs")],
                             ondelete={"baobab_livreur": "cascade"})"""

WEBHOOK = """import hashlib
import hmac
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebhookPayDem(http.Controller):

    @http.route("/baobab/paiement/webhook", type="http", auth="public", methods=["POST"], csrf=False)
    def webhook(self, **kw):
        corps = request.httprequest.get_data()
        secret = request.env["ir.config_parameter"].sudo().get_str("baobab_paiement.secret")
        attendu = hmac.new(secret.encode(), corps, hashlib.sha256).hexdigest()
        recu = request.httprequest.headers.get("X-PayDem-Signature", "")
        # 1. Vérifier la signature AVANT de lire le contenu (compare_digest : comparaison sûre)
        if not secret or not hmac.compare_digest(attendu, recu):
            _logger.warning("Webhook PayDem refusé : signature invalide")
            return request.make_json_response({"erreur": "signature invalide"}, status=403)
        donnees = json.loads(corps)
        paiement = request.env["baobab.paiement"].sudo().search([("reference", "=", donnees.get("reference"))], limit=1)
        if not paiement:
            return request.make_json_response({"erreur": "paiement inconnu"}, status=404)
        # 2. Ne pas traiter deux fois le même avis
        traite = paiement._confirmer(donnees.get("statut"), donnees.get("id"))
        return request.make_json_response({"ok": True, "deja_traite": not traite})"""

APPEL_EXTERIEUR = """DELAIS = (3, 10)        # 3 s pour se connecter, 10 s pour recevoir la réponse

    def _envoyer_demande(self):
        \"\"\"Demande le paiement à l'opérateur. Ne lève jamais d'erreur : Odoo ne doit pas bloquer.\"\"\"
        url, base = self._parametres()
        for paiement in self:
            paiement.tentatives += 1
            try:
                reponse = requests.post(f"{url}/paiements", timeout=DELAIS, json={
                    "reference": paiement.reference,
                    "montant": paiement.montant,
                    "telephone": paiement.telephone,
                    "url_retour": f"{base}/baobab/paiement/webhook",
                })
            except requests.Timeout:
                paiement.erreur = self.env._("Le service de paiement ne répond pas (délai dépassé).")
                continue
            except requests.ConnectionError:
                paiement.erreur = self.env._("Le service de paiement est injoignable.")
                continue
            if reponse.status_code >= 400:
                paiement.write({"state": "echec", "erreur": reponse.json().get("message", reponse.text)})
                continue
            paiement.write({"reference_operateur": reponse.json()["id"], "erreur": False})"""

MODELE_MAIL = """<odoo noupdate="1">
    <record id="mail_template_course_livree" model="mail.template">
        <field name="name">Baobab : votre colis est livré</field>
        <field name="model_id" ref="model_baobab_course"/>
        <field name="subject">Votre colis {{ object.name }} est livré</field>
        <field name="email_from">{{ (object.company_id.email_formatted or user.email_formatted) }}</field>
        <field name="partner_to">{{ object.client_id.id }}</field>
        <field name="lang">{{ object.client_id.lang }}</field>
        <field name="body_html" type="html">
<div>
    <p>Bonjour <t t-out="object.client_id.name"/>,</p>
    <p>Votre colis <strong t-out="object.name"/> a été livré
       le <t t-out="format_datetime(object.date_livraison, dt_format='short')"/>
       par <t t-out="object.livreur_id.name or 'notre livreur'"/>.</p>
    <p>Merci de votre confiance,<br/>L'équipe Baobab Livraison</p>
</div>
        </field>
    </record>
</odoo>"""

LECONS = [
# ---------------------------------------------------------------- 4.1.1
dict(code="4.1.1", id=1361, seq=11, minutes=10,
titre="Les API d'Odoo : JSON-2 et les anciennes XML-RPC / JSON-RPC",
description="Quelle porte d'entrée choisir pour qu'un autre logiciel parle à Odoo, selon la version du client.",
html=fiche(
objectif="savoir par quelle « porte » un autre logiciel (une appli mobile, un site, un tableur) peut lire et écrire dans Odoo, selon la version.",
intro="L'appli des livreurs, le site d'une boutique, l'outil comptable d'un client : tous veulent parler à Odoo. Ils passent par une <b>API</b> (interface de programmation) : des adresses web qui répondent avec des données au lieu de pages.",
corps=[
("h", "Les trois API d'Odoo"),
("tableau", ["API", "Adresse", "Versions", "État en Odoo 20"], [
  ["<b>JSON-2</b>", "<code>POST /json/2/&lt;modèle&gt;/&lt;méthode&gt;</code>", "nouvelle en 19.0", "<b>la bonne</b> : clé d'API, réponses claires (codes HTTP)"],
  ["XML-RPC", "<code>/xmlrpc/2/common</code>, <code>/xmlrpc/2/object</code>", "depuis toujours", "fonctionne encore, <b>dépréciée</b>"],
  ["JSON-RPC", "<code>/jsonrpc</code>", "depuis longtemps", "fonctionne encore, <b>dépréciée</b>"],
]),
("p", "Essai réel d'un appel XML-RPC sur Odoo 20 : il marche, mais le journal d'Odoo écrit à chaque appel :"),
("code", """WARNING b3 odoo.addons.rpc.controllers.xmlrpc: The /xmlrpc, /xmlrpc/2 and /jsonrpc endpoints are deprecated
in Odoo 19 and scheduled for removal in Odoo 22. Please report the problem to the client making the request.""", "Journal d'Odoo 20"),
("version", "<b>Odoo 18</b> : seulement XML-RPC et JSON-RPC (login + mot de passe ou clé). <b>Odoo 19</b> : JSON-2 arrive, les anciennes sont dépréciées. <b>Odoo 20</b> : le service <code>db</code> (lister, créer, copier des bases par l'API) est supprimé : un appel répond <code>ValueError: Invalid service name: db</code> (vérifié). <b>Odoo 22</b> : suppression prévue de <code>/xmlrpc</code> et <code>/jsonrpc</code>. Chez un client en Odoo 17 ou 18, tu utiliseras encore XML-RPC ; pour tout nouveau projet sur 19+, JSON-2."),
("h", "Ce que l'API peut faire"),
("p", "Toutes les méthodes publiques des modèles : <code>search_read</code>, <code>create</code>, <code>write</code>, et aussi tes méthodes à toi (<code>action_demarrer</code>). Avec les <b>droits de l'utilisateur</b> à qui appartient la clé : pas plus. Une méthode dont le nom commence par <code>_</code> n'est jamais appelable de l'extérieur."),
("attention", "Un compte par logiciel", "Crée un utilisateur dédié pour chaque logiciel qui se connecte (« API boutique », « Appli livreurs »), avec les droits minimum. Jamais la clé de l'administrateur dans un logiciel tiers."),
],
exercice=[
("p", "Ton client a Odoo 17, un autre Odoo 20. Pour chacun, quelle API proposes-tu pour relier leur boutique en ligne, et pourquoi ? Puis, sur ta base, ouvre <code>/doc</code> (module <code>api_doc</code>, installé avec Odoo 20) et retrouve la méthode <code>search_read</code> du modèle <code>baobab.course</code>."),
],
retenir=[
  "Odoo 19+ : <b>JSON-2</b>, <code>POST /json/2/&lt;modèle&gt;/&lt;méthode&gt;</code> avec une clé d'API.",
  "XML-RPC et JSON-RPC : dépréciées, suppression prévue en Odoo 22.",
  "Odoo 20 : plus de service <code>db</code> par l'API.",
  "L'API agit avec les droits de l'utilisateur de la clé : un utilisateur dédié, droits minimum.",
]),
quiz=[
("Pour un nouveau projet sur Odoo 20, quelle API choisir ?", [
  ("JSON-2 (/json/2/<modèle>/<méthode>)", V, "Oui."),
  ("XML-RPC", F, "Elle marche encore, mais elle est dépréciée et sa suppression est prévue en Odoo 22."),
  ("Accéder directement à PostgreSQL", F, "Non : on contourne alors tous les droits et toutes les règles d'Odoo."),
]),
("Avec quels droits un appel API est-il exécuté ?", [
  ("Ceux de l'utilisateur à qui appartient la clé", V, "Oui : d'où un utilisateur dédié aux droits minimum."),
  ("Tous les droits, comme le super-utilisateur", F, "Non."),
  ("Aucun droit : seulement la lecture", F, "Non : il peut écrire s'il en a le droit."),
]),
("Peut-on appeler la méthode _cron_relancer_retards par l'API ?", [
  ("Non : une méthode qui commence par _ est privée", V, "Oui."),
  ("Oui, comme toute méthode", F, "Non."),
  ("Oui, seulement en XML-RPC", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 4.1.2
dict(code="4.1.2", id=2943, seq=12, minutes=10,
titre="Créer une clé d'API et faire un premier appel JSON-2",
description="Générer une clé d'API dans Odoo 20 et lire les courses depuis un script Python.",
html=fiche(
objectif="créer une clé d'API et lire les courses depuis un script Python, avec l'API JSON-2 d'Odoo 20.",
intro="Pour parler à Odoo de l'extérieur, il faut une <b>clé d'API</b> : une longue chaîne secrète qui remplace le mot de passe. Elle se crée en deux minutes.",
corps=[
("h", "1. Créer la clé"),
("liste", [
  "En haut à droite : ton avatar › <b>Préférences</b> (ou la fiche de l'utilisateur dédié) › onglet <b>Sécurité</b> › <b>Ajouter une clé API</b>.",
  "Donne-lui un nom clair (« Script de test »), choisis une durée (1 jour, 1 mois, 1 an).",
  "Odoo affiche la clé <b>une seule fois</b>. Copie-la dans un gestionnaire de mots de passe ou une variable d'environnement, jamais dans un fichier du dépôt Git.",
]),
("version", "En Odoo 20, la clé d'un utilisateur qui n'est pas administrateur <b>expire forcément</b> : sans date, Odoo refuse (« The API key must have an expiration date ») ; la durée maximale dépend de ses groupes (1 jour par défaut ; on la règle avec le champ <code>api_key_duration</code> du groupe). Vérifié : avec 90 jours autorisés, une clé de 120 jours est refusée (« You cannot exceed 90.0 days. »)."),
("h", "2. Un premier appel avec curl"),
("code", """curl -X POST http://localhost:8069/json/2/baobab.course/search_read \\
     -H "Authorization: bearer $ODOO_CLE_API" \\
     -H "Content-Type: application/json" \\
     -d '{"domain": [["poids", ">", 5]], "fields": ["name", "prix", "state"]}'""", "Terminal"),
("code", """[{"id": 2, "name": "BL/2026/0002", "prix": 4400.0, "state": "en_route"}]""", "Réponse réelle"),
("p", "Les arguments de la méthode sont envoyés <b>par leur nom</b>, en JSON : <code>domain</code>, <code>fields</code>, <code>limit</code>… Une mauvaise clé répond <code>401</code> avec <code>\"message\": \"Invalid apikey\"</code>."),
("h", "3. Le même appel en Python"),
("code", SCRIPT, "lire_courses.py"),
("code", """export ODOO_CLE_API='…la clé…'
python3 lire_courses.py
BL/2026/0015 Plateau 1000.0 brouillon
BL/2026/0013 Plateau 1000.0 brouillon
BL/2026/0002 Rufisque 4400.0 en_route
BL/2026/0001 Mermoz 1500.0 en_route""", "Terminal : résultat réel sur la base de test"),
("astuce", "Plusieurs bases sur le serveur", "Si le serveur héberge plusieurs bases, l'en-tête <code>X-Odoo-Database</code> dit laquelle utiliser."),
],
exercice=[
("p", "Crée une clé d'API (1 jour), mets-la dans la variable <code>ODOO_CLE_API</code>, et lance le script. Modifie-le pour afficher seulement les courses de la zone Mermoz, triées par prix (<code>order=\"prix desc\"</code>). Puis lance-le avec une clé fausse et lis l'erreur."),
],
retenir=[
  "Clé d'API : Préférences › Sécurité › Ajouter une clé API ; affichée une seule fois.",
  "<code>POST /json/2/&lt;modèle&gt;/&lt;méthode&gt;</code>, en-tête <code>Authorization: bearer &lt;clé&gt;</code>, arguments en JSON par leur nom.",
  "Odoo 20 : une clé non-administrateur expire toujours.",
  "La clé va dans une variable d'environnement, jamais dans le code.",
]),
quiz=[
("Comment s'authentifie un appel JSON-2 ?", [
  ("En-tête Authorization: bearer <clé d'API>", V, "Oui."),
  ("Login et mot de passe dans l'adresse", F, "Jamais : l'adresse se retrouve dans les journaux."),
  ("Un cookie de session", F, "Non : JSON-2 est fait pour les programmes, sans session."),
]),
("Où garder la clé d'API utilisée par ton script ?", [
  ("Dans une variable d'environnement ou un gestionnaire de secrets", V, "Oui."),
  ("En dur dans le script, committé dans Git", F, "Jamais : quiconque lit le dépôt aurait accès à Odoo."),
  ("Dans le nom du fichier", F, "Non."),
]),
("Un livreur (non administrateur) crée une clé sans date d'expiration. Que fait Odoo 20 ?", [
  ("Il refuse : la clé doit avoir une date d'expiration", V, "Oui (vérifié)."),
  ("Il l'accepte pour toujours", F, "Seul un administrateur peut créer une clé sans fin."),
  ("Il met 1 an", F, "Non : il refuse."),
]),
]),

# ---------------------------------------------------------------- 4.1.3
dict(code="4.1.3", id=2945, seq=13, minutes=10,
titre="Créer et modifier des données depuis l'extérieur",
description="Créer une course, la modifier et appeler une action depuis un autre logiciel, et gérer les refus.",
html=fiche(
objectif="créer et modifier des courses depuis un autre logiciel, et comprendre les réponses d'Odoo quand c'est refusé.",
intro="La boutique d'Awa Diop veut créer ses courses elle-même depuis son site. Avec JSON-2, on appelle <code>create</code>, <code>write</code> ou une action, exactement comme dans le terminal d'Odoo.",
corps=[
("code", """nouvelle = appeler("baobab.course", "create",
                   vals_list=[{"client_id": 3, "zone_id": 1, "poids": 2.5, "consigne": "Créée par l'API"}])
print("Créée :", nouvelle)
try:
    appeler("baobab.course", "action_demarrer", ids=nouvelle)
except requests.HTTPError as erreur:
    print("Refusé :", erreur.response.status_code, erreur.response.json()["message"])""", "Suite de lire_courses.py"),
("code", """Créée : [16]
Refusé : 422 Choisis un livreur avant de démarrer la course BL/2026/0016.""", "Résultat réel"),
("tableau", ["Appel", "Arguments JSON", "Réponse"], [
  ["<code>create</code>", "<code>{\"vals_list\": [{…}, {…}]}</code>", "la liste des id créés : <code>[16]</code>"],
  ["<code>write</code>", "<code>{\"ids\": [2], \"vals\": {\"consigne\": \"Appeler avant\"}}</code>", "<code>true</code>"],
  ["une action", "<code>{\"ids\": [16]}</code>", "ce que renvoie la méthode"],
]),
("h", "Lire les codes de réponse"),
("tableau", ["Code", "Signification"], [
  ["200", "tout va bien"],
  ["401", "clé absente, fausse ou expirée"],
  ["403", "droits insuffisants (AccessError)"],
  ["404", "modèle, méthode ou fiche introuvable"],
  ["422", "règle métier refusée (UserError, ValidationError) : le message explique pourquoi"],
]),
("p", "Toutes les règles du Bloc 2 s'appliquent : la référence BL/… est donnée par la séquence, le prix est calculé, les contraintes et les vérifications des actions protègent la base. C'est pour cela qu'on passe par l'API et jamais directement par PostgreSQL."),
("attention", "Les id ne sont pas les mêmes partout", "<code>\"client_id\": 3</code> vaut pour <b>ta</b> base. Dans la vraie intégration, cherche d'abord l'id (par exemple le client par son e-mail avec <code>search_read</code>), ne l'écris jamais en dur."),
],
exercice=[
("p", "Écris un script qui lit un petit fichier CSV de commandes (client, zone, poids) et crée les courses par l'API : il cherche l'id du client par son nom et celui de la zone par son nom, puis crée la course. Affiche les références obtenues. Essaie une zone qui n'existe pas : ton script doit le dire clairement."),
],
retenir=[
  "<code>create</code> prend <code>vals_list</code> ; <code>write</code> prend <code>ids</code> et <code>vals</code>.",
  "200 ok · 401 clé · 403 droits · 404 introuvable · 422 règle métier.",
  "L'API respecte toutes les règles du module (séquence, calculs, contraintes).",
  "Chercher les id, ne jamais les écrire en dur.",
]),
quiz=[
("Que renvoie un appel JSON-2 à create ?", [
  ("La liste des id créés, par exemple [16]", V, "Oui."),
  ("La fiche complète", F, "Non : il faut un search_read ou un read ensuite."),
  ("true", F, "Non : c'est la réponse de write."),
]),
("Une action refuse avec UserError. Quel code HTTP reçoit le logiciel ?", [
  ("422", V, "Oui (vérifié), avec le message de l'erreur."),
  ("200", F, "Non."),
  ("500", F, "Non : ce n'est pas un plantage, c'est une règle métier."),
]),
("Pourquoi passer par l'API plutôt que d'écrire directement dans PostgreSQL ?", [
  ("Pour que les règles d'Odoo s'appliquent : droits, séquence, calculs, contraintes", V, "Oui."),
  ("Parce que PostgreSQL est lent", F, "Non."),
  ("C'est pareil", F, "Non : en SQL direct, aucune règle d'Odoo ne s'applique."),
]),
]),

# ---------------------------------------------------------------- 4.1.4
dict(code="4.1.4", id=2748, seq=14, minutes=10,
titre="Créer ses propres adresses web (contrôleurs HTTP)",
description="L'API de l'appli des livreurs : des adresses simples, protégées par une clé d'API à portée limitée.",
html=fiche(
objectif="créer une petite API sur mesure pour l'appli des livreurs, protégée par une clé d'API à portée limitée.",
intro="L'appli des livreurs a besoin de deux choses : « mes courses du jour » et « j'ai livré ». Plutôt que de lui ouvrir tout JSON-2, on lui écrit deux adresses sur mesure, qui ne renvoient que l'utile.",
corps=[
("code", API_LIVREUR, "baobab_livraison/controllers/api_livreur.py"),
("tableau", ["Paramètre", "Rôle"], [
  ["<code>auth=\"bearer\"</code>", "l'appel doit porter une clé d'API (en-tête <code>Authorization: bearer …</code>)"],
  ["<code>bearer_scope=\"baobab_livreur\"</code>", "seule une clé de cette <b>portée</b> est acceptée (obligatoire avec <code>auth=\"bearer\"</code>)"],
  ["<code>methods=[\"GET\"]</code>", "la méthode HTTP acceptée"],
  ["<code>csrf=False</code>", "indispensable pour un POST qui vient d'une appli : sinon <code>400 Session expired (invalid CSRF token)</code> (vérifié)"],
  ["<code>request.make_json_response(…, status=…)</code>", "répondre en JSON avec le bon code"],
]),
("h", "Une portée à part pour les clés des livreurs"),
("code", PORTEE, "baobab_livraison/models/res_users_apikeys.py"),
("p", "Le livreur crée sa clé en choisissant la portée « Appli des livreurs ». Vérifié : cette clé ouvre <code>/api/livreur/…</code> mais <b>pas</b> JSON-2 (401), et une clé JSON-2 (« RPC ») n'ouvre pas l'API des livreurs (401). Si le téléphone est perdu, la clé ne donne accès qu'aux courses du livreur."),
("code", """$ curl http://localhost:8069/api/livreur/courses -H "Authorization: bearer $CLE_IBOU"
[{"id": 1, "name": "BL/2026/0001", "date_course": "2026-11-28", "state": "brouillon", "poids": 3.5, "consigne": false, "zone": "Mermoz", "client": "Awa Diop", "adresse": "Dakar", "telephone": ""}]
$ curl -X POST http://localhost:8069/api/livreur/courses/2/livrer -H "Authorization: bearer $CLE_IBOU"
{"erreur": "Course introuvable."}""", "Réponses réelles (la course 2 n'est pas à Ibou)"),
("version", "<code>auth=\"bearer\"</code> et <code>bearer_scope</code> sont récents (Odoo 19+). En Odoo 18, on écrivait <code>auth=\"user\"</code> avec une session, ou on vérifiait un jeton à la main. Depuis Odoo 19, <code>type=\"json\"</code> s'écrit <code>type=\"jsonrpc\"</code> (l'ancien nom est un alias déprécié)."),
("attention", "Pas de sudo() dans une API", "Le contrôleur cherche les courses <b>avec les droits du livreur</b> : c'est la règle d'accès (leçon 4.3.3) qui ne lui laisse voir que les siennes. Avec <code>sudo()</code>, n'importe quel livreur verrait toutes les courses, adresses et téléphones des clients compris."),
],
exercice=[
("p", "Ajoute les deux adresses et la portée. Crée une clé « Appli des livreurs » pour Ibou, puis teste avec curl : la liste, une livraison réussie, une course qui n'est pas à lui. Ajoute ensuite une troisième adresse <code>POST /api/livreur/courses/&lt;id&gt;/demarrer</code>."),
],
retenir=[
  "Une API sur mesure = un contrôleur <code>type=\"http\"</code> qui répond avec <code>make_json_response</code>.",
  "<code>auth=\"bearer\"</code> + <code>bearer_scope</code> : clé d'API à portée limitée.",
  "<code>csrf=False</code> pour les POST venant d'une appli.",
  "Jamais <code>sudo()</code> : les droits de l'utilisateur filtrent.",
]),
quiz=[
("Avec auth=\"bearer\", quel paramètre est obligatoire en Odoo 20 ?", [
  ("bearer_scope", V, "Oui : la portée des clés acceptées."),
  ("website=True", F, "Non."),
  ("sitemap=False", F, "Non."),
]),
("L'appli envoie un POST et reçoit « 400 Session expired (invalid CSRF token) ». Que manque-t-il ?", [
  ("csrf=False sur la route", V, "Oui : la protection CSRF vise les formulaires web, pas les applis avec clé."),
  ("Une clé plus longue", F, "Non."),
  ("methods=[\"GET\"]", F, "Non : livrer modifie des données, c'est un POST."),
]),
("Pourquoi une portée « Appli des livreurs » plutôt qu'une clé RPC classique ?", [
  ("Une clé volée n'ouvre que l'API des livreurs, pas toute l'API JSON-2", V, "Oui (vérifié : 401 sur JSON-2)."),
  ("Elle n'expire jamais", F, "Non : elle expire comme les autres."),
  ("C'est obligatoire pour les POST", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 4.1.5
dict(code="4.1.5", id=2948, seq=15, minutes=10,
titre="Recevoir un webhook",
description="Recevoir l'avis d'un service extérieur : vérifier la signature, ne pas traiter deux fois le même avis.",
html=fiche(
objectif="recevoir un avis (webhook) envoyé par un service extérieur, en vérifiant qu'il vient bien de lui et sans le traiter deux fois.",
intro="Quand le client paie sur son téléphone, l'opérateur de paiement prévient Odoo en appelant une de ses adresses : c'est un <b>webhook</b>. Mais cette adresse est publique : n'importe qui peut l'appeler et prétendre « la course est payée ». Deux protections sont indispensables.",
corps=[
("code", WEBHOOK, "baobab_livraison_paiement/controllers/webhook.py"),
("h", "Protection 1 : la signature"),
("p", "L'opérateur et Odoo partagent un <b>secret</b>. L'opérateur calcule une empreinte (HMAC SHA-256) du contenu avec ce secret et l'envoie dans un en-tête. Odoo refait le calcul : si les deux empreintes diffèrent, le message est faux ou modifié → <code>403</code>. <code>hmac.compare_digest</code> compare sans laisser deviner l'empreinte par le temps de réponse."),
("p", "Le secret est un <b>paramètre système</b> (<code>baobab_paiement.secret</code>, lu avec <code>get_str</code>), saisi par l'administrateur : jamais dans le code ni dans les données du module."),
("h", "Protection 2 : ne pas traiter deux fois"),
("p", "Les opérateurs renvoient souvent le même avis (réseau lent, pas de réponse à temps). Notre faux opérateur l'envoie exprès deux fois. Résultat réel :"),
("code", """webhook -> 200 {"ok": true, "deja_traite": false}
webhook -> 200 {"ok": true, "deja_traite": true}""", "Journal du faux opérateur PayDem"),
("p", "La méthode <code>_confirmer</code> ne fait rien si le paiement n'est plus « en attente », et une contrainte <code>UNIQUE(reference_operateur)</code> empêche d'enregistrer deux fois le même paiement : un seul message « Paiement mobile reçu » dans le fil (vérifié par un test)."),
("version", "<code>auth=\"public\"</code> + <code>csrf=False</code> + <code>sudo()</code> est le schéma habituel d'un webhook, dans toutes les versions. En Odoo 20, la lecture des paramètres système s'écrit <code>get_str</code> / <code>get_int</code> (avant : <code>get_param</code>)."),
("attention", "Répondre vite", "Un webhook doit répondre en quelques secondes, sinon l'opérateur renvoie. Ne fais pas de long traitement dedans : enregistre l'information et laisse une action planifiée faire le reste si besoin."),
],
exercice=[
("p", "Ajoute le webhook. Dans le terminal, calcule une signature avec Python (<code>hmac.new(secret, corps, hashlib.sha256).hexdigest()</code>) et envoie l'avis avec curl : vérifie le passage à « Payé ». Puis modifie un caractère du corps sans changer la signature : tu dois recevoir 403. Renvoie le bon avis : <code>deja_traite</code> doit valoir <code>true</code>."),
],
retenir=[
  "Webhook = une adresse publique (<code>auth=\"public\"</code>, <code>csrf=False</code>) appelée par un service.",
  "Toujours vérifier la signature HMAC avec <code>hmac.compare_digest</code>, avant tout.",
  "Toujours prévoir les doublons : état + contrainte UNIQUE.",
  "Le secret dans les paramètres système, jamais dans le code.",
]),
quiz=[
("Pourquoi vérifier la signature d'un webhook ?", [
  ("Parce que l'adresse est publique : n'importe qui pourrait prétendre qu'une course est payée", V, "Oui."),
  ("Pour aller plus vite", F, "Non."),
  ("C'est facultatif si on utilise HTTPS", F, "Non : HTTPS chiffre, il ne prouve pas qui envoie."),
]),
("Le même avis de paiement arrive deux fois. Que doit faire Odoo ?", [
  ("Le traiter une seule fois, et répondre 200 à la deuxième", V, "Oui : sinon l'opérateur renverrait encore."),
  ("Enregistrer deux paiements", F, "Surtout pas."),
  ("Répondre 500 à la deuxième", F, "Non : l'opérateur réessaierait sans fin."),
]),
("Où mettre le secret partagé avec l'opérateur ?", [
  ("Dans un paramètre système saisi par l'administrateur", V, "Oui."),
  ("Dans le code du contrôleur", F, "Non : il serait dans Git."),
  ("Dans un fichier de données XML du module", F, "Non : il serait aussi dans Git."),
]),
]),

# ---------------------------------------------------------------- 4.1.6
dict(code="4.1.6", id=2749, seq=16, minutes=10,
titre="Appeler un service extérieur : délais, erreurs, nouvelles tentatives",
description="Appeler une API extérieure depuis Odoo sans jamais bloquer les utilisateurs quand elle est en panne.",
html=fiche(
objectif="appeler un service extérieur depuis Odoo sans bloquer les utilisateurs quand ce service est lent ou en panne.",
intro="Pour demander un paiement, Odoo appelle l'opérateur. Mais le réseau coupe, l'opérateur est lent, un numéro est refusé. Le code doit prévoir chaque cas, sinon le bouton « Demander le paiement » tourne sans fin, ou plante devant le client.",
corps=[
("code", APPEL_EXTERIEUR, "baobab_livraison_paiement/models/paiement.py (extrait)"),
("h", "Les quatre règles"),
("liste", [
  "<b>Toujours un délai</b> : <code>timeout=(3, 10)</code>. Sans lui, <code>requests</code> attend sans fin et bloque un processus d'Odoo.",
  "<b>Attraper les erreurs réseau</b> : <code>requests.Timeout</code>, <code>requests.ConnectionError</code>. On note l'erreur sur la fiche, on ne plante pas.",
  "<b>Distinguer « refusé » et « pas de réponse »</b> : un 400 (numéro refusé) est définitif ; un délai dépassé se retente plus tard.",
  "<b>Retenter plus tard, pas tout de suite</b> : une action planifiée reprend les paiements en attente (leçon 4.2.3), avec un nombre maximum d'essais.",
]),
("h", "Résultats réels avec le faux opérateur PayDem"),
("tableau", ["Téléphone", "Comportement de PayDem", "Résultat dans Odoo", "Durée du clic"], [
  ["+221 77 123 45 67", "accepte", "en attente, référence PD-1, puis « Payé » au webhook", "0,0 s"],
  ["… 0000", "refuse (400)", "Échec : « Numéro refusé par l'opérateur »", "0,0 s"],
  ["… 9999", "ne répond pas", "en attente : « Le service de paiement ne répond pas (délai dépassé). »", "10,0 s (le délai)"],
]),
("attention", "Jamais d'adresse ni de clé en dur", "L'adresse de l'opérateur (<code>baobab_paiement.url</code>) et ses secrets sont des paramètres système. Ainsi la même version du module marche en test (faux opérateur) et en production (vrai opérateur)."),
("astuce", "Tester sans réseau", "Dans un test, on remplace <code>requests.post</code> par un faux avec <code>unittest.mock.patch(…, side_effect=requests.Timeout)</code> : on vérifie le comportement en cas de panne sans dépendre d'Internet."),
],
exercice=[
("p", "Lance le faux opérateur (<code>PAYDEM_SECRET=… python3 outils/faux_paydem.py</code>), règle les deux paramètres système, puis demande le paiement pour trois clients aux numéros finissant par 4567, 0000 et 9999. Note le résultat et la durée. Écris ensuite le test qui simule une panne avec <code>patch</code>."),
],
retenir=[
  "Toujours <code>timeout=</code> sur un appel extérieur.",
  "Attraper <code>Timeout</code> et <code>ConnectionError</code> ; noter l'erreur sur la fiche.",
  "Refus définitif ≠ panne passagère : seule la panne se retente.",
  "Adresse et secrets dans les paramètres système ; tests avec <code>mock.patch</code>.",
]),
quiz=[
("Que se passe-t-il avec requests.post(url, json=…) sans timeout, si le service ne répond plus ?", [
  ("Odoo attend sans fin et bloque l'utilisateur", V, "Oui : toujours un timeout."),
  ("requests abandonne après 10 secondes", F, "Non : sans timeout, il n'y a pas de limite."),
  ("Odoo réessaie tout seul", F, "Non."),
]),
("Le service répond 400 « Numéro refusé ». Faut-il retenter plus tard ?", [
  ("Non : c'est un refus définitif, on marque le paiement en échec", V, "Oui."),
  ("Oui, toutes les 10 minutes", F, "Non : la réponse ne changera pas."),
  ("Oui, tout de suite en boucle", F, "Jamais en boucle."),
]),
("Comment tester le cas « service en panne » sans couper le réseau ?", [
  ("unittest.mock.patch sur requests.post avec side_effect=requests.Timeout", V, "Oui."),
  ("Débrancher le câble pendant le test", F, "Non : un test doit tourner tout seul."),
  ("Ce n'est pas testable", F, "Si."),
]),
]),

# ---------------------------------------------------------------- 4.1.7
dict(code="4.1.7", id=2950, seq=17, minutes=10,
titre="Envoyer des e-mails automatiques",
description="Un modèle d'e-mail « Votre colis est livré », envoyé au client dès la livraison.",
html=fiche(
objectif="envoyer automatiquement au client l'e-mail « Votre colis est livré », avec un modèle d'e-mail.",
intro="Quand le livreur marque une course livrée, le client doit être prévenu. Odoo a pour cela les <b>modèles d'e-mail</b> (<code>mail.template</code>) : un sujet et un texte avec des trous à remplir.",
corps=[
("code", MODELE_MAIL, "baobab_livraison/data/mail_template_data.xml"),
("liste", [
  "<code>{{ … }}</code> : une valeur dans le sujet ou les destinataires.",
  "Le corps est du QWeb : <code>t-out</code>, <code>t-if</code>… <code>object</code> est la course.",
  "<code>partner_to</code> : le destinataire (le client) ; <code>lang</code> : l'e-mail part dans sa langue.",
  "<code>noupdate=\"1\"</code> : l'entreprise peut retoucher le texte, une mise à jour ne l'écrasera pas.",
]),
("h", "L'envoyer à la livraison"),
("code", """modele = self.env.ref("baobab_livraison.mail_template_course_livree", raise_if_not_found=False)
for course in self.filtered("client_id.email"):
    course.message_post_with_source(
        modele, message_type="comment", subtype_xmlid="mail.mt_comment",
        partner_ids=course.client_id.ids,
    )""", "Dans action_livrer, après le write"),
("p", "<code>message_post_with_source</code> écrit le message dans le fil de la course <b>et</b> l'envoie par e-mail aux <code>partner_ids</code>. Résultat réel : un e-mail « Votre colis BL/2026/0001 est livré » adressé à awa.diop@exemple.sn, avec « Bonjour Awa Diop, Votre colis BL/2026/0001 a été livré le … par Ibou Fall »."),
("attention", "En développement, l'e-mail reste « en échec »", "Sans serveur d'envoi, Odoo crée l'e-mail mais ne peut pas l'envoyer : il apparaît avec l'état « Échec » dans Paramètres › Technique › E-mails (mode développeur). C'est normal sur ta machine. En production, on configure un serveur d'envoi (Paramètres › Serveurs de messagerie sortants). Et sur une <b>copie</b> de la base d'un client, on neutralise toujours les envois (leçon 4.3.6)."),
("version", "<code>message_post_with_source</code> existe depuis Odoo 17 (avant : <code>message_post_with_template</code>). La syntaxe <code>{{ … }}</code> dans les champs simples et QWeb dans le corps est celle d'Odoo 15 et suivants."),
],
exercice=[
("p", "Ajoute le modèle d'e-mail et l'envoi dans <code>action_livrer</code>. Donne un e-mail à Awa Diop, livre une course, puis regarde : le message dans le fil de la course, et l'e-mail dans Paramètres › Technique › E-mails. Ouvre le modèle (Paramètres › Technique › Modèles d'e-mail) et change le texte depuis l'écran."),
],
retenir=[
  "Modèle d'e-mail = <code>mail.template</code> : sujet, destinataires et corps QWeb.",
  "<code>message_post_with_source(modele, partner_ids=…)</code> : dans le fil et par e-mail.",
  "<code>noupdate=\"1\"</code> pour que l'entreprise puisse modifier le texte.",
  "Sans serveur d'envoi, l'e-mail est créé mais reste en échec.",
]),
quiz=[
("Dans un modèle d'e-mail, comment écrire la référence de la course dans le sujet ?", [
  ("Votre colis {{ object.name }} est livré", V, "Oui."),
  ("Votre colis <t t-out=\"object.name\"/> est livré", F, "Non : t-out sert dans le corps, pas dans le sujet."),
  ("Votre colis %s est livré", F, "Non."),
]),
("Sur ta machine, l'e-mail apparaît « en échec ». Pourquoi ?", [
  ("Aucun serveur d'envoi n'est configuré : c'est normal en développement", V, "Oui."),
  ("Le modèle est faux", F, "Le message a bien été créé : c'est l'envoi qui échoue."),
  ("Le client n'existe pas", F, "Non."),
]),
("Pourquoi noupdate=\"1\" sur le modèle d'e-mail ?", [
  ("Pour que les retouches de l'entreprise ne soient pas écrasées par une mise à jour", V, "Oui."),
  ("Pour que l'e-mail ne parte jamais", F, "Non."),
  ("Pour l'envoyer une seule fois", F, "Non."),
]),
]),
]
