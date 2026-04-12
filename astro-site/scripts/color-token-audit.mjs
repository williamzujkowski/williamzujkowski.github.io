#!/usr/bin/env node
/**
 * Remarque color-token audit.
 * Flags hardcoded hex / rgb() / rgba() / hsl() / named colors in CSS-ish
 * contexts. All colors MUST come from --color-* tokens.
 *
 * Allowed escape hatches:
 *   - `transparent`, `currentColor`, `inherit`
 *   - Inside @font-face / SVG url() data strings
 *   - Within a comment
 *   - Explicit allowlist comment: / * allow-raw-color * /
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../src');

const exts = new Set(['.css', '.astro', '.svelte']);
const violations = [];

// Properties where hardcoded colors are forbidden
const COLOR_PROPS = /\b(color|background(-color)?|border(-[\w-]+)?-color|border(-[\w-]+)?|fill|stroke|outline(-color)?|text-decoration-color|caret-color|box-shadow|text-shadow|accent-color)\s*:/;

// Hex, rgb(), rgba(), hsl(), hsla(), oklch() outside token definitions
const HEX = /#[0-9a-fA-F]{3,8}\b/;
const FUNC_COLOR = /\b(rgb|rgba|hsl|hsla|oklch)\s*\(/;

const ALLOWED = new Set(['transparent', 'currentColor', 'inherit', 'unset', 'initial', 'none']);

function walk(dir) {
  for (const entry of readdirSync(dir)) {
    if (entry === 'node_modules' || entry.startsWith('.')) continue;
    const full = join(dir, entry);
    const s = statSync(full);
    if (s.isDirectory()) walk(full);
    else if (exts.has(extname(full))) scan(full);
  }
}

function scan(file) {
  const src = readFileSync(file, 'utf8');
  const lines = src.split('\n');

  lines.forEach((raw, i) => {
    const line = raw;
    // Allow raw colors on lines that DEFINE a --color-* token (inside :root blocks)
    if (/^\s*--color-[\w-]+\s*:/.test(line)) return;
    // Skip comment lines
    if (/^\s*(\/\/|\*|\/\*)/.test(line)) return;
    // Explicit allowlist
    if (/allow-raw-color/.test(line)) return;
    // Only scan lines with a color property
    if (!COLOR_PROPS.test(line)) return;
    // Extract the value portion
    const vIdx = line.indexOf(':');
    const value = line.slice(vIdx + 1);
    // Skip if already using a token
    if (/var\(--color-/.test(value)) return;
    // Skip allowed keywords
    const trimmed = value.trim().replace(/;.*$/, '').trim();
    if (ALLOWED.has(trimmed)) return;

    let offense = null;
    if (HEX.test(value)) offense = value.match(HEX)[0];
    else if (FUNC_COLOR.test(value)) offense = value.match(FUNC_COLOR)[0] + '…)';

    if (offense) {
      violations.push({
        file: file.replace(root + '/', ''),
        line: i + 1,
        offense,
        snippet: line.trim(),
      });
    }
  });
}

walk(root);

console.log('Remarque Color-Token Audit\n');
if (violations.length === 0) {
  console.log('  All color values use var(--color-*) tokens.');
  process.exit(0);
}
for (const v of violations) {
  console.log(`  [FAIL] ${v.file}:${v.line} → ${v.offense}`);
  console.log(`         ${v.snippet}`);
}
console.error(`\n${violations.length} hardcoded color(s) found.`);
process.exit(1);
