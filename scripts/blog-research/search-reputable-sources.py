#!/usr/bin/env -S uv run python3
"""
SCRIPT: search-reputable-sources.py
PURPOSE: Search for reputable sources using Playwright to back up technical claims in blog posts
CATEGORY: utilities
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Search for reputable sources using Playwright to back up technical claims in blog posts. This script is part of the utilities
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/search-reputable-sources.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/search-reputable-sources.py

    # With verbose output
    python scripts/search-reputable-sources.py --verbose

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

MANIFEST_REGISTRY: scripts/search-reputable-sources.py
"""

import asyncio
import json
import sys
from playwright.async_api import async_playwright
from pathlib import Path
import frontmatter
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

class ReputableSourceSearcher:
    def __init__(self):
        self.sources_found = {}
        self.reputable_domains = [
            'arxiv.org',
            'ieee.org',
            'acm.org',
            'nist.gov',
            'owasp.org',
            'sans.org',
            'cve.mitre.org',
            'cloudflare.com/learning',
            'kubernetes.io',
            'docker.com/docs',
            'aws.amazon.com/documentation',
            'cloud.google.com/docs',
            'docs.microsoft.com',
            'github.com',
            'stackoverflow.com',
            'reddit.com/r/netsec',
            'reddit.com/r/cybersecurity',
            'schneier.com',
            'krebsonsecurity.com'
        ]
    
    async def search_for_topic(self, browser, topic: str, context: str = ""):
        """Search for reputable sources on a specific topic."""
        page = await browser.new_page()
        
        try:
            # Build search query
            search_query = f'{topic} {context} site:arxiv.org OR site:ieee.org OR site:nist.gov OR site:owasp.org'
            
            # Use Google Scholar for academic sources
            await page.goto('https://scholar.google.com')
            await page.wait_for_selector('input[name="q"]')
            
            # Search
            await page.fill('input[name="q"]', search_query)
            await page.press('input[name="q"]', 'Enter')
            
            # Wait for results
            await page.wait_for_selector('.gs_r', timeout=5000)
            
            # Extract top results
            results = await page.evaluate('''() => {
                const items = document.querySelectorAll('.gs_r');
                const sources = [];
                for (let i = 0; i < Math.min(items.length, 5); i++) {
                    const titleEl = items[i].querySelector('h3 a');
                    const snippetEl = items[i].querySelector('.gs_rs');
                    if (titleEl) {
                        sources.push({
                            title: titleEl.innerText,
                            url: titleEl.href,
                            snippet: snippetEl ? snippetEl.innerText.substring(0, 200) : ''
                        });
                    }
                }
                return sources;
            }''')
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching for {topic}: {e}")
            return []
        finally:
            await page.close()
    
    async def search_technical_docs(self, browser, technology: str):
        """Search official documentation for specific technologies."""
        page = await browser.new_page()
        
        sources = []
        
        # Technology-specific documentation sites
        doc_sites = {
            'kubernetes': 'https://kubernetes.io/docs/',
            'docker': 'https://docs.docker.com/',
            'terraform': 'https://www.terraform.io/docs/',
            'aws': 'https://docs.aws.amazon.com/',
            'python': 'https://docs.python.org/',
            'security': 'https://owasp.org/',
            'networking': 'https://www.cloudflare.com/learning/',
            'ebpf': 'https://ebpf.io/what-is-ebpf/',
            'prometheus': 'https://prometheus.io/docs/',
            'grafana': 'https://grafana.com/docs/'
        }
        
        tech_lower = technology.lower()
        for key, url in doc_sites.items():
            if key in tech_lower or tech_lower in key:
                sources.append({
                    'title': f'Official {key.title()} Documentation',
                    'url': url,
                    'type': 'official_docs'
                })
        
        await page.close()
        return sources
    
    async def enhance_post_with_sources(self, post_path: Path, browser):
        """Search for sources specific to a blog post's content."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        tags = post.metadata.get('tags', [])
        title = post.metadata.get('title', '')

        logger.info(f"Searching sources for: {post_path.name}")
        
        all_sources = []
        
        # Search based on title keywords
        title_keywords = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', title)
        for keyword in title_keywords[:3]:  # Top 3 key phrases
            sources = await self.search_for_topic(browser, keyword)
            all_sources.extend(sources)
        
        # Search for technology-specific documentation
        for tag in tags:
            if tag not in ['posts']:
                tech_sources = await self.search_technical_docs(browser, tag)
                all_sources.extend(tech_sources)
        
        # Remove duplicates
        unique_sources = []
        seen_urls = set()
        for source in all_sources:
            if source.get('url') and source['url'] not in seen_urls:
                seen_urls.add(source['url'])
                unique_sources.append(source)
        
        self.sources_found[post_path.name] = unique_sources[:5]  # Top 5 sources
        
        return unique_sources[:5]
    
    async def search_all_posts(self):
        """Search for sources for all blog posts."""
        posts_dir = Path('src/posts')
        
        # Priority posts that need sources most
        priority_posts = [
            '2025-07-01-ebpf-security-monitoring-practical-guide.md',
            '2024-10-22-ai-edge-computing.md',
            '2024-06-15-quantum-computing-cybersecurity.md',
            '2024-05-10-blockchain-security-analysis.md',
            '2025-02-10-automating-home-network-security.md'
        ]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Search for priority posts
            for post_name in priority_posts:
                post_path = posts_dir / post_name
                if post_path.exists():
                    await self.enhance_post_with_sources(post_path, browser)
                    await asyncio.sleep(2)  # Be respectful to search engines
            
            await browser.close()
        
        # Save sources to file
        with open('docs/blog-sources.json', 'w') as f:
            json.dump(self.sources_found, f, indent=2)

        logger.info(f"Found sources for {len(self.sources_found)} posts")
        logger.info("Sources saved to: docs/blog-sources.json")

async def main(quiet=False):
    searcher = ReputableSourceSearcher()
    await searcher.search_all_posts()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Search for reputable sources using Playwright to back up technical claims',
        epilog='''
Examples:
  %(prog)s
  %(prog)s --quiet
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    try:
        asyncio.run(main(args.quiet))
        sys.exit(0)
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error("Expected: src/posts/")
        logger.error("Tip: Run from repository root")
        sys.exit(2)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)