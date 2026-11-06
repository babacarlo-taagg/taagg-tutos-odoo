#!/usr/bin/env python3
"""État de départ des capsules E-Business, préparé par l'API (jamais à la main à l'écran).

    python3 formations/e-business/etat-depart.py EB-01        # prépare la base pour EB-01
    python3 formations/e-business/etat-depart.py EB-01 --voir # montre ce qui serait fait, sans rien changer

Lit ODOO_URL, ODOO_BASE, ODOO_LOGIN_API et ODOO_CLE_API dans le .env du dépôt.
Chaque fonction peut être relancée autant de fois qu'on veut : elle remet le même état.
On ne supprime rien : on dépublie, on annule ou on archive (seule exception : les fiches que les prises
d'une capsule créent elles-mêmes, ex. la catégorie et l'attribut d'EB-05).
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
    return r.get('result')  # certaines méthodes (ex. action_apply_inventory) ne renvoient rien


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
    # e-mail de la société (factures, e-mails, page Contact) : adresse fictive, jamais une vraie personne ;
    # nom de la société remis (la ligne Copyright du pied de page le modifie si on l'édite dans l'éditeur,
    # et la formation Comptabilité l'utilise tel quel)
    ecrire('res.company', [1], {'email': EMAIL, 'name': 'correction les délices de maimouna'},
           f'e-mail de la société : {EMAIL} ; nom de la société d\'origine')
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

ACCUEIL_VIDE = '''<t name="Homepage" t-name="website.homepage">
    <t t-call="website.layout" pageName.f="homepage">
        <div id="wrap" class="oe_structure oe_empty"/>
    </t>
</t>'''

# fichiers de style du site qui retiennent les couleurs, polices… choisies dans l'onglet Thème
# (contenu d'origine gardé dans donnees/, relevé le 29/10/2026)
STYLES = {
    '/_custom/web.assets_frontend/website/static/src/scss/options/user_values.scss': 'user_values.scss',
    '/_custom/web.assets_frontend/website/static/src/scss/options/colors/user_theme_color_palette.scss': 'user_theme_color_palette.scss',
}

# photos proposées dans la médiathèque de l'éditeur (double-clic sur une image du site)
MEDIATHEQUE = ['fraisier.jpg', 'gateau-d-anniversaire.jpg', 'foret-noire.jpg', 'tartelette-aux-fruits.jpg']


def accueil_et_theme():
    print("Site : page d'accueil vide, thème d'origine, médiathèque")
    ctx = dict(CTX, website_id=SITE)
    vue = odoo('ir.ui.view', 'search', [('key', '=', 'website.homepage'), ('website_id', '=', SITE)], context=ctx)
    ecrire('ir.ui.view', vue, {'arch_db': ACCUEIL_VIDE}, "page d'accueil vidée (« Glissez un bloc ici »)")
    for url, nom in STYLES.items():
        piece = odoo('ir.attachment', 'search', [('url', '=', url), ('website_id', '=', SITE)])
        contenu = base64.b64encode((ICI / 'donnees' / nom).read_bytes()).decode()
        ecrire('ir.attachment', piece, {'datas': contenu}, f"style d'origine : {nom}")
    for nom in MEDIATHEQUE:
        if odoo('ir.attachment', 'search', [('name', '=', nom), ('res_model', '=', 'ir.ui.view')]):
            continue
        print(f'  · photo {nom} ajoutée à la médiathèque')
        if not VOIR:
            odoo('ir.attachment', 'create', {'name': nom, 'datas': image(f'produits/{nom}'), 'res_model': 'ir.ui.view',
                                             'res_id': 0, 'public': True, 'mimetype': 'image/jpeg'})

# ---------------------------------------------------------------- capsules

def eb_01():
    """EB-01 · De WhatsApp à la boutique en ligne : boutique présentable, 3 commandes passées."""
    site_et_coordonnees()
    accueil_et_theme()
    catalogue()
    clients_et_commandes()
    paniers_de_tournage()


def eb_02():
    """EB-02 · Construire son site : même boutique qu'EB-01, page d'accueil vide, couleurs d'origine,
    4 photos dans la médiathèque. Le tournage remplit la page d'accueil et change les couleurs :
    relancer ce script avant chaque prise (et avant de retourner EB-01)."""
    eb_01()


PAGES_EB03 = ['/a-propos', '/livraison-et-retours']   # pages créées pendant le tournage d'EB-03


def site_fin_eb02():
    """Le site tel qu'à la fin d'EB-02 : page d'accueil construite, palette caramel (relevés le 31/10/2026)."""
    print("Site : page d'accueil et couleurs de la fin d'EB-02")
    ctx = dict(CTX, website_id=SITE)
    vue = odoo('ir.ui.view', 'search', [('key', '=', 'website.homepage'), ('website_id', '=', SITE)], context=ctx)
    ecrire('ir.ui.view', vue, {'arch_db': (ICI / 'donnees' / 'eb02-accueil.xml').read_text(encoding='utf-8')},
           "page d'accueil d'EB-02 (accroche + Nos gâteaux du moment)")
    for url, nom in STYLES.items():
        piece = odoo('ir.attachment', 'search', [('url', '=', url), ('website_id', '=', SITE)])
        contenu = base64.b64encode((ICI / 'donnees' / f'eb02-{nom}').read_bytes()).decode()
        ecrire('ir.attachment', piece, {'datas': contenu}, f'couleurs EB-02 : {nom}')


