#!/usr/bin/env -S uv run python3
"""
Fix INDEX.yaml token budgets using accurate word count × 1.33 formula.

This script:
1. Reads INDEX.yaml
2. For each module, calculates actual tokens from file word count
3. Updates estimated_tokens using formula: (word_count * 1.33), rounded to nearest 50
4. Recalculates category token_budget totals
5. Writes updated INDEX.yaml

USAGE:
    uv run python scripts/validation/fix-index-token-budgets.py
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, Any

# Add scripts directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

logger = setup_logger(__name__)


def calculate_tokens(file_path: str) -> tuple[int, int]:
    """
    Calculate tokens from file word count.

    Args:
        file_path: Path to markdown file

    Returns:
        Tuple of (word_count, token_estimate)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        words = content.split()
        word_count = len(words)

        # Formula: word_count * 1.33, rounded to nearest 50
        token_estimate = round((word_count * 1.33) / 50) * 50

        return word_count, token_estimate
    except Exception as e:
        logger.warning(f"Error reading {file_path}: {e}")
        return 0, 0


def fix_index_yaml() -> None:
    """Fix all token budgets in INDEX.yaml."""
    index_path = Path("docs/context/INDEX.yaml")

    if not index_path.exists():
        logger.error("INDEX.yaml not found")
        return

    # Load INDEX.yaml
    with open(index_path, 'r', encoding='utf-8') as f:
        index = yaml.safe_load(f)

    logger.info("🔍 Analyzing INDEX.yaml token budgets...\n")

    # Track changes
    modules_updated = 0
    total_token_change = 0

    # Fix each module
    for category_name, category_data in index.get('categories', {}).items():
        if not isinstance(category_data, dict):
            continue

        logger.info(f"📁 Category: {category_name}")
        category_token_total = 0

        for module in category_data.get('modules', []):
            if not isinstance(module, dict):
                continue

            module_name = module.get('name', 'unknown')
            file_path = module.get('file', '')
            old_estimate = module.get('estimated_tokens', 0)

            if not file_path or not Path(file_path).exists():
                logger.info(f"  ⏭️  Skipping {module_name} (file not found)")
                category_token_total += old_estimate
                continue

            # Calculate actual tokens
            word_count, new_estimate = calculate_tokens(file_path)

            if old_estimate != new_estimate:
                variance = abs(new_estimate - old_estimate) / old_estimate * 100 if old_estimate > 0 else 0
                logger.info(f"  ✏️  {module_name}: {old_estimate} → {new_estimate} tokens "
                           f"({variance:.0f}% change, {word_count} words)")

                module['estimated_tokens'] = new_estimate
                modules_updated += 1
                total_token_change += (new_estimate - old_estimate)
            else:
                logger.info(f"  ✅ {module_name}: {old_estimate} tokens (no change)")

            category_token_total += new_estimate

        # Update category token_budget
        old_budget = category_data.get('token_budget', 0)
        category_data['token_budget'] = category_token_total

        if old_budget != category_token_total:
            logger.info(f"  📊 Category budget: {old_budget} → {category_token_total} tokens\n")
        else:
            logger.info(f"  📊 Category budget: {category_token_total} tokens (unchanged)\n")

    # Calculate total across all categories
    total_tokens = sum(
        category_data.get('token_budget', 0)
        for category_data in index.get('categories', {}).values()
        if isinstance(category_data, dict)
    )

    logger.info(f"\n📈 Summary:")
    logger.info(f"  Modules updated: {modules_updated}")
    logger.info(f"  Total token change: {total_token_change:+,} tokens")
    logger.info(f"  New total budget: {total_tokens:,} tokens")

    # Write updated INDEX.yaml
    with open(index_path, 'w', encoding='utf-8') as f:
        yaml.dump(index, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    logger.info(f"\n✅ INDEX.yaml updated successfully")


if __name__ == "__main__":
    fix_index_yaml()
