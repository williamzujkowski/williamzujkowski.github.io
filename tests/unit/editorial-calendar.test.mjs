// Scheduled posts must not collide (see astro-site/src/lib/editorial-calendar.mjs).
//
// The fixture tests plant each conflict and require the checker to report it;
// a checker that returned [] for everything would pass the corpus test alone.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { calendarConflicts } from '../../astro-site/src/lib/editorial-calendar.mjs';

const postsDir = resolve(dirname(fileURLToPath(import.meta.url)), '../../src/posts');
const NOW = new Date('2026-10-01T12:00:00Z');
const post = (file, date, draft = false) => ({ file, date: new Date(`${date}T00:00:00Z`), draft });

test('a clean weekly schedule reports nothing', () => {
  const posts = [
    post('2026-09-28-a.md', '2026-09-28'),
    post('2026-10-08-b.md', '2026-10-08'),
    post('2026-10-15-c.md', '2026-10-15'),
  ];
  assert.deepEqual(calendarConflicts(posts, NOW), []);
});

test('two scheduled posts on the same day are a conflict', () => {
  const out = calendarConflicts([post('2026-10-08-a.md', '2026-10-08'), post('2026-10-08-b.md', '2026-10-08')], NOW);
  assert.equal(out.length, 1);
  assert.match(out[0], /same day/);
});

test('a scheduled post too close to the newest published post is a conflict', () => {
  const out = calendarConflicts([post('2026-09-30-a.md', '2026-09-30'), post('2026-10-02-b.md', '2026-10-02')], NOW);
  assert.equal(out.length, 1);
  assert.match(out[0], /2 day\(s\) after 2026-09-30-a\.md/);
});

test('a rescheduled post whose filename kept the old date is a conflict', () => {
  const out = calendarConflicts([post('2026-10-08-a.md', '2026-10-22')], NOW);
  assert.equal(out.length, 1);
  assert.match(out[0], /filename/);
});

test('drafts and published history are out of scope', () => {
  const posts = [
    post('2024-05-14-old.md', '2024-11-19'),
    post('2026-08-18-x.md', '2026-08-18'),
    post('2026-08-18-y.md', '2026-08-18'),
    post('2026-10-02-draft.md', '2026-10-02', true),
  ];
  assert.deepEqual(calendarConflicts(posts, NOW), []);
});

test('the real corpus has no scheduling conflicts', () => {
  const files = readdirSync(postsDir).filter((f) => /^\d{4}-\d{2}-\d{2}-.*\.md$/.test(f));
  assert.ok(files.length > 50, `found only ${files.length} posts under ${postsDir}`);
  const posts = files.map((file) => {
    const fm = readFileSync(join(postsDir, file), 'utf8').split('---')[1] ?? '';
    const date = fm.match(/^date:\s*["']?(\d{4}-\d{2}-\d{2})/m);
    assert.ok(date, `${file}: no parseable date`);
    return { file, date: new Date(`${date[1]}T00:00:00Z`), draft: /^draft:\s*true\b/m.test(fm) };
  });
  const problems = calendarConflicts(posts, new Date());
  assert.deepEqual(problems, [], `scheduling conflicts:\n  ${problems.join('\n  ')}`);
});
