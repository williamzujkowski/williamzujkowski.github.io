# Testing Framework

This document outlines the comprehensive testing framework for verifying website functionality, implemented as part of Phase 4.

## Overview

The testing framework validates that all aspects of the website function correctly after code changes or refactoring. It includes tests for template structure, build process, component functionality, security, performance, and accessibility.

## Testing Philosophy

The testing strategy follows these core principles:

1. **Coverage**: Test critical user flows and components
2. **Maintainability**: Tests should be easy to maintain and update
3. **Speed**: Tests should run quickly to support rapid development
4. **Reliability**: Tests should be deterministic and reliable
5. **Automation**: Tests should be automated as part of the CI/CD pipeline

## Test Commands

The following npm scripts are available for testing:

- `npm test` - Run all tests
- `npm run test:templates` - Test template structure
- `npm run test:build` - Test build process
- `npm run test:components` - Test JavaScript components
- `npm run test:security` - Run security tests
- `npm run test:performance` - Run performance tests
- `npm run test:accessibility` - Run accessibility tests
- `npm run test:e2e` - Run end-to-end tests

## Test Categories

### 1. Template Structure Tests

These tests verify that the template organization is correct:

- Directory structure follows conventions (layouts, partials, macros)
- Required template files exist
- No inline JavaScript remains in templates
- Template include paths use proper directory prefixes
- main.js includes all necessary component imports

### 2. Build Process Tests

These tests verify that the build process works correctly:

- CSS builds successfully
- JavaScript bundling works correctly
- Output structure is correct
- HTML files reference CSS and JS properly
- Template rendering produces expected output

### 3. Component Tests

These tests verify that JavaScript components function correctly:

- Unit tests for utility functions
- Integration tests for component interactions
- Security tests for user input handling
- Event handling tests for interactive elements

### 4. End-to-End Tests

These tests simulate real user interactions with the website:

- Navigation flow tests
- Search functionality tests
- Blog post viewing and filtering tests
- Theme switching tests

### 5. Security Tests

These tests verify that security measures function correctly:

- Input validation and sanitization tests
- XSS protection tests
- Content Security Policy tests
- Secure DOM manipulation tests

### 6. Performance Tests

These tests measure the performance of the website:

- JavaScript bundle size analysis
- Load time measurements
- Core Web Vitals metrics
- Animation and rendering performance

### 7. Accessibility Tests

These tests verify accessibility compliance:

- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader compatibility
- Color contrast and font size

## Test Implementation

### Component Test Example

```javascript
// tests/components/search.test.js
const { JSDOM } = require("jsdom");
const { test, assert } = require("../test-framework");

test("Search sanitizes user input", function () {
  // Setup test DOM
  const dom = new JSDOM(`
    <input id="search-input" type="text" />
    <div id="search-results"></div>
  `);

  // Mock global objects
  global.document = dom.window.document;
  global.window = dom.window;

  // Import the component
  const { sanitizeSearchQuery } = require("../../src/js/search");

  // Test cases
  const testCases = [
    { input: "<script>alert(1)</script>", expected: "scriptalert1script" },
    { input: "javascript:alert(1)", expected: "javascriptalert1" },
    { input: "normal text", expected: "normal text" },
    { input: "text with <b>tags</b>", expected: "text with tags" },
  ];

  // Run tests
  testCases.forEach(({ input, expected }) => {
    const result = sanitizeSearchQuery(input);
    assert.equal(result, expected, `Failed to sanitize: ${input}`);
  });

  // Clean up
  delete global.document;
  delete global.window;

  return true;
});
```

### Performance Test Example

```javascript
// tests/performance/bundle-size.test.js
const fs = require("fs");
const path = require("path");
const { test, assert } = require("../test-framework");

test("JavaScript bundle size is below threshold", function () {
  const BUNDLE_SIZE_THRESHOLD = 100 * 1024; // 100 KB

  const bundlePath = path.join(__dirname, "../../_site/js/main.bundle.js");

  // Check if bundle exists
  if (!fs.existsSync(bundlePath)) {
    return "Bundle file not found";
  }

  // Get file size
  const stats = fs.statSync(bundlePath);
  const bundleSize = stats.size;

  // Check against threshold
  if (bundleSize > BUNDLE_SIZE_THRESHOLD) {
    return `Bundle size (${bundleSize} bytes) exceeds threshold (${BUNDLE_SIZE_THRESHOLD} bytes)`;
  }

  return true;
});
```

## Adding New Tests

To add new tests:

1. Determine which test category your test belongs to
2. Add your test file to the appropriate directory:
   - Template tests: `tests/templates/`
   - Build tests: `tests/build/`
   - Component tests: `tests/components/`
   - E2E tests: `tests/e2e/`
   - Security tests: `tests/security/`
   - Performance tests: `tests/performance/`
   - Accessibility tests: `tests/accessibility/`
3. Use the `test()` function to run your test:

```javascript
test("My new test", function () {
  // Test logic here
  // Return true if test passes
  // Return a string error message if test fails
});
```

## Testing Tools

The testing framework uses the following tools:

- **Test Runner**: Custom test runner in `scripts/testing/run-tests.js`
- **DOM Testing**: JSDOM for browser environment simulation
- **Assertion Library**: Custom assertions in `tests/test-framework.js`
- **E2E Testing**: Playwright for browser automation
- **Performance Testing**: Lighthouse for performance metrics
- **Accessibility Testing**: axe-core for accessibility compliance
- **Security Testing**: Custom security tests with JSDOM

## Continuous Integration

It's recommended to run tests before committing changes:

```bash
# Run all tests
npm test

# Fix any issues
npm run lint:fix
npm run format

# Run tests again to verify fixes
npm test
```

## Test Output

Tests produce colorized output with clear pass/fail status:

- Green: Test passed
- Yellow: Warning (test passed with concerns)
- Red: Test failed

A summary is displayed at the end showing total tests, passed, failed, and warnings.

## Code Coverage

Code coverage is tracked using a custom coverage tool:

```bash
# Run tests with coverage
npm run test:coverage
```

Coverage reports are generated in the `/coverage` directory and include:

- Statement coverage
- Branch coverage
- Function coverage
- Line coverage

## Best Practices

1. **Arrange-Act-Assert**: Structure tests with clear setup, action, and verification phases
2. **Test Isolation**: Tests should not depend on each other
3. **Meaningful Assertions**: Make assertions specific and meaningful
4. **Mocking External Dependencies**: Use mocks for external APIs and services
5. **Test Performance**: Keep tests fast to support rapid development

## Future Enhancements

Future enhancements to the testing framework include:

- Browser-based visual testing with screenshot comparison
- Expanded accessibility testing with voice recognition
- Advanced performance profiling with Web Vitals metrics
- Integration with GitHub Actions CI/CD pipeline
- Mobile device simulation for responsive design testing
