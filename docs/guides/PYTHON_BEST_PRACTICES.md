# Python Script Best Practices Guide

**Version:** 1.0.0
**Updated:** 2025-11-02
**Audience:** AI agents, human developers, script authors

---

## Overview

This guide defines best practices for Python scripts in this repository based on the Python Audit Report findings and successful patterns from existing high-quality scripts.

**Reference Implementations:**
- ✅ `scripts/blog-content/humanization-validator.py` - Excellent logging, type hints, error handling
- ✅ `scripts/lib/logging_config.py` - Well-documented library module
- ✅ `scripts/lib/manifest_loader.py` - Comprehensive docstrings, thread-safe

---

## 1. Shebang and Imports

### UV Shebang (Required)

**Always use UV shebang:**
```python
#!/usr/bin/env -S uv run python3
```

**Why:** UV is 10-100x faster than pip and provides consistent environment management.

### Import Organization

```python
# Standard library imports (alphabetical)
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Third-party imports
import yaml
import frontmatter

# Local imports (last)
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger
from manifest_loader import ManifestLoader
```

**Order:**
1. Standard library
2. Third-party packages
3. Local modules

**Note:** Always use `sys.path.insert(0, ...)` for lib imports to ensure library modules are found.

---

## 2. Script Header Documentation

### Required Structure

```python
#!/usr/bin/env -S uv run python3
"""
SCRIPT: script-name.py
PURPOSE: Brief one-line description
CATEGORY: blog_content | blog_research | validation | utilities | link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-02

DESCRIPTION:
    Detailed multi-line description explaining:
    - What the script does
    - Key features or capabilities
    - Important behaviors or constraints

USAGE:
    # Example 1: Basic usage
    uv run python scripts/category/script-name.py

    # Example 2: With options
    uv run python scripts/category/script-name.py --option value

ARGUMENTS:
    --arg1 (type): Description (default: value)
    --arg2 (bool): Description (default: False)

OUTPUT:
    - What the script produces
    - Exit codes: 0 (success), 1 (error), 130 (cancelled)

DEPENDENCIES:
    - Python 3.8+
    - Package requirements

RELATED_SCRIPTS:
    - path/to/related-script.py: How it relates

MANIFEST_REGISTRY: scripts/category/script-name.py
"""
```

### Key Elements

1. **SCRIPT:** Filename (helps LLMs find the file)
2. **PURPOSE:** One-line summary
3. **CATEGORY:** One of the standard categories
4. **LLM_READY:** True if LLMs can safely execute
5. **VERSION:** Semantic versioning
6. **UPDATED:** Last modification date (YYYY-MM-DD)
7. **MANIFEST_REGISTRY:** Full path for file tracking

---

## 3. Logging (Required)

### Setup Logger

```python
from logging_config import setup_logger

# At module level (after imports)
logger = setup_logger(__name__)
```

### Logger Usage

```python
# Information messages (user-facing)
logger.info("Processing 42 files...")
logger.info(f"✅ Successfully processed {count} items")

# Debug messages (developer-facing)
logger.debug(f"Processing file: {filepath}")
logger.debug(f"Intermediate result: {data}")

# Warnings (potential issues)
logger.warning(f"Skipping {filepath}: unsupported format")
logger.warning("No configuration file found, using defaults")

# Errors (recoverable failures)
logger.error(f"Failed to process {filepath}: {error}")
logger.error(f"Validation failed: {reason}")

# Critical errors (with stack trace)
logger.error(f"Fatal error: {e}", exc_info=True)
```

### Never Use Print

**❌ Wrong:**
```python
print("Processing files...")
print(f"Error: {e}")
```

**✅ Correct:**
```python
logger.info("Processing files...")
logger.error(f"Error: {e}")
```

**Why:** Logger provides:
- Colored output (automatic)
- File logging support
- Quiet mode support
- Structured output
- Consistent formatting

---

## 4. Type Hints (Strongly Recommended)

### Function Signatures

