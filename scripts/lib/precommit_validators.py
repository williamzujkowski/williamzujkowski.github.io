#!/usr/bin/env -S uv run python3
"""
Pre-commit validation functions for parallel execution.

Each validator is independent and can run concurrently.
All validators return (success: bool, message: str).

UPDATED: 2025-11-01 - Added lazy loading support for MANIFEST v5.0
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any

# Import lazy loader for MANIFEST v5.0
try:
    from lib.manifest_loader import ManifestLoader
    LAZY_LOADING_AVAILABLE = True
except ImportError:
    LAZY_LOADING_AVAILABLE = False


def validate_manifest() -> Tuple[bool, str]:
    """
    Validate MANIFEST.json exists and has valid structure.

    Returns:
        (success, message)
    """
    manifest_path = Path("MANIFEST.json")
    if not manifest_path.exists():
        return False, "MANIFEST.json not found"

    try:
        with open(manifest_path) as f:
            manifest = json.load(f)

        if "version" not in manifest:
            return False, "Missing version field"

        return True, f"Valid (version {manifest.get('version', 'unknown')})"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error reading manifest: {e}"


def check_duplicates() -> Tuple[bool, str]:
    """
    Check for duplicate files in staged changes.

    OPTIMIZED: Uses lazy loading for MANIFEST v5.0.
    Only loads full registry if hash check indicates potential conflicts.

    Returns:
        (success, message)
    """
    # Get staged files
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    staged_files = [f for f in result.stdout.strip().split('\n') if f]

    if not staged_files:
        return True, "No files staged"

    # Load manifest (use lazy loader if available)
    try:
        if LAZY_LOADING_AVAILABLE:
            loader = ManifestLoader()
            manifest = loader.get_core()
            # Lazy-load file registry (only loads if needed)
            file_registry = loader.get_file_registry()
        else:
            # Fallback: load full manifest (v4.0 compatible)
            with open('MANIFEST.json') as f:
                manifest = json.load(f)
            file_registry = manifest.get('inventory', {}).get('files', {}).get('file_registry', {})

        allowed_duplicates = manifest.get('project_overrides', {}).get('allowed_duplicates', [])
    except Exception as e:
        # Graceful degradation
        file_registry = {}
        allowed_duplicates = []

    # Build allowed duplicate pairs
    allowed_pairs = set()
    for override in allowed_duplicates:
        project_file = override.get('project_file', '')
        standards_file = override.get('standards_file', '')
        if project_file and standards_file:
            allowed_pairs.add((project_file, standards_file))
            allowed_pairs.add((standards_file, project_file))

    # Check for duplicates
    duplicates = []
    for staged in staged_files:
        # Skip .standards/ submodule files
        if staged.startswith('.standards/'):
            continue

        staged_name = Path(staged).name

        # Skip README.md - they're directory-specific
        if staged_name == 'README.md':
            continue

        for registered in file_registry.keys():
            if registered.startswith('.standards/'):
                continue

            if Path(registered).name == staged_name and registered != staged:
                if (staged, registered) not in allowed_pairs:
                    duplicates.append((staged, registered))

    if duplicates:
        error_lines = ["Duplicate files detected:"]
        for new, existing in duplicates[:5]:  # Limit to 5 for brevity
            error_lines.append(f"  {new} duplicates {existing}")
        if len(duplicates) > 5:
            error_lines.append(f"  ... and {len(duplicates) - 5} more")
        return False, "\n".join(error_lines)

    return True, f"No duplicates in {len(staged_files)} staged files"


def check_standards_compliance() -> Tuple[bool, str]:
    """
    Check that .claude-rules.json is valid.

    Returns:
        (success, message)
    """
    rules_path = Path(".claude-rules.json")
    if not rules_path.exists():
        return True, "No .claude-rules.json (optional)"

    try:
        with open(rules_path) as f:
            rules = json.load(f)
        return True, f"Standards rules loaded ({len(rules)} sections)"
    except json.JSONDecodeError as e:
        return False, f"Invalid .claude-rules.json: {e}"
    except Exception as e:
        return False, f"Error loading standards: {e}"


def validate_humanization_scores() -> Tuple[bool, str]:
    """
    Check humanization scores for modified blog posts.

    Returns:
        (success, message)
    """
    # Get modified markdown files in src/posts/
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get modified files"

    modified_files = result.stdout.strip().split('\n') if result.stdout else []

    # Filter for blog posts (exclude welcome.md)
    modified_posts = [
        f for f in modified_files
        if f.startswith('src/posts/') and f.endswith('.md') and 'welcome.md' not in f
    ]

    if not modified_posts:
        return True, "No blog posts modified"

    # Validate each post
    failed_posts = []
    for post in modified_posts:
        if not Path(post).exists():
            continue

        # Run humanization validator
        result = subprocess.run(
            ['uv', 'run', 'python', 'scripts/blog-content/humanization-validator.py',
             '--post', post, '--output', 'json'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            failed_posts.append((post, 0, 'validation error'))
            continue

        # Parse JSON output
        try:
            data = json.loads(result.stdout)
            score = data.get('score', 0)

            if score < 75:
                failed_posts.append((post, score, 'below threshold'))
        except json.JSONDecodeError:
            failed_posts.append((post, 0, 'parse error'))

    if failed_posts:
        error_lines = ["Humanization scores below 75/100:"]
        for post, score, reason in failed_posts[:3]:
            error_lines.append(f"  {Path(post).name}: {score}/100 ({reason})")
        if len(failed_posts) > 3:
            error_lines.append(f"  ... and {len(failed_posts) - 3} more")
        error_lines.append("\nFix posts or use --no-verify (not recommended)")
        return False, "\n".join(error_lines)

    return True, f"All {len(modified_posts)} posts meet standards (≥75/100)"


def check_code_ratios() -> Tuple[bool, str]:
    """
    Check code-to-content ratio for blog posts (<25%).

    Returns:
        (success, message)
    """
    # Get modified blog posts
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get modified files"

    modified_files = result.stdout.strip().split('\n') if result.stdout else []

    # Filter for blog posts
    modified_posts = [
        f for f in modified_files
        if f.startswith('src/posts/') and f.endswith('.md') and 'welcome.md' not in f
    ]

    if not modified_posts:
        return True, "No blog posts modified"

    # Analyze each post
    violations = []
    for post_file in modified_posts:
        if not Path(post_file).exists():
            continue

        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2]

            # Count lines
            total_lines = len(content.split('\n'))

            # Extract code blocks (EXCLUDE mermaid diagrams)
            # Pattern: Match ``` followed by optional language, but NOT mermaid
            code_blocks = re.findall(r'```(?!mermaid).*?\n(.*?)```', content, re.DOTALL)
            code_lines = sum(len(block.split('\n')) for block in code_blocks)

            # Calculate ratio
            code_ratio = (code_lines / total_lines * 100) if total_lines > 0 else 0

            if code_ratio > 25:
                violations.append((Path(post_file).name, code_ratio, code_lines, total_lines))
        except Exception as e:
            # Don't fail the whole check for one file error
            continue

    if violations:
        error_lines = ["Code ratio violations detected:"]
        for filename, ratio, code_lines, total_lines in violations:
            error_lines.append(f"  {filename}: {ratio:.1f}% (threshold: 25%)")
            error_lines.append(f"    Code lines: {code_lines} / Total lines: {total_lines}")
        error_lines.append("\nTip: Extract code to gists or reduce code examples.")
        error_lines.append("See: docs/context/workflows/gist-management.md")
        error_lines.append("Run: uv run python scripts/blog-content/optimize-blog-content.py")
        return False, "\n".join(error_lines)

    return True, f"All {len(modified_posts)} posts <25% code ratio"


def check_image_variants() -> Tuple[bool, str]:
    """
    Prevent recursive image variants from being committed.

    Returns:
        (success, message)
    """
    # Get staged files with status
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-status"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    staged_lines = result.stdout.strip().split('\n') if result.stdout else []

    # Check for recursive image patterns
    recursive_pattern = re.compile(r'.*-\d+-\d+.*\.(jpg|png|webp)$')
    problem_files = []

    for line in staged_lines:
        if not line:
            continue
        parts = line.split('\t', 1)
        if len(parts) < 2:
            continue
        status, filepath = parts[0], parts[1]

        # Only flag Added (A) or Modified (M), not Deleted (D)
        if status in ('A', 'M') and recursive_pattern.match(filepath):
            problem_files.append(filepath)

    if problem_files:
        error_lines = ["Recursive image variants detected!"]
        error_lines.append("Files matching *-###-###.* pattern:")
        for f in problem_files[:5]:
            error_lines.append(f"  {f}")
        if len(problem_files) > 5:
            error_lines.append(f"  ... and {len(problem_files) - 5} more")
        error_lines.append("\nRun: find src/assets/images/blog/ -regex \".*-[0-9]+-[0-9]+.*\" -delete")
        return False, "\n".join(error_lines)

    # Warn if image count is high (but don't fail)
    result = subprocess.run(
        ['find', 'src/assets/images/blog/', '-type', 'f'],
        capture_output=True,
        text=True
    )
    img_count = len([l for l in result.stdout.strip().split('\n') if l])

    if img_count > 300:
        return True, f"No recursive variants (warning: {img_count} images > 300 threshold)"

    return True, f"No recursive image variants ({img_count} images)"


def update_manifest() -> Tuple[bool, str]:
    """
    Update MANIFEST.json with current timestamp and stage it.

    OPTIMIZED: For MANIFEST v5.0, only updates timestamp in core file.
    File registry updates handled separately by manifest_loader.

    Note: This should run AFTER all other validators pass.

    Returns:
        (success, message)
    """
    # Get staged files
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    staged_files = [f for f in result.stdout.strip().split('\n') if f]

    if not staged_files:
        return True, "No changes to manifest needed"

    try:
        # Load manifest (small core only for v5.0)
        with open('MANIFEST.json') as f:
            manifest = json.load(f)

        # Update timestamp
        from datetime import datetime
        manifest['last_validated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-04:00')

        # Save manifest
        with open('MANIFEST.json', 'w') as f:
            json.dump(manifest, f, indent=2)

        # Stage the updated manifest
        result = subprocess.run(['git', 'add', 'MANIFEST.json'])
        if result.returncode != 0:
            return False, "Failed to stage MANIFEST.json"

        # If v5.0, also stage .manifest/ files if they changed
        schema = manifest.get('schema', '')
        if 'optimized' in schema or manifest.get('version', '').startswith('5.'):
            # Stage .manifest directory if it exists
            manifest_dir = Path('.manifest')
            if manifest_dir.exists():
                subprocess.run(['git', 'add', '.manifest/'], check=False)

        return True, f"Updated for {len(staged_files)} staged files"
    except Exception as e:
        return False, f"Failed to update manifest: {e}"


# Registry of all validators
VALIDATORS = {
    "manifest_validation": validate_manifest,
    "duplicate_check": check_duplicates,
    "standards_compliance": check_standards_compliance,
    "humanization_scores": validate_humanization_scores,
    "code_ratios": check_code_ratios,
    "image_variants": check_image_variants,
}

# Validators that must run sequentially AFTER parallel checks pass
SEQUENTIAL_VALIDATORS = {
    "manifest_update": update_manifest,
}


def main():
    """Test all validators."""
    print("Testing all validators...\n")

    for name, validator in VALIDATORS.items():
        success, message = validator()
        status = "✅" if success else "❌"
        print(f"{status} {name}:")
        for line in message.split('\n'):
            print(f"  {line}")
        print()

    print("\nSequential validators:")
    for name, validator in SEQUENTIAL_VALIDATORS.items():
        success, message = validator()
        status = "✅" if success else "❌"
        print(f"{status} {name}:")
        for line in message.split('\n'):
            print(f"  {line}")


if __name__ == "__main__":
    main()
