# Search Functionality Testing

**Created:** 2025-11-14
**Script:** `scripts/test-search-functionality.js`
**npm command:** `npm run test:search`
**Purpose:** Automated testing of search functionality, input accessibility, result quality, and error detection

---

## Quick Start

```bash
# Start local server (required)
npm run serve

# In another terminal, run search tests
npm run test:search
```

## What It Tests

### 1. **Search Input Accessibility** ✅
- Verifies search input exists and is accessible
- Checks for proper ARIA labels and roles
- Validates keyboard accessibility
- Ensures proper input type (`type="search"` or `role="searchbox"`)

### 2. **Search Query Functionality** 🔍
Tests multiple query scenarios:
- **Common term search** ("security") - Should find 5+ results
- **Uppercase search** ("AI") - Should find 3+ results
- **Non-existent term** ("xyzabc123nonexistent") - Should show no results
- **Multi-word search** ("homelab security") - Should find 1+ results

### 3. **Search Result Quality** 📊
Analyzes first 3 results to ensure:
- Each result has a title (h3, h4, or .title)
- Each result has a clickable link
- Each result has an excerpt/description
- Content is properly structured

### 4. **Console Error Detection** ⚠️
Monitors for:
- JavaScript errors during search
- Page errors and exceptions
- Console warnings related to search functionality

---

## Test Output

### Console Output

```
🔍 Search Functionality Test Suite

==================================================

📍 Navigating to search page...

🔍 Test 1: Search Input Accessibility
  ✅ Search input is accessible

🔍 Test 2: Search Queries
  → Testing query: "security" (Common topic search)
     ✅ "security": 12 results
  → Testing query: "AI" (Uppercase search)
     ✅ "AI": 8 results
  → Testing query: "xyzabc123nonexistent" (Non-existent term)
     ✅ "xyzabc123nonexistent": 0 results
  → Testing query: "homelab security" (Multi-word search)
     ✅ "homelab security": 4 results

🔍 Test 3: Search Result Quality
  ✅ Search results have good quality

🔍 Test 4: Console Errors
  ✅ No console errors detected

==================================================

📊 Test Summary: 7/7 passed
   ✅ All tests passed!

📄 Report saved: docs/reports/search-functionality-report.json
📸 Screenshots saved: screenshots/search
```

### Generated Files

1. **JSON Report:** `docs/reports/search-functionality-report.json`
   ```json
   {
     "timestamp": "2025-11-14T23:45:00.000Z",
     "tests": {
       "accessibility": {
         "passed": true,
         "issues": [],
         "details": {
           "hasLabel": true,
           "hasRole": true,
           "ariaLabel": "Search posts",
           "placeholder": "Search..."
         }
       },
       "queries": [
         {
           "query": "security",
           "description": "Common topic search",
           "passed": true,
           "resultCount": 12,
           "errors": []
         }
       ],
       "quality": {
         "passed": true,
         "issues": [],
         "samples": [...]
       },
       "consoleErrors": {
         "count": 0,
         "errors": [],
         "passed": true
       }
     },
     "summary": {
       "total": 7,
       "passed": 7,
       "failed": 0
     }
   }
   ```

2. **Screenshots:** `screenshots/search/`
   - `search-security.png` - Common term results
   - `search-AI.png` - Uppercase search results
   - `search-xyzabc123nonexistent.png` - No results state
   - `search-homelab-security.png` - Multi-word results

---

## Configuration

### Search Selectors

The script searches for common search input patterns:

```javascript
const SEARCH_SELECTORS = {
  input: [
    'input[type="search"]',
    'input[name="search"]',
    'input[placeholder*="search" i]',
    '#search',
    '.search-input',
    '[role="searchbox"]'
  ],
  results: [
    '.search-results',
    '#search-results',
    '[role="region"][aria-label*="search" i]'
  ],
  resultItems: [
    '.search-result',
    '.result-item',
    '[data-search-result]'
  ]
};
```

### Test Queries

Customize test queries in `TEST_QUERIES`:

```javascript
const TEST_QUERIES = [
  {
    query: 'security',
    shouldFindResults: true,
    minResults: 5,
    description: 'Common topic search'
  },
  // Add more test cases...
];
```

### Timeouts

- **Page load timeout:** 10,000ms (10 seconds)
- **Search debounce wait:** 500ms
- **Page stabilization:** 1,000ms

---

## Troubleshooting

### Test Failures

#### "Search input not found"
- Verify search component is visible on `/posts/` page
- Check if selectors match your search input
- Ensure local server is running

#### "No results found for query"
- Verify search index is built
- Check if search functionality is working manually
- Ensure expected content exists in posts

#### "Console errors detected"
- Review console errors in report
- Fix JavaScript errors in search implementation
- Check for missing dependencies

### Running with Debug

```bash
# Enable Playwright debug logging
DEBUG=pw:api npm run test:search

# Run with visible browser (non-headless)
# Edit scripts/test-search-functionality.js:
# Change: headless: true → headless: false
```

---

## Integration

### CI/CD Integration

Add to GitHub Actions workflow:

```yaml
- name: Test Search Functionality
  run: |
    npm run serve &
    sleep 5
    npm run test:search
```

### Pre-deployment Checklist

Run before deploying:

```bash
npm run build
npm run serve &
sleep 5
npm run validate:mermaid
npm run test:darkmode
npm run test:search
```

---

## Maintenance

### Adding New Test Cases

1. Edit `scripts/test-search-functionality.js`
2. Add new query to `TEST_QUERIES` array:
   ```javascript
   {
     query: 'your-search-term',
     shouldFindResults: true,
     minResults: 2,
     description: 'Description of test case'
   }
   ```
3. Run tests to verify

### Updating Selectors

If search HTML structure changes:

1. Identify new selectors
2. Add to `SEARCH_SELECTORS` object
3. Prioritize selectors (most specific first)
4. Test with `npm run test:search`

---

## Related Documentation

- [Mermaid Validation](./README-MERMAID-VALIDATION.md) - Diagram rendering tests
- [Dark Mode Testing](./README-DARK-MODE-TESTING.md) - Theme toggle tests
- [UI/UX Audit](./playwright-ui-ux-audit.js) - Responsive design tests

---

## Version History

- **v1.0.0** (2025-11-14) - Initial implementation
  - Search input accessibility testing
  - Query functionality tests (4 scenarios)
  - Result quality validation
  - Console error monitoring
  - JSON report generation
  - Screenshot capture

---

**For issues or questions, see:** [TODO.md](../TODO.md) Task #12
