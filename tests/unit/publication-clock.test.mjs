import { test } from 'node:test';
import assert from 'node:assert/strict';
import { publicationClock } from '../../astro-site/src/lib/publication-clock.mjs';

const now = new Date('2026-09-11T15:00:00Z');

test('publication clock uses actual supplied time unless explicitly previewing', () => {
  assert.equal(publicationClock({}, now).toISOString(), now.toISOString());
  assert.notEqual(publicationClock({}, now), now);
  assert.equal(publicationClock({ CI: 'true' }, now).toISOString(), now.toISOString());
  for (const timestamp of ['2026-09-14T00:00:00Z', '2026-09-21T00:00:00.123Z']) {
    assert.equal(publicationClock({ PUBLICATION_AS_OF: timestamp }, now).getTime(), Date.parse(timestamp));
  }
  assert.throws(() => publicationClock({}, new Date(NaN)), /valid Date/);
});

test('preview overrides fail closed in CI and GitHub Actions', () => {
  for (const flag of ['CI', 'GITHUB_ACTIONS']) {
    for (const value of ['true', '1', 'false']) {
      assert.throws(() => publicationClock({ [flag]: value,
        PUBLICATION_AS_OF: '2026-09-21T00:00:00Z' }, now), /must not be set in CI/);
    }
  }
});

test('preview dates reject ambiguity, invalid calendar values and malformed timestamps', () => {
  for (const timestamp of ['', '2026-09-21', '2026-09-21T00:00:00',
    '2026-09-21T00:00:00+00:00', '2026-02-30T00:00:00Z',
    '2026-13-01T00:00:00Z', '2026-09-21T24:00:00Z', 'not-a-date']) {
    assert.throws(() => publicationClock({ PUBLICATION_AS_OF: timestamp }, now), TypeError, timestamp);
  }
});
