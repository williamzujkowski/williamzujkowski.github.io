#!/usr/bin/env -S uv run python3
"""
Parallel validation framework for pre-commit hooks.

Runs multiple independent validators concurrently to achieve 3-5x speedup
over sequential execution.

Usage:
    from scripts.lib.parallel_validator import ParallelValidator

    validator = ParallelValidator(max_workers=4)
    validator.add_validator("manifest", validate_manifest)
    success, errors = validator.run_all()

VERSION: 1.1.0
"""

import concurrent.futures
import sys
import time
from pathlib import Path
from typing import List, Tuple, Callable

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from logging_config import setup_logger

logger = setup_logger(__name__)


class ValidationResult:
    """Container for validation results with timing information."""

    def __init__(self, name: str, success: bool, message: str = "", duration: float = 0.0):
        self.name = name
        self.success = success
        self.message = message
        self.duration = duration

    def __repr__(self):
        status = "✅" if self.success else "❌"
        return f"{status} {self.name} ({self.duration:.2f}s): {self.message}"


class ParallelValidator:
    """
    Run multiple validators in parallel for fast pre-commit validation.

    Features:
    - Concurrent execution with configurable worker pool
    - Automatic error collection and reporting
    - Timing statistics for performance monitoring
    - Graceful error handling per validator

    Example:
        validator = ParallelValidator(max_workers=4)
        validator.add_validator("check_1", lambda: (True, "OK"))
        validator.add_validator("check_2", lambda: (False, "Failed"))
        success, results = validator.run_all()

        if not success:
            for result in results:
                if not result.success:
                    print(f"Failed: {result.name} - {result.message}")
    """

    def __init__(self, max_workers: int = 4, verbose: bool = False):
        """
        Initialize parallel validator.

        Args:
            max_workers: Maximum number of concurrent validators
            verbose: Print detailed timing information
        """
        self.max_workers = max_workers
        self.verbose = verbose
        self.validators: List[Tuple[str, Callable[[], Tuple[bool, str]]]] = []

    def add_validator(self, name: str, func: Callable[[], Tuple[bool, str]]) -> None:
        """
        Register a validator function.

        Args:
            name: Human-readable name for the validator
            func: Callable that returns (success: bool, message: str)
        """
        self.validators.append((name, func))

    def _run_validator(self, name: str, func: Callable[[], Tuple[bool, str]]) -> ValidationResult:
        """
        Execute a single validator with timing and error handling.

        Args:
            name: Validator name
            func: Validator function

        Returns:
            ValidationResult with success status, message, and duration
        """
        start_time = time.time()
        try:
            success, message = func()
            duration = time.time() - start_time
            return ValidationResult(name, success, message, duration)
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Exception: {str(e)}"
            return ValidationResult(name, False, error_msg, duration)

    def run_all(self) -> Tuple[bool, List[ValidationResult]]:
        """
        Run all validators in parallel.

        Returns:
            Tuple of (all_passed: bool, results: List[ValidationResult])
        """
        start_time = time.time()
        results: List[ValidationResult] = []

        if not self.validators:
            return True, results

        # Run validators in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all validators
            future_to_name = {
                executor.submit(self._run_validator, name, func): name
                for name, func in self.validators
            }

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_name):
                result = future.result()
                results.append(result)

                # Log live status if verbose
                if self.verbose:
                    logger.info(f"Validation completed: {result}")

        # Calculate statistics
        total_duration = time.time() - start_time
        all_passed = all(result.success for result in results)

        # Sort results by name for consistent output
        results.sort(key=lambda r: r.name)

        # Log summary
        if self.verbose:
            serial_time = sum(r.duration for r in results)
            speedup = serial_time / total_duration if total_duration > 0 else 1.0
            logger.info("Validation Summary")
            logger.info(f"Total time: {total_duration:.2f}s")
            logger.info(f"Serial equivalent: {serial_time:.2f}s")
            logger.info(f"Speedup: {speedup:.1f}x")
            logger.info(f"Status: {'PASS' if all_passed else 'FAIL'}")

        return all_passed, results


if __name__ == "__main__":
    print("This module provides the ParallelValidator class.")
    print("Import it from other scripts to use parallel validation.")
