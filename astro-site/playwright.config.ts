import { defineConfig } from 'playwright/test';

const port = Number(process.env.PLAYWRIGHT_PORT ?? 4321);

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  retries: 1,
  // Playwright defaults to a single worker when CI is set, so the whole e2e
  // suite ran serially inside a 20-minute job and kept hitting the ceiling —
  // 2 of the last 5 runs were cancelled on timeout. These are read-only page
  // visits against a static preview server, so they parallelise safely.
  // ubuntu-latest gives 2 vCPUs; asking for more than that just thrashes.
  fullyParallel: true,
  workers: process.env.CI ? 2 : undefined,
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    headless: true,
  },
  webServer: {
    command: 'node scripts/preview-for-tests.mjs',
    url: `http://127.0.0.1:${port}`,
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});
