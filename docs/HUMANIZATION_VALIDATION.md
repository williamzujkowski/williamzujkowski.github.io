# Humanization Validation Tools

**Version:** 1.0.0
**Created:** 2025-10-28
**Purpose:** Automated validation of blog posts to ensure human tone and authentic voice

---

## Overview

Three integrated tools for detecting AI-generated content tells and enforcing humanization requirements:

1. **humanization-patterns.yaml** - Pattern definitions and scoring rules
2. **humanization-validator.py** - Standalone human tone validation
3. **full-post-validation.py** - Comprehensive pre-publish validation

## Quick Start

```bash
# Single post humanization check
python scripts/blog-content/humanization-validator.py --post src/posts/example.md

# Comprehensive validation (all checks)
python scripts/blog-content/full-post-validation.py --post src/posts/example.md

# Strict mode (fail on any violation)
python scripts/blog-content/humanization-validator.py --post src/posts/example.md --strict

# JSON output for CI/CD
python scripts/blog-content/full-post-validation.py --post src/posts/example.md --output json
```

---

## Tool 1: humanization-patterns.yaml

**Location:** `/home/william/git/williamzujkowski.github.io/scripts/blog-content/humanization-patterns.yaml`

### Purpose
Configuration file defining:
- Banned tokens (AI-tells)
- Required patterns (humanization elements)
- Sentiment analysis thresholds
- Scoring weights

### Key Sections

#### Banned Tokens
1. **Punctuation**
   - Em dashes (—) - severity: high
   - Semicolons (;) in narrative - severity: medium

2. **Transitions**
   - "in conclusion" - severity: high
   - "overall" - severity: medium
   - "in summary" - severity: high

3. **Jargon**
   - "leverage" → use "use" or "take advantage of"
   - "utilize" → use "use"
   - "facilitate" → use "help" or "enable"

4. **Hype Words**
   - "exciting", "remarkable", "amazing"
   - "revolutionary", "game-changing"
   - "cutting-edge", "seamless"

#### Required Patterns
1. **First Person** (min: 1)
   - "I tested", "I tried", "I found"
   - "my homelab", "my setup"

2. **Uncertainty** (min: 1)
   - "probably", "likely", "might"
   - "depends on", "your mileage may vary"

3. **Specificity** (min: 1)
   - Version numbers (1.2.3)
   - Dates (2025-01-15)
   - Quantitative specs (16GB, 100ms)

4. **Trade-offs** (min: 1)
   - "trade-off", "downside", "limitation"
   - "but", "however", "on the other hand"

5. **Concrete Details** (min: 2)
   - Code blocks
   - "why it matters", "here's how"
   - "for example", "in practice"

#### Sentiment Analysis
- **Threshold:** 1.2 (mean sentiment score)
- **Formula:** (positive_words - negative_words) / paragraphs
- **Scale:** -2 (very negative) to +2 (very positive)

#### Scoring
- Banned token penalty: -5 per occurrence
- Missing required pattern: -10 per type
- Overly positive sentiment: -15
- Max score: 100
- Passing score: 70

### Customization

Edit `humanization-patterns.yaml` to:
- Add new banned tokens
- Adjust severity levels
- Modify required pattern thresholds
- Change scoring weights

```yaml
# Example: Add new banned token
banned_tokens:
  jargon:
    - word: "synergy"
      severity: "high"
      message: "Corporate buzzword. Be specific."
      suggested_replacements: ["collaboration", "combined effect"]
```

---

## Tool 2: humanization-validator.py

**Location:** `/home/william/git/williamzujkowski.github.io/scripts/blog-content/humanization-validator.py`
**Lines of Code:** ~450

### Purpose
Standalone tool for validating blog posts against humanization requirements.

### Usage

