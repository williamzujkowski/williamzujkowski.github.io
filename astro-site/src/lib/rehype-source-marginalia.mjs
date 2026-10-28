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
 *      exactly one entry's key, inserts a `remarque-sidenote-ref` and a
 *      `remarque-sidenote` carrying the entry's own words (title as plain
 *      text, not a second link; year, annotation, venue) at the END OF THE
 *      SENTENCE that holds the link (see "Placement" below).
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
 * PLACEMENT: a ref and note placed right after the link split the sentence
 * ("...from RouteLLM's [note] cost-quality tradeoff to..."), and at narrow
 * widths, where the note is an inline block, that breaks the reader's
 * sentence in two. So they go at the END OF THE SENTENCE: after the terminal
 * `.`, `?` or `!` and any closing quote or bracket, before the next sentence.
 * A sentence ends at terminal punctuation followed by whitespace and then an
 * uppercase letter, an opening quote or bracket, a digit, or the end of the
 * host block. Not an end: abbreviations (e.g., i.e., et al., vs., etc., Fig.,
 * Dr., single initials, U.S.-style dotted forms, and "No.", "Vol.", "pp.",
 * "Ch.", "Sec.", "Eq." or "Art." before a digit),
 * decimals and versions (no whitespace follows the dot), and anything inside
 * code. With no end in the host block, the pair goes at the end of the
 * block's inline content. The scan runs over the host's flattened inline text
 * (nested lists excluded), so it crosses em/strong/links; an insertion point
 * at the end of an inline element is lifted out to the parent, and never
 * lands inside another link. Several links in one sentence share ONE ref and
 * ONE note (one number): the note carries each matched entry in link order,
 * separated by <br>. (Two refs at one spot read as a stray digit on its own
 * line at narrow widths and touch each other, failing target-size, at wide.) Only a text node may be split (its words stay in order), so the text
 * outside the notes is unchanged.
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


// ---- Sentence-end placement ------------------------------------------------

