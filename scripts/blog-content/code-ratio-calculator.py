#!/usr/bin/env -S uv run python3
"""
Code Ratio Calculator for Blog Posts

AUTHORITATIVE METHODOLOGY:
=========================

This tool is the single source of truth for code ratio measurements across all blog posts.
It implements the standardized methodology defined in CLAUDE.md and used by pre-commit hooks.

CALCULATION METHOD:
------------------

1. **Frontmatter Exclusion**: Skip all lines from start until the closing `---` marker
2. **Code Block Detection**: Count lines BETWEEN triple-backtick (```) fence markers
3. **Marker Exclusion**: Do NOT count the ``` fence markers themselves
4. **Blank Line Handling**: Exclude blank/whitespace-only lines within code blocks
5. **Total Line Count**: All content lines after frontmatter (including blank lines)
6. **Formula**: (code_lines / content_lines) * 100

EXAMPLE CALCULATION:
-------------------

Given this post:
```
---
title: Test Post
---

Some intro text.

```bash
echo "hello"
echo "world"
```

More text.
```

Step-by-step:
- Frontmatter: lines 1-3 (excluded)
- Content lines: 6 (including blank line after intro, excluding code fence markers)
- Code lines in block: 2 (both echo commands)
- Blank lines in code block: 0
- Code ratio: (2 / 6) * 100 = 33.3%

USAGE:
------

Single post analysis:
    uv run python scripts/blog-content/code-ratio-calculator.py --post src/posts/file.md

Batch analysis:
    uv run python scripts/blog-content/code-ratio-calculator.py --batch

JSON output:
    uv run python scripts/blog-content/code-ratio-calculator.py --post file.md --json

Set custom threshold:
    uv run python scripts/blog-content/code-ratio-calculator.py --batch --threshold 30

Author: Claude Code Agent
Version: 1.1.0
Last Updated: 2025-11-03
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)


@dataclass
class CodeBlock:
    """
    Represents a single code block within a markdown file.

    Attributes:
        start_line: Line number where ``` fence begins (1-indexed)
        end_line: Line number where closing ``` fence appears (1-indexed)
        code_lines: Number of non-blank lines between fences
        language: Language identifier (e.g., 'python', 'bash', or '' if none)
    """
    start_line: int
    end_line: int
    code_lines: int
    language: str

    def __str__(self) -> str:
        lang_display = f"[{self.language}]" if self.language else "[no-language]"
        return f"Block at lines {self.start_line}-{self.end_line}: {self.code_lines} lines {lang_display}"


@dataclass
class CodeRatioResult:
    """
    Complete analysis result for a single blog post.

    Attributes:
        filename: Name of the analyzed file
        total_lines: Total content lines (excluding frontmatter)
        code_blocks: List of detected code blocks
        total_code_lines: Sum of all code lines across blocks
        mermaid_lines: Lines in Mermaid diagram blocks
        actual_code_lines: Lines in non-Mermaid code blocks
        code_ratio: Percentage of code vs total content
        mermaid_percentage: Percentage of Mermaid within all code
        actual_code_percentage: Percentage of actual code vs total content
        compliant: Whether ratio is below threshold
        threshold: Threshold used for compliance check
        is_diagram_heavy: Whether post is primarily Mermaid diagrams
    """
    filename: str
    total_lines: int
    code_blocks: List[CodeBlock]
    total_code_lines: int
    mermaid_lines: int
    actual_code_lines: int
    code_ratio: float
    mermaid_percentage: float
    actual_code_percentage: float
    compliant: bool
    threshold: float
    is_diagram_heavy: bool

    def to_dict(self) -> Dict:
        """Convert result to dictionary for JSON serialization."""
        return {
            "filename": self.filename,
            "total_lines": self.total_lines,
            "code_blocks": [
                {
                    "start_line": block.start_line,
                    "end_line": block.end_line,
                    "code_lines": block.code_lines,
                    "language": block.language
                }
                for block in self.code_blocks
            ],
            "total_code_lines": self.total_code_lines,
            "mermaid_lines": self.mermaid_lines,
            "actual_code_lines": self.actual_code_lines,
            "code_ratio": round(self.code_ratio, 1),
            "mermaid_percentage": round(self.mermaid_percentage, 1),
            "actual_code_percentage": round(self.actual_code_percentage, 1),
            "compliant": self.compliant,
            "threshold": self.threshold,
            "is_diagram_heavy": self.is_diagram_heavy
        }


def skip_frontmatter(lines: List[str]) -> int:
    """
    Find the end of YAML frontmatter and return the starting index for content.

    Args:
        lines: All lines from the markdown file

    Returns:
        Index of first line after frontmatter (0-indexed)

    Example:
        >>> lines = ["---", "title: Test", "---", "Content"]
        >>> skip_frontmatter(lines)
        3
    """
    if not lines or not lines[0].strip().startswith("---"):
        return 0

    # Find the closing --- marker
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1

    # No closing marker found, treat as no frontmatter
    logger.warning("Frontmatter opening --- found but no closing marker")
    return 0


def extract_code_blocks(lines: List[str], content_start: int) -> Tuple[List[CodeBlock], int, int, int]:
    """
    Extract all code blocks from content lines, tracking Mermaid separately.

    METHODOLOGY:
    -----------
    1. Iterate through lines starting after frontmatter
    2. Detect opening ``` fence (with optional language identifier)
    3. Count non-blank lines until closing ``` fence
    4. Store block metadata (start, end, line count, language)
    5. Track Mermaid blocks separately for diagram-heavy detection
    6. Exclude fence markers themselves from all counts

    Args:
        lines: All lines from the markdown file
        content_start: Index where content begins (after frontmatter)

    Returns:
        Tuple of (list of CodeBlock objects, total code lines, mermaid lines, actual code lines)

    Example:
        >>> lines = ["---", "title: Test", "---", "", "```python", "print(1)", "", "print(2)", "```"]
        >>> blocks, total, mermaid, actual = extract_code_blocks(lines, 3)
        >>> len(blocks)
        1
        >>> total
        2
        >>> actual
        2
    """
    code_blocks: List[CodeBlock] = []
    total_code_lines = 0
    mermaid_lines = 0
    actual_code_lines = 0
    in_code_block = False
    current_block_start = 0
    current_block_lines = 0
    current_language = ""

    for i in range(content_start, len(lines)):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code_block:
                # Opening fence
                in_code_block = True
                current_block_start = i + 1  # +1 for 1-indexed display
                current_block_lines = 0
                # Extract language identifier (e.g., "```python" -> "python")
                current_language = stripped[3:].strip()
            else:
                # Closing fence
                block = CodeBlock(
                    start_line=current_block_start,
                    end_line=i + 1,  # +1 for 1-indexed display
                    code_lines=current_block_lines,
                    language=current_language
                )
                code_blocks.append(block)
                total_code_lines += current_block_lines

                # Track Mermaid vs actual code separately
                if current_language.lower() == 'mermaid':
                    mermaid_lines += current_block_lines
                else:
                    actual_code_lines += current_block_lines

                in_code_block = False
                current_language = ""
        elif in_code_block:
            # Count non-blank lines within code block
            if stripped:  # Non-empty line
                current_block_lines += 1

    # Handle unclosed code block
    if in_code_block:
        logger.warning(f"Unclosed code block starting at line {current_block_start}")
        block = CodeBlock(
            start_line=current_block_start,
            end_line=len(lines),
            code_lines=current_block_lines,
            language=current_language
        )
        code_blocks.append(block)
        total_code_lines += current_block_lines

        # Track Mermaid vs actual code for unclosed block
        if current_language.lower() == 'mermaid':
            mermaid_lines += current_block_lines
        else:
            actual_code_lines += current_block_lines

    return code_blocks, total_code_lines, mermaid_lines, actual_code_lines


def count_content_lines(lines: List[str], content_start: int) -> int:
    """
    Count total content lines, excluding frontmatter and code fence markers.

    METHODOLOGY:
    -----------
    - Count ALL lines after frontmatter (including blank lines)
    - Exclude the ``` fence markers themselves
    - Include blank lines in content count (they affect readability/structure)

    Args:
        lines: All lines from the markdown file
        content_start: Index where content begins (after frontmatter)

    Returns:
        Number of content lines

    Example:
        >>> lines = ["---", "title: Test", "---", "Text", "", "```bash", "echo", "```", "More"]
        >>> count_content_lines(lines, 3)
        5  # "Text", blank, "echo", blank, "More" (excludes 2 fence markers)
    """
    total_lines = 0
    in_code_block = False

    for i in range(content_start, len(lines)):
        line = lines[i].strip()

        if line.startswith("```"):
            in_code_block = not in_code_block
            # Do NOT count the fence marker itself
            continue

        # Count all other lines (including blanks)
        total_lines += 1

    return total_lines


