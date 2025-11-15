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
import yaml
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

    FIX: Handles git rename operations (git mv) correctly.
    Renames are tracked as R100 status and should be excluded from duplicate checking.

    Returns:
        (success, message)
    """
    # Get staged files with status to detect renames
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-status"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    staged_lines = result.stdout.strip().split('\n') if result.stdout else []

    # Parse status and filenames
    # Status format: "STATUS\tFILE" or "R###\tOLD_FILE\tNEW_FILE" for renames
    staged_files = []
    rename_pairs = set()

    for line in staged_lines:
        if not line:
            continue
        parts = line.split('\t')
        status = parts[0]

        if status.startswith('R'):  # Rename operation (R100, R095, etc.)
            if len(parts) >= 3:
                old_path = parts[1]
                new_path = parts[2]
                # Track both paths as part of rename
                rename_pairs.add((old_path, new_path))
                rename_pairs.add((new_path, old_path))
                staged_files.append(new_path)  # Still check new path for other duplicates
        elif len(parts) >= 2:
            # Normal add/modify/delete
            staged_files.append(parts[1])

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
                # Skip if this is part of a rename operation
                if (staged, registered) in rename_pairs or (registered, staged) in rename_pairs:
                    continue

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


def _skip_frontmatter_inline(lines: List[str]) -> int:
    """
    Helper: Find the end of YAML frontmatter and return the starting index for content.

    This is an inline copy of skip_frontmatter() from code-ratio-calculator.py
    to avoid circular import dependencies in pre-commit hooks.

    Args:
        lines: All lines from the markdown file

    Returns:
        Index of first line after frontmatter (0-indexed)
    """
    if not lines or not lines[0].strip().startswith("---"):
        return 0

    # Find the closing --- marker
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1

    # No closing marker found, treat as no frontmatter
    return 0


def _extract_code_blocks_inline(lines: List[str], content_start: int) -> Tuple[int, int]:
    """
    Helper: Extract all code blocks from content lines and count total code lines.

    This is an inline copy of extract_code_blocks() from code-ratio-calculator.py
    to avoid circular import dependencies in pre-commit hooks.

    METHODOLOGY:
    -----------
    1. Iterate through lines starting after frontmatter
    2. Detect opening ``` fence (with optional language identifier)
    3. Count non-blank lines until closing ``` fence
    4. Store line count per block
    5. Exclude fence markers themselves from all counts
    6. Include ALL code blocks (including Mermaid diagrams)

    NOTE: Mermaid diagrams are counted as code because they contribute to
    technical density and can make posts harder to read for non-technical audiences.

    Args:
        lines: All lines from the markdown file
        content_start: Index where content begins (after frontmatter)

    Returns:
        Tuple of (number of code blocks, total code lines)
    """
    num_blocks = 0
    total_code_lines = 0
    in_code_block = False
    current_block_lines = 0

    for i in range(content_start, len(lines)):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code_block:
                # Opening fence
                in_code_block = True
                current_block_lines = 0
            else:
                # Closing fence - count all code blocks
                num_blocks += 1
                total_code_lines += current_block_lines
                in_code_block = False
        elif in_code_block:
            # Count non-blank lines within code block
            if stripped:  # Non-empty line
                current_block_lines += 1

    # Handle unclosed code block
    if in_code_block:
        num_blocks += 1
        total_code_lines += current_block_lines

    return num_blocks, total_code_lines


def _count_content_lines_inline(lines: List[str], content_start: int) -> int:
    """
    Helper: Count total content lines, excluding frontmatter and code fence markers.

    This is an inline copy of count_content_lines() from code-ratio-calculator.py
    to avoid circular import dependencies in pre-commit hooks.

    METHODOLOGY:
    -----------
    - Count ALL lines after frontmatter (including blank lines)
    - Exclude the ``` fence markers themselves
    - Include blank lines in content count (they affect readability/structure)

    Args:
        lines: All lines from the markdown file
        content_start: Index where content begins (after frontmatter)

    Returns:
        Number of content lines
    """
    total_lines = 0
    in_code_block = False

    for i in range(content_start, len(lines)):
        line = lines[i].strip()

        if line.startswith("```"):
            in_code_block = not in_code_block
            # Do NOT count the fence marker itself
            continue

        # Count all other lines (including blanks)
        total_lines += 1

    return total_lines


