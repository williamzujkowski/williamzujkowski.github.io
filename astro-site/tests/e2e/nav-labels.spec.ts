import { test, expect, type Page } from 'playwright/test';

/**
 * One name per section (issue #698, option C). The masthead said "Colophon"
 * and opened a page titled "About"; four of six labels disagreed with the
 * <h1>/<title> of the page they led to, and breadcrumbs said "Home / Blog".
 *
 * Everything here is read from the RENDERED masthead, so renaming a label
 * without renaming its page (or the reverse) fails.
 */

const POST = '/posts/2024-01-08-writing-secure-code-developers-guide/';

async function navLinks(page: Page) {
  await page.goto('/');
  const links = page.locator('nav[aria-label="Primary navigation"] a');
  const out: { label: string; href: string }[] = [];
  for (const a of await links.all()) {
    out.push({ label: (await a.textContent())!.trim(), href: (await a.getAttribute('href'))! });
  }
  expect(out.length).toBe(6);
  return out;
}

async function schemaCrumbs(page: Page) {
  const blocks = await page.locator('script[type="application/ld+json"]').allTextContents();
  const list = blocks.map((b) => JSON.parse(b)).find((s) => s['@type'] === 'BreadcrumbList');
  return (list?.itemListElement ?? []) as { name: string; item: string }[];
}

test('every nav label names its destination: <h1>, <title> and breadcrumb schema', async ({ page }) => {
  const links = await navLinks(page);
  for (const { label, href } of links) {
    await page.goto(href);
    const word = new RegExp(`\\b${label}\\b`);
    // sr-only headings count: /posts/ and / carry the label for screen readers.
    const h1 = (await page.locator('main h1').first().textContent())!.trim();
    expect(h1, `${href} <h1>`).toMatch(word);
    const title = await page.title();
    if (href === '/') {
      // The front page's <title> is the brand on its own; brand is not a section.
      expect(title).toBe('William Zujkowski');
    } else {
      expect(title, `${href} <title>`).toMatch(new RegExp(`^${label} - `));
      const crumbs = await schemaCrumbs(page);
      expect(crumbs.map((c) => c.name)).toEqual(['Front', label]);
    }
    await expect(
      page.locator('nav[aria-label="Primary navigation"] a[aria-current="page"]'),
      `${href} highlights its own label`,
    ).toHaveText(label);
  }
});

for (const path of [POST, '/tags/security/']) {
  test(`breadcrumbs on ${path} use the nav labels`, async ({ page }) => {
    const links = await navLinks(page);
    const labelFor = (href: string) => links.find((l) => l.href === href)!.label;
    await page.goto(path);

    const crumbLinks = page.locator('nav[aria-label="Breadcrumb"] a');
    await expect(crumbLinks.nth(0)).toHaveText(labelFor('/'));
    await expect(crumbLinks.nth(0)).toHaveAttribute('href', '/');
    await expect(crumbLinks.nth(1)).toHaveText(labelFor('/posts/'));
    await expect(crumbLinks.nth(1)).toHaveAttribute('href', '/posts/');

    const names = (await schemaCrumbs(page)).map((c) => c.name);
    expect(names.slice(0, 2)).toEqual([labelFor('/'), labelFor('/posts/')]);

    // Posts and tag pages both live under Dispatches.
    await expect(
      page.locator('nav[aria-label="Primary navigation"] a[aria-current="page"]'),
    ).toHaveText(labelFor('/posts/'));
  });
}

test('404 chips use the nav labels', async ({ page }) => {
  const links = await navLinks(page);
  await page.goto('/404.html');
  for (const href of ['/', '/posts/']) {
    const label = links.find((l) => l.href === href)!.label;
    await expect(page.locator(`main a.chip[href="${href}"]`)).toContainText(label);
  }
});
