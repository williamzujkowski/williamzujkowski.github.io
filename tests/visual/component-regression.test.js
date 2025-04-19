/**
 * Visual regression tests for UI components
 * Part of Phase 4 testing implementation
 */

const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const pixelmatch = require('pixelmatch');
const { PNG } = require('pngjs');
const config = require('./config');

// Ensure directories exist
for (const dir of [config.baselineDir, config.actualDir, config.diffDir]) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * Compares two images with pixelmatch
 * 
 * @param {Buffer} img1 - First image buffer
 * @param {Buffer} img2 - Second image buffer
 * @param {string} diffPath - Path to save diff image
 * @returns {number} Number of different pixels
 */
function compareImages(img1, img2, diffPath) {
  const png1 = PNG.sync.read(img1);
  const png2 = PNG.sync.read(img2);
  
  const { width, height } = png1;
  const diff = new PNG({ width, height });
  
  const numDiffPixels = pixelmatch(
    png1.data,
    png2.data,
    diff.data,
    width,
    height,
    { threshold: config.threshold }
  );
  
  fs.writeFileSync(diffPath, PNG.sync.write(diff));
  
  return numDiffPixels;
}

/**
 * Gets the path for a screenshot file
 * 
 * @param {string} dir - Base directory
 * @param {string} component - Component name
 * @param {string} viewport - Viewport name
 * @returns {string} Full path
 */
function getScreenshotPath(dir, component, viewport) {
  return path.join(dir, `${component}-${viewport}.png`);
}

/**
 * Runs visual regression test for a component
 * 
 * @param {Object} component - Component config
 * @param {string} viewport - Viewport name
 */
async function testComponent(component, viewport, page) {
  // Set viewport size
  await page.setViewportSize(config.viewports[viewport]);
  
  // Navigate to the page
  await page.goto(`${config.baseUrl}${component.path}`);
  
  // Wait for network and animations to complete
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000); // Additional time for animations
  
  // Find the element
  const element = await page.locator(component.selector);
  
  // Ensure element is visible
  await expect(element).toBeVisible();
  
  // Take screenshot
  const actualPath = getScreenshotPath(config.actualDir, component.name, viewport);
  await element.screenshot({ path: actualPath });
  
  // Check if baseline exists
  const baselinePath = getScreenshotPath(config.baselineDir, component.name, viewport);
  if (!fs.existsSync(baselinePath)) {
    console.log(`Creating baseline for ${component.name} in ${viewport} viewport`);
    fs.copyFileSync(actualPath, baselinePath);
    return;
  }
  
  // Compare with baseline
  const diffPath = getScreenshotPath(config.diffDir, component.name, viewport);
  const img1 = fs.readFileSync(baselinePath);
  const img2 = fs.readFileSync(actualPath);
  
  const numDiffPixels = compareImages(img1, img2, diffPath);
  
  // Get dimensions for percentage calculation
  const png = PNG.sync.read(img1);
  const totalPixels = png.width * png.height;
  const diffPercentage = (numDiffPixels / totalPixels) * 100;
  
  console.log(`Component: ${component.name}, Viewport: ${viewport}`);
  console.log(`Different pixels: ${numDiffPixels} (${diffPercentage.toFixed(2)}%)`);
  
  // Fail test if difference is above threshold
  if (diffPercentage > config.threshold * 100) {
    throw new Error(
      `Visual difference detected for ${component.name} in ${viewport} viewport: ` +
      `${diffPercentage.toFixed(2)}% of pixels are different (threshold: ${config.threshold * 100}%)`
    );
  }
}

test.describe('Visual Regression Tests', () => {
  for (const component of config.components) {
    for (const viewport of component.viewports) {
      test(`${component.name} in ${viewport} viewport looks correct`, async ({ page }) => {
        await testComponent(component, viewport, page);
      });
    }
  }
  
  // Test full page regression for key pages
  const keyPages = [
    { name: 'homepage', path: '/' },
    { name: 'blog', path: '/blog/' },
    { name: 'links', path: '/links/' }
  ];
  
  for (const page of keyPages) {
    test(`Full page: ${page.name} looks correct`, async ({ page: browserPage }) => {
      // Set desktop viewport
      await browserPage.setViewportSize(config.viewports.desktop);
      
      // Navigate to the page
      await browserPage.goto(`${config.baseUrl}${page.path}`);
      
      // Wait for network and animations to complete
      await browserPage.waitForLoadState('networkidle');
      await browserPage.waitForTimeout(1000); // Additional time for animations
      
      // Take full page screenshot
      const actualPath = path.join(config.actualDir, `fullpage-${page.name}.png`);
      await browserPage.screenshot({ path: actualPath, fullPage: true });
      
      // Check if baseline exists
      const baselinePath = path.join(config.baselineDir, `fullpage-${page.name}.png`);
      if (!fs.existsSync(baselinePath)) {
        console.log(`Creating baseline for full page ${page.name}`);
        fs.copyFileSync(actualPath, baselinePath);
        return;
      }
      
      // Compare with baseline
      const diffPath = path.join(config.diffDir, `fullpage-${page.name}.png`);
      const img1 = fs.readFileSync(baselinePath);
      const img2 = fs.readFileSync(actualPath);
      
      const numDiffPixels = compareImages(img1, img2, diffPath);
      
      // Get dimensions for percentage calculation
      const png = PNG.sync.read(img1);
      const totalPixels = png.width * png.height;
      const diffPercentage = (numDiffPixels / totalPixels) * 100;
      
      console.log(`Full page: ${page.name}`);
      console.log(`Different pixels: ${numDiffPixels} (${diffPercentage.toFixed(2)}%)`);
      
      // Full pages can have more differences, so we set a higher threshold
      const fullPageThreshold = config.threshold * 2;
      
      // Fail test if difference is above threshold
      if (diffPercentage > fullPageThreshold * 100) {
        throw new Error(
          `Visual difference detected for full page ${page.name}: ` +
          `${diffPercentage.toFixed(2)}% of pixels are different (threshold: ${fullPageThreshold * 100}%)`
        );
      }
    });
  }
});