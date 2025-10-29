# Humanization Pre-commit Hook Documentation

## Overview

The humanization pre-commit hook automatically validates blog posts for human-like writing style before allowing commits. It ensures all blog posts maintain a minimum quality score of **75/100** on humanization metrics.

## Location

The hook is integrated into the main pre-commit hook:
```
.git/hooks/pre-commit
```

## How It Works

1. **Detects Modified Posts**: Scans staged files for blog posts in `src/posts/*.md`
2. **Excludes Special Files**: Skips `welcome.md` (documentation)
3. **Validates Each Post**: Runs `humanization-validator.py` on each modified post
4. **Checks Score**: Blocks commit if any post scores below 75/100
5. **Reports Results**: Shows clear pass/fail messages with scores

## Validation Process

### What Gets Checked

When you commit changes to blog posts, the hook validates:

- **AI-tells**: Em dashes (—), excessive semicolons, corporate buzzwords
- **Personal Voice**: First-person perspective, personal experiences
- **Authenticity**: Uncertainty expressions, specific details, trade-offs
- **Sentence Structure**: Variety in length and complexity
- **Sentiment Balance**: Avoids overly positive/hype language
- **Jargon Avoidance**: Corporate and AI-generated phrases

### Score Calculation

- **100 points baseline**
- **Deductions for violations**: -5 to -15 points each
- **Minimum passing score**: 75/100
- **Strict mode available**: Can be configured in validator

## Usage

### Normal Commit Flow

```bash
# Make changes to blog posts
vim src/posts/2025-10-28-my-post.md

# Stage changes
git add src/posts/2025-10-28-my-post.md

# Commit (hook runs automatically)
git commit -m "Add new blog post"
```

### Expected Output

#### Passing Commit
```
🔍 Running pre-commit standards validation...
  Checking MANIFEST.json...
✅ MANIFEST.json valid
  Checking for duplicates...
✅ No duplicates found
  Checking standards compliance...
✅ Standards rules loaded
  Checking humanization scores...
✅ src/posts/2025-10-28-my-post.md: 85/100
✅ All posts meet humanization standards
  Updating MANIFEST.json...
✅ MANIFEST.json updated
✅ Pre-commit validation passed
```

#### Failing Commit
```
🔍 Running pre-commit standards validation...
  Checking MANIFEST.json...
✅ MANIFEST.json valid
  Checking for duplicates...
✅ No duplicates found
  Checking standards compliance...
✅ Standards rules loaded
  Checking humanization scores...
❌ src/posts/2025-10-28-my-post.md: 65/100 (minimum 75 required)

❌ Humanization validation FAILED
The following posts scored below 75/100:
  - src/posts/2025-10-28-my-post.md: 65/100 (below threshold)

Please fix the posts and try again, or use --no-verify to bypass (not recommended)
```

## Bypassing the Hook

### When to Bypass

- Emergency fixes (with team approval)
- Committing drafts (use branch naming like `draft/...`)
- Testing purposes (local only)

### How to Bypass

```bash
git commit --no-verify -m "Emergency fix"
```

**⚠️ Warning**: Bypassing the hook should be rare and documented in commit messages.

## Fixing Low-Scoring Posts

### Check Score Manually

```bash
python scripts/blog-content/humanization-validator.py \
  --post src/posts/my-post.md \
  --output json | jq '.score'
```

### Get Detailed Report

```bash
python scripts/blog-content/humanization-validator.py \
  --post src/posts/my-post.md
```

### Common Issues and Fixes

#### 1. Too Many AI-tells

**Problem**: Em dashes (—), semicolons, corporate buzzwords

**Fix**:
```markdown
# ❌ Before
The solution leverages cutting-edge technology—delivering unprecedented results; moreover, it revolutionizes workflows.

# ✅ After
I tried this approach and it worked better than expected. It simplified my workflow and saved me hours.
```

#### 2. Missing Personal Voice

**Problem**: No first-person perspective

**Fix**:
```markdown
# ❌ Before
The optimal configuration involves setting up multiple VLANs.

# ✅ After
I spent way too long figuring out VLANs. Here's what worked for me after breaking my network three times.
```

#### 3. Too Generic

**Problem**: Vague statements without specifics

**Fix**:
```markdown
# ❌ Before
This approach improves performance significantly.

# ✅ After
This cut my build time from 45 minutes to 12 minutes. Not sure if it'll scale, but it works for my setup.
```

#### 4. Overly Positive

**Problem**: Hype language, no trade-offs mentioned

**Fix**:
```markdown
# ❌ Before
This revolutionary solution delivers best-in-class results with zero downtime.

# ✅ After
This works well for my use case, but it uses more memory than I'd like. If you're tight on RAM, consider alternatives.
```

## Configuration

