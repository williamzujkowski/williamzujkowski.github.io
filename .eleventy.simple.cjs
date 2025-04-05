// Import the RSS plugin
const pluginRss = require("@11ty/eleventy-plugin-rss");

module.exports = function(eleventyConfig) {
  // Add RSS plugin
  eleventyConfig.addPlugin(pluginRss);
  // Copy assets
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("site.webmanifest");
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("icon.svg");
  eleventyConfig.addPassthroughCopy("apple-touch-icon.png");
  eleventyConfig.addPassthroughCopy("android-chrome-192x192.png");
  eleventyConfig.addPassthroughCopy("android-chrome-512x512.png");
  eleventyConfig.addPassthroughCopy(".nojekyll");
  
  // Debug filter
  eleventyConfig.addFilter('log', function(value) {
    console.log('DEBUG:', value);
    return value;
  });
  
  // Date filters
  eleventyConfig.addFilter("isoDate", function(date) {
    return new Date(date).toISOString();
  });
  
  eleventyConfig.addFilter("readableDate", function(date) {
    const d = new Date(date);
    return d.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  });
  
  // Text manipulation filters
  eleventyConfig.addFilter("striptags", function(value) {
    // Simple HTML tag stripper
    return value.replace(/<[^>]*>/g, '');
  });
  
  // JSON filter
  eleventyConfig.addFilter("json", function(value) {
    return JSON.stringify(value);
  });
  
  // RSS filters from the plugin
  eleventyConfig.addFilter("dateToRfc3339", pluginRss.dateToRfc3339);
  eleventyConfig.addFilter("dateToRfc822", pluginRss.dateToRfc822);
  eleventyConfig.addFilter("htmlToAbsoluteUrls", pluginRss.htmlToAbsoluteUrls);
  
  // Add shortcode for current year
  eleventyConfig.addShortcode("year", () => new Date().getFullYear());
  
  // Add collection utilities
  eleventyConfig.addFilter("getNewestCollectionItemDate", (collection) => {
    if( !collection || !collection.length ) {
      return new Date();
    }
    
    return new Date(Math.max(...collection.map(item => {
      return item.date ? item.date.getTime() : 0;
    })));
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "../_includes",
      layouts: "../_layouts"
    }
  };
};