def pages_de_confiance_a_refaire():
    """Défait ce que le tournage d'EB-03 crée ou change : pages, menus, Contact, pied de page, copyright."""
    print('Pages de confiance : remises à faire (état avant EB-03)')
    ctx = dict(CTX, website_id=SITE)
    # pages des tournages précédents (y compris /a-propos-1, -2… et celles déjà archivées)
    domaine = ['|'] * (len(PAGES_EB03) - 1) + [('url', '=like', f'{u}%') for u in PAGES_EB03] + [('website_id', '=', SITE)]
    pages = odoo('website.page', 'search_read', domaine, fields=['url', 'active'], context=dict(CTX, active_test=False))
    pages = [pg for pg in pages if not pg['url'].startswith('/archive-')]
    if pages:
        ids = [pg['id'] for pg in pages]
        menus = odoo('website.menu', 'search', [('page_id', 'in', ids)])
        print(f'  · {len(menus)} entrée(s) de menu retirée(s) (créées par le tournage)')
        if not VOIR and menus:
            odoo('website.menu', 'unlink', menus)
        print(f"  · {len(pages)} page(s) archivée(s), adresse libérée : " + ', '.join(pg['url'] for pg in pages))
        if not VOIR:
            for pg in pages:  # l'adresse /a-propos redevient libre pour la prochaine prise
                odoo('website.page', 'write', [pg['id']], {'active': False, 'url': f"/archive-{pg['id']}{pg['url']}"})
    for cle, fichier in (('website.contactus', 'contact-origine.xml'), ('website.footer_custom', 'pied-de-page-origine.xml')):
        vue = odoo('ir.ui.view', 'search', [('key', '=', cle), ('website_id', '=', SITE)], context=ctx)
        ecrire('ir.ui.view', vue, {'arch_db': (ICI / 'donnees' / fichier).read_text(encoding='utf-8')}, f'{cle} remis comme avant')
    # copie propre au site de la ligne « Copyright © Nom de l'entreprise » : archivée → texte d'origine
    copie = odoo('ir.ui.view', 'search', [('key', '=', 'website.footer_copyright_company_name'), ('website_id', '=', SITE)], context=ctx)
    ecrire('ir.ui.view', copie, {'active': False}, 'ligne de copyright d\'origine')
    if not odoo('ir.attachment', 'search', [('name', '=', 'maimouna-boutique.jpg'), ('res_model', '=', 'ir.ui.view')]):
        print('  · photo maimouna-boutique.jpg ajoutée à la médiathèque')
        if not VOIR:
            odoo('ir.attachment', 'create', {'name': 'maimouna-boutique.jpg', 'datas': image('eb-01-ambiance-whatsapp.jpg'),
                                             'res_model': 'ir.ui.view', 'res_id': 0, 'public': True, 'mimetype': 'image/jpeg'})


def eb_03():
    """EB-03 · Les pages qui donnent confiance : le site de la fin d'EB-02, sans pages À propos / Livraison,
    page Contact et pied de page encore remplis d'exemples d'Odoo (« Ma société », « Nous sommes une équipe… »)."""
    eb_01()
    site_fin_eb02()
    pages_de_confiance_a_refaire()


NOUVEAUX_PRODUITS_EB04 = ['Tarte au citron meringuée', 'Tarte test EB04']   # créés pendant les prises d'EB-04


def produits_eb04_a_refaire():
    """Archive les produits créés par les prises d'EB-04 et republie le chausson (dépublié pendant la capsule)."""
    print("Produits : remis comme avant EB-04")
    nouveaux = odoo('product.template', 'search', [('name', 'in', NOUVEAUX_PRODUITS_EB04)])
    ecrire('product.template', nouveaux, {'active': False, 'is_published': False},
           f'{len(nouveaux)} produit(s) des prises précédentes archivé(s)')
    chausson = odoo('product.template', 'search', [('name', '=', 'Chausson aux pommes')])
    ecrire('product.template', chausson, {'is_published': True}, 'Chausson aux pommes republié')


def eb_04():
    """EB-04 · Mettre ses produits en ligne : la boutique de la fin d'EB-03 (pages À propos, Livraison, Contact
    et pied de page corrigés restent tels quels), sans la Tarte au citron meringuée que la capsule crée."""
    eb_01()
    site_fin_eb02()
    produits_eb04_a_refaire()


# Ordre d'affichage de la boutique au début d'EB-05 (« En vedette ») : la capsule remonte le gâteau d'anniversaire
ORDRE_BOUTIQUE = [
    'Pain aux raisins', 'Millefeuille', 'Opéra', 'Paris-Brest', 'Tartelette aux fruits', 'Éclair au café',
    'Éclair au chocolat', 'Chausson aux pommes', 'Croissant', 'Croissant aux amandes',
    'Pain au chocolat (Chocolatine)', 'Religieuse', 'Forêt Noire', 'Fraisier', "Gâteau d'anniversaire", 'Macaron',
    'Moelleux au chocolat', 'Tarte au citron meringuée',
]
TARTE = {  # la tarte telle qu'elle est à la fin d'EB-04
    'name': 'Tarte au citron meringuée', 'list_price': 12712, 'standard_price': 6500, 'taxes_id': [(6, 0, [5])],
    'is_published': True, 'website_ribbon_id': False,
    'description_ecommerce': '<p>Pâte sablée, crème de citron frais et meringue dorée. 6 à 8 parts. '
                             'Commandez la veille avant 18 h.</p>',
}
FORMATEUR = 27  # contact « Formateur TAAGG » (seul auteur qu'on laisse dans l'historique des fiches filmées)


