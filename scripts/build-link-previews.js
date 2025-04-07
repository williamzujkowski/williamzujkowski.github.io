/**
 * This script pre-generates metadata and screenshots for links using Microlink open source tools
 * It runs during the build process to create a JSON file that can be used for link previews
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import metascraperAuthor from 'metascraper-author';
import metascraperDate from 'metascraper-date';
import metascraperDescription from 'metascraper-description';
import metascraperImage from 'metascraper-image';
import metascraperLogo from 'metascraper-logo';
import metascraperPublisher from 'metascraper-publisher';
import metascraperTitle from 'metascraper-title';
import metascraperUrl from 'metascraper-url';
import metascraper from 'metascraper';
import got from 'got';
import puppeteer from 'puppeteer';
import goto from '@browserless/goto';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize metascraper with rules
const metascraperWithRules = metascraper([
  metascraperAuthor(),
  metascraperDate(),
  metascraperDescription(),
  metascraperImage(),
  metascraperLogo(),
  metascraperPublisher(),
  metascraperTitle(),
  metascraperUrl()
]);

// Set screenshot dimensions
const VIEWPORT = { width: 1200, height: 675, deviceScaleFactor: 1 };
const SCREENSHOT_QUALITY = 80;
const OUTPUT_DIR = path.join(__dirname, '..', '_data');
const MAX_CONCURRENT = 3; // Maximum concurrent operations to avoid overloading

/**
 * Extract metadata from a URL using metascraper
 */
async function getMetadata(url) {
  try {
    console.log(`Fetching metadata for ${url}...`);
    const { body: html, url: finalUrl } = await got(url);
    const metadata = await metascraperWithRules({ html, url: finalUrl });
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
  // Check for command line arguments
  const args = process.argv.slice(2);
  const forceInitialRun = args.includes('--initial');
  try {
    // Create output directory if it doesn't exist
    await fs.mkdir(path.join(OUTPUT_DIR, 'screenshots'), { recursive: true });
    
    // Read site configuration with links
    const siteJsonPath = path.join(__dirname, '..', 'src', '_data', 'site.json');
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
    
    // Check if we already have processed links data
    let existingLinks = [];
    const outputPath = path.join(OUTPUT_DIR, 'link-previews.json');
    
    try {
      const existingData = await fs.readFile(outputPath, 'utf-8');
      const parsedData = JSON.parse(existingData);
      // Ensure the data is an array
      existingLinks = Array.isArray(parsedData) ? parsedData : [];
      console.log(`Found existing data for ${existingLinks.length} links`);
    } catch (error) {
      console.log('No existing link data found, will process all links');
      existingLinks = [];
    }
    
    // Determine which links to process
    const isInitialRun = existingLinks.length === 0 || forceInitialRun;
    let linksToProcess;
    
    if (isInitialRun) {
      // Process all links on initial run
      linksToProcess = allLinks;
      console.log('Initial run - processing all links');
    } else {
      // Create a map for quick lookup of link IDs in all links
      const allLinksMap = new Map(allLinks.map(link => [link.id, link]));
      
      // Create a map of existing links
      const existingLinksMap = new Map(existingLinks.map(link => [link.id, link]));
      
      // Find new links that don't exist in our data
      const newLinks = allLinks.filter(link => !existingLinksMap.has(link.id));
      console.log(`Found ${newLinks.length} new links to process`);
      
      // Find the 10 oldest links by last_checked date
      const oldestLinks = [...existingLinks]
        .filter(link => allLinksMap.has(link.id)) // Only consider links that still exist
        .sort((a, b) => {
          // Sort by last_checked date
          const dateA = a.last_checked ? new Date(a.last_checked) : new Date(0);
          const dateB = b.last_checked ? new Date(b.last_checked) : new Date(0);
          return dateA - dateB;
        })
        .slice(0, 10)
        .map(link => {
          // Map to current link data
          const currentLink = allLinksMap.get(link.id);
          return {
            ...currentLink,
            previousData: link
          };
        });
      
      console.log(`Refreshing data for ${oldestLinks.length} oldest links`);
      
      // Combine new links and oldest links
      linksToProcess = [...newLinks, ...oldestLinks];
      console.log(`Total links to process: ${linksToProcess.length}`);
    }
    
    if (linksToProcess.length === 0) {
      console.log('No links to process at this time');
      return;
    }
    
    // Process metadata for selected links
    const metadataResults = await processInChunks(linksToProcess, async (link) => {
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
          group: link.group || (link.previousData ? link.previousData.group : null),
          metadata: link.previousData ? link.previousData.metadata : null,
          screenshot: link.previousData ? link.previousData.screenshot : null,
          last_checked: link.previousData ? link.previousData.last_checked : new Date().toISOString()
        };
      }
      
      if (link.metadata) {
        processedLinks[link.id].metadata = link.metadata;
        processedLinks[link.id].last_checked = new Date().toISOString();
      }
      
      if (link.screenshot) {
        processedLinks[link.id].screenshot = link.screenshot;
        processedLinks[link.id].last_checked = new Date().toISOString();
      }
    }
    
    // Final link data by combining existing and newly processed links
    let finalLinkData;
    
    if (isInitialRun) {
      // Use all processed links for initial run
      finalLinkData = Object.values(processedLinks);
    } else {
      // Create a map of newly processed links
      const processedLinksMap = new Map(Object.entries(processedLinks));
      
      // Update existing links with new data
      const updatedExistingLinks = existingLinks.map(link => {
        if (processedLinksMap.has(link.id)) {
          return processedLinksMap.get(link.id);
        }
        return link;
      });
      
      // Add any new links that don't exist in updated list
      const updatedLinkIds = new Set(updatedExistingLinks.map(link => link.id));
      const additionalNewLinks = Object.values(processedLinks).filter(link => !updatedLinkIds.has(link.id));
      
      finalLinkData = [...updatedExistingLinks, ...additionalNewLinks];
    }
    
    // Save the results to a JSON file
    await fs.writeFile(outputPath, JSON.stringify(finalLinkData, null, 2));
    
    // Ensure screenshots directory is copied to assets
    const assetsScreenshotsDir = path.join(__dirname, '..', 'assets', 'data', 'screenshots');
    await fs.mkdir(assetsScreenshotsDir, { recursive: true });
    
    // Copy all screenshots to assets directory
    try {
      const screenshotFiles = await fs.readdir(path.join(OUTPUT_DIR, 'screenshots'));
      for (const file of screenshotFiles) {
        const sourcePath = path.join(OUTPUT_DIR, 'screenshots', file);
        const destPath = path.join(assetsScreenshotsDir, file);
        await fs.copyFile(sourcePath, destPath);
      }
    } catch (error) {
      console.error('Error copying screenshots:', error.message);
    }
    
    console.log(`Successfully processed ${Object.keys(processedLinks).length} links!`);
    console.log(`Total links in data: ${finalLinkData.length}`);
    console.log(`Results saved to ${outputPath}`);
    
  } catch (error) {
    console.error('Error in main process:', error);
    process.exit(1);
  }
}

// Run the main function
main();