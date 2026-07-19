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
  expect(bg).toMatch(/0?\.2882/); // dracula bg lightness (leading zero varies by browser)
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
  expect(bg).toMatch(/0?\.95 0?\.015 75/);
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
  // Header variant has no text label — assert selection state instead.
  await expect(page.locator('.deck-option[data-deck-slug=""]')).toHaveAttribute(
    'aria-checked',
    'true'
  );
});

test.describe('crossfade (motion allowed)', () => {
  test.use({ contextOptions: { reducedMotion: 'no-preference' } });
  test('theme crossfade: absent at load and restore, present only on a deliberate switch', async ({
  page,
}) => {
  // Plain first visit — no stored preference at all. The crossfade class
  // must never be present at/after load (issue #274 item 3 vote condition:
  // class-gated, added after first paint, never during the anti-FOUC
  // restore).
  await page.goto('/');
  await expect(page.locator('html')).not.toHaveClass(/theme-transition/);

  // localStorage-restore path — a stored deck pref exists BEFORE the head
  // script runs. The class must still be absent at and after load; only
  // ThemeToggle.astro's toggle() / ThemeDeck.astro's applyDeck() may add it.
  await page.evaluate(() => localStorage.setItem('themeDeck', 'dracula|dark'));
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-theme-deck', 'dracula');
  await expect(page.locator('html')).not.toHaveClass(/theme-transition/);
  // Give any errant post-load script a moment it would need to (wrongly) add
  // the class, then re-assert it's still absent.
  await page.waitForTimeout(300);
  await expect(page.locator('html')).not.toHaveClass(/theme-transition/);

  // A deliberate switch (deck picker) DOES add the class, transiently, then
  // removes it again ~250ms later.
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="nord"]').click();
  await expect(page.locator('html')).toHaveClass(/theme-transition/);
  await expect(page.locator('html')).not.toHaveClass(/theme-transition/, { timeout: 1000 });

  // Same guarantee for the base light/dark toggle.
  await page.locator('#theme-toggle').click();
  await expect(page.locator('html')).toHaveClass(/theme-transition/);
  await expect(page.locator('html')).not.toHaveClass(/theme-transition/, { timeout: 1000 });
});
});

test('crossfade never fires under prefers-reduced-motion: reduce', async ({ browser }) => {
  const ctx = await browser.newContext({ reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto('/');
  await page.locator('.theme-deck summary').click();
  await page.locator('[data-deck-slug="dracula"]').click();
  await expect(page.locator('html')).toHaveAttribute('data-theme-deck', 'dracula');
  await expect(page.locator('html')).not.toHaveClass(/theme-transition/);
  await ctx.close();
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
  expect(bg).not.toMatch(/0?\.95 0?\.015 75/); // Remarque light bg
});
