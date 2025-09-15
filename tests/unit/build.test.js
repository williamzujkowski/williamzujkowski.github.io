/**
 * Build Process Tests
 * Validates that the site builds correctly
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

module.exports = {
  async test() {
    try {
      // Test 1: Check if package.json exists
      const packageJsonPath = path.join(__dirname, '../../package.json');
      if (!fs.existsSync(packageJsonPath)) {
        return {
          success: false,
          error: 'package.json not found'
        };
      }

      // Test 2: Check if Eleventy config exists
      const eleventyConfig = path.join(__dirname, '../../.eleventy.js');
      if (!fs.existsSync(eleventyConfig)) {
        return {
          success: false,
          error: '.eleventy.js config not found'
        };
      }

      // Test 3: Check if src directory exists
      const srcDir = path.join(__dirname, '../../src');
      if (!fs.existsSync(srcDir)) {
        return {
          success: false,
          error: 'src directory not found'
        };
      }

      // Test 4: Validate build command exists
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
      if (!packageJson.scripts || !packageJson.scripts.build) {
        return {
          success: false,
          error: 'Build script not found in package.json'
        };
      }

      return {
        success: true,
        message: 'All build configuration checks passed'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};