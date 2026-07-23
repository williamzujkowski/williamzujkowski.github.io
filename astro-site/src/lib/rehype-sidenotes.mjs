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
 * MODULE MIGRATION (issue #378): this plugin now emits the markup contract
 * of `remarque-tokens/essay` (graduated from this same plugin upstream via
 * remarque#52) instead of this site's own former `.sidenote`/`.toc` CSS,
 * which is deleted. The two things that change shape here:
 *
 *   1. Numbering is no longer authored by this plugin. `essay.css` numbers
 *      sidenotes with CSS counters (`counter-reset` on `.remarque-prose`,
 *      `counter-increment` on `.remarque-sidenote-ref`, generated content
 *      on both `::after`/`::before`) — this plugin used to inject a literal
 *      `<span class="sidenote-number">`, taken from GFM's own reference
 *      number text. That text is now BLANKED on every reference (see
 *      `refNode.children = []` below) so the two mechanisms don't both
 *      render a digit (double numbering, the exact failure mode issue #378
 *      calls out). A repeat citation of an already-noted footnote gets the
 *      module's `remarque-sidenote-ref--repeat` modifier class, which the
 *      module's CSS uses to skip `counter-increment` for that instance
 *      (`counter-increment: none`) — the shared counter isn't advanced for
 *      a note that was already printed, same rule as before, now enforced
 *      by CSS instead of a `seen` check gating a literal number.
 *   2. GFM wraps every footnote reference in `<sup>` (`<sup><a
 *      data-footnote-ref>1</a></sup>`); the module's own reference markup
 *      is a bare `<a class="remarque-sidenote-ref">` with `vertical-align:
 *      super` baked into the class itself, so the `<sup>` wrapper is
 *      unwrapped (not just restyled) — keeping it would compound two
 *      independent `vertical-align: super` contexts.
 *
 * A11y regression found and fixed during the migration (not part of the
 * module's own contract, which shows the reference as a bare, empty `<a>`):
 * blanking the reference's visible text for CSS-counter numbering leaves an
 * empty, focusable link with no accessible name — real axe runs against the
 * built site caught this as a `link-name` violation (WCAG 4.1.2 / 2.4.4).
 * `aria-describedby` alone doesn't fix it (it adds a description, not a
 * name). This plugin adds `aria-label="Note N"`, where N is assigned in the
 * same first-citation order the CSS counter itself advances in, so the
 * label always matches what's visually rendered without this plugin having
 * to author any VISIBLE number again.
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
 *   3. Unwraps every footnote reference from GFM's `<sup>` wrapper (see
 *      "MODULE MIGRATION" above).
 *   4. Walks the top-level flow (paragraphs, blockquotes, etc.) in document
 *      order, and for every footnote reference found, tags it
 *      `class="remarque-sidenote-ref"` (plus `remarque-sidenote-ref--repeat`
 *      on a second-or-later citation of the same note) and inserts an
 *      `<aside class="remarque-sidenote" role="note">` element as the NEXT
 *      SIBLING of the top-level block that contains the reference — i.e.
 *      immediately after the paragraph that cited it, in real DOM order.
 *      Screen readers hit the note right where the citation happens; no
 *      separate "jump to footnotes" detour.
 *
 * Dangling ARIA (fixed): GFM stamps every footnote reference with
 * `aria-describedby="footnote-label"`, pointing at the `<h2 id=
 * "footnote-label">Footnotes</h2>` inside the section this plugin removes.
 * Left alone, that's a broken ARIA reference — assistive tech would resolve
 * `aria-describedby` to nothing. This plugin instead repoints it at the
 * note's own id when a note exists (the module's markup contract calls this
 * out as "optional but recommended") — the note is a real, resolvable
 * element, either immediately adjacent (first citation) or elsewhere in the
 * document (a repeat citation, where `aria-describedby` doesn't require
 * adjacency to be valid). For a reference whose target has no matching
 * definition at all, the attribute is dropped outright — nothing to point
 * at either way.
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
 * narrower fit. The module's own `::before` generated content puts the
 * visible number ahead of the note's content — for a single paragraph of
 * note text that reads inline ("1 Note text..."); for a multi-paragraph
 * note it reads as a small label line above the first paragraph. Both are
 * essay.css's own documented behavior, not something this plugin controls.
 *
 * Layout (CSS, not this file): `.remarque-sidenote` renders as a small-print
 * block right in the text flow by default (the same place GFM would render
 * it, just per-paragraph instead of end-of-document) — this doubles as the
 * narrow-viewport fallback with zero extra markup. At >=80rem, essay.css
 * floats it into the LEFT rail of `.remarque-essay`'s existing 3-column
 * grid (the TOC owns the right rail) via a negative-margin float, no JS.
 *
 * If a footnote is referenced more than once (rare), only the FIRST
 * reference gets a sidenote inserted after it; later references still get
 * `.remarque-sidenote-ref` (+ `--repeat`) styling but no duplicate note —
 * two copies of the same margin note fighting for space reads worse than
 * one.
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
 * whitespace node would render as a spurious blank line ahead of the
 * `<aside>`'s real content (verified against the actual built HTML output,
 * not just inferred).
 */
