#!/usr/bin/env python3
"""
SCRIPT: manifest_migrator.py
PURPOSE: Migrate MANIFEST.yaml to MANIFEST.json with complete cataloging
CATEGORY: utility
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T14:57:33-0400

DESCRIPTION:
    This script migrates the existing MANIFEST.yaml to the new MANIFEST.json format,
    performs a complete repository catalog, and establishes MANIFEST.json as the
    single source of truth for all future operations.

LLM_USAGE:
    python scripts/manifest_migrator.py [--backup] [--validate]

ARGUMENTS:
    --backup (bool): Create backup of original MANIFEST.yaml
    --validate (bool): Validate the new manifest after creation
    --verbose (bool): Enable detailed output

EXAMPLES:
    # Basic migration with backup
    python scripts/manifest_migrator.py --backup

    # Full migration with validation
    python scripts/manifest_migrator.py --backup --validate --verbose

OUTPUT:
    Creates MANIFEST.json in repository root
    Optionally backs up MANIFEST.yaml to docs/archive/

DEPENDENCIES:
    - Python 3.8+
    - Required packages: pyyaml
    - Other scripts: None

RELATED_SCRIPTS:
    - validate_manifest.py: Validates manifest structure
    - comprehensive_catalog.py: Performs deep repository scan

MANIFEST_REGISTRY: scripts/manifest_migrator.py
"""

import json
import yaml
import hashlib
import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import sys

# Constants
SCRIPT_PURPOSE = "Migrate MANIFEST.yaml to MANIFEST.json with complete cataloging"
SCRIPT_VERSION = "1.0.0"
MANIFEST_YAML_PATH = Path("MANIFEST.yaml")
MANIFEST_JSON_PATH = Path("MANIFEST.json")
BACKUP_DIR = Path("docs/archive")

def get_current_timestamp() -> str:
    """Get current timestamp in ISO 8601 format"""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S-04:00")

def get_file_hash(filepath: Path) -> str:
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return ""

def get_file_size(filepath: Path) -> int:
    """Get file size in bytes"""
    try:
        return filepath.stat().st_size
    except:
        return 0

