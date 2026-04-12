#!/usr/bin/env node
/**
 * APCA (WCAG 3 draft) contrast audit — ADVISORY ONLY.
 *
 * APCA is perceptually more accurate than WCAG 2's relative-luminance math,
 * but WCAG 3 is still a W3C Working Draft. Thresholds may shift. This
 * script is informational — it exits 0 regardless of pass/fail so a
 * draft-stage regression never blocks a release.
 *
 * When WCAG 3 becomes Recommendation, flip the exit code at the bottom.
 *
 * APCA Lc (Lightness contrast) thresholds for the Bronze/Silver conformance
 * targets in the current WCAG 3 draft (approximate):
 *   Lc 90+  Exemplary — any text
 *   Lc 75+  Body copy and small fluent text (equivalent guidance to WCAG 2 AA body)
 *   Lc 60+  Large text, non-critical content
 *   Lc 45+  Large bold / hero / headlines / interactive controls
 *   Lc 30+  Non-text contrast (UI controls, borders, icons)
 *   Lc <15  Invisible — fails by any standard
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { APCAcontrast, sRGBtoY } from 'apca-w3';

const here = dirname(fileURLToPath(import.meta.url));
const css = readFileSync(resolve(here, '../src/styles/global.css'), 'utf8');

// OKLCH → linear sRGB → sRGB 0-255 (same conversion as contrast-audit.mjs)
function oklchToSrgb255(L, C, h) {
  const r = (h * Math.PI) / 180;
  const a = C * Math.cos(r);
  const b = C * Math.sin(r);
  const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
  const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
  const s_ = L - 0.0894841775 * a - 1.291485548 * b;
  const lCube = l_ ** 3;
  const mCube = m_ ** 3;
  const sCube = s_ ** 3;
  const lin = [
    4.0767416621 * lCube - 3.3077115913 * mCube + 0.2309699292 * sCube,
    -1.2684380046 * lCube + 2.6097574011 * mCube - 0.3413193965 * sCube,
    -0.0041960863 * lCube - 0.7034186147 * mCube + 1.707614701 * sCube,
  ];
  // Linear → sRGB (gamma encode), clip, scale to 0-255
  return lin.map((v) => {
    const clipped = Math.max(0, Math.min(1, v));
    const gamma = clipped <= 0.0031308 ? 12.92 * clipped : 1.055 * clipped ** (1 / 2.4) - 0.055;
    return Math.round(Math.max(0, Math.min(1, gamma)) * 255);
  });
}

function parseTheme(blockRegex) {
  const m = css.match(blockRegex);
  if (!m) throw new Error(`Theme block not found: ${blockRegex}`);
  const out = {};
  for (const entry of m[0].matchAll(
    /--color-([\w-]+):\s*oklch\(([\d.]+)\s+([\d.]+)\s+([\d.]+)\)/g,
  )) {
    out[entry[1]] = [parseFloat(entry[2]), parseFloat(entry[3]), parseFloat(entry[4])];
  }
  return out;
}

const light = parseTheme(/:root\s*\{[^}]+\}/);
const dark = parseTheme(/:root\.dark\s*\{[^}]+\}/);

// text on bg (polarity matters for APCA — text is first, bg is second)
const pairs = [
  ['light', 'fg', 'bg', 75, 'body copy'],
  ['light', 'fg-muted', 'bg', 75, 'body-adjacent (fg-muted)'],
  ['light', 'muted', 'bg', 60, 'metadata text'],
  ['light', 'border-bold', 'bg', 30, 'interactive border (non-text)'],
  ['light', 'accent', 'bg', 60, 'accent links'],
  ['dark', 'fg', 'bg', 75, 'body copy'],
  ['dark', 'fg-muted', 'bg', 75, 'body-adjacent (fg-muted)'],
  ['dark', 'muted', 'bg', 60, 'metadata text'],
  ['dark', 'border-bold', 'bg', 30, 'interactive border (non-text)'],
  ['dark', 'accent', 'bg', 60, 'accent links'],
];

function apcaLc(theme, textKey, bgKey) {
  const src = theme === 'light' ? light : dark;
  const textRgb = oklchToSrgb255(...src[textKey]);
  const bgRgb = oklchToSrgb255(...src[bgKey]);
  const textY = sRGBtoY(textRgb);
  const bgY = sRGBtoY(bgRgb);
  return APCAcontrast(textY, bgY);
}

console.log('APCA (WCAG 3 draft) — ADVISORY contrast report\n');
let warnings = 0;
for (const [theme, text, bg, target, label] of pairs) {
  const Lc = apcaLc(theme, text, bg);
  const abs = Math.abs(Lc);
  const status = abs >= target ? 'OK    ' : 'REVIEW';
  if (abs < target) warnings++;
  const lcStr = Lc.toFixed(1).padStart(6);
  console.log(
    `  [${status}] ${theme.padEnd(5)} ${text.padEnd(12)} vs ${bg.padEnd(4)} Lc ${lcStr} (target ≥${target}) — ${label}`,
  );
}

if (warnings > 0) {
  console.log(`\n${warnings} pair(s) below APCA target. Advisory only — not blocking.`);
} else {
  console.log('\nAll pairs meet APCA draft targets.');
}
// Always exit 0 — advisory until WCAG 3 becomes Recommendation.
process.exit(0);
