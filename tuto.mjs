#!/usr/bin/env node
// Tutoriels vidéo Odoo avec voix off.
// Un scénario YAML (texte dit + gestes à l'écran, étape par étape) devient une vidéo MP4 :
//   1. voix      : chaque texte est lu (ElevenLabs, OpenAI, fichiers enregistrés, ou muet)
//   2. tournage  : un navigateur rejoue les gestes dans Odoo, au rythme de la voix
//   3. montage   : ffmpeg pose la voix, les sous-titres, le générique TAAGG et la musique
//
// Usage :
//   node tuto.mjs <scenario.yaml> [--voix elevenlabs|openai|fichiers|muet] [--brouillon]
//                 [--seulement-voix] [--remonter] [--sans-sous-titres] [--visible]
//   node tuto.mjs explorer <chemin Odoo, ex. /odoo/contacts/new>
//
// Réglages (variables d'environnement ou fichier .env à côté de ce script, jamais versionné) :
//   ODOO_URL, ODOO_BASE, ODOO_LOGIN, ODOO_MOT_DE_PASSE
//   ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, ELEVENLABS_MODELE
//   OPENAI_API_KEY, OPENAI_VOIX

import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';
import { chromium } from 'playwright';

const ICI = path.dirname(fileURLToPath(import.meta.url));
const LOGO = path.join(ICI, 'ressources/logo_taagg_sombre.png');
const COULEURS = { fond: '#0B415B', accent: '#68C184', texte: '#FFFFFF' };
const SORTIE_HD = { l: 1920, h: 1080, ips: 30 };

// ---------------------------------------------------------------- outils communs

function lireEnv() {
  const f = path.join(ICI, '.env');
  if (!fs.existsSync(f)) return;
  for (const ligne of fs.readFileSync(f, 'utf8').split('\n')) {
    const m = ligne.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*?)\s*$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}

function arreter(message) {
  console.error(`\n✗ ${message}`);
  process.exit(1);
}

const pause = (ms) => new Promise((r) => setTimeout(r, ms));

function ffmpeg(args) {
  try {
    execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: ['ignore', 'inherit', 'inherit'] });
  } catch {
    arreter(`ffmpeg a échoué : ffmpeg ${args.join(' ')}`);
  }
}

function duree(fichier) {
  const s = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', fichier]).toString();
  return parseFloat(s);
}

function police(gras) {
  try {
    return execFileSync('fc-match', ['-f', '%{file}', gras ? 'Inter:bold' : 'Inter']).toString().trim();
  } catch {
    return '';
  }
}

