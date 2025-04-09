# Changelog

## [1.1.0] - 2025-04-05
### Added
- JSON caching for GitHub-style visualizations
  - Created build-visualizations.js for pre-generating visualization data
  - Added cache/_data directory for storing pre-computed visualization data
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
