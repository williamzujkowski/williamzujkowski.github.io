/**
 * Centralized test configuration for the project
 * Supports consistent configuration across different test types
 */

export const testConfig = {
  // General configuration
  testTimeout: 30000, // 30 seconds
  slowTestThreshold: 5000, // 5 seconds

  // Test directories
  dirs: {
    unit: "./tests/unit",
    integration: "./tests/integration",
    e2e: "./tests/e2e",
    visual: "./tests/visual",
    performance: "./tests/performance",
    coverage: "./coverage",
  },

  // Coverage configuration
  coverage: {
    // Directories to include in coverage
    include: ["src/js/**/*.js", "js/**/*.js"],
    // Directories/files to exclude from coverage
    exclude: ["node_modules/**", "tests/**", "**/*.test.js", "scripts/**"],
    // Coverage thresholds
    thresholds: {
      global: {
        statements: 75,
        branches: 70,
        functions: 75,
        lines: 75,
      },
      // Critical path components with higher thresholds
      "./src/js/search.js": {
        statements: 90,
        branches: 85,
        functions: 90,
        lines: 90,
      },
      "./src/js/theme-utils.js": {
        statements: 85,
        branches: 80,
        functions: 85,
        lines: 85,
      },
    },
  },

  // Visual testing configuration
  visual: {
    snapshotDir: "./tests/visual/snapshots",
    diffThreshold: 0.1, // 0.1% difference allowed
    viewports: [
      { name: "mobile", width: 375, height: 667 },
      { name: "tablet", width: 768, height: 1024 },
      { name: "desktop", width: 1280, height: 800 },
    ],
  },

  // Browser configuration for E2E tests
  browsers: {
    chromium: true,
    firefox: true,
    webkit: true,
  },

  // Test reporting
  reports: {
    outputDir: "./test-results",
    formats: ["json", "html", "lcov"],
  },
};

export default testConfig;
