/**
 * Component Test Runner
 *
 * Runs unit and integration tests for JavaScript components
 * Implemented as part of Phase 4 testing
 */

const fs = require("fs");
const path = require("path");
const chalk = require("chalk");
const { resetCounters, printSummary } = require("../../tests/test-framework");

// Constants for test directories
const TEST_DIRS = {
  unit: path.join(__dirname, "../../tests/unit"),
  integration: path.join(__dirname, "../../tests/integration"),
  security: path.join(__dirname, "../../tests/security"),
  performance: path.join(__dirname, "../../tests/performance"),
};

// Parse command-line arguments
const args = process.argv.slice(2);
const options = {
  category: args.find((arg) => Object.keys(TEST_DIRS).includes(arg)) || "all",
  verbose: args.includes("--verbose"),
  pattern: args.find((arg) => arg.startsWith("--pattern="))?.split("=")[1],
};

// Print welcome message
console.log(chalk.blue("=== Component Test Runner ==="));
console.log(chalk.blue(`Running tests in category: ${options.category}`));
if (options.pattern) {
  console.log(chalk.blue(`Filtering by pattern: ${options.pattern}`));
}
console.log("");

/**
 * Check if a file matches the pattern
 *
 * @param {string} filePath - The file path to check
 * @returns {boolean} - Whether the file matches the pattern
 */
function fileMatchesPattern(filePath) {
  if (!options.pattern) {
    return true;
  }

  return path.basename(filePath).includes(options.pattern);
}

/**
 * Run tests in a directory
 *
 * @param {string} directory - The directory containing test files
 */
function runTestsInDirectory(directory) {
  // Check if directory exists
  if (!fs.existsSync(directory)) {
    console.log(chalk.yellow(`Warning: Directory ${directory} does not exist.`));
    return;
  }

  // Get all test files
  const testFiles = fs
    .readdirSync(directory)
    .filter((file) => file.endsWith(".test.js"))
    .filter((file) => fileMatchesPattern(file))
    .map((file) => path.join(directory, file));

  if (testFiles.length === 0) {
    console.log(chalk.yellow(`No test files found in ${directory}`));
    return;
  }

  console.log(chalk.blue(`Found ${testFiles.length} test files in ${directory}`));

  // Run each test file
  testFiles.forEach((file) => {
    console.log(chalk.blue(`\nRunning tests in ${path.basename(file)}`));
    console.log(chalk.gray("------------------------------------------------"));

    try {
      // Clear module cache to ensure tests run fresh each time
      delete require.cache[require.resolve(file)];

      // Run the tests
      require(file);
    } catch (error) {
      console.log(chalk.red(`Error running tests in ${file}:`));
      console.log(chalk.red(error.stack));
    }
  });
}

// Reset counters before running tests
resetCounters();

// Run tests
if (options.category === "all") {
  // Run tests in all directories
  Object.values(TEST_DIRS).forEach((dir) => {
    runTestsInDirectory(dir);
  });
} else {
  // Run tests in a specific directory
  runTestsInDirectory(TEST_DIRS[options.category]);
}

// Print summary
printSummary();

// Exit with appropriate code
process.exit(0);
