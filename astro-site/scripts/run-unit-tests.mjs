#!/usr/bin/env node
/**
 * Wrapper around `node --test` for the unit suite.
 *
 * Why this exists: `node --test` with a glob that matches nothing prints
 *
 *   # tests 0
 *   # pass 0
 *   # fail 0
 *
 * and exits 0. A renamed directory, a changed glob, or a moved test file
 * would therefore turn this gate green by removing its own subject —
 * exactly the failure mode run-remarque-audit.mjs had (issue #492), where
 * an empty result was indistinguishable from a clean one.
 *
 * So: run the suite, then require that it actually ran at least
 * MIN_TESTS of them. Raise the floor when tests are added; it is a ratchet,
 * not a target.
 */
import { spawnSync } from 'node:child_process';

const MIN_TESTS = 7;
const GLOB = '../tests/unit/**/*.test.mjs';

const result = spawnSync(process.execPath, ['--test', GLOB], {
  encoding: 'utf8',
  stdio: ['ignore', 'pipe', 'pipe'],
});

const output = `${result.stdout || ''}${result.stderr || ''}`;
process.stdout.write(output);

if (result.error) {
  console.error(`\nunit tests could not be spawned: ${result.error.message}\n`);
  process.exit(1);
}

const match = output.match(/^# tests (\d+)$/m);
const ran = match ? Number(match[1]) : 0;

if (ran < MIN_TESTS) {
  console.error(
    `\nunit tests: ran ${ran}, expected at least ${MIN_TESTS}. ` +
      'A suite that matches no files is not a passing suite — check the glob ' +
      `(${GLOB}) and that tests/unit/ still exists.\n`,
  );
  process.exit(1);
}

if (result.status !== 0) {
  process.exit(result.status ?? 1);
}

console.log(`\nunit tests: ${ran} ran, all passed (floor ${MIN_TESTS}) ✓\n`);