function slug(texte) {
  return texte.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function urlOdoo(chemin) {
  const base = (process.env.ODOO_URL || 'http://localhost:8069').replace(/\/$/, '');
  return /^https?:/.test(chemin) ? chemin : base + (chemin.startsWith('/') ? chemin : '/' + chemin);
}

// ---------------------------------------------------------------- scénario

function chargerScenario(fichier) {
  if (!fs.existsSync(fichier)) arreter(`Scénario introuvable : ${fichier}`);
  const sc = YAML.parse(fs.readFileSync(fichier, 'utf8'));
  if (!sc?.titre) arreter('Le scénario doit avoir un « titre ».');
  if (!Array.isArray(sc.etapes) || !sc.etapes.length) arreter('Le scénario doit avoir des « etapes ».');
  sc.etapes.forEach((e, i) => {
    if (!e.texte) arreter(`Étape ${i + 1} : il manque le « texte » (ce que dit la voix).`);
    e.actions = e.actions || [];
  });
  sc.ecran = sc.ecran || [1600, 900];
  sc.depart = sc.depart || '/odoo';
  sc.prononciation = sc.prononciation || {};
  sc.fichier = path.resolve(fichier);
  sc.nom = path.basename(fichier).replace(/\.ya?ml$/, '');
  return sc;
}

// ---------------------------------------------------------------- 1. voix

function texteParle(sc, texte) {
  let t = texte;
  for (const [mot, dit] of Object.entries(sc.prononciation)) t = t.replaceAll(mot, dit);
  return t;
}

async function synthese(moteur, texte, vitesse, cible) {
  if (moteur === 'elevenlabs') {
    const cle = process.env.ELEVENLABS_API_KEY;
    const voix = process.env.ELEVENLABS_VOICE_ID;
    if (!cle || !voix) arreter('Voix ElevenLabs : renseignez ELEVENLABS_API_KEY et ELEVENLABS_VOICE_ID dans le fichier .env du projet');
    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voix}?output_format=mp3_44100_128`, {
      method: 'POST',
      headers: { 'xi-api-key': cle, 'content-type': 'application/json' },
      body: JSON.stringify({
        text: texte,
        model_id: process.env.ELEVENLABS_MODELE || 'eleven_multilingual_v2',
        voice_settings: { stability: 0.5, similarity_boost: 0.75, speed: vitesse },
      }),
    });
    if (!r.ok) arreter(`ElevenLabs a refusé (${r.status}) : ${await r.text()}`);
    fs.writeFileSync(cible, Buffer.from(await r.arrayBuffer()));
  } else if (moteur === 'openai') {
    const cle = process.env.OPENAI_API_KEY;
    if (!cle) arreter('Voix OpenAI : renseignez OPENAI_API_KEY dans le fichier .env du projet');
    const r = await fetch('https://api.openai.com/v1/audio/speech', {
      method: 'POST',
      headers: { authorization: `Bearer ${cle}`, 'content-type': 'application/json' },
      body: JSON.stringify({
        model: 'gpt-4o-mini-tts',
        voice: process.env.OPENAI_VOIX || 'coral',
        input: texte,
        speed: vitesse,
        instructions: "Français d'Afrique de l'Ouest, ton chaleureux et posé de formateur, phrases bien articulées.",
        response_format: 'mp3',
      }),
    });
    if (!r.ok) arreter(`OpenAI a refusé (${r.status}) : ${await r.text()}`);
    fs.writeFileSync(cible, Buffer.from(await r.arrayBuffer()));
  } else {
    // muet : silence de la durée qu'aurait la phrase (≈ 2,6 mots par seconde)
    const mots = texte.split(/\s+/).filter(Boolean).length;
    const d = (mots / 2.6 / vitesse + 0.4).toFixed(2);
    ffmpeg(['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', d, '-q:a', '4', cible]);
  }
}

async function preparerVoix(sc, moteur, dossier) {
  const dVoix = path.join(dossier, 'voix');
  fs.mkdirSync(dVoix, { recursive: true });
  const vitesse = sc.voix?.vitesse || 1;
  const pistes = [];
  for (const [i, e] of sc.etapes.entries()) {
    const n = String(i + 1).padStart(2, '0');
    let fichier;
    if (moteur === 'fichiers') {
      // voix enregistrée à la main : <scenario>.voix/01.mp3, 02.wav, …
      const dSource = sc.fichier.replace(/\.ya?ml$/, '.voix');
      const trouve = ['mp3', 'wav', 'm4a', 'ogg'].map((x) => path.join(dSource, `${n}.${x}`)).find((f) => fs.existsSync(f));
      if (!trouve) arreter(`Voix enregistrée manquante pour l'étape ${i + 1} : ${path.join(dSource, n + '.mp3')}`);
      fichier = trouve;
    } else {
      const dit = texteParle(sc, e.texte);
      const empreinte = createHash('sha1').update([moteur, vitesse, dit, process.env.ELEVENLABS_VOICE_ID, process.env.OPENAI_VOIX].join('|')).digest('hex').slice(0, 8);
      fichier = path.join(dVoix, `${n}-${moteur}-${empreinte}.mp3`);
      if (!fs.existsSync(fichier)) {
        process.stdout.write(`  voix étape ${n}… `);
        await synthese(moteur, dit, vitesse, fichier);
        console.log('ok');
      }
    }
    pistes.push({ fichier, duree: duree(fichier) });
  }
  const total = pistes.reduce((s, p) => s + p.duree, 0);
  console.log(`  ${pistes.length} pistes de voix, ${total.toFixed(0)} s de parole au total`);
  return pistes;
}

// ---------------------------------------------------------------- 2. tournage

