module.exports = function(eleventyConfig) {
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

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_includes"
    }
  };
};