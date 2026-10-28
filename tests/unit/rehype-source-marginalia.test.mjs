// Unit tests for the Sources-driven margin citation transform .
import test from 'node:test';
import assert from 'node:assert/strict';
import rehypeSourceMarginalia, {
  transformSourceMarginalia,
  normalizeUrl,
  isEcho,
  ECHO_MAX_NEW_WORDS,
} from '../../astro-site/src/lib/rehype-source-marginalia.mjs';

const text = (value) => ({ type: 'text', value });
const el = (tagName, properties, children) => ({
  type: 'element',
  tagName,
  properties: properties || {},
  children: children || [],
});
const link = (href, label) => el('a', { href }, [text(label)]);

function sourcesList(entries) {
  return [
    el('h2', { id: 'sources' }, [text('Sources')]),
    el(
      'ol',
      {},
      entries.map(([href, title, rest]) =>
        // Every fixture entry carries an author and venue, so its note adds
        // information and is not dropped as an echo of the link text.
        el('li', {}, [link(href, title), text(` ${rest || ''} · Someone et al. · Test Journal`)])
      )
    ),
  ];
}

const textOf = (n) => (n.type === 'text' ? n.value : (n.children || []).map(textOf).join(' '));
const hasNoteClass = (n) => Array.isArray(n.properties?.className) && n.properties.className.includes('remarque-sidenote');
const asides = (tree) => {
  const out = [];
  const walk = (n) => {
    if (hasNoteClass(n)) out.push(n);
    (n.children || []).forEach(walk);
  };
  walk(tree);
  return out;
};

// Flatten a hast tree into a compact "kind" string for DOM-order assertions.
const kinds = (nodes) =>
  nodes.map((n) => {
    if (n.type === 'text') return 'text';
    if (n.tagName === 'a') return n.properties.className ? 'ref' : 'a';
    if (hasNoteClass(n)) return 'note';
    return n.tagName;
  });

const textOutsideNotes = (n) => {
  if (n.type === 'text') return n.value;
  if (hasNoteClass(n)) return '';
  return (n.children || []).map(textOutsideNotes).join('');
};

const run = (tree, frontmatter) => rehypeSourceMarginalia()(tree, { data: { astro: { frontmatter } } });

const simpleTree = () => ({
  type: 'root',
  children: [
    el('p', {}, [text('See '), link('https://example.com/paper', 'the paper'), text('.')]),
    ...sourcesList([['https://example.com/paper', 'The Paper', '(2020)']]),
  ],
});

test('normalizeUrl ignores scheme, www, trailing slash, fragment and utm_*', () => {
  assert.equal(
    normalizeUrl('http://www.Example.com/a/b/?utm_source=x#frag'),
    normalizeUrl('https://example.com/a/b')
  );
  assert.notEqual(normalizeUrl('https://example.com/a?id=1'), normalizeUrl('https://example.com/a?id=2'));
  assert.equal(normalizeUrl('mailto:a@b.c'), null);
});

test('an inline link matching a Sources entry gets a ref and a note at the end of its sentence', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('See '), link('https://example.com/paper', 'the paper'), text('.')]),
      el('p', {}, [text('Next.')]),
      ...sourcesList([['https://example.com/paper/', 'The Paper', '(2020) - by Someone']]),
    ],
  };
  transformSourceMarginalia(tree);
  const p = tree.children[0];
  assert.deepEqual(kinds(p.children), ['text', 'a', 'text', 'ref', 'note']);
  const [, , , ref, note] = p.children;
  assert.equal(ref.properties.className[0], 'remarque-sidenote-ref');
  assert.equal(ref.properties.ariaLabel, 'Note 1');
  assert.equal(note.properties.role, 'note');
  assert.equal(note.tagName, 'span'); // phrasing content, valid inside <p>
  assert.equal(ref.properties.ariaDescribedBy[0], note.properties.id);
  // the title link is not repeated as a second link
  assert.equal(note.children.some((c) => c.tagName === 'a'), false);
  // nothing else in the document changed
  assert.equal(tree.children.length, 4);
});

test('a link whose URL is in no entry gets nothing; text of the post is untouched', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://other.example/x', 'other')]),
      ...sourcesList([['https://example.com/paper', 'The Paper']]),
    ],
  };
  transformSourceMarginalia(tree);
  assert.equal(asides(tree).length, 0);
  assert.equal(tree.children[0].children.length, 1);
});

