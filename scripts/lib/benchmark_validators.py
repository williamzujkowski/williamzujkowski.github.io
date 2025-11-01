#!/usr/bin/env -S uv run python3
"""
Benchmark script to compare sequential vs parallel validator execution.

Measures the speedup achieved by parallel execution.
"""

import sys
import time
from pathlib import Path
from typing import List, Tuple

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.parallel_validator import ParallelValidator
from lib.precommit_validators import VALIDATORS


def run_sequential() -> Tuple[float, bool]:
    """Run all validators sequentially."""
    start_time = time.time()
    all_passed = True

    for name, validator in VALIDATORS.items():
        success, _ = validator()
        if not success:
            all_passed = False

    duration = time.time() - start_time
    return duration, all_passed


def run_parallel(max_workers: int = 6) -> Tuple[float, bool]:
    """Run all validators in parallel."""
    start_time = time.time()

    validator = ParallelValidator(max_workers=max_workers, verbose=False)
    for name, func in VALIDATORS.items():
        validator.add_validator(name, func)

    all_passed, _ = validator.run_all()
    duration = time.time() - start_time
    return duration, all_passed


def main():
    """Run benchmarks and print results."""
    print("=" * 60)
    print("PRE-COMMIT HOOK BENCHMARK")
    print("=" * 60)
    print(f"\nValidators to test: {len(VALIDATORS)}")
    print(f"Parallel workers: 6\n")

    # Run sequential
    print("Running sequential execution...")
    seq_times = []
    for i in range(5):
        duration, passed = run_sequential()
        seq_times.append(duration)
        print(f"  Run {i + 1}: {duration:.3f}s {'✅' if passed else '❌'}")

    seq_avg = sum(seq_times) / len(seq_times)
    seq_min = min(seq_times)
    seq_max = max(seq_times)

    # Run parallel
    print("\nRunning parallel execution...")
    par_times = []
    for i in range(5):
        duration, passed = run_parallel()
        par_times.append(duration)
        print(f"  Run {i + 1}: {duration:.3f}s {'✅' if passed else '❌'}")

    par_avg = sum(par_times) / len(par_times)
    par_min = min(par_times)
    par_max = max(par_times)

    # Calculate speedup
    speedup_avg = seq_avg / par_avg if par_avg > 0 else 0
    speedup_best = seq_max / par_min if par_min > 0 else 0

    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nSequential execution:")
    print(f"  Average: {seq_avg:.3f}s")
    print(f"  Range:   {seq_min:.3f}s - {seq_max:.3f}s")

    print(f"\nParallel execution (6 workers):")
    print(f"  Average: {par_avg:.3f}s")
    print(f"  Range:   {par_min:.3f}s - {par_max:.3f}s")

    print(f"\n🚀 Speedup:")
    print(f"  Average: {speedup_avg:.2f}x faster")
    print(f"  Best:    {speedup_best:.2f}x faster")

    print(f"\n⏱️  Time saved per commit:")
    print(f"  Average: {(seq_avg - par_avg):.3f}s")
    print(f"  Best:    {(seq_max - par_min):.3f}s")

    print("\n" + "=" * 60)

    # Check if speedup meets target
    if speedup_avg >= 3.0:
        print(f"✅ TARGET MET: {speedup_avg:.1f}x speedup (target: 3-5x)")
    elif speedup_avg >= 2.0:
        print(f"⚠️  PARTIAL: {speedup_avg:.1f}x speedup (target: 3-5x)")
    else:
        print(f"❌ BELOW TARGET: {speedup_avg:.1f}x speedup (target: 3-5x)")


if __name__ == "__main__":
    main()
