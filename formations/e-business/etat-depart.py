#!/usr/bin/env python3
"""État de départ des capsules E-Business, préparé par l'API (jamais à la main à l'écran).

    python3 formations/e-business/etat-depart.py EB-01        # prépare la base pour EB-01
    python3 formations/e-business/etat-depart.py EB-01 --voir # montre ce qui serait fait, sans rien changer

Lit ODOO_URL, ODOO_BASE, ODOO_LOGIN_API et ODOO_CLE_API dans le .env du dépôt.
Chaque fonction peut être relancée autant de fois qu'on veut : elle remet le même état.
On ne supprime rien : on dépublie, on annule ou on archive.
"""
import base64
import json
import sys
import urllib.request
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent.parent
IMAGES = ICI / 'images'
VOIR = '--voir' in sys.argv

# ---------------------------------------------------------------- connexion

def lire_env():
    env = {}
    for ligne in (RACINE / '.env').read_text(encoding='utf-8').splitlines():
        ligne = ligne.split(' #')[0].strip()
        if '=' in ligne and not ligne.startswith('#'):
            k, v = ligne.split('=', 1)
            env[k.strip()] = v.strip().strip('"\'')
    return env

ENV = lire_env()
URL, BASE, CLE = ENV['ODOO_URL'].rstrip('/'), ENV['ODOO_BASE'], ENV['ODOO_CLE_API']


def rpc(service, methode, *args):
    corps = json.dumps({'jsonrpc': '2.0', 'method': 'call', 'params': {'service': service, 'method': methode, 'args': args}})
    req = urllib.request.Request(URL + '/jsonrpc', corps.encode(), {'Content-Type': 'application/json'})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    if 'error' in r:
        raise SystemExit(f"✗ Odoo : {r['error']['data'].get('message', r['error'])}")
    return r['result']


UID = rpc('common', 'login', BASE, ENV['ODOO_LOGIN_API'], CLE)
CTX = {'lang': 'fr_FR'}


def odoo(modele, methode, *args, **kw):
    kw.setdefault('context', CTX)
    return rpc('object', 'execute_kw', BASE, UID, CLE, modele, methode, list(args), kw)


def ecrire(modele, ids, valeurs, quoi):
    print(f'  · {quoi}')
    if not VOIR and ids:
        odoo(modele, 'write', ids, valeurs)


def image(nom):
    f = IMAGES / nom
    return base64.b64encode(f.read_bytes()).decode() if f.exists() else None

# ---------------------------------------------------------------- la boutique d'exemple

SITE = 1  # site « correction les délices de maimouna »

# Coordonnées fictives affichées sur le site (jamais de vraies personnes)
TELEPHONE = '+221 33 800 00 00'
EMAIL = 'commandes@delices-maimouna.sn'

# Catalogue de la boutique : catégorie de la boutique → {produit: prix TTC en francs CFA}
# (TVA 18 % non comprise dans les prix Odoo : on cherche le prix HT en francs entiers qui redonne
#  exactement ce TTC ; certains TTC sont impossibles, ex. 600 F → 599 ou 601 : choisir un autre prix)
CATALOGUE = {
    'Gâteaux': {
        'Fraisier': 18000, 'Forêt Noire': 16000, 'Opéra': 20000, "Gâteau d'anniversaire": 24000,
    },
    'Pâtisseries': {
        'Éclair au chocolat': 1500, 'Éclair au café': 1500, 'Millefeuille': 1500, 'Paris-Brest': 2000,
        'Religieuse': 1500, 'Tartelette aux fruits': 1500, 'Macaron': 500, 'Moelleux au chocolat': 1500,
    },
    'Viennoiseries': {
        'Croissant': 400, 'Croissant aux amandes': 700, 'Pain au chocolat (Chocolatine)': 500,
        'Pain aux raisins': 650, 'Chausson aux pommes': 700,
    },
}

# Clients fictifs et leurs commandes passées sur la boutique (affichées dans eCommerce › Commandes)
CLIENTS = [
    {'name': 'Awa Diop', 'email': 'awa.diop@exemple.sn', 'phone': '+221 77 000 00 00', 'city': 'Dakar'},
    {'name': 'Moussa Ndiaye', 'email': 'moussa.ndiaye@exemple.sn', 'phone': '+221 77 000 00 01', 'city': 'Pikine'},
    {'name': 'Khady Sarr', 'email': 'khady.sarr@exemple.sn', 'phone': '+221 77 000 00 02', 'city': 'Dakar'},
]
# La TVA est arrondie sur le total de la commande : ces paniers tombent sur des totaux ronds
# (28 000, 20 000 et 26 000 F) ; vérifier le total affiché si on les change.
COMMANDES = [  # (repère, client, [(produit, quantité)])
    ('EB-DEMO-1', 'Awa Diop', [("Gâteau d'anniversaire", 1), ('Croissant', 10)]),
    ('EB-DEMO-2', 'Moussa Ndiaye', [('Forêt Noire', 1), ('Croissant', 10)]),
    ('EB-DEMO-3', 'Khady Sarr', [('Fraisier', 1), ('Paris-Brest', 4)]),
]


