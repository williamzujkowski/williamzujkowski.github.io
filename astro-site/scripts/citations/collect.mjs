#!/usr/bin/env node
/**
 * citations:collect -- fills src/data/citations.json for the given posts.
 * Extracts the posts' note-eligible external links, fetches each page
 * (citation_title / og:title / h1 / <title>; og:site_name; article:published_time,
 * citation_date) and writes `{ title, publisher, date, checked }` under the
 * plugin's normalised URL. GitHub repos, issues, PRs, releases and advisories
 * go through `gh api`. Existing entries are NEVER overwritten without
 * --refresh. Anything unresolved is listed for manual completion. A person
 * must still verify every written entry against the page: this is a draft.
 * The site build never runs this and never fetches.
 *
 * Usage (from astro-site/): pnpm citations:collect -- [--refresh] [--dry-run] <slug...>
 */
import { writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { eligibleLinks, hasSourcesHeading, readCitations, readPost, CITATIONS_FILE } from './lib.mjs';

const TODAY = new Date().toISOString().slice(0, 10);
const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', mdash: '—', rsquo: '’', lsquo: '‘', ldquo: '“', rdquo: '”', hellip: '…' };
export const decode = (s) =>
  s.replace(/&(?:#x([0-9a-f]+)|#(\d+)|([a-z]+));/gi, (m, hex, dec, name) =>
    name ? (ENT[name.toLowerCase()] ?? m) : String.fromCodePoint(hex ? parseInt(hex, 16) : Number(dec)))
   .replace(/\s+/g, ' ').trim();

function metas(html) {
  const map = {};
  for (const m of html.matchAll(/<meta\b[^>]*>/gi)) {
    const tag = m[0];
    const k = /(?:property|name|itemprop)\s*=\s*["']([^"']+)["']/i.exec(tag)?.[1];
    const v = /content\s*=\s*"([^"]*)"|content\s*=\s*'([^']*)'/i.exec(tag);
    if (k && v && !(k.toLowerCase() in map)) map[k.toLowerCase()] = decode(v[1] ?? v[2] ?? '');
  }
  return map;
}
const tagText = (html, tag) => {
  const m = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}>`, 'i').exec(html);
  return m ? decode(m[1].replace(/<[^>]+>/g, '')) : null;
};

const isoDate = (s) => {
  if (!s) return null;
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s.trim());
  if (m) return `${m[1]}-${m[2]}-${m[3]}`;
  const y = /^(\d{4})$/.exec(s.trim());
  if (y) return y[1];
  const d = new Date(s);
  return Number.isNaN(d.getTime()) ? null : d.toISOString().slice(0, 10);
};

/** Pure: page HTML + host -> { title, publisher, date, notes[] }. */
export function parseHtml(html, host) {
  const m = metas(html);
  const notes = [];
  let title = m.citation_title || m['og:title'] || tagText(html, 'h1') || tagText(html, 'title');
  const publisher = m['citation_publisher'] || m['og:site_name'] || null;
  if (title && publisher) {
    const esc = publisher.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    title = title.replace(new RegExp(`\\s*[|\\-–—·:]\\s*${esc}\\s*$`, 'i'), '');
  }
  if (!publisher) notes.push(`no site name, publisher falls back to ${host}`);
  const date = isoDate(m.citation_publication_date || m.citation_date || m['article:published_time'] || m['datepublished'] || m['date']);
  return { title: title || null, publisher: publisher || host, date, notes };
}

const OWN_REPO = 'williamzujkowski/williamzujkowski.github.io';
/** Publisher wording for a GitHub issue or PR: `owner/repo #N` (`this site's repo #N` for this repo). */
export const githubPublisher = (repo, id) => `${repo === OWN_REPO ? "this site's repo" : repo}${id ? ` #${id}` : ''}`;

const gh = (p) => JSON.parse(execFileSync('gh', ['api', p], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }));

