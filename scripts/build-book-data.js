// build-book-data.js
// This script fetches book metadata from the Open Library API based on ISBNs in site.json

import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current file directory with ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read the site.json file to get books from reading_list
async function getReadingListFromConfig() {
  try {
    const siteJsonPath = path.join(__dirname, '..', 'src', '_data', 'site.json');
    const siteJsonContent = await fs.promises.readFile(siteJsonPath, 'utf8');
    const siteData = JSON.parse(siteJsonContent);
    
    if (siteData.homepage && Array.isArray(siteData.homepage.reading_list)) {
      return siteData.homepage.reading_list;
    } else {
      console.log('No reading list found in site.json');
      return [];
    }
  } catch (error) {
    console.error('Error reading site.json:', error);
    return [];
  }
}

// Fetch book data from Open Library API
async function fetchBookData(isbn) {
  try {
    const response = await fetch(`https://openlibrary.org/api/books?bibkeys=ISBN:${isbn}&format=json&jscmd=data`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    return data[`ISBN:${isbn}`];
  } catch (error) {
    console.error(`Error fetching book data for ISBN ${isbn}:`, error);
    return null;
  }
}

// Extract and process the relevant book data
function processBookData(bookApiData, bookConfig) {
  // Return null if no API data was found
  if (!bookApiData) {
    return {
      title: bookConfig.title,
      author: bookConfig.author,
      isbn: bookConfig.isbn,
      progress: bookConfig.progress || 0,
      cover_url: null,
      description: null,
      publish_date: null,
      page_count: null,
      subjects: []
    };
  }
  
  // Extract author(s)
  const authors = bookApiData.authors ? 
    bookApiData.authors.map(author => author.name).join(', ') : 
    bookConfig.author;
  
  // Extract cover image URL (medium size)
  const coverUrl = bookApiData.cover ? 
    (bookApiData.cover.medium || bookApiData.cover.small || bookApiData.cover.large) : 
    null;
  
  // Extract subjects (up to 5)
  const subjects = bookApiData.subjects ? 
    bookApiData.subjects.slice(0, 5).map(subject => subject.name || subject) : 
    [];
  
  // Return formatted book data
  return {
    title: bookApiData.title || bookConfig.title,
    author: authors,
    isbn: bookConfig.isbn,
    progress: bookConfig.progress || 0,
    cover_url: coverUrl,
    description: bookApiData.notes && bookApiData.notes.value ? 
      bookApiData.notes.value : 
      (bookApiData.excerpts && bookApiData.excerpts[0] ? bookApiData.excerpts[0].text : null),
    publish_date: bookApiData.publish_date || null,
    page_count: bookApiData.number_of_pages || null,
    subjects: subjects
  };
}

async function main() {
  try {
    // Get reading list from site.json
    const readingList = await getReadingListFromConfig();
    
    if (readingList.length === 0) {
      console.log('No books found in reading list. Add books to site.json under homepage.reading_list.');
      return;
    }
    
    console.log(`Found ${readingList.length} books in reading list. Fetching metadata...`);
    
    // Process each book
    const enrichedBooks = [];
    
    for (const book of readingList) {
      if (!book.isbn) {
        console.log(`Skipping book "${book.title}" - no ISBN provided`);
        // Still add the book with available data
        enrichedBooks.push({
          title: book.title,
          author: book.author,
          isbn: null,
          progress: book.progress || 0,
          cover_url: null,
          description: null,
          publish_date: null,
          page_count: null,
          subjects: []
        });
        continue;
      }
      
      console.log(`Fetching data for "${book.title}" (ISBN: ${book.isbn})...`);
      const bookApiData = await fetchBookData(book.isbn);
      
      if (bookApiData) {
        console.log(`Found metadata for "${book.title}"`);
      } else {
        console.log(`No metadata found for "${book.title}" (ISBN: ${book.isbn})`);
      }
      
      const processedBook = processBookData(bookApiData, book);
      enrichedBooks.push(processedBook);
    }
    
    // Write the enriched book data to a JSON file
    const outputDir = path.join(__dirname, '..', '_data');
    const outputFile = path.join(outputDir, 'books.json');
    
    // Ensure the _data directory exists
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Write the JSON file
    fs.writeFileSync(outputFile, JSON.stringify(enrichedBooks, null, 2));
    console.log(`Successfully wrote ${enrichedBooks.length} books to ${outputFile}`);
    
  } catch (error) {
    console.error('Error in main function:', error);
  }
}

main();