# Testing Guide

This guide provides an overview of the comprehensive testing framework implemented in this website.

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Test Types](#test-types)
   - [Unit Tests](#unit-tests)
   - [Integration Tests](#integration-tests)
   - [End-to-End Tests](#end-to-end-tests)
   - [Visual Regression Tests](#visual-regression-tests)
   - [Performance Tests](#performance-tests)
3. [Test Configuration](#test-configuration)
4. [Running Tests](#running-tests)
5. [Writing Tests](#writing-tests)
6. [Continuous Integration](#continuous-integration)
7. [Code Coverage](#code-coverage)
8. [Best Practices](#best-practices)

## Testing Overview

The website uses a multi-layered testing approach to ensure quality and prevent regressions. Our testing framework includes:

- **Unit tests** for individual JavaScript functions and utilities
- **Integration tests** for component interactions and data flows
- **End-to-end tests** for complete user journeys
- **Visual regression tests** for UI consistency
- **Performance tests** for optimization metrics

These tests are configured to run both locally during development and in CI/CD pipelines.

## Test Types

### Unit Tests

Unit tests verify individual functions and components in isolation. They use Jest as the testing framework and testing-library for DOM interactions.

**Key files:**

- `tests/unit/*.test.js` - Unit test files
- `tests/jest.setup.js` - Jest setup configuration
- `jest.config.js` - Jest configuration

**Example unit test:**

```javascript
// tests/unit/theme-utils.test.js
import { generateOklchColor } from "../../src/js/theme-utils.js";

describe("generateOklchColor", () => {
  test("generates correctly formatted OKLCH color string", () => {
    const result = generateOklchColor(180, 0.2, 0.5);
    expect(result).toBe("oklch(0.5 0.2 180)");
  });

  test("clamps values to valid ranges", () => {
    expect(generateOklchColor(400, 0.1, 0.5)).toBe("oklch(0.5 0.1 360)");
    expect(generateOklchColor(180, 0.5, 0.5)).toBe("oklch(0.5 0.4 180)");
    expect(generateOklchColor(180, 0.2, 1.5)).toBe("oklch(1 0.2 180)");
  });
});
```

### Integration Tests

Integration tests verify the interaction between multiple components or modules. These tests ensure that different parts of the application work correctly together.

**Key files:**

- `tests/integration/*.test.js` - Integration test files

**Example integration test:**

```javascript
// tests/integration/blog-components.test.js
import { screen, render } from "@testing-library/dom";
import { initBlogSearch } from "../../src/js/blog-search.js";

describe("Blog search integration", () => {
  // Set up DOM environment
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="search-input" type="text" />
      <div class="searchable" data-title="Test Post" data-tags="javascript,testing">
        <h2>Test Post</h2>
      </div>
    `;
  });

  test("search input filters content correctly", () => {
    // Initialize the search functionality
    initBlogSearch();

    // Get the search input
    const searchInput = screen.getByRole("textbox");

    // Simulate user input
    searchInput.value = "javascript";
    searchInput.dispatchEvent(new Event("input"));

    // Check that content is filtered correctly
    const searchableItem = document.querySelector(".searchable");
    expect(searchableItem).toBeVisible();

    // Test non-matching search
    searchInput.value = "nonexistent";
    searchInput.dispatchEvent(new Event("input"));
    expect(searchableItem).not.toBeVisible();
  });
});
```

### End-to-End Tests

End-to-end tests verify the application from a user's perspective, simulating user interactions and ensuring all parts work together correctly.

**Key files:**

- `tests/e2e/*.test.js` - E2E test files
- `tests/e2e/helpers.js` - Helper functions for E2E tests
- `playwright.config.js` - Playwright configuration

**Example E2E test:**

```javascript
// tests/e2e/navigation.test.js
const { test, expect } = require("@playwright/test");
const { navigateTo, waitForPageReady } = require("./helpers");

test.describe("Site Navigation", () => {
  test("main navigation links work correctly", async ({ page }) => {
    // Go to home page
    await navigateTo(page, "/");
    await waitForPageReady(page);

    // Check that page title is correct
    await expect(page).toHaveTitle(/William Zujkowski/);

    // Click blog link
    await page.click('a[href="/blog/"]');
    await waitForPageReady(page);

    // Verify we navigated to the blog page
    await expect(page).toHaveURL(/blog/);
    await expect(page.locator("h1")).toContainText("Blog");

    // Click home link
    await page.click('a[href="/"]');
    await waitForPageReady(page);

    // Verify we returned to the home page
    await expect(page).toHaveURL(/\/$/);
  });
});
```

### Visual Regression Tests

Visual regression tests capture screenshots of UI elements and compare them to baseline images to detect visual changes.

**Key files:**

- `tests/visual/*.test.js` - Visual regression test files
- `tests/visual/playwright.config.js` - Visual test configuration
- `tests/visual/snapshots/` - Baseline screenshots

**Example visual regression test:**

```javascript
// tests/visual/improved-component-regression.test.js
const { test, expect } = require("@playwright/test");
const { navigateTo } = require("../e2e/helpers");

test.describe("Visual Regression - Core Components", () => {
  test("header appearance", async ({ page }) => {
    await navigateTo(page, "/");

    // Take screenshot of header and compare to baseline
    await expect(page.locator("header")).toHaveScreenshot("header-default.png");

    // Test mobile header
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator("header")).toHaveScreenshot("header-mobile.png");
  });
});
```

### Performance Tests

Performance tests verify that the website meets performance targets like bundle size limits and load time thresholds.

**Key files:**

- `tests/performance/*.test.js` - Performance test files

**Example performance test:**

```javascript
// tests/performance/bundle-size.test.js
const fs = require("fs");
const path = require("path");
const { test, assert } = require("../test-framework");

test("JavaScript bundle sizes are within limits", () => {
  const siteDir = path.join(__dirname, "../../_site");
  const jsDir = path.join(siteDir, "js");

  // Main bundle should be under 100KB
  const mainBundle = path.join(jsDir, "main.bundle.js");
  const mainSize = fs.statSync(mainBundle).size;

  assert.ok(mainSize < 102400, `Main bundle size ${mainSize} exceeds limit of 100KB`);

  return true;
});
```

## Test Configuration

The test configuration is centralized in the following files:

- **`tests/config/test-config.js`**: Central configuration for all test types
- **`jest.config.js`**: Jest configuration for unit and integration tests
- **`playwright.config.js`**: Playwright configuration for E2E tests
- **`tests/visual/playwright.config.js`**: Playwright configuration for visual tests

## Running Tests

The project includes various npm scripts for running tests:

```bash
# Run all tests
npm run test:enhanced:all

# Run unit tests only
npm run test:enhanced:unit

# Run integration tests
npm run test:enhanced:integration

# Run end-to-end tests
npm run test:enhanced:e2e

# Run visual regression tests
npm run test:visual

# Run with code coverage
npm run test:enhanced:coverage

# Run tests in watch mode (for development)
npm run test:watch
```

These commands are implemented in the enhanced test runner at `scripts/testing/run-tests-enhanced.js`.

## Writing Tests

When writing new tests, follow these guidelines:

### Unit Tests

1. Create files in `tests/unit/` with the naming pattern `*.test.js`
2. Use Jest's `describe` and `test` functions to organize tests
3. Test individual functions in isolation
4. Mock dependencies and external modules
5. Aim for high coverage of critical functions

### Integration Tests

1. Create files in `tests/integration/` with the naming pattern `*.test.js`
2. Test interactions between multiple components
3. Create realistic DOM environments for testing
4. Test data flow between components
5. Use proper assertions for expected behavior

### End-to-End Tests

1. Create files in `tests/e2e/` with the naming pattern `*.test.js`
2. Use Playwright's API for browser interactions
3. Test complete user journeys from start to finish
4. Include assertions for expected page state after actions
5. Use helper functions from `tests/e2e/helpers.js`

### Visual Regression Tests

1. Create files in `tests/visual/` with the naming pattern `*.test.js`
2. Capture screenshots of UI components
3. Compare against baseline images
4. Test different viewport sizes
5. Test different states (hover, active, etc.)

## Continuous Integration

Tests are configured to run in CI/CD pipelines. The `test:ci` script runs all tests in CI mode:

```bash
npm run test:ci
```

In CI mode:

- Tests are run with stricter settings
- Visual regression tests use a different configuration
- Failed tests cause the CI pipeline to fail

## Code Coverage

Code coverage is tracked using Jest's coverage reporter. The coverage configuration is in `jest.config.js` and `tests/config/test-config.js`.

To run tests with coverage:

```bash
npm run test:enhanced:coverage
```

Coverage reports are generated in the `coverage/` directory. The coverage thresholds are:

- **Global**: 75% statements, 70% branches, 75% functions, 75% lines
- **Critical paths**: Higher thresholds for critical modules

## Best Practices

Follow these best practices when working with tests:

1. **Write tests first**: Practice test-driven development when possible
2. **Keep tests focused**: Each test should verify one specific behavior
3. **Maintain independence**: Tests should not depend on each other
4. **Use descriptive names**: Test names should describe the behavior being tested
5. **Avoid testing implementation details**: Test behavior, not how it's implemented
6. **Update tests with code changes**: Keep tests in sync with implementation
7. **Run tests frequently**: Run relevant tests during development
8. **Fix failing tests promptly**: Don't let failures accumulate
9. **Don't skip tests**: Fix broken tests instead of skipping them
10. **Write testable code**: Design code with testing in mind
