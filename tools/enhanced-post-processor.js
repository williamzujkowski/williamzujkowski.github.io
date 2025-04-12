#!/usr/bin/env node

/**
 * Enhanced Blog Post Processing Script
 * 
 * This script automates the blog post workflow with extended capabilities:
 * - Multiple input formats (txt, md, html)
 * - Advanced frontmatter generation
 * - AI-assisted tag and image suggestions
 * - Smart publication date scheduling
 * - Standardized post template application
 * - Content enhancement suggestions
 * - Citation cleanup and formatting
 * - SEO optimization helpers
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { existsSync } from 'fs';
import readline from 'readline';

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.join(__dirname, '..');

// Configuration
const SOURCE_DIR = path.join(rootDir, 'new_posts');
const TARGET_DIR = path.join(rootDir, 'src', 'posts');
const IMAGE_DIR = path.join(rootDir, 'assets', 'images', 'blog');
const IMAGE_CONFIG_PATH = path.join(rootDir, 'src', '_data', 'config', 'blog', 'images.json');
const TEMPLATE_PATH = path.join(rootDir, 'Prompts', 'post-template.md');
const PROCESSED_DIR = path.join(SOURCE_DIR, 'processed');
const DAYS_BETWEEN_POSTS = 10; // Base spacing between posts (10-14 days)

// Create interactive readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Helper function to prompt for user input
function prompt(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

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
  // Add some randomization to space posts naturally (10-14 days)
  date.setDate(date.getDate() + daysToAdd + Math.floor(Math.random() * 5));
  return date;
}

function formatDate(date) {
  return date.toISOString().split('T')[0]; // YYYY-MM-DD format
}

async function getPostTemplate() {
  try {
    if (existsSync(TEMPLATE_PATH)) {
      return await fs.readFile(TEMPLATE_PATH, 'utf-8');
    }
    
    // Default template if no file exists
    return `---
title: "{{POST_TITLE}}"
date: {{POST_DATE}}
layout: post.njk
tags: {{POST_TAGS}}
description: "{{POST_DESCRIPTION}}"
image: {{IMAGE_PATH}}
image_alt: "{{IMAGE_ALT}}"
---

{{POST_CONTENT}}

## Further Resources

- [Resource 1](https://example.com)
- [Resource 2](https://example.com)
`;
  } catch (error) {
    console.error('Error loading post template:', error);
    // Fallback minimal template
    return `---
title: "{{POST_TITLE}}"
date: {{POST_DATE}}
layout: post.njk
tags: {{POST_TAGS}}
---

{{POST_CONTENT}}
`;
  }
}

async function loadImageConfig() {
  try {
    if (existsSync(IMAGE_CONFIG_PATH)) {
      const configData = await fs.readFile(IMAGE_CONFIG_PATH, 'utf-8');
      return JSON.parse(configData);
    }
    return { image_mapping: {}, keyword_mapping: {} };
  } catch (error) {
    console.error('Error loading image configuration:', error);
    return { image_mapping: {}, keyword_mapping: {} };
  }
}

async function suggestImage(title, content, tags = []) {
  // Load image configuration
  const imageConfig = await loadImageConfig();
  const { image_mapping, keyword_mapping } = imageConfig;
  
  // Default image
  let imageKey = "default";
  
  // First, check if any tags match directly
  if (tags && tags.length > 0) {
    for (const tag of tags) {
      const lowercaseTag = tag.toLowerCase();
      if (image_mapping[lowercaseTag]) {
        imageKey = lowercaseTag;
        break;
      }
    }
  }
  
  // If still using default, try to infer from title and content
  if (imageKey === "default") {
    const titleLower = title.toLowerCase();
    const contentLower = content.toLowerCase();
    
    // Check each keyword mapping to find a match
    for (const [key, keywords] of Object.entries(keyword_mapping)) {
      for (const keyword of keywords) {
        if (titleLower.includes(keyword.toLowerCase()) || contentLower.includes(keyword.toLowerCase())) {
          imageKey = key;
          break;
        }
      }
      if (imageKey !== "default") break;
    }
  }
  
  // Get the image mapping
  const imageData = image_mapping[imageKey] || image_mapping["default"];
  
  return {
    path: imageData.path,
    alt: imageData.alt
  };
}

function guessTagsFromContent(title, content) {
  const tags = ['posts']; // Default tag for all posts
  
  // Clean and combine title and content for analysis
  const fullText = (title + ' ' + content).toLowerCase();
  
  // Common topics to check for
  const topicTags = {
    'security': ['security', 'cybersecurity', 'encryption', 'privacy', 'vulnerability', 'exploit', 'threat'],
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'neural network', 'deep learning', 'llm', 'transformer'],
    'cloud': ['cloud', 'aws', 'azure', 'gcp', 'kubernetes', 'container', 'serverless'],
    'devops': ['devops', 'ci/cd', 'pipeline', 'automation', 'deployment', 'infrastructure'],
    'programming': ['code', 'programming', 'javascript', 'python', 'typescript', 'rust', 'go'],
    'architecture': ['architecture', 'microservice', 'system design', 'scale', 'resilience', 'reliability'],
    'quantum': ['quantum', 'qubit', 'superposition', 'entanglement'],
    'cryptography': ['cryptography', 'encryption', 'hash', 'signature', 'cipher', 'quantum-resistant'],
    'edge': ['edge computing', 'edge', 'iot', 'real-time', 'device'],
    'hpc': ['high-performance computing', 'hpc', 'supercomputing', 'compute', 'cluster'],
    'rag': ['retrieval augmented generation', 'rag', 'retrieval', 'vector'],
    'prompt': ['prompt engineering', 'prompt', 'instruction'],
    'containers': ['container', 'docker', 'kubernetes', 'k8s', 'orchestration', 'pod'],
    'resilience': ['resilient', 'resilience', 'fault tolerance', 'chaos', 'reliability'],
    'llm': ['llm', 'language model', 'gpt', 'claude', 'gemini', 'large language model'],
    'ethics': ['ethics', 'ethical', 'bias', 'fairness', 'responsible ai']
  };
  
  // Check content for each topic
  for (const [tag, keywords] of Object.entries(topicTags)) {
    if (keywords.some(keyword => fullText.includes(keyword))) {
      tags.push(tag);
    }
  }
  
  return tags;
}

function generateDescription(title, content, maxLength = 160) {
  // Clean up content by removing markdown and other formatting
  const cleanContent = content
    .replace(/\s+/g, ' ')          // Normalize whitespace
    .replace(/#+\s+.+?\n/g, '')    // Remove headers
    .replace(/\[.*?\]\(.*?\)/g, '') // Remove links
    .replace(/`.*?`/g, '')         // Remove inline code
    .replace(/```[\s\S]*?```/g, '') // Remove code blocks
    .replace(/!\[.*?\]\(.*?\)/g, '') // Remove images
    .trim();
  
  // Use the first paragraph that's not too short
  const paragraphs = cleanContent.split(/\n\n+/);
  let description = '';
  
  for (const paragraph of paragraphs) {
    if (paragraph.length > 40) {
      description = paragraph;
      break;
    }
  }
  
  // If no good paragraph found, use first 160 chars of cleaned content
  if (!description) {
    description = cleanContent;
  }
  
  // Truncate to max length and ensure it doesn't end mid-word
  if (description.length > maxLength) {
    description = description.substring(0, maxLength).trim();
    const lastSpaceIndex = description.lastIndexOf(' ');
    if (lastSpaceIndex > 0) {
      description = description.substring(0, lastSpaceIndex) + '...';
    } else {
      description += '...';
    }
  }
  
  return description;
}

function cleanupCitations(content) {
  let cleanedContent = content;
  let citationsRemoved = 0;
  
  // Clean up any citation artifacts
  const citationPatterns = [
    { pattern: /\s+citeturn\w+/g, name: "citeturn marker" },
    { pattern: /\s+\[\d+\]/g, name: "numeric reference" },
    { pattern: /\s+\(citation\s*\d*\)/gi, name: "citation placeholder" },
    { pattern: /\s+\[citation\s*needed\]/gi, name: "citation needed" },
    { pattern: /\s+\[ref\]/gi, name: "ref marker" }
  ];
  
  for (const { pattern, name } of citationPatterns) {
    if (pattern.test(cleanedContent)) {
      pattern.lastIndex = 0;
      const matches = cleanedContent.match(pattern) || [];
      if (matches.length > 0) {
        cleanedContent = cleanedContent.replace(pattern, '');
        citationsRemoved += matches.length;
      }
    }
  }
  
  // Fix cases where multiple spaces might have been created
  cleanedContent = cleanedContent.replace(/\s{2,}/g, ' ');
  
  return { cleanedContent, citationsRemoved };
}

function formatFrontMatter(metadata) {
  // Create YAML frontmatter
  let frontmatter = '---\n';
  
  for (const [key, value] of Object.entries(metadata)) {
    // For arrays (like tags), format as YAML array
    if (Array.isArray(value)) {
      frontmatter += `${key}:\n`;
      value.forEach(item => {
        frontmatter += `  - ${item}\n`;
      });
    } else if (typeof value === 'string') {
      // Escape quotes in string values
      const escapedValue = value.replace(/"/g, '\\"');
      frontmatter += `${key}: "${escapedValue}"\n`;
    } else {
      frontmatter += `${key}: ${value}\n`;
    }
  }
  
  frontmatter += '---\n\n';
  return frontmatter;
}

async function extractPostInfo(filename) {
  try {
    // Read the source file
    const sourceFilePath = path.join(SOURCE_DIR, filename);
    const content = await fs.readFile(sourceFilePath, 'utf-8');
    
    let title, body, existingMeta = {};
    const isMarkdown = filename.endsWith('.md');
    
    if (isMarkdown) {
      // Check if there's a markdown front matter
      const frontMatterMatch = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
      if (frontMatterMatch) {
        const frontMatter = frontMatterMatch[1];
        body = frontMatterMatch[2].trim();
        
        // Extract title from frontmatter
        const titleMatch = frontMatter.match(/title:\s*["']?([^"'\n]+)["']?/);
        if (titleMatch) {
          title = titleMatch[1].trim();
        }
        
        // Extract other frontmatter fields
        const metaFields = ['date', 'tags', 'description', 'image', 'image_alt'];
        for (const field of metaFields) {
          const pattern = new RegExp(`${field}:\\s*(.+?)(?=\\n[a-z]+:|$)`, 's');
          const match = frontMatter.match(pattern);
          if (match) {
            let value = match[1].trim();
            
            // Handle tags specially
            if (field === 'tags') {
              // Handle both yaml array and space-separated formats
              if (value.startsWith('- ')) {
                // YAML array format
                const tagLines = value.split('\n').map(line => line.trim());
                value = tagLines
                  .filter(line => line.startsWith('- '))
                  .map(line => line.substring(2).trim());
              } else if (value.startsWith('[') && value.endsWith(']')) {
                // JS array format
                value = value.substring(1, value.length - 1).split(',').map(t => t.trim());
              } else {
                // Space-separated format
                value = value.split(/[\s,]+/).filter(Boolean);
              }
              existingMeta[field] = value;
            } else {
              // For other fields, remove quotes if present
              if ((value.startsWith('"') && value.endsWith('"')) || 
                  (value.startsWith("'") && value.endsWith("'"))) {
                value = value.substring(1, value.length - 1);
              }
              existingMeta[field] = value;
            }
          }
        }
        
        // If no title in frontmatter, look for H1
        if (!title) {
          const h1Matches = Array.from(body.matchAll(/^#\s+(.+?)($|\n)/gm));
          if (h1Matches.length > 0) {
            title = h1Matches[0][1].trim();
          }
        }
      } else {
        // No frontmatter, look for H1 headers
        const h1Matches = Array.from(content.matchAll(/^#\s+(.+?)($|\n)/gm));
        if (h1Matches.length > 0) {
          title = h1Matches[0][1].trim();
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
    
    return {
      title: title || `Untitled Post (${filename})`,
      body,
      existingMeta
    };
  } catch (error) {
    console.error(`Error extracting info from ${filename}:`, error);
    return null;
  }
}

async function processPost(filename, options = {}) {
  try {
    console.log(`\n🔍 Analyzing ${filename}...`);
    
    // Extract post information
    const postInfo = await extractPostInfo(filename);
    if (!postInfo) return null;
    
    const { title, body, existingMeta } = postInfo;
    
    // Create slug from title or use existing one
    const slug = existingMeta.slug || slugify(title);
    
    // Clean up citations
    const { cleanedContent, citationsRemoved } = cleanupCitations(body);
    if (citationsRemoved > 0) {
      console.log(`  🧹 Removed ${citationsRemoved} citation artifacts`);
    }
    
    // Calculate word count
    const wordCount = cleanedContent.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 230); // 230 words per minute
    console.log(`  📊 Word count: ${wordCount} (${readingTime} min read)`);
    
    // Determine date
    let postDate;
    if (options.customDate) {
      postDate = options.customDate;
    } else if (existingMeta.date) {
      postDate = existingMeta.date;
    } else {
      // Set future date if not provided
      const latestDate = await getLatestPostDate();
      postDate = formatDate(getNextPostDate(latestDate));
    }
    
    // Determine tags
    let tags;
    if (existingMeta.tags && existingMeta.tags.length > 0) {
      tags = existingMeta.tags;
      // Ensure 'posts' tag is included
      if (!tags.includes('posts')) {
        tags.unshift('posts');
      }
    } else {
      tags = guessTagsFromContent(title, cleanedContent);
    }
    
    // Format tags for display
    const tagsFormatted = tags.join(', ');
    console.log(`  🏷️  Suggested tags: ${tagsFormatted}`);
    
    // Generate description if not provided
    const description = existingMeta.description || generateDescription(title, cleanedContent);
    
    // Suggest image based on content and tags
    const suggestedImage = await suggestImage(title, cleanedContent, tags);
    const image = existingMeta.image || suggestedImage.path;
    const imageAlt = existingMeta.image_alt || suggestedImage.alt;
    console.log(`  🖼️  Image: ${image}`);
    
    // Prepare metadata
    const metadata = {
      title,
      date: postDate,
      layout: 'post.njk',
      tags,
      description,
      image,
      image_alt: imageAlt,
      ...options.additionalMeta
    };
    
    // Get post template
    const template = await getPostTemplate();
    
    // Combine frontmatter and content
    const frontmatter = formatFrontMatter(metadata);
    
    // Create final content
    let finalContent;
    
    // If template has placeholders, use them
    if (template.includes('{{POST_CONTENT}}')) {
      finalContent = template
        .replace('{{POST_TITLE}}', title)
        .replace('{{POST_DATE}}', postDate)
        .replace('{{POST_TAGS}}', tags.map(t => `"${t}"`).join(', '))
        .replace('{{POST_DESCRIPTION}}', description)
        .replace('{{IMAGE_PATH}}', image)
        .replace('{{IMAGE_ALT}}', imageAlt)
        .replace('{{POST_CONTENT}}', cleanedContent);
    } else {
      // Otherwise use standard frontmatter + content format
      finalContent = frontmatter + cleanedContent;
    }
    
    return {
      title,
      slug,
      date: postDate,
      content: finalContent,
      tags,
      wordCount,
      readingTime,
      imagePath: image
    };
  } catch (error) {
    console.error(`Error processing ${filename}:`, error);
    return null;
  }
}

async function batchProcessPosts(options = {}) {
  try {
    // Find latest post date
    const latestDate = await getLatestPostDate();
    console.log(`\n📅 Latest post date: ${formatDate(latestDate)}`);
    
    // Get list of files in source directory
    const files = await fs.readdir(SOURCE_DIR);
    const postFiles = files.filter(file => {
      // Filter out directories and processed files
      const filePath = path.join(SOURCE_DIR, file);
      const isDirectory = existsSync(filePath) && (file === 'processed' || file.startsWith('.'));
      return !isDirectory && (file.endsWith('.txt') || file.endsWith('.md'));
    });
    
    if (postFiles.length === 0) {
      console.log('📭 No new posts to process.');
      return [];
    }
    
    console.log(`\n🔎 Found ${postFiles.length} new posts to process.`);
    
    // Process each file
    const results = [];
    let currentDate = new Date(latestDate);
    
    for (const file of postFiles) {
      // Calculate the next date for this post
      const nextDate = formatDate(getNextPostDate(currentDate));
      const customOptions = { ...options, customDate: nextDate };
      
      const processed = await processPost(file, customOptions);
      if (processed) {
        results.push({
          file,
          processed
        });
        
        currentDate = new Date(processed.date);
      }
    }
    
    return results;
  } catch (error) {
    console.error('Error in batch process:', error);
    return [];
  }
}

async function writePosts(results) {
  console.log('\n📝 Writing processed posts:');
  
  // Create processed directory if it doesn't exist
  await fs.mkdir(PROCESSED_DIR, { recursive: true });
  
  for (const { file, processed } of results) {
    try {
      // Create the target filename
      const targetFilename = `${processed.date}-${processed.slug}.md`;
      const targetPath = path.join(TARGET_DIR, targetFilename);
      
      // Write the file
      await fs.writeFile(targetPath, processed.content);
      console.log(`  ✅ Created: ${targetFilename}`);
      
      // Move the processed file to the processed directory
      await fs.rename(
        path.join(SOURCE_DIR, file),
        path.join(PROCESSED_DIR, file)
      );
    } catch (error) {
      console.error(`  ❌ Error writing ${file}:`, error);
    }
  }
  
  return results.length;
}

async function processInteractive() {
  try {
    console.log('🔄 Starting interactive blog post processor...');
    
    // Get list of files in source directory
    const files = await fs.readdir(SOURCE_DIR);
    const postFiles = files.filter(file => {
      // Filter out directories and processed files
      const filePath = path.join(SOURCE_DIR, file);
      const isDirectory = existsSync(filePath) && (file === 'processed' || file.startsWith('.'));
      return !isDirectory && (file.endsWith('.txt') || file.endsWith('.md'));
    });
    
    if (postFiles.length === 0) {
      console.log('📭 No new posts to process.');
      rl.close();
      return;
    }
    
    console.log(`\n📄 Found ${postFiles.length} file(s) to process:\n${postFiles.map(f => '  - ' + f).join('\n')}`);
    
    const choice = await prompt('\n🔄 Process all posts? (y/n) ');
    
    if (choice.toLowerCase() === 'y') {
      // Process all posts
      const results = await batchProcessPosts();
      
      if (results.length > 0) {
        const writeChoice = await prompt('\n💾 Write posts to final destination? (y/n) ');
        
        if (writeChoice.toLowerCase() === 'y') {
          const count = await writePosts(results);
          console.log(`\n🎉 Successfully processed ${count} post(s).`);
        } else {
          console.log('\n⏸️  Processing cancelled. No files were written.');
        }
      }
    } else {
      // Individual post processing
      console.log('\n⚙️  Select a post to process:');
      for (let i = 0; i < postFiles.length; i++) {
        console.log(`  ${i + 1}. ${postFiles[i]}`);
      }
      
      const fileIndex = parseInt(await prompt('\nEnter file number: ')) - 1;
      
      if (fileIndex >= 0 && fileIndex < postFiles.length) {
        const selectedFile = postFiles[fileIndex];
        const processed = await processPost(selectedFile);
        
        if (processed) {
          console.log('\n📋 Preview of frontmatter:');
          const frontmatterLines = processed.content.split('---')[1].trim().split('\n');
          console.log('---');
          frontmatterLines.forEach(line => console.log(line));
          console.log('---');
          
          const writeChoice = await prompt('\n💾 Write post to final destination? (y/n) ');
          
          if (writeChoice.toLowerCase() === 'y') {
            await writePosts([{ file: selectedFile, processed }]);
            console.log(`\n🎉 Successfully processed ${selectedFile}.`);
          } else {
            console.log('\n⏸️  Processing cancelled. No file was written.');
          }
        }
      } else {
        console.log('❌ Invalid selection.');
      }
    }
    
    rl.close();
  } catch (error) {
    console.error('Error in interactive process:', error);
    rl.close();
  }
}

// Main function for CLI usage
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Enhanced Blog Post Processor

Usage:
  node enhanced-post-processor.js [options]

Options:
  --interactive, -i   Run in interactive mode
  --batch, -b         Process all posts without confirmation
  --help, -h          Show this help message

Examples:
  node enhanced-post-processor.js -i  # Run interactive mode
  node enhanced-post-processor.js -b  # Process all posts in batch mode
    `);
    return;
  }
  
  if (args.includes('--interactive') || args.includes('-i')) {
    await processInteractive();
  } else if (args.includes('--batch') || args.includes('-b')) {
    // Non-interactive batch mode
    const results = await batchProcessPosts();
    
    if (results.length > 0) {
      const count = await writePosts(results);
      console.log(`\n🎉 Successfully processed ${count} post(s).`);
    }
    rl.close();
  } else {
    // Default to interactive mode
    await processInteractive();
  }
}

// Run the main function
main().catch(error => {
  console.error('Unhandled error:', error);
  rl.close();
  process.exit(1);
});