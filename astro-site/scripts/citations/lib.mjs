// Shared helpers for citations:collect and citations:check. No network here.
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import { visit } from 'unist-util-visit';
import { normalizeUrl, isSkippedCitationKey } from '../../src/lib/rehype-source-marginalia.mjs';

export const POSTS_DIR = fileURLToPath(new URL('../../../src/posts/', import.meta.url));
export const CITATIONS_FILE = fileURLToPath(new URL('../../src/data/citations.json', import.meta.url));

export function readCitations(file = CITATIONS_FILE) {
  return existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : {};
}

export function splitFrontmatter(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  return m ? { fm: m[1], body: m[2] } : { fm: '', body: raw };
}

export function allSlugs(dir = POSTS_DIR) {
  return readdirSync(dir).filter((f) => f.endsWith('.md')).map((f) => f.replace(/\.md$/, '')).sort();
}

/** Has a root-level "## Sources" heading (such posts never use the citation file). */
export const hasSourcesHeading = (body) => /^## Sources\s*$/m.test(body);
export const hasFootnotes = (body) => /^\[\^[^\]]+\]:/m.test(body);

/** Body links of one post, in order, as { href, key, text }: rendered like the site, code excluded. */
export async function bodyLinks(body) {
  const found = [];
  const collect = () => (tree) => {
    visit(tree, (n) => n.type === 'element' && n.tagName === 'a' && n.properties?.href, (n) => {
      found.push({ href: String(n.properties.href), text: textOf(n) });
    });
  };
  const p = await createMarkdownProcessor({ syntaxHighlight: false, rehypePlugins: [collect] });
  await p.render(body);
  return found;
}
const textOf = (n) => (n.type === 'text' ? n.value : (n.children || []).map(textOf).join(''));

/** Unique note-eligible external keys of a post: [{ key, href }] in first-seen order. */
export async function eligibleLinks(body) {
  const out = new Map();
  for (const l of await bodyLinks(body)) {
    const key = normalizeUrl(l.href);
    if (!key || isSkippedCitationKey(key) || out.has(key)) continue;
    out.set(key, { key, href: l.href });
  }
  return [...out.values()];
}

export function readPost(slug, dir = POSTS_DIR) {
  const file = path.join(dir, `${slug}.md`);
  if (!existsSync(file)) throw new Error(`no such post: ${slug}`);
  return splitFrontmatter(readFileSync(file, 'utf8'));
}
