#!/usr/bin/env node
// ── BUILD WEB BUNDLE ───────────────────────────────────────────────────────────
// Assembles ONLY the files the shipped game needs into dist/, which is Capacitor's
// webDir (it copies dist/ verbatim into the iOS/Android app bundle).
//
// Why a build step at all: the repo root also holds dev-only material (the scratch
// harnesses, source-res icons, code/, illustrated_test.html, .git). None of that
// belongs in an App Store binary — it inflates the download and hands a reviewer
// things that read as an unfinished dev build.
//
//   node build-web.mjs          -> dist/
//   npm run sync                -> dist/ + npx cap sync
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const DIST = path.join(ROOT, 'dist');

// Everything the game actually fetches at runtime (verified against index.html).
const FILES = ['index.html', 'manifest.json', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png'];
const DIRS  = ['vendor', 'models', 'audio', 'images', 'thumbs', 'levels'];

const copyDir = (src, dst) => {
  if (!fs.existsSync(src)) return 0;
  fs.mkdirSync(dst, { recursive: true });
  let n = 0;
  for (const e of fs.readdirSync(src, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue;
    const s = path.join(src, e.name), d = path.join(dst, e.name);
    n += e.isDirectory() ? copyDir(s, d) : (fs.copyFileSync(s, d), 1);
  }
  return n;
};

const dirSize = (p) => {
  if (!fs.existsSync(p)) return 0;
  let t = 0;
  for (const e of fs.readdirSync(p, { withFileTypes: true })) {
    const f = path.join(p, e.name);
    t += e.isDirectory() ? dirSize(f) : fs.statSync(f).size;
  }
  return t;
};

fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(DIST, { recursive: true });

let count = 0;
for (const f of FILES) {
  const s = path.join(ROOT, f);
  if (fs.existsSync(s)) { fs.copyFileSync(s, path.join(DIST, f)); count++; }
  else console.warn(`  ! missing (skipped): ${f}`);
}
for (const d of DIRS) {
  const n = copyDir(path.join(ROOT, d), path.join(DIST, d));
  if (n) console.log(`  ${d}/  ${n} files`);
  count += n;
}

// Guard: a native build must be fully self-contained. Any remaining CDN reference
// for a *code or font* asset means the app breaks (or renders wrong) offline and
// reads as "a website in a box" to App Review. Remote SERVICES (multiplayer,
// map data) are legitimately remote and are allowed through.
const html = fs.readFileSync(path.join(DIST, 'index.html'), 'utf8');
const ALLOW = ['robits-server', 'cdn.ably.com', 'overpass-api.de', 'fonts.googleapis.com/css2?family=PLACEHOLDER'];
const offenders = [...html.matchAll(/https?:\/\/[^"'\s)]+/g)]
  .map(m => m[0])
  .filter(u => !ALLOW.some(a => u.includes(a)))
  .filter(u => /\.(js|mjs|css|woff2?|ttf)(\?|$)/.test(u) || /fonts\.googleapis|fonts\.gstatic|cdnjs|jsdelivr|unpkg/.test(u));
if (offenders.length) {
  console.error('\n  ✗ BUILD FAILED — external asset references remain (must be vendored):');
  for (const u of [...new Set(offenders)]) console.error('      ' + u);
  process.exit(1);
}

const mb = (dirSize(DIST) / 1048576).toFixed(1);
console.log(`\n  ✓ dist/ ready — ${count} files, ${mb} MB`);
console.log('  ✓ no external code/font dependencies — bundle is self-contained\n');
