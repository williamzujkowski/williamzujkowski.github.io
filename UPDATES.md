# Recent Updates

## April 6, 2025 - Folder Structure Reorganization and Path Consistency

1. **Fixed Configuration Paths**
   - Updated PostCSS config to correctly reference Tailwind config at `./config/tailwind.config.cjs`
   - Updated CSS build scripts to explicitly use config from config directory with `--config=config/postcss.config.cjs`
   - Enhanced the root `.eleventy.simple.cjs` file with proper icon file paths for GitHub Actions builds

2. **Updated Documentation**
   - Enhanced CLAUDE.md with detailed directory structure information
   - Added comprehensive configuration file references
   - Documented the blog post processing workflow and directory structure
   - Added references to utility scripts and their locations

3. **Verified Asset Organization**
   - Confirmed icons are properly organized in assets/icons directory
   - Ensured build scripts reference correct asset paths

4. **Tested Complete Build Process**
   - Verified that all configuration files work correctly with updated paths
   - Confirmed that the site builds successfully with the reorganized structure

## April 5, 2025 - Blog Workflow Automation

1. **Post Processing Script**
   - Created tools/process-new-posts.js to automate blog post conversion
   - Added support for both text (.txt) and markdown (.md) files
   - Implemented intelligent title extraction
   - Added content-based tag suggestion
   - Built image selection based on content keywords
   - Automated post date spacing (10-14 days between posts)

2. **Comprehensive Documentation**
   - Created BLOG-WORKFLOW.md with detailed instructions
   - Added BLOG-POST-README.md with system overview
   - Updated main README.md with new features
   - Added MAINTENANCE.md with comprehensive maintenance guide

3. **Enhanced Formatting**
   - Improved markdown structure in processed posts
   - Added code samples with syntax highlighting
   - Created ASCII diagrams for technical concepts
   - Standardized frontmatter across all posts

4. **Build Improvements**
   - Created simplified Eleventy configuration for GitHub Actions
   - Fixed layout path issues for continuous integration
   - Added proper handling of assets and static files