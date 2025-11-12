# Mermaid Rendering Validation Script

## Overview

`validate-mermaid-rendering.js` validates Mermaid diagram rendering across all blog posts using Playwright for automated browser testing.

## Purpose

- **Automated validation**: Test all 49 posts with Mermaid diagrams
- **Regression prevention**: Catch rendering issues after Mermaid upgrades
- **Quality assurance**: Verify diagram count matches expectations
- **Syntax detection**: Identify deprecated Mermaid v9 syntax

## Installation

```bash
# Install Playwright browsers (required first time)
npx playwright install

# Verify installation
npx playwright --version
```

## Usage

### Run via npm script (recommended):
```bash
npm run validate:mermaid
```

### Run directly:
```bash
node scripts/validate-mermaid-rendering.js
```

### Prerequisites:
- Development server must be running on `http://localhost:8080`
- Start with: `npm run serve` or `npm run watch:eleventy`

## What It Tests

### 1. Post Discovery
- Scans `src/posts/*.md` for files containing 'mermaid'
- Extracts post slugs from filenames
- Counts expected diagrams per post

### 2. Browser Validation
- Navigates to each post URL
- Waits for Mermaid rendering completion
- Validates SVG elements generated successfully

### 3. Error Detection
- **Console errors**: Mermaid.js initialization or rendering errors
- **DOM errors**: Missing SVG elements in mermaid containers
- **Syntax warnings**: Deprecated v9 syntax patterns
- **Layout issues**: Horizontal scroll from oversized diagrams

### 4. Quality Checks
- Rendered diagram count matches expected count
- No JavaScript errors during page load
- Diagrams fit within viewport boundaries

## Output

### Console Report
```
================================================================================
🔍 MERMAID RENDERING VALIDATION REPORT
================================================================================

📊 SUMMARY
   Total posts: 49
   ✅ Passed: 47 (96%)
   ❌ Failed: 2
   ⚠️  With warnings: 5

📋 DETAILED RESULTS

✅ ebpf-security-monitoring
   9/9 diagrams

✅ bitwarden-migration
   2/2 diagrams

❌ kubernetes-security
   2/3 diagrams
   Errors:
     • Diagram 3: No SVG rendered
   Warnings:
     ⚠️  Diagram count mismatch: expected 3, rendered 2

================================================================================
❌ FAILED POSTS REQUIRING ATTENTION
================================================================================

• kubernetes-security
    - Diagram 3: No SVG rendered
• network-monitoring
    - Console error: Syntax error in mermaid diagram
```

### JSON Report
Saved to `mermaid-validation-report.json`:

```json
{
  "timestamp": "2025-11-11T12:34:56.789Z",
  "totalPosts": 49,
  "passed": 47,
  "failed": 2,
  "results": [
    {
      "slug": "ebpf-security-monitoring",
      "file": "2024-11-04-ebpf-security-monitoring",
      "success": true,
      "rendered": 9,
      "expected": 9,
      "errors": [],
      "warnings": []
    }
  ]
}
```

## Exit Codes

- **0**: All posts passed validation
- **1**: One or more posts failed or fatal error occurred

## Common Issues

### Server Not Running
```
❌ Cannot connect to http://localhost:8080
   Please start the development server: npm start
```
**Fix**: Start development server in separate terminal:
```bash
npm run serve
```

### Playwright Not Installed
```
❌ Executable doesn't exist at ~/.cache/ms-playwright/...
```
**Fix**: Install Playwright browsers:
```bash
npx playwright install
```

### Diagram Count Mismatch
```
⚠️  Diagram count mismatch: expected 3, rendered 2
```
**Causes**:
- Syntax error preventing diagram rendering
- Missing closing backticks in markdown
- Mermaid v9 vs v10 syntax incompatibility

**Fix**: Check post markdown source and browser console

### Horizontal Scroll Warning
```
⚠️  Horizontal scroll detected (1400px > 1280px)
```
**Causes**:
- Diagram too wide for viewport
- Complex flowcharts with many nodes

**Fix**: Add responsive Mermaid config or simplify diagram

## Integration with CI/CD

### GitHub Actions
```yaml
- name: Validate Mermaid Rendering
  run: |
    npm install
    npx playwright install --with-deps chromium
    npm run serve &
    sleep 5
    npm run validate:mermaid
```

### Pre-deployment Check
```bash
#!/bin/bash
npm run build
npm run serve &
SERVER_PID=$!
sleep 3
npm run validate:mermaid
RESULT=$?
kill $SERVER_PID
exit $RESULT
```

## Architecture

### Key Components

1. **Post Discovery**: `findMermaidPosts()`
   - Uses `grep` for fast file scanning
   - Extracts slugs via filename parsing
   - Counts diagrams with regex

2. **Browser Automation**: `validatePost()`
   - Playwright chromium headless
   - 30-second timeout per post
   - Console message capture
   - DOM inspection for SVG elements

3. **Error Detection**: Multi-layer validation
   - Page-level JavaScript errors
   - Console error messages
   - DOM structure validation
   - Layout overflow detection

4. **Reporting**: Dual output format
   - Human-readable console table
   - Machine-parseable JSON

### Performance

- **49 posts validated in ~90 seconds**
- 2-second wait per post for rendering
- Headless browser for speed
- Parallel-ready architecture (future enhancement)

## Maintenance

### Adding New Checks

Edit `validatePost()` function:

```javascript
// Example: Check for accessibility issues
const a11yIssues = await page.evaluate(() => {
  const svgs = document.querySelectorAll('.mermaid svg');
  return Array.from(svgs).filter(svg => !svg.getAttribute('role'));
});

if (a11yIssues.length > 0) {
  warnings.push(`${a11yIssues.length} diagrams missing ARIA roles`);
}
```

### Updating Mermaid Syntax Patterns

Edit warning detection in `validatePost()`:

```javascript
// Check for v9 subgraph syntax
if (text.includes('subgraph') && !text.includes('subgraph[')) {
  warnings.push(`Mermaid v9 syntax detected: ${text}`);
}
```

## Related Scripts

- **playwright-ui-ux-audit.js**: UI/UX responsive testing
- **test-gist-rendering.py**: GitHub Gist embed validation
- **blog-content/humanization-validator.py**: Content quality scoring

## References

- [Mermaid v10 Migration Guide](https://mermaid.js.org/config/migration/v10-to-v11.html)
- [Playwright Test Documentation](https://playwright.dev/docs/intro)
- [Blog Enhancement Report](../docs/reports/phase-1-p0-completion-report.md)