def catalogue_eb05_a_refaire():
    """Défait ce que les prises d'EB-05 créent : catégorie Tartes, attribut Nombre de parts (et les variantes
    du gâteau), ruban, ordre de la boutique. Ce sont des fiches créées par la capsule : on les supprime."""
    print('Catalogue : remis comme à la fin d’EB-04')
    if not VOIR:
        # la plus récente (celle de la prise finale d'EB-04) ; les tartes des prises d'essai restent archivées
        tarte = odoo('product.template', 'search', [('name', '=', TARTE['name'])], order='id desc',
                     context=dict(CTX, active_test=False))
        if tarte[1:]:
            odoo('product.template', 'write', tarte[1:], {'active': False, 'is_published': False})
        valeurs = dict(TARTE, active=True, public_categ_ids=[(6, 0, odoo('product.public.category', 'search', [('name', '=', 'Pâtisseries')]))])
        photo = image('produits/tarte-au-citron-meringuee.jpg')
        if photo:
            valeurs['image_1920'] = photo
        if tarte:
            odoo('product.template', 'write', tarte[:1], valeurs)
        else:
            odoo('product.template', 'create', valeurs, context=dict(CTX, tracking_disable=True))
    print('  · Tarte au citron meringuée : publiée, Pâtisseries, sans ruban')
    attributs = odoo('product.attribute', 'search', [('name', '=', 'Nombre de parts')], context=dict(CTX, active_test=False))
    lignes = odoo('product.template.attribute.line', 'search', [('attribute_id', 'in', attributs)]) if attributs else []
    print(f'  · {len(lignes)} ligne(s) de variantes et {len(attributs)} attribut « Nombre de parts » supprimés')
    if not VOIR and lignes:
        odoo('product.template.attribute.line', 'unlink', lignes)
    for attribut in ([] if VOIR else attributs):
        try:
            odoo('product.attribute', 'unlink', [attribut])
        except SystemExit:  # déjà dans une commande (panier d'essai) : Odoo refuse, on l'archive sous un autre nom
            odoo('product.attribute', 'write', [attribut], {'active': False, 'name': f'Nombre de parts (essai {attribut})'})
    tartes = odoo('product.public.category', 'search', [('name', '=', 'Tartes')])
    print(f'  · {len(tartes)} catégorie « Tartes » supprimée')
    if not VOIR and tartes:
        odoo('product.public.category', 'unlink', tartes)
    par_nom = {p['name']: p['id'] for p in odoo('product.template', 'search_read', [('name', 'in', ORDRE_BOUTIQUE)], fields=['name'])}
    print('  · ordre de la boutique remis (le gâteau d’anniversaire en 15e position)')
    for rang, nom in enumerate(ORDRE_BOUTIQUE):
        if nom in par_nom and not VOIR:
            odoo('product.template', 'write', [par_nom[nom]], {'website_sequence': 10000 + 10 * rang})
    # Les fiches ouvertes à l'écran ne gardent dans leur historique que les messages du Formateur TAAGG
    # (les autres sont signés du compte de Babacar, une vraie personne).
    filmees = [par_nom[n] for n in ("Gâteau d'anniversaire", TARTE['name']) if n in par_nom]
    messages = odoo('mail.message', 'search', [('model', '=', 'product.template'), ('res_id', 'in', filmees),
                                               ('author_id', '!=', FORMATEUR)])
    print(f'  · {len(messages)} message(s) d’historique retirés des fiches filmées')
    if not VOIR and messages:
        odoo('mail.message', 'unlink', messages)


# Texte sous le bouton « Ajouter au panier » de chaque fiche produit (modèle d'Odoo : « Garantie satisfait ou
# remboursé de 30 jours, Livraison : 2-3 jours ouvrables », faux pour une pâtisserie). Copie propre au site.
TEXTE_FICHE_PRODUIT = """<t name="Terms and Conditions" t-name="website_sale.product_terms_and_conditions">
        <small class="text-muted mb-0">
            <a href="/terms" class="o_translate_inline text-muted"><u>Conditions générales</u></a><br/>
            Gâteaux sur commande : commandez la veille avant 18 h<br/>
            Livraison à moto dans Dakar ou retrait en boutique
        </small>
    </t>"""


def texte_fiche_produit():
    """Remplace le texte d'exemple sous « Ajouter au panier » (à partir d'EB-06)."""
    print('Fiches produit : texte sous le bouton « Ajouter au panier »')
    ctx = dict(CTX, website_id=SITE)
    cle = 'website_sale.product_terms_and_conditions'
    vue = odoo('ir.ui.view', 'search', [('key', '=', cle), ('website_id', '=', SITE)], context=ctx)
    if not vue and not VOIR:
        # ⚠ écrire sur le modèle ne crée PAS de copie pour ce modèle-là (essayé le 04/11/2026 : le modèle commun
        #   avait changé) : on copie nous-mêmes le modèle pour le site, sans jamais écrire sur l'original
        modele = odoo('ir.ui.view', 'search', [('key', '=', cle), ('website_id', '=', False)], context=ctx)
        copie = odoo('ir.ui.view', 'copy', modele[0], {'website_id': SITE, 'key': cle}, context=ctx)
        vue = copie if isinstance(copie, list) else [copie]  # Odoo 19 renvoie une liste
    ecrire('ir.ui.view', vue, {'arch_db': TEXTE_FICHE_PRODUIT},
           'copie du site : commande la veille avant 18 h, livraison à moto dans Dakar ou retrait en boutique')


def eb_05():
    """EB-05 · Organiser son catalogue : la boutique de la fin d'EB-04 (avec la Tarte au citron meringuée),
    sans la catégorie Tartes, sans l'attribut Nombre de parts, dans l'ordre ORDRE_BOUTIQUE."""
    eb_01()
    site_fin_eb02()
    catalogue_eb05_a_refaire()


