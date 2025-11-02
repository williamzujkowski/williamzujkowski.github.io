#!/usr/bin/env -S uv run python3
"""
SCRIPT: full-post-validation.py
PURPOSE: Comprehensive blog post validation combining humanization, citations, and content quality checks
CATEGORY: content_validation
LLM_READY: True
VERSION: 1.1.0
UPDATED: 2025-11-02

DESCRIPTION:
    Comprehensive pre-publish validation tool that combines:
    - Humanization checks (AI-tells, tone, sentiment)
    - Citation coverage and link validation
    - Content quality (bullets, weak language, readability)
    - Smart Brevity principles
    - Accessibility requirements

    Provides a single validation command for blog posts before publishing.

LLM_USAGE:
    python scripts/blog-content/full-post-validation.py [options]

ARGUMENTS:
    --post (str): Path to blog post file (required)
    --min-human-score (int): Minimum humanization score (default: 70)
    --min-citation-coverage (float): Minimum citation percentage (default: 0.9)
    --strict (bool): Strict mode - fail on any violation (default: False)
    --output (str): Output format [text|json|markdown] (default: text)
    --report-file (str): Save report to file (optional)

EXAMPLES:
    # Validate single post
    python scripts/blog-content/full-post-validation.py --post src/posts/2025-01-15-example.md

    # Strict validation with report
    python scripts/blog-content/full-post-validation.py --post src/posts/example.md --strict --report-file validation-report.md

    # JSON output for CI/CD
    python scripts/blog-content/full-post-validation.py --post src/posts/example.md --output json

OUTPUT:
    - Overall validation status (PASS/FAIL)
    - Comprehensive scorecard across all dimensions
    - Specific violations and recommendations
    - Exit code: 0 (pass), 1 (fail), 2 (error)

DEPENDENCIES:
    - Python 3.8+
    - humanization-validator.py
    - PyYAML for config
    - frontmatter for post parsing

RELATED_SCRIPTS:
    - scripts/blog-content/humanization-validator.py: Human tone validation
    - scripts/blog-research/research-validator.py: Citation validation
    - scripts/link-validation/link-validator.py: Link checking
    - scripts/blog-content/analyze-blog-content.py: Content metrics

MANIFEST_REGISTRY: scripts/blog-content/full-post-validation.py
"""

import os
import re
import sys
import json
import yaml
import argparse
import frontmatter
import logging
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# ANSI color codes for terminal output (kept for backward compatibility with print_results)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Import humanization validator
sys.path.insert(0, str(Path(__file__).parent))
try:
    # Try importing from same directory
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "humanization_validator",
        Path(__file__).parent / "humanization-validator.py"
    )
    humanization_validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(humanization_validator)
    HumanizationValidator = humanization_validator.HumanizationValidator
except Exception as e:
    print(f"Warning: Could not import humanization-validator.py: {e}", file=sys.stderr)
    print("Humanization validation will be skipped.", file=sys.stderr)
    HumanizationValidator = None

