import { test, expect } from 'playwright/test';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const postsDir = fileURLToPath(new URL('../../../src/posts/', import.meta.url));
const drafts = readdirSync(postsDir).filter((file) => file.endsWith('.md')
  && /^draft:\s*true\s*$/m.test(readFileSync(join(postsDir, file), 'utf8').split('---')[1] || ''))
  .map((file) => file.replace(/\.md$/, ''));

interface FeedItem { url: string; tags?: string[] }

test('archive, feeds, tags and generated cards share the published post set', async ({ page, request }) => {
  test.setTimeout(90_000);
  const feedResponse = await request.get('/feed.json');
  expect(feedResponse.ok()).toBe(true);
  const items: FeedItem[] = (await feedResponse.json()).items;
  expect(items.length).toBeGreaterThan(80);
  const paths = items.map((item) => new URL(item.url).pathname);
  expect(new Set(paths).size).toBe(paths.length);

  await page.goto('/posts/');
  const archive = await page.locator('.year-section .entry-title a').evaluateAll((links) =>
    links.map((link) => new URL((link as HTMLAnchorElement).href).pathname));
  expect(archive).toEqual(paths);
  const rss = await request.get('/feed.xml');
  expect(rss.ok()).toBe(true);
  const rssPaths = await page.evaluate((xml) => {
    const document = new DOMParser().parseFromString(xml, 'application/xml');
    return [...document.querySelectorAll('item > link')].map((link) => new URL(link.textContent!).pathname);
  }, await rss.text());
  expect(rssPaths).toEqual(paths);

  // Every card must exist. Check tags using the feed's independently rendered
  // categories, including canonical piece numbers after filtering.
  for (const path of paths) {
    const card = await request.get(`/og/${path.split('/')[2]}.png`);
    expect(card.ok(), path).toBe(true);
    expect(card.headers()['content-type']).toContain('image/png');
  }
  const tags = [...new Set(items.flatMap((item) => item.tags ?? []))];
  for (const tag of tags) {
    const response = await request.get(`/tags/${tag}/`);
    expect(response.ok(), tag).toBe(true);
    const { actual, pieces } = await page.evaluate((html) => {
      const document = new DOMParser().parseFromString(html, 'text/html');
      return {
        actual: [...document.querySelectorAll('.entry-title a')].map((link) => link.getAttribute('href')),
        pieces: [...document.querySelectorAll('.entry-numeral')].map((entry) => Number(entry.textContent)),
      };
    }, await response.text());
    expect(actual, tag).toEqual(items.filter((item) => item.tags?.includes(tag)).map((item) => new URL(item.url).pathname));
    expect(pieces, tag).toEqual(actual.map((path) => paths.length - paths.indexOf(path!)));
  }
});

test('drafts have no post or social image route and never appear in feeds', async ({ request }) => {
  expect(drafts.length).toBeGreaterThan(0);
  for (const format of ['json', 'xml']) {
    const response = await request.get(`/feed.${format}`);
    for (const slug of drafts) expect(await response.text()).not.toContain(`/posts/${slug}/`);
  }
  for (const slug of drafts) {
    expect((await request.get(`/posts/${slug}/`)).status()).toBe(404);
    expect((await request.get(`/og/${slug}.png`)).status()).toBe(404);
  }
});

test('archive year and page edit date reflect content dates', async ({ page }) => {
  await page.goto('/posts/');
  const welcomeYear = page.locator('.year-section').filter({ has: page.locator('a[href="/posts/welcome/"]') });
  await expect(welcomeYear.locator('.year-number')).toHaveText('2025');
  await page.goto('/uses/');
  const edited = page.locator('p').filter({ hasText: 'Page last edited' });
  await expect(edited.locator('time')).toHaveAttribute('datetime', '2026-09-08');
});