### Minimum Score

The minimum score is hardcoded to **75** in the hook. To change it:

1. Edit `.git/hooks/pre-commit`
2. Find the line: `if score < 75:`
3. Change `75` to your desired threshold

### Excluded Files

Currently excludes:
- `src/posts/welcome.md` (documentation)

To exclude more files, edit the filter in the hook:

```python
modified_posts = [
    f for f in modified_files
    if f.startswith('src/posts/')
    and f.endswith('.md')
    and 'welcome.md' not in f
    and 'draft' not in f  # Add more exclusions here
]
```

## Testing

### Run Tests

```bash
# Simple focused tests
bash tests/simple-hook-test.sh

# Comprehensive test suite
bash tests/test-humanization-hook.sh
```

### Manual Testing

```bash
# Create a low-scoring test post
cat > src/posts/test-low.md << 'EOF'
---
title: "Test"
date: 2025-10-28
---
Leveraging cutting-edge solutions revolutionizes paradigms.
EOF

# Try to commit it (should fail)
git add src/posts/test-low.md
git commit -m "Test"

# Cleanup
git reset HEAD src/posts/test-low.md
rm src/posts/test-low.md
```

## Dependencies

### Required Tools

- Python 3.8+
- `jq` (JSON parser)
- `bc` (calculator for float comparison)

### Install Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install jq bc

# macOS
brew install jq bc

# Verify installation
which jq bc
```

### Python Dependencies

The validator requires:
- `PyYAML`
- `python-frontmatter`

Install via:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### Hook Not Running

**Problem**: Commit succeeds without validation

**Check**:
```bash
# Verify hook exists and is executable
ls -la .git/hooks/pre-commit

# Should show: -rwxr-xr-x (executable)
```

**Fix**:
```bash
chmod +x .git/hooks/pre-commit
```

### Validation Fails on All Posts

**Problem**: Every post fails validation

**Check**:
```bash
# Test validator directly
python scripts/blog-content/humanization-validator.py \
  --post src/posts/your-post.md \
  --output json
```

**Possible causes**:
- Missing `humanization-patterns.yaml`
- Python dependency issues
- Invalid YAML configuration

### False Positives

**Problem**: Good posts score too low

**Solutions**:
1. Check detailed violation report
2. Consider adjusting minimum score
3. Add exceptions for specific patterns
4. Review `humanization-patterns.yaml` rules

### Performance Issues

**Problem**: Hook takes too long

**Optimize**:
- Only modified posts are checked (not all posts)
- Validator runs in ~1-2 seconds per post
- Consider parallelizing multiple posts (future enhancement)

## CI/CD Integration

### GitHub Actions

The hook runs locally, but you can also add validation to CI/CD:

```yaml
# .github/workflows/validate-posts.yml
name: Validate Blog Posts

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
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Validate humanization scores
        run: |
          for post in $(git diff --name-only origin/main HEAD | grep 'src/posts/.*\.md'); do
            python scripts/blog-content/humanization-validator.py \
              --post "$post" \
              --min-score 75 \
              --output json
          done
```

## Best Practices

### For Writers

1. **Write naturally first**: Don't worry about the score while drafting
2. **Run validator manually**: Check score before committing
3. **Fix incrementally**: Address one type of violation at a time
4. **Use personal voice**: Write like you're explaining to a friend
5. **Include specifics**: Real examples beat generic descriptions

### For Teams

1. **Document exceptions**: When bypassing, explain why in commit message
2. **Regular reviews**: Periodically review patterns and adjust rules
3. **Share examples**: Keep a library of high-scoring posts
4. **Onboard new writers**: Train on humanization requirements
5. **Monitor trends**: Track average scores over time

## Future Enhancements

Planned improvements:

- [ ] Parallel validation for multiple posts
- [ ] Integration with editor plugins (VS Code)
- [ ] Real-time scoring during writing
- [ ] Historical score tracking
- [ ] Per-author score profiles
- [ ] Automatic suggestion system
- [ ] AI-powered rewriting assistant

## Support

### Getting Help

1. **Check validator output**: Detailed violations with line numbers
2. **Review patterns file**: `scripts/blog-content/humanization-patterns.yaml`
3. **Run tests**: Use test scripts to verify setup
4. **Check logs**: Look for Python errors in hook output

### Reporting Issues

When reporting problems:
1. Include full hook output
2. Share the blog post (or relevant excerpt)
3. Provide validator score and violations
4. Mention Python version and dependencies

## License

Part of williamzujkowski.github.io repository.
See main repository LICENSE file.

## Version History

- **v1.0.0** (2025-10-28): Initial implementation
  - 75/100 minimum score
  - Integrated into pre-commit hook
  - Excludes welcome.md
  - JSON output support
  - Comprehensive test suite
