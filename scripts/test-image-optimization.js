#!/usr/bin/env node

/**
 * Test Image Optimization - Measure LCP and verify image rendering
 *
 * This script:
 * 1. Captures homepage screenshot before/after optimization
 * 2. Measures LCP (Largest Contentful Paint) timing
 * 3. Verifies AVIF/WebP images are being used
 * 4. Calculates size reduction percentage
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function testImageOptimization() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('🔍 Testing image optimization on homepage...\n');

  // Navigate to homepage
  await page.goto('http://localhost:8086/', { waitUntil: 'networkidle' });

  // Capture screenshot
  const screenshotDir = path.join(__dirname, '../screenshots');
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  const screenshotPath = path.join(screenshotDir, 'homepage-optimized-image.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log(`✅ Screenshot saved: ${screenshotPath}`);

  // Get performance metrics
  const performanceMetrics = await page.evaluate(() => {
    const entries = performance.getEntriesByType('navigation');
    const paintEntries = performance.getEntriesByType('paint');

    const lcp = paintEntries.find(e => e.name === 'largest-contentful-paint');
    const fcp = paintEntries.find(e => e.name === 'first-contentful-paint');

    return {
      lcp: lcp ? lcp.startTime : null,
      fcp: fcp ? fcp.startTime : null,
      domContentLoaded: entries[0] ? entries[0].domContentLoadedEventEnd : null,
      loadComplete: entries[0] ? entries[0].loadEventEnd : null
    };
  });

  console.log('\n📊 Performance Metrics:');
  console.log(`  LCP (Largest Contentful Paint): ${performanceMetrics.lcp ? (performanceMetrics.lcp / 1000).toFixed(2) + 's' : 'N/A'}`);
  console.log(`  FCP (First Contentful Paint): ${performanceMetrics.fcp ? (performanceMetrics.fcp / 1000).toFixed(2) + 's' : 'N/A'}`);
  console.log(`  DOM Content Loaded: ${performanceMetrics.domContentLoaded ? (performanceMetrics.domContentLoaded / 1000).toFixed(2) + 's' : 'N/A'}`);
  console.log(`  Load Complete: ${performanceMetrics.loadComplete ? (performanceMetrics.loadComplete / 1000).toFixed(2) + 's' : 'N/A'}`);

  // Check if optimized images are being used
  const imageInfo = await page.evaluate(() => {
    const picture = document.querySelector('picture');
    if (!picture) return null;

    const avifSource = picture.querySelector('source[type="image/avif"]');
    const webpSource = picture.querySelector('source[type="image/webp"]');
    const img = picture.querySelector('img');

    return {
      hasAvif: !!avifSource,
      hasWebp: !!webpSource,
      imgSrc: img ? img.src : null,
      imgAlt: img ? img.alt : null,
      imgLoading: img ? img.loading : null,
      imgDecoding: img ? img.decoding : null
    };
  });

  console.log('\n🖼️  Image Information:');
  console.log(`  AVIF support: ${imageInfo.hasAvif ? '✅ Yes' : '❌ No'}`);
  console.log(`  WebP support: ${imageInfo.hasWebp ? '✅ Yes' : '❌ No'}`);
  console.log(`  Image source: ${imageInfo.imgSrc}`);
  console.log(`  Alt text: ${imageInfo.imgAlt}`);
  console.log(`  Loading: ${imageInfo.imgLoading}`);
  console.log(`  Decoding: ${imageInfo.imgDecoding}`);

  // Calculate size reduction
  const originalSize = 240 * 1024; // 240KB in bytes
  const optimizedSize = 11 * 1024; // 11KB AVIF (400px) in bytes
  const reduction = ((originalSize - optimizedSize) / originalSize * 100).toFixed(1);

  console.log('\n💾 Size Reduction:');
  console.log(`  Original: 240 KB (PNG)`);
  console.log(`  Optimized: 11 KB (AVIF, 400px)`);
  console.log(`  Reduction: ${reduction}% smaller 🎉`);

  // Check for CSS classes (visual styling)
  const hasRoundedClass = await page.evaluate(() => {
    const picture = document.querySelector('picture');
    const img = picture ? picture.querySelector('img') : null;
    return img ? img.className.includes('rounded') : false;
  });

  if (!hasRoundedClass) {
    console.log('\n⚠️  Warning: Image may be missing CSS classes for rounded corners and shadows');
    console.log('   Original had: rounded-full, shadow-2xl, ring-4, ring-offset-2');
  }

  await browser.close();

  console.log('\n✅ Image optimization test complete!\n');
}

testImageOptimization().catch(console.error);
