/**
 * Enhanced Blog Post Processor
 * 
 * A unified utility for processing blog posts with advanced features:
 * - Handles different input formats (txt, md)
 * - Applies proper formatting and frontmatter
 * - Uses templates for consistent post structure
 * - Schedules posts with appropriate dates
 * - Suggests relevant images based on content
 * - Provides clear console feedback
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import matter from 'gray-matter';

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..', '..', '..');
const newPostsDir = path.join(rootDir, 'new_posts');
const processedDir = path.join(newPostsDir, 'processed');
const postsDir = path.join(rootDir, 'src', 'posts');
const templatesDir = path.join(rootDir, 'src', '_data', 'templates', 'blog');

// Topic mapping for template selection
const topicMap = {
  'security': 'cybersecurity',
  'cybersecurity': 'cybersecurity',
  'infosec': 'cybersecurity',
  'hacking': 'cybersecurity',
  'vulnerability': 'cybersecurity',
  
  'ai': 'ai-ml',
  'ml': 'ai-ml',
  'artificial intelligence': 'ai-ml',
  'machine learning': 'ai-ml',
  'neural': 'ai-ml',
  'llm': 'ai-ml',
  
  'cloud': 'cloud-computing',
  'aws': 'cloud-computing',
  'azure': 'cloud-computing',
  'gcp': 'cloud-computing',
  'serverless': 'cloud-computing',
  
  'quantum': 'quantum-computing',
  'qubit': 'quantum-computing',
  
  'devops': 'devops',
  'ci/cd': 'devops',
  'pipeline': 'devops',
  'jenkins': 'devops',
  'kubernetes': 'devops',
  'docker': 'devops',
  'container': 'devops'
};

// Ensure directories exist
if (!fs.existsSync(processedDir)) {
  fs.mkdirSync(processedDir, { recursive: true });
}

/**
 * Find the most recent post date
 * @returns {Date} Date of the most recent post
 */
function findMostRecentPostDate() {
  try {
    const files = fs.readdirSync(postsDir);
    const dateRegex = /^(\d{4}-\d{2}-\d{2})/;
    
    const dates = files
      .filter(file => file.endsWith('.md'))
      .map(file => {
        const match = file.match(dateRegex);
        return match ? new Date(match[1]) : null;
      })
      .filter(date => date !== null)
      .sort((a, b) => b - a);
    
    return dates.length > 0 ? dates[0] : new Date();
  } catch (error) {
    console.error('Error finding most recent post date:', error);
    return new Date();
  }
}

/**
 * Generate a future date for the post
 * @returns {string} Date in YYYY-MM-DD format
 */
function generatePostDate() {
  const mostRecentDate = findMostRecentPostDate();
  const newDate = new Date(mostRecentDate);
  
  // Add 10-14 days to the most recent post date
  const daysToAdd = 10 + Math.floor(Math.random() * 5);
  newDate.setDate(newDate.getDate() + daysToAdd);
  
  // Format as YYYY-MM-DD
  const year = newDate.getFullYear();
  const month = String(newDate.getMonth() + 1).padStart(2, '0');
  const day = String(newDate.getDate()).padStart(2, '0');
  
  return `${year}-${month}-${day}`;
}

/**
 * Create a URL-friendly slug from a title
 * @param {string} title - The post title
 * @returns {string} URL-friendly slug
 */
function createSlug(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')     // Remove special characters
    .replace(/\s+/g, '-')          // Replace spaces with hyphens
    .replace(/--+/g, '-')          // Replace multiple hyphens with single hyphen
    .replace(/^-+|-+$/g, '');      // Remove leading/trailing hyphens
}

/**
 * Detect topics in the post content to determine appropriate template
 * @param {string} content - The post content
 * @returns {string} The best matching template name
 */
