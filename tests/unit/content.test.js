/**
 * Content Structure Tests
 * Validates blog posts and page structure
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

module.exports = {
  async test() {
    try {
      const postsDir = path.join(__dirname, '../../src/posts');

      // Test 1: Check if posts directory exists
      if (!fs.existsSync(postsDir)) {
        return {
          success: false,
          error: 'Posts directory not found'
        };
      }

      // Test 2: Check if posts have required frontmatter
      const posts = fs.readdirSync(postsDir)
        .filter(file => file.endsWith('.md'));

      if (posts.length === 0) {
        return {
          success: false,
          error: 'No blog posts found'
        };
      }

      for (const post of posts) {
        const postPath = path.join(postsDir, post);
        const content = fs.readFileSync(postPath, 'utf8');
        const { data } = matter(content);

        // Check required frontmatter fields
        if (!data.title) {
          return {
            success: false,
            error: `Post ${post} missing title in frontmatter`
          };
        }

        if (!data.date) {
          return {
            success: false,
            error: `Post ${post} missing date in frontmatter`
          };
        }

        if (!data.description) {
          return {
            success: false,
            error: `Post ${post} missing description in frontmatter`
          };
        }
      }

      // Test 3: Check pages directory
      const pagesDir = path.join(__dirname, '../../src/pages');
      if (!fs.existsSync(pagesDir)) {
        return {
          success: false,
          error: 'Pages directory not found'
        };
      }

      return {
        success: true,
        message: `All content checks passed. Found ${posts.length} valid posts.`
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};