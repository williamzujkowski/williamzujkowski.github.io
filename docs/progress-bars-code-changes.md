# Progress Bars - Code Changes Reference

Quick reference for the exact changes made to add tqdm progress bars.

## 1. batch-improve-blog-posts.py

### Import Statement (Line 65)
```python
from tqdm import tqdm
```

### Loop 1: Analyzing Posts (Line 496)
**Before:**
```python
for post_path in posts:
    improvements = self.improve_post(post_path)
```

**After:**
```python
for post_path in tqdm(posts, desc="Analyzing posts"):
    improvements = self.improve_post(post_path)
```

### Loop 2: Applying Improvements (Line 619)
**Before:**
```python
for post_path in posts:
    if improver.apply_automatic_improvements(post_path):
```

**After:**
```python
for post_path in tqdm(posts, desc="Applying improvements"):
    if improver.apply_automatic_improvements(post_path):
```

---

## 2. add-academic-citations.py

### Import Statement (Line 49)
```python
from tqdm import tqdm
```

### Refactored main() Function (Lines 365-375)
**Before:**
```python
# Add citations to posts with most uncited claims
add_citations_to_sustainable_computing()  # 25 uncited claims
add_citations_to_zero_trust()  # 12 uncited claims
add_citations_to_llm_security()  # 11 uncited claims
add_citations_to_claude_flow()  # 10 uncited claims
add_citations_to_local_llm()  # 9 uncited claims
```

**After:**
```python
# Define citation functions to run
citation_functions = [
    ("Sustainable Computing", add_citations_to_sustainable_computing),
    ("Zero Trust Architecture", add_citations_to_zero_trust),
    ("LLM Security", add_citations_to_llm_security),
    ("Claude Flow", add_citations_to_claude_flow),
    ("Local LLM", add_citations_to_local_llm),
]

# Add citations to posts with progress bar
for name, func in tqdm(citation_functions, desc="Adding citations"):
    func()
```

---

## 3. batch-link-fixer.py

### Import Statement (Line 54)
```python
from tqdm import tqdm
```

### Loop: Applying File Repairs (Line 187)
**Before:**
```python
for file_path, file_repairs in repairs_by_file.items():
    self._apply_file_repairs(file_path, file_repairs)
```

**After:**
```python
for file_path, file_repairs in tqdm(repairs_by_file.items(), desc="Fixing files"):
    self._apply_file_repairs(file_path, file_repairs)
```

---

## Pattern Summary

All changes follow the same simple pattern:

```python
# 1. Add import at top of file
from tqdm import tqdm

# 2. Wrap existing loop
for item in tqdm(items, desc="Descriptive text"):
    # ... existing code unchanged ...
```

**Key Points:**
- Only 2 changes per script (import + loop wrapper)
- No changes to loop body
- No changes to function signatures
- No changes to existing functionality
- Minimal code disruption

## Optional: Quiet Mode Support

To add --quiet flag support in the future:

```python
# In argument parser
parser.add_argument('--quiet', action='store_true', help='Suppress progress bars')

# In loop
for item in tqdm(items, desc="Processing", disable=args.quiet):
    process_item(item)
```

This allows users to disable progress bars for automated scripts or when piping output.
