const eleventyImg = require("@11ty/eleventy-img");

module.exports = function (eleventyConfig) {
    eleventyConfig.addPlugin(eleventyImg);

    // Create collections for blog posts, projects, and fun links
    eleventyConfig.addCollection("blog", function (collectionApi) {
        return collectionApi.getFilteredByGlob("blog/*.md");
    });

    eleventyConfig.addCollection("projects", function (collectionApi) {
        return collectionApi.getFilteredByGlob("projects/*.md");
    });

    eleventyConfig.addCollection("funLinks", function (collectionApi) {
        return collectionApi.getFilteredByGlob("fun-links/*.md");
    });

    // Add other configurations here
    return {
        dir: {
            input: ".",  // Change from "src" to "." as files are in root
            output: "public"
        }
    };
};