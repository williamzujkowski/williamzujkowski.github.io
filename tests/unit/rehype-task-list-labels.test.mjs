import assert from 'node:assert/strict';
import test from 'node:test';
import config from '../../astro-site/astro.config.mjs';

// Exercise Astro's actual configured parser, transforms and sanitizer, so a
// disconnected plugin or stripped aria-label cannot make this suite green.
const renderer = await config.markdown.processor.createRenderer(config.markdown);

test('tight GFM tasks retain their states and gain visible-text names', async () => {
  const { code } = await renderer.render('- [ ] Review `kernel.lockdown` and [docs](https://example.com)\n- [x] Done');
  assert.match(code, /<input type="checkbox" disabled aria-label="Review kernel.lockdown and docs">/);
  assert.match(code, /<input type="checkbox" checked disabled aria-label="Done">/);
  assert.match(code, /<code>kernel.lockdown<\/code>/);
  assert.match(code, /<a href="https:\/\/example.com">docs<\/a>/);
});

test('loose and nested tasks receive their own names', async () => {
  const { code } = await renderer.render('- [ ] Parent task\n\n  More context.\n\n  - [x] Child task\n\n- [ ] Other task');
  assert.match(code, /aria-label="Parent task More context\."/);
  assert.match(code, /aria-label="Child task"/);
  assert.match(code, /aria-label="Other task"/);
  assert.doesNotMatch(code, /aria-label="Parent task[^\"]*Child/);
});

test('explicit checkbox names and non-task inputs are preserved', async () => {
  const { code } = await renderer.render('<ul><li class="task-list-item"><input type="checkbox" disabled aria-label="Authored name">Visible text</li></ul>\n\n<input type="checkbox" aria-label="Independent control">');
  assert.match(code, /aria-label="Authored name"/);
  assert.match(code, /aria-label="Independent control"/);
  assert.doesNotMatch(code, /aria-label="Visible text"/);
});
