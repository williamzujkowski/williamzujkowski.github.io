import assert from 'node:assert/strict';
import test from 'node:test';
import config from '../../astro-site/astro.config.mjs';

// Through Astro's configured pipeline, so dropping the plugin from the list
// (or moving it before rehype-raw, where the HTML is still a raw string)
// fails here.
const renderer = await config.markdown.processor.createRenderer(config.markdown);

test('raw-HTML captions get typographic apostrophes', async () => {
  const { code } = await renderer.render(`Text.\n\n<p class="hand-note">the meter doesn't care</p>\n\n<figure><figcaption>Mosca's test</figcaption></figure>`);
  assert.match(code, /doesn’t care/);
  assert.match(code, /Mosca’s test/);
});

test('code and call-shaped diagram text keep straight quotes', async () => {
  const { code } = await renderer.render(`<div class="seq-step">open("/etc/shadow", O_RDONLY)</div>\n\n<p><code>it's</code> stays</p>`);
  assert.match(code, /open\("\/etc\/shadow", O_RDONLY\)|open\(&#x22;\/etc\/shadow&#x22;, O_RDONLY\)/);
  assert.match(code, /<code>it's<\/code>|<code>it&#x27;s<\/code>/);
});
