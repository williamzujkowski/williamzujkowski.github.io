#!/usr/bin/env python3
"""
SCRIPT: fetch-stock-images.py
PURPOSE: Stock Image Fetcher for Blog Posts
CATEGORY: image_management
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Stock Image Fetcher for Blog Posts. This script is part of the image management
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/fetch-stock-images.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/fetch-stock-images.py

    # With verbose output
    python scripts/fetch-stock-images.py --verbose

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

MANIFEST_REGISTRY: scripts/fetch-stock-images.py
"""

import os
import json
import requests
import time
from pathlib import Path
from urllib.parse import quote, urlparse
import hashlib

class StockImageFetcher:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.images_dir = self.base_path / "src" / "assets" / "images" / "blog" / "stock"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Track downloaded images to avoid duplicates
        self.cache_file = self.images_dir / "image_cache.json"
        self.cache = self.load_cache()
    
    def load_cache(self):
        """Load cache of downloaded images"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_cache(self):
        """Save cache of downloaded images"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_search_terms(self, title: str, tags: list) -> list:
        """Generate search terms from post title and tags"""
        # Map technical terms to visual concepts
        term_mapping = {
            'security': ['cybersecurity', 'data protection', 'lock', 'shield'],
            'ai': ['artificial intelligence', 'robot', 'neural network', 'technology'],
            'cloud': ['cloud computing', 'server', 'data center', 'network'],
            'blockchain': ['cryptocurrency', 'blockchain', 'digital', 'network'],
            'quantum': ['quantum computing', 'quantum', 'physics', 'technology'],
            'devops': ['development', 'automation', 'coding', 'pipeline'],
            'docker': ['container', 'shipping', 'deployment', 'technology'],
            'kubernetes': ['orchestration', 'network', 'cloud', 'containers'],
            'python': ['programming', 'code', 'development', 'technology'],
            'javascript': ['web development', 'coding', 'programming', 'technology'],
            'database': ['data', 'storage', 'server', 'technology'],
            'api': ['connection', 'integration', 'network', 'technology'],
            'llm': ['artificial intelligence', 'language', 'neural network'],
            'machine-learning': ['machine learning', 'data science', 'AI', 'algorithm'],
            'cryptography': ['encryption', 'security', 'lock', 'data protection'],
            'network': ['network', 'connection', 'internet', 'technology'],
            'homelab': ['home server', 'technology', 'computer', 'network'],
            'raspberry-pi': ['raspberry pi', 'electronics', 'computer', 'technology'],
            'zero-trust': ['security', 'authentication', 'network security'],
            'vulnerability': ['security', 'protection', 'shield', 'cybersecurity']
        }
        
        search_terms = []
        
        # Check tags for mapped terms
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower in term_mapping:
                search_terms.extend(term_mapping[tag_lower])
        
        # Check title for keywords
        title_lower = title.lower()
        for key, terms in term_mapping.items():
            if key in title_lower:
                search_terms.extend(terms)
        
        # Remove duplicates and limit
        search_terms = list(dict.fromkeys(search_terms))[:3]
        
        # If no specific terms found, use generic tech terms
        if not search_terms:
            search_terms = ['technology', 'digital', 'innovation']
        
        return search_terms
    
    def search_pexels_no_api(self, query: str, count: int = 1):
        """Search Pexels without API key"""
        results = []
        search_url = f"https://www.pexels.com/search/{quote(query)}/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            # Note: This is a simplified example - in production you'd use proper scraping
            print(f"  🔍 Searching Pexels for: {query}")
            # For now, return placeholder since actual scraping requires more complex handling
            results.append({
                'url': f"https://images.pexels.com/photos/placeholder/{query}.jpg",
                'photographer': 'Pexels Photographer',
                'source': 'Pexels',
                'license': 'Pexels License'
            })
        except Exception as e:
            print(f"  ⚠️ Error searching Pexels: {e}")
        
        return results[:count]
    
    def search_unsplash_no_api(self, query: str, count: int = 1):
        """Search Unsplash without API key"""
        results = []
        search_url = f"https://unsplash.com/s/photos/{quote(query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            print(f"  🔍 Searching Unsplash for: {query}")
            # Placeholder for actual implementation
            results.append({
                'url': f"https://images.unsplash.com/photo-placeholder-{query}",
                'photographer': 'Unsplash Photographer',
                'source': 'Unsplash',
                'license': 'Unsplash License'
            })
        except Exception as e:
            print(f"  ⚠️ Error searching Unsplash: {e}")
        
        return results[:count]
    
    def download_image(self, url: str, filename: str) -> str:
        """Download image from URL"""
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            
            filepath = self.images_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(filepath)
        except Exception as e:
            print(f"  ❌ Error downloading {url}: {e}")
            return None
    
    def process_blog_post(self, post_file: Path) -> dict:
        """Process a single blog post to find and download relevant images"""
        # Read post metadata
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        if content.startswith('---'):
            try:
                import yaml
                _, fm, _ = content.split('---', 2)
                frontmatter = yaml.safe_load(fm)
            except:
                return None
        else:
            return None
        
        title = frontmatter.get('title', '')
        tags = frontmatter.get('tags', [])
        
        # Skip if already has custom images
        if 'images' in frontmatter and 'custom' in frontmatter.get('images', {}):
            print(f"  ⏭️ Skipping {post_file.name} (has custom images)")
            return None
        
        # Generate search terms
        search_terms = self.get_search_terms(title, tags)
        
        print(f"\n📸 Processing: {title}")
        print(f"  🏷️ Tags: {', '.join(tags)}")
        print(f"  🔎 Search terms: {', '.join(search_terms)}")
        
        # Search for images
        images = []
        for term in search_terms[:1]:  # Just use first term for hero image
            # Try Pexels first
            results = self.search_pexels_no_api(term, 1)
            if results:
                images.extend(results)
                break
            
            # Fallback to Unsplash
            results = self.search_unsplash_no_api(term, 1)
            if results:
                images.extend(results)
                break
        
        if not images:
            print(f"  ⚠️ No images found")
            return None
        
        # Use first image as hero
        image = images[0]
        
        # Generate filename
        filename_base = post_file.stem
        filename = f"{filename_base}-stock.jpg"
        
        # Check cache
        cache_key = f"{filename_base}"
        if cache_key in self.cache:
            print(f"  ✅ Using cached image")
            return self.cache[cache_key]
        
        # For now, create metadata without actual download
        # In production, you'd implement proper image download
        image_data = {
            'hero': {
                'src': f"/assets/images/blog/stock/{filename}",
                'alt': f"{title} - Photo from {image['source']}",
                'caption': f"Photo by {image['photographer']} on {image['source']}",
                'attribution': {
                    'photographer': image['photographer'],
                    'source': image['source'],
                    'license': image['license'],
                    'url': image['url']
                }
            }
        }
        
        # Cache the result
        self.cache[cache_key] = image_data
        self.save_cache()
        
        print(f"  ✅ Image metadata created")
        
        return image_data

