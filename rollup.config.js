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
      dir: "_site/js",
      entryFileNames: "[name].bundle.js",
      chunkFileNames: "chunks/[name]-[hash].js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: commonPlugins,
  },

  // Blog-specific functionality
  {
    input: "src/js/blog-search.js",
    output: {
      dir: "_site/js/blog",
      entryFileNames: "blog.bundle.js",
      chunkFileNames: "../chunks/[name]-[hash].js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: commonPlugins,
  },

  // Search functionality (for non-blog pages)
  {
    input: "src/js/search.js",
    output: {
      dir: "_site/js/search",
      entryFileNames: "search.bundle.js",
      chunkFileNames: "../chunks/[name]-[hash].js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: commonPlugins,
  },

  // Component bundles
  {
    input: "src/js/components/theme-toggle.js",
    output: {
      dir: "_site/js/components",
      entryFileNames: "theme-toggle.bundle.js",
      chunkFileNames: "../chunks/[name]-[hash].js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: commonPlugins,
  },

  // Optional components - code highlighting
  {
    input: "src/js/components/code-highlight.js",
    output: {
      dir: "_site/js/components",
      entryFileNames: "code-highlight.bundle.js",
      chunkFileNames: "../chunks/[name]-[hash].js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: commonPlugins,
  },

  // Utils bundle - utility functions
  {
    input: "src/js/theme-utils.js",
    output: {
      dir: "_site/js/utils",
      entryFileNames: "utils.bundle.js",
      chunkFileNames: "../chunks/[name]-[hash].js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: commonPlugins,
  },
];
