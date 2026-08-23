# Link Validation and Repair System

## Overview

Comprehensive link validation infrastructure for maintaining citation quality and preventing link rot across all blog posts.

## System Components

### Core Scripts

1. **link-extractor.py**
   - Extracts all links from markdown files with context
   - Categorizes links (citations, inline, documentation, etc.)
   - Preserves surrounding text for relevance checking

2. **link-validator.py**
   - Validates links using HTTP and optional Playwright
   - Detects paywalls, redirects, SSL issues
   - Implements retry logic with exponential backoff

3. **simple-validator.py**
   - Lightweight HTTP-only validation (no Playwright dependency)
   - Fast batch validation with concurrent requests
   - Basic status checking for quick scans

4. **citation-repair.py**
   - Finds replacements for broken academic citations
   - Searches arXiv, CrossRef, Semantic Scholar
   - Wayback Machine integration for archived content
   - DOI resolution and open access alternatives

5. **citation-report.py**
   - Generates citation validation reports for GitHub Actions
   - Combines validation results with extracted citation metadata
   - Produces markdown summaries for CI output

6. **link-report-generator.py**
   - Generates comprehensive reports in multiple formats
   - Creates action plans for fixes
   - Produces manual review queues

7. **batch-link-fixer.py**
   - Orchestrates entire validation pipeline
   - Applies repairs based on confidence thresholds
   - Creates backups before modifications

## Quick Start

Current post count: **92**.

### 1. Extract Links
```bash
python scripts/link-validation/link-extractor.py \
  --posts-dir src/posts \
  --output links.json
```

### 2. Validate Links
```bash
# Simple validation (no Playwright)
python scripts/link-validation/simple-validator.py \
  --links links.json \
  --output validation.json

# Full validation (requires Playwright)
pip install playwright
playwright install chromium
python scripts/link-validation/link-validator.py \
  --input links.json \
  --output validation.json
```

### 3. Find Repairs
```bash
echo '{"results": []}' > relevance.json  # Placeholder if no relevance check
python scripts/link-validation/citation-repair.py \
  --links links.json \
  --validation validation.json \
  --relevance relevance.json \
  --output repairs.json
```

### 4. Generate Reports
```bash
python scripts/link-validation/link-report-generator.py \
  --links links.json \
  --validation validation.json \
  --relevance relevance.json \
  --repairs repairs.json \
  --output-dir reports
```

### 5. Apply Fixes
```bash
# Dry run to see changes
python scripts/link-validation/batch-link-fixer.py \
  --repairs repairs.json \
  --confidence-threshold 90 \
  --dry-run

# Apply high-confidence fixes
python scripts/link-validation/batch-link-fixer.py \
  --repairs repairs.json \
  --confidence-threshold 90 \
  --apply \
  --posts-dir src/posts
```

## Full Pipeline

Run the complete validation and repair pipeline:

```bash
# One command to rule them all
python scripts/link-validation/batch-link-fixer.py \
  --posts-dir src/posts \
  --confidence-threshold 90
```

## Continuous Monitoring

### GitHub Actions
The `.github/workflows/link-monitor.yml` workflow:
- Runs daily link health checks
- Validates links on pull requests
- Auto-fixes high-confidence repairs
- Creates issues for critical problems

### Local Check
```bash
# Extract and validate current links
python scripts/link-validation/link-extractor.py \
  --posts-dir src/posts \
  --output links.json

python scripts/link-validation/simple-validator.py \
  --links links.json \
  --output validation.json

python scripts/link-validation/citation-report.py \
  --input validation.json \
  --links links.json \
  --output citation-report.md
```

## Configuration

### Confidence Thresholds
- **95%+**: Automatic fix (exact replacements)
- **90-94%**: High confidence (manual review recommended)
- **70-89%**: Medium confidence (requires review)
- **<70%**: Low confidence (manual intervention required)

### Repair Sources (Priority Order)
1. Direct URL updates (HTTPS upgrades, www additions)
2. arXiv version updates
3. DOI resolution
4. CrossRef metadata
5. Semantic Scholar
6. Wayback Machine
7. Academic search engines

### Domain Reliability Scores
- **95**: arXiv, DOI, PubMed, NIST, OWASP
- **90**: IEEE, ACM, Nature, official docs
- **85**: GitHub, GitLab
- **80**: StackOverflow
- **75**: Wikipedia
- **60-70**: Medium, Dev.to
- **50**: Unknown domains

## Manual Review Process

### Review Queue
After running validation, check the manual review queue:
```bash
cat reports/manual_review.md
```

### Priority Levels
- **Critical**: Broken academic citations, security resources
- **High**: Outdated documentation, moved repositories
- **Medium**: Redirected links, slow responses
- **Low**: Social media links, news articles

### Applying Manual Fixes
1. Review suggested replacements
2. Verify content relevance
3. Update links in source files
4. Re-run validation

## Archiving Strategy

### Critical Links to Archive
- Academic papers (arXiv, DOI)
- Security advisories (NIST, OWASP, CVE)
- Official documentation
- GitHub repositories
- Important blog posts

### Archive Handling

There is no standalone local archiver script. Run repair discovery to find archived alternatives for broken citations:

```bash
python scripts/link-validation/citation-repair.py \
  --links links.json \
  --validation validation.json \
  --output repairs.json
```

## Statistics

Deliberately not reproduced here. This section used to carry an undated
snapshot labelled "Latest Run" claiming 40.8% of links were broken, in a
repo that validates links nightly — a number with no date is worse than no
number. Current figures are in the `link-validation-reports` artifact of the
most recent `link-monitor.yml` run.


## Best Practices

### For New Posts
1. Validate links before publishing
2. Use DOI links for academic papers
3. Archive important links immediately
4. Prefer official documentation over blogs

### For Existing Posts
1. Run monthly validation checks
2. Apply high-confidence fixes automatically
3. Review medium-confidence suggestions
4. Update outdated documentation links

### Citation Guidelines
- Always use permanent identifiers (DOI, arXiv ID)
- Include publication year in citation text
- Link to open access versions when available
- Archive critical citations to Wayback Machine

## Troubleshooting

### Playwright Issues
```bash
# Install Playwright
pip install playwright
playwright install chromium

# If still failing, use simple validator
python scripts/link-validation/simple-validator.py
```

### Rate Limiting
- Add delays between requests
- Use smaller batch sizes
- Implement exponential backoff

### False Positives
- Check domain-specific validation rules
- Verify SSL certificates
- Test with curl/wget manually

## Future Enhancements

- [ ] Machine learning for better repair suggestions
- [ ] Integration with citation databases
- [ ] Real-time validation in editor
- [ ] Browser extension for link checking
- [ ] API for third-party integrations
- [ ] Dashboard for link health metrics

## Dependencies

```bash
pip install aiohttp asyncio pathlib dataclasses
# Optional for advanced features:
pip install playwright scikit-learn numpy
```

## License

Part of the williamzujkowski.github.io project.

---

For issues or suggestions, please open a GitHub issue.
