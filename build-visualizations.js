// build-visualizations.js
// This script generates a GitHub-style contribution heatmap data structure
// based on blog post dates from markdown files in the src/posts directory.

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current file directory with ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Source directory for blog posts
const POSTS_DIR = path.join(__dirname, 'src', 'posts');
// Output file for heatmap data
const OUTPUT_FILE = path.join(__dirname, '_data', 'contribution-heatmap.json');

/**
 * Extract date from filename that follows the pattern YYYY-MM-DD-title.md
 * @param {string} filename
 * @returns {Date|null} A Date object or null if pattern doesn't match
 */
function extractDateFromFilename(filename) {
  const datePattern = /^(\d{4}-\d{2}-\d{2})-/;
  const match = filename.match(datePattern);
  
  if (match && match[1]) {
    return new Date(match[1]);
  }
  return null;
}

/**
 * Format a date as YYYY-MM-DD
 * @param {Date} date
 * @returns {string} Formatted date string
 */
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

/**
 * Calculate intensity value (0-4) based on number of posts per day
 * @param {number} count Number of posts on a given day
 * @returns {number} Intensity value from 0-4
 */
function calculateIntensity(count) {
  if (count === 0) return 0;
  if (count === 1) return 1;
  if (count === 2) return 2;
  if (count === 3) return 3;
  return 4; // 4+ posts gets max intensity
}

/**
 * Generate contribution heatmap data from blog post dates
 */
async function generateHeatmapData() {
  try {
    console.log('Generating contribution heatmap data...');
    
    // Create a map to store posts per day
    const postsByDay = new Map();
    
    // Read the posts directory
    const files = fs.readdirSync(POSTS_DIR);
    
    // Filter for markdown files and extract dates
    const postDates = files
      .filter(file => file.endsWith('.md') && !file.includes('template'))
      .map(file => {
        const date = extractDateFromFilename(file);
        return date ? { file, date } : null;
      })
      .filter(Boolean); // Remove null values
    
    if (postDates.length === 0) {
      console.warn('No valid blog post dates found.');
      return;
    }
    
    console.log(`Found ${postDates.length} blog posts with dates.`);
    
    // Group posts by day
    postDates.forEach(({ file, date }) => {
      const dateStr = formatDate(date);
      if (postsByDay.has(dateStr)) {
        postsByDay.set(dateStr, postsByDay.get(dateStr) + 1);
      } else {
        postsByDay.set(dateStr, 1);
      }
    });
    
    // Convert to array and add intensity values
    const heatmapData = Array.from(postsByDay.entries()).map(([date, count]) => {
      return {
        date,
        count,
        intensity: calculateIntensity(count)
      };
    });
    
    // Sort by date (oldest first)
    heatmapData.sort((a, b) => new Date(a.date) - new Date(b.date));
    
    // Prepare output directory
    const outputDir = path.dirname(OUTPUT_FILE);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Create final data structure
    const contributionData = {
      contributions: heatmapData
    };
    
    // Write the data to a JSON file
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(contributionData, null, 2));
    console.log(`Successfully wrote heatmap data for ${heatmapData.length} days to ${OUTPUT_FILE}`);
    
    // Summary for visualization
    const intensityCounts = [0, 0, 0, 0, 0]; // Counts for intensity levels 0-4
    heatmapData.forEach(day => {
      intensityCounts[day.intensity]++;
    });
    
    console.log('Intensity distribution:');
    console.log(`- Level 1 (light): ${intensityCounts[1]} days`);
    console.log(`- Level 2 (medium): ${intensityCounts[2]} days`);
    console.log(`- Level 3 (medium-high): ${intensityCounts[3]} days`);
    console.log(`- Level 4 (high): ${intensityCounts[4]} days`);
    
  } catch (error) {
    console.error('Error generating heatmap data:', error);
    process.exit(1);
  }
}

// Main function
async function main() {
  await generateHeatmapData();
}

main();