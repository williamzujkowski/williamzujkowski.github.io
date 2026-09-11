import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  selectPublishedPosts as selectAtDate, countPostTags, postPieceNumbers, postsByUTCYear,
} from '../../astro-site/src/lib/publication.mjs';

const selectPublishedPosts = (posts) => selectAtDate(posts, new Date('2026-09-11T00:00:00Z'));

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


test('scheduled publication opens at its UTC instant and never publishes explicit drafts', () => {
  const posts = [post('old', '2026-09-01'), post('scheduled', '2026-09-14'),
    post('later', '2026-09-21'), post('draft', '2026-09-01', { draft: true })];
  const ids = (date) => selectAtDate(posts, new Date(date)).map((p) => p.id);
  assert.deepEqual(ids('2026-09-13T23:59:59.999Z'), ['old']);
  assert.deepEqual(ids('2026-09-14T00:00:00.000Z'), ['scheduled', 'old']);
  assert.deepEqual(ids('2026-09-20T23:59:59.999Z'), ['scheduled', 'old']);
  assert.deepEqual(ids('2026-09-21T00:00:00.000Z'), ['later', 'scheduled', 'old']);
  assert.throws(() => selectAtDate(posts, new Date(NaN)), /valid Date/);
});

test('scheduled publication respects timestamp offsets and hides future taxonomy', () => {
  const posts = [post('utc', '2026-09-14T00:00:00Z', { tags: ['published'] }),
    post('offset', '2026-09-13T20:00:00-04:00'),
    post('later', '2026-09-14T00:00:00.001Z', { tags: ['future-only'] })];
  const selected = selectAtDate(posts, new Date('2026-09-14T00:00:00Z'));
  assert.deepEqual(selected.map((p) => p.id), ['offset', 'utc']);
  assert.deepEqual([...countPostTags(selected)], [['published', 1]]);
  assert.deepEqual([...postPieceNumbers(selected)], [['offset', 2], ['utc', 1]]);
});

test('publication cutoff is independent of the machine timezone', () => {
  const moduleUrl = new URL('../../astro-site/src/lib/publication.mjs', import.meta.url).href;
  const script = `import { selectPublishedPosts } from ${JSON.stringify(moduleUrl)};
    const posts = [{id:'scheduled',data:{date:new Date('2026-09-14')}}];
    console.log(JSON.stringify([
      selectPublishedPosts(posts,new Date('2026-09-13T23:59:59.999Z')).length,
      selectPublishedPosts(posts,new Date('2026-09-14T00:00:00Z')).length
    ]));`;
  for (const timezone of ['UTC', 'America/New_York', 'Pacific/Kiritimati']) {
    const result = spawnSync(process.execPath, ['--input-type=module', '-e', script], {
      encoding: 'utf8', env: { ...process.env, TZ: timezone },
    });
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(JSON.parse(result.stdout), [0, 1], timezone);
  }
});