def check_code_ratios() -> Tuple[bool, str]:
    """
    Check code-to-content ratio for blog posts (<25%).

    Uses the AUTHORITATIVE code-ratio-calculator.py which includes:
    - Mermaid diagram detection and separate tracking
    - DIAGRAM-HEAVY policy exceptions (>80% Mermaid + <10% actual code)
    - Accurate line-by-line parsing

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

    # Use the authoritative calculator with DIAGRAM-HEAVY detection
    violations = []
    for post_file in modified_posts:
        if not Path(post_file).exists():
            continue

        try:
            # Call the authoritative calculator
            result = subprocess.run(
                ["uv", "run", "python", "scripts/blog-content/code-ratio-calculator.py", "--post", post_file, "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                continue

            data = json.loads(result.stdout)

            # Check if post violates threshold AND is not DIAGRAM-HEAVY
            code_ratio = data.get('code_ratio', 0)
            is_diagram_heavy = data.get('is_diagram_heavy', False)

            # Violation only if exceeds threshold AND not DIAGRAM-HEAVY exception
            if code_ratio > 25 and not is_diagram_heavy:
                violations.append((
                    Path(post_file).name,
                    code_ratio,
                    data.get('total_code_lines', 0),
                    data.get('total_lines', 0)
                ))

        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
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
        error_lines.append("\nNote: DIAGRAM-HEAVY posts (>80% Mermaid) are exempt from ratio checks")
        return False, "\n".join(error_lines)

    return True, f"All {len(modified_posts)} posts <25% code ratio (DIAGRAM-HEAVY exceptions applied)"


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


def validate_token_budgets() -> Tuple[bool, str]:
    """
    Validate that INDEX.yaml token estimates are accurate for modified modules.

    Uses measured word counts and proven 1.33 tokens/word ratio (not the old 6.2
    ratio that caused 97.5% overestimation in Phase 1).

    UPDATED (P2 Session 41): Changed from WARNING to BLOCKING for >20% variance.
    Stricter enforcement prevents token budget drift at commit time.

    Returns:
        (success, message)
    """
    # Check if INDEX.yaml exists
    index_path = Path("docs/context/INDEX.yaml")
    if not index_path.exists():
        return True, "INDEX.yaml not found (skipping)"

    # Get modified context module files
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    modified_files = result.stdout.strip().split('\n') if result.stdout else []

    # Filter for docs/context/ modules (markdown files)
    modified_modules = [
        f for f in modified_files
        if f.startswith('docs/context/') and f.endswith('.md')
    ]

    if not modified_modules:
        return True, "No context modules modified"

    # Load INDEX.yaml
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index = yaml.safe_load(f)
    except Exception as e:
        return False, f"Failed to load INDEX.yaml: {e}"

    # Build module lookup from INDEX.yaml
    module_estimates = {}
    for category_name, category_data in index.get('categories', {}).items():
        if not isinstance(category_data, dict):
            continue
        for module in category_data.get('modules', []):
            if not isinstance(module, dict):
                continue
            file_path = module.get('file', '')
            estimated_tokens = module.get('estimated_tokens', 0)
            module_name = module.get('name', '')
            if file_path:
                module_estimates[file_path] = {
                    'name': module_name,
                    'estimated': estimated_tokens,
                    'category': category_name
                }

    # Check each modified module
    warnings = []
    for module_file in modified_modules:
        if module_file not in module_estimates:
            # Module not in INDEX.yaml yet (probably new)
            continue

        module_info = module_estimates[module_file]
        estimated = module_info['estimated']

        # Calculate actual tokens from word count
        try:
            with open(module_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count words (split on whitespace)
            words = content.split()
            word_count = len(words)

            # Use proven 1.33 tokens/word ratio (validated by tester agent)
            # Round to nearest 50 for readability
            actual_tokens = round((word_count * 1.33) / 50) * 50

            # Calculate variance percentage
            if estimated > 0:
                variance = abs(actual_tokens - estimated) / estimated * 100

                # Warn if >20% variance
                if variance > 20:
                    warnings.append({
                        'file': module_file,
                        'name': module_info['name'],
                        'category': module_info['category'],
                        'estimated': estimated,
                        'actual': actual_tokens,
                        'variance': variance,
                        'word_count': word_count
                    })
        except Exception as e:
            # Don't fail the whole check for one file error
            continue

    if warnings:
        error_lines = ["❌ Token budget variance >20% (BLOCKING):"]
        for w in warnings[:3]:  # Limit to 3 for brevity
            error_lines.append(
                f"  {w['category']}/{w['name']}: "
                f"{w['estimated']} → {w['actual']} tokens "
                f"({w['variance']:.0f}% variance, {w['word_count']} words)"
            )
        if len(warnings) > 3:
            error_lines.append(f"  ... and {len(warnings) - 3} more")
        error_lines.append("\n🔧 FIX: Update INDEX.yaml token estimates")
        error_lines.append("  Option 1 (Automatic): uv run python scripts/validation/fix-index-token-budgets.py")
        error_lines.append("  Option 2 (Manual): Update estimated_tokens in INDEX.yaml")
        error_lines.append("  Formula: (word_count * 1.33), rounded-sm to nearest 50")
        error_lines.append("\nThen stage INDEX.yaml and retry commit")

        # CHANGED (P2): Return False to BLOCK commit instead of warning
        return False, "\n".join(error_lines)

    return True, f"Token budgets accurate for {len(modified_modules)} modified modules"


def check_python_logging() -> Tuple[bool, str]:
    """
    Enforce proper logging usage in Python scripts.

    PROBLEM: Only 5% of scripts use scripts/lib/logging_config.py
    SOLUTION: Reject commits with print() statements in scripts/ directory

    Returns:
        (success, message)
    """
    # Get modified/added Python files in scripts/ directory
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    modified_files = result.stdout.strip().split('\n') if result.stdout else []

    # Filter for Python scripts in scripts/ directory
    python_scripts = [
        f for f in modified_files
        if f.startswith('scripts/') and f.endswith('.py')
    ]

    if not python_scripts:
        return True, "No Python scripts modified"

    # Exempt the logging_config.py itself
    python_scripts = [
        f for f in python_scripts
        if not f.endswith('lib/logging_config.py')
    ]

    # Check each script for print() statements
    violations = []
    for script_file in python_scripts:
        if not Path(script_file).exists():
            continue

        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find print() statements
            # Pattern: print( but not in comments or docstrings
            lines = content.split('\n')
            in_docstring = False
            docstring_delim = None

            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()

                # Track docstring state (multi-line docstrings)
                # Check for triple quotes
                triple_double = '"""'
                triple_single = "'''"

                # Count occurrences of triple quotes in line
                double_count = line.count(triple_double)
                single_count = line.count(triple_single)

                if not in_docstring:
                    # Check if docstring is starting
                    if double_count > 0:
                        in_docstring = True
                        docstring_delim = triple_double
                        # If there are 2+ occurrences, it's a one-line docstring
                        if double_count >= 2:
                            in_docstring = False
                        continue
                    elif single_count > 0:
                        in_docstring = True
                        docstring_delim = triple_single
                        if single_count >= 2:
                            in_docstring = False
                        continue
                else:
                    # We're in a docstring, check if it's ending
                    if docstring_delim in line:
                        in_docstring = False
                        docstring_delim = None
                    continue

                # Skip comments and lines inside docstrings
                if stripped.startswith('#'):
                    continue

                # Check for print( statements
                # Skip if line has noqa comment (intentional print for data output)
                if re.search(r'\bprint\s*\(', line) and '# noqa' not in line:
                    violations.append((script_file, line_num, stripped[:60]))

        except Exception as e:
            # Don't fail the whole check for one file error
            continue

    if violations:
        error_lines = ["❌ Python scripts using print() instead of logging:"]
        error_lines.append("")

        # Group by file
        files_with_violations = {}
        for filepath, line_num, content in violations:
            if filepath not in files_with_violations:
                files_with_violations[filepath] = []
            files_with_violations[filepath].append((line_num, content))

        for filepath, lines in sorted(files_with_violations.items())[:5]:
            error_lines.append(f"  📄 {filepath}")
            for line_num, content in lines[:3]:
                error_lines.append(f"     Line {line_num}: {content}...")
            if len(lines) > 3:
                error_lines.append(f"     ... and {len(lines) - 3} more")
            error_lines.append("")

        if len(files_with_violations) > 5:
            error_lines.append(f"  ... and {len(files_with_violations) - 5} more files")
            error_lines.append("")

        error_lines.append("🔧 FIX:")
        error_lines.append("  1. Import logging: from logging_config import setup_logger")
        error_lines.append("  2. Setup logger: logger = setup_logger(__name__)")
        error_lines.append("  3. Replace print() with:")
        error_lines.append("     - logger.info()   # User-facing messages")
        error_lines.append("     - logger.debug()  # Developer debugging")
        error_lines.append("     - logger.warning() # Warnings")
        error_lines.append("     - logger.error()  # Errors")
        error_lines.append("")
        error_lines.append("📖 See: docs/guides/PYTHON_BEST_PRACTICES.md")
        return False, "\n".join(error_lines)

    return True, f"All {len(python_scripts)} scripts use proper logging"


