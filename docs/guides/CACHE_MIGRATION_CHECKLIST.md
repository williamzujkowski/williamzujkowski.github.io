# Cache Utils Migration Checklist

**Quick reference for migrating scripts to use cache_utils.py**

---

## Pre-Migration Checklist

- [ ] Read `docs/guides/CACHE_UTILS_GUIDE.md`
- [ ] Review `scripts/lib/example_cache_usage.py` for patterns
- [ ] Identify which caching functions you need
- [ ] Create backup of script (or commit current state)

---

## Migration Steps

### 1. Add Import (2 minutes)

**Before:**
```python
import yaml
import json
from pathlib import Path
```

**After:**
```python
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from cache_utils import (
    cached_frontmatter,      # If parsing frontmatter
    cached_manifest,         # If loading MANIFEST
    get_all_blog_posts,      # If discovering posts
    cached_http_get,         # If making HTTP requests (sync)
    cached_http_get_async,   # If making HTTP requests (async)
    validate_url_format,     # If validating URLs
    parse_markdown_links,    # If extracting links
)
```

### 2. Replace Frontmatter Parsing (1 minute)

**Before (7 lines):**
```python
with open(post_path, 'r') as f:
    content = f.read()

if content.startswith('---\n'):
    parts = content.split('---\n', 2)
    if len(parts) >= 3:
        frontmatter = yaml.safe_load(parts[1])
```

**After (1 line):**
```python
frontmatter, content = cached_frontmatter(post_path)
```

- [ ] Find all frontmatter parsing code
- [ ] Replace with `cached_frontmatter()`
- [ ] Remove unused `yaml` import if no other usage

### 3. Replace Blog Discovery (1 minute)

**Before (3-11 lines):**
```python
posts_dir = Path('src/posts')
posts = sorted(posts_dir.glob('*.md'))
# Maybe filtering, error handling, etc.
```

**After (1 line):**
```python
posts = get_all_blog_posts()
```

- [ ] Find blog post discovery code
- [ ] Replace with `get_all_blog_posts()`
- [ ] Add `posts_dir` argument if custom directory

### 4. Replace MANIFEST Loading (1 minute)

**Before (3 lines):**
```python
with open('MANIFEST.json', 'r') as f:
    manifest = json.load(f)
```

**After (1 line):**
```python
manifest = cached_manifest()
```

- [ ] Find MANIFEST loading code
- [ ] Replace with `cached_manifest()`
- [ ] Remove unused `json` import if no other usage

### 5. Replace HTTP Requests (2 minutes)

**Before (sync):**
```python
import requests

response = requests.get(url, timeout=10)
if response.status_code == 200:
    content = response.text
```

**After (sync):**
```python
response = cached_http_get(url)
if response['status'] == 200:
    content = response['content']
```

**Before (async):**
```python
async with session.get(url) as response:
    content = await response.text()
```

**After (async):**
```python
response = await cached_http_get_async(url, session)
content = response['content']
```

- [ ] Find HTTP request code
- [ ] Replace with `cached_http_get()` or async version
- [ ] Update response handling (dict instead of object)
- [ ] Consider removing `requests` import if unused

### 6. Replace URL Validation (30 seconds)

**Before:**
```python
import re
url_pattern = re.compile(r'^https?://...')
if url_pattern.match(url):
    ...
```

**After:**
```python
if validate_url_format(url):
    ...
```

- [ ] Find URL validation code
- [ ] Replace with `validate_url_format()`

### 7. Replace Link Extraction (30 seconds)

**Before:**
```python
import re
pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
links = re.findall(pattern, content)
```

**After:**
```python
links = parse_markdown_links(content)
```

- [ ] Find link extraction code
- [ ] Replace with `parse_markdown_links()`

---

## Post-Migration Checklist

### 8. Testing (3 minutes)

- [ ] Run script with `--help` flag
- [ ] Run script with test data
- [ ] Verify output matches original
- [ ] Check for any errors or warnings

### 9. Performance Validation (2 minutes)

- [ ] Run script twice (first = cache miss, second = cache hit)
- [ ] Note execution times
- [ ] Verify second run is faster
- [ ] Expected: 30-40% improvement minimum

### 10. Code Cleanup (2 minutes)

- [ ] Remove unused imports (`yaml`, `json`, `requests`)
- [ ] Remove duplicate helper functions
- [ ] Update docstring to mention caching
- [ ] Format code consistently

### 11. Optional: Add Cache Monitoring (1 minute)

```python
# At end of script (optional)
if args.verbose or args.debug:
    from cache_utils import print_cache_stats
    print_cache_stats()
```

