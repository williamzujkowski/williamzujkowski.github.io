/**
 * Incremental Data Converter
 *
 * Provides utilities for incrementally updating data files
 * rather than regenerating them completely
 */

import fs from "fs";
import path from "path";
import { performance } from "perf_hooks";

/**
 * Process a data file with incremental updates
 *
 * @param {Object} options - Options for processing
 * @param {string} options.sourceFilePath - Path to source data file
 * @param {string} options.targetFilePath - Path to target/output file
 * @param {Function} options.processor - Function to process each data item
 * @param {Function} options.identifier - Function to extract unique ID from item
 * @param {Function} options.shouldUpdate - Function to determine if item needs update
 * @param {boolean} options.forceRegenerate - Force regeneration of all items
 * @returns {Object} Statistics about the processing
 */
export async function updateDataIncrementally(options) {
  const {
    sourceFilePath,
    targetFilePath,
    processor,
    identifier = (item) => item.id || item.url,
    shouldUpdate = () => true,
    forceRegenerate = false,
  } = options;

  const startTime = performance.now();

  // Statistics
  const stats = {
    total: 0,
    updated: 0,
    skipped: 0,
    added: 0,
    removed: 0,
    processingTime: 0,
  };

  try {
    // Read source data
    const sourceData = JSON.parse(fs.readFileSync(sourceFilePath, "utf8"));
    stats.total = Array.isArray(sourceData)
      ? sourceData.length
      : Object.keys(sourceData).length;

    // Read existing target data if it exists
    let existingData;
    try {
      if (fs.existsSync(targetFilePath)) {
        existingData = JSON.parse(fs.readFileSync(targetFilePath, "utf8"));
      } else {
        // Create empty data structure matching source
        existingData = Array.isArray(sourceData) ? [] : {};
      }
    } catch (error) {
      console.warn(
        `Warning: Could not read existing data at ${targetFilePath}. Creating new file.`
      );
      existingData = Array.isArray(sourceData) ? [] : {};
    }

    // Process the data
    let resultData;

    if (Array.isArray(sourceData)) {
      // Array processing
      resultData = [];
      const existingMap = new Map();

      // Create a map of existing items by ID
      for (const item of existingData) {
        const id = identifier(item);
        if (id) {
          existingMap.set(id, item);
        }
      }

      // Process each source item
      for (const item of sourceData) {
        const id = identifier(item);
        const existing = id ? existingMap.get(id) : null;

        // Determine if this item should be updated
        if (!existing) {
          // New item
          const processedItem = await processor(item, null);
          resultData.push(processedItem);
          stats.added++;
        } else if (forceRegenerate || shouldUpdate(item, existing)) {
          // Item needs update
          const processedItem = await processor(item, existing);
          resultData.push(processedItem);
          stats.updated++;
          existingMap.delete(id);
        } else {
          // Item unchanged, use existing
          resultData.push(existing);
          stats.skipped++;
          existingMap.delete(id);
        }
      }

      // Count removed items (those in existing but not in source)
      stats.removed = existingMap.size;
    } else {
      // Object processing
      resultData = {};
      const sourceKeys = new Set(Object.keys(sourceData));
      const existingKeys = new Set(Object.keys(existingData));

      // Process each source item
      for (const key of sourceKeys) {
        const sourceItem = sourceData[key];
        const existingItem = existingData[key];

        // Determine if this item should be updated
        if (!existingItem) {
          // New item
          resultData[key] = await processor(sourceItem, null, key);
          stats.added++;
        } else if (forceRegenerate || shouldUpdate(sourceItem, existingItem, key)) {
          // Item needs update
          resultData[key] = await processor(sourceItem, existingItem, key);
          stats.updated++;
        } else {
          // Item unchanged, use existing
          resultData[key] = existingItem;
          stats.skipped++;
        }

        existingKeys.delete(key);
      }

      // Count removed items (those in existing but not in source)
      stats.removed = existingKeys.size;
    }

    // Save the result
    fs.writeFileSync(targetFilePath, JSON.stringify(resultData, null, 2));

    // Calculate total processing time
    stats.processingTime = performance.now() - startTime;

    return stats;
  } catch (error) {
    console.error(`Error in incremental data update:`, error);
    throw error;
  }
}

/**
 * Create an incremental processor for link previews
 *
 * @param {Function} metadataFetcher - Function to fetch metadata for a URL
 * @returns {Function} A configured updateDataIncrementally function
 */
export function createLinkPreviewProcessor(metadataFetcher) {
  return async (options) => {
    const { sourceFilePath, targetFilePath } = options;

    return updateDataIncrementally({
      sourceFilePath,
      targetFilePath,
      identifier: (item, key) => key || item.url,
      shouldUpdate: (sourceItem, existingItem) => {
        // Update if no metadata or if it's been more than a week
        if (!existingItem.metadata || !existingItem.lastUpdated) {
          return true;
        }

        const lastUpdated = new Date(existingItem.lastUpdated).getTime();
        const oneWeek = 7 * 24 * 60 * 60 * 1000;
        return Date.now() - lastUpdated > oneWeek;
      },
      processor: async (sourceItem, existingItem, key) => {
        // If we have a valid existing item, return it
        if (existingItem && existingItem.metadata && existingItem.lastUpdated) {
          return existingItem;
        }

        // Otherwise fetch new metadata
        const url = key || sourceItem.url;
        try {
          const metadata = await metadataFetcher(url);
          return {
            ...sourceItem,
            metadata,
            lastUpdated: new Date().toISOString(),
          };
        } catch (error) {
          console.error(`Error fetching metadata for ${url}:`, error.message);
          return {
            ...sourceItem,
            metadata: {
              status: "error",
              error: error.message,
            },
            lastUpdated: new Date().toISOString(),
          };
        }
      },
    });
  };
}

export default {
  updateDataIncrementally,
  createLinkPreviewProcessor,
};
