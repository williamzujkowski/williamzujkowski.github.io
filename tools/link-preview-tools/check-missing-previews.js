/**
 * This script checks for links that are missing preview images or have error status
 * It generates a report and can help identify which links need attention
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const LINK_PREVIEWS_PATH = path.join(__dirname, '../../_data/link-previews.json');
const SCREENSHOTS_DIR = path.join(__dirname, '../../_data/screenshots');
const ASSETS_SCREENSHOTS_DIR = path.join(__dirname, '../../assets/data/screenshots');

async function main() {
  try {
    console.log(`
------------------------------------------
📊 LINK PREVIEW STATUS REPORT
------------------------------------------
`);
    
    // Load link preview data
    let linkData = [];
    try {
      const data = await fs.readFile(LINK_PREVIEWS_PATH, 'utf8');
      linkData = JSON.parse(data);
      console.log(`Found ${linkData.length} links in the preview data`);
    } catch (error) {
      console.error('Could not read link preview data:', error.message);
      process.exit(1);
    }
    
    // Check for screenshots directory
    let screenshotFiles = [];
    try {
      screenshotFiles = await fs.readdir(SCREENSHOTS_DIR);
      console.log(`Found ${screenshotFiles.length} screenshot files in _data/screenshots`);
    } catch (error) {
      console.warn('Could not read screenshots directory:', error.message);
    }
    
    // Check for assets screenshots directory
    let assetsScreenshotFiles = [];
    try {
      assetsScreenshotFiles = await fs.readdir(ASSETS_SCREENSHOTS_DIR);
      console.log(`Found ${assetsScreenshotFiles.length} screenshot files in assets/data/screenshots`);
    } catch (error) {
      console.warn('Could not read assets screenshots directory:', error.message);
    }
    
    // Create sets for easy checking
    const screenshotFilesSet = new Set(screenshotFiles);
    const assetsScreenshotFilesSet = new Set(assetsScreenshotFiles);
    
    // Analyze link data
    const missingScreenshots = [];
    const metadataErrors = [];
    const filesMissingInAssets = [];
    const unreferencedScreenshots = [];
    const oldLinks = [];
    
    // Current date for age calculation
    const now = new Date();
    const threeMonthsAgo = new Date();
    threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
    
    // Analyze each link
    for (const link of linkData) {
      // Check for missing screenshots
      if (!link.screenshot) {
        missingScreenshots.push(link);
      } else {
        // Extract filename from screenshot path
        const filename = link.screenshot.split('/').pop();
        
        // Check if screenshot exists in data dir but not in assets
        if (screenshotFilesSet.has(filename) && !assetsScreenshotFilesSet.has(filename)) {
          filesMissingInAssets.push({
            link: link.name,
            url: link.url,
            filename
          });
        }
      }
      
      // Check for metadata errors
      if (!link.metadata || link.metadata.status === 'error') {
        metadataErrors.push(link);
      }
      
      // Check for old links (not updated in 3+ months)
      if (link.last_checked) {
        const lastCheckedDate = new Date(link.last_checked);
        if (lastCheckedDate < threeMonthsAgo) {
          oldLinks.push({
            ...link,
            age: Math.round((now - lastCheckedDate) / (1000 * 60 * 60 * 24)) // Age in days
          });
        }
      } else {
        // No last_checked date, consider it old
        oldLinks.push({
          ...link,
          age: 'unknown'
        });
      }
    }
    
    // Find unreferenced screenshots
    const referencedFilenames = new Set(
      linkData
        .filter(link => link.screenshot)
        .map(link => link.screenshot.split('/').pop())
    );
    
    for (const filename of screenshotFiles) {
      if (!referencedFilenames.has(filename)) {
        unreferencedScreenshots.push(filename);
      }
    }
    
    // Sort old links by age
    oldLinks.sort((a, b) => {
      if (a.age === 'unknown') return -1;
      if (b.age === 'unknown') return 1;
      return b.age - a.age;
    });
    
    // Generate report
    console.log('\n===== REPORT =====\n');
    
    console.log(`Total links: ${linkData.length}`);
    console.log(`Links missing screenshots: ${missingScreenshots.length}`);
    console.log(`Links with metadata errors: ${metadataErrors.length}`);
    console.log(`Links not updated in 3+ months: ${oldLinks.length}`);
    console.log(`Screenshot files missing in assets: ${filesMissingInAssets.length}`);
    console.log(`Unreferenced screenshot files: ${unreferencedScreenshots.length}`);
    
    // Print detailed information
    if (missingScreenshots.length > 0) {
      console.log('\n----- LINKS MISSING SCREENSHOTS -----');
      missingScreenshots.forEach(link => {
        console.log(`- ${link.name} (${link.url})`);
      });
    }
    
    if (metadataErrors.length > 0) {
      console.log('\n----- LINKS WITH METADATA ERRORS -----');
      metadataErrors.forEach(link => {
        const errorMsg = link.metadata?.message || 'Unknown error';
        console.log(`- ${link.name} (${link.url}): ${errorMsg}`);
      });
    }
    
    if (oldLinks.length > 0) {
      console.log('\n----- OLD LINKS (3+ MONTHS) -----');
      // Show top 10 oldest links
      oldLinks.slice(0, 10).forEach(link => {
        const age = link.age === 'unknown' ? 'unknown age' : `${link.age} days old`;
        console.log(`- ${link.name} (${link.url}): ${age}`);
      });
      if (oldLinks.length > 10) {
        console.log(`... and ${oldLinks.length - 10} more`);
      }
    }
    
    if (filesMissingInAssets.length > 0) {
      console.log('\n----- FILES MISSING IN ASSETS DIR -----');
      filesMissingInAssets.forEach(item => {
        console.log(`- ${item.filename} (for ${item.link})`);
      });
    }
    
    if (unreferencedScreenshots.length > 0) {
      console.log('\n----- UNREFERENCED SCREENSHOTS -----');
      unreferencedScreenshots.forEach(filename => {
        console.log(`- ${filename}`);
      });
    }
    
    // Copy missing files if any
    if (filesMissingInAssets.length > 0) {
      console.log('\nCopying missing files to assets directory...');
      
      let copyCount = 0;
      for (const item of filesMissingInAssets) {
        try {
          const sourcePath = path.join(SCREENSHOTS_DIR, item.filename);
          const destPath = path.join(ASSETS_SCREENSHOTS_DIR, item.filename);
          await fs.copyFile(sourcePath, destPath);
          copyCount++;
        } catch (error) {
          console.error(`Error copying ${item.filename}:`, error.message);
        }
      }
      
      console.log(`Copied ${copyCount} files to assets directory`);
    }
    
    // Print suggestions
    console.log('\n===== SUGGESTIONS =====\n');
    
    if (missingScreenshots.length > 0 || metadataErrors.length > 0) {
      console.log('To fix missing screenshots and metadata errors, run:');
      console.log('node tools/link-preview-tools/force-update-link-previews.js --missing');
    }
    
    if (oldLinks.length > 0) {
      console.log('To update the oldest links, run:');
      console.log('node tools/link-preview-tools/force-update-link-previews.js --limit=20');
    }
    
    if (unreferencedScreenshots.length > 0) {
      console.log('To clean up unreferenced screenshots, you can manually delete them from:');
      console.log('_data/screenshots/ and assets/data/screenshots/');
    }
    
    console.log('\n✅ Report complete');
  } catch (error) {
    console.error('Unexpected error:', error);
    process.exit(1);
  }
}

main();