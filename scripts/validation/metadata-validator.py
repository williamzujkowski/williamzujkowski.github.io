#!/usr/bin/env -S uv run python3
"""
SCRIPT: metadata-validator.py
PURPOSE: Validate blog post metadata for quality and completeness
CATEGORY: validation
LLM_READY: True
VERSION: 4.0.0
UPDATED: 2025-11-02

DESCRIPTION:
    Validates YAML frontmatter metadata across all blog posts to ensure
    quality, completeness, and compliance with SEO best practices.

    Validation checks:
    1. Required fields: title, description, date, author, tags
    2. Description length (optimal: 120-160 chars for SEO)
    3. Date format (YYYY-MM-DD or ISO 8601)
    4. Hero image path validation
    5. Tag count and quality (3-8 recommended)

    PERFORMANCE: Sequential validation is optimal for this workload (58ms for 63 posts).
    Parallel execution infrastructure available but adds overhead for fast I/O operations.
    Used in CI/CD pipeline to ensure content quality before deployment.

USAGE:
    # Text report (default, sequential)
    uv run python scripts/validation/metadata-validator.py

    # JSON report for CI/CD
    uv run python scripts/validation/metadata-validator.py --format json

    # Experimental: parallel execution (slower for this workload)
    uv run python scripts/validation/metadata-validator.py --workers 4

    # Validate specific directory
    uv run python scripts/validation/metadata-validator.py --posts-dir src/drafts

ARGUMENTS:
    --format: Output format [text|json] (default: text)
    --posts-dir: Posts directory (default: src/posts)
    --workers: Parallel workers (default: 1 [optimal], experimental)

OUTPUT:
    - Total posts scanned
    - Validation statistics
    - Detailed issue reports per post
    - Exit code: 0 (valid), 1 (errors detected)

DEPENDENCIES:
    - Python 3.8+
    - PyYAML for frontmatter parsing
    - logging_config for consistent logging
    - concurrent.futures for parallel execution

RELATED_SCRIPTS:
    - scripts/validation/build-monitor.py: Build process validation

MANIFEST_REGISTRY: scripts/validation/metadata-validator.py
"""

import re
import sys
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

# Pre-compiled regex for date validation (Optimization #1)
DATE_PATTERN_SIMPLE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
DATE_PATTERN_ISO = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$')

