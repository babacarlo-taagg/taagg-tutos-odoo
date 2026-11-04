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
BOUTIQUE_ALMADIES = 12  # le client de la facture INV/2026/00001


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


def cpt_05():
    # la taxe « 18% TTC » est créée à l'écran en dupliquant « 18% » (ventes) : on enlève les copies
    ids = odoo('account.tax', 'search', [['company_id', '=', SOCIETE], '|', ['name', '=', '18% TTC'], ['name', 'like', '(copie)']],
               context={'active_test': False, 'lang': 'fr_FR'})  # nom traduit : chercher en français
    if ids:
        odoo('account.tax', 'unlink', ids)
    return len(ids)


def cpt_06():
    # le client « Pâtisserie de Banjul » et sa facture brouillon sont créés à l'écran : on les enlève
    clients = odoo('res.partner', 'search', [['name', '=', 'Pâtisserie de Banjul']], context={'active_test': False})
    factures = odoo('account.move', 'search', [['partner_id', 'in', clients], ['state', '=', 'draft']]) if clients else []
    if factures:
        odoo('account.move', 'unlink', factures)
    if clients:
        odoo('res.partner', 'unlink', clients)
    return len(clients), len(factures)


def cpt_07():
    # la condition « 50 % à la commande, solde à 30 jours » est créée à l'écran et posée sur la Boutique Les Almadies
    odoo('res.partner', 'write', [BOUTIQUE_ALMADIES], {'property_payment_term_id': False}, context={'allowed_company_ids': [SOCIETE]})
    brouillons = odoo('account.move', 'search', [['partner_id', '=', BOUTIQUE_ALMADIES], ['state', '=', 'draft']])
    if brouillons:  # la facture brouillon de la démonstration (la facture INV/2026/00001, validée, ne bouge pas)
        odoo('account.move', 'unlink', brouillons)
    ids = odoo('account.payment.term', 'search', [['name', 'ilike', '50 % à la commande']], context={'active_test': False, 'lang': 'fr_FR'})
    if ids:
        odoo('account.payment.term', 'unlink', ids)
    return len(ids)


def cpt_08():
    # numéro de compte du journal Banque, journal Wave (et son compte), option et arrondi des espèces : on défait tout
    banque = odoo('account.journal', 'search', [['code', '=', 'BNK1'], ['company_id', '=', SOCIETE]])
    odoo('account.journal', 'write', banque, {'bank_account_id': False})
    ribs = odoo('res.partner.bank', 'search', [['acc_number', '=', 'SN012 01001 012345678901 23']], context={'active_test': False})
    if ribs:
        # Odoo archive le compte au lieu de l'effacer : on libère le numéro pour pouvoir le recréer à l'écran
        # (un compte « approuvé » ne se renomme pas : on retire d'abord l'autorisation d'envoyer de l'argent)
        for rib in ribs:
            odoo('res.partner.bank', 'write', [rib], {'allow_out_payment': False})
            odoo('res.partner.bank', 'write', [rib], {'acc_number': f'archive-tournage-{rib}', 'active': False})
    wave = odoo('account.journal', 'search', [['code', '=', 'WAV'], ['company_id', '=', SOCIETE]], context={'active_test': False})
    if wave:
        odoo('account.journal', 'unlink', wave)
    comptes = odoo('account.account', 'search', [['code', '=like', '521%'], ['name', '=', 'Wave']], context={'allowed_company_ids': [SOCIETE]})
    if comptes:
        odoo('account.account', 'unlink', comptes)
    brouillons = odoo('account.move', 'search', [['partner_id', '=', BOUTIQUE_ALMADIES], ['state', '=', 'draft']])
    if brouillons:  # la facture brouillon de la démonstration de l'arrondi
        odoo('account.move', 'unlink', brouillons)
    arrondis = odoo('account.cash.rounding', 'search', [['name', '=', 'Arrondi au 5 F']], context={'active_test': False})
    if arrondis:
        odoo('account.cash.rounding', 'unlink', arrondis)
    reglages = odoo('res.config.settings', 'create', {'group_cash_rounding': False}, context={'allowed_company_ids': [SOCIETE]})
    odoo('res.config.settings', 'execute', [reglages], context={'allowed_company_ids': [SOCIETE]})
    return len(ribs), len(wave), len(comptes), len(arrondis)