def site_et_coordonnees():
    print('Site : nom, logo, prix TTC, coordonnées fictives')
    valeurs = {'name': 'Les Délices de Maïmouna', 'show_line_subtotals_tax_selection': 'tax_included'}
    # vendeur des commandes du site : le compte fictif « Formateur TAAGG » (jamais une vraie personne)
    formateur = odoo('res.users', 'search', [('login', '=', ENV.get('ODOO_LOGIN', ''))])
    if formateur:
        valeurs['salesperson_id'] = formateur[0]
    logo = image('logo-delices-maimouna.png')
    if logo:
        valeurs['logo'] = logo
    ecrire('website', [SITE], valeurs, 'nom « Les Délices de Maïmouna », logo, prix affichés TTC, vendeur Formateur TAAGG')
    # filtres de la boutique : masquer les caractéristiques qui ne concernent pas la pâtisserie
    inutiles = odoo('product.attribute', 'search', [('name', 'in', ['Taille', 'Type de poisson', 'Poissons gras', 'Type de viande', 'Type', 'Parfum / Saveur'])])
    ecrire('product.attribute', inutiles, {'visibility': 'hidden'}, f'{len(inutiles)} filtres inutiles masqués dans la boutique')
    # filtre « Fourchette de prix » : il affiche les prix hors taxes (1 à 20 339 F), source de confusion
    ctx = dict(CTX, website_id=SITE)
    filtre = odoo('ir.ui.view', 'search', [('key', '=', 'website_sale.filter_products_price'), ('website_id', 'in', [False, SITE])],
                  order='website_id', context=dict(ctx, active_test=False))
    if filtre:
        print('  · filtre « Fourchette de prix » masqué')
        if not VOIR:
            odoo('ir.ui.view', 'write', [filtre[-1]], {'active': False}, context=ctx)
    # en-tête et pied de page : remplacer les coordonnées de démonstration d'Odoo
    # (écrire avec website_id dans le contexte crée une copie propre au site, comme l'éditeur)
    ctx = dict(CTX, website_id=SITE)
    for cle in ('website.header_text_element', 'website.footer_custom', 'website.contactus', 'website.s_contact_info'):
        vues = odoo('ir.ui.view', 'search_read', [('key', '=', cle), ('website_id', 'in', [False, SITE])],
                    fields=['arch_db', 'website_id'], order='website_id', context=ctx)
        if not vues:
            continue
        vue = next((v for v in vues if v['website_id']), vues[0])
        arch = (vue['arch_db'].replace('+1 555-555-5556', TELEPHONE).replace('+1 (650) 555-0111', TELEPHONE)
                .replace('info@yourcompany.example.com', EMAIL))
        if arch != vue['arch_db']:
            print(f'  · coordonnées fictives dans {cle}')
            if not VOIR:
                odoo('ir.ui.view', 'write', [vue['id']], {'arch_db': arch}, context=ctx)


def catalogue():
    print('Catalogue : catégories, prix, photos, publication')
    tous = odoo('product.template', 'search_read', [('sale_ok', '=', True)], fields=['name', 'is_published'])
    par_nom = {p['name']: p['id'] for p in tous}
    a_publier = set()
    for rang, (categorie, produits) in enumerate(CATALOGUE.items()):
        cat = odoo('product.public.category', 'search', [('name', '=', categorie)])
        if not cat:
            print(f'  · nouvelle catégorie de la boutique « {categorie} »')
            cat = [0] if VOIR else [odoo('product.public.category', 'create', {'name': categorie, 'sequence': rang + 1})]
        for nom, ttc in produits.items():
            if nom not in par_nom:
                print(f'  ⚠ produit introuvable : {nom}')
                continue
            pid = par_nom[nom]
            a_publier.add(pid)
            ht = next((h for h in range(int(ttc / 1.18) - 2, int(ttc / 1.18) + 3) if round(h * 1.18) == ttc), None)
            if ht is None:
                raise SystemExit(f'✗ {nom} : {ttc} F TTC impossible avec la TVA 18 % en francs entiers, choisir un autre prix')
            valeurs = {'list_price': ht, 'public_categ_ids': [(6, 0, cat)], 'is_published': True,
                       'taxes_id': [(6, 0, [5])]}  # TVA 18 %
            photo = image(f'produits/{slug(nom)}.jpg')
            if photo:
                valeurs['image_1920'] = photo
            ecrire('product.template', [pid], valeurs, f'{nom} : {ttc:,} F TTC'.replace(',', ' ') + (', photo' if photo else ''))
    autres = [p['id'] for p in tous if p['id'] not in a_publier and p['is_published']]
    ecrire('product.template', autres, {'is_published': False}, f'{len(autres)} autres produits dépubliés')


