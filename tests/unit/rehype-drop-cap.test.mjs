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

test('a capitalised or numeric lead keeps the drop cap, even after a heading', async () => {
  for (const md of ['Years ago I worked on this.', '42 posts later.', '## Heading\n\nThe lead follows a heading.']) {
    const { code } = await renderer.render(md);
    assert.doesNotMatch(code, /no-drop-cap/, md);
  }
});
