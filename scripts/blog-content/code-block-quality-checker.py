#!/usr/bin/env -S uv run python3
"""
Code Block Quality Checker for Blog Posts

AUTHORITATIVE PURPOSE:
======================

Validates code blocks in blog posts against quality standards defined in
CODE_BLOCK_CONTENT_STANDARDS.md. Ensures code blocks enhance reader
understanding and maintain professional quality.

VALIDATION CRITERIA:
-------------------

1. **Annotations**: Non-obvious logic has explanatory comments
2. **Language Tags**: All code blocks have language identifiers
3. **Completeness**: Runnable code is complete or links to full version
4. **Gist Extraction**: Flags opportunities for extracting verbose code
5. **Truncation**: Detects unmarked pseudocode/incomplete snippets
6. **Security Warnings**: Verifies PoC code includes responsible use warnings
7. **Attribution**: Checks adapted code has source attribution

QUALITY PATTERNS (Session 22):
------------------------------

**KEEP inline (<15 lines):**
- Teaches core concept (syntax examples, key patterns)
- Context-critical (interrupting flow breaks learning)
- Complete and runnable (or clearly labeled as simplified)

**EXTRACT to gist (>20 lines):**
- Complete implementations readers will copy-paste
- Reference material (full configs, complete scripts)
- Reusable across projects

**DELETE/CONVERT:**
- Truncated with "# ... (additional implementation)" - incomplete pseudocode
- Redundant with official documentation (link instead)
- Better expressed as prose (2-3 sentences)
- Better expressed as Mermaid diagram (workflows, sequences)

USAGE:
------

Audit mode (analyze all posts):
    uv run python scripts/blog-content/code-block-quality-checker.py --audit

Validate single post:
    uv run python scripts/blog-content/code-block-quality-checker.py --post src/posts/file.md

Identify gist extraction opportunities:
    uv run python scripts/blog-content/code-block-quality-checker.py --extract --batch

Generate quality report:
    uv run python scripts/blog-content/code-block-quality-checker.py --report output.csv

Batch processing:
    uv run python scripts/blog-content/code-block-quality-checker.py --batch --validate

CROSS-REFERENCES:
----------------
- Standards: docs/STANDARDS/CODE_BLOCK_CONTENT_STANDARDS.md
- Gist workflow: docs/context/workflows/gist-management.md
- Code ratio tool: scripts/blog-content/code-ratio-calculator.py

Author: Claude Code Agent
Version: 1.0.0
Created: 2025-11-11
Last Updated: 2025-11-11
"""

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

VERSION = "1.0.0"
logger = setup_logger(__name__)


@dataclass
class CodeBlockIssue:
    """
    Represents a quality issue found in a code block.

    Attributes:
        block_number: Index of the code block in the post (1-indexed)
        line_start: Line number where code block begins
        line_end: Line number where code block ends
        issue_type: Category of issue (annotation, language_tag, truncation, etc.)
        severity: HIGH, MEDIUM, LOW
        description: Human-readable description of the issue
        recommendation: Suggested fix
    """
    block_number: int
    line_start: int
    line_end: int
    issue_type: str
    severity: str
    description: str
    recommendation: str

    def __str__(self) -> str:
        return (f"Block {self.block_number} (lines {self.line_start}-{self.line_end}): "
                f"[{self.severity}] {self.description}")


@dataclass
class CodeBlockAnalysis:
    """
    Analysis result for a single code block.

    Attributes:
        block_number: Index in post (1-indexed)
        line_start: Starting line number
        line_end: Ending line number
        line_count: Number of lines in block
        language: Language identifier (e.g., 'python', 'bash')
        has_language_tag: Whether language tag is present
        has_annotations: Whether block contains comments
        is_truncated: Whether block contains truncation markers
        is_runnable: Whether code appears to be complete
        needs_gist_extraction: Whether block is candidate for gist
        issues: List of quality issues found
    """
    block_number: int
    line_start: int
    line_end: int
    line_count: int
    language: str
    has_language_tag: bool
    has_annotations: bool
    is_truncated: bool
    is_runnable: bool
    needs_gist_extraction: bool
    issues: List[CodeBlockIssue] = field(default_factory=list)

    def quality_score(self) -> int:
        """
        Calculate quality score for this block (0-100).

        Scoring:
        - Start at 100
        - Deduct 20 for missing language tag
        - Deduct 15 for lack of annotations (if >10 lines)
        - Deduct 25 for truncation without clear labels
        - Deduct 10 for each HIGH severity issue
        - Deduct 5 for each MEDIUM severity issue
        """
        score = 100

        if not self.has_language_tag:
            score -= 20

        if not self.has_annotations and self.line_count > 10:
            score -= 15

        if self.is_truncated:
            score -= 25

        for issue in self.issues:
            if issue.severity == "HIGH":
                score -= 10
            elif issue.severity == "MEDIUM":
                score -= 5

        return max(0, score)


