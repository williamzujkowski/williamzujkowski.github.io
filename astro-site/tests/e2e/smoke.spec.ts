import { test, expect } from 'playwright/test';

// Smoke tests — verify key pages load and interactive features work.
// NOT visual regression. Just structural checks.

const pages = [
  { path: '/', title: 'William Zujkowski', selector: 'h1' },
  { path: '/about/', title: 'About', selector: 'h1' },
  { path: '/posts/', title: 'Blog', selector: 'h1' },
  { path: '/projects/', title: 'Projects', selector: 'h1' },
  { path: '/uses/', title: 'Uses', selector: 'h1' },
  { path: '/now/', title: 'Now', selector: 'h1' },
  { path: '/tags/', title: 'Tags', selector: 'h1' },
];

for (const page of pages) {
  test(`${page.path} loads with status 200`, async ({ page: p }) => {
    const response = await p.goto(page.path);
    expect(response?.status()).toBe(200);
    await expect(p.locator(page.selector).first()).toBeVisible();
  });
}

test('404 page renders correctly', async ({ page }) => {
  // 404.html exists at /404.html in the built output.
  // Astro preview server may not serve it at /404/ — test the direct path.
  // No `if (response?.status() === 200)` guard: wrapping the body in one made
  // this test pass when 404.html was missing from the build entirely, which is
  // precisely the regression it exists to catch. The preview server does serve
  // /404.html directly, so assert unconditionally.
  const response = await page.goto('/404.html');
  expect(response?.status()).toBe(200);
  await expect(page.locator('text=Page not found')).toBeVisible();
  await expect(page.locator('text=Recent Posts')).toBeVisible();
  // On live GitHub Pages, 404.html is served for missing routes automatically
});

test('dark mode toggle switches theme', async ({ page }) => {
  await page.goto('/');
  const html = page.locator('html');

  // The root element always carries `class="scroll-smooth"`, so the old
  // `expect(classAfter).toBeTruthy()` was satisfied before the toggle was
  // even clicked — removing ThemeToggle.astro's click listener outright
  // still passed. Assert the *theme* class specifically, and that it moved.
  const classBefore = (await html.getAttribute('class')) ?? '';
  expect(classBefore, 'a fresh load must not already be pinned dark').not.toMatch(/\bdark\b/);

  // Click dark mode toggle (aria-label is "Switch to dark/light theme")
  const toggle = page.locator('button[aria-label*="theme"]');
  await toggle.first().click();

  await expect(html).toHaveClass(/\bdark\b/);
  expect(await html.getAttribute('class'), 'theme class must change on click').not.toBe(
    classBefore
  );

  // Round-trip: a second click must go back to light, so a toggle that only
  // ever adds `dark` fails here rather than passing the first assertion.
  await toggle.first().click();
  await expect(html).toHaveClass(/\blight\b/);
  await expect(html).not.toHaveClass(/\bdark\b/);
});

test('search dialog opens and closes', async ({ page }) => {
  await page.goto('/');

  // Open search
  const searchButton = page.locator('button:has-text("Search"), button[aria-label*="Search"]');
  await searchButton.first().click();

  // Dialog should be visible
  const dialog = page.locator('[role="dialog"], dialog');
  await expect(dialog.first()).toBeVisible();
  // Search.svelte focuses the input on a 50ms timer after mount. Waiting for
  // that settles the open before the Escape below, and is itself the modal's
  // focus-management contract.
  await expect(dialog.locator('input').first()).toBeFocused();

  // Close with Escape. The test is named "opens AND closes" but used to end
  // on the keypress with nothing asserted after it, so a broken/absent
  // Escape handler passed. Search.svelte's `{#if isOpen}` unmounts the
  // overlay, so a real close means the node is gone.
  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
});

test('primary nav is visible on small viewport', async ({ page }) => {
  // The Remarque design has no hamburger menu — the section nav is always
  // rendered. Assert the nav links stay reachable at phone width.
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');

  await expect(page.getByRole('link', { name: 'Dispatches' }).first()).toBeVisible();
});

test('blog post page renders content', async ({ page }) => {
  // Go to posts listing and click the first post
  await page.goto('/posts/');
  const firstPostLink = page.locator('.entry-title a').first();
  await firstPostLink.click();

  // Post page should have article content
  await expect(page.locator('article')).toBeVisible();
  await expect(page.locator('.prose')).toBeVisible();
});

test('RSS feed is valid XML', async ({ page }) => {
  const response = await page.goto('/feed.xml');
  expect(response?.status()).toBe(200);
  const contentType = response?.headers()['content-type'] ?? '';
  expect(contentType).toContain('xml');

  const body = (await response?.text()) ?? '';
  // Self-referencing atom:link must be an absolute URL with no doubled slash
  // in the path (regression: siteUrl once kept its trailing slash).
  const selfLink = body.match(/<atom:link href="([^"]+)" rel="self"/)?.[1];
  expect(selfLink).toBeDefined();
  expect(selfLink).toMatch(/^https:\/\/[^/]+\/feed\.xml$/);
  expect(body).toContain('<lastBuildDate>');
});

test('homepage title has no duplicated site name', async ({ page }) => {
  await page.goto('/');
  const title = await page.title();
  // Regression: index passes the site name as its page title; the layout
  // must not render "Name - Name".
  const half = title.slice(0, Math.floor(title.length / 2)).trim();
  expect(title).not.toBe(`${half} - ${half}`);
  expect(title).toBe('William Zujkowski');
});

test('skip link exists and points to main', async ({ page }) => {
  await page.goto('/');
  const skipLink = page.locator('a[href="#main"]');
  await expect(skipLink).toHaveCount(1);
});

test('series navigation shows on series posts', async ({ page }) => {
  // Navigate to a post in the Homelab Security series
  await page.goto('/posts/2025-12-10-homelab-security-dashboard-grafana-prometheus/');
  await expect(page.locator('nav[aria-label*="series"]')).toBeVisible();
  await expect(page.locator('text=Series:')).toBeVisible();
});
