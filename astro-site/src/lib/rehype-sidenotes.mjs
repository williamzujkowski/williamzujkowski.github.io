import { visit } from 'unist-util-visit';

/**
 * rehype plugin — Tufte/gwern-style sidenotes (issue #272, epic #269).
 *
 * SURVEY (2026-07): no maintained remark/rehype plugin does this. Checked
 * npm registry `time.modified` for remark-sidenotes, rehype-sidenotes,
 * @tufte/sidenotes, remark-sidenote, rehype-footnotes, tufte-css, sidenotes
 * (curvenote) — none fit. `rehype-footnotes` (published 2026, "maintained")
 * transforms GFM footnotes for Littlefoot.js hover/click *popovers*, which
 * leaves the footnote definition physically at the end of the document (a
 * runtime JS library fetches/positions it on interaction) — that fails the
 * hard a11y requirement here (definition must be in DOM reading order right
 * after its reference, not just reachable via JS). `tufte-css` is an
 * opinionated end-to-end stylesheet, not a composable plugin, and would
 * fight this site's own Remarque design tokens. `remark-sidenote` and the
 * `sidenotes` npm package are unrelated tools (source-offset mapping for a
 * commenting UI, and a Google-Docs-style React commenting library,
 * respectively — name collision only). Verdict: hand-roll, per the issue's
 * vote condition.
 *
 * Astro's markdown pipeline runs GFM footnotes by default (mdast-util-to-hast
 * `footer()` — see node_modules/mdast-util-to-hast/lib/footer.js): every
 * `[^n]` reference becomes `<sup><a data-footnote-ref href="#user-content-fn-n"
 * id="user-content-fnref-n">n</a></sup>` inline, and ALL definitions are
 * collected into one `<section data-footnotes>` appended at the very end of
 * the document — exactly the "read the whole footnotes section separately"
 * pattern sidenotes are meant to replace.
 *
 * This plugin, run as a rehype step (after that hast tree exists):
 *   1. Reads `<section data-footnotes>`'s `<li>` definitions into a map,
 *      keyed by their `id` (e.g. "user-content-fn-grqc-timeline"), and
 *      removes GFM's `↩` backreference link from each (see rationale below).
 *   2. Removes the `<section data-footnotes>` from the tree — its content
 *      is being relocated, not duplicated.
 *   3. Walks the top-level flow (paragraphs, blockquotes, etc.) in document
 *      order, and for every footnote reference found, tags it
 *      `class="sidenote-ref"` and inserts an `<aside class="sidenote">`
 *      element as the NEXT SIBLING of the top-level block that contains the
 *      reference — i.e. immediately after the paragraph that cited it, in
 *      real DOM order. Screen readers hit the note right where the citation
 *      happens; no separate "jump to footnotes" detour.
 *
 * Dangling ARIA (fixed): GFM stamps every footnote reference with
 * `aria-describedby="footnote-label"`, pointing at the `<h2 id=
 * "footnote-label">Footnotes</h2>` inside the section this plugin removes.
 * Left alone, that's a broken ARIA reference — assistive tech would resolve
 * `aria-describedby` to nothing. This plugin strips it from every reference
 * (removing the whole section it "describes" makes the attribute
 * meaningless anyway; the note is now immediately adjacent and
 * self-explanatory). The `href`/`id` pair that makes the reference actually
 * NAVIGATE to its note, by contrast, is real and kept: the moved element
 * reuses the original definition id, so `href="#user-content-fn-x"` still
 * resolves to a real element with `id="user-content-fn-x"` after the move —
 * verified against the built HTML, not just asserted (see astro-site/tests/
 * e2e/sidenotes.spec.ts's DOM-order and click-navigation tests).
 *
 * Backreference links (↩): dropped, not preserved. GFM's backref exists so a
 * reader who jumped to a footnote at the bottom of a long document can jump
 * back to where they were reading. Once the note is relocated to sit a few
 * pixels below its own reference, that round trip is already zero-distance —
 * keeping the arrow would just be visual noise pointing at text the reader
 * can already see. (Tufte/gwern-style margin notes don't carry backref
 * arrows either, for the same reason.)
 *
 * Element choice — `<aside>`, not `<small>` (fixed): footnote definitions
 * can be arbitrary block content — multiple paragraphs, lists, blockquotes —
 * and HTML5's content model for `<small>` is phrasing content ONLY, so
 * nesting a `<p>` (or worse, a `<ul>`) inside one is invalid markup. `<aside>`
 * permits flow content (everything `<small>` allows, plus block elements),
 * so footnote content nests as-is with no lossy flattening step required —
 * simpler code and correct for content this plugin doesn't fully control
 * (it's whatever an author writes in a `[^n]:` definition). `<aside>` is
 * also the closer HTML5 semantic match for "tangentially related content
 * set apart from the main flow", which is exactly what a margin note is;
 * `<small>` is meant for fine-print/legal-disclaimer-style annotations, a
 * narrower fit. The leading mono-voice number stays inline with the note's
 * OPENING text either way — it's injected as a leading child of the first
 * paragraph (or directly, if the content isn't paragraph-wrapped) rather
 * than as a block-level sibling, so the visual "1 Note text..." pairing
 * from the `<small>` version is unchanged.
 *
 * Layout (CSS, not this file): `.sidenote` is a small-print block right in
 * the text flow by default (the same place GFM would render it, just
 * per-paragraph instead of end-of-document) — this doubles as the narrow-
 * viewport fallback with zero extra markup. At >=1280px, global.css floats
 * it into the LEFT rail of `.post-article`'s existing 3-column grid (the
 * TOC owns the right rail — #299) via a negative-margin float, no JS.
 *
 * If a footnote is referenced more than once (rare), only the FIRST
 * reference gets a sidenote inserted after it; later references still get
 * `.sidenote-ref` styling but no duplicate note — two copies of the same
 * margin note fighting for space reads worse than one.
 *
 * Exports the pure tree transform (`transformSidenotes`) separately from the
 * unified-plugin factory so it can be unit-tested against a hand-built hast
 * tree without spinning up a full unified/remark/rehype pipeline — see
 * tests/unit/rehype-sidenotes.test.mjs.
 */

