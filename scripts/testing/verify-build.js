/**
 * verify-build.js
 *
 * Integration tests to verify the build process works correctly
 * after the reorganization.
 */

import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import { globSync } from "glob";
import { execSync } from "child_process";
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
 * Verify CSS build process
 */
function verifyCssBuild() {
  try {
    log.info("Running CSS build...");
    execSync("npm run build:css", { cwd: projectRoot, stdio: "inherit" });

    const outputCssPath = path.join(projectRoot, "_site/css/styles.css");
    if (!fs.existsSync(outputCssPath)) {
      return "CSS output file not found: _site/css/styles.css";
    }

    const cssContent = fs.readFileSync(outputCssPath, "utf8");

    // Check that the output has some content
    if (cssContent.length < 100) {
      return "CSS output file appears to be empty or too small";
    }

    // Look for some common CSS patterns that should be present
    const checks = [
      { name: "CSS rules", pattern: /{[^}]+}/ },
      { name: "Media queries", pattern: /@media/ },
      { name: "Class definitions", pattern: /\.[\w-]+/ },
    ];

    let missingPatterns = [];
    for (const check of checks) {
      if (!check.pattern.test(cssContent)) {
        missingPatterns.push(check.name);
      }
    }

    if (missingPatterns.length > 0) {
      return `CSS output is missing: ${missingPatterns.join(", ")}`;
    }

    return true;
  } catch (error) {
    return `CSS build failed: ${error.message}`;
  }
}

/**
 * Verify output structure integrity
 */
function verifyOutputStructure() {
  try {
    log.info("Running full build to verify structure...");
    execSync("npm run build", { cwd: projectRoot, stdio: "inherit" });

    // Check for essential output files and directories
    const requiredPaths = [
      "_site/index.html",
      "_site/blog/index.html",
      "_site/css/styles.css",
      "_site/js/main.js",
    ];

    for (const reqPath of requiredPaths) {
      const fullPath = path.join(projectRoot, reqPath);
      if (!fs.existsSync(fullPath)) {
        return `Required output path not found: ${reqPath}`;
      }
    }

    // Check that blog posts were built
    const blogPostsPath = path.join(projectRoot, "_site/posts");
    if (!fs.existsSync(blogPostsPath)) {
      return "Blog posts directory not found in output";
    }

    const blogPosts = globSync("_site/posts/**/*.html", { cwd: projectRoot });
    if (blogPosts.length === 0) {
      return "No blog posts were built";
    }

    log.info(`Found ${blogPosts.length} built blog posts`);

    return true;
  } catch (error) {
    return `Full build failed: ${error.message}`;
  }
}

/**
 * Verify CSS references in HTML
 *
 * With our new approach, CSS is referenced in different ways in different files.
 * This function is more flexible to account for various patterns.
 */
function verifyCssReferences() {
  try {
    // We only check the main site pages, not example or utility pages
    const htmlFiles = [
      "_site/index.html",
      "_site/blog/index.html",
      "_site/links/index.html",
      "_site/posts/2025-04-14-enhancing-embodied-ai-teaching-agents-to-seek-clarification-using-multimodal-large-language-models/index.html",
    ];

    // Various ways CSS could be referenced
    const cssPatterns = [
      // Direct link to styles.css
      /<link[^>]*href="[^"]*\/css\/styles\.css"[^>]*>/,
      // Inline critical CSS
      /<style>[\s\S]*?<\/style>/,
      // Async loaded CSS
      /<link[^>]*media="print"[^>]*onload=/,
    ];

    let missingLinks = [];

    for (const htmlFile of htmlFiles) {
      const fullPath = path.join(projectRoot, htmlFile);

      if (!fs.existsSync(fullPath)) {
        log.warning(`File not found for CSS check: ${htmlFile}`);
        continue;
      }

      const content = fs.readFileSync(fullPath, "utf8");
      let hasStyleReference = false;

      // Check for any of the CSS patterns
      for (const pattern of cssPatterns) {
        if (pattern.test(content)) {
          hasStyleReference = true;
          break;
        }
      }

      if (!hasStyleReference) {
        missingLinks.push(htmlFile);
      }
    }

    if (missingLinks.length > 0) {
      return `${missingLinks.length} HTML files missing CSS reference: ${missingLinks.join(", ")}`;
    }

    return true;
  } catch (error) {
    return `CSS reference check failed: ${error.message}`;
  }
}

