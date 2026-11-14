"""Remet la base de tournage dans l'état de départ d'une capsule, par l'API (jamais à l'écran).

Usage : python3 formations/comptabilite/etat-depart.py CPT-02
Lit ODOO_URL, ODOO_BASE, ODOO_LOGIN_API et ODOO_CLE_API dans l'environnement, sinon dans le .env du projet.
"""
import datetime
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
    # historique (à droite) des factures du tournage : on retire les traces laissées par les tournages de CPT-12
    # (paiements, retours en arrière), en gardant celles de CPT-10 et CPT-11
    factures = odoo('account.move', 'search', [['partner_id', 'in', [traiteur, BOUTIQUE_ALMADIES]], ['move_type', 'in', ['out_invoice', 'out_refund']]])
    traces = odoo('mail.message', 'search', [['model', '=', 'account.move'], ['res_id', 'in', factures], ['date', '>=', '2026-11-03 00:00:00']])
    if traces:
        odoo('mail.message', 'unlink', traces)
    # même banque destinataire sur les deux factures des Almadies, sinon Odoo ne propose pas de regrouper le paiement
    rib = odoo('res.partner.bank', 'search', [['acc_number', '=', 'SN012 01001 012345678901 23']])
    odoo('account.move', 'write', [1], {'partner_bank_id': rib[0]}, context=fr)
    return (facture_simple(BOUTIQUE_ALMADIES, [('Croissant', 40, 500)], terme='Paiement immédiat'),
            facture_simple(traiteur, [("Gâteau d'anniversaire", 4, 25000)], terme='2/7 Net 30'))


def facture_en_retard(partenaire, lignes, jours_de_retard, ref):
    # facture validée dont l'échéance est passée de « jours_de_retard » jours (dates calculées le jour du tournage)
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    aujourdhui = datetime.date.today()
    echeance = aujourdhui - datetime.timedelta(days=jours_de_retard)
    facture = odoo('account.move', 'create', {
        'move_type': 'out_invoice', 'partner_id': partenaire, 'ref': ref,
        'invoice_date': str(echeance - datetime.timedelta(days=15)), 'invoice_date_due': str(echeance),
        'invoice_payment_term_id': False,
        'invoice_line_ids': [[0, 0, {'product_id': odoo('product.product', 'search', [['name', '=', nom]])[0],
                                     'quantity': q, 'price_unit': pu}] for nom, q, pu in lignes]}, context=fr)
    odoo('account.move', 'write', [facture], {'invoice_date_due': str(echeance)}, context=fr)
    odoo('account.move', 'action_post', [facture], context=fr)
    return odoo('account.move', 'read', [facture], ['name', 'invoice_date_due'])[0]


def cpt_13():
    # deux factures en retard (Almadies : 20 jours ; Traiteur : 35 jours), adresses e-mail fictives (.example),
    # aucune relance faite, pas de niveau « 60 jours » ; les relances envoyées à l'écran laissent des messages,
    # retirés ici
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    traiteur = odoo('res.partner', 'search', [['name', '=', 'Traiteur Saveurs du Plateau']])[0]
    odoo('res.partner', 'write', [traiteur], {'email': 'compta@saveurs-du-plateau.example'}, context=fr)
    odoo('res.partner', 'write', [BOUTIQUE_ALMADIES], {'email': 'gerance@boutique-almadies.example'}, context=fr)
    niveaux = odoo('account_followup.followup.line', 'search', [['delay', '>', 30]], context=fr)
    if niveaux:
        odoo('account_followup.followup.line', 'unlink', niveaux, context=fr)
    anciennes = odoo('account.move', 'search', [['move_type', '=', 'out_invoice'], ['ref', 'in', ['Commande du séminaire', 'Réassort de la vitrine']]], order='name desc')
    for f in anciennes:
        paiements = odoo('account.payment', 'search', [['reconciled_invoice_ids', 'in', [f]]])
        if paiements:
            odoo('account.payment', 'action_draft', paiements, context=fr)
            odoo('account.payment', 'unlink', paiements, context=fr)
        if odoo('account.move', 'read', [f], ['state'])[0]['state'] != 'draft':
            odoo('account.move', 'button_draft', [f], context=fr)
        odoo('account.move', 'unlink', [f], context=fr)
    for p in (traiteur, BOUTIQUE_ALMADIES):
        traces = odoo('mail.message', 'search', [['model', '=', 'res.partner'], ['res_id', '=', p], ['date', '>=', '2026-11-05 00:00:00']])
        if traces:
            odoo('mail.message', 'unlink', traces)
        odoo('res.partner', 'write', [p], {'followup_next_action_date': False}, context=fr)
    return (facture_en_retard(BOUTIQUE_ALMADIES, [('Croissant', 60, 500)], 20, 'Réassort de la vitrine'),
            facture_en_retard(traiteur, [('Opéra', 4, 17000), ('Macaron', 100, 400)], 35, 'Commande du séminaire'))


