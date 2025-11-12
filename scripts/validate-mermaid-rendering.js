const { chromium } = require('@playwright/test');
const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

const BASE_URL = 'http://localhost:8080';
const POSTS_DIR = path.join(__dirname, '..', 'src', 'posts');
const TIMEOUT_MS = 30000;

/**
 * Find all posts with Mermaid diagrams
 * @returns {Promise<Array<{file: string, slug: string, diagramCount: number}>>}
 */
async function findMermaidPosts() {
  try {
    // Find all markdown files containing 'mermaid'
    const grepResult = execSync(
      `grep -l "mermaid" ${POSTS_DIR}/*.md`,
      { encoding: 'utf-8' }
    ).trim();

    const files = grepResult.split('\n').filter(Boolean);
    const posts = [];

    for (const file of files) {
      // Extract slug from filename (remove date prefix and .md extension)
      const basename = path.basename(file, '.md');
      const slug = basename.replace(/^\d{4}-\d{2}-\d{2}-/, '');

      // Count mermaid diagrams
      const content = await fs.readFile(file, 'utf-8');
      const diagramCount = (content.match(/```mermaid/g) || []).length;

      posts.push({
        file: basename,
        slug,
        diagramCount
      });
    }

    return posts.sort((a, b) => a.slug.localeCompare(b.slug));
  } catch (error) {
    if (error.status === 1) {
      // grep returns exit code 1 when no matches found
      return [];
    }
    throw error;
  }
}

/**
 * Validate Mermaid rendering on a single post
 * @param {import('@playwright/test').Page} page
 * @param {string} slug
 * @param {number} expectedDiagrams
 * @returns {Promise<{success: boolean, rendered: number, expected: number, errors: string[], warnings: string[]}>}
 */
async function validatePost(page, slug, expectedDiagrams) {
  const url = `${BASE_URL}/posts/${slug}/`;
  const errors = [];
  const warnings = [];

  try {
    // Collect console messages
    const consoleMessages = [];
    page.on('console', msg => {
      const text = msg.text();
      consoleMessages.push({
        type: msg.type(),
        text
      });

      // Check for mermaid-specific errors
      if (text.toLowerCase().includes('mermaid') && msg.type() === 'error') {
        errors.push(`Console error: ${text}`);
      }

      // Check for v9 deprecation warnings
      if (text.includes('subgraph') && text.includes('requires')) {
        warnings.push(`Mermaid v9 syntax detected: ${text}`);
      }
    });

    // Collect page errors
    page.on('pageerror', error => {
      errors.push(`Page error: ${error.message}`);
    });

    // Navigate to post
    await page.goto(url, {
      waitUntil: 'networkidle',
      timeout: TIMEOUT_MS
    });

    // Wait for mermaid to render (mermaid.js adds SVG elements)
    await page.waitForTimeout(2000);

    // Evaluate page for mermaid elements
    const result = await page.evaluate(() => {
      const mermaidContainers = document.querySelectorAll('.mermaid, [data-mermaid]');
      const svgElements = document.querySelectorAll('.mermaid svg, [data-mermaid] svg');

      // Check for rendering errors in mermaid containers
      const renderErrors = [];
      mermaidContainers.forEach((container, index) => {
        const svg = container.querySelector('svg');
        if (!svg) {
          renderErrors.push(`Diagram ${index + 1}: No SVG rendered`);
        } else if (svg.querySelector('text[data-error]')) {
          const errorText = svg.querySelector('text[data-error]').textContent;
          renderErrors.push(`Diagram ${index + 1}: ${errorText}`);
        }
      });

      return {
        totalContainers: mermaidContainers.length,
        renderedSVGs: svgElements.length,
        renderErrors,
        documentWidth: document.documentElement.scrollWidth,
        viewportWidth: window.innerWidth
      };
    });

    // Check if diagram count matches
    if (result.renderedSVGs !== expectedDiagrams) {
      warnings.push(
        `Diagram count mismatch: expected ${expectedDiagrams}, rendered ${result.renderedSVGs}`
      );
    }

    // Check for horizontal scroll (potential layout issue)
    if (result.documentWidth > result.viewportWidth + 10) {
      warnings.push(
        `Horizontal scroll detected (${result.documentWidth}px > ${result.viewportWidth}px)`
      );
    }

    // Add render errors from DOM
    errors.push(...result.renderErrors);

    return {
      success: errors.length === 0,
      rendered: result.renderedSVGs,
      expected: expectedDiagrams,
      errors,
      warnings,
      consoleMessages: consoleMessages.filter(m => m.type === 'error')
    };

  } catch (error) {
    return {
      success: false,
      rendered: 0,
      expected: expectedDiagrams,
      errors: [`Navigation/timeout error: ${error.message}`],
      warnings,
      consoleMessages: []
    };
  }
}

/**
 * Generate console report
 * @param {Array} results
 */
function printReport(results) {
  console.log('\n' + '='.repeat(80));
  console.log('🔍 MERMAID RENDERING VALIDATION REPORT');
  console.log('='.repeat(80) + '\n');

  const passed = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);
  const withWarnings = results.filter(r => r.warnings.length > 0);

  // Summary statistics
  console.log('📊 SUMMARY');
  console.log(`   Total posts: ${results.length}`);
  console.log(`   ✅ Passed: ${passed.length} (${Math.round(passed.length / results.length * 100)}%)`);
  console.log(`   ❌ Failed: ${failed.length}`);
  console.log(`   ⚠️  With warnings: ${withWarnings.length}\n`);

  // Individual results
  console.log('📋 DETAILED RESULTS\n');

  results.forEach(result => {
    const icon = result.success ? '✅' : '❌';
    const diagrams = `${result.rendered}/${result.expected} diagrams`;

    console.log(`${icon} ${result.slug}`);
    console.log(`   ${diagrams}`);

    if (result.errors.length > 0) {
      console.log('   Errors:');
      result.errors.forEach(err => console.log(`     • ${err}`));
    }

    if (result.warnings.length > 0) {
      console.log('   Warnings:');
      result.warnings.forEach(warn => console.log(`     ⚠️  ${warn}`));
    }

    console.log('');
  });

  // Failed posts list
  if (failed.length > 0) {
    console.log('\n' + '='.repeat(80));
    console.log('❌ FAILED POSTS REQUIRING ATTENTION');
    console.log('='.repeat(80) + '\n');

    failed.forEach(result => {
      console.log(`• ${result.slug}`);
      result.errors.forEach(err => console.log(`    - ${err}`));
    });
    console.log('');
  }

  // Warning summary
  if (withWarnings.length > 0) {
    console.log('\n' + '='.repeat(80));
    console.log('⚠️  POSTS WITH WARNINGS');
    console.log('='.repeat(80) + '\n');

    withWarnings.forEach(result => {
      console.log(`• ${result.slug}`);
      result.warnings.forEach(warn => console.log(`    - ${warn}`));
    });
    console.log('');
  }
}

/**
 * Main validation function
 */
async function validateMermaidRendering() {
  console.log('🔍 Finding posts with Mermaid diagrams...\n');

  // Find all posts with mermaid
  const posts = await findMermaidPosts();

  if (posts.length === 0) {
    console.log('❌ No posts with Mermaid diagrams found!');
    process.exit(1);
  }

  console.log(`📝 Found ${posts.length} posts with Mermaid diagrams\n`);
  console.log('🌐 Starting browser validation...\n');

  // Check if server is running
  try {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
  } catch (error) {
    console.error(`❌ Cannot connect to ${BASE_URL}`);
    console.error('   Please start the development server: npm start');
    process.exit(1);
  }

  const browser = await chromium.launch({
    headless: true,
    timeout: TIMEOUT_MS
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();
  const results = [];

  // Validate each post
  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const progress = `[${i + 1}/${posts.length}]`;

    process.stdout.write(`${progress} Validating ${post.slug}...`);

    const result = await validatePost(page, post.slug, post.diagramCount);
    results.push({
      slug: post.slug,
      file: post.file,
      ...result
    });

    const status = result.success ? '✅' : '❌';
    console.log(` ${status}`);
  }

  await browser.close();

  // Save detailed JSON report
  const reportPath = path.join(__dirname, '..', 'mermaid-validation-report.json');
  await fs.writeFile(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalPosts: posts.length,
    passed: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    results
  }, null, 2));

  // Print console report
  printReport(results);

  console.log(`📄 Detailed report saved to: ${reportPath}\n`);

  // Exit with appropriate code
  const hasFailures = results.some(r => !r.success);
  process.exit(hasFailures ? 1 : 0);
}

// Run validation
validateMermaidRendering().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
