/**
 * Generate test screenshots for the links page
 * This script creates a small set of screenshots for testing the links page
 */

import puppeteer from 'puppeteer';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Test links to capture
const LINKS_TO_CAPTURE = [
  { id: 'github', url: 'https://github.com', name: 'GitHub' },
  { id: 'centauri-dreams', url: 'https://www.centauri-dreams.org', name: 'Centauri Dreams' },
  { id: 'museum-of-obsolete-media', url: 'https://obsoletemedia.org', name: 'Museum of Obsolete Media' },
  { id: 'paperclip-ai-game', url: 'https://www.decisionproblem.com/paperclips/', name: 'Paperclip AI Game' },
  { id: 'learn-x-in-y-minutes', url: 'https://learnxinyminutes.com', name: 'Learn X in Y Minutes' },
  { id: 'orions-arm-universe-project', url: 'https://www.orionsarm.com', name: 'Orion\'s Arm Universe Project' }
];

// Set screenshot dimensions
const VIEWPORT = { width: 1200, height: 675, deviceScaleFactor: 1 };
const SCREENSHOT_QUALITY = 80;
const OUTPUT_DIR = path.join(__dirname, '..', 'assets', 'data', 'screenshots');

/**
 * Take a screenshot of a URL using puppeteer
 */
async function takeScreenshot(link) {
  let browser;
  try {
    console.log(`Taking screenshot of ${link.url}...`);
    browser = await puppeteer.launch({
      headless: 'new',
      args: [
        '--no-sandbox', 
        '--disable-setuid-sandbox',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials'
      ]
    });
    
    const page = await browser.newPage();
    await page.setViewport(VIEWPORT);
    
    // Set a realistic user agent
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36');
    
    // Set additional headers to appear more like a real browser
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    });
    
    // Navigate to the URL with better error handling
    await page.goto(link.url, {
      timeout: 30000,
      waitUntil: 'networkidle2'
    });
    
    // Ensure the page is fully loaded
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // Take screenshot
    const outputPath = path.join(OUTPUT_DIR, `${link.id}.jpg`);
    await page.screenshot({
      path: outputPath,
      type: 'jpeg',
      quality: SCREENSHOT_QUALITY,
      fullPage: false
    });
    
    console.log(`Screenshot saved to: ${outputPath}`);
    return outputPath;
  } catch (error) {
    console.error(`Error taking screenshot for ${link.url}:`, error.message);
    return null;
  } finally {
    if (browser) await browser.close();
  }
}

/**
 * Main function to process all links
 */
async function main() {
  try {
    // Create output directory if it doesn't exist
    await fs.mkdir(OUTPUT_DIR, { recursive: true });
    
    // Track results
    const results = {
      success: 0,
      failed: 0
    };
    
    // Process each link sequentially to avoid memory issues
    for (const link of LINKS_TO_CAPTURE) {
      const result = await takeScreenshot(link);
      if (result) {
        results.success++;
      } else {
        results.failed++;
      }
      
      // Small delay between screenshots
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Update the link-previews.json file to reference these screenshots
    const linkPreviewsPath = path.join(__dirname, '..', 'assets', 'data', 'link-previews.json');
    let linkPreviewsData = [];
    
    try {
      const data = await fs.readFile(linkPreviewsPath, 'utf-8');
      linkPreviewsData = JSON.parse(data);
    } catch (error) {
      console.warn('Could not read existing link-previews.json, creating new file');
    }
    
    // Update entries in the JSON file
    for (const link of LINKS_TO_CAPTURE) {
      const existingIndex = linkPreviewsData.findIndex(item => item.id === link.id);
      
      if (existingIndex >= 0) {
        // Update existing entry
        linkPreviewsData[existingIndex].screenshot = `/assets/data/screenshots/${link.id}.jpg`;
        linkPreviewsData[existingIndex].last_checked = new Date().toISOString();
      } else {
        // Create new entry
        linkPreviewsData.push({
          id: link.id,
          url: link.url,
          name: link.name,
          type: 'link',
          group: null,
          metadata: {
            status: 'pending'
          },
          screenshot: `/assets/data/screenshots/${link.id}.jpg`,
          last_checked: new Date().toISOString()
        });
      }
    }
    
    // Save updated JSON
    await fs.writeFile(linkPreviewsPath, JSON.stringify(linkPreviewsData, null, 2));
    console.log(`Updated link-previews.json with ${LINKS_TO_CAPTURE.length} screenshot references`);
    
    // Summary
    console.log('========== SUMMARY ==========');
    console.log(`Total links processed: ${LINKS_TO_CAPTURE.length}`);
    console.log(`Successful screenshots: ${results.success}`);
    console.log(`Failed screenshots: ${results.failed}`);
    console.log('============================');
  } catch (error) {
    console.error('Error in main process:', error);
    process.exit(1);
  }
}

// Run the main function
main();