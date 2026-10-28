"""Remet la base de tournage dans l'état de départ d'une capsule, par l'API (jamais à l'écran).

Usage : python3 formations/comptabilite/etat-depart.py CPT-02
Lit ODOO_URL, ODOO_BASE, ODOO_LOGIN_API et ODOO_CLE_API dans l'environnement, sinon dans le .env du projet.
"""
import json
import os
import pathlib
import sys
import urllib.request

ICI = pathlib.Path(__file__).resolve().parents[2]
ENV = dict(l.split('=', 1) for l in (ICI / '.env').read_text().splitlines() if '=' in l and not l.startswith('#'))
ENV = {k.strip(): v.split('#')[0].strip() for k, v in ENV.items()}
ENV.update({k: v for k, v in os.environ.items() if k.startswith('ODOO_')})  # les variables d'environnement passent avant le .env
SOCIETE = 1  # « correction les délices de maimouna »


def appel(service, methode, *args):
    corps = {'jsonrpc': '2.0', 'method': 'call', 'params': {'service': service, 'method': methode, 'args': args}}
    req = urllib.request.Request(ENV['ODOO_URL'] + '/jsonrpc', json.dumps(corps).encode(), {'Content-Type': 'application/json'})
    rep = json.load(urllib.request.urlopen(req, timeout=60))
    if 'error' in rep:
        sys.exit('Odoo a refusé : ' + rep['error']['data'].get('message', str(rep['error'])))
    return rep['result']


UID = appel('common', 'authenticate', ENV['ODOO_BASE'], ENV['ODOO_LOGIN_API'], ENV['ODOO_CLE_API'], {})


def odoo(modele, methode, *args, **kw):
    return appel('object', 'execute_kw', ENV['ODOO_BASE'], UID, ENV['ODOO_CLE_API'], modele, methode, list(args), kw)


def cpt_02():
    # adresse vide, aucune mise en page choisie, montant en lettres décoché
    odoo('res.company', 'write', [SOCIETE], {
        'street': False, 'city': False,
        'external_report_layout_id': False,
        'display_invoice_amount_total_words': False,
    })
    return odoo('res.company', 'read', [SOCIETE], fields=['street', 'city', 'external_report_layout_id', 'display_invoice_amount_total_words'])


def cpt_03():
    # le compte 702110 « Ventes de pâtisseries » est créé à l'écran : on l'enlève s'il existe (jamais utilisé)
    ids = odoo('account.account', 'search', [['code', 'in', ['702110']]], context={'allowed_company_ids': [SOCIETE]})
    if ids:
        odoo('account.account', 'unlink', ids)
    return odoo('account.account', 'search_count', [['code', '=', '702110']], context={'allowed_company_ids': [SOCIETE]})


def cpt_04():
    # le journal « Caisse boutique » (préfixe CAI) est créé à l'écran : on l'enlève s'il existe et n'a jamais servi
    ids = odoo('account.journal', 'search', [['code', '=', 'CAI'], ['company_id', '=', SOCIETE]], context={'active_test': False})
    if ids:
        odoo('account.journal', 'unlink', ids)
    # et le compte que Odoo crée avec lui (571001 « Caisse boutique »)
    comptes = odoo('account.account', 'search', [['code', '=like', '5710%'], ['name', '=', 'Caisse boutique']], context={'allowed_company_ids': [SOCIETE]})
    if comptes:
        odoo('account.account', 'unlink', comptes)
    return odoo('account.journal', 'search_count', [['code', '=', 'CAI'], ['company_id', '=', SOCIETE]]), len(comptes)


CAPSULES = {'CPT-02': cpt_02, 'CPT-03': cpt_03, 'CPT-04': cpt_04}

if __name__ == '__main__':
    code = sys.argv[1] if len(sys.argv) > 1 else ''
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    print(code, 'prête :', CAPSULES[code]())
