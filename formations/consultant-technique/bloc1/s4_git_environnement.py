"""Bloc 1 — Section « Git et l'environnement » (section 2707, cours 208).
Testé le 21/11/2026 : Git 2.43, Odoo 20.0 depuis les sources (Python 3.12, PostgreSQL 16, Ubuntu 24.04),
image Docker officielle odoo:20 + postgres:16, debugpy 1.8. Non testé ici : l'interface de VS Code et GitHub en ligne."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

LECONS = [
# ---------------------------------------------------------------- 1.4.1
dict(code="1.4.1", id=2708, seq=51, minutes=10,
titre="Git : dépôt, commit, historique",
description="Créer le dépôt baobab_livraison et enregistrer ton travail étape par étape.",
html=fiche(
objectif="créer un dépôt Git, enregistrer des versions de ton travail (commits) et relire l'historique.",
intro="Git est un « appareil photo » pour ton code : à chaque étape importante, tu prends une photo (un <b>commit</b>). Si tu casses quelque chose, tu reviens à la photo d'avant. Toutes les équipes Odoo du monde travaillent avec Git.",
corps=[
("h", "Installer et se présenter (une seule fois)"),
("code", """sudo apt install git
git config --global user.name "Awa Diop"
git config --global user.email "awa@example.com"
git config --global init.defaultBranch main""", "Terminal (mets ton nom et ton e-mail)"),
("h", "Créer le dépôt de Baobab Livraison"),
("code", """mkdir -p ~/baobab_livraison
cd ~/baobab_livraison
git init
cp ~/baobab/scripts/tarifs.py .      # ton script de la leçon 1.0.6
git status""", "Terminal"),
("code", """Untracked files:
        tarifs.py""", "Git voit le fichier mais ne le suit pas encore"),
("h", "Les trois gestes de base"),
("code", """git add tarifs.py                              # 1. préparer : « je veux photographier ce fichier »
git commit -m "Ajoute le calcul du prix d'une course"   # 2. photographier, avec un message
git log --oneline                              # 3. relire l'historique
bb7964f Ajoute le calcul du prix d'une course""", "Terminal"),
("p", "Modifie <code>tarifs.py</code> (ajoute une zone), puis :"),
("code", """git diff                 # ce qui a changé depuis le dernier commit
git commit -am "Ajoute la zone Pikine"   # -a : ajoute tous les fichiers déjà suivis
git log --oneline""", "Terminal"),
("h", "Écrire de bons messages"),
("tableau", ["Mauvais message", "Bon message"], [
  ["<code>modif</code>", "<code>Ajoute le supplément de poids au-delà de 5 kg</code>"],
  ["<code>correction</code>", "<code>Corrige l'arrondi du prix pour Rufisque</code>"],
  ["<code>wip</code>", "<code>Crée le modèle baobab.zone</code>"],
]),
("p", "Un commit = une seule idée, avec un message qui dit <b>ce que fait</b> le changement. Fais des petits commits, souvent."),
("astuce", "Revenir en arrière", "<code>git restore tarifs.py</code> annule les modifications pas encore committées d'un fichier. Pour revoir un ancien état : <code>git show bb7964f</code>."),
],
exercice=[
("p", "Crée le dépôt <code>~/baobab_livraison</code>, ajoute <code>tarifs.py</code>, fais un premier commit. Puis fais trois petits commits successifs : ajout de la zone Pikine (2 500 F), ajout d'une fonction <code>en_francs</code>, correction d'une faute dans un commentaire. Affiche l'historique avec <code>git log --oneline</code>."),
],
retenir=[
  "Un dépôt Git garde toutes les versions de ton code.",
  "<code>git add</code> prépare, <code>git commit -m \"…\"</code> enregistre, <code>git log</code> montre l'historique.",
  "<code>git status</code> et <code>git diff</code> : à taper sans modération.",
  "Petits commits, une idée chacun, message clair.",
]),
quiz=[
("Dans quel ordre enregistre-t-on une modification avec Git ?", [
  ("git add, puis git commit", V, "Oui : on prépare, puis on enregistre."),
  ("git commit, puis git add", F, "Non : un commit enregistre ce qui a été préparé avec add."),
  ("git log, puis git commit", F, "Non : git log ne fait que lire l'historique."),
]),
("Quelle commande montre ce qui a changé depuis le dernier commit ?", [
  ("git diff", V, "Oui."),
  ("git init", F, "Non : git init crée un dépôt."),
  ("git config", F, "Non : git config règle tes préférences."),
]),
("Quel message de commit est le meilleur ?", [
  ("Ajoute le supplément de poids au-delà de 5 kg", V, "Oui : on comprend ce que fait le changement."),
  ("modif", F, "Trop vague : dans un mois, personne ne saura ce que c'était."),
  ("travail du mardi", F, "Ne dit rien du contenu."),
]),
]),

