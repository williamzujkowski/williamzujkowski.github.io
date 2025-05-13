/**
 * Critical CSS Extractor
 *
 * This script:
 * 1. Extracts critical CSS for different page templates
 * 2. Inlines the critical CSS in the HTML
 * 3. Adds async loading for the remaining CSS
 * 4. Generates optimized CSS bundles for each page type
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { glob } from "glob";
import critical from "critical";
import cssnano from "cssnano";
import postcss from "postcss";
import autoprefixer from "autoprefixer";
import { PurgeCSS } from "purgecss";

// Directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..");
const siteDir = path.join(rootDir, "_site");
const cssDir = path.join(siteDir, "css");
const optimizedCssDir = path.join(cssDir, "optimized");

// Page templates to extract critical CSS for
const PAGE_TEMPLATES = [
  { name: "home", url: "/", outputPath: "home.css" },
  { name: "blog", url: "/blog/", outputPath: "blog.css" },
  {
    name: "post",
    url: "/blog/2025-05-28-evaluating-large-language-models-for-smart-contract-vulnerability-detection-current-capabilities-limitations-and-future-potential/",
    outputPath: "post.css",
  },
];

// CSS files to optimize
const CSS_FILES = ["styles.css", "blog-enhanced.css"];

// PurgeCSS safelist
const PURGE_SAFELIST = [
  // Utility classes that might be added dynamically
  /^theme-/,
  /^dark:/,
  /^light:/,
  /^hover:/,
  /^focus:/,
  /^lg:/,
  /^md:/,
  /^sm:/,
  "dark",
  "light",
  "active",
  "selected",
  // Animation classes
  /^fade-/,
  /^animate-/,
  /^motion-/,
  // State classes
  "is-loading",
  "is-hidden",
  "is-active",
  "no-js",
];

/**
 * Ensure directory exists
 * @param {string} dirPath - Directory path
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * Process CSS with PostCSS plugins
 * @param {string} css - CSS content
 * @param {boolean} isProduction - Whether to run production optimizations
 * @returns {Promise<string>} - Processed CSS
 */
async function processCss(css, isProduction = true) {
  const plugins = [autoprefixer];

  if (isProduction) {
    plugins.push(
      cssnano({
        preset: [
          "advanced",
          {
            discardComments: {
              removeAll: true,
            },
            normalizeWhitespace: true,
            minifyFontValues: true,
            minifyParams: true,
          },
        ],
      })
    );
  }

  const result = await postcss(plugins).process(css, {
    from: undefined,
  });

  return result.css;
}

/**
 * Run PurgeCSS on a CSS file
 * @param {string} cssPath - Path to CSS file
 * @param {string} outputPath - Path to output file
 * @param {Array<string>} contentPaths - Paths to content files
 */
async function purgeCss(cssPath, outputPath, contentPaths) {
  console.log(`Running PurgeCSS on ${cssPath}`);

  try {
    const purgeCSSResult = await new PurgeCSS().purge({
      content: contentPaths,
      css: [cssPath],
      safelist: PURGE_SAFELIST,
      defaultExtractor: (content) => content.match(/[A-Za-z0-9-_:/]+/g) || [],
    });

    if (purgeCSSResult.length > 0) {
      const purgedCss = purgeCSSResult[0].css;
      const processedCss = await processCss(purgedCss, true);
      fs.writeFileSync(outputPath, processedCss);

      const originalSize = fs.statSync(cssPath).size;
      const purgedSize = fs.statSync(outputPath).size;
      const reduction = (((originalSize - purgedSize) / originalSize) * 100).toFixed(2);

      console.log(`Purged CSS: ${cssPath} → ${outputPath}`);
      console.log(
        `Size reduced by ${reduction}% (${originalSize} → ${purgedSize} bytes)`
      );
    }
  } catch (error) {
    console.error(`Error purging CSS ${cssPath}:`, error);
  }
}

/**
 * Extract critical CSS for a page
 * @param {string} pageUrl - URL of the page
 * @param {string} outputPath - Path to output file
 */
async function extractCriticalCss(pageUrl, outputPath) {
  console.log(`Extracting critical CSS for ${pageUrl}`);

  try {
    const result = await critical.generate({
      src: pageUrl,
      target: outputPath,
      inline: false,
      dimensions: [
        { width: 375, height: 667 }, // Mobile
        { width: 768, height: 1024 }, // Tablet
        { width: 1280, height: 800 }, // Desktop
      ],
      penthouse: {
        timeout: 120000,
        renderWaitTime: 500,
      },
    });

    console.log(`Critical CSS extracted for ${pageUrl}: ${outputPath}`);
    return result;
  } catch (error) {
    console.error(`Error extracting critical CSS for ${pageUrl}:`, error);
    return null;
  }
}

