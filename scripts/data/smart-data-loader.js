/**
 * Smart Data Loader
 *
 * A better data loading module that uses more efficient loading techniques
 * and includes caching for Eleventy data files
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Get the directory name for the current file
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Configuration
const DATA_DIR = path.resolve(process.cwd(), "_data");
const PUBLIC_DATA_DIR = path.resolve(process.cwd(), "assets/data");

// In-memory cache for data files
const dataCache = new Map();

/**
 * Load a JSON data file with intelligent caching
 *
 * @param {string} filename - Name of the data file
 * @param {Object} options - Options for loading
 * @param {boolean} options.usePublic - Whether to load from public data
 * @param {boolean} options.cache - Whether to cache the data
 * @param {number} options.ttl - Time to live for cache in milliseconds
 * @returns {Object|Array} The parsed data
 */
export function loadData(filename, options = {}) {
  const {
    usePublic = process.env.NODE_ENV === "production",
    cache = true,
    ttl = 5 * 60 * 1000, // 5 minutes default TTL
  } = options;

  const cacheKey = `${filename}:${usePublic ? "public" : "internal"}`;

  // Check cache first
  if (cache && dataCache.has(cacheKey)) {
    const cachedData = dataCache.get(cacheKey);

    // Check if cache is still valid
    if (Date.now() < cachedData.expiry) {
      return cachedData.data;
    }

    // Cache expired, remove it
    dataCache.delete(cacheKey);
  }

  // Determine file path
  const filePath = path.join(usePublic ? PUBLIC_DATA_DIR : DATA_DIR, filename);

  try {
    // Check if file exists
    if (!fs.existsSync(filePath)) {
      console.warn(
        `Warning: ${filename} not found at ${filePath}. Returning empty data.`
      );
      return filename.includes("link-previews") ? {} : [];
    }

    // Read and parse data
    const contents = fs.readFileSync(filePath, "utf8");
    const data = JSON.parse(contents);

    // Cache the data if requested
    if (cache) {
      dataCache.set(cacheKey, {
        data,
        expiry: Date.now() + ttl,
      });
    }

    return data;
  } catch (error) {
    console.error(`Error loading data from ${filePath}:`, error.message);
    return filename.includes("link-previews") ? {} : [];
  }
}

/**
 * Get a specific data item by key from a JSON data file
 *
 * @param {string} filename - Name of the data file
 * @param {string} key - The key to look up
 * @param {*} defaultValue - Default value if key not found
 * @param {Object} options - Loading options
 * @returns {*} The value for the key or defaultValue
 */
export function getDataItem(filename, key, defaultValue = null, options = {}) {
  const data = loadData(filename, options);

  if (typeof data !== "object" || data === null) {
    return defaultValue;
  }

  return key in data ? data[key] : defaultValue;
}

/**
 * Load preview data for a specific URL
 *
 * @param {string} url - The URL to get preview data for
 * @param {Object} options - Options for loading
 * @returns {Object} The preview data or null if not found
 */
export function getPreviewByUrl(url, options = {}) {
  // Try to load from the main previews file first
  const allPreviews = loadData("link-previews.json", options);

  if (allPreviews[url]) {
    return allPreviews[url];
  }

  // Look in category-specific previews
  const categories = [
    "art_culture__exploration",
    "artists",
    "blogs",
    "creative",
    "fun__curiosities",
    "gaming",
    "miscellaneous",
    "music",
    "people",
    "projects",
    "retrocomputing",
    "rollerblading",
    "social",
    "technology__innovation",
  ];

  for (const category of categories) {
    try {
      const categoryPreviews = loadData(`link-previews-${category}.json`, options);
      if (categoryPreviews[url]) {
        return categoryPreviews[url];
      }
    } catch (error) {
      // Continue to next category
    }
  }

  return null;
}

/**
 * Clear all cached data
 */
export function clearCache() {
  dataCache.clear();
}

/**
 * Create a CommonJS wrapper for this module
 * This enables compatibility with both ESM and CommonJS
 */
export function createCommonJSDataLoader(filename) {
  return function () {
    return loadData(filename, {
      usePublic: false, // Always use internal data for Eleventy
      cache: true,
      ttl: 60 * 1000, // 1 minute cache for Eleventy data functions
    });
  };
}

// Default export for CommonJS compatibility
export default {
  loadData,
  getDataItem,
  getPreviewByUrl,
  clearCache,
  createCommonJSDataLoader,
};
