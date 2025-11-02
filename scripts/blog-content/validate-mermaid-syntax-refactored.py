#!/usr/bin/env -S uv run python3
"""
SCRIPT: validate-mermaid-syntax.py
PURPOSE: Validate Mermaid diagram syntax in all blog posts
CATEGORY: blog_content
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-02

DESCRIPTION:
    Validates Mermaid diagram syntax across all blog posts to catch errors
    before they cause build failures or rendering issues.

    Validation checks:
    1. Proper fencing (```mermaid ... ```)
    2. Valid diagram types (graph, flowchart, sequenceDiagram, etc.)
    3. Balanced quotes in node labels
    4. Proper subgraph/end structure
    5. Common syntax errors (invalid arrows, unescaped characters)

    Used in CI/CD pipeline to ensure diagram quality.

USAGE:
    # Validate all posts
    uv run python scripts/blog-content/validate-mermaid-syntax.py

    # Validate specific directory
    uv run python scripts/blog-content/validate-mermaid-syntax.py --posts-dir src/drafts

    # JSON output for CI/CD
    uv run python scripts/blog-content/validate-mermaid-syntax.py --format json

ARGUMENTS:
    --posts-dir: Directory containing blog posts (default: src/posts)
    --format: Output format [text|json] (default: text)
    --strict: Exit with error on warnings (default: False)

OUTPUT:
    - Posts scanned count
    - Posts with Mermaid diagrams
    - Total blocks validated
    - Detailed error reports with line numbers
    - Exit code: 0 (pass), 1 (validation errors)

DEPENDENCIES:
    - Python 3.8+
    - logging_config for consistent logging
    - PyYAML for pattern configuration (future)

RELATED_SCRIPTS:
    - scripts/blog-content/fix-mermaid-subgraphs.py: Fix subgraph syntax

MANIFEST_REGISTRY: scripts/blog-content/validate-mermaid-syntax.py
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)


# Valid Mermaid diagram types (v10+)
VALID_DIAGRAM_TYPES = {
    'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
    'stateDiagram', 'erDiagram', 'gantt', 'pie', 'gitGraph',
    'journey', 'requirementDiagram', 'quadrantChart', 'timeline'
}


@dataclass
class MermaidBlock:
    """Represents a Mermaid code block in a markdown file."""
    content: str
    start_line: int
    end_line: int
    filepath: Path

    def get_first_line(self) -> str:
        """Get the first line of the block."""
        return self.content.split('\n')[0].strip() if self.content else ''

    def get_diagram_type(self) -> str:
        """Extract diagram type from first line."""
        first_line = self.get_first_line()
        return first_line.split()[0] if first_line.split() else ''


@dataclass
class ValidationError:
    """Represents a validation error in a Mermaid block."""
    type: str
    message: str
    line: int
    content: str = ''
    suggestion: str = ''

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class MermaidSyntaxValidator:
    """Validate Mermaid diagram syntax in blog posts."""

    # Common problematic patterns (pattern, description)
    PROBLEMATIC_PATTERNS = [
        (r'[^\\][{}\[\]<>()]', 'Unescaped special characters in node labels'),
        (r'--+(?!>|[-|])', 'Invalid arrow syntax (missing > or proper connection)'),
        (r'^\s*subgraph\s+[^"\w]', 'Subgraph name must be quoted or alphanumeric'),
        (r'^\s*end\s+\S', 'end keyword must be on its own line'),
    ]

    def __init__(self, posts_dir: Path, strict: bool = False):
        """
        Initialize the validator.

        Args:
            posts_dir: Directory containing blog post markdown files
            strict: If True, treat warnings as errors
        """
        self.posts_dir = posts_dir
        self.strict = strict
        self.stats = {
            'posts_scanned': 0,
            'posts_with_mermaid': 0,
            'blocks_validated': 0,
            'files_with_issues': 0,
            'total_errors': 0
        }

    def extract_mermaid_blocks(self, content: str, filepath: Path) -> List[MermaidBlock]:
        """
        Extract all Mermaid code blocks from markdown content.

        Args:
            content: Markdown file content
            filepath: Path to the markdown file

        Returns:
            List of MermaidBlock objects
        """
        blocks = []
        lines = content.split('\n')
        in_mermaid = False
        current_block = []
        start_line = 0

        for i, line in enumerate(lines, 1):
            if line.strip() == '```mermaid':
                in_mermaid = True
                start_line = i
                current_block = []
            elif line.strip() == '```' and in_mermaid:
                blocks.append(MermaidBlock(
                    content='\n'.join(current_block),
                    start_line=start_line,
                    end_line=i,
                    filepath=filepath
                ))
                in_mermaid = False
                current_block = []
            elif in_mermaid:
                current_block.append(line)

        if in_mermaid:
            logger.warning(f"Unclosed Mermaid block in {filepath.name} starting at line {start_line}")

        return blocks

    def validate_diagram_type(self, block: MermaidBlock) -> List[ValidationError]:
        """
        Validate the diagram type is recognized.

        Args:
            block: Mermaid block to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        diagram_type = block.get_diagram_type()

        if diagram_type not in VALID_DIAGRAM_TYPES:
            errors.append(ValidationError(
                type='INVALID_DIAGRAM_TYPE',
                message=f'Invalid or missing diagram type: "{diagram_type}"',
                line=block.start_line + 1,
                suggestion=f'Valid types: {", ".join(sorted(VALID_DIAGRAM_TYPES))}'
            ))

        return errors

    def validate_balanced_quotes(self, block: MermaidBlock) -> List[ValidationError]:
        """
        Validate quotes are balanced in each line.

        Args:
            block: Mermaid block to validate

        Returns:
            List of validation errors
        """
        errors = []

        for line_num, line in enumerate(block.content.split('\n'), 1):
            # Count unescaped quotes
            quote_count = line.count('"') - line.count('\\"')
            if quote_count % 2 != 0:
                errors.append(ValidationError(
                    type='UNBALANCED_QUOTES',
                    message='Unbalanced quotes in line',
                    line=block.start_line + line_num,
                    content=line.strip()
                ))

        return errors

    def validate_subgraph_structure(self, block: MermaidBlock) -> List[ValidationError]:
        """
        Validate subgraph/end structure is balanced.

        Args:
            block: Mermaid block to validate

        Returns:
            List of validation errors
        """
        errors = []
        subgraph_count = block.content.count('subgraph')
        end_count = len([
            line for line in block.content.split('\n')
            if line.strip() == 'end'
        ])

        if subgraph_count != end_count:
            errors.append(ValidationError(
                type='SUBGRAPH_MISMATCH',
                message=f'Subgraph/end mismatch: {subgraph_count} subgraphs but {end_count} ends',
                line=block.start_line,
                suggestion='Ensure each subgraph has a matching end statement'
            ))

        return errors

    def validate_common_patterns(self, block: MermaidBlock) -> List[ValidationError]:
        """
        Check for common syntax issues using pattern matching.

        Args:
            block: Mermaid block to validate

        Returns:
            List of validation errors
        """
        errors = []

        for line_num, line in enumerate(block.content.split('\n'), 1):
            for pattern, description in self.PROBLEMATIC_PATTERNS:
                if re.search(pattern, line):
                    errors.append(ValidationError(
                        type='SYNTAX_ERROR',
                        message=description,
                        line=block.start_line + line_num,
                        content=line.strip()
                    ))

        return errors

    def validate_block(self, block: MermaidBlock) -> List[ValidationError]:
        """
        Validate a single Mermaid block.

        Args:
            block: Mermaid block to validate

        Returns:
            List of all validation errors found
        """
        if not block.content.strip():
            return [ValidationError(
                type='EMPTY_BLOCK',
                message='Empty Mermaid block',
                line=block.start_line
            )]

        errors = []
        errors.extend(self.validate_diagram_type(block))
        errors.extend(self.validate_balanced_quotes(block))
        errors.extend(self.validate_subgraph_structure(block))
        errors.extend(self.validate_common_patterns(block))

        return errors

    def validate_file(self, filepath: Path) -> Dict[str, Any]:
        """
        Validate all Mermaid blocks in a file.

        Args:
            filepath: Path to markdown file

        Returns:
            Dictionary with filepath and list of errors
        """
        try:
            content = filepath.read_text(encoding='utf-8')
            blocks = self.extract_mermaid_blocks(content, filepath)

            if blocks:
                self.stats['blocks_validated'] += len(blocks)

            all_errors = []
            for block in blocks:
                errors = self.validate_block(block)
                all_errors.extend(errors)

            return {
                'filepath': str(filepath),
                'blocks': len(blocks),
                'errors': [error.to_dict() for error in all_errors]
            }

        except UnicodeDecodeError as e:
            logger.error(f"Encoding error in {filepath}: {e}")
            return {
                'filepath': str(filepath),
                'blocks': 0,
                'errors': [{
                    'type': 'FILE_ERROR',
                    'message': f'Encoding error: {e}',
                    'line': 0
                }]
            }
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}", exc_info=True)
            return {
                'filepath': str(filepath),
                'blocks': 0,
                'errors': [{
                    'type': 'FILE_ERROR',
                    'message': str(e),
                    'line': 0
                }]
            }

    def run(self) -> Dict[str, Any]:
        """
        Run validation on all posts.

        Returns:
            Dictionary with validation results
        """
        logger.info("🔍 Validating Mermaid diagram syntax...")

        if not self.posts_dir.exists():
            logger.error(f"Posts directory not found: {self.posts_dir}")
            return {'error': 'Posts directory not found'}

        # Find all markdown files
        post_files = list(self.posts_dir.glob('*.md'))
        self.stats['posts_scanned'] = len(post_files)

        # Validate each file
        issues = {}
        for post_file in sorted(post_files):
            result = self.validate_file(post_file)

            # Check if file has Mermaid blocks
            if result['blocks'] > 0:
                self.stats['posts_with_mermaid'] += 1

            # Check if file has errors
            if result['errors']:
                issues[str(post_file)] = result['errors']
                self.stats['files_with_issues'] += 1
                self.stats['total_errors'] += len(result['errors'])

        return {
            'stats': self.stats,
            'issues': issues
        }

    def print_text_report(self, results: Dict[str, Any]) -> None:
        """Print formatted text report."""
        stats = results['stats']
        issues = results['issues']

        logger.info("\n📊 Scan Summary:")
        logger.info(f"  - Posts scanned: {stats['posts_scanned']}")
        logger.info(f"  - Posts with Mermaid: {stats['posts_with_mermaid']}")
        logger.info(f"  - Total Mermaid blocks: {stats['blocks_validated']}")
        logger.info(f"  - Files with issues: {stats['files_with_issues']}")

        if not issues:
            logger.info("\n✅ All Mermaid diagrams validated successfully!")
            return

        logger.warning(f"\n⚠️  Found issues in {len(issues)} files:")

        for filepath, errors in sorted(issues.items()):
            rel_path = Path(filepath).relative_to(self.posts_dir.parent.parent)
            logger.warning(f"\n📄 {rel_path}")
            logger.info("=" * 80)

            for error in errors:
                logger.error(f"\n  Line {error['line']}: {error['type']}")
                logger.error(f"  ├─ {error['message']}")
                if error.get('content'):
                    logger.info(f"  ├─ Content: {error['content']}")
                if error.get('suggestion'):
                    logger.info(f"  └─ Suggestion: {error['suggestion']}")

        logger.error(f"\n\n❌ Validation failed with {stats['total_errors']} total errors")

    def print_json_report(self, results: Dict[str, Any]) -> None:
        """Print JSON report for CI/CD integration."""
        print(json.dumps(results, indent=2))


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate Mermaid diagram syntax in blog posts',
        epilog='Example: %(prog)s --format json'
    )
    parser.add_argument(
        '--posts-dir',
        type=Path,
        default=Path(__file__).parent.parent.parent / 'src' / 'posts',
        help='Posts directory (default: src/posts)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    try:
        validator = MermaidSyntaxValidator(
            posts_dir=args.posts_dir,
            strict=args.strict
        )
        results = validator.run()

        if 'error' in results:
            return 1

        if args.format == 'json':
            validator.print_json_report(results)
        else:
            validator.print_text_report(results)

        # Return exit code based on validation results
        return 1 if results['stats']['total_errors'] > 0 else 0

    except KeyboardInterrupt:
        logger.warning("\nValidation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
