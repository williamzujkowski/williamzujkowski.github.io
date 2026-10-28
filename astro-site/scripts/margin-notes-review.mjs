#!/usr/bin/env node
/**
 * Review data for the opt-in margin notes (src/lib/rehype-source-marginalia.mjs).
 *
 * For EVERY post the plugin would affect if its `marginNotes` flag were on,
 * prints JSON with the post slug and title and, per proposed note: the full
 * sentence holding the matched link (link text marked with U+27E6/U+27E7),
 * the note as it would render, and the source URL. It renders each post with
 * the same remark/rehype stages the site uses up to and including the plugin
 * (smartypants, GFM, rehype-sidenotes, the plugin itself), forcing
 * `marginNotes: true` in the in-memory frontmatter. No file is changed.
 * The site's sanitize and drop-cap steps are not run; they do not alter a
 * note's words.
 *
 * Usage: node scripts/margin-notes-review.mjs [--out FILE]   (run from astro-site/)
 * Prints the JSON to stdout when --out is absent. A summary line goes to stderr.
 */
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import remarkSmartypants from 'remark-smartypants';
import rehypeSidenotes from '../src/lib/rehype-sidenotes.mjs';
import rehypeSourceMarginalia from '../src/lib/rehype-source-marginalia.mjs';
import rehypeSmartQuotes from '../src/lib/rehype-smart-quotes.mjs';

const POSTS = fileURLToPath(new URL('../../src/posts/', import.meta.url));
const CITATIONS = JSON.parse(readFileSync(fileURLToPath(new URL('../src/data/citations.json', import.meta.url)), 'utf8'));
const OPEN = '⟦';
const CLOSE = '⟧';

const outIdx = process.argv.indexOf('--out');
const outFile = outIdx > -1 ? process.argv[outIdx + 1] : null;

function splitFrontmatter(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  return m ? { fm: m[1], body: m[2] } : { fm: '', body: raw };
}

