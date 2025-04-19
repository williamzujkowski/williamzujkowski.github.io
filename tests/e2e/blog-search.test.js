/**
 * End-to-end tests for blog search functionality
 * Part of Phase 4 testing implementation
 */

const { test, expect } = require('@playwright/test');
const { navigateTo, waitForPageReady, takeScreenshot } = require('./helpers');

test.describe('Blog Search Functionality', () => {
  // Setup for each test
  test.beforeEach(async ({ page }) => {
    // Go to the blog page
    await navigateTo(page, '/blog/');
    await waitForPageReady(page);
  });

  test('Search input is visible and functional', async ({ page }) => {
    // Check that search input exists
    const searchInput = page.locator('#search-input');
    await expect(searchInput).toBeVisible();
    
    // Take screenshot of initial state
    await takeScreenshot(page, 'blog-search', 'initial-state');
    
    // Count initial number of posts
    const initialPostCount = await page.locator('.searchable').count();
    expect(initialPostCount).toBeGreaterThan(0);
    
    // Type a search term that should match some posts
    await searchInput.fill('security');
    await page.waitForTimeout(500); // Wait for debounce
    
    // Take screenshot of search results
    await takeScreenshot(page, 'blog-search', 'security-search');
    
    // Check that some posts are still visible but fewer than before
    const securitySearchCount = await page.locator('.searchable:visible').count();
    expect(securitySearchCount).toBeGreaterThan(0);
    expect(securitySearchCount).toBeLessThanOrEqual(initialPostCount);
    
    // Type a search term that should match no posts
    await searchInput.fill('xyznonexistentterm');
    await page.waitForTimeout(500); // Wait for debounce
    
    // Take screenshot of no results
    await takeScreenshot(page, 'blog-search', 'no-results');
    
    // Check that no posts are visible and no results message is shown
    const noResultsVisible = await page.locator('#no-results-message').isVisible();
    expect(noResultsVisible).toBe(true);
    
    // Clear search and verify all posts return
    await searchInput.fill('');
    await page.waitForTimeout(500); // Wait for debounce
    
    // Take screenshot of cleared search
    await takeScreenshot(page, 'blog-search', 'cleared-search');
    
    // Check that all posts are visible again
    const afterClearCount = await page.locator('.searchable:visible').count();
    expect(afterClearCount).toBe(initialPostCount);
  });

  test('Tag filtering works correctly', async ({ page }) => {
    // Find tag buttons
    const tagButtons = page.locator('.tag-btn');
    await expect(tagButtons.first()).toBeVisible();
    
    // Click a specific tag (e.g., security)
    const securityTag = page.locator('.tag-btn[data-tag="security"]');
    
    // If security tag exists, test it, otherwise use the first non-all tag
    if (await securityTag.count() > 0) {
      await securityTag.click();
      await page.waitForTimeout(500); // Wait for animation
      
      // Take screenshot of security tag filtered results
      await takeScreenshot(page, 'blog-search', 'security-tag-filter');
      
      // Check that search input was updated with tag
      const searchInput = page.locator('#search-input');
      const inputValue = await searchInput.inputValue();
      expect(inputValue).toBe('security');
      
      // Check that some posts are visible
      const filteredCount = await page.locator('.searchable:visible').count();
      expect(filteredCount).toBeGreaterThan(0);
    } else {
      // Find first tag that's not "All Topics"
      const firstTag = page.locator('.tag-btn:not([data-tag=""])').first();
      
      if (await firstTag.count() > 0) {
        const tagName = await firstTag.getAttribute('data-tag');
        
        await firstTag.click();
        await page.waitForTimeout(500); // Wait for animation
        
        // Take screenshot of tag filtered results
        await takeScreenshot(page, 'blog-search', `${tagName}-tag-filter`);
        
        // Check that search input was updated with tag
        const searchInput = page.locator('#search-input');
        const inputValue = await searchInput.inputValue();
        expect(inputValue).toBe(tagName);
      }
    }
    
    // Test clicking "All Topics" tag
    const allTopicsTag = page.locator('.tag-btn[data-tag=""]');
    await allTopicsTag.click();
    await page.waitForTimeout(500); // Wait for animation
    
    // Take screenshot of all topics
    await takeScreenshot(page, 'blog-search', 'all-topics');
    
    // Check that search input is cleared
    const searchInput = page.locator('#search-input');
    const inputValue = await searchInput.inputValue();
    expect(inputValue).toBe('');
  });

  test('Clear filters button resets search', async ({ page }) => {
    // Search for something first
    const searchInput = page.locator('#search-input');
    await searchInput.fill('technology');
    await page.waitForTimeout(500); // Wait for debounce
    
    // Take screenshot of technology search
    await takeScreenshot(page, 'blog-search', 'technology-search');
    
    // Click clear filters button
    const clearFilters = page.locator('#clear-filters');
    await clearFilters.click();
    await page.waitForTimeout(500); // Wait for animation
    
    // Take screenshot after clearing
    await takeScreenshot(page, 'blog-search', 'after-clear-filters');
    
    // Check that search input is cleared
    const inputValue = await searchInput.inputValue();
    expect(inputValue).toBe('');
    
    // Check that "All Topics" tag is selected
    const allTopicsTag = page.locator('.tag-btn[data-tag=""]');
    const hasSelectedClass = await allTopicsTag.evaluate(el => el.classList.contains('selected'));
    expect(hasSelectedClass).toBe(true);
  });
});