```bash
# Basic validation
python scripts/blog-content/humanization-validator.py --post src/posts/example.md

# Custom config file
python scripts/blog-content/humanization-validator.py \
  --post src/posts/example.md \
  --config custom-patterns.yaml

# JSON output (for automation)
python scripts/blog-content/humanization-validator.py \
  --post src/posts/example.md \
  --output json

# Strict mode (fail on any violation)
python scripts/blog-content/humanization-validator.py \
  --post src/posts/example.md \
  --strict

# Custom minimum score
python scripts/blog-content/humanization-validator.py \
  --post src/posts/example.md \
  --min-score 80
```

### Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--post` | str | (required) | Path to blog post markdown file |
| `--config` | str | humanization-patterns.yaml | Path to patterns config |
| `--output` | choice | text | Output format: text, json |
| `--strict` | flag | False | Fail on any violation |
| `--min-score` | int | 70 | Minimum passing score (0-100) |

### Output

#### Text Format (Default)
```
============================================================
HUMANIZATION VALIDATION REPORT
============================================================

Post: src/posts/example.md
Score: 75/100 - PASS

VIOLATIONS (2)
  [HIGH] banned_token
    Em dashes are AI-tells. Use commas or split into two sentences.
    Found: 3 occurrence(s)

  [HIGH] missing_required_pattern
    Include specific timestamps, versions, or measurements from your testing.

WARNINGS (1)
  [MEDIUM] jargon
    Corporate buzzword. Just say 'use'.
    Found: 2 occurrence(s)
    Suggestions: use

PASSED CHECKS (5)
  ✓ first_person
    Found: 3 (required: 1)

  ✓ uncertainty
    Found: 2 (required: 1)

  ✓ trade_offs
    Found: 5 (required: 1)

  ✓ sentiment_balance
    Sentiment score: 0.8 (threshold: 1.2)

  ✓ sentence_variety
    Short sentences: 12, Avg length: 18.5
```

#### JSON Format
```json
{
  "score": 75,
  "violations": [
    {
      "type": "banned_token",
      "severity": "high",
      "token": "—",
      "count": 3,
      "message": "Em dashes are AI-tells..."
    }
  ],
  "warnings": [],
  "passed_checks": [
    {
      "type": "first_person",
      "found": 3,
      "required": 1
    }
  ],
  "post_path": "src/posts/example.md"
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Pass - meets requirements |
| 1 | Fail - below minimum score or violations in strict mode |
| 2 | Error - file not found or invalid arguments |

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Validate Humanization
  run: |
    python scripts/blog-content/humanization-validator.py \
      --post ${{ env.POST_PATH }} \
      --min-score 70 \
      --output json > validation-report.json
  continue-on-error: false
```

---

## Tool 3: full-post-validation.py

**Location:** `/home/william/git/williamzujkowski.github.io/scripts/blog-content/full-post-validation.py`
**Lines of Code:** ~550

### Purpose
Comprehensive pre-publish validation combining:
- Humanization checks (30% weight)
- Citation coverage (25% weight)
- Content quality (20% weight)
- Metadata completeness (15% weight)
- Accessibility (10% weight)

### Usage

```bash
# Basic validation
python scripts/blog-content/full-post-validation.py --post src/posts/example.md

# Custom thresholds
python scripts/blog-content/full-post-validation.py \
  --post src/posts/example.md \
  --min-human-score 80 \
  --min-citation-coverage 0.95

# Markdown report
python scripts/blog-content/full-post-validation.py \
  --post src/posts/example.md \
  --output markdown \
  --report-file validation-report.md

# Strict mode
python scripts/blog-content/full-post-validation.py \
  --post src/posts/example.md \
  --strict
```

### Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--post` | str | (required) | Path to blog post markdown file |
| `--min-human-score` | int | 70 | Minimum humanization score |
| `--min-citation-coverage` | float | 0.9 | Minimum citation coverage (0.0-1.0) |
| `--strict` | flag | False | Fail on any violation |
| `--output` | choice | text | Output format: text, json, markdown |
| `--report-file` | str | None | Save report to file |

### Validation Checks

#### 1. Humanization (30% weight)
- AI-tells detection
- Required patterns verification
- Sentiment analysis
- Sentence/paragraph structure

#### 2. Citations (25% weight)
- Claim detection
- Citation coverage percentage
- Link validation
- Academic source requirements

