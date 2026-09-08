import { defineConfig } from 'playwright/test';

// Deliberate, manual full-site validation after deployment. Uses the built
// route inventory so noindex and 404 pages are checked as well as the sitemap.
export default defineConfig({
  testDir: './tests/live',
  timeout: 60_000,
  retries: 0,
  workers: 2,
  fullyParallel: true,
  outputDir: process.env.SITE_ARTIFACTS || '/tmp/website-live-artifacts',
  use: {
    baseURL: process.env.SITE_URL || 'https://williamzujkowski.github.io',
    browserName: 'chromium',
    headless: true,
    navigationTimeout: 30_000,
    trace: 'retain-on-failure',
  },
  reporter: [['list'], ['json', { outputFile: process.env.SITE_REPORT || '/tmp/website-live-report.json' }]],
  projects: [
    { name: 'desktop-light', use: { viewport: { width: 1280, height: 900 }, colorScheme: 'light' } },
    { name: 'mobile-dark', use: { viewport: { width: 375, height: 812 }, colorScheme: 'dark', isMobile: true, hasTouch: true } },
  ],
});
