# STU-08 · Le livreur ne voit que ses livraisons — texte de la voix off

## Introduction

1. Bonjour. Modou, le livreur des Délices de Maïmouna, va recevoir un compte Odoo pour valider ses livraisons depuis son téléphone. Maïmouna pose une condition : il ne doit voir que ses livraisons à lui.

2. Cacher une colonne ne suffit pas : la donnée resterait accessible par un autre écran ou par un export. Pour protéger, on utilise les groupes et les règles d'accès. C'est ce que nous allons faire.

## 1. Le constat

3. Voici les bons de livraison des deux mariages. Sur chacun, le champ Livreur, créé dans la capsule sur les liens, indique qui livre : Modou pour la famille Ndiaye, un autre livreur pour la famille Sarr.

4. Aujourd'hui, Modou verrait toutes les livraisons de l'entreprise, avec les adresses de tous les clients. Construisons sa protection.

## 2. Un groupe pour les livreurs

5. Les droits se donnent à des groupes, pas à des personnes. En mode développeur, ouvrez Paramètres, Utilisateurs et sociétés, Groupes, et cliquez sur Nouveau.

6. Nommez-le comme un rôle : Livraison, Livreur.

7. Dans l'onglet Utilisateurs, ajoutez Modou. Le jour où un deuxième livreur arrive, il suffira de l'ajouter ici.

## 3. La règle : ses livraisons seulement

8. Les droits d'accès disent ce qu'un groupe peut faire sur un type de fiche. Les règles sur les enregistrements disent sur quelles fiches. Ouvrez cet onglet, Ajouter une ligne, puis Nouveau.

9. Un nom clair : Livreur, ses livraisons seulement. Le modèle : Transfert, c'est-à-dire les livraisons.

10. Et le domaine, la condition à remplir : le livreur de la livraison est l'utilisateur connecté. Le mot user désigne la personne qui utilise Odoo à ce moment-là.

11. Les quatre cases, lire, écrire, créer et supprimer, restent cochées : la règle s'applique à tout. La case Global est encore cochée : elle s'enlève quand la règle est rattachée au groupe, à l'enregistrement. Enregistrez la règle, puis le groupe.

## 4. Tester avec le compte de Modou

12. Votre compte d'administrateur voit presque tout : un test fait avec lui ne prouve rien. On se connecte donc avec le compte de Modou.

13. Voici l'accueil de Modou. Ouvrons Inventaire, les transferts, et cherchons les deux mariages.

14. Une seule ligne : la livraison de la famille Ndiaye, la sienne. Celle de la famille Sarr, confiée à un autre livreur, n'existe pas pour lui. C'est Odoo qui filtre, sur tous les écrans, les exports et les recherches.

## Les pièges à éviter

15. Trois pièges fréquents. Premier piège : croire qu'une colonne masquée est protégée. Faites toujours le test de l'export avec le compte de la personne : si la donnée y apparaît, elle n'est pas protégée.

16. Deuxième piège : les groupes s'additionnent. Si Modou recevait aussi un rôle plus large sur les livraisons, c'est la règle la plus large qui l'emporterait. Ne donnez jamais un rôle « au cas où ».

17. Troisième piège : tester avec votre propre compte. Gardez un compte de test par profil, et vérifiez chaque règle avec lui avant de la livrer au client.

## Récapitulatif

18. Récapitulons. Les droits se donnent à un groupe, jamais à une personne. Les droits d'accès disent quoi, les règles sur les enregistrements disent sur quelles fiches. Et on teste toujours avec le compte concerné.

19. Votre exercice : créez une règle pour que chaque vendeur ne voie que ses propres devis. Dans la prochaine capsule, nous verrons comment faire passer une personnalisation de la base de test à la production. À tout de suite !
