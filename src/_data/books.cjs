// src/_data/books.cjs
// Enhanced data loader for books.json with multilevel fallbacks

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
    path.join(__dirname, "..", "..", "_data", "books.json"),
    // Fallback locations
    path.join(__dirname, "..", "..", "assets", "data", "books.json"),
    path.join(__dirname, "books.json"),
  ];

  // Try each data path
  for (const dataPath of dataPaths) {
    try {
      if (fs.existsSync(dataPath)) {
        // Read and parse the JSON file
        const fileContents = fs.readFileSync(dataPath, "utf8");

        // Check if the content is not empty and parse it
        if (
          fileContents &&
          fileContents.trim() !== "" &&
          fileContents.trim() !== "[]"
        ) {
          const data = JSON.parse(fileContents);

          // Cache the data
          cache.data = data;
          cache.timestamp = now;

          return data;
        }
      }
    } catch (error) {
      // Try next data path
      console.warn(`Warning: Failed to load books.json from ${dataPath}`);
    }
  }

  // Fall back to reading from site.json if books.json doesn't exist or is empty
  try {
    const siteJsonPath = path.join(__dirname, "site.json");
    const siteBackupPath = path.join(__dirname, "site.json.backup");

    // Try the main site.json first
    if (fs.existsSync(siteJsonPath)) {
      const siteData = JSON.parse(fs.readFileSync(siteJsonPath, "utf8"));

      if (siteData.homepage && Array.isArray(siteData.homepage.reading_list)) {
        console.log("Using reading list from site.json");
        // Return the reading list from site.json with minimal formatting
        const data = siteData.homepage.reading_list.map((book) => ({
          title: book.title,
          author: book.author,
          isbn: book.isbn || null,
          progress: book.progress || 0,
          cover_url: null,
          description: null,
          publish_date: null,
          page_count: null,
          subjects: [],
        }));

        // Cache the data
        cache.data = data;
        cache.timestamp = now;

        return data;
      }
    }

    // Try the backup site.json if main one doesn't have reading list
    if (fs.existsSync(siteBackupPath)) {
      const siteData = JSON.parse(fs.readFileSync(siteBackupPath, "utf8"));

      if (siteData.homepage && Array.isArray(siteData.homepage.reading_list)) {
        console.log("Using reading list from site.json.backup");
        // Return the reading list from site.json.backup with minimal formatting
        const data = siteData.homepage.reading_list.map((book) => ({
          title: book.title,
          author: book.author,
          isbn: book.isbn || null,
          progress: book.progress || 0,
          cover_url: null,
          description: null,
          publish_date: null,
          page_count: null,
          subjects: [],
        }));

        // Cache the data
        cache.data = data;
        cache.timestamp = now;

        return data;
      }
    }
  } catch (error) {
    console.error("Error reading site.json data:", error);
  }

  // Final fallback: sample data
  console.warn("Warning: No reading list data found in any source. Using sample data.");
  const sampleData = [
    {
      title: "Designing Data-Intensive Applications",
      author: "Martin Kleppmann",
      isbn: "9781449373320",
      progress: 75,
      subjects: ["Development", "Database management"],
    },
  ];

  // Cache the sample data
  cache.data = sampleData;
  cache.timestamp = now;

  return sampleData;
};
