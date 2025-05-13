/**
 * Playwright configuration for visual regression testing
 */

const { devices } = require("@playwright/test");
const { testConfig } = require("../config/test-config");

/**
 * @type {import('@playwright/test').PlaywrightTestConfig}
 */
const config = {
  testDir: "./tests/visual",
  timeout: testConfig.testTimeout,
  retries: process.env.CI ? 1 : 0, // Retry once on CI, not locally

  // Only keep a single worker for visual tests to avoid flakiness
  workers: 1,

  reporter: [
    ["html", { outputFolder: testConfig.reports.outputDir + "/visual-html" }],
    ["json", { outputFile: testConfig.reports.outputDir + "/visual-results.json" }],
    ["list"],
  ],

  forbidOnly: !!process.env.CI,

  // Folder for test artifacts such as screenshots, videos, traces, etc.
  outputDir: testConfig.reports.outputDir + "/visual-artifacts",

  use: {
    baseURL: "http://localhost:8080",
    screenshot: "on",
    trace: "retain-on-failure",
    video: "on-first-retry",
  },

  projects: [
    // Desktop viewports
    {
      name: "chromium-desktop",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1280, height: 800 },
      },
    },
    // Tablet viewports
    {
      name: "chromium-tablet",
      use: {
        ...devices["iPad Pro 11"],
      },
    },
    // Mobile viewports
    {
      name: "chromium-mobile",
      use: {
        ...devices["Pixel 5"],
      },
    },
  ],
};

module.exports = config;
