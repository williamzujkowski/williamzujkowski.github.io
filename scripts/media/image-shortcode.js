/**
 * Enhanced Image Shortcode Utility
 *
 * This script provides a helper for generating HTML for optimized images
 * using the data from the image optimization process.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..", "..");
const imageDir = path.join(rootDir, "assets", "images");
const metadataFile = path.join(rootDir, "assets", "data", "image-metadata.json");

// Load image metadata
let imageMetadata = {};
try {
  if (fs.existsSync(metadataFile)) {
    imageMetadata = JSON.parse(fs.readFileSync(metadataFile, "utf8"));
  }
} catch (error) {
  console.error("Error loading image metadata:", error);
}

/**
 * Generate HTML for responsive images
 *
 * @param {string} src - Image source path (relative to assets/images)
 * @param {string} alt - Alt text for the image
 * @param {string} sizes - Sizes attribute for responsive images (e.g., "100vw" or "(min-width: 1024px) 50vw, 100vw")
 * @param {Object} options - Additional options
 * @returns {string} HTML for the responsive image
 */
function responsiveImage(src, alt, sizes = "100vw", options = {}) {
  try {
    // Ensure src is properly formatted (remove leading slash if present)
    src = src.startsWith("/") ? src.substring(1) : src;

    // If src doesn't include assets/images, add it
    if (!src.includes("assets/images/")) {
      src = `assets/images/${src}`;
    }

    // Get relative path from assets/images
    const relativePath = src.replace("assets/images/", "");

    // Check if we have metadata for this image
    if (!imageMetadata[relativePath]) {
      console.warn(`No metadata found for: ${relativePath}`);
      return `<img src="/${src}" alt="${alt}" class="${options.class || ""}" loading="lazy" decoding="async">`;
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
      fallbackSrc = `/${src}`;
    }

    // Width and height for aspect ratio
    const width = imageMetadata[relativePath].original.width;
    const height = imageMetadata[relativePath].original.height;

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

    // Additional classes
    const classList = ["responsive-image"];
    if (options.class) {
      classList.push(options.class);
    }

    // Add img tag with fallback
    html += `  <img 
    src="${fallbackSrc}" 
    alt="${alt}" 
    class="${classList.join(" ")}" 
    loading="${options.loading || "lazy"}" 
    decoding="${options.decoding || "async"}" 
    width="${width}" 
    height="${height}"`;

    // Add additional attributes
    if (options.id) html += ` id="${options.id}"`;
    if (options.style) html += ` style="${options.style}"`;

    html += ">\n";
    html += "</picture>";

    return html;
  } catch (error) {
    console.error(`Error generating HTML for ${src}:`, error);
    return `<img src="/${src}" alt="${alt}" class="${options.class || ""}" loading="lazy" decoding="async">`;
  }
}

// Export the function
export { responsiveImage };
