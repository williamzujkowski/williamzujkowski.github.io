/**
 * Generate screenshots for a batch of links
 * This script processes a specific batch of links from the link-previews.json file
 */

import puppeteer from 'puppeteer';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Set screenshot dimensions
const VIEWPORT = { width: 1200, height: 675, deviceScaleFactor: 1 };
const SCREENSHOT_QUALITY = 80;
const OUTPUT_DIR = path.join(__dirname, '..', 'assets', 'data', 'screenshots');
const BATCH_SIZE = 5; // Process 5 links at a time to avoid memory issues

// List of domains to skip (sites that block scraping or aren't suitable for screenshots)
const DOMAINS_TO_SKIP = [
  'linkedin.com',
  'thekidshouldseethis.com',
  'neal.fun',
  'planetminecraft.com',
  'be-mag.com',
  'kickscondor.com',
  'youtube.com',
  'youtu.be',
  'maps.google.com',
  'githubusercontent.com'
];

// Parse command line arguments
const args = process.argv.slice(2);
const startIndex = parseInt(args[0] || '0', 10);
const count = parseInt(args[1] || '20', 10);
console.log(`Processing batch starting at index ${startIndex} with count ${count}`);

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
 * Process a batch of links
 */
async function processBatch(batch, results) {
  const promises = batch.map(async (link) => {
    const result = await takeScreenshot(link);
    if (result) {
      results.success++;
      // Update the link's last_checked date and screenshot path
      link.last_checked = new Date().toISOString();
      link.screenshot = `/assets/data/screenshots/${link.id}.jpg`;
      return link;
    } else {
      results.failed++;
      return link;
    }
  });
  
  return await Promise.all(promises);
}

/**
 * Check if a URL should be skipped based on domain patterns
 */
function shouldSkipUrl(url) {
  try {
    const urlObj = new URL(url);
    return DOMAINS_TO_SKIP.some(domain => urlObj.hostname.includes(domain));
  } catch (error) {
    console.warn(`Invalid URL: ${url}`);
    return true;
  }
}

/**
 * Main function to process a batch of links
 */
async function main() {
  try {
    // Create output directory if it doesn't exist
    await fs.mkdir(OUTPUT_DIR, { recursive: true });
    
    // Read link-previews.json
    const linkPreviewsPath = path.join(__dirname, '..', 'assets', 'data', 'link-previews.json');
    let linkPreviewsData = [];
    
    try {
      const data = await fs.readFile(linkPreviewsPath, 'utf-8');
      linkPreviewsData = JSON.parse(data);
      console.log(`Loaded ${linkPreviewsData.length} links from link-previews.json`);
    } catch (error) {
      console.error('Failed to read link-previews.json:', error.message);
      process.exit(1);
    }
    
    // Filter links to process (skip ones that should be avoided)
    let linksToProcess = linkPreviewsData.filter(link => {
      if (!link.url || !link.id) {
        console.log(`Skipping invalid link:`, link);
        return false;
      }
      
      if (shouldSkipUrl(link.url)) {
        console.log(`Skipping blocked domain: ${link.url}`);
        return false;
      }
      
      return true;
    });
    
    // Get the specific batch to process
    linksToProcess = linksToProcess.slice(startIndex, startIndex + count);
    
    console.log(`Processing ${linksToProcess.length} links (batch ${startIndex} to ${startIndex + linksToProcess.length - 1})`);
    
    // Track results
    const results = {
      success: 0,
      failed: 0,
      total: linksToProcess.length
    };
    
    // Process links in smaller batches
    for (let i = 0; i < linksToProcess.length; i += BATCH_SIZE) {
      const batch = linksToProcess.slice(i, i + BATCH_SIZE);
      console.log(`\nProcessing sub-batch ${Math.floor(i / BATCH_SIZE) + 1} of ${Math.ceil(linksToProcess.length / BATCH_SIZE)} (${batch.length} links)`);
      
      // Process the batch and update the corresponding links in linkPreviewsData
      const processedBatch = await processBatch(batch, results);
      
      // Update the links in the linkPreviewsData array
      for (const processedLink of processedBatch) {
        const index = linkPreviewsData.findIndex(link => link.id === processedLink.id);
        if (index !== -1) {
          linkPreviewsData[index] = processedLink;
        }
      }
      
      // Save the updated JSON file after each batch (in case the process is interrupted)
      await fs.writeFile(linkPreviewsPath, JSON.stringify(linkPreviewsData, null, 2));
      console.log(`Updated link-previews.json after sub-batch ${Math.floor(i / BATCH_SIZE) + 1}`);
      
      // Add a delay between batches
      if (i + BATCH_SIZE < linksToProcess.length) {
        console.log('Pausing for 2 seconds before next sub-batch...');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }
    
    // Copy link-previews.json to _data directory if it exists
    const dataDir = path.join(__dirname, '..', '_data');
    if (await fs.access(dataDir).then(() => true).catch(() => false)) {
      await fs.copyFile(linkPreviewsPath, path.join(dataDir, 'link-previews.json'));
      console.log('Copied link-previews.json to _data directory');
    }
    
    // Summary
    console.log('\n========== SUMMARY ==========');
    console.log(`Batch: ${startIndex} to ${startIndex + count - 1}`);
    console.log(`Actual links processed: ${results.total}`);
    console.log(`Successful screenshots: ${results.success}`);
    console.log(`Failed screenshots: ${results.failed}`);
    console.log(`Success rate: ${Math.round((results.success / results.total) * 100)}%`);
    console.log('============================');
    
    console.log('\nProcess completed. Screenshots have been generated and link-previews.json has been updated.');
  } catch (error) {
    console.error('Error in main process:', error);
    process.exit(1);
  }
}

// Run the main function
main();