// Curseur visible, onde au clic et cadre de surlignage, injectés dans chaque page.
const DECOR = `
(() => {
  if (window.__tuto) return;
  window.__tuto = true;
  const poser = () => {
    if (document.getElementById('tuto-curseur')) return;
    const st = document.createElement('style');
    st.textContent = \`
      #tuto-curseur{position:fixed;z-index:2147483647;pointer-events:none;width:28px;height:28px;
        margin:-3px 0 0 -4px;transition:transform .08s;filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))}
      #tuto-curseur.appui{transform:scale(.85)}
      .tuto-onde{position:fixed;z-index:2147483646;pointer-events:none;width:44px;height:44px;margin:-22px 0 0 -22px;
        border-radius:50%;background:rgba(104,193,132,.45);border:2px solid #68C184;animation:tuto-onde .55s ease-out forwards}
      @keyframes tuto-onde{from{transform:scale(.3);opacity:1}to{transform:scale(1.6);opacity:0}}
      .tuto-cadre{position:fixed;z-index:2147483645;pointer-events:none;border:4px solid #68C184;border-radius:10px;
        box-shadow:0 0 0 9999px rgba(11,65,91,.28);transition:opacity .3s}\`;
    document.head.appendChild(st);
    const c = document.createElement('div');
    c.id = 'tuto-curseur';
    c.innerHTML = '<svg viewBox="0 0 24 24" width="28" height="28"><path d="M4 2l16 10.5-7 1.2 4.3 7.6-3 1.7-4.3-7.6L4 20z" fill="#fff" stroke="#0B415B" stroke-width="1.6" stroke-linejoin="round"/></svg>';
    const p = JSON.parse(sessionStorage.getItem('tuto-pos') || '[-50,-50]');
    c.style.left = p[0] + 'px'; c.style.top = p[1] + 'px';
    document.body.appendChild(c);
  };
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', poser) : poser();
  addEventListener('mousemove', (ev) => {
    const c = document.getElementById('tuto-curseur'); if (!c) return poser();
    c.style.left = ev.clientX + 'px'; c.style.top = ev.clientY + 'px';
    sessionStorage.setItem('tuto-pos', JSON.stringify([ev.clientX, ev.clientY]));
  }, true);
  addEventListener('mousedown', (ev) => {
    document.getElementById('tuto-curseur')?.classList.add('appui');
    const o = document.createElement('div'); o.className = 'tuto-onde';
    o.style.left = ev.clientX + 'px'; o.style.top = ev.clientY + 'px';
    document.body.appendChild(o); setTimeout(() => o.remove(), 600);
  }, true);
  addEventListener('mouseup', () => document.getElementById('tuto-curseur')?.classList.remove('appui'), true);
  window.__tutoCadre = (r, ms) => {
    const d = document.createElement('div'); d.className = 'tuto-cadre';
    Object.assign(d.style, { left: r.x - 8 + 'px', top: r.y - 8 + 'px', width: r.width + 16 + 'px', height: r.height + 16 + 'px' });
    document.body.appendChild(d);
    setTimeout(() => { d.style.opacity = 0; setTimeout(() => d.remove(), 350); }, ms);
  };
})();`;

async function connexion(navigateur, sc) {
  const login = process.env.ODOO_LOGIN;
  if (!login) return undefined; // page publique, pas besoin de se connecter
  const ctx = await navigateur.newContext({ viewport: { width: sc.ecran[0], height: sc.ecran[1] }, locale: 'fr-FR' });
  const page = await ctx.newPage();
  const base = process.env.ODOO_BASE ? `?db=${encodeURIComponent(process.env.ODOO_BASE)}` : '';
  await page.goto(urlOdoo('/web/login' + base));
  await page.fill('input[name="login"]', login);
  await page.fill('input[name="password"]', process.env.ODOO_MOT_DE_PASSE || '');
  await Promise.all([page.waitForURL((u) => !u.pathname.startsWith('/web/login'), { timeout: 20000 }).catch(() => {}), page.click('button[type="submit"]')]);
  if (new URL(page.url()).pathname.startsWith('/web/login')) arreter('Connexion à Odoo refusée : vérifiez ODOO_LOGIN / ODOO_MOT_DE_PASSE / ODOO_BASE.');
  const etat = await ctx.storageState();
  await ctx.close();
  return etat;
}

class Realisateur {
  constructor(page) {
    this.page = page;
    this.x = -50;
    this.y = -50;
  }

  champ(nom) {
    return this.page.locator(`.o_field_widget[name="${nom}"]`).first();
  }

