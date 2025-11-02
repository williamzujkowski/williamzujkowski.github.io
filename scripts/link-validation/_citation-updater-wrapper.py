#!/usr/bin/env -S uv run python3
"""
DEPRECATED: This script has been replaced by link-manager.py
Use: python scripts/link-validation/link-manager.py update-citations [options]

This wrapper provides backward compatibility.
"""

import sys
import subprocess
from pathlib import Path

def main():
    # Build command for new unified script
    script_path = Path(__file__).parent / "link-manager.py"
    cmd = [sys.executable, str(script_path), "update-citations"] + sys.argv[1:]

    # Execute and forward return code
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == '__main__':
    print("⚠️  WARNING: citation-updater.py is deprecated. Use: link-manager.py update-citations")
    print("   Running compatibility wrapper...\n")
    sys.exit(main())
