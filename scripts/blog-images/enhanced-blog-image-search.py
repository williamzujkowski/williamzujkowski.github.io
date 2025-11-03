#!/usr/bin/env -S uv run python3
"""
SCRIPT: enhanced-blog-image-search.py
PURPOSE: Enhanced Blog Image Search Tool
CATEGORY: blog_images
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Enhanced Blog Image Search Tool. This script is part of the blog_images
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/enhanced-blog-image-search.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/enhanced-blog-image-search.py

    # With verbose output
    python scripts/enhanced-blog-image-search.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in blog_management category]

MANIFEST_REGISTRY: scripts/enhanced-blog-image-search.py
"""

import os
import sys
import json
import time
import hashlib
import requests
import argparse
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
import frontmatter
from datetime import datetime
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from logging_config import setup_logger

# Setup logging
logger = setup_logger(__name__)

# Optional imports for image processing
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    logger.warning("PIL not installed. Install with: pip install Pillow")

class BlogImageSearcher:
    def __init__(self, posts_dir: str = "src/posts", images_dir: str = "src/assets/images/blog"):
        self.posts_dir = Path(posts_dir)
        self.images_dir = Path(images_dir)
        self.downloaded_hashes = set()  # Track unique images
        self.tag_to_search_terms = {
            # Security tags
            "security": ["cybersecurity dashboard", "network security", "digital protection"],
            "cryptography": ["encryption visualization", "cryptographic algorithms", "secure communication"],
            "zero-trust": ["zero trust architecture", "network segmentation", "identity verification"],
            "vulnerability": ["vulnerability scanning", "security assessment", "penetration testing"],
            
            # AI/ML tags
            "ai": ["artificial intelligence", "machine learning", "neural networks"],
            "llm": ["large language models", "transformer architecture", "natural language processing"],
            "machine-learning": ["deep learning", "data science", "model training"],
            "multimodal": ["multimodal AI", "computer vision", "audio processing"],
            
            # Cloud/DevOps tags
            "cloud": ["cloud computing", "cloud infrastructure", "kubernetes"],
            "devops": ["CI/CD pipeline", "automation workflow", "deployment"],
            "containers": ["docker containers", "containerization", "microservices"],
            
            # Quantum tags
            "quantum": ["quantum computing", "quantum circuits", "qubits visualization"],
            "quantum-computing": ["quantum processor", "quantum algorithms", "quantum gates"],
            
            # Blockchain tags
            "blockchain": ["blockchain network", "distributed ledger", "cryptocurrency"],
            "smart-contracts": ["smart contract", "ethereum", "defi"],
            
            # Hardware/IoT tags
            "raspberry-pi": ["raspberry pi projects", "IoT devices", "embedded systems"],
            "edge-computing": ["edge devices", "IoT edge", "distributed computing"],
            "homelab": ["home laboratory", "server rack", "network setup"],
            
            # Development tags
            "python": ["python programming", "code editor python", "python development"],
            "javascript": ["javascript code", "web development", "nodejs"],
            "open-source": ["open source community", "github", "collaboration"],
            
            # Generic tech tags
            "tutorial": ["tech tutorial", "learning", "education technology"],
            "architecture": ["system architecture", "software design", "technical diagram"],
            "performance": ["performance monitoring", "optimization", "metrics dashboard"],
        }
        
        # Track which images are used where to ensure uniqueness
        self.image_usage = {}  # image_hash -> list of posts using it
        
    def get_post_metadata(self, post_path: Path) -> Dict:
        """Extract metadata from a blog post."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            return {
                'title': post.metadata.get('title', ''),
                'tags': post.metadata.get('tags', []),
                'date': post.metadata.get('date', ''),
                'description': post.metadata.get('description', ''),
                'slug': post_path.stem,
                'content_preview': post.content[:500] if post.content else ''
            }
    
    def generate_search_queries(self, metadata: Dict) -> List[str]:
        """Generate unique search queries based on post metadata."""
        queries = []
        tags = metadata.get('tags', [])
        title = metadata.get('title', '')
        
        # Add tag-based queries
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower in self.tag_to_search_terms:
                queries.extend(self.tag_to_search_terms[tag_lower])
            else:
                # Generic search for unknown tags
                queries.append(f"{tag} technology")
        
        # Add title-based query (extract key concepts)
        if title:
            # Remove common words and create search query
            important_words = [w for w in title.split() if len(w) > 4 and w.lower() not in 
                             ['with', 'from', 'using', 'guide', 'introduction', 'understanding']]
            if important_words:
                queries.append(' '.join(important_words[:3]))
        
        # Add content-based queries
        content = metadata.get('content_preview', '')
        if 'docker' in content.lower():
            queries.append("docker containers visualization")
        if 'kubernetes' in content.lower() or 'k8s' in content.lower():
            queries.append("kubernetes architecture")
        if 'terraform' in content.lower():
            queries.append("infrastructure as code")
        
        # Ensure uniqueness and limit queries
        seen = set()
        unique_queries = []
        for q in queries:
            if q.lower() not in seen:
                seen.add(q.lower())
                unique_queries.append(q)
        
        return unique_queries[:5]  # Limit to 5 queries per post
    
    def calculate_image_hash(self, image_data: bytes) -> str:
        """Calculate hash of image data to detect duplicates."""
        return hashlib.sha256(image_data).hexdigest()
    
    def is_image_unique(self, image_hash: str, current_post: str) -> bool:
        """Check if image is unique across all posts."""
        if image_hash in self.image_usage:
            # Image already used, check if it's for a different post
            return current_post not in self.image_usage[image_hash]
        return True
    
    def download_image(self, url: str, save_path: Path, post_slug: str) -> bool:
        """Download image and ensure it's unique."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                image_hash = self.calculate_image_hash(response.content)
                
                # Check if image is unique
                if not self.is_image_unique(image_hash, post_slug):
                    logger.info(f"  Skipping duplicate image for {post_slug}")
                    return False
                
                # Save image
                save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                # Track usage
                if image_hash not in self.image_usage:
                    self.image_usage[image_hash] = []
                self.image_usage[image_hash].append(post_slug)
                
                # Optimize if PIL available
                if HAS_PIL:
                    self.optimize_image(save_path)
                
                return True
        except Exception as e:
            logger.error(f"  Error downloading image: {e}")
            return False
    
    def optimize_image(self, image_path: Path):
        """Optimize image size and quality."""
        try:
            img = Image.open(image_path)
            
            # Convert RGBA to RGB if needed
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                img = rgb_img
            
            # Resize if too large
            max_width = 1200
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save optimized
            img.save(image_path, quality=85, optimize=True)
        except Exception as e:
            logger.warning(f"  Could not optimize image: {e}")
    
    def create_search_report(self) -> Dict:
        """Create a report of search activities and results."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'posts_processed': 0,
            'images_downloaded': 0,
            'unique_images': len(self.image_usage),
            'posts_with_images': [],
            'posts_without_images': [],
            'tag_coverage': {}
        }
        
        # Analyze coverage
        for post_file in sorted(self.posts_dir.glob("*.md")):
            metadata = self.get_post_metadata(post_file)
            slug = metadata['slug']
            
            # Check if post has images
            hero_path = self.images_dir / 'hero' / f"{slug}-hero.jpg"
            if hero_path.exists():
                report['posts_with_images'].append(slug)
            else:
                report['posts_without_images'].append(slug)
            
            # Track tag coverage
            for tag in metadata.get('tags', []):
                if tag not in report['tag_coverage']:
                    report['tag_coverage'][tag] = 0
                report['tag_coverage'][tag] += 1
        
        report['posts_processed'] = len(list(self.posts_dir.glob("*.md")))
        return report
    
    def process_all_posts(self, limit: Optional[int] = None):
        """Process all blog posts and search for images."""
        posts = sorted(self.posts_dir.glob("*.md"))
        if limit:
            posts = posts[:limit]

        logger.info(f"Processing {len(posts)} blog posts...")

        for i, post_file in enumerate(posts, 1):
            logger.info(f"\n[{i}/{len(posts)}] Processing: {post_file.name}")
            metadata = self.get_post_metadata(post_file)

            # Generate search queries
            queries = self.generate_search_queries(metadata)
            logger.info(f"  Generated {len(queries)} search queries")

            # Create image paths
            slug = metadata['slug']
            hero_dir = self.images_dir / 'hero'
            inline_dir = self.images_dir / 'inline'

            hero_dir.mkdir(parents=True, exist_ok=True)
            inline_dir.mkdir(parents=True, exist_ok=True)

            # Note: Actual image search would require Playwright integration
            # This is a placeholder for the search logic
            logger.info(f"  Search queries: {', '.join(queries[:2])}")

            # Generate placeholder metadata for now
            self.update_post_frontmatter(post_file, metadata)
    
    def update_post_frontmatter(self, post_path: Path, metadata: Dict):
        """Update post frontmatter with image metadata."""
        with open(post_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Check if images section exists
        if 'images' not in post.metadata:
            slug = metadata['slug']
            post.metadata['images'] = {
                'hero': {
                    'src': f"/assets/images/blog/hero/{slug}-hero.jpg",
                    'alt': f"{metadata.get('title', '')} - Hero Image",
                    'caption': f"Visual representation of {metadata.get('title', '')}",
                    'width': 1200,
                    'height': 630
                },
                'og': {
                    'src': f"/assets/images/blog/hero/{slug}-og.jpg",
                    'alt': f"{metadata.get('title', '')} - Social Media Preview"
                }
            }
            
            # Save updated post
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            logger.info(f"  Updated frontmatter for {post_path.name}")

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced blog image search tool',
        epilog='''
Examples:
  %(prog)s --report
  %(prog)s --limit 5
  %(prog)s --posts-dir src/posts --quiet
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--posts-dir', default='src/posts', help='Directory containing blog posts')
    parser.add_argument('--images-dir', default='src/assets/images/blog', help='Directory for images')
    parser.add_argument('--limit', type=int, help='Limit number of posts to process')
    parser.add_argument('--report', action='store_true', help='Generate coverage report')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress progress messages')

    args = parser.parse_args()
    
    try:
        searcher = BlogImageSearcher(args.posts_dir, args.images_dir)

        if args.report:
            report = searcher.create_search_report()
            if not args.quiet:
                logger.info("\n=== Blog Image Coverage Report ===")
                logger.info(f"Posts processed: {report['posts_processed']}")
                logger.info(f"Posts with images: {len(report['posts_with_images'])}")
                logger.info(f"Posts without images: {len(report['posts_without_images'])}")
                logger.info(f"Unique images: {report['unique_images']}")
                logger.info("\nTag coverage:")
                for tag, count in sorted(report['tag_coverage'].items(), key=lambda x: x[1], reverse=True):
                    logger.info(f"  {tag}: {count} posts")
        else:
            searcher.process_all_posts(limit=args.limit)
            if not args.quiet:
                logger.info("\nImage search preparation complete!")
                logger.info("Note: This script prepares metadata. Use playwright-image-search.py for actual downloads.")

        sys.exit(0)
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error(f"Expected: {args.posts_dir}")
        logger.error(f"Current directory: {os.getcwd()}")
        logger.error("Tip: Run from repository root")
        sys.exit(2)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()