import assert from 'node:assert/strict';
import test from 'node:test';
import config from '../../astro-site/astro.config.mjs';

// Exercise the configuration Astro actually uses, including plugin order and
// the sanitizer. Repeating the plugin list or schema here would miss drift.
const renderer = await config.markdown.processor.createRenderer(config.markdown);

test('authored diagrams retain accessibility, SVG geometry and stable anchors', async () => {
  const { code } = await renderer.render(`
<div class="flow" role="group" aria-labelledby="diagram-heading" data-stage="review">
<h2 id="diagram-heading">Review boundary</h2>
<svg viewBox="0 0 100 60" role="img" aria-labelledby="drawing-title drawing-description">
<title id="drawing-title">Restricted path</title>
<desc id="drawing-description">A single permitted connection.</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"><path d="M 0 0 L 10 5 L 0 10" fill="currentColor"></path></marker></defs>
<path id="connection" d="M 10 30 L 90 30" stroke="currentColor" marker-end="url(#arrow)"></path>
<use href="#connection"></use>
</svg>
<a href="#diagram-heading">Return to diagram</a>
</div>
`);
  assert.match(code, /<div class="flow" role="group" aria-labelledby="diagram-heading" data-stage="review">/);
  assert.match(code, /<h2 id="diagram-heading">Review boundary<\/h2>/);
  assert.match(code, /<svg viewBox="0 0 100 60" role="img" aria-labelledby="drawing-title drawing-description">/);
  assert.match(code, /<title id="drawing-title">Restricted path<\/title>/);
  assert.match(code, /<desc id="drawing-description">A single permitted connection\.<\/desc>/);
  assert.match(code, /<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5">/);
  assert.match(code, /<path id="connection" d="M 10 30 L 90 30" stroke="currentColor" marker-end="url\(#arrow\)">/);
  assert.match(code, /<use href="#connection">/);
  assert.match(code, /<a href="#diagram-heading">Return to diagram<\/a>/);
  assert.doesNotMatch(code, /id="user-content-diagram-heading"/);
});

test('configured transforms preserve tables, sidenotes, punctuation and titled syntax highlighting', async () => {
  const { code } = await renderer.render(`
"Measure twice," she said -- then checked...[^evidence]

| Control | State |
| --- | --- |
| Database role | Restricted |

\`\`\`python title="agent.py"
print("reviewed")
\`\`\`

[^evidence]: The note remains next to its reference.
`);
  assert.match(code, /“Measure twice,” she said/);
  assert.match(code, /she said – then checked/);
  assert.match(code, /checked…/);
  assert.match(code, /<div class="scroll-wrap" tabindex="0">\s*<table>/);
  assert.match(code, /<td>Database role<\/td>/);
  const noteLink = code.match(/<a[^>]*class="remarque-sidenote-ref"[^>]*>/)?.[0];
  assert.ok(noteLink, 'the configured sidenote transform must name the reference');
  assert.match(noteLink, /aria-label="Note 1"/);
  const target = noteLink.match(/href="#([^"]+)"/)?.[1];
  assert.ok(target);
  assert.ok(noteLink.includes(`aria-describedby="${target}"`));
  assert.ok(code.includes(`id="${target}"`));
  assert.match(code, /<aside[^>]*class="remarque-sidenote"[^>]*role="note"/);
  assert.ok(code.indexOf('The note remains next to its reference.') < code.indexOf('<table>'));
  assert.doesNotMatch(code, /<section[^>]*data-footnotes/);
  assert.match(code, /<pre[^>]*class="astro-code remarque"[^>]*data-title="agent\.py"/);
  assert.match(code, /var\(--color-syntax-/);
});

test('the configured sanitizer rejects scripts, event handlers and unsafe URL protocols', async () => {
  const { code } = await renderer.render(`
<div>
<script>untrustedScriptPayload()</script>
<a href="javascript:untrustedHref()" onclick="untrustedClick()">Unsafe link</a>
<a href="https://example.com/research" onmouseover="untrustedHover()">Research</a>
<img src="data:text/html,untrustedDataPayload" onerror="untrustedError()" alt="Unsafe image">
<img src="https://example.com/chart.png" onload="untrustedLoad()" alt="Chart">
<svg viewBox="0 0 10 10" onload="untrustedSvgLoad()">
<script>untrustedSvgScript()</script>
<use xlink:href="javascript:untrustedXlink()"></use>
<image href="javascript:untrustedSvgHref()" src="javascript:untrustedSvgSrc()"></image>
</svg>
</div>
`);
  assert.doesNotMatch(code, /<script\b/i);
  assert.doesNotMatch(code, /\son\w+=/i);
  assert.doesNotMatch(code, /untrusted|javascript:|data:text\/html/i);
  assert.match(code, /<a>Unsafe link<\/a>/);
  assert.match(code, /<a href="https:\/\/example\.com\/research">Research<\/a>/);
  assert.match(code, /<img src="https:\/\/example\.com\/chart\.png" alt="Chart">/);
  assert.match(code, /<svg viewBox="0 0 10 10">/);
  assert.match(code, /<use><\/use>/);
  assert.match(code, /<image><\/image>/);
});
