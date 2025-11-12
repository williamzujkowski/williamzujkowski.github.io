#!/usr/bin/env -S uv run python3
"""
SCRIPT: script-name.py
PURPOSE: Brief one-line description of what this script does
CATEGORY: content_validation | automation | analysis | validation | reporting
LLM_READY: True | False
VERSION: 1.0.0
UPDATED: YYYY-MM-DD

DESCRIPTION:
    Detailed description of the script's purpose and functionality.
    This should explain:
    - What problem the script solves
    - Key features and capabilities
    - Important constraints or limitations
    - Any performance considerations

    Multi-paragraph descriptions are acceptable for complex scripts.

LLM_USAGE:
    python scripts/category/script-name.py [options]

ARGUMENTS:
    --input (str): Description of input argument
    --output (str): Description of output argument
    --format (str): Output format [text|json] (default: text)
    --verbose, -v (bool): Enable debug logging
    --quiet, -q (bool): Suppress non-essential output
    --log-file (Path): Write logs to specified file

EXAMPLES:
    # Basic usage
    python scripts/category/script-name.py --input data.json

    # With JSON output
    python scripts/category/script-name.py --input data.json --format json

    # Debug mode with log file
    python scripts/category/script-name.py --input data.json --verbose --log-file logs/debug.log

    # Quiet mode (errors only)
    python scripts/category/script-name.py --input data.json --quiet

OUTPUT:
    - Description of what the script outputs
    - Exit codes: 0 (success), 1 (error), 130 (interrupted)
    - File outputs if any

DEPENDENCIES:
    - Python 3.8+
    - PyYAML (if parsing YAML)
    - frontmatter (if parsing blog posts)
    - Additional dependencies as needed

RELATED_SCRIPTS:
    - scripts/category/related-script-1.py: Brief description
    - scripts/category/related-script-2.py: Brief description

MANIFEST_REGISTRY: scripts/category/script-name.py
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# Module metadata
__version__ = "1.0.0"
__author__ = "William Zujkowski"
__all__ = ["ScriptClass", "main"]

# Initialize logger (will be reconfigured in main() based on CLI args)
logger = setup_logger(__name__)


@dataclass
class DataClass:
    """Data class for structured data representation.

    Attributes:
        field1: Description of field1
        field2: Description of field2
        field3: Optional field with default

    Examples:
        >>> data = DataClass(field1="value1", field2=42)
        >>> print(data.field1)
        value1
    """
    field1: str
    field2: int
    field3: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the data class.
        """
        return asdict(self)


