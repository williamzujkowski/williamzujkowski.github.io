#!/usr/bin/env -S uv run python3
"""
SCRIPT: benchmark_validators.py
PURPOSE: Benchmark script to compare sequential vs parallel validator execution
CATEGORY: infrastructure
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Measures the speedup achieved by parallel execution.
"""

import sys
import time
from pathlib import Path
from typing import List, Tuple

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from logging_config import setup_logger

# Setup logging
logger = setup_logger(__name__)

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
    logger.info("=" * 60)
    logger.info("PRE-COMMIT HOOK BENCHMARK")
    logger.info("=" * 60)
    logger.info(f"\nValidators to test: {len(VALIDATORS)}")
    logger.info(f"Parallel workers: 6\n")

    # Run sequential
    logger.info("Running sequential execution...")
    seq_times = []
    for i in range(5):
        duration, passed = run_sequential()
        seq_times.append(duration)
        logger.info(f"  Run {i + 1}: {duration:.3f}s {'✅' if passed else '❌'}")

    seq_avg = sum(seq_times) / len(seq_times)
    seq_min = min(seq_times)
    seq_max = max(seq_times)

    # Run parallel
    logger.info("\nRunning parallel execution...")
    par_times = []
    for i in range(5):
        duration, passed = run_parallel()
        par_times.append(duration)
        logger.info(f"  Run {i + 1}: {duration:.3f}s {'✅' if passed else '❌'}")

    par_avg = sum(par_times) / len(par_times)
    par_min = min(par_times)
    par_max = max(par_times)

    # Calculate speedup
    speedup_avg = seq_avg / par_avg if par_avg > 0 else 0
    speedup_best = seq_max / par_min if par_min > 0 else 0

    # Print results
    logger.info("\n" + "=" * 60)
    logger.info("RESULTS")
    logger.info("=" * 60)
    logger.info(f"\nSequential execution:")
    logger.info(f"  Average: {seq_avg:.3f}s")
    logger.info(f"  Range:   {seq_min:.3f}s - {seq_max:.3f}s")

    logger.info(f"\nParallel execution (6 workers):")
    logger.info(f"  Average: {par_avg:.3f}s")
    logger.info(f"  Range:   {par_min:.3f}s - {par_max:.3f}s")

    logger.info(f"\n🚀 Speedup:")
    logger.info(f"  Average: {speedup_avg:.2f}x faster")
    logger.info(f"  Best:    {speedup_best:.2f}x faster")

    logger.info(f"\n⏱️  Time saved per commit:")
    logger.info(f"  Average: {(seq_avg - par_avg):.3f}s")
    logger.info(f"  Best:    {(seq_max - par_min):.3f}s")

    logger.info("\n" + "=" * 60)

    # Check if speedup meets target
    if speedup_avg >= 3.0:
        logger.info(f"✅ TARGET MET: {speedup_avg:.1f}x speedup (target: 3-5x)")
    elif speedup_avg >= 2.0:
        logger.info(f"⚠️  PARTIAL: {speedup_avg:.1f}x speedup (target: 3-5x)")
    else:
        logger.info(f"❌ BELOW TARGET: {speedup_avg:.1f}x speedup (target: 3-5x)")


if __name__ == "__main__":
    main()
