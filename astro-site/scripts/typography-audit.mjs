#!/usr/bin/env node
/**
 * USWDS typography-floor audit.
 * Scans src/ for hardcoded font-size values below the Remarque floors:
 *   - body text ≥ 17px (1.0625rem)
 *   - small/meta text ≥ 14px (0.875rem)
 *   - micro (timestamps) ≥ 13px (0.8125rem) — hard floor
 * Flags absolute font-size values (px/rem) under the floor. Relative values
 * (em, %) are exempt because they scale with their parent's size — decorative
 * supers like ↗ indicators or chip counts (<1em) are legitimate.
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../src');

const FLOOR_PX = 13;
const exts = new Set(['.css', '.astro', '.svelte', '.ts', '.tsx', '.mdx']);
const violations = [];

function walk(dir) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const s = statSync(full);
    if (s.isDirectory()) walk(full);
    else if (exts.has(extname(full))) scan(full);
  }
}

function toPx(value, unit) {
  const v = parseFloat(value);
  if (unit === 'px') return v;
  if (unit === 'rem') return v * 16;
  return null; // em/% exempt (relative to parent)
}

function scan(file) {
  const src = readFileSync(file, 'utf8');
  const lines = src.split('\n');
  lines.forEach((line, i) => {
    // skip comments
    if (/^\s*(\/\/|\*|\/\*)/.test(line)) return;
    // match font-size: N(px|rem|em)
    const m = line.match(/font-size:\s*([\d.]+)(px|rem)\b/);
    if (!m) return;
    const px = toPx(m[1], m[2]);
    if (px === null) return;
    if (px < FLOOR_PX) {
      violations.push({
        file: file.replace(root + '/', ''),
        line: i + 1,
        value: `${m[1]}${m[2]}`,
        px: px.toFixed(1),
        snippet: line.trim(),
      });
    }
  });
}

walk(root);

console.log('USWDS Typography Floor Audit\n');
console.log(`  Floor: ${FLOOR_PX}px (Remarque --text-micro)\n`);
if (violations.length === 0) {
  console.log('  No violations found.');
  process.exit(0);
}
for (const v of violations) {
  console.log(`  [FAIL] ${v.file}:${v.line} → ${v.value} (${v.px}px)`);
  console.log(`         ${v.snippet}`);
}
console.error(`\n${violations.length} typography violation(s).`);
process.exit(1);
