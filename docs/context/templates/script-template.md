---
title: Python Script Template
category: templates
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 500
load_when:
  - Creating new Python scripts
  - Standardizing script structure
dependencies: []
tags: [template, script, python, automation]
---

# Python Script Template

## Module Metadata
- **Category:** templates
- **Priority:** LOW
- **Load frequency:** When creating new Python automation scripts
- **Dependencies:** None

## Purpose

This module provides a standardized template for Python scripts in the `/scripts` directory, ensuring consistent structure, documentation, error handling, and logging patterns.

## When to Load This Module

- Creating new Python scripts
- Standardizing existing scripts
- Ensuring consistent automation patterns

---

## Complete Script Template

```python
#!/usr/bin/env python3
"""
[Script Title - Brief Description]

Purpose: [What this script does and why it exists]

Usage:
    python [script-name].py [required-args] [optional-args]

Examples:
    # Example 1: [Common use case]
    python [script-name].py --input file.txt --output result.txt

    # Example 2: [Another use case]
    python [script-name].py --batch --directory src/posts/

Arguments:
    --input FILE        Input file path
    --output FILE       Output file path
    --option VALUE      [Description of option]
    --verbose           Enable verbose logging
    --dry-run           Preview changes without applying

Dependencies:
    - Required packages (install via: pip install -r requirements.txt)
    - [package1]: [purpose]
    - [package2]: [purpose]

Author: William Zujkowski
License: MIT
Created: YYYY-MM-DD
Last Modified: YYYY-MM-DD
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('script.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


class ScriptError(Exception):
    """Custom exception for script-specific errors"""
    pass


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments

    Examples:
        >>> args = parse_arguments()
        >>> print(args.input)
        'file.txt'
    """
    parser = argparse.ArgumentParser(
        description='[Script description]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --input file.txt
    %(prog)s --batch --directory src/posts/
        """
    )

    # Required arguments
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input file path'
    )

    # Optional arguments
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying'
    )

    return parser.parse_args()


def validate_inputs(args: argparse.Namespace) -> None:
    """
    Validate input arguments and files.

    Args:
        args: Parsed command-line arguments

    Raises:
        ScriptError: If validation fails
        FileNotFoundError: If input file doesn't exist
    """
    input_path = Path(args.input)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if not input_path.is_file():
        raise ScriptError(f"Input path is not a file: {input_path}")

    logger.info(f"Validated input: {input_path}")


def process_file(input_path: Path, output_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Process the input file and generate results.

    Args:
        input_path: Path to input file
        output_path: Optional path to output file

    Returns:
        dict: Processing results with statistics

    Raises:
        ScriptError: If processing fails
    """
    logger.info(f"Processing file: {input_path}")

    try:
        # Read input
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Process content
        result = transform_content(content)

        # Write output
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            logger.info(f"Wrote output to: {output_path}")

        return {
            'success': True,
            'input': str(input_path),
            'output': str(output_path) if output_path else 'stdout',
            'lines_processed': result['lines_processed'],
            'changes_made': result['changes_made']
        }

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise ScriptError(f"Processing failed: {e}") from e


def transform_content(content: str) -> Dict[str, Any]:
    """
    Transform the input content.

    Args:
        content: Input content as string

    Returns:
        dict: Transformed content and statistics
    """
    lines = content.splitlines()
    transformed_lines = []
    changes_made = 0

    for line in lines:
        # Apply transformations
        new_line = line.strip()

        if new_line != line:
            changes_made += 1

        transformed_lines.append(new_line)

    return {
        'content': '\n'.join(transformed_lines),
        'lines_processed': len(lines),
        'changes_made': changes_made
    }


def main() -> int:
    """
    Main entry point for the script.

    Returns:
        int: Exit code (0 = success, 1 = error)
    """
    try:
        # Parse arguments
        args = parse_arguments()

        # Set logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")

        # Validate inputs
        logger.info("Starting [script name]")
        validate_inputs(args)

        # Process file(s)
        input_path = Path(args.input)
        output_path = Path(args.output) if args.output else None

        if args.dry_run:
            logger.info("DRY RUN: No changes will be applied")

        result = process_file(input_path, output_path)

        # Report results
        logger.info(f"Processing completed successfully")
        logger.info(f"Lines processed: {result['lines_processed']}")
        logger.info(f"Changes made: {result['changes_made']}")

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1

    except ScriptError as e:
        logger.error(f"Script error: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("Script interrupted by user")
        return 130

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Key Components Explained

### 1. Docstring Header

**Required elements:**
- Script title and brief description
- Purpose statement
- Usage examples
- Argument documentation
- Dependencies list
- Author and license

### 2. Logging Configuration

**Standard setup:**
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('script.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)
```

