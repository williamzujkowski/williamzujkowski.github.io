#!/usr/bin/env -S uv run python3
"""
Realistic benchmark simulating expensive validators (with blog posts).

This simulates the real-world scenario where humanization validation
runs on multiple blog posts, which is computationally expensive.
"""

import sys
import time
from pathlib import Path
from typing import List, Tuple
import tempfile
import subprocess

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.parallel_validator import ParallelValidator


def create_test_blog_post() -> Path:
    """Create a temporary blog post for testing."""
    content = """---
title: Test Post
date: 2024-01-01
description: Test post for benchmarking
---

This is a test blog post with enough content to trigger humanization validation.

The quick brown fox jumps over the lazy dog. This sentence is repeated multiple
times to create enough content for the humanization validator to analyze properly.

## Section 1

More content here with natural language patterns and varied sentence structure.
We want to make sure this passes the humanization threshold of 75/100.

## Section 2

Additional paragraphs with technical content mixed with natural language.
This helps simulate a real blog post that would need validation.

The validator checks for various metrics including sentence variation, word choice,
paragraph structure, and overall readability scores.

## Conclusion

Final thoughts to wrap up the test content. This should be sufficient for
proper validation testing and benchmark purposes.
"""

    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.md',
        prefix='test-post-',
        dir='.',
        delete=False
    )
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)


def simulate_expensive_validator(delay: float = 2.0) -> Tuple[bool, str]:
    """Simulate an expensive validator (e.g., humanization check)."""
    time.sleep(delay)
    return True, f"Validated (took {delay}s)"


def simulate_cheap_validator(delay: float = 0.01) -> Tuple[bool, str]:
    """Simulate a cheap validator."""
    time.sleep(delay)
    return True, f"Validated (took {delay}s)"


def run_sequential_realistic() -> Tuple[float, bool]:
    """Run realistic validators sequentially."""
    start_time = time.time()

    # 4 expensive validators (humanization, code ratio analysis, link checking, image validation)
    validators = [
        ("humanization_1", lambda: simulate_expensive_validator(2.5)),
        ("humanization_2", lambda: simulate_expensive_validator(2.3)),
        ("humanization_3", lambda: simulate_expensive_validator(2.8)),
        ("code_ratio_check", lambda: simulate_expensive_validator(2.0)),
        # 3 cheap validators (manifest, duplicates, standards)
        ("manifest", lambda: simulate_cheap_validator(0.01)),
        ("duplicates", lambda: simulate_cheap_validator(0.02)),
        ("standards", lambda: simulate_cheap_validator(0.01)),
    ]

    all_passed = True
    for name, validator in validators:
        success, _ = validator()
        if not success:
            all_passed = False

    duration = time.time() - start_time
    return duration, all_passed


def run_parallel_realistic(max_workers: int = 6) -> Tuple[float, bool]:
    """Run realistic validators in parallel."""
    validator = ParallelValidator(max_workers=max_workers, verbose=False)

    # Same validators as sequential
    validator.add_validator("humanization_1", lambda: simulate_expensive_validator(2.5))
    validator.add_validator("humanization_2", lambda: simulate_expensive_validator(2.3))
    validator.add_validator("humanization_3", lambda: simulate_expensive_validator(2.8))
    validator.add_validator("code_ratio_check", lambda: simulate_expensive_validator(2.0))
    validator.add_validator("manifest", lambda: simulate_cheap_validator(0.01))
    validator.add_validator("duplicates", lambda: simulate_cheap_validator(0.02))
    validator.add_validator("standards", lambda: simulate_cheap_validator(0.01))

    all_passed, _ = validator.run_all()
    return 0, all_passed  # Return 0 for duration as validator tracks its own time


def main():
    """Run realistic benchmarks."""
    print("=" * 60)
    print("REALISTIC PRE-COMMIT HOOK BENCHMARK")
    print("=" * 60)
    print("\nSimulating scenario:")
    print("  - 3 blog posts + code ratio check (4 expensive validators)")
    print("  - Each validation takes ~2-2.8s")
    print("  - 3 cheap validators (<50ms each)")
    print("  - Total sequential time: ~9.6s")
    print("  - Total parallel time: ~2.8s (max worker time)")
    print("  - Expected speedup: ~3.4x\n")

    # Run sequential
    print("Running SEQUENTIAL execution (3 runs)...")
    seq_times = []
    for i in range(3):
        duration, passed = run_sequential_realistic()
        seq_times.append(duration)
        print(f"  Run {i + 1}: {duration:.2f}s {'✅' if passed else '❌'}")

    seq_avg = sum(seq_times) / len(seq_times)

    # Run parallel
    print("\nRunning PARALLEL execution (3 runs)...")
    par_times = []
    for i in range(3):
        start = time.time()
        _, passed = run_parallel_realistic()
        duration = time.time() - start
        par_times.append(duration)
        print(f"  Run {i + 1}: {duration:.2f}s {'✅' if passed else '❌'}")

    par_avg = sum(par_times) / len(par_times)

    # Calculate speedup
    speedup = seq_avg / par_avg if par_avg > 0 else 0
    time_saved = seq_avg - par_avg

    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nSequential execution: {seq_avg:.2f}s average")
    print(f"Parallel execution:   {par_avg:.2f}s average")
    print(f"\n🚀 Speedup: {speedup:.2f}x faster")
    print(f"⏱️  Time saved: {time_saved:.2f}s per commit")

    if speedup >= 3.0:
        print(f"\n✅ TARGET MET: {speedup:.1f}x speedup (target: 3-5x)")
    elif speedup >= 2.5:
        print(f"\n⚠️  CLOSE: {speedup:.1f}x speedup (target: 3-5x)")
    else:
        print(f"\n❌ BELOW TARGET: {speedup:.1f}x speedup (target: 3-5x)")

    print("\n" + "=" * 60)
    print("NOTE: Real-world speedup depends on:")
    print("  - Number of blog posts modified")
    print("  - Complexity of humanization validation")
    print("  - System CPU cores and load")
    print("=" * 60)


if __name__ == "__main__":
    main()
