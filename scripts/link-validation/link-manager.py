#!/usr/bin/env -S uv run python3
"""
SCRIPT: link-manager.py
PURPOSE: Unified Link Management Suite
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-02T00:00:00-04:00

DESCRIPTION:
    Unified link validation, fixing, and citation management tool.
    Consolidates link-validator.py, batch-link-fixer.py, citation-updater.py,
    and validate-gist-links.py into a single interface with subcommands.

LLM_USAGE:
    python scripts/link-validation/link-manager.py <subcommand> [options]

SUBCOMMANDS:
    validate         - Validate links using Playwright and HTTP checks
    fix              - Batch fix broken links in blog posts
    update-citations - Update citations to newer versions
    check-gists      - Validate GitHub gist links

EXAMPLES:
    # Validate all links
    python scripts/link-validation/link-manager.py validate --input links.json

    # Fix broken links with dry-run preview
    python scripts/link-validation/link-manager.py fix --dry-run

    # Update citations to latest versions
    python scripts/link-validation/link-manager.py update-citations --posts-dir src/posts

    # Check gist links only
    python scripts/link-validation/link-manager.py check-gists --verbose

OUTPUT:
    - Validation results in JSON format
    - Fix reports with confidence scores
    - Updated citations with backup files
    - Gist validation summary

DEPENDENCIES:
    - Python 3.8+
    - aiohttp, playwright (optional), requests
    - See imports for complete requirements

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - Replaces: link-validator.py, batch-link-fixer.py, citation-updater.py, validate-gist-links.py

MANIFEST_REGISTRY: scripts/link-validation/link-manager.py
"""

import json
import re
import shutil
import asyncio
import argparse
import subprocess
import sys
import time
import logging
import ssl
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlparse
import hashlib

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

import aiohttp
import certifi

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ============================================================================
# SHARED UTILITIES (Consolidated from all 4 scripts)
# ============================================================================

@dataclass
class ValidationResult:
    """Result of link validation"""
    url: str
    status: str  # valid, broken, redirect, timeout, error
    status_code: Optional[int]
    final_url: Optional[str]
    issue_type: Optional[str]
    error_message: Optional[str]
    response_time: float
    content_type: Optional[str]
    page_title: Optional[str]
    requires_js: bool
    ssl_valid: bool
    validation_time: str
    retry_count: int

    def to_dict(self):
        return asdict(self)

@dataclass
class CitationUpdate:
    """Represents a citation update"""
    original_citation: str
    updated_citation: str
    url_old: str
    url_new: str
    reason: str
    confidence: float
    metadata: Dict

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return 'unknown'

# ============================================================================
# LINK VALIDATOR (from link-validator.py)
# ============================================================================

