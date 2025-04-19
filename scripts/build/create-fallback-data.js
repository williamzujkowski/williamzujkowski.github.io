/**
 * Create Fallback Data
 *
 * This script creates fallback data files for the website build process,
 * ensuring that the site can build even when dynamic data fetching fails.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..', '..');
const dataDir = path.join(rootDir, '_data');

// Ensure data directory exists
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Simple fallback data structures
const fallbackData = {
  'arxiv-feed.json': [
    {
      "id": "http://arxiv.org/abs/2504.07965v1",
      "title": "Cat, Rat, Meow: On the Alignment of Language Model and Human Term-Similarity Judgments",
      "summary": "Small and mid-sized generative language models have gained increasing attention. Their size and availability make them amenable to being analyzed at a behavioral as well as a representational level, allowing investigations of how these levels interact.",
      "published": "2025-04-10T17:59:57Z",
      "formattedDate": "Apr 10, 2025",
      "updated": "2025-04-10T17:59:57Z",
      "firstAuthor": "Lorenz Linhardt",
      "authors": ["Lorenz Linhardt", "Tom Neuhäuser", "Lenka Tětková", "Oliver Eberle"],
      "link": "http://arxiv.org/abs/2504.07965v1",
      "categoryLabel": "AI",
      "progress": 34
    },
    {
      "id": "http://arxiv.org/abs/2504.07945v1",
      "title": "GenEAva: Generating Cartoon Avatars with Fine-Grained Facial Expressions",
      "summary": "Cartoon avatars have been widely used in various applications, including social media, online tutoring, and gaming.",
      "published": "2025-04-10T17:54:02Z",
      "formattedDate": "Apr 10, 2025",
      "updated": "2025-04-10T17:54:02Z",
      "firstAuthor": "Hao Yu",
      "authors": ["Hao Yu", "Rupayan Mallick", "Margrit Betke", "Sarah Adel Bargal"],
      "link": "http://arxiv.org/abs/2504.07945v1",
      "categoryLabel": "Security",
      "progress": 11
    }
  ],
  'books.json': [
    {
      "title": "The Pragmatic Programmer",
      "author": "David Thomas & Andrew Hunt",
      "isbn": "9780135957059",
      "coverImage": "pragmatic-programmer.jpg",
      "progress": 100,
      "rating": 5,
      "notes": "Classic software engineering text",
      "dateStarted": "2025-01-15",
      "dateFinished": "2025-02-20"
    },
    {
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "isbn": "9780132350884",
      "coverImage": "clean-code.jpg",
      "progress": 85,
      "rating": 4,
      "notes": "Essential reading for software developers",
      "dateStarted": "2025-03-01",
      "dateFinished": null
    }
  ],
  'current-reading.json': [
    {
      "id": "http://arxiv.org/abs/2504.07965v1",
      "title": "Cat, Rat, Meow: On the Alignment of Language Model and Human Term-Similarity Judgments",
      "summary": "Small and mid-sized generative language models have gained increasing attention. Their size and availability make them amenable to being analyzed at a behavioral as well as a representational level, allowing investigations of how these levels interact.",
      "published": "2025-04-10T17:59:57Z",
      "formattedDate": "Apr 10, 2025",
      "updated": "2025-04-10T17:59:57Z",
      "firstAuthor": "Lorenz Linhardt",
      "authors": ["Lorenz Linhardt", "Tom Neuhäuser", "Lenka Tětková", "Oliver Eberle"],
      "link": "http://arxiv.org/abs/2504.07965v1",
      "categoryLabel": "AI",
      "progress": 34
    },
    {
      "id": "http://arxiv.org/abs/2504.07950v1",
      "title": "Localized quasiparticles in a fluxonium with quasi-two-dimensional amorphous kinetic inductors",
      "summary": "Disordered superconducting materials with high kinetic inductance are an important resource to generate nonlinearity in quantum circuits and create high-impedance environments.",
      "published": "2025-04-10T17:56:04Z",
      "formattedDate": "Apr 10, 2025",
      "updated": "2025-04-10T17:56:04Z",
      "firstAuthor": "Trevyn F. Q. Larson",
      "authors": ["Trevyn F. Q. Larson", "Sarah Garcia Jones", "Tamás Kalmár"],
      "link": "http://arxiv.org/abs/2504.07950v1",
      "categoryLabel": "Quantum",
      "progress": 81
    }
  ],
  'github-pins.json': [
    {
      "name": "website",
      "description": "Personal website and blog",
      "language": "JavaScript",
      "stars": 12,
      "forks": 3,
      "url": "https://github.com/williamzujkowski/williamzujkowski.github.io"
    },
    {
      "name": "quantum-algorithms",
      "description": "Implementation of various quantum algorithms",
      "language": "Python",
      "stars": 45,
      "forks": 12,
      "url": "https://github.com/williamzujkowski/quantum-algorithms"
    },
    {
      "name": "ml-experiments",
      "description": "Machine learning research and experiments",
      "language": "Python",
      "stars": 28,
      "forks": 7,
      "url": "https://github.com/williamzujkowski/ml-experiments"
    }
  ],
  'contribution-heatmap.json': {
    "data": [
      {"date": "2025-04-01", "count": 5},
      {"date": "2025-04-02", "count": 2},
      {"date": "2025-04-03", "count": 7},
      {"date": "2025-04-04", "count": 3},
      {"date": "2025-04-05", "count": 0},
      {"date": "2025-04-06", "count": 1},
      {"date": "2025-04-07", "count": 4},
      {"date": "2025-04-08", "count": 6},
      {"date": "2025-04-09", "count": 2},
      {"date": "2025-04-10", "count": 3}
    ]
  },
  'link-previews.json': []
};

// Write fallback data files
for (const [filename, data] of Object.entries(fallbackData)) {
  const filePath = path.join(dataDir, filename);
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  console.log(`Created fallback ${filename}`);
}

console.log('Fallback data creation complete.');
