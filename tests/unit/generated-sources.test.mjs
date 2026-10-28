// Unit tests for the generated Sources list (astro-site/src/lib/generatedSources.mjs):
// the shared function, the page block and the feed output.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import config from '../../astro-site/astro.config.mjs';
import {
  generatedSourceItems,
  generatedSourcesBlock,
  sourcesListNodes,
  transformNotesAndSources,
  GENERATED_SOURCES_CLASS,
} from '../../astro-site/src/lib/generatedSources.mjs';
import { transformSourceMarginalia } from '../../astro-site/src/lib/rehype-source-marginalia.mjs';
import { renderPostForFeed, renderGeneratedSources } from '../../astro-site/src/lib/feedContent.ts';

const text = (value) => ({ type: 'text', value });
const el = (tagName, properties, children) => ({ type: 'element', tagName, properties: properties || {}, children: children || [] });
const link = (href, label) => el('a', { href }, [text(label)]);
const p = (...inline) => el('p', {}, inline);
const root = (...children) => ({ type: 'root', children });

const CITES = {
  'a.example/one': { title: 'First source', publisher: 'Alpha Press', date: '2024-05-06' },
  'b.example/two': { title: 'Second source', publisher: 'Beta', date: null },
  'c.example/three': { title: 'Third source about caches', publisher: 'Caches', date: '2021' }, // publisher elided
  'd.example/paper.pdf': { title: 'One Paper', publisher: 'D', date: '2020' },
  'd.example/paper': { title: 'one paper', publisher: 'D', date: '2020' }, // same title: one citation
  'e.example/echo': { title: 'Echo', publisher: 'E', date: null }, // note dropped as an echo
  'github.com/o/r/blob/main/f.js': { title: 'f.js', publisher: 'GitHub', date: null },
  'github.com/o/r/issues/7': { title: 'Cache eviction regression', publisher: 'o/r #7', date: '2026-01-02' },
  'williamzujkowski.github.io/posts/x': { title: 'Own post', publisher: 'Me', date: null },
};
const items = (tree) => generatedSourceItems(tree, CITES);
const lines = (tree) => items(tree).map((i) => [i.title, i.publisher, i.year].filter(Boolean).join(' | '));
const textOf = (n) => (n.type === 'text' ? n.value : (n.children || []).map(textOf).join(''));

test('items come in first-link order, one per URL and per citation title', () => {
  const tree = root(
    p(text('Start with '), link('https://b.example/two', 'two'), text(' then '), link('https://a.example/one', 'one'), text('.')),
    p(link('https://a.example/one/', 'one again'), text(' and '), link('https://d.example/paper.pdf', 'pdf'), text(' and '), link('https://d.example/paper', 'page'), text('.'))
  );
  assert.deepEqual(lines(tree), ['Second source | Beta', 'First source | Alpha Press | 2024', 'One Paper | D | 2020']);
  assert.equal(items(tree)[1].href, 'https://a.example/one');
});

test('items omit missing parts and elide a publisher already in the title', () => {
  const tree = root(p(link('https://c.example/three', 'c'), text(' and '), link('https://b.example/two', 'b'), text('.')));
  assert.deepEqual(lines(tree), ['Third source about caches | 2021', 'Second source | Beta']);
});

test('eligibility matches the margin notes: own domain, relative, non-http, GitHub files and unknown URLs are left out', () => {
  const tree = root(
    p(link('https://williamzujkowski.github.io/posts/x', 'mine'), text(' one. '), link('/posts/x', 'rel'), text(' two. '), link('mailto:a@b.example', 'mail'), text(' three.')),
    p(link('https://github.com/o/r/blob/main/f.js', 'file'), text(' four. '), link('https://nowhere.example/z', 'unknown'), text(' five. '), link('https://github.com/o/r/issues/7', 'issue'), text(' six.'))
  );
  assert.deepEqual(lines(tree), ['Cache eviction regression | o/r #7 | 2026']);
});

test('only body prose is read: links in headings, code, tables and raw blocks are skipped', () => {
  const tree = root(
    el('h3', {}, [link('https://a.example/one', 'in a heading')]),
    el('table', {}, [el('tr', {}, [el('td', {}, [link('https://b.example/two', 'in a table')])])]),
    p(el('code', {}, [text('https://c.example/three')]), text(' only code.'))
  );
  assert.deepEqual(lines(tree), []);
});

