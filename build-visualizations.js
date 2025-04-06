/**
 * Pre-generate data for GitHub-style visualizations
 * This script processes blog posts and creates cached JSON data for faster visualization rendering
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import matter from 'gray-matter';

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Constants
const POSTS_DIR = path.join(__dirname, 'src/posts');
const OUTPUT_DIR = path.join(__dirname, '_data/cache');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Create a date formatter helper
function formatDate(date, format) {
  const d = new Date(date);
  
  const formatters = {
    'yyyy': () => d.getFullYear(),
    'MM': () => String(d.getMonth() + 1).padStart(2, '0'),
    'dd': () => String(d.getDate()).padStart(2, '0'),
    'MMM': () => d.toLocaleString('en-US', { month: 'short' }),
    'MMMM': () => d.toLocaleString('en-US', { month: 'long' }),
    'short': () => d.toLocaleString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    })
  };
  
  return formatters[format] ? formatters[format]() : d.toISOString();
}

// Generate activity timeline data
function generateActivityData(posts) {
  // Group posts by month-year
  const postsByMonth = {};
  
  posts.forEach(post => {
    const date = new Date(post.date);
    const monthYear = `${formatDate(date, 'MMM')} ${formatDate(date, 'yyyy')}`;
    
    if (!postsByMonth[monthYear]) {
      postsByMonth[monthYear] = [];
    }
    
    postsByMonth[monthYear].push({
      title: post.title,
      url: post.url || `/posts/${post.slug}/`,
      date: post.date,
      formattedDate: formatDate(date, 'short')
    });
  });
  
  // Sort months chronologically (newest first)
  const sortedMonths = Object.keys(postsByMonth).sort((a, b) => {
    const dateA = new Date(postsByMonth[a][0].date);
    const dateB = new Date(postsByMonth[b][0].date);
    return dateB - dateA;
  });
  
  // Create the final data structure
  const activityData = sortedMonths.map(month => ({
    month,
    posts: postsByMonth[month].sort((a, b) => new Date(b.date) - new Date(a.date))
  }));
  
  return activityData;
}

// Read and parse all blog posts
function getAllPosts() {
  const files = fs.readdirSync(POSTS_DIR).filter(file => file.endsWith('.md'));
  
  const posts = files.map(file => {
    const filePath = path.join(POSTS_DIR, file);
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    
    // Use gray-matter to parse front matter
    const { data, content } = matter(fileContent);
    
    // Extract file name without extension as slug
    const slug = file.replace(/\.md$/, '');
    
    return {
      title: data.title,
      date: data.date,
      slug,
      url: data.permalink || `/posts/${slug}/`
    };
  });
  
  // Sort by date (newest first)
  return posts.sort((a, b) => new Date(b.date) - new Date(a.date));
}

// Main execution
try {
  console.log('Generating visualization data...');
  const posts = getAllPosts();
  console.log(`Found ${posts.length} blog posts`);
  
  // Generate and save activity data
  const activityData = generateActivityData(posts);
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'activity.json'),
    JSON.stringify(activityData, null, 2)
  );
  console.log(`Saved activity data with ${activityData.length} month groups`);
  
  console.log('Visualization data generation complete!');
} catch (error) {
  console.error('Error generating visualization data:', error);
  process.exit(1);
}