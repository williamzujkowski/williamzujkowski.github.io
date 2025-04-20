// Patched 11ty config for debugging
const fs = require("fs");
const path = require("path");
const config = require("./.eleventy.cjs");

module.exports = function (eleventyConfig) {
  // Run the original config
  config(eleventyConfig);

  // Add a custom transformer for feed.njk to fix the author tag
  eleventyConfig.addTransform("fixFeedAuthorTag", function (content, outputPath) {
    if (outputPath && outputPath.endsWith("/feed.xml")) {
      console.log("Patching feed.xml author tag...");
      return content.replace(/<n>([^<]+)<\/n>/g, "<name>$1</name>");
    }
    return content;
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts",
    },
  };
};