def catalogue_fin_eb05():
    """Ce que la capsule EB-05 a construit à l'écran, refait par l'API : catégorie Tartes (avec la tarte),
    attribut Nombre de parts (6, 8, 12 parts) sur le gâteau d'anniversaire, gâteau en tête de la boutique."""
    print('Catalogue : comme à la fin d’EB-05')
    if VOIR:
        return
    cat = odoo('product.public.category', 'create', {'name': 'Tartes', 'sequence': 4})
    tarte = odoo('product.template', 'search', [('name', '=', TARTE['name'])])
    odoo('product.template', 'write', tarte, {'public_categ_ids': [(4, cat)]})
    attribut = odoo('product.attribute', 'create', {
        'name': 'Nombre de parts', 'display_type': 'pills', 'create_variant': 'always', 'visibility': 'visible',
        'value_ids': [(0, 0, {'name': n, 'default_extra_price': e}) for n, e in (('6 parts', 0), ('8 parts', 5085), ('12 parts', 13559))]})
    valeurs = odoo('product.attribute.value', 'search', [('attribute_id', '=', attribut)])
    gateau = odoo('product.template', 'search', [('name', '=', "Gâteau d'anniversaire")])
    odoo('product.template', 'write', gateau, {'website_sequence': 9995, 'attribute_line_ids': [
        (0, 0, {'attribute_id': attribut, 'value_ids': [(6, 0, valeurs)]})]}, context=dict(CTX, tracking_disable=True))
    print('  · Tartes, Nombre de parts (3 variantes du gâteau), gâteau en tête de la boutique')


# Cliente fictive qui commande à l'écran (EB-06…) : compte client (portail) dont le mot de passe est dans .env.
# Elle est connectée pour que la boutique voie qu'elle est au Sénégal (sinon, l'ordinateur de tournage étant
# situé à l'étranger, la boutique affiche les prix hors taxes).
CLIENTE = {'name': 'Fatou Ba', 'email': 'fatou.ba@exemple.sn', 'phone': '', 'street': '', 'street2': '',
           'city': '', 'zip': '', 'company_name': False}


def cliente_fictive():
    """Fatou Ba : compte client sans adresse (elle la tape à l'écran) et sans commande des prises précédentes."""
    print('Cliente fictive : Fatou Ba')
    login, mdp = ENV.get('ODOO_CLIENTE_LOGIN'), ENV.get('ODOO_CLIENTE_MOT_DE_PASSE')
    if not (login and mdp):
        raise SystemExit('✗ ODOO_CLIENTE_LOGIN et ODOO_CLIENTE_MOT_DE_PASSE manquent dans .env')
    senegal = odoo('res.country', 'search', [('code', '=', 'SN')])[0]
    actx = dict(CTX, active_test=False, tracking_disable=True)
    partenaires = odoo('res.partner', 'search', [('email', '=', CLIENTE['email'])], context=actx)
    commandes = odoo('sale.order', 'search', [('partner_id', 'child_of', partenaires), ('state', '!=', 'cancel')]) if partenaires else []
    print(f'  · {len(commandes)} commande(s) des prises précédentes annulée(s)')
    # factures et paiements des prises d'EB-09 : annulés d'abord (sinon Odoo refuse d'annuler la commande)
    factures = odoo('account.move', 'search', [('partner_id', 'child_of', partenaires), ('move_type', '=', 'out_invoice'),
                                               ('state', '!=', 'cancel')]) if partenaires else []
    paiements = odoo('account.payment', 'search', [('partner_id', 'child_of', partenaires), ('state', 'not in', ['draft', 'canceled', 'cancel'])]) if partenaires else []
    if factures or paiements:
        print(f'  · {len(factures)} facture(s) et {len(paiements)} paiement(s) des prises précédentes annulés')
    if not VOIR:
        for pmt in paiements:
            odoo('account.payment', 'action_draft', [pmt])
            odoo('account.payment', 'action_cancel', [pmt])
        for fac in factures:
            if odoo('account.move', 'read', [fac], fields=['state'])[0]['state'] == 'posted':
                odoo('account.move', 'button_draft', [fac])
            odoo('account.move', 'button_cancel', [fac])
    if not VOIR and commandes:
        odoo('sale.order', 'action_cancel', commandes, context=dict(actx, disable_cancel_warning=True))
    utilisateur = odoo('res.users', 'search', [('login', '=', login)], context=actx)
    print('  · compte client ' + ('remis à zéro' if utilisateur else 'créé') + ' (adresse vide, Sénégal)')
    if VOIR:
        return
    portail = odoo('ir.model.data', 'search_read', [('module', '=', 'base'), ('name', '=', 'group_portal')], fields=['res_id'])[0]['res_id']
    if not utilisateur:
        utilisateur = [odoo('res.users', 'create', {'name': CLIENTE['name'], 'login': login, 'password': mdp,
                                                   'group_ids': [(6, 0, [portail])]}, context=actx)]
    else:
        odoo('res.users', 'write', utilisateur, {'active': True, 'password': mdp}, context=actx)
    partenaire = odoo('res.users', 'read', utilisateur, fields=['partner_id'], context=actx)[0]['partner_id'][0]
    odoo('res.partner', 'write', [partenaire], dict(CLIENTE, country_id=senegal, active=True), context=actx)
    # adresses de livraison ajoutées pendant les prises : archivées ; autres fiches « Fatou Ba » des essais aussi
    autres = odoo('res.partner', 'search', ['|', ('parent_id', '=', partenaire), '&', ('email', '=', CLIENTE['email']),
                                            ('id', '!=', partenaire)], context=actx)
    if autres:
        odoo('res.partner', 'write', autres, {'active': False}, context=actx)


