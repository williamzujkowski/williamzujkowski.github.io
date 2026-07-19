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

  // And across a navigation
  await page.goto('/about/');
  await expect(page.locator('html')).toHaveAttribute('data-theme-deck', 'dracula');
});

test('deck theme is stamped before first paint (no FOUC)', async ({ page }) => {
  await page.goto('/');
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="nord"]').click();

  // On the next load, the attribute must be present at DOMContentLoaded —
  // i.e. set by the inline head script, not by post-load component JS.
  const attrAtDcl = await page.evaluate(() => {
    return new Promise<string | null>((resolve) => {
      const w = window.open('/', '_blank');
      if (!w) return resolve('window-blocked');
      w.addEventListener('DOMContentLoaded', () =>
        resolve(w.document.documentElement.getAttribute('data-theme-deck'))
      );
    });
  });
  expect(attrAtDcl).toBe('nord');
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
