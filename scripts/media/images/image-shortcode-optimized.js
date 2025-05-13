/**
 * Enhanced responsive image shortcode with performance optimizations
 *
 * Features:
 * - Native lazy loading with fallback
 * - Automatic WebP generation
 * - AVIF support
 * - Fetch priority signals
 * - CSS aspect ratio
 * - Blur-up loading effect
 * - Content-visibility optimization
 */

import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import Image from "@11ty/eleventy-img";

// Directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..", "..");

// Base output location for processed images
const IMAGE_OUTPUT_DIR = path.join(rootDir, "_site", "img");

// Low-quality image placeholder settings
const LQIP_OPTIONS = {
  width: 24,
  quality: 20,
  formats: ["webp"],
};

/**
 * Process an image with Eleventy Image
 *
 * @param {string} src - The image path
 * @param {Object} options - Image processing options
 * @returns {Promise<Object>} - Metadata about the processed image
 */
async function processImage(src, options = {}) {
  // Default options
  const defaultOptions = {
    widths: [300, 600, 900, 1200, 1600],
    formats: ["avif", "webp", "jpeg"],
    outputDir: IMAGE_OUTPUT_DIR,
    urlPath: "/img/",
    sharpWebpOptions: {
      quality: 80,
      lossless: false,
    },
    sharpAvifOptions: {
      quality: 65,
      effort: 7,
    },
    filenameFormat: (id, src, width, format) => {
      const extension = path.extname(src);
      const name = path.basename(src, extension);
      return `${name}-${width}w.${format}`;
    },
  };

  // Merge options
  const imageOptions = { ...defaultOptions, ...options };

  // Generate images
  return await Image(src, imageOptions);
}

/**
 * Generate a low-quality image placeholder (LQIP)
 *
 * @param {string} src - The image path
 * @returns {Promise<string>} - Base64 encoded placeholder image
 */
async function generateLQIP(src) {
  try {
    // Process the image at low quality
    const metadata = await Image(src, LQIP_OPTIONS);

    // Get the WebP version
    const webp = metadata.webp[0];

    // Read the file and convert to base64
    const buffer = fs.readFileSync(webp.outputPath);
    const base64 = buffer.toString("base64");

    return `data:image/webp;base64,${base64}`;
  } catch (error) {
    console.error(`Error generating LQIP for ${src}:`, error);
    return null;
  }
}

/**
 * Enhanced image shortcode for templates
 *
 * @param {Object} eleventyConfig - Eleventy configuration
 */
function configureImageShortcode(eleventyConfig) {
  eleventyConfig.addShortcode("respimg", async function (src, alt, options = {}) {
    // Default options
    const defaultOptions = {
      widths: [300, 600, 900, 1200, 1600],
      sizes: "(min-width: 1024px) 1024px, 100vw",
      loading: "lazy",
      decoding: "async",
      fetchpriority: "auto",
      class: "",
      style: "",
      useLQIP: true,
    };

    // Merge options
    const imgOptions = { ...defaultOptions, ...options };

    // Configure loading and priority
    const isEager = imgOptions.loading === "eager";
    const isPriority = imgOptions.fetchpriority === "high" || isEager;

    // Generate main image
    let metadata;
    try {
      metadata = await processImage(src, {
        widths: imgOptions.widths,
        formats: ["avif", "webp", "jpeg"],
      });
    } catch (error) {
      console.error(`Error processing image ${src}:`, error);
      return `<img src="${src}" alt="${alt}" class="${imgOptions.class}" style="${imgOptions.style}">`;
    }

    // Generate LQIP if needed
    let lqip = null;
    if (imgOptions.useLQIP) {
      lqip = await generateLQIP(src);
    }

    // Get image dimensions from metadata
    const imageWidth = metadata.jpeg[metadata.jpeg.length - 1].width;
    const imageHeight = metadata.jpeg[metadata.jpeg.length - 1].height;
    const aspectRatio = (imageHeight / imageWidth) * 100;

    // Build the necessary attributes
    const attributes = {
      alt,
      loading: imgOptions.loading,
      decoding: imgOptions.decoding,
      width: imageWidth,
      height: imageHeight,
      sizes: imgOptions.sizes,
      class: imgOptions.class,
      style: `${imgOptions.style}${lqip ? ` background-size: cover; background-image: url('${lqip}');` : ""}`,
    };

    // Add fetchpriority if supported and explicitly set
    if (imgOptions.fetchpriority !== "auto") {
      attributes.fetchpriority = imgOptions.fetchpriority;
    }

    // Format attributes as HTML string
    const attributesString = Object.entries(attributes)
      .filter(([_, value]) => value !== "")
      .map(([key, value]) => `${key}="${value}"`)
      .join(" ");

    // Build picture element
    let picture = `<picture class="responsive-picture" style="display: block; aspect-ratio: ${imageWidth}/${imageHeight};">`;

    // Add AVIF source if available
    if (metadata.avif) {
      const avifSrcset = metadata.avif
        .map((img) => `${img.url} ${img.width}w`)
        .join(", ");
      picture += `\n  <source type="image/avif" srcset="${avifSrcset}" sizes="${imgOptions.sizes}">`;
    }

    // Add WebP source
    if (metadata.webp) {
      const webpSrcset = metadata.webp
        .map((img) => `${img.url} ${img.width}w`)
        .join(", ");
      picture += `\n  <source type="image/webp" srcset="${webpSrcset}" sizes="${imgOptions.sizes}">`;
    }

    // Add JPEG fallback
    const jpegSrcset = metadata.jpeg
      .map((img) => `${img.url} ${img.width}w`)
      .join(", ");
    picture += `\n  <source type="image/jpeg" srcset="${jpegSrcset}" sizes="${imgOptions.sizes}">`;

    // Add img tag with the smallest JPEG as fallback
    const fallback = metadata.jpeg[0];
    picture += `\n  <img src="${fallback.url}" ${attributesString}>`;
    picture += "\n</picture>";

    // Add content-visibility optimization for non-priority images that are lazy-loaded
    if (!isPriority && imgOptions.loading === "lazy") {
      return `<div style="content-visibility: auto; contain-intrinsic-size: ${imageWidth}px ${imageHeight}px;">${picture}</div>`;
    }

    return picture;
  });
}

export default configureImageShortcode;
