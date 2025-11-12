const { chromium } = require('@playwright/test');
const fs = require('fs').promises;
const path = require('path');

const BASE_URL = 'http://localhost:8080';
const TIMEOUT_MS = 10000;
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'screenshots', 'dark-mode');

/**
 * Dark mode toggle selectors (ordered by priority)
 */
const TOGGLE_SELECTORS = [
  '[aria-label*="theme"]',
  '[aria-label*="Theme"]',
  '[data-theme-toggle]',
  '.theme-toggle',
  'button:has-text("theme")',
  'button:has-text("Theme")',
  '[class*="dark-mode"]',
  '[class*="theme-switch"]'
];

/**
 * Theme detection patterns
 * Check for CSS classes on html/body or data attributes
 */
const THEME_PATTERNS = {
  dark: ['dark', 'dark-mode', 'theme-dark', 'dark-theme'],
  light: ['light', 'light-mode', 'theme-light', 'light-theme']
};

/**
 * Find dark mode toggle element
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<{selector: string, element: import('@playwright/test').ElementHandle}>}
 */
async function findToggleElement(page) {
  for (const selector of TOGGLE_SELECTORS) {
    try {
      const element = await page.$(selector);
      if (element) {
        const isVisible = await element.isVisible();
        const isEnabled = await element.isEnabled();

        if (isVisible && isEnabled) {
          return { selector, element };
        }
      }
    } catch (error) {
      // Continue to next selector
      continue;
    }
  }

  throw new Error('Dark mode toggle not found. Searched selectors: ' + TOGGLE_SELECTORS.join(', '));
}

/**
 * Detect current theme from DOM
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<{theme: string, detected: string, source: string}>}
 */
async function detectTheme(page) {
  const themeInfo = await page.evaluate((patterns) => {
    const html = document.documentElement;
    const body = document.body;

    // Check html element classes
    for (const darkClass of patterns.dark) {
      if (html.classList.contains(darkClass)) {
        return { theme: 'dark', detected: darkClass, source: 'html.class' };
      }
    }

    // Check body element classes
    for (const darkClass of patterns.dark) {
      if (body.classList.contains(darkClass)) {
        return { theme: 'dark', detected: darkClass, source: 'body.class' };
      }
    }

    // Check data attributes
    const htmlTheme = html.getAttribute('data-theme');
    if (htmlTheme === 'dark') {
      return { theme: 'dark', detected: htmlTheme, source: 'html.data-theme' };
    }

    const bodyTheme = body.getAttribute('data-theme');
    if (bodyTheme === 'dark') {
      return { theme: 'dark', detected: bodyTheme, source: 'body.data-theme' };
    }

    // Check for light mode explicitly
    for (const lightClass of patterns.light) {
      if (html.classList.contains(lightClass) || body.classList.contains(lightClass)) {
        return { theme: 'light', detected: lightClass, source: html.classList.contains(lightClass) ? 'html.class' : 'body.class' };
      }
    }

    // Default to light if no dark mode detected
    return { theme: 'light', detected: 'default', source: 'default' };
  }, THEME_PATTERNS);

  return themeInfo;
}

/**
 * Check localStorage for theme persistence
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<{hasStorage: boolean, key: string, value: string}>}
 */
async function checkThemePersistence(page) {
  const storageInfo = await page.evaluate(() => {
    const possibleKeys = ['theme', 'color-theme', 'dark-mode', 'mode', 'color-mode'];

    for (const key of possibleKeys) {
      const value = localStorage.getItem(key);
      if (value !== null) {
        return { hasStorage: true, key, value };
      }
    }

    return { hasStorage: false, key: null, value: null };
  });

  return storageInfo;
}

/**
 * Validate dark mode toggle functionality
 * @param {import('@playwright/test').Page} page
 * @returns {Promise<{success: boolean, errors: string[], warnings: string[], details: object}>}
 */
