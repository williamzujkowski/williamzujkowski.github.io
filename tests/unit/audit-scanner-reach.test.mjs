/**
 * The design audits must see the constructs they claim to forbid.
 *
 * Each case here is a mutation that the scanner ACCEPTED before its fix.
 * These are pattern-reach tests, not end-to-end runs: they assert the
 * regexes the scanners key on, which is where all three holes were.
 *
 * Paired negatives are deliberate. A regex that matches everything would
 * satisfy the positive half of each test, so every "must be caught" case
 * has a "must not be caught" sibling.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const scripts = resolve(here, '../../astro-site/scripts');

/** Pull a named regex literal out of a scanner without executing it. */
function extractRegex(file, name) {
  const src = readFileSync(resolve(scripts, file), 'utf8');
  // `const NAME =` optionally on its own line, then a /.../flags literal.
  const m = src.match(
    new RegExp(`const\\s+${name}\\s*=\\s*\\n?\\s*(/.*/[gimsuy]*);`)
  );
  assert.ok(m, `${name} not found in ${file} — did it get renamed?`);
  const body = m[1];
  const lastSlash = body.lastIndexOf('/');
  return new RegExp(body.slice(1, lastSlash), body.slice(lastSlash + 1));
}

test('color-token-audit: background-image is inside COLOR_PROPS', () => {
  const COLOR_PROPS = extractRegex('color-token-audit.mjs', 'COLOR_PROPS');
  // The mutation that used to pass: a gradient of two literal hexes.
  assert.ok(
    COLOR_PROPS.test('  background-image: linear-gradient(#ff0000, #00ff00);'),
    'background-image must be checked for hardcoded colors'
  );
});

test('color-token-audit: COLOR_PROPS still matches the properties it always did', () => {
  const COLOR_PROPS = extractRegex('color-token-audit.mjs', 'COLOR_PROPS');
  for (const decl of [
    '  color: #fff;',
    '  background: #fff;',
    '  background-color: #fff;',
    '  border-color: #fff;',
    '  box-shadow: 0 0 2px #fff;',
    '  fill: #fff;',
  ]) {
    assert.ok(COLOR_PROPS.test(decl), `${decl.trim()} must still be checked`);
  }
});

test('color-token-audit: COLOR_PROPS is not a catch-all', () => {
  const COLOR_PROPS = extractRegex('color-token-audit.mjs', 'COLOR_PROPS');
  // Negative control: if this matched, the positive tests above would pass
  // for the wrong reason.
  for (const decl of ['  margin: 0;', '  display: flex;', '  z-index: 3;']) {
    assert.ok(!COLOR_PROPS.test(decl), `${decl.trim()} must not be treated as a color`);
  }
});

test('accent-font-audit: .hand-note-wrapper does not open the allowlist', () => {
  const src = readFileSync(resolve(scripts, 'accent-font-audit.mjs'), 'utf8');
  const m = src.match(/\/\\\.hand-note[^/]*\/(?=\.test)/);
  assert.ok(m, 'the .hand-note selector guard was not found');
  const body = m[0].slice(1, -1);
  const re = new RegExp(body);

  // The mutation that used to pass: a hyphenated sibling class smuggling
  // `body` and `.post-content` into the accent-font allowlist.
  assert.ok(
    !re.test('.hand-note-wrapper p, body, .post-content {'),
    '.hand-note-wrapper must not match the .hand-note allowlist'
  );
  assert.ok(!re.test('.hand-note-inner {'), 'hyphenated siblings must not match');
  assert.ok(!re.test('.hand-notes {'), 'suffixed siblings must not match');

  // Paired positive: the real selector must still be allowed, or the fix
  // would have broken the feature rather than the hole.
  assert.ok(re.test('.hand-note {'), '.hand-note itself must still match');
  assert.ok(re.test('.hand-note, .other {'), 'comma-joined selectors must match');
  assert.ok(re.test('.post-content .hand-note em {'), 'descendant form must match');
});

test('run-remarque-audit: no unread never-suppressible list', () => {
  const src = readFileSync(resolve(scripts, 'run-remarque-audit.mjs'), 'utf8');
  // Matches a DECLARATION, not a mention: the removal comment names the
  // constant on purpose, and a test that forbade the words would forbid
  // explaining why they are gone.
  assert.doesNotMatch(
    src,
    /(const|let|var)\s+NEVER_SUPPRESSIBLE_CATEGORIES/,
    'the list was read by nothing; the rule is enforced by the missing ' +
      'file:line prefix instead. Re-adding it needs wiring, not a constant.'
  );
  // The enforcement it stood in for must actually be present.
  assert.match(
    src,
    /never suppressed/i,
    'the structural never-suppressible branch must still exist'
  );
});
