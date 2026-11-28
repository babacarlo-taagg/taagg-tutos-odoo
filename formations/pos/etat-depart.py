"""Remet la base de tournage dans l'état de départ d'une capsule Point de Vente (POS-xx), par l'API (jamais à l'écran).

Usage : python3 formations/pos/etat-depart.py POS-01              montre ce qui serait défait, ne touche à rien
        python3 formations/pos/etat-depart.py POS-01 --oui        défait (accord permanent de Babacar pour ce que
                                                                  les capsules créent)
        python3 formations/pos/etat-depart.py POS-01 --preparer   crée seulement ce qui manque, ne retire rien

Ne défait QUE ce que les capsules POS créent, tout étant postérieur à l'installation du Point de Vente (17/11/2026) :
le point de vente « Comptoir Médina », les modes de paiement (il n'en existait aucun avant), les journaux créés par
Odoo à la première caisse (« Point de Vente », « Espèces ») et ceux préparés pour le comptoir (« Wave Comptoir »,
« Orange Money Comptoir »), avec leurs comptes. Jamais les journaux « Caisse boutique », « Wave », « Bank » ni les
produits existants. Les écritures des sessions clôturées (POS-04 et suivantes) restent (choix de Babacar, 28/11).
Travaille avec le compte « Formateur TAAGG » (droits Point de Vente / Administrateur, ajoutés le 28/11).
Lit ODOO_URL, ODOO_BASE, ODOO_LOGIN et ODOO_MOT_DE_PASSE dans l'environnement, sinon dans le .env du projet.
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
INSTALLATION = '2026-11-17 00:00:00'  # rien de ce qui est plus ancien n'est touché
CAISSE = 'Comptoir Médina'
JOURNAUX_ODOO = ['Point de Vente', 'Espèces']  # créés par Odoo à la première caisse
JOURNAUX_COMPTOIR = [('Wave Comptoir', 'WAVC'), ('Orange Money Comptoir', 'OMC')]  # préparés par l'API
OUI = '--oui' in sys.argv
PREPARER = '--preparer' in sys.argv


def appel(service, methode, *args):
    corps = {'jsonrpc': '2.0', 'method': 'call', 'params': {'service': service, 'method': methode, 'args': args}}
    req = urllib.request.Request(ENV['ODOO_URL'] + '/jsonrpc', json.dumps(corps).encode(), {'Content-Type': 'application/json'})
    rep = json.load(urllib.request.urlopen(req, timeout=60))
    if 'error' in rep:
        sys.exit('Odoo a refusé : ' + rep['error']['data'].get('message', str(rep['error'])))
    return rep.get('result')


UID = appel('common', 'authenticate', ENV['ODOO_BASE'], ENV['ODOO_LOGIN'], ENV['ODOO_MOT_DE_PASSE'], {})


def odoo(modele, methode, *args, **kw):
    return appel('object', 'execute_kw', ENV['ODOO_BASE'], UID, ENV['ODOO_MOT_DE_PASSE'], modele, methode, list(args), kw)


def chercher(modele, domaine):
    return odoo(modele, 'search', domaine + [['create_date', '>', INSTALLATION]], context={'active_test': False})


def retirer(modele, ids, quoi):
    """Montre ce qui serait retiré ; ne le retire qu'avec --oui."""
    if not ids:
        return
    noms = [r['display_name'] for r in odoo(modele, 'read', ids, fields=['display_name'])]
    print(('  RETIRÉ  ' if OUI else '  à retirer  ') + f'{quoi} ({modele}) : ' + ' ; '.join(noms))
    if OUI:
        odoo(modele, 'unlink', ids)


def journaux(noms):
    return chercher('account.journal', [['name', 'in', noms]])


def pos_01():
    # POS-01 crée à l'écran le point de vente (Odoo ajoute alors les journaux « Point de Vente » et « Espèces » et
    # 3 modes de paiement), retire « Carte » et « Compte client », ajoute Wave et Orange Money.
    # État de départ : aucun point de vente, aucun mode de paiement ; les 2 journaux « Comptoir » existent.
    retirer('pos.config', chercher('pos.config', []), 'points de vente')
    retirer('pos.payment.method', chercher('pos.payment.method', []), 'modes de paiement')
    ids = journaux(JOURNAUX_ODOO)
    comptes = [j['default_account_id'][0] for j in odoo('account.journal', 'read', ids, fields=['default_account_id'])
               if j['default_account_id']]
    retirer('account.journal', ids, 'journaux créés par la première caisse')
    retirer('account.account', chercher('account.account', [['id', 'in', comptes]]), 'leurs comptes')
    return 'aucun point de vente ; journaux « Comptoir » : ' + preparer_pos01()


