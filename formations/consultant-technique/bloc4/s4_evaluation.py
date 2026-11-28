"""Bloc 4 — Section « Évaluation » (section 2755, cours 211) : travail à rendre (2756).
Corrigé testé sur Odoo 20.0 le 28/11/2026 : base neuve avec démonstration, trois modules, 26 tests verts ; filtres de
surveillance des paiements vérifiés dans Chromium. Le corrigé n'est PAS dans ce dépôt (dépôt public) : transmis à
Babacar. Le faux opérateur PayDem (faux_paydem.py) est un outil d'entraînement, pas un corrigé."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

LECONS = [
dict(code="4.4.1", id=2756, seq=41, minutes=300,
titre="Travail à rendre : l'API des livreurs, le paiement mobile simulé et les droits",
description="Le projet de fin de Bloc 4 : une appli des livreurs complète, des paiements surveillés, des droits sûrs et une durée de conservation.",
html=fiche(
duree="environ 5 h",
titre_exercice="Comment rendre ton travail",
objectif="montrer que tu sais ouvrir un module Odoo 20 à d'autres logiciels (API, paiement mobile) sans créer de faille, et respecter les données des clients.",
intro="Baobab Livraison teste l'appli des livreurs et le paiement mobile depuis une semaine. Le gérant revient avec cinq demandes, et un auditeur de sécurité a relu le code.",
corps=[
("h", "Point de départ"),
("p", "Les modules du bloc : <code>baobab_livraison</code> (groupes Livreur et Responsable, droits par fiche, e-mail « colis livré », API <code>/api/livreur/…</code> avec la portée « Appli des livreurs »), <code>baobab_livraison_paiement</code> (paiements, webhook signé, rapprochement) et le faux opérateur PayDem."),
("h", "Les cinq demandes"),
("tableau", ["Demande", "Ce qu'on attend"], [
  ["1. Démarrer depuis l'appli", "Une adresse <code>POST /api/livreur/courses/&lt;id&gt;/demarrer</code>, mêmes règles que <code>livrer</code> (404 si la course n'est pas au livreur, 409 si l'action est refusée)."],
  ["2. Annulation réservée", "L'auditeur a vu qu'un livreur pouvait annuler une course par l'API. Seul un Responsable doit pouvoir annuler : vérification <b>dans la méthode</b>, pas seulement un bouton caché."],
  ["3. Surveiller les paiements", "Un menu « Paiements » réservé aux Responsables, avec deux filtres actifs à l'ouverture : « En attente depuis hier ou avant » et « Échecs du jour », et le total des montants."],
  ["4. Durée de conservation", "Une action planifiée hebdomadaire efface la consigne des courses livrées depuis plus d'un an (elle peut contenir un code de portail, un détail personnel)."],
  ["5. Le rapport d'audit", "Un fichier <code>SECURITE.md</code> qui liste chaque <code>sudo()</code>, <code>csrf=False</code>, <code>auth=\"public\"</code> et <code>cr.execute</code> du code, avec pour chacun : pourquoi c'est sûr, ou ce que tu as corrigé."],
]),
("h", "Les tests"),
("liste", [
  "Tous les tests des modules restent verts.",
  "Au moins <b>5 nouveaux tests</b>, dont : un livreur ne peut pas annuler (AccessError) ; un responsable peut ; démarrer par l'API ; l'effacement des vieilles consignes ; un webhook avec une mauvaise signature est refusé.",
  "La commande de test et sa ligne de résultat sont dans le <code>README.md</code>.",
]),
("attention", "Aucun secret, aucune vraie donnée", "Pas de clé d'API, pas de secret PayDem, pas de mot de passe dans le dépôt : les tests créent leurs propres clés et règlent le secret dans <code>setUp</code>. Pas de vraie donnée client, même dans un exemple."),
("h", "Comment tu seras évalué (sur 20)"),
("tableau", ["Critère", "Points"], [
  ["Les modules s'installent sur une base neuve sans erreur", "2"],
  ["API : démarrer, codes de réponse justes, aucun sudo, portée de clé respectée", "4"],
  ["Annulation réservée dans la méthode, testée", "3"],
  ["Menu et filtres de surveillance des paiements justes", "3"],
  ["Durée de conservation : action planifiée et test", "2"],
  ["SECURITE.md : complet et juste", "3"],
  ["Tests : tous verts, au moins 5 nouveaux ; Git propre, aucun secret", "3"],
]),
],
exercice=[
("liste", [
  "Rends ton dépôt GitHub public, ou invite ton formateur dans le dépôt.",
  "Envoie le lien de ton dépôt à ton formateur <b>avant l'atelier de fin de Bloc 4</b> : la correction se fait en revue de code, avec une démonstration (appel curl à ton API, paiement avec PayDem).",
]),
("astuce", "Avant d'envoyer", "Sur une base neuve : installe les modules avec <code>--with-demo</code>, lance tous les tests, puis fais le parcours complet à la main : clé d'API d'Ibou, <code>curl</code> sur ses courses, démarrer, livrer, demander le paiement avec PayDem lancé. Et passe <code>grep -rn \"sudo()\" .</code> une dernière fois."),
],
retenir=[
  "Cinq demandes : démarrer par l'API, annulation réservée, surveillance des paiements, durée de conservation, rapport d'audit.",
  "Une interdiction se vérifie dans la méthode, pas seulement dans la vue.",
  "Aucun secret ni aucune vraie donnée dans le dépôt.",
  "Lien du dépôt à envoyer avant l'atelier de fin de Bloc 4.",
]),
quiz=[]),
]
