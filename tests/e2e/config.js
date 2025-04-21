/**
 * End-to-end testing configuration
 * Part of Phase 4 testing implementation
 */

const BASE_URL = process.env.TEST_URL || "http://localhost:8080";
const TIMEOUT = 30000; // 30 seconds
const SCREENSHOT_DIR = "./tests/e2e/screenshots";
const REPORT_DIR = "./tests/e2e/reports";

/**
 * Test configuration settings
 */
const config = {
  baseUrl: BASE_URL,
  timeout: TIMEOUT,
  viewports: {
    mobile: { width: 375, height: 667 },
    tablet: { width: 768, height: 1024 },
    desktop: { width: 1280, height: 800 },
  },
  screenshotDir: SCREENSHOT_DIR,
  reportDir: REPORT_DIR,
};

module.exports = config;
