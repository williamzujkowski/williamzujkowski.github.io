#!/usr/bin/env node

/**
 * Fix Citations Script
 * 
 * This script removes citation artifacts like "citeturn0academia0" from blog posts
 * that appear to be artifacts from AI generation.
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current file directory with ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const POSTS_DIR = path.join(__dirname, '..', 'src', 'posts');

async function fixCitations() {
  try {
    // Get list of files in posts directory
    const files = await fs.readdir(POSTS_DIR);
    const postFiles = files.filter(file => file.endsWith('.md'));
    
    if (postFiles.length === 0) {
      console.log('No posts found.');
      return;
    }
    
    console.log(`Found ${postFiles.length} posts to check for citation artifacts.`);
    let fixedCount = 0;
    
    // Process each file
    for (const file of postFiles) {
      const filePath = path.join(POSTS_DIR, file);
      const content = await fs.readFile(filePath, 'utf-8');
      
      // Check for citation artifacts (citeturn pattern)
      const citationRegex = /\s+citeturn\w+/g;
      
      if (content.includes('citeturn')) {
        // Remove the citations
        const fixedContent = content.replace(/\s+citeturn\w+/g, '');
        
        // Write the fixed content back to the file
        await fs.writeFile(filePath, fixedContent);
        
        fixedCount++;
        console.log(`Fixed citations in: ${file}`);
      }
    }
    
    console.log(`Citation fixing complete! Fixed ${fixedCount} files.`);
    
  } catch (error) {
    console.error('Error fixing citations:', error);
    process.exit(1);
  }
}

// Run the function
fixCitations();