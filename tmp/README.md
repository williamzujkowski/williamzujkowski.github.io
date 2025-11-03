# Temporary Files Directory

**Purpose:** Working files and temporary artifacts that are not committed to git.

**Status:** Gitignored (see .gitignore line 29)

---

## Current Contents

### gists/ (44KB, 9 files)
Reference files for GitHub gist creation, prepared during Session 7 (2025-11-02).

**Purpose:** Reduce code ratio in Container Security blog post from 32.8% to <25% by extracting inline code blocks into embedded gists.

**Files:**
- `CREATE_GISTS_INSTRUCTIONS.md` - Manual gist creation guide (80 lines)
- 8 code files (303 lines total):
  - `ai-docker-compose.yml` - Docker compose config
  - `ai-firewall-rules.sh` - Firewall rules
  - `secure-model-loader.py` - Model integrity checker
  - `prompt-security-filter.py` - Prompt injection detector
  - `ai-resource-monitor.py` - GPU/CPU monitor
  - `privacy-preserving-ai.py` - PII redaction
  - `secure-api-manager.py` - API key encryption
  - `family-safe-ai.py` - Content filtering

**Retention:** Keep as reference until gists created and blog post updated, then review for deletion.

---

## Retention Policy

### Keep
- Reference files with ongoing value (e.g., gist prep files until deployed)
- Documentation of decisions (e.g., CREATE_GISTS_INSTRUCTIONS.md)

### Delete
- Working files after session completion
- Temporary exports/extracts after processing
- Draft files after final version created

### Review Frequency
- **Quarterly:** Scan tmp/ for outdated files (>90 days)
- **Session end:** Remove files no longer needed
- **Monthly:** Check size (alert if >10MB)

---

## Usage Guidelines

### Appropriate Uses
- Temporary code extracts for analysis
- Working drafts before final placement
- Session-specific artifacts (exports, reports)
- Gist preparation files

### Inappropriate Uses
- Long-term storage (use docs/, scripts/, or appropriate directory)
- Final versions of files (use proper location)
- Large binary files (use external storage)

### Naming Convention
```
tmp/
├── [session-name]/          # Session-specific work
├── [feature-name]/          # Feature-specific temp files
└── [tool-output]/           # Tool-generated artifacts
```

**Example:**
```
tmp/
├── gists/                   # Session 7: Gist preparation
├── image-analysis/          # Image optimization work
└── export-2025-11/          # Monthly export artifacts
```

---

## Cleanup Commands

### Review contents
```bash
# List all files with sizes
find tmp/ -type f -exec ls -lh {} \;

# Check total size
du -sh tmp/*

# Find old files (>90 days)
find tmp/ -type f -mtime +90
```

### Safe cleanup
```bash
# Remove empty directories
find tmp/ -type d -empty -delete

# Remove old files (review first!)
find tmp/ -type f -mtime +90 -ls
# find tmp/ -type f -mtime +90 -delete  # Uncomment after review
```

### Nuclear option (use with caution)
```bash
# Remove everything except README.md
find tmp/ -mindepth 1 ! -name "README.md" -delete
```

---

## History

### Session 7 (2025-11-02)
- Created `gists/` directory with 8 AI experiment code files
- Prepared gists for Container Security post code ratio compliance
- Target: Reduce 32.8% → <25% via gist embeds

### Session 9 (2025-11-02)
- Audited tmp/ directory (44KB, all appropriate)
- Created tmp/README.md to document policy
- Added tmp/ to .gitignore (line 29)
- Recommendation: Keep gists/ as reference

---

## Related Documentation

- **Audit report:** `docs/reports/SESSION_9_TMP_CLEANUP.md`
- **Code ratio policy:** `docs/context/workflows/gist-management.md`
- **File organization:** `docs/context/core/file-management.md` (Section 4.2)
- **.gitignore policy:** `.gitignore` (line 26-30)

---

**Last updated:** 2025-11-02 (Session 9)
**Next review:** 2026-02-02 (quarterly)
