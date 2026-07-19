import { defineConfig } from 'playwright/test';

/**
 * Dedicated Playwright config for tests/e2e/visual-baselines.spec.ts.
 *
 * Runs its own preview server on port 4331 instead of the shared 4321 used
 * by playwright.config.ts, so authoring/regenerating screenshot baselines
 * never collides with a dev server (or another test run) already bound to
 * 4321. Not used in CI — the spec self-skips under CI (see its header).
 *
 * Usage:
 *   pnpm build
 *   npx playwright test --config=playwright.visual.config.ts --update-snapshots
 */
export default defineConfig({
  testDir: './tests/e2e',
  testMatch: /visual-baselines\.spec\.ts/,
  timeout: 60_000,
  use: {
    baseURL: 'http://localhost:4331',
    headless: true,
  },
  webServer: {
    command: 'npx astro preview --port 4331',
    port: 4331,
    reuseExistingServer: true,
    timeout: 60_000,
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});
