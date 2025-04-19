/**
 * run-tests.js
 *
 * Master script to run all integration tests
 */

import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import chalk from "chalk";

// Set up paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, "../../");

// Log with color
console.log(chalk.blue("=================================================="));
console.log(chalk.blue("          WEBSITE INTEGRATION TESTS"));
console.log(chalk.blue("=================================================="));

try {
  // Run template structure tests
  console.log(chalk.yellow("\n1. Running Template Structure Tests..."));
  console.log(chalk.yellow("---------------------------------"));

  try {
    execSync("node scripts/testing/verify-templates.js", {
      cwd: projectRoot,
      stdio: "inherit",
    });
    console.log(chalk.green("\n✓ Template tests completed successfully"));
  } catch (error) {
    console.log(chalk.red("\n✗ Template tests failed"));
    process.exit(1);
  }

  // Run build verification tests
  console.log(chalk.yellow("\n2. Running Build Verification Tests..."));
  console.log(chalk.yellow("---------------------------------"));

  try {
    execSync("node scripts/testing/verify-build.js", {
      cwd: projectRoot,
      stdio: "inherit",
    });
    console.log(chalk.green("\n✓ Build verification tests completed successfully"));
  } catch (error) {
    console.log(chalk.red("\n✗ Build verification tests failed"));
    process.exit(1);
  }

  // All tests passed
  console.log(chalk.green("\n=================================================="));
  console.log(chalk.green("          ALL INTEGRATION TESTS PASSED"));
  console.log(chalk.green("=================================================="));

  process.exit(0);
} catch (error) {
  console.log(chalk.red("\nTest suite execution failed:"));
  console.log(chalk.red(error.message));
  process.exit(1);
}