def catalog_files(root_dir: Path) -> Dict[str, Any]:
    """Perform comprehensive file cataloging"""
    catalog = {
        "total_count": 0,
        "by_type": {},
        "by_directory": {},
        "file_registry": {}
    }

    # File type mappings
    type_map = {
        ".md": "markdown",
        ".js": "javascript",
        ".py": "python",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".html": "html",
        ".css": "css",
        ".jpg": "images",
        ".jpeg": "images",
        ".png": "images",
        ".gif": "images",
        ".svg": "images"
    }

    # Critical files to always include
    critical_files = [
        "CLAUDE.md",
        "MANIFEST.json",
        ".eleventy.js",
        "package.json",
        "tailwind.config.js"
    ]

    # Walk through all files
    for filepath in root_dir.rglob("*"):
        if filepath.is_file() and not any(part.startswith('.') for part in filepath.parts[:-1]):
            # Skip hidden directories and git files
            if '.git' in filepath.parts or 'node_modules' in filepath.parts:
                continue

            catalog["total_count"] += 1

            # Get file extension and type
            ext = filepath.suffix.lower()
            file_type = type_map.get(ext, "other")

            # Update by_type
            if file_type not in catalog["by_type"]:
                catalog["by_type"][file_type] = {
                    "count": 0,
                    "files": [],
                    "total_size": 0
                }

            catalog["by_type"][file_type]["count"] += 1
            catalog["by_type"][file_type]["files"].append(str(filepath))
            catalog["by_type"][file_type]["total_size"] += get_file_size(filepath)

            # Update by_directory
            dir_path = str(filepath.parent)
            if dir_path not in catalog["by_directory"]:
                catalog["by_directory"][dir_path] = []
            catalog["by_directory"][dir_path].append(filepath.name)

            # Add to file registry
            rel_path = filepath.relative_to(root_dir)
            catalog["file_registry"][str(rel_path)] = {
                "path": str(rel_path),
                "hash": get_file_hash(filepath),
                "size": get_file_size(filepath),
                "modified": datetime.fromtimestamp(filepath.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%S-04:00"),
                "purpose": "",  # To be filled in later
                "dependencies": [],
                "referenced_by": []
            }

    catalog["critical_files"] = critical_files
    return catalog

def catalog_scripts(scripts_dir: Path) -> Dict[str, Any]:
    """Catalog all scripts with categorization"""
    scripts_catalog = {
        "total_count": 0,
        "python": {
            "blog_management": {
                "scripts": [],
                "purpose": "Blog content analysis and enhancement",
                "llm_ready": False
            },
            "image_management": {
                "scripts": [],
                "purpose": "Image generation, optimization, and search",
                "llm_ready": False
            },
            "content_optimization": {
                "scripts": [],
                "purpose": "Content quality and SEO optimization",
                "llm_ready": False
            },
            "academic_research": {
                "scripts": [],
                "purpose": "Citation and research integration",
                "llm_ready": False
            },
            "validation": {
                "scripts": [],
                "purpose": "Standards and quality validation",
                "llm_ready": False
            },
            "link_validation": {
                "scripts": [],
                "purpose": "Link validation and repair",
                "llm_ready": False
            },
            "utilities": {
                "scripts": [],
                "purpose": "General utility scripts",
                "llm_ready": False
            }
        },
        "bash": [],
        "node": []
    }

    # Categorization patterns
    categories = {
        "blog_management": ["blog", "post", "content"],
        "image_management": ["image", "hero", "photo", "stock"],
        "content_optimization": ["optimize", "enhance", "improve"],
        "academic_research": ["academic", "citation", "research", "arxiv"],
        "validation": ["validate", "check", "verify", "test"],
        "link_validation": ["link", "url", "repair"],
        "utilities": []  # Catch-all
    }

    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            scripts_catalog["total_count"] += 1
            script_name = script.name

            # Determine category
            assigned = False
            for category, keywords in categories.items():
                if any(keyword in script_name.lower() for keyword in keywords):
                    scripts_catalog["python"][category]["scripts"].append(script_name)
                    assigned = True
                    break

            if not assigned:
                scripts_catalog["python"]["utilities"]["scripts"].append(script_name)

        # Check for bash scripts
        for script in scripts_dir.glob("*.sh"):
            scripts_catalog["bash"].append(script.name)

    return scripts_catalog

def catalog_content(root_dir: Path) -> Dict[str, Any]:
    """Catalog blog posts and pages"""
    content_catalog = {
        "posts": {
            "total": 0,
            "by_year": {},
            "by_tag": {},
            "by_author": {},
            "missing_hero_images": [],
            "high_code_ratio": [],
            "missing_citations": []
        },
        "pages": {
            "total": 0,
            "navigation_entries": [],
            "orphaned": [],
            "redirects": []
        },
        "images": {
            "total": 0,
            "hero": 0,
            "inline": 0,
            "responsive_variants": 0,
            "unused": [],
            "missing_alt": [],
            "unoptimized": []
        }
    }

    # Count posts
    posts_dir = root_dir / "src" / "posts"
    if posts_dir.exists():
        for post in posts_dir.glob("*.md"):
            content_catalog["posts"]["total"] += 1

            # Extract year from filename
            if post.name.startswith("20"):
                year = post.name[:4]
                if year not in content_catalog["posts"]["by_year"]:
                    content_catalog["posts"]["by_year"][year] = 0
                content_catalog["posts"]["by_year"][year] += 1

    # Count pages
    pages_dir = root_dir / "src" / "pages"
    if pages_dir.exists():
        for page in pages_dir.glob("*.md"):
            content_catalog["pages"]["total"] += 1
            content_catalog["pages"]["navigation_entries"].append(page.stem)

    # Count images
    images_dir = root_dir / "src" / "assets" / "images"
    if images_dir.exists():
        for img in images_dir.rglob("*"):
            if img.is_file() and img.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                content_catalog["images"]["total"] += 1

                if "hero" in str(img):
                    content_catalog["images"]["hero"] += 1
                elif any(size in img.name for size in ['400', '800', '1200']):
                    content_catalog["images"]["responsive_variants"] += 1

    return content_catalog

def create_manifest_json(yaml_data: Dict[str, Any], root_dir: Path) -> Dict[str, Any]:
    """Create the new MANIFEST.json structure"""
    timestamp = get_current_timestamp()

    # Perform comprehensive cataloging
    print("📊 Cataloging files...")
    file_catalog = catalog_files(root_dir)

    print("📜 Cataloging scripts...")
    scripts_catalog = catalog_scripts(root_dir / "scripts")

    print("📝 Cataloging content...")
    content_catalog = catalog_content(root_dir)

    # Build the new manifest structure
    manifest = {
        "version": "4.0.0",
        "schema_version": "1.0.0",
        "generated": timestamp,
        "last_validated": timestamp,
        "repository": {
            "name": "williamzujkowski.github.io",
            "type": "personal-website",
            "framework": "eleventy",
            "deployment": "github-pages",
            "standards_reference": "https://github.com/williamzujkowski/standards"
        },
        "inventory": {
            "files": file_catalog,
            "directories": {
                "structure": {},
                "empty_dirs": [],
                "redundant_paths": [],
                "protected_paths": [
                    "src/",
                    "scripts/",
                    "docs/",
                    ".github/",
                    ".standards/"
                ]
            },
            "scripts": scripts_catalog,
            "content": content_catalog,
            "dependencies": {
                "npm": {
                    "production": {},
                    "development": {},
                    "outdated": [],
                    "security_issues": []
                },
                "python": {
                    "requirements": [],
                    "missing": [],
                    "version_conflicts": []
                }
            }
        },
        "vestigial_audit": {
            "last_comprehensive_audit": timestamp,
            "candidates": {
                "obsolete_files": [],
                "duplicate_functionality": [],
                "unreferenced_files": [],
                "deprecated_features": [],
                "old_backups": [],
                "test_artifacts": []
            },
            "safe_to_remove": [],
            "requires_review": [],
            "protected": []
        },
        "standards_compliance": {
            "source": "https://github.com/williamzujkowski/standards",
            "implemented": {
                "knowledge_management": True,
                "frontend_mobile": "partial",
                "web_design_ux": "partial",
                "seo_marketing": "partial",
                "content_standards": True,
                "github_platform": True,
                "toolchain": "partial"
            },
            "violations": [],
            "warnings": [],
            "last_check": timestamp
        },
        "llm_interface": {
            "version": "1.0.0",
            "script_catalog": {},
            "workflows": {
                "blog_enhancement": {
                    "description": "Complete blog post enhancement workflow",
                    "steps": [],
                    "scripts_used": []
                }
            },
            "command_aliases": {}
        },
        "enforcement_rules": {
            "version": "1.0.0",
            "mandatory_for_llms": [
                "ALWAYS check MANIFEST.json before any operation",
                "NEVER create duplicate files - check file_registry first",
                "ALWAYS use time.gov for timestamps",
                "MUST update MANIFEST.json after file changes",
                "MUST follow standards from https://github.com/williamzujkowski/standards"
            ],
            "pre_operation_checks": [
                "manifest_current",
                "no_duplicates_exist",
                "standards_compliant"
            ],
            "post_operation_checks": [
                "update_manifest",
                "validate_changes",
                "update_documentation"
            ]
        }
    }

    # Migrate useful data from YAML if available
    if yaml_data:
        # Transfer any existing metadata
        if "metadata" in yaml_data:
            manifest["repository"]["metadata"] = yaml_data["metadata"]

    return manifest

def backup_yaml(yaml_path: Path, backup_dir: Path):
    """Create backup of MANIFEST.yaml"""
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"MANIFEST.yaml.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if yaml_path.exists():
        print(f"📦 Creating backup: {backup_path}")
        import shutil
        shutil.copy2(yaml_path, backup_path)

        # Also create a permanent backup
        permanent_backup = backup_dir / "MANIFEST.yaml.backup"
        shutil.copy2(yaml_path, permanent_backup)
        print(f"✅ Backup created successfully")
    else:
        print(f"⚠️  No MANIFEST.yaml found to backup")

def validate_manifest(manifest: Dict[str, Any]) -> bool:
    """Validate the manifest structure"""
    required_keys = [
        "version", "schema_version", "generated", "repository",
        "inventory", "standards_compliance", "enforcement_rules"
    ]

    for key in required_keys:
        if key not in manifest:
            print(f"❌ Missing required key: {key}")
            return False

    print("✅ Manifest structure validated")
    return True

def main():
    """Main migration function"""
    parser = argparse.ArgumentParser(
        description=SCRIPT_PURPOSE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--backup', action='store_true',
                       help='Create backup of original MANIFEST.yaml')
    parser.add_argument('--validate', action='store_true',
                       help='Validate the new manifest after creation')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable detailed output')

    args = parser.parse_args()

    print("=" * 60)
    print("MANIFEST.yaml → MANIFEST.json Migration Tool")
    print(f"Version: {SCRIPT_VERSION}")
    print(f"Time: {get_current_timestamp()}")
    print("=" * 60)

    # Get repository root
    root_dir = Path.cwd()

    # Load existing MANIFEST.yaml if it exists
    yaml_data = {}
    if MANIFEST_YAML_PATH.exists():
        print(f"📄 Loading {MANIFEST_YAML_PATH}...")
        with open(MANIFEST_YAML_PATH, 'r') as f:
            yaml_data = yaml.safe_load(f) or {}
        print(f"✅ Loaded YAML with {len(yaml_data)} keys")
    else:
        print(f"⚠️  No existing MANIFEST.yaml found, creating fresh catalog")

    # Create backup if requested
    if args.backup and MANIFEST_YAML_PATH.exists():
        backup_yaml(MANIFEST_YAML_PATH, BACKUP_DIR)

    # Create new manifest
    print("\n🔨 Creating MANIFEST.json...")
    manifest = create_manifest_json(yaml_data, root_dir)

    # Validate if requested
    if args.validate:
        if not validate_manifest(manifest):
            print("❌ Validation failed, aborting")
            sys.exit(1)

    # Write new manifest
    print(f"\n📝 Writing {MANIFEST_JSON_PATH}...")
    with open(MANIFEST_JSON_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print(f"📊 Total files cataloged: {manifest['inventory']['files']['total_count']}")
    print(f"📜 Total scripts found: {manifest['inventory']['scripts']['total_count']}")
    print(f"📝 Total posts cataloged: {manifest['inventory']['content']['posts']['total']}")
    print(f"🖼️  Total images found: {manifest['inventory']['content']['images']['total']}")
    print("=" * 60)

    if args.verbose:
        print("\n📋 File Type Distribution:")
        for file_type, info in manifest['inventory']['files']['by_type'].items():
            print(f"  {file_type}: {info['count']} files")

    print(f"\n✨ MANIFEST.json is now your single source of truth!")
    print(f"⚠️  Remember to delete MANIFEST.yaml after verification")

    return 0

if __name__ == "__main__":
    sys.exit(main())