  async glisser(x, y) {
    const pas = Math.max(12, Math.min(40, Math.round(Math.hypot(x - this.x, y - this.y) / 25)));
    const [x0, y0] = [this.x, this.y];
    for (let i = 1; i <= pas; i++) {
      const t = i / pas;
      const e = t < 0.5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2; // accélère puis freine, comme une main
      await this.page.mouse.move(x0 + (x - x0) * e, y0 + (y - y0) * e);
      await pause(16);
    }
    this.x = x;
    this.y = y;
  }

  async viser(loc) {
    await loc.waitFor({ state: 'visible', timeout: 15000 });
    await loc.scrollIntoViewIfNeeded();
    const b = await loc.boundingBox();
    if (!b) throw new Error('élément introuvable à l’écran');
    await this.glisser(b.x + b.width / 2, b.y + b.height / 2);
    await pause(180);
    return b;
  }

  async cliquer(loc) {
    await this.viser(loc);
    await this.page.mouse.down();
    await pause(70);
    await this.page.mouse.up();
    await pause(450);
  }

  async taper(loc, texte, entree) {
    await this.cliquer(loc);
    await loc.fill('');
    await loc.pressSequentially(String(texte), { delay: 55 });
    if (entree) await this.page.keyboard.press('Enter');
    await pause(300);
  }

  saisie(nomChamp) {
    return this.champ(nomChamp).locator('input, textarea, [contenteditable="true"]').first();
  }

  async surligner(loc, secondes) {
    const b = await this.viser(loc);
    await this.page.evaluate(([r, ms]) => window.__tutoCadre?.(r, ms), [b, secondes * 1000]);
    await pause(secondes * 1000);
  }

  async jouer(a) {
    const p = this.page;
    if ('aller' in a) {
      await p.goto(urlOdoo(a.aller));
      await p.waitForLoadState('networkidle').catch(() => {});
      await pause(500);
    } else if ('cliquer' in a) {
      await this.cliquer(p.locator(a.cliquer).first());
    } else if ('bouton' in a) {
      const role = p.getByRole('button', { name: a.bouton, exact: false });
      await this.cliquer((await role.count()) ? role.first() : p.getByText(a.bouton, { exact: true }).first());
    } else if ('cliquer_texte' in a) {
      await this.cliquer(p.getByText(a.cliquer_texte, { exact: a.exact ?? true }).first());
    } else if ('menu' in a) {
      // « Ventes > Commandes > Devis » : appli puis menus du haut
      const niveaux = String(a.menu).split('>').map((s) => s.trim());
      const appli = niveaux.shift();
      await p.goto(urlOdoo('/odoo'));
      await p.waitForLoadState('networkidle').catch(() => {});
      await this.cliquer(p.locator('.o_app').filter({ hasText: appli }).first());
      for (const n of niveaux) {
        await p.waitForLoadState('networkidle').catch(() => {});
        await this.cliquer(p.locator('.o_menu_sections .dropdown-toggle, .o_menu_sections a, .dropdown-item').filter({ hasText: n }).first());
      }
      await p.waitForLoadState('networkidle').catch(() => {});
    } else if ('onglet' in a) {
      await this.cliquer(p.locator('.o_notebook .nav-link').filter({ hasText: a.onglet }).first());
    } else if ('champ' in a && 'taper' in a) {
      await this.taper(this.saisie(a.champ), a.taper, a.entree);
    } else if ('choisir' in a) {
      const { champ, valeur } = a.choisir;
      const select = this.champ(champ).locator('select');
      if (await select.count()) {
        await this.cliquer(select.first());
        await select.first().selectOption({ label: valeur });
      } else {
        await this.taper(this.saisie(champ), valeur);
        const choix = p.locator('.o-autocomplete--dropdown-item, .ui-menu-item').filter({ hasText: valeur }).first();
        await this.cliquer(choix);
      }
    } else if ('cocher' in a) {
      await this.cliquer(this.champ(a.cocher).locator('input[type="checkbox"], label').first());
    } else if ('rechercher' in a) {
      await this.taper(p.locator('.o_searchview_input').first(), a.rechercher, true);
      await p.waitForLoadState('networkidle').catch(() => {});
    } else if ('enregistrer' in a) {
      await this.cliquer(p.locator('.o_form_button_save').first());
      await p.waitForLoadState('networkidle').catch(() => {});
    } else if ('surligner' in a) {
      await this.surligner(p.locator(a.surligner).first(), a.duree ?? 2.5);
    } else if ('surligner_champ' in a) {
      await this.surligner(this.champ(a.surligner_champ), a.duree ?? 2.5);
    } else if ('survoler' in a) {
      await this.viser(p.locator(a.survoler).first());
    } else if ('touche' in a) {
      await p.keyboard.press(a.touche);
      await pause(300);
    } else if ('defiler' in a) {
      if (typeof a.defiler === 'number') await p.mouse.wheel(0, a.defiler);
      else await p.locator(a.defiler).first().scrollIntoViewIfNeeded();
      await pause(500);
    } else if ('attendre' in a) {
      await pause(a.attendre * 1000);
    } else {
      throw new Error(`action inconnue : ${JSON.stringify(a)}`);
    }
  }
}

