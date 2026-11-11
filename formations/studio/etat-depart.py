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
ENV.update({k: v for k, v in os.environ.items() if k.startswith(('ODOO_', 'MODOU_'))})  # l'environnement passe avant le .env
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
    # les champs calculés d'abord : Odoo refuse de retirer un champ dont un autre dépend
    calcules = [c['id'] for c in odoo('ir.model.fields', 'read', ids, fields=['depends']) if c['depends']]
    retirer('ir.model.fields', calcules, 'champs Studio calculés')
    retirer('ir.model.fields', [i for i in ids if i not in calcules], 'champs Studio')


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


def stu_05():
    # STU-05 part de la fin de STU-02 et crée « Prix par convive » (Monétaire calculé, stocké) sur les devis.
    defaire_champs('sale.order', champs_studio('sale.order', ["Type d'événement", 'Nombre de convives', 'Prix par convive',
                                                              'Nouveau Monétaire', 'Nouveau Sélection', 'Nouveau Entier']))
    return devis_demo(), fin_stu_02()


REGLE_STU06 = 'Mariage confirmé → dégustation'
REF_DEVIS_TEST = 'Mariage Sarr'  # devis confirmé à l'écran dans STU-06 (Khady Sarr, client de démonstration)
CLIENT_TEST = 34


def devis_test_stu06():
    """Le devis « Mariage Sarr » en brouillon : 100 × Fraisier à 8 000 F, Mariage, 100 convives. Créé s'il manque."""
    ids = odoo('sale.order', 'search', [['client_order_ref', '=', REF_DEVIS_TEST]])
    if not ids:
        if not (OUI or PREPARER):
            print(f'  à créer  devis de démonstration « {REF_DEVIS_TEST} » (Khady Sarr, Mariage, 100 convives)')
            return None
        ids = [odoo('sale.order', 'create', {'partner_id': CLIENT_TEST, 'client_order_ref': REF_DEVIS_TEST, 'user_id': FORMATEUR,
                                             'x_studio_type_evenement': 'Mariage', 'x_studio_nombre_de_convives': 100,
                                             'order_line': [[0, 0, {'product_id': FRAISIER, 'name': 'Fraisier — buffet de mariage',
                                                                    'product_uom_qty': 100, 'price_unit': 8000}]]})]
    elif OUI or PREPARER:  # le devis existe déjà : on lui remet son événement (perdu si les champs ont été retirés)
        odoo('sale.order', 'write', ids, {'x_studio_type_evenement': 'Mariage', 'x_studio_nombre_de_convives': 100})
    return odoo('sale.order', 'read', ids, fields=['name', 'state'])[0]


def stu_06():
    # STU-06 crée à l'écran la règle « Mariage confirmé → dégustation » (statut défini sur Commande client, appliquée aux
    # mariages, action : activité pour le vendeur du devis) et confirme le devis « Mariage Sarr ».
    # Remise à zéro : la règle et ses actions, le devis « Mariage Sarr » (annulé puis retiré, avec sa livraison et
    # ses activités), puis la fin de STU-02 ; le devis « Mariage Sarr » est recréé en brouillon.
    regles = odoo('base.automation', 'search', [['name', '=', REGLE_STU06]], context={'active_test': False})
    if regles:
        actions = odoo('ir.actions.server', 'search', [['base_automation_id', 'in', regles]])
        retirer('base.automation', regles, 'règle d\'automatisation')
        if OUI and actions:
            actions = odoo('ir.actions.server', 'search', [['id', 'in', actions]])
        retirer('ir.actions.server', actions, 'actions de la règle')
    devis = odoo('sale.order', 'search_read', [['client_order_ref', '=', REF_DEVIS_TEST]], fields=['name', 'state'])
    for d in devis:
        if d['state'] == 'sale':
            print(('  ANNULÉ  ' if OUI else '  à annuler  ') + f"devis {d['name']} (et sa livraison)")
            if OUI:
                odoo('sale.order', 'action_cancel', [d['id']])
        livraisons = odoo('stock.picking', 'search', [['origin', '=', d['name']]])
        if OUI and livraisons:
            odoo('stock.picking', 'action_cancel', livraisons)
        retirer('stock.picking', livraisons, 'livraison du devis de test')
        retirer('sale.order', [d['id']], 'devis de test')
    defaire_champs('sale.order', champs_studio('sale.order', ["Type d'événement", 'Nombre de convives', 'Prix par convive',
                                                              'Nouveau Sélection', 'Nouveau Entier']))
    return devis_demo(), fin_stu_02(), devis_test_stu06()


