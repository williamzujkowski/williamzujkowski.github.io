# Testing Framework

This document outlines the testing framework for verifying website functionality.

## Overview

The testing framework validates that all aspects of the website function correctly after code changes or refactoring. It includes tests for template structure, build process, and rendering integrity.

## Test Commands

The following npm scripts are available for testing:

- `npm test` - Run all integration tests
- `npm run test:templates` - Test only template structure
- `npm run test:build` - Test only build process

## Test Categories

### Template Structure Tests

These tests verify that the template organization is correct:

- Directory structure follows conventions (layouts, partials, macros)
- Required template files exist
- No inline JavaScript remains in templates
- Template include paths use proper directory prefixes
- main.js includes all necessary component imports

### Build Process Tests

These tests verify that the build process works correctly:

- CSS builds successfully
- Output structure is correct
- HTML files reference CSS and JS properly
- Template rendering produces expected output

## Adding New Tests

To add new tests:

1. Determine which test category your test belongs to
2. Add your test function to the appropriate file:
   - Template tests: `scripts/testing/verify-templates.js`
   - Build tests: `scripts/testing/verify-build.js`
3. Use the `test()` function to run your test:

```javascript
test("My new test", function () {
  // Test logic here
  // Return true if test passes
  // Return a string error message if test fails
});
```

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

## Future Enhancements

Future enhancements to the testing framework may include:

- Browser-based visual testing
- Automated accessibility testing
- Performance testing
- Snapshot testing for templates
