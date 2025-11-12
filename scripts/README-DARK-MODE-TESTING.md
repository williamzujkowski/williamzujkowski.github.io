# Dark Mode Toggle Testing

Playwright-based automated testing for dark mode toggle functionality.

## Overview

This script validates:
- Dark mode toggle element exists and is clickable
- Theme changes when toggle is clicked
- Theme persists in localStorage
- Toggle works bidirectionally (light ↔ dark)
- No console errors during theme switching
- Visual differences captured in screenshots

## Requirements

**Before running:**
1. Development server MUST be running (`npm start`)
2. Server should be accessible at `http://localhost:8080`
3. Playwright dependencies installed (`npm install`)

## Usage

### Basic Test
```bash
node scripts/test-dark-mode-toggle.js
```

### Expected Output
```
🌙 Dark Mode Toggle Functionality Test

🌐 Checking server availability...
   ✅ Server is running

🧪 Running dark mode toggle tests...

  → Navigating to homepage...
  → Detecting initial theme...
     Initial theme: light (default via default)
  → Finding dark mode toggle...
     Toggle found: [aria-label*="theme"]
  → Capturing before screenshot...
  → Clicking toggle...
  → Detecting theme after toggle...
     Theme after toggle: dark (dark via html.class)
     ✅ Theme changed: light → dark
  → Capturing after screenshot...
  → Checking theme persistence...
     ✅ Theme persisted: theme=dark
  → Toggling back to original state...
     Final theme: light
     ✅ Returned to original state: light

================================================================================
🌙 DARK MODE TOGGLE VALIDATION REPORT
================================================================================

📊 STATUS: ✅ PASSED

📋 THEME TRANSITIONS:
   Initial:  light (default)
   Toggled:  dark (dark)
   Final:    light (default)

🎯 TOGGLE ELEMENT:
   Selector: [aria-label*="theme"]

💾 PERSISTENCE:
   ✅ localStorage: theme=dark

📸 SCREENSHOTS:
   Directory: screenshots/dark-mode
   Files: before-*.png, after-*.png, final-*.png

================================================================================

📄 Detailed report saved to: dark-mode-validation-report.json
```

## Output Files

### JSON Report
**Location:** `dark-mode-validation-report.json`

**Format:**
```json
{
  "timestamp": "2025-11-11T12:00:00.000Z",
  "baseUrl": "http://localhost:8080",
  "success": true,
  "errors": [],
  "warnings": [],
  "details": {
    "initialTheme": {
      "theme": "light",
      "detected": "default",
      "source": "default"
    },
    "afterToggleTheme": {
      "theme": "dark",
      "detected": "dark",
      "source": "html.class"
    },
    "finalTheme": {
      "theme": "light",
      "detected": "default",
      "source": "default"
    },
    "toggleSelector": "[aria-label*=\"theme\"]",
    "persistence": {
      "hasStorage": true,
      "key": "theme",
      "value": "dark"
    }
  }
}
```

### Screenshots
**Location:** `screenshots/dark-mode/`

**Files:**
- `before-{theme}.png` - Initial page state
- `after-{theme}.png` - State after first toggle
- `final-{theme}.png` - State after toggling back

**Purpose:** Visual regression testing, verify theme changes visible

## Exit Codes

- `0` - All tests passed
- `1` - Test failures or fatal errors

## Troubleshooting

### Error: "Cannot connect to http://localhost:8080"

**Solution:**
```bash
# Start development server
npm start

# Wait for "Server running at http://localhost:8080"
# Then run test in separate terminal
node scripts/test-dark-mode-toggle.js
```

### Error: "Dark mode toggle not found"

**Possible causes:**
1. Toggle element uses non-standard selector
2. Toggle requires user interaction first (e.g., click menu)
3. JavaScript not loaded yet

