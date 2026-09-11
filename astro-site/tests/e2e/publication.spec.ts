import { test, expect } from 'playwright/test';
import { expectedPosts, hiddenPosts } from '../helpers/publication';

interface FeedItem { url: string; content_html: string; tags?: string[] }

test('archive, feeds, tags and generated cards share the published post set', async ({ page, request }) => {
  test.setTimeout(90_000);
  const feedResponse = await request.get('/feed.json');
  expect(feedResponse.ok()).toBe(true);
  const items: FeedItem[] = (await feedResponse.json()).items;
  expect(items.length).toBeGreaterThan(80);
  const paths = items.map((item) => new URL(item.url).pathname);
  expect(new Set(paths).size).toBe(paths.length);
  expect(paths).toEqual(expectedPosts.map((post) => `/posts/${post.id}/`));

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

test('drafts and future posts have no routes, listing metadata or search entries', async ({ page, request }) => {
  expect(hiddenPosts.length).toBeGreaterThan(0);
  for (const path of ['/', '/posts/', '/tags/', '/feed.json', '/feed.xml', '/sitemap-0.xml']) {
    const response = await request.get(path);
    expect(response.ok(), path).toBe(true);
    const body = await response.text();
    for (const post of hiddenPosts) expect(body, `${path}: ${post.id}`).not.toContain(`/posts/${post.id}/`);
  }
  const publishedTags = new Set(expectedPosts.flatMap((post) => post.data.tags));
  for (const post of hiddenPosts) {
    expect((await request.get(`/posts/${post.id}/`)).status()).toBe(404);
    expect((await request.get(`/og/${post.id}.png`)).status()).toBe(404);
    for (const tag of post.data.tags) {
      if (tag !== 'posts' && !publishedTags.has(tag)) {
        expect((await request.get(`/tags/${encodeURIComponent(tag)}/`)).status()).toBe(404);
      }
    }
  }
  await page.goto('/');
  const queries = ['ebpf', ...hiddenPosts.map((post) => post.data.title)];
  const results = await page.evaluate(async (terms) => {
    const moduleUrl = `${window.location.origin}/pagefind/pagefind.js`;
    const pagefind = await import(/* @vite-ignore */ moduleUrl);
    const matches: string[][] = [];
    for (const term of terms) {
      const result = await pagefind.search(term);
      const data = await Promise.all(result.results.map((entry: { data: () => Promise<{ url: string }> }) => entry.data()));
      matches.push(data.map((item: { url: string }) => new URL(item.url, window.location.origin).pathname));
    }
    return matches;
  }, queries);
  expect(results[0].length).toBeGreaterThan(0); // Prove the real index loaded.
  for (const paths of results) {
    for (const post of hiddenPosts) expect(paths).not.toContain(`/posts/${post.id}/`);
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
        // Prior samples scroll for screenshots; compare document coordinates.
        const documentY = box!.y + await page.evaluate(() => window.scrollY);
        expect(documentY, `${sample.slug}: ${label}`).toBeGreaterThan(previousY);
        previousY = documentY;
      }
      const label = page.getByText(sample.labels[0], { exact: true }).first();
      await label.scrollIntoViewIfNeeded();
      await page.screenshot({ path: testInfo.outputPath(`${sample.slug}-${width}.png`) });
    }
  }
});