def cpt_14():
    # la facture des Grands Moulins de Dakar (10 sacs de farine, réf. GMD-2026-1187) est saisie à l'écran : on la supprime,
    # ainsi que toute facture fournisseur en brouillon
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    moulins = odoo('res.partner', 'search', [['name', '=', 'Grands Moulins de Dakar']])
    factures = odoo('account.move', 'search', ['|', '&', ['partner_id', 'in', moulins], ['move_type', '=', 'in_invoice'],
                                               '&', ['move_type', '=', 'in_invoice'], ['state', '=', 'draft']], order='id desc')
    for f in factures:
        if odoo('account.move', 'read', [f], ['state'])[0]['state'] != 'draft':
            odoo('account.move', 'button_draft', [f], context=fr)
        odoo('account.move', 'unlink', [f], context=fr)
    return len(factures)


def facture_moulins():
    # BILL/2026/11/0001 de CPT-14 (Grands Moulins de Dakar, 10 sacs de farine à 18 000 F, réf. GMD-2026-1187) ; recréée si elle manque
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    moulins = odoo('res.partner', 'search', [['name', '=', 'Grands Moulins de Dakar']])[0]
    factures = odoo('account.move', 'search', [['partner_id', '=', moulins], ['move_type', '=', 'in_invoice'], ['ref', '=', 'GMD-2026-1187'], ['state', '=', 'posted']])
    if factures:
        return factures[0]
    farine = odoo('product.product', 'search', [['name', '=like', 'Farine de blé T55%'], ['name', 'not ilike', 'copie']])
    facture = odoo('account.move', 'create', {
        'move_type': 'in_invoice', 'partner_id': moulins, 'ref': 'GMD-2026-1187', 'invoice_date': '2026-11-03',
        'invoice_payment_term_id': odoo('account.payment.term', 'search', [['name', '=', '30 jours']], context=fr)[0],
        'invoice_line_ids': [[0, 0, {'product_id': farine[0], 'quantity': 10, 'price_unit': 18000}]]}, context=fr)
    odoo('account.move', 'action_post', [facture], context=fr)
    return facture


def cpt_15():
    # avoir fournisseur et paiements fournisseurs faits à l'écran : on les défait ; deuxième facture de l'épicerie
    # (BILL/2026/10/0001, 200 œufs, 11 800 F, réf. EPI-1015) refaite à neuf ; mode de paiement sortant de la banque sans compte
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    paiements = odoo('account.payment', 'search', [['partner_type', '=', 'supplier']])
    if paiements:
        valides = odoo('account.payment', 'search', [['id', 'in', paiements], ['state', '!=', 'draft']])
        if valides:
            odoo('account.payment', 'action_draft', valides, context=fr)
        odoo('account.payment', 'unlink', paiements, context=fr)
    lignes = odoo('account.payment.method.line', 'search', [['journal_id.code', '=', 'BNK1'], ['payment_type', '=', 'outbound']], context=fr)
    odoo('account.payment.method.line', 'write', lignes, {'payment_account_id': False}, context=fr)
    a_supprimer = odoo('account.move', 'search', ['|', ['move_type', '=', 'in_refund'], '&', ['move_type', '=', 'in_invoice'], ['ref', '=', 'EPI-1015']], order='id desc')
    for f in a_supprimer:
        if odoo('account.move', 'read', [f], ['state'])[0]['state'] != 'draft':
            odoo('account.move', 'button_draft', [f], context=fr)
        odoo('account.move', 'unlink', [f], context=fr)
    moulins = facture_moulins()
    epicerie = odoo('res.partner', 'search', [['name', '=', 'EPICERIE NOUVELLE J C BITTAR']])[0]
    oeuf = odoo('product.product', 'search', [['name', '=', 'Oeuf']])
    seconde = odoo('account.move', 'create', {
        'move_type': 'in_invoice', 'partner_id': epicerie, 'ref': 'EPI-1015', 'invoice_date': '2026-10-15',
        'invoice_date_due': '2026-10-15', 'invoice_payment_term_id': False,
        'invoice_line_ids': [[0, 0, {'product_id': oeuf[0], 'quantity': 200, 'price_unit': 50}]]}, context=fr)
    odoo('account.move', 'action_post', [seconde], context=fr)
    factures = odoo('account.move', 'search', [['move_type', '=', 'in_invoice']])
    traces = odoo('mail.message', 'search', [['model', '=', 'account.move'], ['res_id', 'in', factures], ['date', '>=', '2026-11-05 12:00:00'],
                                              ['res_id', '!=', seconde]])
    if traces:
        odoo('mail.message', 'unlink', traces)
    # l'historique du journal Banque garde les va-et-vient des tournages de CPT-08 : on le vide (il est filmé ici)
    banque = odoo('account.journal', 'search', [['code', '=', 'BNK1'], ['company_id', '=', SOCIETE]])
    traces = odoo('mail.message', 'search', [['model', '=', 'account.journal'], ['res_id', 'in', banque], ['date', '>=', '2026-10-25 00:00:00']])
    if traces:
        odoo('mail.message', 'unlink', traces)
    return odoo('account.move', 'read', [moulins, seconde], ['name', 'amount_residual'])


