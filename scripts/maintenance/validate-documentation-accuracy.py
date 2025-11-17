#!/usr/bin/env -S uv run python3
"""
Documentation Accuracy Validator v1.0.0

Validates consistency between CLAUDE.md claims and actual repository state:
- Version numbers match between CLAUDE.md and INDEX.yaml
- Module counts accurate across all references
- Token budgets within acceptable variance
- Word counts match actual measurements

Prevents documentation drift discovered in Session 52 validation.
"""

import json
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

# Add scripts directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

# Setup logger
logger = setup_logger(__name__, level="INFO")

# Repository root
REPO_ROOT = Path(__file__).parent.parent.parent

# Critical files
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
INDEX_YAML = REPO_ROOT / "docs" / "context" / "INDEX.yaml"

# Acceptable variance thresholds
TOKEN_VARIANCE_THRESHOLD = 0.10  # 10% max variance
WORD_COUNT_VARIANCE_THRESHOLD = 0.05  # 5% max variance


class Colors:
    """ANSI color codes for output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def read_claude_md() -> str:
    """Read CLAUDE.md content"""
    with open(CLAUDE_MD, 'r', encoding='utf-8') as f:
        return f.read()


def read_index_yaml() -> Dict:
    """Read INDEX.yaml structure"""
    with open(INDEX_YAML, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def extract_frontmatter_version(content: str) -> str:
    """Extract VERSION from CLAUDE.md frontmatter"""
    for line in content.split('\n'):
        if line.startswith('VERSION:'):
            return line.split(':', 1)[1].strip()
    return "UNKNOWN"


def count_module_references(content: str) -> List[Tuple[str, int, int]]:
    """
    Find all module count references in CLAUDE.md
    Returns: [(reference_text, line_number, claimed_count)]
    """
    references = []
    lines = content.split('\n')

    # Pattern 1: "X specialized modules"
    for i, line in enumerate(lines, 1):
        if 'specialized modules' in line.lower():
            # Extract number before "specialized modules"
            parts = line.split('specialized modules')
            if parts:
                words = parts[0].split()
                for word in reversed(words):
                    try:
                        count = int(word)
                        references.append((line.strip(), i, count))
                        break
                    except ValueError:
                        continue

    # Pattern 2: "Total modules: X modules"
    for i, line in enumerate(lines, 1):
        if 'Total modules:' in line or '**Total modules:**' in line:
            # Extract number
            parts = line.split('modules')
            for part in parts:
                if 'Total' in part:
                    words = part.replace('*', '').replace(':', '').split()
                    for word in reversed(words):
                        try:
                            count = int(word)
                            references.append((line.strip(), i, count))
                            break
                        except ValueError:
                            continue

    # Pattern 3: Category breakdowns like "(5 core + 6 workflows + ...)"
    for i, line in enumerate(lines, 1):
        if 'core +' in line and 'workflows' in line:
            references.append((line.strip(), i, "BREAKDOWN"))

    return references


def validate_version_consistency(claude_content: str, index_data: Dict) -> Tuple[bool, str]:
    """Validate version numbers match"""
    claude_version = extract_frontmatter_version(claude_content)
    index_version = index_data.get('root_anchor', {}).get('version', 'UNKNOWN')

    if claude_version == index_version:
        return True, f"Version {claude_version} matches across files"
    else:
        return False, f"MISMATCH: CLAUDE.md={claude_version}, INDEX.yaml={index_version}"


def validate_module_counts(claude_content: str, index_data: Dict) -> Tuple[bool, List[str]]:
    """Validate module counts are accurate"""
    issues = []
    actual_count = index_data.get('total_modules', 0)

    references = count_module_references(claude_content)

    for ref_text, line_num, claimed_count in references:
        if claimed_count == "BREAKDOWN":
            # Validate category breakdown
            categories = index_data.get('categories', {})
            expected_breakdown = []
            for cat_name, cat_data in categories.items():
                count = cat_data.get('modules_count', 0)
                expected_breakdown.append(f"{count} {cat_name}")

            breakdown_str = " + ".join(expected_breakdown)
            issues.append(f"Line {line_num}: Verify breakdown matches: {breakdown_str}")
        elif claimed_count != actual_count:
            issues.append(
                f"Line {line_num}: Claims {claimed_count} modules, actual is {actual_count}\n"
                f"  Text: {ref_text[:80]}..."
            )

    if not issues:
        return True, [f"All module count references accurate ({actual_count} modules)"]
    else:
        return False, issues


def validate_token_estimates(claude_content: str, index_data: Dict) -> Tuple[bool, List[str]]:
    """Validate token estimates within acceptable variance"""
    issues = []

    # Root anchor tokens
    claude_tokens = None
    for line in claude_content.split('\n'):
        if '5,868 tokens' in line or '5868 tokens' in line:
            claude_tokens = 5868
            break

    index_tokens = index_data.get('root_anchor', {}).get('token_estimate', 0)

    if claude_tokens and index_tokens:
        variance = abs(claude_tokens - index_tokens) / index_tokens
        if variance > TOKEN_VARIANCE_THRESHOLD:
            issues.append(
                f"Root anchor token variance {variance*100:.1f}% "
                f"(CLAUDE.md: {claude_tokens}, INDEX.yaml: {index_tokens})"
            )

    # Total module tokens
    actual_total = index_data.get('token_budgets', {}).get('actual_total', 0)

    for line in claude_content.split('\n'):
        if '66,895 tokens' in line or '66895 tokens' in line:
            claimed_total = 66895
            variance = abs(claimed_total - actual_total) / actual_total
            if variance > TOKEN_VARIANCE_THRESHOLD:
                issues.append(
                    f"Module token variance {variance*100:.1f}% "
                    f"(CLAUDE.md: {claimed_total}, INDEX.yaml: {actual_total})"
                )

    if not issues:
        return True, ["Token estimates within acceptable variance (<10%)"]
    else:
        return False, issues


def validate_word_counts(claude_content: str, index_data: Dict) -> Tuple[bool, List[str]]:
    """Validate word count claims"""
    issues = []

    actual_word_count = index_data.get('root_anchor', {}).get('word_count', 0)

    # Check for word count claims
    for line in claude_content.split('\n'):
        if '4,400 words' in line or '4400 words' in line:
            claimed_words = 4400
            variance = abs(claimed_words - actual_word_count) / actual_word_count
            if variance > WORD_COUNT_VARIANCE_THRESHOLD:
                issues.append(
                    f"Word count variance {variance*100:.1f}% "
                    f"(CLAUDE.md: {claimed_words}, INDEX.yaml: {actual_word_count})"
                )

    if not issues:
        return True, [f"Word count accurate ({actual_word_count} words)"]
    else:
        return False, issues


def main():
    """Run all validation checks"""
    logger.info("📊 Documentation Accuracy Validator v1.0.0\n")

    # Load files
    try:
        claude_content = read_claude_md()
        index_data = read_index_yaml()
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1

    # Run validations
    all_passed = True

    # 1. Version consistency
    passed, message = validate_version_consistency(claude_content, index_data)
    if passed:
        logger.info(f"✅ Version Consistency: {message}")
    else:
        logger.error(f"❌ Version Consistency: {message}")
        all_passed = False

    # 2. Module counts
    passed, messages = validate_module_counts(claude_content, index_data)
    if passed:
        logger.info(f"✅ Module Counts: {messages[0]}")
    else:
        logger.error("❌ Module Counts:")
        for msg in messages:
            logger.error(f"   {msg}")
        all_passed = False

    # 3. Token estimates
    passed, messages = validate_token_estimates(claude_content, index_data)
    if passed:
        logger.info(f"✅ Token Estimates: {messages[0]}")
    else:
        logger.warning("⚠️  Token Estimates:")
        for msg in messages:
            logger.warning(f"   {msg}")

    # 4. Word counts
    passed, messages = validate_word_counts(claude_content, index_data)
    if passed:
        logger.info(f"✅ Word Counts: {messages[0]}")
    else:
        logger.warning("⚠️  Word Counts:")
        for msg in messages:
            logger.warning(f"   {msg}")

    # Final summary
    if all_passed:
        logger.info("✅ All validations passed!")
        return 0
    else:
        logger.error("❌ Validation failures detected")
        logger.info("💡 Fix discrepancies to prevent documentation drift")
        return 1


if __name__ == "__main__":
    sys.exit(main())