function trimWhitespaceEdges(nodes) {
  let start = 0;
  let end = nodes.length;
  while (start < end && nodes[start].type === 'text' && /^\s*$/.test(nodes[start].value)) start++;
  while (end > start && nodes[end - 1].type === 'text' && /^\s*$/.test(nodes[end - 1].value)) end--;
  return nodes.slice(start, end);
}

/**
 * Unwrap every footnote reference from GFM's `<sup>` wrapper, in place.
 * `<sup>` always wraps exactly one child (the reference `<a>`) in
 * mdast-util-to-hast's output — mutate the `<sup>` node itself into that
 * `<a>` (same object identity, so no parent/index bookkeeping is needed)
 * rather than splicing it out of its parent's children array. See the
 * "MODULE MIGRATION" note in this file's header comment for why: the
 * module's `.remarque-sidenote-ref` class already carries `vertical-align:
 * super`, so leaving the GFM `<sup>` in place would nest two independent
 * superscript contexts.
 */
function unwrapFootnoteRefSup(tree) {
  visit(
    tree,
    (n) =>
      isElement(n, 'sup') &&
      Array.isArray(n.children) &&
      n.children.length === 1 &&
      isElement(n.children[0], 'a') &&
      hasProperty(n.children[0], 'dataFootnoteRef'),
    (supNode) => {
      const anchor = supNode.children[0];
      supNode.tagName = anchor.tagName;
      supNode.properties = anchor.properties;
      supNode.children = anchor.children;
    }
  );
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

  unwrapFootnoteRefSup(tree);

  const insertions = []; // { afterIndex, sequence, node }
  const seen = new Set();
  const noteNumberByTarget = new Map();
  let sequence = 0;
  let noteNumber = 0;

  tree.children.forEach((child, index) => {
    visit(
      child,
      (n) => isElement(n, 'a') && hasProperty(n, 'dataFootnoteRef'),
      (refNode) => {
        const href = refNode.properties.href || '';
        const targetId = href.startsWith('#') ? href.slice(1) : null;
        const content = targetId ? noteContentById.get(targetId) : undefined;
        const isRepeat = !!targetId && seen.has(targetId);

        const existingClass = Array.isArray(refNode.properties.className)
          ? refNode.properties.className
          : [];
        const classes = [...existingClass, 'remarque-sidenote-ref'];
        if (isRepeat) classes.push('remarque-sidenote-ref--repeat');
        refNode.properties.className = classes;

        // essay.css generates the visible number via a CSS counter
        // (counter-increment on this class, `::after { content:
        // counter(...) }`) — GFM's own reference text (a plain digit) must
        // be blanked or the two would double-number every citation.
        refNode.children = [];

        // Blanking the ref's text (above) leaves it with no accessible
        // name — CSS generated content (`::after`) is not reliably exposed
        // to assistive tech, so axe correctly flags an empty, focusable
        // `<a>` as a `link-name` (WCAG 4.1.2 / 2.4.4) violation. `aria-
        // describedby` (below) only adds a DESCRIPTION, not a NAME, so it
        // doesn't fix this on its own. `aria-label` supplies the name;
        // its number is assigned in the same first-citation order the CSS
        // counter itself advances in (incremented only when a new target
        // is first seen, exactly like the counter), so it always matches
        // what's visually rendered.
        if (targetId && content) {
          if (!noteNumberByTarget.has(targetId)) {
            noteNumber += 1;
            noteNumberByTarget.set(targetId, noteNumber);
          }
          refNode.properties.ariaLabel = `Note ${noteNumberByTarget.get(targetId)}`;
        } else {
          refNode.properties.ariaLabel = 'Footnote reference';
        }

        if (targetId && content) {
          // The note is a real, resolvable element (adjacent for a first
          // citation, elsewhere in the document for a repeat) — unlike
          // GFM's original footnote-label pointer, which this plugin
          // deletes along with the rest of the footnotes section.
          refNode.properties.ariaDescribedBy = [targetId];
        } else {
          delete refNode.properties.ariaDescribedBy;
        }

        if (!targetId || isRepeat || !content) return;
        seen.add(targetId);

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
            properties: { className: ['remarque-sidenote'], id: targetId, role: 'note' },
            children: content,
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