# ---------------------------------------------------------------- 1.4.2
dict(code="1.4.2", id=None, seq=52, minutes=10,
titre="Branches et fusion",
description="Travailler sur une nouvelle fonction sans casser ce qui marche, puis la fusionner.",
html=fiche(
objectif="créer une branche pour une nouvelle fonction, la fusionner dans <code>main</code> et résoudre un conflit simple.",
intro="Imagine : tu ajoutes une nouvelle règle de prix, mais le client a besoin d'une correction urgente sur la version actuelle. Avec les <b>branches</b>, tu peux travailler sur plusieurs choses à la fois sans les mélanger.",
corps=[
("h", "Créer une branche"),
("code", """git switch -c supplement-poids        # crée la branche et s'y place
# ... tu modifies tarifs.py ...
git commit -am "Ajoute le supplément de poids"
git switch main                       # retour sur main : ton changement n'y est pas encore
git branch                            # liste des branches, * = branche actuelle""", "Terminal"),
("h", "Fusionner"),
("code", """git switch main
git merge supplement-poids             # apporte les commits de la branche dans main
git log --oneline --graph
git branch -d supplement-poids         # la branche a servi, on la supprime""", "Terminal"),
("h", "Le conflit : quand deux branches changent la même ligne"),
("p", "Sur une branche, le tarif de Mermoz passe à 1 600 F ; sur <code>main</code>, à 1 700 F. À la fusion :"),
("code", """git merge branche-a
CONFLICT (content): Merge conflict in tarifs.py
Automatic merge failed; fix conflicts and then commit the result.""", "Terminal"),
("p", "Git ne choisit pas à ta place. Il marque l'endroit dans le fichier :"),
("code", """<<<<<<< HEAD
TARIFS = {"Plateau": 1000, "Mermoz": 1700}
=======
TARIFS = {"Plateau": 1000, "Mermoz": 1600}
>>>>>>> branche-a""", "tarifs.py"),
("liste", [
  "Entre <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> et <code>=======</code> : la version de la branche où tu es (<code>main</code>).",
  "Entre <code>=======</code> et <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> : la version qui arrive.",
  "Tu gardes la bonne ligne, tu supprimes les marques, puis <code>git add tarifs.py</code> et <code>git commit</code>.",
  "Pour tout annuler : <code>git merge --abort</code>.",
]),
("astuce", "Éviter les conflits", "Des branches courtes (un ou deux jours), des commits fréquents, et récupérer souvent le travail des autres. Les conflits sont normaux en équipe : ils ne sont graves que si on les règle sans réfléchir."),
],
exercice=[
("p", "Dans <code>~/baobab_livraison</code> : (1) crée une branche <code>zone-yoff</code>, ajoute la zone Yoff à 1 500 F, committe, fusionne dans <code>main</code>. (2) Provoque volontairement un conflit sur le tarif du Plateau entre deux branches, résous-le en gardant 1 100 F, et termine la fusion."),
],
retenir=[
  "<code>git switch -c nom</code> crée une branche ; <code>git switch main</code> revient sur main.",
  "<code>git merge nom</code> fusionne une branche dans celle où tu te trouves.",
  "Conflit : choisir la bonne version, retirer les marques, <code>git add</code>, <code>git commit</code>.",
  "<code>git merge --abort</code> annule une fusion en cours.",
]),
quiz=[
("Quelle commande crée la branche zone-yoff et s'y place ?", [
  ("git switch -c zone-yoff", V, "Oui."),
  ("git merge zone-yoff", F, "Non : merge fusionne une branche existante."),
  ("git commit -m zone-yoff", F, "Non : cela crée un commit, pas une branche."),
]),
("Git annonce CONFLICT pendant une fusion. Que fais-tu ?", [
  ("J'ouvre le fichier, je garde la bonne version, je retire les marques, puis git add et git commit", V, "Oui."),
  ("Je supprime le dépôt et je recommence", F, "Non : un conflit se résout en quelques minutes."),
  ("Je laisse les marques <<<<<<< dans le fichier", F, "Non : le code ne fonctionnerait plus."),
]),
("Tu es sur main et tu tapes git merge supplement-poids. Que se passe-t-il ?", [
  ("Les commits de supplement-poids sont ajoutés à main", V, "Oui."),
  ("main est supprimée", F, "Non."),
  ("supplement-poids reçoit les commits de main", F, "Non : c'est la branche où tu te trouves (main) qui reçoit."),
]),
]),

