const { chromium } = require('@playwright/test');
const fs = require('fs').promises;
const path = require('path');

const BASE_URL = 'http://localhost:8080';
const TIMEOUT_MS = 10000;
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'screenshots', 'search');
const REPORT_FILE = path.join(__dirname, '..', 'docs', 'reports', 'search-functionality-report.json');

/**
 * Search component selectors
 */
const SEARCH_SELECTORS = {
  input: [
    'input[type="search"]',
    'input[name="search"]',
    'input[placeholder*="search" i]',
    '#search',
    '.search-input',
    '[role="searchbox"]'
  ],
  results: [
    '.search-results',
    '#search-results',
    '[role="region"][aria-label*="search" i]',
    '.search-container',
    '[data-search-results]'
  ],
  resultItems: [
    '.search-result',
    '.result-item',
    '[data-search-result]',
    '.search-results > *'
  ],
  clearButton: [
    '.search-clear',
    'button[aria-label*="clear" i]',
    '[data-search-clear]'
  ],
  noResults: [
    '.no-results',
    '.search-empty',
    '[data-no-results]'
  ]
};

/**
 * Test queries with expected behavior
 */
const TEST_QUERIES = [
  {
    query: 'security',
    shouldFindResults: true,
    minResults: 5,
    description: 'Common topic search'
  },
  {
    query: 'AI',
    shouldFindResults: true,
    minResults: 3,
    description: 'Uppercase search'
  },
  {
    query: 'xyzabc123nonexistent',
    shouldFindResults: false,
    minResults: 0,
    description: 'Non-existent term'
  },
  {
    query: 'homelab security',
    shouldFindResults: true,
    minResults: 1,
    description: 'Multi-word search'
  }
];

/**
 * Find search input element
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<import('@playwright/test').ElementHandle>}
 */
async function findSearchInput(page) {
  for (const selector of SEARCH_SELECTORS.input) {
    try {
      const element = await page.$(selector);
      if (element) {
        const isVisible = await element.isVisible();
        if (isVisible) {
          return element;
        }
      }
    } catch (error) {
      continue;
    }
  }

  throw new Error('Search input not found. Searched selectors: ' + SEARCH_SELECTORS.input.join(', '));
}

/**
 * Find search results container
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<import('@playwright/test').ElementHandle|null>}
 */
async function findSearchResults(page) {
  for (const selector of SEARCH_SELECTORS.results) {
    try {
      const element = await page.$(selector);
      if (element) {
        const isVisible = await element.isVisible();
        if (isVisible) {
          return element;
        }
      }
    } catch (error) {
      continue;
    }
  }

  return null;
}

/**
 * Count search result items
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<number>}
 */
async function countResults(page) {
  for (const selector of SEARCH_SELECTORS.resultItems) {
    try {
      const elements = await page.$$(selector);
      if (elements && elements.length > 0) {
        return elements.length;
      }
    } catch (error) {
      continue;
    }
  }

  return 0;
}

/**
 * Check if no-results message is displayed
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<boolean>}
 */
async function hasNoResultsMessage(page) {
  for (const selector of SEARCH_SELECTORS.noResults) {
    try {
      const element = await page.$(selector);
      if (element) {
        const isVisible = await element.isVisible();
        if (isVisible) {
          return true;
        }
      }
    } catch (error) {
      continue;
    }
  }

  return false;
}

/**
 * Test search input accessibility
 * @param {import('@playwright/test').Page} page
 * @param {import('@playwright/test').ElementHandle} searchInput
 * @returns {Promise<{accessible: boolean, issues: string[]}>}
 */
async function testAccessibility(page, searchInput) {
  const issues = [];

  const accessibility = await page.evaluate((input) => {
    const hasLabel = input.getAttribute('aria-label') ||
                     input.getAttribute('placeholder') ||
                     document.querySelector(`label[for="${input.id}"]`);

    const hasRole = input.getAttribute('role') === 'searchbox' || input.type === 'search';

    return {
      hasLabel: !!hasLabel,
      hasRole: !!hasRole,
      ariaLabel: input.getAttribute('aria-label'),
      placeholder: input.getAttribute('placeholder')
    };
  }, searchInput);

  if (!accessibility.hasLabel) {
    issues.push('Search input lacks accessible label');
  }

  if (!accessibility.hasRole) {
    issues.push('Search input should have type="search" or role="searchbox"');
  }

  return {
    accessible: issues.length === 0,
    issues,
    details: accessibility
  };
}