test('an entry whose margin note is dropped as an echo is still listed', () => {
  const tree = root(p(link('https://e.example/echo', 'Echo'), text(' is a thing. '), link('https://a.example/one', 'one'), text(' too.')));
  const probe = structuredClone(tree);
  transformSourceMarginalia(probe, { citations: CITES });
  const noteTexts = [];
  const walk = (n) => {
    if (n.properties?.className?.includes?.('remarque-sidenote')) noteTexts.push(textOf(n));
    (n.children || []).forEach(walk);
  };
  walk(probe);
  assert.deepEqual(noteTexts, ['First source · Alpha Press · 2024'], 'the echo note is suppressed');
  assert.deepEqual(lines(tree), ['Echo | E', 'First source | Alpha Press | 2024']);
});

test('a hand-written Sources h2 means no generated list', () => {
  const tree = root(
    p(link('https://a.example/one', 'one'), text(' says so.')),
    el('h2', { id: 'sources' }, [text('Sources')]),
    el('ul', {}, [el('li', {}, [link('https://a.example/one', 'One')])])
  );
  assert.deepEqual(items(tree), []);
});

test('footnotes mean no generated list (page footnote section, sidenote refs and the feed section)', () => {
  const body = p(link('https://a.example/one', 'one'), text(' says so.'));
  assert.deepEqual(items(root(body, el('section', { dataFootnotes: '' }, []))), []);
  assert.deepEqual(items(root(body, el('section', { className: ['footnotes'] }, []))), []);
  assert.deepEqual(items(root(p(link('https://a.example/one', 'one'), text(' says so.'), el('a', { href: '#n', className: ['remarque-sidenote-ref'] }, [])))), []);
});

test('no citation data, or no eligible link, gives no list', () => {
  assert.deepEqual(generatedSourceItems(root(p(link('https://a.example/one', 'one'), text('.'))), undefined), []);
  assert.deepEqual(items(root(p(text('No links.')))), []);
  const t = root(p(text('No links.')));
  transformNotesAndSources(t, { citations: CITES });
  assert.equal(t.children.length, 1);
});

test('the list is an h2 and a ul of Title · Publisher · Year, marked for tooling', () => {
  const list = sourcesListNodes(items(root(p(link('https://a.example/one', 'one'), text('.')))));
  assert.equal(list[0].tagName, 'h2');
  assert.equal(textOf(list[0]), 'Sources');
  assert.equal(list[0].properties.id, 'sources');
  assert.equal(list[1].tagName, 'ul');
  const li = list[1].children[0];
  assert.equal(li.children[0].tagName, 'a');
  assert.equal(li.children[0].properties.href, 'https://a.example/one');
  assert.equal(textOf(li), 'First source · Alpha Press · 2024');
  const block = generatedSourcesBlock(items(root(p(link('https://a.example/one', 'one'), text('.')))));
  assert.deepEqual(block.properties.className, [GENERATED_SOURCES_CLASS]);
  assert.ok('dataGeneratedSources' in block.properties);
});

test('margin notes are exactly as before, and the list sits after them without being read as a Sources list', () => {
  const make = () => root(
    p(text('See '), link('https://a.example/one', 'the paper'), text(' for details. Then '), link('https://b.example/two', 'two'), text(' follows.'))
  );
  const plain = make();
  transformSourceMarginalia(plain, { citations: CITES });
  const both = make();
  transformNotesAndSources(both, { citations: CITES });
  assert.equal(both.children.length, plain.children.length + 1);
  assert.deepEqual(both.children.slice(0, plain.children.length), plain.children);
  assert.deepEqual(both.children.at(-1).properties.className, [GENERATED_SOURCES_CLASS]);
});

test('a post with a hand-written Sources list is untouched by transformNotesAndSources', () => {
  const make = () => root(
    p(link('https://a.example/one', 'one'), text(' says so with more words than the list has.')),
    el('h2', { id: 'sources' }, [text('Sources')]),
    el('ul', {}, [el('li', {}, [link('https://a.example/one', 'One'), text(' · Someone · Test Journal')])])
  );
  const before = make();
  transformSourceMarginalia(before, { citations: CITES });
  const after = make();
  transformNotesAndSources(after, { citations: CITES });
  assert.deepEqual(after, before);
});

// ---- Pipeline (the configuration Astro uses) ------------------------------------

const renderer = await config.markdown.processor.createRenderer(config.markdown);
const citationFile = JSON.parse(readFileSync(new URL('../../astro-site/src/data/citations.json', import.meta.url), 'utf8'));
const [k1, k2] = Object.keys(citationFile).filter((k) => !k.startsWith('github.com') && !k.includes('williamzujkowski'));
const render = async (md, marginNotes = true) => (await renderer.render(md, { frontmatter: { marginNotes } })).code;
const INLINE = `Early claim from [one](https://${k1}) is plain. Later, [two](https://${k2}) agrees, and [one again](https://${k1}/).\n`;

