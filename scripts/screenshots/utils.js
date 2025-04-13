/**
 * Screenshot utilities for link preview generation
 * Provides common functions used by the screenshot generators
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

// Set up __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Default configuration for screenshot generation
 */
export const DEFAULT_CONFIG = {
  // Screenshot settings
  viewport: { width: 1200, height: 675, deviceScaleFactor: 1 },
  quality: 70, // Lower quality (0-100) = faster processing, smaller files
  fullPage: false,
  
  // Performance settings
  concurrency: Math.max(1, Math.min(os.cpus().length - 1, 4)), // Use up to N-1 CPU cores, max 4
  batchSize: 10, // How many links to process before saving
  pageTimeout: 20000, // Reduce timeout for faster failures (20 seconds)
  
  // Path settings
  outputDir: path.join(__dirname, '..', '..', 'assets', 'data', 'screenshots'),
  cacheDir: path.join(__dirname, '..', '..', '.cache', 'screenshots'),
  metadataFile: path.join(__dirname, '..', '..', 'assets', 'data', 'link-previews.json'),
  
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

/**
 * Check if a URL should be skipped based on domain patterns
 */
export function shouldSkipUrl(url, skipDomains = DEFAULT_CONFIG.skipDomains) {
  try {
    const urlObj = new URL(url);
    return skipDomains.some(domain => urlObj.hostname.includes(domain));
  } catch (error) {
    console.warn(`Invalid URL: ${url}`);
    return true;
  }
}

/**
 * Create necessary directories for screenshot generation
 */
export async function ensureDirectories(config = DEFAULT_CONFIG) {
  await fs.mkdir(config.outputDir, { recursive: true });
  await fs.mkdir(config.cacheDir, { recursive: true });
}

/**
 * Load link metadata from JSON file
 */
export async function loadLinkMetadata(metadataPath = DEFAULT_CONFIG.metadataFile) {
  try {
    const data = await fs.readFile(metadataPath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Failed to read metadata file:', error.message);
    return [];
  }
}

/**
 * Filter links for processing based on criteria
 */
export function filterLinks(links, options = {}) {
  const { updateAll, forceRefresh, skipDomains } = options;
  
  return links.filter(link => {
    if (!link.url || !link.id) {
      console.log(`Skipping invalid link:`, link);
      return false;
    }
    
    if (shouldSkipUrl(link.url, skipDomains)) {
      console.log(`Skipping blocked domain: ${link.url}`);
      return false;
    }
    
    if (!updateAll && !forceRefresh && link.screenshot) {
      // Skip links that already have screenshots unless force refreshing
      return false;
    }
    
    return true;
  });
}

/**
 * Save link metadata to JSON file
 */
export async function saveLinkMetadata(metadata, metadataPath = DEFAULT_CONFIG.metadataFile) {
  // Write directly to assets/data only - no longer copying to _data
  await fs.writeFile(metadataPath, JSON.stringify(metadata, null, 2));
  console.log(`Link metadata saved to ${metadataPath}`);
}

/**
 * Generate a performance report for screenshot generation
 */
export function generateReport(results) {
  const duration = (results.endTime - results.startTime) / 1000;
  const avgTimePerLink = duration / results.total;
  
  return {
    totalLinks: results.total,
    successful: results.success,
    failed: results.failed,
    successRate: Math.round((results.success / results.total) * 100),
    totalTime: duration.toFixed(2),
    averageTimePerLink: avgTimePerLink.toFixed(2)
  };
}