```python
from typing import Dict, List, Optional, Tuple
from pathlib import Path

def process_file(
    filepath: Path,
    options: Dict[str, Any],
    dry_run: bool = False
) -> Tuple[bool, List[str]]:
    """
    Process a single file.

    Args:
        filepath: Path to file to process
        options: Processing options dictionary
        dry_run: If True, don't modify files

    Returns:
        Tuple of (success, list_of_warnings)

    Raises:
        IOError: If file cannot be read
        ValueError: If file content is invalid
    """
    # Implementation...
    return True, []
```

### Common Type Patterns

```python
from typing import Dict, List, Optional, Tuple, Any, Union
from pathlib import Path

# Basic types
def get_count() -> int: ...
def get_name() -> str: ...
def is_valid() -> bool: ...

# Collections
def get_items() -> List[str]: ...
def get_config() -> Dict[str, Any]: ...
def get_mapping() -> Dict[str, List[int]]: ...

# Optional (may be None)
def find_item(name: str) -> Optional[str]: ...
def get_config_value(key: str) -> Optional[int]: ...

# Tuples (fixed size, known types)
def parse_result() -> Tuple[bool, str]: ...
def get_stats() -> Tuple[int, int, float]: ...

# Union (one of multiple types)
def load_data(source: Union[str, Path]) -> Dict: ...

# Path objects
def read_file(filepath: Path) -> str: ...
def find_files(directory: Path) -> List[Path]: ...
```

---

## 5. Error Handling (Required)

### Specific Exceptions

```python
def process_file(filepath: Path) -> Dict[str, Any]:
    """Process file with proper error handling."""
    try:
        # Read file
        content = filepath.read_text(encoding='utf-8')

        # Validate content
        if not content.strip():
            raise ValueError("File is empty")

        # Process
        result = parse_content(content)
        return result

    except UnicodeDecodeError as e:
        logger.error(f"Encoding error in {filepath}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except IOError as e:
        logger.error(f"I/O error reading {filepath}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing {filepath}: {e}", exc_info=True)
        raise
```

### Exception Hierarchy

```python
# Specific to general
try:
    operation()
except FileNotFoundError as e:       # Specific
    handle_missing_file(e)
except PermissionError as e:         # Specific
    handle_permission_error(e)
except IOError as e:                 # General I/O
    handle_io_error(e)
except Exception as e:               # Catch-all
    logger.error(f"Unexpected: {e}", exc_info=True)
    raise
```

### Main Function Pattern

```python
def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0=success, 1=error, 130=cancelled)
    """
    try:
        # Setup
        config = load_config()

        # Process
        result = process(config)

        # Success
        logger.info("✅ Processing completed successfully")
        return 0

    except KeyboardInterrupt:
        logger.warning("\nOperation cancelled by user")
        return 130
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

---

## 6. Class Design

### Dataclasses for Data

```python
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class ValidationResult:
    """Result of validation check."""
    filepath: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
```

### Regular Classes for Behavior

```python
class FileProcessor:
    """Process files with specific logic."""

    def __init__(self, options: Dict[str, Any], dry_run: bool = False):
        """
        Initialize processor.

        Args:
            options: Processing options
            dry_run: If True, don't modify files
        """
        self.options = options
        self.dry_run = dry_run
        self.stats = {'processed': 0, 'errors': 0}
        logger.debug(f"Initialized processor (dry_run={dry_run})")

    def process_file(self, filepath: Path) -> bool:
        """Process single file."""
        try:
            logger.debug(f"Processing {filepath}")
            # Implementation...
            self.stats['processed'] += 1
            return True
        except Exception as e:
            logger.error(f"Error processing {filepath}: {e}")
            self.stats['errors'] += 1
            return False

    def run(self) -> int:
        """Run processing."""
        logger.info("Starting file processing")
        # Implementation...
        return 0 if self.stats['errors'] == 0 else 1
