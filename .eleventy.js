const yaml = require("js-yaml");
const { DateTime } = require("luxon");
const pluginRss = require("@11ty/eleventy-plugin-rss");

module.exports = function(eleventyConfig) {
  // Add plugins
  eleventyConfig.addPlugin(pluginRss);
  
  // Add support for YAML data files
  eleventyConfig.addDataExtension("yml", contents => yaml.load(contents));
  
  // Copy assets directory to the output
  eleventyConfig.addPassthroughCopy("src/assets");
  
  // Date formatting filter
  eleventyConfig.addFilter("formatDate", (dateObj, format = "LLL d, yyyy") => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toFormat(format);
  });
  
  // ISO date filter for RSS
  eleventyConfig.addFilter("dateToRfc3339", (dateObj) => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toISO();
  });
  
  // HTML date filter
  eleventyConfig.addFilter("dateToISO", (dateObj) => {
    return DateTime.fromJSDate(dateObj).toISODate();
  });
  
  // Current year shortcode
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);
  
  // Limit filter for collections
  eleventyConfig.addFilter("limit", (array, limit) => {
    return array.slice(0, limit);
  });
  
  // Get all unique tags from a collection
  eleventyConfig.addFilter("getAllTags", collection => {
    let tagSet = new Set();
    for (let item of collection) {
      (item.data.tags || []).forEach(tag => tagSet.add(tag));
    }
    return Array.from(tagSet).sort();
  });
  
  // Filter out specific tags
  eleventyConfig.addFilter("filterTagList", tags => {
    return (tags || []).filter(tag => ["posts", "all"].indexOf(tag) === -1);
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
