module.exports = function(eleventyConfig) {
    // Create collections for blog posts, projects, and fun links
    eleventyConfig.addCollection("blog", function(collectionApi) {
        return collectionApi.getFilteredByGlob("src/blog/*.md");
    });
    
    eleventyConfig.addCollection("projects", function(collectionApi) {
        return collectionApi.getFilteredByGlob("src/projects/*.md");
    });
    
    eleventyConfig.addCollection("funLinks", function(collectionApi) {
        return collectionApi.getFilteredByGlob("src/fun-links/*.md");
    });

    // Set up BrowserSync to refresh on CSS changes
    eleventyConfig.setBrowserSyncConfig({
        files: './public/static/**/*.css',
    });

    // Add passthrough copy for static files
    eleventyConfig.addPassthroughCopy("src/images");
    
    // Return configuration object
    return {
        dir: {
            input: "src",
            output: "public",
            includes: "../_includes"  // Looking one directory up from src
        }
    };
};