def cpt_16():
    # la dépense d'Amy BA (déjeuner avec un client, 23 600 F) est saisie, comptabilisée et remboursée à l'écran : on défait tout
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    depenses = odoo('hr.expense', 'search', [], context=fr)
    for d in depenses:
        piece = odoo('hr.expense', 'read', [d], ['account_move_id'], context=fr)[0]['account_move_id']
        if piece:
            paiements = odoo('account.payment', 'search', [['reconciled_bill_ids', 'in', [piece[0]]]])
            if paiements:
                odoo('account.payment', 'action_draft', paiements, context=fr)
                odoo('account.payment', 'unlink', paiements, context=fr)
            if odoo('account.move', 'read', [piece[0]], ['state'])[0]['state'] != 'draft':
                odoo('account.move', 'button_draft', [piece[0]], context=fr)
            odoo('account.move', 'unlink', [piece[0]], context=fr)
        if odoo('hr.expense', 'read', [d], ['state'], context=fr)[0]['state'] != 'draft':
            odoo('hr.expense', 'action_reset', [d], context=fr)
    if depenses:
        odoo('hr.expense', 'unlink', depenses, context=fr)
    return len(depenses)


def cpt_17():
    # le relevé de la banque est importé (et une ligne saisie à la main) à l'écran : on supprime les lignes de relevé
    # du journal Banque, en défaisant leurs rapprochements (les paiements repassent « en cours »), puis les relevés
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    banque = odoo('account.journal', 'search', [['code', '=', 'BNK1'], ['company_id', '=', SOCIETE]])
    lignes = odoo('account.bank.statement.line', 'search', [['journal_id', 'in', banque]], context=fr)
    for l in lignes:
        if odoo('account.bank.statement.line', 'read', [l], ['is_reconciled'], context=fr)[0]['is_reconciled']:
            odoo('account.bank.statement.line', 'action_undo_reconciliation', [l], context=fr)
    releves = odoo('account.bank.statement', 'search', [['journal_id', 'in', banque]], context=fr)
    if releves:  # Odoo refuse de supprimer une ligne d'un relevé validé : le relevé d'abord
        odoo('account.bank.statement', 'unlink', releves, context=fr)
    lignes = odoo('account.bank.statement.line', 'search', [['journal_id', 'in', banque]], context=fr)
    if lignes:
        odoo('account.bank.statement.line', 'unlink', lignes, context=fr)
    return len(lignes), len(releves)