test('a URL listed by two entries is ambiguous and gets no note', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://example.com/a', 'a')]),
      ...sourcesList([
        ['https://example.com/a', 'A one'],
        ['https://example.com/a', 'A two'],
      ]),
    ],
  };
  transformSourceMarginalia(tree);
  assert.equal(asides(tree).length, 0);
});

test('only the first link to an entry gets a note', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://example.com/a', 'a')]),
      el('p', {}, [link('https://example.com/a', 'again')]),
      ...sourcesList([['https://example.com/a', 'A']]),
    ],
  };
  transformSourceMarginalia(tree);
  assert.equal(asides(tree).length, 1);
});

test('links inside Sources, headings and code are never annotated; footnote posts are skipped', () => {
  const tree = {
    type: 'root',
    children: [
      el('h2', {}, [link('https://example.com/a', 'heading link')]),
      el('p', {}, [el('code', {}, [link('https://example.com/a', 'code')])]),
      ...sourcesList([['https://example.com/a', 'A']]),
    ],
  };
  transformSourceMarginalia(tree);
  assert.equal(asides(tree).length, 0);

  const withFootnotes = {
    type: 'root',
    children: [
      el('p', {}, [link('https://example.com/a', 'a'), el('a', { className: ['remarque-sidenote-ref'] })]),
      ...sourcesList([['https://example.com/a', 'A']]),
    ],
  };
  transformSourceMarginalia(withFootnotes);
  assert.equal(asides(withFootnotes).length, 0);
});

test('a tight list item gets its note inside the item, before any nested list', () => {
  const li = el('li', {}, [
    link('https://example.com/a', 'a'),
    text(': thing'),
    el('ul', {}, [el('li', {}, [text('sub')])]),
  ]);
  const tree = {
    type: 'root',
    children: [el('ul', {}, [li]), ...sourcesList([['https://example.com/a', 'A']])],
  };
  transformSourceMarginalia(tree);
  assert.deepEqual(kinds(li.children), ['a', 'text', 'ref', 'note', 'ul']);
});

test('flag off, missing or not literally true: the tree is not touched', () => {
  for (const fm of [undefined, {}, { marginNotes: false }, { marginNotes: 'true' }, { marginNotes: 1 }]) {
    const tree = simpleTree();
    const before = JSON.stringify(tree);
    run(tree, fm);
    assert.equal(JSON.stringify(tree), before, `frontmatter ${JSON.stringify(fm)}`);
  }
  // a file object with no data at all (other pipelines) is also inert
  const bare = simpleTree();
  const snap = JSON.stringify(bare);
  rehypeSourceMarginalia()(bare, undefined);
  assert.equal(JSON.stringify(bare), snap);
});

test('flag on: the same tree gets its ref and note', () => {
  const tree = simpleTree();
  run(tree, { marginNotes: true });
  assert.equal(asides(tree).length, 1);
});

test('only http: and https: URLs can match', () => {
  for (const bad of ['mailto:a@example.com', 'javascript:alert(1)', 'data:text/html,x', 'ftp://example.com/a', 'file:///etc/passwd', 'tel:+15551234', '//example.com/a', '/relative/path']) {
    assert.equal(normalizeUrl(bad), null, bad);
  }
  assert.notEqual(normalizeUrl('HTTP://Example.com/a'), null);
  assert.notEqual(normalizeUrl('https://example.com/a'), null);
  // same non-web "URL" in the body and in Sources must still not match
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('ftp://example.com/a', 'ftp'), text(' '), link('javascript:alert(1)', 'js')]),
      ...sourcesList([['ftp://example.com/a', 'F'], ['javascript:alert(1)', 'J']]),
    ],
  };
  transformSourceMarginalia(tree);
  assert.equal(asides(tree).length, 0);
});

