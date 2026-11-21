"""Bloc 1 — Section « Les bases de données » (section 2705, cours 208).
Requêtes testées sur PostgreSQL 16 et une base Odoo 20.0 le 21/11/2026."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

LECONS = [
# ---------------------------------------------------------------- 1.3.1
dict(code="1.3.1", id=None, seq=41, minutes=10,
titre="Installer PostgreSQL, créer un utilisateur et une base",
description="Installer PostgreSQL 16, créer ton utilisateur et te connecter avec psql.",
html=fiche(
objectif="installer PostgreSQL, créer ton utilisateur PostgreSQL et te connecter à une base avec <code>psql</code>.",
intro="Odoo ne garde rien dans des fichiers : contacts, ventes, courses… tout est rangé dans une base de données <b>PostgreSQL</b>. C'est le deuxième pilier de ton poste de travail, après Python.",
corps=[
("h", "Installer"),
("code", """sudo apt update
sudo apt install postgresql postgresql-client
psql --version
psql (PostgreSQL) 16.10""", "Terminal Ubuntu 24.04 (la dernière ligne est un exemple de résultat)"),
("version", "Odoo 19 demandait PostgreSQL 13 au minimum. <b>Odoo 20 exige PostgreSQL 16</b> ou plus récent. Ubuntu 24.04 installe justement la version 16. Sur un serveur plus ancien, il faudra installer une version plus récente de PostgreSQL avant de passer à Odoo 20."),
("h", "Créer ton utilisateur PostgreSQL"),
("p", "Après l'installation, PostgreSQL n'a qu'un seul utilisateur : <code>postgres</code>. Odoo refuse de s'y connecter (c'est l'administrateur, trop puissant). On crée donc un utilisateur qui porte <b>le même nom que ton utilisateur Ubuntu</b> :"),
("code", """sudo -u postgres createuser -d -R -S $USER
createdb $USER""", "Terminal (commandes de la documentation officielle d'Odoo)"),
("liste", [
  "<code>-d</code> : il peut créer des bases (Odoo en a besoin) ;",
  "<code>-R</code> : il ne peut pas créer d'autres utilisateurs ;",
  "<code>-S</code> : ce n'est pas un super-administrateur ;",
  "<code>$USER</code> est remplacé automatiquement par ton nom d'utilisateur Ubuntu.",
]),
("p", "Comme les deux noms sont identiques, tu te connectes <b>sans mot de passe</b> depuis ta machine."),
("h", "Se connecter avec psql"),
("code", """psql                     # se connecte à la base qui porte ton nom
psql -d baobab_sql       # se connecte à une autre base""", "Terminal"),
("tableau", ["Dans psql", "Effet"], [
  ["<code>\\l</code>", "lister les bases"],
  ["<code>\\dt</code>", "lister les tables de la base"],
  ["<code>\\d nom_table</code>", "décrire une table (ses colonnes)"],
  ["<code>\\q</code>", "quitter"],
]),
("attention", "Les points-virgules", "Une requête SQL se termine par <code>;</code>. Si psql affiche <code>baobab_sql-&gt;</code> au lieu de <code>baobab_sql=&gt;</code>, c'est qu'il attend la fin de ta requête : tape <code>;</code> et Entrée."),
],
exercice=[
("p", "Installe PostgreSQL, crée ton utilisateur, puis crée la base d'entraînement de la section :"),
("code", """createdb baobab_sql
psql -d baobab_sql""", "Terminal"),
("p", "Dans psql, tape <code>\\l</code> et repère ta base dans la liste, puis <code>\\q</code>. Note le résultat de <code>psql --version</code> dans ton carnet."),
],
retenir=[
  "Odoo range toutes ses données dans PostgreSQL ; Odoo 20 demande PostgreSQL 16 ou plus.",
  "<code>sudo -u postgres createuser -d -R -S $USER</code> crée ton utilisateur ; Odoo refuse l'utilisateur <code>postgres</code>.",
  "<code>psql -d base</code> pour se connecter ; <code>\\l</code>, <code>\\dt</code>, <code>\\d</code>, <code>\\q</code>.",
  "Une requête SQL se termine par un point-virgule.",
]),
quiz=[
("Quelle version minimale de PostgreSQL demande Odoo 20 ?", [
  ("PostgreSQL 16", V, "Oui. Odoo 19 acceptait encore PostgreSQL 13."),
  ("PostgreSQL 9.6", F, "Non : beaucoup trop ancien."),
  ("N'importe laquelle", F, "Non : Odoo 20 vérifie la version minimale."),
]),
("Pourquoi crée-t-on un utilisateur PostgreSQL au nom de son utilisateur Ubuntu ?", [
  ("Parce qu'Odoo refuse l'utilisateur postgres, et qu'avec le même nom on se connecte sans mot de passe en local", V, "Oui."),
  ("Parce que PostgreSQL ne fonctionne pas sans cela", F, "Non : PostgreSQL fonctionne, mais Odoo refuse l'utilisateur postgres."),
  ("Pour pouvoir supprimer l'utilisateur postgres", F, "Non : on ne le supprime pas."),
]),
("Dans psql, quelle commande liste les tables de la base ?", [
  ("\\dt", V, "Oui."),
  ("\\l", F, "Non : \\l liste les bases."),
  ("SHOW TABLES;", F, "Non : c'est la commande de MySQL, pas de PostgreSQL."),
]),
]),

