#!/usr/bin/env node

const lighthouse = require('lighthouse').default || require('lighthouse');
const chromeLauncher = require('chrome-launcher');
const fs = require('fs').promises;
const path = require('path');

// Configuration for Lighthouse audits
const config = {
  extends: 'lighthouse:default',
  settings: {
    onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
    formFactor: 'desktop',
    throttling: {
      rttMs: 40,
      throughputKbps: 10240,
      cpuSlowdownMultiplier: 1,
      requestLatencyMs: 0,
      downloadThroughputKbps: 0,
      uploadThroughputKbps: 0
    },
    screenEmulation: {
      mobile: false,
      width: 1350,
      height: 940,
      deviceScaleFactor: 1,
      disabled: false
    },
    emulatedUserAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  }
};

// Pages to audit
const testPages = [
  {
    name: 'Homepage',
    url: 'http://localhost:8080',
    description: 'Main landing page with navigation and hero content'
  },
  {
    name: 'Blog Post',
    url: 'http://localhost:8080/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/',
    description: 'Individual blog post with rich content'
  },
  {
    name: 'About Page',
    url: 'http://localhost:8080/about/',
    description: 'About page with personal information'
  }
];

// Key metrics to track for UI/UX scoring
const uiUxMetrics = [
  'tap-targets',
  'color-contrast',
  'focus-visible',
  'focusable-controls',
  'interactive-element-affordance',
  'logical-tab-order',
  'managed-focus',
  'offscreen-content-hidden',
  'use-landmarks',
  'bypass',
  'heading-order',
  'link-name',
  'button-name',
  'form-field-multiple-labels',
  'label',
  'input-image-alt',
  'image-alt',
  'document-title',
  'html-has-lang',
  'valid-lang',
  'aria-allowed-attr',
  'aria-hidden-body',
  'aria-hidden-focus',
  'aria-input-field-name',
  'aria-meter-name',
  'aria-progressbar-name',
  'aria-required-attr',
  'aria-required-children',
  'aria-required-parent',
  'aria-roles',
  'aria-toggle-field-name',
  'aria-tooltip-name',
  'aria-valid-attr-value',
  'aria-valid-attr'
];

async function runLighthouseAudit(url, pageName) {
  console.log(`\n🔍 Starting Lighthouse audit for ${pageName}...`);
  console.log(`URL: ${url}`);

  const chrome = await chromeLauncher.launch({
    chromeFlags: ['--headless', '--disable-gpu', '--no-sandbox']
  });

  try {
    const options = {
      logLevel: 'info',
      output: 'json',
      onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
      port: chrome.port
    };

    const runnerResult = await lighthouse(url, options, config);

    if (!runnerResult || !runnerResult.lhr) {
      throw new Error(`Failed to get valid results for ${pageName}`);
    }

    const { lhr } = runnerResult;

    // Extract category scores
    const scores = {
      performance: Math.round(lhr.categories.performance.score * 100),
      accessibility: Math.round(lhr.categories.accessibility.score * 100),
      bestPractices: Math.round(lhr.categories['best-practices'].score * 100),
      seo: Math.round(lhr.categories.seo.score * 100)
    };

    // Calculate overall UI/UX score (weighted average with emphasis on accessibility)
    const uiUxScore = Math.round(
      (scores.accessibility * 0.4 +
       scores.bestPractices * 0.3 +
       scores.performance * 0.2 +
       scores.seo * 0.1)
    );

    // Extract specific UI/UX audit results
    const uiUxAudits = {};
    uiUxMetrics.forEach(metric => {
      if (lhr.audits[metric]) {
        uiUxAudits[metric] = {
          score: lhr.audits[metric].score,
          displayValue: lhr.audits[metric].displayValue || '',
          description: lhr.audits[metric].description,
          details: lhr.audits[metric].details || null
        };
      }
    });

    // Extract key performance metrics
    const performanceMetrics = {
      firstContentfulPaint: lhr.audits['first-contentful-paint']?.displayValue || 'N/A',
      largestContentfulPaint: lhr.audits['largest-contentful-paint']?.displayValue || 'N/A',
      cumulativeLayoutShift: lhr.audits['cumulative-layout-shift']?.displayValue || 'N/A',
      totalBlockingTime: lhr.audits['total-blocking-time']?.displayValue || 'N/A',
      speedIndex: lhr.audits['speed-index']?.displayValue || 'N/A'
    };

    // Save detailed results
    const results = {
      page: pageName,
      url: url,
      timestamp: new Date().toISOString(),
      scores: scores,
      uiUxScore: uiUxScore,
      performanceMetrics: performanceMetrics,
      uiUxAudits: uiUxAudits,
      rawReport: lhr
    };

    // Save to file
    const filename = `lighthouse-${pageName.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}.json`;
    const filepath = path.join(__dirname, '..', 'docs', filename);
    await fs.writeFile(filepath, JSON.stringify(results, null, 2));

    console.log(`✅ Audit completed for ${pageName}`);
    console.log(`📊 Scores: Performance: ${scores.performance}, Accessibility: ${scores.accessibility}, Best Practices: ${scores.bestPractices}, SEO: ${scores.seo}`);
    console.log(`🎯 UI/UX Score: ${uiUxScore}/100`);
    console.log(`💾 Detailed results saved to: ${filepath}`);

    return results;

  } catch (error) {
    console.error(`❌ Error auditing ${pageName}:`, error.message);
    return null;
  } finally {
    await chrome.kill();
  }
}