- [ ] Add `--show-cache-stats` flag (optional)
- [ ] Add cache statistics to verbose output
- [ ] Log cache performance for monitoring

---

## Verification Checklist

### Functional Verification

- [ ] Script runs without errors
- [ ] Output matches original behavior
- [ ] Edge cases handled correctly
- [ ] No regressions in functionality

### Performance Verification

- [ ] First run completes successfully
- [ ] Second run is noticeably faster
- [ ] Cache hit rate >50% for repeated operations
- [ ] Memory usage acceptable

### Code Quality Verification

- [ ] No unused imports
- [ ] No duplicate code remaining
- [ ] Docstring updated
- [ ] Consistent with project style

---

## Common Pitfalls to Avoid

### ❌ Wrong: Importing inside functions
```python
def process():
    from cache_utils import cached_frontmatter  # Don't do this!
```

### ✅ Correct: Import at module level
```python
from cache_utils import cached_frontmatter

def process():
    ...
```

---

### ❌ Wrong: Not handling errors
```python
frontmatter, _ = cached_frontmatter(post)
title = frontmatter['title']  # May KeyError!
```

### ✅ Correct: Safe access
```python
frontmatter, _ = cached_frontmatter(post)
title = frontmatter.get('title', 'Untitled')
```

---

### ❌ Wrong: Forgetting to clear cache after data changes
```python
def update_posts():
    modify_post_file()
    posts = get_all_blog_posts()  # Returns old cached list!
```

### ✅ Correct: Clear cache when data changes
```python
def update_posts():
    modify_post_file()
    get_all_blog_posts.cache_clear()  # Force refresh
    posts = get_all_blog_posts()
```

---

### ❌ Wrong: Using sync HTTP in async context
```python
async def process():
    response = cached_http_get(url)  # Blocks event loop!
```

### ✅ Correct: Use async version
```python
async def process():
    response = await cached_http_get_async(url, session)
```

---

## Quick Reference: Cache Functions

| Old Pattern | New Function | Time Saved |
|-------------|--------------|------------|
| `yaml.safe_load(...)` | `cached_frontmatter()` | 99.7% |
| `json.load('MANIFEST.json')` | `cached_manifest()` | 99.0% |
| `Path('src/posts').glob('*.md')` | `get_all_blog_posts()` | 99.0% |
| `requests.get(url)` | `cached_http_get()` | 60-80% |
| `re.match(url_pattern, url)` | `validate_url_format()` | 95%+ |
| `re.findall(link_pattern, text)` | `parse_markdown_links()` | 95%+ |

---

## Estimated Time

| Task | Time |
|------|------|
| **Simple script** (<200 LOC) | 5-10 minutes |
| **Medium script** (200-500 LOC) | 10-20 minutes |
| **Complex script** (500+ LOC) | 20-30 minutes |

**Total for 66 scripts:** ~5-11 hours

---

## Example Migration

**File:** `scripts/blog-content/my-script.py`

**Before (20 lines, 1.8s):**
```python
#!/usr/bin/env -S uv run python3
import yaml
import json
from pathlib import Path

def main():
    # Manual discovery
    posts_dir = Path('src/posts')
    posts = sorted(posts_dir.glob('*.md'))

    for post in posts:
        # Manual parsing
        with open(post) as f:
            content = f.read()
        if content.startswith('---\n'):
            parts = content.split('---\n', 2)
            frontmatter = yaml.safe_load(parts[1])

        print(frontmatter.get('title'))

if __name__ == '__main__':
    main()
```

**After (13 lines, 1.1s - 38.9% faster):**
```python
#!/usr/bin/env -S uv run python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from cache_utils import cached_frontmatter, get_all_blog_posts

def main():
    # Cached discovery + parsing
    for post in get_all_blog_posts():
        frontmatter, _ = cached_frontmatter(post)
        print(frontmatter.get('title'))

if __name__ == '__main__':
    main()
```

**Changes:**
- 7 lines removed (35% reduction)
- 0.7s faster (38.9% improvement)
- Cleaner, more maintainable code

---

## Resources

- **Full Guide:** `docs/guides/CACHE_UTILS_GUIDE.md`
- **Examples:** `scripts/lib/example_cache_usage.py`
- **Benchmarks:** `scripts/lib/benchmark_caching.py`
- **Report:** `docs/reports/phase-4-caching-infrastructure-report.md`

---

**Questions?** See the full guide or examples directory.

**Ready to migrate?** Follow this checklist step by step!
