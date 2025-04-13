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

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

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
    const data = fs.readFileSync(filePath, 'utf8');
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
    const groupsPath = path.join(__dirname, 'config', 'links', 'groups.json');
    if (fs.existsSync(groupsPath)) {
      const groupsData = readJsonFile(groupsPath);
      if (groupsData.linkGroups && Array.isArray(groupsData.linkGroups)) {
        return groupsData.linkGroups;
      }
    }
    
    // Fall back to site.json.backup
    const siteJsonPath = path.join(__dirname, 'site.json.backup');
    if (fs.existsSync(siteJsonPath)) {
      const siteData = readJsonFile(siteJsonPath);
      if (siteData.linkGroups && Array.isArray(siteData.linkGroups)) {
        return siteData.linkGroups;
      }
    }
    
    // Return empty array as last resort
    return [];
  } catch (error) {
    console.error('Error processing link groups:', error.message);
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
      'art_culture': 'Art, Culture & Exploration',
      'fun': 'Fun & Curiosities',
      'technology': 'Technology & Innovation',
      'social_links': 'Social',
      'projects': 'Projects',
      'retrocomputing': 'Retrocomputing',
      'misc': 'Miscellaneous',
      'people': 'People',
      'creative': 'Creative',
      'artists': 'Artists', 
      'blogs': 'Blogs',
      'rollerblading': 'Rollerblading',
      'music': 'Music', 
      'gaming': 'Gaming'
    };
    
    // Check for modular config first
    const linksPath = path.join(__dirname, 'config', 'links');
    if (fs.existsSync(linksPath)) {
      const linksDir = fs.readdirSync(linksPath);
      
      for (const file of linksDir.filter(f => f.endsWith('.json') && f !== 'groups.json')) {
        const filePath = path.join(linksPath, file);
        const linkData = readJsonFile(filePath);
        
        // Get group name from filename
        const groupKey = path.basename(file, '.json');
        const groupName = groupNameMapped[groupKey] || groupKey.charAt(0).toUpperCase() + groupKey.slice(1);
        
        // Handle both formats: 'items' (old) and 'links' (new)
        if (linkData.items && Array.isArray(linkData.items)) {
          // Make sure all items have correct group
          const processedItems = linkData.items.map(item => ({
            ...item,
            group: item.group || groupName
          }));
          links.push(...processedItems);
        } else if (linkData.links && Array.isArray(linkData.links)) {
          // Add group information to each link
          const processedLinks = linkData.links.map(link => ({
            ...link,
            group: link.group || groupName
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
    const siteJsonPath = path.join(__dirname, 'site.json.backup');
    if (fs.existsSync(siteJsonPath)) {
      const siteData = readJsonFile(siteJsonPath);
      if (siteData.links && Array.isArray(siteData.links)) {
        console.log(`Loaded ${siteData.links.length} links from site.json.backup`);
        return siteData.links;
      }
    }
    
    // Return empty array as last resort
    console.warn('No links found in configuration files');
    return [];
  } catch (error) {
    console.error('Error processing links:', error.message);
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
    const configDirPath = path.join(__dirname, 'config');
    if (fs.existsSync(configDirPath)) {
      // Load theme.json
      const themePath = path.join(configDirPath, 'theme.json');
      if (fs.existsSync(themePath)) {
        config.theme = readJsonFile(themePath);
      }
      
      // Load meta.json
      const metaPath = path.join(configDirPath, 'meta.json');
      if (fs.existsSync(metaPath)) {
        Object.assign(config, readJsonFile(metaPath));
      }
      
      // Load navigation.json
      const navPath = path.join(configDirPath, 'navigation.json');
      if (fs.existsSync(navPath)) {
        const navData = readJsonFile(navPath);
        if (navData.navigation) {
          config.navigation = navData.navigation;
        }
      }
      
      // Try to load homepage configuration
      const homepagePath = path.join(configDirPath, 'homepage');
      if (fs.existsSync(homepagePath)) {
        config.homepage = {};
        
        // Load each homepage config file
        const homepageFiles = fs.readdirSync(homepagePath)
          .filter(file => file.endsWith('.json'));
        
        for (const file of homepageFiles) {
          const filePath = path.join(homepagePath, file);
          const fileData = readJsonFile(filePath);
          Object.assign(config.homepage, fileData);
        }
      }
    }
    
    // Fall back to site.json.backup for missing sections
    const siteJsonPath = path.join(__dirname, 'site.json.backup');
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
      if (!config.navigation) config.navigation = siteData.navigation;
      
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
    }
    
    // Process link groups and links using specialized functions
    config.linkGroups = processLinkGroups();
    config.links = processLinks();
    
    // Process link previews
    try {
      const linkPreviewsPath = path.join(rootDir, '_data', 'link-previews.json');
      if (fs.existsSync(linkPreviewsPath)) {
        const linkPreviewsData = fs.readFileSync(linkPreviewsPath, 'utf8');
        config.linkPreviews = JSON.parse(linkPreviewsData);
        console.log(`Loaded ${config.linkPreviews.length} link previews`);
      } else {
        console.log('No link previews data found');
        config.linkPreviews = [];
      }
    } catch (error) {
      console.error('Error loading link previews:', error.message);
      config.linkPreviews = [];
    }
    
    return config;
  } catch (error) {
    console.error('Error building site configuration:', error.message);
    
    // Return minimal configuration as fallback
    return {
      title: "William Zujkowski",
      description: "Personal website and technology blog",
      url: "https://williamzujkowski.github.io",
      linkGroups: [],
      links: []
    };
  }
}

// Build the site configuration
const siteConfig = buildSiteConfiguration();
console.log(`Site config built with ${siteConfig.linkGroups?.length || 0} link groups and ${siteConfig.links?.length || 0} links`);

/**
 * Site configuration export function
 * 
 * @returns {Object} Complete site configuration
 */
export default function() {
  return siteConfig;
}