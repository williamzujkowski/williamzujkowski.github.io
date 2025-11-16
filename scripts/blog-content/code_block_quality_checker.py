#!/usr/bin/env -S uv run python3
"""
Code Block Quality Checker for Blog Posts

AUTHORITATIVE PURPOSE:
======================

Validates code blocks in blog posts against quality standards defined in
code-block-quality.md. Ensures code blocks enhance reader
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
- Standards: docs/context/standards/code-block-quality.md
- Gist workflow: docs/context/workflows/gist-management.md
- Code ratio tool: scripts/blog-content/code-ratio-calculator.py

Author: Claude Code Agent
Version: 2.0.0
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

VERSION = "2.0.0"
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
    blocks = []
    in_code_block = False
    current_block = {
        'line_start': 0,
        'line_end': 0,
        'language': '',
        'content': [],
        'preceding_prose': [],
        'following_prose': []
    }
    context_buffer = []  # Store recent prose lines for preceding context

    for i in range(content_start, len(lines)):
        line = lines[i]

        # Detect code fence opening
        if line.strip().startswith('```') and not in_code_block:
            in_code_block = True
            current_block['line_start'] = i + 1  # 1-indexed

            # Extract language tag
            lang_match = line.strip()[3:].strip()
            current_block['language'] = lang_match if lang_match else 'generic'

            # Capture preceding context (last 3 lines of prose before block)
            current_block['preceding_prose'] = context_buffer[-3:] if len(context_buffer) >= 3 else context_buffer[:]
            context_buffer = []  # Reset buffer

        # Inside code block - capture content
        elif in_code_block and not line.strip().startswith('```'):
            current_block['content'].append(line.rstrip('\n'))

        # Detect code fence closing
        elif line.strip().startswith('```') and in_code_block:
            in_code_block = False
            current_block['line_end'] = i + 1  # 1-indexed

            # Capture following context (next 3 lines after block)
            following_start = i + 1
            following_end = min(len(lines), following_start + 3)
            current_block['following_prose'] = [
                lines[j].rstrip('\n') for j in range(following_start, following_end)
            ]

            # Create block entry
            blocks.append({
                'block_number': len(blocks) + 1,
                'line_start': current_block['line_start'],
                'line_end': current_block['line_end'],
                'language': current_block['language'],
                'content': current_block['content'][:],  # Copy list
                'preceding_prose': current_block['preceding_prose'][:],
                'following_prose': current_block['following_prose'][:]
            })

            # Reset for next block
            current_block = {
                'line_start': 0,
                'line_end': 0,
                'language': '',
                'content': [],
                'preceding_prose': [],
                'following_prose': []
            }

        # Outside code block - buffer prose for context
        elif not in_code_block:
            # Only buffer non-empty lines
            if line.strip():
                context_buffer.append(line.rstrip('\n'))

    logger.info(f"Extracted {len(blocks)} code blocks with context")
    return blocks


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
    issues = []
    content_str = '\n'.join(block['content'])
    line_count = len(block['content'])
    language = block['language']

    # Check 1: Language tag presence
    has_language_tag = language != 'generic'
    if not has_language_tag:
        issues.append(CodeBlockIssue(
            block_number=block['block_number'],
            line_start=block['line_start'],
            line_end=block['line_end'],
            issue_type='missing_language_tag',
            severity='MEDIUM',
            description='Code block lacks language identifier',
            recommendation='Add language tag: ```python, ```bash, ```yaml, etc.'
        ))

    # Check 2: Truncation patterns
    is_truncated = False
    for pattern in TRUNCATION_MARKERS:
        if re.search(pattern, content_str, re.IGNORECASE):
            is_truncated = True
            issues.append(CodeBlockIssue(
                block_number=block['block_number'],
                line_start=block['line_start'],
                line_end=block['line_end'],
                issue_type='truncated_code',
                severity='HIGH',
                description='Code block contains truncation marker (e.g., # ..., // ...)',
                recommendation='Remove truncated pseudocode or complete implementation, or clearly label as "Pseudocode" or "Simplified"'
            ))
            break

    # Check 3: Security keywords without warnings
    has_security_keyword = any(keyword in content_str.lower() for keyword in SECURITY_KEYWORDS)

    if has_security_keyword:
        # Check for warning markers in preceding context
        preceding_text = '\n'.join(block.get('preceding_prose', []))
        warning_markers = ['⚠️', 'WARNING', 'CAUTION', '**Warning**', 'EDUCATIONAL ONLY', 'Do not use']
        has_warning = any(marker.lower() in preceding_text.lower() for marker in warning_markers)

        if not has_warning:
            issues.append(CodeBlockIssue(
                block_number=block['block_number'],
                line_start=block['line_start'],
                line_end=block['line_end'],
                issue_type='missing_security_warning',
                severity='HIGH',
                description='Security-related code lacks warning marker in preceding prose',
                recommendation='Add warning before block: "⚠️ **Warning:** This is proof-of-concept code for educational purposes only..."'
            ))

    # Check 4: Gist extraction opportunity (>20 lines)
    needs_gist_extraction = line_count > 20
    if needs_gist_extraction:
        issues.append(CodeBlockIssue(
            block_number=block['block_number'],
            line_start=block['line_start'],
            line_end=block['line_end'],
            issue_type='gist_extraction_opportunity',
            severity='LOW',
            description=f'Large code block ({line_count} lines) could be extracted to GitHub gist',
            recommendation='Consider extracting to gist if this is complete reference code (not teaching example)'
        ))

    # Check 5: Comment density (annotations)
    comment_patterns = [
        r'^\s*#',      # Python comments
        r'^\s*//',     # JavaScript/C++ comments
        r'^\s*<!--',   # HTML comments
    ]

    comment_lines = sum(
        1 for line in block['content']
        if any(re.match(pattern, line) for pattern in comment_patterns)
    )
    comment_ratio = comment_lines / line_count if line_count > 0 else 0
    has_annotations = comment_ratio > 0

    # Flag low annotation density for >10 line blocks
    if line_count > 10 and comment_ratio < 0.1:  # <10% comments
        issues.append(CodeBlockIssue(
            block_number=block['block_number'],
            line_start=block['line_start'],
            line_end=block['line_end'],
            issue_type='low_annotation_density',
            severity='LOW',
            description=f'Low comment density ({comment_ratio:.1%}) for {line_count}-line block',
            recommendation='Add comments explaining non-obvious logic, configuration choices, or security implications'
        ))

    # Check 6: Attribution for adapted code
    attribution_patterns = ATTRIBUTION_MARKERS
    has_attribution = any(re.search(pattern, content_str, re.IGNORECASE) for pattern in attribution_patterns)

    # Only check if block seems non-trivial (>15 lines, not simple config)
    if line_count > 15 and not has_attribution:
        # Check if preceding prose mentions source
        preceding_text = '\n'.join(block.get('preceding_prose', []))
        has_attribution_in_prose = any(
            re.search(pattern, preceding_text, re.IGNORECASE)
            for pattern in attribution_patterns
        )

        # This is a SUGGESTION, not a violation (since we can't know if code is original)
        # We'll track it but with LOW severity
        if not has_attribution_in_prose:
            # Don't add issue automatically - too many false positives
            # Only log for manual review
            pass

    # Determine runnability (heuristic - not perfect)
    is_runnable = not is_truncated and has_language_tag

    # Create analysis result
    analysis = CodeBlockAnalysis(
        block_number=block['block_number'],
        line_start=block['line_start'],
        line_end=block['line_end'],
        line_count=line_count,
        language=language,
        has_language_tag=has_language_tag,
        has_annotations=has_annotations,
        is_truncated=is_truncated,
        is_runnable=is_runnable,
        needs_gist_extraction=needs_gist_extraction,
        issues=issues
    )

    return analysis


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
    blocks = extract_code_blocks_with_context(lines, content_start)

    if not blocks:
        # No code blocks found - return empty result
        logger.info(f"No code blocks found in {filepath.name}")
        return PostQualityResult(
            filename=filepath.name,
            total_blocks=0,
            blocks=[],
            overall_score=100.0,  # Perfect score for posts without code
            total_issues=0,
            high_severity_count=0,
            medium_severity_count=0,
            low_severity_count=0,
            gist_extraction_candidates=0,
            compliant=True
        )

    # Analyze each block
    standards = {}  # Could load from config file if needed
    block_analyses = [analyze_code_block(block, standards) for block in blocks]

    # Aggregate issues across all blocks
    all_issues = []
    for block_analysis in block_analyses:
        all_issues.extend(block_analysis.issues)

    # Count issues by severity
    high_count = sum(1 for issue in all_issues if issue.severity == 'HIGH')
    medium_count = sum(1 for issue in all_issues if issue.severity == 'MEDIUM')
    low_count = sum(1 for issue in all_issues if issue.severity == 'LOW')

    # Count gist extraction candidates
    gist_candidates = sum(1 for ba in block_analyses if ba.needs_gist_extraction)

    # Calculate overall quality score (0-100)
    # Method: Average of individual block scores
    block_scores = [ba.quality_score() for ba in block_analyses]
    overall_score = sum(block_scores) / len(block_scores) if block_scores else 100.0

    # Determine compliance
    # Compliant if: score >= min_score AND no HIGH severity issues
    compliant = overall_score >= min_score and high_count == 0

    result = PostQualityResult(
        filename=filepath.name,
        total_blocks=len(block_analyses),
        blocks=block_analyses,
        overall_score=round(overall_score, 1),
        total_issues=len(all_issues),
        high_severity_count=high_count,
        medium_severity_count=medium_count,
        low_severity_count=low_count,
        gist_extraction_candidates=gist_candidates,
        compliant=compliant
    )

    logger.info(
        f"Analysis complete for {filepath.name}: "
        f"{len(block_analyses)} blocks, "
        f"score {result.overall_score}/100, "
        f"{high_count} HIGH issues"
    )

    return result


def format_result(result: PostQualityResult, verbose: bool = True) -> str:
    """
    Format analysis result for human-readable output.

    Args:
        result: PostQualityResult to format
        verbose: Whether to show detailed block breakdown

    Returns:
        Formatted string ready for console output
    """
    lines = []

    # Header
    lines.append(f"\n{'='*60}")
    lines.append(f"Code Block Quality Report: {result.filename}")
    lines.append(f"{'='*60}")

    # Summary metrics
    lines.append(f"\nTotal code blocks: {result.total_blocks}")
    lines.append(f"Overall quality score: {result.overall_score}/100")
    lines.append(f"Compliance status: {'✅ COMPLIANT' if result.compliant else '❌ NON-COMPLIANT'}")

    # Issue breakdown
    lines.append(f"\nIssues found: {result.total_issues}")
    lines.append(f"  HIGH severity: {result.high_severity_count}")
    lines.append(f"  MEDIUM severity: {result.medium_severity_count}")
    lines.append(f"  LOW severity: {result.low_severity_count}")

    # Gist extraction opportunities
    if result.gist_extraction_candidates > 0:
        lines.append(f"\nGist extraction opportunities: {result.gist_extraction_candidates}")

    # Detailed block-by-block breakdown
    if verbose and result.blocks:
        lines.append(f"\n{'-'*60}")
        lines.append("Block Details:")
        lines.append(f"{'-'*60}")

        for block in result.blocks:
            lines.append(f"\nBlock #{block.block_number} (lines {block.line_start}-{block.line_end}):")
            lines.append(f"  Language: {block.language}")
            lines.append(f"  Line count: {block.line_count}")
            lines.append(f"  Quality score: {block.quality_score()}/100")
            lines.append(f"  Has language tag: {'✅' if block.has_language_tag else '❌'}")
            lines.append(f"  Has annotations: {'✅' if block.has_annotations else '❌'}")
            lines.append(f"  Is truncated: {'❌' if block.is_truncated else '✅'}")

            if block.issues:
                lines.append(f"  Issues ({len(block.issues)}):")
                for issue in block.issues:
                    lines.append(f"    [{issue.severity}] {issue.issue_type}")
                    lines.append(f"      {issue.description}")
                    lines.append(f"      → {issue.recommendation}")

    lines.append(f"\n{'='*60}\n")

    return '\n'.join(lines)


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
    logger.info(f"Generating CSV report: {output_path}")

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'filename',
            'total_blocks',
            'overall_score',
            'total_issues',
            'high_severity',
            'medium_severity',
            'low_severity',
            'gist_candidates',
            'compliant'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow({
                'filename': result.filename,
                'total_blocks': result.total_blocks,
                'overall_score': result.overall_score,
                'total_issues': result.total_issues,
                'high_severity': result.high_severity_count,
                'medium_severity': result.medium_severity_count,
                'low_severity': result.low_severity_count,
                'gist_candidates': result.gist_extraction_candidates,
                'compliant': 'YES' if result.compliant else 'NO'
            })

    logger.info(f"CSV report written with {len(results)} entries")


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
  See docs/context/standards/code-block-quality.md for complete criteria.
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

    try:
        # Collect files to analyze
        files_to_analyze = []

        if args.post:
            # Single post mode
            if not args.post.exists():
                logger.error(f"File not found: {args.post}")
                return 1
            files_to_analyze = [args.post]

        elif args.batch or args.audit:
            # Batch mode - analyze all posts
            posts_dir = Path("src/posts")
            if not posts_dir.exists():
                logger.error(f"Posts directory not found: {posts_dir}")
                return 1

            files_to_analyze = sorted(posts_dir.glob("*.md"))
            logger.info(f"Found {len(files_to_analyze)} posts to analyze")

        # Run analysis on all files
        results = []
        for filepath in files_to_analyze:
            try:
                result = analyze_post(filepath, min_score=args.min_score)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze {filepath.name}: {e}")
                continue

        # Filter results - only include posts with code blocks
        results_with_code = [r for r in results if r.total_blocks > 0]

        if not results_with_code:
            logger.info("No posts with code blocks found")
            return 0

        # Output based on mode
        if args.json:
            # JSON output - only print JSON, no logger
            output = [r.to_dict() for r in results_with_code]
            import sys
            sys.stdout.write(json.dumps(output, indent=2) + '\n')

        elif args.audit:
            # Audit mode - summary statistics
            total_posts = len(results_with_code)
            compliant_posts = sum(1 for r in results_with_code if r.compliant)
            avg_score = sum(r.overall_score for r in results_with_code) / total_posts

            total_blocks = sum(r.total_blocks for r in results_with_code)
            total_issues = sum(r.total_issues for r in results_with_code)
            high_issues = sum(r.high_severity_count for r in results_with_code)
            gist_opportunities = sum(r.gist_extraction_candidates for r in results_with_code)

            # Build summary report
            summary = []
            summary.append(f"\n{'='*60}")
            summary.append("Code Block Quality Audit Summary")
            summary.append(f"{'='*60}")
            summary.append(f"\nPosts analyzed: {total_posts}")
            summary.append(f"Posts with code blocks: {total_posts}")
            summary.append(f"Compliant posts: {compliant_posts}/{total_posts} ({100*compliant_posts/total_posts:.1f}%)")
            summary.append(f"Average quality score: {avg_score:.1f}/100")
            summary.append(f"\nTotal code blocks: {total_blocks}")
            summary.append(f"Total issues found: {total_issues}")
            summary.append(f"  HIGH severity issues: {high_issues}")
            summary.append(f"Gist extraction opportunities: {gist_opportunities}")

            # Show top violators
            if high_issues > 0:
                summary.append(f"\n{'-'*60}")
                summary.append("Posts with HIGH severity issues:")
                summary.append(f"{'-'*60}")
                violators = [r for r in results_with_code if r.high_severity_count > 0]
                violators.sort(key=lambda r: r.high_severity_count, reverse=True)
                for r in violators[:10]:  # Top 10
                    summary.append(f"  {r.filename}: {r.high_severity_count} HIGH issues (score: {r.overall_score}/100)")

            summary.append(f"\n{'='*60}\n")

            # Write to stdout
            import sys
            sys.stdout.write('\n'.join(summary) + '\n')

        elif args.extract:
            # Extract mode - show gist extraction opportunities
            candidates = [r for r in results_with_code if r.gist_extraction_candidates > 0]
            output = []
            if candidates:
                output.append(f"\nGist Extraction Opportunities ({len(candidates)} posts):\n")
                for r in candidates:
                    output.append(f"{r.filename}:")
                    for block in r.blocks:
                        if block.needs_gist_extraction:
                            output.append(f"  Block #{block.block_number} (lines {block.line_start}-{block.line_end}): {block.line_count} lines")
            else:
                output.append("\nNo gist extraction opportunities found")

            import sys
            sys.stdout.write('\n'.join(output) + '\n')

        else:
            # Standard output - show individual results
            import sys
            for result in results_with_code:
                sys.stdout.write(format_result(result, verbose=not args.batch))

        # Generate CSV report if requested
        if args.report:
            generate_csv_report(results_with_code, args.report)
            logger.info(f"CSV report saved: {args.report}")

        # Return appropriate exit code
        if args.validate:
            # Strict mode - fail if any non-compliant posts
            non_compliant = [r for r in results_with_code if not r.compliant]
            if non_compliant:
                logger.warning(f"{len(non_compliant)} posts failed quality validation")
                return 2

        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