async function tourner(sc, pistes, dossier, visible) {
  const navigateur = await chromium.launch({ headless: !visible });
  const etat = await connexion(navigateur, sc);
  const dBrut = path.join(dossier, 'brut');
  fs.rmSync(dBrut, { recursive: true, force: true });
  const [l, h] = sc.ecran;
  const ctx = await navigateur.newContext({
    viewport: { width: l, height: h },
    locale: 'fr-FR',
    storageState: etat,
    recordVideo: { dir: dBrut, size: { width: l, height: h } },
  });
  await ctx.addInitScript(DECOR);
  const t0 = Date.now();
  const page = await ctx.newPage();
  const r = new Realisateur(page);
  const horloge = () => (Date.now() - t0) / 1000;

  await page.goto(urlOdoo(sc.depart));
  await page.waitForLoadState('networkidle').catch(() => {});
  await pause(800);
  const debut = horloge();
  const journal = [];
  for (const [i, e] of sc.etapes.entries()) {
    const a = horloge();
    console.log(`  étape ${i + 1}/${sc.etapes.length} : ${e.texte.slice(0, 60)}…`);
    for (const action of e.actions) {
      try {
        await r.jouer(action);
      } catch (err) {
        const capture = path.join(dossier, `erreur-etape-${i + 1}.png`);
        await page.screenshot({ path: capture }).catch(() => {});
        await ctx.close();
        await navigateur.close();
        arreter(`Étape ${i + 1}, action ${JSON.stringify(action)} : ${err.message.split('\n')[0]}\n  Capture de l'écran au moment de l'erreur : ${capture}`);
      }
    }
    const reste = a + pistes[i].duree + (e.apres ?? 0.6) - horloge();
    if (reste > 0) await pause(reste * 1000);
    journal.push({ debut: a - debut, fin: horloge() - debut });
  }
  await pause(800);
  const fin = horloge();
  const video = page.video();
  await ctx.close();
  await navigateur.close();
  const brut = await video.path();
  return { brut, coupe: [debut, fin], etapes: journal };
}

// ---------------------------------------------------------------- 3. montage

function decouperSousTitres(texte, debut, longueur) {
  // morceaux de 2 lignes max (~84 caractères), coupés aux fins de phrase puis aux virgules
  const morceaux = [];
  for (const phrase of texte.replace(/\s+/g, ' ').trim().split(/(?<=[.!?…])\s+/)) {
    let reste = phrase;
    while (reste.length > 84) {
      let cut = reste.lastIndexOf(', ', 84);
      if (cut < 30) cut = reste.lastIndexOf(' ', 84);
      morceaux.push(reste.slice(0, cut + 1).trim());
      reste = reste.slice(cut + 1).trim();
    }
    if (reste) morceaux.push(reste);
  }
  const total = morceaux.reduce((s, m) => s + m.length, 0);
  let t = debut;
  return morceaux.map((m) => {
    const d = (longueur * m.length) / total;
    const sous = { debut: t, fin: t + d, texte: m.length > 42 ? couperLigne(m) : m };
    t += d;
    return sous;
  });
}

function couperLigne(m) {
  const milieu = m.length / 2;
  let meilleur = -1;
  for (let i = 0; i < m.length; i++) if (m[i] === ' ' && (meilleur < 0 || Math.abs(i - milieu) < Math.abs(meilleur - milieu))) meilleur = i;
  return meilleur < 0 ? m : m.slice(0, meilleur) + '\n' + m.slice(meilleur + 1);
}

