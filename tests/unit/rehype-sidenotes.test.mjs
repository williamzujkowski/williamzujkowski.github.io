// Unit tests for the sidenotes rehype AST transform (issue #272 vote
// condition: "if hand-rolling, the AST transform needs unit tests").
//
// Uses Node's built-in test runner (node:test) — no new devDependency,
// consistent with this repo's Python-scripts-only-3-deps minimalism (see
// AGENTS.md). Run with:
//   node --test tests/unit/rehype-sidenotes.test.mjs
//
// Fixtures below are hand-built hast trees that mirror exactly what
// mdast-util-to-hast's footnote handlers (footnote-reference.js, footer.js)
// actually produce for GFM `[^n]` syntax — not a full unified/remark/rehype
// pipeline, so these tests exercise `transformSidenotes` in isolation.

import test from 'node:test';
import assert from 'node:assert/strict';
import { transformSidenotes } from '../../astro-site/src/lib/rehype-sidenotes.mjs';

function text(value) {
  return { type: 'text', value };
}

function el(tagName, properties, children) {
  return { type: 'element', tagName, properties: properties || {}, children: children || [] };
}

/** A single GFM footnote reference, as mdast-util-to-hast emits it. */
function footnoteRef(id, counter, { rereference } = {}) {
  return el('sup', {}, [
    el(
      'a',
      {
        href: `#user-content-fn-${id}`,
        id: `user-content-fnref-${id}${rereference ? `-${rereference}` : ''}`,
        dataFootnoteRef: true,
        ariaDescribedBy: ['footnote-label'],
      },
      [text(String(counter))]
    ),
  ]);
}

/** A single GFM footnote definition `<li>`, as footer() emits it. */
function footnoteDef(id, paragraphs) {
  const lastP = paragraphs[paragraphs.length - 1];
  const backref = el(
    'a',
    { href: `#user-content-fnref-${id}`, dataFootnoteBackref: '', className: ['data-footnote-backref'] },
    [text('↩')]
  );
  const withBackref = paragraphs.map((p, i) =>
    i === paragraphs.length - 1 ? el('p', p.properties, [...p.children, text(' '), backref]) : p
  );
  return el('li', { id: `user-content-fn-${id}` }, withBackref.length ? withBackref : [backref]);
}

function footnotesSection(defs) {
  return el('section', { dataFootnotes: true, className: ['footnotes'] }, [
    el('h2', { className: ['sr-only'], id: 'footnote-label' }, [text('Footnotes')]),
    el('ol', {}, defs),
  ]);
}

test('document with no footnotes section is returned untouched', () => {
  const tree = { type: 'root', children: [el('p', {}, [text('Hello world.')])] };
  const before = JSON.stringify(tree);
  transformSidenotes(tree);
  assert.equal(JSON.stringify(tree), before);
});

test('moves a single footnote inline right after its paragraph', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('A claim needs a citation.'), footnoteRef('rand', 1)]),
      el('p', {}, [text('An unrelated paragraph.')]),
      footnotesSection([footnoteDef('rand', [el('p', {}, [text('RAND Corporation analysis.')])])]),
    ],
  };

  transformSidenotes(tree);

  // Footnotes section is gone.
  assert.equal(
    tree.children.some((n) => n.tagName === 'section'),
    false
  );

  // Sidenote is the direct next sibling of the referencing paragraph.
  assert.equal(tree.children.length, 3);
  assert.equal(tree.children[0].tagName, 'p');
  assert.equal(tree.children[1].tagName, 'small');
  assert.deepEqual(tree.children[1].properties.className, ['sidenote']);
  assert.equal(tree.children[1].properties.id, 'user-content-fn-rand');
  assert.equal(tree.children[2].tagName, 'p'); // the unrelated paragraph, untouched

  // Ref anchor got the sidenote-ref class, href/id untouched.
  const ref = tree.children[0].children[1].children[0];
  assert.deepEqual(ref.properties.className, ['sidenote-ref']);
  assert.equal(ref.properties.href, '#user-content-fn-rand');

  // Sidenote carries a mono-voice number span using the ref's own counter text.
  const [numberSpan, , ...rest] = tree.children[1].children;
  assert.equal(numberSpan.tagName, 'span');
  assert.deepEqual(numberSpan.properties.className, ['sidenote-number']);
  assert.equal(numberSpan.children[0].value, '1');

  // Backref arrow was stripped — note text shouldn't carry a "back to
  // reference" link (redundant once the note sits next to its reference).
  const noteText = JSON.stringify(rest);
  assert.equal(noteText.includes('dataFootnoteBackref'), false);
  assert.ok(noteText.includes('RAND Corporation analysis.'));
});

