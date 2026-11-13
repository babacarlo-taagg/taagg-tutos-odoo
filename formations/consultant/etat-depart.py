"""Remet la base de tournage dans l'état de départ d'une capsule Consultant (CON-xx), par l'API (jamais à l'écran).

Usage : python3 formations/consultant/etat-depart.py CON-01              montre ce qui serait défait, ne touche à rien
        python3 formations/consultant/etat-depart.py CON-01 --oui        défait (accord permanent de Babacar pour ce
                                                                         que les capsules créent)
        python3 formations/consultant/etat-depart.py CON-06 --preparer   crée seulement ce qui manque, ne retire rien

Ne défait QUE ce que les capsules Consultant créent : les projets, articles et sondages dont le nom finit par
« (formation) », leurs tâches et leurs étapes propres, l'employé « Formateur TAAGG ». Jamais le projet « Ouverture
boutique Almadies », les projets « Interne », les sondages modèles ni les articles des autres formations.
Lit ODOO_URL, ODOO_BASE, ODOO_LOGIN_API et ODOO_CLE_API dans l'environnement, sinon dans le .env du projet.
"""
import json
import os
import pathlib
import sys
import urllib.request

ICI = pathlib.Path(__file__).resolve().parents[2]
ENV = {}
if (ICI / '.env').exists():
    ENV = dict(l.split('=', 1) for l in (ICI / '.env').read_text().splitlines() if '=' in l and not l.startswith('#'))
    ENV = {k.strip(): v.split('#')[0].strip() for k, v in ENV.items()}
ENV.update({k: v for k, v in os.environ.items() if k.startswith('ODOO_')})
ENV.setdefault('ODOO_BASE', 'edu-correction-les-delices-de-maimouna')
FORMATEUR = 6  # « Formateur TAAGG », le compte qui filme
PROJET_CON01 = 'Déploiement Odoo — Délices de Maïmouna'  # nom tapé à l'écran, sans suffixe
EMPLOYE = 'Formateur TAAGG'
OUI = '--oui' in sys.argv
PREPARER = '--preparer' in sys.argv


def appel(service, methode, *args):
    corps = {'jsonrpc': '2.0', 'method': 'call', 'params': {'service': service, 'method': methode, 'args': args}}
    req = urllib.request.Request(ENV['ODOO_URL'] + '/jsonrpc', json.dumps(corps).encode(), {'Content-Type': 'application/json'})
    rep = json.load(urllib.request.urlopen(req, timeout=60))
    if 'error' in rep:
        sys.exit('Odoo a refusé : ' + rep['error']['data'].get('message', str(rep['error'])))
    return rep.get('result')


UID = appel('common', 'authenticate', ENV['ODOO_BASE'], ENV['ODOO_LOGIN_API'], ENV['ODOO_CLE_API'], {})


def odoo(modele, methode, *args, **kw):
    return appel('object', 'execute_kw', ENV['ODOO_BASE'], UID, ENV['ODOO_CLE_API'], modele, methode, list(args), kw)


def retirer(modele, ids, quoi):
    """Montre ce qui serait retiré ; ne le retire qu'avec --oui."""
    if not ids:
        return
    noms = [r['display_name'] for r in odoo(modele, 'read', ids, fields=['display_name'])]
    print(('  RETIRÉ  ' if OUI else '  à retirer  ') + f'{quoi} ({modele}) : ' + ' ; '.join(noms))
    if OUI:
        odoo(modele, 'unlink', ids)


def defaire_projet(nom):
    """Retire un projet de formation : ses feuilles de temps, ses tâches, ses étapes propres, puis le projet."""
    projets = odoo('project.project', 'search', [['name', '=', nom]], context={'active_test': False})
    if not projets:
        return
    retirer('account.analytic.line', odoo('account.analytic.line', 'search', [['project_id', 'in', projets]]), 'feuilles de temps')
    retirer('project.task', odoo('project.task', 'search', [['project_id', 'in', projets]], context={'active_test': False}), 'tâches')
    etapes = odoo('project.task.type', 'search_read', [['project_ids', 'in', projets]], fields=['project_ids'],
                  context={'active_test': False})
    retirer('project.task.type', [e['id'] for e in etapes if set(e['project_ids']) <= set(projets)], 'étapes propres au projet')
    retirer('project.project', projets, 'projet')


def con_01():
    # CON-01 crée à l'écran le projet de déploiement, ses 6 étapes (les phases) et quelques tâches.
    # État de départ : aucun projet « … (formation) ».
    defaire_projet(PROJET_CON01)
    return 'aucun projet de formation'


ARTICLES_CON02 = ['Projet Délices de Maïmouna', 'Projet Délices de Maïmouna (formation)']  # racines, et leurs sous-articles


