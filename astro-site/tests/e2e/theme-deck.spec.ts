import { test, expect, type Page } from 'playwright/test';

// Theme deck: reader-selectable terminal palettes (overhaul P2, issue #271),
// rebuilt on remarque-tokens 0.31's Palette Deck. Every palette is a
// light/dark PAIR set by data-palette; the light/dark toggle is independent
// and a palette follows it.

// The resolved page background, through a transition-free probe: the
// crossfade animates body's own background-color, and deck tokens are
// light-dark() expressions that only the cascade resolves.
const resolvedBg = (page: Page) =>
  page.evaluate(() => {
    const p = document.createElement('div');
    p.style.cssText = 'transition:none;background-color:var(--color-bg)';
    document.body.appendChild(p);
    const c = getComputedStyle(p).backgroundColor;
    p.remove();
    return c;
  });
const bgToken = (page: Page) =>
  page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--color-bg').trim());
// The site's own light background, decimal (0.95) or percentage (95%) form.
const SITE_LIGHT_BG = /(?:0?\.95|95%) 0?\.015 75/;

async function pick(page: Page, name: string) {
  const deck = page.locator('.theme-deck');
  if (!(await deck.evaluate((d) => (d as HTMLDetailsElement).open))) await deck.locator('summary').click();
  await page.locator(`.deck-option:has(input[value="${name}"])`).click();
}

test('a palette applies, persists across reload, and survives navigation', async ({ page }) => {
  await page.goto('/');
  await pick(page, 'nord');
  const html = page.locator('html');
  await expect(html).toHaveAttribute('data-palette', 'nord');
  await expect(page.locator('.deck-option input[value="nord"]')).toBeChecked();

  await page.reload();
  await expect(html).toHaveAttribute('data-palette', 'nord');

  // A REAL link click too: page.goto() always forces a full load.
  await page.getByRole('link', { name: 'About', exact: true }).first().click();
  await expect(page).toHaveURL(/about/);
  await expect(page.locator('html')).toHaveAttribute('data-palette', 'nord');
  expect(await bgToken(page)).not.toMatch(SITE_LIGHT_BG);
});

test('the palette is stamped before first paint (no FOUC)', async ({ page, context }) => {
  await page.goto('/');
  await pick(page, 'rose-pine');
  const [popup] = await Promise.all([context.waitForEvent('page'), page.evaluate(() => window.open('/'))]);
  await popup.waitForLoadState('domcontentloaded');
  expect(await popup.evaluate(() => document.documentElement.getAttribute('data-palette'))).toBe('rose-pine');
  await popup.close();
});

test('a palette is paired: it follows the light/dark toggle instead of forcing a mode', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'light' });
  await page.goto('/');
  await pick(page, 'catppuccin');
  const light = await bgToken(page);
  expect(light).not.toMatch(SITE_LIGHT_BG); // the palette wins in LIGHT mode too

  await page.keyboard.press('Escape');
  await page.locator('#theme-toggle').click();
  await expect(page.locator('html')).toHaveClass(/\bdark\b/);
  await expect(page.locator('html')).toHaveAttribute('data-palette', 'catppuccin'); // toggling keeps it
  const dark = await resolvedBg(page);
  await page.evaluate(() => document.documentElement.removeAttribute('data-palette'));
  const siteDark = await resolvedBg(page);
  expect(dark).not.toBe(siteDark); // and its dark side differs from the site's dark
  await page.evaluate(() => document.documentElement.setAttribute('data-palette', 'catppuccin'));
  await page.locator('#theme-toggle').click();
  expect(await resolvedBg(page)).not.toBe(dark); // back to its light side
});

test('choosing the default clears the palette and storage', async ({ page }) => {
  await page.goto('/');
  await pick(page, 'gruvbox');
  await pick(page, '');
  await expect(page.locator('html')).not.toHaveAttribute('data-palette');
  expect(await page.evaluate(() => localStorage.getItem('remarque-palette'))).toBeNull();
  expect(await bgToken(page)).toMatch(SITE_LIGHT_BG);
});

test('readers of the old 12-theme deck are migrated once', async ({ page }) => {
  await page.addInitScript(() => {
    if (!sessionStorage.getItem('seeded')) {
      localStorage.setItem('themeDeck', 'catppuccin-mocha|dark');
      sessionStorage.setItem('seeded', '1');
    }
  });
  await page.goto('/');
  const html = page.locator('html');
  await expect(html).toHaveAttribute('data-palette', 'catppuccin');
  await expect(html).toHaveClass(/\bdark\b/); // the mode the old theme forced is kept
  expect(await page.evaluate(() => [localStorage.getItem('themeDeck'), localStorage.getItem('remarque-palette'), localStorage.theme]))
    .toEqual([null, 'catppuccin', 'dark']);
});

test('Dracula (no light theme in the dataset) migrates to the default, keeping dark mode', async ({ page }) => {
  await page.addInitScript(() => {
    if (!sessionStorage.getItem('seeded')) {
      localStorage.setItem('themeDeck', 'dracula|dark');
      sessionStorage.setItem('seeded', '1');
    }
  });
  await page.goto('/');
  await expect(page.locator('html')).not.toHaveAttribute('data-palette');
  await expect(page.locator('html')).toHaveClass(/\bdark\b/);
});

test('a garbage stored palette degrades to the default without errors', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto('/');
  await page.evaluate(() => localStorage.setItem('remarque-palette', 'not-a-real-theme'));
  await page.reload();
  expect(await bgToken(page)).toMatch(SITE_LIGHT_BG);
  expect(errors).toEqual([]);
  await pick(page, 'nord');
  await expect(page.locator('html')).toHaveAttribute('data-palette', 'nord');
});

