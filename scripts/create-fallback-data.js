/**
 * This script generates fallback data files for the GitHub Actions build
 * It's used when the regular build scripts fail
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current file directory with ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  try {
    const dataDir = path.join(__dirname, '..', '_data');
    await fs.mkdir(dataDir, { recursive: true });

    // Create empty arxiv-feed.json
    const arxivData = [];
    await fs.writeFile(path.join(dataDir, 'arxiv-feed.json'), JSON.stringify(arxivData, null, 2));
    console.log('Created fallback arxiv-feed.json');

    // Create empty github-pins.json
    const githubData = [];
    await fs.writeFile(path.join(dataDir, 'github-pins.json'), JSON.stringify(githubData, null, 2));
    console.log('Created fallback github-pins.json');

    // Create empty contribution-heatmap.json
    const heatmapData = { data: [] };
    await fs.writeFile(path.join(dataDir, 'contribution-heatmap.json'), JSON.stringify(heatmapData, null, 2));
    console.log('Created fallback contribution-heatmap.json');

    // Create empty link-previews.json
    const linksData = [];
    await fs.writeFile(path.join(dataDir, 'link-previews.json'), JSON.stringify(linksData, null, 2));
    console.log('Created fallback link-previews.json');

    // Create empty current-reading.json
    const currentReadingData = [
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
    ];
    await fs.writeFile(path.join(dataDir, 'current-reading.json'), JSON.stringify(currentReadingData, null, 2));
    console.log('Created fallback current-reading.json');

    // Create fallback books.json
    const booksData = [
      {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "isbn": "9781449373320",
        "progress": 75,
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781449373320-M.jpg",
        "description": "Data-intensive applications are a challenge to build and maintain. Learn how to use these systems effectively with this practical guide to the best design patterns and principles.",
        "publish_date": "2017",
        "page_count": 616,
        "subjects": ["Distributed systems", "Database design", "Software architecture", "Web development", "Big data"]
      },
      {
        "title": "Building Machine Learning Powered Applications",
        "author": "Emmanuel Ameisen",
        "isbn": "9781492045113",
        "progress": 45,
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781492045113-M.jpg",
        "description": "Learn the skills necessary to design, build, and deploy applications powered by machine learning (ML). Through the course of this hands-on book, you'll build an example ML-driven application from initial idea to deployed product.",
        "publish_date": "2020",
        "page_count": 260,
        "subjects": ["Machine Learning", "Python", "Data Science", "Software Development", "Artificial Intelligence"]
      }
    ];
    await fs.writeFile(path.join(dataDir, 'books.json'), JSON.stringify(booksData, null, 2));
    console.log('Created fallback books.json');

    console.log('All fallback data files created successfully');
  } catch (error) {
    console.error('Error creating fallback data:', error);
    process.exit(1);
  }
}

main();