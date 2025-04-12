/**
 * Script to standardize frontmatter across all blog posts
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { glob } from 'glob';
import matter from 'gray-matter';

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');
const postsDir = path.join(rootDir, 'src', 'posts');
const imagesConfig = path.join(rootDir, 'src', '_data', 'config', 'blog', 'images.json');

// Create backup directory
const backupDir = path.join(rootDir, 'src', 'posts', 'backup');
if (!fs.existsSync(backupDir)) {
  fs.mkdirSync(backupDir, { recursive: true });
}

// Load blog images configuration
let blogImages = { image_mapping: {}, keyword_mapping: {} };
try {
  blogImages = JSON.parse(fs.readFileSync(imagesConfig, 'utf8'));
} catch (error) {
  console.error('Error loading blog images configuration:', error.message);
}

/**
 * Find the best image for a post based on its tags and content
 */
function findBestImage(post) {
  const tags = post.data.tags || [];
  const title = post.data.title || '';
  const content = post.content || '';
  
  // If post already has an image defined, use it
  if (post.data.image) {
    return {
      path: post.data.image,
      alt: post.data.image_alt || `Illustration for ${title}`
    };
  }
  
  // Check for tag matches in image mapping
  for (const tag of tags) {
    const normalizedTag = tag.toLowerCase().replace(/\s+/g, '-');
    if (blogImages.image_mapping[normalizedTag]) {
      return blogImages.image_mapping[normalizedTag];
    }
  }
  
  // Check title for keywords
  const titleLower = title.toLowerCase();
  for (const [key, keywords] of Object.entries(blogImages.keyword_mapping)) {
    for (const keyword of keywords) {
      if (titleLower.includes(keyword.toLowerCase()) && blogImages.image_mapping[key]) {
        return blogImages.image_mapping[key];
      }
    }
  }
  
  // Check first 500 chars of content for keywords
  const contentPreview = content.substring(0, 500).toLowerCase();
  for (const [key, keywords] of Object.entries(blogImages.keyword_mapping)) {
    for (const keyword of keywords) {
      if (contentPreview.includes(keyword.toLowerCase()) && blogImages.image_mapping[key]) {
        return blogImages.image_mapping[key];
      }
    }
  }
  
  // Default to a generic image if nothing else matches
  return blogImages.image_mapping.default || {
    path: "github-style/blog-placeholder.jpg",
    alt: "Blog post illustration"
  };
}

/**
 * Generate a description if missing
 */
function generateDescription(content, title) {
  // First, remove any image tags that might be in the content
  let cleanContent = content
    .replace(/^!\[[^\]]*\]\([^)]+\)/g, '') // Remove leading markdown image
    .replace(/^!\[[^\]]*\]/g, '') // Remove image references without paths
    .replace(/^{% image [^%]* %}/g, '') // Remove image shortcodes
    .trim();
  
  // Remove markdown formatting
  const plainText = cleanContent
    .replace(/#+\s+(.*)/g, '$1') // Remove headings
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Remove links
    .replace(/!\[[^\]]*\]\([^)]+\)/g, '') // Remove images
    .replace(/`{1,3}[^`]*`{1,3}/g, '') // Remove code
    .replace(/\*\*([^*]*)\*\*/g, '$1') // Remove bold
    .replace(/\*([^*]*)\*/g, '$1') // Remove italic
    .replace(/>\s*(.*)/g, '$1') // Remove blockquotes
    .replace(/\n+/g, ' ') // Replace newlines with spaces
    .replace(/{% .* %}/g, '') // Remove template tags
    .replace(/\[\^[\d:]+\]/g, '') // Remove footnote references
    .trim();
  
  // Get first paragraph (up to 160 chars)
  const firstParagraph = plainText.split('. ')[0];
  if (firstParagraph.length <= 160) {
    return firstParagraph;
  }
  
  // If it's too long, truncate and add ellipsis
  return firstParagraph.substring(0, 157) + '...';
}

/**
 * Standardize tags
 */
function standardizeTags(tags) {
  let allTags = [];
  
  // Handle different tag formats
  if (Array.isArray(tags)) {
    allTags = [...tags];
  } else if (typeof tags === 'string') {
    // Handle space-separated tags string: "posts tag1 tag2"
    if (tags.includes(' ') && !tags.includes(',')) {
      allTags = tags.split(/\s+/).filter(tag => tag.trim() !== '');
    } else {
      // Handle single tag
      allTags = [tags];
    }
  } else if (tags) {
    // Handle other formats
    allTags = [tags.toString()];
  }
  
  // Clean up tags - remove any duplicate references to 'posts'
  const cleanTags = allTags.flatMap(tag => {
    if (tag.includes(' ') && tag !== 'posts') {
      // Handle "posts tag1 tag2 tag3" format
      return tag.split(/\s+/).filter(t => t.trim() !== '');
    }
    return tag;
  });
  
  // Deduplicate tags and ensure they're clean
  const uniqueTags = Array.from(new Set(cleanTags.map(tag => tag.trim())
    .filter(tag => tag !== '')));
  
  // Remove 'posts' if it exists in the array
  const filteredTags = uniqueTags.filter(tag => tag !== 'posts');
  
  // Add 'posts' as the first tag
  return ['posts', ...filteredTags];
}

/**
 * Process a single post file
 */
async function processPost(filePath) {
  try {
    console.log(`Processing: ${path.basename(filePath)}`);
    
    // Read file content
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Parse frontmatter
    const { data, content: postContent } = matter(content);
    
    // Create backup
    const backupPath = path.join(backupDir, path.basename(filePath));
    fs.writeFileSync(backupPath, content);
    
    // Standardize frontmatter
    const standardizedData = {
      title: data.title,
      description: data.description || generateDescription(postContent, data.title),
      date: data.date,
      layout: 'post.njk',
      tags: standardizeTags(data.tags),
    };
    
    // Find best image
    const bestImage = findBestImage({ data: standardizedData, content: postContent });
    standardizedData.image = bestImage.path;
    standardizedData.image_alt = bestImage.alt;
    
    // Clean up description to remove leading image references
    if (standardizedData.description && standardizedData.description.startsWith('!')) {
      standardizedData.description = standardizedData.description
        .replace(/^!\[[^\]]*\]\([^)]+\)\s*/g, '')
        .replace(/^!\[[^\]]*\]\s*/g, '')
        .trim();
      
      // If description is now too short, regenerate it
      if (standardizedData.description.length < 50) {
        standardizedData.description = generateDescription(postContent, data.title);
      }
    }
    
    // Create new content with standardized frontmatter
    const newContent = matter.stringify(postContent, standardizedData);
    
    // Write updated file
    fs.writeFileSync(filePath, newContent);
    
    console.log(`✅ Updated: ${path.basename(filePath)}`);
    return true;
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    return false;
  }
}

async function main() {
  console.log('🔄 Standardizing blog post frontmatter...');
  
  try {
    // Find all blog post files
    const files = await glob('*.md', { cwd: postsDir });
    
    // Process each file
    let successCount = 0;
    for (const file of files) {
      const filePath = path.join(postsDir, file);
      const success = await processPost(filePath);
      if (success) successCount++;
    }
    
    console.log(`\n✅ Processed ${successCount} of ${files.length} files successfully`);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();