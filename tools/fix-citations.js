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
    
    // Common citation patterns to look for and clean up
    const citationPatterns = [
      { pattern: /\s+citeturn\w+/g, name: "citeturn marker" },
      { pattern: /\s+\[\d+\]/g, name: "numeric reference" },
      { pattern: /\s+\(citation\s*\d*\)/gi, name: "citation placeholder" },
      { pattern: /\s+\[citation\s*needed\]/gi, name: "citation needed" },
      { pattern: /\s+\[ref\]/gi, name: "ref marker" }
    ];
    
    // Process each file
    for (const file of postFiles) {
      const filePath = path.join(POSTS_DIR, file);
      const content = await fs.readFile(filePath, 'utf-8');
      
      let hasChanges = false;
      let fixedContent = content;
      
      // Check for all citation artifacts
      for (const { pattern, name } of citationPatterns) {
        if (pattern.test(fixedContent)) {
          // Reset the RegExp lastIndex
          pattern.lastIndex = 0;
          
          // Count matches before replacing
          const matches = fixedContent.match(pattern) || [];
          
          if (matches.length > 0) {
            // Remove the citations
            fixedContent = fixedContent.replace(pattern, '');
            hasChanges = true;
            console.log(`  - Removed ${matches.length} ${name}(s) from ${file}`);
          }
        }
      }
      
      // Fix cases where multiple spaces might have been created
      if (hasChanges) {
        fixedContent = fixedContent.replace(/\s{2,}/g, ' ');
        
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