function isElement(node, tagName) {
  return !!node && node.type === 'element' && (!tagName || node.tagName === tagName);
}

function hasProperty(node, key) {
  return isElement(node) && !!node.properties && Object.prototype.hasOwnProperty.call(node.properties, key);
}

function isBackref(node) {
  return isElement(node, 'a') && hasProperty(node, 'dataFootnoteBackref');
}

/**
 * Drop GFM backreference anchors from a footnote definition's children.
 * mdast-util-to-hast appends the backref either into the trailing <p>'s
 * children or, if the definition doesn't end in a <p>, directly onto the
 * definition's own children array — handle both, one level deep.
 */
function stripBackrefs(nodes) {
  return nodes
    .filter((n) => !isBackref(n))
    .map((n) => {
      if (!isElement(n) || !Array.isArray(n.children)) return n;
      const kids = n.children.filter((c) => !isBackref(c));
      while (
        kids.length > 0 &&
        kids[kids.length - 1].type === 'text' &&
        /^\s*$/.test(kids[kids.length - 1].value)
      ) {
        kids.pop();
      }
      return { ...n, children: kids };
    });
}

/**
 * mdast-util-to-hast's `state.wrap(content, true)` (footer.js, `loose:
 * true`) pads a footnote definition's block children with leading/trailing
 * `\n` text nodes — e.g. a single-paragraph definition's `li.children` is
 * actually `['\n', <p>, '\n']`, NOT `[<p>]`. Left alone, that leading
 * whitespace node — not the `<p>` — would be `contentNodes[0]`, silently
 * breaking `withLeadingNumber`'s "does this start with a paragraph?" check
 * (verified against the actual built HTML output, not just inferred).
 */
function trimWhitespaceEdges(nodes) {
  let start = 0;
  let end = nodes.length;
  while (start < end && nodes[start].type === 'text' && /^\s*$/.test(nodes[start].value)) start++;
  while (end > start && nodes[end - 1].type === 'text' && /^\s*$/.test(nodes[end - 1].value)) end--;
  return nodes.slice(start, end);
}

/**
 * Inject the mono-voice number marker (+ a following space) so it reads
 * inline with the note's opening text — "1 Some source, description." — the
 * same visual pairing as before, but without requiring the note content to
 * be flattened to phrasing-only first (see the `<aside>` rationale above).
 * If the content starts with a `<p>`, the marker becomes that paragraph's
 * leading children; otherwise (content is already bare phrasing, or starts
 * with some other block) it's just prepended to the content array — `<aside>`
 * permits flow content, so bare text/inline elements are valid siblings of
 * block elements either way.
 */
function withLeadingNumber(numberSpan, contentNodes) {
  const lead = [numberSpan, { type: 'text', value: ' ' }];
  if (contentNodes.length > 0 && isElement(contentNodes[0], 'p')) {
    const [first, ...rest] = contentNodes;
    return [{ ...first, children: [...lead, ...first.children] }, ...rest];
  }
  return [...lead, ...contentNodes];
}