def cpt_18():
    # on part de la fin de CPT-17 (relevé importé, trois virements déjà reliés aux paiements) et on ajoute le virement du
    # traiteur, qui règle INV/2026/00006 (relancée dans CPT-13) ; les rapprochements faits à l'écran (virement du traiteur,
    # frais de tenue de compte, versement d'espèces) sont défaits
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    banque = odoo('account.journal', 'search', [['code', '=', 'BNK1'], ['company_id', '=', SOCIETE]])[0]
    if not odoo('account.bank.statement.line', 'search', [['journal_id', '=', banque], ['payment_ref', 'like', 'VIR GRANDS MOULINS']]):
        sys.exit("Le relevé de CPT-17 manque : retourner CPT-17 (l'import le recrée) avant CPT-18.")
    traiteur = odoo('res.partner', 'search', [['name', '=', 'Traiteur Saveurs du Plateau']])[0]
    a_defaire = odoo('account.bank.statement.line', 'search', [['journal_id', '=', banque], ['is_reconciled', '=', True],
        ['payment_ref', 'in', ['FRAIS TENUE DE COMPTE NOVEMBRE', 'VERSEMENT ESPECES CAISSE BOUTIQUE', 'VIR SAVEURS DU PLATEAU REGLEMENT SEMINAIRE']]])
    for l in a_defaire:
        odoo('account.bank.statement.line', 'action_undo_reconciliation', [l], context=fr)
    if not odoo('account.bank.statement.line', 'search', [['journal_id', '=', banque], ['payment_ref', '=', 'VIR SAVEURS DU PLATEAU REGLEMENT SEMINAIRE']]):
        odoo('account.bank.statement.line', 'create', {'journal_id': banque, 'date': '2026-11-07', 'partner_id': traiteur,
                                                       'payment_ref': 'VIR SAVEURS DU PLATEAU REGLEMENT SEMINAIRE', 'amount': 127440}, context=fr)
    seminaire = odoo('account.move', 'search', [['ref', '=', 'Commande du séminaire'], ['move_type', '=', 'out_invoice']])
    traces = odoo('mail.message', 'search', [['model', '=', 'account.move'], ['res_id', 'in', seminaire], ['date', '>=', '2026-11-07 00:00:00']])
    if traces:
        odoo('mail.message', 'unlink', traces)
    return odoo('account.bank.statement.line', 'search_read', [['journal_id', '=', banque], ['is_reconciled', '=', False]], ['payment_ref', 'amount'])


def cpt_19():
    # le modèle « Frais bancaires » (livré par Odoo : manuel, libellé « Bank Fees », compte 601100) est corrigé et automatisé
    # à l'écran, puis un second relevé (2 lignes de frais) est importé : on remet le modèle d'origine et on supprime ce relevé
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    modele = odoo('account.reconcile.model', 'search', [['name', '=', 'Frais bancaires']], context=fr)
    if modele:
        odoo('account.reconcile.model', 'write', modele, {'trigger': 'manual', 'match_label': 'contains', 'match_label_param': 'Bank Fees',
                                                          'match_journal_ids': [[6, 0, []]]}, context=fr)
        lignes_modele = odoo('account.reconcile.model', 'read', modele, ['line_ids'], context=fr)[0]['line_ids']
        achats = odoo('account.account', 'search', [['code', '=', '601100']], context=fr)
        odoo('account.reconcile.model.line', 'write', lignes_modele[:1], {'account_id': achats[0], 'label': 'Bank Fees'}, context=fr)
        if len(lignes_modele) > 1:
            odoo('account.reconcile.model.line', 'unlink', lignes_modele[1:], context=fr)
    banque = odoo('account.journal', 'search', [['code', '=', 'BNK1'], ['company_id', '=', SOCIETE]])[0]
    lignes = odoo('account.bank.statement.line', 'search', [['journal_id', '=', banque],
                  ['payment_ref', 'in', ['FRAIS VIREMENT SORTANT', 'FRAIS SMS BANKING NOVEMBRE']]], context=fr)
    releves = set()
    for l in lignes:
        info = odoo('account.bank.statement.line', 'read', [l], ['is_reconciled', 'statement_id'], context=fr)[0]
        if info['is_reconciled']:
            odoo('account.bank.statement.line', 'action_undo_reconciliation', [l], context=fr)
        if info['statement_id']:
            releves.add(info['statement_id'][0])
    if releves:
        odoo('account.bank.statement', 'unlink', list(releves), context=fr)
    lignes = odoo('account.bank.statement.line', 'search', [['id', 'in', lignes]], context=fr)
    if lignes:
        odoo('account.bank.statement.line', 'unlink', lignes, context=fr)
    # les lignes ajoutées après l'import de CPT-17 (frais saisis à la main, virement du traiteur) n'ont pas de relevé :
    # le relevé importé ici paraîtrait « invalide » (solde de départ faux). On les range dans le relevé de CPT-17.
    premiere = odoo('account.bank.statement.line', 'search_read', [['journal_id', '=', banque], ['payment_ref', 'like', 'VIR GRANDS MOULINS']], ['statement_id'])
    if premiere and premiere[0]['statement_id']:
        releve = premiere[0]['statement_id'][0]
        orphelines = odoo('account.bank.statement.line', 'search', [['journal_id', '=', banque], ['statement_id', '=', False]])
        if orphelines:
            odoo('account.bank.statement.line', 'write', orphelines, {'statement_id': releve}, context=fr)
        fin = odoo('account.bank.statement', 'read', [releve], ['balance_end'], context=fr)[0]['balance_end']
        odoo('account.bank.statement', 'write', [releve], {'balance_end_real': fin}, context=fr)
    return len(lignes), len(releves)


