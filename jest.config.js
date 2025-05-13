/**
 * Jest configuration file
 */

export default {
  // Test environment
  testEnvironment: "jsdom",

  // Path to resolve modules from
  modulePaths: ["<rootDir>/src"],

  // File extensions to consider
  moduleFileExtensions: ["js", "mjs", "cjs", "jsx", "json"],

  // Transform files with Babel
  transform: {
    "^.+\\.(js|mjs|cjs|jsx)$": "babel-jest",
  },

  // Code coverage configuration
  collectCoverageFrom: [
    "src/js/**/*.js",
    "js/**/*.js",
    "!**/node_modules/**",
    "!**/tests/**",
    "!**/*.test.js",
    "!**/scripts/**",
  ],

  coverageThreshold: {
    global: {
      statements: 75,
      branches: 70,
      functions: 75,
      lines: 75,
    },
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

  // Test timeout
  testTimeout: 30000,

  // Verbose test output
  verbose: true,

  // Test match pattern
  testMatch: [
    "<rootDir>/tests/unit/**/*.test.js",
    "<rootDir>/tests/integration/**/*.test.js",
  ],

  // Setup files
  setupFilesAfterEnv: ["<rootDir>/tests/jest.setup.js"],

  // Jest reporters
  reporters: [
    "default",
    [
      "jest-junit",
      {
        outputDirectory: "./test-results",
        outputName: "jest-junit.xml",
      },
    ],
  ],

  // Display options
  testEnvironmentOptions: {
    url: "http://localhost",
  },
};
