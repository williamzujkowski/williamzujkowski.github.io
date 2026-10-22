// Tag consolidation (issue #698): the retired-tag map, its redirects, the
// schema that rejects retired tags, and the "most specific tag" kicker.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { RETIRED_TAGS, assertTagAliases, tagRedirects } from '../../astro-site/src/lib/tag-taxonomy.mjs';
import { countPostTags, kickerTag, selectPublishedPosts } from '../../astro-site/src/lib/publication.mjs';
import { postSchema } from '../../astro-site/src/lib/post-schema.mjs';

test('kicker is the tag on the fewest posts, ties broken by frontmatter order', () => {
  const counts = new Map([['security', 58], ['homelab', 42], ['docker', 4], ['container-security', 4]]);
  assert.equal(kickerTag({ tags: ['security', 'homelab', 'docker'] }, counts), 'docker');
  assert.equal(kickerTag({ tags: ['security', 'container-security', 'docker'] }, counts), 'container-security');
  assert.equal(kickerTag({ tags: ['security', 'docker', 'container-security'] }, counts), 'docker');
  // The reserved collection tag never labels a post; no tags means no kicker.
  assert.equal(kickerTag({ tags: ['posts', 'security'] }, new Map([['posts', 1], ['security', 58]])), 'security');
  assert.equal(kickerTag({ tags: [] }, counts), undefined);
  assert.equal(kickerTag({}, counts), undefined);
  // A tag with no page (absent from the counts) must not beat one that has a page.
  assert.equal(kickerTag({ tags: ['unknown', 'security'] }, counts), 'security');
});

test('the alias map rejects chains, self-maps and non-slugs', () => {
  assert.doesNotThrow(() => assertTagAliases(RETIRED_TAGS));
  assert.throws(() => assertTagAliases({ a: 'b', b: 'c' }), /chain: "a" -> "b"/);
  assert.throws(() => assertTagAliases({ a: 'a' }), /maps to itself/);
  assert.throws(() => assertTagAliases({ 'Bad Tag': 'security' }), /not a slug/);
  assert.throws(() => assertTagAliases({ a: 'Security' }), /non-slug/);
  assert.throws(() => tagRedirects({ a: 'b', b: null }), /chain/);
});

test('every retired tag gets one redirect; vague tags with no parent go to the index', () => {
  const redirects = tagRedirects();
  assert.equal(Object.keys(redirects).length, Object.keys(RETIRED_TAGS).length);
  assert.equal(redirects['/tags/oscal/'], '/tags/compliance/');
  assert.equal(redirects['/tags/breakthrough/'], '/tags/');
  for (const [from, to] of Object.entries(redirects)) {
    assert.match(from, /^\/tags\/[a-z0-9-]+\/$/);
    assert.match(to, /^\/tags\/(?:[a-z0-9-]+\/)?$/);
  }
});

// The corpus: frontmatter is the source of truth, so check it directly.
const postsDir = resolve(dirname(fileURLToPath(import.meta.url)), '../../src/posts');

/** Just the fields publication needs. Both list styles occur in the corpus. */
function frontmatter(file) {
  const raw = readFileSync(resolve(postsDir, file), 'utf8');
  const lines = raw.split('\n');
  const end = lines.indexOf('---', 1);
  const fm = lines.slice(1, end);
  const field = (name) => fm.find((line) => line.startsWith(`${name}:`))?.slice(name.length + 1).trim().replace(/^['"]|['"]$/g, '');
  const at = fm.findIndex((line) => line.startsWith('tags:'));
  let tags = [];
  const inline = fm[at]?.slice(5).trim();
  if (inline?.startsWith('[')) tags = inline.slice(1, -1).split(',').map((tag) => tag.trim()).filter(Boolean);
  else if (at >= 0) for (let i = at + 1; i < fm.length && /^\s*- /.test(fm[i]); i += 1) tags.push(fm[i].replace(/^\s*- /, '').trim());
  return { title: file, date: field('date'), draft: field('draft') === 'true', tags };
}

const corpus = readdirSync(postsDir).filter((file) => file.endsWith('.md'))
  .map((file) => ({ id: file, data: frontmatter(file) }));

test('the corpus parses (an empty walk is not a passing suite)', () => {
  assert.ok(corpus.length > 90, `found only ${corpus.length} posts`);
  assert.ok(corpus.every((post) => post.data.tags.length > 0), 'a post parsed with no tags');
});

test('no post, published or scheduled, uses a retired or malformed tag', () => {
  const offenders = corpus.flatMap((post) => {
    const result = postSchema.safeParse(post.data);
    return result.success ? [] : result.error.issues.map((issue) => `${post.id}: ${issue.message}`);
  });
  assert.deepEqual(offenders, []);
});

test('every redirect lands on a tag page that exists', () => {
  const published = selectPublishedPosts(corpus.map((post) => ({ ...post, data: postSchema.parse(post.data) })));
  const live = countPostTags(published);
  const dangling = Object.entries(RETIRED_TAGS).filter(([, to]) => to !== null && !live.has(to));
  assert.deepEqual(dangling, [], 'a redirect target has no published post, so its page 404s');
});