/** key -> { title, publisher, date } for GitHub repos/issues/PRs/releases/advisories, or null when not GitHub. */
export function githubResolve(key) {
  if (!key.startsWith('github.com/')) return null;
  const seg = key.slice('github.com/'.length).split('?')[0].split('/');
  if (seg[0] === 'advisories' && seg[1]) {
    const a = gh(`advisories/${seg[1]}`);
    return { title: a.summary, publisher: 'GitHub Advisory Database', date: isoDate(a.published_at) };
  }
  const [o, r, kind, id, id2] = seg;
  if (!o || !r) return null;
  const repo = `${o}/${r}`;
  if (!kind) {
    const d = gh(`repos/${repo}`);
    return { title: d.full_name, publisher: 'GitHub', date: null };
  }
  if (kind === 'issues' && id) {
    const d = gh(`repos/${repo}/issues/${id}`);
    return { title: d.title, publisher: githubPublisher(repo, id), date: isoDate(d.created_at) };
  }
  if (kind === 'pull' && id) {
    const d = gh(`repos/${repo}/pulls/${id}`);
    return { title: d.title, publisher: githubPublisher(repo, id), date: isoDate(d.created_at) };
  }
  if (kind === 'releases' && id === 'tag' && id2) {
    const d = gh(`repos/${repo}/releases/tags/${id2}`);
    return { title: d.name || d.tag_name, publisher: githubPublisher(repo), date: isoDate(d.published_at) };
  }
  if (kind === 'security' && id === 'advisories' && id2) {
    const a = gh(`repos/${repo}/security-advisories/${id2}`);
    return { title: a.summary, publisher: 'GitHub Advisory Database', date: isoDate(a.published_at) };
  }
  return null;
}

async function fetchPage(href) {
  const res = await fetch(href, {
    redirect: 'follow',
    signal: AbortSignal.timeout(25000),
    headers: { 'user-agent': 'Mozilla/5.0 (compatible; citations-collect/1.0)', accept: 'text/html,*/*;q=0.5' },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  if (!/html|xml/i.test(res.headers.get('content-type') || '')) throw new Error(`not HTML (${res.headers.get('content-type')})`);
  return res.text();
}

async function resolve(l) {
  const gr = (() => { try { return githubResolve(l.key); } catch (e) { return { error: String(e.message).split('\n')[0] }; } })();
  if (gr && gr.error) return { error: `gh api: ${gr.error}` };
  if (gr) return { entry: gr, notes: [] };
  const host = l.key.split('/')[0];
  const parsed = parseHtml(await fetchPage(l.href), host);
  return { entry: { title: parsed.title, publisher: parsed.publisher, date: parsed.date }, notes: parsed.notes };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2).filter((a) => a !== '--');
  const refresh = args.includes('--refresh');
  const dry = args.includes('--dry-run');
  const slugs = args.filter((a) => !a.startsWith('--'));
  if (!slugs.length) {
    console.error('usage: pnpm citations:collect -- [--refresh] [--dry-run] <slug...>');
    process.exit(2);
  }
  const citations = readCitations();
  const links = new Map();
  for (const slug of slugs) {
    const { body } = readPost(slug);
    if (hasSourcesHeading(body)) { console.error(`skip ${slug}: has a Sources list`); continue; }
    for (const l of await eligibleLinks(body)) if (!links.has(l.key)) links.set(l.key, { ...l, slug });
  }
  const flagged = [];
  let added = 0;
  for (const l of links.values()) {
    if (citations[l.key] && !refresh) { console.error(`keep    ${l.key}`); continue; }
    try {
      const { entry, notes } = await resolve(l);
      if (!entry.title) throw new Error('no title found');
      citations[l.key] = { title: entry.title, publisher: entry.publisher, date: entry.date, checked: TODAY };
      added++;
      console.error(`wrote   ${l.key}  ->  ${entry.title} | ${entry.publisher} | ${entry.date}`);
      for (const n of notes) flagged.push(`${l.key}: ${n}`);
    } catch (e) {
      flagged.push(`${l.key}: UNRESOLVED (${e.message}) [${l.slug}]`);
    }
  }
  if (!dry) {
    const sorted = Object.fromEntries(Object.entries(citations).sort(([a], [b]) => a.localeCompare(b)));
    writeFileSync(CITATIONS_FILE, JSON.stringify(sorted, null, 2) + '\n');
  }
  console.error(`\ncitations:collect: ${added} written${dry ? ' (dry run, nothing saved)' : ''}, ${flagged.length} flagged`);
  for (const f of flagged) console.error(`  FLAG ${f}`);
}