# ---------------------------------------------------------------- 1.3.2
dict(code="1.3.2", id=1354, seq=42, minutes=10,
titre="Tables, lignes, colonnes : lire des données avec SELECT",
description="Créer les tables zone et course, puis les interroger avec SELECT, WHERE et ORDER BY.",
html=fiche(
objectif="comprendre ce qu'est une table et écrire des requêtes <code>SELECT</code> avec <code>WHERE</code> et <code>ORDER BY</code>.",
intro="Une base de données, c'est un ensemble de <b>tables</b>, comme des feuilles de tableur très strictes. Chaque table a des <b>colonnes</b> (les informations) et des <b>lignes</b> (les fiches). On leur parle en SQL.",
corps=[
("h", "Créer deux tables pour Baobab Livraison"),
("code", """CREATE TABLE zone (
    id SERIAL PRIMARY KEY,               -- numéro unique, donné automatiquement
    nom VARCHAR(50) NOT NULL UNIQUE,     -- texte obligatoire, sans doublon
    tarif INTEGER NOT NULL
);

CREATE TABLE course (
    id SERIAL PRIMARY KEY,
    client VARCHAR(100) NOT NULL,
    zone_id INTEGER REFERENCES zone(id), -- lien vers la table zone
    poids NUMERIC(5,2),
    date_course DATE DEFAULT CURRENT_DATE,
    livree BOOLEAN DEFAULT FALSE
);

INSERT INTO zone (nom, tarif) VALUES
    ('Plateau', 1000), ('Médina', 1000), ('Mermoz', 1500),
    ('Parcelles Assainies', 2000), ('Rufisque', 3000);

INSERT INTO course (client, zone_id, poids) VALUES
    ('Awa Diop', 3, 3.5), ('Moussa Ndiaye', 1, 8),
    ('Fatou Sarr', 5, 12), ('Ibou Fall', 3, 1);""", "psql -d baobab_sql (copie-colle ce bloc)"),
("p", "Le <code>id</code> est la <b>clé primaire</b> : un numéro unique par ligne. <code>zone_id</code> est une <b>clé étrangère</b> : il contient le <code>id</code> d'une ligne de la table <code>zone</code>. Les lignes qui commencent par <code>--</code> sont des commentaires."),
("h", "Lire avec SELECT"),
("code", """SELECT * FROM zone;                          -- toutes les colonnes, toutes les lignes
SELECT nom, tarif FROM zone WHERE tarif >= 1500 ORDER BY tarif DESC;
SELECT client, poids FROM course WHERE poids > 5 ORDER BY poids;
SELECT COUNT(*) FROM course;                 -- combien de courses ?
SELECT client FROM course WHERE client LIKE 'A%';   -- clients qui commencent par A""", "psql"),
("code", """         nom         | tarif
---------------------+-------
 Rufisque            |  3000
 Parcelles Assainies |  2000
 Mermoz              |  1500
(3 rows)""", "Résultat de la 2e requête"),
("liste", [
  "<code>WHERE</code> filtre les lignes ; <code>AND</code>, <code>OR</code> combinent les conditions.",
  "<code>ORDER BY</code> trie ; <code>DESC</code> pour l'ordre décroissant.",
  "Les textes s'écrivent entre <b>apostrophes simples</b> : <code>'Mermoz'</code>.",
]),
("astuce", "Pourquoi apprendre le SQL si Odoo le fait pour moi ?", "Odoo écrit le SQL à ta place, c'est vrai. Mais pour comprendre une lenteur, vérifier des données après une migration ou faire une analyse rapide, le consultant technique lit la base directement. Et le vocabulaire (table, clé, jointure) revient tout le temps dans Odoo."),
],
exercice=[
("p", "Dans <code>baobab_sql</code>, écris les requêtes qui affichent : (1) les zones dont le tarif est de 1 000 F ; (2) les courses de plus de 3 kg, de la plus lourde à la plus légère ; (3) le nombre de zones."),
],
retenir=[
  "Une table = des colonnes (informations) et des lignes (fiches).",
  "<code>id</code> = clé primaire ; <code>zone_id</code> = clé étrangère vers une autre table.",
  "<code>SELECT colonnes FROM table WHERE condition ORDER BY colonne;</code>",
  "Texte entre apostrophes simples, requête terminée par <code>;</code>.",
]),
quiz=[
("Que fait SELECT nom FROM zone WHERE tarif > 1000; ?", [
  ("Elle affiche le nom des zones dont le tarif dépasse 1 000", V, "Oui."),
  ("Elle supprime les zones à plus de 1 000", F, "Non : SELECT ne fait que lire."),
  ("Elle modifie le tarif des zones", F, "Non : c'est le rôle de UPDATE."),
]),
("Dans la table course, à quoi sert la colonne zone_id ?", [
  ("À relier chaque course à une ligne de la table zone", V, "Oui : c'est une clé étrangère."),
  ("À numéroter les courses", F, "Non : c'est le rôle de id, la clé primaire."),
  ("À stocker le nom de la zone en texte", F, "Non : elle stocke le numéro (id) de la zone."),
]),
("Comment trier les zones du tarif le plus élevé au plus bas ?", [
  ("ORDER BY tarif DESC", V, "Oui."),
  ("ORDER BY tarif", F, "Non : sans DESC, l'ordre est croissant."),
  ("WHERE tarif DESC", F, "Non : WHERE sert à filtrer, pas à trier."),
]),
]),

