/**
 * Frontmatter titles/descriptions never pass through remark-smartypants;
 * the post schema curls them with this helper. Paired negatives: code in
 * backticks keeps its straight quotes.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { smartQuotes } from '../../astro-site/src/lib/smart-quotes.mjs';

test('apostrophes inside and closing words become ’', () => {
  assert.equal(smartQuotes("A Correct Answer Doesn't Mean the Agent's Memory Is Clean"),
    'A Correct Answer Doesn’t Mean the Agent’s Memory Is Clean');
  assert.equal(smartQuotes("the users' keys"), 'the users’ keys');
});

test('double quotes open and close by position', () => {
  assert.equal(smartQuotes('What We Mean by "Typography-First"'), 'What We Mean by “Typography-First”');
  assert.equal(smartQuotes('"Quoted" first'), '“Quoted” first');
});

test('backticked code and quote-free strings are untouched', () => {
  assert.equal(smartQuotes("Run `echo 'hi'` and it's done"), "Run `echo 'hi'` and it’s done");
  assert.equal(smartQuotes('No quotes here'), 'No quotes here');
  assert.equal(smartQuotes(undefined), undefined);
});