test('three links in one sentence share one ref and one combined note, in link order', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [
        text('One '), link('https://example.com/a', 'a'), text(' two '),
        link('https://example.com/b', 'b'), text(' three '), link('https://example.com/c', 'c'), text(' end.'),
      ]),
      ...sourcesList([['https://example.com/a', 'Alpha'], ['https://example.com/b', 'Bravo'], ['https://example.com/c', 'Charlie']]),
    ],
  };
  const before = textOutsideNotes(tree.children[0]);
  transformSourceMarginalia(tree);
  const p = tree.children[0];
  assert.deepEqual(kinds(p.children), ['text', 'a', 'text', 'a', 'text', 'a', 'text', 'ref', 'note']);
  const [ref, note] = p.children.slice(-2);
  assert.equal(ref.properties.ariaLabel, 'Note 1');
  assert.equal(ref.properties.ariaDescribedBy[0], note.properties.id);
  assert.equal(note.tagName, 'span');
  assert.equal(note.properties.role, 'note');
  // all three entries, in link order, one per line, phrasing content only
  assert.equal(note.children.filter((c) => c.tagName === 'br').length, 2);
  const t = textOf(note);
  assert.ok(t.indexOf('Alpha') < t.indexOf('Bravo') && t.indexOf('Bravo') < t.indexOf('Charlie'));
  assert.equal(asides(tree).length, 1);
  assert.equal(asides(tree).some((a) => a.properties.style), false);
  assert.equal(tree.children.length, 3);
  assert.equal(textOutsideNotes(p), before);
});

test('refs alternate in document order across paragraphs and list items', () => {
  const li = el('li', {}, [link('https://example.com/b', 'b'), text(' and '), link('https://example.com/c', 'c'), text(' done')]);
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://example.com/a', 'a'), text('.')]),
      el('ul', {}, [li]),
      ...sourcesList([['https://example.com/a', 'A'], ['https://example.com/b', 'B'], ['https://example.com/c', 'C']]),
    ],
  };
  transformSourceMarginalia(tree);
  const flat = [];
  const walk = (n) => {
    if (n.tagName === 'a' && n.properties.className) flat.push('ref:' + n.properties.ariaLabel);
    else if (hasNoteClass(n)) flat.push('note:' + n.properties.id);
    (n.children || []).forEach(walk);
  };
  walk(tree.children[0]);
  walk(tree.children[1]);
  // b and c share the list item's (unterminated) sentence: one combined note, so two numbers in all.
  assert.deepEqual(flat, ['ref:Note 1', 'note:src-note-1', 'ref:Note 2', 'note:src-note-2']);
  assert.deepEqual(kinds(li.children), ['a', 'text', 'a', 'text', 'ref', 'note']);
});

test('a link inside inline emphasis: the pair goes after the emphasis, at the sentence end', () => {
  const tree = {
    type: 'root',
    children: [el('p', {}, [el('em', {}, [text('see '), link('https://example.com/a', 'a')]), text(' ok')]), ...sourcesList([['https://example.com/a', 'A']])],
  };
  transformSourceMarginalia(tree);
  assert.deepEqual(kinds(tree.children[0].children[0].children), ['text', 'a']);
  assert.deepEqual(kinds(tree.children[0].children), ['em', 'text', 'ref', 'note']);
});

test('an entry whose content is not phrasing-only gets no note and consumes no number', () => {
  const blocky = el('li', {}, [link('https://example.com/a', 'A'), el('div', {}, [text('block')])]);
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://example.com/a', 'a'), text(' '), link('https://example.com/b', 'b')]),
      el('h2', {}, [text('Sources')]),
      el('ol', {}, [blocky, el('li', {}, [link('https://example.com/b', 'B'), text(' (2020) · Someone et al. · Test Journal')])]),
    ],
  };
  transformSourceMarginalia(tree);
  assert.equal(asides(tree).length, 1);
  assert.equal(asides(tree)[0].properties.id, 'src-note-1');
});

test('a post with GFM footnotes is excluded (shared counter)', () => {
  const tree = simpleTree();
  tree.children.push(el('section', { dataFootnotes: true }, []));
  run(tree, { marginNotes: true });
  assert.equal(asides(tree).length, 0);
});

test('onMatch sees each hit before the tree changes', () => {
  const tree = simpleTree();
  const seen = [];
  transformSourceMarginalia(tree, {
    onMatch: ({ host, serial }) => seen.push([serial, host.children.length]),
  });
  assert.deepEqual(seen, [[1, 3]]);
});

test('a note that only echoes its link text is dropped and consumes no number', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://example.com/tool', 'nexus-agents'), text(' and '), link('https://example.com/paper', 'the paper'), text('.')]),
      el('h2', { id: 'sources' }, [text('Sources')]),
      el('ol', {}, [
        el('li', {}, [link('https://example.com/tool', 'nexus-agents')]),
        el('li', {}, [link('https://example.com/paper', 'The Paper'), text(' (2021) · Smith et al. · Nature Communications')]),
      ]),
    ],
  };
  transformSourceMarginalia(tree);
  const notes = asides(tree);
  assert.equal(notes.length, 1, 'only the informative note renders');
  assert.match(textOutsideNotes({ type: 'root', children: [] }) + notes[0].children.map((c) => c.value || '').join(''), /Smith/);
  const p = tree.children[0];
  assert.deepEqual(kinds(p.children), ['a', 'text', 'a', 'text', 'ref', 'note']);
  assert.equal(p.children[4].properties.ariaLabel, 'Note 1');
});

