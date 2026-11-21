"""Bloc 1 — Section « Linux et le terminal » (section 2700, cours 208).
Commandes testées sur Ubuntu 24.04 le 21/11/2026 (sauf l'installation de WSL sous Windows : à tester sur un PC Windows)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "outils"))
from fiche import fiche

V, F = True, False

LECONS = [
# ---------------------------------------------------------------- 1.1.1
dict(code="1.1.1", id=1353, seq=21, minutes=10,
titre="Pourquoi Linux ? Installer Ubuntu ou WSL sous Windows",
description="Comprendre pourquoi Odoo vit sur Linux et obtenir un terminal Ubuntu sur ton ordinateur.",
html=fiche(
objectif="comprendre pourquoi on développe Odoo sous Linux et avoir un terminal Ubuntu qui fonctionne.",
intro="Presque tous les serveurs Odoo du monde tournent sous Linux. En développant sous Linux, tu travailles dans les mêmes conditions que la production : moins de surprises le jour de la mise en ligne.",
corps=[
("h", "Pourquoi Linux ?"),
("liste", [
  "<b>C'est là qu'Odoo tourne</b> : Odoo.sh, les serveurs des intégrateurs, l'image Docker officielle… tout est sous Linux.",
  "<b>Les outils sont prévus pour</b> : PostgreSQL, Git, Python s'installent en une commande.",
  "<b>Le terminal</b> devient ton outil principal : lancer Odoo, lire les journaux, se connecter à un serveur.",
]),
("p", "On utilise <b>Ubuntu 24.04</b> : une version de Linux très répandue, qui contient déjà Python 3.12 (le minimum pour Odoo 20)."),
("h", "Trois façons d'avoir Ubuntu"),
("tableau", ["Ton ordinateur", "Solution conseillée"], [
  ["Windows 10 ou 11", "<b>WSL</b> (Windows Subsystem for Linux) : un vrai Ubuntu à l'intérieur de Windows, sans réinstaller ton PC."],
  ["Déjà sous Ubuntu", "Rien à faire !"],
  ["macOS", "Le terminal de macOS ressemble beaucoup à Linux : la plupart des commandes du parcours marchent. Pour PostgreSQL et Odoo, l'option Docker (section Git et environnement) est la plus simple."],
]),
("h", "Installer WSL sous Windows"),
("p", "Ouvre <b>PowerShell en administrateur</b> (clic droit sur le menu Démarrer → Terminal (admin)) et tape :"),
("code", "wsl --install -d Ubuntu-24.04", "PowerShell (administrateur)"),
("p", "Redémarre l'ordinateur quand Windows le demande. Au premier lancement d'Ubuntu, choisis un <b>nom d'utilisateur</b> (en minuscules, sans espace, par exemple <code>awa</code>) et un <b>mot de passe</b>. Rien ne s'affiche quand tu tapes le mot de passe : c'est normal."),
("attention", "Retiens ce mot de passe", "Il te sera demandé à chaque commande <code>sudo</code> (installer un logiciel, par exemple). Ne le donne à personne et ne l'écris jamais dans ton code."),
("h", "Vérifier que tout marche"),
("p", "Dans le terminal Ubuntu, mets d'abord le système à jour, puis vérifie Python :"),
("code", """sudo apt update
sudo apt upgrade -y
python3 --version""", "Terminal Ubuntu"),
("code", "Python 3.12.3", "Résultat attendu (le dernier chiffre peut varier)"),
("astuce", "Où sont mes fichiers ?", "Sous WSL, ton dossier personnel Ubuntu est <code>/home/ton_nom</code>. Depuis l'explorateur Windows, tu le retrouves dans « Linux » dans la colonne de gauche. Travaille toujours dans ce dossier Linux, pas dans <code>/mnt/c/…</code> (le disque Windows) : Odoo y serait beaucoup plus lent."),
],
exercice=[
("p", "Installe Ubuntu (WSL ou natif), lance <code>sudo apt update</code>, puis note dans ton carnet : ton nom d'utilisateur Ubuntu et le résultat de <code>python3 --version</code>."),
("p", "Bonus : tape <code>lsb_release -a</code> pour afficher la version exacte d'Ubuntu."),
],
retenir=[
  "Odoo tourne presque toujours sous Linux : on développe dans les mêmes conditions.",
  "Sous Windows : <code>wsl --install -d Ubuntu-24.04</code> dans PowerShell administrateur.",
  "Ubuntu 24.04 fournit Python 3.12, le minimum pour Odoo 20.",
  "Travaille dans ton dossier Linux (<code>/home/…</code>), pas dans le disque Windows.",
]),
quiz=[
("Pourquoi développe-t-on Odoo sous Linux ?", [
  ("Parce que la plupart des serveurs Odoo tournent sous Linux", V, "Oui : on travaille dans les mêmes conditions que la production."),
  ("Parce qu'Odoo ne s'affiche pas dans un navigateur sous Windows", F, "Non : le navigateur fonctionne partout. C'est le serveur qui vit sous Linux."),
  ("Parce que Linux est obligatoire pour écrire du Python", F, "Non : Python existe aussi sous Windows et macOS."),
]),
("Sous Windows, quelle solution permet d'avoir Ubuntu sans réinstaller l'ordinateur ?", [
  ("WSL", V, "Oui : Windows Subsystem for Linux."),
  ("PowerPoint", F, "Non."),
  ("PostgreSQL", F, "Non : c'est la base de données, pas un système."),
]),
("Sous WSL, où faut-il ranger tes projets Odoo ?", [
  ("Dans ton dossier Linux, /home/ton_nom", V, "Oui : c'est beaucoup plus rapide que le disque Windows."),
  ("Dans /mnt/c, sur le disque Windows", F, "Ça marche, mais Odoo y est très lent."),
  ("Sur une clé USB", F, "Non : travaille dans ton dossier Linux."),
]),
]),

# ---------------------------------------------------------------- 1.1.2
dict(code="1.1.2", id=2701, seq=22, minutes=10,
titre="Se déplacer et manipuler des fichiers dans le terminal",
description="pwd, ls, cd, mkdir, cp, mv, rm : les commandes de tous les jours.",
html=fiche(
objectif="te déplacer dans les dossiers et créer, copier, déplacer ou supprimer des fichiers sans peur.",
intro="Dans le terminal, pas de souris : tu donnes des ordres. Sept commandes suffisent pour la grande majorité de ton travail quotidien.",
corps=[
("h", "Où suis-je ? Qu'y a-t-il ici ?"),
("code", """pwd            # affiche le dossier où tu te trouves
/home/awa
ls             # liste le contenu du dossier
ls -l          # liste détaillée : droits, taille, date
ls -a          # montre aussi les fichiers cachés (qui commencent par un point)""", "Terminal"),
("h", "Se déplacer"),
("code", """cd baobab          # entrer dans le dossier baobab
cd ..              # remonter d'un niveau
cd ~               # revenir à ton dossier personnel (~ = /home/awa)
cd /var/log        # aller à un chemin complet""", "Terminal"),
("astuce", "La touche Tab", "Tape le début d'un nom puis appuie sur <b>Tab</b> : le terminal complète tout seul. Les flèches ↑ et ↓ rappellent les commandes précédentes. Tu vas gagner un temps fou."),
("h", "Créer, copier, déplacer, supprimer"),
("code", """mkdir -p ~/essai/journaux     # créer un dossier (et ses parents avec -p)
touch notes.txt               # créer un fichier vide
cp notes.txt copie.txt        # copier
mv copie.txt journaux/        # déplacer (ou renommer)
rm journaux/copie.txt         # supprimer un fichier
rm -r journaux                # supprimer un dossier et tout son contenu""", "Terminal"),
("attention", "rm ne prévient pas", "Il n'y a pas de corbeille dans le terminal : un fichier supprimé avec <code>rm</code> est perdu. Relis toujours ta commande avant d'appuyer sur Entrée, surtout avec <code>rm -r</code>."),
("h", "Chemins absolus et relatifs"),
("tableau", ["Chemin", "Signification"], [
  ["<code>/home/awa/baobab</code>", "Absolu : part de la racine <code>/</code>, marche depuis n'importe où"],
  ["<code>baobab/tarifs.py</code>", "Relatif : part du dossier où tu te trouves"],
  ["<code>~</code>", "Ton dossier personnel"],
  ["<code>.</code> et <code>..</code>", "Le dossier actuel et le dossier parent"],
]),
("p", "Pour lire un fichier court : <code>cat tarifs.py</code>. Pour le modifier dans le terminal : <code>nano tarifs.py</code> (Ctrl+O pour enregistrer, Ctrl+X pour quitter)."),
],
exercice=[
("p", "Crée cette organisation de dossiers pour le parcours, en utilisant uniquement le terminal :"),
("code", """~/baobab/
├── scripts/        ← tu y déplaces tarifs.py (leçon 1.0.6)
├── addons/         ← tes modules Odoo (Bloc 2)
└── notes/
    └── commandes.txt""", "Organisation attendue"),
("p", "Puis vérifie avec <code>ls -R ~/baobab</code> (le <code>-R</code> liste aussi les sous-dossiers)."),
],
retenir=[
  "<code>pwd</code> où je suis · <code>ls</code> ce qu'il y a · <code>cd</code> se déplacer.",
  "<code>mkdir</code>, <code>cp</code>, <code>mv</code>, <code>rm</code> : créer, copier, déplacer, supprimer.",
  "<code>rm</code> est définitif : relis avant d'appuyer sur Entrée.",
  "La touche Tab complète les noms ; ↑ rappelle les commandes précédentes.",
]),
quiz=[
("Quelle commande affiche le dossier dans lequel tu te trouves ?", [
  ("pwd", V, "Oui : print working directory."),
  ("ls", F, "Non : ls liste le contenu du dossier."),
  ("cd", F, "Non : cd sert à changer de dossier."),
]),
("Que fait mv ancien.txt nouveau.txt ?", [
  ("Il renomme le fichier", V, "Oui : mv déplace ou renomme."),
  ("Il copie le fichier", F, "Non : c'est cp qui copie."),
  ("Il supprime les deux fichiers", F, "Non."),
]),
("Tu as supprimé un fichier avec rm par erreur. Que se passe-t-il ?", [
  ("Il est perdu : rm n'utilise pas de corbeille", V, "Oui. D'où l'importance de Git, qu'on voit plus loin, pour garder l'historique de ton code."),
  ("Il est dans la corbeille", F, "Non : le terminal n'a pas de corbeille."),
  ("On peut l'annuler avec Ctrl+Z", F, "Non : Ctrl+Z ne restaure pas un fichier supprimé."),
]),
]),

