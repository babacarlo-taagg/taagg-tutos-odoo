"""Bloc 4 — Section « La sécurité » (section 2752, cours 211).
Vérifié sur Odoo 20.0 le 28/11/2026 : groupes Livreur / Responsable (res.groups.privilege), règles ir.access avec domaine,
connexion d'Ibou (livreur) dans Chromium (une seule course, menu Configuration caché, prix et boutons masqués), messages
AccessError recopiés, injection SQL démontrée sur une base de test, commande neutralize essayée sur une copie.
Leçon 4.3.6 : texte juridique à faire relire (loi n° 2008-12) ; aucune donnée réelle utilisée."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

GROUPES = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Le « privilège » regroupe les groupes de l'application dans la fiche utilisateur -->
    <record id="privilege_baobab" model="res.groups.privilege">
        <field name="name">Baobab Livraison</field>
        <field name="sequence">50</field>
    </record>

    <record id="group_livreur" model="res.groups">
        <field name="name">Livreur</field>
        <field name="sequence">10</field>
        <field name="privilege_id" ref="privilege_baobab"/>
        <field name="implied_ids" eval="[Command.link(ref('base.group_user'))]"/>
        <field name="comment">Voit et livre ses propres courses.</field>
        <field name="api_key_duration">90</field>
    </record>

    <record id="group_responsable" model="res.groups">
        <field name="name">Responsable</field>
        <field name="sequence">20</field>
        <field name="privilege_id" ref="privilege_baobab"/>
        <field name="implied_ids" eval="[Command.link(ref('group_livreur'))]"/>
        <field name="user_ids" eval="[Command.link(ref('base.user_root')), Command.link(ref('base.user_admin'))]"/>
        <field name="comment">Gère toutes les courses, les zones et les tarifs.</field>
    </record>
</odoo>"""

ACCES = """id,name,model_id,group_id/id,operation,domain
access_baobab_course_livreur,Courses : le livreur voit et modifie les siennes,baobab.course,group_livreur,ru,"[('livreur_id.user_ids', 'in', [user.id])]"
access_baobab_course_responsable,Courses : le responsable gère tout,baobab.course,group_responsable,crud,
access_baobab_zone_livreur,Zones : lecture livreur,baobab.zone,group_livreur,r,
access_baobab_zone_responsable,Zones : responsable,baobab.zone,group_responsable,crud,
access_baobab_etiquette_livreur,Étiquettes : lecture livreur,baobab.etiquette,group_livreur,r,
access_baobab_etiquette_responsable,Étiquettes : responsable,baobab.etiquette,group_responsable,crud,"""

