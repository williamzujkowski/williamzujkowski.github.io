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

// There was a NEVER_SUPPRESSIBLE_CATEGORIES list here. Nothing read it.
// The rule it encoded is enforced structurally instead: a contrast/gamut
// failure comes from the --palette parse and carries no "file:line" prefix,
// so it never matches srcScanMatch and takes the never-suppressible branch
// below. Removed rather than wired up, because a list that looks like a
// hardening knob and changes nothing is worse than no list -- an editor
// adding a category to it would believe they had hardened the gate.

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

// The tool must be proven to have RUN before a zero-failure count means
// anything. Without this, a spawn failure (registry outage, renamed bin, a
// blocking `npx` prompt) produces empty output, which parses as zero failures
// and reports a pass — the gate fails open on exactly the cases where it is
// least able to tell you so.
if (result.error) {
  console.error(`\nremarque-audit could not be spawned: ${result.error.message}\n`);
  process.exit(1);
}

// Every check the tool performs prints a "  ✓" or "  ✗" line. Zero of them
// means it never got as far as auditing anything, whatever its exit code says.
const checksPerformed = lines.filter((l) => l.startsWith('  ✓') || l.startsWith('  ✗')).length;
if (checksPerformed === 0) {
  console.error(output);
  console.error(
    `\nremarque-audit performed 0 checks (exit ${result.status}) — treating as a FAILURE, ` +
      'not a pass. An empty result is not a clean result.\n',
  );
  process.exit(1);
}

let realFailures = 0;
let suppressed = 0;

for (const line of lines) {
  // Gamut failures: "  ✗ --name oklch(...) is outside sRGB gamut ..."
  // Contrast failures: "  ✗ tokenA/tokenB = X:1 < Y:1 (...)" or resolver errors
  // Both have NO "file:line" prefix (they come from the --palette parse,
  // not the --src walk) — that shape alone makes them structurally
  // ineligible for baseline suppression; the check below is an explicit,
  // redundant guarantee of that rule.
  const srcScanMatch = line.match(/^ {2}✗ (\S+):(\d+) (.+)/);

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

// A non-zero exit we cannot fully account for is still a failure — the tool
// is telling us something this parser does not understand.
//
// "Fully account for" is the load-bearing part, and it used to be missing.
// This was previously `if (result.status !== 0) exit(1)` unconditionally,
// which made the baseline UNUSABLE: the tool exits 1 whenever it finds
// anything, so a finding that was reviewed and baselined still failed the
// build. The baseline's own README describes adding an entry after hand
// review as the supported path — it never worked. Nobody noticed because
// the baseline has been empty since 2026-07-23, so the path was never
// taken (issue #642's shape: a mechanism whose success case is unreachable).
//
// The fix is not to trust the parse. It is to prove the parse is COMPLETE:
// the tool prints its own total as "audit FAILED — N problem(s)". If we
// parsed and classified exactly N findings, our accounting covers
// everything the tool objected to and a suppressed-to-zero run may pass.
// If the numbers disagree, the tool saw something we did not, and we fail
// closed exactly as before.
if (result.status !== 0) {
  const totalMatch = output.match(/audit FAILED\s*[—-]+\s*(\d+)\s*problem/i);
  const reportedTotal = totalMatch ? Number(totalMatch[1]) : null;
  const accountedFor = realFailures + suppressed;

  if (reportedTotal === null || reportedTotal !== accountedFor) {
    console.error(
      `\nremarque-audit exited ${result.status} with ` +
        `${reportedTotal ?? 'an unparseable number of'} problem(s), but this ` +
        `wrapper accounted for ${accountedFor}. Failing closed rather than ` +
        'trusting the parse.\n',
    );
    process.exit(1);
  }
}
console.log('\nremarque-audit passed (contrast + gamut clean; all source-scan findings are reviewed, baselined false positives) ✓\n');
