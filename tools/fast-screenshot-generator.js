/**
 * Fast Screenshot and Metadata Generator
 * Optimized for speed with parallel processing, caching, and performance tweaks
 */

import puppeteer from 'puppeteer';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  // Screenshot settings
  viewport: { width: 1200, height: 675, deviceScaleFactor: 1 },
  quality: 70, // Lower quality (0-100) = faster processing, smaller files
  fullPage: false,
  
  // Performance settings
  concurrency: Math.max(1, Math.min(os.cpus().length - 1, 4)), // Use up to N-1 CPU cores, max 4
  batchSize: 10, // How many links to process before saving
  pageTimeout: 20000, // Reduce timeout for faster failures (20 seconds)
  
  // Path settings
  outputDir: path.join(__dirname, '..', 'assets', 'data', 'screenshots'),
  cacheDir: path.join(__dirname, '..', '.cache', 'screenshots'),
  metadataFile: path.join(__dirname, '..', 'assets', 'data', 'link-previews.json'),
  
  // Browser settings
  browserArgs: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage', // Reduce memory usage
    '--disable-accelerated-2d-canvas', // Disable GPU acceleration
    '--no-first-run',
    '--no-zygote',
    '--disable-gpu',
    '--disable-web-security',
    '--disable-features=IsolateOrigins,site-per-process',
    '--disable-site-isolation-trials'
  ],
  
  // Domains to skip
  skipDomains: [
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
  ]
};

// Parse command-line arguments
const args = process.argv.slice(2);
const startIndex = parseInt(args[0] || '0', 10);
const count = parseInt(args[1] || '20', 10);
const updateAll = args.includes('--update-all');
const forceRefresh = args.includes('--force-refresh');

console.log(`
📸 Fast Screenshot Generator
===========================
Start Index: ${startIndex}
Count: ${count}
Update All: ${updateAll}
Force Refresh: ${forceRefresh}
Concurrency: ${CONFIG.concurrency}
Batch Size: ${CONFIG.batchSize}
===========================
`);

/**
 * Check if a URL should be skipped based on domain patterns
 */
function shouldSkipUrl(url) {
  try {
    const urlObj = new URL(url);
    return CONFIG.skipDomains.some(domain => urlObj.hostname.includes(domain));
  } catch (error) {
    console.warn(`Invalid URL: ${url}`);
    return true;
  }
}

/**
 * Take a screenshot of a URL using puppeteer with optimized settings
 */
async function takeScreenshot(browser, link) {
  let page;
  try {
    console.log(`📷 Taking screenshot of ${link.url}...`);
    
    // Check cache first if not forcing refresh
    const cacheFile = path.join(CONFIG.cacheDir, `${link.id}.jpg`);
    const cacheExpiry = 30 * 24 * 60 * 60 * 1000; // 30 days
    
    // Use cached screenshot if available and recent
    if (!forceRefresh && await fs.access(cacheFile).then(() => true).catch(() => false)) {
      const stats = await fs.stat(cacheFile);
      const age = Date.now() - stats.mtimeMs;
      
      if (age < cacheExpiry) {
        console.log(`✓ Using cached screenshot for ${link.id} (${Math.round(age / (24 * 60 * 60 * 1000))} days old)`);
        const outputPath = path.join(CONFIG.outputDir, `${link.id}.jpg`);
        await fs.copyFile(cacheFile, outputPath);
        return outputPath;
      }
    }
    
    // Create new page
    page = await browser.newPage();
    
    // Set viewport
    await page.setViewport(CONFIG.viewport);
    
    // Optimize page settings for speed
    await page.setRequestInterception(true);
    page.on('request', (request) => {
      // Block unnecessary resources
      const resourceType = request.resourceType();
      if (resourceType === 'font' || resourceType === 'media' || 
          resourceType === 'websocket') {
        request.abort();
      } else {
        request.continue();
      }
    });
    
    // Set a realistic user agent
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36');
    
    // Set additional headers
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    });
    
    // Navigate to the URL with better error handling and reduced timeout
    await page.goto(link.url, {
      timeout: CONFIG.pageTimeout,
      waitUntil: 'domcontentloaded' // Use faster load state
    });
    
    // Wait a bit for visual elements to load
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Ensure the page is scrolled to top
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // Take screenshot
    const outputPath = path.join(CONFIG.outputDir, `${link.id}.jpg`);
    await page.screenshot({
      path: outputPath,
      type: 'jpeg',
      quality: CONFIG.quality,
      fullPage: CONFIG.fullPage
    });
    
    // Save to cache
    await fs.mkdir(CONFIG.cacheDir, { recursive: true });
    await fs.copyFile(outputPath, cacheFile);
    
    console.log(`✅ Screenshot saved for ${link.id}`);
    return outputPath;
  } catch (error) {
    console.error(`❌ Error taking screenshot for ${link.url}:`, error.message);
    return null;
  } finally {
    if (page) await page.close();
  }
}

/**
 * Process a batch of links concurrently
 */