def con_02():
    # CON-02 crée à l'écran, dans l'espace privé du formateur, l'article « Projet Délices de Maïmouna » et ses
    # sous-articles (compte-rendu d'atelier, cahier des charges). Rien n'est partagé ni envoyé.
    racines = odoo('knowledge.article', 'search', [['name', 'in', ARTICLES_CON02], ['create_uid', '=', FORMATEUR]],
                   context={'active_test': False})
    if racines:
        tous = odoo('knowledge.article', 'search', [['id', 'child_of', racines]], context={'active_test': False})
        enfants = [i for i in tous if i not in racines]
        retirer('knowledge.article', enfants, 'sous-articles')
        retirer('knowledge.article', racines, 'article du projet')
    # un tournage interrompu laisse parfois un article privé vide (« Sans titre ») dans l'espace du formateur
    retirer('knowledge.article', odoo('knowledge.article', 'search', [['name', '=', False], ['create_uid', '=', FORMATEUR],
                                                                       ['category', '=', 'private']],
                                      context={'active_test': False}), 'article vide laissé par un essai')
    return 'aucun article de formation'


PROJET_CON04 = 'Recette — Délices de Maïmouna'
ETAPES_CON04 = ['Signalée', 'Qualifiée', 'En correction', 'À re-tester', 'Clôturée']
ETIQUETTES_CON04 = ['Gravité 1 — bloquant', 'Gravité 2 — contournable', 'Gravité 3 — mineur', 'Erreur de formation',
                    'Nouvelle demande']


def con_04():
    # CON-04 : le projet de recette (préparé par l'API), ses étapes, ses tâches, puis les étiquettes de gravité
    # (les étiquettes de projet sont communes à toute la base : on ne retire que celles-ci, aux noms de la capsule).
    defaire_projet(PROJET_CON04)
    retirer('project.tags', odoo('project.tags', 'search', [['name', 'in', ETIQUETTES_CON04]]), 'étiquettes de la recette')
    return 'aucun projet de recette'


def preparer_con04():
    """Le projet « Recette » aux 5 étapes, les étiquettes, et deux signalements déjà reçus (créés hors caméra)."""
    if odoo('project.project', 'search', [['name', '=', PROJET_CON04]]):
        return 'projet de recette déjà prêt'
    tags = {}
    for n in ETIQUETTES_CON04:
        t = odoo('project.tags', 'search', [['name', '=', n]])
        tags[n] = t[0] if t else odoo('project.tags', 'create', {'name': n})
    projet = odoo('project.project', 'create', {'name': PROJET_CON04, 'allow_timesheets': False})
    etapes = {n: odoo('project.task.type', 'create', {'name': n, 'sequence': i, 'project_ids': [[6, 0, [projet]]],
                                                      'fold': False})
              for i, n in enumerate(ETAPES_CON04)}
    taches = [
        ("R-T-03 : pas d'activité pour Moussa quand on confirme un mariage", 'Qualifiée', 'Gravité 1 — bloquant',
         "<p><b>Scénario :</b> R-T-03 (Awa). <b>Fait :</b> confirmé le devis S00083 (mariage). <b>Attendu :</b> une activité "
         "pour Moussa. <b>Obtenu :</b> aucune activité.</p>"),
        ("Je ne trouve pas le bouton Envoyer sur le devis", 'Signalée', None,
         "<p><b>Signalé par :</b> Awa. <b>Fait :</b> devis ouvert, cherché le bouton d'envoi en bas de page.</p>"),
        ("Ce serait bien d'avoir aussi un rapport des baptêmes", 'Signalée', None,
         "<p><b>Signalé par :</b> Maïmouna DIOP, pendant la recette.</p>"),
    ]
    for nom, etape, tag, desc in taches:
        odoo('project.task', 'create', {'name': nom, 'project_id': projet, 'stage_id': etapes[etape], 'description': desc,
                                        'tag_ids': [[6, 0, [tags[tag]] if tag else []]], 'user_ids': [[6, 0, [FORMATEUR]]]})
    return f'projet de recette prêt ({len(taches)} signalements)'


def employe():
    """CON-06 : le compte « Formateur TAAGG » a besoin d'une fiche employé pour saisir du temps (accord de Babacar)."""
    e = odoo('hr.employee', 'search', [['user_id', '=', FORMATEUR]], context={'active_test': False})
    if e:
        odoo('hr.employee', 'write', e, {'active': True})
        return f'employé {EMPLOYE} réactivé'
    odoo('hr.employee', 'create', {'name': EMPLOYE, 'user_id': FORMATEUR})
    return f'employé {EMPLOYE} créé'


CAPSULES = {'CON-01': con_01, 'CON-02': con_02, 'CON-04': con_04}

if __name__ == '__main__':
    code = next((a for a in sys.argv[1:] if not a.startswith('--')), '')
    if PREPARER:
        print(code, '— préparation (création seulement) :', employe() if code == 'CON-06' or '--employe' in sys.argv else '',
              preparer_con04() if code == 'CON-04' else '')
        sys.exit(0)
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    print(code, '— ' + ('remise à zéro' if OUI else "aperçu (rien n'est modifié ; ajouter --oui pour défaire)"))
    print(code, 'prête :', CAPSULES[code]())
