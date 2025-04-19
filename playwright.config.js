/**
 * Playwright configuration for end-to-end testing
 * Part of Phase 4 testing implementation
 */

// @ts-check
const { devices } = require('@playwright/test');
const config = require('./tests/e2e/config');

/**
 * @see https://playwright.dev/docs/test-configuration
 * @type {import('@playwright/test').PlaywrightTestConfig}
 */
const playwrightConfig = {
  testDir: './tests/e2e',
  timeout: config.timeout,
  retries: process.env.CI ? 2 : 0, // Retry on CI, not locally
  
  // Only keep a single worker when debugging/watching
  workers: process.env.CI ? undefined : (process.env.WATCH ? 1 : undefined),
  
  reporter: [
    ['html', { outputFolder: config.reportDir + '/html' }],
    ['json', { outputFile: config.reportDir + '/results.json' }],
    ['list']
  ],
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Global setup and teardown
  globalSetup: require.resolve('./tests/e2e/global-setup'),
  globalTeardown: require.resolve('./tests/e2e/global-teardown'),
  
  // Folder for test artifacts such as screenshots, videos, traces, etc.
  outputDir: config.reportDir + '/artifacts',
  
  use: {
    // Base URL to use in actions like `await page.goto('/')`
    baseURL: config.baseUrl,
    
    // Track snapshots for visual comparisons
    screenshot: 'only-on-failure',
    
    // Record trace on failure
    trace: 'retain-on-failure',
    
    // Record video for failing tests
    video: 'on-first-retry',
  },
  
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
      },
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
      },
    },
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 5'],
      },
    },
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 12'],
      },
    },
  ],
};

module.exports = playwrightConfig;