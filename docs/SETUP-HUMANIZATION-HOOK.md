# Humanization Hook Setup Guide

## Quick Start

This repository includes a pre-commit hook that validates blog posts for human-like writing quality. Posts must score **75/100 or higher** to be committed.

## For New Developers

### Prerequisites

```bash
# Install required dependencies
sudo apt-get install jq bc  # Ubuntu/Debian
# or
brew install jq bc          # macOS

# Install Python dependencies
pip install -r requirements.txt
```

### Verify Installation

The hook is already installed in `.git/hooks/pre-commit`. Verify it works:

```bash
# Check hook exists and is executable
ls -la .git/hooks/pre-commit

# Should show:
# -rwxr-xr-x ... pre-commit

# Test the hook
bash tests/simple-hook-test.sh
```

### First Commit

When you commit a blog post for the first time:

```bash
# Create or modify a post
vim src/posts/my-post.md

# Stage changes
git add src/posts/my-post.md

# Commit (hook runs automatically)
git commit -m "Add blog post"

# If validation fails:
# ❌ src/posts/my-post.md: 65/100 (minimum 75 required)
#
# Fix issues and try again
```

## Understanding Scores

### What Gets Validated

✅ **Good practices** (increase score):
- Personal voice (I, me, my)
- Uncertainty expressions (probably, might, not sure)
- Specific details and examples
- Trade-offs and limitations
- Varied sentence structure

❌ **AI-tells** (decrease score):
- Em dashes (—)
- Excessive semicolons
- Corporate buzzwords (leverage, paradigm, revolutionary)
- Overly positive sentiment
- Generic statements

### Check Your Score

Before committing, check your post's score:

```bash
# Get score
python scripts/blog-content/humanization-validator.py \
  --post src/posts/my-post.md \
  --output json | jq '.score'

# Get detailed report
python scripts/blog-content/humanization-validator.py \
  --post src/posts/my-post.md
```

## Common Scenarios

### Scenario 1: Score Too Low

```
❌ src/posts/my-post.md: 65/100 (minimum 75 required)
```

**Solution**: Get detailed violations:
```bash
python scripts/blog-content/humanization-validator.py \
  --post src/posts/my-post.md
```

Review violations and fix them. Common issues:
- Missing first-person perspective
- Too many corporate buzzwords
- No uncertainty or trade-offs mentioned
- Overly positive tone

### Scenario 2: Emergency Commit

Need to commit without validation?

```bash
# Use --no-verify (document why in commit message)
git commit --no-verify -m "Emergency: Fix broken link

Bypassing humanization check because this is a critical fix.
Will improve content quality in follow-up commit."
```

### Scenario 3: Working on Drafts

Create drafts in a separate directory or use branch naming:

```bash
# Option 1: Use draft branch
git checkout -b draft/my-new-post
# Hook still validates, but it's okay to fail

# Option 2: Exclude draft files
# Edit .git/hooks/pre-commit to exclude 'draft' in filename
```

## Hook Behavior

### What Gets Checked

- ✅ Files in `src/posts/*.md`
- ✅ Only staged files (modified or added)
- ❌ `src/posts/welcome.md` (excluded)
- ❌ Files outside `src/posts/`

### When Hook Runs

```
git commit
  ↓
Pre-commit hook starts
  ↓
1. Validate MANIFEST.json
2. Check for duplicate files
3. Check standards compliance
4. Validate humanization scores ← NEW
5. Update MANIFEST.json
  ↓
If all pass → Commit succeeds
If any fail → Commit blocked
```

## Troubleshooting

### Hook Doesn't Run

```bash
# Fix permissions
chmod +x .git/hooks/pre-commit

# Verify it's not being skipped
git config --get core.hooksPath
# Should be empty or .git/hooks
```

### Dependencies Missing

```bash
# Test dependencies
which jq
which bc
python -c "import yaml, frontmatter; print('OK')"

# Install if missing
pip install PyYAML python-frontmatter
```

### All Posts Fail

```bash
# Test validator directly
python scripts/blog-content/humanization-validator.py \
  --post src/posts/welcome.md

# Check for errors in Python dependencies
python scripts/blog-content/humanization-validator.py \
  --post src/posts/welcome.md 2>&1 | head -20
```

### Hook Too Slow

The hook validates only modified posts (not all posts). Each post takes ~1-2 seconds.

If it's still slow:
```bash
# Profile the hook
time .git/hooks/pre-commit

# Check Python performance
time python scripts/blog-content/humanization-validator.py \
  --post src/posts/example.md
```

## Configuration

### Adjust Minimum Score

Edit `.git/hooks/pre-commit`, find this line:

```python
if score < 75:
```

Change `75` to your desired threshold (0-100).