test('isEcho counts words the note adds beyond the link text', () => {
  const content = (s) => [text(s)];
  assert.equal(ECHO_MAX_NEW_WORDS, 2);
  assert.equal(isEcho(link('u', 'USLM (United States Legislative Markup)'), content('USLM (United States Legislative Markup)')), true);
  assert.equal(isEcho(link('u', 'Renovate'), content('Renovate: minimumReleaseAge configuration')), true);
  assert.equal(isEcho(link('u', 'Harvard Kilobot'), content('Harvard Kilobot swarm research, Harvard DASH repository')), false);
});

// ---- Sentence-end placement ---------------------------------------------------

// One paragraph, one matching link, then check where the pair lands and that
// the visible words outside the notes are unchanged.
function place(children, extra = []) {
  const tree = {
    type: 'root',
    children: [el('p', {}, children), ...sourcesList([['https://example.com/a', 'A'], ['https://example.com/b', 'B'], ...extra])],
  };
  const before = textOutsideNotes(tree.children[0]);
  transformSourceMarginalia(tree);
  const p = tree.children[0];
  assert.equal(textOutsideNotes(p), before, 'text outside the notes is unchanged');
  return p;
}
// The words before the first ref, and after the last note.
function around(p) {
  const out = { before: '', after: '' };
  let seen = 0;
  const walk = (n) => {
    if (n.type === 'text') out[seen ? 'after' : 'before'] += n.value;
    else if (n.tagName === 'a' && n.properties.className) seen = 1;
    else if (hasNoteClass(n)) return;
    else (n.children || []).forEach(walk);
  };
  walk(p);
  return out;
}

test('placement: the pair follows the terminal period, before the next sentence', () => {
  const p = place([text('Models route '), link('https://example.com/a', 'badly'), text(' at first. Then they learn.')]);
  const { before, after } = around(p);
  assert.equal(before, 'Models route badly at first.');
  assert.equal(after, ' Then they learn.');
});

test('placement: ? and ! end a sentence; closing quotes and brackets stay before the pair', () => {
  let p = place([text('Why '), link('https://example.com/a', 'this'), text(' (really?) He said "no!" Next.')]);
  // "(really?)" is followed by a space and an uppercase H: the sentence ends after ")".
  assert.equal(around(p).before, 'Why this (really?)');
  p = place([text('He said "see '), link('https://example.com/a', 'it'), text('!" Then left.')]);
  assert.equal(around(p).before, 'He said "see it!"');
});

test('placement: abbreviations do not end the sentence', () => {
  for (const abbr of ['e.g.', 'i.e.', 'et al.', 'vs.', 'etc.', 'Fig.', 'Dr.', 'U.S.', 'J.']) {
    const p = place([text('Use '), link('https://example.com/a', 'x'), text(` ${abbr} Then more text. Next one.`)]);
    assert.equal(around(p).before, `Use x ${abbr} Then more text.`, abbr);
  }
});

test('placement: "No." ends a sentence unless a number follows', () => {
  let p = place([link('https://example.com/a', 'x'), text(' Answer: no. Then more.')]);
  assert.equal(around(p).before, 'x Answer: no.');
  p = place([link('https://example.com/a', 'x'), text(' see No. 5 for more. Then more.')]);
  assert.equal(around(p).before, 'x see No. 5 for more.');
});

test('placement: citation abbreviations before a number do not end the sentence', () => {
  for (const abbr of ['Vol.', 'vol.', 'pp.', 'Ch.', 'Sec.', 'Eq.', 'Art.']) {
    const p = place([text('See '), link('https://example.com/a', 'x'), text(` (IEEE TDSC ${abbr} 21, 2024). Then more.`)]);
    assert.equal(around(p).before, `See x (IEEE TDSC ${abbr} 21, 2024).`, abbr);
  }
  const p = place([link('https://example.com/a', 'x'), text(' filled the vol. Then more.')]);
  assert.equal(around(p).before, 'x filled the vol.');
});

test('placement: decimals and version numbers do not end the sentence', () => {
  const p = place([text('GPT '), link('https://example.com/a', 'tool'), text(' 3.5 and v0.33 are old. Newer ones exist.')]);
  assert.equal(around(p).before, 'GPT tool 3.5 and v0.33 are old.');
});

