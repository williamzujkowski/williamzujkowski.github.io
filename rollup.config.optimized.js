/**
 * Optimized Rollup configuration for improved JavaScript bundling
 */

import { nodeResolve } from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import terser from "@rollup/plugin-terser";
import { visualizer } from "rollup-plugin-visualizer";

// Check if we're in production mode based on environment
const isProduction = process.env.NODE_ENV === "production";

// Check if we're in analyze mode
const isAnalyze = process.env.ANALYZE === "true";

// Terser options for better minification
const terserOptions = {
  compress: {
    passes: 2,
    drop_console: isProduction,
    drop_debugger: isProduction,
    pure_getters: true,
    unsafe: true,
    unsafe_comps: true,
    unsafe_math: true,
    unsafe_methods: true,
  },
  mangle: {
    properties: {
      regex: /^_/,
    },
  },
  output: {
    comments: false,
  },
};

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
  isProduction && terser(terserOptions),
  // Generate bundle visualization in analyze mode
  isAnalyze &&
    visualizer({
      filename: "build-analysis.html",
      open: true,
      gzipSize: true,
      brotliSize: true,
      template: "treemap", // Use treemap for better visualization
    }),
].filter(Boolean);

// Define bundle destinations
const DIST_DIR = "_site/js";

// Configure different bundle outputs
export default [
  // Core bundle - contains core functionality and utilities
  // This will be loaded on all pages
  {
    input: "src/js/main.js",
    output: {
      dir: DIST_DIR,
      entryFileNames: "core.[hash].js",
      format: "es", // Use ES modules for better tree-shaking
      sourcemap: !isProduction,
      manualChunks: {
        // Extract vendor code into a separate chunk
        vendor: [
          // Add any large third-party dependencies here
        ],
        // Utils that are used across multiple bundles
        utils: ["src/js/theme-utils.js"],
      },
      chunkFileNames: (chunkInfo) => {
        if (chunkInfo.name === "vendor") {
          return "vendor.[hash].js";
        }
        return "[name].[hash].js";
      },
    },
    plugins: commonPlugins,
  },

  // Page-specific bundles
  // Blog bundle - contains all blog-specific functionality
  {
    input: "src/js/blog-search.js",
    output: {
      dir: `${DIST_DIR}/pages`,
      entryFileNames: "blog.[hash].js",
      format: "es",
      sourcemap: !isProduction,
      // Use imports field to declare dynamic imports
      // that should be loaded only when needed
      inlineDynamicImports: false,
    },
    plugins: commonPlugins,
    // Use external to avoid duplicating code in both bundles
    external: (id) => id.includes("theme-utils.js"),
  },

  // Component bundles - these are loaded on demand
  {
    input: {
      "theme-toggle": "src/js/components/theme-toggle.js",
      "code-highlight": "src/js/components/code-highlight.js",
    },
    output: {
      dir: `${DIST_DIR}/components`,
      entryFileNames: "[name].[hash].js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: commonPlugins,
    // Use external to avoid duplicating code in both bundles
    external: (id) => id.includes("theme-utils.js"),
  },

  // Critical CSS inlining helper
  {
    input: "src/js/critical-css.js",
    output: {
      file: `${DIST_DIR}/critical-css.js`,
      format: "es",
      sourcemap: false,
    },
    plugins: commonPlugins,
  },
];
