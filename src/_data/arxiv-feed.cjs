// src/_data/arxiv-feed.cjs
// Enhanced data loader for arxiv-feed.json

const fs = require("fs");
const path = require("path");

// In-memory cache for data
const cache = {
  data: null,
  timestamp: 0,
  ttl: 60 * 1000, // 1 minute TTL
};

module.exports = function () {
  // Check if we have a valid cached version
  const now = Date.now();
  if (cache.data && now - cache.timestamp < cache.ttl) {
    return cache.data;
  }

  // Try to load from different locations with fallbacks
  const dataPaths = [
    // Primary location
    path.join(__dirname, "..", "..", "_data", "arxiv-feed.json"),
    // Fallback locations
    path.join(__dirname, "..", "..", "assets", "data", "arxiv-feed.json"),
    path.join(__dirname, "arxiv-feed.json"),
  ];

  for (const dataPath of dataPaths) {
    try {
      if (fs.existsSync(dataPath)) {
        // Read and parse the JSON file
        const fileContents = fs.readFileSync(dataPath, "utf8");
        const data = JSON.parse(fileContents);

        // Cache the data
        cache.data = data;
        cache.timestamp = now;

        return data;
      }
    } catch (error) {
      // Try next data path
      console.warn(`Warning: Failed to load arxiv-feed.json from ${dataPath}`);
    }
  }

  // No data found, return empty array
  console.warn("Warning: No arxiv-feed.json found in any location. Using empty array.");
  return [];
};
