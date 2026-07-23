import { test, expect } from 'playwright/test';

// Forced-colors (Windows High Contrast Mode) regression for the broadsheet
// gradient-underline hover (issue #382). `.lead-title a` / `.entry-title a`
// paint their hover/focus affordance entirely with `background-image:
// linear-gradient(...)`, which forced-colors mode forces to `none` — without
// the `text-decoration: underline` fallback in global.css's
// `@media (forced-colors: active)` block, hovering/focusing one of these
// links would produce no visible change at all under WHCM.

test.describe('forced-colors: active', () => {
  test.beforeEach(async ({ page }) => {
    await page.emulateMedia({ forcedColors: 'active' });
  });

  test('lead title link shows a text-decoration underline on hover', async ({ page }) => {
    await page.goto('/');
    const link = page.locator('.lead-title a').first();
    await expect(link).toBeVisible();

    await link.hover();
    const decoration = await link.evaluate(
      (el) => getComputedStyle(el).textDecorationLine
    );
    expect(decoration).not.toBe('none');
    expect(decoration).toContain('underline');
  });

  test('entry title link shows a text-decoration underline on hover', async ({ page }) => {
    await page.goto('/');
    const link = page.locator('.entry-title a').first();
    await expect(link).toBeVisible();

    await link.hover();
    const decoration = await link.evaluate(
      (el) => getComputedStyle(el).textDecorationLine
    );
    expect(decoration).not.toBe('none');
    expect(decoration).toContain('underline');
  });

  test('entry title link shows a text-decoration underline on keyboard focus', async ({
    page,
  }) => {
    await page.goto('/');
    const link = page.locator('.entry-title a').first();
    await link.focus();
    const decoration = await link.evaluate(
      (el) => getComputedStyle(el).textDecorationLine
    );
    expect(decoration).not.toBe('none');
    expect(decoration).toContain('underline');
  });
});
