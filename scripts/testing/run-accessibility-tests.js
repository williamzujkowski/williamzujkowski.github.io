/**
 * Accessibility Test Runner
 *
 * Tests website pages for accessibility compliance using axe-core
 * Implemented as part of Phase 4 testing
 */

const puppeteer = require("puppeteer");
const { AxePuppeteer } = require("@axe-core/puppeteer");
const chalk = require("chalk");
const path = require("path");
const fs = require("fs");

// URL of the local development server
const DEV_SERVER_URL = "http://localhost:8080";

// Pages to test
const PAGES_TO_TEST = ["/", "/blog/", "/links/"];

// Results directory
const RESULTS_DIR = path.join(__dirname, "../../accessibility-reports");

// Create results directory if it doesn't exist
if (!fs.existsSync(RESULTS_DIR)) {
  fs.mkdirSync(RESULTS_DIR, { recursive: true });
}

/**
 * Run accessibility tests on a page
 *
 * @param {Page} page - Puppeteer page object
 * @param {string} url - URL to test
 * @returns {Promise<Object>} - Test results
 */
async function testPage(page, url) {
  console.log(chalk.blue(`Testing page: ${url}`));

  try {
    // Navigate to the page
    await page.goto(url, { waitUntil: "networkidle2", timeout: 60000 });

    // Run axe on the page
    const results = await new AxePuppeteer(page).analyze();

    // Return the results
    return results;
  } catch (error) {
    console.error(chalk.red(`Error testing ${url}:`), error);
    return {
      url,
      error: error.message,
      violations: [],
      passes: [],
      incomplete: [],
      inapplicable: [],
    };
  }
}

/**
 * Print test results
 *
 * @param {Object} results - Test results
 * @param {string} url - URL that was tested
 */
function printResults(results, url) {
  console.log(chalk.blue(`\nResults for ${url}:`));

  // Check if there was an error
  if (results.error) {
    console.log(chalk.red(`Error: ${results.error}`));
    return;
  }

  // Print violations
  if (results.violations.length === 0) {
    console.log(chalk.green(`✓ No accessibility violations detected`));
  } else {
    console.log(
      chalk.red(`✗ ${results.violations.length} accessibility violations detected`)
    );

    results.violations.forEach((violation, index) => {
      console.log(chalk.red(`\n${index + 1}. ${violation.id}: ${violation.help}`));
      console.log(chalk.yellow(`   Impact: ${violation.impact}`));
      console.log(chalk.white(`   Description: ${violation.description}`));
      console.log(chalk.white(`   Affected nodes: ${violation.nodes.length}`));

      // Print the first node as an example
      if (violation.nodes.length > 0) {
        const node = violation.nodes[0];
        console.log(chalk.gray(`   Example: ${node.html}`));
        console.log(chalk.white(`   Fix: ${node.failureSummary}`));
      }
    });
  }

  // Print summary
  console.log(chalk.blue(`\nSummary:`));
  console.log(chalk.green(`✓ Passes: ${results.passes.length}`));
  console.log(chalk.red(`✗ Violations: ${results.violations.length}`));
  console.log(chalk.yellow(`⚠ Incomplete: ${results.incomplete.length}`));
  console.log(chalk.gray(`- Inapplicable: ${results.inapplicable.length}`));
}

/**
 * Save test results to a file
 *
 * @param {Object} results - Test results
 * @param {string} url - URL that was tested
 */
function saveResults(results, url) {
  // Create a filename based on the URL
  const filename =
    url === "/" ? "home.json" : url.replace(/\//g, "-").replace(/^-|-$/g, "") + ".json";

  const filePath = path.join(RESULTS_DIR, filename);

  // Save results to file
  fs.writeFileSync(filePath, JSON.stringify(results, null, 2));

  console.log(chalk.blue(`Results saved to ${filePath}`));
}

/**
 * Main function
 */
async function main() {
  console.log(chalk.blue("=== Accessibility Test Runner ==="));

  // Check if development server is running
  let browser;

  try {
    // Launch browser
    browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Set viewport size
    await page.setViewport({ width: 1280, height: 800 });

    // Check if server is running
    try {
      await page.goto(DEV_SERVER_URL, { timeout: 5000 });
      console.log(chalk.green("Development server is running."));
    } catch (error) {
      console.log(
        chalk.yellow("Development server is not running. Starting in 5 seconds...")
      );
      console.log(chalk.yellow('Please run "npm run serve" in another terminal.'));

      // Wait for the server to start
      await new Promise((resolve) => setTimeout(resolve, 5000));

      // Try again
      try {
        await page.goto(DEV_SERVER_URL, { timeout: 5000 });
        console.log(chalk.green("Development server is now running."));
      } catch (error) {
        console.log(
          chalk.red(
            'Could not connect to development server. Please run "npm run serve" and try again.'
          )
        );
        process.exit(1);
      }
    }

    // Run tests on each page
    const allResults = [];

    for (const pageUrl of PAGES_TO_TEST) {
      const url = DEV_SERVER_URL + pageUrl;
      const results = await testPage(page, url);

      // Print and save results
      printResults(results, pageUrl);
      saveResults(results, pageUrl);

      // Add to all results
      allResults.push({
        url: pageUrl,
        violations: results.violations.length,
        passes: results.passes.length,
      });
    }

    // Print summary
    console.log(chalk.blue("\n=== Test Summary ==="));

    let totalViolations = 0;
    let totalPasses = 0;

    allResults.forEach((result) => {
      console.log(
        `${result.url}: ${chalk.green(`${result.passes} passes`)}, ${chalk.red(`${result.violations} violations`)}`
      );
      totalViolations += result.violations;
      totalPasses += result.passes;
    });

    console.log(
      chalk.blue(
        `\nTotal: ${chalk.green(`${totalPasses} passes`)}, ${chalk.red(`${totalViolations} violations`)}`
      )
    );

    // Exit with appropriate code
    process.exit(totalViolations > 0 ? 1 : 0);
  } catch (error) {
    console.error(chalk.red("Error running tests:"), error);
    process.exit(1);
  } finally {
    // Close the browser
    if (browser) {
      await browser.close();
    }
  }
}

// Run the main function
main();
