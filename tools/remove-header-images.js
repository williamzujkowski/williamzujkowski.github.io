/**
 * Script to remove header images from blog posts
 * 
 * This script searches for and removes the header image pattern that appears
 * at the start of many blog posts, specifically lines like:
 * ![High-Performance Computing infrastructure with advanced cooling systems](/assets/images/blog/tech-header.jpg)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current file's directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const POSTS_DIR = path.join(__dirname, '..', 'src', 'posts');
const IMAGE_PATTERN = /^!\[.*?\]\(\/assets\/images\/blog\/.*?\)(\r?\n){1,2}/m;

async function removeHeaderImagesFromPosts() {
  try {
    console.log('Removing header images from blog posts...');
    
    // Get all markdown files in the posts directory
    const files = await fs.promises.readdir(POSTS_DIR);
    const mdFiles = files.filter(file => file.endsWith('.md'));
    
    console.log(`Found ${mdFiles.length} markdown files to process`);
    
    let modifiedCount = 0;
    
    // Process each file
    for (const file of mdFiles) {
      const filePath = path.join(POSTS_DIR, file);
      const fileStats = await fs.promises.stat(filePath);
      
      // Skip if not a regular file
      if (!fileStats.isFile()) continue;
      
      // Read the file content
      const content = await fs.promises.readFile(filePath, 'utf8');
      
      // Look for the image pattern after the frontmatter
      // We're assuming frontmatter is at the top and ends with ---
      if (IMAGE_PATTERN.test(content)) {
        // Remove the image line
        const newContent = content.replace(IMAGE_PATTERN, '');
        
        // Write the updated content back to the file
        await fs.promises.writeFile(filePath, newContent);
        
        modifiedCount++;
        console.log(`Removed header image from: ${file}`);
      }
    }
    
    console.log(`Done! Modified ${modifiedCount} files out of ${mdFiles.length} total markdown files.`);
    
  } catch (error) {
    console.error('Error processing files:', error);
  }
}

// Run the script
removeHeaderImagesFromPosts();