test('multiple footnotes across multiple paragraphs land after the correct paragraph, in order', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', { id: 'p1' }, [text('First claim.'), footnoteRef('a', 1)]),
      el('p', { id: 'p2' }, [text('Second claim.'), footnoteRef('b', 2)]),
      footnotesSection([
        footnoteDef('a', [el('p', {}, [text('Source A.')])]),
        footnoteDef('b', [el('p', {}, [text('Source B.')])]),
      ]),
    ],
  };

  transformSidenotes(tree);

  assert.deepEqual(
    tree.children.map((n) => n.tagName),
    ['p', 'small', 'p', 'small']
  );
  assert.equal(tree.children[0].properties.id, 'p1');
  assert.ok(JSON.stringify(tree.children[1]).includes('Source A.'));
  assert.equal(tree.children[2].properties.id, 'p2');
  assert.ok(JSON.stringify(tree.children[3]).includes('Source B.'));
});

test('two footnotes cited in the SAME paragraph land after it in citation order', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [
        text('First citation'),
        footnoteRef('a', 1),
        text(' and second citation'),
        footnoteRef('b', 2),
        text('.'),
      ]),
      footnotesSection([
        footnoteDef('a', [el('p', {}, [text('Source A.')])]),
        footnoteDef('b', [el('p', {}, [text('Source B.')])]),
      ]),
    ],
  };

  transformSidenotes(tree);

  assert.deepEqual(
    tree.children.map((n) => n.tagName),
    ['p', 'small', 'small']
  );
  // Citation order preserved: A's note comes before B's note, matching the
  // order the two `[^n]` refs appear in the paragraph.
  assert.equal(tree.children[1].properties.id, 'user-content-fn-a');
  assert.equal(tree.children[2].properties.id, 'user-content-fn-b');
});

test('a footnote referenced twice only inserts one sidenote', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('First mention.'), footnoteRef('x', 1)]),
      el('p', {}, [text('Second mention.'), footnoteRef('x', 1, { rereference: 2 })]),
      footnotesSection([footnoteDef('x', [el('p', {}, [text('Shared source.')])])]),
    ],
  };

  transformSidenotes(tree);

  const smalls = tree.children.filter((n) => n.tagName === 'small');
  assert.equal(smalls.length, 1);
  // Both references still get the sidenote-ref class for styling.
  const refs = [];
  for (const p of tree.children.filter((n) => n.tagName === 'p')) {
    const a = p.children.find((c) => c.tagName === 'sup')?.children[0];
    if (a) refs.push(a);
  }
  assert.equal(refs.length, 2);
  for (const r of refs) assert.deepEqual(r.properties.className, ['sidenote-ref']);
});

test('a multi-paragraph footnote definition is flattened to phrasing content with a <br> between paragraphs', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('Claim.'), footnoteRef('multi', 1)]),
      footnotesSection([
        footnoteDef('multi', [
          el('p', {}, [text('First paragraph of the note.')]),
          el('p', {}, [text('Second paragraph of the note.')]),
        ]),
      ]),
    ],
  };

  transformSidenotes(tree);

  const small = tree.children.find((n) => n.tagName === 'small');
  assert.ok(small, 'sidenote should be inserted');
  // No nested <p> elements — small only contains phrasing content.
  assert.equal(
    small.children.some((n) => n.tagName === 'p'),
    false
  );
  assert.ok(small.children.some((n) => n.tagName === 'br'));
  const flat = JSON.stringify(small.children);
  assert.ok(flat.includes('First paragraph of the note.'));
  assert.ok(flat.includes('Second paragraph of the note.'));
});

test('a reference whose target id has no matching definition is left as a plain styled ref (no crash)', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('Dangling.'), footnoteRef('missing', 1)]),
      footnotesSection([footnoteDef('other', [el('p', {}, [text('Unrelated.')])])]),
    ],
  };

  assert.doesNotThrow(() => transformSidenotes(tree));
  assert.equal(
    tree.children.some((n) => n.tagName === 'small'),
    false
  );
});
