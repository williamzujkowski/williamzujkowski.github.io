module.exports = function(eleventyConfig) {
  // Copy assets
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy({ "src/js": "js" });
  eleventyConfig.addPassthroughCopy({ "src/css/*.!(css)": "css" });
  eleventyConfig.addPassthroughCopy("site.webmanifest");
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("icon.svg");
  eleventyConfig.addPassthroughCopy("apple-touch-icon.png");
  
  // Layout aliases
  eleventyConfig.addLayoutAlias('base', '_layouts/base.njk');
  eleventyConfig.addLayoutAlias('base.njk', '_layouts/base.njk');
  eleventyConfig.addLayoutAlias('post', '_layouts/post.njk');
  eleventyConfig.addLayoutAlias('post.njk', '_layouts/post.njk');

  // Debug filter
  eleventyConfig.addFilter('log', function(value) {
    console.log('DEBUG:', value);
    return value;
  });

  return {
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk",
    dir: {
      input: ".",
      includes: "_includes",
      layouts: "_layouts",
      data: "_data",
      output: "_site"
    }
  };
};