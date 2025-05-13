/**
 * Enhanced visual regression tests for critical UI components
 */

const { test, expect } = require("@playwright/test");
const { readFileSync } = require("fs");
const path = require("path");
const testConfig = require("../config/test-config").testConfig;

// Load helper functions
/**
 * Navigate to a page and wait for it to be ready
 * @param {import('@playwright/test').Page} page
 * @param {string} url
 */
async function navigateTo(page, url) {
  await page.goto(url);
  await page.waitForLoadState("networkidle");
}

/**
 * Take a snapshot and compare with baseline
 * @param {import('@playwright/test').Page} page
 * @param {string} componentName
 * @param {string} stateName
 * @param {object} options
 */
async function compareSnapshot(page, componentName, stateName, options = {}) {
  const fullName = `${componentName}-${stateName}`;
  const snapshotOptions = {
    mask: options.mask || [],
    threshold: options.threshold || testConfig.visual.diffThreshold,
    animations: "disabled",
    ...options,
  };

  // Wait for any animations or loading states to complete
  await page.waitForTimeout(300);

  // Take screenshot and compare to baseline
  await expect(page).toHaveScreenshot(`${fullName}.png`, snapshotOptions);
}

// Test basic site components
test.describe("Visual Regression - Core Components", () => {
  test("Header appearance", async ({ page }) => {
    await navigateTo(page, "/");

    // Test default header
    await compareSnapshot(page.locator("header"), "header", "default");

    // Test mobile header
    await page.setViewportSize({ width: 375, height: 667 });
    await compareSnapshot(page.locator("header"), "header", "mobile");
  });

  test("Footer appearance", async ({ page }) => {
    await navigateTo(page, "/");
    await compareSnapshot(page.locator("footer"), "footer", "default");
  });

  test("Theme toggle button", async ({ page }) => {
    await navigateTo(page, "/");

    // Get the theme toggle button
    const themeToggle = page.locator(".theme-toggle");

    // Test light theme appearance
    await compareSnapshot(themeToggle, "theme-toggle", "light-theme");

    // Click the toggle and test dark theme appearance
    await themeToggle.click();
    await page.waitForTimeout(500); // Wait for animation
    await compareSnapshot(themeToggle, "theme-toggle", "dark-theme");
  });
});

// Test blog page components
test.describe("Visual Regression - Blog Components", () => {
  test("Blog post cards", async ({ page }) => {
    await navigateTo(page, "/blog/");

    // Test blog post cards
    const firstPostCard = page.locator(".searchable").first();
    await compareSnapshot(firstPostCard, "blog-card", "default");
  });

  test("Blog search functionality", async ({ page }) => {
    await navigateTo(page, "/blog/");

    // Get the search input
    const searchInput = page.locator("#search-input");

    // Test default search appearance
    await compareSnapshot(page.locator(".search-container"), "blog-search", "empty");

    // Test search with results
    await searchInput.fill("security");
    await page.waitForTimeout(500); // Wait for debounce
    await compareSnapshot(page.locator("main"), "blog-search", "with-results");

    // Test search with no results
    await searchInput.fill("nonexistentterm123456");
    await page.waitForTimeout(500); // Wait for debounce
    await compareSnapshot(page.locator("main"), "blog-search", "no-results");
  });

  test("Tag filters", async ({ page }) => {
    await navigateTo(page, "/blog/");

    // Test tag buttons
    await compareSnapshot(page.locator(".tag-container"), "blog-tags", "default");

    // Click a tag and test filtered results
    const securityTag = page.locator('.tag-btn[data-tag="security"]');
    if ((await securityTag.count()) > 0) {
      await securityTag.click();
      await page.waitForTimeout(500); // Wait for animation
      await compareSnapshot(page.locator("main"), "blog-tags", "filtered");
    }
  });
});

// Test responsiveness of critical pages
test.describe("Visual Regression - Responsive Layouts", () => {
  const viewports = [
    { width: 375, height: 667, name: "mobile" },
    { width: 768, height: 1024, name: "tablet" },
    { width: 1280, height: 800, name: "desktop" },
  ];

  for (const viewport of viewports) {
    test(`Home page at ${viewport.name} viewport`, async ({ page }) => {
      // Set viewport size
      await page.setViewportSize({ width: viewport.width, height: viewport.height });

      // Navigate to home page
      await navigateTo(page, "/");

      // Take screenshot of the main content area
      await compareSnapshot(page.locator("main"), "home-page", viewport.name);
    });

    test(`Blog page at ${viewport.name} viewport`, async ({ page }) => {
      // Set viewport size
      await page.setViewportSize({ width: viewport.width, height: viewport.height });

      // Navigate to blog page
      await navigateTo(page, "/blog/");

      // Take screenshot of the main content area
      await compareSnapshot(page.locator("main"), "blog-page", viewport.name);
    });
  }
});

// Test theme switching visual consistency
test.describe("Visual Regression - Theme Switching", () => {
  test("Home page in both themes", async ({ page }) => {
    await navigateTo(page, "/");

    // Test light theme
    await compareSnapshot(page, "home-theme", "light");

    // Get the theme toggle button and switch to dark theme
    const themeToggle = page.locator(".theme-toggle");
    await themeToggle.click();
    await page.waitForTimeout(500); // Wait for animation

    // Test dark theme
    await compareSnapshot(page, "home-theme", "dark");
  });
});
