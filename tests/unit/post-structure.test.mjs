// Structural invariants over the post corpus (issue #498).
//
// These are not style opinions — they are things that render visibly wrong
// and that no existing gate could see. `PostLayout.astro` emits the <h1> from
// frontmatter, so a `# Title` in the body renders the title TWICE at display
// size and puts two top-level headings in the accessibility outline.
//
// Eight posts had it. axe's `heading-order` does not fire (no level JUMP,
// just a repeat) and there is no "exactly one h1" rule in the wcag2a/wcag2aa
// tag set the axe suite selects, so CI was green on all eight.
//
// Lives here rather than in the advisory compliance script because this runs
// in audits.yml's `check-lint` job, which is a required check.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const postsDir = resolve(dirname(fileURLToPath(import.meta.url)), '../../src/posts');
const posts = readdirSync(postsDir).filter((f) => f.endsWith('.md'));

/** Body text with frontmatter and fenced code blocks removed. */
function bodyLines(raw) {
  const parts = raw.split('---');
  const body = parts.length >= 3 ? parts.slice(2).join('---') : raw;
  const out = [];
  let inFence = false;
  for (const line of body.split('\n')) {
    if (line.trim().startsWith('```')) { inFence = !inFence; continue; }
    if (!inFence) out.push(line);
  }
  return out;
}

test('the corpus is non-empty (an empty walk is not a passing suite)', () => {
  assert.ok(posts.length > 50, `found only ${posts.length} posts under ${postsDir}`);
});

test('no post carries a body-level H1 — the layout already renders the title', () => {
  const offenders = [];
  for (const name of posts) {
    const bad = bodyLines(readFileSync(join(postsDir, name), 'utf8')).find((l) =>
      /^#\s+\S/.test(l),
    );
    if (bad) offenders.push(`${name}: ${bad.trim().slice(0, 60)}`);
  }
  assert.deepEqual(
    offenders,
    [],
    `PostLayout.astro emits <h1>{title}</h1>, so these render the title twice:\n  ${offenders.join('\n  ')}`,
  );
});

test('every post has frontmatter delimiters', () => {
  const offenders = posts.filter((n) => !readFileSync(join(postsDir, n), 'utf8').startsWith('---'));
  assert.deepEqual(offenders, [], `missing opening frontmatter: ${offenders.join(', ')}`);
});
