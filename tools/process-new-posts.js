#!/usr/bin/env node

/**
 * Post Processing Script
 * 
 * This script automatically converts blog posts from the new_posts directory
 * to properly formatted Markdown files in the src/posts directory with:
 * - Proper frontmatter
 * - Date spacing (1-2 weeks apart)
 * - Standardized file naming
 * - Enhanced formatting
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current file directory with ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const SOURCE_DIR = path.join(__dirname, '..', 'new_posts');
const TARGET_DIR = path.join(__dirname, '..', 'src', 'posts');
const IMAGE_DIR = path.join(__dirname, '..', 'assets', 'images', 'blog');
const DAYS_BETWEEN_POSTS = 10; // Spacing between posts (10-14 days)

// Helper functions
function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
}

async function getLatestPostDate() {
  try {
    // List all posts and sort by filename (which starts with date)
    const files = await fs.readdir(TARGET_DIR);
    const postFiles = files.filter(file => file.match(/^\d{4}-\d{2}-\d{2}/));
    
    if (postFiles.length === 0) {
      // Default to current date if no posts exist
      return new Date();
    }
    
    // Sort in descending order (newest first)
    postFiles.sort().reverse();
    
    // Extract date from newest post filename
    const latestPostFile = postFiles[0];
    const dateMatch = latestPostFile.match(/^(\d{4}-\d{2}-\d{2})/);
    
    if (dateMatch && dateMatch[1]) {
      return new Date(dateMatch[1]);
    } else {
      return new Date();
    }
  } catch (error) {
    console.error('Error finding latest post date:', error);
    return new Date();
  }
}

function getNextPostDate(previousDate, daysToAdd = DAYS_BETWEEN_POSTS) {
  const date = new Date(previousDate);
  date.setDate(date.getDate() + daysToAdd);
  return date;
}

function formatDate(date) {
  return date.toISOString().split('T')[0]; // YYYY-MM-DD format
}

function guessTagsFromContent(content) {
  const tags = ['posts']; // Default tag for all posts
  
  // Common topics to check for
  const topicTags = {
    'security': ['security', 'cybersecurity', 'encryption', 'privacy', 'vulnerability'],
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'neural network', 'deep learning', 'llm', 'transformer'],
    'cloud': ['cloud', 'aws', 'azure', 'gcp', 'kubernetes', 'container', 'serverless'],
    'devops': ['devops', 'ci/cd', 'pipeline', 'automation', 'deployment', 'infrastructure'],
    'programming': ['code', 'programming', 'javascript', 'python', 'typescript', 'rust', 'go'],
    'architecture': ['architecture', 'microservice', 'system design', 'scale', 'resilience', 'reliability']
  };
  
  // Check content for each topic
  const contentLower = content.toLowerCase();
  for (const [tag, keywords] of Object.entries(topicTags)) {
    if (keywords.some(keyword => contentLower.includes(keyword))) {
      tags.push(tag);
    }
  }
  
  return tags;
}

function enhanceMarkdown(title, content) {
  // Basic frontmatter template
  let enhancedContent = `---
title: "${title}"
date: {{POST_DATE}}
layout: post.njk
tags: {{POST_TAGS}}
---

![{{IMAGE_ALT}}](/assets/images/blog/{{IMAGE_FILENAME}})

${content}`;

  return enhancedContent;
}

function suggestImage(title, content) {
  // Map keywords to existing images
  const imageMap = {
    'ai': 'ai-blog.jpg',
    'artificial intelligence': 'ai-blog.jpg',
    'machine learning': 'ai-blog.jpg',
    'cloud': 'cloud-blog.jpg',
    'security': 'security-blog.jpg',
    'cybersecurity': 'security-blog.jpg', 
    'transformer': 'transformer-blog.jpg',
    'ethics': 'ethics-blog.jpg',
    'pizza': 'pizza-blog.jpg',
  };
  
  // Default image if nothing matches
  let selectedImage = 'tech-header.jpg';
  let imageAlt = title;
  
  const contentLower = content.toLowerCase();
  
  // Check for matches
  for (const [keyword, image] of Object.entries(imageMap)) {
    if (title.toLowerCase().includes(keyword) || contentLower.includes(keyword)) {
      selectedImage = image;
      break;
    }
  }
  
  return { filename: selectedImage, alt: imageAlt };
}

async function processPost(filename) {
  try {
    // Read the source file
    const sourceFilePath = path.join(SOURCE_DIR, filename);
    const content = await fs.readFile(sourceFilePath, 'utf-8');
    
    let title, body;
    const isMarkdown = filename.endsWith('.md');
    
    if (isMarkdown) {
      // Check if there's a markdown front matter title first
      const frontMatterMatch = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
      if (frontMatterMatch) {
        const frontMatter = frontMatterMatch[1];
        const titleMatch = frontMatter.match(/title:\s*["']?([^"'\n]+)["']?/);
        if (titleMatch) {
          title = titleMatch[1].trim();
          body = frontMatterMatch[2].trim();
        } else {
          // Look for H1 headers if no title in front matter
          const h1Matches = Array.from(frontMatterMatch[2].matchAll(/^#\s+(.+?)($|\n)/gm));
          if (h1Matches.length > 0) {
            // Use the first H1 that's not "Summary"
            let foundTitle = null;
            for (const match of h1Matches) {
              if (match[1].trim().toLowerCase() !== "summary") {
                foundTitle = match[1].trim();
                break;
              }
            }
            title = foundTitle || h1Matches[0][1].trim();
            body = frontMatterMatch[2].trim();
          } else {
            // Use filename as title if no H1 found in frontmatter content
            title = filename.replace(/\.md$/, '').replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            body = frontMatterMatch[2].trim();
          }
        }
      } else {
        // Look for H1 headers if no front matter
        const h1Matches = Array.from(content.matchAll(/^#\s+(.+?)($|\n)/gm));
        if (h1Matches.length > 0) {
          // Use the first H1 that's not "Summary"
          let foundTitle = null;
          for (const match of h1Matches) {
            if (match[1].trim().toLowerCase() !== "summary") {
              foundTitle = match[1].trim();
              break;
            }
          }
          title = foundTitle || h1Matches[0][1].trim();
          
          // Don't remove the title from content - we want to keep the H1 headings
          body = content.trim();
        } else {
          // Use filename as title if no front matter or H1 found
          title = filename.replace(/\.md$/, '').replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
          body = content.trim();
        }
      }
    } else {
      // For .txt files, use first line as title and the rest as body (skip blank line)
      const lines = content.split('\n');
      title = lines[0].trim();
      body = lines.slice(2).join('\n').trim(); // Skip the title and blank line
    }
    
    // Create slug from title
    const slug = slugify(title);
    
    // Guess tags based on content
    const tags = guessTagsFromContent(content);
    
    // Suggest an image based on content
    const image = suggestImage(title, content);
    
    // Enhanced markdown with proper formatting
    let enhancedContent = enhanceMarkdown(title, body);
    
    // Replace placeholders
    enhancedContent = enhancedContent.replace('{{POST_TAGS}}', tags.join(', '));
    enhancedContent = enhancedContent.replace('{{IMAGE_FILENAME}}', image.filename);
    enhancedContent = enhancedContent.replace('{{IMAGE_ALT}}', image.alt);
    
    return {
      title,
      slug,
      content: enhancedContent,
      tags
    };
  } catch (error) {
    console.error(`Error processing ${filename}:`, error);
    return null;
  }
}

async function main() {
  try {
    // Find latest post date
    const latestDate = await getLatestPostDate();
    console.log(`Latest post date: ${formatDate(latestDate)}`);
    
    // Get list of files in source directory
    const files = await fs.readdir(SOURCE_DIR);
    const postFiles = files.filter(file => file.endsWith('.txt') || file.endsWith('.md'));
    
    // Filter out the "processed" directory
    const filesToProcess = postFiles.filter(file => file !== 'processed');
    
    if (filesToProcess.length === 0) {
      console.log('No new posts to process.');
      return;
    }
    
    console.log(`Found ${filesToProcess.length} new posts to process.`);
    let currentDate = latestDate;
    
    // Process each file
    for (const [index, file] of filesToProcess.entries()) {
      // Calculate the date for this post (spaced out from previous)
      currentDate = getNextPostDate(currentDate, DAYS_BETWEEN_POSTS + Math.floor(Math.random() * 5));
      const postDate = formatDate(currentDate);
      
      console.log(`Processing "${file}" with date ${postDate}...`);
      
      // Process the content
      const processed = await processPost(file);
      if (!processed) continue;
      
      // Add the date to the content
      const finalContent = processed.content.replace('{{POST_DATE}}', postDate);
      
      // Create the target filename
      const targetFilename = `${postDate}-${processed.slug}.md`;
      const targetPath = path.join(TARGET_DIR, targetFilename);
      
      // Write the file
      await fs.writeFile(targetPath, finalContent);
      console.log(`Created post: ${targetFilename}`);
      
      // Move the processed file to a backup or delete it
      const processedDir = path.join(SOURCE_DIR, 'processed');
      await fs.mkdir(processedDir, { recursive: true });
      await fs.rename(
        path.join(SOURCE_DIR, file),
        path.join(processedDir, file)
      );
    }
    
    console.log('Post processing complete!');
    
  } catch (error) {
    console.error('Error in main process:', error);
    process.exit(1);
  }
}

// Run the main function
main();