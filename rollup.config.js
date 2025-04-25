/**
 * Rollup configuration for bundling JavaScript
 * Part of the Phase 4 performance optimization implementation
 */

import { nodeResolve } from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import terser from "@rollup/plugin-terser";
import { visualizer } from "rollup-plugin-visualizer";

// Check if we're in production mode based on environment
const isProduction = process.env.NODE_ENV === "production";

// Check if we're in analyze mode
const isAnalyze = process.env.ANALYZE === "true";

// Common plugins used in all bundles
const commonPlugins = [
  // Resolve node modules
  nodeResolve({
    browser: true,
    preferBuiltins: false,
  }),
  // Convert CommonJS modules to ES6
  commonjs({
    include: "node_modules/**",
  }),
  // Minify in production only
  isProduction &&
    terser({
      compress: {
        drop_console: isProduction,
        drop_debugger: isProduction,
      },
      output: {
        comments: false,
      },
    }),
  // Generate bundle visualization in analyze mode
  isAnalyze &&
    visualizer({
      filename: "build-analysis.html",
      open: true,
      gzipSize: true,
      brotliSize: true,
    }),
].filter(Boolean);

// Configure different bundle outputs
export default [
  // Main bundle - critical path rendering
  {
    input: "src/js/main.js",
    output: {
      file: "_site/js/main.bundle.js", // Use file instead of dir for IIFE format
      format: "iife", // Use IIFE format instead of ES modules for browser compatibility
      sourcemap: !isProduction,
      name: "main", // Global variable name for IIFE
    },
    plugins: commonPlugins,
    // Explicitly mark certain imports as external to prevent warnings
    external: [
      "/js/components/joke-generator.bundle.js",
      "../../js/components/joke-generator.bundle.js",
    ],
  },

  // Blog-specific functionality
  {
    input: "src/js/blog-search.js",
    output: {
      file: "_site/js/blog/blog.bundle.js",
      format: "iife", // Use IIFE format instead of ES modules
      sourcemap: !isProduction,
      name: "blogSearch",
    },
    plugins: commonPlugins,
  },

  // Search functionality (for non-blog pages)
  {
    input: "src/js/search.js",
    output: {
      file: "_site/js/search/search.bundle.js",
      format: "iife", // Use IIFE format instead of ES modules
      sourcemap: !isProduction,
      name: "search",
    },
    plugins: commonPlugins,
  },

  // Component bundles
  {
    input: "src/js/components/theme-toggle.js",
    output: {
      file: "_site/js/components/theme-toggle.bundle.js",
      format: "iife", // Use IIFE format instead of ES modules
      sourcemap: !isProduction,
      name: "themeToggle",
    },
    plugins: commonPlugins,
  },

  // Optional components - code highlighting
  {
    input: "src/js/components/code-highlight.js",
    output: {
      file: "_site/js/components/code-highlight.bundle.js",
      format: "iife", // Use IIFE format instead of ES modules
      sourcemap: !isProduction,
      name: "codeHighlight",
    },
    plugins: commonPlugins,
  },

  // Utils bundle - utility functions
  {
    input: "src/js/theme-utils.js",
    output: {
      file: "_site/js/utils/utils.bundle.js",
      format: "iife", // Use IIFE format instead of ES modules
      sourcemap: !isProduction,
      name: "themeUtils",
    },
    plugins: commonPlugins,
  },

  // Special bundle for joke generator - copy from existing file to target location
  {
    input: "js/components/joke-generator.bundle.js",
    output: {
      file: "_site/js/components/joke-generator.bundle.js",
      format: "iife",
      sourcemap: false,
      name: "jokeGenerator",
    },
    plugins: commonPlugins,
  },
];
