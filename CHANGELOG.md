# Changelog

## [1.2.0] - 2025-05-17

### Added

- Comprehensive testing framework
  - Added Jest configuration for unit and integration tests
  - Implemented Playwright for end-to-end tests
  - Added visual regression testing
  - Created test configuration centralization
  - Implemented code coverage reporting
- Advanced performance optimizations
  - Implemented critical CSS extraction and inlining
  - Added enhanced JavaScript bundling with code splitting
  - Created script loading prioritization system
  - Added service worker for offline support and caching
  - Implemented adaptive resource loading based on network conditions

### Changed

- Improved JavaScript organization
  - Optimized Rollup configuration with better code splitting
  - Added priority-based script loading
  - Implemented module/nomodule pattern for modern/legacy browsers
- Enhanced image optimization
  - Added AVIF format support
  - Implemented content-visibility optimization
  - Created blur-up placeholder system
  - Added fetch priority signals for critical images
- Updated documentation
  - Added comprehensive Performance Optimization Guide
  - Created detailed Testing Guide
  - Updated README with new features and improvements

### Fixed

- Resolved JavaScript file duplication between src/js and js directories
- Fixed inefficient resource loading patterns
- Improved page load performance by optimizing critical rendering path
- Enhanced mobile performance with better resource prioritization

## [1.1.1] - 2025-04-13

### Added

- Enhanced folder structure documentation
- Updated configuration file references in documentation
- Added comprehensive blog post processing workflow and directory structure documentation

### Changed

- Updated PostCSS config to correctly reference Tailwind config at `./config/tailwind.config.cjs`
- Updated CSS build scripts to explicitly use config from config directory
- Enhanced the root `.eleventy.simple.cjs` file with proper icon file paths for GitHub Actions builds

### Fixed

- Verified that all configuration files work correctly with updated paths
- Confirmed that the site builds successfully with the reorganized structure

## [1.1.0] - 2025-04-05

### Added

- JSON caching for GitHub-style visualizations
  - Created build-visualizations.js for pre-generating visualization data
  - Added cache/\_data directory for storing pre-computed visualization data
  - Pre-generates heatmap data with cells grouped by intensity
  - Pre-generates activity timeline data grouped by month
- Configuration-based pinned repositories system
  - Added pinned_repositories array to site.json configuration
  - Updated build-github-pins.js to use configuration if available
  - Fallback to GitHub API when configuration is not available

### Changed

- Modified index.njk to use cached visualization data
  - Updated heatmap rendering to use pre-generated cell data
  - Updated activity feed to use cached month/post groupings
  - Added fallback visualizations when cached data isn't available
- Updated eleventy config to load cached visualization data
- Added build:viz script to package.json build pipeline
- Changed pinned repositories to use site configuration instead of GitHub API

### Fixed

- Resolved rendering issues with the activity timeline and contribution graph
- Improved site performance by moving visualization computations to build time
- Fixed GitHub API rate limit issues by using configuration-based repositories

## [1.0.9] - 2025-04-13

### Added

- Removed unused link preview content and code (400+ files)
- Simplified build process by removing link preview generation
- Reduced repository size significantly
- Enhanced blog post topic diversity features:
  - Updated blogpost.prompt for topic diversity
  - Added topic diversity analysis template
  - Implemented checks to prevent topic repetition
  - Added metadata guidelines for unique titles

### Fixed

- GitHub Actions build reliability:
  - Added missing filters and shortcodes to root `.eleventy.simple.cjs`
  - Updated GitHub Actions workflow to use correct script paths
  - Created dedicated fallback data script

### Changed

- Updated dependencies for security and compatibility:
  - Downgraded packages for Node.js 18 compatibility
  - Enhanced data generation with graceful fallbacks

## [1.0.8] - 2025-04-05

### Added

- Post processing automation script (tools/process-new-posts.js)
  - Automated blog post conversion for .txt/.md files
  - Intelligent title extraction
  - Content-based tag suggestion
  - Image selection based on content keywords
  - Automated post date spacing

### Changed

- Enhanced blog post formatting
  - Improved markdown structure
  - Added code samples with syntax highlighting
  - Created ASCII diagrams for technical concepts
  - Standardized frontmatter across all posts

### Fixed

- Created simplified Eleventy configuration for GitHub Actions
- Fixed layout path issues for continuous integration
- Added proper handling of assets and static files