def cpt_20():
    # journal « Caisse boutique » : on supprime toutes ses lignes de relevé (encaissement de la facture des Almadies,
    # achat de gaz, versement à la banque, écart de caisse faits à l'écran) et on recrée la recette de départ :
    # « VENTES COMPTOIR DU 1er AU 4 NOVEMBRE », +300 000 F, déjà rangée en 701100 (sans quoi la caisse ne pourrait pas
    # verser 300 000 F à la banque). La facture INV/2026/00005 (Almadies, 35 400 F, CPT-13) redevient due.
    fr = {'lang': 'fr_FR', 'allowed_company_ids': [SOCIETE]}
    caisse = odoo('account.journal', 'search', [['code', '=', 'CAI'], ['company_id', '=', SOCIETE]])[0]
    lignes = odoo('account.bank.statement.line', 'search', [['journal_id', '=', caisse]], context=fr)
    for l in lignes:
        if odoo('account.bank.statement.line', 'read', [l], ['is_reconciled'], context=fr)[0]['is_reconciled']:
            odoo('account.bank.statement.line', 'action_undo_reconciliation', [l], context=fr)
    releves = odoo('account.bank.statement', 'search', [['journal_id', '=', caisse]], context=fr)
    if releves:
        odoo('account.bank.statement', 'unlink', releves, context=fr)
    lignes = odoo('account.bank.statement.line', 'search', [['journal_id', '=', caisse]], context=fr)
    if lignes:
        odoo('account.bank.statement.line', 'unlink', lignes, context=fr)
    ligne = odoo('account.bank.statement.line', 'create', {'journal_id': caisse, 'date': '2026-11-04', 'amount': 300000,
                                                           'payment_ref': 'VENTES COMPTOIR DU 1er AU 4 NOVEMBRE'}, context=fr)
    piece = odoo('account.bank.statement.line', 'read', [ligne], ['move_id'], context=fr)[0]['move_id'][0]
    especes = odoo('account.journal', 'read', [caisse], ['default_account_id'], context=fr)[0]['default_account_id'][0]
    attente = odoo('account.move.line', 'search', [['move_id', '=', piece], ['account_id', '!=', especes]])
    ventes = odoo('account.account', 'search', [['code', '=', '701100']], context=fr)[0]
    odoo('account.move', 'button_draft', [piece], context=fr)
    odoo('account.move.line', 'write', attente, {'account_id': ventes}, context=fr)
    odoo('account.move', 'action_post', [piece], context=fr)
    reassort = odoo('account.move', 'search', [['ref', '=', 'Réassort de la vitrine'], ['move_type', '=', 'out_invoice']])
    traces = odoo('mail.message', 'search', [['model', '=', 'account.move'], ['res_id', 'in', reassort], ['date', '>=', '2026-11-08 00:00:00']])
    if traces:
        odoo('mail.message', 'unlink', traces)
    return odoo('account.move', 'read', reassort, ['name', 'amount_residual'])


CAPSULES = {'CPT-02': cpt_02, 'CPT-03': cpt_03, 'CPT-04': cpt_04, 'CPT-05': cpt_05, 'CPT-06': cpt_06, 'CPT-07': cpt_07,
            'CPT-08': cpt_08, 'CPT-09': cpt_09, 'CPT-10': cpt_10, 'CPT-11': cpt_11, 'CPT-12': cpt_12, 'CPT-13': cpt_13, 'CPT-14': cpt_14, 'CPT-15': cpt_15, 'CPT-16': cpt_16, 'CPT-17': cpt_17, 'CPT-18': cpt_18, 'CPT-19': cpt_19, 'CPT-20': cpt_20}

if __name__ == '__main__':
    code = sys.argv[1] if len(sys.argv) > 1 else ''
    if code not in CAPSULES:
        sys.exit(f"Capsule inconnue : {code} (connues : {', '.join(CAPSULES)})")
    print(code, 'prête :', CAPSULES[code]())
