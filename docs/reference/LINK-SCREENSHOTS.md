# Link Screenshots for Website Links

This document explains how website screenshots are captured, stored, and displayed for the links page on this website.

## Overview

The website uses screenshots of linked websites as background images for link cards on the links page. These screenshots provide a visual preview of the linked content, making the links page more engaging and informative.

## How It Works

1. **Screenshot Generation**: Website screenshots are generated using Puppeteer, a headless Chrome browser that can navigate to URLs and capture screenshots.

2. **Storage**: Screenshots are stored as JPEG images in the `/assets/data/screenshots/` directory, with filenames based on the link's ID (a simplified version of the link name).

3. **Metadata**: References to these screenshots are stored in the `link-previews.json` file, which contains metadata about each link, including the screenshot path.

4. **Display**: The frontend JavaScript (`microlink-integration.js`) reads this metadata and displays the screenshots as background images for the link cards.

## Screenshot Generation Script

The repository includes a script (`tools/generate-test-screenshots.js`) to manually generate screenshots for specific websites. This is useful for:

- Testing the screenshot functionality
- Generating screenshots for important links
- Populating the screenshots directory during development

### Running the Script

To generate screenshots:

```bash
# From the project root
node tools/generate-test-screenshots.js
```

This will:
1. Take screenshots of predefined websites
2. Save them to `/assets/data/screenshots/`
3. Update `link-previews.json` with references to these screenshots

### Configuring the Script

To change which websites are captured, edit the `LINKS_TO_CAPTURE` array in `tools/generate-test-screenshots.js`:

```javascript
const LINKS_TO_CAPTURE = [
  { id: 'github', url: 'https://github.com', name: 'GitHub' },
  { id: 'centauri-dreams', url: 'https://www.centauri-dreams.org', name: 'Centauri Dreams' },
  // Add or remove links as needed
];
```

## Automated Screenshot Generation

In addition to the manual script, the site's build process includes a more comprehensive screenshot generation script (`scripts/build-link-previews.js`) that:

1. Reads all links from the site configuration
2. Fetches metadata for each link
3. Takes screenshots for a subset of links (based on age and newness)
4. Updates the `link-previews.json` file with this data

This script runs during the full build process, but due to its resource-intensive nature:
- It processes links in batches
- It prioritizes new links and those with the oldest screenshots
- It can be limited by GitHub Actions timeout constraints

## Troubleshooting

If screenshots are not appearing on the links page:

1. **Check the JSON file**: Ensure `link-previews.json` contains valid screenshot paths
   ```bash
   grep "screenshot" assets/data/link-previews.json | head
   ```

2. **Verify screenshot files**: Make sure the screenshot files actually exist
   ```bash
   ls -la assets/data/screenshots/
   ```

3. **Check browser console**: Look for JavaScript errors in the browser console

4. **Generate test screenshots**: Use the script to generate new screenshots
   ```bash
   node tools/generate-test-screenshots.js
   ```

5. **Verify with test page**: Open the verification page to check if screenshots load
   ```bash
   # After starting a development server
   open http://localhost:8000/tools/verify-screenshots.html
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

1. Edit `tools/generate-test-screenshots.js`
2. Add entries to the `LINKS_TO_CAPTURE` array
3. Run the script
4. Commit the generated screenshots and updated JSON file

### Option 2: Generate All Screenshots

To generate screenshots for all links in batches:

1. Use the `tools/generate-screenshots-batch.js` script which processes links in small batches:
   ```bash
   # Process links starting at index 0, taking 20 links
   node tools/generate-screenshots-batch.js 0 20
   ```

2. Or use the helper shell script to process all links in sequential batches:
   ```bash
   # Run the batch processing script
   ./tools/run-screenshot-batches.sh
   ```

The batch processing tools will:
- Skip domains known to block screenshots
- Process links in small batches to avoid memory issues
- Save progress after each batch in case the process is interrupted
- Provide a summary of successful and failed screenshots