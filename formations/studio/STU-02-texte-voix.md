# STU-02 · Ajouter des champs : le type d'événement — texte de la voix off

Brouillon muet : 4 min 32. Voix : 3592 caractères.

## Introduction

Bonjour et bienvenue dans cette capsule consacrée à Studio. Les Délices de Maïmouna font une grande partie de leur chiffre en traiteur : mariages, baptêmes, séminaires.

Maïmouna veut savoir, devis par devis, de quel événement il s'agit et pour combien de convives. À la fin de cette capsule, vous saurez ajouter ces deux champs sur les devis, sans écrire une ligne de code.


## 1. Ouvrir Studio sur un devis

Ouvrons le devis du mariage de la famille Ndiaye.

Le petit insecte en haut de l'écran indique que le mode développeur est actif. Gardez-le : il permet de choisir le nom technique de chaque champ.

Cliquez maintenant sur l'icône de Studio, en haut à droite. Studio s'ouvre sur l'écran que vous regardiez : ici, la fiche du devis.


## 2. Le type d'événement

À gauche, la liste des nouveaux champs. Pour le type d'événement, prenez Sélection : une liste de choix fixes.

Faites-la glisser juste sous le client.

Odoo demande les valeurs possibles. Tapez-les dans l'ordre où l'utilisateur les lira : Mariage, Baptême, Séminaire, Anniversaire, et Autre.

Cliquez sur Confirmer. Le champ est créé, et ses propriétés s'affichent à gauche.

Donnez-lui d'abord son libellé, celui que verront les utilisateurs : Type d'événement.

Puis vérifiez le nom technique, juste en dessous. Studio ajoute toujours le préfixe x studio. Écrivez type événement, sans accent ni espace. Faites-le tout de suite : une fois le champ utilisé, ce nom ne change plus.

Et une infobulle d'aide, pour expliquer quand le remplir : laisser vide pour une commande de la boutique.


## 3. Le nombre de convives

Deuxième champ : le nombre de convives. C'est un nombre entier. Glissez le champ Entier juste sous le type d'événement.

Même méthode : le libellé d'abord, Nombre de convives, puis le nom technique.

Ce champ n'a de sens que pour un événement. Rendons-le d'abord obligatoire, mais seulement quand un type d'événement est choisi. À côté de Requis, cliquez sur Conditionnel.

Choisissez le champ Type d'événement, puis la règle : est défini.

Confirmez.

Ensuite, cachons-le quand il ne sert à rien. À côté d'Invisible, cliquez sur Conditionnel, choisissez Type d'événement, et cette fois : n'est pas défini.

Confirmez. Le champ disparaît de Studio : c'est normal, ce devis n'a pas encore de type d'événement.

Fermez Studio. Chaque geste est déjà enregistré : il n'y a pas de bouton Sauvegarder.


## 4. Tester sur le devis

Testons. Dans le champ Type d'événement, choisissez Mariage.

Le nombre de convives apparaît aussitôt. Saisissez cent cinquante, puis enregistrez.

Le devis porte maintenant son événement. Une liste de choix fixes garantit des valeurs propres : vous pourrez compter vos mariages, et non des mariage, MARIAGE ou mariage Thiès.


## Les pièges à éviter

Trois pièges fréquents. Premier piège : un nombre entier vaut zéro par défaut. Pour Odoo, zéro est une valeur : Requis n'empêche donc pas d'enregistrer zéro convive. Vérifiez-le à la relecture des devis.

Deuxième piège : rendre un champ obligatoire et invisible dans les mêmes conditions. L'utilisateur ne peut plus enregistrer, et ne voit pas ce qu'on lui demande.

Troisième piège : supprimer une valeur de la liste plus tard. Les devis qui la portaient la perdent. Pour changer un mot, modifiez la valeur au lieu de la supprimer.


## Récapitulatif

Récapitulons. On ouvre Studio sur l'écran à modifier, on glisse le bon type de champ, on fixe aussitôt son libellé et son nom technique, et on règle Requis et Invisible avec Conditionnel. Puis on teste sur un vrai devis.

Votre exercice : ajoutez sur les devis un champ Date de l'événement, visible seulement quand un type d'événement est choisi. Dans la prochaine capsule, nous verrons comment relier deux fiches entre elles. À tout de suite !

