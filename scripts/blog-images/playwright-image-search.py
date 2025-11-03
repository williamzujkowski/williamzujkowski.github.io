#!/usr/bin/env -S uv run python3
"""
SCRIPT: playwright-image-search.py
PURPOSE: Playwright-based Stock Image Search and Download
CATEGORY: blog_images
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Playwright-based Stock Image Search and Download. This script is part of the blog_images
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/playwright-image-search.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/playwright-image-search.py

    # With verbose output
    python scripts/playwright-image-search.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in image_management category]

MANIFEST_REGISTRY: scripts/playwright-image-search.py
"""

import sys
import asyncio
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from playwright.async_api import async_playwright
import aiohttp
import aiofiles

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from logging_config import setup_logger

# Setup logging
logger = setup_logger(__name__)

class PlaywrightImageSearcher:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.posts_dir = self.base_path / "src" / "posts"
        self.images_dir = self.base_path / "src" / "assets" / "images" / "blog" / "stock"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache for tracking downloaded images
        self.cache_file = self.images_dir / "image_metadata.json"
        self.cache = self.load_cache()
        
        # Keywords mapping for better search results
        self.keyword_mapping = {
            'ai': 'artificial intelligence technology',
            'security': 'cybersecurity data protection',
            'cloud': 'cloud computing servers',
            'docker': 'container technology deployment',
            'kubernetes': 'orchestration cloud infrastructure',
            'python': 'programming code development',
            'javascript': 'web development coding',
            'database': 'data storage servers',
            'api': 'connection integration network',
            'blockchain': 'cryptocurrency digital ledger',
            'quantum': 'quantum computing physics',
            'devops': 'automation deployment pipeline',
            'llm': 'artificial intelligence language',
            'machine-learning': 'data science algorithms',
            'homelab': 'home server technology',
            'network': 'networking infrastructure',
            'vulnerability': 'cybersecurity protection',
            'cryptography': 'encryption security',
            'zero-trust': 'network security authentication'
        }
    
    def load_cache(self) -> Dict:
        """Load existing image metadata cache"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_cache(self):
        """Save image metadata cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_search_query(self, title: str, tags: List[str]) -> str:
        """Generate optimized search query from title and tags"""
        # Check tags for mapped keywords
        for tag in tags:
            tag_lower = tag.lower().replace('-', '')
            if tag_lower in self.keyword_mapping:
                return self.keyword_mapping[tag_lower]
        
        # Check title for keywords
        title_lower = title.lower()
        for keyword, query in self.keyword_mapping.items():
            if keyword.replace('-', ' ') in title_lower or keyword in title_lower:
                return query
        
        # Default to technology theme
        return "technology innovation digital"
    
    async def search_pexels(self, page, query: str) -> Optional[Dict]:
        """Search Pexels for images using Playwright"""
        try:
            logger.info(f"    🔍 Searching Pexels for: {query}")
            
            # Navigate to Pexels search
            search_url = f"https://www.pexels.com/search/{query}/"
            await page.goto(search_url, wait_until='networkidle', timeout=30000)
            
            # Wait for images to load
            await page.wait_for_selector('article[class*="photo-item"]', timeout=10000)
            
            # Get first image data
            first_image = await page.query_selector('article[class*="photo-item"] a img')
            if first_image:
                img_src = await first_image.get_attribute('src')
                img_alt = await first_image.get_attribute('alt')
                
                # Get photographer info if available
                photographer_elem = await page.query_selector('article[class*="photo-item"] a[class*="photographer"]')
                photographer = "Pexels Photographer"
                if photographer_elem:
                    photographer = await photographer_elem.inner_text()
                
                # Get high-res version
                if img_src:
                    # Pexels provides different sizes, get a good quality one
                    img_src = img_src.replace('?auto=compress&cs=tinysrgb&h=130', '?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')
                    
                    return {
                        'url': img_src,
                        'alt': img_alt or query,
                        'photographer': photographer.strip(),
                        'source': 'Pexels',
                        'source_url': search_url,
                        'license': 'Pexels License (Free to use)'
                    }

        except Exception as e:
            logger.warning(f"    Pexels search error: {e}")

        return None
    
    async def search_unsplash(self, page, query: str) -> Optional[Dict]:
        """Search Unsplash for images using Playwright"""
        try:
            logger.info(f"    🔍 Searching Unsplash for: {query}")
            
            # Navigate to Unsplash search
            search_url = f"https://unsplash.com/s/photos/{query}"
            await page.goto(search_url, wait_until='networkidle', timeout=30000)
            
            # Wait for images to load
            await page.wait_for_selector('figure[itemprop="image"]', timeout=10000)
            
            # Get first image data
            first_image = await page.query_selector('figure[itemprop="image"] img')
            if first_image:
                img_src = await first_image.get_attribute('src')
                img_alt = await first_image.get_attribute('alt')
                
                # Get photographer info
                photographer_elem = await page.query_selector('figure[itemprop="image"] a[title*="Photo by"]')
                photographer = "Unsplash Photographer"
                if photographer_elem:
                    title_attr = await photographer_elem.get_attribute('title')
                    if title_attr and 'Photo by' in title_attr:
                        photographer = title_attr.replace('Photo by ', '').split(' on ')[0]
                
                if img_src:
                    # Get higher quality version
                    img_src = img_src.split('?')[0] + '?w=1920&q=80'
                    
                    return {
                        'url': img_src,
                        'alt': img_alt or query,
                        'photographer': photographer.strip(),
                        'source': 'Unsplash',
                        'source_url': search_url,
                        'license': 'Unsplash License (Free to use)'
                    }

        except Exception as e:
            logger.warning(f"    Unsplash search error: {e}")

        return None
    
    async def search_pixabay(self, page, query: str) -> Optional[Dict]:
        """Search Pixabay for images using Playwright"""
        try:
            logger.info(f"    🔍 Searching Pixabay for: {query}")
            
            # Navigate to Pixabay search
            search_url = f"https://pixabay.com/images/search/{query}/"
            await page.goto(search_url, wait_until='networkidle', timeout=30000)
            
            # Wait for images to load
            await page.wait_for_selector('div.results a[href*="/photos/"]', timeout=10000)
            
            # Get first image link
            first_link = await page.query_selector('div.results a[href*="/photos/"]')
            if first_link:
                # Navigate to image page for full res
                await first_link.click()
                await page.wait_for_selector('img#media_container img', timeout=10000)
                
                # Get image data
                img_elem = await page.query_selector('img#media_container img')
                if img_elem:
                    img_src = await img_elem.get_attribute('src')
                    
                    # Get photographer
                    photographer_elem = await page.query_selector('a[href*="/users/"]')
                    photographer = "Pixabay Contributor"
                    if photographer_elem:
                        photographer = await photographer_elem.inner_text()
                    
                    if img_src:
                        return {
                            'url': img_src,
                            'alt': query,
                            'photographer': photographer.strip(),
                            'source': 'Pixabay',
                            'source_url': page.url,
                            'license': 'Pixabay License (Free for commercial use)'
                        }

        except Exception as e:
            logger.warning(f"    Pixabay search error: {e}")

        return None
    
    async def download_image(self, url: str, filename: str) -> bool:
        """Download image from URL asynchronously"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        filepath = self.images_dir / filename
                        
                        async with aiofiles.open(filepath, 'wb') as f:
                            await f.write(content)

                        logger.info(f"    ✅ Downloaded: {filename}")
                        return True
        except Exception as e:
            logger.error(f"    Download failed: {e}")

        return False
    
    async def process_post(self, post_file: Path, browser) -> Optional[Dict]:
        """Process a single blog post to find and download relevant image"""
        # Read post metadata
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        if not content.startswith('---'):
            return None
        
        try:
            _, fm, post_content = content.split('---', 2)
            frontmatter = yaml.safe_load(fm)
        except:
            return None
        
        title = frontmatter.get('title', '')
        tags = frontmatter.get('tags', [])
        
        # Skip if already processed
        cache_key = post_file.stem
        if cache_key in self.cache and self.cache[cache_key].get('downloaded'):
            logger.info(f"  ⏭️ Already processed: {post_file.name}")
            return None

        logger.info(f"\n📝 Processing: {title[:60]}...")
        
        # Generate search query
        search_query = self.get_search_query(title, tags)
        
        # Create new page for searching
        page = await browser.new_page()
        
        # Try different sources
        image_data = None
        for search_func in [self.search_pexels, self.search_unsplash, self.search_pixabay]:
            image_data = await search_func(page, search_query)
            if image_data:
                break
        
        await page.close()

        if not image_data:
            logger.warning(f"  No images found for: {title[:40]}...")
            return None
        
        # Download the image
        filename = f"{cache_key}-hero.jpg"
        downloaded = await self.download_image(image_data['url'], filename)
        
        if downloaded:
            # Create metadata for the post
            metadata = {
                'hero': {
                    'src': f"/assets/images/blog/stock/{filename}",
                    'alt': image_data['alt'],
                    'caption': f"Photo by {image_data['photographer']} on {image_data['source']}",
                    'attribution': {
                        'photographer': image_data['photographer'],
                        'source': image_data['source'],
                        'source_url': image_data['source_url'],
                        'license': image_data['license']
                    }
                },
                'downloaded': True
            }
            
            # Update cache
            self.cache[cache_key] = metadata
            self.save_cache()
            
            # Update the blog post file
            frontmatter['images'] = metadata
            
            # Rebuild file content
            new_content = '---\n'
            new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            new_content += '---'
            new_content += post_content
            
            # Write back to file
            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            logger.info(f"  ✅ Updated: {post_file.name}")
            return metadata

        return None
    
    async def process_all_posts(self):
        """Process all blog posts to add relevant stock images"""
        logger.info("🖼️ Playwright Image Search & Download")
        logger.info("=" * 50)

        posts = sorted(list(self.posts_dir.glob('*.md')))
        logger.info(f"Found {len(posts)} blog posts\n")
        
        async with async_playwright() as p:
            # Use Chromium for better compatibility
            browser = await p.chromium.launch(headless=True)
            
            processed = 0
            for i, post_file in enumerate(posts, 1):
                logger.info(f"\n[{i}/{len(posts)}]")
                result = await self.process_post(post_file, browser)
                if result:
                    processed += 1

                # Small delay to be respectful to the sites
                await asyncio.sleep(2)

            await browser.close()

        logger.info("\n" + "=" * 50)
        logger.info(f"✨ Processing complete!")
        logger.info(f"   Processed: {processed} posts")
        logger.info(f"   Skipped: {len(posts) - processed} posts")

        logger.info("\n📋 Summary:")
        logger.info("• Downloaded relevant hero images from free stock sites")
        logger.info("• Added proper attribution for all images")
        logger.info("• Updated blog post metadata with image information")
        logger.info("• Images saved to /assets/images/blog/stock/")

async def main(quiet=False):
    """Main execution"""
    searcher = PlaywrightImageSearcher()
    await searcher.process_all_posts()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Playwright-based Stock Image Search and Download',
        epilog='''
Examples:
  %(prog)s
  %(prog)s --quiet
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    try:
        if not args.quiet:
            logger.info("🚀 Starting Playwright-based image search...")
            logger.info("This will search and download relevant images from:")
            logger.info("  • Pexels")
            logger.info("  • Unsplash")
            logger.info("  • Pixabay")
            logger.info("\nNo API keys required!\n")

        asyncio.run(main(args.quiet))
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)