# STU-03 · Choisir le bon lien entre deux fiches — texte de la voix off

Voix : 3466 caractères.

## Introduction

Bonjour. Dans la capsule précédente, nous avons ajouté des champs simples : une liste de choix et un nombre. Aujourd'hui, nous allons relier deux fiches entre elles.

La plupart des champs mal conçus ne sont pas des erreurs de libellé, mais des erreurs de lien. Et on ne change pas le type d'un champ rempli sans perdre ses données. À la fin de cette capsule, vous saurez choisir le bon lien, et éviter de recopier une information qui existe déjà.


## 1. La question à poser

Avant d'ouvrir Studio, posez une question : combien de X pour un Y ? Un livreur par livraison ? Plusieurs allergènes par produit ? Plusieurs moments dans le déroulé d'un mariage ?

Voici le bon de livraison du mariage de la famille Ndiaye. Maïmouna veut y voir le livreur, et le téléphone du client pour qu'il puisse l'appeler en route.

Ouvrons Studio sur ce bon de livraison.

Dans la liste des nouveaux champs, quatre servent à relier des fiches. Many2One : un seul élément choisi dans une liste, par exemple un livreur pour une livraison.

Étiquettes : plusieurs éléments partagés entre les fiches, comme les allergènes, réutilisés sur tous les produits.

Lignes : plusieurs lignes qui n'appartiennent qu'à cette fiche, comme le déroulé d'un mariage : treize heures le cocktail, quinze heures le déjeuner.

Et le champ associé : aucune saisie, il affiche une valeur déjà enregistrée ailleurs.


## 2. Le livreur : un Many2One

Un seul livreur par livraison : c'est un Many2One. Glissez-le sous le type d'opération.

Odoo demande vers quelles fiches pointer. Le livreur devra se connecter à Odoo : on choisit donc les utilisateurs. Leur nom technique est res.users ; tapez-le pour les trouver plus vite, et choisissez Utilisateur.

Confirmez.

Le libellé : Livreur. Puis le nom technique : livreur.


## 3. Le téléphone : un champ associé

Pour le téléphone du client, le réflexe naïf serait de créer un champ Téléphone et de le remplir. Ce serait une deuxième copie, jamais à jour. Le champ associé, lui, lit le téléphone sur la fiche du client.

Odoo demande le chemin. Cherchez Contact, le client de la livraison, et cliquez sur la flèche pour entrer dans sa fiche.

Puis choisissez Téléphone, et confirmez.

Libellé : Téléphone du client. Nom technique : téléphone du client.

Fermez Studio.


## 4. Le résultat

Le téléphone de Moussa Ndiaye s'affiche déjà, sans aucune saisie. Le jour où il change de numéro sur sa fiche, le bon de livraison suit tout seul.

Le livreur se choisit dans la liste des utilisateurs. Seules les personnes qui ont un compte Odoo y figurent : Modou, notre livreur, recevra le sien dans la capsule sur les droits d'accès.


## Les pièges à éviter

Trois pièges fréquents. Premier piège : un texte à la place d'un Many2One. Un livreur tapé à la main, Modou, modou F., ne se relie à personne : impossible de compter les livraisons par livreur.

Deuxième piège : une liste de choix à la place d'étiquettes. Un produit qui contient du gluten et du lait ne peut porter qu'une seule valeur.

Troisième piège : des étiquettes à la place de lignes. Les horaires du déroulé seraient partagés entre tous les mariages ; en modifier un modifierait les autres.


## Récapitulatif

Récapitulons. Un seul élément : Many2One. Plusieurs éléments partagés : Étiquettes. Plusieurs lignes propres à la fiche : Lignes. Une valeur qui existe déjà ailleurs : un champ associé, jamais une copie. Et dessinez le lien sur papier avant d'ouvrir Studio.

Votre exercice : sur les devis, ajoutez un champ associé qui affiche l'adresse e-mail du client. Dans la prochaine capsule, nous rangerons les écrans : formulaire, liste et kanban. À tout de suite !

