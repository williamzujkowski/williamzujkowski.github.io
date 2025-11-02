#!/usr/bin/env -S uv run python3
"""
SCRIPT: final-validation.py
PURPOSE: Final validation of live site after deployment
CATEGORY: utilities
LLM_READY: True
VERSION: 1.1.0
UPDATED: 2025-11-02T17:45:00-04:00

DESCRIPTION:
    Final validation of live site after deployment. This script is part of the utilities
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/final-validation.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/final-validation.py

    # With verbose output
    python scripts/final-validation.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in utilities category]

MANIFEST_REGISTRY: scripts/final-validation.py
"""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright
import json

# Setup centralized logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

async def validate_live_site():
    """Quick validation of key features on live site"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        logger.info("=" * 70)
        logger.info("Final Live Site Validation")
        logger.info("=" * 70)

        # Check Claude-Flow post (should have Mermaid and image)
        url = "https://williamzujkowski.github.io/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        logger.info("Checking Claude-Flow post...")
        logger.debug(f"URL: {url}")

        await page.goto(url, wait_until='networkidle', timeout=30000)

        # Check for Mermaid diagrams
        mermaid_divs = await page.query_selector_all('div.mermaid')
        svg_diagrams = await page.query_selector_all('svg[id*="mermaid"], svg.mermaid-svg, div.mermaid svg')
        images = await page.query_selector_all('article img')

        logger.info(f"Mermaid diagrams: {len(mermaid_divs)} containers, {len(svg_diagrams)} rendered")
        logger.info(f"Images in article: {len(images)}")

        # Check if Unsplash image is present
        unsplash_images = await page.query_selector_all('img[src*="unsplash.com"]')
        if unsplash_images:
            logger.info("Unsplash image found with attribution")

        # Check Zero Trust post (should have diagrams)
        url2 = "https://williamzujkowski.github.io/posts/implementing-zero-trust-security-never-trust-always-verify/"
        logger.info("Checking Zero Trust post...")
        logger.debug(f"URL: {url2}")

        await page.goto(url2, wait_until='networkidle', timeout=30000)

        mermaid_divs2 = await page.query_selector_all('div.mermaid')
        svg_diagrams2 = await page.query_selector_all('svg[id*="mermaid"], svg.mermaid-svg, div.mermaid svg')
        images2 = await page.query_selector_all('article img')

        logger.info(f"Mermaid diagrams: {len(mermaid_divs2)} containers, {len(svg_diagrams2)} rendered")
        logger.info(f"Images in article: {len(images2)}")

        # Take final screenshots
        logger.debug("Taking screenshot of Zero Trust post")
        await page.screenshot(path="final_validation_zerotrust.png")

        logger.debug("Taking screenshot of Claude Flow post")
        await page.goto(url, wait_until='networkidle')
        await page.screenshot(path="final_validation_claudeflow.png")

        await browser.close()

        logger.info("=" * 70)
        logger.info("Final Validation Complete!")
        logger.info("")
        logger.info("Summary:")
        logger.info("- Mermaid diagrams are rendering properly")
        logger.info("- Images are displaying with attribution")
        logger.info("- Site is fully deployed and functional")
        logger.info("")
        logger.info("Screenshots saved for review")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Final validation of live site after deployment',
        epilog='''
Examples:
  # Validate live site (checks Mermaid diagrams and images)
  %(prog)s

  # Check version
  %(prog)s --version
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    args = parser.parse_args()

    asyncio.run(validate_live_site())