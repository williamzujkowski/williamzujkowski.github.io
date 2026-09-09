import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  selectPublishedPosts, countPostTags, postPieceNumbers, postsByUTCYear,
} from '../../astro-site/src/lib/publication.mjs';

const post = (id, date, extra = {}) => ({ id, data: { date: new Date(date), ...extra } });

test('publication excludes a newest draft and has deterministic equal-date ordering', () => {
  const inputs = [
    post('z', '2026-01-01'), post('draft', '2027-01-01', { draft: true }),
    post('old', '2025-01-01'), post('a', '2026-01-01', { draft: false }),
  ];
  assert.deepEqual(selectPublishedPosts(inputs).map((p) => p.id), ['a', 'z', 'old']);
  assert.deepEqual(selectPublishedPosts([...inputs].reverse()).map((p) => p.id), ['a', 'z', 'old']);
});

test('publication metadata does not mutate frozen source collections or tag arrays', () => {
  const inputs = Object.freeze([
    Object.freeze(post('old', '2025-01-01', { tags: Object.freeze(['security', 'posts']) })),
    Object.freeze(post('new', '2026-01-01')),
  ]);
  const selected = selectPublishedPosts(inputs);
  countPostTags(inputs);
  postsByUTCYear(inputs);
  postPieceNumbers(inputs);
  assert.deepEqual(inputs.map((p) => p.id), ['old', 'new']);
  assert.deepEqual(selected.map((p) => p.id), ['new', 'old']);
});

test('tag counts measure distinct posts and exclude the reserved collection tag', () => {
  const posts = selectPublishedPosts([
    post('a', '2026-01-01', { tags: ['security', 'security', 'posts'] }),
    post('b', '2025-01-01', { tags: ['security', 'homelab'] }),
    post('c', '2024-01-01'),
    post('draft', '2027-01-01', { draft: true, tags: ['unpublished'] }),
  ]);
  assert.deepEqual([...countPostTags(posts)], [['security', 2], ['homelab', 1]]);
});

test('piece numbers remain canonical when rendering a filtered tag archive', () => {
  const posts = selectPublishedPosts([
    post('old', '2024-01-01'), post('new', '2026-01-01'), post('middle', '2025-01-01'),
  ]);
  const pieces = postPieceNumbers(posts);
  assert.deepEqual([pieces.get('new'), pieces.get('old')], [3, 1]);
  assert.deepEqual([...postPieceNumbers([])], []);
});

test('January 1 belongs to the same archive year in UTC and America/New_York', () => {
  const moduleUrl = new URL('../../astro-site/src/lib/publication.mjs', import.meta.url).href;
  const script = `import { postsByUTCYear } from ${JSON.stringify(moduleUrl)};
    console.log(JSON.stringify([...postsByUTCYear([
      {id:'new',data:{date:new Date('2025-01-01')}},
      {id:'old',data:{date:new Date('2024-12-31')}}
    ])].map(([year, posts]) => [year, posts.map(p => p.id)])));`;
  for (const timezone of ['UTC', 'America/New_York']) {
    const result = spawnSync(process.execPath, ['--input-type=module', '-e', script], {
      encoding: 'utf8', env: { ...process.env, TZ: timezone },
    });
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(JSON.parse(result.stdout), [[2025, ['new']], [2024, ['old']]], timezone);
  }
});
