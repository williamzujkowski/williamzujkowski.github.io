/**
 * Visual regression testing configuration
 * Part of Phase 4 testing implementation
 */

const path = require("path");

// Configuration for visual regression tests
const config = {
  // Base URL for testing
  baseUrl: process.env.TEST_URL || "http://localhost:8080",

  // Screenshots directory
  baselineDir: path.join(__dirname, "baseline"),
  actualDir: path.join(__dirname, "actual"),
  diffDir: path.join(__dirname, "diff"),

  // Comparison options
  threshold: 0.1, // Allowed difference threshold (0.1 = 10%)

  // Which components to test
  components: [
    // Header component
    {
      name: "header",
      path: "/",
      selector: "header",
      viewports: ["mobile", "desktop"],
    },
    // Footer component
    {
      name: "footer",
      path: "/",
      selector: "footer",
      viewports: ["mobile", "desktop"],
    },
    // Post card component
    {
      name: "post-card",
      path: "/blog/",
      selector: ".gh-post-card:first-child",
      viewports: ["mobile", "desktop"],
    },
    // Search component
    {
      name: "search",
      path: "/blog/",
      selector: ".gh-search-container",
      viewports: ["mobile", "desktop"],
    },
    // Tags component
    {
      name: "tags",
      path: "/blog/",
      selector: ".tags-filter",
      viewports: ["mobile", "desktop"],
    },
  ],

  // Viewport sizes
  viewports: {
    mobile: { width: 375, height: 667 },
    tablet: { width: 768, height: 1024 },
    desktop: { width: 1280, height: 800 },
  },

  // Test timeout
  timeout: 30000,
};

module.exports = config;
