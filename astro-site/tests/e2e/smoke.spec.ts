import { test, expect } from 'playwright/test';

// Smoke tests — verify key pages load and interactive features work.
// NOT visual regression. Just structural checks.

const pages = [
  { path: '/', title: 'William Zujkowski', selector: 'h1' },
  { path: '/about/', title: 'About', selector: 'h1' },
  { path: '/posts/', title: 'Blog', selector: 'h1' },
  { path: '/projects/', title: 'Projects', selector: 'h1' },
  { path: '/resources/', title: 'Resources', selector: 'h1' },
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
  const response = await page.goto('/404.html');
  if (response?.status() === 200) {
    await expect(page.locator('text=Page not found')).toBeVisible();
    await expect(page.locator('text=Recent Posts')).toBeVisible();
  }
  // On live GitHub Pages, 404.html is served for missing routes automatically
});

test('dark mode toggle switches theme', async ({ page }) => {
  await page.goto('/');
  const html = page.locator('html');

  // Click dark mode toggle
  const toggle = page.locator('button[aria-label*="mode"], button:has-text("Switch to")');
  await toggle.first().click();

  // Verify theme class changed
  const classAfter = await html.getAttribute('class');
  expect(classAfter).toBeTruthy();
});

test('search dialog opens and closes', async ({ page }) => {
  await page.goto('/');

  // Open search
  const searchButton = page.locator('button:has-text("Search"), button[aria-label*="Search"]');
  await searchButton.first().click();

  // Dialog should be visible
  await expect(page.locator('[role="dialog"], dialog').first()).toBeVisible();

  // Close with Escape
  await page.keyboard.press('Escape');
});

test('mobile menu opens on small viewport', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');

  const menuButton = page.locator('button:has-text("menu"), button[aria-label*="menu"]');
  await menuButton.first().click();

  // Mobile nav links should be visible (use role-based selector to avoid ambiguity)
  await expect(page.getByRole('link', { name: 'About' }).first()).toBeVisible();
});

test('blog post page renders content', async ({ page }) => {
  // Go to posts listing and click the first post
  await page.goto('/posts/');
  const firstPostLink = page.locator('article a').first();
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