def stu_07():
    # STU-07 modifie à l'écran le rapport « Devis / Commande » : Studio enregistre une vue de personnalisation
    # (web_studio.report_editor_customization_diff…) et une copie de sauvegarde inactive du modèle d'origine.
    # Remise à zéro : ces deux vues (créées par le formateur), puis les champs de STU-02 ; la fin de STU-02 est recréée.
    vues = odoo('ir.ui.view', 'search', ['|', ['key', '=like', 'web_studio.report_editor_customization_diff.view._sale.report_saleorder%'],
                                         ['key', '=like', 'web_studio.__backup__.%sale.report_saleorder%'],
                                         ['create_uid', 'in', [FORMATEUR, UID]]], context={'active_test': False})
    retirer('ir.ui.view', vues, 'personnalisation Studio du rapport Devis / Commande')
    stu_02()
    return devis_demo(), fin_stu_02()


LOGIN_MODOU = 'modou.livreur@exemple.sn'  # compte de test de STU-08 (adresse fictive) ; mot de passe : MODOU_MOT_DE_PASSE
GROUPE_STU08 = 'Livraison : Livreur'
REGLE_STU08 = 'Livreur : ses livraisons seulement'
REF_LIVRAISON_2 = 'Mariage Sarr'  # seconde livraison de démonstration, confiée à un autre livreur


def fin_stu_03():
    """Recrée par l'API le champ « Livreur » (Many2One vers Utilisateur) de STU-03 et sa place dans le bon de livraison."""
    if odoo('ir.model.fields', 'search', [['model', '=', 'stock.picking'], ['name', '=', 'x_studio_livreur']]):
        return 'déjà là'
    if not (OUI or PREPARER):
        print('  à créer  champ « Livreur » sur les transferts et sa place dans la fiche')
        return None
    modele = odoo('ir.model', 'search', [['model', '=', 'stock.picking']])[0]
    odoo('ir.model.fields', 'create', {'model_id': modele, 'name': 'x_studio_livreur', 'ttype': 'many2one', 'state': 'manual',
                                       'relation': 'res.users', 'field_description': 'Livreur', 'copied': True})
    fiche = odoo('ir.model.data', 'search_read', [['module', '=', 'stock'], ['name', '=', 'view_picking_form']], fields=['res_id'])[0]['res_id']
    odoo('ir.ui.view', 'create', {'name': 'Odoo Studio: stock.picking.form customization', 'model': 'stock.picking', 'type': 'form',
                                  'mode': 'extension', 'inherit_id': fiche, 'priority': 99, 'arch_db':
                                  "<data><xpath expr=\"/form/sheet/group/group/field[@name='picking_type_id']\" position=\"after\">"
                                  "<field name=\"x_studio_livreur\"/></xpath></data>"})
    return 'recréée'


def modou():
    """Le compte de test « Modou GUEYE (livreur) » : utilisateur interne, Inventaire / Utilisateur. Créé ou réactivé."""
    ids = odoo('res.users', 'search', [['login', '=', LOGIN_MODOU]], context={'active_test': False})
    if not (OUI or PREPARER):
        if not ids:
            print('  à créer  utilisateur de test « Modou GUEYE (livreur) »')
        return ids[0] if ids else None
    if not ENV.get('MODOU_MOT_DE_PASSE'):
        sys.exit('MODOU_MOT_DE_PASSE manque (mot de passe du compte de test, jamais dans le dépôt)')
    groupes = [odoo('ir.model.data', 'search_read', [['module', '=', m], ['name', '=', n]], fields=['res_id'])[0]['res_id']
               for m, n in (('base', 'group_user'), ('stock', 'group_stock_user'))]
    if ids:
        odoo('res.users', 'write', ids, {'active': True, 'password': ENV['MODOU_MOT_DE_PASSE'], 'group_ids': [[6, 0, groupes]]})
        return ids[0]
    return odoo('res.users', 'create', {'name': 'Modou GUEYE (livreur)', 'login': LOGIN_MODOU, 'lang': 'fr_FR', 'tz': 'Africa/Dakar',
                                        'password': ENV['MODOU_MOT_DE_PASSE'], 'group_ids': [[6, 0, groupes]]})