# ---------------------------------------------------------------- 1.1.3
dict(code="1.1.3", id=None, seq=23, minutes=10,
titre="Chercher et lire : cat, less, grep, tail -f",
description="Lire un fichier, chercher un mot dans des milliers de lignes, suivre un journal en direct.",
html=fiche(
objectif="retrouver une information dans un gros fichier et suivre le journal d'Odoo en direct.",
intro="Quand Odoo plante, la réponse est presque toujours dans son <b>journal</b> (le fichier où il note tout ce qu'il fait). Un journal peut faire des milliers de lignes : il faut savoir y chercher.",
corps=[
("h", "À quoi ressemble une ligne du journal d'Odoo"),
("code", "2026-11-21 23:35:06,185 1263 WARNING baobab_dev odoo.service.server: 'inotify' module not installed. Code autoreload feature is disabled", "Une ligne réelle d'un journal Odoo 20"),
("p", "Dans l'ordre : la date et l'heure, le numéro du processus, le <b>niveau</b> (INFO, WARNING, ERROR, CRITICAL), le nom de la base, la partie d'Odoo qui parle, puis le message."),
("h", "Lire un fichier"),
("code", """cat odoo.log           # tout afficher d'un coup (pour les petits fichiers)
less odoo.log          # lire page par page : espace = page suivante,
                       # /mot = chercher, q = quitter
head -n 20 odoo.log    # les 20 premières lignes
tail -n 50 odoo.log    # les 50 dernières lignes""", "Terminal"),
("h", "Chercher avec grep"),
("code", """grep ERROR odoo.log              # les lignes qui contiennent ERROR
grep -i error odoo.log           # sans tenir compte des majuscules
grep -n WARNING odoo.log         # avec le numéro de ligne
grep -c INFO odoo.log            # compter les lignes
grep -rn "baobab" ~/baobab       # chercher dans tous les fichiers d'un dossier""", "Terminal"),
("h", "Suivre le journal en direct"),
("code", "tail -f odoo.log", "Terminal"),
("p", "<code>tail -f</code> affiche les nouvelles lignes au fur et à mesure qu'Odoo les écrit. Fais une action dans Odoo et regarde le journal réagir. Ctrl+C pour arrêter."),
("h", "Combiner les commandes avec |"),
("p", "Le tuyau <code>|</code> envoie le résultat d'une commande à la suivante :"),
("code", """tail -f odoo.log | grep -i error     # suivre seulement les erreurs
grep ERROR odoo.log | tail -n 5      # les 5 dernières erreurs""", "Terminal"),
("astuce", "Trouver un fichier", "<code>find ~/odoo/addons -name \"__manifest__.py\"</code> trouve tous les fichiers de ce nom. Très utile pour explorer le code d'Odoo."),
],
exercice=[
("p", "Crée un faux journal pour t'entraîner :"),
("code", """cat > ~/essai.log << 'FIN'
2026-11-21 08:00:01,100 1263 INFO baobab_dev odoo.modules.loading: Modules loaded.
2026-11-21 08:05:12,400 1263 WARNING baobab_dev odoo.models: zone vide
2026-11-21 08:07:45,900 1263 ERROR baobab_dev odoo.http: KeyError: 'Yoff'
2026-11-21 08:09:02,250 1263 INFO baobab_dev odoo.http: GET /web 200
FIN""", "Terminal"),
("p", "Avec une seule commande à chaque fois : (1) affiche la ligne d'erreur avec son numéro, (2) compte les lignes INFO, (3) affiche les lignes qui ne sont pas INFO (indice : cherche l'option <code>-v</code> de grep avec <code>man grep</code>)."),
],
retenir=[
  "Le journal d'Odoo dit presque toujours pourquoi ça ne marche pas.",
  "<code>less</code> pour lire, <code>grep</code> pour chercher, <code>tail -f</code> pour suivre en direct.",
  "<code>|</code> enchaîne les commandes : <code>tail -f odoo.log | grep -i error</code>.",
  "Les niveaux : INFO, WARNING, ERROR, CRITICAL.",
]),
quiz=[
("Quelle commande permet de suivre en direct la fin d'un fichier de journal ?", [
  ("tail -f odoo.log", V, "Oui. Ctrl+C pour arrêter."),
  ("head odoo.log", F, "Non : head montre le début du fichier."),
  ("cat -f odoo.log", F, "Non : cat n'a pas cette option."),
]),
("Que fait grep -i error odoo.log ?", [
  ("Il affiche les lignes contenant « error », en majuscules ou minuscules", V, "Oui : -i ignore la casse."),
  ("Il supprime les erreurs du fichier", F, "Non : grep ne modifie jamais le fichier."),
  ("Il compte les erreurs", F, "Non : c'est l'option -c qui compte."),
]),
("À quoi sert le symbole | entre deux commandes ?", [
  ("À envoyer le résultat de la première commande à la seconde", V, "Oui : c'est le « tuyau »."),
  ("À lancer les deux commandes en même temps sur deux fichiers", F, "Non."),
  ("À écrire le résultat dans un fichier", F, "Non : pour écrire dans un fichier, on utilise >."),
]),
]),