/**
 * Test search functionality with a specific query
 * @param {import('@playwright/test').Page} page
 * @param {object} testCase
 * @returns {Promise<{success: boolean, errors: string[], resultCount: number}>}
 */
async function testSearchQuery(page, testCase) {
  const errors = [];
  let resultCount = 0;

  try {
    console.log(`  → Testing query: "${testCase.query}" (${testCase.description})`);

    // Find search input
    const searchInput = await findSearchInput(page);

    // Clear any existing input
    await searchInput.click({ clickCount: 3 });
    await searchInput.press('Backspace');

    // Type search query
    await searchInput.type(testCase.query, { delay: 50 });

    // Wait for search results to update (debounce time + processing)
    await page.waitForTimeout(500);

    // Check for results
    resultCount = await countResults(page);
    const hasNoResults = await hasNoResultsMessage(page);

    if (testCase.shouldFindResults) {
      if (resultCount === 0 && !hasNoResults) {
        errors.push(`No results found for "${testCase.query}", but results were expected`);
      } else if (resultCount < testCase.minResults) {
        errors.push(`Found ${resultCount} results, expected at least ${testCase.minResults}`);
      }
    } else {
      if (resultCount > 0) {
        errors.push(`Found ${resultCount} results for "${testCase.query}", but no results were expected`);
      }
      if (!hasNoResults) {
        errors.push('No "no results" message displayed when search returned no results');
      }
    }

    // Take screenshot
    const screenshotPath = path.join(SCREENSHOTS_DIR, `search-${testCase.query.replace(/\s+/g, '-')}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false });

  } catch (error) {
    errors.push(`Search test failed: ${error.message}`);
  }

  return {
    success: errors.length === 0,
    errors,
    resultCount
  };
}

/**
 * Test search result quality
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<{success: boolean, issues: string[], samples: object[]}>}
 */
async function testResultQuality(page) {
  const issues = [];
  const samples = [];

  try {
    // Search for a common term
    const searchInput = await findSearchInput(page);
    await searchInput.click({ clickCount: 3 });
    await searchInput.press('Backspace');
    await searchInput.type('security', { delay: 50 });
    await page.waitForTimeout(500);

    // Analyze first 3 results
    const results = await page.evaluate(() => {
      const resultElements = document.querySelectorAll('.search-result, .result-item, [data-search-result]');
      const analyzed = [];

      for (let i = 0; i < Math.min(3, resultElements.length); i++) {
        const result = resultElements[i];
        const title = result.querySelector('h3, h4, .title, [data-result-title]');
        const link = result.querySelector('a');
        const excerpt = result.querySelector('.excerpt, .description, [data-result-excerpt]');

        analyzed.push({
          hasTitle: !!title,
          hasLink: !!link,
          hasExcerpt: !!excerpt,
          titleText: title ? title.textContent.trim().substring(0, 50) : null,
          linkHref: link ? link.getAttribute('href') : null
        });
      }

      return analyzed;
    });

    results.forEach((result, index) => {
      samples.push(result);

      if (!result.hasTitle) {
        issues.push(`Result ${index + 1} lacks a title`);
      }
      if (!result.hasLink) {
        issues.push(`Result ${index + 1} lacks a clickable link`);
      }
      if (!result.hasExcerpt) {
        issues.push(`Result ${index + 1} lacks an excerpt/description`);
      }
    });

  } catch (error) {
    issues.push(`Result quality test failed: ${error.message}`);
  }

  return {
    success: issues.length === 0,
    issues,
    samples
  };
}

/**
 * Monitor console errors during search
 * @param {import('@playwright/test').Page} page
 * @returns {Array}
 */
function setupConsoleMonitoring(page) {
  const consoleErrors = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push({
        text: msg.text(),
        location: msg.location()
      });
    }
  });

  page.on('pageerror', error => {
    consoleErrors.push({
      text: error.message,
      stack: error.stack
    });
  });

  return consoleErrors;
}

/**
 * Main test execution
 */
async function runSearchTests() {
  console.log('🔍 Search Functionality Test Suite\n');
  console.log('='.repeat(50));

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  const page = await context.newPage();

  // Setup console monitoring
  const consoleErrors = setupConsoleMonitoring(page);

  const report = {
    timestamp: new Date().toISOString(),
    tests: {},
    summary: {
      total: 0,
      passed: 0,
      failed: 0
    }
  };

  try {
    // Create screenshots directory
    await fs.mkdir(SCREENSHOTS_DIR, { recursive: true });

    // Navigate to homepage (or search page)
    console.log('\n📍 Navigating to search page...');
    await page.goto(`${BASE_URL}/posts/`, {
      waitUntil: 'networkidle',
      timeout: TIMEOUT_MS
    });

    await page.waitForTimeout(1000);

    // Test 1: Search input existence and accessibility
    console.log('\n🔍 Test 1: Search Input Accessibility');
    report.tests.accessibility = {};
    try {
      const searchInput = await findSearchInput(page);
      const accessibility = await testAccessibility(page, searchInput);

      report.tests.accessibility = {
        passed: accessibility.accessible,
        issues: accessibility.issues,
        details: accessibility.details
      };

      if (accessibility.accessible) {
        console.log('  ✅ Search input is accessible');
        report.summary.passed++;
      } else {
        console.log('  ❌ Accessibility issues found:');
        accessibility.issues.forEach(issue => console.log(`     - ${issue}`));
        report.summary.failed++;
      }
      report.summary.total++;
    } catch (error) {
      console.log(`  ❌ Failed: ${error.message}`);
      report.tests.accessibility = { passed: false, error: error.message };
      report.summary.failed++;
      report.summary.total++;
    }

    // Test 2-N: Query tests
    console.log('\n🔍 Test 2: Search Queries');
    report.tests.queries = [];

    for (const testCase of TEST_QUERIES) {
      const result = await testSearchQuery(page, testCase);

      report.tests.queries.push({
        query: testCase.query,
        description: testCase.description,
        passed: result.success,
        resultCount: result.resultCount,
        errors: result.errors
      });

      if (result.success) {
        console.log(`     ✅ "${testCase.query}": ${result.resultCount} results`);
        report.summary.passed++;
      } else {
        console.log(`     ❌ "${testCase.query}": Failed`);
        result.errors.forEach(error => console.log(`        - ${error}`));
        report.summary.failed++;
      }
      report.summary.total++;
    }

    // Test 3: Result quality
    console.log('\n🔍 Test 3: Search Result Quality');
    const qualityTest = await testResultQuality(page);

    report.tests.quality = {
      passed: qualityTest.success,
      issues: qualityTest.issues,
      samples: qualityTest.samples
    };

    if (qualityTest.success) {
      console.log('  ✅ Search results have good quality');
      report.summary.passed++;
    } else {
      console.log('  ❌ Quality issues found:');
      qualityTest.issues.forEach(issue => console.log(`     - ${issue}`));
      report.summary.failed++;
    }
    report.summary.total++;

    // Test 4: Console errors
    console.log('\n🔍 Test 4: Console Errors');
    report.tests.consoleErrors = {
      count: consoleErrors.length,
      errors: consoleErrors,
      passed: consoleErrors.length === 0
    };

    if (consoleErrors.length === 0) {
      console.log('  ✅ No console errors detected');
      report.summary.passed++;
    } else {
      console.log(`  ❌ Found ${consoleErrors.length} console errors:`);
      consoleErrors.forEach((error, index) => {
        console.log(`     ${index + 1}. ${error.text}`);
      });
      report.summary.failed++;
    }
    report.summary.total++;

  } catch (error) {
    console.error('\n❌ Test suite failed:', error.message);
    report.error = error.message;
    report.stack = error.stack;
  } finally {
    await browser.close();
  }

  // Generate report
  console.log('\n' + '='.repeat(50));
  console.log(`\n📊 Test Summary: ${report.summary.passed}/${report.summary.total} passed`);

  if (report.summary.failed > 0) {
    console.log(`   ❌ ${report.summary.failed} tests failed`);
  } else {
    console.log('   ✅ All tests passed!');
  }

  // Save report
  const reportDir = path.dirname(REPORT_FILE);
  await fs.mkdir(reportDir, { recursive: true });
  await fs.writeFile(REPORT_FILE, JSON.stringify(report, null, 2));

  console.log(`\n📄 Report saved: ${REPORT_FILE}`);
  console.log(`📸 Screenshots saved: ${SCREENSHOTS_DIR}`);

  // Exit with appropriate code
  process.exit(report.summary.failed > 0 ? 1 : 0);
}

// Run tests
runSearchTests().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
