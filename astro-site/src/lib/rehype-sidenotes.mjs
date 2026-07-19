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
 *      `class="sidenote-ref"` and inserts a `<small class="sidenote">`
 *      element as the NEXT SIBLING of the top-level block that contains the
 *      reference — i.e. immediately after the paragraph that cited it, in
 *      real DOM order. Screen readers hit the note right where the citation
 *      happens; no separate "jump to footnotes" detour.
 *
 * Backreference links (↩): dropped, not preserved. GFM's backref exists so a
 * reader who jumped to a footnote at the bottom of a long document can jump
 * back to where they were reading. Once the note is relocated to sit a few
 * pixels below its own reference, that round trip is already zero-distance —
 * keeping the arrow would just be visual noise pointing at text the reader
 * can already see. (Tufte/gwern-style margin notes don't carry backref
 * arrows either, for the same reason.)
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
 * `<small>` is phrasing content only (HTML5) — flatten a footnote
 * definition's block children (almost always a single `<p>`) into inline
 * content so the sidenote markup stays valid. Multiple paragraphs (a
 * footnote spanning >1 <p>) get a `<br>` between them rather than being
 * silently dropped.
 */
function flattenToPhrasing(nodes) {
  const out = [];
  for (const n of nodes) {
    if (isElement(n, 'p')) {
      if (out.length > 0) out.push({ type: 'element', tagName: 'br', properties: {}, children: [] });
      out.push(...n.children);
    } else if (n.type === 'text' && /^\s*$/.test(n.value)) {
      // whitespace-only text between block siblings — drop it
    } else {
      out.push(n);
    }
  }
  return out;
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
      noteContentById.set(li.properties.id, stripBackrefs(li.children || []));
    }
  }

  // Content is being relocated inline, not duplicated — remove the original.
  tree.children.splice(footnoteSectionIndex, 1);

  const insertions = []; // { afterIndex, node }
  const seen = new Set();

  tree.children.forEach((child, index) => {
    visit(
      child,
      (n) => isElement(n, 'a') && hasProperty(n, 'dataFootnoteRef'),
      (refNode) => {
        const existingClass = Array.isArray(refNode.properties.className)
          ? refNode.properties.className
          : [];
        refNode.properties.className = [...existingClass, 'sidenote-ref'];

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

        insertions.push({
          afterIndex: index,
          node: {
            type: 'element',
            tagName: 'small',
            // Reuse the original footnote-definition id: the reference's
            // href already points at it, so it keeps resolving after the
            // element moves — no extra id bookkeeping needed.
            properties: { className: ['sidenote'], id: targetId },
            children: [
              {
                type: 'element',
                tagName: 'span',
                properties: { className: ['sidenote-number'], ariaHidden: 'true' },
                children: [{ type: 'text', value: number }],
              },
              { type: 'text', value: ' ' },
              ...flattenToPhrasing(content),
            ],
          },
        });
      }
    );
  });

  // Splice back-to-front so an earlier insertion doesn't shift the index
  // a later one was computed against.
  insertions
    .sort((a, b) => b.afterIndex - a.afterIndex)
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
