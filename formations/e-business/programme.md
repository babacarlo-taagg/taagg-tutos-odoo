# Formation E-Business Odoo — programme

Formation vidéo qui accompagne le programme TAAGG School
« [E-Business : lancer sa boutique en ligne avec Odoo](https://www.taagg-school.com/programmes/e-business-lancer-sa-boutique-en-ligne-avec-odoo-7) »
(8 semaines + 3 mois d'incubation, 37 leçons). Les capsules couvrent **les gestes dans Odoo** ;
les leçons sans écran Odoo (modèle e-business, publicité Meta/TikTok, cadre légal, financement, pitch)
restent dans le cours en ligne et les ateliers (voir la fin de ce fichier).

Base de tournage : « Les Délices de Maïmouna » — Odoo 19 Enterprise, francs CFA, TVA 18 %.
L'entreprise d'exemple est une **pâtisserie de Dakar qui vendait sur WhatsApp et ouvre sa boutique en ligne**
(gâteaux sur commande, viennoiseries, livraison à moto dans Dakar, retrait en boutique).
Capsules d'environ 10 minutes, structure commune décrite dans la compétence `formation-odoo`.
Illustrations (schémas, images d'ambiance) : compétence `tuto-odoo-illustrations`.

> ⚠ Les apprenants reçoivent une licence Odoo d'un an (Site Web, eCommerce, Ventes, CRM, Inventaire,
> Facturation). Tout ce qui est filmé ici existe en **Community**, sauf ce qui est marqué **[E]**
> (Enterprise uniquement).

### Modules installés dans la base de tournage le 28/10/2026 (avec l'accord de Babacar)

| Module | Pour | Capsules |
|---|---|---|
| eCommerce (`website_sale`) | boutique, panier, tunnel d'achat, rapports | toutes |
| Livraison (`delivery`) | modes de livraison, paiement à la livraison | EB-10, EB-11 |
| Paiement Démo (`payment_demo`) | simuler un paiement par carte sans argent réel | EB-06, EB-08, EB-11 |
| Paiement personnalisé (`payment_custom`) | « Wave / Orange Money » avec instructions, virement | EB-08, EB-09 |
| Promotions eCommerce (`website_sale_loyalty`) | codes promo, cartes de fidélité | EB-15, EB-16 |
| Retrait en boutique (`website_sale_collect`) | « je passe chercher mon gâteau » | EB-10 |
| Chat en direct (`website_livechat`) | service client sur le site | EB-12 |
| Paiement Flutterwave (`payment_flutterwave`) | montrer un vrai prestataire de paiement africain (sans clé, réglages seulement) | EB-08 |

Aussi à préparer par l'API (`etat-depart.py`) : **les prix de vente sont tous à 1 F** dans la base
(à remplacer par des prix réalistes), photos des produits, catégories de la boutique.

Avancement : ☐ à écrire · ✎ brouillon OK · 🎙 voix OK · ✅ publiée

## Parcours 1 — Créer sa boutique (Module 2 du cours)

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| EB-01 | De WhatsApp à la boutique en ligne | ce que change une boutique en ligne ; le parcours d'un client sur le site ; les menus Site Web (Site, eCommerce, Analyse, Configuration) ; où arrivent les commandes | Site Web, Boutique, Commandes | 🎙 |
| EB-02 | Construire son site | thème, couleurs, logo, page d'accueil avec des blocs, version téléphone, publier | Éditeur du site | ✎ |
| EB-03 | Les pages qui donnent confiance | À propos, Contact, Livraison et retours, Conditions de vente ; menu et pied de page | Pages, Menus | ☐ |
| EB-04 | Mettre ses produits en ligne | fiche produit pour la boutique : photo, prix TTC, description, publier / dépublier | Produits | ☐ |
| EB-05 | Organiser son catalogue | catégories de la boutique, variantes (gâteau 6, 8 ou 12 parts), filtres, ordre d'affichage | Catégories, Attributs | ☐ |
| EB-06 | Le tunnel d'achat | les étapes du client : panier, adresse, livraison, paiement, confirmation ; les réglages de la boutique (compte client, téléphone obligatoire…) | Paramètres eCommerce, Boutique | ☐ |
| EB-07 | Stock et disponibilité en ligne | afficher le stock ou « en rupture », vendre sur commande, faire l'inventaire | Inventaire, Produits | ☐ |

## Parcours 2 — Encaisser et livrer (Module 3)

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| EB-08 | Les moyens de paiement | carte (Démo), Wave et Orange Money avec instructions, virement ; Flutterwave : ce qu'il faut pour l'activer | Moyens de paiement | ☐ |
| EB-09 | Où arrive l'argent | transaction, commande payée, facture, paiement ; vérifier un paiement Wave reçu à la main | Transactions, Factures | ☐ |
| EB-10 | Organiser la livraison | forfait Dakar, zones (Plateau, banlieue, régions), livraison gratuite dès un montant, retrait en boutique, paiement à la livraison | Modes de livraison | ☐ |
| EB-11 | Une commande de bout en bout | commande test : le client paie → la commande → la livraison → la facture (livrable du module 3) | Boutique, Commandes, Inventaire | ☐ |
| EB-12 | Service client et confiance | e-mails de confirmation, l'espace « Mon compte » du client, chat en direct, avis clients | Modèles d'e-mail, Chat en direct | ☐ |

## Parcours 3 — Attirer les clients (Module 4)

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| EB-13 | Être trouvé sur Google | titre, description et image de partage de chaque page et produit ; adresse des pages ; Google Search Console et Analytics | Optimiser le référencement, Paramètres | ☐ |
| EB-14 | Mesurer ses campagnes WhatsApp, Facebook, TikTok | liens de suivi : savoir quelle publication amène les ventes | Liens traceurs | ☐ |
| EB-15 | Promotions et codes promo | code « TABASKI », réduction sur une catégorie, livraison offerte | Programmes de remise et de fidélité | ☐ |
| EB-16 | Fidéliser ses clients | carte de fidélité, newsletter, relance des paniers abandonnés | Fidélité, Marketing par e-mail | ☐ |

## Parcours 4 — Vendre et piloter (Module 5)

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| EB-17 | Du message WhatsApp au client : le CRM | noter une demande, suivre ses prospects, transformer en devis | CRM | ☐ |
| EB-18 | Devis en ligne pour les commandes sur mesure | devis envoyé par lien, accepté et payé en ligne (gâteau de mariage) | Ventes › Devis | ☐ |
| EB-19 | Facturation, coûts et marge | factures des commandes, paiements, coût et marge par produit | Facturation, Produits | ☐ |
| EB-20 | Le tableau de bord de la boutique | ventes, panier moyen, produits les plus vendus, paniers abandonnés, taux de conversion | Rapports eCommerce, Analytics | ☐ |

## Parcours 5 — Faire grandir la boutique (incubation)

| Code | Capsule | Ce qu'on apprend | Écrans | État |
|---|---|---|---|---|
| EB-21 | Augmenter le panier moyen | produits optionnels et accessoires (bougies, carte), prix barrés, listes de prix | Produits, Listes de prix | ☐ |
| EB-22 | Réapprovisionner sans rupture | fournisseurs, règles de réassort automatique, bons d'achat | Achats, Inventaire | ☐ |
| EB-23 | Prête pour le lancement | nom de domaine, check-list avant d'ouvrir, test sur téléphone | Paramètres du site | ☐ |

**23 capsules ≈ 4 h de formation.** EB-01 : 6 min 46 (voix de Babacar, vitesse 1,0) — à publier.

## Hors Odoo (pas de capsule filmée dans Odoo)

Ces leçons du cours n'ont pas d'écran Odoo à montrer. Elles peuvent devenir plus tard de courtes vidéos
illustrées (schémas + voix, compétence `tuto-odoo-illustrations`) si Babacar le souhaite :
modèles de vente en ligne ; persona et parcours d'achat ; offre, prix et marge ; publicité Meta et TikTok ;
cadre légal du commerce en ligne au Sénégal ; plan de croissance 12 mois ; prévisionnel et financement ; pitch.

## Ce qui est Enterprise dans la base de tournage (à ne pas filmer comme « standard »)

Marketing Automation, Social Marketing, WhatsApp, Studio, tableau de bord des ventes du site
(`website_sale_dashboard`, installé automatiquement avec eCommerce : EB-20 utilisera les rapports Community), Assistance (Helpdesk) : **[E]**, non utilisés dans les capsules ci-dessus.

## Ordre de tournage proposé

1. EB-01 (pilote : valide le ton, la voix, les illustrations et la durée de 10 min).
2. Parcours 1 et 2 dans l'ordre (la boutique doit exister avant de vendre).
3. Parcours 3, 4, 5.
