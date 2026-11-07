"""Remet la base de tournage dans l'état de départ d'une capsule Studio, par l'API (jamais à l'écran).

Usage : python3 formations/studio/etat-depart.py STU-02          montre ce qui serait défait, ne touche à rien
        python3 formations/studio/etat-depart.py STU-02 --oui    défait vraiment (après l'accord de Babacar)
        python3 formations/studio/etat-depart.py STU-04 --preparer   crée seulement ce qui manque, ne retire rien

Ne défait QUE ce que les capsules Studio ont créé : champs Studio aux libellés de la capsule, créés par le compte
« Formateur TAAGG », la vue Studio du devis, les valeurs par défaut de ces champs. Jamais les données des autres
formations (Comptabilité, E-business…).
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
ENV.update({k: v for k, v in os.environ.items() if k.startswith('ODOO_')})  # l'environnement passe avant le .env
ENV.setdefault('ODOO_BASE', 'edu-correction-les-delices-de-maimouna')
FORMATEUR = 6  # « Formateur TAAGG », le compte qui filme : tout ce que Studio crée à l'écran porte son nom
CLIENT_DEMO = 33  # Moussa Ndiaye (client de démonstration)
FRAISIER = 95
REF_DEVIS = 'Mariage Ndiaye'  # référence client du devis de démonstration, créé par ce script
OUI = '--oui' in sys.argv
PREPARER = '--preparer' in sys.argv  # crée seulement ce qui manque, ne retire jamais rien


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


def champs_studio(modele, libelles):
    return odoo('ir.model.fields', 'search', [['model', '=', modele], ['name', '=like', 'x_studio_%'],
                                               ['field_description', 'in', libelles], ['create_uid', 'in', [FORMATEUR, UID]]])


def defaire_champs(modele, ids):
    """Retire des champs Studio : d'abord leur place dans les vues Studio, leurs valeurs par défaut, puis les champs."""
    if not ids:
        return
    noms = [c['name'] for c in odoo('ir.model.fields', 'read', ids, fields=['name'])]
    vues = odoo('ir.ui.view', 'search_read', [['model', '=', modele], ['name', '=like', 'Odoo Studio: %'], ['create_uid', 'in', [FORMATEUR, UID]]],
                fields=['arch_db'], context={'active_test': False})
    retirer('ir.ui.view', [v['id'] for v in vues if any(n in v['arch_db'] for n in noms)], 'vue Studio qui affiche ces champs')
    retirer('ir.default', odoo('ir.default', 'search', [['field_id', 'in', ids]]), 'valeurs par défaut')
    retirer('ir.model.fields', ids, 'champs Studio')


def devis_demo():
    """Le devis de démonstration « Mariage Ndiaye » : 150 × Fraisier à 8 000 F = 1 200 000 F HT. Créé s'il manque."""
    ids = odoo('sale.order', 'search', [['client_order_ref', '=', REF_DEVIS]])
    if not ids:
        if not (OUI or PREPARER):
            print(f'  à créer  devis de démonstration « {REF_DEVIS} » (Moussa Ndiaye, 150 × Fraisier à 8 000 F)')
            return None
        ids = [odoo('sale.order', 'create', {'partner_id': CLIENT_DEMO, 'client_order_ref': REF_DEVIS, 'user_id': FORMATEUR,
                                             'order_line': [[0, 0, {'product_id': FRAISIER, 'name': 'Fraisier — buffet de mariage',
                                                                    'product_uom_qty': 150, 'price_unit': 8000}]]})]
    return odoo('sale.order', 'read', ids, fields=['name', 'state', 'amount_untaxed'])[0]


def stu_02():
    # STU-02 crée à l'écran « Type d'événement » (Sélection) et « Nombre de convives » (Entier) sur les devis.
    # État de départ : aucun des deux champs, pas de vue Studio du devis, le devis « Mariage Ndiaye » en brouillon.
    defaire_champs('sale.order', champs_studio('sale.order', ["Type d'événement", 'Nombre de convives', 'Nouveau Sélection', 'Nouveau Entier']))
    return devis_demo()


def livraison_demo():
    """Le bon de livraison de démonstration « Mariage Ndiaye » : 150 Fraisier pour Moussa Ndiaye, en brouillon."""
    ids = odoo('stock.picking', 'search', [['origin', '=', REF_DEVIS], ['picking_type_code', '=', 'outgoing'], ['partner_id', '=', CLIENT_DEMO]])
    if not ids:
        if not (OUI or PREPARER):
            print(f'  à créer  bon de livraison de démonstration « {REF_DEVIS} » (Moussa Ndiaye, 150 Fraisier)')
            return None
        ids = [odoo('stock.picking', 'create', {'picking_type_id': 2, 'partner_id': CLIENT_DEMO, 'origin': REF_DEVIS,
                                                'location_id': 5, 'location_dest_id': 2,
                                                'move_ids': [[0, 0, {'product_id': FRAISIER, 'product_uom_qty': 150,
                                                                     'location_id': 5, 'location_dest_id': 2}]]})]
    return odoo('stock.picking', 'read', ids, fields=['name', 'state'])[0]


