# Git Rename Fix Implementation Report

**Date:** 2025-11-01
**Author:** Claude Code
**Status:** ✅ Complete

## Problem Description

The `check_duplicates()` pre-commit hook was falsely detecting duplicates during `git mv` (rename) operations. When a file was renamed, the hook would report:

```
Duplicate files detected:
  docs/archive/test-file.md duplicates docs/test-file.md
```

This occurred because the hook only checked staged filenames without considering that the old and new paths were part of a single rename operation, not two separate files.

## Root Cause

The original implementation used:
```bash
git diff --cached --name-only
```

This command returns filenames but not their status. For a rename operation, it would return both the old and new paths as separate entries, triggering the duplicate detection logic.

## Solution

### Implementation Changes

**File:** `scripts/lib/precommit_validators.py`
**Function:** `check_duplicates()`

**Key changes:**

1. **Use `--name-status` instead of `--name-only`:**
   ```python
   # Before:
   subprocess.run(["git", "diff", "--cached", "--name-only"], ...)

   # After:
   subprocess.run(["git", "diff", "--cached", "--name-status"], ...)
   ```

2. **Parse rename operations:**
   ```python
   rename_pairs = set()

   for line in staged_lines:
       parts = line.split('\t')
       status = parts[0]

       if status.startswith('R'):  # R100, R095, etc.
           if len(parts) >= 3:
               old_path = parts[1]
               new_path = parts[2]
               rename_pairs.add((old_path, new_path))
               rename_pairs.add((new_path, old_path))
   ```

3. **Skip rename pairs during duplicate checking:**
   ```python
   if Path(registered).name == staged_name and registered != staged:
       # Skip if this is part of a rename operation
       if (staged, registered) in rename_pairs or (registered, staged) in rename_pairs:
           continue

       if (staged, registered) not in allowed_pairs:
           duplicates.append((staged, registered))
   ```

### Git Status Codes Reference

| Status | Meaning | Example |
|--------|---------|---------|
| `A` | Added | New file created |
| `M` | Modified | Existing file changed |
| `D` | Deleted | File removed |
| `R100` | Renamed (100% similar) | File moved with no changes |
| `R095` | Renamed (95% similar) | File moved with minor edits |

## Testing

### Test Suite

Created comprehensive test suite: `tests/test_rename_fix.py`

**Test 1: Rename Detection**
- Create git repo with a file in MANIFEST
- Use `git mv` to rename the file
- Verify `check_duplicates()` returns success (no false positive)

**Test 2: Real Duplicate Detection**
- Create actual duplicate file (not a rename)
- Verify `check_duplicates()` correctly fails

### Test Results

```
======================================================================
Git Rename Handling Test Suite
======================================================================

Test repository: /tmp/rename_test_h1hf8r72

=== Test 1: Git rename should NOT trigger duplicate detection ===
Staged changes:
R100	docs/test-file.md	docs/archive/test-file.md

✅ PASS: No duplicates in 1 staged files

=== Test 2: Real duplicates should STILL be detected ===
✅ PASS: Duplicate correctly detected

======================================================================
Test Summary
======================================================================
Test 1 (Rename handling): ✅ PASS
Test 2 (Real duplicates):  ✅ PASS

🎉 All tests passed! Rename handling works correctly.
```

## Impact

### Before Fix
- ❌ `git mv` operations required `--no-verify` flag
- ❌ False positive duplicate detection
- ❌ Workaround bypassed all pre-commit checks

### After Fix
- ✅ `git mv` operations work normally
- ✅ No false positives for renames
- ✅ Real duplicates still detected correctly
- ✅ No need for `--no-verify` workaround

## Validation Commands

```bash
# Test the fix with a real rename
git mv docs/old-file.md docs/archive/old-file.md
git commit -m "docs: archive old file"
# Should succeed without --no-verify

# Verify validators still work
uv run python scripts/lib/precommit_validators.py

# Run test suite
uv run python tests/test_rename_fix.py
```

## Documentation Updates

- ✅ Added inline comments explaining rename handling
- ✅ Updated function docstring with FIX notice
- ✅ Created test suite with detailed scenarios
- ✅ Created this implementation report

## Future Improvements

1. **Additional edge cases:** Test copy operations (C100) if needed
2. **Performance:** Rename detection adds minimal overhead (single git command)
3. **Logging:** Consider adding debug output for detected renames

## References

- **Git Documentation:** `man git-diff` (--name-status option)
- **Pre-commit Hook:** `.git/hooks/pre-commit`
- **Validators:** `scripts/lib/precommit_validators.py`
- **Test Suite:** `tests/test_rename_fix.py`

---

**Status:** ✅ Fix verified and deployed
**Next Steps:** Monitor for any edge cases in production use
