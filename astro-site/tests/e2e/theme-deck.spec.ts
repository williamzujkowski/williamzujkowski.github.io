import { test, expect } from 'playwright/test';

// Theme deck — reader-selectable terminal themes (overhaul P2, issue #271).

test('deck theme applies, persists across reload, and survives navigation', async ({ page }) => {
  await page.goto('/');
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="dracula"]').click();

  const html = page.locator('html');
  await expect(html).toHaveAttribute('data-theme-deck', 'dracula');
  await expect(html).toHaveClass(/dark/);

  // Persist across a full reload (restored by the before-paint head script)
  await page.reload();
  await expect(html).toHaveAttribute('data-theme-deck', 'dracula');

  // And across a REAL link click — a review finding showed page.goto() can't
  // detect navigation-mode regressions (it always forces a full load).
  await page.getByRole('link', { name: 'Colophon' }).first().click();
  await expect(page).toHaveURL(/about/);
  await expect(page.locator('html')).toHaveAttribute('data-theme-deck', 'dracula');
  const bg = await page.evaluate(() =>
    getComputedStyle(document.documentElement).getPropertyValue('--color-bg').trim()
  );
  expect(bg).toContain('0.2882'); // dracula bg lightness — theme actually painted
});

test('deck theme is stamped before first paint (no FOUC)', async ({ page, context }) => {
  await page.goto('/');
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="nord"]').click();

  // On a fresh page, the attribute must be present at DOMContentLoaded —
  // i.e. set by the inline head script, not by post-load component JS.
  // Playwright-native popup sync (review finding: a hand-rolled window.open
  // + DOMContentLoaded listener races and times out instead of failing).
  const [popup] = await Promise.all([
    context.waitForEvent('page'),
    page.evaluate(() => window.open('/')),
  ]);
  await popup.waitForLoadState('domcontentloaded');
  const attr = await popup.evaluate(() =>
    document.documentElement.getAttribute('data-theme-deck')
  );
  expect(attr).toBe('nord');
  await popup.close();
});

test('garbage localStorage slug degrades to default Remarque without errors', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(String(e)));

  await page.goto('/');
  await page.evaluate(() => localStorage.setItem('themeDeck', 'not-a-real-theme|dark'));
  await page.reload();

  // Attribute carries the garbage value but no CSS matches: Remarque default.
  const bg = await page.evaluate(() =>
    getComputedStyle(document.documentElement).getPropertyValue('--color-bg').trim()
  );
  expect(bg).toContain('0.95 0.015 75');
  expect(errors).toEqual([]);

  // Picker still functional afterward
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="dracula"]').click();
  await expect(page.locator('html')).toHaveAttribute('data-theme-deck', 'dracula');
});

test('base light/dark toggle clears an active deck theme', async ({ page }) => {
  await page.goto('/');
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="rose-pine"]').click();
  await expect(page.locator('html')).toHaveAttribute('data-theme-deck', 'rose-pine');

  await page.locator('#theme-toggle').click();
  await expect(page.locator('html')).not.toHaveAttribute('data-theme-deck');
  const stored = await page.evaluate(() => localStorage.getItem('themeDeck'));
  expect(stored).toBeNull();
  await expect(page.locator('#theme-deck-current')).toHaveText('Remarque');
});

test('picking a light theme pins light mode', async ({ page }) => {
  await page.goto('/');
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="catppuccin-latte"]').click();

  const html = page.locator('html');
  await expect(html).toHaveAttribute('data-theme-deck', 'catppuccin-latte');
  await expect(html).toHaveClass(/light/);

  // Background token actually changed from the Remarque default
  const bg = await page.evaluate(() =>
    getComputedStyle(document.documentElement).getPropertyValue('--color-bg').trim()
  );
  expect(bg).not.toBe('');
  expect(bg).not.toContain('0.95 0.015 75'); // Remarque light bg
});