test('placement: a period inside code is not a sentence end', () => {
  const p = place([link('https://example.com/a', 'tool'), text(' calls '), el('code', {}, [text('a. B')]), text(' then stops. Next.')]);
  assert.equal(around(p).before, 'tool calls a. B then stops.');
});

test('placement: no sentence end falls back to the end of the host block', () => {
  const p = place([text('A fragment with '), link('https://example.com/a', 'a link'), text(' and no stop')]);
  assert.deepEqual(kinds(p.children), ['text', 'a', 'text', 'ref', 'note']);
});

test('placement: a link whose parent closes before the sentence end continues in the parent', () => {
  const p = place([el('em', {}, [text('see '), link('https://example.com/a', 'a')]), text(' and more words. Next.')]);
  assert.deepEqual(kinds(p.children), ['em', 'text', 'ref', 'note', 'text']);
  assert.equal(p.children[1].value, ' and more words.');
  assert.equal(p.children[4].value, ' Next.');
});

test('placement: a sentence ending inside inline emphasis lifts the pair out of the emphasis', () => {
  const p = place([el('em', {}, [link('https://example.com/a', 'a'), text(' is *the* point.')]), text(' Next.')]);
  assert.deepEqual(kinds(p.children), ['em', 'ref', 'note', 'text']);
});

test('placement: two links in one sentence get one ref and one combined note at the sentence end', () => {
  const p = place([
    text('From '), link('https://example.com/a', 'a'), text(' to '), link('https://example.com/b', 'b'),
    text(' adaptive learning. Second sentence.'),
  ]);
  assert.deepEqual(kinds(p.children), ['text', 'a', 'text', 'a', 'text', 'ref', 'note', 'text']);
  assert.equal(p.children[5].properties.ariaLabel, 'Note 1');
  assert.equal(p.children[5].properties.ariaDescribedBy[0], p.children[6].properties.id);
  assert.deepEqual(kinds(p.children[6].children).filter((k) => k === 'br'), ['br']);
  assert.equal(around(p).before, 'From a to b adaptive learning.');
});

test('placement: numbering continues in document order after a combined note', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://example.com/a', 'a'), text(' and '), link('https://example.com/b', 'b'), text(' agree. Then '), link('https://example.com/c', 'c'), text(' too.')]),
      el('p', {}, [link('https://example.com/d', 'd'), text(' last.')]),
      ...sourcesList([['https://example.com/a', 'A'], ['https://example.com/b', 'B'], ['https://example.com/c', 'C'], ['https://example.com/d', 'D']]),
    ],
  };
  transformSourceMarginalia(tree);
  const labels = [];
  const walk = (n) => {
    if (n.tagName === 'a' && n.properties.className) labels.push(n.properties.ariaLabel);
    (n.children || []).forEach(walk);
  };
  walk(tree.children[0]);
  walk(tree.children[1]);
  assert.deepEqual(labels, ['Note 1', 'Note 2', 'Note 3']);
  assert.equal(asides(tree).length, 3);
});

test('placement: the block-end fallback also combines links into one note', () => {
  const p = place([link('https://example.com/a', 'a'), text(' and '), link('https://example.com/b', 'b'), text(' no stop')]);
  assert.deepEqual(kinds(p.children), ['a', 'text', 'a', 'text', 'ref', 'note']);
});

test('onMatch reports every hit of a combined note with the same serial', () => {
  const tree = {
    type: 'root',
    children: [el('p', {}, [link('https://example.com/a', 'a'), text(' and '), link('https://example.com/b', 'b'), text('.')]), ...sourcesList([['https://example.com/a', 'A'], ['https://example.com/b', 'B']])],
  };
  const seen = [];
  transformSourceMarginalia(tree, { onMatch: ({ serial }) => seen.push(serial) });
  assert.deepEqual(seen, [1, 1]);
});

test('placement: links in different sentences each get their own sentence end', () => {
  const p = place([
    link('https://example.com/a', 'a'), text(' one. Then '), link('https://example.com/b', 'b'), text(' two. Last.'),
  ]);
  assert.deepEqual(kinds(p.children), ['a', 'text', 'ref', 'note', 'text', 'a', 'text', 'ref', 'note', 'text']);
  assert.equal(p.children[2].properties.ariaLabel, 'Note 1');
  assert.equal(p.children[7].properties.ariaLabel, 'Note 2');
});

