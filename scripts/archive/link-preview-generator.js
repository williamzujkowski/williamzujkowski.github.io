/**
 * Link Preview Generator
 *
 * Generates metadata-based link previews for site links without needing screenshots.
 * Uses metascraper to fetch metadata from URLs and stores it in JSON files.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import got from "got";
import metascraper from "metascraper";
import metascraperAuthor from "metascraper-author";
import metascraperDate from "metascraper-date";
import metascraperDescription from "metascraper-description";
import metascraperImage from "metascraper-image";
import metascraperLogo from "metascraper-logo";
import metascraperPublisher from "metascraper-publisher";
import metascraperTitle from "metascraper-title";
import metascraperUrl from "metascraper-url";

// Get directory paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..");
const dataDir = path.join(rootDir, "_data");
const assetsDataDir = path.join(rootDir, "assets", "data");
const srcDataDir = path.join(rootDir, "src", "_data");
const configLinksDir = path.join(srcDataDir, "config", "links");

// Initialize metascraper
const scraper = metascraper([
  metascraperAuthor(),
  metascraperDate(),
  metascraperDescription(),
  metascraperImage(),
  metascraperLogo(),
  metascraperPublisher(),
  metascraperTitle(),
  metascraperUrl(),
]);

// Ensure output directories exist
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

if (!fs.existsSync(path.join(assetsDataDir))) {
  fs.mkdirSync(path.join(assetsDataDir), { recursive: true });
}

/**
 * Convert a string to a URL-friendly slug
 */
function slugify(text) {
  return text
    .toString()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\w\-]+/g, "")
    .replace(/\-\-+/g, "-")
    .replace(/^-+/, "")
    .replace(/-+$/, "");
}

/**
 * Load links from configuration files
 */
async function loadLinks() {
  try {
    const links = [];
    const groupNameMapped = {
      art_culture: "Art, Culture & Exploration",
      fun: "Fun & Curiosities",
      technology: "Technology & Innovation",
      social_links: "Social",
      projects: "Projects",
      retrocomputing: "Retrocomputing",
      misc: "Miscellaneous",
      people: "People",
      creative: "Creative",
      artists: "Artists",
      blogs: "Blogs",
      rollerblading: "Rollerblading",
      music: "Music",
      gaming: "Gaming",
    };

    // Check for modular config
    if (fs.existsSync(configLinksDir)) {
      const linksDir = fs.readdirSync(configLinksDir);

      for (const file of linksDir.filter(
        (f) => f.endsWith(".json") && f !== "groups.json"
      )) {
        const filePath = path.join(configLinksDir, file);
        const fileData = fs.readFileSync(filePath, "utf8");
        const linkData = JSON.parse(fileData);

        // Get group name from filename
        const groupKey = path.basename(file, ".json");
        const groupName =
          groupNameMapped[groupKey] ||
          groupKey.charAt(0).toUpperCase() + groupKey.slice(1);

        // Handle both formats: 'items' (old) and 'links' (new)
        if (linkData.items && Array.isArray(linkData.items)) {
          // Make sure all items have correct group
          const processedItems = linkData.items.map((item) => ({
            ...item,
            group: item.group || groupName,
          }));
          links.push(...processedItems);
        } else if (linkData.links && Array.isArray(linkData.links)) {
          // Add group information to each link
          const processedLinks = linkData.links.map((link) => ({
            ...link,
            group: link.group || groupName,
          }));
          links.push(...processedLinks);
        }
      }
    }

    console.log(`Loaded ${links.length} links from configuration`);
    return links;
  } catch (error) {
    console.error("Error loading links:", error);
    return [];
  }
}

/**
 * Fetch metadata for a URL using metascraper
 */
async function fetchMetadata(url) {
  try {
    console.log(`Fetching metadata for ${url}`);
    const { body: html, url: finalUrl } = await got(url, { timeout: 10000 });
    const metadata = await scraper({ html, url: finalUrl });
    return { ...metadata, status: "success" };
  } catch (error) {
    console.error(`Error fetching metadata for ${url}:`, error.message);
    return {
      status: "error",
      error: error.message,
    };
  }
}

/**
 * Generate and save link previews
 */
async function generateLinkPreviews() {
  try {
    // Load all links
    const links = await loadLinks();
    if (links.length === 0) {
      console.log("No links found, exiting.");
      return;
    }

    // Group links by category
    const linksByGroup = {};
    const allPreviews = [];

    // Process each link
    for (const link of links) {
      if (!link.url) continue;

      // Generate a unique ID for the link
      const id = link.id || slugify(link.name);

      // Fetch metadata for the link
      const metadata = await fetchMetadata(link.url);

      // Create preview object
      const preview = {
        id,
        url: link.url,
        name: link.name,
        type: "link",
        group: link.group,
        metadata,
        description: link.description || metadata.description,
        last_checked: new Date().toISOString(),
      };

      // Add to group-specific array
      const groupSlug = slugify(link.group);
      if (!linksByGroup[groupSlug]) {
        linksByGroup[groupSlug] = [];
      }
      linksByGroup[groupSlug].push(preview);

      // Add to all previews
      allPreviews.push(preview);
    }

    // Save all previews to a single file
    fs.writeFileSync(
      path.join(dataDir, "link-previews.json"),
      JSON.stringify(allPreviews, null, 2)
    );

    // Create a copy in the assets directory
    if (!fs.existsSync(assetsDataDir)) {
      fs.mkdirSync(assetsDataDir, { recursive: true });
    }
    fs.writeFileSync(
      path.join(assetsDataDir, "link-previews.json"),
      JSON.stringify(allPreviews, null, 2)
    );

    // Save group-specific preview files
    for (const [group, groupPreviews] of Object.entries(linksByGroup)) {
      fs.writeFileSync(
        path.join(assetsDataDir, `link-previews-${group}.json`),
        JSON.stringify(groupPreviews, null, 2)
      );
    }

    // Create index file mapping URLs to preview IDs
    const previewIndex = allPreviews.reduce((acc, preview) => {
      acc[preview.url] = preview.id;
      return acc;
    }, {});

    fs.writeFileSync(
      path.join(assetsDataDir, "link-previews-index.json"),
      JSON.stringify(previewIndex, null, 2)
    );

    console.log(
      `Generated preview data for ${allPreviews.length} links in ${Object.keys(linksByGroup).length} groups.`
    );
  } catch (error) {
    console.error("Error generating link previews:", error);
    process.exit(1);
  }
}

// Run the generator
generateLinkPreviews()
  .then(() => {
    console.log("Link preview generation complete!");
  })
  .catch((error) => {
    console.error("Error in link preview generation:", error);
    process.exit(1);
  });
