// Essai complet sans vrai Odoo : sert un faux Odoo en local et tourne les scénarios d'exemple, voix muette
// (01 : écran d'Odoo ; 02 : mode terminal).
// Usage : npm test            (vidéo complète avec générique)
//         npm test -- --brouillon
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ICI = path.dirname(fileURLToPath(import.meta.url));
const RACINE = path.join(ICI, 'odoo-factice');
const serveur = http.createServer((req, res) => {
  let f = path.join(RACINE, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!f.startsWith(RACINE) || !fs.existsSync(f)) return res.writeHead(404).end();
  res.writeHead(200, { 'content-type': f.endsWith('.css') ? 'text/css' : 'text/html; charset=utf-8' }).end(fs.readFileSync(f));
});
serveur.listen(0, async () => {
  const env = { ...process.env, ODOO_URL: `http://127.0.0.1:${serveur.address().port}`, ODOO_LOGIN: '' };
  const { spawn } = await import('node:child_process');
  const tourner = (scenario) => new Promise((ok) => {
    const p = spawn(process.execPath, [path.join(ICI, '..', 'tuto.mjs'), path.join(ICI, '..', 'scenarios', scenario), '--voix', 'muet', ...process.argv.slice(2)], { env, stdio: 'inherit' });
    p.on('exit', ok);
  });
  // 1. scénario Odoo (sur le faux Odoo), 2. scénario en mode terminal (commandes lancées pour de vrai)
  let r = await tourner('01-creer-un-contact.yaml');
  if (r === 0) r = await tourner('02-terminal-premiers-pas.yaml');
  serveur.close();
  process.exit(r);
});