async function generateComprehensiveReport(allResults) {
  console.log('\n📋 Generating comprehensive report...');

  const report = `# Lighthouse Audit Results - ${new Date().toLocaleDateString()}

## Executive Summary

${allResults.map(result => {
  if (!result) return '';

  const status = result.uiUxScore >= 90 ? '✅ PASSED' : result.uiUxScore >= 80 ? '⚠️ NEEDS IMPROVEMENT' : '❌ FAILED';
  return `**${result.page}**: ${status} (${result.uiUxScore}/100 UI/UX Score)`;
}).filter(Boolean).join('\n')}

### Overall Assessment
${allResults.every(r => r && r.uiUxScore >= 90) ?
  '🎉 **CONGRATULATIONS!** All pages have achieved the 90+ UI/UX score target!' :
  '⚠️ Some pages need additional optimization to reach the 90+ target.'
}

## Detailed Results by Page

${allResults.map(result => {
  if (!result) return '';

  return `### ${result.page}
**URL**: ${result.url}
**Audit Date**: ${new Date(result.timestamp).toLocaleString()}

#### Category Scores
- **Performance**: ${result.scores.performance}/100
- **Accessibility**: ${result.scores.accessibility}/100
- **Best Practices**: ${result.scores.bestPractices}/100
- **SEO**: ${result.scores.seo}/100
- **Overall UI/UX**: ${result.uiUxScore}/100

#### Performance Metrics
- **First Contentful Paint**: ${result.performanceMetrics.firstContentfulPaint}
- **Largest Contentful Paint**: ${result.performanceMetrics.largestContentfulPaint}
- **Cumulative Layout Shift**: ${result.performanceMetrics.cumulativeLayoutShift}
- **Total Blocking Time**: ${result.performanceMetrics.totalBlockingTime}
- **Speed Index**: ${result.performanceMetrics.speedIndex}

#### Key UI/UX Audit Results
${Object.entries(result.uiUxAudits)
  .filter(([key, audit]) => audit.score !== null && audit.score < 1)
  .map(([key, audit]) => `- **${key}**: ${audit.score === 0 ? '❌ Failed' : '⚠️ Partial'} - ${audit.description}`)
  .join('\n') || '✅ All UI/UX audits passed!'}

---
`;
}).filter(Boolean).join('\n')}

## Touch Target Analysis
${allResults.map(result => {
  if (!result || !result.uiUxAudits['tap-targets']) return '';

  const tapTargets = result.uiUxAudits['tap-targets'];
  if (tapTargets.score === 1) {
    return `**${result.page}**: ✅ All touch targets are appropriately sized`;
  } else {
    const details = tapTargets.details;
    const violationCount = details?.items?.length || 0;
    return `**${result.page}**: ⚠️ ${violationCount} touch target violations found`;
  }
}).filter(Boolean).join('\n')}

## Color Contrast Analysis
${allResults.map(result => {
  if (!result || !result.uiUxAudits['color-contrast']) return '';

  const contrast = result.uiUxAudits['color-contrast'];
  if (contrast.score === 1) {
    return `**${result.page}**: ✅ All text has sufficient color contrast`;
  } else {
    const details = contrast.details;
    const violationCount = details?.items?.length || 0;
    return `**${result.page}**: ⚠️ ${violationCount} color contrast violations found`;
  }
}).filter(Boolean).join('\n')}

## Focus Management Analysis
${allResults.map(result => {
  if (!result) return '';

  const focusVisible = result.uiUxAudits['focus-visible'];
  const logicalTabOrder = result.uiUxAudits['logical-tab-order'];
  const managedFocus = result.uiUxAudits['managed-focus'];

  const focusIssues = [];
  if (focusVisible && focusVisible.score < 1) focusIssues.push('Focus visibility');
  if (logicalTabOrder && logicalTabOrder.score < 1) focusIssues.push('Tab order');
  if (managedFocus && managedFocus.score < 1) focusIssues.push('Focus management');

  if (focusIssues.length === 0) {
    return `**${result.page}**: ✅ All focus management requirements met`;
  } else {
    return `**${result.page}**: ⚠️ Issues found: ${focusIssues.join(', ')}`;
  }
}).filter(Boolean).join('\n')}

## Recommendations

### Immediate Actions Needed
${allResults.some(r => r && r.uiUxScore < 90) ? `
- Review and fix touch target sizing issues
- Improve color contrast ratios where needed
- Enhance focus visibility and keyboard navigation
- Optimize accessibility attributes and ARIA labels
` : '✅ No immediate actions needed - all targets met!'}

### Performance Optimizations
- Monitor Core Web Vitals metrics
- Optimize image loading and sizing
- Review JavaScript bundles for efficiency
- Implement proper caching strategies

### Accessibility Enhancements
- Regular screen reader testing
- Keyboard navigation verification
- Color contrast monitoring
- ARIA attribute validation

## Summary Statistics

**Total Pages Audited**: ${allResults.filter(Boolean).length}
**Pages Meeting 90+ Target**: ${allResults.filter(r => r && r.uiUxScore >= 90).length}
**Average UI/UX Score**: ${Math.round(allResults.filter(Boolean).reduce((sum, r) => sum + r.uiUxScore, 0) / allResults.filter(Boolean).length)}/100

**Target Achievement**: ${allResults.every(r => r && r.uiUxScore >= 90) ? '✅ ACHIEVED' : '⚠️ IN PROGRESS'}

---
*Report generated on ${new Date().toLocaleString()} using Lighthouse CI*
`;

  const reportPath = path.join(__dirname, '..', 'docs', `lighthouse-comprehensive-report-${Date.now()}.md`);
  await fs.writeFile(reportPath, report);

  console.log(`📄 Comprehensive report saved to: ${reportPath}`);
  return report;
}