# ---------------------------------------------------------------- 1.4.3
dict(code="1.4.3", id=None, seq=53, minutes=10,
titre="GitHub : envoyer, récupérer, demande de fusion et .gitignore",
description="Mettre ton dépôt en ligne sur GitHub, sans jamais y envoyer de mot de passe.",
html=fiche(
objectif="publier ton dépôt sur GitHub, récupérer le travail des autres et protéger tes secrets avec <code>.gitignore</code>.",
intro="Ton dépôt n'existe pour l'instant que sur ton ordinateur. <b>GitHub</b> en garde une copie en ligne : sauvegarde, travail en équipe, et vitrine pour ton futur employeur.",
corps=[
("h", "D'abord : protéger ce qui ne doit pas partir"),
("p", "Crée un fichier <code>.gitignore</code> à la racine du dépôt. Git ignorera tout ce qui y est listé :"),
("code", """__pycache__/
*.pyc
.env
*.conf""", ".gitignore"),
("code", """echo "CLE=secret" > .env
git status --short
?? .gitignore""", "Terminal : .env n'apparaît pas, il est bien ignoré"),
("attention", "Jamais de secret dans Git", "Mots de passe, clés d'API, fichier <code>odoo.conf</code> : jamais dans un dépôt. Même supprimé ensuite, un secret reste dans l'historique. Si ça arrive, considère-le comme volé : change-le tout de suite."),
("h", "Envoyer le dépôt sur GitHub"),
("liste", [
  "Crée un compte sur github.com, puis un nouveau dépôt vide nommé <code>baobab_livraison</code> (sans README).",
  "GitHub n'accepte plus ton mot de passe dans le terminal : il te faut un <b>jeton d'accès</b> (Settings → Developer settings → Personal access tokens) ou l'outil officiel <code>gh</code>. Garde ce jeton aussi précieusement qu'un mot de passe.",
]),
("code", """git remote add origin https://github.com/TON_COMPTE/baobab_livraison.git
git push -u origin main          # envoie main et la relie à GitHub
git push                         # les fois suivantes""", "Terminal"),
("h", "Récupérer le travail des autres"),
("code", """git clone https://github.com/TON_COMPTE/baobab_livraison.git   # copier un dépôt
git pull                                                        # récupérer les nouveaux commits""", "Terminal"),
("astuce", "La bonne habitude", "<code>git pull</code> avant de commencer à travailler, <code>git push</code> quand tu as fini. Moins tu attends, moins tu as de conflits."),
("h", "La demande de fusion (pull request)"),
("p", "En équipe, on ne pousse pas directement sur <code>main</code>. On pousse une branche (<code>git push -u origin zone-yoff</code>), puis on ouvre sur GitHub une <b>demande de fusion</b> (« pull request ») : un collègue relit le code, commente, puis accepte la fusion. On y reviendra au Bloc 5."),
],
exercice=[
("p", "Ajoute un <code>.gitignore</code> et un fichier <code>README.md</code> qui présente le projet en trois lignes. Crée le dépôt sur GitHub et envoie ton travail. Vérifie sur le site que <code>tarifs.py</code> et <code>README.md</code> sont là, et qu'aucun fichier <code>.env</code> ou <code>.conf</code> n'est parti."),
("p", "Ce dépôt GitHub est la deuxième pièce du travail à rendre du Bloc 1."),
],
retenir=[
  "<code>.gitignore</code> liste ce que Git ne doit jamais suivre (secrets, fichiers générés).",
  "Un secret envoyé sur GitHub est un secret volé : change-le.",
  "<code>git push</code> envoie, <code>git pull</code> récupère, <code>git clone</code> copie un dépôt.",
  "En équipe : une branche + une demande de fusion relue par un collègue.",
]),
quiz=[
("À quoi sert le fichier .gitignore ?", [
  ("À dire à Git quels fichiers ne jamais suivre", V, "Oui : secrets, fichiers générés…"),
  ("À supprimer des fichiers de l'ordinateur", F, "Non : il ne supprime rien."),
  ("À cacher le dépôt sur GitHub", F, "Non : la visibilité du dépôt se règle sur GitHub."),
]),
("Tu as envoyé par erreur un mot de passe sur GitHub. Que fais-tu en priorité ?", [
  ("Je change ce mot de passe tout de suite", V, "Oui : il reste dans l'historique, considère-le comme volé."),
  ("Je supprime le fichier et je fais un commit, c'est réglé", F, "Non : le mot de passe reste dans l'historique Git."),
  ("Rien, personne ne regarde", F, "Des robots cherchent en permanence les secrets publiés sur GitHub."),
]),
("Quelle commande récupère les nouveaux commits de tes collègues ?", [
  ("git pull", V, "Oui."),
  ("git push", F, "Non : push envoie tes commits."),
  ("git init", F, "Non : init crée un nouveau dépôt."),
]),
]),

