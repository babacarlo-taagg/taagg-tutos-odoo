# STU-05 · Un champ calculé : le prix par convive — texte de la voix off

Brouillon muet : 4 min 13. Voix : 3127 caractères.

## Introduction

Bonjour. Maïmouna compare ses mariages au prix par convive. Aujourd'hui, elle le calcule à la main sur son téléphone. Dans cette capsule, Odoo va le calculer pour elle, à partir du total du devis et du nombre de convives.

Un champ calculé ne se saisit pas : Odoo le remplit tout seul. C'est la limite du sans-code : nous écrirons deux lignes de Python, pas plus.


## 1. Vérifier le standard d'abord

Avant de créer un champ calculé, vérifiez qu'Odoo ne le fait pas déjà. Dans les paramètres des ventes, cherchons Marges.

La marge sur les ventes existe en standard : il suffit de cocher cette case, inutile de la recalculer. Le prix par convive, lui, n'existe pas : nous le créons.


## 2. Le champ Monétaire

Ouvrons le devis du mariage de la famille Ndiaye, puis Studio.

Un prix, c'est un montant en francs CFA : prenez Monétaire, et glissez-le sous le nombre de convives. Studio ajoute aussi la devise, juste en dessous.

Le libellé : Prix par convive. Puis le nom technique : prix par convive.


## 3. Écrire le calcul

Le calcul ne se règle pas dans ce panneau. En bas, cliquez sur Plus : Odoo ouvre la fiche technique du champ.

Ouvrez l'onglet Calculer. Odoo rappelle en dessous comment on écrit un champ calculé.

D'abord, les dépendances : les champs qui, en changeant, doivent relancer le calcul. Ici, le montant hors taxes, et le nombre de convives.

Puis le calcul. Première ligne : pour chaque devis. Odoo calcule souvent plusieurs fiches à la fois.

Deuxième ligne : le prix par convive vaut le montant hors taxes divisé par le nombre de convives, s'il y en a. Sinon, zéro. Ce « sinon » est obligatoire : chaque devis doit recevoir une valeur.

Enregistrez.

Dans l'onglet Propriétés, la case Enregistré est cochée : la valeur est gardée en base. On pourra donc trier et regrouper les devis par prix par convive. Fermez Studio.


## 4. Tester

Surprise : le prix par convive affiche zéro. Un champ calculé ajouté après coup ne recalcule pas tout seul les devis déjà existants. Il attend qu'une de ses dépendances change.

Passons à cent soixante convives.

Le calcul se fait aussitôt : un million deux cent mille divisé par cent soixante, sept mille cinq cents francs.

Revenons à cent cinquante, et enregistrez : huit mille francs par convive.


## Les pièges à éviter

Trois pièges fréquents. Premier piège : oublier une dépendance. Le calcul ne se relance plus quand ce champ change, et la valeur affichée devient fausse sans que personne ne s'en aperçoive.

Deuxième piège : les devis existants restent à zéro. Après avoir créé le champ, prévoyez de les mettre à jour, ou prévenez le client que seuls les nouveaux devis seront calculés.

Troisième piège : aller trop loin. Si la formule dépasse quelques lignes ou va chercher des données dans trois écrans différents, arrêtez-vous : c'est un travail de développeur, à faire dans un module.


## Récapitulatif

Récapitulons. On vérifie d'abord le standard. On crée le champ avec Studio, puis Plus, onglet Calculer : les dépendances, et deux lignes de calcul qui donnent toujours une valeur. Et on teste avec un vrai devis.

Votre exercice : créez un champ Acompte, égal à la moitié du total du devis. Dans la prochaine capsule, Odoo agira tout seul : nous créerons une règle d'automatisation. À tout de suite !