def cpt_09():
    # les comptes des catégories « Pâtisseries Individuelles » (revenus) et « Intrants » (charges) sont changés à l'écran
    patisseries = odoo('product.category', 'search', [['name', '=', 'Pâtisseries Individuelles']])
    intrants = odoo('product.category', 'search', [['name', 'ilike', 'Intrants Cuisine']])
    vente_marchandises = odoo('account.account', 'search', [['code', '=', '701100']], context={'allowed_company_ids': [SOCIETE]})
    achat_biens = odoo('account.account', 'search', [['code', '=', '601100']], context={'allowed_company_ids': [SOCIETE]})
    odoo('product.category', 'write', patisseries, {'property_account_income_categ_id': vente_marchandises[0]}, context={'allowed_company_ids': [SOCIETE]})
    odoo('product.category', 'write', intrants, {'property_account_expense_categ_id': achat_biens[0]}, context={'allowed_company_ids': [SOCIETE]})
    brouillons = odoo('account.move', 'search', [['partner_id', '=', BOUTIQUE_ALMADIES], ['state', '=', 'draft']])
    if brouillons:  # la facture brouillon de la démonstration
        odoo('account.move', 'unlink', brouillons)
    return len(patisseries), len(intrants), len(brouillons)


def cpt_10():
    # le client « Traiteur Saveurs du Plateau » et sa facture validée (INV/2026/00002) sont créés à l'écran
    # on retire aussi les factures brouillon laissées par les capsules précédentes (et le client de CPT-06)
    retires = 0
    for nom in ['Traiteur Saveurs du Plateau', 'Pâtisserie de Banjul']:
        clients = odoo('res.partner', 'search', [['name', '=', nom]], context={'active_test': False})
        if not clients:
            continue
        pieces = odoo('account.move', 'search', [['partner_id', 'in', clients]])
        validees = odoo('account.move', 'search', [['id', 'in', pieces], ['state', '!=', 'draft']])
        if validees:  # dernière facture de la séquence : on peut la remettre en brouillon puis la supprimer
            odoo('account.move', 'button_draft', validees)
        if pieces:
            odoo('account.move', 'unlink', pieces)
        odoo('res.partner', 'unlink', clients)
        retires += len(pieces)
    brouillons = odoo('account.move', 'search', [['move_type', '=', 'out_invoice'], ['state', '=', 'draft']])
    if brouillons:
        odoo('account.move', 'unlink', brouillons)
    # le client de la démonstration est recréé propre (Odoo ne crée pas de client en un clic depuis une facture)
    odoo('res.partner', 'create', {'name': 'Traiteur Saveurs du Plateau', 'is_company': True, 'street': 'Avenue Léopold Sédar Senghor',
                                   'city': 'Dakar', 'country_id': 204}, context={'allowed_company_ids': [SOCIETE]})
    return retires, len(brouillons)


def facture_traiteur():
    # la facture INV/2026/00002 du Traiteur (CPT-10), validée ; recréée par l'API si elle manque
    ctx = {'allowed_company_ids': [SOCIETE], 'lang': 'fr_FR'}
    traiteur = odoo('res.partner', 'search', [['name', '=', 'Traiteur Saveurs du Plateau']], context=ctx)
    if not traiteur:
        traiteur = [odoo('res.partner', 'create', {'name': 'Traiteur Saveurs du Plateau', 'is_company': True,
                                                   'street': 'Avenue Léopold Sédar Senghor', 'city': 'Dakar', 'country_id': 204}, context=ctx)]
    factures = odoo('account.move', 'search', [['partner_id', '=', traiteur[0]], ['move_type', '=', 'out_invoice'], ['state', '=', 'posted'],
                                               ['ref', '=', 'Réception du 7 novembre']])
    if factures:
        return factures[0]
    trente = odoo('account.payment.term', 'search', [['name', '=', '30 jours']], context={'lang': 'fr_FR'})
    fraisier = odoo('product.product', 'search', [['name', '=', 'Fraisier']])
    macaron = odoo('product.product', 'search', [['name', '=', 'Macaron']])
    facture = odoo('account.move', 'create', {
        'move_type': 'out_invoice', 'partner_id': traiteur[0], 'invoice_payment_term_id': trente[0], 'ref': 'Réception du 7 novembre',
        'invoice_line_ids': [[0, 0, {'product_id': fraisier[0], 'quantity': 2, 'price_unit': 15000}],
                             [0, 0, {'product_id': macaron[0], 'quantity': 50, 'price_unit': 400}],
                             [0, 0, {'display_type': 'line_note', 'name': 'Livraison le samedi 7 novembre, au Plateau.'}]],
    }, context=ctx)
    odoo('account.move', 'action_post', [facture], context=ctx)
    return facture


