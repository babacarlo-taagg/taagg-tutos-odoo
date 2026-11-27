"""Bloc 2 — Section « Les données du module » (section 2728, cours 209).
Vérifié sur Odoo 20.0 le 27/11/2026 : chargement des fichiers (journal de -u), identifiants externes, noupdate,
écrasement d'un tarif modifié à la mise à jour, script de migration pre- (avec et sans script)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

LECONS = [
# ---------------------------------------------------------------- 2.5.1
dict(code="2.5.1", id=2729, seq=51, minutes=10,
titre="Fichiers de données XML et CSV, identifiants externes",
description="Charger les six zones de Dakar et les étiquettes avec le module, et les retrouver par leur identifiant externe.",
html=fiche(
objectif="livrer des données avec ton module (les zones de Dakar, les étiquettes) et les retrouver grâce à leur identifiant externe.",
intro="Un client qui installe Baobab Livraison doit trouver tout de suite les six zones de Dakar et les étiquettes Fragile et Urgent. Pas besoin de les saisir : le module les apporte, dans des fichiers de données.",
corps=[
("h", "Le format CSV : pratique pour les listes"),
("code", """id,name,tarif
zone_plateau,Plateau,1000
zone_medina,Médina,1000
zone_mermoz,Mermoz,1500
zone_parcelles,Parcelles Assainies,2000
zone_pikine,Pikine,2500
zone_rufisque,Rufisque,3000""", "data/baobab.zone.csv"),
("liste", [
  "Le <b>nom du fichier</b> donne le modèle : <code>baobab.zone.csv</code> → modèle <code>baobab.zone</code>.",
  "La première ligne : les noms techniques des champs.",
  "La colonne <code>id</code> : l'<b>identifiant externe</b> de chaque fiche.",
]),
("h", "Le format XML : pour tout le reste"),
("code", """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="etiquette_fragile" model="baobab.etiquette">
        <field name="name">Fragile</field>
        <field name="color">1</field>
    </record>
    <record id="etiquette_urgent" model="baobab.etiquette">
        <field name="name">Urgent</field>
        <field name="color">2</field>
    </record>
