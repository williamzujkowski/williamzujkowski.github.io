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
  cryptography: 'https://images.unsplash.com/photo-1639762681057-408e52192e55?q=80&w=1600&auto=format&fit=crop',
  quantum: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1600&auto=format&fit=crop',
  'edge-computing': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1600&auto=format&fit=crop',
  hpc: 'https://images.unsplash.com/photo-1597852074816-d933c7d2b988?q=80&w=1600&auto=format&fit=crop',
  rag: 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600&auto=format&fit=crop',
  'prompt-engineering': 'https://images.unsplash.com/photo-1526378722484-bd91ca387e72?q=80&w=1600&auto=format&fit=crop',
  containers: 'https://images.unsplash.com/photo-1605745341075-1b7460b99df8?q=80&w=1600&auto=format&fit=crop',
  resilience: 'https://images.unsplash.com/photo-1533073526757-2c8ca1df9f1c?q=80&w=1600&auto=format&fit=crop',
  llm: 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1600&auto=format&fit=crop',
  ai: 'https://images.unsplash.com/photo-1677442135969-00adbd2f9844?q=80&w=1600&auto=format&fit=crop',
  security: 'https://images.unsplash.com/photo-1614064641938-3bbee52942c7?q=80&w=1600&auto=format&fit=crop',
  cloud: 'https://images.unsplash.com/photo-1484557052118-f32bd25b45b5?q=80&w=1600&auto=format&fit=crop',
  ethics: 'https://images.unsplash.com/photo-1589578527966-fdac0f44566c?q=80&w=1600&auto=format&fit=crop',
  transformer: 'https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?q=80&w=1600&auto=format&fit=crop',
  pizza: 'https://images.unsplash.com/photo-1593246049226-ded77bf90326?q=80&w=1600&auto=format&fit=crop',
  programming: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1600&auto=format&fit=crop',
  cybersecurity: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1600&auto=format&fit=crop',
  deepfake: 'https://images.unsplash.com/photo-1614064642639-e398c3591a40?q=80&w=1600&auto=format&fit=crop',
  machine_learning: 'https://images.unsplash.com/photo-1655720035861-ba4147ea7725?q=80&w=1600&auto=format&fit=crop',
  opensource: 'https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?q=80&w=1600&auto=format&fit=crop'
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
    
    // Read each file and extract tags
    for (const file of files) {
      const filePath = path.join(postsDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Extract frontmatter
      const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
      if (frontmatterMatch) {
        const frontmatter = frontmatterMatch[1];
        
        // Extract tags
        const tagsMatch = frontmatter.match(/tags:\s*\[([^\]]+)\]/);
        if (tagsMatch) {
          const tags = tagsMatch[1].split(',').map(tag => 
            tag.trim().replace(/["']/g, '')
          );
          
          // Add to set of all tags
          tags.forEach(tag => {
            if (tag && tag !== 'posts') {
              allTags.add(tag);
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
  // Generate filename based on tag
  const tagKey = tag.toLowerCase().replace(/\s+/g, '-');
  const filename = `${tagKey}.jpg`;
  const relativePath = `blog/topics/${filename}`;
  
  // Add to image mapping
  if (!config.image_mapping[tagKey]) {
    config.image_mapping[tagKey] = {
      path: relativePath,
      alt: `${tag} illustration`
    };
    
    // Add to keyword mapping if it doesn't exist
    if (!config.keyword_mapping[tagKey]) {
      config.keyword_mapping[tagKey] = [tag.toLowerCase()];
    }
    
    // Write updated config
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`✅ Updated configuration for tag: ${tag}`);
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