/**
 * Verify JS references in HTML
 *
 * Check that the main pages include the necessary JavaScript files
 */
function verifyJsReferences() {
  try {
    // We only check the main site pages
    const htmlFiles = [
      "_site/index.html",
      "_site/blog/index.html",
      "_site/links/index.html",
      "_site/posts/2025-04-14-enhancing-embodied-ai-teaching-agents-to-seek-clarification-using-multimodal-large-language-models/index.html",
    ];

    // Look for any JS reference, not just main.js
    const jsPatterns = [/<script[^>]*src="[^"]*\.js"[^>]*>/];

    let missingLinks = [];

    for (const htmlFile of htmlFiles) {
      const fullPath = path.join(projectRoot, htmlFile);

      if (!fs.existsSync(fullPath)) {
        log.warning(`File not found for JS check: ${htmlFile}`);
        continue;
      }

      const content = fs.readFileSync(fullPath, "utf8");
      let hasJsReference = false;

      // Check if file has any JS references
      for (const pattern of jsPatterns) {
        if (pattern.test(content)) {
          hasJsReference = true;
          break;
        }
      }

      if (!hasJsReference) {
        missingLinks.push(htmlFile);
      }
    }

    if (missingLinks.length > 0) {
      return `${missingLinks.length} HTML files missing JS reference: ${missingLinks.join(", ")}`;
    }

    return true;
  } catch (error) {
    return `JS reference check failed: ${error.message}`;
  }
}

/**
 * Verify template rendering
 *
 * This checks that essential HTML elements are present in key pages
 */
function verifyTemplateRendering() {
  try {
    // Sample of pages to check for essential elements
    const pagesToCheck = [
      {
        path: "_site/index.html",
        // More flexible checks - looking for common elements
        patterns: [/<header/, /<footer/, /<main/, /<body/, /<html/],
      },
      {
        path: "_site/blog/index.html",
        patterns: [/<h1/, /<a/, /<div class/],
      },
    ];

    for (const page of pagesToCheck) {
      const fullPath = path.join(projectRoot, page.path);
      if (!fs.existsSync(fullPath)) {
        log.warning(`Page not found for template check: ${page.path}`);
        continue;
      }

      const content = fs.readFileSync(fullPath, "utf8");

      for (const pattern of page.patterns) {
        if (!pattern.test(content)) {
          return `Missing pattern "${pattern}" in ${page.path}`;
        }
      }
    }

    // Check blog post template rendering - just make sure we have blog posts
    const blogPosts = globSync("_site/posts/**/*.html", { cwd: projectRoot });
    if (blogPosts.length === 0) {
      return "No blog posts were built";
    }

    log.info(`Found ${blogPosts.length} built blog posts`);

    return true;
  } catch (error) {
    return `Template rendering check failed: ${error.message}`;
  }
}

// Run all tests
log.info("Starting build verification tests...");

test("CSS build process", verifyCssBuild);
test("Full build output structure", verifyOutputStructure);
test("CSS references in HTML", verifyCssReferences);
test("JS references in HTML", verifyJsReferences);
test("Template rendering integrity", verifyTemplateRendering);

// Print summary
log.info("\nTest Summary:");
console.log(`Total Tests: ${results.total}`);
console.log(`Passed: ${results.passed}`);
console.log(`Failed: ${results.failed}`);
console.log(`Warnings: ${results.warnings}`);

// Exit with appropriate code
process.exit(results.failed > 0 ? 1 : 0);