def main():
    """Main execution"""
    print("🖼️ Stock Image Fetcher for Blog Posts")
    print("=" * 50)
    print("\n⚠️ NOTE: This is a demonstration script.")
    print("For production use, you should:")
    print("1. Register for free API keys from Pexels/Unsplash")
    print("2. Use their official APIs for better reliability")
    print("3. Implement proper rate limiting and error handling")
    print("\nAlternatively, use Playwright for automated browser-based search.")
    print("\n" + "=" * 50)
    
    fetcher = StockImageFetcher()
    posts_dir = Path("src/posts")
    
    # Process a few posts as examples
    posts = list(posts_dir.glob("*.md"))[:5]  # Just process first 5 as demo
    
    for post_file in posts:
        result = fetcher.process_blog_post(post_file)
        if result:
            print(f"  📁 Would update: {post_file.name}")
    
    print("\n" + "=" * 50)
    print("✨ Image search complete!")
    print("\n🎯 Next Steps:")
    print("1. Register for API keys at:")
    print("   - Pexels: https://www.pexels.com/api/")
    print("   - Unsplash: https://unsplash.com/developers")
    print("2. Update this script with your API keys")
    print("3. Run the full image download process")
    print("\nOR")
    print("\n1. Use the Playwright-based image searcher (no API keys needed)")
    print("2. Run: python scripts/playwright-image-search.py")

if __name__ == "__main__":
    main()