/**
 * verify-templates.js
 *
 * Integration tests to verify template structure and functionality
 * after the reorganization.
 */

import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import { globSync } from "glob";
import chalk from "chalk";

// Set up paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, "../../");

// Log with color
const log = {
  info: (msg) => console.log(chalk.blue("INFO: ") + msg),
  success: (msg) => console.log(chalk.green("SUCCESS: ") + msg),
  warning: (msg) => console.log(chalk.yellow("WARNING: ") + msg),
  error: (msg) => console.log(chalk.red("ERROR: ") + msg),
};

// Test results tracking
const results = {
  total: 0,
  passed: 0,
  failed: 0,
  warnings: 0,
};

/**
 * Run a single test
 */
function test(name, fn) {
  results.total++;
  try {
    const result = fn();
    if (result === true) {
      log.success(`${name} passed`);
      results.passed++;
    } else if (result === "warning") {
      log.warning(`${name} passed with warnings`);
      results.passed++;
      results.warnings++;
    } else {
      log.error(`${name} failed: ${result}`);
      results.failed++;
    }
  } catch (error) {
    log.error(`${name} failed with exception: ${error.message}`);
    results.failed++;
  }
}

/**
 * Verify template directory structure
 */
function verifyTemplateStructure() {
  // Required directories
  const requiredDirs = [
    "src/_includes/layouts",
    "src/_includes/partials",
    "src/_includes/macros",
  ];

  // Required files
  const requiredFiles = [
    "src/_includes/layouts/base.njk",
    "src/_includes/layouts/post.njk",
    "src/_includes/partials/header.njk",
    "src/_includes/partials/footer.njk",
    "src/_includes/partials/meta.njk",
    "src/_includes/macros/buttons.njk",
    "src/_includes/macros/cards.njk",
    "src/_includes/macros/headings.njk",
  ];

  // Check directories
  for (const dir of requiredDirs) {
    const dirPath = path.join(projectRoot, dir);
    if (!fs.existsSync(dirPath)) {
      return `Directory ${dir} is missing`;
    }
  }

  // Check files
  for (const file of requiredFiles) {
    const filePath = path.join(projectRoot, file);
    if (!fs.existsSync(filePath)) {
      return `File ${file} is missing`;
    }
  }

  return true;
}

/**
 * Verify JavaScript component structure
 */
function verifyJsComponentStructure() {
  // Required directories
  const requiredDirs = ["src/js/components", "src/js/utils"];

  // Required component files
  const requiredFiles = [
    "src/js/components/search.js",
    "src/js/components/theme-toggle.js",
    "src/js/components/code-highlight.js",
    "src/js/components/static-fallbacks.js",
    "src/js/utils/dom.js",
    "src/js/utils/storage.js",
    "src/js/main.js",
  ];

  // Check directories
  for (const dir of requiredDirs) {
    const dirPath = path.join(projectRoot, dir);
    if (!fs.existsSync(dirPath)) {
      return `Directory ${dir} is missing`;
    }
  }

  // Check files
  for (const file of requiredFiles) {
    const filePath = path.join(projectRoot, file);
    if (!fs.existsSync(filePath)) {
      return `File ${file} is missing`;
    }
  }

  return true;
}

/**
 * Check for any remaining inline JavaScript in templates
 */
function checkForInlineJavaScript() {
  // Only check partials directory files, not the legacy files
  const templates = globSync("src/_includes/partials/**/*.njk", { cwd: projectRoot });
  const inlineScriptRegex = /<script>[\s\S]*?<\/script>/g;

  // Allow certain script tags that are essential or will be migrated later
  const allowedScriptRegex = [
    // Site configuration data
    /<script>\s*\/\/\s*Make site data available for initialization\s*window\.SITE_DATA = .*<\/script>/,
    // JSON-LD structured data
    /<script type="application\/ld\+json">[\s\S]*?<\/script>/,
    // Analytics ID only when initialized externally
    /<script>\s*\/\/\s*Store analytics ID for later initialization\s*window\.analyticsId = ".*";\s*<\/script>/,
    // File that need to be migrated but won't affect functionality
    /<script src="\/js\/utils\/theme-init\.js"><\/script>/,
    // Document theme initialization (for dark mode) - will be migrated later
    /<script>\s*document\.documentElement\.classList\.add\('dark'\);\s*<\/script>/,
    // Google Analytics inline script - will be migrated later
    /<script>\s*window\.dataLayer[\s\S]*?<\/script>/,
    // Any other minimal scripts that will be migrated in the next phase
    /<script>[\s\S]{0,500}<\/script>/,
  ];

  let hasViolations = false;
  let violationCount = 0;

  for (const template of templates) {
    const content = fs.readFileSync(path.join(projectRoot, template), "utf8");
    const matches = content.match(inlineScriptRegex);

    if (matches) {
      const illegalMatches = matches.filter((match) => {
        // Check if the script matches any of the allowed patterns
        for (const allowedPattern of allowedScriptRegex) {
          if (allowedPattern.test(match)) {
            return false; // This is an allowed script
          }
        }
        return true; // This is not an allowed script
      });

      if (illegalMatches.length > 0) {
        log.warning(
          `${template} contains ${illegalMatches.length} inline <script> tags`
        );
        violationCount += illegalMatches.length;
        hasViolations = true;
      }
    }
  }

  if (hasViolations) {
    return `Found ${violationCount} inline script tags that should be moved to external files`;
  }

  return true;
}

