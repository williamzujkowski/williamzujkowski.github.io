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
      { name: 'contribution-heatmap.json', content: { data: [] } },
      { name: 'link-previews.json', content: [] },
      { name: 'current-reading.json', content: [
        {
          "title": "Designing Data-Intensive Applications",
          "firstAuthor": "Martin Kleppmann",
          "categoryLabel": "Research",
          "progress": 75,
          "link": "https://arxiv.org/abs/2001.00001"
        },
        {
          "title": "Building ML Powered Applications",
          "firstAuthor": "Emmanuel Ameisen",
          "categoryLabel": "AI",
          "progress": 45,
          "link": "https://arxiv.org/abs/2001.00002"
        }
      ]},
      { name: 'books.json', content: [
        {
          "title": "Dungeon Crawler Carl",
          "author": "Matt Dinniman",
          "isbn": "059382024X",
          "progress": 62,
          "cover_url": null,
          "description": null,
          "publish_date": "2024",
          "page_count": null,
          "subjects": ["series:dungeon_crawler_carl", "Fantasy"]
        },
        {
          "title": "Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems",
          "author": "Martin Kleppmann",
          "isbn": "9781449373320",
          "progress": 75,
          "cover_url": "https://covers.openlibrary.org/b/id/8434671-M.jpg",
          "description": null,
          "publish_date": "Apr 02, 2017",
          "page_count": 624,
          "subjects": ["Development", "Database management", "Databases"]
        },
        {
          "title": "Building Machine Learning Powered Applications",
          "author": "Emmanuel Ameisen",
          "isbn": "9781492045113", 
          "progress": 45,
          "cover_url": null,
          "description": null,
          "publish_date": "2020",
          "page_count": 260,
          "subjects": ["Science"]
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