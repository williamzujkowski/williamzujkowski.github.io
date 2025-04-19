/**
 * Unified Image Optimization Script
 *
 * This script provides a standardized way to optimize images for the website:
 * - Processes new images in assets/images directories
 * - Creates responsive image sizes
 * - Compresses images for better performance
 * - Updates image metadata
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import sharp from "sharp";
import { glob } from "glob";

// Directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..", "..");
const imageDir = path.join(rootDir, "assets", "images");
const outputDir = path.join(rootDir, "assets", "images", "optimized");
const metadataFile = path.join(rootDir, "assets", "data", "image-metadata.json");

// Image optimization settings
const sizes = [
  { width: 320, suffix: "xs" },
  { width: 640, suffix: "sm" },
  { width: 768, suffix: "md" },
  { width: 1024, suffix: "lg" },
  { width: 1280, suffix: "xl" },
  { width: 1536, suffix: "2xl" },
];

const imageFormats = [
  { format: "jpeg", options: { quality: 80 } },
  { format: "webp", options: { quality: 75 } },
];

// Metadata tracking
let imageMetadata = {};

/**
 * Initialize metadata tracking
 */
function initMetadata() {
  try {
    if (fs.existsSync(metadataFile)) {
      const data = fs.readFileSync(metadataFile, "utf8");
      imageMetadata = JSON.parse(data);
      console.log(`Loaded metadata for ${Object.keys(imageMetadata).length} images`);
    } else {
      console.log("No existing metadata file found, creating new one");
      imageMetadata = {};
    }
  } catch (error) {
    console.error("Error loading metadata:", error);
    imageMetadata = {};
  }
}

/**
 * Save metadata to file
 */