function scalar(fm, key) {
  const m = fm.match(new RegExp(`^${key}:\\s*(.*)$`, 'm'));
  if (!m) return undefined;
  let v = m[1].trim();
  if (v.startsWith("'") && v.endsWith("'")) v = v.slice(1, -1).replace(/''/g, "'");
  else if (v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1).replace(/\\"/g, '"');
  return v;
}

const isEl = (n, tag) => n && n.type === 'element' && (!tag || n.tagName === tag);
const textOf = (n) => (n.type === 'text' ? n.value : (n.children || []).map(textOf).join(''));

/** Host block text with the target link's text marked; nested lists excluded. */
function marked(host, link) {
  let before = '';
  let linkText = '';
  let after = '';
  let seen = false;
  const walk = (n) => {
    if (n === link) {
      seen = true;
      linkText = textOf(n);
      return;
    }
    if (n.type === 'text') {
      if (seen) after += n.value;
      else before += n.value;
      return;
    }
    if (isEl(n) && (n.tagName === 'ul' || n.tagName === 'ol')) return;
    (n.children || []).forEach(walk);
  };
  walk(host);
  return { before, linkText, after };
}

const ABBREV = /\b(?:e\.g|i\.e|vs|etc|dr|mr|mrs|ms|st|no|fig|approx|al|inc|ca|cf)\.$/i;

/** The sentence containing the marked link, cut from the whole block. */
function sentenceAround({ before, linkText, after }) {
  const boundary = (s) => {
    // sentence ends: terminal punctuation, optional closers, space, then a capital/digit/opener
    const re = /[.!?]["'”’)\]]*\s+(?=["'“‘([]*[A-Z0-9])/g;
    let m;
    const found = [];
    while ((m = re.exec(s))) {
      const head = s.slice(0, m.index + 1);
      if (ABBREV.test(head)) continue;
      found.push({ start: m.index + 1, end: m.index + m[0].length });
    }
    return { found };
  };
  const b = boundary(before).found;
  const start = b.length ? b[b.length - 1].end : 0;
  const a = boundary(after).found;
  const stop = a.length ? a[0].start : after.length;
  const pre = before.slice(start);
  const post = after.slice(0, stop);
  return {
    sentence: `${pre}${OPEN}${linkText}${CLOSE}${post}`.replace(/\s+/g, ' ').trim(),
    linkText,
  };
}

const NAMED = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };
const stripTags = (html) =>
  html
    .replace(/<[^>]+>/g, '')
    .replace(/&(?:#x([0-9a-f]+)|#(\d+)|(amp|lt|gt|quot|apos));/gi, (_, hex, dec, name) =>
      name ? NAMED[name.toLowerCase()] : String.fromCodePoint(hex ? parseInt(hex, 16) : Number(dec)))
    .replace(/\s+/g, ' ')
    .trim();


const files = readdirSync(POSTS).filter((f) => f.endsWith('.md')).sort();
const posts = [];
const skippedFootnotes = [];
let postsWithSources = 0;

for (const f of files) {
  const slug = f.replace(/\.md$/, '');
  const { fm, body } = splitFrontmatter(readFileSync(path.join(POSTS, f), 'utf8'));
  const title = scalar(fm, 'title') ?? slug;
  const draft = scalar(fm, 'draft') === 'true';
  const alreadyEnabled = scalar(fm, 'marginNotes') === 'true';
  if (/^## Sources\s*$/m.test(body)) postsWithSources += 1;
  if (/^\[\^[^\]]+\]:/m.test(body)) {
    skippedFootnotes.push(slug);
    continue;
  }
  const hits = [];
  const p = await createMarkdownProcessor({
    syntaxHighlight: false,
    remarkPlugins: [[remarkSmartypants, { dashes: 'oldschool' }]],
    rehypePlugins: [
      rehypeSidenotes,
      [rehypeSourceMarginalia, {
        citations: CITATIONS,
        onMatch: ({ link, host, serial, entry, key }) => {
          const { sentence, linkText } = sentenceAround(marked(host, link));
          let entryUrl = null;
          const find = (n) => {
            if (entryUrl) return;
            if (isEl(n, 'a') && n.properties?.href) entryUrl = n.properties.href;
            else (n.children || []).forEach(find);
          };
          find(entry);
          if (!entryUrl) entryUrl = `https://${key}`; // citation-file entry: no link of its own
          hits.push({ serial, sentence, linkText, linkUrl: link.properties.href, sourceUrl: entryUrl });
        },
      }],
      rehypeSmartQuotes,
    ],
  });
  const { code } = await p.render(body, { frontmatter: { marginNotes: true } });
  if (!hits.length) continue;
  const notes = hits.map((h) => {
    const m = code.match(new RegExp(`<span[^>]*id="src-note-${h.serial}"[^>]*>([\\s\\S]*?)</span>`));
    if (!m) throw new Error(`${slug}: note ${h.serial} missing from render`);
    return {
      number: h.serial,
      sentence: h.sentence,
      linkText: h.linkText,
      noteText: stripTags(m[1]),
      noteHtml: m[1].trim(),
      sourceUrl: h.sourceUrl,
      linkUrl: h.linkUrl,
    };
  });
  posts.push({ slug, title, draft, flagAlreadyOn: alreadyEnabled, noteCount: notes.length, notes });
}

const summary = {
  postsTotal: files.length,
  postsWithSourcesSection: postsWithSources,
  postsAffected: posts.length,
  notesTotal: posts.reduce((n, x) => n + x.noteCount, 0),
  draftPostsAffected: posts.filter((x) => x.draft).length,
  postsExcludedForFootnotes: skippedFootnotes,
  sentenceMarker: `link text is wrapped in ${OPEN} ${CLOSE}`,
};
const json = JSON.stringify({ summary, posts }, null, 2) + '\n';
if (outFile) writeFileSync(outFile, json);
else process.stdout.write(json);
console.error(`margin-notes-review: ${summary.notesTotal} notes in ${summary.postsAffected} of ${summary.postsTotal} posts` + (outFile ? ` -> ${outFile}` : ''));