def check_nda_compliance() -> Tuple[bool, str]:
    """
    Check blog posts for NDA compliance violations.

    PROBLEM: Manual NDA review is error-prone and time-consuming
    SOLUTION: Automated pattern detection for forbidden phrases and patterns

    Validates:
    - No recent work timeline references (2-3 year buffer required)
    - No current employer/team references
    - No active vulnerability disclosures
    - Accurate family information (one child, correct age)
    - Time-buffered professional references

    Returns:
        (success, message)
    """
    # Load NDA patterns
    patterns_file = Path("scripts/validation/nda-patterns.yaml")
    if not patterns_file.exists():
        return True, "NDA patterns file not found (skipping)"

    try:
        with open(patterns_file, 'r', encoding='utf-8') as f:
            nda_patterns = yaml.safe_load(f)
    except Exception as e:
        return False, f"Failed to load NDA patterns: {e}"

    # Get modified blog posts
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    modified_files = result.stdout.strip().split('\n') if result.stdout else []

    # Filter for blog posts (exclude welcome.md)
    blog_posts = [
        f for f in modified_files
        if f.startswith('src/posts/') and f.endswith('.md') and 'welcome.md' not in f
    ]

    if not blog_posts:
        return True, "No blog posts modified"

    # Check each post for violations
    violations = []

    for post_file in blog_posts:
        if not Path(post_file).exists():
            continue

        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            # Remove YAML frontmatter (contains date: 2024-01-01 which triggers false positives)
            import re
            content_no_frontmatter = re.sub(r'^---\n.*?\n---\n', '', raw_content, flags=re.DOTALL)

            # Remove markdown link URLs to avoid false positives from internal links
            # Pattern: [text](/posts/2024-01-01-slug) → [text]()
            content_clean = re.sub(r'\[([^\]]+)\]\(/posts/[^\)]+\)', r'[\1]()', content_no_frontmatter)
            content = content_clean.lower()  # Case-insensitive matching

            post_violations = []

            # Check forbidden time references
            time_patterns = nda_patterns.get('forbidden_time_references', {}).get('patterns', [])
            for pattern in time_patterns:
                if pattern in content:
                    # Check if it's in a work context
                    context_patterns = nda_patterns.get('forbidden_time_references', {}).get('context_required', [])
                    for context in context_patterns:
                        if context in content:
                            post_violations.append({
                                'severity': 'CRITICAL',
                                'pattern': pattern,
                                'category': 'Forbidden Time Reference',
                                'fix': "Use time-buffered references like 'Years ago...'"
                            })
                            break

            # Check forbidden work references
            work_patterns = nda_patterns.get('forbidden_work_references', {}).get('patterns', [])
            for pattern in work_patterns:
                if pattern in content:
                    post_violations.append({
                        'severity': 'CRITICAL',
                        'pattern': pattern,
                        'category': 'Current Work Reference',
                        'fix': "Attribute to homelab or use time buffer"
                    })

            # Check family inaccuracies
            family_patterns = nda_patterns.get('family_inaccuracies', {}).get('patterns', [])
            for pattern in family_patterns:
                if pattern in content:
                    post_violations.append({
                        'severity': 'HIGH',
                        'pattern': pattern,
                        'category': 'Family Inaccuracy',
                        'fix': "Use accurate singular: 'my son' or 'my toddler'"
                    })

            # Check unsafe discovery patterns
            discovery_patterns = nda_patterns.get('unsafe_discovery_patterns', {}).get('patterns', [])
            for pattern in discovery_patterns:
                if pattern in content:
                    post_violations.append({
                        'severity': 'CRITICAL',
                        'pattern': pattern,
                        'category': 'Active Vulnerability Disclosure',
                        'fix': "Use homelab attribution or research framing"
                    })

            if post_violations:
                violations.append({
                    'file': post_file,
                    'violations': post_violations
                })

        except Exception as e:
            # Don't fail entire check for one file error
            continue

    if violations:
        error_lines = ["❌ NDA compliance violations detected:"]
        error_lines.append("")

        for v in violations[:3]:  # Limit to 3 files
            error_lines.append(f"  📄 {Path(v['file']).name}")
            for violation in v['violations'][:5]:  # Limit to 5 violations per file
                error_lines.append(f"     [{violation['severity']}] {violation['category']}")
                error_lines.append(f"       Pattern: '{violation['pattern']}'")
                error_lines.append(f"       Fix: {violation['fix']}")
                error_lines.append("")

            if len(v['violations']) > 5:
                error_lines.append(f"     ... and {len(v['violations']) - 5} more violations")
                error_lines.append("")

        if len(violations) > 3:
            error_lines.append(f"  ... and {len(violations) - 3} more files")
            error_lines.append("")

        error_lines.append("🔧 FIX: Review and update blog posts to remove NDA violations")
        error_lines.append("  Guidance: docs/context/core/nda-compliance.md")
        error_lines.append("  Safe patterns:")
        error_lines.append("    - 'In my homelab...'")
        error_lines.append("    - 'Years ago, I worked on...'")
        error_lines.append("    - 'Research shows...'")

        return False, "\n".join(error_lines)

    return True, f"All {len(blog_posts)} posts pass NDA compliance checks"


