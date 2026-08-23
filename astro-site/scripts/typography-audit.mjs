#!/usr/bin/env node
/**
 * USWDS typography-floor audit.
 * Scans src/ for hardcoded font-size values below the Remarque floors:
 *   - body text ≥ 17px (1.0625rem)
 *   - small/meta text ≥ 14px (0.875rem)
 *   - micro (timestamps) ≥ 13px (0.8125rem) — hard floor
 * Flags absolute font-size values (px/pt/rem) under the floor. Relative values
 * (em, %) are exempt because they scale with their parent's size — decorative
 * supers like ↗ indicators or chip counts (<1em) are legitimate.
 *
 * A negative-control audit (issue #511) got five evasions past the old
 * per-line `line.match(...)`, each of which has a shape that occurs in real
 * CSS:
 *   - only the FIRST font-size on a line was tested, so
 *     `.a{font-size:16px} .b{font-size:8px}` passed
 *   - the `font:` shorthand (`font: 10px/1.2 serif`) was not matched at all
 *   - `clamp(9px, 1vw, 12px)` was invisible; 11 real clamp() declarations
 *     ship, so the floor was unenforced for the whole fluid-type system
 *   - a rule line starting with `*` was treated as a comment continuation
 *   - units were matched case-sensitively, so `10PX` passed, and `pt` was
 *     not a recognised unit at all (6pt = 8px)
 */
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../src');

const FLOOR_PX = 13;
const exts = new Set(['.css', '.astro', '.svelte', '.ts', '.tsx', '.mdx']);
const violations = [];
let filesScanned = 0;

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
  switch (unit.toLowerCase()) {
    case 'px': return v;
    case 'rem': return v * 16;
    case 'pt': return (v * 96) / 72;
    default: return null; // em/%/vw exempt (relative to parent or viewport)
  }
}

/**
 * Blank out comments while preserving line numbers. Replaces the old
 * per-line guess, which mistook `* { … }` rule lines for comment
 * continuations — global.css has four of them.
 */
function stripComments(src) {
  let out = src.replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
  return out.replace(/(^|[^:])\/\/[^\n]*/g, (m, p1) => p1 + ' '.repeat(m.length - p1.length));
}

// `font-size: X` and the `font:` shorthand, whose size slot precedes an
// optional `/line-height`. Also reaches inside clamp()/min()/max(), where
// every absolute argument must clear the floor.
const SIZE_RE =
  /(?:font-size\s*:|font\s*:(?:[^;{}]*?\s)?)\s*[^;{}]*?(\d*\.?\d+)\s*(px|rem|pt)\b/gi;
const FUNC_ARG_RE = /(\d*\.?\d+)\s*(px|rem|pt)\b/gi;

function scan(file) {
  filesScanned += 1;
  const raw = readFileSync(file, 'utf8');
  const lines = stripComments(raw).split('\n');
  const rawLines = raw.split('\n');

  lines.forEach((line, i) => {
    // Every size declaration on the line, not just the first.
    for (const decl of line.matchAll(/(?:font-size|font)\s*:[^;{}]*/gi)) {
      const text = decl[0];
      // clamp()/min()/max(): check every absolute argument, since the
      // smallest one is what a narrow viewport actually renders.
      const args = text.match(/\b(?:clamp|min|max)\s*\([^)]*\)/i);
      const candidates = args
        ? [...args[0].matchAll(FUNC_ARG_RE)]
        : [...text.matchAll(SIZE_RE)].map((m) => [m[0], m[1], m[2]]);

      for (const c of candidates) {
        const px = toPx(c[1], c[2]);
        if (px === null || px >= FLOOR_PX) continue;
        violations.push({
          file: file.replace(root + '/', ''),
          line: i + 1,
          value: `${c[1]}${c[2]}`,
          px: px.toFixed(1),
          snippet: (rawLines[i] ?? '').trim(),
        });
        break;
      }
    }
  });
}

if (!existsSync(root)) {
  console.error(`USWDS Typography Floor Audit\n\n  Source root not found: ${root}`);
  process.exit(1);
}
walk(root);

console.log('USWDS Typography Floor Audit\n');
console.log(`  Floor: ${FLOOR_PX}px (Remarque --text-micro)\n`);

// An empty walk is not a clean pass — it means the scan never happened.
if (filesScanned === 0) {
  console.error(`  Scanned 0 files under ${root}. That is a broken audit, not a clean one.\n`);
  process.exit(1);
}

if (violations.length === 0) {
  console.log(`  No violations found. (${filesScanned} files scanned)`);
  process.exit(0);
}
for (const v of violations) {
  console.log(`  [FAIL] ${v.file}:${v.line} → ${v.value} (${v.px}px)`);
  console.log(`         ${v.snippet}`);
}
console.error(`\n${violations.length} typography violation(s).`);
process.exit(1);
