#!/usr/bin/env node
/**
 * citations:verify-sources -- checks each `## Sources` entry of a post against
 * the page it links. Author-time, WITH network; the build never runs it.
 *
 * For every Sources entry with an http(s) URL it fetches the page (`gh api`
 * for GitHub, the arXiv abs page for arXiv PDFs, Crossref for DOIs, plain
 * HTTP otherwise) and raises flags:
 *
 *   dead            4xx/5xx, DNS failure, or a redirect to an unrelated host or a homepage
 *   unverifiable    bot-blocked (401/403/429/451), non-HTML (PDF), timeouts: nothing to compare
 *   title-mismatch  too little token overlap between the entry's title and the page's titles
 *   author-missing  an author surname named in the entry is in neither the page's
 *                   author metadata nor its text
 *   year-mismatch   every year in the entry is more than 1 away from the page's publication year
 *
 * FLAGS ARE LEADS, NOT VERDICTS. Shortened titles, paywalls and CMSs with thin
 * metadata all trip them. A person must read the page before changing an entry.
 *
 * Usage (from astro-site/): pnpm citations:verify-sources -- [--out FILE] [slug...]
 * JSON report to --out (stdout without it); human summary to stderr.
 * No slugs means every post with a `## Sources` h2.
 */
import { writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import { visit } from 'unist-util-visit';
import { allSlugs, hasSourcesHeading, readPost } from './lib.mjs';
import { metaList, parseHtml, tagText, isoDate, decode } from './collect.mjs';

// ---------------------------------------------------------------- pure logic

const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'and', 'to', 'in', 'on', 'with', 'by', 'at', 'from', 'is', 'are', 'as', 'or', 'vs', 'how', 'what', 'why', 'your', 'our', 'that', 'this', 'it', 'its', 'be']);
const fold = (s) => s.normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase();
const stem = (w) => (w.length > 3 && w.endsWith('s') && !w.endsWith('ss') ? w.slice(0, -1) : w);
/** Significant tokens of a title: folded, stop words and single characters dropped, plural -s stemmed. */
export function tokens(s) {
  return new Set(fold(s).split(/[^\p{L}\p{N}]+/u).filter((w) => w.length > 1 && !STOP.has(w)).map(stem));
}

export const TITLE_MIN_OVERLAP = 0.5;
/** Bot-wall and interstitial page titles: the page was not the one linked, so nothing can be compared. */
export const INTERSTITIAL = /client challenge|just a moment|javascript is disabled|enable javascript|access denied|attention required|verify you are (?:a )?human|are you a robot|security check|^redirecting\W*$|^\s*403\b|^\s*forbidden\b/i;
/**
 * Share of the entry title's tokens present in the best-matching page title (1 when the entry has none).
 * `extra` (URL host and path words) counts as page text too, and a token also matches inside the
 * page title with spaces removed ("hackthebox" vs "Hack The Box").
 */
export function titleOverlap(entryTitle, pageTitles, extra = '') {
  const e = tokens(entryTitle);
  const titles = pageTitles.filter(Boolean);
  if (!e.size || !titles.length) return { score: 1, best: null };
  let score = 0;
  let best = null;
  for (const t of titles) {
    const p = new Set([...tokens(t), ...tokens(extra)]);
    const compact = fold(t).replace(/[^\p{L}\p{N}]+/gu, '');
    const s = [...e].filter((w) => p.has(w) || (w.length >= 4 && compact.includes(w))).length / e.size;
    if (s > score || best === null) { score = s; best = t; }
  }
  return { score, best };
}

const NAME = String.raw`[\p{Lu}][\p{L}'’\-]+`;
const ORG_WORDS = /^(team|labs?|research|inc|corp|university|institute|foundation|group|project|lab|consortium|security|staff|authors?|et|al)$/i;
const okSurname = (s) => s.length > 2 && !/^[\p{Lu}]+$/u.test(s) && !ORG_WORDS.test(s);

