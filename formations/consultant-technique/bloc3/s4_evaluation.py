"""Bloc 3 — Section « Évaluation » (section 2744, cours 210) : travail à rendre (2745).
Corrigé testé sur Odoo 20.0 le 28/11/2026 : base neuve avec démonstration, 17 tests verts ; mise à jour depuis le module
de référence vérifiée (sans script de migration, toutes les courses existantes reçoivent le même code de suivi ; avec le
script post-, chacune a le sien) ; filtres et code-barres vérifiés dans Chromium. Le corrigé n'est PAS dans ce dépôt
(dépôt public) : transmis à Babacar."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

LECONS = [
dict(code="3.4.1", id=2745, seq=41, minutes=240,
titre="Travail à rendre : les écrans, le bordereau PDF et la page « Suivre mon colis »",
description="Le projet de fin de Bloc 3 : des écrans complets, un bordereau avec code-barres, une page de suivi protégée par un code secret, le portail client, et des tests.",
html=fiche(
duree="environ 4 h",
titre_exercice="Comment rendre ton travail",
objectif="montrer que tu sais construire toute l'interface d'un module Odoo 20 : écrans, rapport PDF, page du site et portail, sans exposer les données des clients.",
intro="Ton module a maintenant de vrais écrans, un bordereau, une page « Suivre mon colis » et un portail. Le gérant de Baobab a tout essayé pendant une semaine. Il revient avec quatre demandes.",
corps=[
("h", "Point de départ"),
("p", "Les deux modules du bloc : <code>baobab_livraison</code> (vues liste, formulaire, recherche, kanban, calendrier, pivot, graphique ; menus ; fiche contact ; bordereau ; widget d'avancement) et <code>baobab_livraison_site</code> (page de suivi, portail « Mes courses »), avec leurs tests."),
("h", "Les quatre demandes du gérant"),
("tableau", ["Demande", "Ce qu'on attend"], [
  ["1. Repérer les problèmes", "Deux filtres dans la recherche : « En retard » (courses en route dont la date est passée depuis plus d'un jour) et « Colis lourds » (plus de 30 kg). Dans la liste, les colis lourds en rouge."],
  ["2. Un bordereau scannable", "Le code-barres de la référence (Code128) sous le titre du bordereau, avec l'adresse <code>/report/barcode/</code> d'Odoo. Le code de suivi (demande 3) imprimé à côté de la zone."],
  ["3. Une page de suivi protégée", "Un champ <code>code_suivi</code> (6 caractères au hasard, non recopié quand on duplique). La page « Suivre mon colis » demande la référence <b>et</b> le code : sans le bon code, rien ne s'affiche. Une course livrée affiche aussi « Livrée le ». Les courses déjà enregistrées doivent recevoir chacune un code <b>différent</b> : version 20.0.2.1.0 et un script de migration."],
  ["4. Un widget plus parlant", "Quand la course est livrée, le widget d'avancement affiche « Livrée ! » au lieu de « Étape 3 sur 3 »."],
]),
("attention", "Le piège de la demande 3", "Un champ ajouté avec <code>default=</code> reçoit, pour les fiches <b>déjà</b> enregistrées, une seule et même valeur. Essai réel : sans script, les deux courses existantes ont reçu le même code. Il faut un script <code>post-</code> qui donne un code à chaque course (leçon 2.5.3)."),
("h", "Les tests"),
("liste", [
  "Tous les tests des deux modules restent verts.",
  "Au moins <b>4 nouveaux tests</b>, dont : la page sans le bon code n'affiche rien ; deux courses ont des codes différents ; le bordereau contient le code-barres ; une course livrée affiche « Livrée le ».",
  "La commande de test et sa ligne de résultat sont recopiées dans le <code>README.md</code>.",
]),
("h", "Le dépôt Git"),
("liste", [
  "Les deux modules dans le dépôt <code>baobab_livraison</code> ; une branche par demande, fusionnée dans <code>main</code>.",
  "Le <code>README.md</code> explique comment installer (<code>-i baobab_livraison_site --with-demo</code>) et comment tester.",
  "Aucun mot de passe dans le dépôt, ni ceux des comptes portail de test.",
]),
("h", "Comment tu seras évalué (sur 20)"),
("tableau", ["Critère", "Points"], [
  ["Les deux modules s'installent sur une base neuve sans erreur ni avertissement de vue", "2"],
  ["Filtres « En retard » et « Colis lourds » justes ; colis lourds en rouge", "3"],
  ["Bordereau : code-barres et code de suivi ; PDF lisible", "3"],
  ["Page de suivi : référence + code obligatoires, rien de personnel affiché, « Livrée le »", "4"],
  ["Script de migration : un code différent par course existante", "3"],
  ["Widget « Livrée ! » (OWL 3, écriture d'Odoo 20)", "1"],
  ["Tests : tous verts, au moins 4 nouveaux, pertinents", "3"],
  ["Git : branches, README, aucun secret", "1"],
]),
],
exercice=[
("liste", [
  "Rends ton dépôt GitHub public, ou invite ton formateur dans le dépôt.",
  "Envoie le lien de ton dépôt à ton formateur <b>avant l'atelier de fin de Bloc 3</b> : la correction se fait en revue de code pendant l'atelier.",
  "Le formateur mettra à jour une base créée avec la version du bloc, pour vérifier ton script de migration : teste ce cas toi-même.",
]),
("astuce", "Avant d'envoyer", "Installe la version du bloc sur une base neuve avec <code>--with-demo</code>, puis passe à ta version avec <code>-u baobab_livraison</code> : dans <code>psql</code>, <code>SELECT name, code_suivi FROM baobab_course;</code> doit montrer des codes tous différents. Si les codes-barres ne s'affichent pas, relis la leçon 3.2.4."),
],
retenir=[
  "Quatre demandes : filtres, bordereau scannable, page protégée par un code, widget « Livrée ! ».",
  "Nouveau champ + fiches existantes = script de migration <code>post-</code>.",
  "Une page publique ne montre jamais de données personnelles.",
  "Lien du dépôt à envoyer avant l'atelier de fin de Bloc 3.",
]),
quiz=[]),
]
