/**
 * Enhanced script to download blog post images based on configuration and tags
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import fetch from 'node-fetch';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';
import { glob } from 'glob';

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

// Load blog images configuration
const configPath = path.join(rootDir, 'src', '_data', 'config', 'blog', 'images.json');
const blogImagesDir = path.join(rootDir, 'assets', 'images', 'blog', 'topics');
const blogMainImagesDir = path.join(rootDir, 'assets', 'images', 'blog');
const postsDir = path.join(rootDir, 'src', 'posts');

// Ensure blog images directories exist
if (!fs.existsSync(blogImagesDir)) {
  fs.mkdirSync(blogImagesDir, { recursive: true });
}
if (!fs.existsSync(blogMainImagesDir)) {
  fs.mkdirSync(blogMainImagesDir, { recursive: true });
}

// API Keys - Replace with your own if needed
// For Unsplash: Register at https://unsplash.com/developers
// For Pixabay: Register at https://pixabay.com/api/docs/
// For Pexels: Register at https://www.pexels.com/api/
const API_KEYS = {
  UNSPLASH_ACCESS_KEY: 'YOUR_UNSPLASH_ACCESS_KEY', // Optional: Add your key here
  PIXABAY_API_KEY: 'YOUR_PIXABAY_API_KEY', // Optional: Add your key here
  PEXELS_API_KEY: 'YOUR_PEXELS_API_KEY' // Optional: Add your key here
};

// Define image sources for known topics
const imageSources = {
  // Core technology
  cryptography: 'https://images.unsplash.com/photo-1639762681057-408e52192e55?q=80&w=1600&auto=format&fit=crop',
  quantum: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1600&auto=format&fit=crop',
  'edge-computing': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1600&auto=format&fit=crop',
  edge: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1600&auto=format&fit=crop',
  hpc: 'https://images.unsplash.com/photo-1597852074816-d933c7d2b988?q=80&w=1600&auto=format&fit=crop',
  rag: 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600&auto=format&fit=crop',
  'prompt-engineering': 'https://images.unsplash.com/photo-1526378722484-bd91ca387e72?q=80&w=1600&auto=format&fit=crop',
  containers: 'https://images.unsplash.com/photo-1605745341075-1b7460b99df8?q=80&w=1600&auto=format&fit=crop',
  resilience: 'https://images.unsplash.com/photo-1533073526757-2c8ca1df9f1c?q=80&w=1600&auto=format&fit=crop',
  
  // AI and ML
  llm: 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1600&auto=format&fit=crop',
  ai: 'https://images.unsplash.com/photo-1677442135969-00adbd2f9844?q=80&w=1600&auto=format&fit=crop',
  'machine-learning': 'https://images.unsplash.com/photo-1655720035861-ba4147ea7725?q=80&w=1600&auto=format&fit=crop',
  'machine_learning': 'https://images.unsplash.com/photo-1655720035861-ba4147ea7725?q=80&w=1600&auto=format&fit=crop',
  'deep-learning': 'https://images.unsplash.com/photo-1591453089816-0fbb971b454c?q=80&w=1600&auto=format&fit=crop',
  transformer: 'https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?q=80&w=1600&auto=format&fit=crop',
  'reinforcement-learning': 'https://images.unsplash.com/photo-1456428746267-a1756408f782?q=80&w=1600&auto=format&fit=crop',
  'multimodal-llm': 'https://images.unsplash.com/photo-1633613286848-e6f43bbafb8d?q=80&w=1600&auto=format&fit=crop',
  'embodied-ai': 'https://images.unsplash.com/photo-1546776310-eef45dd6d63c?q=80&w=1600&auto=format&fit=crop',
  robotics: 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=1600&auto=format&fit=crop',
  
  // Security
  security: 'https://images.unsplash.com/photo-1614064641938-3bbee52942c7?q=80&w=1600&auto=format&fit=crop',
  cybersecurity: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1600&auto=format&fit=crop',
  'national-security': 'https://images.unsplash.com/photo-1569792063396-8a941bec4d06?q=80&w=1600&auto=format&fit=crop',
  deepfake: 'https://images.unsplash.com/photo-1572304320973-82db05a6c439?q=80&w=1600&auto=format&fit=crop',
  
  // Cloud & DevOps
  cloud: 'https://images.unsplash.com/photo-1484557052118-f32bd25b45b5?q=80&w=1600&auto=format&fit=crop',
  devops: 'https://images.unsplash.com/photo-1517420879524-86d64ac2f339?q=80&w=1600&auto=format&fit=crop',
  architecture: 'https://images.unsplash.com/photo-1470175369463-7bb9f41439f1?q=80&w=1600&auto=format&fit=crop',
  
  // Other tech 
  database: 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=1600&auto=format&fit=crop',
  ethics: 'https://images.unsplash.com/photo-1589578527966-fdac0f44566c?q=80&w=1600&auto=format&fit=crop',
  pizza: 'https://images.unsplash.com/photo-1593246049226-ded77bf90326?q=80&w=1600&auto=format&fit=crop',
  programming: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1600&auto=format&fit=crop',
  opensource: 'https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?q=80&w=1600&auto=format&fit=crop',
  'computational-science': 'https://images.unsplash.com/photo-1620662736427-b8a198f52a4d?q=80&w=1600&auto=format&fit=crop',
  exascale: 'https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?q=80&w=1600&auto=format&fit=crop',
  sustainability: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?q=80&w=1600&auto=format&fit=crop',
  
  // Quantum specific
  'quantum-computing': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1600&auto=format&fit=crop',
  'quantum-algorithms': 'https://images.unsplash.com/photo-1516110833967-0b5716ca1387?q=80&w=1600&auto=format&fit=crop',
  'quantum-supremacy': 'https://images.unsplash.com/photo-1576400883215-7083980b6193?q=80&w=1600&auto=format&fit=crop'
};

/**
 * Download an image from a URL
 */