def validate_index_yaml() -> Tuple[bool, str]:
    """
    Validate INDEX.yaml structure and token budgets.

    PROBLEM: Session 41 discovered 23.1% token budget underestimate and 2 undocumented modules
    SOLUTION: Automated validation of module counts, file existence, and token accuracy

    Validates:
    - INDEX.yaml exists and has valid structure
    - total_modules matches actual module count in categories
    - Each module file exists on filesystem
    - Token budgets are within 20% variance (blocks commit if >20%)
    - Category module_count matches actual modules in category

    Returns:
        (success, message)
    """
    index_path = Path("docs/context/INDEX.yaml")
    if not index_path.exists():
        return False, "INDEX.yaml not found at docs/context/"

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index = yaml.safe_load(f)
    except Exception as e:
        return False, f"Failed to parse INDEX.yaml: {e}"

    # Validation checks
    errors = []
    warnings = []

    # Check 1: total_modules matches actual count
    total_modules = index.get('total_modules', 0)
    actual_modules = []

    for category_name, category_data in index.get('categories', {}).items():
        if not isinstance(category_data, dict):
            continue
        modules = category_data.get('modules', [])
        actual_modules.extend(modules)

    if len(actual_modules) != total_modules:
        errors.append(
            f"total_modules mismatch: INDEX.yaml claims {total_modules} but found {len(actual_modules)} modules"
        )

    # Check 2: Validate each module file exists and token budgets
    missing_files = []
    token_variances = []

    for category_name, category_data in index.get('categories', {}).items():
        if not isinstance(category_data, dict):
            continue

        modules = category_data.get('modules', [])
        category_module_count = category_data.get('modules_count', 0)
        category_token_budget = category_data.get('token_budget', 0)

        # Check 3: Category modules_count matches actual
        if len(modules) != category_module_count:
            errors.append(
                f"{category_name}: modules_count={category_module_count} but found {len(modules)} modules"
            )

        # Check 4: Sum of estimated_tokens matches category token_budget
        actual_budget = sum(m.get('estimated_tokens', 0) for m in modules)
        if actual_budget != category_token_budget:
            errors.append(
                f"{category_name}: token_budget={category_token_budget} but sum={actual_budget} "
                f"(variance: {abs(actual_budget - category_token_budget)})"
            )

        for module in modules:
            if not isinstance(module, dict):
                continue

            module_name = module.get('name', 'unknown')
            file_path = module.get('file', '')
            estimated_tokens = module.get('estimated_tokens', 0)

            # Check file exists
            if file_path:
                if not Path(file_path).exists():
                    missing_files.append(f"{category_name}/{module_name}: {file_path}")
                elif estimated_tokens > 0:
                    # Check token variance (only for existing files)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        words = content.split()
                        word_count = len(words)
                        actual_tokens = round((word_count * 1.33) / 50) * 50
                        variance = abs(actual_tokens - estimated_tokens) / estimated_tokens * 100

                        # BLOCK commits with >20% variance
                        if variance > 20:
                            token_variances.append({
                                'category': category_name,
                                'name': module_name,
                                'file': file_path,
                                'estimated': estimated_tokens,
                                'actual': actual_tokens,
                                'variance': variance,
                                'word_count': word_count
                            })
                    except Exception:
                        # Don't fail for read errors
                        pass

    # Build error message
    if missing_files:
        errors.append("Missing module files:")
        for f in missing_files[:5]:
            errors.append(f"  {f}")
        if len(missing_files) > 5:
            errors.append(f"  ... and {len(missing_files) - 5} more")

    if token_variances:
        errors.append("Token budget variance >20% (BLOCKING):")
        for v in token_variances[:5]:
            errors.append(
                f"  {v['category']}/{v['name']}: "
                f"{v['estimated']} → {v['actual']} tokens "
                f"({v['variance']:.0f}% variance, {v['word_count']} words)"
            )
        if len(token_variances) > 5:
            errors.append(f"  ... and {len(token_variances) - 5} more")
        errors.append("\nUpdate INDEX.yaml estimates to reflect actual token counts")
        errors.append("Formula: (word_count * 1.33), rounded-sm to nearest 50")

    if errors:
        return False, "\n".join(errors)

    return True, f"INDEX.yaml valid: {total_modules} modules, all files exist, token budgets accurate"


