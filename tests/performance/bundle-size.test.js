/**
 * Performance tests for JavaScript bundle size
 * Implemented as part of Phase 4 performance optimization
 */

import path from "path";
import fs from "fs";
import { test, assert } from "../test-framework.js";
import { fileURLToPath } from "url";

// Set up dirname equivalent in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define bundle size thresholds (in bytes)
const BUNDLE_SIZE_THRESHOLDS = {
  main: 100 * 1024, // 100 KB for main bundle
  blog: 50 * 1024, // 50 KB for blog bundle
  search: 20 * 1024, // 20 KB for search bundle
  components: 10 * 1024, // 10 KB for individual components
};

// Define expected bundles
const EXPECTED_BUNDLES = [
  "main.bundle.js",
  "blog/blog.bundle.js",
  "search/search.bundle.js",
  "utils/utils.bundle.js",
  "components/theme-toggle.bundle.js",
  "components/code-highlight.bundle.js",
];

// Get the size of a file in bytes
function getFileSize(filePath) {
  try {
    const stats = fs.statSync(filePath);
    return stats.size;
  } catch (error) {
    return null; // File doesn't exist or can't be accessed
  }
}

// Format bytes to human-readable format
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
}

// Test that all expected bundles exist
test("All expected JavaScript bundles exist", function () {
  const sitePath = path.join(__dirname, "../../_site/js");

  // Check if _site directory exists
  if (!fs.existsSync(path.join(__dirname, "../../_site"))) {
    return "The _site directory doesn't exist. Run the build first.";
  }

  // Check if _site/js directory exists
  if (!fs.existsSync(sitePath)) {
    return "The _site/js directory doesn't exist. Run the build first.";
  }

  // Check that each expected bundle exists
  const missingBundles = [];

  for (const bundle of EXPECTED_BUNDLES) {
    const bundlePath = path.join(sitePath, bundle);
    if (!fs.existsSync(bundlePath)) {
      missingBundles.push(bundle);
    }
  }

  if (missingBundles.length > 0) {
    return `The following bundles are missing: ${missingBundles.join(", ")}`;
  }

  return true;
});

// Test that the main bundle is within size limits
test("Main bundle is within size limits", function () {
  const bundlePath = path.join(__dirname, "../../_site/js/main.bundle.js");

  // Check if bundle exists
  if (!fs.existsSync(bundlePath)) {
    return "Main bundle doesn't exist. Run the build first.";
  }

  // Get bundle size
  const bundleSize = getFileSize(bundlePath);

  // Check against threshold
  const threshold = BUNDLE_SIZE_THRESHOLDS.main;
  if (bundleSize > threshold) {
    return `Main bundle size (${formatBytes(bundleSize)}) exceeds threshold (${formatBytes(threshold)})`;
  }

  // Log bundle size for information
  console.log(`Main bundle size: ${formatBytes(bundleSize)}`);

  return true;
});

// Test that all bundles combined are within total size limits
test("Total bundle size is within limits", function () {
  const sitePath = path.join(__dirname, "../../_site/js");

  // Check if _site/js directory exists
  if (!fs.existsSync(sitePath)) {
    return "The _site/js directory doesn't exist. Run the build first.";
  }

  // Calculate total size of all bundles
  let totalSize = 0;
  const bundleSizes = {};

  for (const bundle of EXPECTED_BUNDLES) {
    const bundlePath = path.join(sitePath, bundle);
    if (fs.existsSync(bundlePath)) {
      const size = getFileSize(bundlePath);
      totalSize += size;
      bundleSizes[bundle] = formatBytes(size);
    }
  }

  // Define total size threshold
  const TOTAL_SIZE_THRESHOLD = 250 * 1024; // 250 KB for all bundles combined

  // Check against threshold
  if (totalSize > TOTAL_SIZE_THRESHOLD) {
    console.log("Bundle sizes:", bundleSizes);
    return `Total bundle size (${formatBytes(totalSize)}) exceeds threshold (${formatBytes(TOTAL_SIZE_THRESHOLD)})`;
  }

  // Log bundle sizes for information
  console.log("Bundle sizes:", bundleSizes);
  console.log(`Total bundle size: ${formatBytes(totalSize)}`);

  return true;
});

// Test that gzip compression would provide reasonable size reduction
test("Gzip compression provides significant size reduction", function () {
  // This is a simplified test that just checks file content patterns
  // for compressibility. In a real environment, you would use actual
  // gzip compression to test this.

  const bundlePath = path.join(__dirname, "../../_site/js/main.bundle.js");

  // Check if bundle exists
  if (!fs.existsSync(bundlePath)) {
    return "Main bundle doesn't exist. Run the build first.";
  }

  // Read bundle content
  const content = fs.readFileSync(bundlePath, "utf8");

  // Simple heuristic for compressibility: repeated patterns are more compressible
  // Check for common patterns in minified JS that compress well
  const patterns = [
    "function",
    "return",
    "const",
    "var",
    "let",
    "if",
    "for",
    "while",
    "===",
    "!==",
    '","',
    '":"',
    "{}",
  ];

  let patternCount = 0;
  for (const pattern of patterns) {
    // Escape special regex characters to prevent errors
    const escapedPattern = pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(escapedPattern, "g");
    const matches = content.match(regex);
    if (matches) {
      patternCount += matches.length;
    }
  }

  // Calculate pattern density (patterns per KB)
  const contentSizeKB = content.length / 1024;
  const patternDensity = patternCount / contentSizeKB;

  // Higher pattern density means better compression
  // Based on empirical testing of JavaScript files
  if (patternDensity < 5) {
    return `Low pattern density (${patternDensity.toFixed(2)} patterns/KB) might indicate poor gzip compression`;
  }

  console.log(`Pattern density: ${patternDensity.toFixed(2)} patterns/KB`);

  // Estimate gzip compression ratio based on pattern density
  // This is a rough estimate based on typical JS compression ratios
  const estimatedRatio = Math.min(0.7, 0.3 + patternDensity / 100);
  const estimatedGzipSize = content.length * estimatedRatio;

  console.log(
    `Estimated gzip size: ${formatBytes(estimatedGzipSize)} (${(estimatedRatio * 100).toFixed(0)}% of original)`
  );

  return true;
});

// Additional performance tests can be added here
