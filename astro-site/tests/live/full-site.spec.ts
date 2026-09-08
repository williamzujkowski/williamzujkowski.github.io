import { test, expect } from 'playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readdirSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, relative } from 'node:path';

const build = fileURLToPath(new URL('../../dist/', import.meta.url));
function htmlFiles(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? htmlFiles(path) : entry.name.endsWith('.html') ? [path] : [];
  });
}
const files = htmlFiles(build);
if (files.length < 90) throw new Error(`Expected the full site build, found only ${files.length} pages`);
const routes = files.map((file) => `/${relative(build, file).replace(/index\.html$/, '')}`);
const postsDir = fileURLToPath(new URL('../../../src/posts/', import.meta.url));
const draftSlugs = readdirSync(postsDir).filter((name) => name.endsWith('.md')
  && /^draft:\s*true\s*$/m.test(readFileSync(join(postsDir, name), 'utf8').split('---')[1] || ''))
  .map((name) => name.slice(0, -3));
const fetched = new Map<string, Promise<{ status: number; html: string }>>();

for (const route of routes) {
  test(route, async ({ page, request, baseURL }) => {
    const origin = new URL(baseURL!).origin;
    const badResponses: string[] = [];
    const runtimeErrors: string[] = [];
    page.on('pageerror', (error) => runtimeErrors.push(error.message));
    page.on('requestfailed', (request) => {
      if (new URL(request.url()).origin === origin) {
        runtimeErrors.push(`${request.failure()?.errorText} ${request.url()}`);
      }
    });
    page.on('response', (response) => {
      const url = new URL(response.url());
      if (url.origin === origin && response.status() >= 400 && url.pathname !== '/404.html') {
        badResponses.push(`${response.status()} ${url.pathname}`);
      }
    });
    const response = await page.goto(route);
    expect(response).not.toBeNull();
    expect(route === '/404.html' ? [200, 404] : [200]).toContain(response!.status());
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('h1')).toHaveCount(1);
    await page.evaluate(() => document.fonts.ready);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    const canonical = await page.locator('link[rel=canonical]').getAttribute('href');
    // Astro emits its error route as 404.html, with the logical /404 canonical.
    expect(new URL(canonical!).pathname.replace(/\/$/, '')).toBe((route === '/404.html' ? '/404' : route).replace(/\/$/, ''));

    const references = await page.evaluate(() => Array.from(document.querySelectorAll('a[href], img[src], link[rel=stylesheet]'))
      .map((el) => el.getAttribute('href') || el.getAttribute('src') || '')
      .filter(Boolean));
    for (const reference of references) {
      const url = new URL(reference, page.url());
      if (url.origin !== origin || !['http:', 'https:'].includes(url.protocol)) continue;
      const fragment = url.hash ? decodeURIComponent(url.hash.slice(1)) : '';
      url.hash = '';
      if (!fetched.has(url.href)) {
        fetched.set(url.href, request.get(url.href, { timeout: 15_000 }).then(async (r) => ({
          status: r.status(), html: r.headers()['content-type']?.includes('text/html') ? await r.text() : '',
        })));
      }
      const { status, html } = await fetched.get(url.href)!;
      expect(url.pathname === '/404.html' ? [200, 404] : [200], reference).toContain(status);
      if (fragment && html) {
        expect(await page.evaluate(({ html, fragment }) => {
          const doc = new DOMParser().parseFromString(html, 'text/html');
          return !!doc.getElementById(fragment) || doc.getElementsByName(fragment).length > 0;
        }, { html, fragment }), reference).toBe(true);
      }
    }
    const audit = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
    expect(audit.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.map((n) => n.target) }))).toEqual([]);
    expect(badResponses).toEqual([]);
    expect(runtimeErrors).toEqual([]);
  });
}

test('feeds, sitemap and built route inventory agree on published drafts', async ({ request }) => {
  for (const path of ['/feed.xml', '/feed.json', '/sitemap-index.xml', '/sitemap-0.xml']) {
    const response = await request.get(path);
    expect(response.status()).toBe(200);
    const body = await response.text();
    for (const slug of draftSlugs) expect(body).not.toContain(slug);
    if (path === '/feed.json') expect(JSON.parse(body).items.length).toBeGreaterThan(80);
    if (path === '/sitemap-0.xml') {
      const local = readFileSync(join(build, 'sitemap-0.xml'), 'utf8');
      const locations = (xml: string) => Array.from(xml.matchAll(/<loc>(.*?)<\/loc>/g), (m) => new URL(m[1]).pathname).sort();
      expect(locations(body)).toEqual(locations(local));
    }
  }
});

test('search recovery, real query, theme persistence and reading paths', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Search site', exact: true }).click();
  await page.getByRole('textbox', { name: 'Search site content' }).waitFor();
  await page.keyboard.press('Control+k');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).toHaveCount(0);
  expect(await page.locator('[data-search-inert]').count()).toBe(0);
  await page.getByRole('button', { name: 'Search site', exact: true }).click();
  await page.getByRole('textbox', { name: 'Search site content' }).fill('ebpf');
  await expect(page.locator('.search-results a').first()).toHaveAttribute('href', /\/posts\//);
  const destinations = await page.locator('.search-results a').evaluateAll((links) => links.map((link) => link.getAttribute('href')));
  expect(destinations.every((url) => !/^\/(tags|404|posts\/$)/.test(url!))).toBe(true);
  await page.keyboard.press('Escape');
  const toggle = page.locator('#theme-toggle');
  const before = await toggle.getAttribute('aria-label');
  await toggle.click();
  await expect(toggle).not.toHaveAttribute('aria-label', before!);
  const selected = await toggle.getAttribute('aria-label');
  await page.reload();
  await expect(toggle).toHaveAttribute('aria-label', selected!);
  await page.locator('a[href="/posts/#start-here"]').click();
  await expect(page.locator('#start-here')).toBeVisible();
});

test('reading paths work without JavaScript', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, baseURL });
  try {
    const page = await context.newPage();
    await page.goto('/posts/#start-here');
    await expect(page.locator('#start-here a')).toHaveCount(6);
    await page.locator('#start-here a').first().click();
    await expect(page.locator('article')).toBeVisible();
  } finally {
    await context.close();
  }
});
