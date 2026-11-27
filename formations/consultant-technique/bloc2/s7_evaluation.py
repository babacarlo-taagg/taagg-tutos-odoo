"""Bloc 2 — Section « Évaluation » (section 2733, cours 209) : travail à rendre (2734).
Corrigé testé sur Odoo 20.0 le 27/11/2026 (base neuve avec démonstration, 12 tests verts, tarif protégé par noupdate
après -u). Il n'est PAS dans ce dépôt (dépôt public) : transmis à Babacar."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

LECONS = [
dict(code="2.7.1", id=2734, seq=71, minutes=240,
titre="Travail à rendre : le module Baobab Livraison côté serveur",
description="Le projet de fin de Bloc 2 : le module baobab_livraison complet, trois améliorations demandées par le client, des tests verts et un historique Git propre.",
html=fiche(
duree="environ 4 h",
titre_exercice="Comment rendre ton travail",
objectif="montrer que tu sais construire un module Odoo 20 complet, le faire évoluer à la demande d'un client et prouver qu'il marche avec des tests.",
intro="Ton module <code>baobab_livraison</code> tourne. Le gérant de Baobab l'a essayé une semaine et revient avec trois demandes. C'est la vie normale d'un consultant technique : livrer, écouter, améliorer, sans rien casser.",
corps=[
("h", "Point de départ"),
("p", "Le module tel que tu l'as construit pendant le bloc : zones, étiquettes, courses (prix calculé, statuts et boutons, référence automatique, contraintes, chatter, action planifiée), livreurs sur les contacts, données de démonstration, et au moins 8 tests verts. Le module pont <code>baobab_livraison_vente</code> est un bonus."),
("h", "Les trois demandes du client"),
("tableau", ["Demande", "Ce qu'on attend"], [
  ["1. Option express", "Une case « Express (dans l'heure) » sur la course. Une course express coûte <b>1 000 F de plus</b>. Le prix se recalcule dès qu'on coche la case. Le changement est suivi dans le fil."],
  ["2. Zones fermées", "Quand Baobab arrête de desservir une zone, on l'<b>archive</b>. Il doit alors être impossible de créer une course (ou de déplacer une course) vers cette zone, avec le message « La zone … n'est plus desservie. »"],
  ["3. Tarifs protégés", "Le gérant a changé le tarif de Mermoz, et une mise à jour du module l'a remis à 1 500 F. Les zones doivent passer dans un fichier XML <code>noupdate=\"1\"</code> (mêmes identifiants externes), et la version du module passe à <code>20.0.1.1.0</code>."],
]),
("h", "Résultats attendus (à vérifier par tes tests)"),
("tableau", ["Course (zone à 1 500 F)", "Prix"], [
  ["3 kg, normale", "1 500 F"],
  ["3 kg, express", "2 500 F"],
  ["7,2 kg, express", "3 100 F"],
  ["Course existante de 3 kg, on coche « express »", "passe à 2 500 F"],
]),
("h", "Les tests"),
("liste", [
  "Tous les tests du bloc restent verts.",
  "Au moins <b>4 nouveaux tests</b> : les trois prix ci-dessus et le refus d'une zone archivée (<code>assertRaises(ValidationError)</code>).",
  "La commande de test et sa ligne de résultat (<code>0 failed, 0 error(s) of … tests</code>) sont recopiées dans le <code>README.md</code>.",
]),
("h", "Le dépôt Git"),
("liste", [
  "Le dossier du module à la racine du dépôt <code>baobab_livraison</code> (celui du Bloc 1, ou un nouveau).",
  "Une <b>branche par demande</b> du client, fusionnée dans <code>main</code> ; au moins 8 commits aux messages clairs.",
  "Un <code>.gitignore</code> : aucun <code>__pycache__</code>, aucun fichier <code>.conf</code>.",
  "Un <code>README.md</code> : à quoi sert le module, comment l'installer, comment lancer les tests.",
]),
("attention", "Aucun secret", "Ni mot de passe de base, ni mot de passe maître (<code>admin_passwd</code>), ni jeton GitHub dans le dépôt. Un secret dans le dépôt fait perdre tous les points de la ligne « Git »."),
("h", "Comment tu seras évalué (sur 20)"),
("tableau", ["Critère", "Points"], [
  ["Le module s'installe sur une base neuve sans erreur, avec <code>--with-demo</code>", "3"],
  ["Option express : champ, prix, suivi dans le fil", "3"],
  ["Zone archivée refusée, avec le bon message", "3"],
  ["Zones en <code>noupdate</code> : le tarif modifié survit à un <code>-u</code> ; version 20.0.1.1.0", "3"],
  ["Tests : tous verts, au moins 4 nouveaux, pertinents", "4"],
  ["Code lisible et conforme à Odoo 20 (<code>ir.access.csv</code>, <code>models.Constraint</code>, <code>self.env._</code>)", "2"],
  ["Git : branches, commits clairs, <code>README.md</code>, aucun secret", "2"],
]),
],
exercice=[
("liste", [
  "Rends ton dépôt GitHub public, ou invite ton formateur dans le dépôt.",
  "Envoie le lien de ton dépôt à ton formateur <b>avant l'atelier de fin de Bloc 2</b> : la correction se fait en revue de code pendant l'atelier.",
  "Le formateur installera ton module sur une base neuve et lancera tes tests : vérifie que c'est possible en suivant ton propre <code>README.md</code>.",
]),
("astuce", "Avant d'envoyer", "Crée une base toute neuve (<code>createdb essai_final</code>), installe ton module avec <code>-i baobab_livraison --with-demo</code> puis lance les tests. Ensuite, change un tarif à l'écran, fais <code>-u</code> et vérifie qu'il est toujours là."),
],
retenir=[
  "Trois demandes : option express (+1 000 F), zone archivée refusée, zones en <code>noupdate</code>.",
  "Tous les tests verts, dont au moins 4 nouveaux.",
  "Une branche par demande, un README, aucun secret.",
  "Lien du dépôt à envoyer avant l'atelier de fin de Bloc 2.",
]),
quiz=[]),
]
