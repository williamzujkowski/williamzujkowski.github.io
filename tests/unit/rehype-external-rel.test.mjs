import assert from 'node:assert/strict';
import test from 'node:test';
import config from '../../astro-site/astro.config.mjs';

// Astro's real pipeline, so a disconnected plugin or a sanitizer that strips
// `rel` cannot leave this green.
const renderer = await config.markdown.processor.createRenderer(config.markdown);

test('off-site links get rel="external" and own-site links do not', async () => {
  const { code } = await renderer.render(
    '[out](https://example.com/a) [own](https://williamzujkowski.github.io/posts/x/) [local](/tags/ai/) [anchor](#top)',
  );
  assert.match(code, /<a href="https:\/\/example\.com\/a" rel="external">out<\/a>/);
  assert.doesNotMatch(code, /williamzujkowski\.github\.io[^>]*rel=/);
  assert.doesNotMatch(code, /href="\/tags\/ai\/"[^>]*rel=/);
  assert.doesNotMatch(code, /href="#top"[^>]*rel=/);
});

test('existing rel tokens are kept and external is added once', async () => {
  const { code } = await renderer.render('<a href="https://example.com" rel="noopener external">x</a>');
  assert.match(code, /rel="noopener external"/);
});
