# STU-06 · Une règle d'automatisation : le mariage confirmé — texte de la voix off

Brouillon muet : 4 min 08. Voix : 3035 caractères.

## Introduction

Bonjour. Deux fois cette année, la cuisine des Délices de Maïmouna a appris la veille qu'elle devait préparer un mariage de trois cents couverts. Aujourd'hui, nous allons faire en sorte qu'Odoo prévienne tout seul, le jour même de la confirmation.

Une automatisation se dit toujours en une phrase : QUAND quelque chose arrive, SI une condition est remplie, ALORS Odoo fait une action. Ici : quand un devis devient une commande, si c'est un mariage, alors on crée une activité « Préparer la dégustation » pour le vendeur.


## 1. QUAND : le déclencheur

Ouvrons un devis, puis Studio, et le menu Automatisations.

Cliquez sur Nouveau. Donnez à la règle un nom qui dit QUAND et ALORS : on la relit en un coup d'œil.

Le déclencheur : Le statut est défini sur. Il agit au moment précis où le devis change de statut, et pas à chaque modification.

Quel statut ? Commande client : c'est l'état d'un devis confirmé.


## 2. SI : la condition

Maintenant, la condition. Dans Appliquer sur, cliquez sur Modifier le domaine : la règle ne concernera que les devis qui correspondent.

Ajoutez une règle, choisissez le champ Type d'événement, et la valeur Mariage.

Confirmez. Seuls les mariages déclencheront la règle.


## 3. ALORS : l'action

Reste l'action. Cliquez sur Ajouter une action. Odoo sait mettre à jour la fiche, envoyer un e-mail ou un SMS, ajouter des abonnés… Choisissez Créer une activité.

Le type : To-Do, c'est-à-dire à faire. Le titre : Préparer la dégustation. L'échéance : dans trois jours.

Pour qui ? Plutôt qu'un nom, choisissez un rôle : un utilisateur dynamique, ici le vendeur du devis. Le jour où quelqu'un quitte l'entreprise, la règle continue de fonctionner.

Enregistrez l'action, puis la règle. Elle est active immédiatement.

Fermez Studio.


## 4. Tester

Testons sur un autre mariage, celui de la famille Sarr, encore en devis.

Le client accepte. Cliquez sur Confirmer.

Le devis devient une commande, et à droite, une activité est apparue toute seule : Préparer la dégustation, pour le vendeur, dans trois jours. Personne n'a eu à y penser.


## Les pièges à éviter

Trois pièges fréquents. Premier piège : un déclencheur trop large. Avec « à la mise à jour » sans précaution, chaque modification d'un mariage confirmé créerait une nouvelle activité. Au bout d'une semaine, le vendeur en aurait quinze, et n'en lirait plus aucune.

Deuxième piège : une boucle. Si l'action modifie le champ qui déclenche la règle, la règle se relance sans fin. Ne surveillez jamais le champ que vous modifiez.

Troisième piège : tester sur de vrais clients. Une règle qui envoie un e-mail se teste d'abord avec un contact dont l'adresse est la vôtre. Et si une règle se trompe, archivez-la : elle s'arrête sans rien perdre.


## Récapitulatif

Récapitulons. On écrit d'abord la phrase QUAND, SI, ALORS. Dans Studio, Automatisations, Nouveau : le déclencheur, le domaine dans Appliquer sur, puis Ajouter une action. Et on teste sur un devis de test.

Votre exercice : créez une règle qui, quand un devis de séminaire est confirmé, ajoute une activité « Réserver la salle ». Dans la prochaine capsule, nous ferons apparaître l'événement sur le devis PDF. À tout de suite !