def livraisons_stu08(livreur):
    """Deux livraisons de démonstration : « Mariage Ndiaye » confiée à Modou, « Mariage Sarr » au formateur."""
    une = livraison_demo()
    ids = odoo('stock.picking', 'search', [['origin', '=', REF_LIVRAISON_2], ['partner_id', '=', CLIENT_TEST], ['picking_type_code', '=', 'outgoing']])
    if not ids and (OUI or PREPARER):
        ids = [odoo('stock.picking', 'create', {'picking_type_id': 2, 'partner_id': CLIENT_TEST, 'origin': REF_LIVRAISON_2,
                                                'location_id': 5, 'location_dest_id': 2,
                                                'move_ids': [[0, 0, {'product_id': FRAISIER, 'product_uom_qty': 100,
                                                                     'location_id': 5, 'location_dest_id': 2}]]})]
    if (OUI or PREPARER) and une and ids and livreur:
        odoo('stock.picking', 'write', [une['id']], {'x_studio_livreur': livreur})
        odoo('stock.picking', 'write', ids, {'x_studio_livreur': FORMATEUR})
    return une, ids


def stu_08():
    # STU-08 crée à l'écran le groupe « Livraison : Livreur », y ajoute Modou, et pose la règle d'enregistrement
    # « Livreur : ses livraisons seulement » sur les transferts. État de départ : le champ « Livreur » de STU-03 (API),
    # deux livraisons de démonstration (une à Modou, une au formateur), le compte de test de Modou actif.
    # Remise à zéro : la règle, le groupe, le compte de Modou archivé (jamais supprimé), puis le champ « Livreur ».
    retirer('ir.rule', odoo('ir.rule', 'search', [['name', '=', REGLE_STU08]], context={'active_test': False}), "règle d'enregistrement")
    retirer('res.groups', odoo('res.groups', 'search', [['name', '=', GROUPE_STU08]]), 'groupe')
    m = odoo('res.users', 'search', [['login', '=', LOGIN_MODOU], ['active', '=', True]])
    if m:
        print(('  ARCHIVÉ  ' if OUI else '  à archiver  ') + 'utilisateur de test « Modou GUEYE (livreur) »')
        if OUI:
            odoo('res.users', 'write', m, {'active': False})
    defaire_champs('stock.picking', champs_studio('stock.picking', ['Livreur', 'Téléphone du client', 'Nouveau Many2One']))
    return livraison_demo()


def preparer_stu08():
    fin_stu_03()
    return livraisons_stu08(modou())


def stu_09():
    # STU-09 ne crée rien dans la base : l'export Studio est un fichier téléchargé, la fenêtre d'import est fermée sans
    # rien charger. Pour avoir quelque chose à exporter, --preparer remet la fin de STU-02 (champs du devis) et le
    # champ « Livreur » de STU-03 ; --oui les retire.
    stu_03()
    return stu_02()


def stu_10():
    # STU-10 est une revue : rien n'est créé (la règle d'automatisation est ouverte puis abandonnée sans être
    # enregistrée). --preparer remet la fin de STU-02 pour le regroupement par type d'événement ; --oui la retire.
    return stu_02()


CAPSULES = {'STU-01': stu_01, 'STU-02': stu_02, 'STU-03': stu_03, 'STU-04': stu_04, 'STU-05': stu_05, 'STU-06': stu_06,
            'STU-07': stu_07, 'STU-08': stu_08, 'STU-09': stu_09, 'STU-10': stu_10}

if __name__ == '__main__':
    code = next((a for a in sys.argv[1:] if not a.startswith('--')), '')
    if PREPARER:
        # --preparer : seulement créer ce qui manque (devis, livraison, fin de STU-02), sans rien retirer
        print(code, '— préparation (création seulement) :', devis_demo(), livraison_demo(),
              fin_stu_02() if code in ('STU-04', 'STU-05', 'STU-06', 'STU-07', 'STU-09', 'STU-10') else '',
              fin_stu_03() if code == 'STU-09' else '',
              devis_test_stu06() if code == 'STU-06' else '',
              preparer_stu08() if code == 'STU-08' else '')
        sys.exit(0)
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    print(code, '— ' + ('remise à zéro' if OUI else "aperçu (rien n'est modifié ; ajouter --oui pour défaire)"))
    print(code, 'prête :' if OUI else 'devis :', CAPSULES[code]())
