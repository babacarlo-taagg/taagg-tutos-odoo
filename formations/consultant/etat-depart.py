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


def employe():
    """CON-06 : le compte « Formateur TAAGG » a besoin d'une fiche employé pour saisir du temps (accord de Babacar)."""
    e = odoo('hr.employee', 'search', [['user_id', '=', FORMATEUR]], context={'active_test': False})
    if e:
        odoo('hr.employee', 'write', e, {'active': True})
        return f'employé {EMPLOYE} réactivé'
    odoo('hr.employee', 'create', {'name': EMPLOYE, 'user_id': FORMATEUR})
    return f'employé {EMPLOYE} créé'


CAPSULES = {'CON-01': con_01, 'CON-02': con_02}

if __name__ == '__main__':
    code = next((a for a in sys.argv[1:] if not a.startswith('--')), '')
    if PREPARER:
        print(code, '— préparation (création seulement) :', employe() if code == 'CON-06' or '--employe' in sys.argv else '')
        sys.exit(0)
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    print(code, '— ' + ('remise à zéro' if OUI else "aperçu (rien n'est modifié ; ajouter --oui pour défaire)"))
    print(code, 'prête :', CAPSULES[code]())