def paiement_eb06():
    """Pour EB-06 : la carte Démo (sujet d'EB-08) est cachée ; restent « Paiement comptant à la livraison »
    et « Payer sur Place »."""
    demo = odoo('payment.provider', 'search', [('code', '=', 'demo'), ('state', '!=', 'disabled')])
    ecrire('payment.provider', demo, {'is_published': False}, 'carte Démo cachée (remise en ligne pour EB-08)')
    # « Paiement comptant à la livraison » n'apparaît que si le mode de livraison l'autorise (réglé en EB-10)
    livraison = odoo('delivery.carrier', 'search', [('name', '=', 'Livraison standard')])
    ecrire('delivery.carrier', livraison, {'allow_cash_on_delivery': True}, 'Livraison standard : paiement à la livraison autorisé')
    ecrire('website', [SITE], {'add_to_cart_action': 'stay', 'account_on_checkout': 'optional'},
           'réglages de la boutique : rester sur la page produit, compte client facultatif (la capsule change le 1er)')


def eb_06():
    """EB-06 · Le tunnel d'achat : la boutique de la fin d'EB-05, texte des fiches produit corrigé,
    Fatou Ba (cliente fictive) sans adresse ni commande, carte Démo cachée."""
    eb_05()
    catalogue_fin_eb05()
    texte_fiche_produit()
    cliente_fictive()
    paiement_eb06()


# EB-07 : produits dont la capsule règle le stock (les autres gardent « vendre en rupture », sans stock affiché)
STOCK_EB07 = ['Croissant', 'Chausson aux pommes']


def stock_eb07_a_refaire():
    """Stock à zéro pour les produits suivis, ventes en rupture autorisées, rien d'affiché, sans message ;
    historique des fiches filmées nettoyé (messages signés du compte de Babacar)."""
    print('Stock : remis comme avant EB-07')
    ecrire('website', [SITE], {'add_to_cart_action': 'go_to_cart'}, 'Ajouter au panier → aller au panier (réglé en EB-06)')
    publies = odoo('product.template', 'search', [('sale_ok', '=', True), ('is_published', '=', True)])
    ecrire('product.template', publies, {'allow_out_of_stock_order': True, 'show_availability': False,
                                         'available_threshold': 5, 'out_of_stock_message': False},
           f'{len(publies)} produits : vente en rupture autorisée, quantité non affichée')
    gateaux = odoo('product.template', 'search', [('name', 'in', list(CATALOGUE['Gâteaux']) + [TARTE['name']])])
    ecrire('product.template', gateaux, {'is_storable': False}, 'gâteaux et tarte (sur commande) : stock non suivi')
    viennoiseries = odoo('product.template', 'search', [('name', 'in', list(CATALOGUE['Viennoiseries']))])
    ecrire('product.template', viennoiseries, {'is_storable': True}, 'viennoiseries (fournée du matin) : stock suivi')
    # les livraisons des commandes de démo (10 croissants chacune) réserveraient la fournée filmée
    livraisons = odoo('stock.picking', 'search', [('sale_id.client_order_ref', 'like', 'EB-DEMO'),
                                                  ('state', 'not in', ['done', 'cancel'])])
    print(f'  · {len(livraisons)} livraison(s) des commandes de démo annulée(s) (sinon elles réservent les croissants)')
    if not VOIR and livraisons:
        odoo('stock.picking', 'action_cancel', livraisons)
    filmes = odoo('product.template', 'search', [('name', 'in', STOCK_EB07)])
    variantes = odoo('product.product', 'search', [('product_tmpl_id', 'in', filmes)])
    quants = odoo('stock.quant', 'search', [('product_id', 'in', variantes), ('location_id.usage', '=', 'internal')])
    print(f'  · stock des {len(STOCK_EB07)} produits filmés remis à 0 ({len(quants)} ligne(s) de stock)')
    if not VOIR and quants:
        odoo('stock.quant', 'write', quants, {'inventory_quantity': 0})
        odoo('stock.quant', 'action_apply_inventory', quants)
    messages = odoo('mail.message', 'search', [('model', '=', 'product.template'), ('res_id', 'in', filmes),
                                               ('author_id', '!=', FORMATEUR)])
    print(f'  · {len(messages)} message(s) d’historique retirés des fiches filmées')
    if not VOIR and messages:
        odoo('mail.message', 'unlink', messages)


def eb_07():
    """EB-07 · Stock et disponibilité en ligne : la boutique de la fin d'EB-06, stock des croissants
    et du chausson à zéro, aucun produit en rupture affiché."""
    eb_06()
    stock_eb07_a_refaire()


VIREMENT_MSG_ORIGINE = ('<div><h5>Veuillez utiliser les informations suivantes pour le transfert bancaire.</h5><p><br></p>'
                        '<h6>Comptes bancaires</h6><ul></ul><p><br></p></div>')