LECONS = [
# ---------------------------------------------------------------- 4.3.1
dict(code="4.3.1", id=None, seq=31, minutes=10,
titre="Groupes d'utilisateurs",
description="Créer les groupes « Livreur » et « Responsable » et les donner aux utilisateurs.",
html=fiche(
objectif="créer les groupes Livreur et Responsable, et comprendre comment un groupe en inclut un autre.",
intro="Jusqu'ici, tout utilisateur interne avait tous les droits sur les courses. Chez Baobab, ce n'est pas possible : un livreur ne doit voir que ses courses et ne jamais toucher aux tarifs. Première étape : des <b>groupes</b>.",
corps=[
("code", GROUPES, "baobab_livraison/security/baobab_security.xml (en tête de data, avant ir.access.csv)"),
("tableau", ["Champ", "Rôle"], [
  ["<code>res.groups.privilege</code>", "regroupe les groupes d'une application : dans la fiche utilisateur, une liste « Baobab Livraison : Livreur / Responsable »"],
  ["<code>implied_ids</code>", "un groupe en inclut d'autres : un Responsable est aussi Livreur, un Livreur est aussi utilisateur interne"],
  ["<code>user_ids</code>", "les utilisateurs déjà membres (ici l'administrateur)"],
  ["<code>api_key_duration</code>", "durée maximale (en jours) des clés d'API de ce groupe : 90 pour l'appli des livreurs"],
]),
("p", "Vérifié dans la fiche de l'utilisateur Ibou Fall (Paramètres › Utilisateurs) : une ligne « Baobab Livraison » avec le choix Livreur ou Responsable."),
("version", "<b>Odoo 20</b> (et 19) : <code>privilege_id</code> vers un <code>res.groups.privilege</code>, et <code>user_ids</code>. <b>Odoo 18</b> : les groupes avaient un <code>category_id</code> (une catégorie de module) et un champ <code>users</code>. Un ancien fichier de groupes doit être adapté."),
("astuce", "Peu de groupes, bien nommés", "Deux ou trois groupes par application suffisent presque toujours. Nomme-les comme le métier (Livreur, Responsable), pas comme la technique (« groupe_ecriture »)."),
],
exercice=[
("p", "Crée le fichier des groupes, ajoute-le au manifeste avant <code>ir.access.csv</code>, mets à jour. Crée l'utilisateur Ibou Fall relié au contact du livreur, et donne-lui le groupe Livreur. Vérifie dans sa fiche que « Responsable » n'est pas coché."),
],
retenir=[
  "Un groupe = un rôle métier ; <code>implied_ids</code> pour l'héritage entre groupes.",
  "Odoo 19-20 : <code>res.groups.privilege</code> + <code>privilege_id</code> + <code>user_ids</code>.",
  "Le fichier des groupes avant celui des droits dans <code>data</code>.",
  "<code>api_key_duration</code> règle la durée des clés d'API du groupe.",
]),
quiz=[
("Comment faire qu'un Responsable ait automatiquement les droits d'un Livreur ?", [
  ("implied_ids du groupe Responsable contient le groupe Livreur", V, "Oui."),
  ("Copier toutes les lignes de droits du Livreur", F, "Inutile : implied_ids le fait."),
  ("Ce n'est pas possible", F, "Si."),
]),
("En Odoo 20, à quoi sert res.groups.privilege ?", [
  ("À regrouper les groupes d'une application dans la fiche utilisateur", V, "Oui."),
  ("À donner tous les droits", F, "Non."),
  ("À remplacer ir.access", F, "Non : les droits restent dans ir.access."),
]),
("Pourquoi le fichier des groupes doit-il être chargé avant ir.access.csv ?", [
  ("Parce que les lignes de droits font référence aux groupes", V, "Oui."),
  ("Pour aller plus vite", F, "Non."),
  ("L'ordre n'a pas d'importance", F, "Si."),
]),
]),

# ---------------------------------------------------------------- 4.3.2
dict(code="4.3.2", id=1362, seq=32, minutes=10,
titre="Droits d'accès : ir.access (20) et ir.model.access (18-19)",
description="Qui peut lire, créer, modifier, supprimer : les droits par groupe, et les messages d'erreur à reconnaître.",
html=fiche(
objectif="donner à chaque groupe exactement les opérations dont il a besoin, et reconnaître les erreurs de droits.",
intro="Au Bloc 2, une ligne donnait tout à tout le monde. Maintenant, chaque groupe reçoit juste ce qu'il faut : le Livreur lit et modifie, le Responsable fait tout.",
corps=[
("code", ACCES, "baobab_livraison/security/ir.access.csv"),
("tableau", ["Groupe", "Courses", "Zones, étiquettes"], [
  ["Livreur", "<code>ru</code> : lire et modifier (pour démarrer et livrer), <b>seulement les siennes</b> (colonne domain, leçon suivante)", "<code>r</code> : lire"],
  ["Responsable", "<code>crud</code> : tout", "<code>crud</code> : tout"],
]),
("p", "Le droit de modifier (<code>u</code>) est nécessaire au livreur : les boutons Démarrer et Livrée écrivent dans la course. Sans lui, même ses propres courses lui seraient refusées."),
("h", "Les messages à reconnaître (réels, Odoo 20)"),
("code", """You are not allowed to create 'Zone de livraison' (baobab.zone) records.

This operation is allowed for the following groups:
	- Baobab Livraison / Responsable

Contact your administrator to request access if necessary.""", "Ibou (livreur) essaie de créer une zone : le droit manque"),
("code", """Uh-oh! Looks like you have stumbled upon some top-secret records.

Sorry, Ibou Fall (id=8) doesn't have 'read' access to:
- Course de livraison (baobab.course)""", "Ibou essaie de lire la course d'un autre livreur : le domaine le refuse"),
("p", "Le premier message dit <b>quel groupe</b> a le droit : il manque une ligne de droits. Le second (avec son clin d'œil sur les cookies) dit que le droit existe, mais que <b>cette fiche</b> n'est pas autorisée : c'est le domaine."),
("version", "<b>Odoo 18 et 19</b> : fichier <code>security/ir.model.access.csv</code>, colonnes <code>id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink</code> avec des 1 et des 0 (<code>access_x,…,model_baobab_course,group_livreur,1,1,0,0</code>). <b>Odoo 20</b> : <code>security/ir.access.csv</code>, colonne <code>operation</code> en lettres (<code>ru</code>) et colonne <code>domain</code>. Ne recopie jamais un ancien fichier tel quel : le modèle <code>ir.model.access</code> n'existe plus et la base ne démarre pas."),
],
exercice=[
("p", "Écris les six lignes de droits, mets à jour, puis teste dans le terminal d'Odoo avec <code>with_user(ibou)</code> : lire les zones (permis), créer une zone (refusé), supprimer une de ses courses (refusé : pas de <code>d</code>). Note chaque message."),
],
retenir=[
  "Une ligne par groupe et par modèle ; <code>operation</code> = lettres c, r, u, d.",
  "Le droit minimum : le livreur a besoin de <code>u</code> pour ses boutons, pas de <code>c</code> ni <code>d</code>.",
  "« allowed for the following groups » = ligne de droits manquante ; « top-secret records » = domaine.",
  "Odoo 18-19 : <code>ir.model.access.csv</code> à 1/0 ; Odoo 20 : <code>ir.access.csv</code>.",
]),
quiz=[
("Le livreur doit pouvoir cliquer sur Démarrer et Livrée. Quelles opérations lui faut-il sur les courses ?", [
  ("r et u (lire et modifier)", V, "Oui : les boutons écrivent dans la course."),
  ("r seulement", F, "Les boutons échoueraient : ils modifient la course."),
  ("crud", F, "Trop : il pourrait créer et supprimer des courses."),
]),
("Message « This operation is allowed for the following groups: Baobab Livraison / Responsable ». Que manque-t-il ?", [
  ("Une ligne de droits pour le groupe de l'utilisateur (ou il n'est pas dans le bon groupe)", V, "Oui."),
  ("Un domaine", F, "Non : ce message vise l'opération, pas une fiche."),
  ("Une contrainte SQL", F, "Non."),
]),
("Un client en Odoo 18 : où sont les droits de son module ?", [
  ("Dans security/ir.model.access.csv, avec perm_read, perm_write… à 1 ou 0", V, "Oui."),
  ("Dans security/ir.access.csv avec la colonne operation", F, "C'est Odoo 20."),
  ("Dans le manifeste", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 4.3.3
dict(code="4.3.3", id=None, seq=33, minutes=10,
titre="Restreindre par fiche : un livreur ne voit que ses courses",
description="Le domaine dans ir.access (Odoo 20) ou une règle ir.rule (Odoo 18-19) pour limiter les fiches visibles.",
html=fiche(
objectif="faire qu'un livreur ne voie et ne modifie que ses propres courses, partout : écrans, API, rapports.",
intro="Ibou a le droit de lire les courses, mais pas celles de Moussa. Ce n'est plus une question d'opération (lire, modifier) mais de <b>fiches</b>. On ajoute un domaine au droit.",
corps=[
("code", """access_baobab_course_livreur,Courses : le livreur voit et modifie les siennes,baobab.course,group_livreur,ru,"[('livreur_id.user_ids', 'in', [user.id])]\"""", "La colonne domain de ir.access.csv"),
("liste", [
  "Le domaine s'écrit comme dans le code ; <code>user</code> est l'utilisateur connecté.",
  "<code>livreur_id.user_ids</code> : les comptes utilisateurs reliés au contact du livreur. Ibou Fall l'utilisateur est relié à Ibou Fall le contact.",
  "Les guillemets autour du domaine sont nécessaires dans le CSV (il contient des virgules).",
]),
("h", "Vérifié dans le navigateur, connecté en Ibou"),
("liste", [
  "La liste des courses n'affiche que BL/2026/0001, la sienne (alors que la base en contient bien d'autres).",
  "Par l'API JSON-2 avec la clé d'Ibou, <code>search_count</code> renvoie 1.",
  "Par l'API de l'appli, une course qui n'est pas à lui répond « Course introuvable ».",
]),
("p", "C'est la grande force de cette méthode : la règle s'applique <b>partout</b> (écrans, recherches, API, rapports, exports), sans que tu aies à y penser dans chaque contrôleur."),
("version", "<b>Odoo 18 et 19</b> : il fallait une <b>règle</b> à part, en XML : un enregistrement <code>ir.rule</code> avec <code>model_id</code>, <code>groups</code> et <code>domain_force</code>, en plus de la ligne de <code>ir.model.access.csv</code>. <b>Odoo 20</b> : le domaine est dans la même ligne que le droit. Le principe ne change pas : un droit dit « quelles opérations », un domaine dit « sur quelles fiches »."),
("attention", "Le Responsable n'a pas de domaine", "Les droits s'additionnent : un Responsable (qui est aussi Livreur) voit tout grâce à sa propre ligne sans domaine. Si tu ajoutes un domaine à la ligne du Responsable, il ne verra plus tout."),
],
exercice=[
("p", "Ajoute le domaine à la ligne du livreur. Crée un deuxième livreur (Moussa) avec une course. Connecte-toi en Ibou dans une fenêtre privée : il ne voit que la sienne. Connecte-toi en administrateur : tu vois tout. Écris le test qui vérifie que <code>search([])</code> en tant qu'Ibou ne renvoie que sa course."),
],
retenir=[
  "Droit = quelles opérations ; domaine = sur quelles fiches.",
  "Odoo 20 : colonne <code>domain</code> de <code>ir.access.csv</code>, avec <code>user</code>.",
  "Odoo 18-19 : une règle <code>ir.rule</code> (<code>domain_force</code>) en plus du droit.",
  "La règle s'applique partout : écrans, API, rapports.",
]),
quiz=[
("Comment limiter un livreur à ses propres courses en Odoo 20 ?", [
  ("Un domaine [('livreur_id.user_ids', 'in', [user.id])] dans sa ligne d'ir.access.csv", V, "Oui."),
  ("Un filtre par défaut dans la vue recherche", F, "Non : il suffit de l'enlever pour tout voir, et l'API n'est pas concernée."),
  ("Un sudo() dans le contrôleur", F, "C'est l'inverse : sudo enlève toute restriction."),
]),
("Le livreur appelle l'API JSON-2 avec sa clé : voit-il les courses des autres ?", [
  ("Non : le domaine s'applique aussi à l'API", V, "Oui (vérifié : 1 course)."),
  ("Oui, l'API ignore les règles", F, "Non."),
  ("Oui, en search_read seulement", F, "Non."),
]),
("Un client en Odoo 18 : comment faire la même chose ?", [
  ("Une règle ir.rule avec domain_force, en plus du droit dans ir.model.access.csv", V, "Oui."),
  ("Une colonne domain dans ir.model.access.csv", F, "Cette colonne n'existe pas avant Odoo 20."),
  ("Ce n'est pas possible en 18", F, "Si, avec ir.rule."),
]),
]),

# ---------------------------------------------------------------- 4.3.4
dict(code="4.3.4", id=None, seq=34, minutes=10,
titre="Protéger un champ ou un bouton",
description="groups=\"…\" sur les champs, les boutons et les menus : cacher le prix et la configuration aux livreurs.",
html=fiche(
objectif="cacher un champ, un bouton ou un menu à certains groupes, et savoir ce que cela protège vraiment.",
intro="Ibou n'a pas besoin de voir le prix de la course, ni le bouton Annuler, ni le menu Configuration. On les réserve au groupe Responsable avec l'attribut <code>groups</code>.",
corps=[
("code", """<button name="action_annuler" type="object" string="Annuler"
        invisible="state in ('livree', 'annulee')"
        groups="baobab_livraison.group_responsable"/>
…
<field name="prix" groups="baobab_livraison.group_responsable"/>""", "Formulaire de la course"),
("code", """<menuitem id="menu_baobab_config" name="Configuration" parent="menu_baobab_root" sequence="90"
          groups="baobab_livraison.group_responsable"/>""", "Menus"),
("p", "Vérifié, connecté en Ibou : le menu ne montre que « Courses », le formulaire n'a ni prix, ni bouton Annuler, ni bouton Demander le paiement. Connecté en administrateur (Responsable) : tout est là."),
("tableau", ["Où", "Effet de groups=…", "Protection réelle ?"], [
  ["sur un champ de <b>vue</b>", "le champ n'est pas envoyé à l'écran pour les autres", "à l'écran seulement : l'API peut encore le lire"],
  ["sur un <b>bouton</b>", "le bouton n'apparaît pas", "non : la méthode reste appelable par l'API si le droit d'écriture existe"],
  ["sur un <b>menu</b>", "le menu disparaît", "non : l'action reste accessible si les droits le permettent"],
  ["sur le champ <b>Python</b> : <code>fields.Monetary(…, groups=\"…\")</code>", "le champ n'existe pas pour les autres, même par l'API", "<b>oui</b>"],
]),
("attention", "La vraie protection est dans le Python et les droits", "Cacher un bouton est du confort. Pour interdire vraiment l'annulation aux livreurs, vérifie le groupe dans la méthode : <code>if not self.env.user.has_group(\"baobab_livraison.group_responsable\"): raise AccessError(…)</code>. Pour un champ sensible (un salaire, un numéro de pièce d'identité), mets <code>groups=</code> dans la définition Python du champ."),
],
exercice=[
("p", "Ajoute <code>groups</code> au prix, au bouton Annuler et au menu Configuration. Connecte-toi en Ibou et vérifie. Puis, avec la clé RPC d'Ibou, appelle <code>action_annuler</code> par JSON-2 : que se passe-t-il ? Ajoute la vérification <code>has_group</code> dans la méthode et recommence."),
],
retenir=[
  "<code>groups=\"module.groupe\"</code> sur champ, bouton, menu, page, dans les vues.",
  "Dans une vue, c'est du confort d'affichage, pas une sécurité.",
  "<code>groups=</code> sur le champ Python le cache aussi à l'API.",
  "Une action interdite se vérifie dans la méthode (<code>has_group</code>).",
]),
quiz=[
("Le bouton Annuler a groups=\"…group_responsable\". Un livreur peut-il annuler par l'API ?", [
  ("Oui, s'il a le droit de modifier et que la méthode ne vérifie rien", V, "Oui : d'où la vérification dans la méthode."),
  ("Non, jamais", F, "Le bouton caché ne protège pas la méthode."),
  ("Seulement en XML-RPC", F, "Non."),
]),
("Comment cacher vraiment un champ sensible, y compris à l'API ?", [
  ("groups=\"…\" dans la définition Python du champ", V, "Oui."),
  ("groups=\"…\" dans la vue seulement", F, "L'API pourrait encore le lire."),
  ("invisible=\"1\" dans la vue", F, "Non : il est seulement caché à l'écran."),
]),
("Comment vérifier dans une méthode que l'utilisateur est Responsable ?", [
  ("self.env.user.has_group(\"baobab_livraison.group_responsable\")", V, "Oui."),
  ("self.env.user.name == \"admin\"", F, "Non : on teste le rôle, jamais un nom."),
  ("self.env.su", F, "Non : su indique le mode super-utilisateur."),
]),
]),

# ---------------------------------------------------------------- 4.3.5
dict(code="4.3.5", id=2753, seq=35, minutes=10,
titre="Les erreurs de sécurité les plus courantes",
description="sudo mal placé, données exposées par une API ou une page publique, injection SQL, secrets dans le code.",
html=fiche(
objectif="reconnaître les cinq erreurs de sécurité qu'on trouve le plus souvent dans les modules Odoo, et savoir les corriger.",
intro="La plupart des failles ne viennent pas de pirates géniaux, mais de petites facilités dans le code. En relisant le module d'un collègue (ou le tien), cherche ces cinq erreurs en premier.",
corps=[
("h", "1. L'injection SQL"),
("code", """saisie = "x' OR '1'='1"
cr.execute(f"SELECT count(*) FROM baobab_course WHERE name = '{saisie}'")   # DANGER
→ 7   (toutes les courses !)
cr.execute("SELECT count(*) FROM baobab_course WHERE name = %s", [saisie])  # bon
→ 0
cr.execute(SQL("SELECT count(*) FROM baobab_course WHERE name = %s", saisie))  # bon (Odoo 20)
→ 0""", "Essai réel sur la base de test"),
("p", "Ne colle <b>jamais</b> une valeur dans une requête SQL avec f\"…\", + ou %. Passe-la en paramètre, ou utilise <code>from odoo.tools import SQL</code>, l'outil d'Odoo pour composer des requêtes sûres. Et d'abord : préfère l'ORM (<code>search</code>), qui applique aussi les droits."),
("h", "2. Le sudo() mal placé"),
("p", "<code>sudo()</code> dans une API ou une page publique, suivi d'un <code>search</code> large : tout le monde voit tout. Règle : <code>sudo()</code> seulement sur une opération précise, et ne renvoyer que les champs nécessaires (comme la page « Suivre mon colis » du Bloc 3)."),
("h", "3. Trop de données dans les réponses"),
("p", "Une API qui renvoie <code>course.read()</code> sans liste de champs envoie tout, y compris ce que l'appli n'affiche pas. Liste les champs publiés (<code>CHAMPS_PUBLIES</code> dans l'API des livreurs)."),
("h", "4. Les secrets dans le code"),
("p", "Clé d'API, mot de passe d'un serveur, secret d'un opérateur : jamais dans le code ni dans un fichier de données du module, car ils finissent dans Git. Ils vont dans les paramètres système (<code>get_str</code>), les variables d'environnement ou le fichier de configuration du serveur."),
("h", "5. Les adresses sans contrôle"),
("p", "Une route <code>auth=\"public\"</code> qui modifie des données sans vérifier qui appelle (webhook sans signature), ou <code>csrf=False</code> sur un formulaire du site. Chaque adresse publique doit répondre à la question : « et si un inconnu l'appelle ? »."),
("attention", "Les droits d'abord", "La plupart de ces erreurs sont rattrapées si les droits (leçons 4.3.2 et 4.3.3) sont justes et si le code utilise l'ORM avec les droits de l'utilisateur. La sécurité se construit en couches : droits, puis code prudent, puis tests."),
],
exercice=[
("p", "Relis ton module comme un auditeur. Cherche avec <code>grep -rn \"sudo()\\|cr.execute\\|csrf=False\\|auth=\\\"public\\\"\" .</code> et, pour chaque résultat, écris une ligne : « justifié parce que… » ou « à corriger ». Puis écris un test qui vérifie qu'une saisie <code>x' OR '1'='1</code> dans ta page de suivi ne renvoie rien."),
],
retenir=[
  "Jamais de valeur collée dans du SQL : paramètres ou <code>SQL()</code>, et l'ORM d'abord.",
  "<code>sudo()</code> : une opération précise, des champs choisis.",
  "Une API renvoie une liste de champs choisie.",
  "Secrets hors du code ; chaque adresse publique vérifie qui l'appelle.",
]),
quiz=[
("Quelle ligne est sûre ?", [
  ("cr.execute(\"SELECT id FROM baobab_course WHERE name = %s\", [nom])", V, "Oui : la valeur est passée en paramètre."),
  ("cr.execute(f\"SELECT id FROM baobab_course WHERE name = '{nom}'\")", F, "Injection SQL possible (vérifié : toutes les courses sortent)."),
  ("cr.execute(\"SELECT id FROM baobab_course WHERE name = '\" + nom + \"'\")", F, "Même faille."),
]),
("Une API publique fait sudo().search([]) puis renvoie read() sans liste de champs. Le problème ?", [
  ("Elle expose toutes les fiches et tous leurs champs à n'importe qui", V, "Oui."),
  ("Elle est trop lente, c'est tout", F, "C'est surtout une fuite de données."),
  ("Aucun problème", F, "Si."),
]),
("Où ranger la clé secrète d'un opérateur de paiement ?", [
  ("Dans un paramètre système ou la configuration du serveur", V, "Oui."),
  ("Dans une constante Python du module", F, "Elle serait dans Git."),
  ("Dans le README", F, "Encore pire."),
]),
]),

# ---------------------------------------------------------------- 4.3.6
dict(code="4.3.6", id=2754, seq=36, minutes=10,
titre="Données personnelles : ce que demande la loi sénégalaise",
description="Les obligations du développeur face à la loi n° 2008-12 et à la CDP : finalité, minimisation, sécurité, durée, droits des personnes.",
html=fiche(
objectif="connaître les règles de protection des données personnelles qui s'appliquent à ton travail de développeur au Sénégal, et les traduire en choix techniques.",
intro="Baobab Livraison enregistre des noms, des adresses, des téléphones, des paiements. Ce sont des <b>données personnelles</b>. Au Sénégal, leur utilisation est encadrée par la loi, et contrôlée par une autorité : la CDP. Le développeur n'est pas juriste, mais beaucoup d'obligations se jouent dans son code.",
corps=[
("h", "Le cadre"),
("liste", [
  "<b>Loi n° 2008-12 du 25 janvier 2008</b> sur la protection des données à caractère personnel, et son décret d'application n° 2008-721 du 30 juin 2008.",
  "<b>La CDP</b> (Commission de Protection des Données Personnelles) : l'autorité qui reçoit les déclarations et demandes d'autorisation, contrôle et peut sanctionner. Site : cdp.sn.",
  "Avant de traiter des données personnelles, l'entreprise (le <b>responsable du traitement</b>, ici Baobab) doit accomplir des formalités auprès de la CDP (déclaration, ou autorisation pour certains traitements sensibles).",
]),
("attention", "À vérifier pour chaque projet", "Cette fiche résume les grands principes ; elle ne remplace pas un juriste. Les textes évoluent (un projet de nouvelle loi est en discussion depuis plusieurs années) : vérifie toujours la version en vigueur sur cdp.sn, et fais valider le traitement par le responsable de l'entreprise cliente."),
("h", "Les principes, et ce qu'ils veulent dire dans Odoo"),
("tableau", ["Principe", "Dans ton code"], [
  ["<b>Finalité</b> : collecter pour un but précis", "chaque champ personnel sert la livraison ; pas de champ « au cas où »"],
  ["<b>Proportionnalité</b> (minimisation)", "pas de numéro de pièce d'identité du client pour livrer un colis ; la page publique ne montre que le statut"],
  ["<b>Sécurité et confidentialité</b>", "droits par groupe et par fiche (4.3.2, 4.3.3), pas de <code>sudo()</code> large, secrets hors du code, HTTPS"],
  ["<b>Durée de conservation limitée</b>", "une action planifiée qui anonymise ou archive les vieilles courses (par exemple après la durée fixée par l'entreprise)"],
  ["<b>Droits des personnes</b> : accès, rectification, opposition, suppression", "pouvoir retrouver et exporter toutes les données d'un client, les corriger, les effacer ou les anonymiser"],
  ["<b>Transferts hors du Sénégal</b> : encadrés", "savoir où est hébergé le serveur et où partent les données (service d'e-mail, opérateur de paiement) ; le signaler au client"],
]),
("h", "Les bons réflexes du développeur"),
("liste", [
  "<b>Jamais de vraies données sur ta machine ou en démonstration</b> : bases de test avec des données inventées (comme Awa Diop, Ibou Fall).",
  "<b>Une copie de la base d'un client se neutralise</b> avant tout : <code>python3 odoo-bin neutralize -c odoo.conf -d copie_client</code>. Vérifié sur Odoo 20 : la commande coupe les serveurs d'envoi d'e-mails (et efface leurs mots de passe), en ajoute un faux qui n'envoie rien, et arrête les actions planifiées. Odoo 20 propose aussi <code>odoo-bin obfuscate</code> pour brouiller des champs d'une copie.",
  "<b>Pas de données personnelles dans les journaux</b> ni dans les messages d'erreur renvoyés par une API.",
  "<b>Prévenir le client</b> quand ton module crée un nouveau traitement (nouvelles données, nouvel outil externe) : c'est à lui de mettre ses formalités à jour auprès de la CDP.",
]),
],
exercice=[
("p", "Fais l'inventaire des données personnelles de Baobab Livraison (modèle, champ, pourquoi on en a besoin, qui peut le voir). Repère un champ dont on pourrait se passer. Puis écris l'action planifiée qui, pour les courses livrées depuis plus d'un an, remplace la consigne par « (supprimée) » : c'est un premier pas vers une durée de conservation."),
],
retenir=[
  "Sénégal : loi n° 2008-12 et la CDP ; formalités par l'entreprise avant le traitement.",
  "Finalité, minimisation, sécurité, durée limitée, droits des personnes.",
  "Jamais de vraies données en test ; une copie se neutralise (<code>odoo-bin neutralize</code>).",
  "Vérifier le texte en vigueur sur cdp.sn et faire valider par un juriste.",
]),
quiz=[
("Quelle autorité contrôle la protection des données personnelles au Sénégal ?", [
  ("La CDP (Commission de Protection des Données Personnelles)", V, "Oui."),
  ("L'ARTP", F, "Non : elle régule les télécommunications et les postes."),
  ("Odoo S.A.", F, "Non."),
]),
("Tu reçois une copie de la base d'un client pour corriger un bogue. Premier réflexe ?", [
  ("La neutraliser (odoo-bin neutralize) avant de la lancer", V, "Oui : sinon elle peut envoyer de vrais e-mails et lancer des tâches."),
  ("La lancer tout de suite pour voir le bogue", F, "Risque d'envoyer des e-mails aux vrais clients."),
  ("La partager avec un collègue par e-mail", F, "Surtout pas : ce sont des données personnelles."),
]),
("La page « Suivre mon colis » affiche le statut mais pas le nom du client. Quel principe est appliqué ?", [
  ("La proportionnalité (minimisation)", V, "Oui : ne montrer que le nécessaire."),
  ("La durée de conservation", F, "Non."),
  ("Le transfert hors du pays", F, "Non."),
]),
]),
]