def cpt_11():
    # l'avoir RINV/… du Traiteur est créé à l'écran et lettré avec INV/2026/00002 : on le défait,
    # puis on refait la facture à neuf, pour que son historique (à droite) ne garde pas les tournages précédents
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    traiteur = odoo('res.partner', 'search', [['name', '=', 'Traiteur Saveurs du Plateau']])
    avoirs = odoo('account.move', 'search', [['partner_id', 'in', traiteur], ['move_type', '=', 'out_refund']])
    valides = odoo('account.move', 'search', [['id', 'in', avoirs], ['state', '!=', 'draft']])
    if valides:  # remettre en brouillon défait aussi le lettrage
        odoo('account.move', 'button_draft', valides, context=fr)
    if avoirs:
        odoo('account.move', 'unlink', avoirs, context=fr)
    factures = odoo('account.move', 'search', [['partner_id', 'in', traiteur], ['move_type', '=', 'out_invoice']])
    if factures:  # dernière facture de la séquence : Odoo redonnera le même numéro, INV/2026/00002
        brouillons = odoo('account.move', 'search', [['id', 'in', factures], ['state', '!=', 'draft']])
        if brouillons:
            odoo('account.move', 'button_draft', brouillons, context=fr)
        odoo('account.move', 'unlink', factures, context=fr)
    facture = facture_traiteur()
    return odoo('account.move', 'read', [facture], ['name'])[0]['name']


TRAITEUR_NOTE_AVOIR = '10 macarons abîmés à la livraison'


def avoir_traiteur(facture):
    # l'avoir RINV/2026/00001 de CPT-11 (10 macarons, 4 720 F), lettré avec la facture ; recréé s'il manque
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    avoirs = odoo('account.move', 'search', [['reversed_entry_id', '=', facture], ['move_type', '=', 'out_refund'], ['state', '=', 'posted']])
    if avoirs:
        return avoirs[0]
    partenaire = odoo('account.move', 'read', [facture], ['partner_id'])[0]['partner_id'][0]
    macaron = odoo('product.product', 'search', [['name', '=', 'Macaron']])
    avoir = odoo('account.move', 'create', {
        'move_type': 'out_refund', 'partner_id': partenaire, 'reversed_entry_id': facture, 'ref': TRAITEUR_NOTE_AVOIR,
        'invoice_line_ids': [[0, 0, {'product_id': macaron[0], 'quantity': 10, 'price_unit': 400}]],
    }, context=fr)
    odoo('account.move', 'action_post', [avoir], context=fr)
    ligne = odoo('account.move.line', 'search', [['move_id', '=', avoir], ['account_id.account_type', '=', 'asset_receivable']])
    odoo('account.move', 'js_assign_outstanding_line', [facture], ligne[0], context=fr)
    return avoir


def facture_simple(partenaire, lignes, terme=None):
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    valeurs = {'move_type': 'out_invoice', 'partner_id': partenaire,
               'invoice_line_ids': [[0, 0, {'product_id': odoo('product.product', 'search', [['name', '=', nom]])[0],
                                            'quantity': q, 'price_unit': pu}] for nom, q, pu in lignes]}
    if terme:
        valeurs['invoice_payment_term_id'] = odoo('account.payment.term', 'search', [['name', '=', terme]], context=fr)[0]
    facture = odoo('account.move', 'create', valeurs, context=fr)
    odoo('account.move', 'action_post', [facture], context=fr)
    return odoo('account.move', 'read', [facture], ['name'])[0]['name']


