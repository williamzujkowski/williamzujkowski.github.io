/**
 * site.js - Unified site configuration
 *
 * This module handles loading and merging all modular configuration files from
 * the config directory into a single site configuration object for use in templates.
 *
 * Key features:
 * - Loads JSON files from a structured directory hierarchy
 * - Merges configuration in a predictable way
 * - Provides special handling for sections like homepage and links
 * - Handles errors gracefully with fallbacks
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Get the directory name in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Reads and parses a JSON file
 *
 * @param {string} filePath - Path to the JSON file
 * @returns {Object} Parsed JSON data or empty object on error
 */
function readJsonFile(filePath) {
  try {
    const data = fs.readFileSync(filePath, "utf8");
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error reading ${filePath}:`, error.message);
    return {};
  }
}

/**
 * Process link groups from configuration
 *
 * @returns {Array} Array of link groups
 */
function processLinkGroups() {
  try {
    // Check for modular config first
    const groupsPath = path.join(__dirname, "config", "links", "groups.json");
    if (fs.existsSync(groupsPath)) {
      const groupsData = readJsonFile(groupsPath);
      if (groupsData.linkGroups && Array.isArray(groupsData.linkGroups)) {
        return groupsData.linkGroups;
      }
    }

    // Fall back to site.json.backup
    const siteJsonPath = path.join(__dirname, "site.json.backup");
    if (fs.existsSync(siteJsonPath)) {
      const siteData = readJsonFile(siteJsonPath);
      if (siteData.linkGroups && Array.isArray(siteData.linkGroups)) {
        return siteData.linkGroups;
      }
    }

    // Return empty array as last resort
    return [];
  } catch (error) {
    console.error("Error processing link groups:", error.message);
    return [];
  }
}

/**
 * Process links from modular configuration
 *
 * @returns {Array} Array of links
 */
function processLinks() {
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

    console.log("Starting to process links");

    // Check for modular config first
    const linksPath = path.join(__dirname, "config", "links");
    if (fs.existsSync(linksPath)) {
      const linksDir = fs.readdirSync(linksPath);

      for (const file of linksDir.filter(
        (f) => f.endsWith(".json") && f !== "groups.json"
      )) {
        const filePath = path.join(linksPath, file);
        const linkData = readJsonFile(filePath);

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

      if (links.length > 0) {
        console.log(`Loaded ${links.length} links from modular configuration`);
        return links;
      }
    }

    // Fall back to site.json.backup
    const siteJsonPath = path.join(__dirname, "site.json.backup");
    if (fs.existsSync(siteJsonPath)) {
      const siteData = readJsonFile(siteJsonPath);
      if (siteData.links && Array.isArray(siteData.links)) {
        console.log(`Loaded ${siteData.links.length} links from site.json.backup`);
        return siteData.links;
      }
    }

    // Return empty array as last resort
    console.warn("No links found in configuration files");
    return [];
  } catch (error) {
    console.error("Error processing links:", error.message);
    return [];
  }
}

/**
 * Load configuration from files and build complete site config
 */
function buildSiteConfiguration() {
  try {
    let config = {};

    // Try to load modular configuration
    const configDirPath = path.join(__dirname, "config");
    if (fs.existsSync(configDirPath)) {
      // Load theme.json
      const themePath = path.join(configDirPath, "theme.json");
      if (fs.existsSync(themePath)) {
        config.theme = readJsonFile(themePath);
      }

      // Load meta.json
      const metaPath = path.join(configDirPath, "meta.json");
      if (fs.existsSync(metaPath)) {
        Object.assign(config, readJsonFile(metaPath));
      }

      // Load navigation.json
      const navPath = path.join(configDirPath, "navigation.json");
      if (fs.existsSync(navPath)) {
        const navData = readJsonFile(navPath);
        if (navData.navigation) {
          config.navigation = navData.navigation;
          console.log(`Loaded ${config.navigation.length} navigation items from ${navPath}`);
        } else {
          console.warn(`Navigation data found at ${navPath} but missing 'navigation' key`);
        }
      } else {
        console.warn(`Navigation file not found at ${navPath}`);
      }

      // Try to load homepage configuration
      const homepagePath = path.join(configDirPath, "homepage");
      if (fs.existsSync(homepagePath)) {
        config.homepage = {};

        // Load each homepage config file
        const homepageFiles = fs
          .readdirSync(homepagePath)
          .filter((file) => file.endsWith(".json"));

        for (const file of homepageFiles) {
          const filePath = path.join(homepagePath, file);
          const fileData = readJsonFile(filePath);
          Object.assign(config.homepage, fileData);
        }
      }

      // Load social media configuration
      const socialPath = path.join(configDirPath, "social");
      if (fs.existsSync(socialPath)) {
        const socialMediaPath = path.join(socialPath, "social_media.json");
        if (fs.existsSync(socialMediaPath)) {
          const socialData = readJsonFile(socialMediaPath);
          if (socialData.social_media && Array.isArray(socialData.social_media)) {
            config.social_media = socialData.social_media;
            console.log(`Loaded ${config.social_media.length} social media links`);
          }
        }
      }
    }

    // Fall back to site.json.backup for missing sections
    const siteJsonPath = path.join(__dirname, "site.json.backup");
    if (fs.existsSync(siteJsonPath)) {
      const siteData = readJsonFile(siteJsonPath);

      // Use backup values for any missing fields
      if (!config.title) config.title = siteData.title;
      if (!config.description) config.description = siteData.description;
      if (!config.url) config.url = siteData.url;
      if (!config.author) config.author = siteData.author;
      if (!config.email) config.email = siteData.email;
      if (!config.theme) config.theme = siteData.theme;
      if (!config.seo) config.seo = siteData.seo;
      if (!config.navigation) {
        config.navigation = siteData.navigation;
        if (config.navigation) {
          console.log(`Loaded ${config.navigation.length} navigation items from site.json.backup`);
        } else {
          console.warn("No navigation data found in site.json.backup");
        }
      }

      // Copy homepage settings if missing
      if (!config.homepage && siteData.homepage) {
        config.homepage = siteData.homepage;
      } else if (config.homepage && siteData.homepage) {
        // Fill in any missing homepage settings
        for (const key in siteData.homepage) {
          if (!config.homepage[key]) {
            config.homepage[key] = siteData.homepage[key];
          }
        }
      }

      // Copy blog settings if missing
      if (!config.blog && siteData.blog) {
        config.blog = siteData.blog;
      }

      // Copy social media settings if missing
      if (!config.social_media && siteData.social_media) {
        config.social_media = siteData.social_media;
        console.log(
          `Loaded ${config.social_media.length} social media links from backup`
        );
      }
    }

    // Process link groups and links using specialized functions
    config.linkGroups = processLinkGroups();
    config.links = processLinks();

    // Process link previews
    try {
      // Define the rootDir properly for this context
      const dataRootDir = path.resolve(__dirname, "..", "..");
      const linkPreviewsPath = path.join(dataRootDir, "_data", "link-previews.json");

      if (fs.existsSync(linkPreviewsPath)) {
        const linkPreviewsData = fs.readFileSync(linkPreviewsPath, "utf8");
        config.linkPreviews = JSON.parse(linkPreviewsData);
        console.log(`Loaded ${config.linkPreviews.length} link previews`);
      } else {
        console.log("No link previews data found");
        config.linkPreviews = [];
      }
    } catch (error) {
      console.error("Error loading link previews:", error.message);
      config.linkPreviews = [];
    }

    return config;
  } catch (error) {
    console.error("Error building site configuration:", error.message);

    // Return minimal configuration as fallback
    return {
      title: "William Zujkowski",
      description: "Personal website and technology blog",
      url: "https://williamzujkowski.github.io",
      navigation: [
        {
          name: "Home",
          url: "/",
          icon: ""
        },
        {
          name: "Links",
          url: "/links/",
          icon: ""
        },
        {
          name: "Blog",
          url: "/blog/",
          icon: ""
        },
        {
          name: "Vulnerability Analysis",
          url: "/vulnerability-analysis/",
          icon: "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"currentColor\" class=\"bi bi-shield-exclamation\" viewBox=\"0 0 16 16\"><path d=\"M5.338 1.59a61 61 0 0 0-2.837.856.48.48 0 0 0-.328.39c-.554 4.157.726 7.19 2.253 9.188a10.7 10.7 0 0 0 2.287 2.233c.346.244.652.42.893.533q.18.085.293.126a1 1 0 0 0 .866 0q.114-.04.293-.126c.24-.113.547-.29.893-.533a10.7 10.7 0 0 0 2.287-2.233c1.527-1.997 2.807-5.03 2.253-9.188a.48.48 0 0 0-.328-.39c-.651-.213-1.75-.56-2.837-.856C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.524zM5.072.56C6.157.265 7.31 0 8 0s1.843.265 2.928.56c1.11.3 2.229.655 2.887.87a1.54 1.54 0 0 1 1.044 1.262c.596 4.477-.787 7.795-2.465 9.99a11.8 11.8 0 0 1-2.517 2.453 7 7 0 0 1-1.048.625c-.28.132-.581.24-.829.24s-.548-.108-.829-.24a7 7 0 0 1-1.048-.625 11.8 11.8 0 0 1-2.517-2.453C1.928 10.487.545 7.169 1.141 2.692A1.54 1.54 0 0 1 2.185 1.43 63 63 0 0 1 5.072.56z\"/><path d=\"M7.001 11h2v2h-2zm1-8a1 1 0 0 0-1 1v4a1 1 0 1 0 2 0V4a1 1 0 0 0-1-1z\"/></svg>"
        }
      ],
      linkGroups: [],
      links: [],
      social_media: [],
    };
  }
}

// Build the site configuration
const siteConfig = buildSiteConfiguration();
console.log(
  `Site config built with ${siteConfig.navigation?.length || 0} navigation items, ${siteConfig.linkGroups?.length || 0} link groups, ${siteConfig.links?.length || 0} links, and ${siteConfig.social_media?.length || 0} social media links`
);

/**
 * Site configuration export function
 *
 * @returns {Object} Complete site configuration
 */
export default function () {
  return siteConfig;
}
