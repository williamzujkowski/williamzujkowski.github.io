import { test, expect } from 'playwright/test';
import type { Page, Response } from 'playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Key pages covering each layout archetype
const PAGES = [
  { path: '/', name: 'landing' },
  { path: '/about/', name: 'about' },
  { path: '/posts/', name: 'blog-index' },
  { path: '/uses/', name: 'uses-specimen' },
  { path: '/now/', name: 'now' },
  { path: '/projects/', name: 'projects' },
  { path: '/tags/', name: 'tags' },
  { path: '/posts/2026-02-09-building-nexus-agents-multi-model-orchestration/', name: 'blog-post' },
  // Sidenotes pilot post (issue #272) — exercises the margin-note DOM/CSS
  // path (see tests/e2e/sidenotes.spec.ts for layout-specific assertions;
  // this just adds it to the general sweep at the default viewport).
  {
    path: '/posts/2025-10-29-post-quantum-cryptography-homelab/',
    name: 'blog-post-sidenotes',
  },
  // Both were omitted, so nothing had ever scanned them (issue #508).
  // /pizza-ops/ is the most interactive page on the site — a Svelte island
  // with a radiogroup, a range input and a live region — which makes it the
  // one most likely to have a11y defects and the one that was unscanned.
  { path: '/pizza-ops/', name: 'pizza-ops' },
  { path: '/404.html', name: 'not-found' },
];

/**
 * Run axe against the page with Remarque conventions:
 *  - WCAG 2 / 2.1 / 2.2 Level AA
 *  - Syntax-highlighted code inside <pre class="astro-code"> is excluded from
 *    color-contrast. Shiki's github-light theme uses token colors like
 *    #E36209 (parameter names) that are ~3.5:1 on white. This is true of
 *    every popular syntax theme — WCAG prose-contrast doesn't match the
 *    pattern-recognition task syntax highlighting serves. The surrounding
 *    prose still has to pass.
 */
/**
 * Liveness precondition — run BEFORE axe on every scan.
 *
 * `expect(results.violations).toEqual([])` is vacuously true for a page that
 * does not exist: axe on the preview server's bare 404 body finds nothing to
 * violate, so the whole suite passed green against an empty `dist/`
 * (18 passed, exit 0). A scan that cannot fail is not a test. This asserts
 * the page actually rendered — HTTP 200 and a visible `<main>` landmark,
 * which every page in PAGES has exactly one of — so a broken or missing
 * build fails here instead of being reported as "no accessibility
 * violations".
 */
async function assertPageIsLive(page: Page, response: Response | null, path: string) {
  expect(response, `no navigation response for ${path}`).not.toBeNull();
  expect(response!.status(), `${path} must return HTTP 200 before axe runs`).toBe(200);
  await expect(page.locator('main'), `${path} must render a <main> landmark`).toBeVisible();
}

async function runAxe(page: Page) {
  const builder = new AxeBuilder({ page })
    // 'best-practice' added (issue #508): without it, landmark-unique and
    // region never run, so two unnamed <nav> landmarks sitting beside the
    // named primary nav went unreported.
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice'])
    .disableRules([])
    // Exclude Shiki-rendered syntax tokens from color-contrast only.
    .options({
      rules: {
        'color-contrast': {
          enabled: true,
        },
      },
    })
    .exclude('pre.astro-code span');
  return builder.analyze();
}

for (const { path, name } of PAGES) {

  test(`a11y: ${name} (${path}) — light`, async ({ page }) => {
    const response = await page.goto(path);
    await assertPageIsLive(page, response, path);
    const results = await runAxe(page);
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });

  test(`a11y: ${name} (${path}) — dark`, async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    const response = await page.goto(path);
    await assertPageIsLive(page, response, path);
    const results = await runAxe(page);
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });
}

// The flow captions sit on surface, where Latte's muted text fell below 4.5:1.
for (const [deck, mode, width] of [
  ['catppuccin-latte', 'light', 1440],
  ['dracula', 'dark', 390],
] as const) {
  test(`DoH flow and checklist — ${deck}`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.addInitScript(({ deck, mode }) => {
      localStorage.setItem('themeDeck', `${deck}|${mode}`);
    }, { deck, mode });
    const path = '/posts/2025-07-08-implementing-dns-over-https-home-networks/';
    const response = await page.goto(path);
    await assertPageIsLive(page, response, path);
    await expect(page.locator('html')).toHaveAttribute('data-theme-deck', deck);
    await expect(page.getByRole('group', {
      name: 'Pi-hole upstream DNS path; HTTPS begins at the local proxy',
    })).toBeVisible();
    const results = await runAxe(page);
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  });
}
