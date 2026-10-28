#!/usr/bin/env node
/**
 * citations:check -- no network. For each given post (all posts when none are
 * named) prints its external links that would get a citation-fallback note but
 * have no entry in src/data/citations.json, then entries no post links any
 * more (only when every post was scanned). Exits non-zero only with --strict.
 * Posts with a "## Sources" list are skipped: they never use the file.
 *
 * Usage (from astro-site/): pnpm citations:check -- [--strict] [slug...]
 */
import { allSlugs, eligibleLinks, hasSourcesHeading, readCitations, readPost, POSTS_DIR, CITATIONS_FILE } from './lib.mjs';

/** @returns {Promise<{ missing: {slug,key,href}[], unused: string[], skipped: string[] }>} */
export async function checkCitations({ slugs, citations, postsDir = POSTS_DIR, all = false }) {
  const missing = [];
  const skipped = [];
  const linked = new Set();
  for (const slug of slugs) {
    const { body } = readPost(slug, postsDir);
    if (hasSourcesHeading(body)) {
      skipped.push(slug);
      continue;
    }
    for (const l of await eligibleLinks(body)) {
      linked.add(l.key);
      if (!citations[l.key]) missing.push({ slug, key: l.key, href: l.href });
    }
  }
  const unused = all ? Object.keys(citations).filter((k) => !linked.has(k)) : [];
  return { missing, unused, skipped };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2).filter((a) => a !== '--');
  const strict = args.includes('--strict');
  const named = args.filter((a) => !a.startsWith('--'));
  const all = named.length === 0;
  const slugs = all ? allSlugs() : named;
  const { missing, unused, skipped } = await checkCitations({ slugs, citations: readCitations(CITATIONS_FILE), all });
  for (const m of missing) console.log(`missing  ${m.slug}  ${m.href}`);
  for (const k of unused) console.log(`unused   ${k}`);
  if (skipped.length) console.error(`(skipped, have a Sources list: ${skipped.length})`);
  console.error(`citations:check: ${missing.length} missing, ${unused.length} unused`);
  if (strict && (missing.length || unused.length)) process.exit(1);
}