def analyze_file(filepath: Path, threshold: float = 25.0) -> CodeRatioResult:
    """
    Analyze a single markdown file for code ratio with Mermaid distinction.

    Args:
        filepath: Path to markdown file
        threshold: Maximum acceptable code ratio percentage

    Returns:
        CodeRatioResult object with complete analysis

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty or invalid
    """
    logger.info(f"Analyzing file: {filepath}")

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Read all lines
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError(f"File is empty: {filepath}")

    # Step 1: Skip frontmatter
    content_start = skip_frontmatter(lines)
    logger.debug(f"Content starts at line {content_start + 1}")

    # Step 2: Extract code blocks with Mermaid tracking
    code_blocks, total_code_lines, mermaid_lines, actual_code_lines = extract_code_blocks(lines, content_start)
    logger.debug(f"Found {len(code_blocks)} code blocks with {total_code_lines} total code lines")
    logger.debug(f"  Mermaid: {mermaid_lines} lines, Actual code: {actual_code_lines} lines")

    # Step 3: Count total content lines
    total_lines = count_content_lines(lines, content_start)
    logger.debug(f"Total content lines: {total_lines}")

    # Step 4: Calculate ratios
    code_ratio = (total_code_lines / total_lines * 100) if total_lines > 0 else 0.0
    mermaid_percentage = (mermaid_lines / total_code_lines * 100) if total_code_lines > 0 else 0.0
    actual_code_percentage = (actual_code_lines / total_lines * 100) if total_lines > 0 else 0.0

    # Step 5: Determine if diagram-heavy
    # Criteria: >80% of code is Mermaid AND actual code <10% of post
    is_diagram_heavy = (mermaid_percentage > 80.0 and actual_code_percentage < 10.0)

    compliant = code_ratio <= threshold

    result = CodeRatioResult(
        filename=filepath.name,
        total_lines=total_lines,
        code_blocks=code_blocks,
        total_code_lines=total_code_lines,
        mermaid_lines=mermaid_lines,
        actual_code_lines=actual_code_lines,
        code_ratio=code_ratio,
        mermaid_percentage=mermaid_percentage,
        actual_code_percentage=actual_code_percentage,
        compliant=compliant,
        threshold=threshold,
        is_diagram_heavy=is_diagram_heavy
    )

    status = 'COMPLIANT' if compliant else 'EXCEEDS THRESHOLD'
    if is_diagram_heavy:
        status += ' (DIAGRAM-HEAVY)'
    logger.info(f"Analysis complete: {code_ratio:.1f}% code ratio ({status})")
    return result


