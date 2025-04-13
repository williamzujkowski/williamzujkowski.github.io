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
      
      // Check if the content is not empty and parse it
      if (fileContents && fileContents.trim() !== '' && fileContents.trim() !== '[]') {
        const data = JSON.parse(fileContents);
        // Debug output
        console.log('Loaded books data:', JSON.stringify(data));
        return data;
      } else {
        console.warn('Warning: books.json is empty. Checking for fallback data.');
      }
    } else {
      console.warn('Warning: books.json not found. Checking for fallback data.');
    }

    // Fall back to reading from site.json if books.json doesn't exist or is empty
    const siteJsonPath = path.join(__dirname, 'site.json');
    const siteBackupPath = path.join(__dirname, 'site.json.backup');
    
    // Try the main site.json first
    if (fs.existsSync(siteJsonPath)) {
      const siteData = JSON.parse(fs.readFileSync(siteJsonPath, 'utf8'));
      
      if (siteData.homepage && Array.isArray(siteData.homepage.reading_list)) {
        console.log('Using reading list from site.json');
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
    
    // Try the backup site.json if main one doesn't have reading list
    if (fs.existsSync(siteBackupPath)) {
      const siteData = JSON.parse(fs.readFileSync(siteBackupPath, 'utf8'));
      
      if (siteData.homepage && Array.isArray(siteData.homepage.reading_list)) {
        console.log('Using reading list from site.json.backup');
        // Return the reading list from site.json.backup with minimal formatting
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
    
    console.warn('Warning: No reading list data found in any source. Using empty array.');
    return [];
  } catch (error) {
    console.error('Error reading books data:', error, error.stack);
    return [];
  }
};