/**
 * Screenshot generator index module
 * Provides a unified interface for screenshot functionality
 */

import { generateScreenshots } from './generate-screenshots.js';
export * from './utils.js';

/**
 * Main screenshot generation API
 */
export {
  generateScreenshots
};

/**
 * Generate screenshots for a batch of links
 * @param {number} startIndex - Index to start processing from
 * @param {number} count - Number of links to process
 */
export async function generateBatch(startIndex = 0, count = 20) {
  return generateScreenshots({ startIndex, count });
}

/**
 * Generate screenshots for all links without screenshots
 */
export async function generateMissing() {
  return generateScreenshots({ count: 1000 });
}

/**
 * Force refresh all screenshots
 */
export async function refreshAll() {
  return generateScreenshots({ 
    updateAll: true, 
    forceRefresh: true,
    count: 1000
  });
}

// Default export for convenience
export default {
  generateScreenshots,
  generateBatch,
  generateMissing,
  refreshAll
};