def format_result(result: CodeRatioResult, show_blocks: bool = True) -> str:
    """
    Format analysis result for human-readable output with Mermaid breakdown.

    Args:
        result: CodeRatioResult to format
        show_blocks: Whether to show detailed block breakdown

    Returns:
        Formatted string ready for console output
    """
    status = "✅ COMPLIANT" if result.compliant else "❌ EXCEEDS THRESHOLD"

    output = [
        f"\nPost: {result.filename}",
        f"Total lines: {result.total_lines} (excluding frontmatter)",
        f"Code blocks: {len(result.code_blocks)}",
    ]

    if show_blocks and result.code_blocks:
        for i, block in enumerate(result.code_blocks, 1):
            output.append(f"  Block {i} (lines {block.start_line}-{block.end_line}): {block.code_lines} lines [{block.language or 'no-language'}]")

    # Enhanced breakdown showing Mermaid vs actual code
    if result.total_code_lines > 0:
        output.extend([
            f"Total code lines: {result.total_code_lines} ({result.code_ratio:.1f}%)",
            f"├─ Mermaid diagrams: {result.mermaid_lines} lines ({result.mermaid_percentage:.1f}% of code)",
            f"└─ Actual code: {result.actual_code_lines} lines ({result.actual_code_percentage:.1f}% of post)",
        ])
    else:
        output.append(f"Total code lines: {result.total_code_lines}")

    # Add diagram-heavy classification
    if result.is_diagram_heavy:
        output.extend([
            f"",
            f"Status: ⚠️  DIAGRAM-HEAVY ({result.mermaid_percentage:.1f}% Mermaid)",
            f"Recommendation: Educational visualizations - consider policy exception for ratio",
            f"Compliance: {status} (threshold: {result.threshold}%)",
        ])
    else:
        output.append(f"Status: {status} (threshold: {result.threshold}%)")

    return "\n".join(output)