# ---------------------------------------------------------------- 1.4.4
dict(code="1.4.4", id=2709, seq=54, minutes=10,
titre="Installer Odoo 20 Community depuis les sources",
description="Télécharger le code d'Odoo 20, installer ses dépendances et créer ta première base.",
html=fiche(
objectif="avoir Odoo 20 Community qui tourne sur ton ordinateur, installé depuis son code source.",
intro="Le grand moment du Bloc 1 ! Tu as Linux, Python, PostgreSQL et Git : tout est prêt pour installer Odoo. On l'installe depuis les <b>sources</b> (le code), comme le font les développeurs : tu pourras lire le code d'Odoo et le déboguer.",
corps=[
("h", "1. Les bibliothèques du système"),
("code", """sudo apt update
sudo apt install git python3-venv python3-dev build-essential \\
     libldap2-dev libpq-dev libsasl2-dev""", "Terminal"),
("p", "Certaines bibliothèques Python d'Odoo (<code>psycopg2</code> pour parler à PostgreSQL, <code>python-ldap</code>) sont compilées pendant l'installation : elles ont besoin de ces paquets."),
("h", "2. Télécharger Odoo 20"),
("code", "git clone --depth 1 --branch 20.0 https://github.com/odoo/odoo.git ~/odoo", "Terminal"),
("p", "<code>--branch 20.0</code> : la version 20. <code>--depth 1</code> : seulement la dernière version, sans tout l'historique. Compte environ <b>1,4 Go</b> sur ton disque : lance-le avec une bonne connexion."),
("h", "3. L'environnement virtuel et les dépendances"),
("code", """python3 -m venv ~/venv-odoo
source ~/venv-odoo/bin/activate
cd ~/odoo
pip install setuptools wheel
pip install -r requirements.txt""", "Terminal"),
("p", "Quelques minutes plus tard, la dernière ligne doit commencer par <code>Successfully installed</code>."),
("attention", "« Failed to build psycopg2 python-ldap »", "C'est l'erreur qu'on a eue en préparant cette leçon : <code>fatal error: libpq-fe.h: No such file or directory</code>. Cause : l'étape 1 n'avait pas marché, car <code>sudo apt update</code> manquait. Refais l'étape 1, puis relance <code>pip install -r requirements.txt</code>."),
("h", "4. Créer ta base et démarrer"),
("code", """python3 odoo-bin --addons-path=addons -d baobab_dev -i base""", "Terminal (dans ~/odoo, environnement activé)"),
("liste", [
  "<code>--addons-path=addons</code> : où trouver les modules ;",
  "<code>-d baobab_dev</code> : le nom de la base (créée si elle n'existe pas) ;",
  "<code>-i base</code> : installe le module de base.",
]),
("p", "Attends la ligne <code>Modules loaded.</code>, puis ouvre <b>http://localhost:8069</b> dans ton navigateur. Connexion : identifiant <code>admin</code>, mot de passe <code>admin</code>. Bravo, Odoo 20 tourne chez toi !"),
("version", "Depuis Odoo 18.3, les données de démonstration ne sont plus chargées par défaut. Pour une base avec des exemples (contacts, produits…), ajoute <code>--with-demo</code> à la création de la base."),
("astuce", "L'autre méthode officielle", "La documentation d'Odoo propose aussi <code>sudo ./setup/debinstall.sh</code>, qui installe les dépendances avec les paquets d'Ubuntu au lieu de pip. Pour développer, l'environnement virtuel est plus souple : on garde cette méthode."),
],
exercice=[
("p", "Installe Odoo 20 et crée la base <code>baobab_dev</code>. Connecte-toi, puis installe l'application <b>Contacts</b> depuis le menu Applications. Fais une capture d'écran de la page d'accueil d'Odoo avec ton navigateur : elle fait partie du travail à rendre."),
("p", "Pense à refaire l'exercice de la leçon « PostgreSQL et Odoo » maintenant que ta base existe."),
],
retenir=[
  "<code>sudo apt update</code>, puis les bibliothèques de compilation (<code>libpq-dev</code>, <code>libldap2-dev</code>, <code>libsasl2-dev</code>…).",
  "<code>git clone --depth 1 --branch 20.0 https://github.com/odoo/odoo.git</code>",
  "Environnement virtuel + <code>pip install -r requirements.txt</code>.",
  "<code>python3 odoo-bin --addons-path=addons -d baobab_dev -i base</code>, puis http://localhost:8069 (admin / admin).",
]),
quiz=[
("Quelle option de git clone télécharge seulement la dernière version, sans tout l'historique ?", [
  ("--depth 1", V, "Oui : beaucoup plus léger."),
  ("--branch 20.0", F, "Non : --branch choisit la version d'Odoo, pas la profondeur de l'historique."),
  ("--light", F, "Cette option n'existe pas."),
]),
("pip affiche « fatal error: libpq-fe.h: No such file or directory ». Que manque-t-il ?", [
  ("Les bibliothèques de développement du système, comme libpq-dev (avec apt update avant)", V, "Oui : psycopg2 en a besoin pour se compiler."),
  ("Une base de données vide", F, "Non : l'erreur arrive pendant l'installation des bibliothèques."),
  ("Une connexion au port 8069", F, "Non, rien à voir."),
]),
("Que fait l'option -i base dans python3 odoo-bin --addons-path=addons -d baobab_dev -i base ?", [
  ("Elle installe le module base dans la base baobab_dev", V, "Oui."),
  ("Elle importe une sauvegarde", F, "Non."),
  ("Elle ignore les erreurs", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 1.4.5
dict(code="1.4.5", id=None, seq=55, minutes=10,
titre="Variante : Odoo 20 avec Docker",
description="Lancer Odoo 20 et PostgreSQL 16 en une commande avec docker compose.",
html=fiche(
objectif="lancer Odoo 20 et sa base PostgreSQL avec Docker, et y brancher ton dossier de modules.",
intro="Docker fait tourner des logiciels déjà installés dans des « conteneurs ». C'est la solution la plus rapide sous macOS, ou pour avoir une deuxième version d'Odoo à côté de la première. C'est aussi ainsi qu'on déploie souvent en production (Bloc 5).",
corps=[
("h", "Le principe"),
("liste", [
  "Une <b>image</b> : un logiciel prêt à l'emploi (l'image officielle <code>odoo:20</code>, l'image <code>postgres:16</code>).",
  "Un <b>conteneur</b> : une image en train de tourner.",
  "Un fichier <code>compose.yaml</code> décrit plusieurs conteneurs qui travaillent ensemble.",
]),
("p", "Installe Docker Desktop (Windows, macOS) ou Docker Engine (Ubuntu) en suivant la documentation officielle de Docker."),
("h", "Le fichier compose.yaml"),
("code", """services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
      POSTGRES_DB: postgres
    volumes:
      - db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:20
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    volumes:
      - odoo-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons

volumes:
  db-data:
  odoo-data:""", "~/baobab-docker/compose.yaml (testé avec odoo:20 et postgres:16)"),
("liste", [
  "<code>ports: \"8069:8069\"</code> : Odoo sera accessible sur http://localhost:8069.",
  "<code>HOST, USER, PASSWORD</code> : comment Odoo se connecte au conteneur <code>db</code>.",
  "<code>./addons:/mnt/extra-addons</code> : ton dossier <code>addons</code> apparaît dans Odoo. C'est là que tu mettras <code>baobab_livraison</code>.",
  "Les <b>volumes</b> gardent les données même quand on arrête les conteneurs.",
]),
("attention", "Mot de passe d'entraînement seulement", "<code>odoo</code> / <code>odoo</code> convient pour ton ordinateur. En production, on met des mots de passe solides, rangés hors du dépôt Git (Bloc 5)."),
("h", "Démarrer, regarder, arrêter"),
("code", """cd ~/baobab-docker
mkdir -p addons
docker compose up -d          # démarrer en arrière-plan
docker compose ps             # état des conteneurs
docker compose logs -f odoo   # suivre le journal d'Odoo (Ctrl+C pour sortir)
docker compose down           # arrêter (les données restent dans les volumes)""", "Terminal"),
("p", "Ouvre http://localhost:8069 : Odoo te propose de créer une base. Choisis un mot de passe maître et note-le."),
("astuce", "Bon à savoir", "L'image <code>odoo:20</code> pèse plusieurs gigaoctets : premier téléchargement long. Et le dossier <code>/mnt/extra-addons</code> n'apparaît dans les chemins de modules d'Odoo que lorsqu'il contient au moins un module : c'est normal qu'il soit absent au début."),
],
exercice=[
("p", "Crée <code>~/baobab-docker/compose.yaml</code>, démarre les conteneurs, crée une base <code>baobab_docker</code> depuis le navigateur. Vérifie la version avec <code>docker compose exec odoo odoo --version</code> (résultat attendu : <code>Odoo Server 20.0-…</code>). Arrête tout avec <code>docker compose down</code>, redémarre, et vérifie que ta base est toujours là."),
],
retenir=[
  "Image = logiciel prêt à l'emploi ; conteneur = image qui tourne.",
  "<code>compose.yaml</code> décrit Odoo (<code>odoo:20</code>) et sa base (<code>postgres:16</code>).",
  "<code>docker compose up -d</code>, <code>ps</code>, <code>logs -f odoo</code>, <code>down</code>.",
  "Tes modules vont dans le dossier relié à <code>/mnt/extra-addons</code>.",
]),
quiz=[
("Dans le compose.yaml de la leçon, à quoi sert la ligne « ./addons:/mnt/extra-addons » ?", [
  ("À rendre ton dossier addons visible par Odoo dans le conteneur", V, "Oui : c'est là que tu mettras tes modules."),
  ("À installer tous les modules d'Odoo", F, "Non."),
  ("À sauvegarder la base de données", F, "Non : ce sont les volumes db-data et odoo-data qui gardent les données."),
]),
("Après docker compose down, ta base a-t-elle disparu ?", [
  ("Non : elle est gardée dans le volume db-data", V, "Oui : les volumes survivent à l'arrêt des conteneurs."),
  ("Oui, il faut tout recréer", F, "Non, grâce aux volumes."),
  ("Oui, sauf si on a fait un git push", F, "Git ne sauvegarde pas la base de données."),
]),
("Quelle commande suit le journal d'Odoo dans Docker ?", [
  ("docker compose logs -f odoo", V, "Oui."),
  ("tail -f odoo", F, "Non : le journal est dans le conteneur, on passe par docker compose logs."),
  ("docker compose up odoo.log", F, "Non."),
]),
]),

# ---------------------------------------------------------------- 1.4.6
dict(code="1.4.6", id=2710, seq=56, minutes=10,
titre="Lancer Odoo : fichier de configuration, mode développeur, journaux",
description="Ranger tes réglages dans un fichier, activer le mode développeur et le rechargement automatique.",
html=fiche(
objectif="lancer Odoo avec un fichier de configuration, activer le mode développeur et faire recharger Odoo tout seul quand tu modifies ton code.",
intro="Taper toutes les options à chaque démarrage, c'est long et source d'erreurs. On range les réglages dans un <b>fichier de configuration</b>, et on prépare Odoo pour le développement.",
corps=[
("h", "Créer le fichier de configuration"),
("code", """cd ~/odoo
source ~/venv-odoo/bin/activate
python3 odoo-bin -c ~/baobab/odoo.conf --addons-path=addons -d baobab_dev \\
    --db-filter='^baobab_dev$' --save --stop-after-init""", "Terminal"),
("p", "<code>--save</code> écrit toutes les options dans le fichier donné par <code>-c</code>, et <code>--stop-after-init</code> arrête Odoo juste après. Ouvre-le :"),
("code", """[options]
addons_path = /home/awa/odoo/addons
admin_passwd = admin
db_name = baobab_dev
dbfilter = ^baobab_dev$
http_port = 8069
...""", "~/baobab/odoo.conf (extrait)"),
("p", "Désormais, une seule commande suffit : <code>python3 odoo-bin -c ~/baobab/odoo.conf</code>."),
("attention", "Deux pièges vérifiés sur Odoo 20", "1) <code>admin_passwd = admin</code> est le <b>mot de passe maître</b> (il permet de créer, copier et supprimer des bases) : change-le, même en local. 2) Sans <code>-c</code>, <code>--save</code> enregistre dans <code>~/.config/Odoo/odoo.conf</code>, alors que l'aide d'Odoo parle encore de <code>~/.odoorc</code> : donne toujours le chemin avec <code>-c</code>, c'est plus clair."),
("h", "Le mode développeur, côté code"),
("code", """pip install inotify            # une fois, dans l'environnement virtuel
python3 odoo-bin -c ~/baobab/odoo.conf --dev=xml,reload""", "Terminal"),
("liste", [
  "<code>reload</code> : Odoo redémarre tout seul quand tu enregistres un fichier Python. Sans le paquet <code>inotify</code>, le journal affiche <code>'inotify' module not installed. Code autoreload feature is disabled</code>.",
  "<code>xml</code> : les vues sont relues directement depuis tes fichiers XML (Bloc 3).",
  "<code>--dev=all</code> active toutes les aides. Jamais en production !",
]),
("h", "Le mode développeur, côté écran"),
("p", "Dans Odoo : <b>Paramètres</b> → tout en bas, <b>Activer le mode développeur</b>. Ou ajoute <code>?debug=1</code> à l'adresse : <code>http://localhost:8069/web?debug=1</code>. Un petit insecte apparaît en haut : tu peux voir les noms techniques des champs, les vues, les modèles."),
("h", "Garder le journal dans un fichier"),
("code", """python3 odoo-bin -c ~/baobab/odoo.conf --logfile=/home/awa/baobab/odoo.log
tail -f ~/baobab/odoo.log | grep -E "WARNING|ERROR\"""", "Deux terminaux côte à côte"),
("astuce", "Mettre à jour un module", "Quand tu modifieras ton module (Bloc 2) : <code>-u baobab_livraison</code> met à jour le module dans la base. On verra en détail quand redémarrer et quand mettre à jour."),
],
exercice=[
("p", "Crée ton fichier <code>~/baobab/odoo.conf</code> avec <code>--save</code>, change le mot de passe maître dans le fichier, installe <code>inotify</code>, puis lance Odoo avec <code>--dev=xml,reload</code> et <code>--logfile</code>. Dans le journal, retrouve la ligne <code>AutoReload watcher running with inotify</code>. Active ensuite le mode développeur dans Paramètres et repère le nom technique du champ « E-mail » d'un contact (survole le champ)."),
],
retenir=[
  "<code>-c fichier --save</code> enregistre les options ; ensuite <code>python3 odoo-bin -c fichier</code>.",
  "Change le mot de passe maître (<code>admin_passwd</code>) : par défaut, c'est <code>admin</code>.",
  "<code>--dev=xml,reload</code> pour développer (avec le paquet <code>inotify</code>) ; jamais en production.",
  "Mode développeur à l'écran : Paramètres → Activer le mode développeur, ou <code>?debug=1</code>.",
]),
quiz=[
("À quoi sert l'option --save avec -c ~/baobab/odoo.conf ?", [
  ("À écrire les options de la commande dans ce fichier de configuration", V, "Oui."),
  ("À sauvegarder la base de données", F, "Non : ce n'est pas une sauvegarde de la base."),
  ("À enregistrer le code dans Git", F, "Non."),
]),
("Le journal dit « 'inotify' module not installed. Code autoreload feature is disabled ». Que faire ?", [
  ("Installer le paquet Python inotify dans l'environnement virtuel", V, "Oui : pip install inotify, puis relancer Odoo."),
  ("Désactiver le mode développeur", F, "Non : on veut justement le rechargement automatique."),
  ("Réinstaller PostgreSQL", F, "Non, rien à voir."),
]),
("Quel est le risque si on laisse admin_passwd = admin ?", [
  ("N'importe qui avec cet accès peut créer, copier ou supprimer des bases", V, "Oui : c'est le mot de passe maître."),
  ("Aucun, c'est le mot de passe d'un utilisateur de démonstration", F, "Non : c'est le mot de passe maître du serveur."),
  ("Odoo refuse de démarrer", F, "Non : il démarre, et c'est justement le problème."),
]),
]),

# ---------------------------------------------------------------- 1.4.7
dict(code="1.4.7", id=None, seq=57, minutes=10,
titre="L'éditeur de code : VS Code et son débogueur",
description="Ouvrir Odoo et ton module dans VS Code, mettre un point d'arrêt dans Odoo.",
html=fiche(
objectif="travailler dans VS Code et arrêter Odoo sur un point d'arrêt pour inspecter les variables.",
intro="Tu peux écrire du code avec <code>nano</code>, mais un bon éditeur change tout : couleurs, complétion, recherche dans tout Odoo, et surtout un <b>débogueur</b> pour voir ce qui se passe à l'intérieur.",
corps=[
("h", "Installer VS Code"),
("liste", [
  "Télécharge Visual Studio Code (gratuit) sur code.visualstudio.com.",
  "Sous Windows avec WSL : installe VS Code sous Windows, puis l'extension <b>WSL</b> ; dans le terminal Ubuntu, tape <code>code ~/baobab_livraison</code>.",
  "Installe les extensions <b>Python</b> et <b>Python Debugger</b> (éditeur Microsoft).",
  "En bas à droite, choisis l'interpréteur Python <code>~/venv-odoo/bin/python</code>.",
]),
("h", "Ouvrir les bons dossiers"),
("p", "Ouvre à la fois <code>~/odoo</code> (pour lire le code d'Odoo) et ton dossier de modules : <b>Fichier → Ajouter un dossier à l'espace de travail</b>. Ensuite, <b>Ctrl+Maj+F</b> cherche dans tous les fichiers, <b>Ctrl+clic</b> sur un nom de fonction ouvre sa définition, même dans le code d'Odoo."),
("h", "Lancer Odoo dans le débogueur"),
("p", "Crée le fichier <code>.vscode/launch.json</code> dans ton espace de travail :"),
("code", """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Odoo 20 (baobab_dev)",
            "type": "debugpy",
            "request": "launch",
            "program": "${env:HOME}/odoo/odoo-bin",
            "args": ["-c", "${env:HOME}/baobab/odoo.conf", "--dev=xml,reload"],
            "python": "${env:HOME}/venv-odoo/bin/python",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}""", ".vscode/launch.json"),
("p", "Puis <b>F5</b> : Odoo démarre sous le contrôle de VS Code. Clique dans la marge à gauche d'une ligne de code pour poser un <b>point d'arrêt</b> (un rond rouge). Quand Odoo passe par cette ligne, il s'arrête : tu vois toutes les variables à gauche, et tu avances ligne par ligne avec <b>F10</b> (ligne suivante) et <b>F11</b> (entrer dans la fonction)."),
("astuce", "Le rechargement marche aussi ici", "Odoo 20 sait redémarrer sous le débogueur : avec <code>--dev=xml,reload</code>, quand tu enregistres un fichier Python, Odoo relance un nouveau processus et VS Code continue de le suivre. Tes points d'arrêt restent actifs."),
("astuce", "Bon à savoir", "Le débogueur de VS Code s'appuie sur <code>debugpy</code> ; on a vérifié qu'Odoo 20 démarre normalement sous <code>debugpy</code>."),
],
exercice=[
("p", "Installe VS Code et ses extensions, crée le <code>launch.json</code>, lance Odoo avec F5. Ouvre <code>~/odoo/odoo/addons/base/models/res_partner.py</code>, cherche (Ctrl+F) <code>def _compute_display_name</code> et pose un point d'arrêt sur la première ligne de la boucle de cette méthode. Ouvre un contact dans Odoo : VS Code doit s'arrêter. Regarde la valeur de <code>partner.name</code>, puis continue avec F5."),
],
retenir=[
  "VS Code + extensions Python et Python Debugger ; interpréteur = <code>~/venv-odoo/bin/python</code>.",
  "Ctrl+Maj+F cherche dans tout Odoo ; Ctrl+clic ouvre une définition.",
  "<code>launch.json</code> lance <code>odoo-bin</code> avec ton fichier de configuration ; F5 pour démarrer.",
  "Point d'arrêt dans la marge ; F10 ligne suivante, F11 entrer dans la fonction.",
]),
quiz=[
("Quelle touche lance Odoo dans le débogueur de VS Code, une fois launch.json créé ?", [
  ("F5", V, "Oui."),
  ("F1", F, "Non : F1 ouvre la palette de commandes."),
  ("Ctrl+S", F, "Non : Ctrl+S enregistre le fichier."),
]),
("Quel interpréteur Python faut-il choisir dans VS Code pour Odoo ?", [
  ("Celui de l'environnement virtuel ~/venv-odoo", V, "Oui : c'est là que sont installées les bibliothèques d'Odoo."),
  ("Le Python du système, /usr/bin/python3", F, "Non : les bibliothèques d'Odoo n'y sont pas."),
  ("Peu importe", F, "Non : avec le mauvais interpréteur, Odoo ne démarre pas."),
]),
("À quoi sert un point d'arrêt ?", [
  ("À arrêter le programme sur une ligne pour regarder les variables", V, "Oui."),
  ("À arrêter définitivement Odoo", F, "Non : on continue ensuite avec F5."),
  ("À supprimer une ligne de code", F, "Non."),
]),
]),
]