def check_mermaid_syntax() -> Tuple[bool, str]:
    """
    Validate Mermaid v10 syntax in modified markdown files.

    PROBLEM: Mermaid v10 broke 88% of diagrams (deprecated v9 syntax)
    SOLUTION: Reject commits with old syntax patterns

    Returns:
        (success, message)
    """
    # Get modified markdown files
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return False, "Failed to get staged files"

    modified_files = result.stdout.strip().split('\n') if result.stdout else []

    # Filter for markdown files (exclude archived files)
    markdown_files = [
        f for f in modified_files
        if f.endswith('.md') and not f.startswith('docs/archive/')
    ]

    if not markdown_files:
        return True, "No markdown files modified"

    # Check each file for Mermaid blocks with deprecated syntax
    violations = []
    for md_file in markdown_files:
        if not Path(md_file).exists():
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract Mermaid blocks
            in_mermaid = False
            current_block = []
            block_start = 0

            for line_num, line in enumerate(content.split('\n'), 1):
                if line.strip() == '```mermaid':
                    in_mermaid = True
                    block_start = line_num
                    current_block = []
                elif line.strip() == '```' and in_mermaid:
                    # Check block for deprecated patterns
                    block_content = '\n'.join(current_block)

                    # Pattern 1: Old style syntax (style NodeName fill:#color)
                    old_style_pattern = r'^\s*style\s+\w+\s+fill:'
                    if re.search(old_style_pattern, block_content, re.MULTILINE):
                        violations.append({
                            'file': md_file,
                            'line': block_start,
                            'type': 'DEPRECATED_STYLE',
                            'pattern': 'style NodeName fill:#color',
                            'suggestion': 'Use: classDef myClass fill:#color; class NodeName myClass'
                        })

                    # Pattern 2: Old subgraph syntax (subgraph "Name With Spaces")
                    old_subgraph_pattern = r'^\s*subgraph\s+"[^"]*"'
                    if re.search(old_subgraph_pattern, block_content, re.MULTILINE):
                        violations.append({
                            'file': md_file,
                            'line': block_start,
                            'type': 'DEPRECATED_SUBGRAPH',
                            'pattern': 'subgraph "Name With Spaces"',
                            'suggestion': 'Use: subgraph id["Name With Spaces"]'
                        })

                    # Pattern 3: Check for graph direction at wrong position
                    graph_direction_pattern = r'^\s*graph\s+(TB|TD|BT|RL|LR)\s*$'
                    if re.search(graph_direction_pattern, block_content, re.MULTILINE):
                        # This is actually valid, but check if it's flowchart instead
                        if 'flowchart' not in block_content:
                            # Suggest using flowchart instead of graph
                            violations.append({
                                'file': md_file,
                                'line': block_start,
                                'type': 'PREFER_FLOWCHART',
                                'pattern': 'graph TB/LR',
                                'suggestion': 'Use: flowchart TB/LR (preferred in v10)'
                            })

                    in_mermaid = False
                    current_block = []
                elif in_mermaid:
                    current_block.append(line)

        except Exception as e:
            # Don't fail the whole check for one file error
            continue

    if violations:
        error_lines = ["❌ Deprecated Mermaid v9 syntax detected:"]
        error_lines.append("")

        # Group by file
        files_with_violations = {}
        for v in violations:
            filepath = v['file']
            if filepath not in files_with_violations:
                files_with_violations[filepath] = []
            files_with_violations[filepath].append(v)

        for filepath, issues in sorted(files_with_violations.items())[:5]:
            error_lines.append(f"  📄 {filepath}")
            for issue in issues[:3]:
                error_lines.append(f"     Line {issue['line']}: {issue['type']}")
                error_lines.append(f"       ❌ Old: {issue['pattern']}")
                error_lines.append(f"       ✅ New: {issue['suggestion']}")
                error_lines.append("")
            if len(issues) > 3:
                error_lines.append(f"     ... and {len(issues) - 3} more issues")
                error_lines.append("")

        if len(files_with_violations) > 5:
            error_lines.append(f"  ... and {len(files_with_violations) - 5} more files")
            error_lines.append("")

        error_lines.append("🔧 MERMAID V10 MIGRATION:")
        error_lines.append("  1. Replace 'style' with 'classDef' + 'class':")
        error_lines.append("     OLD: style NodeA fill:#f9f")
        error_lines.append("     NEW: classDef highlight fill:#f9f; class NodeA highlight")
        error_lines.append("")
        error_lines.append("  2. Fix subgraph syntax:")
        error_lines.append("     OLD: subgraph \"My Subgraph\"")
        error_lines.append("     NEW: subgraph mySubgraph[\"My Subgraph\"]")
        error_lines.append("")
        error_lines.append("  3. Prefer 'flowchart' over 'graph'")
        error_lines.append("")
        error_lines.append("🔍 VALIDATE:")
        error_lines.append("  uv run python scripts/blog-content/validate-mermaid-syntax.py")
        error_lines.append("")
        error_lines.append("📖 See: https://mermaid.js.org/config/setup/modules/mermaidAPI.html")
        return False, "\n".join(error_lines)

    # Count total Mermaid blocks checked
    total_blocks = 0
    for md_file in markdown_files:
        if Path(md_file).exists():
            content = Path(md_file).read_text(encoding='utf-8')
            total_blocks += content.count('```mermaid')

    if total_blocks > 0:
        return True, f"All {total_blocks} Mermaid blocks use v10 syntax"
    else:
        return True, "No Mermaid diagrams modified"


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
    "token_budgets": validate_token_budgets,
    "python_logging": check_python_logging,
    "mermaid_syntax": check_mermaid_syntax,
    "index_yaml_validation": validate_index_yaml,
    "nda_compliance": check_nda_compliance,
}

# Validators that must run sequentially AFTER parallel checks pass
SEQUENTIAL_VALIDATORS = {
    "manifest_update": update_manifest,
}


def main():
    """Test all validators."""
    # Note: Using print() here is acceptable as this is test/debug code
    # and runs standalone (not part of the pre-commit hook execution).
    # The pre-commit hook uses parallel_validator.py which has proper logging.
    import sys
    sys.stdout.write("Testing all validators...\n\n")

    for name, validator in VALIDATORS.items():
        success, message = validator()
        status = "✅" if success else "❌"
        sys.stdout.write(f"{status} {name}:\n")
        for line in message.split('\n'):
            sys.stdout.write(f"  {line}\n")
        sys.stdout.write("\n")

    sys.stdout.write("\nSequential validators:\n")
    for name, validator in SEQUENTIAL_VALIDATORS.items():
        success, message = validator()
        status = "✅" if success else "❌"
        sys.stdout.write(f"{status} {name}:\n")
        for line in message.split('\n'):
            sys.stdout.write(f"  {line}\n")


if __name__ == "__main__":
    main()
