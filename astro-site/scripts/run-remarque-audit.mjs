#!/usr/bin/env node
/**
 * Wrapper around `npx remarque-audit` that applies a hand-reviewed,
 * exact-match baseline of known upstream false positives (see
 * remarque-audit-baseline.json) so this site can adopt the upstream tool
 * as its CI gate today, without either (a) weakening any token value to
 * dodge a check, or (b) silently swallowing categories of failure the
 * tool exists to catch.
 *
 * Design:
 *   - CONTRAST and GAMUT failures (the --palette checks) are NEVER
 *     suppressible, full stop — the baseline file only ever contains
 *     source-scan entries, and this script hard-codes that rule
 *     independently of what the baseline file says, as defense in depth.
 *   - Source-scan failures (font-floor / hardcoded-color / oklch-literal)
 *     are only suppressed on an EXACT (file, line, category) match against
 *     the baseline. If a flagged line moves — even by one line, e.g. a
 *     comment gets added above it — the entry stops matching and the
 *     finding resurfaces as a real, blocking failure. This is intentional
 *     (fail closed): the baseline can only shrink safely by manual review,
 *     never silently expand its coverage.
 *   - Any failure NOT in the baseline is real and fails the build.
 *
 * See astro-site/DESIGN-DEVIATIONS.md #6 for why these specific baseline
 * entries exist (all are upstream tool false positives, not real defects,
 * verified by hand against the flagged CSS).
 */
import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const cwd = resolve(here, '..');
const baselinePath = resolve(here, 'remarque-audit-baseline.json');

const NEVER_SUPPRESSIBLE_CATEGORIES = [
  /^oklch\(\).*sRGB gamut/i, // handled separately below (gamut lines don't have a file:line prefix)
];

const baseline = JSON.parse(readFileSync(baselinePath, 'utf8'));
const baselineSet = new Set(
  baseline.entries.map((e) => `${e.file}:${e.line}:${e.category}`),
);

const args = ['--palette', 'src/styles/global.css', '--src', 'src/styles'];
const result = spawnSync('npx', ['remarque-audit', ...args], {
  cwd,
  encoding: 'utf8',
});

const output = `${result.stdout || ''}${result.stderr || ''}`;
const lines = output.split('\n');

let realFailures = 0;
let suppressed = 0;

for (const line of lines) {
  // Gamut failures: "  ✗ --name oklch(...) is outside sRGB gamut ..."
  // Contrast failures: "  ✗ tokenA/tokenB = X:1 < Y:1 (...)" or resolver errors
  // Both have NO "file:line" prefix (they come from the --palette parse,
  // not the --src walk) — that shape alone makes them structurally
  // ineligible for baseline suppression; the check below is an explicit,
  // redundant guarantee of that rule.
  const srcScanMatch = line.match(/^  ✗ (\S+):(\d+) (.+)/);

  if (!line.startsWith('  ✗')) {
    console.log(line);
    continue;
  }

  if (!srcScanMatch) {
    // A --palette (contrast/gamut) failure — never suppressible.
    realFailures++;
    console.log(`${line}   [BLOCKING — contrast/gamut checks are never suppressed]`);
    continue;
  }

  const [, file, lineNo, rest] = srcScanMatch;
  let category = null;
  if (/^oklch\(\) literal outside token files/.test(rest)) category = 'oklch() literal outside token files';
  else if (/^hardcoded hex\/rgb\/hsl color/.test(rest)) category = 'hardcoded hex/rgb/hsl color';
  else if (/^statically unverifiable font-size/.test(rest)) category = 'statically unverifiable font-size (clamp/%)';
  else if (/below the 13px floor/.test(rest)) category = '13px font floor';

  const key = `${file}:${lineNo}:${category}`;
  if (category !== '13px font floor' && baselineSet.has(key)) {
    suppressed++;
    console.log(`${line}   [suppressed — known upstream false positive, see remarque-audit-baseline.json]`);
  } else {
    realFailures++;
    console.log(line);
  }
}

console.log('');
console.log(
  `remarque-audit: ${suppressed} known false positive(s) suppressed, ${realFailures} real failure(s).`,
);

if (realFailures > 0) {
  console.error('\nremarque-audit FAILED (after baseline suppression).\n');
  process.exit(1);
}
console.log('\nremarque-audit passed (contrast + gamut clean; all source-scan findings are reviewed, baselined false positives) ✓\n');
