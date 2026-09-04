// Invariants over what is INSIDE fenced code blocks.
//
// A reader copy-pastes code blocks. Prose can be a little wrong and still
// inform; a command that does not run is worse than no command, because it
// costs the reader the time to find out.
//
// Fifteen lines across five posts had markdown link syntax wrapped around the
// URL inside a fence, all self-referential `[url](url)`:
//
//     curl -sSL [https://install.pi-hole.net](https://install.pi-hole.net) | bash
//     self.nvd_base = "[https://services.nvd.nist.gov/...](https://services...)"
//
// The first is a broken shell command. The second is worse -- it is a Python
// string whose VALUE is markdown, so the code parses, runs, and requests a
// nonsense URL. Nothing could see it: the syntax is valid markdown, the fence
// is never rendered as links, and the link checker extracted the href and
// reported it healthy, because as a URL it is.
//
// Runs in audits.yml's `check-lint`, a required check.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const postsDir = resolve(dirname(fileURLToPath(import.meta.url)), '../../src/posts');
const posts = readdirSync(postsDir).filter((f) => f.endsWith('.md'));

/** Lines inside fenced code blocks, as [lineNumber, text] pairs. */
export function fencedLines(raw) {
  const out = [];
  let inFence = false;
  raw.split('\n').forEach((line, i) => {
    if (line.trim().startsWith('```')) { inFence = !inFence; return; }
    if (inFence) out.push([i + 1, line]);
  });
  return out;
}

const MARKDOWN_LINK = /\[[^\]\n]*\]\((https?:\/\/[^)\s]+)\)/;

test('no markdown link syntax inside fenced code blocks', () => {
  const offenders = [];
  for (const file of posts) {
    const raw = readFileSync(join(postsDir, file), 'utf8');
    for (const [lineNo, line] of fencedLines(raw)) {
      if (MARKDOWN_LINK.test(line)) offenders.push(`${file}:${lineNo}  ${line.trim()}`);
    }
  }
  assert.deepEqual(
    offenders, [],
    `Markdown link syntax inside a code fence. A reader copy-pastes these:\n  ${offenders.join('\n  ')}`,
  );
});

test('the fence tracker actually finds fenced content', () => {
  // Guards the test above against passing for the wrong reason. If fencedLines
  // ever returned nothing, the assertion would be vacuously true across all 92
  // posts and this file would report success while checking nothing.
  const total = posts.reduce(
    (n, f) => n + fencedLines(readFileSync(join(postsDir, f), 'utf8')).length, 0);
  assert.ok(total > 1000, `expected thousands of fenced lines in the corpus, saw ${total}`);
});