function horodatage(s) {
  const ms = Math.round(s * 1000);
  const p = (n, l = 2) => String(n).padStart(l, '0');
  return `${p(Math.floor(ms / 3600000))}:${p(Math.floor(ms / 60000) % 60)}:${p(Math.floor(ms / 1000) % 60)},${p(ms % 1000, 3)}`;
}

function carton(dossier, nom, lignes, secondes) {
  // carton plein écran aux couleurs TAAGG : logo + jusqu'à 2 lignes de texte
  const sortie = path.join(dossier, `${nom}.mp4`);
  const [gras, normal] = [police(true), police(false)];
  const filtres = [`[1:v]scale=640:-1[logo]`, `[0:v][logo]overlay=(W-w)/2:H*0.22[v0]`];
  let dernier = 'v0';
  lignes.forEach((l, i) => {
    const f = path.join(dossier, `${nom}-${i}.txt`);
    fs.writeFileSync(f, l.texte);
    const pol = (l.gras ? gras : normal) ? `fontfile='${l.gras ? gras : normal}':` : '';
    filtres.push(`[${dernier}]drawtext=${pol}textfile='${f}':fontsize=${l.taille}:fontcolor=${l.couleur}:x=(w-text_w)/2:y=${l.y}[v${i + 1}]`);
    dernier = `v${i + 1}`;
  });
  filtres.push(`[${dernier}]fade=t=in:st=0:d=0.4,fade=t=out:st=${secondes - 0.4}:d=0.4,format=yuv420p[v]`);
  ffmpeg([
    '-f', 'lavfi', '-i', `color=c=${COULEURS.fond}:s=${SORTIE_HD.l}x${SORTIE_HD.h}:r=${SORTIE_HD.ips}:d=${secondes}`,
    '-i', LOGO,
    '-f', 'lavfi', '-i', `anullsrc=r=44100:cl=stereo`,
    '-filter_complex', filtres.join(';'),
    '-map', '[v]', '-map', '2:a', '-t', String(secondes),
    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', sortie,
  ]);
  return sortie;
}

