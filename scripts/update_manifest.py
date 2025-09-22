#!/usr/bin/env python3
"""
Update MANIFEST.json with current repository inventory.
Maintains the single source of truth for file registry.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import hashlib

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:8]
    except:
        return None

def should_ignore(path):
    """Check if path should be ignored"""
    ignore_patterns = [
        '.git', '__pycache__', 'node_modules', '_site',
        '.pytest_cache', '.env', '.DS_Store', '*.pyc'
    ]

    path_str = str(path)
    for pattern in ignore_patterns:
        if pattern in path_str:
            return True
        if pattern.startswith('*.') and path_str.endswith(pattern[1:]):
            return True
    return False

def update_manifest():
    """Update MANIFEST.json with current file inventory"""
    manifest_path = Path("MANIFEST.json")

    # Load existing manifest or create new
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    else:
        manifest = {
            "version": "2.0.0",
            "last_validated": "",
            "inventory": {
                "files": {
                    "file_registry": {},
                    "total_count": 0
                }
            }
        }

    # Scan repository
    file_registry = {}
    for path in Path(".").rglob("*"):
        if path.is_file() and not should_ignore(path):
            rel_path = str(path.relative_to("."))

            file_registry[rel_path] = {
                "size": path.stat().st_size,
                "modified": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
                "hash": get_file_hash(path),
                "category": categorize_file(rel_path)
            }

    # Update manifest
    manifest["last_validated"] = datetime.now(timezone.utc).isoformat()
    manifest["inventory"]["files"]["file_registry"] = file_registry
    manifest["inventory"]["files"]["total_count"] = len(file_registry)

    # Add statistics
    categories = {}
    for file_info in file_registry.values():
        cat = file_info.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1

    manifest["inventory"]["files"]["by_category"] = categories

    # Write updated manifest
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ MANIFEST.json updated")
    print(f"   Total files: {len(file_registry)}")
    print(f"   Categories: {categories}")

    return 0

def categorize_file(filepath):
    """Categorize file based on path and extension"""
    path = Path(filepath)

    if path.suffix == '.py':
        if 'scripts' in str(path):
            return 'script'
        elif 'tests' in str(path):
            return 'test'
        return 'python'
    elif path.suffix in ['.md', '.markdown']:
        if 'posts' in str(path):
            return 'post'
        elif 'docs' in str(path):
            return 'documentation'
        return 'markdown'
    elif path.suffix in ['.yml', '.yaml']:
        if '.github/workflows' in str(path):
            return 'workflow'
        return 'config'
    elif path.suffix in ['.js', '.jsx']:
        return 'javascript'
    elif path.suffix in ['.css', '.scss']:
        return 'style'
    elif path.suffix in ['.html', '.njk']:
        return 'template'
    elif path.suffix in ['.json']:
        return 'config'
    elif path.suffix in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
        return 'image'
    else:
        return 'other'

if __name__ == "__main__":
    sys.exit(update_manifest())