def slug(texte):
    import unicodedata
    t = unicodedata.normalize('NFD', texte.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return '-'.join(''.join(c if c.isalnum() else ' ' for c in t).split())


def clients_et_commandes():
    print('Clients fictifs et commandes de la boutique')
    ids = {}
    for c in CLIENTS:
        trouve = odoo('res.partner', 'search', [('email', '=', c['email'])], limit=1)
        if trouve:
            ids[c['name']] = trouve[0]
        else:
            print(f"  · nouveau client {c['name']}")
            ids[c['name']] = 0 if VOIR else odoo('res.partner', 'create', dict(c, country_id=odoo('res.country', 'search', [('code', '=', 'SN')])[0]))
    produits = {p['name']: p['product_variant_id'][0] for p in
                odoo('product.template', 'search_read', [('sale_ok', '=', True)], fields=['name', 'product_variant_id'])}
    for repere, client, lignes in COMMANDES:
        if odoo('sale.order', 'search', [('client_order_ref', '=', repere)]):
            continue
        print(f'  · commande en ligne {repere} de {client}')
        if VOIR:
            continue
        # sans messages dans l'historique : ils seraient signés du compte API (une vraie personne)
        silence = dict(CTX, tracking_disable=True, mail_create_nolog=True, mail_notrack=True, mail_notify_force_send=False)
        cmd = odoo('sale.order', 'create', {
            'partner_id': ids[client], 'website_id': SITE, 'client_order_ref': repere,
            'user_id': odoo('website', 'read', [SITE], ['salesperson_id'])[0]['salesperson_id'][0],
            'order_line': [(0, 0, {'product_id': produits[p], 'product_uom_qty': q}) for p, q in lignes]}, context=silence)
        odoo('sale.order', 'action_confirm', [cmd], context=silence)
        auteurs = odoo('mail.message', 'search_read', [('model', '=', 'sale.order'), ('res_id', '=', cmd)], fields=['author_id'])
        if auteurs:
            print(f'    ⚠ {len(auteurs)} message(s) dans l’historique de la commande : vérifier l’auteur affiché')
        total = odoo('sale.order', 'read', [cmd], ['amount_total'])[0]['amount_total']
        print(f'    total {total:,.0f} F'.replace(',', ' ') + ('' if total % 500 == 0 else '  ⚠ total pas rond'))


def paniers_de_tournage():
    # les paniers laissés par les tournages précédents (compte Formateur TAAGG) encombrent les listes
    formateur = odoo('res.users', 'search_read', [('login', '=', ENV.get('ODOO_LOGIN', ''))], fields=['partner_id'])
    if not formateur:
        return
    paniers = odoo('sale.order', 'search', [('website_id', '!=', False), ('state', '=', 'draft'),
                                           ('partner_id', '=', formateur[0]['partner_id'][0])])
    if paniers:
        print(f'  · {len(paniers)} panier(s) de tournage annulé(s)')
        if not VOIR:
            odoo('sale.order', 'action_cancel', paniers)

# ---------------------------------------------------------------- capsules

def eb_01():
    """EB-01 · De WhatsApp à la boutique en ligne : boutique présentable, 3 commandes passées."""
    site_et_coordonnees()
    catalogue()
    clients_et_commandes()
    paniers_de_tournage()


CAPSULES = {'EB-01': eb_01}

if __name__ == '__main__':
    code = next((a.upper() for a in sys.argv[1:] if not a.startswith('--')), None)
    if code not in CAPSULES:
        raise SystemExit(f"Usage : python3 {Path(__file__).name} <{'|'.join(CAPSULES)}> [--voir]")
    print(f"▶ État de départ {code}{' (simulation)' if VOIR else ''} — {URL}")
    CAPSULES[code]()
    print('✓ Terminé')
