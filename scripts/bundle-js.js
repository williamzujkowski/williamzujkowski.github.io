#!/usr/bin/env node

/**
 * JavaScript Bundling and Minification Script
 * Bundles and minifies JavaScript files for optimal performance
 */

const fs = require('fs');
const path = require('path');
const { minify } = require('terser');

const srcDir = path.join(__dirname, '..', 'src', 'assets', 'js');
const distDir = path.join(__dirname, '..', '_site', 'assets', 'js');

// Define bundles
const bundles = {
  // Core bundle - loaded on all pages
  'core.min.js': [
    'ui-enhancements.js',
    'back-to-top.js',
    'code-collapse.js'
  ],
  // Blog bundle - loaded on blog posts
  'blog.min.js': [
    'reading-progress.js',
    'table-of-contents.js'
  ],
  // Search bundle - loaded on posts listing
  'search.min.js': [
    'search.js'
  ]
};

async function bundleAndMinify() {
  console.log('Starting JavaScript bundling and minification...');

  // Ensure dist directory exists
  if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
  }

  let totalOriginalSize = 0;
  let totalMinifiedSize = 0;

  for (const [bundleName, files] of Object.entries(bundles)) {
    console.log(`\nCreating bundle: ${bundleName}`);

    let bundleContent = '';
    let bundleOriginalSize = 0;

    // Concatenate files
    for (const file of files) {
      const filePath = path.join(srcDir, file);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        bundleContent += `\n// Source: ${file}\n${content}\n`;
        bundleOriginalSize += content.length;
        console.log(`  - Added ${file} (${(content.length / 1024).toFixed(2)} KB)`);
      } else {
        console.warn(`  ⚠ Warning: ${file} not found`);
      }
    }

    totalOriginalSize += bundleOriginalSize;

    try {
      // Minify the bundle
      const result = await minify(bundleContent, {
        compress: {
          drop_console: false, // Keep console.logs for debugging
          drop_debugger: true,
          passes: 2
        },
        mangle: {
          safari10: true // Fix for Safari 10 issues
        },
        format: {
          comments: false
        }
      });

      if (result.code) {
        // Write minified bundle
        const outputPath = path.join(distDir, bundleName);
        fs.writeFileSync(outputPath, result.code);
        totalMinifiedSize += result.code.length;

        const reduction = ((1 - result.code.length / bundleOriginalSize) * 100).toFixed(1);
        console.log(`  ✓ Minified: ${(bundleOriginalSize / 1024).toFixed(2)} KB → ${(result.code.length / 1024).toFixed(2)} KB (${reduction}% reduction)`);
      }
    } catch (error) {
      console.error(`  ✗ Error minifying ${bundleName}:`, error);
    }
  }

  // Also copy original files for fallback
  console.log('\nCopying original files as fallback...');
  const jsFiles = fs.readdirSync(srcDir).filter(f => f.endsWith('.js'));
  for (const file of jsFiles) {
    const srcPath = path.join(srcDir, file);
    const destPath = path.join(distDir, file);
    fs.copyFileSync(srcPath, destPath);
  }

  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('Summary:');
  console.log(`Total original size: ${(totalOriginalSize / 1024).toFixed(2)} KB`);
  console.log(`Total minified size: ${(totalMinifiedSize / 1024).toFixed(2)} KB`);
  console.log(`Overall reduction: ${((1 - totalMinifiedSize / totalOriginalSize) * 100).toFixed(1)}%`);
  console.log('='.repeat(50));
}

// Run if executed directly
if (require.main === module) {
  bundleAndMinify().catch(console.error);
}

module.exports = { bundleAndMinify };