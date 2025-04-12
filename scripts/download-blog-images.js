/**
 * Script to download blog post images based on configuration
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import fetch from 'node-fetch';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

// Load blog images configuration
const configPath = path.join(rootDir, 'src', '_data', 'config', 'blog', 'images.json');
const blogImagesDir = path.join(rootDir, 'assets', 'images', 'blog', 'topics');

// Ensure blog images directory exists
if (!fs.existsSync(blogImagesDir)) {
  fs.mkdirSync(blogImagesDir, { recursive: true });
}

// Define image sources
const imageSources = {
  cryptography: 'https://images.unsplash.com/photo-1639762681057-408e52192e55?q=80&w=1600&auto=format&fit=crop',
  quantum: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1600&auto=format&fit=crop',
  'edge-computing': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=1600&auto=format&fit=crop',
  hpc: 'https://images.unsplash.com/photo-1597852074816-d933c7d2b988?q=80&w=1600&auto=format&fit=crop',
  rag: 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600&auto=format&fit=crop',
  'prompt-engineering': 'https://images.unsplash.com/photo-1526378722484-bd91ca387e72?q=80&w=1600&auto=format&fit=crop',
  containers: 'https://images.unsplash.com/photo-1605745341075-1b7460b99df8?q=80&w=1600&auto=format&fit=crop',
  resilience: 'https://images.unsplash.com/photo-1533073526757-2c8ca1df9f1c?q=80&w=1600&auto=format&fit=crop',
  llm: 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1600&auto=format&fit=crop'
};

async function downloadImage(url, imagePath) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch image: ${response.statusText}`);
    }
    
    await pipeline(response.body, createWriteStream(imagePath));
    console.log(`✅ Downloaded: ${path.basename(imagePath)}`);
  } catch (error) {
    console.error(`❌ Error downloading ${url}:`, error.message);
  }
}

async function main() {
  console.log('🖼️ Downloading blog post images...');
  
  // Check if config exists
  if (!fs.existsSync(configPath)) {
    console.error('❌ Blog images configuration not found');
    return;
  }
  
  // Load config
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const imageMapping = config.image_mapping;
  
  // Download images
  const downloadPromises = [];
  
  for (const [key, imageUrl] of Object.entries(imageSources)) {
    if (imageMapping[key] && imageMapping[key].path.startsWith('blog/topics/')) {
      const filename = path.basename(imageMapping[key].path);
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
  console.log('✅ Blog image download completed');
}

main().catch(err => {
  console.error('❌ Error:', err);
  process.exit(1);
});