#### 3. Content Quality (20% weight)
- Bullet points (min 2 lists)
- Weak language detection
- Passive voice analysis
- Paragraph length limits
- Subheading structure (min 3)

#### 4. Metadata (15% weight)
- Required fields: title, date, description, tags, author
- Description length (150-160 chars)
- Tag count (4-8 tags)
- Image metadata presence

#### 5. Accessibility (10% weight)
- Alt text on images
- Heading hierarchy (H1 → H2 → H3)
- Code block language specification
- Screen reader compatibility

### Output

#### Text Format
```
======================================================================
COMPREHENSIVE BLOG POST VALIDATION
======================================================================

Post: src/posts/example.md
Overall Score: 82.0/100 - PASS
Validated: 2025-10-28T12:00:00

SCORECARD
----------------------------------------------------------------------
Humanization          70.0/100 [PASS]
Citations            100.0/100 [PASS]
Content Quality       90.0/100 [PASS]
Metadata              60.0/100 [FAIL]
Accessibility         90.0/100 [PASS]
----------------------------------------------------------------------

HUMANIZATION
  ✗ Em dashes are AI-tells. Use commas or split into two sentences.
  ✗ Semicolons in narrative text are overly formal.

METADATA
  ✗ Missing required field: author
  ✗ Tag count 3. Should have 4-8 tags.
```

#### Markdown Report Format
```markdown
# Blog Post Validation Report

**Post:** src/posts/example.md
**Validated:** 2025-10-28T12:00:00
**Overall Score:** 82.0/100 - **PASS**

## Scorecard

| Check | Score | Status |
|-------|-------|--------|
| Humanization | 70/100 | ✅ PASS |
| Citations | 100/100 | ✅ PASS |
| Content Quality | 90/100 | ✅ PASS |
| Metadata | 60/100 | ❌ FAIL |
| Accessibility | 90/100 | ✅ PASS |

## Violations

### Humanization
- ❌ Em dashes are AI-tells...
```

---

## Workflow Integration

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Find staged markdown files
STAGED_MD=$(git diff --cached --name-only --diff-filter=ACM | grep "^src/posts/.*\.md$")

if [ -n "$STAGED_MD" ]; then
  echo "Validating blog posts..."
  for file in $STAGED_MD; do
    python scripts/blog-content/full-post-validation.py \
      --post "$file" \
      --min-human-score 70 \
      --output text

    if [ $? -ne 0 ]; then
      echo "❌ Validation failed for $file"
      exit 1
    fi
  done
  echo "✅ All posts passed validation"
fi
```

### GitHub Actions

```yaml
name: Blog Post Validation

on:
  pull_request:
    paths:
      - 'src/posts/**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install pyyaml python-frontmatter

      - name: Validate new/modified posts
        run: |
          for file in $(git diff --name-only origin/main...HEAD | grep "^src/posts/.*\.md$"); do
            python scripts/blog-content/full-post-validation.py \
              --post "$file" \
              --output json > "validation-${file//\//-}.json"
          done

      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: validation-reports
          path: validation-*.json
```

---

## Best Practices

### For Writers

1. **Run validation early and often**
   ```bash
   # Quick check while writing
   python scripts/blog-content/humanization-validator.py --post draft.md
   ```

2. **Address high-severity violations first**
   - Em dashes, semicolons, AI transitions
   - Missing required patterns (first-person, specificity)

3. **Don't over-optimize**
   - 70+ score is acceptable
   - Some violations are OK if content flows naturally
   - Use `--strict` mode sparingly

### For Reviewers

1. **Use comprehensive validation**
   ```bash
   python scripts/blog-content/full-post-validation.py --post src/posts/review.md
   ```

2. **Generate markdown reports**
   ```bash
   python scripts/blog-content/full-post-validation.py \
     --post src/posts/review.md \
     --output markdown \
     --report-file review-report.md
   ```

3. **Focus on pattern, not just score**
   - Check sentiment balance
   - Verify concrete examples
   - Ensure trade-offs are discussed

### For Automation

1. **Use JSON output for parsing**
   ```bash
   python scripts/blog-content/humanization-validator.py \
     --post src/posts/example.md \
     --output json | jq '.score'
   ```

2. **Set appropriate thresholds**
   - Development: `--min-score 60`
   - Staging: `--min-score 70`
   - Production: `--min-score 75` with `--strict`

3. **Fail fast in CI/CD**
   ```bash
   set -e  # Exit on first error
   python scripts/blog-content/full-post-validation.py --post "$FILE" --strict
   ```

---

## Troubleshooting

### Common Issues

#### "Post file not found"
```bash
# Use absolute path or run from repo root
python scripts/blog-content/humanization-validator.py \
  --post /full/path/to/post.md