```

---

## 7. Argument Parsing

### Standard Pattern

```python
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Brief description of script purpose',
        epilog='Example: %(prog)s --option value'
    )

    # Required arguments
    parser.add_argument(
        'input_file',
        type=Path,
        help='Input file to process'
    )

    # Optional arguments
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file (default: stdout)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'yaml'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without modifying files'
    )

    args = parser.parse_args()

    # Setup logger with verbosity
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level)

    # Use arguments
    process(args.input_file, args.output, args.format)
```

### Common Argument Patterns

```python
# File/directory arguments
parser.add_argument('input', type=Path, help='Input file')
parser.add_argument('--dir', type=Path, default=Path('src/posts'))

# Boolean flags
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--strict', action='store_true')

# Choices
parser.add_argument('--format', choices=['text', 'json'])
parser.add_argument('--level', choices=['low', 'medium', 'high'])

# Integers with defaults
parser.add_argument('--count', type=int, default=10)
parser.add_argument('--min-score', type=int, default=70)

# Lists
parser.add_argument('--tags', nargs='+', help='List of tags')
```

---

## 8. File Operations

### Path Objects (Required)

```python
from pathlib import Path

# ✅ Correct
posts_dir = Path('src/posts')
for filepath in posts_dir.glob('*.md'):
    content = filepath.read_text(encoding='utf-8')
    filepath.write_text(content, encoding='utf-8')

# ❌ Wrong
import os
posts_dir = 'src/posts'
for filename in os.listdir(posts_dir):
    with open(os.path.join(posts_dir, filename)) as f:
        content = f.read()
```

### Safe File Operations

```python
def save_file(filepath: Path, content: str, backup: bool = True) -> None:
    """
    Save content to file with optional backup.

    Args:
        filepath: Destination file path
        content: Content to write
        backup: If True, create .bak file

    Raises:
        IOError: If file cannot be written
    """
    try:
        # Create backup if requested
        if backup and filepath.exists():
            backup_path = filepath.with_suffix('.bak')
            shutil.copy2(filepath, backup_path)
            logger.debug(f"Created backup: {backup_path}")

        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        filepath.write_text(content, encoding='utf-8')
        logger.debug(f"Saved {filepath}")

    except IOError as e:
        logger.error(f"Failed to save {filepath}: {e}")
        raise
```

---

## 9. Configuration Files

### YAML Configuration

```python
import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Load YAML configuration file.

    Args:
        config_path: Path to YAML config file

    Returns:
        Configuration dictionary

    Raises:
        FileNotFoundError: If config file not found
        yaml.YAMLError: If config file is invalid
    """
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Config not found: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        logger.debug(f"Loaded configuration from {config_path}")
        return config

    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {config_path}: {e}")
        raise
```

### Default Configuration

```python
DEFAULT_CONFIG = {
    'min_score': 70,
    'max_attempts': 3,
    'timeout': 30,
    'strict_mode': False
}

def load_config_with_defaults(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load config with defaults fallback."""
    config = DEFAULT_CONFIG.copy()

    if config_path and config_path.exists():
        user_config = load_config(config_path)
        config.update(user_config)
        logger.info(f"Loaded custom configuration from {config_path}")
    else:
        logger.info("Using default configuration")

    return config
```

---

## 10. Testing Patterns

### Unit Test Structure

```python
#!/usr/bin/env -S uv run python3
"""Unit tests for script-name.py"""

import pytest
from pathlib import Path
from script_name import ScriptClass, helper_function

