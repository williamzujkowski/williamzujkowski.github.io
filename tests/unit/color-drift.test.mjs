// Pins the colour maths that cannot share a module (issue #506).
//
// grain-contrast-audit.mjs runs one luminance function inside page.evaluate,
// where the module scope is unavailable, so a second copy of the WCAG
// transfer function has to exist there. Rather than eval-inject a string into
// the page, the two are pinned here: this test extracts the in-page source
// from the script and checks it agrees numerically with lib/color.mjs across
// the whole 0-255 range. If someone edits one and not the other, this fails.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const { relLum255, TRANSFER_FN_SOURCE } = await import(
  resolve(root, 'astro-site/scripts/lib/color.mjs')
);

const grainSrc = readFileSync(
  resolve(root, 'astro-site/scripts/grain-contrast-audit.mjs'),
  'utf8',
);

test('the in-page luminance function still exists (guards against a silent rename)', () => {
  assert.match(grainSrc, /function relLum\(r, g, b\)/);
});

test('the in-page transfer function matches lib/color.mjs across 0-255', () => {
  const m = grainSrc.match(/function relLum\(r, g, b\) \{[\s\S]*?\n {6}\}/);
  assert.ok(m, 'could not extract the in-page relLum from grain-contrast-audit.mjs');

  // eslint-disable-next-line no-new-func
  const inPage = new Function(`${m[0]}; return relLum;`)();

  // Fine grid, not integers. An earlier version of this test stepped v by 1
  // over 0-255 and MISSED a planted mutation that moved the branch threshold
  // from 0.03928 to 0.04: no integer channel value maps into that gap
  // (10/255 = 0.0392, 11/255 = 0.0431). The threshold region is where a
  // transfer-function edit is most likely to land, so sample it densely.
  const samples = [];
  for (let v = 0; v <= 255; v += 1) samples.push(v);
  for (let v = 9; v <= 12; v += 0.005) samples.push(v);   // spans the 0.03928 knee
  for (let v = 0; v <= 255; v += 0.37) samples.push(v);   // non-integer sweep

  for (const v of samples) {
    const mine = relLum255([v, v, v]);
    const theirs = inPage(v, v, v);
    assert.ok(
      Math.abs(mine - theirs) < 1e-12,
      `luminance disagrees at ${v}: module ${mine} vs in-page ${theirs}`,
    );
  }
});

test('TRANSFER_FN_SOURCE is the same formula the module uses', () => {
  // eslint-disable-next-line no-eval
  const fn = eval(TRANSFER_FN_SOURCE);
  for (const v of [0, 0.03928, 0.05, 0.5, 1]) {
    const viaSource = fn(v);
    const expected = v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
    assert.ok(Math.abs(viaSource - expected) < 1e-15, `mismatch at ${v}`);
  }
});
