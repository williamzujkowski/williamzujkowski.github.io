#!/usr/bin/env -S uv run python3
"""
SCRIPT: validate-suricata-gists.py
PURPOSE: Validate Suricata blog post gist embeds using Playwright
CATEGORY: validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Validates that GitHub gist embeds render correctly on the Suricata blog post.
    Checks for console errors, network failures, and gist loading status.

    Post: Building a Network Traffic Analysis Lab with Suricata
    URL: http://localhost:8080/posts/building-a-network-traffic-analysis-lab-with-suricata/
    Expected gists: 7

USAGE:
    # Start local server first
    npm start

    # Run validation
    uv run python scripts/validation/validate-suricata-gists.py

OUTPUT:
    - ✅/❌ Status for each gist
    - Console errors (if any)
    - Network request summary
    - Page load time
    - Issues found

DEPENDENCIES:
    - uv run playwright install chromium
    - Local server running on port 8080
"""

import sys
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Tuple

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from logging_config import setup_logger

logger = setup_logger(__name__)

try:
    from playwright.async_api import async_playwright, Page, Response
except ImportError:
    logger.error("Playwright not installed. Run: uv pip install playwright && uv run playwright install chromium")
    sys.exit(1)


async def validate_gists(url: str, expected_gists: int = 7) -> Dict:
    """Validate gist embeds on a blog post.

    Args:
        url: Post URL to validate
        expected_gists: Expected number of gist embeds

    Returns:
        Dict with validation results
    """
    results = {
        'url': url,
        'expected_gists': expected_gists,
        'load_time': 0.0,
        'console_errors': [],
        'network_errors': [],
        'gists_loaded': [],
        'gists_failed': [],
        'total_requests': 0,
        'success': False
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Track console errors
        console_errors: List[str] = []
        page.on('console', lambda msg:
            console_errors.append(f"{msg.type}: {msg.text}") if msg.type == 'error' else None
        )

        # Track network requests
        network_requests: List[Response] = []
        network_errors: List[Tuple[str, str]] = []

        async def track_response(response: Response):
            network_requests.append(response)
            if response.status >= 400:
                network_errors.append((response.url, str(response.status)))

        page.on('response', track_response)

        # Navigate and measure load time
        start_time = time.perf_counter()
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
        except Exception as e:
            logger.error(f"Failed to load page: {e}")
            results['console_errors'].append(f"Navigation error: {e}")
            await browser.close()
            return results

        load_time = time.perf_counter() - start_time
        results['load_time'] = load_time

        # Check for gist script tags
        gist_scripts = await page.locator('script[src*="gist.github.com"]').all()
        results['gists_loaded'] = [
            await script.get_attribute('src') for script in gist_scripts
        ]

        # Wait for gist iframes to render (gists inject iframes dynamically)
        try:
            # Wait for at least one iframe to appear (max 10 seconds)
            await page.wait_for_selector('.gist, .gist-file', timeout=10000)
            # Give remaining gists time to render
            await page.wait_for_timeout(3000)
        except Exception as e:
            logger.warning(f"Timeout waiting for gist containers: {e}")

        # Check for gist containers (GitHub's gist embed structure)
        # Gists render as <div class="gist"> elements, not iframes
        gist_containers = await page.locator('.gist').all()
        rendered_gists = len(gist_containers)

        # Check for stuck "Loading..." states
        loading_elements = await page.locator('text=Loading...').all()
        stuck_loading = len(loading_elements)

        # Store results
        results['console_errors'] = console_errors
        results['network_errors'] = network_errors
        results['total_requests'] = len(network_requests)
        results['rendered_gists'] = rendered_gists
        results['stuck_loading'] = stuck_loading

        # Determine success
        results['success'] = (
            rendered_gists == expected_gists and
            len(network_errors) == 0 and
            stuck_loading == 0
        )

        # Take screenshot for visual verification (optional)
        screenshot_path = Path(__file__).parent.parent.parent / 'tmp' / 'suricata-gists-screenshot.png'
        screenshot_path.parent.mkdir(exist_ok=True)
        await page.screenshot(path=str(screenshot_path), full_page=True)
        results['screenshot'] = str(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")

        await browser.close()

    return results


def print_report(results: Dict) -> int:
    """Print validation report and return exit code.

    Args:
        results: Validation results dictionary

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    logger.info("=" * 80)
    logger.info("SURICATA GIST VALIDATION REPORT")
    logger.info("=" * 80)
    logger.info(f"URL: {results['url']}")
    logger.info(f"Expected gists: {results['expected_gists']}")
    logger.info(f"Load time: {results['load_time']:.3f}s")
    logger.info("")

    # Gist status
    logger.info("GIST RENDERING STATUS:")
    logger.info("-" * 80)
    rendered = results.get('rendered_gists', 0)
    expected = results['expected_gists']

    if rendered == expected:
        logger.info(f"✅ All gists loaded: {rendered}/{expected}")
    else:
        logger.error(f"❌ Gist mismatch: {rendered}/{expected} rendered")

    stuck = results.get('stuck_loading', 0)
    if stuck > 0:
        logger.error(f"❌ Stuck loading states: {stuck}")
    else:
        logger.info("✅ No stuck loading states")

    logger.info("")

    # Console errors
    logger.info("CONSOLE ERRORS:")
    logger.info("-" * 80)
    if results['console_errors']:
        logger.error(f"❌ Found {len(results['console_errors'])} console errors:")
        for error in results['console_errors']:
            logger.error(f"  - {error}")
    else:
        logger.info("✅ Zero console errors")

    logger.info("")

    # Network errors
    logger.info("NETWORK STATUS:")
    logger.info("-" * 80)
    logger.info(f"Total requests: {results['total_requests']}")

    if results['network_errors']:
        logger.error(f"❌ Found {len(results['network_errors'])} network errors:")
        for url, status in results['network_errors']:
            logger.error(f"  - {status}: {url}")
    else:
        logger.info("✅ All network requests successful")

    logger.info("")

    # Gist URLs loaded
    logger.info("GIST SCRIPT TAGS FOUND:")
    logger.info("-" * 80)
    for i, gist_url in enumerate(results['gists_loaded'], 1):
        logger.info(f"{i}. {gist_url}")

    logger.info("")

    # Screenshot
    if 'screenshot' in results:
        logger.info("SCREENSHOT:")
        logger.info("-" * 80)
        logger.info(f"Saved to: {results['screenshot']}")
        logger.info("")

    # Final verdict
    logger.info("=" * 80)
    logger.info("FINAL RESULT:")
    logger.info("=" * 80)

    if results['success']:
        logger.info("✅ VALIDATION PASSED")
        logger.info("All gists loaded successfully with zero errors")
        return 0
    else:
        logger.error("❌ VALIDATION FAILED")
        logger.error("Issues detected - see details above")
        return 1


async def main() -> int:
    """Main validation function."""
    url = "http://localhost:8080/posts/building-a-network-traffic-analysis-lab-with-suricata/"
    expected_gists = 7

    logger.info("Starting Suricata gist validation...")
    logger.info(f"Target: {url}")
    logger.info(f"Expected gists: {expected_gists}")
    logger.info("")

    results = await validate_gists(url, expected_gists)
    return print_report(results)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
