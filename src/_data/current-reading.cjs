// src/_data/current-reading.cjs
// This file loads current-reading.json data for use in templates

const fs = require('fs');
const path = require('path');

module.exports = function() {
  // Set the path to the current-reading.json file
  const dataPath = path.join(__dirname, '..', '..', '_data', 'current-reading.json');
  
  try {
    // Check if the file exists
    if (fs.existsSync(dataPath)) {
      // Read and parse the JSON file
      const fileContents = fs.readFileSync(dataPath, 'utf8');
      return JSON.parse(fileContents);
    } else {
      console.warn('Warning: current-reading.json not found. Using empty array instead.');
      return [];
    }
  } catch (error) {
    console.error('Error reading current-reading.json:', error);
    return [];
  }
};