test('page: a marginNotes post with no Sources list ends with the generated Sources block', async () => {
  const code = await render(INLINE);
  const block = code.match(/<div class="generated-sources"[^>]*>([\s\S]*)<\/div>\s*$/);
  assert.ok(block, 'block at the end of the body');
  assert.match(code, /<div class="generated-sources" data-generated-sources(?:="")? data-pagefind-ignore(?:="")?>/);
  assert.match(block[1], /^<h2 id="sources">Sources<\/h2><ul>/);
  assert.equal((block[1].match(/<li>/g) || []).length, 2);
  assert.ok(block[1].indexOf(`href="https://${k1}"`) < block[1].indexOf(`href="https://${k2}"`));
  assert.match(block[1], /rel="external"/);
  assert.match(code, /remarque-sidenote/, 'the margin notes still render');
  assert.ok(code.indexOf('remarque-sidenote') < code.indexOf('generated-sources'));
});

test('page: byte identity when a post has its own Sources list, footnotes, or no marginNotes flag', async () => {
  const withSources = `${INLINE}\n## Sources\n\n- [One](https://${k1}) - a note\n`;
  const withFootnote = `${INLINE} Also this.[^1]\n\n[^1]: A footnote.\n`;
  for (const md of [withSources, withFootnote]) {
    const out = await render(md);
    assert.doesNotMatch(out, /generated-sources/);
    const baseline = (await renderer.render(md, { frontmatter: { marginNotes: true } })).code;
    assert.equal(out, baseline);
  }
  assert.doesNotMatch(await render(INLINE, false), /generated-sources|remarque-sidenote/);
});

// ---- Feeds ----------------------------------------------------------------------

const site = 'https://example.org/';
const feedOpts = { marginNotes: true, citations: CITES };
const FEED_BODY = [
  'Read [two](https://b.example/two) first, then [one](https://a.example/one) and [two again](https://b.example/two/).',
  '',
  'A [bare-linkified](https://c.example/three) one, and https://d.example/paper too.',
  '',
].join('\n');

test('feed: appends the same list, in link order, as plain h2 + ul with links', () => {
  const html = renderPostForFeed(FEED_BODY, site, feedOpts);
  const tail = html.slice(html.indexOf('<h2>Sources</h2>'));
  assert.ok(tail.length > 0 && html.endsWith('</ul>'));
  assert.deepEqual(
    [...tail.matchAll(/<li>(.*?)<\/li>/g)].map((m) => m[1].replace(/<[^>]+>/g, '')),
    ['Second source · Beta', 'First source · Alpha Press · 2024', 'Third source about caches · 2021', 'one paper · D · 2020']
  );
  assert.match(tail, /<a href="https:\/\/b\.example\/two">Second source<\/a>/);
  assert.doesNotMatch(html, /generated-sources|data-/);
});

test('feed: the list matches the page function on the same body', () => {
  const fromFeed = renderGeneratedSources(FEED_BODY, feedOpts);
  const pageTree = root(
    p(text('Read '), link('https://b.example/two', 'two'), text(' first, then '), link('https://a.example/one', 'one'), text(' and '), link('https://b.example/two/', 'two again'), text('.')),
    p(text('A '), link('https://c.example/three', 'x'), text(' one, and '), link('https://d.example/paper', 'https://d.example/paper'), text(' too.'))
  );
  const fromPage = generatedSourceItems(pageTree, CITES);
  assert.equal((fromFeed.match(/<li>/g) || []).length, fromPage.length);
});

test('feed: byte identity for posts with their own Sources list, footnotes, no flag or no citations', () => {
  const sources = `${FEED_BODY}\n## Sources\n\n- [Two](https://b.example/two) - note\n`;
  const footnote = `${FEED_BODY}\nA claim.[^1]\n\n[^1]: Note.\n`;
  for (const body of [sources, footnote]) {
    assert.equal(renderPostForFeed(body, site, feedOpts), renderPostForFeed(body, site));
  }
  assert.equal(renderPostForFeed(FEED_BODY, site, { marginNotes: false, citations: CITES }), renderPostForFeed(FEED_BODY, site));
  assert.equal(renderPostForFeed(FEED_BODY, site, { marginNotes: true }), renderPostForFeed(FEED_BODY, site));
  assert.equal(renderGeneratedSources('No links here.', feedOpts), '');
});

test('feed: titles and URLs from the citation file are escaped', () => {
  const html = renderPostForFeed('See [x](https://x.example/a) now.', site, {
    marginNotes: true,
    citations: { 'x.example/a': { title: '<script>alert(1)</script> & "q"', publisher: 'P<b>', date: '2020' } },
  });
  assert.doesNotMatch(html, /<script|<b>/);
  assert.match(html, /&amp; /);
});