def main() -> int:
    """
    Main entry point for CLI usage.

    Returns:
        Exit code (0 = success, 1 = failure, 2 = non-compliant files found)
    """
    parser = argparse.ArgumentParser(
        description="Calculate code-to-content ratio in blog posts using standardized methodology",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single post
  %(prog)s --post src/posts/my-post.md

  # Analyze all posts
  %(prog)s --batch

  # JSON output for automation
  %(prog)s --batch --json

  # Custom threshold
  %(prog)s --batch --threshold 30

  # Debug mode
  %(prog)s --post src/posts/my-post.md --debug

Methodology:
  See module docstring for complete calculation methodology.
  This tool matches pre-commit hook behavior exactly.
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
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=25.0,
        help="Code ratio threshold percentage (default: 25.0)"
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
    if not args.post and not args.batch:
        parser.error("Must specify either --post or --batch")

    if args.post and args.batch:
        parser.error("Cannot specify both --post and --batch")

    # Collect files to analyze
    files_to_analyze: List[Path] = []

    if args.post:
        if not args.post.exists():
            logger.error(f"File not found: {args.post}")
            return 1
        files_to_analyze.append(args.post)
    else:
        # Batch mode
        posts_dir = Path("src/posts")
        if not posts_dir.exists():
            logger.error(f"Posts directory not found: {posts_dir}")
            return 1

        files_to_analyze = sorted(posts_dir.glob("*.md"))
        if not files_to_analyze:
            logger.error(f"No markdown files found in {posts_dir}")
            return 1

        logger.info(f"Found {len(files_to_analyze)} posts to analyze")

    # Analyze all files
    results: List[CodeRatioResult] = []
    non_compliant_count = 0

    for filepath in files_to_analyze:
        try:
            result = analyze_file(filepath, args.threshold)
            results.append(result)
            if not result.compliant:
                non_compliant_count += 1
        except Exception as e:
            logger.error(f"Failed to analyze {filepath}: {e}")
            if args.debug:
                import traceback
                traceback.print_exc()
            return 1

    # Output results
    if args.json:
        output = {
            "summary": {
                "total_files": len(results),
                "compliant": len(results) - non_compliant_count,
                "non_compliant": non_compliant_count,
                "threshold": args.threshold
            },
            "results": [r.to_dict() for r in results]
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        for result in results:
            print(format_result(result, show_blocks=True))

        # Summary
        if len(results) > 1:
            avg_ratio = sum(r.code_ratio for r in results) / len(results)
            print(f"\n{'='*60}")
            print(f"Summary: {len(results)} files analyzed")
            print(f"Average code ratio: {avg_ratio:.1f}%")
            print(f"Compliant: {len(results) - non_compliant_count}")
            print(f"Non-compliant: {non_compliant_count}")
            print(f"Threshold: {args.threshold}%")

    # Return appropriate exit code
    if non_compliant_count > 0:
        logger.warning(f"{non_compliant_count} file(s) exceed code ratio threshold")
        return 2  # Non-zero but distinct from errors

    return 0


if __name__ == "__main__":
    sys.exit(main())
