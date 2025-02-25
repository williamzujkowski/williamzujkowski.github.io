const yaml = require("js-yaml");
const { DateTime } = require("luxon");

module.exports = function(eleventyConfig) {
  // Add support for YAML data files
  eleventyConfig.addDataExtension("yml", contents => yaml.load(contents));
  
  // Copy assets directory to the output
  eleventyConfig.addPassthroughCopy("src/assets");
  
  // Date formatting filter
  eleventyConfig.addFilter("formatDate", (dateObj, format = "LLL d, yyyy") => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toFormat(format);
  });
  
  // Current year shortcode
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);
  
  // Limit filter for collections
  eleventyConfig.addFilter("limit", (array, limit) => {
    return array.slice(0, limit);
  });
  
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
