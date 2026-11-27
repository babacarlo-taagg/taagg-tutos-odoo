"""Bloc 2 — Section « Les tests » (section 2731, cours 209).
Tests et sorties réels, Odoo 20.0, 27/11/2026 : 8 tests verts, puis un test volontairement faux."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

TEST = """from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCourse(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.zone = cls.env["baobab.zone"].create({"name": "Zone de test", "tarif": 1500})
        cls.client = cls.env["res.partner"].create({"name": "Client test"})

    def creer_course(self, **valeurs):
        return self.env["baobab.course"].create(
            {"client_id": self.client.id, "zone_id": self.zone.id, **valeurs})

    def test_prix_sans_supplement(self):
        self.assertEqual(self.creer_course(poids=3).prix, 1500)

    def test_prix_avec_supplement(self):
        # 7,2 kg : 3 kilos entamés au-delà de 5 kg, 200 F chacun
        self.assertEqual(self.creer_course(poids=7.2).prix, 2100)"""

LECONS = [
# ---------------------------------------------------------------- 2.6.1
dict(code="2.6.1", id=2732, seq=61, minutes=10,
titre="Écrire un premier test",
description="Vérifier automatiquement le calcul du prix avec TransactionCase.",
html=fiche(
objectif="écrire des tests automatiques qui vérifient le calcul du prix et les règles de la course.",
intro="Tu changes une ligne du calcul du prix… et tu casses sans le voir les courses de plus de 5 kg. Un <b>test automatique</b> le verrait en une seconde. Chez un client, un module sans tests est un module dont personne n'ose toucher le code.",
corps=[
("h", "Le fichier de test"),
("code", TEST, "tests/test_course.py"),
("code", """from . import test_course""", "tests/__init__.py"),
("liste", [
  "Le dossier <code>tests/</code> n'est <b>pas</b> importé dans le <code>__init__.py</code> du module : Odoo le trouve seul quand on lance les tests.",
  "<code>TransactionCase</code> : chaque test tourne dans une transaction <b>annulée à la fin</b>. Tes essais ne salissent pas la base.",
  "<code>setUpClass</code> : prépare une fois les données communes (une zone, un client).",
  "Chaque méthode qui commence par <code>test_</code> est un test.",
  "<code>@tagged(\"post_install\", \"-at_install\")</code> : le test tourne après l'installation de tous les modules (habitude conseillée).",
]),
("h", "Vérifier qu'une erreur est bien levée"),
("code", """from odoo.exceptions import UserError, ValidationError

    def test_demarrer_sans_livreur(self):
        with self.assertRaises(UserError):
            self.creer_course().action_demarrer()

    def test_livreur_doit_etre_livreur(self):
        with self.assertRaises(ValidationError):
            self.creer_course(livreur_id=self.client.id)""", "tests/test_course.py (suite)"),
("tableau", ["Vérification", "Sens"], [
  ["<code>assertEqual(a, b)</code>", "a est égal à b"],
  ["<code>assertTrue(x)</code> / <code>assertFalse(x)</code>", "x est vrai / faux (ou vide)"],
  ["<code>assertIn(a, b)</code>", "a se trouve dans b"],
  ["<code>with self.assertRaises(Erreur):</code>", "le bloc doit lever cette erreur"],
]),
("astuce", "Que tester ?", "Les calculs (le prix), les règles (contraintes, statuts), et chaque bogue corrigé (un test pour qu'il ne revienne jamais). Inutile de tester ce qu'Odoo fait déjà (enregistrer un texte dans un champ)."),
],
exercice=[
("p", "Écris les tests du prix (sans et avec supplément), puis ajoute : la référence commence par <code>BL/</code> ; démarrer sans livreur lève <code>UserError</code> ; le cycle complet brouillon → en route → livrée remplit <code>date_livraison</code>. Tu dois arriver à au moins 6 tests (on les lance dans la leçon suivante)."),
],
retenir=[
  "Tests dans <code>tests/</code>, fichiers <code>test_*.py</code>, importés par <code>tests/__init__.py</code>.",
  "<code>TransactionCase</code> : tout est annulé après chaque test.",
  "Méthodes <code>test_…</code> + <code>assertEqual</code>, <code>assertRaises</code>…",
  "Un bogue corrigé = un test de plus.",
]),
quiz=[
("Avec TransactionCase, que deviennent les courses créées pendant un test ?", [
  ("Elles sont annulées à la fin du test", V, "Oui : la base reste propre."),
  ("Elles restent dans la base", F, "Non."),
  ("Elles sont archivées", F, "Non."),
]),
("Comment vérifier que démarrer une course sans livreur est refusé ?", [
  ("with self.assertRaises(UserError): course.action_demarrer()", V, "Oui."),
  ("self.assertEqual(course.action_demarrer(), False)", F, "Non : la méthode lève une erreur, elle ne renvoie pas False."),
  ("Avec un print", F, "Non : un test doit vérifier tout seul."),
]),
("Quelle méthode est reconnue comme un test ?", [
  ("def test_prix_avec_supplement(self):", V, "Oui : le nom commence par test_."),
  ("def verifier_prix(self):", F, "Non : elle ne serait pas lancée automatiquement."),
  ("def setUpClass(cls):", F, "Non : elle prépare les données."),
]),
]),

# ---------------------------------------------------------------- 2.6.2
dict(code="2.6.2", id=2920, seq=62, minutes=10,
titre="Lancer ses tests et lire le résultat",
description="--test-tags, lire la ligne de résultat, comprendre et corriger un test qui échoue.",
html=fiche(
objectif="lancer les tests de ton module, lire le résultat, et comprendre un test qui échoue.",
intro="Écrire des tests, c'est bien ; les lancer à chaque modification, c'est mieux. Une seule commande, et une ligne à lire.",
corps=[
("h", "Lancer les tests du module"),
("code", """python3 odoo-bin -c ~/baobab/odoo.conf -d baobab_test -u baobab_livraison \\
    --test-tags /baobab_livraison --stop-after-init""", "Terminal"),
("liste", [
  "<code>-u baobab_livraison</code> : met à jour le module (le code testé est le code actuel).",
  "<code>--test-tags /baobab_livraison</code> : seulement les tests de ce module.",
  "<code>--stop-after-init</code> : Odoo s'arrête une fois les tests finis.",
  "Utilise une <b>base de test</b>, jamais la base d'un client.",
]),
("code", """INFO baobab_test odoo.addons.baobab_livraison.tests.test_course: Starting TestCourse.test_cycle_complet ...
INFO baobab_test odoo.addons.baobab_livraison.tests.test_course: Starting TestCourse.test_demarrer_sans_livreur ...
…
INFO baobab_test odoo.tests.result: 0 failed, 0 error(s) of 8 tests when loading database 'baobab_test'""", "Tout est vert"),
("p", "La ligne à chercher : <code>0 failed, 0 error(s) of 8 tests</code>. <b>failed</b> = une vérification fausse ; <b>error</b> = le test a planté (faute de frappe, champ inexistant…)."),
("h", "Un test qui échoue"),
("p", "Imaginons qu'on se trompe dans le résultat attendu : on écrit 2 000 au lieu de 2 100. On lance un seul test avec <code>--test-tags /baobab_livraison:TestCourse.test_prix_avec_supplement</code> :"),
("code", """ERROR baobab_test odoo.addons.baobab_livraison.tests.test_course: FAIL: TestCourse.test_prix_avec_supplement
Traceback (most recent call last):
  File "/home/awa/baobab/addons/baobab_livraison/tests/test_course.py", line 27, in test_prix_avec_supplement
    self.assertEqual(self.creer_course(poids=7.2).prix, 2000)
AssertionError: 2100.0 != 2000
ERROR baobab_test odoo.tests.result: 1 failed, 0 error(s) of 1 tests when loading database 'baobab_test'""", "Sortie réelle (Odoo 20)"),
("liste", [
  "<code>FAIL: TestCourse.test_prix_avec_supplement</code> : quel test.",
  "<code>line 27</code> : quelle ligne.",
  "<code>AssertionError: 2100.0 != 2000</code> : le programme a calculé 2 100, le test attendait 2 000.",
]),
("attention", "Qui a raison : le code ou le test ?", "Un test rouge ne veut pas toujours dire que le code est faux. Refais le calcul à la main : 7,2 kg → 3 kilos entamés au-delà de 5 → 1 500 + 3 × 200 = 2 100. Ici, c'est le <b>test</b> qui est faux. On corrige le test, jamais on ne le supprime pour « faire passer »."),
("version", "<code>--test-tags</code> existe depuis Odoo 12. En Odoo 20, la ligne de résultat se termine par <code>when loading database '…'</code>. Le format <code>/module:Classe.methode</code> permet de lancer un seul test."),
],
exercice=[
("p", "Lance tes tests : tu dois lire <code>0 failed, 0 error(s)</code>. Puis casse volontairement le calcul du prix (remplace <code>math.ceil</code> par <code>int</code>) : quels tests deviennent rouges ? Lis le message, explique pourquoi, et remets le code."),
],
retenir=[
  "<code>-u module --test-tags /module --stop-after-init</code>, sur une base de test.",
  "La ligne à lire : <code>X failed, Y error(s) of N tests</code>.",
  "Un FAIL se lit : quel test, quelle ligne, valeur obtenue != valeur attendue.",
  "On corrige le code ou le test, on ne supprime jamais un test rouge.",
]),
quiz=[
("Que signifie « 0 failed, 0 error(s) of 8 tests » ?", [
  ("Les 8 tests sont passés", V, "Oui."),
  ("Aucun test n'a été lancé", F, "Non : 8 tests ont tourné."),
  ("8 tests ont échoué", F, "Non."),
]),
("« AssertionError: 2100.0 != 2000 » : que s'est-il passé ?", [
  ("Le code a donné 2 100 alors que le test attendait 2 000", V, "Oui."),
  ("Le test a planté avant de vérifier", F, "Non : ce serait une error, pas un failed."),
  ("Odoo n'a pas trouvé le champ prix", F, "Non."),
]),
("Un test est rouge juste avant une livraison au client. Que faire ?", [
  ("Comprendre pourquoi, puis corriger le code ou le test", V, "Oui."),
  ("Supprimer le test", F, "Jamais : il protège le client."),
  ("Livrer quand même", F, "Non."),
]),
]),
]