/**
 * Author surnames an entry asserts, from the text AROUND the title link:
 * "X et al.", "X and Y", "by A, B and C", "Surname, A." and "A. Surname".
 * Heuristic and conservative: organisations and acronyms are skipped.
 */
export function entryAuthors(rest, title = '') {
  const found = new Set();
  const add = (s) => { if (s && okSurname(s)) found.add(s); };
  const txt = rest.replace(/\*+/g, '');
  for (const m of txt.matchAll(new RegExp(`(${NAME})(?:,? (?:and|&) (${NAME}))?,? et al\\b`, 'gu'))) { add(m[1]); add(m[2]); }
  for (const m of txt.matchAll(/\bby ([^.;(*\n]+)/gu)) {
    for (const chunk of m[1].split(/,| and | & /)) {
      const ws = chunk.trim().split(/\s+/);
      if (ws.length >= 1 && ws.length <= 3 && ws.every((w) => new RegExp(`^${NAME}\\.?$`, 'u').test(w))) add(ws[ws.length - 1].replace(/\.$/, ''));
    }
  }
  for (const m of txt.matchAll(new RegExp(`(${NAME}) (?:and|&) (${NAME})(?=,? \\(?(?:19|20)\\d\\d|\\s*$|\\s*[—–-]|\\.$)`, 'gu'))) { add(m[1]); add(m[2]); }
  for (const m of txt.matchAll(new RegExp(`(${NAME}), (?:\\p{Lu}\\.\\s?)+`, 'gu'))) add(m[1]);
  for (const m of txt.matchAll(new RegExp(`(?:\\p{Lu}\\.\\s?)+(${NAME})`, 'gu'))) add(m[1]);
  const titleWords = tokens(title);
  return [...found].filter((s) => !titleWords.has(stem(fold(s))));
}

/** Surnames from `entryAuthors` that appear in neither the page's author list nor its text. */
export function authorsMissing(surnames, pageAuthors, pageText = '') {
  const hay = fold(pageAuthors.join(' | '));
  const text = fold(pageText);
  return surnames.filter((s) => {
    const f = fold(s);
    const re = new RegExp(`(?:^|[^\\p{L}])${f.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?:[^\\p{L}]|$)`, 'u');
    return !re.test(hay) && !re.test(text);
  });
}

/** Years (1950..next year) stated in an entry's text, excluding any inside URLs. */
export function entryYears(rest, nowYear = new Date().getUTCFullYear()) {
  const t = rest.replace(/https?:\/\/\S+/g, ' ');
  return [...new Set([...t.matchAll(/(?<![\d.\-/])((?:19[5-9]|20[0-4])\d)(?![\d\-/]\d|\d)/g)].map((m) => Number(m[1])).filter((y) => y <= nowYear + 1))];
}

/** year-mismatch detail, or null. Fires only when EVERY entry year is more than 1 from the page's year. */
export function yearMismatch(years, pageYear) {
  if (!years.length || !pageYear) return null;
  const closest = Math.min(...years.map((y) => Math.abs(y - pageYear)));
  return closest > 1 ? { entryYears: years, pageYear } : null;
}

const BLOCKED = new Set([401, 403, 429, 451, 999]);
/** HTTP status -> 'ok' | 'unverifiable' | 'dead'. */
export function classifyStatus(status) {
  if (status >= 200 && status < 400) return 'ok';
  if (BLOCKED.has(status)) return 'unverifiable';
  return status >= 400 ? 'dead' : 'ok';
}

const SLD = new Set(['co', 'com', 'org', 'net', 'ac', 'gov', 'edu']);
export function registrable(host) {
  const p = host.toLowerCase().replace(/^www\./, '').split('.');
  if (p.length <= 2) return p.join('.');
  return p.slice(SLD.has(p[p.length - 2]) && p[p.length - 1].length === 2 ? -3 : -2).join('.');
}
const TRANSPARENT = new Set(['doi.org', 'dx.doi.org']);
/** Redirect assessment: a string reason when the final URL looks like a different page, else null. */
export function redirectProblem(from, to) {
  let a; let b;
  try { a = new URL(from); b = new URL(to); } catch { return null; }
  if (TRANSPARENT.has(a.hostname.replace(/^www\./, ''))) return null;
  if (registrable(a.hostname) !== registrable(b.hostname)) return `redirects to unrelated host ${b.hostname}`;
  const homepage = (u) => u.pathname.replace(/\/+$/, '') === '' && !u.search;
  if (homepage(b) && !homepage(a)) return 'redirects to a homepage';
  return null;
}

/**
 * Compare one entry with what its page says. `page` is
 * { titles[], authors[], year, text }; returns flags [{ kind, detail }].
 */
export function compareEntry(entry, page) {
  const flags = [];
  if (entry.title && !(page.titles || []).some((t) => INTERSTITIAL.test(t))) {
    const o = titleOverlap(entry.title, page.titles || [], page.urlWords || '');
    if (o.score < TITLE_MIN_OVERLAP) flags.push({ kind: 'title-mismatch', detail: { overlap: Number(o.score.toFixed(2)), entryTitle: entry.title, closestPageTitle: o.best } });
  }
  const missing = authorsMissing(entry.authors || [], page.authors || [], page.text || '');
  if (missing.length) flags.push({ kind: 'author-missing', detail: { missing, entryAuthors: entry.authors, pageAuthors: (page.authors || []).slice(0, 12) } });
  const ym = yearMismatch(entry.years || [], page.year);
  if (ym) flags.push({ kind: 'year-mismatch', detail: ym });
  return flags;
}

// ---------------------------------------------------------- page extraction

const textOfNode = (n) => (n.type === 'text' ? n.value : (n.children || []).map(textOfNode).join(''));

/** Sources entries of a rendered post: [{ text, url, title, authors, years }]; first link keys the entry, as the margin-note plugin does. */
export async function sourcesEntries(body) {
  const rows = [];
  const grab = () => (tree) => {
    const idx = tree.children.findIndex((n) => n.type === 'element' && n.tagName === 'h2' && textOfNode(n).trim().toLowerCase() === 'sources');
    if (idx === -1) return;
    for (let i = idx + 1; i < tree.children.length; i++) {
      const n = tree.children[i];
      if (n.type === 'element' && n.tagName === 'h2') break;
      if (n.type !== 'element' || (n.tagName !== 'ul' && n.tagName !== 'ol')) continue;
      for (const li of n.children) {
        if (li.type !== 'element' || li.tagName !== 'li') continue;
        let a = null;
        visit(li, (x) => x.type === 'element' && x.tagName === 'a' && x.properties?.href, (x) => { a = x; return false; });
        rows.push({ li, a });
      }
    }
  };
  const p = await createMarkdownProcessor({ syntaxHighlight: false, rehypePlugins: [grab] });
  await p.render(body);
  return rows.map(({ li, a }) => {
    const text = textOfNode(li).replace(/\s+/g, ' ').trim();
    const url = a ? String(a.properties.href) : null;
    if (!/^https?:\/\//i.test(url || '')) return { text, url, skip: true };
    const linkText = textOfNode(a).replace(/\s+/g, ' ').trim();
    const bare = /^https?:\/\//i.test(linkText);
    const at = text.indexOf(linkText);
    // Bare-URL entries ("Title - description. https://...") title = the text before the URL.
    const title = bare ? text.slice(0, at).replace(/^\d+\.\s*/, '').split(/\s[-—–]\s|\.\s/)[0].trim() : linkText;
    const rest = bare ? text.replace(linkText, ' ') : text.replace(linkText, ' ');
    return { text, url, title, authors: entryAuthors(rest, title), years: entryYears(rest.replace(title, ' ')) };
  });
}

const stripTags = (html) => decode(html.replace(/<(script|style|noscript|svg)\b[\s\S]*?<\/\1>/gi, ' ').replace(/<[^>]+>/g, ' '));

function jsonLd(html) {
  const out = [];
  for (const m of html.matchAll(/<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi)) {
    try { out.push(JSON.parse(m[1])); } catch { /* ignore malformed JSON-LD */ }
  }
  return out.flatMap((o) => (Array.isArray(o) ? o : o['@graph'] ? [o, ...o['@graph']] : [o]));
}
const asList = (v) => (v == null ? [] : Array.isArray(v) ? v : [v]);

/** Pure: page HTML -> { titles[], authors[], year, publisher, text }. */
export function pageFacts(html, host = '') {
  const meta = metaList(html);
  const all = (k) => meta.filter(([n]) => n === k).map(([, v]) => v).filter(Boolean);
  const ld = jsonLd(html);
  const authors = [...all('citation_author'), ...all('author'), ...all('article:author'), ...all('dc.creator'), ...all('twitter:creator')];
  let ldDate = null;
  for (const o of ld) {
    for (const a of asList(o.author)) authors.push(typeof a === 'string' ? a : a?.name);
    ldDate ||= o.datePublished || null;
  }
  for (const m of html.matchAll(/rel=["']author["'][^>]*>([^<]{2,60})</gi)) authors.push(decode(m[1]));
  for (const m of html.matchAll(/class=["'][^"']*(?:byline|author)[^"']*["'][^>]*>([^<]{2,80})</gi)) authors.push(decode(m[1]));
  const titles = [all('citation_title')[0], all('og:title')[0], all('twitter:title')[0], tagText(html, 'h1'), tagText(html, 'title')].filter(Boolean);
  const date = isoDate(all('citation_publication_date')[0] || all('citation_date')[0] || all('citation_online_date')[0] || all('article:published_time')[0] || all('datepublished')[0] || all('dc.date')[0] || all('date')[0] || ldDate);
  return {
    titles,
    authors: authors.filter(Boolean).map((a) => a.trim()),
    year: date ? Number(date.slice(0, 4)) : null,
    publisher: parseHtml(html, host).publisher,
    text: stripTags(html).slice(0, 60000),
    urlWords: host,
  };
}

// ------------------------------------------------------------------ network

const UA = 'Mozilla/5.0 (compatible; citations-verify-sources/1.0)';
const hostOf = (u) => new URL(u).hostname.replace(/^www\./, '');

async function fetchHtml(href) {
  try {
    const res = await fetch(href, { redirect: 'follow', signal: AbortSignal.timeout(25000), headers: { 'user-agent': UA, accept: 'text/html,*/*;q=0.5' } });
    const type = res.headers.get('content-type') || '';
    const base = { status: res.status, finalUrl: res.url };
    if (classifyStatus(res.status) !== 'ok') return base;
    if (!/html|xml/i.test(type)) return { ...base, nonHtml: type };
    return { ...base, html: await res.text() };
  } catch (e) {
    const code = e.cause?.code || e.code || '';
    if (/ENOTFOUND|EAI_AGAIN/.test(code)) return { dns: true, error: code };
    return { error: `${e.name}: ${e.message}${code ? ` (${code})` : ''}` };
  }
}

const gh = (p) => JSON.parse(execFileSync('gh', ['api', p], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }));
const ghStatus = (e) => /HTTP (\d{3})/.exec(String(e.stderr || e.message))?.[1];

/** GitHub URL -> page facts via gh api, or null when the URL is not a repo-scoped GitHub page. */
function githubFacts(url) {
  const u = new URL(url);
  if (u.hostname !== 'github.com') return null;
  const seg = u.pathname.split('/').filter(Boolean);
  try {
    if (seg[0] === 'advisories' && seg[1]) {
      const a = gh(`advisories/${seg[1]}`);
      return { titles: [a.summary, a.ghsa_id], authors: [], year: Number(String(a.published_at).slice(0, 4)), text: a.description || '', via: 'gh api' };
    }
    const [o, r, kind, id] = seg;
    if (!o || !r) return null;
    const repo = gh(`repos/${o}/${r}`);
    const facts = { titles: [repo.full_name, repo.name, repo.description].filter(Boolean), authors: [repo.owner.login, repo.owner.name].filter(Boolean), year: null, text: `${repo.full_name} ${repo.description || ''} ${repo.owner.login}`, via: 'gh api', renamedTo: repo.full_name.toLowerCase() !== `${o}/${r}`.toLowerCase() ? repo.full_name : undefined };
    const issue = kind === 'issues' || kind === 'pull' ? gh(`repos/${o}/${r}/${kind === 'pull' ? 'pulls' : 'issues'}/${id}`) : null;
    if (issue) { facts.titles = [issue.title, ...facts.titles]; facts.year = Number(issue.created_at.slice(0, 4)); facts.authors.push(issue.user?.login); facts.text += ` ${issue.title}`; }
    if (kind === 'releases' && id === 'tag') {
      const rel = gh(`repos/${o}/${r}/releases/tags/${seg[4]}`);
      facts.titles = [rel.name || rel.tag_name, ...facts.titles]; facts.year = Number(String(rel.published_at).slice(0, 4));
    }
    // Source views (blob/tree/commit) and bare repos: the repo exists; a file title adds nothing to compare.
    facts.skipTitle = !issue && kind !== 'releases' && !!kind;
    return facts;
  } catch (e) {
    const s = Number(ghStatus(e));
    return { ghError: s || null, message: String(e.stderr || e.message).split('\n')[0] };
  }
}

async function crossref(doi) {
  const res = await fetch(`https://api.crossref.org/works/${encodeURIComponent(doi)}`, { signal: AbortSignal.timeout(25000), headers: { 'user-agent': UA } });
  if (!res.ok) return { status: res.status };
  const m = (await res.json()).message;
  const issued = m.issued?.['date-parts']?.[0]?.[0] || m.published?.['date-parts']?.[0]?.[0] || null;
  return { facts: { titles: [...asList(m.title), ...asList(m['container-title'])], authors: asList(m.author).map((a) => [a.family, a.given].filter(Boolean).join(', ') || a.name), year: issued, text: asList(m.author).map((a) => a.family).join(' '), via: 'crossref' } };
}

/** URL -> { class: 'ok'|'dead'|'unverifiable', facts?, evidence } */
export async function inspect(url) {
  let u;
  try { u = new URL(url); } catch { return { class: 'unverifiable', evidence: { reason: 'unparseable URL' } }; }
  const gf = githubFacts(url);
  if (gf?.ghError === 404) return { class: 'dead', evidence: { via: 'gh api', status: 404, message: gf.message } };
  if (gf?.ghError) return { class: 'unverifiable', evidence: { via: 'gh api', status: gf.ghError, message: gf.message } };
  if (gf && !gf.message) return { class: 'ok', facts: gf, evidence: { via: 'gh api', titles: gf.titles.slice(0, 3), renamedTo: gf.renamedTo } };
  const doi = /^(?:dx\.)?doi\.org$/.test(u.hostname.replace(/^www\./, '')) ? decodeURIComponent(u.pathname.slice(1)) : null;
  if (doi) {
    try {
      const c = await crossref(doi);
      if (c.status === 404) return { class: 'dead', evidence: { via: 'crossref', status: 404, doi } };
      if (c.facts) return { class: 'ok', facts: c.facts, evidence: { via: 'crossref', doi, titles: c.facts.titles.slice(0, 2), year: c.facts.year } };
    } catch { /* fall through to a plain fetch */ }
  }
  let target = url;
  const ax = /^(?:www\.)?arxiv\.org\/(?:pdf|html)\/(.+?)(?:\.pdf)?(?:v\d+)?$/.exec(`${u.hostname}${u.pathname}`);
  if (ax) target = `https://arxiv.org/abs/${ax[1]}`;
  let r = await fetchHtml(target);
  if ((r.status >= 500 || r.error) && !r.dns) r = await fetchHtml(target); // one retry for flaky hosts
  if (r.dns) return { class: 'dead', evidence: { reason: 'DNS failure', error: r.error } };
  if (r.error) return { class: 'unverifiable', evidence: { reason: 'network error', error: r.error } };
  const cls = classifyStatus(r.status);
  if (cls !== 'ok') return { class: cls, evidence: { status: r.status, finalUrl: r.finalUrl } };
  const redir = redirectProblem(target, r.finalUrl);
  if (redir) return { class: 'dead', evidence: { status: r.status, finalUrl: r.finalUrl, reason: redir } };
  if (r.nonHtml !== undefined) return { class: 'unverifiable', evidence: { status: r.status, reason: `non-HTML (${r.nonHtml}); reachable, content not compared` } };
  const facts = pageFacts(r.html, hostOf(url));
  facts.urlWords = `${hostOf(url)} ${u.pathname.replace(/[/_.-]+/g, ' ')}`;
  return { class: 'ok', facts, evidence: { status: r.status, finalUrl: r.finalUrl, titles: facts.titles.slice(0, 4), authors: facts.authors.slice(0, 8), year: facts.year } };
}

// ---------------------------------------------------------------------- run

/** Verify one post's entries. `lookup` is injectable for tests. */
export async function verifySlug(slug, lookup) {
  const { body } = readPost(slug);
  if (!hasSourcesHeading(body)) return null;
  const rows = [];
  for (const e of await sourcesEntries(body)) {
    if (e.skip) continue;
    const res = await lookup(e.url);
    const flags = [];
    if (res.class === 'dead') flags.push({ kind: 'dead', detail: res.evidence });
    else if (res.class === 'unverifiable') flags.push({ kind: 'unverifiable', detail: res.evidence });
    else if (res.facts.titles.some((t) => INTERSTITIAL.test(t))) flags.push({ kind: 'unverifiable', detail: { reason: 'bot wall or interstitial page', titles: res.facts.titles.slice(0, 2) } });
    else flags.push(...compareEntry(res.facts.skipTitle ? { ...e, title: '' } : e, res.facts));
    rows.push({ slug, entry: e.text, url: e.url, flags, evidence: res.evidence });
  }
  return rows;
}

function memoLookup() {
  const cache = new Map();
  return (url) => {
    if (!cache.has(url)) cache.set(url, inspect(url));
    return cache.get(url);
  };
}

async function pool(items, n, fn) {
  const out = new Array(items.length);
  let i = 0;
  await Promise.all(Array.from({ length: n }, async () => { while (i < items.length) { const k = i++; out[k] = await fn(items[k]); } }));
  return out;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2).filter((a) => a !== '--');
  const oi = args.indexOf('--out');
  const outFile = oi > -1 ? args[oi + 1] : null;
  const named = args.filter((a, i) => !a.startsWith('--') && i !== oi + 1);
  const slugs = (named.length ? named : allSlugs());
  const lookup = memoLookup();
  const posts = (await pool(slugs, 5, (s) => verifySlug(s, lookup).catch((e) => { console.error(`error ${s}: ${e.message}`); return null; })));
  const rows = posts.flat().filter(Boolean);
  const counts = {};
  for (const r of rows) for (const f of r.flags) counts[f.kind] = (counts[f.kind] || 0) + 1;
  const report = { generated: new Date().toISOString(), note: 'Flags are leads for a human to check against the page, not verdicts.', posts: posts.filter(Boolean).length, entries: rows.length, counts, results: rows };
  const json = JSON.stringify(report, null, 2) + '\n';
  if (outFile) writeFileSync(outFile, json); else process.stdout.write(json);
  console.error(`\ncitations:verify-sources: ${report.posts} posts with Sources, ${rows.length} entries checked`);
  for (const k of ['dead', 'unverifiable', 'title-mismatch', 'author-missing', 'year-mismatch']) console.error(`  ${k.padEnd(15)} ${counts[k] || 0}`);
  console.error('Flags are leads, not verdicts: read the page before changing an entry. 403s are "unverifiable", not dead.');
  for (const r of rows.filter((x) => x.flags.length && !x.flags.every((f) => f.kind === 'unverifiable'))) {
    console.error(`  ${r.slug}  ${r.flags.map((f) => f.kind).join(',')}  ${r.url}`);
  }
}
