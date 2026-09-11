import { test, expect } from 'playwright/test';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const postsDir = fileURLToPath(new URL('../../../src/posts/', import.meta.url));
const drafts = readdirSync(postsDir).filter((file) => file.endsWith('.md')
  && /^draft:\s*true\s*$/m.test(readFileSync(join(postsDir, file), 'utf8').split('---')[1] || ''))
  .map((file) => file.replace(/\.md$/, ''));

interface FeedItem { url: string; content_html: string; tags?: string[] }

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
  const rssItems = await page.evaluate((xml) => {
    const document = new DOMParser().parseFromString(xml, 'application/xml');
    if (document.querySelector('parsererror')) throw new Error('RSS must be valid XML');
    return [...document.querySelectorAll('item')].map((item) => ({
      path: new URL(item.querySelector('link')!.textContent!).pathname,
      html: item.getElementsByTagNameNS('http://purl.org/rss/1.0/modules/content/', 'encoded')[0]?.textContent,
    }));
  }, await rss.text());
  expect(rssItems.map((item) => item.path)).toEqual(paths);
  expect(rssItems.map((item) => item.html)).toEqual(items.map((item) => item.content_html));

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


test('generated feed diagrams stay readable without site CSS', async ({ page, request }, testInfo) => {
  const response = await request.get('/feed.json');
  const items: FeedItem[] = (await response.json()).items;
  const findings = await page.evaluate((entries) => entries.flatMap((item) => {
    const document = new DOMParser().parseFromString(item.content_html, 'text/html');
    const problems: string[] = [];
    if (document.querySelector('script, style, iframe, object, embed, svg, math, [style], [data-feed-label], [data-feed-detail], [data-feed-doodle]')) {
      problems.push('active markup, CSS or temporary attributes');
    }
    for (const element of document.querySelectorAll('*')) {
      if ([...element.attributes].some((attribute) => /^on/i.test(attribute.name))) problems.push('event handler');
    }
    for (const reference of document.querySelectorAll('.footnote-ref a, a.footnote-backref')) {
      const id = reference.getAttribute('href')?.slice(1);
      if (!id || !document.getElementById(id)) problems.push('missing footnote target');
    }
    document.querySelectorAll('pre, code').forEach((element) => element.remove());
    if (/<(?:div|section|figure)\b[^>]*class=["'](?:arch|flow|zine)/.test(document.body.textContent ?? '')) {
      problems.push('escaped authored diagram');
    }
    return problems.map((problem) => `${item.url}: ${problem}`);
  }), items);
  expect(findings).toEqual([]);

  // Render actual feed HTML in an empty document. No site styles can rescue it.
  await page.route('**/*', (route) => route.abort());
  const samples = [
    { slug: '2025-09-20-iot-security-homelab-owasp', labels: ['IoT Testing VLAN 666', 'No Internet', 'IoTGoat Device', 'Packet Capture'] },
    { slug: '2025-10-06-automated-security-scanning-pipeline', labels: ['Critical', 'Block on Critical', 'Review', 'Manual Review'] },
  ];
  for (const sample of samples) {
    const item = items.find((entry) => entry.url.endsWith(`/posts/${sample.slug}/`));
    expect(item, sample.slug).toBeDefined();
    for (const width of [360, 1024]) {
      await page.setViewportSize({ width, height: 800 });
      await page.setContent(item!.content_html);
      expect(await page.locator('style, link[rel="stylesheet"]').count()).toBe(0);
      let previousY = -1;
      for (const label of sample.labels) {
        const element = page.getByText(label, { exact: true }).first();
        await expect(element).toBeVisible();
        const box = await element.boundingBox();
        expect(box!.y, `${sample.slug}: ${label}`).toBeGreaterThan(previousY);
        previousY = box!.y;
      }
      const label = page.getByText(sample.labels[0], { exact: true }).first();
      await label.scrollIntoViewIfNeeded();
      await page.screenshot({ path: testInfo.outputPath(`${sample.slug}-${width}.png`) });
    }
  }
});
