#!/usr/bin/env node

const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

// Pages to audit
const testPages = [
  {
    name: 'Homepage',
    url: 'http://localhost:8080',
    description: 'Main landing page'
  },
  {
    name: 'Blog-Post',
    url: 'http://localhost:8080/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/',
    description: 'Individual blog post'
  },
  {
    name: 'About-Page',
    url: 'http://localhost:8080/about/',
    description: 'About page'
  }
];

async function runLighthouseAudit(page) {
  return new Promise((resolve, reject) => {
    console.log(`\n🔍 Running Lighthouse audit for ${page.name}...`);
    console.log(`URL: ${page.url}`);

    const outputPath = path.join(__dirname, '..', 'docs', `lighthouse-${page.name.toLowerCase()}-${Date.now()}.json`);

    const lighthouse = spawn('npx', [
      'lighthouse',
      page.url,
      '--output=json',
      `--output-path=${outputPath}`,
      '--chrome-flags=--headless',
      '--quiet',
      '--only-categories=performance,accessibility,best-practices,seo'
    ]);

    let output = '';
    let errorOutput = '';

    lighthouse.stdout.on('data', (data) => {
      output += data.toString();
    });

    lighthouse.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    lighthouse.on('close', async (code) => {
      if (code === 0) {
        try {
          // Read the generated report
          const reportData = await fs.readFile(outputPath, 'utf8');
          const report = JSON.parse(reportData);

          // Extract scores
          const scores = {
            performance: Math.round(report.categories.performance.score * 100),
            accessibility: Math.round(report.categories.accessibility.score * 100),
            bestPractices: Math.round(report.categories['best-practices'].score * 100),
            seo: Math.round(report.categories.seo.score * 100)
          };

          // Calculate UI/UX score (weighted average)
          const uiUxScore = Math.round(
            (scores.accessibility * 0.4 +
             scores.bestPractices * 0.3 +
             scores.performance * 0.2 +
             scores.seo * 0.1)
          );

          // Extract key audit results
          const keyAudits = {
            tapTargets: report.audits['tap-targets'],
            colorContrast: report.audits['color-contrast'],
            focusVisible: report.audits['focus-visible'],
            logicalTabOrder: report.audits['logical-tab-order'],
            managedFocus: report.audits['managed-focus']
          };

          // Performance metrics
          const performanceMetrics = {
            firstContentfulPaint: report.audits['first-contentful-paint']?.displayValue || 'N/A',
            largestContentfulPaint: report.audits['largest-contentful-paint']?.displayValue || 'N/A',
            cumulativeLayoutShift: report.audits['cumulative-layout-shift']?.displayValue || 'N/A',
            totalBlockingTime: report.audits['total-blocking-time']?.displayValue || 'N/A',
            speedIndex: report.audits['speed-index']?.displayValue || 'N/A'
          };

          const result = {
            page: page.name,
            url: page.url,
            scores,
            uiUxScore,
            performanceMetrics,
            keyAudits,
            reportPath: outputPath
          };

          console.log(`✅ Audit completed for ${page.name}`);
          console.log(`📊 Performance: ${scores.performance}, Accessibility: ${scores.accessibility}, Best Practices: ${scores.bestPractices}, SEO: ${scores.seo}`);
          console.log(`🎯 UI/UX Score: ${uiUxScore}/100`);

          resolve(result);
        } catch (error) {
          console.error(`❌ Error parsing report for ${page.name}:`, error.message);
          reject(error);
        }
      } else {
        console.error(`❌ Lighthouse failed for ${page.name} with code ${code}`);
        console.error('Error output:', errorOutput);
        reject(new Error(`Lighthouse process exited with code ${code}`));
      }
    });
  });
}