async function validateDarkModeToggle(page) {
  const errors = [];
  const warnings = [];
  const details = {};

  try {
    // Navigate to homepage
    console.log('  → Navigating to homepage...');
    await page.goto(BASE_URL, {
      waitUntil: 'networkidle',
      timeout: TIMEOUT_MS
    });

    // Wait for page to stabilize
    await page.waitForTimeout(1000);

    // Detect initial theme
    console.log('  → Detecting initial theme...');
    const initialTheme = await detectTheme(page);
    details.initialTheme = initialTheme;
    console.log(`     Initial theme: ${initialTheme.theme} (${initialTheme.detected} via ${initialTheme.source})`);

    // Find toggle element
    console.log('  → Finding dark mode toggle...');
    const toggle = await findToggleElement(page);
    details.toggleSelector = toggle.selector;
    console.log(`     Toggle found: ${toggle.selector}`);

    // Capture initial screenshot
    console.log('  → Capturing before screenshot...');
    await fs.mkdir(SCREENSHOTS_DIR, { recursive: true });
    await page.screenshot({
      path: path.join(SCREENSHOTS_DIR, `before-${initialTheme.theme}.png`),
      fullPage: false
    });

    // Click toggle
    console.log('  → Clicking toggle...');
    await toggle.element.click();

    // Wait for theme transition
    await page.waitForTimeout(500);

    // Detect theme after toggle
    console.log('  → Detecting theme after toggle...');
    const afterToggleTheme = await detectTheme(page);
    details.afterToggleTheme = afterToggleTheme;
    console.log(`     Theme after toggle: ${afterToggleTheme.theme} (${afterToggleTheme.detected} via ${afterToggleTheme.source})`);

    // Verify theme changed
    if (initialTheme.theme === afterToggleTheme.theme) {
      errors.push(`Theme did not change after toggle (still ${initialTheme.theme})`);
    } else {
      console.log(`     ✅ Theme changed: ${initialTheme.theme} → ${afterToggleTheme.theme}`);
    }

    // Capture screenshot after toggle
    console.log('  → Capturing after screenshot...');
    await page.screenshot({
      path: path.join(SCREENSHOTS_DIR, `after-${afterToggleTheme.theme}.png`),
      fullPage: false
    });

    // Check localStorage persistence
    console.log('  → Checking theme persistence...');
    const storageInfo = await checkThemePersistence(page);
    details.persistence = storageInfo;

    if (storageInfo.hasStorage) {
      console.log(`     ✅ Theme persisted: ${storageInfo.key}=${storageInfo.value}`);
    } else {
      warnings.push('No localStorage persistence detected');
    }

    // Toggle back to original state
    console.log('  → Toggling back to original state...');
    await toggle.element.click();
    await page.waitForTimeout(500);

    const finalTheme = await detectTheme(page);
    details.finalTheme = finalTheme;
    console.log(`     Final theme: ${finalTheme.theme}`);

    // Verify returned to original state
    if (initialTheme.theme !== finalTheme.theme) {
      warnings.push(`Theme did not return to original state (${initialTheme.theme} → ${finalTheme.theme})`);
    } else {
      console.log(`     ✅ Returned to original state: ${finalTheme.theme}`);
    }

    // Capture final screenshot
    await page.screenshot({
      path: path.join(SCREENSHOTS_DIR, `final-${finalTheme.theme}.png`),
      fullPage: false
    });

    // Check for console errors
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    page.on('pageerror', error => {
      consoleErrors.push(error.message);
    });

    if (consoleErrors.length > 0) {
      warnings.push(`${consoleErrors.length} console errors detected`);
      details.consoleErrors = consoleErrors;
    }

    return {
      success: errors.length === 0,
      errors,
      warnings,
      details
    };

  } catch (error) {
    errors.push(`Fatal error: ${error.message}`);
    return {
      success: false,
      errors,
      warnings,
      details
    };
  }
}

/**
 * Generate console report
 * @param {object} result
 */
function printReport(result) {
  console.log('\n' + '='.repeat(80));
  console.log('🌙 DARK MODE TOGGLE VALIDATION REPORT');
  console.log('='.repeat(80) + '\n');

  // Overall status
  const status = result.success ? '✅ PASSED' : '❌ FAILED';
  console.log(`📊 STATUS: ${status}\n`);

  // Details
  if (result.details.initialTheme) {
    console.log('📋 THEME TRANSITIONS:');
    console.log(`   Initial:  ${result.details.initialTheme.theme} (${result.details.initialTheme.detected})`);
    console.log(`   Toggled:  ${result.details.afterToggleTheme.theme} (${result.details.afterToggleTheme.detected})`);
    console.log(`   Final:    ${result.details.finalTheme.theme} (${result.details.finalTheme.detected})\n`);
  }

  if (result.details.toggleSelector) {
    console.log('🎯 TOGGLE ELEMENT:');
    console.log(`   Selector: ${result.details.toggleSelector}\n`);
  }

  if (result.details.persistence) {
    console.log('💾 PERSISTENCE:');
    if (result.details.persistence.hasStorage) {
      console.log(`   ✅ localStorage: ${result.details.persistence.key}=${result.details.persistence.value}`);
    } else {
      console.log('   ⚠️  No localStorage persistence');
    }
    console.log('');
  }

  // Errors
  if (result.errors.length > 0) {
    console.log('❌ ERRORS:');
    result.errors.forEach(err => console.log(`   • ${err}`));
    console.log('');
  }

  // Warnings
  if (result.warnings.length > 0) {
    console.log('⚠️  WARNINGS:');
    result.warnings.forEach(warn => console.log(`   • ${warn}`));
    console.log('');
  }

  // Screenshots
  console.log('📸 SCREENSHOTS:');
  console.log(`   Directory: ${SCREENSHOTS_DIR}`);
  console.log(`   Files: before-*.png, after-*.png, final-*.png\n`);

  console.log('='.repeat(80) + '\n');
}

/**
 * Main test function
 */
async function testDarkModeToggle() {
  console.log('🌙 Dark Mode Toggle Functionality Test\n');

  // Check if server is running
  console.log('🌐 Checking server availability...');
  try {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
    console.log('   ✅ Server is running\n');
  } catch (error) {
    console.error(`❌ Cannot connect to ${BASE_URL}`);
    console.error('   Please start the development server: npm start');
    process.exit(1);
  }

  const browser = await chromium.launch({
    headless: true,
    timeout: TIMEOUT_MS
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2
  });

  const page = await context.newPage();

  console.log('🧪 Running dark mode toggle tests...\n');
  const result = await validateDarkModeToggle(page);

  await browser.close();

  // Save JSON report
  const reportPath = path.join(__dirname, '..', 'dark-mode-validation-report.json');
  await fs.writeFile(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    baseUrl: BASE_URL,
    ...result
  }, null, 2));

  // Print console report
  printReport(result);

  console.log(`📄 Detailed report saved to: ${reportPath}\n`);

  // Exit with appropriate code
  process.exit(result.success ? 0 : 1);
}

// Run test
testDarkModeToggle().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
