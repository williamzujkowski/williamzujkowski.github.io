# Update Blog Gist URLs Script

## Overview

`update-blog-gist-urls.py` replaces placeholder GitHub gist URLs in blog posts with real URLs from `gists/gist-mapping.json`.

## Prerequisites

1. **Gist mapping file exists:** `gists/gist-mapping.json` (created by `create-gists-from-folder.py`)
2. **Blog posts contain placeholder URLs:** Format: `https://gist.github.com/williamzujkowski/{slug}`

## Usage

### Basic Usage

```bash
# Preview changes without writing (recommended first)
python scripts/update-blog-gist-urls.py --dry-run

# Apply changes to blog posts
python scripts/update-blog-gist-urls.py
```

### Expected Workflow

1. **Create gists:** Run `create-gists-from-folder.py` to create gists and generate `gist-mapping.json`
2. **Preview replacements:** Run with `--dry-run` to see what will be replaced
3. **Apply updates:** Run without flags to update blog posts
4. **Validate:** Script automatically checks that all placeholders were replaced

## Blog Posts Updated

The script updates these 4 blog posts:

- `src/posts/2025-10-06-automated-security-scanning-pipeline.md`
- `src/posts/2025-09-14-threat-intelligence-mitre-attack-dashboard.md`
- `src/posts/2025-09-08-zero-trust-vlan-segmentation-homelab.md`
- `src/posts/2025-09-29-proxmox-high-availability-homelab.md`

## Mapping File Format

The `gists/gist-mapping.json` file should have this structure:

```json
{
  "gists/security-scanning/integrations/vscode-security-scan-tasks.json": {
    "url": "https://gist.github.com/williamzujkowski/abc123def456789",
    "slug": "vscode-security-scan-tasks"
  },
  "gists/vlan-segmentation/vlan-dhcp-config.json": {
    "url": "https://gist.github.com/williamzujkowski/def456789abc123",
    "slug": "vlan-dhcp-config"
  }
}
```

## Example Output

### Dry Run Mode

```
🔍 DRY RUN MODE - No changes will be written

📖 Loading gist mapping from: gists/gist-mapping.json
✓ Loaded 45 gist mappings

📝 Processing: 2025-10-06-automated-security-scanning-pipeline.md
------------------------------------------------------------

✓ Made 15 replacement(s):

  ✓ Replaced vscode-security-scan-tasks
    Old: https://gist.github.com/williamzujkowski/vscode-security-scan-tasks
    New: https://gist.github.com/williamzujkowski/abc123def456789
    Source: gists/security-scanning/integrations/vscode-security-scan-tasks.json

  ✓ Replaced grype-config
    Old: https://gist.github.com/williamzujkowski/grype-config
    New: https://gist.github.com/williamzujkowski/def456789abc123
    Source: gists/security-scanning/configs/grype.yaml

...

============================================================
SUMMARY
============================================================
Total replacements: 52
Posts processed: 4

🔍 DRY RUN - No files were modified
Run without --dry-run to apply changes
```

### Apply Mode

```
📖 Loading gist mapping from: gists/gist-mapping.json
✓ Loaded 45 gist mappings

📝 Processing: 2025-10-06-automated-security-scanning-pipeline.md
------------------------------------------------------------

✓ Made 15 replacement(s):

  ✓ Replaced vscode-security-scan-tasks
    Old: https://gist.github.com/williamzujkowski/vscode-security-scan-tasks
    New: https://gist.github.com/williamzujkowski/abc123def456789
    Source: gists/security-scanning/integrations/vscode-security-scan-tasks.json

...

✓ All placeholders successfully replaced

============================================================
SUMMARY
============================================================
Total replacements: 52
Posts processed: 4

✓ All placeholder URLs successfully replaced!
```

## Validation

The script performs automatic validation:

1. **Placeholder detection:** Finds all URLs matching pattern `https://gist.github.com/williamzujkowski/{slug}`
2. **Mapping lookup:** Matches slug to real URL in `gist-mapping.json`
3. **Replacement:** Updates blog post content
4. **Post-validation:** Checks that no placeholders remain (ignoring legitimate 32-char hex gist IDs)

### Success Criteria

- ✅ All placeholder URLs replaced with real gist URLs
- ✅ No unmapped slugs remain
- ✅ Script exits with code 0

### Failure Scenarios

The script will exit with error code 1 if:

- ❌ `gist-mapping.json` doesn't exist
- ❌ `gist-mapping.json` contains invalid JSON
- ❌ Placeholders remain after update (some slugs not in mapping)

## Example Placeholder URL Pattern

**Before (placeholder):**
```markdown
[Full implementation](https://gist.github.com/williamzujkowski/vscode-security-scan-tasks)
```

**After (real URL):**
```markdown
[Full implementation](https://gist.github.com/williamzujkowski/abc123def456789)
```

## Troubleshooting

### Error: "Gist mapping file not found"

**Cause:** `gists/gist-mapping.json` doesn't exist

**Solution:** Run `create-gists-from-folder.py` first to create gists and generate the mapping file

### Warning: "No mapping found for slug"

**Cause:** Blog post references a slug that isn't in the mapping file

**Solution:**
1. Check if the slug name matches the filename in `gists/` directories
2. Re-run `create-gists-from-folder.py` to ensure all gists were created
3. Update the blog post URL to match an existing gist slug

### No placeholders found

**Cause:** Blog posts already use real gist URLs or don't contain any gist links

**Solution:** This is normal if gists were already updated. Script will report 0 replacements.

## Testing

### Unit Tests

```bash
# Test helper functions
python -c "
import sys
sys.path.insert(0, 'scripts')
exec(open('scripts/update-blog-gist-urls.py').read().replace('if __name__ == \"__main__\":', 'if False:'))

# Test extract_slug_from_url
test_url = 'https://gist.github.com/williamzujkowski/vlan-dhcp-config'
slug = extract_slug_from_url(test_url)
assert slug == 'vlan-dhcp-config'

print('✅ All tests passed!')
"
```

### Integration Test

```bash
# 1. Create test mapping file
cat > /tmp/test-mapping.json << 'EOF'
{
  "test/file.json": {
    "url": "https://gist.github.com/williamzujkowski/abc123",
    "slug": "test-slug"
  }
}
EOF

# 2. Create test blog post with placeholder
cat > /tmp/test-post.md << 'EOF'
# Test Post
[Link](https://gist.github.com/williamzujkowski/test-slug)
EOF

# 3. Run script (would need to modify BLOG_POSTS constant)
# Expected: placeholder replaced with real URL
```

## See Also

- **Create Gists:** `create-gists-from-folder.py` - Creates gists and generates mapping file
- **Gist Structure:** `gists/README.md` - Documentation of gist organization
- **Blog Posts:** `src/posts/*.md` - Blog posts containing gist links

## License

MIT
