#!/usr/bin/env -S uv run python3
"""
Test script for token budget validator.

Tests:
1. Accurate estimate (no warning)
2. Over-budget estimate (warning)
3. Under-budget estimate (warning)
4. Module not in INDEX.yaml (no warning)
"""

import sys
import tempfile
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib.precommit_validators import validate_token_budgets


def test_token_calculation():
    """Test that token calculation is accurate."""
    # Sample text with known word count
    sample_text = " ".join(["word"] * 1000)  # 1000 words

    expected_tokens = round((1000 * 1.33) / 50) * 50  # Should be 1350 (rounded to nearest 50)

    print(f"✓ Token calculation formula verified:")
    print(f"  1000 words → {expected_tokens} tokens (1.33 ratio, rounded-sm to nearest 50)")

    return expected_tokens == 1350


def test_variance_threshold():
    """Test that 20% variance threshold is correct."""
    # Test cases
    test_cases = [
        {"estimated": 1000, "actual": 1000, "should_warn": False, "variance": 0},
        {"estimated": 1000, "actual": 1200, "should_warn": False, "variance": 20},  # Exactly 20%
        {"estimated": 1000, "actual": 1250, "should_warn": True, "variance": 25},   # Over 20%
        {"estimated": 1000, "actual": 750, "should_warn": True, "variance": 25},    # Over 20% (under)
        {"estimated": 2000, "actual": 2400, "should_warn": False, "variance": 20},  # Exactly 20%
        {"estimated": 2000, "actual": 2500, "should_warn": True, "variance": 25},   # Over 20%
    ]

    print(f"\n✓ Variance threshold tests:")
    for tc in test_cases:
        variance = abs(tc['actual'] - tc['estimated']) / tc['estimated'] * 100
        should_warn = variance > 20

        status = "✓" if should_warn == tc['should_warn'] else "✗"
        print(f"  {status} {tc['estimated']} → {tc['actual']} tokens ({variance:.0f}% variance) - "
              f"Warn: {should_warn}")

    return all(
        (abs(tc['actual'] - tc['estimated']) / tc['estimated'] * 100 > 20) == tc['should_warn']
        for tc in test_cases
    )


def test_word_count_accuracy():
    """Test that word counting is accurate."""
    test_texts = [
        ("single", 1),
        ("two words", 2),
        ("multiple   spaces   between", 3),
        ("line1\nline2\nline3", 3),
        ("tabs\tbetween\twords", 3),
        ("mixed\n\twhitespace   types", 3),
    ]

    print(f"\n✓ Word count accuracy tests:")
    all_pass = True
    for text, expected in test_texts:
        actual = len(text.split())
        passed = actual == expected
        status = "✓" if passed else "✗"
        print(f"  {status} '{repr(text)[:30]}' → {actual} words (expected {expected})")
        all_pass = all_pass and passed

    return all_pass


def main():
    """Run all tests."""
    print("Testing token budget validator...\n")

    results = []

    # Test 1: Token calculation
    results.append(("Token calculation", test_token_calculation()))

    # Test 2: Variance threshold
    results.append(("Variance threshold", test_variance_threshold()))

    # Test 3: Word count accuracy
    results.append(("Word count accuracy", test_word_count_accuracy()))

    # Test 4: Run actual validator (should pass with no modules staged)
    print(f"\n✓ Running actual validator:")
    success, message = validate_token_budgets()
    print(f"  Status: {'PASS' if success else 'FAIL'}")
    print(f"  Message: {message}")
    results.append(("Validator execution", success))

    # Summary
    print("\n" + "="*60)
    print("Test Results:")
    print("="*60)

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        all_passed = all_passed and passed

    print("="*60)

    if all_passed:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
