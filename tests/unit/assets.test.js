/**
 * Assets Tests
 * Validates CSS, JS, and image assets
 */

const fs = require('fs');
const path = require('path');

module.exports = {
  async test() {
    try {
      const assetsDir = path.join(__dirname, '../../src/assets');

      // Test 1: Check if assets directory exists
      if (!fs.existsSync(assetsDir)) {
        return {
          success: false,
          error: 'Assets directory not found'
        };
      }

      // Test 2: Check CSS directory
      const cssDir = path.join(assetsDir, 'css');
      if (!fs.existsSync(cssDir)) {
        return {
          success: false,
          error: 'CSS directory not found'
        };
      }

      // Test 3: Check main CSS file (source Tailwind CSS)
      const tailwindCss = path.join(cssDir, 'tailwind.css');
      if (!fs.existsSync(tailwindCss)) {
        return {
          success: false,
          error: 'Tailwind CSS source file not found'
        };
      }

      // Test 4: Check images directory structure
      const imagesDir = path.join(assetsDir, 'images');
      if (!fs.existsSync(imagesDir)) {
        return {
          success: false,
          error: 'Images directory not found'
        };
      }

      const blogImagesDir = path.join(imagesDir, 'blog');
      if (!fs.existsSync(blogImagesDir)) {
        return {
          success: false,
          error: 'Blog images directory not found'
        };
      }

      // Test 5: Check Tailwind config
      const tailwindConfig = path.join(__dirname, '../../tailwind.config.js');
      if (!fs.existsSync(tailwindConfig)) {
        return {
          success: false,
          error: 'Tailwind config not found'
        };
      }

      // Test 6: Check PostCSS config
      const postcssConfig = path.join(__dirname, '../../postcss.config.js');
      if (!fs.existsSync(postcssConfig)) {
        return {
          success: false,
          error: 'PostCSS config not found'
        };
      }

      return {
        success: true,
        message: 'All asset checks passed'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};