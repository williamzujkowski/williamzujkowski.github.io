// src/_data/arxiv-feed.cjs
// This file loads arxiv-feed.json data for use in templates

const fs = require('fs');
const path = require('path');

module.exports = function() {
  // Set the path to the arxiv-feed.json file
  const dataPath = path.join(__dirname, '..', '..', '_data', 'arxiv-feed.json');
  
  try {
    // Check if the file exists
    if (fs.existsSync(dataPath)) {
      // Read and parse the JSON file
      const fileContents = fs.readFileSync(dataPath, 'utf8');
      return JSON.parse(fileContents);
    } else {
      console.warn('Warning: arxiv-feed.json not found. Using empty array instead.');
      return [];
    }
  } catch (error) {
    console.error('Error reading arxiv-feed.json:', error);
    return [];
  }
};