test.describe('crossfade (motion allowed)', () => {
  test.use({ contextOptions: { reducedMotion: 'no-preference' } });
  test('absent at load and restore, present only on a deliberate switch', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('html')).not.toHaveClass(/theme-transition/);
    await page.evaluate(() => localStorage.setItem('remarque-palette', 'nord'));
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-palette', 'nord');
    await page.waitForTimeout(300);
    await expect(page.locator('html')).not.toHaveClass(/theme-transition/);

    await pick(page, 'tokyonight');
    await expect(page.locator('html')).toHaveClass(/theme-transition/);
    await expect(page.locator('html')).not.toHaveClass(/theme-transition/, { timeout: 1000 });

    await page.keyboard.press('Escape');
    await page.locator('#theme-toggle').click();
    await expect(page.locator('html')).toHaveClass(/theme-transition/);
    await expect(page.locator('html')).not.toHaveClass(/theme-transition/, { timeout: 1000 });
  });
});

test('crossfade never fires under prefers-reduced-motion: reduce', async ({ browser }) => {
  const ctx = await browser.newContext({ reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto('/');
  await pick(page, 'nord');
  await expect(page.locator('html')).toHaveAttribute('data-palette', 'nord');
  await expect(page.locator('html')).not.toHaveClass(/theme-transition/);
  await ctx.close();
});

test('the picker is native radios: keyboard selection works with no pointer', async ({ page }) => {
  await page.goto('/');
  await page.locator('.theme-deck summary').click();
  await page.locator('.deck-option input[value=""]').focus();
  await page.keyboard.press('ArrowDown');
  await expect(page.locator('html')).toHaveAttribute('data-palette', /.+/);
  expect(await page.locator('.deck-option [role="radio"]').count()).toBe(0);
});

test('light/dark and palette choices work when storage is unavailable', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'light' });
  await page.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', {
      get() { throw new DOMException('Storage is unavailable', 'SecurityError'); },
    });
  });
  await page.goto('/');
  const root = page.locator('html');
  const toggle = page.locator('#theme-toggle');
  await toggle.click();
  await expect(root).toHaveClass(/\bdark\b/);
  await pick(page, 'nord');
  await expect(root).toHaveAttribute('data-palette', 'nord');
  await page.keyboard.press('Escape');
  await toggle.click();
  await expect(root).toHaveClass(/\blight\b/);
  await expect(root).toHaveAttribute('data-palette', 'nord');
  await toggle.click({ modifiers: ['Shift'] });
  await expect(root).not.toHaveClass(/\b(?:dark|light)\b/);
});

test('system theme changes update the toggle action without overriding explicit choices', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'light' });
  await page.goto('/');
  const toggle = page.locator('#theme-toggle');
  await expect(toggle).toHaveAttribute('aria-label', 'Switch to dark theme');
  await page.emulateMedia({ colorScheme: 'dark' });
  await expect(toggle).toHaveAttribute('aria-label', 'Switch to light theme');
  await toggle.click();
  await expect(page.locator('html')).toHaveClass(/\blight\b/);
  await page.emulateMedia({ colorScheme: 'light' });
  await page.emulateMedia({ colorScheme: 'dark' });
  await expect(page.locator('html')).toHaveClass(/\blight\b/);
  await expect(toggle).toHaveAttribute('aria-label', 'Switch to dark theme');
});

test('theme-color meta tracks the painted background through toggles and palettes', async ({ browser }) => {
  const ctx = await browser.newContext({ colorScheme: 'light', reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  const state = () =>
    page.evaluate(() => {
      const hex = (color: string) => {
        const g = document.createElement('canvas').getContext('2d')!;
        g.fillStyle = color;
        g.fillRect(0, 0, 1, 1);
        const d = g.getImageData(0, 0, 1, 1).data;
        return [d[0], d[1], d[2]].map((v) => v.toString(16).padStart(2, '0')).join('');
      };
      const active = [...document.querySelectorAll<HTMLMetaElement>('meta[name="theme-color"]')]
        .filter((m) => !m.media || matchMedia(m.media).matches)
        .map((m) => hex(m.content));
      const bg = hex(getComputedStyle(document.body).backgroundColor);
      return active.length === 1 && active[0] === bg ? 'match' : `meta ${active.join(',')} vs body ${bg}`;
    });
  const expectMatch = (when: string) => expect.poll(state, { message: when }).toBe('match');

  await page.goto('/');
  await expectMatch('default');
  await page.locator('#theme-toggle').click();
  await expectMatch('after toggling to dark');
  for (const name of ['nord', 'gruvbox', 'solarized']) {
    await pick(page, name);
    await expect(page.locator('html')).toHaveAttribute('data-palette', name);
    await expectMatch(`palette ${name}`);
    await page.keyboard.press('Escape');
  }
  await page.reload();
  await expectMatch('palette restored on reload');
  await ctx.close();
});

for (const viewport of [{ width: 360, height: 800 }, { width: 1280, height: 900 }]) {
  test(`deck panel shows its last option without an inner scroll at ${viewport.width}px`, async ({ browser }) => {
    const ctx = await browser.newContext({ viewport });
    const page = await ctx.newPage();
    await page.goto('/');
    await page.locator('.theme-deck summary').click();
    const last = page.locator('.deck-option').last();
    await last.scrollIntoViewIfNeeded();
    await expect(last).toBeInViewport({ ratio: 1 });
    const clipped = await page.locator('.deck-panel').evaluate((p) => p.scrollHeight > p.clientHeight + 1);
    expect(clipped).toBe(false);
    await ctx.close();
  });
}
