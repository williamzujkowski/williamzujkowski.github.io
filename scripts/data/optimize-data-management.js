/**
 * Data Management Optimization
 *
 * This script implements smart caching and optimization for
 * external data sources to reduce build times and payload sizes.
 */

import fs from "fs";
import path from "path";
import crypto from "crypto";
import { performance } from "perf_hooks";

// Configuration
const CONFIG = {
  dataDir: path.resolve(process.cwd(), "_data"),
  publicDataDir: path.resolve(process.cwd(), "assets/data"),
  cacheDir: path.resolve(process.cwd(), "_data/.cache"),
  dataManifestPath: path.resolve(process.cwd(), "_data/.cache/data-manifest.json"),
  compressionThreshold: 1024 * 10, // 10KB
  // Data sources that should be optimized (add more as needed)
  dataSources: [
    {
      name: "arxiv-feed.json",
      ttl: 24 * 60 * 60 * 1000, // 24 hours in ms
      compression: true,
      incremental: true,
    },
    {
      name: "books.json",
      ttl: 7 * 24 * 60 * 60 * 1000, // 7 days in ms
      compression: true,
      incremental: false,
    },
    {
      name: "current-reading.json",
      ttl: 24 * 60 * 60 * 1000, // 24 hours in ms
      compression: false,
      incremental: false,
    },
    {
      name: "github-pins.json",
      ttl: 6 * 60 * 60 * 1000, // 6 hours in ms
      compression: true,
      incremental: true,
    },
    {
      name: "contribution-heatmap.json",
      ttl: 24 * 60 * 60 * 1000, // 24 hours
      compression: true,
      incremental: true,
    },
    {
      pattern: "link-previews*.json",
      ttl: 7 * 24 * 60 * 60 * 1000, // 7 days
      compression: true,
      incremental: true,
    },
  ],
};

// Stats tracking
const stats = {
  processed: 0,
  updated: 0,
  cached: 0,
  compressedSize: 0,
  originalSize: 0,
};

/**
 * Initialize data optimization system
 */
function init() {
  // Create cache directory if it doesn't exist
  if (!fs.existsSync(CONFIG.cacheDir)) {
    fs.mkdirSync(CONFIG.cacheDir, { recursive: true });
  }

  // Create data manifest if it doesn't exist
  if (!fs.existsSync(CONFIG.dataManifestPath)) {
    fs.writeFileSync(
      CONFIG.dataManifestPath,
      JSON.stringify({
        lastRun: Date.now(),
        files: {},
      })
    );
  }
}

/**
 * Load existing data manifest
 */
function loadManifest() {
  try {
    const content = fs.readFileSync(CONFIG.dataManifestPath, "utf8");
    return JSON.parse(content);
  } catch (error) {
    console.warn("Warning: Failed to load data manifest, creating new one");
    return { lastRun: Date.now(), files: {} };
  }
}

/**
 * Save updated manifest
 */
function saveManifest(manifest) {
  fs.writeFileSync(CONFIG.dataManifestPath, JSON.stringify(manifest, null, 2));
}

/**
 * Compute hash of file contents
 */
function computeFileHash(filePath) {
  try {
    const content = fs.readFileSync(filePath);
    return crypto.createHash("md5").update(content).digest("hex");
  } catch (error) {
    console.error(`Error computing hash for ${filePath}:`, error.message);
    return null;
  }
}

/**
 * Determine if a data file needs updating based on
 * - File modified time
 * - Content hash comparison
 * - TTL configuration
 */
function needsUpdate(sourceInfo, filePath, manifest) {
  // If file doesn't exist, it needs updating
  if (!fs.existsSync(filePath)) {
    return true;
  }

  const stats = fs.statSync(filePath);
  const fileInfo = manifest.files[filePath];

  // If no previous info, needs update
  if (!fileInfo) {
    return true;
  }

  // Check TTL expiration
  const now = Date.now();
  if (now - fileInfo.lastProcessed > sourceInfo.ttl) {
    return true;
  }

  // Check if file has been modified
  if (stats.mtimeMs > fileInfo.lastModified) {
    // Compute current hash
    const currentHash = computeFileHash(filePath);

    // If hash changed, needs update
    if (currentHash !== fileInfo.contentHash) {
      return true;
    }
  }

  return false;
}

/**
 * Compress JSON data by removing unnecessary whitespace
 * and optionally removing null fields
 */