VUE_DEVIS_STU02 = """<data>
  <xpath expr="/form//field[@name='partner_id']" position="after">
    <field name="x_studio_type_evenement" help="Laisser vide pour une commande de la boutique"/>
    <field name="x_studio_nombre_de_convives" required="x_studio_type_evenement" invisible="not x_studio_type_evenement"/>
  </xpath>
</data>"""


def fin_stu_02():
    """Recrée par l'API ce que STU-02 construit à l'écran (pour tourner les capsules suivantes sans refilmer STU-02)."""
    if odoo('ir.model.fields', 'search', [['model', '=', 'sale.order'], ['name', '=', 'x_studio_type_evenement']]):
        return 'déjà là'
    if not (OUI or PREPARER):
        print("  à créer  champs « Type d'événement » et « Nombre de convives » sur les devis, et leur place dans la fiche")
        return None
    modele = odoo('ir.model', 'search', [['model', '=', 'sale.order']])[0]
    valeurs = ['Mariage', 'Baptême', 'Séminaire', 'Anniversaire', 'Autre']
    odoo('ir.model.fields', 'create', {'model_id': modele, 'name': 'x_studio_type_evenement', 'ttype': 'selection', 'state': 'manual',
                                       'field_description': "Type d'événement", 'copied': True,
                                       'selection_ids': [[0, 0, {'value': v, 'name': v, 'sequence': i}] for i, v in enumerate(valeurs)]})
    odoo('ir.model.fields', 'create', {'model_id': modele, 'name': 'x_studio_nombre_de_convives', 'ttype': 'integer', 'state': 'manual',
                                       'field_description': 'Nombre de convives', 'copied': True})
    formulaire = odoo('ir.model.data', 'search_read', [['module', '=', 'sale'], ['name', '=', 'view_order_form']], fields=['res_id'])[0]['res_id']
    odoo('ir.ui.view', 'create', {'name': 'Odoo Studio: sale.order.form customization', 'model': 'sale.order', 'type': 'form',
                                  'mode': 'extension', 'inherit_id': formulaire, 'priority': 99, 'arch_db': VUE_DEVIS_STU02})
    devis = odoo('sale.order', 'search', [['client_order_ref', '=', REF_DEVIS]])
    odoo('sale.order', 'write', devis, {'x_studio_type_evenement': 'Mariage', 'x_studio_nombre_de_convives': 150})
    return 'recréée'


def stu_01():
    # STU-01 est une visite : rien n'est créé. On vérifie seulement le devis de démonstration.
    return devis_demo()


def stu_03():
    # STU-03 crée « Livreur » (Many2One vers Utilisateur) et « Téléphone du client » (champ associé) sur les transferts.
    defaire_champs('stock.picking', champs_studio('stock.picking', ['Livreur', 'Téléphone du client', 'Nouveau Many2One',
                                                                    'Nouveau Champ associé', 'Téléphone', 'Nouveau Many2one']))
    return livraison_demo()


def stu_04():
    # STU-04 part de la fin de STU-02 (les deux champs sur la fiche du devis) et range les écrans :
    # un onglet « Événement » dans la fiche, une colonne dans la liste, le type sur la carte kanban.
    # Remise à zéro : on défait tout (y compris les champs de STU-02), puis on recrée la fin de STU-02 par l'API.
    for vue in odoo('ir.ui.view', 'search', [['model', '=', 'sale.order'], ['name', '=like', 'Odoo Studio: %'],
                                             ['create_uid', 'in', [FORMATEUR, UID]]], context={'active_test': False}):
        retirer('ir.ui.view', [vue], 'vue Studio des devis')
    stu_02()
    return devis_demo(), fin_stu_02()


CAPSULES = {'STU-01': stu_01, 'STU-02': stu_02, 'STU-03': stu_03, 'STU-04': stu_04}

if __name__ == '__main__':
    code = next((a for a in sys.argv[1:] if not a.startswith('--')), '')
    if PREPARER:
        # --preparer : seulement créer ce qui manque (devis, livraison, fin de STU-02), sans rien retirer
        print(code, '— préparation (création seulement) :', devis_demo(), livraison_demo(),
              fin_stu_02() if code in ('STU-04', 'STU-05', 'STU-06', 'STU-07') else '')
        sys.exit(0)
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    print(code, '— ' + ('remise à zéro' if OUI else "aperçu (rien n'est modifié ; ajouter --oui pour défaire)"))
    print(code, 'prête :' if OUI else 'devis :', CAPSULES[code]())
