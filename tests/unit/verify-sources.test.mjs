// Unit tests for citations:verify-sources comparison logic. No network: fixtures only.
import test from 'node:test';
import assert from 'node:assert/strict';
import {
  tokens, titleOverlap, entryAuthors, authorsMissing, entryYears, yearMismatch,
  classifyStatus, redirectProblem, registrable, compareEntry, pageFacts, sourcesEntries,
} from '../../astro-site/scripts/citations/verify-sources.mjs';

test('tokens: drops stop words, folds case and diacritics, stems plurals', () => {
  assert.deepEqual([...tokens('The Éthics of Models')].sort(), ['ethic', 'model']);
});

test('titleOverlap: a shortened title still matches; an unrelated one does not', () => {
  assert.equal(titleOverlap('Attention Is All You Need', ['Attention Is All You Need | arXiv']).score, 1);
  assert.ok(titleOverlap('Self-Refine: Iterative Refinement with Self-Feedback', ['Self-Refine: Iterative Refinement with Self-Feedback']).score === 1);
  assert.ok(titleOverlap('Quantum Supremacy Using a Programmable Superconducting Processor', ['Welcome to a gaming site']).score < 0.5);
});

test('titleOverlap: URL words and run-together names count', () => {
  assert.equal(titleOverlap('HackTheBox', ['Cyber Mastery | Hack The Box']).score, 1);
  assert.equal(titleOverlap('Wazuh Documentation', ['Introduction'], 'documentation.wazuh.com current').score, 1);
});

test('titleOverlap: no page title means nothing to compare', () => {
  assert.equal(titleOverlap('Anything', []).score, 1);
});

test('entryAuthors: et al., by-lines, initials, and organisations skipped', () => {
  assert.deepEqual(entryAuthors('Wei et al. (2022)'), ['Wei']);
  assert.deepEqual(entryAuthors('O’Reilly book by Gilman and Barth').sort(), ['Barth', 'Gilman']);
  assert.deepEqual(entryAuthors('Vaswani, A., Shazeer, N. (2017)').sort(), ['Shazeer', 'Vaswani']);
  assert.deepEqual(entryAuthors('Google Coral Team'), []);
  assert.deepEqual(entryAuthors('NIST and CISA'), []);
});

test('entryAuthors: a name inside the title is not an author claim', () => {
  assert.deepEqual(entryAuthors('Turing et al.', 'The Turing Test'), []);
});

test('authorsMissing: metadata or page text satisfies; absence flags', () => {
  assert.deepEqual(authorsMissing(['Vaswani'], ['Vaswani, Ashish', 'Shazeer, Noam']), []);
  assert.deepEqual(authorsMissing(['Gidney'], [], 'by Craig Gidney and Martin Ekera'), []);
  assert.deepEqual(authorsMissing(['Wei'], ['Zhou, Denny']), ['Wei']);
  assert.deepEqual(authorsMissing(['Ekerå'], ['Ekera, Martin']), []);
});

test('entryYears: finds years, ignores URLs, versions and decimals', () => {
  assert.deepEqual(entryYears('Paper (2019) at https://x.org/2015/page, v1.2000'), [2019]);
  assert.deepEqual(entryYears('Too far ahead 2099 and 1999', 2026), [1999]);
});

test('yearMismatch: only when every entry year is more than 1 from the page year', () => {
  assert.equal(yearMismatch([2023], 2024), null);
  assert.equal(yearMismatch([2019, 2024], 2024), null);
  assert.deepEqual(yearMismatch([2019], 2024), { entryYears: [2019], pageYear: 2024 });
  assert.equal(yearMismatch([], 2024), null);
  assert.equal(yearMismatch([2019], null), null);
});

test('classifyStatus: bot blocks are unverifiable, 404/500 are dead', () => {
  assert.equal(classifyStatus(200), 'ok');
  assert.equal(classifyStatus(301), 'ok');
  assert.equal(classifyStatus(403), 'unverifiable');
  assert.equal(classifyStatus(429), 'unverifiable');
  assert.equal(classifyStatus(404), 'dead');
  assert.equal(classifyStatus(410), 'dead');
  assert.equal(classifyStatus(503), 'dead');
});

test('redirectProblem: host change and homepage landing are problems; www and doi.org are not', () => {
  assert.equal(registrable('docs.example.co.uk'), 'example.co.uk');
  assert.equal(redirectProblem('https://example.com/a/b', 'https://www.example.com/a/b'), null);
  assert.equal(redirectProblem('https://docs.example.com/a', 'https://example.com/b'), null);
  assert.match(redirectProblem('https://old.example/a', 'https://other.example/a'), /unrelated host/);
  assert.match(redirectProblem('https://example.com/a/b', 'https://example.com/'), /homepage/);
  assert.equal(redirectProblem('https://doi.org/10.1/x', 'https://journal.example/x'), null);
});

const page = pageFacts(`<html><head><title>Chain of Thought Prompting | arXiv</title>
<meta name="citation_title" content="Chain-of-Thought Prompting Elicits Reasoning in Large Language Models">
<meta name="citation_author" content="Wei, Jason"><meta name="citation_author" content="Wang, Xuezhi">
<meta name="citation_date" content="2022/01/28"></head><body><h1>Chain</h1></body></html>`, 'arxiv.org');

test('pageFacts: repeated citation_author kept, date parsed to a year', () => {
  assert.deepEqual(page.authors, ['Wei, Jason', 'Wang, Xuezhi']);
  assert.equal(page.year, 2022);
  assert.equal(page.titles[0], 'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models');
});

test('pageFacts: JSON-LD author and datePublished are read', () => {
  const p = pageFacts('<script type="application/ld+json">{"@type":"Article","author":{"name":"Ada Lovelace"},"datePublished":"2019-05-01"}</script>');
  assert.deepEqual(p.authors, ['Ada Lovelace']);
  assert.equal(p.year, 2019);
});

test('compareEntry: a correct entry raises nothing', () => {
  const e = { title: 'Chain-of-Thought Prompting Elicits Reasoning', authors: ['Wei'], years: [2022] };
  assert.deepEqual(compareEntry(e, page), []);
});

test('compareEntry: wrong author, year and title are each flagged', () => {
  const e = { title: 'Retrieval Augmented Generation for Knowledge Tasks', authors: ['Lewis'], years: [2019] };
  assert.deepEqual(compareEntry(e, page).map((f) => f.kind), ['title-mismatch', 'author-missing', 'year-mismatch']);
});

test('compareEntry: an interstitial page title is not compared', () => {
  const e = { title: 'Some Real Paper Title', authors: [], years: [] };
  assert.deepEqual(compareEntry(e, { titles: ['Client Challenge'], authors: [], year: null, text: '' }), []);
});

test('sourcesEntries: first link keys the entry, nested lines join the text, bare URLs and relative links handled', async () => {
  const body = [
    'Intro.', '', '## Sources', '',
    '- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (2017)',
    '   - Vaswani et al.',
    '2. Some Standard - description. https://example.org/std',
    '- [Own post](/posts/x)',
    '', '## Later', '', '- [Not a source](https://example.net/)',
  ].join('\n');
  const es = await sourcesEntries(body);
  assert.equal(es.length, 3);
  assert.equal(es[0].url, 'https://arxiv.org/abs/1706.03762');
  assert.equal(es[0].title, 'Attention Is All You Need');
  assert.deepEqual(es[0].authors, ['Vaswani']);
  assert.deepEqual(es[0].years, [2017]);
  assert.equal(es[1].title, 'Some Standard');
  assert.equal(es[2].skip, true);
});