class FullPostValidator:
    def __init__(self):
        self.results = {
            'overall_status': 'PASS',
            'overall_score': 0,
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }

    def validate_post(self, post_path: str, min_human_score: int = 70,
                     min_citation_coverage: float = 0.9) -> Dict:
        """Run comprehensive validation."""
        post = frontmatter.load(post_path)
        content = post.content
        metadata = post.metadata

        # 1. Humanization validation
        humanization_results = self._validate_humanization(post_path, min_human_score)

        # 2. Citation coverage
        citation_results = self._validate_citations(content, min_citation_coverage)

        # 3. Content quality
        quality_results = self._validate_content_quality(content)

        # 4. Metadata completeness
        metadata_results = self._validate_metadata(metadata)

        # 5. Accessibility
        accessibility_results = self._validate_accessibility(content, metadata)

        # Aggregate results
        all_checks = [
            humanization_results,
            citation_results,
            quality_results,
            metadata_results,
            accessibility_results
        ]

        # Calculate overall score (weighted average)
        weights = [0.30, 0.25, 0.20, 0.15, 0.10]  # Humanization weighted highest
        overall_score = sum(check['score'] * weight for check, weight in zip(all_checks, weights))

        # Determine overall status
        if overall_score >= 80:
            overall_status = 'PASS'
        elif overall_score >= 60:
            overall_status = 'NEEDS IMPROVEMENT'
        else:
            overall_status = 'FAIL'

        self.results['overall_score'] = round(overall_score, 1)
        self.results['overall_status'] = overall_status
        self.results['post_path'] = post_path
        self.results['checks'] = {
            'humanization': humanization_results,
            'citations': citation_results,
            'quality': quality_results,
            'metadata': metadata_results,
            'accessibility': accessibility_results
        }

        return self.results

    def _validate_humanization(self, post_path: str, min_score: int) -> Dict:
        """Validate human tone using humanization-validator."""
        if HumanizationValidator is None:
            return {
                'name': 'Humanization',
                'score': 0,
                'status': 'SKIPPED',
                'violations': 0,
                'warnings': 0,
                'details': {'error': 'HumanizationValidator not available'}
            }

        validator = HumanizationValidator()
        results = validator.validate_post(post_path)

        return {
            'name': 'Humanization',
            'score': results['score'],
            'status': 'PASS' if results['score'] >= min_score else 'FAIL',
            'violations': len(results['violations']),
            'warnings': len(results['warnings']),
            'details': results
        }

    def _validate_citations(self, content: str, min_coverage: float) -> Dict:
        """Validate citation coverage."""
        # Count claims that need citations
        claim_patterns = [
            r'\b\d+(?:\.\d+)?%',  # Percentages
            r'\b\d+(?:\.\d+)?x\s+(?:faster|slower|better|improvement)',  # Multipliers
            r'(?:studies show|research (?:shows|indicates))',  # Research claims
            r'according to',  # Attribution
        ]

        total_claims = 0
        for pattern in claim_patterns:
            total_claims += len(re.findall(pattern, content, re.IGNORECASE))

        # Count citations
        citation_patterns = [
            r'\[([^\]]+)\]\(https?://[^\)]+\)',  # Markdown links
            r'\[\d+\]',  # Numbered references
        ]

        total_citations = 0
        for pattern in citation_patterns:
            total_citations += len(re.findall(pattern, content))

        # Calculate coverage
        if total_claims == 0:
            coverage = 1.0  # No claims = perfect coverage
            score = 100
        else:
            coverage = min(total_citations / total_claims, 1.0)
            score = coverage * 100

        violations = []
        if coverage < min_coverage:
            violations.append(f'Citation coverage {coverage:.1%} below minimum {min_coverage:.1%}')

        return {
            'name': 'Citations',
            'score': round(score, 1),
            'status': 'PASS' if coverage >= min_coverage else 'FAIL',
            'coverage': round(coverage, 2),
            'claims': total_claims,
            'citations': total_citations,
            'violations': violations
        }

    def _validate_content_quality(self, content: str) -> Dict:
        """Validate content quality using Smart Brevity principles."""
        violations = []
        score = 100

        # Check for bullet points (should have at least 2 bulleted lists)
        bullet_lists = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
        if bullet_lists < 2:
            violations.append(f'Only {bullet_lists} bullet points found. Use bullets to break up content.')
            score -= 10

        # Check for weak language
        weak_phrases = [
            'very', 'really', 'quite', 'somewhat', 'rather',
            'a bit', 'kind of', 'sort of'
        ]
        weak_count = sum(len(re.findall(r'\b' + phrase + r'\b', content, re.IGNORECASE))
                        for phrase in weak_phrases)
        if weak_count > 5:
            violations.append(f'Found {weak_count} instances of weak language. Be more direct.')
            score -= 5

        # Check for passive voice indicators
        passive_indicators = ['was', 'were', 'been', 'being']
        passive_count = sum(len(re.findall(r'\b' + word + r'\s+\w+ed\b', content, re.IGNORECASE))
                           for word in passive_indicators)
        if passive_count > 10:
            violations.append(f'{passive_count} potential passive voice constructions. Use active voice.')
            score -= 5

        # Check for long paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        long_paragraphs = sum(1 for p in paragraphs if len(p.split()) > 150)
        if long_paragraphs > 2:
            violations.append(f'{long_paragraphs} paragraphs exceed 150 words. Break them up.')
            score -= 10

        # Check for subheadings (should have at least 3)
        subheadings = len(re.findall(r'^#{2,}\s', content, re.MULTILINE))
        if subheadings < 3:
            violations.append(f'Only {subheadings} subheadings. Add more structure.')
            score -= 10

        return {
            'name': 'Content Quality',
            'score': max(0, score),
            'status': 'PASS' if score >= 70 else 'FAIL',
            'violations': violations,
            'metrics': {
                'bullet_lists': bullet_lists,
                'weak_language': weak_count,
                'passive_voice': passive_count,
                'long_paragraphs': long_paragraphs,
                'subheadings': subheadings
            }
        }

    def _validate_metadata(self, metadata: Dict) -> Dict:
        """Validate frontmatter metadata completeness."""
        required_fields = ['title', 'date', 'description', 'tags', 'author']
        violations = []
        score = 100

        for field in required_fields:
            if field not in metadata:
                violations.append(f'Missing required field: {field}')
                score -= 20

        # Check description length (150-160 chars for SEO)
        if 'description' in metadata:
            desc_len = len(metadata['description'])
            if desc_len < 150 or desc_len > 160:
                violations.append(f'Description length {desc_len} chars. Should be 150-160.')
                score -= 10

        # Check tags (should have 4-8)
        if 'tags' in metadata:
            tag_count = len(metadata['tags'])
            if tag_count < 4 or tag_count > 8:
                violations.append(f'Tag count {tag_count}. Should have 4-8 tags.')
                score -= 10

        # Check for image metadata
        if 'images' not in metadata:
            violations.append('Missing image metadata')
            score -= 15

        return {
            'name': 'Metadata',
            'score': max(0, score),
            'status': 'PASS' if score >= 70 else 'FAIL',
            'violations': violations
        }

    def _validate_accessibility(self, content: str, metadata: Dict) -> Dict:
        """Validate accessibility requirements."""
        violations = []
        score = 100

        # Check for alt text on images
        images = re.findall(r'!\[([^\]]*)\]\([^\)]+\)', content)
        images_without_alt = sum(1 for alt in images if not alt.strip())
        if images_without_alt > 0:
            violations.append(f'{images_without_alt} images missing alt text')
            score -= 20

        # Check heading hierarchy
        headings = re.findall(r'^(#{1,6})\s', content, re.MULTILINE)
        if headings:
            # Should start with H2 (H1 is title)
            if headings[0] != '##':
                violations.append('First heading should be H2 (##)')
                score -= 10

            # Check for skipped levels
            prev_level = 2
            for heading in headings:
                level = len(heading)
                if level > prev_level + 1:
                    violations.append(f'Heading hierarchy skips from H{prev_level} to H{level}')
                    score -= 10
                    break
                prev_level = level

        # Check for code blocks with language specification
        code_blocks = re.findall(r'```(\w*)\n', content)
        unspecified_blocks = sum(1 for lang in code_blocks if not lang)
        if unspecified_blocks > 0:
            violations.append(f'{unspecified_blocks} code blocks missing language specification')
            score -= 10

        return {
            'name': 'Accessibility',
            'score': max(0, score),
            'status': 'PASS' if score >= 70 else 'FAIL',
            'violations': violations,
            'metrics': {
                'images_without_alt': images_without_alt,
                'unspecified_code_blocks': unspecified_blocks
            }
        }