function compressJsonData(data, removeNulls = true) {
  if (removeNulls) {
    // Remove null/undefined values to reduce payload size
    const removeNullsFromObject = (obj) => {
      Object.keys(obj).forEach((key) => {
        if (obj[key] === null || obj[key] === undefined) {
          delete obj[key];
        } else if (typeof obj[key] === "object" && obj[key] !== null) {
          if (Array.isArray(obj[key])) {
            obj[key] = obj[key].filter((item) => item !== null && item !== undefined);
            obj[key].forEach((item) => {
              if (typeof item === "object" && item !== null) {
                removeNullsFromObject(item);
              }
            });
          } else {
            removeNullsFromObject(obj[key]);
          }
        }
      });
      return obj;
    };

    if (Array.isArray(data)) {
      data = data.filter((item) => item !== null && item !== undefined);
      data.forEach((item) => {
        if (typeof item === "object" && item !== null) {
          removeNullsFromObject(item);
        }
      });
    } else if (typeof data === "object" && data !== null) {
      data = removeNullsFromObject(data);
    }
  }

  // Serialize with no whitespace
  return JSON.stringify(data);
}

/**
 * Process a single data file
 */
async function processDataFile(sourceInfo, filePath, manifest) {
  console.log(`Processing ${path.basename(filePath)}...`);
  stats.processed++;

  try {
    // Check if file needs updating
    if (!needsUpdate(sourceInfo, filePath, manifest)) {
      console.log(`  • Using cached version of ${path.basename(filePath)}`);
      stats.cached++;
      return false;
    }

    // Read and parse the file
    const content = fs.readFileSync(filePath, "utf8");
    const data = JSON.parse(content);

    // Measure original size
    const originalSize = Buffer.byteLength(content);
    stats.originalSize += originalSize;

    // Optimize the data if needed
    let optimizedContent;

    if (sourceInfo.compression && originalSize > CONFIG.compressionThreshold) {
      // Compress the data
      optimizedContent = compressJsonData(data);
      const compressedSize = Buffer.byteLength(optimizedContent);
      stats.compressedSize += compressedSize;

      console.log(
        `  • Compressed ${path.basename(filePath)}: ${formatBytes(originalSize)} → ${formatBytes(compressedSize)} (${Math.round((1 - compressedSize / originalSize) * 100)}% reduction)`
      );
    } else {
      // Just minify without removing nulls
      optimizedContent = JSON.stringify(data);
      stats.compressedSize += Buffer.byteLength(optimizedContent);
    }

    // Write optimized data to destination directory
    const publicPath = path.join(CONFIG.publicDataDir, path.basename(filePath));
    fs.writeFileSync(publicPath, optimizedContent);

    // Keep a properly formatted version in _data for development
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));

    // Update manifest information
    manifest.files[filePath] = {
      lastProcessed: Date.now(),
      lastModified: fs.statSync(filePath).mtimeMs,
      contentHash: computeFileHash(filePath),
      optimizedSize: Buffer.byteLength(optimizedContent),
      originalSize,
    };

    stats.updated++;
    return true;
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
    return false;
  }
}

/**
 * Process link preview files (which follow a pattern)
 */
async function processLinkPreviewFiles(sourceInfo, manifest) {
  const pattern = sourceInfo.pattern;
  const baseName = pattern.replace("*", "");

  // Find all matching files in the data directory
  const files = fs
    .readdirSync(CONFIG.dataDir)
    .filter((file) => file.startsWith(baseName) && file.endsWith(".json"));

  console.log(`Found ${files.length} link preview files matching ${pattern}`);

  for (const file of files) {
    const filePath = path.join(CONFIG.dataDir, file);
    await processDataFile(sourceInfo, filePath, manifest);
  }
}

/**
 * Format bytes into a human-readable string
 */
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
}

/**
 * Process all configured data sources
 */
async function optimizeData() {
  const startTime = performance.now();
  console.log("🔄 Starting data optimization...");

  // Initialize system
  init();

  // Load manifest
  const manifest = loadManifest();
  manifest.lastRun = Date.now();

  // Process each configured data source
  for (const sourceInfo of CONFIG.dataSources) {
    if (sourceInfo.pattern) {
      // Handle pattern-based sources (like link previews)
      await processLinkPreviewFiles(sourceInfo, manifest);
    } else {
      // Handle named files
      const filePath = path.join(CONFIG.dataDir, sourceInfo.name);
      await processDataFile(sourceInfo, filePath, manifest);
    }
  }

  // Save updated manifest
  saveManifest(manifest);

  // Print summary
  const duration = performance.now() - startTime;
  console.log("\n✅ Data optimization complete:");
  console.log(`  • Files processed: ${stats.processed}`);
  console.log(`  • Files updated: ${stats.updated}`);
  console.log(`  • Files cached: ${stats.cached}`);

  if (stats.compressedSize > 0 && stats.originalSize > 0) {
    const reduction = Math.round((1 - stats.compressedSize / stats.originalSize) * 100);
    console.log(
      `  • Size reduction: ${formatBytes(stats.originalSize)} → ${formatBytes(stats.compressedSize)} (${reduction}%)`
    );
  }

  console.log(`  • Completed in ${duration.toFixed(2)}ms`);
}

// Run the optimization
optimizeData().catch((error) => {
  console.error("Fatal error during data optimization:", error);
  process.exit(1);
});