</odoo>""", "data/baobab_etiquette_data.xml"),
("p", "N'oublie pas d'ajouter chaque fichier dans <code>data</code> du manifeste, <b>dans l'ordre</b> : les droits d'abord, puis les données, puis les écrans. Au <code>-u</code>, le journal montre chaque fichier chargé : <code>loading baobab_livraison/data/baobab.zone.csv</code>."),
("h", "L'identifiant externe : le nom stable d'une fiche"),
("p", "L'<code>id</code> d'une fiche (3, 47…) change d'une base à l'autre. L'identifiant externe, lui, est le même partout : <code>baobab_livraison.zone_mermoz</code> (nom du module + identifiant)."),
("code", """>>> env.ref("baobab_livraison.zone_mermoz")
baobab.zone(3,)
>>> env.ref("baobab_livraison.zone_mermoz").name
'Mermoz'""", "Terminal d'Odoo"),
("liste", [
  "En XML, on s'y réfère avec <code>ref=\"zone_mermoz\"</code> (dans le même module) ou <code>ref=\"base.group_user\"</code> (dans un autre module).",
  "En Python : <code>self.env.ref(\"baobab_livraison.zone_mermoz\")</code>.",
  "À l'écran (mode développeur) : sur une fiche, icône du mode développeur (le petit insecte) › <b>Afficher les métadonnées</b>.",
  "Odoo les range dans le modèle <code>ir.model.data</code>.",
]),
("astuce", "Pourquoi c'est précieux", "Grâce à l'identifiant externe, une mise à jour du module retrouve « sa » zone Mermoz et la met à jour au lieu d'en créer une deuxième. C'est aussi ce qui permet aux autres modules de s'y référer."),
],
exercice=[
("p", "Ajoute le CSV des zones et le XML des étiquettes, mets-les dans le manifeste, puis mets à jour sur une base neuve. Vérifie : six zones et deux étiquettes. Dans le terminal d'Odoo, retrouve la zone Pikine avec <code>env.ref</code> et affiche son tarif. Ajoute ensuite une septième zone, Guédiawaye à 2 500 F, dans le CSV, et mets à jour."),
],
retenir=[
  "CSV : le nom du fichier = le modèle ; colonne <code>id</code> = identifiant externe.",
  "XML : <code>&lt;record id=\"…\" model=\"…\"&gt;</code> + des <code>&lt;field&gt;</code>.",
  "Identifiant externe complet : <code>module.identifiant</code> ; <code>env.ref(...)</code> en Python.",
  "Les fichiers sont listés dans <code>data</code>, dans le bon ordre.",
]),
quiz=[
("Le fichier data/baobab.zone.csv crée des fiches de quel modèle ?", [
  ("baobab.zone", V, "Oui : le nom du fichier donne le modèle."),
  ("Celui indiqué dans la première ligne", F, "Non : la première ligne liste les champs."),
  ("Aucun, il faut l'importer à la main", F, "Non : il est chargé à l'installation s'il est dans data."),
]),
("Quel est l'identifiant externe complet de la zone Mermoz ?", [
  ("baobab_livraison.zone_mermoz", V, "Oui : module.identifiant."),
  ("3", F, "Non : c'est son id, qui change d'une base à l'autre."),
  ("baobab.zone.mermoz", F, "Non."),
]),
("À quoi sert l'identifiant externe lors d'une mise à jour du module ?", [
  ("À retrouver la fiche existante pour la mettre à jour au lieu d'en créer une autre", V, "Oui."),
  ("À rien", F, "Non."),
  ("À supprimer la fiche", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 2.5.2
dict(code="2.5.2", id=2918, seq=52, minutes=10,
titre="Données de démonstration et noupdate",
description="Préparer une base de test réaliste, et protéger les données que le client modifie.",
html=fiche(
objectif="préparer des données d'exemple pour tes bases de test, et comprendre <code>noupdate</code> pour ne jamais écraser le travail d'un client.",
intro="Pour tester, il faut des clients, des livreurs, des courses. Les saisir à chaque nouvelle base serait pénible : on les met dans des <b>données de démonstration</b>. Et il faut un réglage pour qu'une mise à jour n'efface pas ce que le client a modifié : <code>noupdate</code>.",
corps=[
("h", "Les données de démonstration"),
("code", """<odoo>
    <record id="partenaire_awa" model="res.partner">
        <field name="name">Awa Diop</field>
        <field name="city">Dakar</field>
    </record>
    <record id="livreur_ibou" model="res.partner">
        <field name="name">Ibou Fall</field>
        <field name="est_livreur" eval="True"/>
    </record>
    <record id="course_demo_1" model="baobab.course">
        <field name="client_id" ref="partenaire_awa"/>
        <field name="livreur_id" ref="livreur_ibou"/>
        <field name="zone_id" ref="zone_mermoz"/>
        <field name="poids">3.5</field>
        <field name="etiquette_ids" eval="[Command.link(ref('etiquette_fragile'))]"/>
    </record>
