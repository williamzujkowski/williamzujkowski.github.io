const eleventyImg = require("@11ty/eleventy-img");

module.exports = function(eleventyConfig) {
    eleventyConfig.addPlugin(eleventyImg);

    // Add other configurations here
    return {
        dir: {
            input: "src",
            output: "public"
        }
    };
};
