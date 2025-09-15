/**
 * Template Tests
 * Validates Eleventy templates and layouts
 */

const fs = require('fs');
const path = require('path');

module.exports = {
  async test() {
    try {
      const srcDir = path.join(__dirname, '../../src');
      const includesDir = path.join(srcDir, '_includes');

      // Test 1: Check includes directory
      if (!fs.existsSync(includesDir)) {
        return {
          success: false,
          error: '_includes directory not found'
        };
      }

      // Test 2: Check layouts directory
      const layoutsDir = path.join(includesDir, 'layouts');
      if (!fs.existsSync(layoutsDir)) {
        return {
          success: false,
          error: 'Layouts directory not found'
        };
      }

      // Test 3: Check for base layout
      const baseLayout = path.join(layoutsDir, 'base.njk');
      if (!fs.existsSync(baseLayout)) {
        return {
          success: false,
          error: 'Base layout template not found'
        };
      }

      // Test 4: Check for post layout
      const postLayout = path.join(layoutsDir, 'post.njk');
      if (!fs.existsSync(postLayout)) {
        return {
          success: false,
          error: 'Post layout template not found'
        };
      }

      // Test 5: Check partials directory
      const partialsDir = path.join(includesDir, 'partials');
      if (!fs.existsSync(partialsDir)) {
        return {
          success: false,
          error: 'Partials directory not found'
        };
      }

      // Test 6: Check critical templates
      const criticalTemplates = ['index.njk', 'feed.njk', 'sitemap.njk'];
      for (const template of criticalTemplates) {
        const templatePath = path.join(srcDir, template);
        if (!fs.existsSync(templatePath)) {
          return {
            success: false,
            error: `Critical template ${template} not found`
          };
        }
      }

      return {
        success: true,
        message: 'All template checks passed'
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};