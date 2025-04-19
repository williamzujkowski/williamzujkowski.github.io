/**
 * Simple test framework for website testing
 * Implemented as part of Phase 4 testing
 */

const chalk = require("chalk");

// Test counters
let totalTests = 0;
let passedTests = 0;
let failedTests = 0;
let warnings = 0;

/**
 * Run a test function with the given name
 *
 * @param {string} name - The name of the test
 * @param {Function} testFn - The test function that returns true, a warning string, or throws an error
 */
function test(name, testFn) {
  totalTests++;

  console.log(chalk.blue(`Running test: ${name}`));

  try {
    const result = testFn();

    // If the result is true, the test passed
    if (result === true) {
      console.log(chalk.green(`✓ PASS: ${name}`));
      passedTests++;
    }
    // If the result is a string, it's a warning
    else if (typeof result === "string") {
      console.log(chalk.yellow(`⚠ WARNING: ${name} - ${result}`));
      passedTests++;
      warnings++;
    }
    // If it's anything else, it's a failure
    else {
      console.log(chalk.red(`✗ FAIL: ${name} - Unexpected return value: ${result}`));
      failedTests++;
    }
  } catch (error) {
    console.log(chalk.red(`✗ FAIL: ${name} - ${error.message}`));
    if (error.stack) {
      console.log(chalk.gray(error.stack.split("\n").slice(1).join("\n")));
    }
    failedTests++;
  }

  // Add a blank line after each test
  console.log("");
}

/**
 * Print a summary of the test results
 */
function printSummary() {
  console.log(chalk.blue("=== Test Summary ==="));
  console.log(chalk.blue(`Total tests: ${totalTests}`));
  console.log(chalk.green(`Passed: ${passedTests}`));
  console.log(chalk.red(`Failed: ${failedTests}`));
  if (warnings > 0) {
    console.log(chalk.yellow(`Warnings: ${warnings}`));
  }

  if (failedTests === 0) {
    console.log(chalk.green("\n✓ All tests passed!"));
    if (warnings > 0) {
      console.log(chalk.yellow(`⚠ But there were ${warnings} warnings.`));
    }
  } else {
    console.log(chalk.red(`\n✗ ${failedTests} tests failed.`));
  }
}

/**
 * Reset test counters
 */
function resetCounters() {
  totalTests = 0;
  passedTests = 0;
  failedTests = 0;
  warnings = 0;
}

/**
 * Assert module for testing
 */
const assert = {
  /**
   * Assert that two values are equal
   *
   * @param {*} actual - The actual value
   * @param {*} expected - The expected value
   * @param {string} message - Optional message
   */
  equal(actual, expected, message = "") {
    if (actual !== expected) {
      throw new Error(`${message} Expected ${expected} but got ${actual}`);
    }
  },

  /**
   * Assert that two values are not equal
   *
   * @param {*} actual - The actual value
   * @param {*} expected - The expected value
   * @param {string} message - Optional message
   */
  notEqual(actual, expected, message = "") {
    if (actual === expected) {
      throw new Error(`${message} Expected ${actual} not to equal ${expected}`);
    }
  },

  /**
   * Assert that a value is truthy
   *
   * @param {*} value - The value to check
   * @param {string} message - Optional message
   */
  ok(value, message = "") {
    if (!value) {
      throw new Error(`${message} Expected truthy value but got ${value}`);
    }
  },

  /**
   * Assert that a function throws an error
   *
   * @param {Function} fn - The function to call
   * @param {string|RegExp} expected - The expected error message or pattern
   * @param {string} message - Optional message
   */
  throws(fn, expected, message = "") {
    try {
      fn();
      throw new Error(`${message} Expected function to throw an error but it did not`);
    } catch (error) {
      if (expected instanceof RegExp) {
        if (!expected.test(error.message)) {
          throw new Error(
            `${message} Expected error message to match ${expected} but got ${error.message}`
          );
        }
      } else if (typeof expected === "string") {
        if (error.message !== expected) {
          throw new Error(
            `${message} Expected error message "${expected}" but got "${error.message}"`
          );
        }
      }
    }
  },

  /**
   * Assert that a value is within a range
   *
   * @param {number} actual - The actual value
   * @param {number} lower - The lower bound
   * @param {number} upper - The upper bound
   * @param {string} message - Optional message
   */
  range(actual, lower, upper, message = "") {
    if (actual < lower || actual > upper) {
      throw new Error(
        `${message} Expected ${actual} to be between ${lower} and ${upper}`
      );
    }
  },

  /**
   * Assert that an object has a property
   *
   * @param {Object} obj - The object to check
   * @param {string} prop - The property name
   * @param {string} message - Optional message
   */
  hasProperty(obj, prop, message = "") {
    if (!Object.prototype.hasOwnProperty.call(obj, prop)) {
      throw new Error(`${message} Expected object to have property ${prop}`);
    }
  },

  /**
   * Assert that a string contains a substring
   *
   * @param {string} haystack - The string to search in
   * @param {string} needle - The substring to search for
   * @param {string} message - Optional message
   */
  contains(haystack, needle, message = "") {
    if (!haystack.includes(needle)) {
      throw new Error(`${message} Expected "${haystack}" to contain "${needle}"`);
    }
  },
};

module.exports = {
  test,
  printSummary,
  resetCounters,
  assert,
};
