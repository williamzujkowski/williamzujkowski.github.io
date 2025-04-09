/**
 * Image optimization script
 * 
 * This script optimizes all images in the assets directory:
 * - Compresses images to reduce file size
 * - Generates WebP versions for modern browsers
 * - Preserves original format as fallback
 * - Creates responsive sizes for larger images
 * 
 * Usage: node scripts/optimize-images.js
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp'; // Make sure to install: npm install sharp

// Convert __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const config = {
  // Directories to scan for images
  imageDirs: [
    path.join(__dirname, '..', 'assets', 'images'),
    path.join(__dirname, '..', 'assets', 'icons')
  ],
  // Image quality settings
  quality: {
    jpeg: 80,
    webp: 75,
    avif: 65,
    png: 80
  },
  // Size breakpoints for responsive images
  sizes: [1920, 1280, 800, 640, 320],
  // Only resize images larger than this width
  resizeThreshold: 800,
  // Skip files matching these patterns
  skipPatterns: [
    /\.webp$/,
    /\.avif$/,
    /\-resized\-/,
    /\.min\./
  ]
};

// Process all images in the specified directories
async function optimizeImages() {
  console.log('Starting image optimization...');
  
  let totalSaved = 0;
  let totalProcessed = 0;
  
  for (const dir of config.imageDirs) {
    console.log(`\nScanning directory: ${dir}`);
    await processDirectory(dir);
  }
  
  console.log(`\nOptimization complete!`);
  console.log(`Total images processed: ${totalProcessed}`);
  console.log(`Total space saved: ${formatBytes(totalSaved)}`);
  
  // Process a directory recursively
  async function processDirectory(directory) {
    try {
      const entries = await fs.readdir(directory, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(directory, entry.name);
        
        if (entry.isDirectory()) {
          // Process subdirectories recursively
          await processDirectory(fullPath);
        } else if (isImage(entry.name) && !shouldSkip(entry.name)) {
          // Process image files
          const savings = await optimizeImage(fullPath);
          totalSaved += savings;
          totalProcessed++;
        }
      }
    } catch (error) {
      console.error(`Error processing directory ${directory}:`, error);
    }
  }
  
  // Check if a file is an image based on extension
  function isImage(filename) {
    const ext = path.extname(filename).toLowerCase();
    return ['.jpg', '.jpeg', '.png', '.gif'].includes(ext);
  }
  
  // Check if a file should be skipped
  function shouldSkip(filename) {
    return config.skipPatterns.some(pattern => pattern.test(filename));
  }
  
  // Format bytes to human-readable format
  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

// Optimize a single image
async function optimizeImage(filePath) {
  try {
    console.log(`Processing: ${path.basename(filePath)}`);
    
    // Get original file stats
    const originalStats = await fs.stat(filePath);
    const originalSize = originalStats.size;
    
    // Read image with Sharp
    const image = sharp(filePath);
    const metadata = await image.metadata();
    
    // Get file information
    const ext = path.extname(filePath).toLowerCase();
    const dir = path.dirname(filePath);
    const basename = path.basename(filePath, ext);
    
    // Process based on format
    let optimizedSize = 0;
    
    // Optimize the original format
    if (ext === '.jpg' || ext === '.jpeg') {
      await image
        .jpeg({ quality: config.quality.jpeg, progressive: true })
        .toFile(path.join(dir, `${basename}.min${ext}`));
    } else if (ext === '.png') {
      await image
        .png({ quality: config.quality.png, progressive: true })
        .toFile(path.join(dir, `${basename}.min${ext}`));
    } else if (ext === '.gif' && metadata.pages <= 1) {
      // Only process static GIFs, animated GIFs won't be processed
      await image
        .png({ quality: config.quality.png })
        .toFile(path.join(dir, `${basename}.min.png`));
    }
    
    // Create WebP version
    await image
      .webp({ quality: config.quality.webp })
      .toFile(path.join(dir, `${basename}.webp`));
    
    // Get optimized file stats
    const optimizedStats = await fs.stat(path.join(dir, `${basename}.min${ext}`));
    optimizedSize = optimizedStats.size;
    
    // Create responsive versions if image is large enough
    if (metadata.width > config.resizeThreshold) {
      for (const width of config.sizes.filter(size => size < metadata.width)) {
        const resizedImage = sharp(filePath)
          .resize({ width, withoutEnlargement: true })
          .jpeg({ quality: config.quality.jpeg, progressive: true });
        
        await resizedImage.toFile(path.join(dir, `${basename}-resized-${width}${ext}`));
        await resizedImage.webp({ quality: config.quality.webp }).toFile(path.join(dir, `${basename}-resized-${width}.webp`));
      }
    }
    
    // Calculate and return space savings
    const savings = originalSize - optimizedSize;
    const percent = ((savings / originalSize) * 100).toFixed(2);
    console.log(`  • Reduced by ${formatBytes(savings)} (${percent}%)`);
    
    return savings;
  } catch (error) {
    console.error(`Error optimizing ${filePath}:`, error);
    return 0;
  }
  
  // Format bytes to human-readable format
  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

// Execute the main function
optimizeImages().catch(console.error);