**Solution:**
```javascript
// Add custom selector to TOGGLE_SELECTORS array in script:
const TOGGLE_SELECTORS = [
  '[aria-label*="theme"]',
  '[data-theme-toggle]',
  '.theme-toggle',
  '.your-custom-selector'  // Add here
];
```

### Warning: "No localStorage persistence detected"

**Not necessarily an error.** Some implementations use:
- Cookies instead of localStorage
- Server-side session storage
- No persistence (defaults to system preference)

**To investigate:**
```javascript
// Run in browser console
Object.keys(localStorage).forEach(key => {
  console.log(`${key}: ${localStorage.getItem(key)}`);
});
```

### Warning: "Theme did not return to original state"

**Possible causes:**
1. Theme state cached incorrectly
2. Animation timing issue
3. Toggle requires multiple clicks

**Solution:** Increase wait time in script:
```javascript
// Change from 500ms to 1000ms
await page.waitForTimeout(1000);
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Dark Mode Testing

on:
  pull_request:
    paths:
      - 'src/**'
      - 'scripts/**'
  push:
    branches: [main]

jobs:
  test-dark-mode:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build site
        run: npm run build

      - name: Start dev server
        run: npm start &

      - name: Wait for server
        run: npx wait-on http://localhost:8080

      - name: Run dark mode tests
        run: node scripts/test-dark-mode-toggle.js

      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: dark-mode-screenshots
          path: screenshots/dark-mode/

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: dark-mode-report
          path: dark-mode-validation-report.json
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Only run on files that affect theme
if git diff --cached --name-only | grep -qE "(theme|dark-mode|toggle)"; then
  echo "🌙 Running dark mode tests..."

  # Check if server is running
  if ! curl -s http://localhost:8080 > /dev/null; then
    echo "⚠️  Dev server not running. Skipping dark mode tests."
    exit 0
  fi

  # Run tests
  if ! node scripts/test-dark-mode-toggle.js; then
    echo "❌ Dark mode tests failed!"
    exit 1
  fi
fi
```

## Advanced Usage

### Test Multiple Breakpoints
```javascript
// Modify script to test responsive dark mode
const BREAKPOINTS = [
  { width: 375, height: 812 },   // Mobile
  { width: 768, height: 1024 },  // Tablet
  { width: 1920, height: 1080 }  // Desktop
];

for (const viewport of BREAKPOINTS) {
  await page.setViewportSize(viewport);
  const result = await validateDarkModeToggle(page);
  // Save results per breakpoint
}
```

### Test Theme Preference Detection
```javascript
// Test prefers-color-scheme
const context = await browser.newContext({
  colorScheme: 'dark'  // or 'light'
});

// Verify page respects system preference
```

### Performance Testing
```javascript
// Measure theme switch performance
const startTime = Date.now();
await toggle.element.click();
await page.waitForTimeout(500);
const endTime = Date.now();

console.log(`Theme switch took ${endTime - startTime}ms`);
```

## Related Scripts

- `scripts/playwright-ui-ux-audit.js` - Full UI/UX audit (includes dark mode check)
- `scripts/validate-mermaid-rendering.js` - Validates diagrams render in both themes

## Maintenance

**Monthly checklist:**
- [ ] Verify toggle selectors still match DOM
- [ ] Check for new theme implementation patterns
- [ ] Update screenshots if design changes
- [ ] Review localStorage key names
- [ ] Test on latest Playwright version

**When to update:**
- Theme implementation changes
- New toggle UI introduced
- localStorage schema changes
- Accessibility improvements to toggle
- Browser compatibility issues

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [WCAG Dark Mode Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html)
- [Web.dev Dark Mode Article](https://web.dev/prefers-color-scheme/)

## Support

**Issues?** Check:
1. Server running? (`npm start`)
2. Latest dependencies? (`npm install`)
3. Playwright browsers installed? (`npx playwright install`)
4. Console errors? (Check browser DevTools)

**Still stuck?** Review `dark-mode-validation-report.json` for detailed diagnostics.
