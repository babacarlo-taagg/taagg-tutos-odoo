// Essai complet sans vrai Odoo : sert un faux Odoo en local et tourne le scénario d'exemple, voix muette.
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
  const r = await new Promise((ok) => {
    import('node:child_process').then(({ spawn }) => {
      const p = spawn(process.execPath, [path.join(ICI, '..', 'tuto.mjs'), path.join(ICI, '..', 'scenarios', '01-creer-un-contact.yaml'), '--voix', 'muet', ...process.argv.slice(2)], { env, stdio: 'inherit' });
      p.on('exit', ok);
    });
  });
  serveur.close();
  process.exit(r);
});
