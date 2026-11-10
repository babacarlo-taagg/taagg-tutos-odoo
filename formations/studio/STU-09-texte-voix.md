# STU-09 · Du test à la production — texte de la voix off

## Introduction

1. Bonjour. Tout ce que nous avons construit pour les Délices de Maïmouna l'a été dans une base de test. Il reste à le livrer dans la vraie base, celle où l'équipe travaille chaque jour, sans rien refaire à la main et sans rien casser.

2. Dans cette capsule : tenir le registre des personnalisations, faire la recette, puis exporter depuis le test et importer en production.

## 1. Le registre des personnalisations

3. Odoo garde la liste technique de ce que Studio a créé. En mode développeur, Paramètres, Technique, Champs : cherchez x_studio.

4. Voici nos champs : le type d'événement et le nombre de convives sur les devis, le livreur sur les transferts. Le nom technique, le modèle, le type : tout y est.

5. Mais Odoo ne sait pas pourquoi un champ existe, ni qui l'a demandé. C'est le rôle du registre : un simple tableur, une ligne par personnalisation, avec la date, le nom technique, le pourquoi et le demandeur. Dans deux ans, c'est lui qui dira si un champ peut être retiré.

## 2. La recette avant la livraison

6. Avant d'exporter, on fait la recette dans la base de test : chaque champ est utile et lu quelque part, chaque automatisation est testée dans ses trois cas, chaque droit est vérifié avec le compte de la personne.

7. La check-list de la fiche de cette leçon se fait signer par un utilisateur du client. Une seule case vide, et la personnalisation n'est pas terminée.

## 3. Exporter depuis la base de test

8. Ouvrez Studio depuis l'écran d'accueil. En haut, deux boutons : Exporter et Import.

9. Cliquez sur Exporter. Par défaut, Odoo exporte la structure : les champs, les vues, les automatisations, les rapports. Pas les devis ni les clients : la vraie base a déjà les siens.

10. Cliquez sur Exporter : Odoo télécharge un fichier point zip. Renommez-le avec la date et le nom du client, et rangez-le avec le registre : c'est la trace exacte de ce qui a été livré.

## 4. Importer en production

11. Dans la base de production, première chose : une sauvegarde, faite le jour même. Si l'import se passe mal, c'est elle qui vous sauve.

12. Puis Studio, Import. On choisit le fichier point zip, et on clique sur Installer.

13. Laissez décochées les deux cases : on ne charge jamais de données de démonstration dans une vraie base.

14. Ici, nous sommes sur la base de test : on annule.

## Les pièges à éviter

15. Trois pièges fréquents. Premier piège : personnaliser directement la production pendant la réunion avec le client. C'est rapide, et c'est la source de la plupart des catastrophes.

16. Deuxième piège : importer dans une base différente. La base de production doit avoir la même version d'Odoo et les mêmes applications installées que la base de test.

17. Troisième piège : oublier le registre. Sans lui, personne ne saura plus pourquoi un champ existe, et on n'osera plus jamais rien retirer.

## Récapitulatif

18. Récapitulons. On construit dans une base de test, on tient le registre, on fait la recette avec la check-list. Puis Studio, Exporter, une sauvegarde de la production, et Studio, Import.

19. Votre exercice : remplissez le registre pour toutes les personnalisations de cette formation, puis faites un export daté. Ensuite, place à l'atelier : les cinq demandes de Maïmouna. À vous de jouer !