# ---------------------------------------------------------------- 1.3.3
dict(code="1.3.3", id=None, seq=43, minutes=10,
titre="Écrire et relier : INSERT, UPDATE, DELETE et les jointures",
description="Modifier des données en SQL et relier deux tables avec JOIN.",
html=fiche(
objectif="ajouter, modifier et supprimer des lignes, puis relier deux tables avec une jointure.",
intro="Lire ne suffit pas : il faut savoir modifier. Et surtout, savoir <b>relier</b> les tables entre elles : c'est le principe de toute base de données, et d'Odoo.",
corps=[
("h", "Ajouter, modifier, supprimer"),
("code", """INSERT INTO course (client, zone_id, poids) VALUES ('Khady Ba', 2, 2);

UPDATE course SET livree = TRUE WHERE client = 'Awa Diop';

DELETE FROM course WHERE client = 'Ibou Fall';""", "psql -d baobab_sql"),
("attention", "N'oublie jamais le WHERE", "<code>UPDATE course SET livree = TRUE;</code> sans <code>WHERE</code> marque <b>toutes</b> les courses comme livrées. <code>DELETE FROM course;</code> les supprime toutes. Écris toujours le <code>WHERE</code> en premier, et vérifie-le avec un <code>SELECT</code> avant."),
("h", "La base protège ses liens"),
("code", """INSERT INTO course (client, zone_id) VALUES ('Test', 99);
ERROR:  insert or update on table "course" violates foreign key constraint "course_zone_id_fkey"
DETAIL:  Key (zone_id)=(99) is not present in table "zone".""", "psql"),
("p", "La zone 99 n'existe pas : PostgreSQL refuse. C'est la <b>contrainte de clé étrangère</b>. Odoo crée ces contraintes pour toi sur chaque champ relationnel (Many2one)."),
("h", "Relier deux tables : JOIN"),
("code", """SELECT c.client, z.nom AS zone, z.tarif
FROM course c
JOIN zone z ON z.id = c.zone_id
ORDER BY z.tarif, c.client;""", "psql"),
("code", """    client     |   zone   | tarif
---------------+----------+-------
 Khady Ba      | Médina   |  1000
 Moussa Ndiaye | Plateau  |  1000
 Awa Diop      | Mermoz   |  1500
 Fatou Sarr    | Rufisque |  3000""", "Résultat (après l'ajout de Khady Ba et la suppression d'Ibou Fall)"),
("p", "<code>course c</code> et <code>zone z</code> donnent un surnom court à chaque table. <code>ON z.id = c.zone_id</code> dit comment les relier."),
("h", "Compter par groupe : GROUP BY"),
("code", """SELECT z.nom, COUNT(c.id) AS nb_courses
FROM zone z
LEFT JOIN course c ON c.zone_id = z.id
GROUP BY z.nom
ORDER BY nb_courses DESC, z.nom;""", "psql"),
("code", """         nom         | nb_courses
---------------------+------------
 Mermoz              |          1
 Médina              |          1
 Plateau             |          1
 Rufisque            |          1
 Parcelles Assainies |          0""", "Résultat"),
("p", "<code>LEFT JOIN</code> garde aussi les zones <b>sans</b> course (avec 0). Avec un simple <code>JOIN</code>, elles disparaîtraient du résultat."),
("astuce", "Dans Odoo", "Quand tu écriras <code>course.zone_id.nom</code> en Python, Odoo fera cette jointure pour toi. Et les vues « Regrouper par » des listes d'Odoo font des <code>GROUP BY</code>."),
],
exercice=[
("p", "1. Ajoute deux courses pour Parcelles Assainies. 2. Marque comme livrées toutes les courses de Mermoz (vérifie d'abord avec un <code>SELECT</code> les lignes concernées). 3. Écris une requête qui affiche, pour chaque course, le client, la zone et le tarif, seulement pour les courses non livrées."),
],
retenir=[
  "<code>INSERT</code> ajoute, <code>UPDATE … SET … WHERE</code> modifie, <code>DELETE … WHERE</code> supprime.",
  "Toujours un <code>WHERE</code>, vérifié d'abord avec un <code>SELECT</code>.",
  "<code>JOIN … ON</code> relie deux tables ; <code>LEFT JOIN</code> garde aussi les lignes sans correspondance.",
  "<code>GROUP BY</code> regroupe pour compter ou additionner.",
]),
quiz=[
("Que fait UPDATE course SET livree = TRUE; (sans WHERE) ?", [
  ("Elle marque TOUTES les courses comme livrées", V, "Oui : c'est l'erreur à ne jamais faire."),
  ("Elle ne fait rien sans WHERE", F, "Non : elle s'applique à toutes les lignes."),
  ("Elle marque seulement la dernière course", F, "Non."),
]),
("PostgreSQL refuse une course avec zone_id = 99. Pourquoi ?", [
  ("Parce que la zone 99 n'existe pas : la contrainte de clé étrangère bloque", V, "Oui."),
  ("Parce que 99 est un nombre trop grand", F, "Non."),
  ("Parce que la table course est pleine", F, "Non."),
]),
("Quelle différence entre JOIN et LEFT JOIN zone → course ?", [
  ("LEFT JOIN garde aussi les zones qui n'ont aucune course", V, "Oui."),
  ("Aucune différence", F, "Si : JOIN fait disparaître les zones sans course."),
  ("LEFT JOIN trie le résultat", F, "Non : le tri se fait avec ORDER BY."),
]),
]),