@dataclass
class ValidationResult:
    """Represents validation result for a single post.

    Attributes:
        filename: Name of the validated markdown file.
        issues: List of validation errors that must be fixed.
        warnings: List of non-critical suggestions for improvement.
        valid: Boolean indicating if post passes all required validations.
    """
    filename: str
    issues: List[str]
    warnings: List[str]
    valid: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of validation result.
        """
        return asdict(self)


class MetadataValidator:
    """Validate blog post metadata for quality and completeness.

    This validator checks YAML frontmatter in markdown files for:
    - Required fields (title, description, date, author, tags)
    - SEO-optimized description length (120-160 characters)
    - Valid date formats (YYYY-MM-DD or ISO 8601)
    - Hero image path existence
    - Appropriate tag counts (3-8 recommended)

    Attributes:
        DESCRIPTION_MIN: Minimum acceptable description length (50 chars).
        DESCRIPTION_OPTIMAL_MIN: Lower bound for SEO-optimal range (120 chars).
        DESCRIPTION_OPTIMAL_MAX: Upper bound for SEO-optimal range (160 chars).
        DESCRIPTION_MAX: Maximum acceptable description length (200 chars).
        TAG_MIN_WARN: Minimum tags before warning (3).
        TAG_MAX: Maximum allowed tags (10).
        TAG_OPTIMAL_RANGE: Optimal tag count range (3-8).
    """

    # SEO-optimal description length
    DESCRIPTION_MIN: int = 50
    DESCRIPTION_OPTIMAL_MIN: int = 120
    DESCRIPTION_OPTIMAL_MAX: int = 160
    DESCRIPTION_MAX: int = 200

    # Tag count recommendations
    TAG_MIN_WARN: int = 3
    TAG_MAX: int = 10
    TAG_OPTIMAL_RANGE: Tuple[int, int] = (3, 8)

    def __init__(self, posts_dir: Path, workers: int = 1) -> None:
        """Initialize the metadata validator.

        Args:
            posts_dir: Directory containing blog post markdown files.
            workers: Number of parallel workers for file validation (default: 1).
                    Note: Sequential (workers=1) is fastest for this workload.
                    Parallel execution adds overhead that exceeds I/O savings.

        Raises:
            TypeError: If posts_dir is not a Path object.
        """
        if not isinstance(posts_dir, Path):
            raise TypeError(f"posts_dir must be Path, got {type(posts_dir)}")

        self.posts_dir: Path = posts_dir
        self.workers: int = max(1, workers)  # Ensure at least 1 worker
        self._lock = threading.Lock()  # Thread-safe result aggregation
        self.results: Dict[str, Any] = {
            "total_posts": 0,
            "posts_with_issues": [],
            "metadata_coverage": {},
            "issues_summary": {
                "missing_tags": 0,
                "missing_description": 0,
                "missing_author": 0,
                "missing_date": 0,
                "missing_hero_image": 0,
                "invalid_description_length": 0,
                "invalid_date_format": 0,
                "broken_image_paths": 0,
                "missing_title": 0
            }
        }

    def extract_frontmatter(self, file_path: Path) -> Tuple[Dict[str, Any], Optional[str]]:
        """Extract YAML frontmatter from markdown file.

        Parses the YAML metadata block at the beginning of markdown files,
        delimited by '---' markers.

        Args:
            file_path: Path to markdown file to parse.

        Returns:
            Tuple containing:
                - frontmatter_dict: Parsed YAML as dictionary (empty if error).
                - error_message: Error description string or None if successful.

        Examples:
            >>> validator = MetadataValidator(Path("posts"))
            >>> frontmatter, error = validator.extract_frontmatter(Path("post.md"))
            >>> if error is None:
            ...     print(frontmatter['title'])
        """
        try:
            content: str = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            error_msg = f"Encoding error: {e}"
            logger.error(f"Encoding error in {file_path.name}: {e}")
            return {}, error_msg
        except (IOError, OSError) as e:
            error_msg = f"I/O error: {e}"
            logger.error(f"Cannot read {file_path.name}: {e}")
            return {}, error_msg

        if not content.startswith('---'):
            return {}, "No frontmatter found"

        try:
            # Find second --- delimiter
            end_index: int = content.find('---', 3)
            if end_index == -1:
                return {}, "Malformed frontmatter (no closing ---)"

            frontmatter_text: str = content[3:end_index].strip()
            frontmatter: Any = yaml.safe_load(frontmatter_text)
            return frontmatter or {}, None
        except yaml.YAMLError as e:
            error_msg = f"YAML parsing error: {str(e)}"
            logger.error(f"YAML parsing error in {file_path.name}: {e}")
            return {}, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"Unexpected error parsing {file_path.name}: {e}", exc_info=True)
            return {}, error_msg

    def validate_description_length(self, description: Optional[str]) -> Tuple[bool, str]:
        """Validate description length for SEO optimization.

        Checks if meta description falls within SEO-optimal ranges:
        - Critical: 50-200 characters (hard limits)
        - Optimal: 120-160 characters (Google search snippet length)
        - Acceptable: 50-119 or 161-200 characters

        Args:
            description: Meta description text from frontmatter.

        Returns:
            Tuple containing:
                - is_valid: True if description meets minimum requirements.
                - status_message: Human-readable validation result.

        Examples:
            >>> validator = MetadataValidator(Path("posts"))
            >>> valid, msg = validator.validate_description_length("Short")
            >>> print(valid, msg)
            False Too short (5 chars, recommend 120-160)
        """
        if not description:
            return False, "Missing"

        length: int = len(description)
        if length < self.DESCRIPTION_MIN:
            return False, f"Too short ({length} chars, recommend 120-160)"
        elif length > self.DESCRIPTION_MAX:
            return False, f"Too long ({length} chars, recommend 120-160)"
        elif length < self.DESCRIPTION_OPTIMAL_MIN or length > self.DESCRIPTION_OPTIMAL_MAX:
            return True, f"Acceptable ({length} chars, optimal: 120-160)"
        else:
            return True, f"Optimal ({length} chars)"

    def validate_date_format(self, date_value: Any) -> Tuple[bool, str]:
        """Validate date format compliance.

        Accepts YAML date objects, YYYY-MM-DD strings, or ISO 8601 timestamps.
        Uses regex pre-filter for performance (Optimization #1).

        Args:
            date_value: Date value from frontmatter (string, datetime, or None).

        Returns:
            Tuple containing:
                - is_valid: True if date format is acceptable.
                - status_message: Description of date format or error.

        Examples:
            >>> validator = MetadataValidator(Path("posts"))
            >>> valid, msg = validator.validate_date_format("2025-11-02")
            >>> print(valid, msg)
            True Valid (YYYY-MM-DD)
        """
        if not date_value:
            return False, "Missing"

        # Handle datetime objects from YAML parser
        if isinstance(date_value, datetime):
            return True, "Valid (datetime object)"

        date_str: str = str(date_value)

        # Fast regex pre-filter (Optimization #1)
        if DATE_PATTERN_SIMPLE.match(date_str):
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return True, "Valid (YYYY-MM-DD)"
            except ValueError as e:
                logger.debug(f"Date regex matched but parsing failed: {date_str} - {e}")
                return False, f"Invalid format: {date_value}"

        if DATE_PATTERN_ISO.match(date_str):
            # ISO 8601 format - accept without full parsing
            return True, "Valid (ISO 8601)"

        # Fallback: no regex match
        return False, f"Invalid format: {date_value}"

    def validate_image_path(self, image_path: Optional[str]) -> Tuple[bool, str]:
        """Validate hero image path exists.

        Checks both absolute paths and paths relative to project root.

        Args:
            image_path: Path to hero image (absolute or relative to project root).

        Returns:
            Tuple containing:
                - is_valid: True if image file exists at specified path.
                - status_message: Validation result or error description.

        Examples:
            >>> validator = MetadataValidator(Path("posts"))
            >>> valid, msg = validator.validate_image_path("/images/hero.jpg")
            >>> print(valid, msg)
            True Valid
        """
        if not image_path:
            return False, "Missing"

        try:
            # Check if absolute path exists
            img_path: Path = Path(image_path)
            if img_path.is_absolute():
                if not img_path.exists():
                    return False, f"Path not found: {image_path}"
            else:
                # Check relative to project root
                full_path: Path = self.posts_dir.parent.parent / image_path.lstrip('/')
                if not full_path.exists():
                    return False, f"Path not found: {image_path}"

            return True, "Valid"
        except (OSError, ValueError) as e:
            logger.debug(f"Image path validation error: {image_path} - {e}")
            return False, f"Invalid path: {image_path}"

    def validate_tags(self, tags: Any) -> Tuple[bool, str]:
        """Validate tags presence and count.

        Checks that tags field is a non-empty list with appropriate count.
        Optimal range is 3-8 tags for SEO and discoverability.

        Args:
            tags: List of tag strings from frontmatter (or other type if invalid).

        Returns:
            Tuple containing:
                - is_valid: True if tags meet minimum requirements.
                - status_message: Validation result with tag count.

        Examples:
            >>> validator = MetadataValidator(Path("posts"))
            >>> valid, msg = validator.validate_tags(["python", "tutorial", "web"])
            >>> print(valid, msg)
            True Good (3 tags)
        """
        if not tags:
            return False, "Missing"

        if not isinstance(tags, list):
            return False, "Not a list"

        tag_count: int = len(tags)
        if tag_count == 0:
            return False, "Empty list"
        elif tag_count < self.TAG_MIN_WARN:
            return True, f"Sparse ({tag_count} tags, recommend 3-8)"
        elif tag_count > self.TAG_MAX:
            return False, f"Too many ({tag_count} tags, recommend 3-8)"
        else:
            return True, f"Good ({tag_count} tags)"

    def validate_post(self, file_path: Path) -> Dict[str, Any]:
        """Validate all metadata for a single post.

        Runs all validation checks on a blog post's YAML frontmatter and
        aggregates results into issues (must fix) and warnings (suggestions).

        Args:
            file_path: Path to blog post markdown file.

        Returns:
            Dictionary containing:
                - file: Filename of the validated post.
                - issues: List of validation errors (critical).
                - warnings: List of suggestions (non-critical).
                - valid: Boolean indicating if post passes all checks.

        Examples:
            >>> validator = MetadataValidator(Path("posts"))
            >>> result = validator.validate_post(Path("posts/my-post.md"))
            >>> if not result['valid']:
            ...     print(result['issues'])
        """
        post_result: Dict[str, Any] = {
            "file": file_path.name,
            "issues": [],
            "warnings": [],
            "valid": True
        }

        # Extract frontmatter
        frontmatter, error = self.extract_frontmatter(file_path)
        if error:
            post_result["issues"].append(f"Frontmatter error: {error}")
            post_result["valid"] = False
            return post_result

        # Validate title
        if not frontmatter.get('title'):
            post_result["issues"].append("Missing title")
            post_result["valid"] = False
            with self._lock:
                self.results["issues_summary"]["missing_title"] += 1

        # Validate description
        description_valid, description_msg = self.validate_description_length(
            frontmatter.get('description', '')
        )
        if not description_valid:
            if "Missing" in description_msg:
                post_result["issues"].append(f"Description: {description_msg}")
                with self._lock:
                    self.results["issues_summary"]["missing_description"] += 1
            else:
                post_result["issues"].append(f"Description: {description_msg}")
                with self._lock:
                    self.results["issues_summary"]["invalid_description_length"] += 1
            post_result["valid"] = False
        elif "Acceptable" in description_msg:
            post_result["warnings"].append(f"Description: {description_msg}")

        # Validate date
        date_valid, date_msg = self.validate_date_format(frontmatter.get('date'))
        if not date_valid:
            post_result["issues"].append(f"Date: {date_msg}")
            post_result["valid"] = False
            with self._lock:
                self.results["issues_summary"]["invalid_date_format"] += 1

        # Validate author
        if not frontmatter.get('author'):
            post_result["issues"].append("Missing author")
            post_result["valid"] = False
            with self._lock:
                self.results["issues_summary"]["missing_author"] += 1

        # Validate tags
        tags_valid, tags_msg = self.validate_tags(frontmatter.get('tags', []))
        if not tags_valid:
            post_result["issues"].append(f"Tags: {tags_msg}")
            post_result["valid"] = False
            with self._lock:
                self.results["issues_summary"]["missing_tags"] += 1
        elif "Sparse" in tags_msg:
            post_result["warnings"].append(f"Tags: {tags_msg}")

        # Validate hero image
        hero_image = frontmatter.get('hero_image') or frontmatter.get('heroImage')
        if hero_image:
            image_valid, image_msg = self.validate_image_path(hero_image)
            if not image_valid:
                post_result["issues"].append(f"Hero image: {image_msg}")
                post_result["valid"] = False
                with self._lock:
                    self.results["issues_summary"]["broken_image_paths"] += 1
        else:
            post_result["warnings"].append("Hero image: Missing (not critical)")
            with self._lock:
                self.results["issues_summary"]["missing_hero_image"] += 1

        if not post_result["valid"] or post_result["warnings"]:
            with self._lock:
                self.results["posts_with_issues"].append(post_result)

        return post_result

    def validate_all_posts(self) -> Dict[str, Any]:
        """Validate all posts in the posts directory (parallel execution).

        Scans all markdown files in the configured posts directory and runs
        validation checks on each using ThreadPoolExecutor for parallel I/O.
        Aggregates results into summary statistics.

        Parallel execution available via self.workers parameter but sequential
        (workers=1) is fastest for this workload due to low I/O wait time.

        Returns:
            Dictionary containing:
                - total_posts: Total number of markdown files scanned.
                - posts_with_issues: List of posts with errors or warnings.
                - metadata_coverage: Statistics dict with validation counts.
                - issues_summary: Breakdown of specific issue types.

        Examples:
            >>> validator = MetadataValidator(Path("posts"), workers=6)
            >>> results = validator.validate_all_posts()
            >>> print(f"Valid: {results['metadata_coverage']['posts_valid']}")
        """
        post_files: List[Path] = sorted(self.posts_dir.glob("*.md"))
        self.results["total_posts"] = len(post_files)

        logger.info("=" * 80)
        logger.info("METADATA VALIDATION REPORT")
        logger.info("=" * 80)
        logger.info(f"Validating {len(post_files)} posts in {self.posts_dir}/ (parallel: {self.workers} workers)...")

        valid_count: int = 0
        warning_count: int = 0

        # Parallel validation with ThreadPoolExecutor (I/O-bound task)
        if self.workers > 1 and len(post_files) > 1:
            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                # Submit all validation tasks
                future_to_file = {
                    executor.submit(self.validate_post, post_file): post_file
                    for post_file in post_files
                }

                # Collect results as they complete (with timeout per file)
                for future in as_completed(future_to_file, timeout=30):
                    post_file = future_to_file[future]
                    try:
                        result: Dict[str, Any] = future.result(timeout=5)
                        if result["valid"] and not result["warnings"]:
                            valid_count += 1
                        elif result["warnings"] and not result["issues"]:
                            warning_count += 1
                    except TimeoutError:
                        logger.error(f"Timeout validating {post_file.name}")
                    except Exception as e:
                        logger.error(f"Error validating {post_file.name}: {e}", exc_info=True)
        else:
            # Sequential fallback for single worker or single file
            for post_file in post_files:
                try:
                    result: Dict[str, Any] = self.validate_post(post_file)
                    if result["valid"] and not result["warnings"]:
                        valid_count += 1
                    elif result["warnings"] and not result["issues"]:
                        warning_count += 1
                except Exception as e:
                    logger.error(f"Error validating {post_file.name}: {e}", exc_info=True)

        # Calculate coverage
        total_posts: int = self.results["total_posts"]
        validation_rate: float = (valid_count / total_posts * 100) if total_posts > 0 else 0.0

        self.results["metadata_coverage"] = {
            "posts_valid": valid_count,
            "posts_with_warnings": warning_count,
            "posts_with_errors": len(self.results["posts_with_issues"]) - warning_count,
            "validation_rate": f"{validation_rate:.1f}%"
        }

        return self.results

    def print_text_report(self) -> None:
        """Print formatted text report to console.

        Outputs human-readable validation results including:
        - Summary statistics (total posts, validation rate)
        - Issue breakdown by type
        - Detailed per-post issues and warnings
        - Final status (PASSED/FAILED)

        Note: Uses logger for structured output. Print statements only used
        for JSON output in print_json_report().
        """
        # Summary statistics
        logger.info("\n📊 Summary Statistics:")
        logger.info(f"  - Total posts: {self.results['total_posts']}")
        logger.info(f"  - Posts valid: {self.results['metadata_coverage']['posts_valid']}")
        logger.info(f"  - Posts with warnings: {self.results['metadata_coverage']['posts_with_warnings']}")
        logger.info(f"  - Posts with errors: {self.results['metadata_coverage']['posts_with_errors']}")
        logger.info(f"  - Validation rate: {self.results['metadata_coverage']['validation_rate']}")

        # Issues breakdown
        issues = self.results["issues_summary"]
        has_issues = any(count > 0 for count in issues.values())

        if has_issues:
            logger.info("\n📋 Issues Breakdown:")
            for issue_type, count in issues.items():
                if count > 0:
                    level = "ERROR" if count > 5 else "WARNING"
                    logger.warning(f"  - {issue_type.replace('_', ' ').title()}: {count} ({level})")

        # Detailed issues
        if self.results["posts_with_issues"]:
            logger.info("\n📄 Detailed Issues:")
            for post in self.results["posts_with_issues"]:
                rel_path = Path(post['file'])
                logger.info(f"\n  {rel_path.name}")
                logger.info("  " + "-" * 78)

                if post["issues"]:
                    logger.error("  Errors:")
                    for issue in post["issues"]:
                        logger.error(f"    • {issue}")

                if post["warnings"]:
                    logger.warning("  Warnings:")
                    for warning in post["warnings"]:
                        logger.warning(f"    • {warning}")

        logger.info("\n" + "=" * 80)

        # Final status
        if self.results['metadata_coverage']['posts_with_errors'] > 0:
            logger.error("❌ Validation FAILED - Fix errors before committing")
        elif self.results['metadata_coverage']['posts_with_warnings'] > 0:
            logger.warning("⚠️  Validation PASSED with warnings")
        else:
            logger.info("✅ Validation PASSED - All metadata valid")

    def print_json_report(self) -> None:
        """Print JSON report for CI/CD integration.

        Outputs validation results as JSON to stdout for parsing by CI/CD
        pipelines or other automation tools.

        Note: This is the ONLY method that uses print() instead of logger,
        as it produces machine-readable output that should go to stdout.
        """
        print(json.dumps(self.results, indent=2))

    def run(self) -> int:
        """Run the validation process.

        Validates all posts in the configured directory and returns
        appropriate exit code for shell scripts and CI/CD integration.

        Returns:
            Exit code:
                - 0: Validation passed (all posts valid or only warnings).
                - 1: Validation failed (posts with errors or directory not found).

        Raises:
            OSError: If posts directory cannot be accessed.
        """
        if not self.posts_dir.exists():
            logger.error(f"Posts directory not found: {self.posts_dir}")
            return 1

        self.validate_all_posts()
        return 1 if self.results['metadata_coverage']['posts_with_errors'] > 0 else 0


def main() -> int:
    """Main entry point for metadata-validator.py script.

    Parses command-line arguments, configures validator, runs validation,
    and outputs report in requested format (text or JSON).

    Returns:
        Exit code:
            - 0: Validation passed (no errors).
            - 1: Validation failed (errors detected) or fatal error.
            - 130: User interrupted with Ctrl+C.

    Examples:
        Run from command line:
            $ uv run python scripts/validation/metadata-validator.py
            $ uv run python scripts/validation/metadata-validator.py --format json
    """
    parser = argparse.ArgumentParser(
        description='Validate blog post metadata for quality and completeness',
        epilog='Example: %(prog)s --format json --workers 8'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--posts-dir',
        type=Path,
        default=Path(__file__).parent.parent.parent / 'src' / 'posts',
        help='Posts directory (default: src/posts)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Number of parallel workers (default: 1 [optimal], min: 1)'
    )

    args = parser.parse_args()

    try:
        validator = MetadataValidator(posts_dir=args.posts_dir, workers=args.workers)
        exit_code = validator.run()

        if args.format == 'json':
            validator.print_json_report()
        else:
            validator.print_text_report()

        return exit_code

    except KeyboardInterrupt:
        logger.warning("\nValidation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
