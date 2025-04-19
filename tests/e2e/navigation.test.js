/**
 * End-to-end tests for website navigation
 * Part of Phase 4 testing implementation
 */

const { test, expect } = require('@playwright/test');
const { navigateTo, waitForPageReady, takeScreenshot, setViewport } = require('./helpers');
const config = require('./config');

test.describe('Navigation Tests', () => {
  // Setup for all tests
  test.beforeEach(async ({ page }) => {
    // Set desktop viewport by default
    await setViewport(page, 'desktop');
  });

  test('Main navigation links work correctly', async ({ page }) => {
    // Go to homepage
    await navigateTo(page, '/');
    await waitForPageReady(page);
    await takeScreenshot(page, 'navigation', 'homepage');
    
    // Verify page title
    const title = await page.title();
    expect(title).toContain('William Zujkowski'); // Adjust based on actual title
    
    // Test navigation to Blog page
    const blogLink = page.locator('nav a[href="/blog/"]');
    await expect(blogLink).toBeVisible();
    
    await blogLink.click();
    await waitForPageReady(page);
    await takeScreenshot(page, 'navigation', 'blog-page');
    
    // Verify we're on the blog page
    expect(page.url()).toContain('/blog/');
    const blogHeading = page.locator('h1:has-text("Blog Posts")');
    await expect(blogHeading).toBeVisible();
    
    // Navigate to Links page
    const linksLink = page.locator('nav a[href="/links/"]');
    await expect(linksLink).toBeVisible();
    
    await linksLink.click();
    await waitForPageReady(page);
    await takeScreenshot(page, 'navigation', 'links-page');
    
    // Verify we're on the links page
    expect(page.url()).toContain('/links/');
    
    // Return to homepage via logo/home link
    const homeLink = page.locator('a[href="/"]').first();
    await homeLink.click();
    await waitForPageReady(page);
    
    // Verify we're back on the homepage
    expect(page.url()).toBe(config.baseUrl + '/');
  });
  
  test('Skip to content link works for accessibility', async ({ page }) => {
    // Go to homepage
    await navigateTo(page, '/');
    
    // Find the skip link (might be hidden by default)
    const skipLink = page.locator('.skip-link');
    
    // Make sure it exists
    await expect(skipLink).toBeTruthy();
    
    // Tab to make it visible
    await page.keyboard.press('Tab');
    
    // Take screenshot showing skip link
    await takeScreenshot(page, 'navigation', 'skip-link-visible');
    
    // Click the skip link
    await skipLink.click();
    
    // Verify focus moved to main content
    const activeElement = await page.evaluate(() => {
      return document.activeElement.id;
    });
    
    // Main content should have focus (it should have id "main-content")
    expect(activeElement).toBe('main-content');
  });
  
  test('Responsive navigation works on mobile', async ({ page }) => {
    // Set mobile viewport
    await setViewport(page, 'mobile');
    
    // Go to homepage
    await navigateTo(page, '/');
    await waitForPageReady(page);
    
    // Take screenshot of mobile navigation
    await takeScreenshot(page, 'navigation', 'mobile-nav-closed');
    
    // Find and click the mobile menu toggle
    const menuToggle = page.locator('button.menu-toggle, .mobile-menu-toggle');
    
    if (await menuToggle.isVisible()) {
      // If there is a mobile menu toggle, verify it works
      await menuToggle.click();
      await page.waitForTimeout(500); // Wait for animation
      
      // Take screenshot of open mobile menu
      await takeScreenshot(page, 'navigation', 'mobile-nav-open');
      
      // Verify menu items are visible
      const navItems = page.locator('nav a');
      await expect(navItems.first()).toBeVisible();
      
      // Click a nav link
      const blogLink = page.locator('nav a[href="/blog/"]');
      await blogLink.click();
      
      // Verify navigation worked
      await waitForPageReady(page);
      expect(page.url()).toContain('/blog/');
    } else {
      // If no mobile toggle, the navigation might be always visible or use a different pattern
      // Just verify the links are accessible
      const navItems = page.locator('nav a');
      await expect(navItems.first()).toBeVisible();
      
      // Click a nav link
      const blogLink = page.locator('nav a[href="/blog/"]');
      await blogLink.click();
      
      // Verify navigation worked
      await waitForPageReady(page);
      expect(page.url()).toContain('/blog/');
    }
  });
});