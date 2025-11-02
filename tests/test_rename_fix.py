#!/usr/bin/env -S uv run python3
"""
Test script to validate git rename handling in duplicate check.

This test verifies that the check_duplicates() function correctly handles
git rename operations (git mv) without false positive duplicate detection.

Author: Claude Code
Date: 2025-11-01
"""

import subprocess
import sys
import tempfile
from pathlib import Path
import shutil
import json

def setup_test_repo():
    """Create a temporary git repo for testing."""
    test_dir = Path(tempfile.mkdtemp(prefix="rename_test_"))

    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=test_dir, check=True, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=test_dir, check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=test_dir, check=True)

    # Create directory structure
    (test_dir / 'docs').mkdir()
    (test_dir / 'docs' / 'archive').mkdir()

    # Create MANIFEST.json
    manifest = {
        "version": "5.0.0",
        "schema": "optimized",
        "last_validated": "2025-11-01T12:00:00-04:00",
        "inventory": {
            "files": {
                "file_registry": {
                    "docs/test-file.md": {
                        "path": "docs/test-file.md",
                        "size": 100,
                        "category": "documentation"
                    }
                }
            }
        },
        "project_overrides": {
            "allowed_duplicates": []
        }
    }

    with open(test_dir / 'MANIFEST.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    # Copy the precommit validators
    scripts_dir = test_dir / 'scripts' / 'lib'
    scripts_dir.mkdir(parents=True)

    # Copy our fixed validator
    shutil.copy(
        Path(__file__).parent.parent / 'scripts' / 'lib' / 'precommit_validators.py',
        scripts_dir / 'precommit_validators.py'
    )

    # Create initial file
    test_file = test_dir / 'docs' / 'test-file.md'
    test_file.write_text("# Test File\n\nThis is a test file for rename detection.\n")

    # Commit initial state
    subprocess.run(['git', 'add', '.'], cwd=test_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=test_dir, check=True, capture_output=True)

    return test_dir


def test_rename_no_false_positive(test_dir):
    """Test that git mv doesn't trigger false duplicate detection."""
    print("\n=== Test 1: Git rename should NOT trigger duplicate detection ===")

    # Perform git rename
    old_path = test_dir / 'docs' / 'test-file.md'
    new_path = test_dir / 'docs' / 'archive' / 'test-file.md'

    subprocess.run(['git', 'mv', str(old_path), str(new_path)], cwd=test_dir, check=True)

    # Check staged changes
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-status'],
        cwd=test_dir,
        capture_output=True,
        text=True,
        check=True
    )

    print(f"Staged changes:\n{result.stdout}")

    # Import and run validator
    sys.path.insert(0, str(test_dir / 'scripts' / 'lib'))
    try:
        from precommit_validators import check_duplicates

        # Change to test directory for validator to work
        original_dir = Path.cwd()
        import os
        os.chdir(test_dir)

        success, message = check_duplicates()

        os.chdir(original_dir)

        if success:
            print(f"✅ PASS: {message}")
            return True
        else:
            print(f"❌ FAIL: {message}")
            print("  Expected: Success (rename should not trigger duplicate)")
            return False
    finally:
        sys.path.pop(0)


def test_real_duplicate_detected(test_dir):
    """Test that real duplicates are still detected."""
    print("\n=== Test 2: Real duplicates should STILL be detected ===")

    # Reset staging
    subprocess.run(['git', 'reset', 'HEAD'], cwd=test_dir, capture_output=True)

    # Create a real duplicate (not a rename)
    new_file = test_dir / 'docs' / 'archive' / 'test-file.md'
    new_file.write_text("# Different Test File\n\nThis is different content.\n")

    subprocess.run(['git', 'add', str(new_file)], cwd=test_dir, check=True)

    # Import and run validator
    sys.path.insert(0, str(test_dir / 'scripts' / 'lib'))
    try:
        from precommit_validators import check_duplicates

        # Change to test directory
        original_dir = Path.cwd()
        import os
        os.chdir(test_dir)

        success, message = check_duplicates()

        os.chdir(original_dir)

        if not success and "duplicates" in message.lower():
            print(f"✅ PASS: Duplicate correctly detected")
            print(f"  Message: {message.split(chr(10))[0]}")
            return True
        else:
            print(f"❌ FAIL: Real duplicate not detected")
            print(f"  Got: {message}")
            return False
    finally:
        sys.path.pop(0)


def main():
    """Run all tests."""
    print("=" * 70)
    print("Git Rename Handling Test Suite")
    print("=" * 70)

    # Setup
    test_dir = setup_test_repo()
    print(f"\nTest repository: {test_dir}")

    try:
        # Run tests
        test1_pass = test_rename_no_false_positive(test_dir)
        test2_pass = test_real_duplicate_detected(test_dir)

        # Summary
        print("\n" + "=" * 70)
        print("Test Summary")
        print("=" * 70)
        print(f"Test 1 (Rename handling): {'✅ PASS' if test1_pass else '❌ FAIL'}")
        print(f"Test 2 (Real duplicates):  {'✅ PASS' if test2_pass else '❌ FAIL'}")

        if test1_pass and test2_pass:
            print("\n🎉 All tests passed! Rename handling works correctly.")
            return 0
        else:
            print("\n⚠️  Some tests failed. Review the implementation.")
            return 1

    finally:
        # Cleanup
        shutil.rmtree(test_dir)
        print(f"\nCleaned up test directory: {test_dir}")


if __name__ == '__main__':
    sys.exit(main())