test('placement: a link that is itself the whole sentence ends it there', () => {
  const p = place([link('https://example.com/a', 'A whole sentence.'), text(' Next one here.')]);
  assert.deepEqual(kinds(p.children), ['a', 'ref', 'note', 'text']);
});

test('placement: a note never lands inside another link', () => {
  const p = place([
    link('https://example.com/a', 'a'), text(' then '), link('https://other.example/x', 'Foo. Bar'), text(' baz.'),
  ]);
  const inLink = (n) => n.tagName === 'a' && !n.properties.className && (n.children || []).some(hasNoteClass);
  assert.equal(p.children.some(inLink), false);
  assert.equal(around(p).before, 'a then Foo. Bar baz.');
});

test('onMatch still reports the host block with its full sentence text', () => {
  const tree = {
    type: 'root',
    children: [el('p', {}, [text('See '), link('https://example.com/a', 'a'), text(' now. Done.')]), ...sourcesList([['https://example.com/a', 'A']])],
  };
  let seen = null;
  transformSourceMarginalia(tree, { onMatch: ({ host, serial }) => (seen = { text: textOutsideNotes(host), serial }) });
  assert.deepEqual(seen, { text: 'See a now. Done.', serial: 1 });
});

// ---- Citation-file fallback ---------------------------------------------------

import { isSkippedCitationKey, citationText, isSentenceEcho, SENTENCE_ECHO_MAX_NEW_WORDS } from '../../astro-site/src/lib/rehype-source-marginalia.mjs';

const CITES = {
  'docs.example.com/provenance': { title: 'Generating provenance statements', publisher: 'Example Docs', date: '2025-03-04', checked: '2026-10-28' },
  'blog.example.org/post': { title: 'A long post about caches', publisher: 'Example Blog', date: null, checked: '2026-10-28' },
  'github.com/o/r/blob/main/file.mjs': { title: 'file.mjs', publisher: 'GitHub', date: null, checked: '2026-10-28' },
  'github.com/o/r/issues/7': { title: 'Cache eviction regression', publisher: 'GitHub (o/r)', date: '2026-01-02', checked: '2026-10-28' },
  'williamzujkowski.github.io/posts/x': { title: 'Own post', publisher: 'Me', date: null, checked: '2026-10-28' },
  'untitled.example/x': { title: '', publisher: 'P', date: '2020', checked: '2026-10-28' },
  'nopub.example/x': { title: 'Only a title for notes', date: null, checked: '2026-10-28' },
};
const inlineTree = (...inline) => ({ type: 'root', children: [el('p', {}, inline)] });
const noteTexts = (tree) => asides(tree).map((n) => textOf(n).replace(/\s+/g, ' ').trim());

test('fallback: a post with no Sources heading takes its notes from the citation file', () => {
  const tree = inlineTree(text("npm's "), link('https://docs.example.com/provenance', 'docs'), text(' say so. Next.'));
  transformSourceMarginalia(tree, { citations: CITES });
  assert.deepEqual(noteTexts(tree), ['Generating provenance statements · Example Docs · 2025']);
  assert.deepEqual(kinds(tree.children[0].children), ['text', 'a', 'text', 'ref', 'note', 'text']);
});

test('fallback: normalised URL matching (www, scheme, trailing slash, utm) works against file keys', () => {
  const tree = inlineTree(link('http://www.docs.example.com/provenance/?utm_source=x#frag', 'docs'), text(' says so.'));
  transformSourceMarginalia(tree, { citations: CITES });
  assert.equal(asides(tree).length, 1);
});

test('fallback: missing fields are omitted, an entry without a title gets no note', () => {
  const a = inlineTree(link('https://blog.example.org/post', 'a post'), text(' says so.'));
  transformSourceMarginalia(a, { citations: CITES });
  assert.deepEqual(noteTexts(a), ['A long post about caches · Example Blog']);
  const b = inlineTree(link('https://nopub.example/x', 'it'), text(' says so.'));
  transformSourceMarginalia(b, { citations: CITES });
  assert.deepEqual(noteTexts(b), ['Only a title for notes']);
  const c = inlineTree(link('https://untitled.example/x', 'it'), text(' says so.'));
  transformSourceMarginalia(c, { citations: CITES });
  assert.equal(asides(c).length, 0);
  assert.equal(citationText({ title: 'T', publisher: 'P', date: '2024-05-06' }), 'T · P · 2024');
  assert.equal(citationText({ publisher: 'P' }), null);
});

