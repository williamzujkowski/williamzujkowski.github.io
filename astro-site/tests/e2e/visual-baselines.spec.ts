import { test, expect } from 'playwright/test';

/**
 * Visual regression baselines — typography phase 1 (issue #274, epic #269
 * "overhaul P2.5 — Phosphor broadsheet", ratified 7-0). Vote condition: no
 * wide visual sweep (body serif swap, measure change, mono-voice sweep,
 * etc.) may land without screenshot baselines existing FIRST.
 *
 * This is a LOCAL VISUAL-AUTHORING TOOL, not a CI gate — see the skip
 * guard below. CI's Chromium build renders system/fallback fonts (and
 * subpixel AA) differently than this authoring machine, so committed
 * PNGs would flap red on every CI run for reasons that have nothing to
 * do with a real regression. Run it locally, eyeball the diff, re-commit.
 *
 * Regenerate (after `pnpm build`; do this in a fresh terminal so the
 * preview server it starts doesn't collide with anything else running):
 *
 *   npx playwright test --config=playwright.visual.config.ts \
 *     visual-baselines --update-snapshots
 *
 * playwright.visual.config.ts runs its own preview server on port 4331
 * (not the shared 4321 in playwright.config.ts) and manages its
 * start/stop for you.
 *
 * Ordering note (matters if you're diffing history): the baseline PNGs
 * committed alongside this spec's FIRST commit were captured against the
 * PRE-swap site (Inter body face) — that's what the vote condition
 * requires ("baselines before any wide visual sweep"). A follow-up commit
 * in the same typography-phase-1 branch regenerated every baseline AFTER
 * the body-serif swap (Source Serif 4) and measure/text-wrap changes
 * landed, so the baseline set committed on `main` reflects the NEW
 * (post-swap) typography, not the old one. `git log --oneline -- \
 * tests/e2e/visual-baselines.spec.ts-snapshots/` shows the split.
 *
 * Baselines are NOT committed: font rendering is machine-specific (the same
 * reason this spec skips in CI). Before a visual sweep, generate YOUR
 * machine's baselines first:
 *   npx playwright test --config=playwright.visual.config.ts --update-snapshots
 */

test.skip(!!process.env.CI, 'local visual authoring tool — CI browsers render fonts differently');

const PAGES: Array<{ slug: string; path: string }> = [
  { slug: 'home', path: '/' },
  { slug: 'posts-index', path: '/posts/' },
  { slug: 'about', path: '/about/' },
  // Diagram-heavy post — exercises the hand-drawn mermaid rendering path.
  { slug: 'gvisor-post', path: '/posts/2024-09-25-gvisor-container-sandboxing-security/' },
  { slug: '404', path: '/404.html' },
];

const STATES: Array<{ slug: string; init: () => void }> = [
  {
    // Remarque default, dark.
    slug: 'remarque-dark',
    init: () => {
      localStorage.setItem('theme', 'dark');
    },
  },
  {
    // Remarque default, light.
    slug: 'remarque-light',
    init: () => {
      localStorage.setItem('theme', 'light');
    },
  },
  {
    // Deck theme, dark family.
    slug: 'deck-dracula',
    init: () => {
      localStorage.setItem('themeDeck', 'dracula|dark');
    },
  },
  {
    // Deck theme, light family.
    slug: 'deck-catppuccin-latte',
    init: () => {
      localStorage.setItem('themeDeck', 'catppuccin-latte|light');
    },
  },
];

for (const state of STATES) {
  test.describe(`theme: ${state.slug}`, () => {
    for (const p of PAGES) {
      test(`${p.slug} — ${state.slug}`, async ({ page }) => {
        // Stamp localStorage before the head script runs, so the theme
        // applies before first paint — same mechanism theme-deck.spec.ts
        // exercises for the interactive picker, applied here directly so
        // every page/state combination doesn't need a UI round-trip.
        await page.addInitScript(state.init);
        await page.goto(p.path, { waitUntil: 'networkidle' });
        // Avoid FOIT/FOUT flake: wait for all @font-face loads to settle
        // before the screenshot, so a baseline never captures a fallback
        // font mid-swap.
        await page.evaluate(() => document.fonts.ready);
        await page.waitForTimeout(300);
        // The diagram-heavy post embeds mermaid SVGs as `data:` URIs sized
        // via `height: auto` — the HTML width/height attributes are only
        // a CLS hint, so the box can shift a few px per diagram on first
        // decode. A generous timeout lets Playwright's own stability loop
        // (two consecutive identical screenshots) ride that out instead of
        // us hand-rolling image-decode waits.
        await expect(page).toHaveScreenshot(`${p.slug}--${state.slug}.png`, {
          fullPage: true,
          animations: 'disabled',
          timeout: 45_000,
        });
      });
    }
  });
}
