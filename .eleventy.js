const eleventyNavigationPlugin = require("@11ty/eleventy-navigation");
const { execSync } = require('child_process');
const path = require('path');

module.exports = function(eleventyConfig) {
  // Plugins
  eleventyConfig.addPlugin(eleventyNavigationPlugin);

  // Copy static files
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/CNAME");
  eleventyConfig.addPassthroughCopy({ "src/.nojekyll": ".nojekyll" });
  eleventyConfig.addPassthroughCopy("src/robots.txt");
  eleventyConfig.addPassthroughCopy("src/manifest.json");

  // Watch for changes
  eleventyConfig.addWatchTarget("src/assets/");

  // Layout aliases
  eleventyConfig.addLayoutAlias("base", "layouts/base.njk");
  eleventyConfig.addLayoutAlias("page", "layouts/page.njk");
  eleventyConfig.addLayoutAlias("post", "layouts/post.njk");
  eleventyConfig.addLayoutAlias("redirect", "redirect.njk");

  // Date filters
  eleventyConfig.addFilter("readableDate", dateObj => {
    return new Date(dateObj).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  });

  eleventyConfig.addFilter("htmlDateString", dateObj => {
    return new Date(dateObj).toISOString().split('T')[0];
  });

  // Limit filter
  eleventyConfig.addFilter("limit", (array, limit) => {
    return array.slice(0, limit);
  });

  // Reading time filter
  eleventyConfig.addFilter("readingTime", (content) => {
    if (!content) return 0;
    
    // Strip HTML tags and get plain text
    const plainText = content.replace(/<[^>]*>/g, '');
    
    // Count words (split by whitespace)
    const wordCount = plainText.split(/\s+/).filter(word => word.length > 0).length;
    
    // Average reading speed is 200-250 words per minute
    // Using 225 as a middle ground
    const wordsPerMinute = 225;
    const readingTime = Math.ceil(wordCount / wordsPerMinute);
    
    return readingTime;
  });

  // Get the newest date from a collection
  eleventyConfig.addFilter("getNewestCollectionItemDate", collection => {
    if (!collection || !collection.length) {
      return new Date();
    }
    return new Date(Math.max(...collection.map(item => item.date)));
  });

  // Convert URLs to absolute URLs for RSS
  eleventyConfig.addFilter("htmlToAbsoluteUrls", (htmlContent, base) => {
    if (!htmlContent) return '';
    
    // Simple regex to convert relative URLs to absolute
    return htmlContent
      .replace(/src="\/([^"]+)"/g, `src="${base}/$1"`)
      .replace(/href="\/([^"]+)"/g, `href="${base}/$1"`);
  });

  // Add rel="noopener noreferrer" to external links for security
  eleventyConfig.addFilter("externalLinks", (content) => {
    if (!content) return '';
    
    // Add rel attribute to external links
    return content.replace(
      /<a\s+href="https?:\/\/(?!williamzujkowski\.github\.io)[^"]+"/g,
      (match) => {
        // Check if rel attribute already exists
        if (match.includes('rel=')) {
          return match;
        }
        // Add rel attribute before the closing >
        return match + ' rel="noopener noreferrer"';
      }
    );
  });

  // Add lazy loading to images
  eleventyConfig.addFilter("lazyImages", (content) => {
    if (!content) return '';
    
    // Add loading="lazy" to img tags that don't already have a loading attribute
    return content.replace(
      /<img\s+(?![^>]*\sloading=)[^>]*>/gi,
      (match) => {
        // Skip if it's an SVG or data URI
        if (match.includes('data:') || match.includes('.svg')) {
          return match;
        }
        // Add loading="lazy" before the closing >
        return match.replace(/>$/, ' loading="lazy">');
      }
    );
  });

  // Get git last modified date for a file
  eleventyConfig.addFilter("gitLastModified", (inputPath) => {
    try {
      if (!inputPath) return null;
      
      // Remove the leading ./ and src/ if present
      let cleanPath = inputPath.replace(/^\.\//, '');
      if (cleanPath.startsWith('src/')) {
        cleanPath = cleanPath.substring(4);
      }
      
      // Construct the full file path
      const filePath = path.join(__dirname, 'src', cleanPath);
      
      // Get the last commit date for this file
      const gitCommand = `git log -1 --format=%cI -- "${filePath}"`;
      const result = execSync(gitCommand, { encoding: 'utf-8' }).trim();
      
      if (result) {
        return new Date(result);
      }
    } catch (error) {
      console.error(`Error getting git date for ${inputPath}:`, error.message);
    }
    
    return null;
  });

  // Create collection of all tags
  eleventyConfig.addCollection("tagList", function(collection) {
    let tagSet = new Set();
    collection.getAll().forEach(item => {
      (item.data.tags || []).forEach(tag => tagSet.add(tag));
    });
    // Convert to array and sort
    return [...tagSet].sort();
  });

  // Slugify filter for URLs
  eleventyConfig.addFilter("slugify", (str) => {
    if (!str) return "";
    return str.toString().toLowerCase()
      .replace(/\s+/g, '-')           // Replace spaces with -
      .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
      .replace(/\-\-+/g, '-')         // Replace multiple - with single -
      .replace(/^-+/, '')             // Trim - from start of text
      .replace(/-+$/, '');            // Trim - from end of text
  });

  // Override the built-in slug filter to properly handle apostrophes
  eleventyConfig.addFilter("slug", (str) => {
    if (!str) return "";
    return str.toString().toLowerCase()
      .replace(/['′'']/g, '')        // Remove apostrophes and smart quotes
      .replace(/\s+/g, '-')           // Replace spaces with -
      .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
      .replace(/\-\-+/g, '-')         // Replace multiple - with single -
      .replace(/^-+/, '')             // Trim - from start of text
      .replace(/-+$/, '');            // Trim - from end of text
  });

  // Truncate filter
  eleventyConfig.addFilter("truncate", (str, length = 100) => {
    if (!str) return "";
    if (str.length <= length) return str;
    return str.substring(0, length).trim() + "...";
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk"
  };
};