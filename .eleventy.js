module.exports = function(eleventyConfig) {
  // Copy assets directory to the output
  eleventyConfig.addPassthroughCopy("src/assets");
  
  // Set custom directories for input, output, includes, and data
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    // Set default template engine to Nunjucks
    templateFormats: ["njk", "md", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk"
  };
};
