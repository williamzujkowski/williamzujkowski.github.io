const { chromium } = require('@playwright/test');
const fs = require('fs').promises;
const path = require('path');

const BREAKPOINTS = [
  { name: 'Mobile-S', width: 320, height: 568 },
  { name: 'Mobile-M', width: 375, height: 812 },
  { name: 'Mobile-L', width: 414, height: 896 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Tablet-L', width: 1024, height: 1366 },
  { name: 'Laptop', width: 1280, height: 800 },
  { name: 'Desktop', width: 1920, height: 1080 },
  { name: '4K', width: 2560, height: 1440 }
];

const PAGES_TO_REVIEW = [
  '/',
  '/about/',
  '/posts/',
  '/uses/',
  '/posts/2024-08-07-claude-flow-development/'
];

async function auditUI() {
  const browser = await chromium.launch({ headless: true });
  const auditResults = {};

  // Create screenshots directory
  const screenshotsDir = path.join(__dirname, '..', 'screenshots');
  try {
    await fs.mkdir(screenshotsDir, { recursive: true });
  } catch (err) {
    console.log('Screenshots directory exists');
  }

  for (const breakpoint of BREAKPOINTS) {
    console.log(`\n📱 Testing ${breakpoint.name} (${breakpoint.width}x${breakpoint.height})`);

    const context = await browser.newContext({
      viewport: breakpoint,
      deviceScaleFactor: 2,
      hasTouch: breakpoint.width < 1024
    });

    const page = await context.newPage();
    auditResults[breakpoint.name] = {};

    for (const pagePath of PAGES_TO_REVIEW) {
      console.log(`  → Testing ${pagePath}`);

      try {
        await page.goto(`http://localhost:8080${pagePath}`, {
          waitUntil: 'networkidle'
        });

        // Wait for content to stabilize
        await page.waitForTimeout(1000);

        const metrics = await page.evaluate(() => {
          // First Impressions
          const h1 = document.querySelector('h1');
          const heroVisible = h1 ? h1.getBoundingClientRect() : null;
          const ctaElement = document.querySelector('.btn-primary, [class*="button"], a[href*="posts"]');
          const ctaAboveFold = ctaElement ? ctaElement.getBoundingClientRect() : null;

          // Navigation
          const nav = document.querySelector('nav');
          const navAccessible = nav ? nav.getAttribute('aria-label') : null;
          const mobileMenuButton = document.querySelector('.mobile-menu-button, [aria-label*="menu"]');

          // Typography
          const body = document.body;
          const fontSize = window.getComputedStyle(body).fontSize;
          const lineHeight = window.getComputedStyle(body).lineHeight;
          const firstParagraph = document.querySelector('p');
          const paragraphSpacing = firstParagraph ?
            window.getComputedStyle(firstParagraph).marginBottom : '0';

          // Visual Hierarchy
          const headingSizes = {};
          ['h1', 'h2', 'h3', 'h4'].forEach(tag => {
            const element = document.querySelector(tag);
            if (element) {
              headingSizes[tag] = window.getComputedStyle(element).fontSize;
            }
          });

          // Dark Mode
          const darkModeToggle = document.querySelector('[aria-label*="theme"], [data-theme-toggle]');

          // Touch Targets
          const touchTargets = [];
          const interactiveElements = document.querySelectorAll('a, button, input, textarea, select');
          interactiveElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44)) {
              touchTargets.push({
                element: el.tagName.toLowerCase(),
                text: (el.textContent || el.getAttribute('aria-label') || '').substring(0, 30),
                width: Math.round(rect.width),
                height: Math.round(rect.height)
              });
            }
          });

          // Layout Issues
          const hasHorizontalScroll = document.documentElement.scrollWidth > window.innerWidth;

          // Color Contrast
          const bgColor = window.getComputedStyle(body).backgroundColor;
          const textColor = window.getComputedStyle(body).color;

          // Content Quality
          const hasImages = document.querySelectorAll('img').length > 0;
          const hasCodeBlocks = document.querySelectorAll('pre, code').length > 0;
          const hasCitations = document.querySelectorAll('a[href*="arxiv"], a[href*="doi"]').length > 0;

          return {
            firstImpressions: {
              heroVisible: heroVisible ? heroVisible.top < window.innerHeight : false,
              ctaAboveFold: ctaAboveFold ? ctaAboveFold.top < window.innerHeight : false,
              hasH1: !!h1
            },
            navigation: {
              hasAriaLabel: !!navAccessible,
              hasMobileMenu: !!mobileMenuButton,
              navPresent: !!nav
            },
            typography: {
              baseFontSize: fontSize,
              lineHeight: lineHeight,
              paragraphSpacing: paragraphSpacing
            },
            visualHierarchy: headingSizes,
            touchTargets: touchTargets,
            layoutIssues: {
              hasHorizontalScroll,
              viewportWidth: window.innerWidth,
              documentWidth: document.documentElement.scrollWidth
            },
            darkMode: {
              hasToggle: !!darkModeToggle
            },
            colors: {
              background: bgColor,
              text: textColor
            },
            content: {
              hasImages,
              hasCodeBlocks,
              hasCitations,
              elementCount: document.querySelectorAll('*').length
            }
          };
        });

        // Take screenshot for visual review
        const screenshotName = `${breakpoint.name}-${pagePath.replace(/\//g, '-')}.png`;
        await page.screenshot({
          path: path.join(screenshotsDir, screenshotName),
          fullPage: false
        });

        auditResults[breakpoint.name][pagePath] = {
          ...metrics,
          screenshot: screenshotName,
          success: true
        };

      } catch (error) {
        console.error(`    ❌ Error testing ${pagePath}: ${error.message}`);
        auditResults[breakpoint.name][pagePath] = {
          error: error.message,
          success: false
        };
      }
    }

    await context.close();
  }

  await browser.close();

  // Save audit results
  const resultsPath = path.join(__dirname, '..', 'ui-ux-audit-results.json');
  await fs.writeFile(resultsPath, JSON.stringify(auditResults, null, 2));

  console.log('\n✅ Audit complete! Results saved to ui-ux-audit-results.json');
  return auditResults;
}

// Run the audit
auditUI().catch(console.error);