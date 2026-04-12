#!/usr/bin/env node
/**
 * WCAG contrast audit for Remarque tokens.
 * Parses global.css, extracts OKLCH values, reports AA/AAA pass/fail.
 * Exit 1 if any required pair fails.
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const css = readFileSync(resolve(here, '../src/styles/global.css'), 'utf8');

function oklchToRgb(L, C, h) {
  const r = (h * Math.PI) / 180;
  const a = C * Math.cos(r);
  const b = C * Math.sin(r);
  const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
  const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
  const s_ = L - 0.0894841775 * a - 1.291485548 * b;
  const l = l_ ** 3, m = m_ ** 3, s = s_ ** 3;
  return [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
}
const lum = (rgb) => {
  const c = (v) => Math.max(0, Math.min(1, v));
  const [r, g, b] = rgb.map(c);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const contrast = (a, b) => {
  const [hi, lo] = [a, b].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};

// Parse OKLCH values from CSS (first occurrence per selector block)
function parseTheme(blockRegex) {
  const match = css.match(blockRegex);
  if (!match) throw new Error(`Theme block not found: ${blockRegex}`);
  const block = match[0];
  const out = {};
  for (const m of block.matchAll(/--color-([\w-]+):\s*oklch\(([\d.]+)\s+([\d.]+)\s+([\d.]+)\)/g)) {
    out[m[1]] = [parseFloat(m[2]), parseFloat(m[3]), parseFloat(m[4])];
  }
  return out;
}

const light = parseTheme(/:root\s*\{[^}]+\}/);
const dark = parseTheme(/:root\.dark\s*\{[^}]+\}/);

// Required pairs — [theme, fg, bg, minContrast, label]
const required = [
  ['light', 'fg', 'bg', 4.5, 'body text'],
  ['light', 'fg-muted', 'bg', 7.0, 'fg-muted (AAA body-adjacent)'],
  ['light', 'muted', 'bg', 4.5, 'muted text'],
  ['light', 'border-bold', 'bg', 3.0, 'interactive border (WCAG 1.4.11)'],
  ['light', 'accent', 'bg', 4.5, 'accent text'],
  ['dark', 'fg', 'bg', 4.5, 'body text'],
  ['dark', 'fg-muted', 'bg', 7.0, 'fg-muted (AAA body-adjacent)'],
  ['dark', 'muted', 'bg', 4.5, 'muted text'],
  ['dark', 'border-bold', 'bg', 3.0, 'interactive border (WCAG 1.4.11)'],
  ['dark', 'accent', 'bg', 4.5, 'accent text'],
];

let failed = 0;
console.log('Remarque Contrast Audit\n');
for (const [theme, fg, bg, min, label] of required) {
  const src = theme === 'light' ? light : dark;
  const c = contrast(lum(oklchToRgb(...src[bg])), lum(oklchToRgb(...src[fg])));
  const pass = c >= min;
  const status = pass ? 'PASS' : 'FAIL';
  if (!pass) failed++;
  console.log(
    `  [${status}] ${theme.padEnd(5)} ${fg.padEnd(12)} vs ${bg.padEnd(4)} ${c.toFixed(2)}:1 (min ${min}:1) — ${label}`,
  );
}

if (failed > 0) {
  console.error(`\n${failed} contrast check(s) failed.`);
  process.exit(1);
}
console.log('\nAll contrast requirements met.');
