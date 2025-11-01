#!/usr/bin/env python3
"""
Centralized logging configuration for all scripts.

Provides structured, colored logging with file output support.
Designed for consistent logging across the repository.

Usage:
    from lib.logging_config import setup_logger

    logger = setup_logger(__name__)
    logger.info("Processing started")

    # With file output and quiet mode
    logger = setup_logger(__name__, log_file=Path("output.log"), quiet=True)
    logger.debug("This goes to file only")
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for terminal output."""

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'
    }

    def format(self, record):
        """Format log record with colors if outputting to terminal."""
        if sys.stdout.isatty():
            levelname = record.levelname
            record.levelname = f"{self.COLORS.get(levelname, '')}{levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    quiet: bool = False
) -> logging.Logger:
    """
    Setup a logger with console and optional file output.

    Args:
        name: Logger name (usually __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for log output
        quiet: If True, only log WARNING and above to console

    Returns:
        Configured logger instance

    Examples:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Processing started")

        >>> logger = setup_logger(__name__, level=logging.DEBUG, quiet=True)
        >>> logger.debug("This goes to file only if log_file is set")

        >>> logger = setup_logger(__name__, log_file=Path("logs/output.log"))
        >>> logger.error("Error details logged to file", exc_info=True)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()  # Remove existing handlers

    # Console handler
    console_level = logging.WARNING if quiet else level
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(console_level)
    console.setFormatter(ColoredFormatter(
        '%(levelname)s: %(message)s'
    ))
    logger.addHandler(console)

    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

    return logger