async function downloadImage(url, imagePath) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch image: ${response.statusText}`);
    }
    
    await pipeline(response.body, createWriteStream(imagePath));
    console.log(`✅ Downloaded: ${path.basename(imagePath)}`);
    return true;
  } catch (error) {
    console.error(`❌ Error downloading ${url}:`, error.message);
    return false;
  }
}

/**
 * Search for an image on Unsplash
 */
async function searchUnsplashImage(query) {
  if (!API_KEYS.UNSPLASH_ACCESS_KEY || API_KEYS.UNSPLASH_ACCESS_KEY === 'YOUR_UNSPLASH_ACCESS_KEY') {
    // Use fallback URL without API
    const encodedQuery = encodeURIComponent(query);
    return `https://source.unsplash.com/featured/?${encodedQuery}`;
  }
  
  try {
    const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=1`;
    const response = await fetch(url, {
      headers: {
        'Authorization': `Client-ID ${API_KEYS.UNSPLASH_ACCESS_KEY}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`Unsplash API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.results && data.results.length > 0) {
      return `${data.results[0].urls.raw}&q=80&w=1600&auto=format&fit=crop`;
    }
    
    return null;
  } catch (error) {
    console.error(`Error searching Unsplash: ${error.message}`);
    return null;
  }
}

/**
 * Search for an image on Pixabay
 */
async function searchPixabayImage(query) {
  if (!API_KEYS.PIXABAY_API_KEY || API_KEYS.PIXABAY_API_KEY === 'YOUR_PIXABAY_API_KEY') {
    return null;
  }
  
  try {
    const url = `https://pixabay.com/api/?key=${API_KEYS.PIXABAY_API_KEY}&q=${encodeURIComponent(query)}&image_type=photo&per_page=3`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Pixabay API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.hits && data.hits.length > 0) {
      return data.hits[0].largeImageURL;
    }
    
    return null;
  } catch (error) {
    console.error(`Error searching Pixabay: ${error.message}`);
    return null;
  }
}

/**
 * Search for an image on Pexels
 */
