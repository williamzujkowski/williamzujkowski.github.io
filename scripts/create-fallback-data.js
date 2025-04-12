/**
 * Simple fallback data generator
 * This is a compatibility script for GitHub Actions
 */

import fs from 'fs';
import path from 'path';

async function main() {
  try {
    // Just use the direct path to _data in the root
    const dataDir = './_data';
    
    // Make sure the directory exists
    fs.mkdirSync(dataDir, { recursive: true });

    // Create empty fallback files
    const files = [
      { name: 'arxiv-feed.json', content: [] },
      { name: 'github-pins.json', content: [] },
      { name: 'contribution-heatmap.json', content: { data: [] } },
      { name: 'link-previews.json', content: [] },
      { name: 'current-reading.json', content: [
        {
          "title": "Fallback Reading Item",
          "firstAuthor": "Author Name",
          "categoryLabel": "Research",
          "progress": 50
        }
      ]},
      { name: 'books.json', content: [
        {
          "title": "Fallback Book",
          "author": "Author Name",
          "isbn": "1234567890",
          "progress": 50
        }
      ]}
    ];

    // Write all files
    for (const file of files) {
      fs.writeFileSync(
        path.join(dataDir, file.name), 
        JSON.stringify(file.content, null, 2)
      );
      console.log(`Created fallback ${file.name}`);
    }

    console.log('All fallback data files created successfully');
  } catch (error) {
    console.error('Error creating fallback data:', error);
    process.exit(1);
  }
}

main();