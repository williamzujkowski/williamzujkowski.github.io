// build-github-pins.js
// This script fetches pinned repositories from a GitHub profile
// and writes them to a JSON file for use in the site.

import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current file directory with ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// GitHub username to fetch pinned repositories from
const GITHUB_USERNAME = 'williamzujkowski';

// GraphQL query to get pinned repositories
const PINNED_REPOS_QUERY = `
{
  user(login: "${GITHUB_USERNAME}") {
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          url
          stargazerCount
          forkCount
          primaryLanguage {
            name
            color
          }
          languages(first: 3, orderBy: {field: SIZE, direction: DESC}) {
            nodes {
              name
              color
            }
          }
          updatedAt
        }
      }
    }
  }
}
`;

async function fetchPinnedRepos() {
  try {
    console.log('Fetching pinned repositories from GitHub...');
    
    // Try to use GitHub token from environment variable if available
    // GitHub Actions automatically provides GITHUB_TOKEN
    const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';
    const headers = token 
      ? { 'Authorization': `Bearer ${token}` }
      : {};
      
    if (token) {
      console.log('Using GitHub token for authentication');
    } else {
      console.log('No GitHub token found, requests may be rate limited');
    }
    
    const response = await fetch('https://api.github.com/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: JSON.stringify({ query: PINNED_REPOS_QUERY })
    });

    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    
    if (data.errors) {
      throw new Error(`GraphQL error: ${data.errors.map(e => e.message).join(', ')}`);
    }

    return data.data.user.pinnedItems.nodes;
  } catch (error) {
    console.error('Error fetching pinned repositories:', error);
    
    // Return empty array if there's an error, so the build doesn't fail
    return [];
  }
}

async function main() {
  // First try to read from the modular configuration
  const reposJsonPath = path.join(__dirname, '..', 'src', '_data', 'config', 'homepage', 'repositories.json');
  let configPinnedRepos = [];
  
  try {
    // Try modular config first
    if (fs.existsSync(reposJsonPath)) {
      const reposConfig = JSON.parse(fs.readFileSync(reposJsonPath, 'utf8'));
      if (reposConfig.featured_repositories && 
          Array.isArray(reposConfig.featured_repositories) &&
          reposConfig.featured_repositories.length > 0) {
        
        console.log(`Using ${reposConfig.featured_repositories.length} repositories from modular configuration`);
        configPinnedRepos = reposConfig.featured_repositories;
      }
    }
    
    // Fallback to legacy site.json if needed
    if (configPinnedRepos.length === 0) {
      const siteJsonPath = path.join(__dirname, '..', 'src', '_data', 'site.json');
      if (fs.existsSync(siteJsonPath)) {
        const siteConfig = JSON.parse(fs.readFileSync(siteJsonPath, 'utf8'));
        if (siteConfig.homepage && 
            siteConfig.homepage.pinned_repositories && 
            Array.isArray(siteConfig.homepage.pinned_repositories) &&
            siteConfig.homepage.pinned_repositories.length > 0) {
          
          console.log(`Using ${siteConfig.homepage.pinned_repositories.length} repositories from legacy site configuration`);
          configPinnedRepos = siteConfig.homepage.pinned_repositories;
        }
      }
    }
  } catch (error) {
    console.error('Error reading configuration:', error);
  }
  
  // If we have repos from config, use those
  if (configPinnedRepos.length > 0) {
    // Define the output path
    const outputDir = path.join(__dirname, '..', '_data');
    const outputFile = path.join(outputDir, 'github-pins.json');

    // Ensure the _data directory exists
    if (!fs.existsSync(outputDir)){
      fs.mkdirSync(outputDir);
    }

    // Write the JSON file
    fs.writeFileSync(outputFile, JSON.stringify(configPinnedRepos, null, 2));
    console.log(`Successfully wrote ${configPinnedRepos.length} pinned repositories from configuration to ${outputFile}`);
    return;
  }
  
  // Otherwise fall back to GitHub API
  console.log('No repositories found in configuration, falling back to GitHub API...');
  const pinnedRepos = await fetchPinnedRepos();
  
  if (pinnedRepos.length === 0) {
    console.log('No pinned repositories found or error occurred.');
    console.log('If you need to authenticate with GitHub, set the GITHUB_TOKEN environment variable.');
    
    // Create an array with one fallback repository
    const fallbackRepos = [{
      name: "Personal Website",
      description: "My personal website and tech blog built with 11ty",
      url: `https://github.com/${GITHUB_USERNAME}/williamzujkowski.github.io`,
      primaryLanguage: { name: "JavaScript", color: "#f1e05a" },
      languages: { nodes: [{ name: "JavaScript", color: "#f1e05a" }] },
      stargazerCount: 0,
      forkCount: 0,
      updatedAt: new Date().toISOString()
    }];
    
    // Use fallback repos
    pinnedRepos.push(...fallbackRepos);
  }

  // Define the output path
  const outputDir = path.join(__dirname, '..', '_data');
  const outputFile = path.join(outputDir, 'github-pins.json');

  // Ensure the _data directory exists
  if (!fs.existsSync(outputDir)){
    fs.mkdirSync(outputDir);
  }

  // Write the JSON file
  fs.writeFileSync(outputFile, JSON.stringify(pinnedRepos, null, 2));
  console.log(`Successfully wrote ${pinnedRepos.length} pinned repositories from GitHub API to ${outputFile}`);
}

main();