def paiements_eb08_a_refaire():
    """Le « Virement bancaire » des Délices redevient tel qu'Odoo l'installe (désactivé) : la capsule le transforme
    en « Wave ou Orange Money ». Carte Démo en mode test, non publiée ; Flutterwave désactivé, sans clés."""
    print('Paiements : remis comme avant EB-08')
    ctx = dict(CTX, active_test=False)
    virement = odoo('payment.provider', 'search', [('custom_mode', '=', 'wire_transfer'), ('company_id', '=', 1)], context=ctx)
    ecrire('payment.provider', virement, {'name': 'Virement bancaire', 'state': 'disabled', 'is_published': False,
                                          'pending_msg': VIREMENT_MSG_ORIGINE}, 'Virement bancaire : désactivé, message d’origine')
    methode = odoo('payment.method', 'search', [('code', '=', 'wire_transfer')], context=ctx)
    ecrire('payment.method', methode, {'name': 'Virement bancaire'}, 'mode de paiement « Virement bancaire » (nom d’origine)')
    demo = odoo('payment.provider', 'search', [('code', '=', 'demo'), ('company_id', '=', 1)], context=ctx)
    ecrire('payment.provider', demo, {'state': 'test', 'is_published': False}, 'carte Démo : mode test, non publiée')
    flutterwave = odoo('payment.provider', 'search', [('code', '=', 'flutterwave'), ('company_id', '=', 1)], context=ctx)
    ecrire('payment.provider', flutterwave, {'state': 'disabled', 'is_published': False}, 'Flutterwave : désactivé')
    # Fatou a déjà commandé (EB-06) : son adresse est connue, le tunnel va droit au paiement
    utilisateur = odoo('res.users', 'search_read', [('login', '=', ENV.get('ODOO_CLIENTE_LOGIN'))], fields=['partner_id'], context=ctx)
    if utilisateur:
        ecrire('res.partner', [utilisateur[0]['partner_id'][0]], {'street': '12 rue Carnot', 'city': 'Dakar', 'zip': '10200',
                                                                  'phone': '+221 77 000 00 03'}, 'Fatou Ba : adresse de la commande d’EB-06')


def eb_08():
    """EB-08 · Les moyens de paiement : la boutique de la fin d'EB-07 ; paiements : à la livraison et sur place
    seulement ; Virement bancaire désactivé ; Fatou a son adresse et un panier vide."""
    eb_07()
    paiements_eb08_a_refaire()


def commande_wave_de_fatou():
    """La commande que Fatou a passée à la fin d'EB-08 : gâteau d'anniversaire 6 parts (24 000 F TTC),
    payée « Wave ou Orange Money » : devis envoyé, transaction en attente, pas encore de facture."""
    print('Commande de Fatou : payée par Wave, en attente de vérification')
    if VOIR:
        return
    ctx = dict(CTX, tracking_disable=True)
    partenaire = odoo('res.users', 'search_read', [('login', '=', ENV['ODOO_CLIENTE_LOGIN'])], fields=['partner_id'])[0]['partner_id'][0]
    gateau = odoo('product.product', 'search', [('product_tmpl_id.name', '=', "Gâteau d'anniversaire"),
                                                ('product_template_attribute_value_ids.name', '=', '6 parts')])
    commande = odoo('sale.order', 'create', {'partner_id': partenaire, 'website_id': SITE, 'user_id': odoo('website', 'read', [SITE], fields=['salesperson_id'])[0]['salesperson_id'][0],
                                             'order_line': [(0, 0, {'product_id': gateau[0], 'product_uom_qty': 1})]}, context=ctx)
    odoo('sale.order', 'write', [commande], {'state': 'sent'}, context=ctx)
    total = odoo('sale.order', 'read', [commande], fields=['amount_total', 'name', 'currency_id'])[0]
    wave = odoo('payment.provider', 'search', [('custom_mode', '=', 'wire_transfer'), ('company_id', '=', 1)])[0]
    methode = odoo('payment.method', 'search', [('code', '=', 'wire_transfer')], context=dict(CTX, active_test=False))[0]
    tx = odoo('payment.transaction', 'create', {'provider_id': wave, 'payment_method_id': methode, 'amount': total['amount_total'],
                                                'currency_id': total['currency_id'][0], 'partner_id': partenaire,
                                                'reference': total['name'], 'sale_order_ids': [(6, 0, [commande])]})
    odoo('payment.transaction', 'write', [tx], {'state': 'pending'})
    print(f"  · {total['name']} : {total['amount_total']:,.0f} F, transaction Wave en attente".replace(',', ' '))


def paiements_fin_eb08():
    """Ce que la capsule EB-08 a réglé à l'écran : Wave ou Orange Money activé, publié, avec ses instructions ;
    carte Démo publiée (mode test)."""
    print('Paiements : comme à la fin d’EB-08')
    if VOIR:
        return
    ctx = dict(CTX, active_test=False)
    virement = odoo('payment.provider', 'search', [('custom_mode', '=', 'wire_transfer'), ('company_id', '=', 1)], context=ctx)
    odoo('payment.provider', 'write', virement, {'name': 'Wave ou Orange Money', 'state': 'enabled', 'is_published': True,
        'pending_msg': '<p>Envoyez le montant de votre commande par Wave ou Orange Money au 77 000 00 00 (Les Délices de '
                       'Maïmouna), en indiquant votre numéro de commande. Nous confirmons dès réception.</p>'})
    odoo('payment.method', 'write', odoo('payment.method', 'search', [('code', '=', 'wire_transfer')], context=ctx), {'name': 'Wave ou Orange Money'})
    odoo('payment.provider', 'write', odoo('payment.provider', 'search', [('code', '=', 'demo'), ('company_id', '=', 1)], context=ctx), {'is_published': True})


def eb_09():
    """EB-09 · Où arrive l'argent : la boutique de la fin d'EB-08, avec la commande Wave de Fatou en attente."""
    eb_08()
    paiements_fin_eb08()
    commande_wave_de_fatou()