### Exclude Additional Files

Edit `.git/hooks/pre-commit`, modify the filter:

```python
modified_posts = [
    f for f in modified_files
    if f.startswith('src/posts/')
    and f.endswith('.md')
    and 'welcome.md' not in f
    and 'EXCLUDE_THIS' not in f  # Add your exclusion
]
```

### Customize Validation Rules

Edit validation patterns:
```bash
vim scripts/blog-content/humanization-patterns.yaml
```

After changes, test:
```bash
python scripts/blog-content/humanization-validator.py \
  --config scripts/blog-content/humanization-patterns.yaml \
  --post src/posts/test.md
```

## For CI/CD

### GitHub Actions

Add to `.github/workflows/validate-posts.yml`:

```yaml
name: Validate Posts
on:
  pull_request:
    paths: ['src/posts/**/*.md']

jobs:
  humanization:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install PyYAML python-frontmatter
          sudo apt-get update && sudo apt-get install -y jq bc

      - name: Validate humanization
        run: |
          for post in $(git diff --name-only origin/main HEAD | grep 'src/posts/.*\.md'); do
            echo "Validating $post"
            SCORE=$(python scripts/blog-content/humanization-validator.py \
              --post "$post" --output json | jq -r '.score')
            echo "Score: $SCORE/100"
            if (( $(echo "$SCORE < 75" | bc -l) )); then
              echo "❌ FAILED: $post scored $SCORE/100 (minimum 75)"
              exit 1
            fi
          done
```

## Writing Tips

### Quick Wins for Better Scores

1. **Use first person**: "I tried this" not "One might try"
2. **Be specific**: "It took 45 minutes" not "It took a while"
3. **Show uncertainty**: "I think this works" not "This definitely works"
4. **Mention trade-offs**: "Fast but uses more memory"
5. **Vary sentences**: Mix short and long sentences

### Examples

#### ❌ Low Score (35/100)

```markdown
Leveraging cutting-edge cloud technologies revolutionizes enterprise
deployments; moreover, the robust solution seamlessly integrates with
existing infrastructure—providing unprecedented performance and
scalability.
```

Issues:
- Corporate buzzwords
- Em dash (—)
- Semicolon in narrative
- No personal voice
- Overly positive
- Too generic

#### ✅ High Score (90/100)

```markdown
I spent three days migrating to Kubernetes and honestly, I'm still not
sure I needed it. My setup is probably overkill for a home lab.

The learning curve was steep. I broke the deployment four times before
getting it right. Docker Compose might've been enough, but I wanted to
learn K8s properly.

Trade-off: It uses way more RAM than my old setup. If you're low on
resources, stick with Docker Compose.
```

Why it scores high:
- Personal voice (I, me, my)
- Specific details (three days, four times)
- Uncertainty (probably, not sure, might)
- Trade-offs mentioned
- Conversational tone
- Varied sentence structure

## Best Practices

### Before Committing

1. Write naturally (don't optimize for score while drafting)
2. Check score: `python scripts/.../humanization-validator.py --post ...`
3. Review violations if score is low
4. Fix issues one category at a time
5. Re-check score
6. Commit when score ≥ 75

### For Code Reviews

When reviewing PRs with blog posts:
1. Check humanization score is shown
2. Review if score is close to threshold (75-80)
3. Suggest improvements for authenticity
4. Accept genuine voice over perfect score

### Maintenance

1. Run tests regularly: `bash tests/simple-hook-test.sh`
2. Update patterns when needed
3. Monitor average scores over time
4. Adjust threshold if too strict/lenient

## Getting Help

### Resources

- Full documentation: `docs/HOOKS-HUMANIZATION.md`
- Validator script: `scripts/blog-content/humanization-validator.py`
- Patterns file: `scripts/blog-content/humanization-patterns.yaml`
- Test suite: `tests/simple-hook-test.sh`

### Common Questions

**Q: Can I disable the hook?**
A: Yes, but it's not recommended. Use `git commit --no-verify` for emergencies.

**Q: Why 75 as minimum score?**
A: Balances quality and flexibility. Most well-written posts score 75-95.

**Q: What if I disagree with a violation?**
A: Check patterns file. If a rule is too strict, suggest changes via PR.

**Q: Does it work with GUI git clients?**
A: Yes, pre-commit hooks run with any git commit method.

## Support

If you encounter issues:

1. Run tests: `bash tests/simple-hook-test.sh`
2. Check dependencies: `which jq bc && python -c "import yaml, frontmatter"`
3. Test validator directly on your post
4. Review detailed violations
5. Check hook permissions: `ls -la .git/hooks/pre-commit`

Still stuck? Check the full documentation in `docs/HOOKS-HUMANIZATION.md`.