```

#### "HumanizationValidator not available"
```bash
# Ensure both scripts are in same directory
ls -l scripts/blog-content/humanization-validator.py
ls -l scripts/blog-content/full-post-validation.py
```

#### Low humanization score
Common causes:
- Too many em dashes or semicolons
- Missing first-person statements
- No specific timestamps/versions
- Overly positive sentiment

Fix:
1. Remove em dashes, use commas
2. Add "I tested..." statement
3. Include version numbers or dates
4. Add trade-offs and limitations

#### Low citation score
```bash
# Check claims vs citations
python scripts/blog-content/full-post-validation.py \
  --post src/posts/example.md \
  --output json | jq '.checks.citations'
```

---

## Customization

### Adjust Scoring Weights

Edit `full-post-validation.py`:
```python
# Line ~150
weights = [0.30, 0.25, 0.20, 0.15, 0.10]  # [humanization, citations, quality, metadata, accessibility]

# Example: Prioritize citations
weights = [0.25, 0.35, 0.20, 0.10, 0.10]
```

### Add New Banned Tokens

Edit `humanization-patterns.yaml`:
```yaml
banned_tokens:
  jargon:
    - word: "disrupt"
      severity: "high"
      message: "Buzzword. Be specific about the change."
      suggested_replacements: ["change", "improve", "replace"]
```

### Modify Required Patterns

```yaml
required_patterns:
  code_examples:
    min_occurrences: 1
    patterns:
      - regex: '```[\s\S]+?```'
    message: "Include at least one code example."
```

---

## Performance

### Execution Time
- **humanization-validator.py**: ~0.5-1.0s per post
- **full-post-validation.py**: ~1.0-2.0s per post

### Resource Usage
- Memory: <50MB per validation
- CPU: Single-threaded, minimal usage

### Batch Processing
```bash
# Validate all posts
for post in src/posts/*.md; do
  python scripts/blog-content/humanization-validator.py --post "$post" --output json
done | jq -s 'map(select(.score < 70))'
```

---

## Dependencies

### Required
- Python 3.8+
- PyYAML (`pip install pyyaml`)
- python-frontmatter (`pip install python-frontmatter`)

### Optional
- jq (for JSON parsing in shell)
- colorama (Windows color support)

### Installation
```bash
pip install pyyaml python-frontmatter
```

---

## Maintenance

### Regular Updates

1. **Review patterns quarterly**
   - Analyze false positives
   - Add new AI-tells as they emerge
   - Adjust thresholds based on content evolution

2. **Update documentation**
   - Add examples of good/bad patterns
   - Document edge cases
   - Share common fixes

3. **Monitor effectiveness**
   ```bash
   # Generate validation statistics
   for post in src/posts/*.md; do
     python scripts/blog-content/humanization-validator.py \
       --post "$post" --output json
   done | jq -s 'map(.score) | add / length'
   ```

---

## Support

### Get Help
- Review examples in this documentation
- Check script headers for detailed usage
- Run with `--help` for quick reference

### Report Issues
Include:
- Command used
- Post excerpt causing issue
- Expected vs actual behavior
- Output (text or JSON)

### Contribute
Improvements welcome:
- New pattern definitions
- Better detection algorithms
- Additional validation checks
- Performance optimizations

---

## License

MIT License - Part of williamzujkowski.github.io repository
