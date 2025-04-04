import syntaxHighlight from "@11ty/eleventy-plugin-syntaxhighlight";
import eleventyNavigationPlugin from "@11ty/eleventy-navigation";
import pluginRss from "@11ty/eleventy-plugin-rss";
import { DateTime } from "luxon";
import markdownIt from "markdown-it";
import markdownItAnchor from "markdown-it-anchor";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default function(eleventyConfig) {
  // Plugins
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(eleventyNavigationPlugin);
  eleventyConfig.addPlugin(pluginRss);
  
  // Copy files
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy({ "src/js": "js" });
  eleventyConfig.addPassthroughCopy({ "src/css/*.!(css)": "css" });
  eleventyConfig.addPassthroughCopy(".nojekyll");
  eleventyConfig.addPassthroughCopy("site.webmanifest");
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("icon.svg");
  eleventyConfig.addPassthroughCopy("apple-touch-icon.png");
  
  // Date formatting
  eleventyConfig.addFilter("readableDate", dateObj => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toFormat("LLLL dd, yyyy");
  });

  // Date for sitemap
  eleventyConfig.addFilter("isoDate", dateObj => {
    return DateTime.fromJSDate(dateObj, {zone: 'utc'}).toISO();
  });
  
  // Generic date formatter
  eleventyConfig.addFilter("date", (dateObj, format) => {
    return DateTime.fromISO(dateObj).toFormat(format);
  });

  // Add a shortcode for current year
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);

  // Markdown configuration
  const markdownLibrary = markdownIt({
    html: true,
    breaks: true,
    linkify: true
  }).use(markdownItAnchor);
  
  eleventyConfig.setLibrary("md", markdownLibrary);
  
  // Load site configuration as global data
  eleventyConfig.addGlobalData("site", () => {
    const configPath = path.join(__dirname, 'src', '_data', 'site.json');
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  });
  
  // Load ArXiv feed data if available
  eleventyConfig.addGlobalData("arxiv_feed", () => {
    try {
      const feedPath = path.join(__dirname, '_data', 'arxiv-feed.json');
      if (fs.existsSync(feedPath)) {
        return JSON.parse(fs.readFileSync(feedPath, 'utf8'));
      }
      console.warn("ArXiv feed data not found. Run build-arxiv-feed.js to generate it.");
      return null;
    } catch (e) {
      console.warn("Error loading ArXiv feed:", e);
      return null;
    }
  });
  
  // Load GitHub pinned repositories if available
  eleventyConfig.addGlobalData("github_pins", () => {
    try {
      const pinsPath = path.join(__dirname, '_data', 'github-pins.json');
      if (fs.existsSync(pinsPath)) {
        return JSON.parse(fs.readFileSync(pinsPath, 'utf8'));
      }
      console.warn("GitHub pins data not found. Run build-github-pins.js to generate it.");
      return null;
    } catch (e) {
      console.warn("Error loading GitHub pins:", e);
      return null;
    }
  });

  // Create collection for all posts
  eleventyConfig.addCollection("posts", function(collectionApi) {
    return collectionApi.getFilteredByTag("posts");
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