# ---------------------------------------------------------------- 1.1.4
dict(code="1.1.4", id=None, seq=24, minutes=10,
titre="Utilisateurs, droits, sudo et paquets",
description="Comprendre « Permission denied », installer un logiciel avec apt.",
html=fiche(
objectif="comprendre les droits des fichiers, utiliser sudo avec prudence et installer un logiciel avec apt.",
intro="Sous Linux, chaque fichier appartient à un utilisateur, et chacun n'a le droit de faire que ce qui lui est permis. Le message « Permission denied » vient de là. C'est aussi ce qui protège un serveur Odoo.",
corps=[
("h", "Lire les droits"),
("code", """ls -l ~/baobab/odoo.conf
-rw------- 1 awa awa 1776 Nov 21 23:35 /home/awa/baobab/odoo.conf""", "Terminal"),
("p", "Le début <code>-rw-------</code> se lit en trois groupes après le premier caractère : <b>propriétaire</b> (<code>rw-</code> : lire, écrire), <b>groupe</b> (<code>---</code> : rien), <b>les autres</b> (<code>---</code> : rien). <code>r</code> = lire, <code>w</code> = écrire, <code>x</code> = exécuter (ou entrer, pour un dossier). Ensuite viennent le propriétaire (<code>awa</code>) et le groupe."),
("astuce", "Un bon exemple", "Odoo crée son fichier de configuration en <code>rw-------</code> : seul son propriétaire peut le lire, car il peut contenir des mots de passe."),
("h", "Changer les droits"),
("code", """chmod u+x script.sh     # rendre un script exécutable par son propriétaire
chmod 600 odoo.conf     # lecture/écriture pour le propriétaire seulement
chown awa:awa fichier   # changer le propriétaire (demande sudo)""", "Terminal"),
("h", "sudo : agir en administrateur"),
("p", "<code>sudo</code> exécute une commande avec les droits de l'administrateur (root). Il demande ton mot de passe."),
("attention", "sudo n'est pas une solution magique", "Si une commande dit « Permission denied », ne mets pas <code>sudo</code> devant par réflexe : demande-toi d'abord <i>pourquoi</i> tu n'as pas le droit. Ne lance jamais Odoo avec sudo ni en root : c'est dangereux, et Odoo t'avertit lui-même au démarrage : <code>Running as user 'root' is a security risk.</code>"),
("h", "Installer des logiciels avec apt"),
("code", """sudo apt update                    # 1. mettre à jour la liste des logiciels
sudo apt install postgresql git    # 2. installer
apt list --installed | grep git    # vérifier ce qui est installé""", "Terminal"),
("attention", "N'oublie pas apt update", "Sans <code>sudo apt update</code>, apt peut répondre « Unable to locate package » pour un logiciel qui existe pourtant. On l'a vérifié en préparant cette leçon : c'est l'erreur la plus fréquente pendant l'installation d'Odoo."),
],
exercice=[
("p", "1. Installe les outils dont on aura besoin pour Odoo : <code>sudo apt update</code>, puis <code>sudo apt install git curl</code>."),
("p", "2. Crée un fichier <code>~/baobab/secret.txt</code>, regarde ses droits avec <code>ls -l</code>, puis rends-le lisible par toi seul avec <code>chmod 600</code>. Vérifie à nouveau."),
],
retenir=[
  "<code>ls -l</code> montre les droits : propriétaire, groupe, autres ; r = lire, w = écrire, x = exécuter.",
  "<code>chmod</code> change les droits, <code>chown</code> le propriétaire.",
  "<code>sudo</code> donne les droits d'administrateur : à utiliser en sachant pourquoi.",
  "Toujours <code>sudo apt update</code> avant <code>sudo apt install</code>.",
]),
quiz=[
("Un fichier a les droits -rw-------. Qui peut le lire ?", [
  ("Seulement son propriétaire", V, "Oui : le groupe et les autres n'ont aucun droit (---)."),
  ("Tout le monde", F, "Non : il faudrait un r dans le dernier groupe."),
  ("Personne", F, "Non : le propriétaire a rw-, donc il peut lire et écrire."),
]),
("apt répond « Unable to locate package libpq-dev ». Que fais-tu en premier ?", [
  ("Je lance sudo apt update, puis je réessaie", V, "Oui : la liste des logiciels n'était sans doute pas à jour."),
  ("Je réinstalle Ubuntu", F, "Beaucoup trop radical."),
  ("Je lance Odoo avec sudo", F, "Non : rien à voir, et c'est dangereux."),
]),
("Faut-il lancer Odoo avec sudo ?", [
  ("Non : Odoo doit tourner avec un utilisateur normal", V, "Oui : en cas de faille, un pirate aurait sinon tous les droits sur la machine."),
  ("Oui, sinon il ne démarre pas", F, "Non : Odoo démarre très bien avec ton utilisateur."),
  ("Oui, c'est plus rapide", F, "Non : sudo ne rend rien plus rapide."),
]),
]),

