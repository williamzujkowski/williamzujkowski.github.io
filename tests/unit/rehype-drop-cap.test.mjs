import assert from 'node:assert/strict';
import test from 'node:test';
import config from '../../astro-site/astro.config.mjs';

// Run Astro's configured pipeline, so a plugin dropped from the list or a
// class stripped by a later step fails here rather than passing in isolation.
const renderer = await config.markdown.processor.createRenderer(config.markdown);

test('a lead paragraph opening on a lowercase letter opts out of the drop cap', async () => {
  for (const md of ['npm provenance attests the pipeline.', '**gVisor** adds a kernel.', '"npm" is quoted.']) {
    const { code } = await renderer.render(`${md}\n\nSecond paragraph starts lowercase too.`);
    assert.match(code, /^<p class="no-drop-cap">/, md);
    assert.equal(code.match(/no-drop-cap/g).length, 1, `only the lead is marked: ${md}`);
  }
});

const LONG = 'Years ago I worked on this problem for most of a long and tiring winter, and I kept a notebook of everything that went wrong along the way, which I reread whenever I forget how far the work has come since then. It ends with a sentence that matters to nobody but me.';
const SHORT = 'Years ago I worked on this problem for a long winter, and I kept a notebook of everything that went wrong along the way.';

test('a long capitalised lead keeps the default three-line cap, even after a heading', async () => {
  assert.ok(LONG.length >= 190 && SHORT.length >= 100 && SHORT.length < 190);
  for (const md of [LONG, `## Heading\n\n${LONG}`]) {
    const { code } = await renderer.render(md);
    assert.doesNotMatch(code, /no-drop-cap|remarque-dropcap--short/, md);
  }
});

test('a lead of about two lines gets the two-line cap', async () => {
  const { code } = await renderer.render(`${SHORT}\n\n${LONG}`);
  assert.match(code, /^<p class="remarque-dropcap--short">/);
  assert.equal(code.match(/remarque-dropcap--short/g).length, 1, 'only the lead is marked');
});

test('the thresholds sit at 100 and 190 characters', async () => {
  const at = async (n) => (await renderer.render('A'.padEnd(n, 'b') + '.')).code;
  assert.match(await at(98), /no-drop-cap/); // 99 characters with the full stop
  assert.match(await at(99), /remarque-dropcap--short/); // 100
  assert.match(await at(188), /remarque-dropcap--short/); // 189
  assert.doesNotMatch(await at(189), /no-drop-cap|remarque-dropcap--short/); // 190
});

test('a one-line lead or a numeric opener gets no cap', async () => {
  for (const md of ['Years ago I worked on this.', `42 ${LONG}`, `2025 was the year ${SHORT}`]) {
    const { code } = await renderer.render(md);
    assert.match(code, /^<p class="no-drop-cap">/, md);
  }
});

test('margin-note text does not count toward the lead length', async () => {
  // A 120-character lead plus a long note: the note sits in the gutter, so the
  // lead still reads as two lines and gets the short cap.
  const lead = 'Years ago I worked on this problem for a long winter, and I kept a notebook of everything that went wrong.';
  const { code } = await renderer.render(`${lead}[^n]\n\n[^n]: ${'A very long footnote about nothing in particular. '.repeat(8)}`);
  assert.match(code, /^<p class="remarque-dropcap--short">/);
});
