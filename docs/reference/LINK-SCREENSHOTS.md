# Link Screenshots for Website Links

This document explains how website screenshots are captured, stored, and displayed for the links page on this website.

## Overview

The website uses screenshots of linked websites as background images for link cards on the links page. These screenshots provide a visual preview of the linked content, making the links page more engaging and informative.

## How It Works

1. **Screenshot Generation**: Website screenshots are generated using Puppeteer, a headless Chrome browser that can navigate to URLs and capture screenshots.

2. **Storage**: Screenshots are stored as JPEG images in the `/assets/data/screenshots/` directory, with filenames based on the link's ID (a simplified version of the link name).

3. **Metadata**: References to these screenshots are stored in categorized link preview files:
   - `link-previews-{category}.json` files contain metadata about links in specific categories
   - `link-previews-index.json` contains an index of all categories with counts and filenames
   - `link-previews.json` (legacy format) contains all link metadata for backward compatibility

4. **Display**: The frontend JavaScript (`microlink-integration.js`) reads this metadata and displays the screenshots as background images for the link cards. The script intelligently loads only the necessary category data, improving performance.

## Screenshot Generation Script

The repository includes a script (`scripts/screenshots/generate-test-screenshots.js`) to manually generate screenshots for specific websites. This is useful for:

- Testing the screenshot functionality
- Generating screenshots for important links
- Populating the screenshots directory during development

### Running the Script

To generate screenshots:

```bash
# From the project root
node scripts/screenshots/generate-test-screenshots.js

# Or using the CLI utility
npm run screenshots:test
```

This will:
1. Take screenshots of predefined websites
2. Save them to `/assets/data/screenshots/`
3. Update `link-previews.json` with references to these screenshots

### Configuring the Script

To change which websites are captured, edit the `LINKS_TO_CAPTURE` array in `scripts/screenshots/generate-test-screenshots.js`:

```javascript
const LINKS_TO_CAPTURE = [
  { id: 'github', url: 'https://github.com', name: 'GitHub' },
  { id: 'centauri-dreams', url: 'https://www.centauri-dreams.org', name: 'Centauri Dreams' },
  // Add or remove links as needed
];
```

## Automated Screenshot Generation

In addition to the manual script, the site's build process includes a more comprehensive screenshot generation script (`scripts/build/build-link-previews.js`) that:

1. Reads all links from the site configuration
2. Fetches metadata for each link
3. Takes screenshots for a subset of links (based on age and newness)
4. Updates the `link-previews.json` file with this data

This script runs during the full build process, but due to its resource-intensive nature:
- It processes links in batches
- It prioritizes new links and those with the oldest screenshots
- It can be limited by GitHub Actions timeout constraints

The screenshot generation can also be run independently using the CLI utility:

```bash
# Generate screenshots for all links
npm run screenshots:all

# Update existing screenshots
npm run screenshots:update
```

## Categorized Link Preview System

The website uses a categorized link preview system that offers several advantages:

### How It Works

The system organizes link preview data into separate files by category:

1. **Category Files**: Each category has its own JSON file (e.g., `link-previews-technology_innovation.json`)
2. **Index File**: A small index file (`link-previews-index.json`) lists all categories with their counts and filenames
3. **Legacy Format**: For backward compatibility, all data is also consolidated in `link-previews.json`

### Advantages

- **Reduced Initial Payload**: Only loads the most commonly used categories immediately
- **On-Demand Loading**: Loads additional categories only when needed
- **Improved Troubleshooting**: Easier to identify and fix issues with specific categories
- **Better Performance**: Smaller, more focused files are processed faster by the browser
- **Enhanced Maintainability**: Changes to one category don't require rebuilding all link preview data

### Rebuilding the Link Preview System

If you need to recreate all categorized link preview files from the existing screenshots:

```bash
# Run the rebuild script
./scripts/rebuild-link-previews.sh
```

This script will:
1. Remove old link preview data
2. Rebuild the link previews with the new categorized system
3. Copy screenshots to the assets directory
4. Run the build process to update the site

## Troubleshooting

If screenshots are not appearing on the links page:

1. **Check the category JSON files**: Ensure the category files contain valid screenshot paths
   ```bash
   # Check the index file
   cat assets/data/link-previews-index.json
   
   # Check a specific category file
   grep "screenshot" assets/data/link-previews-technology_innovation.json | head
   ```

2. **Verify screenshot files**: Make sure the screenshot files actually exist
   ```bash
   ls -la assets/data/screenshots/
   ```

3. **Check browser console**: Look for JavaScript errors in the browser console

4. **Generate test screenshots**: Use the script to generate new screenshots
   ```bash
   npm run screenshots:test
   # Or directly with node
   node scripts/screenshots/generate-test-screenshots.js
   ```

5. **Rebuild the link preview system**: Use the rebuild script to recreate the categorized files
   ```bash
   ./scripts/rebuild-link-previews.sh
   ```

6. **Verify with test page**: Open the verification page to check if screenshots load
   ```bash
   # After starting a development server
   open http://localhost:8000/scripts/screenshots/verify-screenshots.html
   ```

## Screenshot Quality

Screenshots are captured with the following settings:
- Width: 1200px
- Height: 675px (16:9 ratio)
- JPEG format with 80% quality
- Non-fullpage (viewport only)

These settings provide a balance between quality and file size, suitable for web display.

## Adding New Screenshots

### Option 1: Manually Add Specific Screenshots

To add screenshots for specific links:

1. Edit `scripts/screenshots/generate-test-screenshots.js`
2. Add entries to the `LINKS_TO_CAPTURE` array
3. Run the script
4. Commit the generated screenshots and updated JSON file

### Option 2: Generate All Screenshots

To generate screenshots for all links in batches:

1. Use the `scripts/screenshots/generate-screenshots-batch.js` script which processes links in small batches:
   ```bash
   # Process links starting at index 0, taking 20 links
   node scripts/screenshots/generate-screenshots-batch.js 0 20
   ```

2. Or use the helper shell script to process all links in sequential batches:
   ```bash
   # Run the batch processing script
   ./scripts/screenshots/run-screenshot-batches.sh
   ```

The batch processing tools will:
- Skip domains known to block screenshots
- Process links in small batches to avoid memory issues
- Save progress after each batch in case the process is interrupted
- Provide a summary of successful and failed screenshots

### Option 3: Use the Screenshot CLI (Recommended)

For the fastest and most efficient screenshot generation, use the screenshot CLI utility:

```bash
# Show help and options
./scripts/screenshots/screenshots.sh

# Generate screenshots for all links without screenshots
./scripts/screenshots/screenshots.sh all
# Or with npm script
npm run screenshots:all

# Update all existing screenshots
./scripts/screenshots/screenshots.sh update
# Or with npm script
npm run screenshots:update

# Process specific batch of links
./scripts/screenshots/screenshots.sh batch 50 10
```

The fast screenshot generator includes many optimizations:

- **Parallel Processing**: Captures multiple screenshots simultaneously
- **Caching**: Reuses screenshots to avoid redoing work
- **Resource Blocking**: Blocks unnecessary fonts, media, and websockets
- **Optimized Browser Settings**: Reduces memory usage and improves performance
- **Adaptive Concurrency**: Uses available CPU cores efficiently
- **Faster Page Loading**: Uses 'domcontentloaded' event instead of waiting for all resources

Performance comparison:
- Standard script: ~5-10 seconds per screenshot
- Fast generator: ~1-3 seconds per screenshot with concurrent processing