module.exports = function(eleventyConfig) {
  // Just a simple passthrough config for GitHub Actions
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy({ "assets/icons/favicon.ico": "favicon.ico" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/icon.svg": "icon.svg" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/apple-touch-icon.png": "apple-touch-icon.png" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/android-chrome-192x192.png": "android-chrome-192x192.png" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/android-chrome-512x512.png": "android-chrome-512x512.png" });
  eleventyConfig.addPassthroughCopy(".nojekyll");
  
  // Import required modules
  const pluginRss = require("@11ty/eleventy-plugin-rss");
  const pluginNavigation = require("@11ty/eleventy-navigation");
  const markdownIt = require("markdown-it");
  const markdownItAnchor = require("markdown-it-anchor");
  const { DateTime } = require("luxon");
  
  // Add plugins
  eleventyConfig.addPlugin(pluginRss);
  eleventyConfig.addPlugin(pluginNavigation);
  
  // Using default Eleventy date-based filtering (posts with dates in the future will not be displayed)
  
  // Add date filters
  eleventyConfig.addFilter("readableDate", dateObj => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toFormat("LLLL dd, yyyy");
  });
  
  eleventyConfig.addFilter("isoDate", dateObj => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toISO();
  });
  
  eleventyConfig.addFilter("date", (dateObj, format) => {
    if (typeof dateObj === 'string') {
      dateObj = new Date(dateObj);
    }
    return DateTime.fromJSDate(dateObj).toFormat(format || "LLLL dd, yyyy");
  });
  
  // Configure Markdown with anchors
  const markdownLibrary = markdownIt({
    html: true,
    breaks: true,
    linkify: true
  }).use(markdownItAnchor);
  
  eleventyConfig.setLibrary("md", markdownLibrary);
  
  // Add Eleventy 3.0+ compatible shortcodes
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);
  
  // HTML to Absolute URLs for RSS feeds
  eleventyConfig.addNunjucksAsyncFilter("htmlToAbsoluteUrls", function(html, base, callback) {
    if(!html) {
      callback(null, "");
      return;
    }
    
    try {
      const baseUrl = new URL(base);
      // Simple replacement for links and images
      let result = html.replace(/(href|src)="(?!http|mailto|#|\/\/)(.*?)"/g, `$1="${baseUrl.origin}/$2"`);
      callback(null, result);
    } catch(e) {
      console.error("Error converting HTML to absolute URLs:", e);
      callback(null, html);
    }
  });
  
  // Add breadcrumb shortcode
  eleventyConfig.addShortcode("breadcrumbs", function(page) {
    if (!page || !page.url) return "";
    
    const parts = page.url.split('/').filter(part => part);
    let breadcrumbs = '<nav aria-label="Breadcrumb" class="breadcrumbs"><div class="breadcrumbs-list">';
    
    // Add home
    breadcrumbs += '<span class="breadcrumbs-item"><a href="/" class="breadcrumbs-link">Home</a></span>';
    
    // Build the breadcrumb path
    let path = "";
    parts.forEach((part, i) => {
      path += `/${part}`;
      
      // Add separator
      breadcrumbs += '<span class="breadcrumbs-separator">&gt;</span>';
      
      // Last item (current page)
      if (i === parts.length - 1) {
        const label = page.title || part.replace(/-/g, ' ');
        breadcrumbs += `<span class="breadcrumbs-item current">${label}</span>`;
      } else {
        // Get proper title if available
        const segment = part.replace(/-/g, ' ');
        const title = segment.charAt(0).toUpperCase() + segment.slice(1);
        
        breadcrumbs += `<span class="breadcrumbs-item">
          <a href="${path}/" class="breadcrumbs-link">${title}</a>
        </span>`;
      }
    });
    
    breadcrumbs += '</div></nav>';
    return breadcrumbs;
  });
  
  // Add image shortcode
  eleventyConfig.addShortcode("image", function(src, alt, sizes = "100vw") {
    if (!src) {
      throw new Error(`Missing image source`);
    }
    if (!alt) {
      throw new Error(`Missing alt text for image: ${src}`);
    }
    
    // Ensure correct path structure
    let imgSrc = src;
    // If it's a relative path that could be from a blog post
    if (!src.startsWith('/') && !src.startsWith('./') && !src.startsWith('../')) {
      imgSrc = `/assets/images/${src}`;
    }
    
    // Simple image tag for GitHub Actions build
    return `<img src="${imgSrc}" alt="${alt}" class="w-full h-auto object-cover" loading="lazy" decoding="async">`;
  });
  
  // Reading time estimation
  eleventyConfig.addFilter("readingTime", (content) => {
    if (!content) return "";
    
    const contentText = content.replace(/<[^>]*>/g, '');
    const wordCount = contentText.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200); // 200 words per minute
    
    return readingTime;
  });
  
  // Extract headings from content for TOC
  eleventyConfig.addFilter("extractHeadings", (content) => {
    if (!content) return [];
    
    const headings = [];
    const regex = /<h([2-3])[^>]*id="([^"]*)"[^>]*>(.*?)<\/h\1>/g;
    let match;
    
    while ((match = regex.exec(content)) !== null) {
      const level = match[1];
      const id = match[2];
      // Remove any HTML tags and get plain text
      const text = match[3].replace(/<[^>]*>/g, '');
      
      headings.push({
        level,
        id,
        text
      });
    }
    
    return headings;
  });
  
  // Get related posts based on tags
  eleventyConfig.addFilter("getRelatedPosts", (collection, currentPost, limit = 3) => {
    // Safety checks
    if (!collection || !currentPost) return [];
    if (!currentPost.data || !currentPost.data.tags) return [];
    
    const currentTags = Array.isArray(currentPost.data.tags) 
      ? currentPost.data.tags.filter(tag => tag !== 'posts') 
      : [];
      
    // If no meaningful tags, return empty array
    if (currentTags.length === 0) return [];
    
    // Create an array of posts that share tags with the current post
    const relatedPosts = collection
      .filter(post => {
        // Safety checks
        if (!post || !post.data) return false;
        
        // Don't include the current post
        if (post.url === currentPost.url) return false;
        
        // Check if it has tags
        if (!post.data.tags || !Array.isArray(post.data.tags)) return false;
        
        // Check if any tags match (excluding the 'posts' tag)
        const postTags = post.data.tags.filter(tag => tag !== 'posts');
        
        return currentTags.some(tag => postTags.includes(tag));
      })
      .sort((a, b) => {
        // Count matching tags
        const aTags = a.data.tags.filter(tag => 
          tag !== 'posts' && currentTags.includes(tag)
        ).length;
        
        const bTags = b.data.tags.filter(tag => 
          tag !== 'posts' && currentTags.includes(tag)
        ).length;
        
        // Sort by number of matching tags (descending)
        return bTags - aTags;
      })
      .slice(0, limit);
    
    return relatedPosts;
  });
  
  // Site structure
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts"
    }
  };
};