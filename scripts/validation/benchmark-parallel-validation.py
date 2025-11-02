#!/usr/bin/env -S uv run python3
"""
SCRIPT: benchmark-parallel-validation.py
PURPOSE: Benchmark parallel validation performance improvements
CATEGORY: validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-02

DESCRIPTION:
    Benchmarks metadata-validator.py performance with different worker counts.
    Compares sequential (workers=1) vs parallel execution (workers=2,4,6,8,10).

    Measures:
    - Total execution time per worker count
    - Speedup vs sequential baseline
    - Optimal worker count for I/O-bound validation

    Used to validate Optimization #3 from performance analysis report.

USAGE:
    uv run python scripts/validation/benchmark-parallel-validation.py

OUTPUT:
    - Execution time per worker count (3 runs averaged)
    - Speedup percentage vs baseline
    - Recommended worker count
    - Performance analysis report

DEPENDENCIES:
    - Python 3.8+
    - metadata-validator.py
"""

import sys
import time
import statistics
from pathlib import Path
from typing import List, Dict, Tuple

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from logging_config import setup_logger

# Import MetadataValidator by executing the script file
import importlib.util
spec = importlib.util.spec_from_file_location(
    "metadata_validator",
    Path(__file__).parent / "metadata-validator.py"
)
metadata_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata_validator)
MetadataValidator = metadata_validator.MetadataValidator

logger = setup_logger(__name__)


def benchmark_workers(posts_dir: Path, workers: int, runs: int = 3) -> Tuple[float, float, float]:
    """Benchmark validation with specific worker count.

    Args:
        posts_dir: Directory containing blog posts
        workers: Number of parallel workers
        runs: Number of benchmark runs (default: 3)

    Returns:
        Tuple of (mean_time, min_time, max_time) in seconds
    """
    times: List[float] = []

    for run in range(runs):
        validator = MetadataValidator(posts_dir=posts_dir, workers=workers)

        start = time.perf_counter()
        validator.validate_all_posts()
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        logger.info(f"  Run {run+1}/{runs}: {elapsed:.4f}s")

    return statistics.mean(times), min(times), max(times)


def main() -> int:
    """Run parallel validation benchmarks."""
    posts_dir = Path(__file__).parent.parent.parent / 'src' / 'posts'

    if not posts_dir.exists():
        logger.error(f"Posts directory not found: {posts_dir}")
        return 1

    post_count = len(list(posts_dir.glob("*.md")))
    logger.info("=" * 80)
    logger.info("PARALLEL VALIDATION BENCHMARK")
    logger.info("=" * 80)
    logger.info(f"Posts directory: {posts_dir}")
    logger.info(f"Total posts: {post_count}")
    logger.info(f"Runs per configuration: 3")
    logger.info("")

    # Benchmark configurations
    worker_counts = [1, 2, 4, 6, 8, 10]
    results: Dict[int, Tuple[float, float, float]] = {}

    for workers in worker_counts:
        logger.info(f"\nBenchmarking workers={workers}:")
        mean_time, min_time, max_time = benchmark_workers(posts_dir, workers, runs=3)
        results[workers] = (mean_time, min_time, max_time)
        logger.info(f"  Mean: {mean_time:.4f}s, Min: {min_time:.4f}s, Max: {max_time:.4f}s")

    # Analysis
    baseline_time = results[1][0]
    logger.info("\n" + "=" * 80)
    logger.info("PERFORMANCE ANALYSIS")
    logger.info("=" * 80)
    logger.info(f"Baseline (sequential, workers=1): {baseline_time:.4f}s")
    logger.info("")
    logger.info("Worker Count | Mean Time | Speedup | Efficiency")
    logger.info("-" * 80)

    best_speedup = 0.0
    best_workers = 1

    for workers in worker_counts:
        mean_time = results[workers][0]
        speedup = (baseline_time / mean_time) * 100 - 100
        efficiency = (baseline_time / mean_time) / workers * 100

        logger.info(f"{workers:>12} | {mean_time:>9.4f}s | {speedup:>6.1f}% | {efficiency:>6.1f}%")

        if speedup > best_speedup:
            best_speedup = speedup
            best_workers = workers

    logger.info("")
    logger.info(f"Best configuration: workers={best_workers} ({best_speedup:.1f}% speedup)")
    logger.info(f"Target speedup: 20-25%")

    if best_speedup >= 20.0:
        logger.info(f"✅ Target achieved! {best_speedup:.1f}% >= 20%")
    else:
        logger.warning(f"⚠️  Target not met: {best_speedup:.1f}% < 20%")

    logger.info("\n" + "=" * 80)
    logger.info("RECOMMENDATION")
    logger.info("=" * 80)

    # Find optimal workers (best speedup with acceptable efficiency)
    optimal_workers = 1
    for workers in worker_counts:
        mean_time = results[workers][0]
        speedup = (baseline_time / mean_time) * 100 - 100
        efficiency = (baseline_time / mean_time) / workers * 100

        # Look for good speedup (>15%) with reasonable efficiency (>70%)
        if speedup > 15.0 and efficiency > 70.0:
            optimal_workers = workers

    logger.info(f"Recommended worker count: {optimal_workers}")
    logger.info(f"This balances speedup ({((baseline_time / results[optimal_workers][0]) * 100 - 100):.1f}%) ")
    logger.info(f"with efficiency ({((baseline_time / results[optimal_workers][0]) / optimal_workers * 100):.1f}%)")
    logger.info("")
    logger.info("Update CLAUDE.md and metadata-validator.py default if different from current (6).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
