/**
 * This script forces an update of link previews for all or specific links
 * It's designed to be run manually when you want to refresh the previews
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const LINK_PREVIEWS_PATH = path.join(__dirname, '../../_data/link-previews.json');
const ROOT_DIR = path.join(__dirname, '../..');

async function main() {
  try {
    // Parse command line arguments
    const args = process.argv.slice(2);
    const specificLinks = args.filter(arg => !arg.startsWith('--'));
    const force = args.includes('--force');
    const limit = args.find(arg => arg.startsWith('--limit='))?.split('=')[1];
    const limitNumber = limit ? parseInt(limit, 10) : null;
    const missing = args.includes('--missing');
    
    console.log(`
-----------------------------------------------
🌐 FORCE UPDATE LINK PREVIEWS
-----------------------------------------------
`);
    
    // Check if the link previews file exists
    let linkData = [];
    try {
      const data = await fs.readFile(LINK_PREVIEWS_PATH, 'utf8');
      linkData = JSON.parse(data);
      console.log(`Found ${linkData.length} existing link previews`);
    } catch (error) {
      console.error('Could not read existing link previews:', error.message);
      console.log('Starting with empty dataset');
    }
    
    // Determine which links to update
    let linksToUpdate = [];
    
    if (specificLinks.length > 0) {
      // Filter the links by name or URL
      linksToUpdate = linkData.filter(link => {
        return specificLinks.some(term => 
          link.name.toLowerCase().includes(term.toLowerCase()) || 
          link.url.toLowerCase().includes(term.toLowerCase())
        );
      });
      
      console.log(`Found ${linksToUpdate.length} links matching your criteria`);
    } else if (missing) {
      // Find links with missing screenshots or metadata
      linksToUpdate = linkData.filter(link => 
        !link.screenshot || 
        !link.metadata || 
        link.metadata.status === 'error'
      );
      
      console.log(`Found ${linksToUpdate.length} links with missing data`);
    } else if (limitNumber) {
      // Take the oldest N links
      linksToUpdate = [...linkData]
        .sort((a, b) => {
          const dateA = a.last_checked ? new Date(a.last_checked) : new Date(0);
          const dateB = b.last_checked ? new Date(b.last_checked) : new Date(0);
          return dateA - dateB;
        })
        .slice(0, limitNumber);
      
      console.log(`Taking ${linksToUpdate.length} oldest links to update`);
    } else if (force) {
      // Update all links
      linksToUpdate = linkData;
      console.log(`Force updating all ${linksToUpdate.length} links`);
    } else {
      console.log(`
Usage:
  node tools/link-preview-tools/force-update-link-previews.js [options] [search terms]

Options:
  --force        Update all links
  --limit=N      Update the N oldest links
  --missing      Update links with missing screenshots or metadata
  
Examples:
  node tools/link-preview-tools/force-update-link-previews.js --force
  node tools/link-preview-tools/force-update-link-previews.js --limit=10
  node tools/link-preview-tools/force-update-link-previews.js --missing
  node tools/link-preview-tools/force-update-link-previews.js github youtube

No action taken. Please specify what to update.
`);
      process.exit(0);
    }
    
    if (linksToUpdate.length === 0) {
      console.log('No links to update. Exiting.');
      process.exit(0);
    }
    
    // Create a temporary file with links to update
    const tempFilePath = path.join(__dirname, 'temp-links-to-update.json');
    await fs.writeFile(tempFilePath, JSON.stringify(linksToUpdate, null, 2));
    
    console.log('Running build-link-previews.js with only selected links...');
    
    try {
      // Run the build-link-previews script with environment variables to control processing
      execSync(`LINK_PREVIEW_INPUT=${tempFilePath} LINK_PREVIEW_FORCE=true node ${path.join(ROOT_DIR, 'scripts/build-link-previews.js')}`, {
        stdio: 'inherit'
      });
      
      console.log('\n✅ Link preview update complete!');
    } catch (error) {
      console.error('\n❌ Error running build-link-previews.js:', error.message);
    } finally {
      // Clean up temporary file
      try {
        await fs.unlink(tempFilePath);
      } catch (error) {
        console.warn('Could not delete temporary file:', error.message);
      }
    }
  } catch (error) {
    console.error('Unexpected error:', error);
    process.exit(1);
  }
}

main();