async function main() {
  console.log('🚀 Starting Comprehensive Lighthouse Audit');
  console.log('==========================================');

  try {
    // Ensure docs directory exists
    const docsDir = path.join(__dirname, '..', 'docs');
    await fs.mkdir(docsDir, { recursive: true });

    // Run audits for all pages
    const results = [];
    for (const page of testPages) {
      const result = await runLighthouseAudit(page.url, page.name);
      results.push(result);

      // Wait between audits to avoid overwhelming the server
      if (results.length < testPages.length) {
        console.log('⏳ Waiting 3 seconds before next audit...');
        await new Promise(resolve => setTimeout(resolve, 3000));
      }
    }

    // Generate comprehensive report
    const report = await generateComprehensiveReport(results);

    console.log('\n🎯 AUDIT SUMMARY');
    console.log('================');

    results.forEach(result => {
      if (result) {
        const status = result.uiUxScore >= 90 ? '✅' : result.uiUxScore >= 80 ? '⚠️' : '❌';
        console.log(`${status} ${result.page}: ${result.uiUxScore}/100 UI/UX Score`);
      }
    });

    const averageScore = Math.round(
      results.filter(Boolean).reduce((sum, r) => sum + r.uiUxScore, 0) /
      results.filter(Boolean).length
    );

    console.log(`\n📊 Average UI/UX Score: ${averageScore}/100`);
    console.log(`🎯 90+ Target: ${results.every(r => r && r.uiUxScore >= 90) ? 'ACHIEVED ✅' : 'IN PROGRESS ⚠️'}`);

    // Display report preview
    console.log('\n📋 REPORT PREVIEW');
    console.log('=================');
    console.log(report.split('\n').slice(0, 20).join('\n'));
    console.log('\n... (full report saved to file) ...');

  } catch (error) {
    console.error('❌ Error running lighthouse audits:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { runLighthouseAudit, generateComprehensiveReport };