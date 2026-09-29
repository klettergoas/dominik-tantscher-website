// Kopiert Schriften und Logos nach public/ und erzeugt Favicons + Open-Graph-Bild.
// Aufruf: npm run assets (nur nötig, wenn sich Logo oder Schriften ändern).
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';
import opentype from 'opentype.js';

const root = path.resolve(import.meta.dirname, '..');
const handoff = path.resolve(root, '../design_handoff_website_dominik_tantscher/assets');
const pub = (...p) => path.join(root, 'public', ...p);
const BG = '#0A0C11';

// Schriften (nur Latin-Subset: deckt alle Zeichen der Website ab)
fs.mkdirSync(pub('fonts'), { recursive: true });
const fonts = [
  ['archivo', 'archivo-latin-400-normal.woff2'],
  ['archivo', 'archivo-latin-600-normal.woff2'],
  ['archivo', 'archivo-latin-700-normal.woff2'],
  ['space-mono', 'space-mono-latin-400-normal.woff2'],
  ['space-mono', 'space-mono-latin-700-normal.woff2'],
];
for (const [pkg, file] of fonts) {
  fs.copyFileSync(path.join(root, 'node_modules/@fontsource', pkg, 'files', file), pub('fonts', file));
}
for (const pkg of ['archivo', 'space-mono']) {
  fs.copyFileSync(path.join(root, 'node_modules/@fontsource', pkg, 'LICENSE'), pub('fonts', `${pkg}-LICENSE.txt`));
}

// Logos
fs.mkdirSync(pub('assets'), { recursive: true });
fs.copyFileSync(path.join(handoff, 'dt-lockup.svg'), pub('assets/dt-lockup.svg'));
fs.copyFileSync(path.join(handoff, 'dt-signet.svg'), pub('favicon.svg'));

const stripMeta = (svg) => svg.replace(/<metadata>[\s\S]*?<\/metadata>/, '').replace(/<title>[\s\S]*?<\/title>/, '');
const inner = (svg) => stripMeta(svg).replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '');
const signetInner = inner(fs.readFileSync(path.join(handoff, 'dt-signet.svg'), 'utf8'));
const lockupInner = inner(fs.readFileSync(path.join(handoff, 'dt-lockup.svg'), 'utf8'));

// Favicons: Signet auf #0A0C11, 16 % Innenabstand
const icon = (size) => {
  const pad = size * 0.16;
  const s = (size - 2 * pad) / 100;
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"><rect width="${size}" height="${size}" fill="${BG}"/><g transform="translate(${pad} ${pad}) scale(${s})">${signetInner}</g></svg>`);
};
await sharp(icon(32)).png().toFile(pub('favicon-32.png'));
await sharp(icon(180)).png().toFile(pub('apple-touch-icon.png'));
await sharp(icon(512)).png().toFile(pub('icon-512.png'));

// Open-Graph-Bild 1200 × 630: Lockup + Claim (Live-Text als Pfad, Archivo 400, #A2A4AC)
const woff = fs.readFileSync(path.join(root, 'node_modules/@fontsource/archivo/files/archivo-latin-400-normal.woff'));
const archivo = opentype.parse(woff.buffer.slice(woff.byteOffset, woff.byteOffset + woff.byteLength));
const claim = 'KI – maßgeschneidert auf Ihre Bedürfnisse.';
const lockH = 120;
const lockScale = lockH / 33;
const x = 96;
// Glyphen manuell setzen (opentype.js unterstützt Archivos ccmp-Lookups nicht)
const claimPath = (() => {
  const size = 40;
  const scale = size / archivo.unitsPerEm;
  let cx = x;
  let prev = null;
  const parts = [];
  for (const ch of claim) {
    const g = archivo.charToGlyph(ch);
    if (prev) cx += archivo.getKerningValue(prev, g) * scale;
    parts.push(g.getPath(cx, 420, size).toPathData(2));
    cx += g.advanceWidth * scale;
    prev = g;
  }
  return parts.join('');
})();
const grid = Array.from({ length: 13 }, (_, i) => {
  const cx = x + i * ((1200 - 2 * x + 24) / 12);
  return `<rect x="${cx.toFixed(1)}" y="0" width="1" height="630" fill="#15171E"/>`;
}).join('');
const og = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="${BG}"/>${grid}<g transform="translate(${x} 210) scale(${lockScale})">${lockupInner}</g><path d="${claimPath}" fill="#A2A4AC"/></svg>`;
await sharp(Buffer.from(og)).png().toFile(pub('og-image.png'));

console.log('Assets erzeugt.');