def livraisons_eb10_a_refaire():
    """Modes de livraison tels qu'au début d'EB-10 : « Livraison standard » gratuite (paiement à la livraison
    autorisé depuis EB-06), « Retrait en magasin » ; les copies faites pendant les prises sont archivées."""
    print('Livraison : remise comme avant EB-10')
    ctx = dict(CTX, active_test=False)
    standard = odoo('delivery.carrier', 'search', [('delivery_type', '=', 'fixed'), ('product_id.default_code', '=', 'Delivery_007')], context=ctx)
    ecrire('delivery.carrier', standard[:1], {'name': 'Livraison standard', 'fixed_price': 0, 'free_over': False, 'amount': 1000,
                                              'allow_cash_on_delivery': True, 'is_published': True, 'active': True},
           'Livraison standard : gratuite, paiement à la livraison autorisé')
    copies = odoo('delivery.carrier', 'search', [('delivery_type', '=', 'fixed'), ('id', 'not in', standard[:1])])
    ecrire('delivery.carrier', copies, {'active': False, 'is_published': False}, f'{len(copies)} mode(s) créé(s) pendant les prises archivé(s)')
    # le prix d'un mode de livraison est celui de son « produit de livraison » : ceux créés pendant les prises sont archivés
    produits = odoo('product.product', 'search', [('name', 'in', ['Livraison banlieue']), ('type', '=', 'service')])
    ecrire('product.product', produits, {'active': False}, f'{len(produits)} produit(s) de livraison des prises archivé(s)')
    retrait = odoo('delivery.carrier', 'search', [('delivery_type', '=', 'in_store')], context=ctx)
    entrepot = odoo('stock.warehouse', 'search', [('code', '=', 'WH'), ('company_id', '=', 1)])
    ecrire('delivery.carrier', retrait[:1], {'name': 'Retrait en magasin', 'is_published': True, 'active': True,
                                             'warehouse_ids': [(6, 0, entrepot)]},
           'Retrait en magasin : publié, à la boutique seulement (pas à l’Entrepôt du Potager)')


def eb_10():
    """EB-10 · Organiser la livraison : la boutique de la fin d'EB-09 (sans la commande de Fatou), livraison gratuite
    unique + retrait en magasin."""
    eb_08()
    paiements_fin_eb08()
    livraisons_eb10_a_refaire()


def livraisons_fin_eb10():
    """Ce que la capsule EB-10 a réglé à l'écran : Dakar ville 1 271 F HT (1 500 F TTC), gratuite dès 30 000 F ;
    banlieue 2 119 F HT (2 500 F TTC) avec son produit ; Retrait en boutique (Médina)."""
    print('Livraison : comme à la fin d’EB-10')
    if VOIR:
        return
    ctx = dict(CTX, active_test=False)
    standard = odoo('delivery.carrier', 'search', [('delivery_type', '=', 'fixed'), ('product_id.default_code', '=', 'Delivery_007')], context=ctx)[:1]
    odoo('delivery.carrier', 'write', standard, {'name': 'À moto – Dakar ville (Plateau, Médina, Fann, Mermoz)', 'fixed_price': 1271,
                                                 'free_over': True, 'amount': 30000})
    produit = odoo('product.product', 'create', {'name': 'Livraison banlieue', 'type': 'service', 'sale_ok': False,
                                                 'taxes_id': [(6, 0, [5])], 'list_price': 2119})
    odoo('delivery.carrier', 'create', {'name': 'À moto – banlieue (Pikine, Guédiawaye, Rufisque)', 'delivery_type': 'fixed',
                                        'product_id': produit, 'fixed_price': 2119, 'allow_cash_on_delivery': True, 'is_published': True})
    retrait = odoo('delivery.carrier', 'search', [('delivery_type', '=', 'in_store')], context=ctx)[:1]
    odoo('delivery.carrier', 'write', retrait, {'name': 'Retrait en boutique (Médina)'})


def sans_sms_de_livraison():
    """La validation d'une livraison envoyait un SMS à la cliente (module stock_sms : crédits payants, et une ligne
    « SMS » en erreur visible dans l'historique). Module désinstallé le 06/11/2026 avec l'accord de Babacar ;
    on vérifie qu'il n'est pas revenu."""
    etat = odoo('ir.module.module', 'search_read', [('name', '=', 'stock_sms')], fields=['state'])
    if etat and etat[0]['state'] == 'installed':
        raise SystemExit('✗ Le module stock_sms est réinstallé : chaque livraison validée tenterait un SMS. '
                         'Le désinstaller (Inventaire › Paramètres › Confirmation SMS) avant de filmer.')
    print('  · Inventaire : module SMS de livraison absent (aucun SMS à la validation des livraisons)')


def eb_11():
    """EB-11 · Une commande de bout en bout : la boutique de la fin d'EB-10 (paiements et livraisons réglés)."""
    eb_10()
    livraisons_fin_eb10()
    sans_sms_de_livraison()


def droits_live_chat():
    """Le compte de tournage « Formateur TAAGG » reçoit le droit Live Chat / Administrateur (accord de Babacar
    du 06/11/2026, pour EB-12). Base de démonstration seulement."""
    utilisateur = odoo('res.users', 'search', [('login', '=', ENV['ODOO_LOGIN'])])
    groupe = odoo('ir.model.data', 'search_read', [('module', '=', 'im_livechat'), ('name', '=', 'im_livechat_group_manager')],
                  fields=['res_id'])[0]['res_id']
    ecrire('res.users', utilisateur, {'group_ids': [(4, groupe)]}, 'Formateur TAAGG : droit Live Chat / Administrateur')