function saveMetadata() {
  try {
    // Ensure directory exists
    const dir = path.dirname(metadataFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(metadataFile, JSON.stringify(imageMetadata, null, 2));
    console.log(`Saved metadata for ${Object.keys(imageMetadata).length} images`);
  } catch (error) {
    console.error("Error saving metadata:", error);
  }
}

/**
 * Create optimized versions of an image
 */
async function optimizeImage(imagePath) {
  try {
    // Get relative path from image directory
    const relativePath = path.relative(imageDir, imagePath);
    console.log(`Processing: ${relativePath}`);

    // Check if file has been modified since last optimization
    const stats = fs.statSync(imagePath);
    const lastModified = stats.mtime.toISOString();

    if (
      imageMetadata[relativePath] &&
      imageMetadata[relativePath].lastModified === lastModified
    ) {
      console.log(`Image unchanged since last optimization: ${relativePath}`);
      return;
    }

    // Get image info
    const image = sharp(imagePath);
    const metadata = await image.metadata();

    // Skip if image is already optimized
    if (relativePath.includes("optimized/")) {
      console.log(`Skipping already optimized image: ${relativePath}`);
      return;
    }

    // Create base directory for output
    const outputPath = path.join(outputDir, path.dirname(relativePath));
    if (!fs.existsSync(outputPath)) {
      fs.mkdirSync(outputPath, { recursive: true });
    }

    // Generate different sizes and formats
    const outputs = [];
    for (const size of sizes) {
      // Skip sizes larger than original
      if (size.width > metadata.width) continue;

      const resizedImage = image.clone().resize(size.width);

      for (const format of imageFormats) {
        const outputFilename =
          path.basename(imagePath, path.extname(imagePath)) +
          `-${size.suffix}.${format.format}`;
        const outputFilePath = path.join(outputPath, outputFilename);

        await resizedImage
          .toFormat(format.format, format.options)
          .toFile(outputFilePath);

        outputs.push({
          size: size.width,
          format: format.format,
          path: path.join("optimized", path.dirname(relativePath), outputFilename),
        });
      }
    }

    // Update metadata
    imageMetadata[relativePath] = {
      original: {
        width: metadata.width,
        height: metadata.height,
        format: metadata.format,
        size: stats.size,
      },
      lastModified,
      outputs,
    };

    console.log(`Optimized: ${relativePath} (${outputs.length} versions created)`);
  } catch (error) {
    console.error(`Error optimizing ${imagePath}:`, error);
  }
}

/**
 * Process all images in a directory
 */
async function processDirectory(dir) {
  try {
    console.log(`Processing directory: ${dir}`);

    // Get all image files
    const imageFiles = await glob("**/*.{jpg,jpeg,png,gif}", {
      cwd: dir,
      absolute: true,
      ignore: ["**/optimized/**", "**/node_modules/**"],
    });

    console.log(`Found ${imageFiles.length} images to process`);

    // Process each image
    for (const imagePath of imageFiles) {
      await optimizeImage(imagePath);
    }

    console.log(`Finished processing directory: ${dir}`);
  } catch (error) {
    console.error(`Error processing directory ${dir}:`, error);
  }
}

/**
 * Generate HTML for responsive images
 */
function generateResponsiveImageHTML(imagePath, alt, sizes = "100vw") {
  try {
    // Get relative path from image directory
    const relativePath = path.relative(imageDir, imagePath).replace(/\\/g, "/");

    // Check if we have metadata for this image
    if (!imageMetadata[relativePath]) {
      console.warn(`No metadata found for: ${relativePath}`);
      return `<img src="${imagePath}" alt="${alt}" loading="lazy" decoding="async">`;
    }

    // Get the outputs
    const outputs = imageMetadata[relativePath].outputs;

    // Group by format
    const byFormat = {};
    for (const output of outputs) {
      if (!byFormat[output.format]) {
        byFormat[output.format] = [];
      }
      byFormat[output.format].push(output);
    }

    // Get webp srcset if available
    let webpSrcset = "";
    if (byFormat.webp) {
      webpSrcset = byFormat.webp
        .sort((a, b) => a.size - b.size)
        .map((output) => `/assets/images/${output.path} ${output.size}w`)
        .join(", ");
    }

    // Get fallback format srcset (jpeg/png)
    const fallbackFormat = byFormat.jpeg ? "jpeg" : Object.keys(byFormat)[0];
    let fallbackSrcset = "";
    let fallbackSrc = "";

    if (byFormat[fallbackFormat]) {
      fallbackSrcset = byFormat[fallbackFormat]
        .sort((a, b) => a.size - b.size)
        .map((output) => `/assets/images/${output.path} ${output.size}w`)
        .join(", ");

      // Use smallest size as fallback src
      fallbackSrc = `/assets/images/${
        byFormat[fallbackFormat].sort((a, b) => a.size - b.size)[0].path
      }`;
    } else {
      // Use original as fallback
      fallbackSrc = `/assets/images/${relativePath}`;
    }

    // Build HTML
    let html = "<picture>\n";

    // Add webp source if available
    if (webpSrcset) {
      html += `  <source type="image/webp" srcset="${webpSrcset}" sizes="${sizes}">\n`;
    }

    // Add fallback source if available and different from webp
    if (fallbackSrcset && fallbackFormat !== "webp") {
      html += `  <source type="image/${fallbackFormat}" srcset="${fallbackSrcset}" sizes="${sizes}">\n`;
    }

    // Add img tag
    html += `  <img src="${fallbackSrc}" alt="${alt}" loading="lazy" decoding="async" width="${imageMetadata[relativePath].original.width}" height="${imageMetadata[relativePath].original.height}">\n`;
    html += "</picture>";

    return html;
  } catch (error) {
    console.error(`Error generating HTML for ${imagePath}:`, error);
    return `<img src="${imagePath}" alt="${alt}" loading="lazy" decoding="async">`;
  }
}

/**
 * Main function
 */
async function main() {
  try {
    console.log("Starting image optimization process...");

    // Initialize metadata
    initMetadata();

    // Process blog images
    await processDirectory(path.join(imageDir, "blog"));

    // Process other directories
    // await processDirectory(path.join(imageDir, 'other'));

    // Save metadata
    saveMetadata();

    console.log("Image optimization process complete");
  } catch (error) {
    console.error("Error during image optimization:", error);
  }
}

// Run the script if called directly
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
} else {
  // Export functions for use in other scripts
  export {
    optimizeImage,
    processDirectory,
    generateResponsiveImageHTML,
    initMetadata,
    saveMetadata,
  };
}
