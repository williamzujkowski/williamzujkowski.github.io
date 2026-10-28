import { visit } from 'unist-util-visit';

/**
 * rehype plugin: margin citations from the post's own `## Sources` list.
 * OPT-IN per post: it runs only when the post's frontmatter says
 * `marginNotes: true` (schema default: false). With the flag absent the
 * transform returns before touching the tree, so every other page renders
 * byte-for-byte as it did without this plugin (vote-1793200470008-hiqgebl,
 * ratified 7-0 as OPT_IN).
 *
 * Posts here cite with ordinary inline links and end with a `## Sources`
 * list. This plugin edits no post text. At render time it:
 *
 *   1. finds the root-level `<h2>Sources</h2>` and reads every list entry
 *      after it (up to the next `<h2>`); an entry is keyed by the URL of its
 *      FIRST link (the title link);
 *   2. walks the body (root children before that heading, paragraphs and
 *      list items only); for each external link whose normalised URL equals
 *      exactly one entry's key, inserts a `remarque-sidenote-ref` right
 *      after the link and an `<aside class="remarque-sidenote">` carrying the
 *      entry's own words: title (plain text, not a second link), year,
 *      annotation, venue.
 *
 * Matching is by EXACT normalised URL only (scheme/`www.`/trailing slash/
 * fragment/utm_* ignored). Only http: and https: URLs can match; mailto:,
 * javascript:, data:, ftp: and anything else normalise to null and are
 * rejected on both the Sources side and the body side. Titles are never
 * fuzzy-matched: a wrong match would put a wrong citation in the margin. A
 * URL listed by two entries is ambiguous and gets no note. Only the first
 * link to an entry gets a note.
 *
 * ESSAY CONTRACT (remarque-tokens/essay, REMARQUE.md "Essay module"): refs
 * and notes must ALTERNATE in DOM order, ref 1, note 1, ref 2, note 2, because
 * the module numbers them with one CSS counter and labels each ref by DOM
 * position. The module's sample markup puts an <aside> after the paragraph,
 * which only alternates when a paragraph holds one citation; with several, the
 * refs would all precede the notes (the footnote plugin has this latent
 * flaw). Here each note is emitted IMMEDIATELY after its own ref, inside the
 * same paragraph or list item, as `<span class="remarque-sidenote"
 * role="note">`. This is a deliberate, documented deviation from `<aside>`:
 *
 *   - An <aside> cannot sit inside a <p> (the HTML parser closes the <p>), so
 *     strict alternation with <aside> would mean splitting the paragraph at
 *     every ref. That puts a hard line break after every citation on desktop
 *     and needs CSS (or inline-style hacks) to hide the seam.
 *   - The note content is phrasing only (text, <em>, <strong>, <code>, links),
 *     so a <span> is valid inside <p> and <li>. essay.css targets the class,
 *     not the tag, and sets `display: block` itself, so the module's layout
 *     (floated into the left gutter at >=80rem, a bordered block below) is
 *     unchanged. `role="note"` keeps it from being exposed as a landmark.
 *   - Nothing is split, moved or cloned: no word of the post changes place,
 *     and the text outside the notes is identical by construction.
 *
 * Entries whose content is not phrasing-only get no note.
 *
 * SHARED COUNTER: GFM footnotes (rehype-sidenotes) use the same counter and
 * the same "Note N" labels. A post that uses both cannot be numbered
 * correctly without rewriting the footnote plugin's output, so a post with
 * footnotes is EXCLUDED: this plugin does nothing there. Today that is one
 * post (2025-10-29-post-quantum-cryptography-homelab). Sidenote refs added
 * by anything else ahead of this plugin have the same effect.
 *
 * The Sources list itself is untouched. Feeds do not run this plugin
 * (feedContent.ts renders raw markdown with markdown-it).
 *
 * Plugin order: after rehypeSidenotes, before rehypeRaw (raw HTML is still
 * `raw` nodes here, never walked).
 */

const NOTE_PREFIX = 'src-note-';

function isEl(node, tag) {
  return !!node && node.type === 'element' && (!tag || node.tagName === tag);
}

function textOf(node) {
  if (!node) return '';
  if (node.type === 'text') return node.value;
  return (node.children || []).map(textOf).join('');
}

