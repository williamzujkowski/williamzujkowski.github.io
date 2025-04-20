// Simplified and consolidated Eleventy configuration

// Import plugins
const rssPlugin = require("@11ty/eleventy-plugin-rss");
const navigationPlugin = require("@11ty/eleventy-navigation");
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const Image = require("@11ty/eleventy-img");
const markdownIt = require("markdown-it");
const markdownItAnchor = require("markdown-it-anchor");
const path = require("path");
const fs = require("fs");

// Copy all functions and plugins from the original config file
module.exports = function (eleventyConfig) {
  // Load the original config
  const originalConfig = require("./.eleventy.cjs");
  originalConfig(eleventyConfig);

  // Add a transform to fix the RSS feed author tag format
  eleventyConfig.addTransform("fixRssFeed", function (content, outputPath) {
    if (outputPath && outputPath.endsWith("/feed.xml")) {
      console.log("Fixing RSS feed author tag format...");
      return content.replace(/<n>([^<]+)<\/n>/g, "<name>$1</name>");
    }
    return content;
  });
};