/**
 * Create CSS loading strategy
 * @param {string} cssPath - Path to original CSS file
 * @param {string} criticalCssPath - Path to critical CSS
 */
function createCssLoadingStrategy(cssPath, criticalCssPath) {
  const cssFilename = path.basename(cssPath);
  const criticalCssFilename = path.basename(criticalCssPath);

  // Load original CSS asynchronously
  const asyncLoaderScript = `
// Async CSS loader
(function() {
  var stylesheet = document.createElement('link');
  stylesheet.href = '/css/${cssFilename}';
  stylesheet.rel = 'stylesheet';
  stylesheet.type = 'text/css';
  stylesheet.media = 'print';
  stylesheet.onload = function() { this.media = 'all'; };
  document.head.appendChild(stylesheet);
})();
`;

  // Inline critical CSS
  const criticalCss = fs.readFileSync(criticalCssPath, "utf8");
  const inlineStyle = `<style id="critical-css">${criticalCss}</style>`;

  return {
    inlineStyle,
    asyncLoaderScript,
  };
}

/**
 * Main function
 */
async function main() {
  try {
    console.log("Starting critical CSS extraction...");

    // Ensure directories exist
    ensureDir(optimizedCssDir);

    // First, optimize and purge CSS
    for (const cssFile of CSS_FILES) {
      const cssPath = path.join(cssDir, cssFile);
      const outputPath = path.join(optimizedCssDir, cssFile);

      // Content paths for PurgeCSS
      const contentPaths = [
        path.join(siteDir, "**/*.html"),
        path.join(siteDir, "**/*.js"),
      ];

      await purgeCss(cssPath, outputPath, contentPaths);
    }

    // Extract critical CSS for each page template
    for (const template of PAGE_TEMPLATES) {
      const pageUrl = `file://${path.join(siteDir, template.url, "index.html")}`;
      const criticalCssPath = path.join(
        optimizedCssDir,
        "critical-" + template.outputPath
      );

      await extractCriticalCss(pageUrl, criticalCssPath);

      // Create loading strategy
      const mainCssPath = path.join(cssDir, "styles.css");
      const { inlineStyle, asyncLoaderScript } = createCssLoadingStrategy(
        mainCssPath,
        criticalCssPath
      );

      // Save loading strategy for the template
      const strategyOutput = path.join(
        optimizedCssDir,
        `${template.name}-strategy.json`
      );
      fs.writeFileSync(
        strategyOutput,
        JSON.stringify(
          {
            inlineStyle,
            asyncLoaderScript,
          },
          null,
          2
        )
      );

      console.log(`CSS strategy created for ${template.name}`);
    }

    // Create a combined file with all optimizations
    console.log("Creating combined critical CSS...");
    const combinedCriticalCss = PAGE_TEMPLATES.map((template) => {
      const criticalCssPath = path.join(
        optimizedCssDir,
        "critical-" + template.outputPath
      );
      return fs.readFileSync(criticalCssPath, "utf8");
    }).join("\n");

    const combinedPath = path.join(optimizedCssDir, "critical.css");
    const processedCombined = await processCss(combinedCriticalCss, true);
    fs.writeFileSync(combinedPath, processedCombined);

    console.log("Critical CSS extraction complete!");

    // Generate stats
    const statsData = {
      timestamp: new Date().toISOString(),
      templates: PAGE_TEMPLATES.map((template) => template.name),
      cssFiles: CSS_FILES,
      sizeReductions: {},
    };

    for (const cssFile of CSS_FILES) {
      const originalPath = path.join(cssDir, cssFile);
      const optimizedPath = path.join(optimizedCssDir, cssFile);

      if (fs.existsSync(originalPath) && fs.existsSync(optimizedPath)) {
        const originalSize = fs.statSync(originalPath).size;
        const optimizedSize = fs.statSync(optimizedPath).size;
        const reduction = (
          ((originalSize - optimizedSize) / originalSize) *
          100
        ).toFixed(2);

        statsData.sizeReductions[cssFile] = {
          originalSize,
          optimizedSize,
          reduction: `${reduction}%`,
        };
      }
    }

    // Save stats
    fs.writeFileSync(
      path.join(optimizedCssDir, "optimization-stats.json"),
      JSON.stringify(statsData, null, 2)
    );
  } catch (error) {
    console.error("Error during critical CSS extraction:", error);
  }
}

// Run the script
main();