class ScriptClass:
    """Main class for script functionality.

    Provides core functionality for the script, following single-responsibility
    principle and clean code practices.

    Attributes:
        input_path: Path to input file or directory
        output_format: Output format (text or json)
        config: Configuration dictionary

    Examples:
        >>> processor = ScriptClass(Path("data.json"))
        >>> results = processor.process()
        >>> processor.print_results(results)
    """

    def __init__(self, input_path: Path, output_format: str = "text") -> None:
        """Initialize the script processor.

        Args:
            input_path: Path to input file or directory
            output_format: Output format (text or json, default: text)

        Raises:
            FileNotFoundError: If input_path does not exist
            ValueError: If output_format is not valid
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input path not found: {input_path}")

        if output_format not in ("text", "json"):
            raise ValueError(f"Invalid output format: {output_format}")

        self.input_path: Path = input_path
        self.output_format: str = output_format
        self.config: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "input_path": str(input_path),
            "items_processed": 0,
            "items_success": 0,
            "items_failed": 0,
            "errors": []
        }

    def load_config(self, config_path: Optional[Path] = None) -> None:
        """Load configuration from file.

        Args:
            config_path: Path to configuration file (optional)

        Raises:
            FileNotFoundError: If config_path specified but not found
            ValueError: If configuration format is invalid
        """
        if config_path is None:
            config_path = Path(__file__).parent / "default-config.yaml"

        if not config_path.exists():
            logger.warning(f"Config not found: {config_path}, using defaults")
            self.config = self._get_default_config()
            return

        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise ValueError(f"Invalid configuration file: {e}")

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration.

        Returns:
            Dictionary with default configuration values.
        """
        return {
            "version": "1.0.0",
            "settings": {
                "timeout": 30,
                "retries": 3,
                "batch_size": 100
            }
        }

    def validate_input(self) -> Tuple[bool, str]:
        """Validate input file or directory.

        Returns:
            Tuple containing:
                - is_valid: True if input is valid
                - message: Validation message or error description

        Examples:
            >>> processor = ScriptClass(Path("data.json"))
            >>> valid, msg = processor.validate_input()
            >>> if not valid:
            ...     logger.error(f"Validation failed: {msg}")
        """
        if not self.input_path.exists():
            return False, f"Path not found: {self.input_path}"

        if self.input_path.is_file():
            if self.input_path.suffix not in ('.json', '.yaml', '.yml', '.md'):
                return False, f"Unsupported file type: {self.input_path.suffix}"
        elif self.input_path.is_dir():
            files = list(self.input_path.glob("*.json"))
            if not files:
                return False, f"No JSON files found in {self.input_path}"

        return True, "Input validation passed"

    def process_item(self, item: Any) -> Dict[str, Any]:
        """Process a single item.

        Args:
            item: Item to process (type depends on input)

        Returns:
            Dictionary with processing results containing:
                - success: Boolean indicating success
                - data: Processed data (if success)
                - error: Error message (if failure)

        Raises:
            ValueError: If item format is invalid
        """
        try:
            # Main processing logic here
            result = {
                "success": True,
                "data": item,
                "processed_at": datetime.now().isoformat()
            }

            self.results["items_success"] += 1
            return result

        except Exception as e:
            logger.error(f"Error processing item: {e}", exc_info=True)
            error_result = {
                "success": False,
                "error": str(e),
                "item": str(item)
            }

            self.results["items_failed"] += 1
            self.results["errors"].append(error_result)
            return error_result

    def process(self) -> Dict[str, Any]:
        """Process all items from input.

        Main processing entry point that handles the full workflow:
        1. Validate input
        2. Load data
        3. Process each item
        4. Aggregate results

        Returns:
            Dictionary with complete processing results

        Raises:
            RuntimeError: If processing fails critically
        """
        logger.info(f"Starting processing: {self.input_path}")

        # Validate input
        valid, msg = self.validate_input()
        if not valid:
            logger.error(f"Validation failed: {msg}")
            raise RuntimeError(f"Invalid input: {msg}")

        logger.info(f"Validation passed: {msg}")

        # Process items (example with JSON file)
        try:
            if self.input_path.is_file():
                with open(self.input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                items = data if isinstance(data, list) else [data]
                self.results["items_processed"] = len(items)

                for item in items:
                    self.process_item(item)

            elif self.input_path.is_dir():
                files = list(self.input_path.glob("*.json"))
                self.results["items_processed"] = len(files)

                for file_path in files:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        item = json.load(f)
                    self.process_item(item)

            logger.info(f"Processing complete: {self.results['items_success']}/{self.results['items_processed']} succeeded")
            return self.results

        except Exception as e:
            logger.error(f"Processing failed: {e}", exc_info=True)
            raise RuntimeError(f"Processing error: {e}")

    def print_text_report(self) -> None:
        """Print formatted text report to console.

        Outputs human-readable processing results including:
        - Summary statistics
        - Success/failure counts
        - Error details if any
        """
        logger.info("\n" + "=" * 80)
        logger.info("PROCESSING REPORT")
        logger.info("=" * 80)
        logger.info(f"\nInput: {self.results['input_path']}")
        logger.info(f"Timestamp: {self.results['timestamp']}")
        logger.info(f"\n📊 Summary:")
        logger.info(f"  - Total items: {self.results['items_processed']}")
        logger.info(f"  - Success: {self.results['items_success']}")
        logger.info(f"  - Failed: {self.results['items_failed']}")

        if self.results['errors']:
            logger.error(f"\n❌ Errors ({len(self.results['errors'])}):")
            for i, error in enumerate(self.results['errors'], 1):
                logger.error(f"  {i}. {error['error']}")
                logger.error(f"     Item: {error['item']}")

        logger.info("\n" + "=" * 80)

        if self.results['items_failed'] > 0:
            logger.error("❌ Processing FAILED - Fix errors above")
        else:
            logger.info("✅ Processing PASSED - All items processed successfully")

    def print_json_report(self) -> None:
        """Print JSON report for CI/CD integration.

        Outputs validation results as JSON to stdout for parsing by CI/CD
        pipelines or other automation tools.

        Note: Uses print() instead of logger for machine-readable output.
        """
        print(json.dumps(self.results, indent=2))

    def run(self) -> int:
        """Run the processing workflow.

        Executes the full processing pipeline and returns appropriate
        exit code for shell integration.

        Returns:
            Exit code:
                - 0: Processing succeeded
                - 1: Processing failed
        """
        try:
            self.process()

            if self.output_format == 'json':
                self.print_json_report()
            else:
                self.print_text_report()

            return 0 if self.results['items_failed'] == 0 else 1

        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            return 1


def main() -> int:
    """Main entry point for script execution.

    Parses command-line arguments, configures processor, runs processing,
    and outputs report in requested format.

    Returns:
        Exit code:
            - 0: Processing succeeded
            - 1: Processing failed
            - 130: User interrupted with Ctrl+C

    Examples:
        Run from command line:
            $ uv run python scripts/category/script-name.py --input data.json
            $ uv run python scripts/category/script-name.py --input data.json --format json --verbose
    """
    parser = argparse.ArgumentParser(
        description='Script description for --help output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  %(prog)s --input data.json

  # JSON output with verbose logging
  %(prog)s --input data.json --format json --verbose

  # Quiet mode (errors only)
  %(prog)s --input data.json --quiet
        """
    )

    # Required arguments
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Input file or directory path'
    )

    # Optional arguments
    parser.add_argument(
        '--output',
        type=Path,
        help='Output file path (optional, default: stdout)'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Configuration file path (optional)'
    )

    # Logging arguments
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable debug logging'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-essential output (errors only)'
    )

    parser.add_argument(
        '--log-file',
        type=Path,
        help='Write logs to specified file'
    )

    # Version argument
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()

    # Setup logging based on arguments
    level = logging.DEBUG if args.verbose else logging.INFO
    global logger
    logger = setup_logger(
        __name__,
        level=level,
        log_file=args.log_file,
        quiet=args.quiet
    )

    try:
        # Initialize processor
        processor = ScriptClass(
            input_path=args.input,
            output_format=args.format
        )

        # Load configuration if provided
        if args.config:
            processor.load_config(args.config)

        # Run processing
        exit_code = processor.run()

        return exit_code

    except KeyboardInterrupt:
        logger.warning("\nProcessing cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
