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
 * 
 * See README.md in this directory for usage documentation.
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
 * Merges all JSON files in a directory into a single object
 * 
 * @param {string} dirPath - Path to the directory
 * @returns {Object} Combined data from all JSON files
 */
function mergeJsonFilesInDirectory(dirPath) {
  try {
    if (!fs.existsSync(dirPath)) {
      console.warn(`Directory ${dirPath} does not exist`);
      return {};
    }

    const files = fs.readdirSync(dirPath);
    return files.reduce((result, file) => {
      const filePath = path.join(dirPath, file);
      const stats = fs.statSync(filePath);
      
      if (stats.isFile() && file.endsWith('.json')) {
        const data = readJsonFile(filePath);
        return { ...result, ...data };
      }
      
      return result;
    }, {});
  } catch (error) {
    console.error(`Error merging files in ${dirPath}:`, error.message);
    return {};
  }
}

/**
 * Recursively merges all JSON files in a directory structure
 * 
 * @param {string} dirPath - Path to the root directory
 * @param {string} prefix - Optional prefix for nested properties
 * @returns {Object} Combined configuration object
 */
function mergeConfigDirectory(dirPath, prefix = '') {
  try {
    if (!fs.existsSync(dirPath)) {
      console.warn(`Directory ${dirPath} does not exist`);
      return {};
    }

    let result = {};
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    
    // First process files
    for (const entry of entries.filter(entry => entry.isFile() && entry.name.endsWith('.json'))) {
      const filePath = path.join(dirPath, entry.name);
      const key = prefix ? `${prefix}.${path.basename(entry.name, '.json')}` : path.basename(entry.name, '.json');
      const data = readJsonFile(filePath);
      
      // Handle special case for files with a single key that matches their directory
      if (Object.keys(data).length === 1 && Object.keys(data)[0] === path.basename(dirPath)) {
        result = { ...result, ...data };
      } else {
        result = { ...result, ...data };
      }
    }
    
    // Then process directories
    for (const entry of entries.filter(entry => entry.isDirectory())) {
      const subDirPath = path.join(dirPath, entry.name);
      const key = prefix ? `${prefix}.${entry.name}` : entry.name;
      
      // Special case for links directory - combine all link items
      if (entry.name === 'links') {
        const linksData = processLinksDirectory(subDirPath);
        result = { ...result, ...linksData };
      } else {
        // For homepage, we want to keep the structure flat but with prefixed keys
        if (entry.name === 'homepage') {
          const homepageData = mergeHomepageDirectory(subDirPath);
          result = { ...result, ...homepageData };
        } else {
          const subDirData = mergeConfigDirectory(subDirPath, key);
          result = { ...result, ...subDirData };
        }
      }
    }
    
    return result;
  } catch (error) {
    console.error(`Error processing directory ${dirPath}:`, error.message);
    return {};
  }
}

/**
 * Special handling for homepage directory
 * Combines all homepage configuration files into a single 'homepage' object
 * 
 * @param {string} dirPath - Path to the homepage directory
 * @returns {Object} Object with 'homepage' key containing merged homepage data
 */
function mergeHomepageDirectory(dirPath) {
  try {
    let homepage = {};
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    
    for (const entry of entries.filter(entry => entry.isFile() && entry.name.endsWith('.json'))) {
      const filePath = path.join(dirPath, entry.name);
      const data = readJsonFile(filePath);
      homepage = { ...homepage, ...data };
    }
    
    return { homepage };
  } catch (error) {
    console.error(`Error processing homepage directory:`, error.message);
    return { homepage: {} };
  }
}

/**
 * Special handling for links directory
 * Combines link groups and all link items from different categories
 * 
 * @param {string} dirPath - Path to the links directory
 * @returns {Object} Object with 'links' array and 'linkGroups' properties
 */
function processLinksDirectory(dirPath) {
  try {
    // Read linkGroups first
    const groupsFile = path.join(dirPath, 'groups.json');
    const groups = fs.existsSync(groupsFile) ? readJsonFile(groupsFile) : { linkGroups: [] };
    
    // Collect all link items
    let allLinks = [];
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    
    for (const entry of entries.filter(entry => entry.isFile() && entry.name.endsWith('.json') && entry.name !== 'groups.json')) {
      const filePath = path.join(dirPath, entry.name);
      const data = readJsonFile(filePath);
      
      if (data.items && Array.isArray(data.items)) {
        allLinks = [...allLinks, ...data.items];
      }
    }
    
    return { links: allLinks, ...groups };
  } catch (error) {
    console.error(`Error processing links directory:`, error.message);
    return { links: [], linkGroups: [] };
  }
}

// Main configuration path
const configDir = path.join(__dirname, 'config');

// Build the site configuration
const siteConfig = mergeConfigDirectory(configDir);

/**
 * Site configuration export function
 * 
 * This function returns the complete site configuration object
 * for use in Eleventy templates. The object structure mirrors 
 * the directory structure, with special handling for certain sections.
 * 
 * @returns {Object} Complete site configuration
 */
export default function() {
  return siteConfig;
};