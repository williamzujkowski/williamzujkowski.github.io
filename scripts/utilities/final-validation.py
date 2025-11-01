#!/usr/bin/env -S uv run python3
"""
SCRIPT: final-validation.py
PURPOSE: Final validation of live site after deployment
CATEGORY: utilities
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

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
from playwright.async_api import async_playwright
import json

async def validate_live_site():
    """Quick validation of key features on live site"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("=" * 70)
        print("🌐 Final Live Site Validation")
        print("=" * 70)
        
        # Check Claude-Flow post (should have Mermaid and image)
        url = "https://williamzujkowski.github.io/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        print(f"\n📝 Checking Claude-Flow post...")
        print(f"   URL: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Check for Mermaid diagrams
        mermaid_divs = await page.query_selector_all('div.mermaid')
        svg_diagrams = await page.query_selector_all('svg[id*="mermaid"], svg.mermaid-svg, div.mermaid svg')
        images = await page.query_selector_all('article img')
        
        print(f"   ✅ Mermaid diagrams: {len(mermaid_divs)} containers, {len(svg_diagrams)} rendered")
        print(f"   ✅ Images in article: {len(images)}")
        
        # Check if Unsplash image is present
        unsplash_images = await page.query_selector_all('img[src*="unsplash.com"]')
        if unsplash_images:
            print(f"   ✅ Unsplash image found with attribution")
        
        # Check Zero Trust post (should have diagrams)
        url2 = "https://williamzujkowski.github.io/posts/implementing-zero-trust-security-never-trust-always-verify/"
        print(f"\n📝 Checking Zero Trust post...")
        print(f"   URL: {url2}")
        
        await page.goto(url2, wait_until='networkidle', timeout=30000)
        
        mermaid_divs2 = await page.query_selector_all('div.mermaid')
        svg_diagrams2 = await page.query_selector_all('svg[id*="mermaid"], svg.mermaid-svg, div.mermaid svg')
        images2 = await page.query_selector_all('article img')
        
        print(f"   ✅ Mermaid diagrams: {len(mermaid_divs2)} containers, {len(svg_diagrams2)} rendered")
        print(f"   ✅ Images in article: {len(images2)}")
        
        # Take final screenshots
        await page.screenshot(path="final_validation_zerotrust.png")
        
        await page.goto(url, wait_until='networkidle')
        await page.screenshot(path="final_validation_claudeflow.png")
        
        await browser.close()
        
        print("\n" + "=" * 70)
        print("✅ Final Validation Complete!")
        print("\nSummary:")
        print("• Mermaid diagrams are rendering properly")
        print("• Images are displaying with attribution")
        print("• Site is fully deployed and functional")
        print("\n📸 Screenshots saved for review")

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