import { defineConfig } from 'playwright/test';

/**
 * Dedicated Playwright config for tests/e2e/visual-baselines.spec.ts.
 *
 * Runs its own preview server on port 4331 instead of the shared 4321 used
 * by playwright.config.ts, so authoring/regenerating screenshot baselines
 * never collides with a dev server (or another test run) already bound to
 * 4321. Not used in CI — the spec self-skips under CI (see its header).
 *
 * Usage (`=all` matters: plain --update-snapshots skips diffs under tolerance):
 *   pnpm build
 *   npx playwright test --config=playwright.visual.config.ts --update-snapshots=all
 */
export default defineConfig({
  testDir: './tests/e2e',
  testMatch: /visual-baselines\.spec\.ts/,
  timeout: 60_000,
  use: {
    baseURL: 'http://127.0.0.1:4331',
    headless: true,
  },
  webServer: {
    // Not `astro preview`: Astro 7 daemonizes it in agent sessions, so
    // Playwright sees the process exit and aborts. preview-for-tests.mjs runs
    // the same preview in the foreground (same adapter playwright.config.ts uses).
    command: 'node scripts/preview-for-tests.mjs',
    env: { PLAYWRIGHT_PORT: '4331' },
    url: 'http://127.0.0.1:4331',
    // Never reuse: a leftover server could serve a stale dist/ into a baseline.
    reuseExistingServer: false,
    timeout: 60_000,
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});
