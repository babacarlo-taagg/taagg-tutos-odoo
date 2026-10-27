# Tutos vidéo Odoo TAAGG — repères pour Claude

- Babacar (fondateur de TAAGG) travaille en français, seul avec Claude. Explications simples, sans jargon. Aucun secret dans le dépôt (les clés vont dans `.env`, ignoré par Git).
- Ce dépôt fabrique des **tutoriels vidéo Odoo avec voix off** : un scénario YAML → `node tuto.mjs` → une vidéo MP4 1080p prête pour YouTube.
- Formations longues (capsules de 10 min) : compétence `formation-odoo`, programmes dans `formations/<module>/programme.md`.
- Pour toute demande de tuto, suivre la compétence `tuto-odoo` (elle renvoie vers `tuto-odoo-scenario`, `tuto-odoo-voix`, `tuto-odoo-montage`).
- Base de tournage : https://edu-correction-les-delices-de-maimouna.odoo.com (exercice « Les Délices de Maïmouna », **Odoo 19 Enterprise** hébergé chez Odoo, en français, monnaie XOF). Accès dans `.env` : `ODOO_LOGIN` + `ODOO_MOT_DE_PASSE` pour filmer (compte « Formateur TAAGG », formateur.tuto@taagg-gui.com), `ODOO_LOGIN_API` + `ODOO_CLE_API` pour lire ou préparer les données par l'API (JSON-RPC, base = `edu-correction-les-delices-de-maimouna`).
- On ne filme **jamais** la base de production avec de vraies données personnelles (élèves, parents, tuteurs) : base de démonstration uniquement.
- La base Odoo de TAAGG (Community 20, modules maison `taagg_*`) est dans le dépôt `babacarlo-taagg/taagg-odoo` ; on ne modifie rien là-bas depuis ce projet.
- Avant de pousser une modification de `tuto.mjs` : `npm test` (tournage complet sur un faux Odoo local, voix muette).