async function processBatch(browser, batch, results) {
  console.log(`\n🔄 Processing batch of ${batch.length} links...`);
  
  // Process links in parallel up to concurrency limit
  const chunks = [];
  for (let i = 0; i < batch.length; i += CONFIG.concurrency) {
    chunks.push(batch.slice(i, i + CONFIG.concurrency));
  }
  
  // Process each chunk concurrently
  for (const chunk of chunks) {
    const chunkPromises = chunk.map(async (link) => {
      const result = await takeScreenshot(browser, link);
      
      if (result) {
        results.success++;
        // Update the link's last_checked date and screenshot path
        link.last_checked = new Date().toISOString();
        link.screenshot = `/assets/data/screenshots/${link.id}.jpg`;
      } else {
        results.failed++;
      }
      
      return link;
    });
    
    // Wait for all screenshots in this chunk to complete
    await Promise.all(chunkPromises);
  }
  
  return batch;
}

/**
 * Main processing function
 */
async function main() {
  let browser;
  
  try {
    // Create output directories
    await fs.mkdir(CONFIG.outputDir, { recursive: true });
    await fs.mkdir(CONFIG.cacheDir, { recursive: true });
    
    // Read link-previews.json
    let linkPreviewsData = [];
    try {
      const data = await fs.readFile(CONFIG.metadataFile, 'utf-8');
      linkPreviewsData = JSON.parse(data);
      console.log(`📋 Loaded ${linkPreviewsData.length} links from metadata file`);
    } catch (error) {
      console.error('❌ Failed to read metadata file:', error.message);
      process.exit(1);
    }
    
    // Filter links to process
    let linksToProcess = linkPreviewsData.filter(link => {
      if (!link.url || !link.id) {
        console.log(`⚠️ Skipping invalid link:`, link);
        return false;
      }
      
      if (shouldSkipUrl(link.url)) {
        console.log(`⏭️ Skipping blocked domain: ${link.url}`);
        return false;
      }
      
      if (!updateAll && !forceRefresh && link.screenshot) {
        // Skip links that already have screenshots unless force refreshing
        return false;
      }
      
      return true;
    });
    
    // Get the specific batch to process if not updating all
    if (!updateAll) {
      linksToProcess = linksToProcess.slice(startIndex, startIndex + count);
    }
    
    console.log(`🎯 Processing ${linksToProcess.length} links (batch ${startIndex} to ${startIndex + linksToProcess.length - 1})`);
    
    if (linksToProcess.length === 0) {
      console.log('✅ No links to process. All links already have screenshots or were filtered out.');
      return;
    }
    
    // Launch browser (shared across all screenshots for efficiency)
    console.log('🚀 Launching browser...');
    browser = await puppeteer.launch({
      headless: 'new',
      args: CONFIG.browserArgs
    });
    
    // Track results
    const results = {
      success: 0,
      failed: 0,
      total: linksToProcess.length,
      startTime: Date.now()
    };
    
    // Process links in batches
    for (let i = 0; i < linksToProcess.length; i += CONFIG.batchSize) {
      const batch = linksToProcess.slice(i, i + CONFIG.batchSize);
      
      // Process the batch
      await processBatch(browser, batch, results);
      
      // Update the links in the linkPreviewsData array
      for (const processedLink of batch) {
        const index = linkPreviewsData.findIndex(link => link.id === processedLink.id);
        if (index !== -1) {
          linkPreviewsData[index] = processedLink;
        }
      }
      
      // Save progress
      await fs.writeFile(CONFIG.metadataFile, JSON.stringify(linkPreviewsData, null, 2));
      console.log(`💾 Saved progress after processing ${i + batch.length} of ${linksToProcess.length} links`);
      
      // Short delay between batches
      if (i + CONFIG.batchSize < linksToProcess.length) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    // Copy to _data directory if it exists
    const dataDir = path.join(__dirname, '..', '_data');
    if (await fs.access(dataDir).then(() => true).catch(() => false)) {
      await fs.copyFile(CONFIG.metadataFile, path.join(dataDir, 'link-previews.json'));
      console.log('📄 Copied link-previews.json to _data directory');
    }
    
    // Calculate timing and performance
    const endTime = Date.now();
    const duration = (endTime - results.startTime) / 1000;
    const avgTimePerLink = duration / results.total;
    
    // Summary
    console.log(`\n📊 SUMMARY`);
    console.log(`===========================`);
    console.log(`🔢 Total links processed: ${results.total}`);
    console.log(`✅ Successful screenshots: ${results.success}`);
    console.log(`❌ Failed screenshots: ${results.failed}`);
    console.log(`📈 Success rate: ${Math.round((results.success / results.total) * 100)}%`);
    console.log(`⏱️ Total time: ${duration.toFixed(2)}s`);
    console.log(`⚡ Average time per link: ${avgTimePerLink.toFixed(2)}s`);
    console.log(`===========================`);
    
  } catch (error) {
    console.error('❌ Error in main process:', error);
    process.exit(1);
  } finally {
    if (browser) {
      console.log('🔚 Closing browser...');
      await browser.close();
    }
  }
}

// Run the main function
main();