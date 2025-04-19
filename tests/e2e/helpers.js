/**
 * End-to-end testing helpers
 * Part of Phase 4 testing implementation
 */

const fs = require('fs');
const path = require('path');
const config = require('./config');

/**
 * Ensures a directory exists, creating it if necessary
 * 
 * @param {string} dirPath - Path to the directory
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * Takes a screenshot with a standardized filename
 * 
 * @param {import('playwright').Page} page - Playwright page object
 * @param {string} testName - Name of the test
 * @param {string} screenshotName - Name for the screenshot
 */
async function takeScreenshot(page, testName, screenshotName) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const dirPath = path.join(config.screenshotDir, testName);
  
  ensureDir(dirPath);
  
  const filePath = path.join(dirPath, `${screenshotName}-${timestamp}.png`);
  await page.screenshot({ path: filePath, fullPage: true });
  
  return filePath;
}

/**
 * Navigates to a URL relative to the base URL
 * 
 * @param {import('playwright').Page} page - Playwright page object
 * @param {string} relativeUrl - URL relative to base URL
 */
async function navigateTo(page, relativeUrl) {
  const url = new URL(relativeUrl, config.baseUrl).toString();
  await page.goto(url, { waitUntil: 'networkidle' });
}

/**
 * Waits for page to be ready (load, network idle, animations complete)
 * 
 * @param {import('playwright').Page} page - Playwright page object
 */
async function waitForPageReady(page) {
  // Wait for network to be idle
  await page.waitForLoadState('networkidle');
  
  // Wait for animations to complete (custom check)
  await page.waitForFunction(() => {
    // Check if any animations are still running
    const animatingElements = document.querySelectorAll('[style*="animation"]');
    for (const el of animatingElements) {
      const computedStyle = window.getComputedStyle(el);
      if (computedStyle.animationPlayState === 'running') {
        return false;
      }
    }
    return true;
  }, { timeout: 5000 }).catch(() => {
    // If timeout waiting for animations, just continue
    console.warn('Timed out waiting for animations to complete');
  });
}

/**
 * Sets the viewport size for responsive testing
 * 
 * @param {import('playwright').Page} page - Playwright page object  
 * @param {string} device - Device name (mobile, tablet, desktop)
 */
async function setViewport(page, device) {
  if (!config.viewports[device]) {
    throw new Error(`Unknown device: ${device}`);
  }
  
  await page.setViewportSize(config.viewports[device]);
}

/**
 * Checks if an element is visible in the viewport
 * 
 * @param {import('playwright').Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @returns {Promise<boolean>} Whether the element is visible
 */
async function isElementVisible(page, selector) {
  return page.evaluate((sel) => {
    const element = document.querySelector(sel);
    if (!element) return false;
    
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= window.innerHeight &&
      rect.right <= window.innerWidth
    );
  }, selector);
}

module.exports = {
  takeScreenshot,
  navigateTo,
  waitForPageReady,
  setViewport,
  isElementVisible,
  ensureDir
};