test('fallback: a Sources list wins; the citation file is ignored for that post', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://docs.example.com/provenance', 'docs'), text(' say so. '), link('https://blog.example.org/post', 'a post'), text(' too.')]),
      ...sourcesList([['https://docs.example.com/provenance', 'From the list']]),
    ],
  };
  transformSourceMarginalia(tree, { citations: CITES });
  const notes = noteTexts(tree);
  assert.equal(notes.length, 1); // the blog link is in the file but the post has a Sources list
  assert.match(notes[0], /From the list/);
  assert.doesNotMatch(notes[0], /Generating provenance/);
});

test('fallback skip rules: own domain, relative links, GitHub files/commits/trees/compares, non-http', () => {
  for (const k of [
    'williamzujkowski.github.io/posts/x',
    'github.com/o/r/blob/main/a.js',
    'github.com/o/r/commit/abc123',
    'github.com/o/r/tree/main/src',
    'github.com/o/r/compare/a...b',
  ]) assert.equal(isSkippedCitationKey(k), true, k);
  for (const k of ['github.com/o/r', 'github.com/o/r/issues/7', 'github.com/o/r/pull/9', 'github.com/advisories/GHSA-aaaa-bbbb-cccc', 'github.com/o/r/releases/tag/v1']) {
    assert.equal(isSkippedCitationKey(k), false, k);
  }
  const tree = inlineTree(
    link('https://williamzujkowski.github.io/posts/x', 'my post'), text(' one. '),
    link('/posts/x', 'relative'), text(' two. '),
    link('https://github.com/o/r/blob/main/file.mjs', 'the file'), text(' three. '),
    link('https://github.com/o/r/issues/7', 'the issue'), text(' four.')
  );
  transformSourceMarginalia(tree, { citations: CITES });
  assert.deepEqual(noteTexts(tree), ['Cache eviction regression · GitHub (o/r) · 2026']);
});

test('fallback: echo suppression applies against the title', () => {
  const citations = { 'e.example/x': { title: 'Cache eviction', publisher: 'Example', date: null } };
  const echo = inlineTree(text('See '), link('https://e.example/x', 'cache eviction example'), text(' here.'));
  transformSourceMarginalia(echo, { citations });
  assert.equal(asides(echo).length, 0); // one new word (Example), at most ECHO_MAX_NEW_WORDS
  const adds = inlineTree(text('See '), link('https://e.example/x', 'this'), text(' here.'));
  transformSourceMarginalia(adds, { citations });
  assert.equal(asides(adds).length, 1);
});

test('fallback: sentence-end placement, one combined note per sentence, only first link per URL', () => {
  const tree = inlineTree(
    text('Both '), link('https://docs.example.com/provenance', 'docs'), text(' and '),
    link('https://blog.example.org/post', 'a post'), text(' agree. Then '),
    link('https://docs.example.com/provenance', 'docs again'), text(' returns.')
  );
  transformSourceMarginalia(tree, { citations: CITES });
  assert.equal(asides(tree).length, 1);
  assert.deepEqual(noteTexts(tree), ['Generating provenance statements · Example Docs · 2025 A long post about caches · Example Blog']);
  assert.equal(textOutsideNotes(tree.children[0]), 'Both docs and a post agree. Then docs again returns.');
});

test('fallback: no citations option, empty file, or footnote posts leave the tree untouched', () => {
  const mk = () => inlineTree(text('See '), link('https://docs.example.com/provenance', 'docs'), text('.'));
  const before = JSON.stringify(mk());
  const a = mk();
  transformSourceMarginalia(a);
  assert.equal(JSON.stringify(a), before);
  const b = mk();
  transformSourceMarginalia(b, { citations: {} });
  assert.equal(JSON.stringify(b), before);
  const c = mk();
  c.children.push(el('section', { dataFootnotes: true }, []));
  transformSourceMarginalia(c, { citations: CITES });
  assert.equal(asides(c).length, 0);
});

test('fallback: no marginNotes flag means byte-identical output even with a citation file', () => {
  const tree = inlineTree(text('See '), link('https://docs.example.com/provenance', 'docs'), text('.'));
  const before = JSON.stringify(tree);
  rehypeSourceMarginalia({ citations: CITES })(tree, { data: { astro: { frontmatter: {} } } });
  assert.equal(JSON.stringify(tree), before);
  rehypeSourceMarginalia({ citations: CITES })(tree, { data: { astro: { frontmatter: { marginNotes: true } } } });
  assert.equal(asides(tree).length, 1);
});

