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

// Generate contribution heatmap data
function generateHeatmapData(posts) {
  // Get all post dates as ISO strings
  const postDates = posts.map(post => {
    const date = new Date(post.date);
    return date.toISOString().split('T')[0]; // YYYY-MM-DD format
  });
  
  // Count posts per date
  const dateCounts = {};
  postDates.forEach(date => {
    dateCounts[date] = (dateCounts[date] || 0) + 1;
  });
  
  // Calculate date range (1 year back from today)
  const endDate = new Date();
  const startDate = new Date();
  startDate.setFullYear(endDate.getFullYear() - 1);
  
  // Fill in all dates in the range
  let currentDate = new Date(startDate);
  while (currentDate <= endDate) {
    const dateStr = currentDate.toISOString().split('T')[0];
    if (!dateCounts[dateStr]) {
      dateCounts[dateStr] = 0;
    }
    currentDate.setDate(currentDate.getDate() + 1);
  }
  
  // Determine maximum contribution count for color intensity scaling
  const counts = Object.values(dateCounts);
  const maxCount = Math.max(...counts, 1); // Ensure non-zero
  
  // Generate cells data grouped by intensity levels (0-4)
  const cells = [[], [], [], [], []];
  
  // Calculate positions and intensities
  currentDate = new Date(startDate);
  const dayMilliseconds = 24 * 60 * 60 * 1000;
  const totalDays = Math.ceil((endDate - startDate) / dayMilliseconds);
  
  for (let i = 0; i < totalDays; i++) {
    const date = new Date(startDate.getTime() + i * dayMilliseconds);
    const dateStr = date.toISOString().split('T')[0];
    
    // Calculate position in the grid
    const dayOfWeek = date.getDay(); // 0 = Sunday, 6 = Saturday
    const adjustedDay = dayOfWeek === 0 ? 6 : dayOfWeek - 1; // Make Monday=0, Sunday=6
    const weekOffset = Math.floor(i / 7);
    
    // Get count and determine intensity (0-4)
    const count = dateCounts[dateStr] || 0;
    let intensity = 0;
    if (count > 0) {
      if (count <= maxCount * 0.25) intensity = 1;
      else if (count <= maxCount * 0.5) intensity = 2;
      else if (count <= maxCount * 0.75) intensity = 3;
      else intensity = 4;
    }
    
    // Add to the appropriate intensity group
    cells[intensity].push({
      date: dateStr,
      count,
      x: weekOffset * 14,
      y: adjustedDay * 14
    });
  }
  
  return {
    dateRange: {
      start: startDate.toISOString(),
      end: endDate.toISOString()
    },
    cells,
    totalContributions: postDates.length,
    maxCountPerDay: maxCount
  };
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
  
  // Generate and save heatmap data
  const heatmapData = generateHeatmapData(posts);
  fs.writeFileSync(
    path.join(OUTPUT_DIR, 'heatmap.json'),
    JSON.stringify(heatmapData, null, 2)
  );
  console.log(`Saved heatmap data for ${heatmapData.totalContributions} contributions`);
  
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