const TERMINAL = new Set(['.', '?', '!', '…']);
const CLOSERS = new Set(['"', "'", '”', '’', ')', ']', '»']);
const OPENERS = /["'“‘([«]/;
const OPAQUE_TAGS = new Set(['code', 'kbd', 'samp', 'br']);
// A single capital initial before the dot ("J. Smith") is not a sentence end.
const SINGLE_INITIAL = /(?:^|[^\p{L}\p{N}])\p{Lu}\.$/u;

/** Flatten a host's inline content to chars; code is one opaque placeholder, nested lists are skipped. */
function flattenHost(host, link) {
  const chars = []; // { ch, node, off, anc }
  let linkStart = -1;
  let linkEnd = -1;
  const walk = (node, anc) => {
    for (const child of node.children || []) {
      if (child === link) linkStart = chars.length;
      if (child.type === 'text') {
        for (let off = 0; off < child.value.length; off++) chars.push({ ch: child.value[off], node: child, off, anc });
      } else if (isEl(child)) {
        if (child.tagName === 'ul' || child.tagName === 'ol') continue;
        if (OPAQUE_TAGS.has(child.tagName)) {
          chars.push({ ch: child.tagName === 'br' ? ' ' : '\u0000', node: child, off: -1, anc });
        } else {
          walk(child, [...anc, child]);
        }
      }
      if (child === link) linkEnd = chars.length;
    }
  };
  walk(host, [host]);
  return { chars, linkStart, linkEnd };
}

const hasContent = (n) => (n.type === 'text' ? /\S/.test(n.value) : isEl(n));

/**
 * Where an insertion after chars[k] goes: { parent, after, split }. `after` is
 * the node to insert after in `parent`; `split` is a text node (and offset) to
 * cut first. Climbs out of an inline element when nothing follows k inside it.
 * Returns null when the spot would be inside a link.
 */
function locate(chars, k, host) {
  const c = chars[k];
  let node = c.node;
  let anc = c.anc;
  let split = null;
  if (c.off >= 0 && c.off + 1 < node.value.length && /\S/.test(node.value.slice(c.off + 1))) {
    split = { node, off: c.off + 1 };
  }
  const trailing = (parent, n) => {
    const sibs = parent.children;
    return sibs.slice(sibs.indexOf(n) + 1).some(hasContent);
  };
  if (!split) {
    while (anc.length > 1 && !trailing(anc[anc.length - 1], node)) {
      node = anc[anc.length - 1];
      anc = anc.slice(0, -1);
    }
  }
  if (anc.some((a) => a !== host && a.tagName === 'a')) return null;
  return { parent: anc[anc.length - 1], after: node, split };
}

/** Does a sentence end at chars[k] (a terminal)? Returns the index of the last closer, or -1. */
function sentenceEndAt(chars, k) {
  if (!TERMINAL.has(chars[k].ch)) return -1;
  let e = k;
  while (e + 1 < chars.length && TERMINAL.has(chars[e + 1].ch)) e++;
  while (e + 1 < chars.length && CLOSERS.has(chars[e + 1].ch)) e++;
  let j = e + 1;
  let sawSpace = false;
  while (j < chars.length && /\s/.test(chars[j].ch)) {
    sawSpace = true;
    j++;
  }
  if (j < chars.length) {
    if (!sawSpace) return -1;
    const next = chars[j].ch;
    if (!(/\p{Lu}/u.test(next) || /\d/.test(next) || OPENERS.test(next))) return -1;
  }
  if (chars[k].ch === '.') {
    const head = chars.slice(Math.max(0, k - 12), k + 1).map((x) => x.ch).join('');
    if (/\b(?:[A-Za-z]\.)+[A-Za-z]\.$/.test(head) || SINGLE_INITIAL.test(head) || /(?:\b(?:e\.g|i\.e|et al|vs|etc|dr|mr|mrs|ms|st|fig|approx|ca|cf|inc))\.$/i.test(head)) return -1;
    if (/\b(?:no|vol|pp|ch|sec|eq|art)\.$/i.test(head) && j < chars.length && /\d/.test(chars[j].ch)) return -1;
  }
  return e;
}

/** Insertion point for a note whose link is `link` inside `host`: end of its sentence. */
function sentenceEndPoint(host, link) {
  const { chars, linkStart, linkEnd } = flattenHost(host, link);
  if (!chars.length) return null;
  const tryAt = (k) => {
    const e = sentenceEndAt(chars, k);
    return e === -1 ? null : { idx: e, loc: locate(chars, e, host) };
  };
  // The link itself may end the sentence ("<a>Whole sentence.</a> Next").
  let j = linkEnd - 1;
  while (j >= linkStart && j >= 0 && CLOSERS.has(chars[j].ch)) j--;
  if (linkEnd > linkStart && j >= linkStart && j >= 0) {
    const r = tryAt(j);
    if (r && r.loc) return { idx: r.idx, ...r.loc };
  }
  for (let k = Math.max(linkEnd, 0); k < chars.length; k++) {
    const r = tryAt(k);
    if (r && r.loc) return { idx: r.idx, ...r.loc };
  }
  // No sentence end: end of the block's inline content.
  let last = chars.length - 1;
  while (last >= 0 && /\s/.test(chars[last].ch)) last--;
  if (last < 0) return null;
  while (last >= 0) {
    const loc = locate(chars, last, host);
    if (loc) return { idx: last, ...loc };
    last--;
  }
  return null;
}

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

  // Phase 2: ref and note go at the end of the link's sentence. A note that
  // only echoes its link text ("nexus-agents" beside the link "nexus-agents")
  // tells the reader nothing the sentence doesn't, so it is dropped: a note
  // must add more than ECHO_MAX_NEW_WORDS words.
  const phrasingOnly = hits.filter((h) => isPhrasing(h.content) && !isEcho(h.link, h.content));
  // Locate every sentence end on the untouched tree. Hits that share an end
  // (same host and char) form ONE group: one ref, one note, one number.
  const groups = [];
  for (const h of phrasingOnly) {
    const host = h.chain[h.hostIdx];
    const pt = sentenceEndPoint(host, h.link);
    if (!pt) {
      // No usable point (should not happen): keep the old placement, right after the link.
      groups.push({ host, idx: -1, parent: h.chain[h.chain.length - 1], after: h.link, split: null, hits: [h] });
      continue;
    }
    const g = groups.find((x) => x.host === host && x.idx === pt.idx);
    if (g) g.hits.push(h);
    else groups.push({ host, ...pt, hits: [h] });
  }
  groups.forEach((g, n) => {
    g.serial = n + 1;
    for (const h of g.hits) h.serial = g.serial;
  });
  // Report every hit before the first insertion, while host text is untouched.
  if (opts.onMatch) {
    for (const h of phrasingOnly) opts.onMatch({ link: h.link, host: h.chain[h.hostIdx], key: h.key, entry: h.li, serial: h.serial });
  }
  // The note holds every entry of its sentence in link order, one per line
  // (<br> keeps the content phrasing-only and the entries distinct).
  const makePair = (g) => {
    const id = `${NOTE_PREFIX}${g.serial}`;
    const ref = {
      type: 'element',
      tagName: 'a',
      properties: {
        href: `#${id}`,
        id: `${id}-ref`,
        className: ['remarque-sidenote-ref'],
        ariaLabel: `Note ${g.serial}`,
        ariaDescribedBy: [id],
      },
      children: [],
    };
    const children = g.hits.flatMap((h, i) =>
      i === 0 ? h.content : [{ type: 'element', tagName: 'br', properties: {}, children: [] }, ...h.content]
    );
    const note = {
      type: 'element',
      tagName: 'span',
      properties: { className: ['remarque-sidenote'], id, role: 'note' },
      children,
    };
    return [ref, note];
  };
  // Inserting later ends first keeps earlier text-node offsets valid.
  const hostOrder = new Map();
  for (const g of groups) if (!hostOrder.has(g.host)) hostOrder.set(g.host, hostOrder.size);
  const pos = (g) => (g.idx === -1 ? Infinity : g.idx);
  [...groups].sort((x, y) => hostOrder.get(x.host) - hostOrder.get(y.host) || pos(y) - pos(x)).forEach((g) => {
    const { parent, after } = g;
    if (g.split) {
      const t = g.split.node;
      const rest = { type: 'text', value: t.value.slice(g.split.off) };
      t.value = t.value.slice(0, g.split.off);
      parent.children.splice(parent.children.indexOf(t) + 1, 0, rest);
    }
    parent.children.splice(parent.children.indexOf(after) + 1, 0, ...makePair(g));
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