test('fallback: onMatch reports the citation entry and key', () => {
  const tree = inlineTree(text('See '), link('https://docs.example.com/provenance', 'docs'), text('.'));
  let seen = null;
  transformSourceMarginalia(tree, { citations: CITES, onMatch: ({ key, serial }) => (seen = { key, serial }) });
  assert.deepEqual(seen, { key: 'docs.example.com/provenance', serial: 1 });
});

test('dedupe: a later link to the same citation gets no note; same title (any case) is one citation', () => {
  const citations = {
    'p.example/paper.pdf': { title: 'Sharpen the Spec, Cut the Code', publisher: 'USENIX', date: '2026' },
    'p.example/paper': { title: 'sharpen the spec, cut the code', publisher: 'USENIX', date: '2026' },
    'other.example/x': { title: 'A different thing entirely here', publisher: 'Other', date: null },
  };
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('First '), link('https://p.example/paper.pdf', 'pdf'), text(' says so.')]),
      el('p', {}, [text('Then '), link('https://p.example/paper', 'page'), text(' again. And '), link('https://other.example/x', 'other'), text(' too.')]),
    ],
  };
  transformSourceMarginalia(tree, { citations });
  assert.deepEqual(noteTexts(tree), ['Sharpen the Spec, Cut the Code · USENIX · 2026', 'A different thing entirely here · Other']);
  assert.equal(tree.children[1].children.filter((c) => c.properties?.className).length, 2); // 'other' only
});

test('dedupe applies to fallback notes only: a Sources post still notes both same-title entries', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [link('https://a.example/1', 'one'), text(' first.')]),
      el('p', {}, [link('https://a.example/2', 'two'), text(' second.')]),
      ...sourcesList([['https://a.example/1', 'Same Title'], ['https://a.example/2', 'Same Title']]),
    ],
  };
  transformSourceMarginalia(tree, { citations: {} });
  assert.equal(asides(tree).length, 2);
});

test('sentence echo: a note that adds at most SENTENCE_ECHO_MAX_NEW_WORDS words the sentence lacks is dropped', () => {
  assert.equal(SENTENCE_ECHO_MAX_NEW_WORDS, 2);
  const citations = { 's.example/x': { title: 'Taxonomy of Attacks on Supply Chains', publisher: 'arXiv', date: '2022' } };
  const echo = inlineTree(text('The Taxonomy of Attacks on '), link('https://s.example/x', 'supply chains'), text(' is on arXiv, from 2022.'));
  transformSourceMarginalia(echo, { citations });
  assert.equal(asides(echo).length, 0);
  const adds = inlineTree(text('The '), link('https://s.example/x', 'taxonomy'), text(' lists attacks.'));
  transformSourceMarginalia(adds, { citations });
  assert.equal(asides(adds).length, 1);
});

test('sentence echo: stop words and separators are ignored, other sentences do not count', () => {
  const content = [text('Guide to the Thing of a Kind · With By At From In On And For')];
  assert.equal(isSentenceEcho('The guide thing kind', content), true);
  // the only sentence words that count are the ones in the link's own sentence
  const citations = { 's.example/y': { title: 'Alpha beta gamma delta', publisher: null, date: null } };
  const tree = inlineTree(text('Alpha beta gamma delta came earlier. See '), link('https://s.example/y', 'this'), text(' now.'));
  transformSourceMarginalia(tree, { citations });
  assert.equal(asides(tree).length, 1);
});

test('sentence echo does not apply to a Sources post (link-text echo only)', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('The Paper by Someone et al. in Test Journal is '), link('https://example.com/paper', 'here'), text('.')]),
      ...sourcesList([['https://example.com/paper', 'The Paper']]),
    ],
  };
  transformSourceMarginalia(tree, { citations: {} });
  assert.equal(asides(tree).length, 1);
});

test('publisher elision: a publisher fully inside the title is omitted', () => {
  assert.equal(citationText({ title: 'The Dafny Programming and Verification Language', publisher: 'Dafny', date: null }), 'The Dafny Programming and Verification Language');
  assert.equal(citationText({ title: 'Packagist: The PHP Package Repository', publisher: 'Packagist', date: '2020' }), 'Packagist: The PHP Package Repository · 2020');
  assert.equal(citationText({ title: 'Thing', publisher: 'Thing Docs', date: null }), 'Thing · Thing Docs');
});
