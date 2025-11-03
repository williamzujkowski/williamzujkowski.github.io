#!/usr/bin/env -S uv run python3
"""
DEPRECATED: This script has been replaced by link-manager.py
Use: python scripts/link-validation/link-manager.py fix [options]

This wrapper provides backward compatibility.

Version: 2.0.0
Updated: 2025-11-03
"""

import sys
import subprocess
from pathlib import Path

# Setup logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

def main():
    # Build command for new unified script
    script_path = Path(__file__).parent / "link-manager.py"
    cmd = [sys.executable, str(script_path), "fix"] + sys.argv[1:]

    # Execute and forward return code
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == '__main__':
    logger.warning("⚠️  WARNING: batch-link-fixer.py is deprecated. Use: link-manager.py fix")
    logger.info("   Running compatibility wrapper...\n")
    sys.exit(main())
