// Unit tests for citations:check (no network) and the collect parser.
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { checkCitations } from '../../astro-site/scripts/citations/check.mjs';
import { parseHtml, decode } from '../../astro-site/scripts/citations/collect.mjs';

const dir = mkdtempSync(path.join(tmpdir(), 'cite-'));
const post = (slug, body) => writeFileSync(path.join(dir, `${slug}.md`), `---\ntitle: T\n---\n\n${body}\n`);
post('a', 'See [docs](https://docs.example.com/x) and [gone](https://dead.example/y), [mine](https://williamzujkowski.github.io/posts/z), [src](https://github.com/o/r/blob/main/f.js), [rel](/about), and `[code](https://code.example/q)`.');
post('b', 'Again [docs](https://www.docs.example.com/x/?utm_source=z) and [issue](https://github.com/o/r/issues/1).\n\n## Sources\n\n- [S](https://s.example/1)');
post('c', 'Text [docs](https://docs.example.com/x).');

test('check: lists eligible links without an entry, skips ineligible ones', async () => {
  const r = await checkCitations({ slugs: ['a'], citations: { 'docs.example.com/x': { title: 'X' } }, postsDir: dir });
  assert.deepEqual(r.missing.map((m) => m.key), ['dead.example/y']);
});

test('check: a post with a Sources list is skipped', async () => {
  const r = await checkCitations({ slugs: ['b'], citations: {}, postsDir: dir });
  assert.deepEqual(r.missing, []);
  assert.deepEqual(r.skipped, ['b']);
});

test('check: entries nobody links are reported only when every post was scanned', async () => {
  const citations = { 'docs.example.com/x': { title: 'X' }, 'dead.example/y': { title: 'Y' }, 'stale.example/z': { title: 'Z' } };
  const some = await checkCitations({ slugs: ['a'], citations, postsDir: dir });
  assert.deepEqual(some.unused, []);
  const all = await checkCitations({ slugs: ['a', 'b', 'c'], citations, postsDir: dir, all: true });
  assert.deepEqual(all.unused, ['stale.example/z']);
  assert.deepEqual(all.missing, []);
});

test('collect: parseHtml prefers citation_title, strips the site suffix, reads the date', () => {
  const html = '<head><title>Ignored</title><meta property="og:site_name" content="Example"><meta property="og:title" content="Big &amp; Bold | Example"><meta property="article:published_time" content="2024-05-06T10:00:00Z"></head><h1>H</h1>';
  assert.deepEqual(parseHtml(html, 'e.example'), { title: 'Big & Bold', publisher: 'Example', date: '2024-05-06', notes: [] });
  const bare = parseHtml('<title>Just a title</title>', 'e.example');
  assert.equal(bare.publisher, 'e.example');
  assert.equal(bare.date, null);
  assert.equal(bare.notes.length, 1);
  assert.equal(decode('a &#8212; b&nbsp;&amp;c'), 'a — b &c');
});
