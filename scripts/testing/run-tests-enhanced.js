#!/usr/bin/env node
/**
 * Enhanced test runner for the project
 * Supports running different types of tests with consolidated reporting
 */

import { execSync } from "child_process";
import fs from "fs";
import path from "path";
import chalk from "chalk";
import { testConfig } from "../../tests/config/test-config.js";

// Ensure output directories exist
function ensureDirectories() {
  const dirs = [
    testConfig.dirs.coverage,
    testConfig.reports.outputDir,
    testConfig.visual.snapshotDir,
  ];

  dirs.forEach((dir) => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    types: [],
    coverage: false,
    watch: false,
    verbose: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--unit":
        options.types.push("unit");
        break;
      case "--integration":
        options.types.push("integration");
        break;
      case "--e2e":
        options.types.push("e2e");
        break;
      case "--visual":
        options.types.push("visual");
        break;
      case "--performance":
        options.types.push("performance");
        break;
      case "--all":
        options.types = ["unit", "integration", "e2e", "visual", "performance"];
        break;
      case "--coverage":
        options.coverage = true;
        break;
      case "--watch":
        options.watch = true;
        break;
      case "--verbose":
        options.verbose = true;
        break;
    }
  }

  // Default to unit tests if none specified
  if (options.types.length === 0) {
    options.types = ["unit"];
  }

  return options;
}

// Run unit and integration tests
function runJsTests(type, options) {
  console.log(chalk.blue(`\n=== Running ${type} Tests ===\n`));

  const testDir = testConfig.dirs[type];
  const testFiles = fs
    .readdirSync(testDir)
    .filter((file) => file.endsWith(".test.js"))
    .map((file) => path.join(testDir, file));

  if (testFiles.length === 0) {
    console.log(chalk.yellow(`No ${type} tests found in ${testDir}`));
    return;
  }

  const coverageArgs = options.coverage
    ? "--coverage --coverageDirectory=" + testConfig.dirs.coverage
    : "";
  const watchArgs = options.watch ? "--watch" : "";
  const verboseArgs = options.verbose ? "--verbose" : "";

  try {
    execSync(
      `node --experimental-vm-modules node_modules/jest/bin/jest.js ${testFiles.join(" ")} ${coverageArgs} ${watchArgs} ${verboseArgs}`,
      { stdio: "inherit" }
    );
    console.log(chalk.green(`\n✓ ${type} Tests completed successfully\n`));
  } catch (error) {
    console.error(chalk.red(`\n✗ ${type} Tests failed\n`));
    if (!options.watch) {
      process.exitCode = 1;
    }
  }
}

// Run E2E tests using Playwright
function runE2ETests(options) {
  console.log(chalk.blue("\n=== Running E2E Tests ===\n"));

  const verboseArgs = options.verbose ? "--debug" : "";
  const watchArgs = options.watch ? "--ui" : "";

  try {
    execSync(`npx playwright test ${verboseArgs} ${watchArgs}`, { stdio: "inherit" });
    console.log(chalk.green("\n✓ E2E Tests completed successfully\n"));
  } catch (error) {
    console.error(chalk.red("\n✗ E2E Tests failed\n"));
    if (!options.watch) {
      process.exitCode = 1;
    }
  }
}

// Run visual regression tests
function runVisualTests(options) {
  console.log(chalk.blue("\n=== Running Visual Regression Tests ===\n"));

  const updateArgs = options.updateSnapshots ? "--update-snapshots" : "";

  try {
    execSync(
      `npx playwright test --config=tests/visual/playwright.config.js ${updateArgs}`,
      { stdio: "inherit" }
    );
    console.log(chalk.green("\n✓ Visual Tests completed successfully\n"));
  } catch (error) {
    console.error(chalk.red("\n✗ Visual Tests failed\n"));
    console.log(
      chalk.yellow(
        "Run with --update-snapshots to update the baseline images if changes are expected"
      )
    );
    if (!options.watch) {
      process.exitCode = 1;
    }
  }
}

// Run performance tests
function runPerformanceTests() {
  console.log(chalk.blue("\n=== Running Performance Tests ===\n"));

  try {
    execSync("node tests/performance/bundle-size.test.js", { stdio: "inherit" });
    console.log(chalk.green("\n✓ Performance Tests completed successfully\n"));
  } catch (error) {
    console.error(chalk.red("\n✗ Performance Tests failed\n"));
    process.exitCode = 1;
  }
}

// Generate coverage report
function generateCoverageReport() {
  console.log(chalk.blue("\n=== Generating Coverage Report ===\n"));

  try {
    // Merge coverage reports if they exist
    if (fs.existsSync(path.join(testConfig.dirs.coverage, "coverage-final.json"))) {
      execSync(
        `npx nyc report --reporter=html --reporter=text --reporter=lcov --report-dir=${testConfig.reports.outputDir}/coverage`,
        { stdio: "inherit" }
      );
      console.log(
        chalk.green(
          `\n✓ Coverage report generated in ${testConfig.reports.outputDir}/coverage\n`
        )
      );
    } else {
      console.log(
        chalk.yellow(
          "\nNo coverage data found. Run tests with --coverage flag first.\n"
        )
      );
    }
  } catch (error) {
    console.error(chalk.red("\n✗ Failed to generate coverage report\n"));
  }
}

// Main function
async function main() {
  console.log(chalk.blue("=== Running Tests ==="));

  const options = parseArgs();
  ensureDirectories();

  console.log(chalk.green(`Test types: ${options.types.join(", ")}`));
  console.log(chalk.green(`Coverage: ${options.coverage}`));
  console.log(chalk.green(`Watch mode: ${options.watch}`));

  for (const type of options.types) {
    switch (type) {
      case "unit":
      case "integration":
        runJsTests(type, options);
        break;
      case "e2e":
        runE2ETests(options);
        break;
      case "visual":
        runVisualTests(options);
        break;
      case "performance":
        runPerformanceTests();
        break;
    }
  }

  if (options.coverage) {
    generateCoverageReport();
  }

  if (process.exitCode !== 1) {
    console.log(chalk.green("\n=== All Tests Completed Successfully ===\n"));
  } else {
    console.error(chalk.red("\n=== Tests Failed ===\n"));
  }
}

main().catch((error) => {
  console.error(chalk.red("Error running tests:"), error);
  process.exitCode = 1;
});
