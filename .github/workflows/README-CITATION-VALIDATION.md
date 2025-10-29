# Citation Link Validation Workflow

## Overview

This GitHub Actions workflow automatically validates all citation links in blog posts on a weekly schedule and creates GitHub issues when broken links are detected.

## Schedule

- **Automatic Run**: Every Monday at 9:00 AM UTC
- **Manual Trigger**: Can be triggered manually via GitHub Actions UI

## What It Does

1. **Extracts Citation Links**: Scans all blog posts in `src/posts/` and identifies citation-specific links (research papers, academic sources, DOI links, arXiv papers, etc.)

2. **Validates Links**: Tests each citation link using multiple strategies:
   - HTTP HEAD/GET requests
   - Playwright browser automation (for JavaScript-rendered sites)
   - Retry logic with exponential backoff
   - Paywall detection
   - SSL certificate validation

3. **Generates Report**: Creates a detailed markdown report with:
   - Broken links grouped by blog post
   - Issue type classification (404, timeout, paywall, SSL error, etc.)
   - Suggested repair actions
   - Summary statistics

4. **Creates/Updates Issue**:
   - Creates a new GitHub issue if broken links are found
   - Updates existing issue if one already exists
   - Labels: `automated`, `citation-validation`, `maintenance`

## Components

### Workflow File
- **Location**: `.github/workflows/citation-validation.yml`
- **Permissions**: `contents:read`, `issues:write`
- **Runs on**: `ubuntu-latest`

### Scripts Used

1. **link-extractor.py** - Extracts links from markdown files
   - `--citations-only` flag filters for academic/research sources
   - Classifies links by type (citation, documentation, resource, news, etc.)

2. **link-validator.py** - Validates links using HTTP and Playwright
   - Detects paywalls, 404s, SSL errors, timeouts
   - Supports retry logic and exponential backoff
   - Handles JavaScript-rendered content

3. **citation-report.py** - Generates markdown report
   - Groups broken links by blog post
   - Includes context and suggested actions
   - Provides repair recommendations

## Testing Locally

Run the test script to simulate the workflow:

```bash
bash scripts/link-validation/test-citation-workflow.sh
```

This will:
- Extract citation links
- Validate all links
- Generate a report (if broken links found)
- Exit with code 1 if broken links detected

## Manual Trigger

1. Go to **Actions** tab in GitHub
2. Select **Citation Link Validation** workflow
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow** button

## Understanding the Report

### Issue Types

- **404** - Page not found (likely moved or deleted)
- **403** - Access forbidden (may require authentication)
- **paywall** - Content behind a subscription wall
- **timeout** - Site didn't respond in time
- **ssl_error** - SSL certificate issues
- **redirect** - URL redirects to different location

### Suggested Actions

Each broken link includes a suggested action:

- **404**: Search for updated URL or alternative source
- **Paywall**: Find open-access alternative or use Wayback Machine
- **Timeout**: Retry later or find more reliable source
- **SSL Error**: Check for valid HTTPS or find alternative
- **Redirect**: Update to final URL

## Repair Workflow

When an issue is created:

1. **Review the issue** - Check all broken links
2. **Find replacements** - Use suggested resources:
   - [Google Scholar](https://scholar.google.com/)
   - [arXiv.org](https://arxiv.org/)
   - [Zenodo](https://zenodo.org/)
   - [CORE](https://core.ac.uk/)
   - [Unpaywall](https://unpaywall.org/)
   - [Wayback Machine](https://web.archive.org/)

3. **Update blog posts** - Replace broken URLs with working alternatives
4. **Re-run validation** - Trigger workflow manually to verify fixes
5. **Close issue** - Once all links are fixed

## Artifacts

The workflow saves validation data as artifacts:
- **citation-links.json** - Extracted citation links
- **citation-validation.json** - Validation results
- **citation-report.md** - Markdown report
- **Retention**: 30 days

## Monitoring

Check workflow status:
- **Actions** tab → **Citation Link Validation**
- Green checkmark = All citations valid
- Red X = Broken links detected (check issue)

## Configuration

### Adjusting Schedule

Edit `.github/workflows/citation-validation.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC
```

Use [crontab.guru](https://crontab.guru/) for custom schedules.

### Adjusting Validation Parameters

In the workflow file, modify:

```yaml
--max-retries 3      # Number of retry attempts
--timeout 30         # Timeout in seconds
```

### Filtering Link Types

The `--citations-only` flag extracts only academic/research links. To validate all links, remove this flag.

## Troubleshooting

### No Citations Found

If the workflow reports 0 citations:
- Check that blog posts exist in `src/posts/`
- Verify citation links match expected patterns (arXiv, DOI, academic domains)
- Review `link-extractor.py` TYPE_PATTERNS

### Validation Timeouts

If many timeouts occur:
- Increase `--timeout` value
- Check if sites are temporarily down
- Consider rate limiting (may need to adjust batch processing)

### False Positives

Some sites block automated requests:
- Playwright helps with JavaScript-rendered content
- May need to manually verify suspected false positives
- Consider adding retry logic for specific domains

## Dependencies

The workflow installs:
- Python 3.11
- requests
- beautifulsoup4
- playwright
- aiohttp
- certifi

Playwright installs:
- Chromium browser

## Security

- Workflow has minimal permissions (`contents:read`, `issues:write`)
- No secrets required
- No external API keys needed
- All operations are read-only except issue creation

## Future Enhancements

Potential improvements:
- Add Slack/email notifications
- Auto-fix high-confidence replacements
- Link to Wayback Machine for archived versions
- Track link health over time
- Generate trend reports

## Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Review generated artifacts
3. Run test script locally for debugging
4. Check script documentation in `scripts/link-validation/`