# ---------------------------------------------------------------- 1.3.4
dict(code="1.3.4", id=2706, seq=44, minutes=10,
titre="PostgreSQL et Odoo : comment Odoo range ses données",
description="Retrouver dans PostgreSQL les modèles, champs et relations d'Odoo, en lecture seule.",
html=fiche(
objectif="retrouver dans PostgreSQL comment Odoo range ses données, sans jamais les modifier directement.",
intro="Maintenant que tu parles SQL, ouvrons une vraie base Odoo pour voir ce qu'il y a dedans. Tu vas reconnaître tout ce qu'on vient d'apprendre.",
corps=[
("h", "Un modèle Odoo = une table"),
("tableau", ["Dans Odoo (Python)", "Dans PostgreSQL"], [
  ["Modèle <code>res.partner</code>", "Table <code>res_partner</code> (les points deviennent des tirets bas)"],
  ["Champ <code>name</code>", "Colonne <code>name</code>"],
  ["Champ Many2one <code>company_id</code>", "Colonne <code>company_id</code> (un id) + clé étrangère"],
  ["Champ Many2many", "Une table de liaison, par exemple <code>res_groups_users_rel</code>"],
  ["Champ One2many", "Aucune colonne : c'est l'autre côté d'un Many2one"],
]),
("h", "Regardons une base Odoo 20"),
("code", """psql -d baobab_dev
SELECT id, name, email, active FROM res_partner ORDER BY id LIMIT 4;""", "Terminal (base créée dans la section suivante)"),
("code", """ id |      name      |        email         | active
----+----------------+----------------------+--------
  1 | YourCompany    | info@yourcompany.com | t
  2 | System         | odoobot@example.com  | f
  3 | Mitchell Admin | admin@example.com    | t
  4 | Public user    |                      | f""", "Résultat sur une base Odoo 20 neuve"),
("p", "Toutes les tables d'Odoo ont aussi quatre colonnes automatiques : <code>create_date</code>, <code>create_uid</code> (qui a créé), <code>write_date</code>, <code>write_uid</code> (qui a modifié en dernier). Et <code>active = f</code> veut dire « archivé » : Odoo cache la fiche sans la supprimer."),
("h", "Les tables qui décrivent Odoo lui-même"),
("code", """SELECT name, state FROM ir_module_module WHERE state = 'installed' ORDER BY name;
SELECT model FROM ir_model WHERE model LIKE 'res.%' ORDER BY model;
SELECT module, name, model, res_id FROM ir_model_data WHERE model = 'res.partner' LIMIT 3;""", "psql"),
("liste", [
  "<code>ir_module_module</code> : les modules et leur état (installé ou non).",
  "<code>ir_model</code> : la liste des modèles.",
  "<code>ir_model_data</code> : les <b>identifiants externes</b> (par exemple <code>base.main_partner</code>) qui permettent à un module de retrouver « sa » fiche. On s'en servira beaucoup au Bloc 2.",
]),
("version", "Depuis Odoo 16, les textes traduisibles sont rangés en JSON, une valeur par langue. Par exemple la colonne <code>name</code> de <code>ir_model</code> contient <code>{\"en_US\": \"Contact\"}</code> : on lit <code>name-&gt;&gt;'en_US'</code> en SQL."),
("attention", "Règle d'or : lecture seule", "On ne modifie <b>jamais</b> une base Odoo en SQL (<code>UPDATE</code>, <code>DELETE</code>) : on contournerait les règles, les calculs, les droits et l'historique d'Odoo. On lit en SQL, on modifie avec Odoo (écran, code Python ou API). Et on ne fait jamais ces essais sur la base d'un client."),
],
exercice=[
("p", "Une fois ta base <code>baobab_dev</code> créée (leçon « Installer Odoo 20 »), reviens ici et trouve en SQL : (1) le nombre de modules installés ; (2) le nom et l'e-mail du contact dont l'identifiant externe est <code>base.partner_admin</code> (indice : relie <code>ir_model_data</code> et <code>res_partner</code> avec un <code>JOIN</code> sur <code>res_id</code>)."),
],
retenir=[
  "Un modèle <code>a.b</code> devient la table <code>a_b</code> ; un champ devient une colonne.",
  "Many2one = colonne + clé étrangère ; Many2many = table de liaison ; One2many = pas de colonne.",
  "<code>active = false</code> veut dire archivé ; <code>ir_model_data</code> contient les identifiants externes.",
  "On lit une base Odoo en SQL, on ne la modifie jamais en SQL.",
]),
quiz=[
("Comment s'appelle dans PostgreSQL la table du modèle Odoo res.partner ?", [
  ("res_partner", V, "Oui : les points deviennent des tirets bas."),
  ("res.partner", F, "Non : un point n'est pas permis dans un nom de table."),
  ("partner", F, "Non."),
]),
("Un champ One2many crée-t-il une colonne dans la table ?", [
  ("Non : c'est l'autre côté d'un Many2one, rangé dans l'autre table", V, "Oui."),
  ("Oui, une colonne qui contient une liste d'id", F, "Non : PostgreSQL ne range pas de liste dans une colonne pour cela."),
  ("Oui, une table de liaison", F, "Non : la table de liaison, c'est pour le Many2many."),
]),
("Un client te demande de corriger 300 prix directement en SQL sur sa base. Que réponds-tu ?", [
  ("Non : on corrige avec Odoo (import, code ou API), jamais en SQL sur sa base", V, "Oui : le SQL contournerait les règles, les calculs et l'historique."),
  ("D'accord, c'est plus rapide", F, "Rapide, mais dangereux : tu contournes toute la logique d'Odoo."),
  ("D'accord, mais seulement le soir", F, "L'heure ne change rien au danger."),
]),
]),
]
