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
import { oklchToSrgb255 } from './lib/color.mjs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { APCAcontrast, sRGBtoY } from 'apca-w3';

const here = dirname(fileURLToPath(import.meta.url));
const css = readFileSync(resolve(here, '../src/styles/global.css'), 'utf8');

// OKLCH → linear sRGB → sRGB 0-255 (same conversion remarque-audit's WCAG
// contrast check uses — see scripts/run-remarque-audit.mjs — kept local
// here because APCA needs sRGB 0-255 ints, not the 0-1 floats WCAG uses)

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

// This audit's FINDINGS are advisory (WCAG 3 is still a draft), but failing to
// resolve any tokens means it measured nothing — and a report over zero tokens
// must not read like a clean one (issue #511). Previously that surfaced as a
// raw TypeError from spreading `undefined`.
for (const [name, theme] of [['light', light], ['dark', dark]]) {
  if (Object.keys(theme).length === 0) {
    console.error(
      `APCA audit: parsed 0 --color-* tokens for the ${name} theme from global.css.\n` +
      'That is a broken run, not a clean one.',
    );
    process.exit(1);
  }
}

// text on bg (polarity matters for APCA — text is first, bg is second)
const pairs = [
  ['light', 'fg', 'bg', 75, 'body copy'],
  ['light', 'fg-muted', 'bg', 75, 'body-adjacent (fg-muted)'],
  ['light', 'muted', 'bg', 60, 'metadata text'],
  ['light', 'border-bold', 'bg', 30, 'interactive border (non-text)'],
  ['light', 'accent', 'bg', 60, 'accent links'],
  ['light', 'accent-hover', 'bg', 55, 'accent hover (#323)'],
  ['dark', 'fg', 'bg', 75, 'body copy'],
  ['dark', 'fg-muted', 'bg', 75, 'body-adjacent (fg-muted)'],
  ['dark', 'muted', 'bg', 60, 'metadata text'],
  ['dark', 'border-bold', 'bg', 30, 'interactive border (non-text)'],
  ['dark', 'accent', 'bg', 60, 'accent links'],
  ['dark', 'accent-hover', 'bg', 55, 'accent hover (#323)'],
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