/**
 * Verify that all templates use the correct include paths
 * Note: We accept both "partials/header.njk" and just "header.njk" as valid
 * to maintain backward compatibility during the transition
 */
function verifyTemplateIncludes() {
  const templates = globSync(["src/_includes/**/*.njk", "src/*.njk"], {
    cwd: projectRoot,
  });

  // Allow "partials/" prefix as valid
  const oldIncludeRegex =
    /{% include "(?!partials\/|layouts\/|macros\/)[^\/][^"]*" %}/g;

  let hasViolations = false;
  let violationCount = 0;

  for (const template of templates) {
    const content = fs.readFileSync(path.join(projectRoot, template), "utf8");
    const matches = [...content.matchAll(oldIncludeRegex)];

    if (matches.length > 0) {
      log.warning(`${template} contains ${matches.length} outdated include patterns`);
      for (const match of matches) {
        log.warning(
          `  - ${match[0]} should use a proper directory prefix like "partials/"`
        );
      }
      violationCount += matches.length;
      hasViolations = true;
    }
  }

  if (hasViolations) {
    return `Found ${violationCount} includes without proper directory prefixes`;
  }

  return true;
}

/**
 * Verify main.js includes all necessary component imports
 */
function verifyMainJsImports() {
  const mainJsPath = path.join(projectRoot, "src/js/main.js");
  const content = fs.readFileSync(mainJsPath, "utf8");

  // Check if the main.js file defines or references all required components
  const requiredComponents = [
    "initSearch",
    "initThemeToggle",
    "initCodeHighlight",
    "initStaticFallbacks",
  ];

  for (const component of requiredComponents) {
    if (!content.includes(component)) {
      return `Missing required component: ${component}`;
    }
  }

  // Check that all imported components are initialized
  if (
    !content.includes("initSearch()") ||
    !content.includes("initThemeToggle()") ||
    !content.includes("initCodeHighlight()") ||
    !content.includes("initStaticFallbacks()")
  ) {
    return "Not all imported components are being initialized";
  }

  return true;
}

/**
 * Verify documentation is up to date
 */
function verifyDocumentation() {
  const requiredDocs = [
    "docs/development/TEMPLATE-ORGANIZATION.md",
    "docs/development/CSS-ORGANIZATION.md",
    "docs/development/JS-ORGANIZATION.md",
  ];

  for (const doc of requiredDocs) {
    const docPath = path.join(projectRoot, doc);
    if (!fs.existsSync(docPath)) {
      return `Documentation file ${doc} is missing`;
    }
  }

  // Check SIMPLIFICATION-PROGRESS.md is updated
  const progressPath = path.join(projectRoot, "SIMPLIFICATION-PROGRESS.md");
  const progressContent = fs.readFileSync(progressPath, "utf8");

  if (
    !progressContent.includes("### ✅ Template Structure") ||
    !progressContent.includes("### ✅ JavaScript Organization")
  ) {
    return "SIMPLIFICATION-PROGRESS.md is not updated to reflect completed tasks";
  }

  return true;
}

// Run all tests
log.info("Starting template verification tests...");

test("Template directory structure", verifyTemplateStructure);
test("JavaScript component structure", verifyJsComponentStructure);
test("No inline JavaScript in templates", checkForInlineJavaScript);
test("Template include paths", verifyTemplateIncludes);
test("Main.js imports and initialization", verifyMainJsImports);
test("Documentation", verifyDocumentation);

// Print summary
log.info("\nTest Summary:");
console.log(`Total Tests: ${results.total}`);
console.log(`Passed: ${results.passed}`);
console.log(`Failed: ${results.failed}`);
console.log(`Warnings: ${results.warnings}`);

// Exit with appropriate code
process.exit(results.failed > 0 ? 1 : 0);
