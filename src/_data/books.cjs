// src/_data/books.cjs
// This file loads books.json data for use in templates

const fs = require('fs');
const path = require('path');

module.exports = function() {
  // Set the path to the books.json file
  const dataPath = path.join(__dirname, '..', '..', '_data', 'books.json');
  
  try {
    // Check if the file exists
    if (fs.existsSync(dataPath)) {
      // Read and parse the JSON file
      const fileContents = fs.readFileSync(dataPath, 'utf8');
      return JSON.parse(fileContents);
    } else {
      // Fall back to reading from site.json if books.json doesn't exist
      const siteJsonPath = path.join(__dirname, 'site.json');
      
      if (fs.existsSync(siteJsonPath)) {
        const siteData = JSON.parse(fs.readFileSync(siteJsonPath, 'utf8'));
        
        if (siteData.homepage && Array.isArray(siteData.homepage.reading_list)) {
          // Return the reading list from site.json with minimal formatting
          return siteData.homepage.reading_list.map(book => ({
            title: book.title,
            author: book.author,
            isbn: book.isbn || null,
            progress: book.progress || 0,
            cover_url: null,
            description: null,
            publish_date: null,
            page_count: null,
            subjects: []
          }));
        }
      }
      
      console.warn('Warning: books.json not found and no reading list in site.json. Using empty array instead.');
      return [];
    }
  } catch (error) {
    console.error('Error reading books data:', error);
    return [];
  }
};