def cpt_12():
    # paiements encaissés à l'écran (Traiteur et Boutique Les Almadies) : on les supprime ;
    # INV/2026/00003 (Almadies, 40 croissants) et INV/2026/00004 (Traiteur, 4 gâteaux, escompte 2/7 Net 30) sont refaites à neuf
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    traiteur = odoo('res.partner', 'search', [['name', '=', 'Traiteur Saveurs du Plateau']])[0]
    paiements = odoo('account.payment', 'search', [['partner_id', 'in', [traiteur, BOUTIQUE_ALMADIES]]])
    if paiements:  # remettre en brouillon défait aussi le lettrage
        valides = odoo('account.payment', 'search', [['id', 'in', paiements], ['state', '!=', 'draft']])
        if valides:
            odoo('account.payment', 'action_draft', valides, context=fr)
        odoo('account.payment', 'unlink', paiements, context=fr)
    # Compte de paiement des modes « Paiement manuel » de Wave et de la caisse : réglé à l'écran dans la capsule
    lignes = odoo('account.payment.method.line', 'search', [['journal_id.code', 'in', ['WAV', 'CAI']], ['payment_type', '=', 'inbound']], context=fr)
    odoo('account.payment.method.line', 'write', lignes, {'payment_account_id': False}, context=fr)
    facture = facture_traiteur()
    avoir = avoir_traiteur(facture)
    en_trop = odoo('account.move', 'search', [['partner_id', '=', traiteur], ['move_type', '=', 'out_refund'], ['id', '!=', avoir]])
    for f in en_trop:
        if odoo('account.move', 'read', [f], ['state'])[0]['state'] != 'draft':
            odoo('account.move', 'button_draft', [f], context=fr)
        odoo('account.move', 'unlink', [f], context=fr)
    anciennes = odoo('account.move', 'search', [['move_type', '=', 'out_invoice'], ['name', 'in', ['INV/2026/00003', 'INV/2026/00004']]], order='name desc')
    for f in anciennes:  # la plus récente d'abord : Odoo redonne ensuite les mêmes numéros
        if odoo('account.move', 'read', [f], ['state'])[0]['state'] != 'draft':
            odoo('account.move', 'button_draft', [f], context=fr)
        odoo('account.move', 'unlink', [f], context=fr)
    brouillons = odoo('account.move', 'search', [['partner_id', 'in', [traiteur, BOUTIQUE_ALMADIES]], ['state', '=', 'draft'], ['move_type', '=', 'out_invoice']])
    if brouillons:
        odoo('account.move', 'unlink', brouillons, context=fr)
    # même banque destinataire sur les deux factures des Almadies, sinon Odoo ne propose pas de regrouper le paiement
    rib = odoo('res.partner.bank', 'search', [['acc_number', '=', 'SN012 01001 012345678901 23']])
    odoo('account.move', 'write', [1], {'partner_bank_id': rib[0]}, context=fr)
    return (facture_simple(BOUTIQUE_ALMADIES, [('Croissant', 40, 500)], terme='Paiement immédiat'),
            facture_simple(traiteur, [("Gâteau d'anniversaire", 4, 25000)], terme='2/7 Net 30'))


CAPSULES = {'CPT-02': cpt_02, 'CPT-03': cpt_03, 'CPT-04': cpt_04, 'CPT-05': cpt_05, 'CPT-06': cpt_06, 'CPT-07': cpt_07,
            'CPT-08': cpt_08, 'CPT-09': cpt_09, 'CPT-10': cpt_10, 'CPT-11': cpt_11, 'CPT-12': cpt_12}

if __name__ == '__main__':
    code = sys.argv[1] if len(sys.argv) > 1 else ''
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    print(code, 'prête :', CAPSULES[code]())