export function transformSidenotes(tree) {
  if (!tree || !Array.isArray(tree.children)) return tree;

  const footnoteSectionIndex = tree.children.findIndex(
    (n) => isElement(n, 'section') && hasProperty(n, 'dataFootnotes')
  );
  if (footnoteSectionIndex === -1) return tree; // no GFM footnotes in this document

  const footnoteSection = tree.children[footnoteSectionIndex];
  const ol = (footnoteSection.children || []).find((n) => isElement(n, 'ol'));
  const noteContentById = new Map();
  if (ol) {
    for (const li of ol.children) {
      if (!isElement(li, 'li') || !li.properties || !li.properties.id) continue;
      noteContentById.set(li.properties.id, trimWhitespaceEdges(stripBackrefs(li.children || [])));
    }
  }

  // Content is being relocated inline, not duplicated — remove the original.
  tree.children.splice(footnoteSectionIndex, 1);

  const insertions = []; // { afterIndex, sequence, node }
  const seen = new Set();
  let sequence = 0;

  tree.children.forEach((child, index) => {
    visit(
      child,
      (n) => isElement(n, 'a') && hasProperty(n, 'dataFootnoteRef'),
      (refNode) => {
        const existingClass = Array.isArray(refNode.properties.className)
          ? refNode.properties.className
          : [];
        refNode.properties.className = [...existingClass, 'sidenote-ref'];

        // GFM points this at the "Footnotes" <h2> inside the section this
        // plugin deletes — leaving it would be a dangling ARIA reference
        // (assistive tech resolves aria-describedby to nothing). The note
        // itself is now immediately adjacent, so no replacement is needed.
        delete refNode.properties.ariaDescribedBy;

        const href = refNode.properties.href || '';
        const targetId = href.startsWith('#') ? href.slice(1) : null;
        if (!targetId || seen.has(targetId)) return;

        const content = noteContentById.get(targetId);
        if (!content) return;
        seen.add(targetId);

        const number =
          refNode.children && refNode.children[0] && refNode.children[0].type === 'text'
            ? refNode.children[0].value
            : '';

        // Reuse the original footnote-definition id for the moved element,
        // and make the reference's href point at it explicitly — the
        // reference still NAVIGATES to a real element after the move
        // (unlike the aria-describedby link above, which pointed at
        // something now deleted).
        const noteId = targetId;
        refNode.properties.href = `#${noteId}`;

        const numberSpan = {
          type: 'element',
          tagName: 'span',
          properties: { className: ['sidenote-number'], ariaHidden: 'true' },
          children: [{ type: 'text', value: number }],
        };

        insertions.push({
          afterIndex: index,
          sequence: sequence++,
          node: {
            type: 'element',
            tagName: 'aside',
            // `<aside>`'s IMPLICIT role is `complementary` — a landmark.
            // A post with several footnotes would otherwise scatter that
            // many unlabeled landmark regions through `<main>`, which axe
            // correctly flags (landmark-is-top-level: "contained in
            // another landmark") and which is genuinely bad for landmark
            // navigation (a screen-reader user jumping by landmark would
            // hit 5+ identical, unlabeled "complementary" stops).
            // `role="note"` overrides that: broadly-supported, explicitly
            // non-landmark, and the closest plain-ARIA semantic match for
            // "an annotation attached to the surrounding content" — the
            // DPUB-ARIA `doc-footnote` role is more precise but has
            // thinner AT support, not worth it for a role whose only job
            // here is "stop being a landmark".
            properties: { className: ['sidenote'], id: noteId, role: 'note' },
            children: withLeadingNumber(numberSpan, content),
          },
        });
      }
    );
  });

  // Splice back-to-front so an earlier insertion doesn't shift the index a
  // later one was computed against. When two references share the same
  // `afterIndex` (two `[^n]` citations inside one paragraph), splicing them
  // both at `afterIndex + 1` means whichever is spliced LAST ends up
  // closest to the paragraph — so ties are broken by descending `sequence`
  // (process the later citation first) to preserve citation order in the
  // final DOM.
  insertions
    .sort((a, b) => b.afterIndex - a.afterIndex || b.sequence - a.sequence)
    .forEach(({ afterIndex, node }) => {
      tree.children.splice(afterIndex + 1, 0, node);
    });

  return tree;
}

/** unified/rehype plugin factory — wire into astro.config.mjs `markdown.rehypePlugins`. */
export default function rehypeSidenotes() {
  return (tree) => {
    transformSidenotes(tree);
  };
}
