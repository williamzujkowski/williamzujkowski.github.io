const { DateTime } = require("luxon");
const navigationPlugin = require("@11ty/eleventy-navigation");
const rssPlugin = require("@11ty/eleventy-plugin-rss");
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const markdownIt = require("markdown-it");
const markdownItAnchor = require("markdown-it-anchor");

module.exports = function(eleventyConfig) {
  // Add plugins
  eleventyConfig.addPlugin(navigationPlugin);
  eleventyConfig.addPlugin(rssPlugin);
  eleventyConfig.addPlugin(syntaxHighlight);

  // Copy static assets to the output folder
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/robots.txt");

  // Add custom date formats
  eleventyConfig.addFilter("readableDate", dateObj => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toFormat("LLLL dd, yyyy");
  });

  eleventyConfig.addFilter("htmlDateString", dateObj => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toFormat("yyyy-LL-dd");
  });

  // Format ISO date strings to readable format
  eleventyConfig.addFilter("formatDate", (dateString) => {
    return DateTime.fromISO(dateString).toFormat("LLLL dd, yyyy");
  });

  // Get the first `n` elements of a collection
  eleventyConfig.addFilter("head", (array, n) => {
    if(!Array.isArray(array) || array.length === 0) {
      return [];
    }
    if(n < 0) {
      return array.slice(n);
    }
    return array.slice(0, n);
  });

  // Return the newest date in a collection
  eleventyConfig.addFilter("latestCollectionDate", (collection) => {
    if(!Array.isArray(collection) || collection.length === 0) {
      return null;
    }
    
    return new Date(Math.max(...collection.map(item => item.date.getTime())));
  });

  // Get the latest post
  eleventyConfig.addFilter("getLatestPost", (collection) => {
    if(!Array.isArray(collection) || collection.length === 0) {
      return null;
    }
    
    return collection.sort((a, b) => b.date - a.date)[0];
  });

  // Custom Markdown configuration with anchor links
  let markdownLibrary = markdownIt({
    html: true,
    breaks: true,
    linkify: true
  }).use(markdownItAnchor, {
    permalink: markdownItAnchor.permalink.ariaHidden({
      placement: "after",
      class: "anchor-link",
      symbol: "#",
      level: [1, 2, 3, 4]
    }),
    slugify: eleventyConfig.getFilter("slugify")
  });

  eleventyConfig.setLibrary("md", markdownLibrary);

  // Error handling for collections
  eleventyConfig.addCollection("posts", function(collectionApi) {
    try {
      return collectionApi.getFilteredByGlob("src/posts/*.md")
        .sort((a, b) => b.date - a.date);
    } catch (error) {
      console.error("Error creating posts collection:", error);
      return [];
    }
  });

  eleventyConfig.addCollection("projects", function(collectionApi) {
    try {
      return collectionApi.getFilteredByGlob("src/projects/*.md")
        .sort((a, b) => b.date - a.date);
    } catch (error) {
      console.error("Error creating projects collection:", error);
      return [];
    }
  });

  // Return all configuration options
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk",
    passthroughFileCopy: true
  };
};