class TestHelperFunction:
    """Tests for helper_function."""

    def test_basic_case(self):
        """Test basic functionality."""
        result = helper_function("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test edge case."""
        result = helper_function("")
        assert result == ""

    def test_invalid_input(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            helper_function(None)


class TestScriptClass:
    """Tests for ScriptClass."""

    @pytest.fixture
    def instance(self):
        """Create test instance."""
        return ScriptClass(option=True)

    def test_initialization(self, instance):
        """Test initialization."""
        assert instance.option is True

    def test_method(self, instance):
        """Test method."""
        result = instance.method("test")
        assert result is not None
```

### Fixtures

```python
@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary directory."""
    test_dir = tmp_path / "test_files"
    test_dir.mkdir()
    return test_dir

@pytest.fixture
def sample_markdown(temp_dir):
    """Create sample markdown file."""
    content = """---
title: Test Post
---

# Test Content
"""
    filepath = temp_dir / "test.md"
    filepath.write_text(content, encoding='utf-8')
    return filepath
```

---

## 11. Common Anti-Patterns to Avoid

### ❌ Don't: Use print() statements

```python
# Wrong
print("Processing files...")
print(f"Error: {e}")
```

### ✅ Do: Use logger

```python
# Correct
logger.info("Processing files...")
logger.error(f"Error: {e}")
```

### ❌ Don't: Generic exception handling

```python
# Wrong
try:
    process_file()
except Exception:
    pass  # Silent failure
```

### ✅ Do: Specific exceptions with logging

```python
# Correct
try:
    process_file()
except IOError as e:
    logger.error(f"I/O error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

### ❌ Don't: Hard-coded paths

```python
# Wrong
POSTS_DIR = "/home/user/git/repo/src/posts"
```

### ✅ Do: Relative paths from script location

```python
# Correct
POSTS_DIR = Path(__file__).parent.parent.parent / 'src' / 'posts'
```

### ❌ Don't: Mixed concerns in one file

```python
# Wrong: 1000-line file doing validation, reporting, and processing
```

### ✅ Do: Separate modules by responsibility

```python
# Correct
# validator.py - validation logic
# reporter.py - reporting/formatting
# processor.py - file processing
# main.py - orchestration
```

---

## 12. Performance Considerations

### Batch Processing

```python
from multiprocessing import Pool, cpu_count

def process_files_parallel(filepaths: List[Path], workers: int = 4) -> List[Dict]:
    """Process files in parallel."""
    with Pool(workers) as pool:
        results = pool.map(process_single_file, filepaths)
    return results
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(key: str) -> str:
    """Cached expensive operation."""
    # Expensive computation
    return result
```

### Generator for Large Files

```python
def read_large_file(filepath: Path) -> Generator[str, None, None]:
    """Read large file line by line."""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()
```

---

## 13. Checklist for New Scripts

Before committing a new Python script, verify:

- [ ] UV shebang: `#!/usr/bin/env -S uv run python3`
- [ ] Complete script header with all required fields
- [ ] Import logging_config and setup logger
- [ ] All print() statements replaced with logger calls
- [ ] Type hints on all function signatures
- [ ] Specific exception handling (not generic `except Exception`)
- [ ] Docstrings on all public functions and classes
- [ ] Path objects used instead of string paths
- [ ] Main function returns int exit code
- [ ] `if __name__ == '__main__': sys.exit(main())`
- [ ] MANIFEST_REGISTRY entry in header
- [ ] Error cases logged with appropriate level
- [ ] Arguments parsed with argparse (if CLI script)

---

## 14. Migration Checklist for Existing Scripts

When refactoring an existing script:

- [ ] Update shebang to UV if needed
- [ ] Add/update script header documentation
- [ ] Import and setup logging_config
- [ ] Replace all print() with logger calls
- [ ] Add type hints to function signatures
- [ ] Improve error handling (specific exceptions)
- [ ] Add/improve docstrings
- [ ] Convert os.path to pathlib.Path
- [ ] Extract configuration to variables/YAML
- [ ] Add unit tests if missing
- [ ] Update MANIFEST.json if needed

---

## Quick Reference

### Template Script

```python
#!/usr/bin/env -S uv run python3
"""
SCRIPT: template.py
PURPOSE: One-line purpose
CATEGORY: category
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-02

DESCRIPTION:
    Detailed description

MANIFEST_REGISTRY: scripts/category/template.py
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)


def main() -> int:
    """Main entry point."""
    try:
        logger.info("Processing...")
        # Implementation
        return 0
    except KeyboardInterrupt:
        logger.warning("\nCancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

---

**Last Updated:** 2025-11-02
**Maintainer:** Python-Script-Auditor Agent
**See Also:** Python Audit Report, LLM Onboarding Guide