@dataclass
class PostQualityResult:
    """
    Complete quality analysis for a blog post.

    Attributes:
        filename: Name of the analyzed file
        total_blocks: Number of code blocks found
        blocks: List of individual block analyses
        overall_score: Average quality score across all blocks
        total_issues: Total number of issues found
        high_severity_count: Number of HIGH severity issues
        medium_severity_count: Number of MEDIUM severity issues
        low_severity_count: Number of LOW severity issues
        gist_extraction_candidates: Number of blocks suitable for gist extraction
        compliant: Whether post meets minimum quality standards
    """
    filename: str
    total_blocks: int
    blocks: List[CodeBlockAnalysis]
    overall_score: float
    total_issues: int
    high_severity_count: int
    medium_severity_count: int
    low_severity_count: int
    gist_extraction_candidates: int
    compliant: bool

    def to_dict(self) -> Dict:
        """Convert result to dictionary for JSON serialization."""
        return {
            "filename": self.filename,
            "total_blocks": self.total_blocks,
            "blocks": [
                {
                    "block_number": b.block_number,
                    "line_range": f"{b.line_start}-{b.line_end}",
                    "line_count": b.line_count,
                    "language": b.language,
                    "quality_score": b.quality_score(),
                    "issues": [
                        {
                            "type": i.issue_type,
                            "severity": i.severity,
                            "description": i.description,
                            "recommendation": i.recommendation
                        }
                        for i in b.issues
                    ]
                }
                for b in self.blocks
            ],
            "overall_score": round(self.overall_score, 1),
            "total_issues": self.total_issues,
            "severity_breakdown": {
                "high": self.high_severity_count,
                "medium": self.medium_severity_count,
                "low": self.low_severity_count
            },
            "gist_extraction_candidates": self.gist_extraction_candidates,
            "compliant": self.compliant
        }


# TRUNCATION PATTERNS
# Detect incomplete code that should be marked as pseudocode
TRUNCATION_MARKERS = [
    r'#\s*\.{3}',                           # Python: # ...
    r'//\s*\.{3}',                          # C/JS: // ...
    r'#\s*\(additional implementation\)',   # Python: # (additional implementation)
    r'//\s*\(additional implementation\)',  # C/JS: // (additional implementation)
    r'#\s*more code here',                  # Python: # more code here
    r'//\s*more code here',                 # C/JS: // more code here
    r'\.{3}\s*$',                           # Trailing ellipsis
]

# SECURITY CODE PATTERNS
# Code that should include warnings
SECURITY_KEYWORDS = [
    'exploit', 'vulnerability', 'attack', 'payload',
    'injection', 'shell', 'exec', 'eval', 'drop table',
    'xss', 'csrf', 'ssrf', 'rce', 'privilege escalation'
]

# ATTRIBUTION PATTERNS
# Adapted code should have source attribution
ATTRIBUTION_MARKERS = [
    r'adapted from',
    r'source:',
    r'based on',
    r'credit:',
    r'inspired by',
    r'https?://github\.com',
    r'https?://stackoverflow\.com'
]