def print_results(results: Dict, output_format: str = 'text'):
    """Print comprehensive validation results."""
    if output_format == 'json':
        print(json.dumps(results, indent=2))
        return

    if output_format == 'markdown':
        print_markdown_results(results)
        return

    # Text format with colors
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}COMPREHENSIVE BLOG POST VALIDATION{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

    # Overall status
    score = results['overall_score']
    status = results['overall_status']
    if status == 'PASS':
        color = Colors.GREEN
    elif status == 'NEEDS IMPROVEMENT':
        color = Colors.YELLOW
    else:
        color = Colors.RED

    print(f"Post: {Colors.CYAN}{results['post_path']}{Colors.RESET}")
    print(f"Overall Score: {color}{score}/100 - {status}{Colors.RESET}")
    print(f"Validated: {results['timestamp']}\n")

    # Individual checks
    print(f"{Colors.BOLD}SCORECARD{Colors.RESET}")
    print(f"{'-'*70}")

    for check_name, check_data in results['checks'].items():
        status_color = Colors.GREEN if check_data['status'] == 'PASS' else Colors.RED
        print(f"{check_data['name']:20} {status_color}{check_data['score']:>5.1f}/100{Colors.RESET} {status_color}[{check_data['status']}]{Colors.RESET}")

    print(f"{'-'*70}\n")

    # Detailed violations
    for check_name, check_data in results['checks'].items():
        if check_data.get('violations') or check_data.get('warnings', 0) > 0:
            print(f"{Colors.BOLD}{check_data['name'].upper()}{Colors.RESET}")

            # Humanization details
            if check_name == 'humanization' and check_data.get('details'):
                details = check_data['details']
                for v in details.get('violations', []):
                    print(f"  {Colors.RED}✗{Colors.RESET} {v.get('message', v.get('type'))}")
                for w in details.get('warnings', []):
                    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {w.get('message', w.get('type'))}")

            # Other violations
            elif isinstance(check_data.get('violations'), list):
                for v in check_data['violations']:
                    print(f"  {Colors.RED}✗{Colors.RESET} {v}")

            print()

    # Summary
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def print_markdown_results(results: Dict):
    """Print results in markdown format for reports."""
    print(f"# Blog Post Validation Report\n")
    print(f"**Post:** {results['post_path']}")
    print(f"**Validated:** {results['timestamp']}")
    print(f"**Overall Score:** {results['overall_score']}/100 - **{results['overall_status']}**\n")

    print("## Scorecard\n")
    print("| Check | Score | Status |")
    print("|-------|-------|--------|")
    for check_name, check_data in results['checks'].items():
        status_emoji = "✅" if check_data['status'] == 'PASS' else "❌"
        print(f"| {check_data['name']} | {check_data['score']}/100 | {status_emoji} {check_data['status']} |")

    print("\n## Violations\n")
    for check_name, check_data in results['checks'].items():
        if check_data.get('violations') or check_data.get('warnings', 0) > 0:
            print(f"### {check_data['name']}\n")

            if check_name == 'humanization' and check_data.get('details'):
                details = check_data['details']
                if details.get('violations'):
                    for v in details['violations']:
                        print(f"- ❌ {v.get('message', v.get('type'))}")
                if details.get('warnings'):
                    for w in details['warnings']:
                        print(f"- ⚠️ {w.get('message', w.get('type'))}")
            elif isinstance(check_data.get('violations'), list):
                for v in check_data['violations']:
                    print(f"- ❌ {v}")
            print()

def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive blog post validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/blog-content/full-post-validation.py --post src/posts/example.md
  python scripts/blog-content/full-post-validation.py --post src/posts/example.md --strict --report-file report.md
  python scripts/blog-content/full-post-validation.py --post src/posts/example.md --output json
        """
    )

    parser.add_argument('--post', required=True, help='Path to blog post file')
    parser.add_argument('--min-human-score', type=int, default=70, help='Minimum humanization score')
    parser.add_argument('--min-citation-coverage', type=float, default=0.9, help='Minimum citation coverage (0.0-1.0)')
    parser.add_argument('--strict', action='store_true', help='Strict mode - fail on any violation')
    parser.add_argument('--output', choices=['text', 'json', 'markdown'], default='text', help='Output format')
    parser.add_argument('--report-file', help='Save report to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    # Validate post exists
    if not os.path.exists(args.post):
        logger.error(f"Post file not found: {args.post}")
        return 2

    # Run validation
    validator = FullPostValidator()
    results = validator.validate_post(
        args.post,
        min_human_score=args.min_human_score,
        min_citation_coverage=args.min_citation_coverage
    )

    # Print results
    if args.report_file:
        import io
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        print_results(results, args.output)
        report_content = sys.stdout.getvalue()
        sys.stdout = original_stdout

        with open(args.report_file, 'w') as f:
            f.write(report_content)
        logger.info(f"Report saved to: {args.report_file}")
    else:
        print_results(results, args.output)

    # Determine exit code
    if args.strict and results['overall_status'] == 'FAIL':
        return 1
    elif results['overall_score'] < 60:
        return 1
    else:
        return 0

if __name__ == '__main__':
    sys.exit(main())