async function generateReport(results) {
  const report = `# Lighthouse Audit Results - ${new Date().toLocaleDateString()}

## 🎯 Executive Summary

${results.map(result => {
  const status = result.uiUxScore >= 90 ? '✅ ACHIEVED' : result.uiUxScore >= 80 ? '⚠️ CLOSE' : '❌ NEEDS WORK';
  return `**${result.page}**: ${status} (${result.uiUxScore}/100 UI/UX Score)`;
}).join('\n')}

### Overall Assessment
${results.every(r => r.uiUxScore >= 90) ?
  '🎉 **CONGRATULATIONS!** All pages have achieved the 90+ UI/UX score target!' :
  `⚠️ Average Score: ${Math.round(results.reduce((sum, r) => sum + r.uiUxScore, 0) / results.length)}/100 - Some optimization needed to reach 90+ target.`
}

## 📊 Detailed Results

${results.map(result => `
### ${result.page}
**URL**: ${result.url}

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
- **Touch Targets**: ${result.keyAudits.tapTargets?.score === 1 ? '✅ Passed' : `❌ Failed (${result.keyAudits.tapTargets?.details?.items?.length || 0} issues)`}
- **Color Contrast**: ${result.keyAudits.colorContrast?.score === 1 ? '✅ Passed' : `❌ Failed (${result.keyAudits.colorContrast?.details?.items?.length || 0} issues)`}
- **Focus Visible**: ${result.keyAudits.focusVisible?.score === 1 ? '✅ Passed' : '❌ Failed'}
- **Logical Tab Order**: ${result.keyAudits.logicalTabOrder?.score === 1 ? '✅ Passed' : '❌ Failed'}
- **Managed Focus**: ${result.keyAudits.managedFocus?.score === 1 ? '✅ Passed' : '❌ Failed'}

**Detailed Report**: ${result.reportPath}
`).join('\n')}

## 🔍 Touch Target Analysis

${results.map(result => {
  const tapTargets = result.keyAudits.tapTargets;
  if (!tapTargets || tapTargets.score === 1) {
    return `**${result.page}**: ✅ All touch targets are appropriately sized (48px minimum)`;
  } else {
    const violations = tapTargets.details?.items?.length || 0;
    return `**${result.page}**: ❌ ${violations} touch target violations found - elements smaller than 48x48px`;
  }
}).join('\n')}

## 🎨 Color Contrast Analysis

${results.map(result => {
  const colorContrast = result.keyAudits.colorContrast;
  if (!colorContrast || colorContrast.score === 1) {
    return `**${result.page}**: ✅ All text meets WCAG AA color contrast requirements`;
  } else {
    const violations = colorContrast.details?.items?.length || 0;
    return `**${result.page}**: ❌ ${violations} color contrast violations found`;
  }
}).join('\n')}

## ⌨️ Keyboard Navigation Analysis

${results.map(result => {
  const focusIssues = [];
  if (result.keyAudits.focusVisible?.score !== 1) focusIssues.push('Focus visibility');
  if (result.keyAudits.logicalTabOrder?.score !== 1) focusIssues.push('Tab order');
  if (result.keyAudits.managedFocus?.score !== 1) focusIssues.push('Focus management');

  if (focusIssues.length === 0) {
    return `**${result.page}**: ✅ All keyboard navigation requirements met`;
  } else {
    return `**${result.page}**: ❌ Issues found: ${focusIssues.join(', ')}`;
  }
}).join('\n')}

## 📈 Summary Statistics

- **Total Pages Audited**: ${results.length}
- **Pages Meeting 90+ Target**: ${results.filter(r => r.uiUxScore >= 90).length}
- **Average UI/UX Score**: ${Math.round(results.reduce((sum, r) => sum + r.uiUxScore, 0) / results.length)}/100
- **Target Achievement**: ${results.every(r => r.uiUxScore >= 90) ? '✅ ACHIEVED' : '⚠️ IN PROGRESS'}

## 🚀 Recommendations

### Immediate Actions for UI/UX Improvement
${results.some(r => r.uiUxScore < 90) ? `
1. **Touch Targets**: Ensure all clickable elements are at least 48x48px
2. **Color Contrast**: Verify all text meets WCAG AA standards (4.5:1 for normal text)
3. **Focus Management**: Improve keyboard navigation and focus visibility
4. **Accessibility Labels**: Add proper ARIA labels and alt text
` : '✅ All UI/UX targets achieved! Continue monitoring and maintain high standards.'}

### Performance Optimization
- Monitor Core Web Vitals regularly
- Optimize image loading and compression
- Minimize JavaScript execution time
- Implement proper caching strategies

---
*Generated on ${new Date().toLocaleString()} using Lighthouse CLI*
`;

  const reportPath = path.join(__dirname, '..', 'docs', `lighthouse-comprehensive-report-${Date.now()}.md`);
  await fs.writeFile(reportPath, report);

  console.log(`\n📄 Comprehensive report saved to: ${reportPath}`);
  return { report, reportPath };
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
      try {
        const result = await runLighthouseAudit(page);
        results.push(result);

        // Wait between audits
        if (results.length < testPages.length) {
          console.log('⏳ Waiting 2 seconds before next audit...');
          await new Promise(resolve => setTimeout(resolve, 2000));
        }
      } catch (error) {
        console.error(`❌ Failed to audit ${page.name}:`, error.message);
      }
    }

    if (results.length === 0) {
      throw new Error('No successful audits completed');
    }

    // Generate comprehensive report
    const { report, reportPath } = await generateReport(results);

    console.log('\n🎯 FINAL AUDIT SUMMARY');
    console.log('======================');

    results.forEach(result => {
      const status = result.uiUxScore >= 90 ? '✅' : result.uiUxScore >= 80 ? '⚠️' : '❌';
      console.log(`${status} ${result.page}: ${result.uiUxScore}/100 UI/UX Score`);
      console.log(`   Performance: ${result.scores.performance} | Accessibility: ${result.scores.accessibility} | Best Practices: ${result.scores.bestPractices} | SEO: ${result.scores.seo}`);
    });

    const averageScore = Math.round(results.reduce((sum, r) => sum + r.uiUxScore, 0) / results.length);
    const targetAchieved = results.every(r => r.uiUxScore >= 90);

    console.log(`\n📊 Average UI/UX Score: ${averageScore}/100`);
    console.log(`🎯 90+ Target: ${targetAchieved ? 'ACHIEVED ✅' : 'IN PROGRESS ⚠️'}`);
    console.log(`📄 Full report: ${reportPath}`);

    if (targetAchieved) {
      console.log('\n🎉 CONGRATULATIONS! All pages have achieved the 90+ UI/UX score target!');
    } else {
      const needWork = results.filter(r => r.uiUxScore < 90);
      console.log(`\n⚠️ ${needWork.length} page(s) still need optimization to reach 90+:`);
      needWork.forEach(r => console.log(`   - ${r.page}: ${r.uiUxScore}/100`));
    }

  } catch (error) {
    console.error('❌ Error running lighthouse audits:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { runLighthouseAudit, generateReport };