class LinkValidator:
    """Validate links using multiple strategies"""

    # Common paywall indicators
    PAYWALL_INDICATORS = [
        'subscribe to read',
        'subscription required',
        'paywall',
        'premium content',
        'members only',
        'sign up to continue',
        'create free account to read',
        'limit reached',
        'article limit'
    ]

    # User agents for different validation strategies
    USER_AGENTS = {
        'bot': 'Mozilla/5.0 (compatible; LinkValidator/1.0; +https://williamzujkowski.github.io)',
        'browser': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout * 1000  # Convert to milliseconds for Playwright
        self.session = None
        self.browser = None
        self.context = None
        self.cache = {}
        self.stats = {
            'total': 0,
            'valid': 0,
            'broken': 0,
            'redirects': 0,
            'timeouts': 0,
            'errors': 0,
            'cached': 0
        }

    async def initialize(self):
        """Initialize HTTP session and Playwright browser"""
        # Create aiohttp session
        connector = aiohttp.TCPConnector(
            ssl=ssl.create_default_context(cafile=certifi.where()),
            limit=10
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers={'User-Agent': self.USER_AGENTS['bot']}
        )

        # Initialize Playwright if available
        if PLAYWRIGHT_AVAILABLE:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=['--disable-dev-shm-usage', '--no-sandbox']
            )
            self.context = await self.browser.new_context(
                user_agent=self.USER_AGENTS['browser'],
                viewport={'width': 1920, 'height': 1080}
            )

    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
        if self.browser:
            await self.browser.close()

    async def validate_batch(self, links: List[Dict]) -> List[ValidationResult]:
        """Validate a batch of links"""
        results = []

        # Group by domain to respect rate limits
        domain_groups = {}
        for link in links:
            domain = extract_domain(link['url'])
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(link)

        # Process each domain group with rate limiting
        for domain, domain_links in domain_groups.items():
            for link_data in domain_links:
                result = await self.validate_link(link_data['url'])
                results.append(result)

                # Rate limiting between requests to same domain
                if len(domain_links) > 1:
                    await asyncio.sleep(0.5)

        return results

    async def validate_link(self, url: str) -> ValidationResult:
        """Validate a single link"""
        self.stats['total'] += 1

        # Check cache
        if url in self.cache:
            self.stats['cached'] += 1
            return self.cache[url]

        start_time = time.time()
        result = None

        # Try different validation strategies
        for retry in range(self.max_retries):
            try:
                # First try with simple HTTP request
                result = await self._validate_http(url, retry)

                # If failed or suspicious, try with Playwright
                if result.status != 'valid' and PLAYWRIGHT_AVAILABLE:
                    playwright_result = await self._validate_playwright(url, retry)
                    if playwright_result.status == 'valid':
                        result = playwright_result

                if result.status == 'valid':
                    self.stats['valid'] += 1
                    break

                # Exponential backoff for retries
                if retry < self.max_retries - 1:
                    await asyncio.sleep(2 ** retry)

            except Exception as e:
                result = ValidationResult(
                    url=url,
                    status='error',
                    status_code=None,
                    final_url=None,
                    issue_type='error',
                    error_message=str(e),
                    response_time=time.time() - start_time,
                    content_type=None,
                    page_title=None,
                    requires_js=False,
                    ssl_valid=False,
                    validation_time=datetime.now().isoformat(),
                    retry_count=retry + 1
                )

        if result:
            # Update stats
            if result.status == 'broken':
                self.stats['broken'] += 1
            elif result.status == 'redirect':
                self.stats['redirects'] += 1
            elif result.status == 'timeout':
                self.stats['timeouts'] += 1
            elif result.status == 'error':
                self.stats['errors'] += 1

            # Cache result
            self.cache[url] = result

        return result

    async def _validate_http(self, url: str, retry: int) -> ValidationResult:
        """Validate using HTTP request"""
        start_time = time.time()

        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with self.session.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                ssl=True
            ) as response:
                response_time = time.time() - start_time

                # Check for redirects
                final_url = str(response.url)
                is_redirect = final_url != url

                # Read content for paywall detection
                content = await response.text()
                content_lower = content.lower()

                # Check for paywall
                has_paywall = any(
                    indicator in content_lower
                    for indicator in self.PAYWALL_INDICATORS
                )

                # Extract page title
                title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
                page_title = title_match.group(1) if title_match else None

                # Determine status and issue type
                if response.status == 200:
                    if has_paywall:
                        status = 'broken'
                        issue_type = 'paywall'
                    elif is_redirect:
                        status = 'redirect'
                        issue_type = 'redirect'
                    else:
                        status = 'valid'
                        issue_type = None
                elif response.status == 404:
                    status = 'broken'
                    issue_type = '404'
                elif response.status == 403:
                    status = 'broken'
                    issue_type = '403'
                elif response.status >= 500:
                    status = 'broken'
                    issue_type = f'{response.status}_error'
                else:
                    status = 'broken'
                    issue_type = f'http_{response.status}'

                return ValidationResult(
                    url=url,
                    status=status,
                    status_code=response.status,
                    final_url=final_url if is_redirect else None,
                    issue_type=issue_type,
                    error_message=None,
                    response_time=response_time,
                    content_type=response.headers.get('Content-Type'),
                    page_title=page_title,
                    requires_js=False,
                    ssl_valid=True,
                    validation_time=datetime.now().isoformat(),
                    retry_count=retry + 1
                )

        except asyncio.TimeoutError:
            return ValidationResult(
                url=url,
                status='timeout',
                status_code=None,
                final_url=None,
                issue_type='timeout',
                error_message='Request timeout',
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=False,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        except aiohttp.ClientSSLError as e:
            return ValidationResult(
                url=url,
                status='broken',
                status_code=None,
                final_url=None,
                issue_type='ssl_error',
                error_message=str(e),
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=False,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        except Exception as e:
            return ValidationResult(
                url=url,
                status='error',
                status_code=None,
                final_url=None,
                issue_type='error',
                error_message=str(e),
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=False,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )

    async def _validate_playwright(self, url: str, retry: int) -> ValidationResult:
        """Validate using Playwright for JavaScript-rendered content"""
        if not self.context:
            return None

        start_time = time.time()
        page = await self.context.new_page()

        try:
            # Navigate to the page
            response = await page.goto(
                url,
                wait_until='networkidle',
                timeout=self.timeout
            )

            response_time = time.time() - start_time

            # Get final URL after redirects
            final_url = page.url
            is_redirect = final_url != url

            # Get page content
            content = await page.content()
            content_lower = content.lower()

            # Check for paywall
            has_paywall = any(
                indicator in content_lower
                for indicator in self.PAYWALL_INDICATORS
            )

            # Get page title
            page_title = await page.title()

            # Determine status
            if response.status == 200:
                if has_paywall:
                    status = 'broken'
                    issue_type = 'paywall'
                elif is_redirect:
                    status = 'redirect'
                    issue_type = 'redirect'
                else:
                    status = 'valid'
                    issue_type = None
            else:
                status = 'broken'
                issue_type = f'http_{response.status}'

            result = ValidationResult(
                url=url,
                status=status,
                status_code=response.status,
                final_url=final_url if is_redirect else None,
                issue_type=issue_type,
                error_message=None,
                response_time=response_time,
                content_type=response.headers.get('content-type'),
                page_title=page_title,
                requires_js=True,
                ssl_valid=True,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )

        except PlaywrightTimeout:
            result = ValidationResult(
                url=url,
                status='timeout',
                status_code=None,
                final_url=None,
                issue_type='timeout',
                error_message='Page load timeout',
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=True,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        except Exception as e:
            result = ValidationResult(
                url=url,
                status='error',
                status_code=None,
                final_url=None,
                issue_type='error',
                error_message=str(e),
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=True,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        finally:
            await page.close()

        return result

    async def save_results(self, results: List[ValidationResult], output_file: Path, logger=None):
        """Save validation results to JSON"""
        data = {
            'validation_date': datetime.now().isoformat(),
            'stats': self.stats,
            'results': [r.to_dict() for r in results]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        if logger:
            logger.info(f"✅ Validated {self.stats['total']} links")
            logger.info(f"✔️  Valid: {self.stats['valid']}")
            logger.info(f"❌ Broken: {self.stats['broken']}")
            logger.info(f"↪️  Redirects: {self.stats['redirects']}")
            logger.info(f"⏱️  Timeouts: {self.stats['timeouts']}")
            logger.info(f"💾 Results saved to {output_file}")

# ============================================================================
# BATCH LINK FIXER (from batch-link-fixer.py)
# ============================================================================

class BatchLinkFixer:
    """Orchestrate link validation and repair"""

    def __init__(self, confidence_threshold: float = 90, dry_run: bool = False, logger=None):
        self.confidence_threshold = confidence_threshold
        self.dry_run = dry_run
        self.changes_made = []
        self.backups_created = []
        self.logger = logger or logging.getLogger(__name__)

    def apply_repairs(self, repairs_file: Path, posts_dir: Path):
        """Apply repairs to blog posts"""
        if isinstance(repairs_file, str):
            repairs_file = Path(repairs_file)
        if isinstance(posts_dir, str):
            posts_dir = Path(posts_dir)

        if not repairs_file.exists():
            self.logger.warning("No repairs file found")
            return

        # Load repairs
        with open(repairs_file, 'r', encoding='utf-8') as f:
            repairs_data = json.load(f)

        repairs = repairs_data.get('repairs', [])
        if not repairs:
            self.logger.info("No repairs to apply")
            return

        # Filter by confidence threshold
        applicable_repairs = [
            r for r in repairs
            if r.get('confidence', 0) >= self.confidence_threshold
        ]

        self.logger.info(f"Found {len(applicable_repairs)} repairs with confidence >= {self.confidence_threshold}%")

        if self.dry_run:
            self.logger.info("🔍 DRY RUN - No changes will be made")
            self._show_planned_changes(applicable_repairs)
            return

        # Group repairs by file
        repairs_by_file = self._group_repairs_by_file(applicable_repairs)

        # Apply repairs to each file
        for file_path, file_repairs in repairs_by_file.items():
            self._apply_file_repairs(file_path, file_repairs)

    def _group_repairs_by_file(self, repairs: List[Dict]) -> Dict[str, List[Dict]]:
        """Group repairs by source file"""
        # This would need links.json to map repairs to files
        # Simplified implementation
        repairs_by_file = {}
        for repair in repairs:
            file_path = repair.get('file_path', 'unknown')
            if file_path not in repairs_by_file:
                repairs_by_file[file_path] = []
            repairs_by_file[file_path].append(repair)
        return repairs_by_file

    def _apply_file_repairs(self, file_path: str, repairs: List[Dict]):
        """Apply repairs to a single file"""
        file_path = Path(file_path)

        if not file_path.exists():
            self.logger.warning(f"File not found: {file_path}")
            return

        # Create backup
        if not self.dry_run:
            backup_path = self._create_backup(file_path)
            self.backups_created.append((file_path, backup_path))

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply each repair
        changes = 0
        for repair in repairs:
            old_url = repair['original_url']
            new_url = repair['suggested_url']

            # Count occurrences
            count = content.count(old_url)
            if count > 0:
                content = content.replace(old_url, new_url)
                changes += count
                self.changes_made.append({
                    'file': str(file_path),
                    'old_url': old_url,
                    'new_url': new_url,
                    'count': count,
                    'confidence': repair['confidence'],
                    'repair_type': repair.get('repair_type', 'unknown')
                })

        # Write changes
        if changes > 0 and not self.dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"✅ Fixed {changes} links in {file_path.name}")

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup of file"""
        backup_path = file_path.with_suffix(f'.bak.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _show_planned_changes(self, repairs: List[Dict]):
        """Show what changes would be made"""
        self.logger.info("Planned changes:")
        self.logger.info("-" * 60)

        for repair in repairs[:10]:  # Show first 10
            self.logger.info(f"\nOriginal: {repair['original_url']}")
            self.logger.info(f"Replace:  {repair['suggested_url']}")
            self.logger.info(f"Confidence: {repair['confidence']}%")

        if len(repairs) > 10:
            self.logger.info(f"\n... and {len(repairs) - 10} more changes")

# ============================================================================
# CITATION UPDATER (from citation-updater.py)
# ============================================================================

class CitationUpdater:
    """Updates citations to newer versions and better sources"""

    def __init__(self, logger=None):
        self.session = None
        self.logger = logger or logging.getLogger(__name__)
        self.stats = {
            'total_citations': 0,
            'updated': 0,
            'already_current': 0,
            'no_update_found': 0,
            'errors': 0
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def check_arxiv_version(self, url: str) -> Optional[CitationUpdate]:
        """Check if arXiv paper has newer version"""
        match = re.search(r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+)(?:v(\d+))?', url)
        if not match:
            return None

        arxiv_id = match.group(1)
        current_version = int(match.group(2)) if match.group(2) else 1

        # Check latest version via arXiv API
        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

        try:
            async with self.session.get(api_url) as response:
                if response.status == 200:
                    content = await response.text()

                    # Parse version from response
                    version_match = re.search(r'<arxiv:comment>.*v(\d+)', content)
                    if version_match:
                        latest_version = int(version_match.group(1))
                    else:
                        version_matches = re.findall(r'/abs/\d+\.\d+v(\d+)', content)
                        latest_version = max(int(v) for v in version_matches) if version_matches else current_version

                    if latest_version > current_version:
                        new_url = re.sub(r'(arxiv\.org/(?:abs|pdf)/\d+\.\d+)(?:v\d+)?',
                                       f'\\1v{latest_version}', url)

                        title_match = re.search(r'<title>([^<]+)</title>', content)
                        title = title_match.group(1) if title_match else "Paper"

                        return CitationUpdate(
                            original_citation=f"[{title}]({url})",
                            updated_citation=f"[{title}]({new_url})",
                            url_old=url,
                            url_new=new_url,
                            reason=f"Updated to version {latest_version} (from v{current_version})",
                            confidence=95,
                            metadata={'latest_version': latest_version, 'old_version': current_version}
                        )

        except Exception as e:
            self.logger.debug(f"Error checking arXiv version: {e}")

        return None

    async def update_all_citations(self, citations: List[Dict]) -> List[CitationUpdate]:
        """Update all citations"""
        updates = []
        self.stats['total_citations'] = len(citations)

        # Process in batches to avoid overwhelming APIs
        batch_size = 10
        for i in range(0, len(citations), batch_size):
            batch = citations[i:i+batch_size]

            for citation in batch:
                url = citation.get('url', '')
                if 'arxiv.org' in url:
                    update = await self.check_arxiv_version(url)
                    if update:
                        updates.append(update)
                        self.stats['updated'] += 1
                    else:
                        self.stats['no_update_found'] += 1

            # Small delay between batches
            await asyncio.sleep(1)

        return updates

# ============================================================================
# GIST VALIDATOR (from validate-gist-links.py)
# ============================================================================

class GistValidator:
    """Validates GitHub gist links in blog posts"""

    def __init__(self, verbose: bool = False, timeout: int = 10, logger=None):
        self.verbose = verbose
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (compatible; GistValidator/1.0)'
            })
        else:
            self.session = None
            self.logger.warning("requests library not available, using basic validation")

    def find_gists_in_file(self, filepath: Path) -> List[Tuple[int, str]]:
        """Find all gist URLs in a file"""
        gist_pattern = re.compile(
            r'https://gist\.github\.com/williamzujkowski/([a-f0-9]{32})'
        )
        comment_pattern = re.compile(r'<!--.*?-->', re.DOTALL)

        gists = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

                # Remove HTML comments before processing
                content_no_comments = comment_pattern.sub('', content)

                # Find gists in non-commented content
                for line_num, line in enumerate(content_no_comments.split('\n'), start=1):
                    matches = gist_pattern.findall(line)
                    for gist_id in matches:
                        full_url = f'https://gist.github.com/williamzujkowski/{gist_id}'
                        gists.append((line_num, full_url))
        except Exception as e:
            self.logger.error(f"Cannot read {filepath}: {e}")
            return []

        return gists

    def validate_gist(self, url: str) -> Tuple[bool, int, str]:
        """Validate a single gist URL"""
        if not self.session:
            return (True, 200, "Validation skipped (requests not available)")

        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)

            # Accept 200 (OK) or 301 (redirect) as valid
            if response.status_code in [200, 301]:
                return (True, response.status_code, "")
            else:
                return (False, response.status_code, f"HTTP {response.status_code}")

        except Exception as e:
            return (False, 0, str(e))

    def scan_posts(self, posts_dir: Path) -> Dict[str, List[Tuple[int, str]]]:
        """Scan all blog posts for gist links"""
        post_gists = {}

        if not posts_dir.exists():
            self.logger.error(f"Posts directory not found: {posts_dir}")
            return post_gists

        for post_file in sorted(posts_dir.glob("*.md")):
            gists = self.find_gists_in_file(post_file)
            if gists:
                post_gists[post_file.name] = gists

        return post_gists

    def validate_all(self, posts_dir: Path) -> Tuple[int, int, List[Dict]]:
        """Validate all gist links in blog posts"""
        start_time = time.time()
        post_gists = self.scan_posts(posts_dir)

        if not post_gists:
            self.logger.info("No gist links found in blog posts")
            return (0, 0, [])

        # Count total gists
        total_gists = sum(len(gists) for gists in post_gists.values())
        self.logger.info(f"📎 Validating {total_gists} GitHub gist links...")

        valid_count = 0
        broken_count = 0
        broken_links = []

        for post_name, gists in post_gists.items():
            # Deduplicate gists
            unique_gists = {}
            for line_num, url in gists:
                if url not in unique_gists:
                    unique_gists[url] = []
                unique_gists[url].append(line_num)

            for url, line_nums in unique_gists.items():
                if self.verbose:
                    self.logger.info(f"  Checking {url}...")

                is_valid, status_code, error_msg = self.validate_gist(url)

                if is_valid:
                    valid_count += 1
                    if self.verbose:
                        self.logger.info("✅")
                else:
                    broken_count += 1
                    if self.verbose:
                        self.logger.info(f"❌ {error_msg}")

                    for line_num in line_nums:
                        broken_links.append({
                            'post': post_name,
                            'line': line_num,
                            'url': url,
                            'error': error_msg
                        })

        # Print summary
        elapsed = time.time() - start_time
        self.logger.info("=" * 60)
        self.logger.info("📊 SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"✅ Valid:   {valid_count}/{total_gists} gists")
        self.logger.info(f"❌ Broken:  {broken_count}/{total_gists} gists")
        self.logger.info(f"⏱️  Time:   {elapsed:.1f}s")

        return (valid_count, broken_count, broken_links)

# ============================================================================
# SUBCOMMAND HANDLERS
# ============================================================================

async def cmd_validate(args, logger):
    """Validate links using Playwright and HTTP checks"""
    if not args.input.exists():
        logger.error(f"❌ Input file not found: {args.input}")
        return 1

    # Log Playwright availability
    if not PLAYWRIGHT_AVAILABLE:
        logger.warning("⚠️  Playwright not installed. Using basic HTTP validation.")

    # Load links
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    links = data.get('links', [])
    logger.info(f"📋 Loaded {len(links)} links to validate")

    # Initialize validator
    validator = LinkValidator(
        max_retries=args.max_retries,
        timeout=args.timeout
    )

    await validator.initialize()

    try:
        # Validate links
        results = await validator.validate_batch(links)

        # Save results
        await validator.save_results(results, args.output, logger)
    finally:
        await validator.cleanup()

    return 0

def cmd_fix(args, logger):
    """Batch fix broken links in blog posts"""
    fixer = BatchLinkFixer(
        confidence_threshold=args.confidence_threshold,
        dry_run=args.dry_run,
        logger=logger
    )

    fixer.apply_repairs(args.repairs, args.posts_dir)
    return 0

async def cmd_update_citations(args, logger):
    """Update citations to newer versions"""
    if not args.links.exists():
        logger.error(f"❌ Error: Links file not found: {args.links}")
        return 1

    # Load links
    with open(args.links, 'r') as f:
        links_data = json.load(f)

    # Filter to citations only
    citations = [
        link for link in links_data.get('links', [])
        if link.get('type') in ['citation', 'reference']
    ]

    logger.info(f"Found {len(citations)} citations to check")

    # Update citations
    async with CitationUpdater(logger=logger) as updater:
        updates = await updater.update_all_citations(citations)

        if updates:
            logger.info(f"📊 Found {len(updates)} citations that can be updated")

            # Save results
            with open(args.output, 'w') as f:
                json.dump({
                    'generated': datetime.now().isoformat(),
                    'stats': updater.stats,
                    'updates': [asdict(u) for u in updates]
                }, f, indent=2)

            logger.info(f"✅ Report saved to {args.output}")
        else:
            logger.info("No citation updates found")

    return 0

def cmd_check_gists(args, logger):
    """Validate GitHub gist links"""
    posts_dir = args.posts_dir

    validator = GistValidator(
        verbose=args.verbose,
        timeout=args.timeout,
        logger=logger
    )

    try:
        valid_count, broken_count, broken_links = validator.validate_all(posts_dir)

        # Output results
        if args.json_output:
            result = {
                'valid': valid_count,
                'broken': broken_count,
                'total': valid_count + broken_count,
                'broken_links': broken_links
            }
            print(json.dumps(result, indent=2))

        if broken_count > 0:
            if not args.json_output:
                logger.error("\n❌ BROKEN LINKS FOUND:\n")
                for broken in broken_links:
                    logger.error(f"src/posts/{broken['post']}:{broken['line']}")
                    logger.error(f"  {broken['url']}")
                    logger.error(f"  {broken['error']}\n")
            return 1

    except KeyboardInterrupt:
        logger.error("\n❌ Interrupted by user")
        return 2
    except Exception as e:
        logger.error(f"\n❌ ERROR: {e}")
        return 2

    return 0

# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Unified link validation, fixing, and citation management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate links
  python scripts/link-validation/link-manager.py validate --input links.json

  # Fix broken links (dry-run)
  python scripts/link-validation/link-manager.py fix --dry-run

  # Update citations
  python scripts/link-validation/link-manager.py update-citations --links links.json

  # Check gist links
  python scripts/link-validation/link-manager.py check-gists --verbose
        """
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Validate subcommand
    validate_parser = subparsers.add_parser('validate', help='Validate links')
    validate_parser.add_argument('--input', type=Path, default=Path('links.json'),
                                help='Input JSON file with extracted links')
    validate_parser.add_argument('--output', type=Path, default=Path('validation.json'),
                                help='Output JSON file')
    validate_parser.add_argument('--max-retries', type=int, default=3,
                                help='Maximum retry attempts')
    validate_parser.add_argument('--timeout', type=int, default=30,
                                help='Request timeout in seconds')

    # Fix subcommand
    fix_parser = subparsers.add_parser('fix', help='Batch fix broken links')
    fix_parser.add_argument('--posts-dir', type=Path, default=Path('src/posts'),
                           help='Directory containing blog posts')
    fix_parser.add_argument('--repairs', type=Path, default=Path('repairs.json'),
                           help='Repairs file to apply')
    fix_parser.add_argument('--confidence-threshold', type=float, default=90,
                           help='Minimum confidence for auto-fix (0-100)')
    fix_parser.add_argument('--dry-run', action='store_true',
                           help='Show what would be changed without modifying files')

    # Update citations subcommand
    update_parser = subparsers.add_parser('update-citations', help='Update citations to newer versions')
    update_parser.add_argument('--links', type=Path, default=Path('links.json'),
                              help='JSON file with extracted links')
    update_parser.add_argument('--posts-dir', type=Path, default=Path('src/posts'),
                              help='Directory containing blog posts')
    update_parser.add_argument('--output', type=Path, default=Path('citation-updates.json'),
                              help='Output report file')

    # Check gists subcommand
    gists_parser = subparsers.add_parser('check-gists', help='Validate GitHub gist links')
    gists_parser.add_argument('--posts-dir', type=Path, default=Path('src/posts'),
                             help='Directory containing blog posts')
    gists_parser.add_argument('--timeout', type=int, default=10,
                             help='Timeout in seconds per gist')
    gists_parser.add_argument('--json-output', action='store_true',
                             help='Output results as JSON')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    # Route to appropriate handler
    try:
        if args.command == 'validate':
            return asyncio.run(cmd_validate(args, logger))
        elif args.command == 'fix':
            return cmd_fix(args, logger)
        elif args.command == 'update-citations':
            return asyncio.run(cmd_update_citations(args, logger))
        elif args.command == 'check-gists':
            return cmd_check_gists(args, logger)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 2

    return 0

if __name__ == '__main__':
    sys.exit(main())