function monter(sc, pistes, prise, dossier, options) {
  const { l, h, ips } = SORTIE_HD;
  const [debut, fin] = prise.coupe;
  const longueur = fin - debut;

  // a. image : on coupe l'attente du début, on passe en 1920×1080
  const ecran = path.join(dossier, 'ecran.mp4');
  ffmpeg([
    '-ss', debut.toFixed(3), '-i', prise.brut, '-t', longueur.toFixed(3),
    '-vf', `scale=${l}:${h}:flags=lanczos,fps=${ips},format=yuv420p`,
    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-an', ecran,
  ]);

  // b. son : chaque voix posée au début de son étape (+ musique douce si demandée)
  const entrees = [];
  const filtres = [];
  pistes.forEach((p, i) => {
    entrees.push('-i', p.fichier);
    const ms = Math.round(prise.etapes[i].debut * 1000);
    filtres.push(`[${i}:a]aresample=44100,aformat=channel_layouts=stereo,adelay=${ms}|${ms}[a${i}]`);
  });
  let mix = `${pistes.map((_, i) => `[a${i}]`).join('')}amix=inputs=${pistes.length}:normalize=0:duration=longest,apad,atrim=0:${longueur.toFixed(3)}`;
  if (sc.musique && !options.brouillon) {
    const musique = path.resolve(path.dirname(sc.fichier), sc.musique);
    if (!fs.existsSync(musique)) arreter(`Musique introuvable : ${musique}`);
    entrees.push('-stream_loop', '-1', '-i', musique);
    const n = pistes.length;
    filtres.push(`[${n}:a]aresample=44100,aformat=channel_layouts=stereo,volume=${sc.volume_musique ?? 0.07},atrim=0:${longueur.toFixed(3)},afade=t=out:st=${(longueur - 3).toFixed(3)}:d=3[mus]`);
    filtres.push(`${mix}[voix]`, `[voix][mus]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5[son]`);
  } else {
    filtres.push(`${mix},loudnorm=I=-16:TP=-1.5[son]`);
  }
  const son = path.join(dossier, 'son.m4a');
  ffmpeg([...entrees, '-filter_complex', filtres.join(';'), '-map', '[son]', '-ar', '44100', '-c:a', 'aac', '-b:a', '192k', son]);

  // c. sous-titres (sur la partie écran) et assemblage écran + son
  const sous = sc.etapes.flatMap((e, i) => decouperSousTitres(e.texte, prise.etapes[i].debut, pistes[i].duree));
  const srtEcran = path.join(dossier, 'ecran.srt');
  fs.writeFileSync(srtEcran, sous.map((s, i) => `${i + 1}\n${horodatage(s.debut)} --> ${horodatage(s.fin)}\n${s.texte}\n`).join('\n'));
  const corps = path.join(dossier, 'corps.mp4');
  const vf = [];
  if (!options.sansSousTitres) {
    const style = 'FontName=Inter,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H005B410B,BackColour=&H995B410B,BorderStyle=3,Outline=6,Shadow=0,MarginV=28';
    vf.push(`subtitles='${srtEcran.replace(/'/g, "\\'")}':force_style='${style}'`);
  }
  ffmpeg([
    '-i', ecran, '-i', son, ...(vf.length ? ['-vf', vf.join(',')] : []),
    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-shortest', corps,
  ]);

  // d. générique de début et de fin (sauf brouillon)
  const final = path.join(dossier, `${slug(sc.titre)}${options.brouillon ? '-brouillon' : ''}.mp4`);
  let decalage = 0;
  if (options.brouillon) {
    fs.copyFileSync(corps, final);
  } else {
    const dIntro = 4;
    const intro = carton(dossier, 'intro', [
      { texte: sc.titre, taille: 76, couleur: COULEURS.texte, gras: true, y: 'h*0.52' },
      ...(sc.sous_titre ? [{ texte: sc.sous_titre, taille: 44, couleur: COULEURS.accent, y: 'h*0.64' }] : []),
    ], dIntro);
    const outro = carton(dossier, 'fin', [
      { texte: sc.fin?.message || 'Merci de votre attention !', taille: 68, couleur: COULEURS.texte, gras: true, y: 'h*0.52' },
      { texte: sc.fin?.lien || 'taagg-gui.com', taille: 44, couleur: COULEURS.accent, y: 'h*0.64' },
    ], 4);
    ffmpeg([
      '-i', intro, '-i', corps, '-i', outro,
      '-filter_complex', '[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]',
      '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart',
      '-c:a', 'aac', '-b:a', '192k', final,
    ]);
    decalage = dIntro;
  }

  // e. fichiers pour la publication : sous-titres séparés (YouTube) et chapitres
  const srt = final.replace(/\.mp4$/, '.srt');
  fs.writeFileSync(srt, sous.map((s, i) => `${i + 1}\n${horodatage(s.debut + decalage)} --> ${horodatage(s.fin + decalage)}\n${s.texte}\n`).join('\n'));
  const chapitres = [];
  sc.etapes.forEach((e, i) => {
    if (e.chapitre) chapitres.push(`${mmss(i === 0 ? 0 : prise.etapes[i].debut + decalage)} ${e.chapitre}`);
  });
  if (chapitres.length) {
    fs.writeFileSync(final.replace(/\.mp4$/, '-chapitres.txt'), chapitres.join('\n') + '\n');
    // YouTube n'affiche les chapitres que s'il y en a 3 ou plus, de 10 s minimum chacun
    const debuts = chapitres.map((c) => c.split(' ')[0].split(':').reduce((m, s) => m * 60 + +s, 0));
    debuts.push(duree(final));
    const courts = chapitres.filter((_, i) => debuts[i + 1] - debuts[i] < 10);
    if (chapitres.length < 3 || courts.length) {
      console.log(`  ⚠ Chapitres refusés par YouTube : il en faut 3 ou plus, de 10 s minimum.${courts.length ? ' Trop courts : ' + courts.join(' / ') : ''}`);
    }
  }
  return final;
}

