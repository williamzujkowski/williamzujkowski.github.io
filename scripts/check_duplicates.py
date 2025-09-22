#!/usr/bin/env python3
"""
Check for duplicate files in the repository.
Part of the repository compliance validation suite.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def check_duplicates():
    """Check for duplicate files in MANIFEST.json"""
    manifest_path = Path("MANIFEST.json")

    if not manifest_path.exists():
        print("❌ MANIFEST.json not found")
        return 1

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing MANIFEST.json: {e}")
        return 1

    # Check file registry for duplicates
    file_registry = manifest.get('inventory', {}).get('files', {}).get('file_registry', {})

    # Track basenames to find duplicates
    basename_map = defaultdict(list)
    for filepath in file_registry.keys():
        basename = Path(filepath).name
        if basename and not basename.startswith('.'):
            basename_map[basename].append(filepath)

    # Find actual duplicates (same basename in different directories)
    duplicates_found = False
    for basename, paths in basename_map.items():
        if len(paths) > 1:
            # Filter out legitimate cases
            if basename == "README.md":
                continue

            # Filter out _site directory (build output)
            non_site_paths = [p for p in paths if not p.startswith("_site/")]

            # Only flag if there are duplicates outside of _site
            if len(non_site_paths) > 1:
                print(f"❌ Duplicate file detected: {basename}")
                for path in non_site_paths:
                    print(f"  - {path}")
                duplicates_found = True

    if duplicates_found:
        print("\n❌ Duplicate file check failed")
        print("   Please check file_registry in MANIFEST.json before creating new files")
        return 1
    else:
        print("✅ No duplicate files found")
        return 0

if __name__ == "__main__":
    sys.exit(check_duplicates())