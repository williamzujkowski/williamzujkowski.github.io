module.exports = function (eleventyConfig) {
  // Just a simple passthrough config for GitHub Actions
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy({
    "src/css/prism-theme-dark.css": "css/prism-theme-dark.css",
  });
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

  // Import required modules
  const pluginRss = require("@11ty/eleventy-plugin-rss");
  const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
  const pluginNavigation = require("@11ty/eleventy-navigation");
  const markdownIt = require("markdown-it");
  const markdownItAnchor = require("markdown-it-anchor");
  const { DateTime } = require("luxon");

  // Add plugins
  eleventyConfig.addPlugin(pluginRss);
  eleventyConfig.addPlugin(pluginNavigation);
  eleventyConfig.addPlugin(syntaxHighlight);

  // Add a manual filter for collections.getNewestCollectionItemDate
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

  // Add a custom collection for posts that explicitly filters out future-dated posts
  eleventyConfig.addCollection("posts", function (collectionApi) {
    const now = new Date();
    now.setHours(0, 0, 0, 0); // Set to beginning of day for consistent comparison
    console.log(`Current date for filtering: ${now.toISOString()}`);

    // Get all posts and filter out future posts
    return collectionApi
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
  });

  // Add date filters
  eleventyConfig.addFilter("readableDate", (dateObj) => {
    return DateTime.fromJSDate(dateObj, { zone: "utc" }).toFormat("LLLL dd, yyyy");
  });

  eleventyConfig.addFilter("isoDate", (dateObj) => {
    return DateTime.fromJSDate(dateObj, { zone: "utc" }).toISO();
  });

  eleventyConfig.addFilter("date", (dateObj, format) => {
    if (typeof dateObj === "string") {
      dateObj = new Date(dateObj);
    }
    return DateTime.fromJSDate(dateObj).toFormat(format || "LLLL dd, yyyy");
  });

  // Configure Markdown with anchors
  const markdownLibrary = markdownIt({
    html: true,
    breaks: true,
    linkify: true,
  }).use(markdownItAnchor);

  eleventyConfig.setLibrary("md", markdownLibrary);

  // Add Eleventy 3.0+ compatible shortcodes
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);

  // HTML to Absolute URLs for RSS feeds
  eleventyConfig.addNunjucksAsyncFilter(
    "htmlToAbsoluteUrls",
    function (html, base, callback) {
      if (!html) {
        callback(null, "");
        return;
      }

      try {
        const baseUrl = new URL(base);
        // Simple replacement for links and images
        let result = html.replace(
          /(href|src)="(?!http|mailto|#|\/\/)(.*?)"/g,
          `$1="${baseUrl.origin}/$2"`
        );
        callback(null, result);
      } catch (e) {
        console.error("Error converting HTML to absolute URLs:", e);
        callback(null, html);
      }
    }
  );

  // Add breadcrumb shortcode
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

  // Add image shortcode
  eleventyConfig.addShortcode("image", function (src, alt, sizes = "100vw") {
    if (!src) {
      throw new Error(`Missing image source`);
    }
    if (!alt) {
      throw new Error(`Missing alt text for image: ${src}`);
    }

    // Ensure correct path structure
    let imgSrc = src;
    // If it's a relative path that could be from a blog post
    if (!src.startsWith("/") && !src.startsWith("./") && !src.startsWith("../")) {
      imgSrc = `/assets/images/${src}`;
    }

    // Simple image tag for GitHub Actions build
    return `<img src="${imgSrc}" alt="${alt}" class="w-full h-auto object-cover" loading="lazy" decoding="async">`;
  });

  // Reading time estimation
  eleventyConfig.addFilter("readingTime", (content) => {
    if (!content) return "";

    const contentText = content.replace(/<[^>]*>/g, "");
    const wordCount = contentText.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200); // 200 words per minute

    return readingTime;
  });

  // Extract headings from content for TOC
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

  // Add a shortcode for getting the appropriate blog image based on post content
  eleventyConfig.addShortcode("blogImage", function (post) {
    // Default image
    let imageKey = "default";

    // For the fallback config, use a hardcoded default mapping
    // This ensures the build works even without access to the images.json file
    let blogImages = {
      image_mapping: {
        ai: {
          path: "blog/ai-blog.jpg",
          alt: "AI illustration with neural networks and connections",
        },
        security: {
          path: "blog/security-blog.jpg",
          alt: "Cybersecurity lock and shield illustration",
        },
        cloud: {
          path: "blog/cloud-blog.jpg",
          alt: "Cloud computing infrastructure illustration",
        },
        ethics: {
          path: "blog/ethics-blog.jpg",
          alt: "AI ethics balance scale illustration",
        },
        transformer: {
          path: "blog/transformer-blog.jpg",
          alt: "Transformer architecture neural network illustration",
        },
        pizza: {
          path: "blog/pizza-blog.jpg",
          alt: "Developer pizza calculator illustration",
        },
        quantum: {
          path: "blog/topics/quantum.jpg",
          alt: "Quantum computing illustration with qubits and superposition",
        },
        llm: {
          path: "blog/topics/llm.jpg",
          alt: "Large Language Model illustration with text processing",
        },
        default: {
          path: "github-style/blog-placeholder.jpg",
          alt: "Default blog post illustration",
        },
      },
      keyword_mapping: {
        security: [
          "secure",
          "security",
          "exploit",
          "vulnerability",
          "cybersecurity",
          "cyber",
        ],
        ai: [
          "ai",
          "artificial intelligence",
          "machine learning",
          "ml",
          "deep learning",
          "neural",
          "model",
        ],
        cloud: ["cloud", "aws", "azure", "gcp", "serverless", "iaas", "paas", "saas"],
        ethics: ["ethics", "ethical", "bias", "fairness", "responsible ai"],
        transformer: ["transformer", "attention", "encoder", "decoder"],
        pizza: ["pizza", "calculator"],
        quantum: ["quantum", "qubit", "superposition", "entanglement"],
        llm: [
          "llm",
          "language model",
          "gpt",
          "claude",
          "gemini",
          "large language model",
        ],
      },
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
        if (blogImages.image_mapping && blogImages.image_mapping[lowercaseTag]) {
          imageKey = lowercaseTag;
          break;
        }
      }
    }

    // If we still have the default, try to infer from title and content
    if (imageKey === "default" && post.data && post.data.title) {
      const titleLower = post.data.title.toLowerCase();

      // Check for pizza in title as a special case
      if (
        titleLower.includes("pizza") &&
        blogImages.image_mapping &&
        blogImages.image_mapping["pizza"]
      ) {
        return blogImages.image_mapping["pizza"];
      }

      // Check each keyword mapping to find a match
      if (blogImages.keyword_mapping) {
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
    }

    // Return the appropriate image or default if not found
    if (blogImages.image_mapping && blogImages.image_mapping[imageKey]) {
      return blogImages.image_mapping[imageKey];
    }

    // Fallback to hardcoded default if nothing is available
    return {
      path: "github-style/blog-placeholder.jpg",
      alt: "Blog post illustration",
    };
  });

  // Load social media data
  const fs = require("fs");
  const path = require("path");
  const socialMediaPath = path.resolve(
    __dirname,
    "src",
    "_data",
    "config",
    "social",
    "social_media.json"
  );
  try {
    if (fs.existsSync(socialMediaPath)) {
      const socialMediaData = JSON.parse(fs.readFileSync(socialMediaPath, "utf8"));
      eleventyConfig.addGlobalData("social_media", socialMediaData.social_media || []);
      console.log(
        `Loaded ${socialMediaData.social_media?.length || 0} social media links`
      );
    } else {
      console.log("Social media configuration not found");
      eleventyConfig.addGlobalData("social_media", []);
    }
  } catch (error) {
    console.error("Error loading social media configuration:", error);
    eleventyConfig.addGlobalData("social_media", []);
  }

  // Site structure
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts",
    },
  };
};