**Use logging, not print():**
- `logger.debug()` - Detailed debugging information
- `logger.info()` - General informational messages
- `logger.warning()` - Warning messages
- `logger.error()` - Error messages
- `logger.exception()` - Error with traceback

### 3. Argument Parsing

**Use argparse with:**
- Clear help messages
- Type hints
- Default values
- Required vs optional distinction
- Example usage in epilog

### 4. Input Validation

**Always validate:**
- File existence
- File types
- Input constraints
- Dependencies availability

### 5. Error Handling

**Use try/except with:**
- Specific exceptions
- Custom exception classes
- Logging before raising
- Graceful degradation

### 6. Type Hints

**Use throughout:**
```python
def function_name(arg1: str, arg2: Optional[int] = None) -> Dict[str, Any]:
    """Docstring"""
    pass
```

---

## Script Organization Standards

### Directory Placement

```
scripts/
├── blog-content/        # Content management scripts
├── blog-images/         # Image automation scripts
├── blog-research/       # Citation and research scripts
├── link-validation/     # Link checking scripts
├── utilities/           # General utilities
└── lib/                 # Shared libraries
    └── common.py        # Common functions
```

### Naming Conventions

**Pattern:** `verb-noun-context.py`

**Examples:**
- `validate-citations.py` - Validation scripts
- `generate-hero-images.py` - Generation scripts
- `update-blog-images.py` - Update scripts
- `check-citation-hyperlinks.py` - Check scripts

---

## Common Patterns

### File Processing Pattern

```python
def process_files(pattern: str) -> List[Path]:
    """Process multiple files matching pattern"""
    files = Path('.').glob(pattern)
    results = []

    for file_path in files:
        try:
            result = process_single_file(file_path)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            continue

    return results
```

### Progress Reporting Pattern

```python
from tqdm import tqdm

def process_batch(items: List[Any]) -> None:
    """Process items with progress bar"""
    for item in tqdm(items, desc="Processing"):
        process_item(item)
```

### Dry-Run Pattern

```python
def apply_changes(changes: List[Change], dry_run: bool = False) -> int:
    """Apply changes with optional dry-run"""
    if dry_run:
        logger.info("DRY RUN: Would apply these changes:")
        for change in changes:
            logger.info(f"  - {change}")
        return 0

    for change in changes:
        change.apply()

    return len(changes)
```

---

## Testing Template

```python
# test_script.py

import unittest
from pathlib import Path
from script_name import process_file, transform_content


class TestScriptFunctions(unittest.TestCase):
    """Test cases for script functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path('tests/fixtures')
        self.test_file = self.test_dir / 'test.txt'

    def test_transform_content(self):
        """Test content transformation"""
        input_text = "  test line  "
        result = transform_content(input_text)

        self.assertEqual(result['content'], "test line")
        self.assertEqual(result['changes_made'], 1)

    def test_process_file_success(self):
        """Test successful file processing"""
        result = process_file(self.test_file)

        self.assertTrue(result['success'])
        self.assertGreater(result['lines_processed'], 0)


if __name__ == '__main__':
    unittest.main()
```

---

## Cross-References

**Related modules:**
- `technical/script-catalog` - Complete script inventory
- `core/file-management` - File organization rules
- `templates/documentation-template` - Documentation standards

**External documentation:**
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [argparse Documentation](https://docs.python.org/3/library/argparse.html)

---

## Changelog
- 2025-11-01: Initial script template creation with best practices
