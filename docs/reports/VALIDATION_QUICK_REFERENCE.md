# Validation Infrastructure Quick Reference

**Last Updated:** 2025-11-02
**Agent:** Build-validation-tester

---

## 🚀 Quick Start

### Run Full Validation
```bash
# Check metadata quality
uv run python scripts/validation/metadata-validator.py

# Check build health
npm run build

# Compare with baseline
uv run python scripts/validation/build-monitor.py --compare
```

### Common Commands

| Task | Command |
|------|---------|
| **Validate metadata** | `uv run python scripts/validation/metadata-validator.py` |
| **JSON output** | `uv run python scripts/validation/metadata-validator.py --format json` |
| **Set baseline** | `uv run python scripts/validation/build-monitor.py --baseline` |
| **Check for regressions** | `uv run python scripts/validation/build-monitor.py --compare` |
| **Continuous monitoring** | `./scripts/validation/continuous-monitor.sh` |
| **Run build** | `npm run build` |

---

## 📊 Current Status

### Build Status: ✅ PASSING

```
Build Time:       8.54s
Eleventy Time:    4.59s
Posts Processed:  63/63
Files Written:    209
Bundle Reduction: 49.6%
```

### Metadata Quality: ⚠️ NEEDS WORK

```
Valid Posts:      0/63 (0.0%)
Critical Errors:  45 issues
- Missing author: 34 posts
- Invalid dates:  11 posts
```

---

## 🔧 Scripts Available

### 1. metadata-validator.py
**Location:** `scripts/validation/metadata-validator.py`

Validates frontmatter across all posts.

**Checks:**
- Title (required)
- Description length (120-160 chars optimal)
- Date format (YYYY-MM-DD)
- Author (required)
- Tags (3-8 recommended)
- Hero image paths

**Exit codes:**
- `0` = Success
- `1` = Critical errors found

### 2. build-monitor.py
**Location:** `scripts/validation/build-monitor.py`

Monitors builds and detects regressions.

**Tracks:**
- Build time
- Files processed
- Bundle sizes
- Warnings/errors
- Performance changes

**Regression alerts:**
- Build failures
- Time increases >20%
- New errors

### 3. continuous-monitor.sh
**Location:** `scripts/validation/continuous-monitor.sh`

Real-time file monitoring with auto-validation.

**Features:**
- inotifywait support (fast)
- Polling fallback
- Auto-validates on save
- Logs to `.validation-monitor.log`

---

## 🔴 Critical Issues to Fix

### Priority 1: Missing Author (34 posts)

**Quick fix:**
```bash
# Add author to specific post
sed -i '/^---$/a author: William Zujkowski' src/posts/[filename].md

# Or edit manually
# Add this line to frontmatter:
author: William Zujkowski
```

**Affected posts:**
```
2024-04-11-ethics-large-language-models.md
2024-10-22-ai-edge-computing.md
2024-11-15-gpu-power-monitoring-homelab-ml.md
2024-02-22-open-source-vs-proprietary-llms.md
2024-07-24-multimodal-foundation-models.md
2024-08-02-quantum-computing-leap-forward.md
2025-05-10-llm-fine-tuning-homelab-guide.md
2025-10-29-privacy-first-ai-lab-local-llms.md
2025-10-29-post-quantum-cryptography-homelab.md
2024-09-19-biomimetic-robotics.md
... (24 more - see full report)
```

### Priority 2: Invalid Date Formats (11 posts)

**Issue:** Using ISO 8601 timestamps instead of YYYY-MM-DD

**Fix:**
```yaml
# WRONG
date: 2024-05-19T00:00:00.000Z

# CORRECT
date: 2024-05-19
```

**Affected posts:**
```
2024-10-22-ai-edge-computing.md
2024-11-15-gpu-power-monitoring-homelab-ml.md
2024-09-19-biomimetic-robotics.md
2024-10-10-blockchain-beyond-cryptocurrency.md
2024-10-03-quantum-computing-defense.md
2024-12-03-context-windows-llms.md
2024-08-27-zero-trust-security-principles.md
2025-08-09-ai-cognitive-infrastructure.md
2024-11-19-llms-smart-contract-vulnerability.md
... (2 more)
```

---

## ⚠️ Warnings (Non-Critical)

### Missing Hero Images (63 posts)
- Currently non-critical (warnings only)
- Improves visual appeal and social sharing
- Can be addressed later

### Suboptimal Descriptions (3 posts)
- Optimal SEO length: 120-160 characters
- Posts affected:
  - `2025-10-29-privacy-first-ai-lab-local-llms.md` (195 chars)
  - `2024-09-25-gvisor-container-sandboxing-security.md` (169 chars)
  - `2025-01-22-llm-agent-homelab-incident-response.md` (165 chars)

### Sparse Tags (1 post)
- `2024-01-18-demystifying-cryptography-beginners-guide.md` has only 2 tags
- Recommend 3-8 tags per post

---

## 📈 Before/After Workflow

### Making Changes

1. **Establish baseline:**
   ```bash
   uv run python scripts/validation/build-monitor.py --baseline
   ```

2. **Make your changes**

3. **Validate:**
   ```bash
   # Check metadata
   uv run python scripts/validation/metadata-validator.py

   # Compare build
   uv run python scripts/validation/build-monitor.py --compare
   ```

4. **Commit if passing**

---

## 🎯 Validation Checklist

Before committing changes:

- [ ] Run metadata validator
- [ ] Check for new errors (validator output)
- [ ] Run build (`npm run build`)
- [ ] Compare with baseline (if major changes)
- [ ] Review warnings (if any)
- [ ] Update MANIFEST.json (if files added/removed)

---

## 📚 Documentation

- **Full report:** `docs/reports/BUILD_VALIDATION_REPORT.md`
- **Script docs:** `scripts/validation/README.md`
- **CLAUDE.md:** Project standards and enforcement

---

## 🆘 Troubleshooting

### "YAML parsing error"
**Solution:** Check frontmatter syntax, ensure `---` delimiters present

### "Path not found" for images
**Solution:** Verify image paths relative to project root

### "Build timeout"
**Solution:** Check for infinite loops, increase timeout, or investigate slow steps

### "No baseline found"
**Solution:** Run with `--baseline` flag first

### "Validation FAILED"
**Solution:** Review error output, fix critical issues before committing

---

## 💡 Tips

1. **Use JSON output** for scripting/automation:
   ```bash
   uv run python scripts/validation/metadata-validator.py --format json | jq '.'
   ```

2. **Filter specific issues:**
   ```bash
   uv run python scripts/validation/metadata-validator.py | grep "Missing author"
   ```

3. **Monitor in background:**
   ```bash
   ./scripts/validation/continuous-monitor.sh &
   tail -f .validation-monitor.log
   ```

4. **Pre-commit integration:**
   Add validation to `.git/hooks/pre-commit` to catch issues early

---

## 🔗 Related Files

```
scripts/validation/
├── metadata-validator.py      # Frontmatter validation
├── build-monitor.py            # Build regression detection
├── continuous-monitor.sh       # Real-time monitoring
└── README.md                   # Full documentation

docs/reports/
├── BUILD_VALIDATION_REPORT.md # Complete analysis
└── VALIDATION_QUICK_REFERENCE.md # This file

Project Root:
└── .build-baseline.json        # Build baseline data
```

---

**Questions?** See full documentation in:
- `docs/reports/BUILD_VALIDATION_REPORT.md`
- `scripts/validation/README.md`
- `CLAUDE.md` (section 4.1-4.4)

**Status:** ✅ Infrastructure operational, ready for use
