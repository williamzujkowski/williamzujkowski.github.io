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

  // Watch for changes
  eleventyConfig.addWatchTarget("src/assets/");

  // Layout aliases
  eleventyConfig.addLayoutAlias("base", "layouts/base.njk");
  eleventyConfig.addLayoutAlias("page", "layouts/page.njk");
  eleventyConfig.addLayoutAlias("post", "layouts/post.njk");

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