def preparer_pos01():
    faits = []
    for nom, code in JOURNAUX_COMPTOIR:
        if not journaux([nom]):
            if OUI or PREPARER:
                odoo('account.journal', 'create', {'name': nom, 'code': code, 'type': 'bank'})
                faits.append(nom + ' créé')
            else:
                faits.append(nom + ' à créer')
        else:
            faits.append(nom + ' présent')
    return ', '.join(faits)


CATEGORIES_POS = ['Boissons', 'Pâtisseries', 'Snacks']  # « Boissons » est créée à l'écran (POS-02)
TAXE_TTC = '18% TTC'  # taxe existante de la base, prix TTC
# Produits préparés pour POS-02 : nom, prix TTC, catégorie de caisse, disponible en caisse.
# « Fataya » est volontairement NON disponible en caisse : c'est l'oubli corrigé à l'écran.
PRODUITS_POS02 = [('Part de fraisier', 1500, 'Pâtisseries', True), ("Part d'opéra", 1500, 'Pâtisseries', True),
                  ('Croissant du comptoir', 350, 'Pâtisseries', True), ('Beignet', 250, 'Snacks', True),
                  ('Thiakry (pot)', 750, 'Snacks', True), ('Fataya', 250, 'Snacks', False)]
PRODUITS_ECRAN = ['Jus de bissap 33 cl']  # créés à l'écran


def pos_02():
    # POS-02 crée à l'écran la catégorie « Boissons » et le produit « Jus de bissap 33 cl », et rend « Fataya »
    # disponible en caisse. État de départ : la caisse de POS-01 ; les 6 produits et 2 catégories préparés.
    noms = [p[0] for p in PRODUITS_POS02] + PRODUITS_ECRAN
    retirer('product.template', chercher('product.template', [['name', 'in', noms]]), 'produits du comptoir')
    retirer('pos.category', chercher('pos.category', [['name', 'in', CATEGORIES_POS]]), 'catégories de caisse')
    return preparer_pos02()


def preparer_pos02():
    if not (OUI or PREPARER):
        return 'produits et catégories à préparer'
    if not chercher('pos.config', [['name', '=', CAISSE]]):
        return 'ATTENTION : la caisse « Comptoir Médina » manque (tourner POS-01 d\'abord)'
    categ = {}
    for nom in ['Pâtisseries', 'Snacks']:
        ids = chercher('pos.category', [['name', '=', nom]])
        categ[nom] = ids[0] if ids else odoo('pos.category', 'create', {'name': nom})
    taxe = odoo('account.tax', 'search', [['name', '=', TAXE_TTC], ['type_tax_use', '=', 'sale']])
    faits = 0
    for nom, prix, cat, en_caisse in PRODUITS_POS02:
        if chercher('product.template', [['name', '=', nom]]):
            continue
        pid = odoo('product.template', 'create', {'name': nom, 'list_price': prix, 'type': 'consu',
                                                   'is_storable': False, 'taxes_id': [[6, 0, taxe]],
                                                   'pos_categ_ids': [[6, 0, [categ[cat]]]]})
        # Odoo coche « Point de Vente » dès qu'une catégorie de caisse est posée : on fixe la case après coup.
        odoo('product.template', 'write', [pid], {'available_in_pos': en_caisse})
        faits += 1
    return f'{faits} produits créés, catégories Pâtisseries et Snacks prêtes'


CAPSULES = {'POS-01': pos_01, 'POS-02': pos_02}

if __name__ == '__main__':
    code = next((a for a in sys.argv[1:] if not a.startswith('--')), '')
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    if PREPARER:
        print(code, '— préparation (création seulement) :', {'POS-01': preparer_pos01, 'POS-02': preparer_pos02}[code]())
        sys.exit(0)
    print(code, '— ' + ('remise à zéro' if OUI else "aperçu (rien n'est modifié ; ajouter --oui pour défaire)"))
    print(code, 'prête :', CAPSULES[code]())