function detectTopics(content) {
  const contentLower = content.toLowerCase();
  const topicMatches = {};
  
  // Count occurrences of topic keywords
  for (const [keyword, template] of Object.entries(topicMap)) {
    const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
    const matches = (contentLower.match(regex) || []).length;
    
    if (matches > 0) {
      topicMatches[template] = (topicMatches[template] || 0) + matches;
    }
  }
  
  // Find the template with the most matches
  let bestTemplate = 'base';
  let maxMatches = 0;
  
  for (const [template, count] of Object.entries(topicMatches)) {
    if (count > maxMatches) {
      maxMatches = count;
      bestTemplate = template;
    }
  }
  
  return bestTemplate;
}

/**
 * Detect tags from post content
 * @param {string} content - The post content
 * @param {string} template - The selected template
 * @returns {Array} Array of tags
 */
function detectTags(content, template) {
  const contentLower = content.toLowerCase();
  const tags = new Set();
  
  // Add template-specific primary tag
  switch (template) {
    case 'cybersecurity':
      tags.add('cybersecurity');
      break;
    case 'ai-ml':
      tags.add('artificial-intelligence');
      tags.add('machine-learning');
      break;
    case 'cloud-computing':
      tags.add('cloud-computing');
      break;
    case 'quantum-computing':
      tags.add('quantum-computing');
      break;
    case 'devops':
      tags.add('devops');
      break;
    default:
      tags.add('technology');
      break;
  }
  
  // Look for common technology topics
  const techTerms = [
    ['security', 'cybersecurity', 'infosec'],
    ['aws', 'amazon', 'cloud'],
    ['azure', 'microsoft'],
    ['gcp', 'google cloud'],
    ['kubernetes', 'k8s', 'container orchestration'],
    ['docker', 'container'],
    ['devops', 'ci/cd', 'continuous integration'],
    ['javascript', 'js', 'frontend'],
    ['python', 'programming'],
    ['database', 'sql', 'nosql'],
    ['api', 'rest', 'graphql'],
    ['blockchain', 'crypto'],
    ['iot', 'internet of things'],
    ['serverless', 'faas'],
    ['microservices', 'service mesh'],
    ['ai', 'artificial intelligence', 'ml', 'machine learning'],
    ['data science', 'analytics'],
    ['quantum', 'quantum computing'],
    ['virtual reality', 'vr', 'augmented reality', 'ar'],
    ['5g', 'networking'],
    ['edge computing', 'fog computing']
  ];
  
  // Add tags based on content
  for (const termGroup of techTerms) {
    const primaryTerm = termGroup[0];
    for (const term of termGroup) {
      if (contentLower.includes(term)) {
        tags.add(primaryTerm);
        break;
      }
    }
  }
  
  return Array.from(tags).slice(0, 5); // Limit to 5 tags
}

/**
 * Process a post file
 * @param {string} filePath - Path to the post file
 */
