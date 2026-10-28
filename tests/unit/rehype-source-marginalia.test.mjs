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

test('several refs in one paragraph alternate strictly: ref, note, ref, note', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [
        text('One '), link('https://example.com/a', 'a'), text(' two '),
        link('https://example.com/b', 'b'), text(' three '), link('https://example.com/c', 'c'), text(' end.'),
      ]),
      ...sourcesList([['https://example.com/a', 'A'], ['https://example.com/b', 'B'], ['https://example.com/c', 'C']]),
    ],
  };
  const before = textOutsideNotes(tree.children[0]);
  transformSourceMarginalia(tree);
  const p = tree.children[0];
  assert.deepEqual(kinds(p.children), ['text', 'a', 'text', 'a', 'text', 'a', 'text', 'ref', 'note', 'ref', 'note', 'ref', 'note']);
  // each ref is described by the note right after it and labelled in DOM order
  [7, 9, 11].forEach((i, n) => {
    assert.equal(p.children[i].properties.ariaLabel, `Note ${n + 1}`);
    assert.equal(p.children[i].properties.ariaDescribedBy[0], p.children[i + 1].properties.id);
  });
  // no counter-set workaround, no paragraph split, no styling hooks
  assert.equal(asides(tree).some((a) => a.properties.style), false);
  assert.equal(tree.children.length, 3);
  assert.equal(p.properties.style, undefined);
  // reading text outside the notes is untouched
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
  assert.deepEqual(flat, ['ref:Note 1', 'note:src-note-1', 'ref:Note 2', 'note:src-note-2', 'ref:Note 3', 'note:src-note-3']);
  assert.deepEqual(kinds(li.children), ['a', 'text', 'a', 'text', 'ref', 'note', 'ref', 'note']);
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

test('placement: two links in one sentence alternate at the sentence end, in link order', () => {
  const p = place([
    text('From '), link('https://example.com/a', 'a'), text(' to '), link('https://example.com/b', 'b'),
    text(' adaptive learning. Second sentence.'),
  ]);
  const k = kinds(p.children);
  assert.deepEqual(k, ['text', 'a', 'text', 'a', 'text', 'ref', 'note', 'ref', 'note', 'text']);
  assert.equal(p.children[5].properties.ariaLabel, 'Note 1');
  assert.equal(p.children[7].properties.ariaLabel, 'Note 2');
  assert.equal(p.children[5].properties.ariaDescribedBy[0], p.children[6].properties.id);
  assert.equal(p.children[7].properties.ariaDescribedBy[0], p.children[8].properties.id);
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