async function searchPexelsImage(query) {
  if (!API_KEYS.PEXELS_API_KEY || API_KEYS.PEXELS_API_KEY === 'YOUR_PEXELS_API_KEY') {
    return null;
  }
  
  try {
    const url = `https://api.pexels.com/v1/search?query=${encodeURIComponent(query)}&per_page=1`;
    const response = await fetch(url, {
      headers: {
        'Authorization': API_KEYS.PEXELS_API_KEY
      }
    });
    
    if (!response.ok) {
      throw new Error(`Pexels API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.photos && data.photos.length > 0) {
      return data.photos[0].src.large2x;
    }
    
    return null;
  } catch (error) {
    console.error(`Error searching Pexels: ${error.message}`);
    return null;
  }
}

/**
 * Find an image URL for a given tag
 */
async function findImageForTag(tag, config) {
  // 1. Check if we have a predefined source
  const normalizedTag = tag.toLowerCase().replace(/\s+/g, '_');
  if (imageSources[normalizedTag]) {
    return imageSources[normalizedTag];
  }
  
  // 2. Check if tag matches any keywords in the mapping
  if (config.keyword_mapping) {
    for (const [key, keywords] of Object.entries(config.keyword_mapping)) {
      if (keywords.includes(tag.toLowerCase()) && imageSources[key]) {
        return imageSources[key];
      }
    }
  }
  
  // 3. Try searching on image services
  // Try Unsplash first (works without API key)
  const unsplashUrl = await searchUnsplashImage(tag);
  if (unsplashUrl) return unsplashUrl;
  
  // Try Pixabay if we have an API key
  const pixabayUrl = await searchPixabayImage(tag);
  if (pixabayUrl) return pixabayUrl;
  
  // Try Pexels if we have an API key
  const pexelsUrl = await searchPexelsImage(tag);
  if (pexelsUrl) return pexelsUrl;
  
  // No image found
  return null;
}

/**
 * Extract tags from blog posts
 */
async function extractTagsFromPosts() {
  try {
    // Find all blog post files
    const files = await glob('*.md', { cwd: postsDir });
    const allTags = new Set();
    
    // Add default tags we want images for - these are the most common categories
    const defaultTags = [
      'quantum', 'security', 'ai', 'cloud', 'llm', 'programming', 'cybersecurity', 'ethics', 
      'transformer', 'hpc', 'cryptography', 'edge', 'rag', 'prompt', 'containers', 'resilience',
      'deepfake', 'machine-learning', 'opensource', 'devops', 'robotics', 'database'
    ];
    
    defaultTags.forEach(tag => allTags.add(tag));
    
    // Read each file and extract tags
    for (const file of files) {
      const filePath = path.join(postsDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Extract frontmatter
      const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
      if (frontmatterMatch) {
        const frontmatter = frontmatterMatch[1];
        
        // Try multiple tag formats
        let tags = [];
        
        // Format 1: tags: [tag1, tag2, tag3]
        const tagsArrayMatch = frontmatter.match(/tags:\s*\[([^\]]+)\]/);
        if (tagsArrayMatch) {
          tags = tagsArrayMatch[1].split(',').map(tag => 
            tag.trim().replace(/["']/g, '')
          );
        } 
        // Format 2: tags: tag1, tag2, tag3
        else {
          const tagsSimpleMatch = frontmatter.match(/tags:\s*(.*)/);
          if (tagsSimpleMatch) {
            tags = tagsSimpleMatch[1].split(',').map(tag => 
              tag.trim().replace(/["']/g, '')
            );
          }
        }
        
        // Format 3: single tag: tags: posts
        if (tags.length === 0) {
          const tagsSingleMatch = frontmatter.match(/tags:\s*(\w+)/);
          if (tagsSingleMatch) {
            tags = [tagsSingleMatch[1]];
          }
        }
        
        // Add extracted tags to the set (individually)
        tags.forEach(tag => {
          if (tag && tag !== 'posts') {
            // For compound tags, split them and add individual keywords
            if (tag.includes(' ')) {
              const parts = tag.split(' ').filter(part => part.length > 2);
              parts.forEach(part => {
                if (part && part !== 'posts' && part !== 'and' && part !== 'the') {
                  allTags.add(part);
                }
              });
            } else {
              allTags.add(tag);
            }
          }
        });
        
        // Extract title for additional keywords
        const titleMatch = frontmatter.match(/title:\s*["'](.+?)["']/);
        if (titleMatch) {
          const title = titleMatch[1].toLowerCase();
          
          // Check for key topics in the title
          const titleKeywords = [
            'quantum', 'security', 'ai', 'cloud', 'llm', 'programming', 
            'cybersecurity', 'ethics', 'transformer', 'hpc', 'cryptography',
            'edge', 'rag', 'prompt', 'containers', 'resilience', 'deepfake',
            'machine learning', 'open source', 'devops', 'robotics'
          ];
          
          titleKeywords.forEach(keyword => {
            if (title.includes(keyword)) {
              allTags.add(keyword.replace(/\s+/g, '-'));
            }
          });
        }
      }
    }
    
    return Array.from(allTags);
  } catch (error) {
    console.error('Error extracting tags:', error);
    return [];
  }
}

/**
 * Update the images.json configuration file
 */
async function updateConfig(config, tag, imageUrl) {
  // Generate filename based on tag - limit to 50 chars to avoid issues with long filenames
  // For complex multi-word tags, use only the first keyword
  let tagKey;
  if (tag.includes(' ')) {
    // For complex tags like "posts ai robotics", just use the first keyword after "posts"
    const parts = tag.split(' ').filter(part => part !== 'posts');
    tagKey = parts.length > 0 ? parts[0].toLowerCase() : 'tag';
  } else {
    tagKey = tag.toLowerCase();
  }
  
  // Clean the tag key and limit length
  tagKey = tagKey.replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
  if (tagKey.length > 50) tagKey = tagKey.substring(0, 50);
  
  const filename = `${tagKey}.jpg`;
  const relativePath = `blog/topics/${filename}`;
  
  // Add to image mapping
  if (!config.image_mapping[tagKey]) {
    config.image_mapping[tagKey] = {
      path: relativePath,
      alt: `${tag.split(' ').slice(0, 3).join(' ')} illustration`
    };
    
    // Add to keyword mapping if it doesn't exist
    if (!config.keyword_mapping[tagKey]) {
      config.keyword_mapping[tagKey] = [tagKey.toLowerCase()];
    }
    
    // Write updated config
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`✅ Updated configuration for tag: ${tagKey} (from "${tag}")`);
  }
  
  return { tagKey, filename, relativePath };
}

async function main() {
  console.log('🖼️ Enhanced blog image downloader starting...');
  
  // Check if config exists
  if (!fs.existsSync(configPath)) {
    console.error('❌ Blog images configuration not found');
    return;
  }
  
  // Load config
  let config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  if (!config.image_mapping) config.image_mapping = {};
  if (!config.keyword_mapping) config.keyword_mapping = {};
  
  // Download predefined images first
  const downloadPromises = [];
  console.log('📥 Downloading predefined images...');
  
  for (const [key, imageUrl] of Object.entries(imageSources)) {
    if (config.image_mapping[key] && config.image_mapping[key].path.startsWith('blog/topics/')) {
      const filename = path.basename(config.image_mapping[key].path);
      const imagePath = path.join(blogImagesDir, filename);
      
      // Check if file exists and has content
      if (!fs.existsSync(imagePath) || fs.statSync(imagePath).size === 0) {
        downloadPromises.push(downloadImage(imageUrl, imagePath));
      } else {
        console.log(`⏭️ Skipping existing image: ${filename}`);
      }
    }
  }
  
  await Promise.all(downloadPromises);
  
  // Extract tags from blog posts
  console.log('🔍 Extracting tags from blog posts...');
  const tags = await extractTagsFromPosts();
  console.log(`Found ${tags.length} unique tags in blog posts`);
  
  // Process each tag
  console.log('🔄 Processing tags and finding images...');
  for (const tag of tags) {
    const tagKey = tag.toLowerCase().replace(/\s+/g, '-');
    
    // Skip if we already have this tag in the configuration
    if (config.image_mapping[tagKey]) {
      const filename = path.basename(config.image_mapping[tagKey].path);
      const imagePath = path.join(rootDir, 'assets', 'images', config.image_mapping[tagKey].path);
      
      // Check if the file exists
      if (fs.existsSync(imagePath) && fs.statSync(imagePath).size > 0) {
        console.log(`⏭️ Skipping existing tag: ${tag}`);
        continue;
      }
    }
    
    console.log(`🔎 Finding image for tag: ${tag}`);
    const imageUrl = await findImageForTag(tag, config);
    
    if (imageUrl) {
      // Update configuration
      const { filename, relativePath } = await updateConfig(config, tag, imageUrl);
      const imagePath = path.join(blogImagesDir, filename);
      
      // Download the image
      console.log(`📥 Downloading image for tag: ${tag}`);
      const success = await downloadImage(imageUrl, imagePath);
      
      if (success) {
        // Reload config after update
        config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      }
    } else {
      console.log(`⚠️ No image found for tag: ${tag}`);
    }
  }
  
  console.log('✅ Blog image download completed');
}

main().catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});