def skip_frontmatter(lines: List[str]) -> int:
    """
    Find the end of YAML frontmatter and return the starting index for content.

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

    logger.warning("Frontmatter opening --- found but no closing marker")
    return 0


def extract_code_blocks_with_context(lines: List[str], content_start: int) -> List[Dict]:
    """
    Extract all code blocks with surrounding context for quality analysis.

    Args:
        lines: All lines from the markdown file
        content_start: Index where content begins (after frontmatter)

    Returns:
        List of dictionaries containing:
        - block_number: 1-indexed block number
        - line_start: Starting line (1-indexed)
        - line_end: Ending line (1-indexed)
        - language: Language identifier
        - content: List of code lines
        - preceding_prose: 3 lines of prose before block
        - following_prose: 3 lines of prose after block
    """
    # TODO: Implement code block extraction with context
    # Reference: code-ratio-calculator.py extract_code_blocks()
    # Enhancement: Include surrounding prose for context analysis
    raise NotImplementedError("extract_code_blocks_with_context() to be implemented by researcher")


def analyze_code_block(block: Dict, standards: Dict) -> CodeBlockAnalysis:
    """
    Analyze a single code block for quality issues.

    Args:
        block: Dictionary with block metadata and content
        standards: Quality standards configuration

    Returns:
        CodeBlockAnalysis with issues and scores

    Quality checks:
    1. Language tag present
    2. Annotations for non-obvious logic
    3. Truncation markers without labels
    4. Completeness (runnable vs pseudocode)
    5. Security warnings for exploit code
    6. Attribution for adapted code
    7. Gist extraction opportunity (>20 lines)
    """
    # TODO: Implement quality analysis logic
    # - Check language tag presence
    # - Scan for comment density
    # - Detect truncation patterns
    # - Identify security keywords without warnings
    # - Check attribution for non-trivial code
    # - Flag gist extraction candidates
    raise NotImplementedError("analyze_code_block() to be implemented by researcher")


def analyze_post(filepath: Path, min_score: int = 70) -> PostQualityResult:
    """
    Analyze all code blocks in a blog post for quality.

    Args:
        filepath: Path to markdown file
        min_score: Minimum acceptable quality score (0-100)

    Returns:
        PostQualityResult with complete analysis

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty or invalid
    """
    logger.info(f"Analyzing post: {filepath}")

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Read all lines
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError(f"File is empty: {filepath}")

    # Skip frontmatter
    content_start = skip_frontmatter(lines)

    # Extract code blocks with context
    # TODO: blocks = extract_code_blocks_with_context(lines, content_start)

    # Analyze each block
    # TODO: block_analyses = [analyze_code_block(block, standards) for block in blocks]

    # Calculate overall metrics
    # TODO: Calculate scores, count issues, identify gist candidates

    # Placeholder return
    return PostQualityResult(
        filename=filepath.name,
        total_blocks=0,
        blocks=[],
        overall_score=0.0,
        total_issues=0,
        high_severity_count=0,
        medium_severity_count=0,
        low_severity_count=0,
        gist_extraction_candidates=0,
        compliant=False
    )


def format_result(result: PostQualityResult, verbose: bool = True) -> str:
    """
    Format analysis result for human-readable output.

    Args:
        result: PostQualityResult to format
        verbose: Whether to show detailed block breakdown

    Returns:
        Formatted string ready for console output
    """
    # TODO: Implement human-readable formatting
    # Similar to code-ratio-calculator.py format_result()
    raise NotImplementedError("format_result() to be implemented")


def generate_csv_report(results: List[PostQualityResult], output_path: Path) -> None:
    """
    Generate CSV report of code block quality across all posts.

    Args:
        results: List of PostQualityResult objects
        output_path: Path to output CSV file

    CSV columns:
    - filename
    - total_blocks
    - overall_score
    - total_issues
    - high_severity
    - medium_severity
    - low_severity
    - gist_candidates
    - compliant
    """
    # TODO: Implement CSV generation
    # Reference: analyze-compliance.py CSV export pattern
    raise NotImplementedError("generate_csv_report() to be implemented")


def main() -> int:
    """
    Main entry point for CLI usage.

    Returns:
        Exit code (0 = success, 1 = failure, 2 = quality issues found)
    """
    parser = argparse.ArgumentParser(
        description="Validate code block quality in blog posts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit all posts
  %(prog)s --audit

  # Validate single post
  %(prog)s --post src/posts/my-post.md

  # Identify gist extraction opportunities
  %(prog)s --extract --batch

  # Generate quality report
  %(prog)s --report output.csv --batch

  # Strict mode (fail on any violation)
  %(prog)s --batch --validate --min-score 90

Quality Standards:
  See docs/STANDARDS/CODE_BLOCK_CONTENT_STANDARDS.md for complete criteria.
        """
    )

    parser.add_argument(
        "--post",
        type=Path,
        help="Path to single blog post to analyze"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Analyze all posts in src/posts/"
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Audit mode: Analyze quality across all posts"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validation mode: Check annotations, language tags, completeness"
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Identify gist extraction opportunities"
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Generate CSV report at specified path"
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=70,
        help="Minimum acceptable quality score (default: 70)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Configure logging level
    if args.debug:
        logger.setLevel("DEBUG")

    # Validate arguments
    if not args.post and not args.batch and not args.audit:
        parser.error("Must specify either --post, --batch, or --audit")

    # TODO: Implement main logic
    # 1. Collect files to analyze
    # 2. Run quality checks
    # 3. Generate reports
    # 4. Return appropriate exit code

    logger.info("Code block quality checker initialized")
    logger.warning("Implementation pending - waiting for researcher baseline")

    return 0


if __name__ == "__main__":
    sys.exit(main())
