import { test } from 'node:test';
import assert from 'node:assert/strict';
import { postSchema } from '../../astro-site/src/lib/post-schema.mjs';
import { selectPublishedPosts } from '../../astro-site/src/lib/publication.mjs';

const minimal = { title: 'A security field note', date: '2026-09-10' };

test('schema defaults publish ordinary posts while explicit drafts stay unpublished', () => {
  const ordinary = postSchema.parse(minimal);
  assert.equal(ordinary.draft, false);
  assert.deepEqual(ordinary.tags, []);
  assert.equal(ordinary.author, 'William Zujkowski');
  const entries = [
    { id: 'ordinary', data: ordinary },
    { id: 'draft', data: postSchema.parse({ ...minimal, draft: true }) },
    { id: 'explicit', data: postSchema.parse({ ...minimal, draft: false }) },
  ];
  assert.deepEqual(selectPublishedPosts(entries).map((post) => post.id), ['explicit', 'ordinary']);
});

test('unknown metadata survives alongside validated series fields', () => {
  const input = {
    ...minimal, reading_time: '5 min', readingTime: 5,
    provenance: { fixture: true, sources: ['homelab'] },
    series: 'Agent permissions', seriesOrder: 2,
  };
  const parsed = postSchema.parse(input);
  for (const key of ['reading_time', 'readingTime', 'provenance', 'series', 'seriesOrder']) {
    assert.deepEqual(parsed[key], input[key]);
  }
  // Existing numeric ordering is deliberately unrestricted by this migration.
  assert.equal(postSchema.parse({ ...minimal, seriesOrder: -1.5 }).seriesOrder, -1.5);
});

test('invalid known fields fail validation instead of becoming defaults or metadata', () => {
  const invalid = [
    ['title', undefined], ['title', 12], ['draft', 'false'], ['draft', 0],
    ['tags', 'security'], ['tags', ['security', 1]], ['tags', null],
    ['author', null], ['series', 2], ['seriesOrder', '2'],
    ['date', 'not-a-date'], ['date', new Date(NaN)], ['lastUpdate', 'not-a-date'],
  ];
  for (const [field, value] of invalid) {
    const result = postSchema.safeParse({ ...minimal, [field]: value });
    assert.equal(result.success, false, `${field}: ${String(value)}`);
    assert.ok(result.error.issues.some((issue) => issue.path[0] === field), field);
  }
});

test('explicit metadata and existing date coercion remain unchanged', () => {
  const parsed = postSchema.parse({
    ...minimal, date: new Date('2026-09-10T00:00:00Z'),
    lastUpdate: '2026-09-11', description: 'A reproducible experiment.',
    author: 'Fixture author', tags: ['security'], post_type: 'research',
  });
  assert.equal(parsed.date.toISOString(), '2026-09-10T00:00:00.000Z');
  assert.equal(parsed.lastUpdate.toISOString(), '2026-09-11T00:00:00.000Z');
  assert.equal(parsed.description, 'A reproducible experiment.');
  assert.equal(parsed.author, 'Fixture author');
  assert.deepEqual(parsed.tags, ['security']);
  assert.equal(parsed.post_type, 'research');
  assert.equal(postSchema.parse(minimal).date.toISOString(), '2026-09-10T00:00:00.000Z');
  // z.coerce.date() already accepts these inputs; this is API migration,
  // not a new frontmatter date policy.
  for (const date of [null, 0]) {
    assert.equal(postSchema.parse({ ...minimal, date }).date.toISOString(), '1970-01-01T00:00:00.000Z');
  }
});
