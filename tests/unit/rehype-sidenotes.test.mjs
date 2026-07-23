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
//
// Updated for issue #378 (migration to remarque-tokens/essay): the plugin
// now emits `remarque-sidenote`/`remarque-sidenote-ref` class names, unwraps
// GFM's `<sup>` reference wrapper, blanks the reference's own visible number
// (essay.css numbers via a CSS counter instead), and points a resolvable
// reference's `aria-describedby` at the note's id rather than always
// deleting it. See rehype-sidenotes.mjs's header comment for the full
// rationale.

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

/**
 * A single GFM footnote definition `<li>`, as footer() emits it —
 * including the leading/trailing/between-siblings `\n` text nodes that
 * `state.wrap(content, true)` (mdast-util-to-hast, `loose: true`) actually
 * adds. A real single-paragraph definition's `li.children` is
 * `['\n', <p>, '\n']`, NOT `[<p>]` — the earlier version of this fixture
 * omitted that whitespace and consequently didn't catch a real bug that
 * only showed up against the real pipeline's output. See
 * `trimWhitespaceEdges` in rehype-sidenotes.mjs.
 */
function footnoteDef(id, paragraphs) {
  const backref = el(
    'a',
    { href: `#user-content-fnref-${id}`, dataFootnoteBackref: '', className: ['data-footnote-backref'] },
    [text('↩')]
  );
  const withBackref = paragraphs.map((p, i) =>
    i === paragraphs.length - 1 ? el('p', p.properties, [...p.children, text(' '), backref]) : p
  );
  const wrapped = [text('\n')];
  withBackref.forEach((node, i) => {
    if (i > 0) wrapped.push(text('\n'));
    wrapped.push(node);
  });
  if (withBackref.length > 0) wrapped.push(text('\n'));
  return el('li', { id: `user-content-fn-${id}` }, wrapped);
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

test('moves a single footnote inline right after its paragraph, unwrapped from <sup>', () => {
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
  assert.equal(tree.children[1].tagName, 'aside');
  assert.deepEqual(tree.children[1].properties.className, ['remarque-sidenote']);
  assert.equal(tree.children[1].properties.id, 'user-content-fn-rand');
  // <aside>'s implicit role is the `complementary` landmark — override it
  // with role="note" so a post with several footnotes doesn't scatter
  // that many unlabeled landmarks through <main> (axe: landmark-is-top-level).
  assert.equal(tree.children[1].properties.role, 'note');
  assert.equal(tree.children[2].tagName, 'p'); // the unrelated paragraph, untouched

  // The reference is unwrapped from GFM's <sup> — it's now a direct child
  // of the paragraph, not nested inside a <sup> element (essay.css's
  // .remarque-sidenote-ref already carries vertical-align: super itself).
  const ref = tree.children[0].children[1];
  assert.equal(ref.tagName, 'a');
  assert.deepEqual(ref.properties.className, ['remarque-sidenote-ref']);
  assert.equal(ref.properties.href, '#user-content-fn-rand');
  // essay.css numbers via a CSS counter (counter-increment + ::after) —
  // GFM's own visible digit is blanked so the two don't double-number.
  assert.deepEqual(ref.children, []);
  // aria-describedby now points at the note's own (real, resolvable) id,
  // instead of GFM's dangling pointer at the deleted Footnotes <h2>.
  assert.deepEqual(ref.properties.ariaDescribedBy, ['user-content-fn-rand']);
  // Blanking ref.children (above) leaves no accessible name of its own —
  // aria-label supplies one (a real axe run against the built site caught
  // the missing-name case as a link-name violation; see this file's header
  // comment). Numbered independently of the visible CSS-counter digit, but
  // in the same first-citation order, so it always matches.
  assert.equal(ref.properties.ariaLabel, 'Note 1');

  // Sidenote's content is the footnote def's paragraph, unmodified except
  // for backref-stripping — no injected leading-number span (the module's
  // CSS ::before supplies the number, not this plugin).
  assert.equal(tree.children[1].children.length, 1);
  const notePara = tree.children[1].children[0];
  assert.equal(notePara.tagName, 'p');
  assert.equal(notePara.children[0].type, 'text');
  assert.equal(notePara.children[0].value, 'RAND Corporation analysis.');

  // Backref arrow was stripped — note text shouldn't carry a "back to
  // reference" link (redundant once the note sits next to its reference).
  assert.equal(JSON.stringify(notePara).includes('dataFootnoteBackref'), false);
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
    ['p', 'aside', 'p', 'aside']
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
    ['p', 'aside', 'aside']
  );
  // Citation order preserved: A's note comes before B's note, matching the
  // order the two `[^n]` refs appear in the paragraph.
  assert.equal(tree.children[1].properties.id, 'user-content-fn-a');
  assert.equal(tree.children[2].properties.id, 'user-content-fn-b');
});

