// Simplified and consolidated Eleventy configuration

// Import plugins
const navigationPlugin = require("@11ty/eleventy-navigation");
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const pluginRss = require("@11ty/eleventy-plugin-rss");
const Image = require("@11ty/eleventy-img");
const markdownIt = require("markdown-it");
const markdownItAnchor = require("markdown-it-anchor");
const path = require("path");
const fs = require("fs");

// Image shortcode function
async function imageShortcode(
  src,
  alt,
  sizes = "100vw",
  widths = [300, 600, 900, 1200],
  formats = ["webp", "jpeg"]
) {
  if (!src) {
    throw new Error(`Missing image source`);
  }
  if (!alt) {
    throw new Error(`Missing alt text for image: ${src}`);
  }

  // Try to use enhanced image shortcode if metadata exists
  try {
    const metadataFile = path.join(__dirname, "assets", "data", "image-metadata.json");

    if (fs.existsSync(metadataFile)) {
      const imageMetadata = JSON.parse(fs.readFileSync(metadataFile, "utf8"));

      // Normalize src path
      let normalizedSrc = src;
      if (!src.startsWith("/") && !src.startsWith("./") && !src.startsWith("../")) {
        normalizedSrc = `assets/images/${src}`;
      } else if (src.startsWith("/")) {
        normalizedSrc = src.substring(1);
      }

      // Get relative path from assets/images
      const relativePath = normalizedSrc.replace(/^assets\/images\//, "");

      // Check if we have metadata for this image
      if (imageMetadata[relativePath]) {
        const outputs = imageMetadata[relativePath].outputs;

        // Group by format
        const byFormat = {};
        for (const output of outputs) {
          if (!byFormat[output.format]) {
            byFormat[output.format] = [];
          }
          byFormat[output.format].push(output);
        }

        // Get webp srcset if available
        let webpSrcset = "";
        if (byFormat.webp) {
          webpSrcset = byFormat.webp
            .sort((a, b) => a.size - b.size)
            .map((output) => `/assets/images/${output.path} ${output.size}w`)
            .join(", ");
        }

        // Get fallback format srcset (jpeg/png)
        const fallbackFormat = byFormat.jpeg ? "jpeg" : Object.keys(byFormat)[0];
        let fallbackSrcset = "";
        let fallbackSrc = "";

        if (byFormat[fallbackFormat]) {
          fallbackSrcset = byFormat[fallbackFormat]
            .sort((a, b) => a.size - b.size)
            .map((output) => `/assets/images/${output.path} ${output.size}w`)
            .join(", ");

          // Use smallest size as fallback src
          fallbackSrc = `/assets/images/${
            byFormat[fallbackFormat].sort((a, b) => a.size - b.size)[0].path
          }`;
        } else {
          // Use original as fallback
          fallbackSrc = normalizedSrc.startsWith("/")
            ? normalizedSrc
            : `/${normalizedSrc}`;
        }

        // Width and height for aspect ratio
        const width = imageMetadata[relativePath].original.width;
        const height = imageMetadata[relativePath].original.height;

        // Build HTML
        let html = "<picture>\n";

        // Add webp source if available
        if (webpSrcset) {
          html += `  <source type="image/webp" srcset="${webpSrcset}" sizes="${sizes}">\n`;
        }

        // Add fallback source if available and different from webp
        if (fallbackSrcset && fallbackFormat !== "webp") {
          html += `  <source type="image/${fallbackFormat}" srcset="${fallbackSrcset}" sizes="${sizes}">\n`;
        }

        // Add img tag with fallback
        html += `  <img src="${fallbackSrc}" alt="${alt}" class="w-full h-auto object-cover" loading="lazy" decoding="async" width="${width}" height="${height}">\n`;
        html += "</picture>";

        return html;
      }
    }
  } catch (error) {
    console.warn("Error using enhanced image shortcode:", error.message);
  }

  // Fallback to simple image tag
  // Ensure correct path structure
  let imgSrc = src;
  // If it's a relative path that could be from a blog post
  if (!src.startsWith("/") && !src.startsWith("./") && !src.startsWith("../")) {
    imgSrc = `/assets/images/${src}`;
  }
  return `<img src="${imgSrc}" alt="${alt}" class="w-full h-auto object-cover" loading="lazy" decoding="async">`;
}

module.exports = function (eleventyConfig) {
  // Add filters to separate vulnerability posts from regular posts
  eleventyConfig.addFilter("filterVulnerabilityPosts", function (posts) {
    if (!posts) return [];
    return posts.filter(
      (post) => post.fileSlug && post.fileSlug.includes("vulnerability-analysis")
    );
  });

  eleventyConfig.addFilter("filterOutVulnerabilityPosts", function (posts) {
    if (!posts) return [];
    return posts.filter(
      (post) => !post.fileSlug || !post.fileSlug.includes("vulnerability-analysis")
    );
  });

  // Add a custom collection for posts that explicitly filters out future-dated posts
  eleventyConfig.addCollection("posts", function (collectionApi) {
    const now = new Date();
    now.setHours(0, 0, 0, 0); // Set to beginning of day for consistent comparison
    console.log(`Current date for filtering: ${now.toISOString()}`);

    // Get all posts and filter out future posts
    const filteredPosts = collectionApi
      .getFilteredByGlob("./src/posts/*.md")
      .filter((item) => {
        // Get post date and normalize to beginning of day
        const postDate = new Date(item.date);
        postDate.setHours(0, 0, 0, 0);

        // Debug output
        console.log(
          `Post: ${item.data.title}, Date: ${postDate.toISOString()}, Include: ${postDate <= now}`
        );

        // Only include if post date is today or earlier
        return postDate <= now;
      })
      .sort((a, b) => b.date - a.date); // Sort by date descending

    console.log(`Filtered posts collection has ${filteredPosts.length} posts`);
    if (filteredPosts.length > 0) {
      console.log(
        `Latest post: ${filteredPosts[0].data.title} (${filteredPosts[0].date.toISOString()})`
      );
    } else {
      console.log("No posts found");
    }

    return filteredPosts;
  });

  // Configure Markdown with anchors
  const markdownLibrary = markdownIt({
    html: true,
    breaks: true,
    linkify: true,
  }).use(markdownItAnchor, {
    permalink: markdownItAnchor.permalink.ariaHidden({
      placement: "after",
      class: "header-anchor",
      symbol: "#",
      level: [1, 2, 3, 4],
    }),
    slugify: (s) =>
      s
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w-]+/g, ""),
  });

  eleventyConfig.setLibrary("md", markdownLibrary);

  // Add plugins
  eleventyConfig.addPlugin(navigationPlugin);
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(pluginRss);

  // ---------- ASSET HANDLING ----------

  // Copy assets
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy({
    "src/css/prism-theme-dark.css": "css/prism-theme-dark.css",
  });

  // Copy scripts/dashboard/ensure-dashboard-data.js to the output directory
  eleventyConfig.on("afterBuild", () => {
    try {
      console.log("Ensuring dashboard data is available...");
      const script = require("./scripts/dashboard/ensure-dashboard-data.js");
      if (typeof script.ensureDashboardData === "function") {
        script.ensureDashboardData();
      } else {
        console.log("Running dashboard data script independently...");
        require("child_process").execSync(
          "node scripts/dashboard/ensure-dashboard-data.js",
          {
            stdio: "inherit",
          }
        );
      }
    } catch (error) {
      console.warn("Error running dashboard data script:", error.message);
    }
  });

  // JS handling (development vs production)
  if (process.env.NODE_ENV !== "production") {
    eleventyConfig.addPassthroughCopy("src/js");
  } else {
    // In production, we'll use minified bundle
    eleventyConfig.addPassthroughCopy({ "_site/js/bundle.min.js": "js/bundle.min.js" });
  }

  // CSS handling
  eleventyConfig.addPassthroughCopy("src/css");

  // Copy website essentials
  eleventyConfig.addPassthroughCopy({ "site.webmanifest": "site.webmanifest" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/favicon.ico": "favicon.ico" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/icon.svg": "icon.svg" });
  eleventyConfig.addPassthroughCopy({
    "assets/icons/apple-touch-icon.png": "apple-touch-icon.png",
  });
  eleventyConfig.addPassthroughCopy({
    "assets/icons/android-chrome-192x192.png": "android-chrome-192x192.png",
  });
  eleventyConfig.addPassthroughCopy({
    "assets/icons/android-chrome-512x512.png": "android-chrome-512x512.png",
  });
  eleventyConfig.addPassthroughCopy(".nojekyll");

  // ---------- FILTERS ----------

  // Debug filter
  eleventyConfig.addFilter("log", function (value) {
    console.log("DEBUG:", value);
    return value;
  });

  // Date filters
  eleventyConfig.addFilter("isoDate", function (date) {
    return new Date(date).toISOString();
  });

  eleventyConfig.addFilter("readableDate", function (date) {
    const d = new Date(date);
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  });

  eleventyConfig.addFilter("date", function (date, format) {
    const d = new Date(date);

    // Handle different format strings
    if (format === "yyyy") {
      return d.getFullYear().toString();
    } else if (format === "MM") {
      return (d.getMonth() + 1).toString().padStart(2, "0");
    } else if (format === "dd") {
      return d.getDate().toString().padStart(2, "0");
    } else if (format === "MM-dd") {
      return `${(d.getMonth() + 1).toString().padStart(2, "0")}-${d.getDate().toString().padStart(2, "0")}`;
    } else if (format === "MMM") {
      return d.toLocaleDateString("en-US", { month: "short" });
    } else if (format === "MMM d, yyyy") {
      return d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    }

    // Default: return ISO string
    return d.toISOString();
  });

  // Text manipulation filters
  eleventyConfig.addFilter("striptags", function (value) {
    // Simple HTML tag stripper
    return value.replace(/<[^>]*>/g, "");
  });

  // Link preview filters
  eleventyConfig.addFilter("getPreviewByUrl", function (previewsArray, url) {
    if (!previewsArray || !Array.isArray(previewsArray)) return null;
    return previewsArray.find((p) => p.url === url);
  });

  eleventyConfig.addFilter("formatDate", function (dateString) {
    if (!dateString) return "";
    try {
      const date = new Date(dateString);
      // If invalid date, return empty string
      if (isNaN(date.getTime())) return "";

      const now = new Date();
      const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));

      if (diffInDays < 1) {
        return "Today";
      } else if (diffInDays === 1) {
        return "Yesterday";
      } else if (diffInDays < 7) {
        return `${diffInDays} days ago`;
      } else if (diffInDays < 30) {
        const weeks = Math.floor(diffInDays / 7);
        return `${weeks} ${weeks === 1 ? "week" : "weeks"} ago`;
      } else {
        return date.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
        });
      }
    } catch (error) {
      return "";
    }
  });

  // JSON filter
  eleventyConfig.addFilter("json", function (value) {
    return JSON.stringify(value);
  });

  // Post utility filters

  // Extract headings for Table of Contents
  eleventyConfig.addFilter("extractHeadings", (content) => {
    if (!content) return [];

    const headings = [];
    const regex = /<h([2-3])[^>]*id="([^"]*)"[^>]*>(.*?)<\/h\1>/g;
    let match;

    while ((match = regex.exec(content)) !== null) {
      const level = match[1];
      const id = match[2];
      // Remove any HTML tags and get plain text
      const text = match[3].replace(/<[^>]*>/g, "");

      headings.push({
        level,
        id,
        text,
      });
    }

    return headings;
  });

  // Reading time estimation
  eleventyConfig.addFilter("readingTime", (content) => {
    if (!content) return "";

    const contentText = content.replace(/<[^>]*>/g, "");
    const wordCount = contentText.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200); // 200 words per minute

    return readingTime;
  });

  // Get related posts based on tags
  eleventyConfig.addFilter("getRelatedPosts", (collection, currentPost, limit = 3) => {
    // Safety checks
    if (!collection || !currentPost) return [];
    if (!currentPost.data || !currentPost.data.tags) return [];

    const currentTags = Array.isArray(currentPost.data.tags)
      ? currentPost.data.tags.filter((tag) => tag !== "posts")
      : [];

    // If no meaningful tags, return empty array
    if (currentTags.length === 0) return [];

    // Create an array of posts that share tags with the current post
    const relatedPosts = collection
      .filter((post) => {
        // Safety checks
        if (!post || !post.data) return false;

        // Don't include the current post
        if (post.url === currentPost.url) return false;

        // Check if it has tags
        if (!post.data.tags || !Array.isArray(post.data.tags)) return false;

        // Check if any tags match (excluding the 'posts' tag)
        const postTags = post.data.tags.filter((tag) => tag !== "posts");

        return currentTags.some((tag) => postTags.includes(tag));
      })
      .sort((a, b) => {
        // Count matching tags
        const aTags = a.data.tags.filter(
          (tag) => tag !== "posts" && currentTags.includes(tag)
        ).length;

        const bTags = b.data.tags.filter(
          (tag) => tag !== "posts" && currentTags.includes(tag)
        ).length;

        // Sort by number of matching tags (descending)
        return bTags - aTags;
      })
      .slice(0, limit);

    return relatedPosts;
  });

  // Collection utilities
  eleventyConfig.addFilter("getNewestCollectionItemDate", (collection) => {
    if (!collection || !collection.length) {
      return new Date();
    }

    return new Date(
      Math.max(
        ...collection.map((item) => {
          return item.date ? item.date.getTime() : 0;
        })
      )
    );
  });

  // ---------- SHORTCODES ----------

  // Basic utility shortcodes
  eleventyConfig.addShortcode("year", () => new Date().getFullYear());
  eleventyConfig.addAsyncShortcode("image", imageShortcode);

  // Breadcrumb shortcode
  eleventyConfig.addShortcode("breadcrumbs", function (page) {
    if (!page || !page.url) return "";

    const parts = page.url.split("/").filter((part) => part);
    let breadcrumbs =
      '<nav aria-label="Breadcrumb" class="breadcrumbs"><div class="breadcrumbs-list">';

    // Add home
    breadcrumbs +=
      '<span class="breadcrumbs-item"><a href="/" class="breadcrumbs-link">Home</a></span>';

    // Build the breadcrumb path
    let path = "";
    parts.forEach((part, i) => {
      path += `/${part}`;

      // Add separator
      breadcrumbs += '<span class="breadcrumbs-separator">&gt;</span>';

      // Last item (current page)
      if (i === parts.length - 1) {
        const label = page.title || part.replace(/-/g, " ");
        breadcrumbs += `<span class="breadcrumbs-item current">${label}</span>`;
      } else {
        // Handle special cases
        if (part === "posts") {
          // For blog posts, link to the blog page instead of /posts/
          breadcrumbs += `<span class="breadcrumbs-item">
            <a href="/blog/" class="breadcrumbs-link">Blog</a>
          </span>`;
        } else {
          // Get proper title if available
          const segment = part.replace(/-/g, " ");
          const title = segment.charAt(0).toUpperCase() + segment.slice(1);

          breadcrumbs += `<span class="breadcrumbs-item">
            <a href="${path}/" class="breadcrumbs-link">${title}</a>
          </span>`;
        }
      }
    });

    breadcrumbs += "</div></nav>";
    return breadcrumbs;
  });

  // ---------- EXTERNAL DATA ----------

  // Load data from the unified data directory
  function loadDataFile(filePath, defaultValue = null) {
    try {
      if (fs.existsSync(filePath)) {
        const data = JSON.parse(fs.readFileSync(filePath, "utf8"));
        return data;
      }
    } catch (error) {
      console.warn(`Error loading data file ${filePath}:`, error.message);
    }
    return defaultValue;
  }

  // Unified data loading from src/_data/core
  const dataDir = path.join(__dirname, "src", "_data", "core");

  // Load arXiv data
  const arxivData = loadDataFile(path.join(dataDir, "arxiv-feed.json"), []);
  eleventyConfig.addGlobalData("arxiv_feed", () => arxivData);
  console.log(`Loaded arXiv data with ${arxivData.length} papers`);

  // Load current reading data
  const currentReadingData = loadDataFile(
    path.join(dataDir, "current-reading.json"),
    []
  );
  eleventyConfig.addGlobalData("current_reading", () => currentReadingData);
  console.log(`Loaded current reading data with ${currentReadingData.length} items`);

  // Load books data
  const booksData = loadDataFile(path.join(dataDir, "books.json"), []);
  eleventyConfig.addGlobalData("books", () => booksData);
  console.log(`Loaded books data with ${booksData.length} books`);

  // Load GitHub pins
  const githubPinsData = loadDataFile(path.join(dataDir, "github-pins.json"), []);
  eleventyConfig.addGlobalData("github_pins", () => githubPinsData);

  // Load blog images mapping
  const blogImagesPath = path.join(
    __dirname,
    "src",
    "_data",
    "config",
    "blog",
    "images.json"
  );
  const blogImagesData = loadDataFile(blogImagesPath, {
    image_mapping: {
      default: {
        path: "github-style/blog-placeholder.jpg",
        alt: "Default blog post illustration",
      },
    },
    keyword_mapping: {},
  });

  eleventyConfig.addGlobalData("blog_images", () => blogImagesData);
  console.log("Loaded blog images mapping data");

  // Load social media data
  const socialMediaPath = path.join(
    __dirname,
    "src",
    "_data",
    "config",
    "social",
    "social_media.json"
  );
  const socialMediaData = loadDataFile(socialMediaPath, { social_media: [] });
  eleventyConfig.addGlobalData(
    "social_media",
    () => socialMediaData.social_media || []
  );
  console.log(`Loaded ${socialMediaData.social_media?.length || 0} social media links`);

  // Blog image shortcode
  eleventyConfig.addShortcode("blogImage", function (post) {
    // Default image
    let imageKey = "default";
    const blogImages = this.ctx.blog_images || {
      image_mapping: {},
      keyword_mapping: {},
    };

    // If image is explicitly set in frontmatter, use that
    if (post.data && post.data.image) {
      return {
        path: post.data.image,
        alt: post.data.image_alt || "Blog post illustration",
      };
    }

    // Check tags first
    if (post.data && post.data.tags && Array.isArray(post.data.tags)) {
      for (const tag of post.data.tags) {
        const lowercaseTag = tag.toLowerCase();
        if (blogImages.image_mapping[lowercaseTag]) {
          imageKey = lowercaseTag;
          break;
        }
      }
    }

    // If we still have the default, try to infer from title and content
    if (imageKey === "default" && post.data && post.data.title) {
      const titleLower = post.data.title.toLowerCase();

      // Check for pizza in title as a special case
      if (titleLower.includes("pizza")) {
        return blogImages.image_mapping["pizza"] || blogImages.image_mapping["default"];
      }

      // Check each keyword mapping to find a match
      for (const [key, keywords] of Object.entries(blogImages.keyword_mapping)) {
        for (const keyword of keywords) {
          if (titleLower.includes(keyword.toLowerCase())) {
            imageKey = key;
            break;
          }
        }
        if (imageKey !== "default") break;
      }
    }

    return blogImages.image_mapping[imageKey] || blogImages.image_mapping["default"];
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
