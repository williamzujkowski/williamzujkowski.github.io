/**
 * This script pre-generates metadata and screenshots for links using Microlink open source tools
 * It runs during the build process to create a JSON file that can be used for link previews
 */

const fs = require('fs').promises;
const path = require('path');
const metascraper = require('metascraper')([
  require('metascraper-author')(),
  require('metascraper-date')(),
  require('metascraper-description')(),
  require('metascraper-image')(),
  require('metascraper-logo')(),
  require('metascraper-publisher')(),
  require('metascraper-title')(),
  require('metascraper-url')()
]);
const got = require('got');
const puppeteer = require('puppeteer');
const goto = require('@browserless/goto');

// Set screenshot dimensions
const VIEWPORT = { width: 1200, height: 675, deviceScaleFactor: 1 };
const SCREENSHOT_QUALITY = 80;
const OUTPUT_DIR = path.join(__dirname, '_data');
const MAX_CONCURRENT = 3; // Maximum concurrent operations to avoid overloading

/**
 * Extract metadata from a URL using metascraper
 */
async function getMetadata(url) {
  try {
    console.log(`Fetching metadata for ${url}...`);
    const { body: html, url: finalUrl } = await got(url);
    const metadata = await metascraper({ html, url: finalUrl });
    return { ...metadata, status: 'success' };
  } catch (error) {
    console.error(`Error fetching metadata for ${url}:`, error.message);
    return { url, status: 'error', message: error.message };
  }
}

/**
 * Take a screenshot of a URL using browserless/puppeteer
 */
async function takeScreenshot(url, outputPath) {
  let browser;
  try {
    console.log(`Taking screenshot of ${url}...`);
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport(VIEWPORT);
    
    // Use browserless/goto for better navigation handling
    await goto(page, url, {
      timeout: 30000,
      waitUntil: 'networkidle2',
      adblock: true
    });
    
    // Ensure the page is fully loaded
    await page.evaluate(() => window.scrollTo(0, 0));
    
    // Take screenshot
    await page.screenshot({
      path: outputPath,
      type: 'jpeg',
      quality: SCREENSHOT_QUALITY,
      fullPage: false
    });
    
    return {
      url,
      status: 'success',
      screenshot: {
        path: outputPath,
        width: VIEWPORT.width,
        height: VIEWPORT.height,
        type: 'jpeg'
      }
    };
  } catch (error) {
    console.error(`Error taking screenshot for ${url}:`, error.message);
    return { url, status: 'error', message: error.message };
  } finally {
    if (browser) await browser.close();
  }
}

/**
 * Process URLs in chunks to avoid overloading
 */
async function processInChunks(items, processFn, chunkSize = MAX_CONCURRENT) {
  const results = [];
  
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    console.log(`Processing chunk ${i / chunkSize + 1} (${chunk.length} items)...`);
    
    const chunkResults = await Promise.all(
      chunk.map(item => processFn(item).catch(err => ({ 
        url: item.url, 
        status: 'error',
        message: err.message 
      })))
    );
    
    results.push(...chunkResults);
    
    // Add a small delay between chunks to avoid overloading
    if (i + chunkSize < items.length) {
      console.log('Pausing before next chunk...');
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
  
  return results;
}

/**
 * Main function to process all links
 */
async function main() {
  try {
    // Create output directory if it doesn't exist
    await fs.mkdir(path.join(OUTPUT_DIR, 'screenshots'), { recursive: true });
    
    // Read site configuration with links
    const siteJsonPath = path.join(__dirname, 'src', '_data', 'site.json');
    const siteJson = JSON.parse(await fs.readFile(siteJsonPath, 'utf-8'));
    
    // Extract all links to process
    const allLinks = [
      ...siteJson.social_media.map(social => ({ 
        type: 'social',
        id: social.name.toLowerCase().replace(/\s+/g, '-'),
        url: social.url,
        name: social.name
      })),
      ...siteJson.links.map(link => ({ 
        type: 'link',
        id: link.name.toLowerCase().replace(/\s+/g, '-'),
        url: link.url,
        name: link.name,
        group: link.group
      })),
      ...siteJson.homepage.pinned_repositories.map(repo => ({
        type: 'repository',
        id: repo.name.toLowerCase().replace(/\s+/g, '-'),
        url: repo.url,
        name: repo.name
      }))
    ].filter(link => link.url.startsWith('http')); // Only process external links
    
    console.log(`Found ${allLinks.length} links to process`);
    
    // Process metadata for all links
    const metadataResults = await processInChunks(allLinks, async (link) => {
      const metadata = await getMetadata(link.url);
      return { ...link, metadata };
    });
    
    // Process screenshots for all successful metadata
    const screenshotResults = await processInChunks(
      metadataResults.filter(item => item.metadata?.status === 'success'),
      async (link) => {
        const screenshotPath = path.join(OUTPUT_DIR, 'screenshots', `${link.id}.jpg`);
        const screenshotResult = await takeScreenshot(link.url, screenshotPath);
        
        return { 
          ...link, 
          screenshot: screenshotResult.status === 'success' 
            ? `/assets/data/screenshots/${link.id}.jpg` 
            : null 
        };
      }
    );
    
    // Merge all results
    const processedLinks = {};
    
    for (const link of [...metadataResults, ...screenshotResults]) {
      if (!processedLinks[link.id]) {
        processedLinks[link.id] = {
          id: link.id,
          url: link.url,
          name: link.name,
          type: link.type,
          group: link.group,
          metadata: null,
          screenshot: null,
          last_checked: new Date().toISOString()
        };
      }
      
      if (link.metadata) {
        processedLinks[link.id].metadata = link.metadata;
      }
      
      if (link.screenshot) {
        processedLinks[link.id].screenshot = link.screenshot;
      }
    }
    
    // Save the results to a JSON file
    const outputPath = path.join(OUTPUT_DIR, 'link-previews.json');
    await fs.writeFile(outputPath, JSON.stringify(Object.values(processedLinks), null, 2));
    
    // Ensure screenshots directory is copied to assets
    const assetsScreenshotsDir = path.join(__dirname, 'assets', 'data', 'screenshots');
    await fs.mkdir(assetsScreenshotsDir, { recursive: true });
    
    // Copy all screenshots to assets directory
    const screenshotFiles = await fs.readdir(path.join(OUTPUT_DIR, 'screenshots'));
    for (const file of screenshotFiles) {
      const sourcePath = path.join(OUTPUT_DIR, 'screenshots', file);
      const destPath = path.join(assetsScreenshotsDir, file);
      await fs.copyFile(sourcePath, destPath);
    }
    
    console.log(`Successfully processed ${Object.keys(processedLinks).length} links!`);
    console.log(`Results saved to ${outputPath}`);
    
  } catch (error) {
    console.error('Error in main process:', error);
    process.exit(1);
  }
}

// Run the main function
main();