async function processPost(filePath) {
  try {
    console.log(`Processing: ${filePath}`);
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const fileName = path.basename(filePath);
    const fileExt = path.extname(filePath).toLowerCase();
    
    // Extract post content and title based on file type
    let title = '';
    let content = '';
    let frontmatter = {};
    
    if (fileExt === '.md') {
      // Parse markdown with frontmatter
      const parsed = matter(fileContent);
      frontmatter = parsed.data;
      content = parsed.content;
      
      // Extract title from frontmatter or first heading
      title = frontmatter.title || '';
      if (!title) {
        const h1Match = content.match(/^#\s+(.+)$/m);
        if (h1Match) {
          title = h1Match[1];
          // Remove the heading from content
          content = content.replace(/^#\s+(.+)$/m, '').trim();
        }
      }
    } else {
      // For text files, assume first line is title
      const lines = fileContent.split('\n');
      title = lines[0].trim();
      content = lines.slice(1).join('\n').trim();
    }
    
    // If no title was found, use filename without extension
    if (!title) {
      title = path.basename(fileName, fileExt)
        .replace(/[-_]/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
    }
    
    console.log(`Title: "${title}"`);
    
    // Generate post date
    const postDate = frontmatter.date || generatePostDate();
    console.log(`Scheduled date: ${postDate}`);
    
    // Detect best template based on content
    const templateName = detectTopics(content);
    console.log(`Selected template: ${templateName}`);
    
    // Read the template
    const templatePath = path.join(templatesDir, `${templateName}.md`);
    let templateContent = '';
    
    try {
      templateContent = fs.readFileSync(templatePath, 'utf8');
    } catch (error) {
      console.warn(`Template ${templateName}.md not found, using base template`);
      templateContent = fs.readFileSync(path.join(templatesDir, 'base.md'), 'utf8');
    }
    
    // Detect tags
    const tags = frontmatter.tags || detectTags(content, templateName);
    console.log(`Tags: ${tags.join(', ')}`);
    
    // Generate description if not present
    const description = frontmatter.description || 
      `${title} - An exploration of ${tags.join(', ')} concepts and applications.`;
    
    // Get primary tag for template
    const primaryTag = tags[0] || 'technology';
    
    // Format additional tags
    const additionalTags = tags.slice(1).map(tag => `  - ${tag}`).join('\n');
    
    // Determine image
    const image = frontmatter.image || 
      `topics/${templateName === 'base' ? 'technology' : templateName}.jpg`;
    
    // Split content into sections or use as is
    let introduction = '';
    let mainContent = '';
    let conclusion = '';
    
    // Try to find sections in the content
    const introMatch = content.match(/(?:introduction|overview)[\s\S]*?(?=##|$)/i);
    const conclusionMatch = content.match(/(?:##\s*conclu[s]?ion|summary)[\s\S]*$/i);
    
    if (introMatch) {
      introduction = introMatch[0].replace(/^(?:##\s*(?:introduction|overview))/i, '').trim();
      content = content.replace(introMatch[0], '');
    }
    
    if (conclusionMatch) {
      conclusion = conclusionMatch[0].replace(/^##\s*(?:conclu[s]?ion|summary)/i, '').trim();
      content = content.replace(conclusionMatch[0], '');
    }
    
    mainContent = content.trim();
    
    if (!introduction) introduction = 'Introduction text will go here.';
    if (!conclusion) conclusion = 'Conclusion text will go here.';
    
    // Replace template variables
    let processedContent = templateContent
      .replace(/{{title}}/g, title)
      .replace(/{{date}}/g, postDate)
      .replace(/{{description}}/g, description)
      .replace(/{{primary_tag}}/g, primaryTag)
      .replace(/{{additional_tags}}/g, additionalTags)
      .replace(/{{image}}/g, image)
      .replace(/{{introduction}}/g, introduction)
      .replace(/{{main_content}}/g, mainContent)
      .replace(/{{conclusion}}/g, conclusion);
    
    // Replace template-specific sections with content if they exist
    const sectionRegex = /{{(\w+)}}/g;
    processedContent = processedContent.replace(sectionRegex, 'Content for this section will be added.');
    
    // Create final filename
    const slug = createSlug(title);
    const finalFilename = `${postDate}-${slug}.md`;
    const outputPath = path.join(postsDir, finalFilename);
    const processedPath = path.join(processedDir, path.basename(filePath));
    
    // Write the new post file
    fs.writeFileSync(outputPath, processedContent);
    console.log(`Created post: ${outputPath}`);
    
    // Move original file to processed directory
    fs.renameSync(filePath, processedPath);
    console.log(`Moved original file to: ${processedPath}`);
    
    return outputPath;
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
    return null;
  }
}

/**
 * Process all new posts in the directory
 */
async function processNewPosts() {
  try {
    if (!fs.existsSync(newPostsDir)) {
      console.warn(`New posts directory does not exist: ${newPostsDir}`);
      return;
    }
    
    const files = fs.readdirSync(newPostsDir);
    const postFiles = files.filter(file => 
      (file.endsWith('.md') || file.endsWith('.txt')) && 
      !file.startsWith('.') && 
      fs.statSync(path.join(newPostsDir, file)).isFile()
    );
    
    if (postFiles.length === 0) {
      console.log('No new posts to process.');
      return;
    }
    
    console.log(`Found ${postFiles.length} new post(s) to process.`);
    
    for (const file of postFiles) {
      await processPost(path.join(newPostsDir, file));
    }
    
    console.log('All posts processed successfully!');
  } catch (error) {
    console.error('Error processing posts:', error);
  }
}

// Run the processor
processNewPosts();