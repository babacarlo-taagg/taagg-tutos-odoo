"""Bloc 4 — Section « Le paiement mobile » (section 2750, cours 211).
Vérifié sur Odoo 20.0 le 28/11/2026 avec le faux opérateur PayDem (fictif, fichier faux_paydem.py de ce dossier) :
paiement accepté puis confirmé par webhook (envoyé deux fois, traité une fois), numéro refusé, délai dépassé, avis jamais
reçu puis rattrapé par le rapprochement ; 4 tests verts. Aucun opérateur réel n'est nommé ni utilisé."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

with open(os.path.join(os.path.dirname(__file__), "faux_paydem.py"), encoding="utf-8") as f:
    FAUX_PAYDEM = f.read().strip()

MODELE = """class BaobabPaiement(models.Model):
    _name = "baobab.paiement"
    _description = "Paiement mobile d'une course"
    _order = "id desc"

    course_id = fields.Many2one("baobab.course", required=True, ondelete="cascade", index=True)
    currency_id = fields.Many2one(related="course_id.currency_id")
    montant = fields.Monetary(required=True, currency_field="currency_id")
    telephone = fields.Char(required=True)
    reference = fields.Char(required=True, readonly=True, copy=False,
                            default=lambda self: uuid.uuid4().hex)
    reference_operateur = fields.Char(readonly=True, copy=False)
    state = fields.Selection([("en_attente", "En attente"), ("paye", "Payé"), ("echec", "Échec")],
                             default="en_attente", required=True, readonly=True)
    tentatives = fields.Integer(readonly=True)
    erreur = fields.Char(readonly=True)

    _reference_unique = models.Constraint("UNIQUE(reference)", "Cette référence de paiement existe déjà.")
    _operateur_unique = models.Constraint("UNIQUE(reference_operateur)", "Ce paiement de l'opérateur est déjà enregistré.")

    def _confirmer(self, statut, reference_operateur):
        \"\"\"Appelé par le webhook ou le rapprochement. Renvoie False si c'était déjà traité.\"\"\"
        self.ensure_one()
        if self.state != "en_attente":
            return False                      # doublon : on ne paie pas deux fois
        if statut == "reussi":
            self.write({"state": "paye", "reference_operateur": reference_operateur, "erreur": False})
            self.course_id.message_post(body=self.env._("Paiement mobile reçu : %s", reference_operateur))
        else:
            self.write({"state": "echec", "erreur": self.env._("Paiement refusé par l'opérateur.")})
        return True"""

BOUTON = """class BaobabCourse(models.Model):
    _inherit = "baobab.course"

    paiement_ids = fields.One2many("baobab.paiement", "course_id", string="Paiements")
    est_payee = fields.Boolean("Payée", compute="_compute_est_payee", store=True)

    @api.depends("paiement_ids.state")
    def _compute_est_payee(self):
        for course in self:
            course.est_payee = any(p.state == "paye" for p in course.paiement_ids)

    def action_demander_paiement(self):
        self.ensure_one()
        if self.est_payee:
            raise UserError(self.env._("Cette course est déjà payée."))
        if not self.client_id.phone:
            raise UserError(self.env._("Ajoute le téléphone du client pour le paiement mobile."))
        if self.paiement_ids.filtered(lambda p: p.state == "en_attente"):
            raise UserError(self.env._("Un paiement est déjà en attente pour cette course."))
        paiement = self.env["baobab.paiement"].create({
            "course_id": self.id, "montant": self.prix, "telephone": self.client_id.phone,
        })
        paiement._envoyer_demande()
        return True"""

RAPPROCHEMENT = """@api.model
def _cron_rapprocher(self):
    \"\"\"Toutes les 10 minutes : relancer ou vérifier les paiements restés en attente.\"\"\"
    url, _base = self._parametres()
    limite = fields.Datetime.now() - timedelta(minutes=10)
    for paiement in self.search([("state", "=", "en_attente"), ("write_date", "<", limite)]):
        if not paiement.reference_operateur:
            if paiement.tentatives >= TENTATIVES_MAX:
                paiement.write({"state": "echec", "erreur": self.env._("Service injoignable après plusieurs essais.")})
            else:
                paiement._envoyer_demande()
            continue
        try:
            reponse = requests.get(f"{url}/paiements/{paiement.reference_operateur}", timeout=DELAIS)
            reponse.raise_for_status()
        except requests.RequestException as erreur:
            _logger.warning("Rapprochement impossible pour %s : %s", paiement.reference, erreur)
            continue
        statut = reponse.json()["statut"]
        if statut != "en_attente":
            paiement._confirmer(statut, paiement.reference_operateur)"""

LECONS = [
# ---------------------------------------------------------------- 4.2.1
dict(code="4.2.1", id=1363, seq=21, minutes=10,
titre="Comment marche un paiement mobile",
description="Demande, validation sur le téléphone, notification, rapprochement, remboursement : le parcours complet.",
html=fiche(
objectif="comprendre le parcours d'un paiement mobile, de la demande à la confirmation, avant d'écrire la moindre ligne.",
intro="En Afrique de l'Ouest, les clients de Baobab paient surtout par paiement mobile, avec leur téléphone. Pour un développeur, ce n'est pas « un bouton payer » : c'est une conversation en plusieurs étapes avec un opérateur, où chaque étape peut échouer.",
corps=[
("h", "Le parcours"),
("tableau", ["Étape", "Qui", "Ce qui se passe"], [
  ["1. Demande", "Odoo → opérateur", "Odoo envoie : montant, téléphone, sa référence unique, l'adresse où être prévenu. L'opérateur répond tout de suite « reçu, en attente » avec <b>sa</b> référence (PD-1)."],
  ["2. Validation", "client", "Le client reçoit une demande sur son téléphone et la valide avec son code secret. Odoo ne voit rien de cette étape."],
  ["3. Notification", "opérateur → Odoo", "L'opérateur appelle le webhook d'Odoo : « PD-1 réussi » (ou « échoué »), signé."],
  ["4. Rapprochement", "Odoo → opérateur", "Pour les paiements restés en attente (avis perdu), Odoo demande lui-même l'état à l'opérateur."],
  ["5. Remboursement", "Odoo → opérateur", "Une demande à part, avec sa propre référence, qui suit le même parcours."],
]),
("h", "Ce que le développeur doit garantir"),
("liste", [
  "<b>Jamais de double paiement</b> : une référence unique par demande, et un avis traité une seule fois.",
  "<b>Jamais de course payée sans preuve</b> : seul un avis signé ou une réponse de l'opérateur peut passer un paiement à « Payé ».",
  "<b>Jamais d'Odoo bloqué</b> : des délais courts, et les cas « pas de réponse » repris plus tard.",
  "<b>Une trace de tout</b> : chaque tentative, chaque erreur, chaque avis est noté sur la fiche du paiement.",
]),
("attention", "Les vrais opérateurs", "Chaque opérateur a son API, sa documentation, ses comptes de test et un contrat. Ce cours utilise un <b>faux opérateur, PayDem</b>, inventé pour s'entraîner : les principes (référence, signature, doublons, rapprochement) sont les mêmes partout. Pour un vrai projet, on lit la documentation de l'opérateur et on travaille d'abord dans son environnement de test, jamais avec de l'argent réel."),
("version", "Odoo a son propre cadre de paiement en ligne (module <code>payment</code> et ses fournisseurs), utilisé par le site et la facturation. Il convient quand l'opérateur y est déjà intégré. Pour un parcours métier simple comme le nôtre, un petit modèle dédié est plus facile à comprendre et à tester : c'est ce qu'on fait ici."),
],
exercice=[
("p", "Dessine sur papier le parcours d'un paiement de 1 500 F pour la course BL/2026/0001, avec les flèches entre Odoo, l'opérateur et le téléphone du client. Puis, pour chaque flèche, écris ce qui se passe si le message se perd. Garde ce dessin : la leçon 4.2.3 y répond."),
],
retenir=[
  "Demande → validation sur le téléphone → avis (webhook) → rapprochement si l'avis manque.",
  "Deux références : celle d'Odoo (unique) et celle de l'opérateur.",
  "Jamais de double paiement, jamais de « payé » sans preuve, jamais d'Odoo bloqué.",
  "On s'entraîne avec un faux opérateur, jamais avec de l'argent réel.",
]),
quiz=[
("Après la demande, l'opérateur répond « en attente ». Odoo peut-il marquer la course payée ?", [
  ("Non : il faut attendre l'avis signé ou vérifier auprès de l'opérateur", V, "Oui."),
  ("Oui, la demande est acceptée", F, "Non : le client n'a peut-être pas validé."),
  ("Oui, après 5 minutes", F, "Non : le temps ne prouve rien."),
]),
("À quoi sert la référence unique envoyée par Odoo ?", [
  ("À relier l'avis de l'opérateur au bon paiement, sans doublon", V, "Oui."),
  ("À afficher le prix", F, "Non."),
  ("À rien, l'opérateur a sa propre référence", F, "Les deux servent."),
]),
("L'avis de paiement n'arrive jamais. Que prévoit le parcours ?", [
  ("Le rapprochement : Odoo demande lui-même l'état à l'opérateur", V, "Oui."),
  ("Marquer payé par défaut", F, "Surtout pas."),
  ("Demander un nouveau paiement au client", F, "Il risquerait de payer deux fois."),
]),
]),

# ---------------------------------------------------------------- 4.2.2
dict(code="4.2.2", id=2751, seq=22, minutes=10,
titre="Exercice : un faux service de paiement",
description="Payer une course avec le faux opérateur PayDem : le modèle des paiements, le bouton et le webhook.",
html=fiche(
objectif="payer une course de bout en bout avec un faux opérateur : demande, avis signé, course marquée payée.",
intro="On met en place un module <code>baobab_livraison_paiement</code> (qui dépend de <code>baobab_livraison</code>) et on le branche sur PayDem, un faux opérateur qui tourne sur ta machine.",
corps=[
("h", "1. Le faux opérateur (fourni)"),
("code", FAUX_PAYDEM, "faux_paydem.py (outil d'entraînement, à lancer dans un terminal à part)"),
("code", """PAYDEM_SECRET=un-secret-de-test python3 faux_paydem.py
PayDem (fictif) écoute sur http://localhost:8090""", "Terminal 1"),
("h", "2. Le modèle des paiements"),
("code", MODELE, "baobab_livraison_paiement/models/paiement.py (avec _envoyer_demande de la leçon 4.1.6)"),
("h", "3. Le bouton sur la course"),
("code", BOUTON, "baobab_livraison_paiement/models/course.py"),
("p", "Le bouton « Demander le paiement » et un onglet « Paiements » s'ajoutent au formulaire par héritage de vue (Bloc 3). Le webhook est celui de la leçon 4.1.5."),
("h", "4. Régler et essayer"),
("liste", [
  "Paramètres système (mode développeur, Paramètres › Technique › Paramètres système) : <code>baobab_paiement.url</code> = <code>http://localhost:8090</code>, <code>baobab_paiement.secret</code> = le même secret que PayDem.",
  "Vérifie que <code>web.base.url</code> vaut bien l'adresse de ton Odoo (<code>http://localhost:8069</code>) : c'est là que PayDem envoie l'avis.",
  "Donne un téléphone à Awa Diop, ouvre une course, clique sur « Demander le paiement ».",
]),
("code", """127.0.0.1 - - [28/Nov/2026 10:28:11] "POST /paiements HTTP/1.1" 201 -
webhook -> 200 {"ok": true, "deja_traite": false}
webhook -> 200 {"ok": true, "deja_traite": true}""", "Terminal 1 : journal réel de PayDem"),
("p", "Deux secondes plus tard, la course BL/2026/0037 est « Payée » : onglet Paiements « Payé », référence PD-4, et un seul message « Paiement mobile reçu : PD-4 » dans le fil."),
("attention", "Un avis peut arriver trop tôt", "Essai réel : quand la demande et l'enregistrement du secret se faisaient dans la même opération encore en cours, l'avis est arrivé <b>avant</b> qu'Odoo ait enregistré quoi que ce soit, et a été refusé (403). Avec un vrai bouton, Odoo enregistre à la fin du clic, bien avant l'avis. Mais retiens-le : un avis refusé n'est pas perdu, le rapprochement le rattrapera (leçon suivante)."),
],
exercice=[
("p", "Monte le module, lance PayDem, règle les paramètres, et paie une course. Vérifie dans psql : <code>SELECT reference_operateur, state FROM baobab_paiement;</code>. Puis essaie de redemander le paiement de la même course : quel message ? Enfin, ajoute la colonne « Payée » (<code>est_payee</code>) dans la liste des courses."),
],
retenir=[
  "Un paiement = une fiche avec deux références, un état, les tentatives et l'erreur.",
  "Le bouton crée la fiche et appelle l'opérateur ; l'avis signé la passe à « Payé ».",
  "Paramètres système : adresse de l'opérateur et secret ; <code>web.base.url</code> juste.",
  "On s'entraîne avec PayDem, un faux opérateur local.",
]),
quiz=[
("Qui passe le paiement à « Payé » ?", [
  ("L'avis signé de l'opérateur (ou le rapprochement)", V, "Oui."),
  ("Le bouton Demander le paiement", F, "Non : il ne fait que demander."),
  ("Le client, en cliquant dans Odoo", F, "Non."),
]),
("PayDem n'arrive pas à prévenir Odoo : quel réglage vérifier en premier ?", [
  ("web.base.url : l'adresse d'Odoo où l'avis est envoyé", V, "Oui, et le secret partagé."),
  ("La langue de l'utilisateur", F, "Non."),
  ("Le nombre de zones", F, "Non."),
]),
("Pourquoi refuser une deuxième demande quand un paiement est déjà « en attente » ?", [
  ("Pour éviter que le client paie deux fois", V, "Oui."),
  ("Parce que l'opérateur l'interdit", F, "Pas forcément : c'est à nous de protéger le client."),
  ("Pour aller plus vite", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 4.2.3
dict(code="4.2.3", id=2944, seq=23, minutes=10,
titre="Échecs, doublons et rapprochement",
description="Que faire quand la confirmation n'arrive jamais, quand l'opérateur ne répond pas ou envoie deux fois le même avis.",
html=fiche(
objectif="gérer tous les cas qui tournent mal : refus, absence de réponse, avis perdu, avis en double.",
intro="Dans la vraie vie, une partie des paiements ne suit pas le chemin idéal. Un bon module de paiement se reconnaît à la façon dont il gère ces cas : sans perdre d'argent, sans faire payer deux fois, sans bloquer personne.",
corps=[
("h", "Le rapprochement : une action planifiée"),
("code", RAPPROCHEMENT, "baobab_livraison_paiement/models/paiement.py"),
("p", "L'action planifiée « Baobab : rapprocher les paiements mobiles » tourne toutes les 10 minutes. Elle ne regarde que les paiements en attente depuis plus de 10 minutes (on laisse le temps au client de valider)."),
("h", "Les cas, et ce qu'on a obtenu pour de vrai"),
("tableau", ["Cas", "Ce que fait le module", "Résultat réel après rapprochement"], [
  ["Avis perdu (PayDem n'envoie rien : numéro en 8888)", "le rapprochement demande l'état à PayDem", "BL/2026/0036 : <b>Payé</b>, PD-2"],
  ["Avis refusé (arrivé trop tôt, leçon précédente)", "idem", "BL/2026/0033 : <b>Payé</b>, PD-1"],
  ["Pas de réponse à la demande (9999)", "nouvelle demande, au plus 3 essais, puis Échec", "BL/2026/0035 : en attente, <b>2 tentatives</b>"],
  ["Numéro refusé (0000)", "Échec définitif, pas de nouvel essai", "BL/2026/0034 : <b>Échec</b>, « Numéro refusé par l'opérateur »"],
  ["Avis reçu deux fois", "le second est ignoré (état + UNIQUE)", "un seul message « Paiement mobile reçu »"],
]),
("attention", "Le cas le plus dangereux", "« Pas de réponse » ne veut pas dire « pas payé » : la demande est peut-être arrivée chez l'opérateur. Avant de redemander, l'idéal est de demander à l'opérateur s'il connaît notre référence (beaucoup d'API le permettent) ; sinon, on garde la <b>même</b> référence Odoo pour que l'opérateur reconnaisse le doublon. Ne crée jamais une nouvelle référence à chaque essai."),
("h", "Et le remboursement ?"),
("p", "Même schéma : une fiche à part (montant négatif ou modèle « remboursement »), sa propre référence unique, une demande, un avis, un rapprochement. Un remboursement se déclenche par un responsable, jamais automatiquement."),
("astuce", "Le tableau de bord du responsable", "Une liste filtrée « Paiements en attente depuis plus d'une heure » et « Échecs du jour » permet au responsable d'appeler le client avant qu'il ne se plaigne. C'est une demande du travail à rendre."),
],
exercice=[
("p", "Avec PayDem, crée quatre paiements (numéros finissant par 4567, 0000, 9999, 8888). Vieillis-les dans psql (<code>UPDATE baobab_paiement SET write_date = now() - interval '20 minutes' WHERE state = 'en_attente';</code>), puis lance l'action planifiée avec « Exécuter manuellement ». Compare avec le tableau ci-dessus. Écris un test qui vérifie qu'après 3 tentatives sans réponse, le paiement passe en Échec."),
],
retenir=[
  "Le rapprochement (action planifiée) rattrape les avis perdus.",
  "Refus = Échec définitif ; pas de réponse = nouvel essai, avec une limite.",
  "Même référence à chaque essai : l'opérateur reconnaît le doublon.",
  "Tout est noté sur la fiche : tentatives et erreur.",
]),
quiz=[
("L'avis de paiement n'arrive pas, mais le client a payé. Comment Odoo le découvre-t-il ?", [
  ("Le rapprochement demande l'état à l'opérateur", V, "Oui (vérifié : la course passe à Payé)."),
  ("Il ne le découvre jamais", F, "Si, grâce au rapprochement."),
  ("Le client doit repayer", F, "Surtout pas."),
]),
("Un appel à l'opérateur dépasse le délai. Que faire ?", [
  ("Réessayer plus tard avec la même référence, et une limite d'essais", V, "Oui."),
  ("Marquer échec définitif tout de suite", F, "Trop tôt : c'est peut-être passager."),
  ("Réessayer en boucle immédiatement", F, "Non : on bloquerait Odoo et l'opérateur."),
]),
("Pourquoi ne pas créer une nouvelle référence à chaque nouvel essai ?", [
  ("Parce que l'opérateur ne pourrait plus reconnaître un doublon : risque de double paiement", V, "Oui."),
  ("Parce que les références coûtent cher", F, "Non."),
  ("Ce n'est pas un problème", F, "Si."),
]),
]),
]