</odoo>""", "demo/baobab_demo.xml (extrait), listé dans \"demo\" du manifeste"),
("liste", [
  "<code>ref=\"…\"</code> pour un Many2one ; <code>eval=\"…\"</code> pour une valeur Python (<code>True</code>, une liste de <code>Command</code>).",
  "La course reçoit automatiquement sa référence (BL/2026/0001) et son prix (1 500 F) : le code du module s'applique aussi aux données chargées.",
]),
("version", "<b>Odoo 18.3 et suivants (donc Odoo 20)</b> : une nouvelle base est créée <b>sans</b> données de démonstration par défaut. Pour les avoir : <code>--with-demo</code> à la création de la base (ou la case à cocher dans le gestionnaire de bases). <b>Avant</b>, c'était l'inverse : il fallait <code>--without-demo</code> pour ne pas les avoir."),
("code", """createdb baobab_test
python3 odoo-bin -c ~/baobab/odoo.conf -d baobab_test -i baobab_livraison --with-demo --stop-after-init""", "Terminal : une base de test avec les données d'exemple"),
("h", "noupdate : protéger les données du client"),
("p", "Expérience réelle : on change le tarif de Mermoz à 1 600 F, puis on met à jour le module (<code>-u baobab_livraison</code>). Résultat : le tarif est revenu à <b>1 500 F</b>. Le fichier CSV a été rechargé et a écrasé la modification."),
("tableau", ["Données", "Mise à jour (-u)"], [
  ["Fichier dans <code>data</code> (normal)", "rechargé : les fiches reprennent les valeurs du fichier"],
  ["<code>&lt;odoo noupdate=\"1\"&gt;</code>", "chargé à l'installation seulement, ensuite plus jamais touché"],
  ["Fichier dans <code>demo</code>", "traité comme <code>noupdate</code> automatiquement"],
]),
("p", "C'est pour cela que la séquence est dans <code>&lt;odoo noupdate=\"1\"&gt;</code> : sinon chaque mise à jour remettrait son compteur à zéro."),
("attention", "Que mettre en noupdate ?", "Tout ce que le client a le droit de modifier : tarifs, séquences, modèles d'e-mails, paramètres. Les zones de Baobab devraient donc être dans un fichier XML <code>noupdate=\"1\"</code> plutôt que dans le CSV : c'est une des améliorations du travail à rendre."),
],
exercice=[
("p", "Crée une base de test avec <code>--with-demo</code> et vérifie les deux courses d'exemple. Puis refais l'expérience : tarif de Mermoz à 1 600 F à l'écran, <code>-u baobab_livraison</code>, regarde le tarif. Ensuite, déplace les zones dans <code>data/baobab_zone_data.xml</code> avec <code>noupdate=\"1\"</code> et recommence sur une nouvelle base : le tarif doit rester à 1 600 F."),
],
retenir=[
  "Données d'exemple dans <code>demo</code> ; Odoo 20 : <code>--with-demo</code> pour les charger.",
  "Sans <code>noupdate</code>, chaque <code>-u</code> remet les valeurs du fichier.",
  "<code>noupdate=\"1\"</code> pour tout ce que le client peut modifier.",
  "Les données de démonstration sont toujours traitées comme <code>noupdate</code>.",
]),
quiz=[
("Un client change le tarif d'une zone chargée par un fichier CSV du module. Que se passe-t-il au prochain -u ?", [
  ("Le tarif revient à la valeur du fichier", V, "Oui (vérifié sur Odoo 20) : d'où l'intérêt de noupdate."),
  ("Le tarif du client est gardé", F, "Non, pas sans noupdate."),
  ("Une deuxième zone est créée", F, "Non : l'identifiant externe retrouve la même fiche."),
]),
("En Odoo 20, comment obtenir les données de démonstration sur une nouvelle base ?", [
  ("Avec --with-demo à la création", V, "Oui : depuis Odoo 18.3, elles ne sont plus chargées par défaut."),
  ("Elles sont toujours chargées", F, "C'était le cas avant Odoo 18.3."),
  ("Il faut les saisir à la main", F, "Non."),
]),
("Pourquoi la séquence des courses est-elle dans <odoo noupdate=\"1\"> ?", [
  ("Pour que la mise à jour ne remette pas le compteur à zéro", V, "Oui."),
  ("Pour qu'elle ne soit jamais installée", F, "Non : elle est installée, puis protégée."),
  ("Parce que c'est obligatoire pour toutes les séquences", F, "Pas obligatoire, mais très conseillé."),
]),
]),

# ---------------------------------------------------------------- 2.5.3
dict(code="2.5.3", id=2730, seq=53, minutes=10,
titre="Scripts de migration du module (pré et post)",
description="Renommer un champ sans perdre les données des clients, avec un script de migration.",
html=fiche(
objectif="faire évoluer ton module chez un client sans perdre ses données, grâce aux scripts de migration.",
intro="Version 1 de Baobab : le champ s'appelait <code>note</code>. En version 1.1, on le renomme <code>consigne</code>, plus clair. Simple ? Chez un client qui a déjà 3 000 courses avec des notes, c'est un piège.",
corps=[
("h", "Sans script : les données disparaissent"),
("p", "On a fait l'essai sur Odoo 20 : on renomme le champ dans le code, on monte la version, <code>-u</code>. Odoo voit un nouveau champ <code>consigne</code> (colonne vide) et un champ <code>note</code> qui n'existe plus dans le code : la colonne <code>note</code> est <b>supprimée</b>, avec tous les textes."),
("h", "Avec un script : on renomme la colonne avant"),
("code", """baobab_livraison/
├── __manifest__.py          ← "version": "20.0.1.1.0"
└── migrations/
    └── 20.0.1.1.0/
        └── pre-renommer-note.py""", "Le dossier migrations"),
("code", """def migrate(cr, version):
    \"\"\"Avant la mise à jour : le champ note devient consigne, sans perdre les textes.\"\"\"
    cr.execute(\"\"\"
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'baobab_course' AND column_name = 'note'
    \"\"\")
    if cr.fetchone():
        cr.execute("ALTER TABLE baobab_course RENAME COLUMN note TO consigne")""", "migrations/20.0.1.1.0/pre-renommer-note.py"),
("liste", [
  "Le dossier porte le <b>numéro de la nouvelle version</b> : le script tourne quand la base passe d'une version plus ancienne à celle-ci, une seule fois.",
  "<code>pre-</code> : <b>avant</b> qu'Odoo charge le nouveau code (la colonne <code>note</code> existe encore). <code>post-</code> : <b>après</b> (les nouveaux champs existent, on peut utiliser l'ORM avec <code>odoo.api.Environment</code>). <code>end-</code> : à la toute fin de la mise à jour.",
  "<code>migrate(cr, version)</code> : <code>cr</code> exécute du SQL ; <code>version</code> est la version <b>installée avant</b> la mise à jour.",
  "On vérifie que la colonne existe : un script doit pouvoir tourner sans danger.",
]),
("code", """INFO migr odoo.modules.migration: module baobab_livraison: Running upgrade [>20.0.1.1.0] pre-renommer-note""", "Le journal pendant le -u : le script a tourné"),
("p", "Résultat : les textes sont toujours là, dans le champ <code>consigne</code>."),
("attention", "Sans changement de version, pas de migration", "Le script ne tourne que si la <code>version</code> du manifeste augmente. Oublier de passer de 20.0.1.0.0 à 20.0.1.1.0, c'est un script qui ne tourne jamais."),
("version", "Le mécanisme <code>migrations/&lt;version&gt;/pre-…py</code> est le même d'Odoo 12 à 20. Les migrations d'une version d'Odoo à une autre (de 17 à 20, par exemple) suivent la même idée à plus grande échelle : c'est l'objet du Bloc 6."),
],
exercice=[
("p", "Sur une base de test, crée deux courses avec une note (champ <code>note</code>, version 20.0.1.0.0). Renomme le champ en <code>consigne</code>, passe la version à 20.0.1.1.0, écris le script, puis <code>-u</code>. Vérifie dans le journal la ligne « Running upgrade » et à l'écran que les textes sont gardés. Bonus : refais l'essai <b>sans</b> script sur une copie de la base et regarde dans <code>psql</code> ce qu'est devenue la colonne <code>note</code>."),
],
retenir=[
  "Renommer un champ sans script = données perdues (la colonne est supprimée).",
  "<code>migrations/&lt;nouvelle version&gt;/pre-xxx.py</code> avec <code>def migrate(cr, version)</code>.",
  "<code>pre-</code> : avant le nouveau code (SQL) ; <code>post-</code> : après.",
  "Le script ne tourne que si la version du manifeste augmente.",
]),
quiz=[
("On renomme le champ note en consigne sans script de migration. Que deviennent les notes ?", [
  ("Elles sont perdues : la colonne note est supprimée", V, "Oui (vérifié sur Odoo 20)."),
  ("Odoo les copie dans consigne", F, "Non : Odoo ne devine pas qu'il s'agit d'un renommage."),
  ("Elles restent visibles", F, "Non."),
]),
("Quand tourne un script pre- placé dans migrations/20.0.1.1.0/ ?", [
  ("Au -u qui fait passer le module à la version 20.0.1.1.0, avant le chargement du nouveau code", V, "Oui."),
  ("À chaque redémarrage", F, "Non : une seule fois."),
  ("À l'installation sur une base neuve", F, "Non : il n'y a rien à migrer sur une base neuve."),
]),
("Ton script ne s'exécute pas au -u. Cause la plus probable ?", [
  ("La version du manifeste n'a pas été augmentée", V, "Oui."),
  ("Le script est en Python", F, "Non : c'est normal."),
  ("Le module a des données de démonstration", F, "Aucun rapport."),
]),
]),
]
