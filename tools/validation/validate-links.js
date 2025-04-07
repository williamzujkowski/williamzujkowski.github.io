/**
 * Link validation script
 * Used to check all links and ensure they are still valid
 * Run with: npm run validate:links
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import got from 'got';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Constants
const LINKS_DATA_PATH = path.join(__dirname, '..', '..', '_data', 'link-previews.json');
const OUTPUT_PATH = path.join(__dirname, '..', '..', '_data', 'link-validation-results.json');
const MAX_CONCURRENT = 3;

// Helper function to validate a URL
async function validateUrl(url) {
  try {
    console.log(`Validating ${url}...`);
    // Just check if the URL is accessible, don't download full content
    const response = await got.head(url, {
      timeout: 10000, // 10 second timeout
      followRedirect: true
    });
    
    return {
      url,
      status: 'valid',
      statusCode: response.statusCode,
      validatedAt: new Date().toISOString()
    };
  } catch (error) {
    console.error(`Error validating ${url}:`, error.message);
    return {
      url,
      status: 'invalid',
      statusCode: error.response?.statusCode || 'unknown',
      message: error.message,
      validatedAt: new Date().toISOString()
    };
  }
}

// Process URLs in chunks to avoid overloading
async function processInChunks(urls, chunkSize = MAX_CONCURRENT) {
  const results = [];
  
  for (let i = 0; i < urls.length; i += chunkSize) {
    const chunk = urls.slice(i, i + chunkSize);
    console.log(`Processing chunk ${i / chunkSize + 1} (${chunk.length} URLs)...`);
    
    const chunkResults = await Promise.all(
      chunk.map(url => validateUrl(url))
    );
    
    results.push(...chunkResults);
    
    // Add a small delay between chunks
    if (i + chunkSize < urls.length) {
      console.log('Pausing before next chunk...');
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
  
  return results;
}

// Main function
async function main() {
  try {
    // Check if the link previews file exists
    let linkPreviewsData;
    try {
      const linkPreviewsContent = await fs.readFile(LINKS_DATA_PATH, 'utf-8');
      linkPreviewsData = JSON.parse(linkPreviewsContent);
    } catch (error) {
      console.error('No link previews data found. Run build:links first.');
      process.exit(1);
    }
    
    // Extract URLs from link previews
    const urls = linkPreviewsData.map(item => item.url).filter(url => url.startsWith('http'));
    
    console.log(`Found ${urls.length} URLs to validate`);
    
    // Validate all URLs
    const validationResults = await processInChunks(urls);
    
    // Count results
    const validCount = validationResults.filter(r => r.status === 'valid').length;
    const invalidCount = validationResults.length - validCount;
    
    console.log(`Validation complete: ${validCount} valid, ${invalidCount} invalid`);
    
    // Update link previews data with validation results
    for (const item of linkPreviewsData) {
      const validationResult = validationResults.find(r => r.url === item.url);
      if (validationResult) {
        item.validation = validationResult;
        item.last_checked = validationResult.validatedAt;
      }
    }
    
    // Save updated link previews data
    await fs.writeFile(LINKS_DATA_PATH, JSON.stringify(linkPreviewsData, null, 2));
    
    // Save validation results separately for reference
    await fs.writeFile(OUTPUT_PATH, JSON.stringify({
      totalUrls: urls.length,
      validUrls: validCount,
      invalidUrls: invalidCount,
      results: validationResults,
      timestamp: new Date().toISOString()
    }, null, 2));
    
    console.log(`Results saved to ${OUTPUT_PATH}`);
    console.log(`Link preview data updated at ${LINKS_DATA_PATH}`);
    
    // Output summary of invalid URLs
    if (invalidCount > 0) {
      console.log('\nInvalid URLs:');
      validationResults
        .filter(r => r.status === 'invalid')
        .forEach(r => {
          console.log(`- ${r.url} (Status: ${r.statusCode}, Error: ${r.message})`);
        });
    }
    
  } catch (error) {
    console.error('Error validating links:', error);
    process.exit(1);
  }
}

// Run the main function
main();