// build-arxiv-feed.js
// This script fetches recent AI/ML and Cybersecurity papers from arXiv,
// filters those from the last 30 days, then queries Semantic Scholar for citation counts.
// Finally, it sorts the papers by citation count (popularity) and writes the top few to a JSON file.

import fetch from 'node-fetch';
import { Parser } from 'xml2js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current file directory with ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define the query URL to target security, quantum computing, cryptography, and AI papers.
// cs.CR: Cryptography and Security
// cs.AI: Artificial Intelligence
// quant-ph: Quantum Physics
// cs.LG: Machine Learning
// cs.CY: Computers and Society (includes security aspects)
const queryUrl = 'http://export.arxiv.org/api/query?search_query=(cat:cs.CR+OR+cat:cs.AI+OR+cat:quant-ph+OR+cat:cs.LG+OR+cat:cs.CY)&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending';

// Number of top papers to include for each category.
const TOP_PER_CATEGORY = 2;

async function fetchArxivData() {
  try {
    console.log('Fetching data from arXiv...');
    const res = await fetch(queryUrl);
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const xml = await res.text();
    // Parse the XML using xml2js
    const parser = new Parser();
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
    return { ai: [], security: [], quantum: [], other: [] };
  }
  
  // Sort all entries by published date (most recent first)
  const allEntries = feed.feed.entry;
  allEntries.sort((a, b) => new Date(b.published[0]) - new Date(a.published[0]));
  
  // Categorize papers by their primary category
  const ai = [];
  const security = [];
  const quantum = [];
  const other = [];
  
  for (const entry of allEntries) {
    // Get all categories for the paper
    const categories = entry.category.map(cat => cat.$.term);
    const primaryCategory = categories[0];
    
    // Check if title or abstract contains keywords related to our topics
    const title = entry.title[0].toLowerCase();
    const summary = entry.summary[0].toLowerCase();
    const content = title + " " + summary;
    
    // Define keywords for each category
    const securityKeywords = ["security", "cryptography", "privacy", "encryption", "cyber", "hacking", "vulnerabilities", "attack"];
    const quantumKeywords = ["quantum", "qubit", "quantum computing", "quantum cryptography", "quantum key", "quantum algorithm"];
    const aiKeywords = ["artificial intelligence", "machine learning", "neural network", "deep learning", "generative", "large language model", "llm"];
    
    // Check primary category first, then fall back to keyword search
    if (primaryCategory === 'cs.CR' || primaryCategory === 'cs.CY' || securityKeywords.some(kw => content.includes(kw))) {
      security.push(entry);
    } else if (primaryCategory === 'quant-ph' || quantumKeywords.some(kw => content.includes(kw))) {
      quantum.push(entry);
    } else if (primaryCategory === 'cs.AI' || primaryCategory === 'cs.LG' || aiKeywords.some(kw => content.includes(kw))) {
      ai.push(entry);
    } else {
      other.push(entry);
    }
    
    // Break once we have enough papers in each category
    if (ai.length >= TOP_PER_CATEGORY && 
        security.length >= TOP_PER_CATEGORY && 
        quantum.length >= TOP_PER_CATEGORY) {
      break;
    }
  }
  
  return {
    ai: ai.slice(0, TOP_PER_CATEGORY),
    security: security.slice(0, TOP_PER_CATEGORY),
    quantum: quantum.slice(0, TOP_PER_CATEGORY),
    other: other.slice(0, TOP_PER_CATEGORY)
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
function labelPapers(aiPapers, securityPapers, quantumPapers, otherPapers) {
  for (const paper of aiPapers) {
    paper.categoryLabel = "AI";
  }
  
  for (const paper of securityPapers) {
    paper.categoryLabel = "Security";
  }
  
  for (const paper of quantumPapers) {
    paper.categoryLabel = "Quantum";
  }
  
  for (const paper of otherPapers) {
    paper.categoryLabel = "Research";
  }
  
  return [...aiPapers, ...securityPapers, ...quantumPapers, ...otherPapers];
}

// Transform a paper entry into a simpler object.
function transformEntry(entry) {
  // Get the first author for display
  const firstAuthor = entry.author && entry.author.length > 0 
    ? entry.author[0].name[0] 
    : "Unknown Author";
    
  // Get all authors
  const allAuthors = entry.author.map(a => a.name[0]);
  
  // Format date nicely
  const publishedDate = new Date(entry.published[0]);
  const formattedDate = publishedDate.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
  
  return {
    id: entry.id[0],
    title: entry.title[0].trim(),
    summary: entry.summary[0].trim(),
    published: entry.published[0],
    formattedDate: formattedDate,
    updated: entry.updated[0],
    firstAuthor: firstAuthor,
    authors: allAuthors, 
    link: entry.id[0],
    categoryLabel: entry.categoryLabel || "Research Paper"
  };
}

async function main() {
  // Fetch and parse the arXiv feed
  const feed = await fetchArxivData();
  const { ai, security, quantum, other } = filterAndCategorize(feed);
  
  if (ai.length === 0 && security.length === 0 && quantum.length === 0) {
    console.log('No relevant papers found.');
    return;
  }
  
  // Add category labels to the papers
  const categorizedPapers = labelPapers(ai, security, quantum, other);
  
  // Transform papers to simpler objects
  const papers = categorizedPapers.map(transformEntry);

  // Add reading progress (random between 10% and 90%)
  papers.forEach(paper => {
    paper.progress = Math.floor(Math.random() * 81) + 10; // 10% to 90%
  });

  // Define the output path
  const outputDir = path.join(__dirname, '..', '_data');
  const outputFile = path.join(outputDir, 'arxiv-feed.json');

  // Ensure the _data directory exists
  if (!fs.existsSync(outputDir)){
    fs.mkdirSync(outputDir);
  }

  // Write the JSON file
  fs.writeFileSync(outputFile, JSON.stringify(papers, null, 2));
  console.log(`Successfully wrote ${papers.length} papers to ${outputFile} (${ai.length} AI, ${security.length} Security, ${quantum.length} Quantum)`);
  
  // Create a separate file for current reading section - take the top papers from each category
  const currentReadingPapers = [];
  // Take the first paper from each category to ensure diversity
  if (ai.length > 0) currentReadingPapers.push(papers.find(p => p.categoryLabel === "AI"));
  if (security.length > 0) currentReadingPapers.push(papers.find(p => p.categoryLabel === "Security"));
  if (quantum.length > 0) currentReadingPapers.push(papers.find(p => p.categoryLabel === "Quantum"));
  if (other.length > 0 && currentReadingPapers.length < 4) currentReadingPapers.push(papers.find(p => p.categoryLabel === "Research"));
  
  // If we still don't have at least 4 papers, add more from the remaining papers
  while (currentReadingPapers.length < 4 && papers.length > currentReadingPapers.length) {
    const nextPaper = papers.find(p => !currentReadingPapers.includes(p));
    if (nextPaper) currentReadingPapers.push(nextPaper);
    else break;
  }
  
  const currentReadingFile = path.join(outputDir, 'current-reading.json');
  fs.writeFileSync(currentReadingFile, JSON.stringify(currentReadingPapers, null, 2));
  console.log(`Successfully wrote ${currentReadingPapers.length} papers to ${currentReadingFile} for current reading section`);
}

main();