function mmss(s) {
  return `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
}

// ---------------------------------------------------------------- explorer une page

async function explorer(chemin) {
  const sc = { ecran: [1600, 900] };
  const navigateur = await chromium.launch();
  const etat = await connexion(navigateur, sc);
  const ctx = await navigateur.newContext({ viewport: { width: 1600, height: 900 }, locale: 'fr-FR', storageState: etat });
  const page = await ctx.newPage();
  await page.goto(urlOdoo(chemin));
  await page.waitForLoadState('networkidle').catch(() => {});
  await pause(1000);
  const infos = await page.evaluate(() => {
    const vu = (el) => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const net = (t) => (t || '').replace(/\s+/g, ' ').trim();
    return {
      titre: document.title,
      menus: [...document.querySelectorAll('.o_menu_sections .dropdown-toggle, .o_menu_sections > a, .o_app')].filter(vu).map((e) => net(e.textContent)),
      boutons: [...document.querySelectorAll('button, a.btn')].filter(vu).map((e) => net(e.textContent) || e.getAttribute('title') || e.className).filter(Boolean),
      champs: [...document.querySelectorAll('.o_field_widget[name]')].filter(vu).map((e) => {
        const nom = e.getAttribute('name');
        const label = document.querySelector(`label[for="${e.querySelector('input,select,textarea')?.id}"]`);
        return `${nom}${label ? ' — ' + net(label.textContent) : ''} (${[...e.classList].find((c) => c.startsWith('o_field_') && c !== 'o_field_widget') || ''})`;
      }),
      onglets: [...document.querySelectorAll('.o_notebook .nav-link')].filter(vu).map((e) => net(e.textContent)),
    };
  });
  const capture = path.join(ICI, 'sortie', 'explorer.png');
  fs.mkdirSync(path.dirname(capture), { recursive: true });
  await page.screenshot({ path: capture });
  await navigateur.close();
  console.log(`Page : ${infos.titre}  (${urlOdoo(chemin)})`);
  for (const [k, v] of Object.entries(infos)) if (Array.isArray(v) && v.length) console.log(`\n${k} :\n  - ${[...new Set(v)].join('\n  - ')}`);
  console.log(`\nCapture d'écran : ${capture}`);
}

// ---------------------------------------------------------------- chef d'orchestre

async function main() {
  lireEnv();
  const args = process.argv.slice(2);
  if (!args.length || args.includes('--aide')) {
    console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').slice(1, 18).join('\n').replace(/^\/\/ ?/gm, ''));
    return;
  }
  if (args[0] === 'explorer') return explorer(args[1] || '/odoo');

  const option = (nom) => args.includes(nom);
  const valeur = (nom) => (args.includes(nom) ? args[args.indexOf(nom) + 1] : undefined);
  const sc = chargerScenario(args[0]);
  const brouillon = option('--brouillon');
  const moteur = valeur('--voix') || (brouillon ? 'muet' : sc.voix?.moteur || 'elevenlabs');
  if (!['elevenlabs', 'openai', 'fichiers', 'muet'].includes(moteur)) arreter(`Voix inconnue : ${moteur}`);
  const dossier = path.join(ICI, 'sortie', sc.nom);
  fs.mkdirSync(dossier, { recursive: true });

  console.log(`▶ ${sc.titre} — ${sc.etapes.length} étapes, voix : ${moteur}${brouillon ? ' (brouillon)' : ''}`);
  console.log('1/3 Voix');
  const pistes = await preparerVoix(sc, moteur, dossier);
  if (option('--seulement-voix')) {
    console.log(`\n✓ Voix prêtes à écouter dans ${path.join(dossier, 'voix')}`);
    return;
  }

  const fJournal = path.join(dossier, 'prise.json');
  let prise;
  if (option('--remonter')) {
    if (!fs.existsSync(fJournal)) arreter('Aucune prise précédente : lancez d’abord sans --remonter.');
    prise = JSON.parse(fs.readFileSync(fJournal, 'utf8'));
    if (prise.etapes.length !== sc.etapes.length) arreter('Le nombre d’étapes a changé depuis la prise : il faut retourner.');
    console.log('2/3 Tournage : on réutilise la prise précédente');
  } else {
    console.log(`2/3 Tournage dans ${urlOdoo(sc.depart)}`);
    prise = await tourner(sc, pistes, dossier, option('--visible'));
    fs.writeFileSync(fJournal, JSON.stringify(prise, null, 2));
  }

  console.log('3/3 Montage');
  const final = monter(sc, pistes, prise, dossier, { brouillon, sansSousTitres: option('--sans-sous-titres') });
  console.log(`\n✓ Vidéo prête : ${final}  (${mmss(duree(final))})`);
}

main().catch((e) => arreter(e.stack || e.message));