def rpc_formateur():
    """Accès avec le compte Formateur TAAGG (Live Chat : le compte API n'y a pas droit)."""
    uid = rpc('common', 'login', BASE, ENV['ODOO_LOGIN'], ENV['ODOO_MOT_DE_PASSE'])
    return lambda modele, methode, *args, **kw: rpc('object', 'execute_kw', BASE, uid, ENV['ODOO_MOT_DE_PASSE'],
                                                    modele, methode, list(args), dict(kw, context=kw.get('context', CTX)))


def service_client_eb12_a_refaire():
    """Chat en direct : canal d'origine (« YourWebsite.com », aucun agent), conversations des prises supprimées ;
    avis clients désactivés sur les fiches produit, avis des prises supprimés."""
    print('Service client : remis comme avant EB-12')
    droits_live_chat()
    if VOIR:
        return
    formateur = rpc_formateur()
    canal = formateur('im_livechat.channel', 'search', [])
    formateur('im_livechat.channel', 'write', canal[:1], {'name': 'YourWebsite.com', 'button_text': 'Besoin d’aide ? Chattez avec nous.',
                                                          'default_message': 'Bonjour, comment puis-je vous aider ?'})
    formateur('im_livechat.channel', 'write', canal[:1], {'user_ids': [(6, 0, [])]})  # aucun agent (à part : sinon ignoré)
    conversations = formateur('discuss.channel', 'search', [('livechat_channel_id', 'in', canal)])
    if conversations:
        formateur('discuss.channel', 'unlink', conversations)
    print(f'  · chat : canal d’origine, sans agent ; {len(conversations)} conversation(s) des prises supprimée(s)')
    vues = odoo('ir.ui.view', 'search', [('key', '=', 'website_sale.product_comment')], context=dict(CTX, active_test=False))
    odoo('ir.ui.view', 'write', vues, {'active': False})
    fatou = odoo('res.partner', 'search', [('email', '=', CLIENTE['email'])], context=dict(CTX, active_test=False))
    avis = odoo('mail.message', 'search', [('model', '=', 'product.template'), ('author_id', 'in', fatou)])
    if avis:
        odoo('mail.message', 'unlink', avis)
    print(f'  · avis clients désactivés ; {len(avis)} avis des prises supprimé(s)')


def commande_livree_de_fatou():
    """La commande de la fin d'EB-11 : gâteau 8 parts (30 000 F), livraison Dakar offerte, confirmée, facturée, payée."""
    print('Commande de Fatou : livrée, facturée, payée (fin d’EB-11)')
    if VOIR:
        return
    ctx = dict(CTX, tracking_disable=True)
    partenaire = odoo('res.users', 'search_read', [('login', '=', ENV['ODOO_CLIENTE_LOGIN'])], fields=['partner_id'])[0]['partner_id'][0]
    gateau = odoo('product.product', 'search', [('product_tmpl_id.name', '=', "Gâteau d'anniversaire"),
                                                ('product_template_attribute_value_ids.name', '=', '8 parts')])
    vendeur = odoo('website', 'read', [SITE], fields=['salesperson_id'])[0]['salesperson_id'][0]
    commande = odoo('sale.order', 'create', {'partner_id': partenaire, 'website_id': SITE, 'user_id': vendeur,
                                             'order_line': [(0, 0, {'product_id': gateau[0], 'product_uom_qty': 1})]}, context=ctx)
    odoo('sale.order', 'action_confirm', [commande], context=ctx)
    for bon in odoo('sale.order', 'read', [commande], fields=['picking_ids'])[0]['picking_ids']:
        odoo('stock.picking', 'button_validate', [bon], context=dict(ctx, skip_sms=True))
    assistant = odoo('sale.advance.payment.inv', 'create', {'advance_payment_method': 'delivered'},
                     context=dict(ctx, active_model='sale.order', active_ids=[commande], active_id=commande))
    odoo('sale.advance.payment.inv', 'create_invoices', [assistant], context=dict(ctx, active_model='sale.order', active_ids=[commande], active_id=commande))
    facture = odoo('sale.order', 'read', [commande], fields=['invoice_ids'])[0]['invoice_ids']
    odoo('account.move', 'action_post', facture, context=ctx)
    banque = odoo('account.journal', 'search', [('code', '=', 'BNK1'), ('company_id', '=', 1)])
    reglement = odoo('account.payment.register', 'create', {'journal_id': banque[0]},
                     context=dict(ctx, active_model='account.move', active_ids=facture))
    odoo('account.payment.register', 'action_create_payments', [reglement], context=dict(ctx, active_model='account.move', active_ids=facture))
    print('  · commande confirmée, livrée, facture confirmée et payée (journal Banque, comme la carte)')


def eb_12():
    """EB-12 · Service client et confiance : la boutique de la fin d'EB-11 (Fatou a une commande livrée et payée),
    chat en direct d'origine sans agent, avis clients désactivés."""
    eb_11()
    commande_livree_de_fatou()
    service_client_eb12_a_refaire()


CAPSULES = {'EB-01': eb_01, 'EB-02': eb_02, 'EB-03': eb_03, 'EB-04': eb_04, 'EB-05': eb_05, 'EB-06': eb_06, 'EB-07': eb_07, 'EB-08': eb_08, 'EB-09': eb_09, 'EB-10': eb_10, 'EB-11': eb_11, 'EB-12': eb_12}

if __name__ == '__main__':
    code = next((a.upper() for a in sys.argv[1:] if not a.startswith('--')), None)
    if code not in CAPSULES:
        raise SystemExit(f"Usage : python3 {Path(__file__).name} <{'|'.join(CAPSULES)}> [--voir]")
    print(f"▶ État de départ {code}{' (simulation)' if VOIR else ''} — {URL}")
    CAPSULES[code]()
    print('✓ Terminé')