test('a footnote referenced twice only inserts one sidenote, and the repeat gets the --repeat modifier class', () => {
  const tree = {
    type: 'root',
    children: [
      el('p', {}, [text('First mention.'), footnoteRef('x', 1)]),
      el('p', {}, [text('Second mention.'), footnoteRef('x', 1, { rereference: 2 })]),
      footnotesSection([footnoteDef('x', [el('p', {}, [text('Shared source.')])])]),
    ],
  };

  transformSidenotes(tree);

  const asides = tree.children.filter((n) => n.tagName === 'aside');
  assert.equal(asides.length, 1);

  const refs = tree.children
    .filter((n) => n.tagName === 'p')
    .map((p) => p.children.find((c) => c.tagName === 'a' && c.properties?.dataFootnoteRef))
    .filter(Boolean);
  assert.equal(refs.length, 2);

  const [firstRef, repeatRef] = refs;
  assert.deepEqual(firstRef.properties.className, ['remarque-sidenote-ref']);
  assert.deepEqual(repeatRef.properties.className, [
    'remarque-sidenote-ref',
    'remarque-sidenote-ref--repeat',
  ]);

  // Both point at the same real note — aria-describedby doesn't require
  // adjacency, so the repeat citation gets it too (the note just isn't
  // physically next to it).
  for (const r of refs) {
    assert.deepEqual(r.properties.ariaDescribedBy, ['user-content-fn-x']);
    assert.deepEqual(r.children, []);
    // Both citations of the same note carry the SAME aria-label — the
    // repeat doesn't advance the shared counter, so its accessible name
    // shouldn't advance either.
    assert.equal(r.properties.ariaLabel, 'Note 1');
  }
});

test('a multi-paragraph footnote definition keeps its paragraph structure (no lossy flattening, no injected number span)', () => {
  // <aside> permits flow content, so unlike the earlier <small>-based
  // design, block content (multiple <p>, or a <ul>/<blockquote>) doesn't
  // need to be flattened to phrasing-only to stay valid HTML.
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

  const aside = tree.children.find((n) => n.tagName === 'aside');
  assert.ok(aside, 'sidenote should be inserted');
  // Both source paragraphs survive as real <p> elements (possibly with a
  // harmless whitespace-only text node between them, mirroring
  // mdast-util-to-hast's own `state.wrap` behavior — that's valid flow
  // content inside <aside>, not something this plugin needs to strip).
  const paragraphs = aside.children.filter((n) => n.tagName === 'p');
  assert.equal(paragraphs.length, 2);
  assert.equal(aside.children[0].tagName, 'p'); // no leading whitespace node survives
  assert.equal(aside.children[aside.children.length - 1].tagName, 'p'); // nor a trailing one
  // No leading-number span is injected anywhere — essay.css's `::before`
  // on `.remarque-sidenote` itself supplies the generated number now.
  assert.equal(paragraphs[0].children[0].type, 'text');
  assert.equal(paragraphs[0].children[0].value, 'First paragraph of the note.');
  assert.ok(JSON.stringify(paragraphs[1]).includes('Second paragraph of the note.'));
  assert.equal(JSON.stringify(aside).includes('sidenote-number'), false);
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
    tree.children.some((n) => n.tagName === 'aside'),
    false
  );
  // Even with no matching definition, the reference is still unwrapped,
  // classed, and blanked — only aria-describedby (nothing to point at) and
  // the aside insertion are skipped. It still gets a generic fallback
  // aria-label rather than being left as an unlabeled, focusable link.
  const ref = tree.children[0].children[1];
  assert.equal(ref.tagName, 'a');
  assert.deepEqual(ref.properties.className, ['remarque-sidenote-ref']);
  assert.deepEqual(ref.children, []);
  assert.equal('ariaDescribedBy' in ref.properties, false);
  assert.equal(ref.properties.ariaLabel, 'Footnote reference');
});
