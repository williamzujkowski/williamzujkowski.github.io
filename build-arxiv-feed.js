// build-arxiv-feed.js
// This script fetches recent AI/ML and Cybersecurity papers from arXiv,
// filters those from the last 30 days, then queries Semantic Scholar for citation counts.
// Finally, it sorts the papers by citation count (popularity) and writes the top few to a JSON file.

const fetch = require('node-fetch');
const xml2js = require('xml2js');
const fs = require('fs');
const path = require('path');

// Define the query URL to target the cs.AI, cs.LG, and cs.CR categories.
const queryUrl = 'http://export.arxiv.org/api/query?search_query=(cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CR)&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending';

// Number of top papers to include for each category.
const TOP_PER_CATEGORY = 1;

async function fetchArxivData() {
  try {
    console.log('Fetching data from arXiv...');
    const res = await fetch(queryUrl);
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const xml = await res.text();
    // Parse the XML using xml2js
    const parser = new xml2js.Parser();
    const result = await parser.parseStringPromise(xml);
    return result;
  } catch (error) {
    console.error('Error fetching or parsing data from arXiv:', error);
    process.exit(1);
  }
}

function filterAndCategorize(feed) {
  if (!feed.feed || !feed.feed.entry) {
    console.error('No entries found in the feed.');
    return { ai_ml: [], cybersecurity: [] };
  }
  
  // Sort all entries by published date (most recent first)
  const allEntries = feed.feed.entry;
  allEntries.sort((a, b) => new Date(b.published[0]) - new Date(a.published[0]));
  
  // Categorize papers by their primary category
  const ai_ml = [];
  const cybersecurity = [];
  
  for (const entry of allEntries) {
    // Look at the primary category (first category)
    const primaryCategory = entry.category[0].$.term;
    
    if (primaryCategory === 'cs.CR') {
      cybersecurity.push(entry);
    } else if (primaryCategory === 'cs.AI' || primaryCategory === 'cs.LG') {
      ai_ml.push(entry);
    }
    
    // Break once we have enough papers in each category
    if (ai_ml.length >= TOP_PER_CATEGORY && cybersecurity.length >= TOP_PER_CATEGORY) {
      break;
    }
  }
  
  return {
    ai_ml: ai_ml.slice(0, TOP_PER_CATEGORY),
    cybersecurity: cybersecurity.slice(0, TOP_PER_CATEGORY)
  };
}

// Helper: Extract the arXiv ID from the URL (e.g., "http://arxiv.org/abs/1234.56789v1" → "1234.56789")
function extractArxivId(url) {
  const match = url.match(/abs\/([\d\.]+)(v\d+)?/);
  if (match) {
    return match[1];
  }
  return url;
}

// Query Semantic Scholar to get the citation count for a paper.
// The API endpoint for an arXiv paper uses the format "arXiv:ID".
async function getCitationCount(arxivUrl) {
  const arxivId = extractArxivId(arxivUrl);
  const semanticId = `arXiv:${arxivId}`;
  const url = `https://api.semanticscholar.org/graph/v1/paper/${semanticId}?fields=citationCount`;

  try {
    const res = await fetch(url);
    if (!res.ok) {
      console.error(`Error fetching citation for ${semanticId}: ${res.status}`);
      return 0;
    }
    const data = await res.json();
    return data.citationCount || 0;
  } catch (error) {
    console.error(`Error fetching citation for ${semanticId}:`, error);
    return 0;
  }
}

// Add category label to each paper
function labelPapers(aimlPapers, cyberPapers) {
  for (const paper of aimlPapers) {
    paper.categoryLabel = "AI/ML";
  }
  
  for (const paper of cyberPapers) {
    paper.categoryLabel = "Cybersecurity";
  }
  
  return [...aimlPapers, ...cyberPapers];
}

// Transform a paper entry into a simpler object.
function transformEntry(entry) {
  return {
    id: entry.id[0],
    title: entry.title[0].trim(),
    summary: entry.summary[0].trim(),
    published: entry.published[0],
    updated: entry.updated[0],
    authors: entry.author.map(a => a.name[0]),
    link: entry.id[0],
    categoryLabel: entry.categoryLabel || "Research Paper"
  };
}

async function main() {
  // Fetch and parse the arXiv feed
  const feed = await fetchArxivData();
  const { ai_ml, cybersecurity } = filterAndCategorize(feed);
  
  if (ai_ml.length === 0 && cybersecurity.length === 0) {
    console.log('No papers found.');
    return;
  }
  
  // Add category labels to the papers
  const categorizedPapers = labelPapers(ai_ml, cybersecurity);
  
  // Transform papers to simpler objects
  const papers = categorizedPapers.map(transformEntry);

  // Define the output path
  const outputDir = path.join(__dirname, '_data');
  const outputFile = path.join(outputDir, 'arxiv-feed.json');

  // Ensure the _data directory exists
  if (!fs.existsSync(outputDir)){
    fs.mkdirSync(outputDir);
  }

  // Write the JSON file
  fs.writeFileSync(outputFile, JSON.stringify(papers, null, 2));
  console.log(`Successfully wrote ${papers.length} papers to ${outputFile} (${ai_ml.length} AI/ML, ${cybersecurity.length} Cybersecurity)`);
}

main();