export function normalizeUrl(href) {
  if (typeof href !== 'string') return null;
  let u;
  try {
    u = new URL(href);
  } catch {
    return null;
  }
  if (u.protocol !== 'http:' && u.protocol !== 'https:') return null;
  const params = [...u.searchParams.entries()]
    .filter(([k]) => !/^utm_/i.test(k))
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${k}=${v}`)
    .join('&');
  const host = u.hostname.toLowerCase().replace(/^www\./, '');
  const path = u.pathname.replace(/\/+$/, '');
  return host + path + (params ? `?${params}` : '');
}

/** Entries after the Sources heading: Map<normalisedUrl, li | null(ambiguous)>. */
function readSources(tree) {
  const idx = tree.children.findIndex(
    (n) => isEl(n, 'h2') && textOf(n).trim().toLowerCase() === 'sources'
  );
  if (idx === -1) return null;
  const entries = new Map();
  for (let i = idx + 1; i < tree.children.length; i++) {
    const n = tree.children[i];
    if (isEl(n, 'h2')) break;
    if (!isEl(n, 'ul') && !isEl(n, 'ol')) continue;
    for (const li of n.children) {
      if (!isEl(li, 'li')) continue;
      let first = null;
      visit(li, (x) => isEl(x, 'a') && x.properties && x.properties.href, (x) => {
        first = x;
        return false; // visit.EXIT
      });
      const key = first && normalizeUrl(first.properties.href);
      if (!key) continue;
      entries.set(key, entries.has(key) ? null : li);
    }
  }
  return { idx, entries };
}

/**
 * Entry <li> -> inline note content. The title link is dropped in favour of
 * its own children (a second link to the same URL right next to the body
 * link would be a duplicate tab stop). It is NOT wrapped in <cite>: the
 * site's sanitize step does not allow <cite>, so the wrapper would vanish at
 * render time anyway and the review data would differ from the page.
 */
function noteContent(li) {
  let titleDone = false;
  const cloneAll = (nodes) => nodes.flatMap((node) => {
    if (node.type !== 'element') return [{ ...node }];
    if (node.tagName === 'a' && !titleDone) {
      titleDone = true;
      return cloneAll(node.children || []);
    }
    return [{ ...node, properties: { ...node.properties }, children: cloneAll(node.children || []) }];
  });
  const clone = (node) => cloneAll([node]);
  const out = [];
  const pushInline = (nodes) => {
    for (const n of nodes) {
      if (isEl(n, 'p')) {
        pushInline(n.children);
      } else if (isEl(n, 'ul') || isEl(n, 'ol')) {
        for (const sub of n.children) {
          if (!isEl(sub, 'li')) continue;
          while (out.length && out[out.length - 1].type === 'text' && /^\s*$/.test(out[out.length - 1].value)) out.pop();
          if (out.length && out[out.length - 1].type === 'text') out[out.length - 1] = { ...out[out.length - 1], value: out[out.length - 1].value.trimEnd() };
          out.push({ type: 'text', value: ' · ' });
          pushInline(sub.children);
        }
      } else if (n.type === 'text' && /^\s*$/.test(n.value)) {
        if (out.length) out.push({ type: 'text', value: ' ' });
      } else {
        out.push(...clone(n));
      }
    }
  };
  // The nested-list items must come after the first line, in order: the
  // recursion above already visits children in order.
  pushInline(li.children);
  while (out.length && out[0].type === 'text' && /^\s*$/.test(out[0].value)) out.shift();
  while (out.length && out[out.length - 1].type === 'text' && /^\s*$/.test(out[out.length - 1].value)) out.pop();
  return out;
}

/** The most words a note may add beyond its link text and still count as an echo. */
export const ECHO_MAX_NEW_WORDS = 2;
const words = (t) => new Set(t.toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean));

/** True when the note adds at most ECHO_MAX_NEW_WORDS words beyond the link's own text. */
export function isEcho(link, content) {
  const linkWords = words(textOf(link));
  let added = 0;
  for (const w of words(textOf({ type: 'root', children: content }))) {
    if (!linkWords.has(w) && ++added > ECHO_MAX_NEW_WORDS) return false;
  }
  return true;
}

const BLOCKED = new Set(['pre', 'code', 'table', 'svg', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'aside', 'figure', 'details', 'div']);
const PHRASING = new Set(['a', 'abbr', 'b', 'bdi', 'bdo', 'cite', 'code', 'data', 'del', 'dfn', 'em', 'i', 'ins', 'kbd', 'mark', 'q', 's', 'samp', 'small', 'span', 'strong', 'sub', 'sup', 'time', 'u', 'var', 'wbr']);

const isPhrasing = (nodes) =>
  nodes.every((n) => n.type !== 'element' || (PHRASING.has(n.tagName) && isPhrasing(n.children || [])));

/**
 * @param {object} tree hast root
 * @param {{ onMatch?: (m: { link: object, host: object, key: string, entry: object, serial: number }) => void }} [opts]
 *   onMatch runs for every hit BEFORE the tree is changed (used by the
 *   review generator, scripts/margin-notes-review.mjs).
 */
export function transformSourceMarginalia(tree, opts = {}) {
  if (!tree || !Array.isArray(tree.children)) return tree;
  // Footnote posts are excluded (shared counter, see header).
  let shared = tree.children.some((n) => isEl(n, 'section') && n.properties && 'dataFootnotes' in n.properties);
  if (!shared) {
    visit(tree, (n) => isEl(n, 'a') && Array.isArray(n.properties?.className) && n.properties.className.includes('remarque-sidenote-ref'), () => {
      shared = true;
      return false;
    });
  }
  if (shared) return tree;
  const sources = readSources(tree);
  if (!sources) return tree;

  // Phase 1: find hits in document order, without changing the tree.
  const used = new Set();
  const hits = [];
  const walk = (node, ancestors) => {
    if (!node.children) return;
    const limit = node === tree ? sources.idx : Infinity;
    for (let i = 0; i < node.children.length && i < limit; i++) {
      const child = node.children[i];
      if (!isEl(child) || BLOCKED.has(child.tagName)) continue;
      if (child.tagName === 'a') {
        const key = normalizeUrl(child.properties && child.properties.href);
        const li = key && sources.entries.get(key);
        if (!li || used.has(key)) continue;
        const chain = [...ancestors, node];
        let hostIdx = -1;
        for (let k = chain.length - 1; k >= 0; k--) {
          if (isEl(chain[k], 'p') || isEl(chain[k], 'li')) {
            hostIdx = k;
            break;
          }
        }
        if (hostIdx < 1) continue; // no host block (or host is the root)
        used.add(key);
        hits.push({ link: child, key, li, chain, hostIdx, content: noteContent(li) });
        continue;
      }
      walk(child, [...ancestors, node]);
    }
  };
  walk(tree, []);

  // Phase 2: ref and note go right after their link, in the link's own parent.
  // A note that only echoes its link text ("nexus-agents" beside the link
  // "nexus-agents") tells the reader nothing the sentence doesn't, so it is
  // dropped: a note must add more than ECHO_MAX_NEW_WORDS words.
  const phrasingOnly = hits.filter((h) => isPhrasing(h.content) && !isEcho(h.link, h.content));
  phrasingOnly.forEach((h, n) => {
    h.serial = n + 1;
  });
  // Report every hit before the first insertion, while host text is untouched.
  if (opts.onMatch) {
    for (const h of phrasingOnly) opts.onMatch({ link: h.link, host: h.chain[h.hostIdx], key: h.key, entry: h.li, serial: h.serial });
  }
  phrasingOnly.forEach((h) => {
    const serial = h.serial;
    const id = `${NOTE_PREFIX}${serial}`;
    const ref = {
      type: 'element',
      tagName: 'a',
      properties: {
        href: `#${id}`,
        id: `${id}-ref`,
        className: ['remarque-sidenote-ref'],
        ariaLabel: `Note ${serial}`,
        ariaDescribedBy: [id],
      },
      children: [],
    };
    const note = {
      type: 'element',
      tagName: 'span',
      properties: { className: ['remarque-sidenote'], id, role: 'note' },
      children: h.content,
    };
    const parent = h.chain[h.chain.length - 1];
    parent.children.splice(parent.children.indexOf(h.link) + 1, 0, ref, note);
  });
  return tree;
}

/** unified/rehype plugin factory: runs only for posts with `marginNotes: true`. */
export default function rehypeSourceMarginalia(options = {}) {
  return (tree, file) => {
    if (file?.data?.astro?.frontmatter?.marginNotes !== true) return;
    transformSourceMarginalia(tree, options);
  };
}