# ---------------------------------------------------------------- 1.1.5
dict(code="1.1.5", id=None, seq=25, minutes=10,
titre="Processus et ports : « le port 8069 est déjà utilisé »",
description="Voir les programmes qui tournent, trouver qui occupe un port, arrêter un programme bloqué.",
html=fiche(
objectif="trouver quel programme occupe un port et arrêter proprement un Odoo bloqué.",
intro="Odoo écoute par défaut sur le <b>port 8069</b> : c'est pour cela qu'on l'ouvre à l'adresse <code>http://localhost:8069</code>. Si un autre Odoo tourne déjà, le nouveau refuse de démarrer. Voici comment s'en sortir.",
corps=[
("h", "Processus et ports en deux phrases"),
("liste", [
  "Un <b>processus</b> est un programme en train de tourner. Chacun a un numéro : le <b>PID</b>.",
  "Un <b>port</b> est une « porte » numérotée par laquelle un programme reçoit des connexions. Un port ne peut être occupé que par un seul programme à la fois.",
]),
("h", "Voir les processus"),
("code", """ps aux | grep odoo-bin       # les processus dont la commande contient odoo-bin
top                          # tableau en direct (q pour quitter)""", "Terminal"),
("h", "Qui occupe le port 8069 ?"),
("code", """sudo ss -ltnp | grep 8069
LISTEN 0  128  0.0.0.0:8069  0.0.0.0:*  users:(("python3",pid=1263,fd=5))""", "Terminal (2e ligne : exemple de résultat)"),
("p", "Ici, le processus <b>1263</b> (un python3, donc un Odoo) occupe le port."),
("h", "Arrêter un processus"),
("code", """kill 1263        # demande poliment au processus de s'arrêter
kill -9 1263     # le force à s'arrêter (en dernier recours)""", "Terminal"),
("p", "Si Odoo tourne dans ton terminal, le plus simple reste <b>Ctrl+C</b>, une fois : Odoo s'arrête proprement (« Initiating shutdown »)."),
("attention", "kill -9 en dernier recours", "<code>kill -9</code> coupe net, sans laisser le programme ranger ses affaires. Essaie toujours <code>kill</code> simple d'abord, attends quelques secondes, puis vérifie avec <code>ps</code>."),
("astuce", "Ou change de port", "Tu peux aussi lancer un deuxième Odoo sur un autre port : <code>--http-port=8070</code>, puis l'ouvrir sur <code>http://localhost:8070</code>."),
],
exercice=[
("p", "Lance un petit serveur web Python qui occupe le port 8069, comme le ferait un Odoo oublié :"),
("code", "python3 -m http.server 8069 &", "Terminal (le & le lance en arrière-plan)"),
("p", "Puis, avec les commandes de la leçon : retrouve son PID, vérifie qu'il occupe bien le port 8069, arrête-le, et vérifie que le port est libre."),
],
retenir=[
  "Odoo écoute sur le port 8069 par défaut.",
  "<code>ps aux | grep odoo-bin</code> pour voir les Odoo qui tournent ; <code>sudo ss -ltnp | grep 8069</code> pour savoir qui occupe le port.",
  "<code>kill PID</code> pour arrêter ; <code>kill -9</code> seulement en dernier recours.",
  "Ctrl+C arrête proprement un Odoo lancé dans ton terminal.",
]),
quiz=[
("Sur quel port Odoo écoute-t-il par défaut ?", [
  ("8069", V, "Oui : http://localhost:8069."),
  ("80", F, "Non : 80 est le port web classique, utilisé en production derrière un serveur web."),
  ("5432", F, "Non : 5432 est le port de PostgreSQL."),
]),
("Qu'est-ce qu'un PID ?", [
  ("Le numéro d'un processus en cours", V, "Oui : on s'en sert par exemple avec kill."),
  ("Le mot de passe de l'administrateur", F, "Non."),
  ("Le numéro du port", F, "Non : le port et le PID sont deux choses différentes."),
]),
("Odoo refuse de démarrer : le port est déjà utilisé. Quelle est la bonne démarche ?", [
  ("Trouver le processus avec ss ou ps, l'arrêter avec kill, puis relancer", V, "Oui. Ou lancer le nouvel Odoo sur un autre port avec --http-port."),
  ("Redémarrer l'ordinateur à chaque fois", F, "Ça marche, mais c'est long : apprends à trouver le processus."),
  ("Supprimer le dossier d'Odoo", F, "Surtout pas !"),
]),
]),
]
