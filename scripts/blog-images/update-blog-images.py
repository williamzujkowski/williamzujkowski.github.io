#!/usr/bin/env -S uv run python3
"""
SCRIPT: update-blog-images.py
PURPOSE: Blog Image Standards Implementation Script
CATEGORY: blog_management
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Blog Image Standards Implementation Script. This script is part of the blog management
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/update-blog-images.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/update-blog-images.py

    # With verbose output
    python scripts/update-blog-images.py --verbose

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

MANIFEST_REGISTRY: scripts/update-blog-images.py
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import yaml

class BlogImageManager:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.posts_dir = self.base_path / "src" / "posts"
        self.images_dir = self.base_path / "src" / "assets" / "images" / "blog"
        
        # Ensure image directories exist
        for subdir in ["hero", "inline", "diagrams", "infographics", "thumbnails"]:
            (self.images_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """Parse frontmatter and content from markdown file"""
        if content.startswith('---'):
            try:
                _, fm, content = content.split('---', 2)
                frontmatter = yaml.safe_load(fm)
                return frontmatter, content.lstrip()
            except:
                return {}, content
        return {}, content
    
    def generate_image_metadata(self, post_file: Path) -> Dict:
        """Generate image metadata for a blog post"""
        # Extract date and slug from filename
        filename = post_file.stem
        match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)', filename)
        if not match:
            return {}
        
        date_str, slug = match.groups()
        
        # Generate image paths
        hero_path = f"/assets/images/blog/hero/{filename}-hero.jpg"
        og_path = f"/assets/images/blog/hero/{filename}-og.jpg"
        
        # Read post content to generate contextual alt text
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()
            frontmatter, _ = self.parse_frontmatter(content)
        
        title = frontmatter.get('title', slug.replace('-', ' ').title())
        description = frontmatter.get('description', '')
        
        # Generate contextual alt text
        alt_text = self.generate_alt_text(title, description)
        
        return {
            'hero': {
                'src': hero_path,
                'alt': alt_text,
                'caption': f"Visual representation of {title}",
                'width': 1200,
                'height': 630
            },
            'og': {
                'src': og_path,
                'alt': alt_text
            }
        }
    
    def generate_alt_text(self, title: str, description: str) -> str:
        """Generate appropriate alt text based on post content"""
        # Map common keywords to descriptive phrases
        keyword_mappings = {
            'claude-flow': 'AI swarm orchestration visualization',
            'security': 'cybersecurity concept illustration',
            'cloud': 'cloud computing architecture diagram',
            'api': 'API architecture and endpoints visualization',
            'quantum': 'quantum computing concept illustration',
            'blockchain': 'blockchain network visualization',
            'ai': 'artificial intelligence concept diagram',
            'llm': 'large language model architecture',
            'docker': 'containerization workflow diagram',
            'kubernetes': 'container orchestration visualization',
            'python': 'Python code and development workflow',
            'javascript': 'JavaScript development visualization',
            'react': 'React component architecture diagram',
            'database': 'database schema and relationships',
            'network': 'network topology and connections',
            'encryption': 'encryption and security visualization',
            'devops': 'DevOps pipeline and workflow diagram',
            'testing': 'software testing methodology visualization',
            'performance': 'performance metrics and optimization graph',
            'architecture': 'system architecture diagram'
        }
        
        # Check for keywords in title and description
        combined_text = f"{title} {description}".lower()
        
        for keyword, alt_phrase in keyword_mappings.items():
            if keyword in combined_text:
                return f"{alt_phrase} for {title}"
        
        # Default alt text
        return f"Hero image illustrating {title}"
    
    def update_post_frontmatter(self, post_file: Path) -> bool:
        """Update a blog post's frontmatter with image metadata"""
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, post_content = self.parse_frontmatter(content)
            
            # Skip if images already defined
            if 'images' in frontmatter:
                print(f"  ⏭️  Skipping {post_file.name} (images already defined)")
                return False
            
            # Generate image metadata
            image_metadata = self.generate_image_metadata(post_file)
            
            if image_metadata:
                frontmatter['images'] = image_metadata
                
                # Rebuild the file content
                new_content = '---\n'
                new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
                new_content += '---\n'
                new_content += post_content
                
                # Write back to file
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ✅ Updated {post_file.name}")
                return True
            
        except Exception as e:
            print(f"  ❌ Error processing {post_file.name}: {e}")
        
        return False
    
    def generate_image_index(self) -> Dict:
        """Generate an index of all blog images"""
        index = {
            'posts': {},
            'stats': {
                'total_posts': 0,
                'posts_with_images': 0,
                'total_images': 0
            }
        }
        
        for post_file in sorted(self.posts_dir.glob('*.md')):
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
                frontmatter, _ = self.parse_frontmatter(content)
            
            index['stats']['total_posts'] += 1
            
            if 'images' in frontmatter:
                index['stats']['posts_with_images'] += 1
                index['posts'][post_file.stem] = frontmatter['images']
                
                # Count images
                if 'hero' in frontmatter['images']:
                    index['stats']['total_images'] += 1
                if 'inline' in frontmatter.get('images', {}):
                    index['stats']['total_images'] += len(frontmatter['images']['inline'])
        
        return index
    
    def process_all_posts(self):
        """Process all blog posts and update their image metadata"""
        print("🖼️  Blog Image Standards Implementation")
        print("=" * 50)
        
        posts = list(self.posts_dir.glob('*.md'))
        print(f"Found {len(posts)} blog posts to process\n")
        
        updated_count = 0
        for post_file in sorted(posts):
            if self.update_post_frontmatter(post_file):
                updated_count += 1
        
        print("\n" + "=" * 50)
        print(f"✨ Processing complete!")
        print(f"   Updated: {updated_count} posts")
        print(f"   Skipped: {len(posts) - updated_count} posts")
        
        # Generate and save index
        index = self.generate_image_index()
        index_path = self.base_path / "docs" / "blog-image-index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        print(f"\n📊 Image Statistics:")
        print(f"   Total posts: {index['stats']['total_posts']}")
        print(f"   Posts with images: {index['stats']['posts_with_images']}")
        print(f"   Total images referenced: {index['stats']['total_images']}")
        print(f"\n📁 Image index saved to: {index_path}")

def main():
    """Main execution function"""
    manager = BlogImageManager()
    manager.process_all_posts()
    
    print("\n🎯 Next Steps:")
    print("1. Generate actual hero images for each post")
    print("2. Optimize images using the provided bash scripts")
    print("3. Create WebP alternatives for better performance")
    print("4. Test responsive image loading")
    print("5. Verify accessibility with screen readers")

if __name__ == "__main__":
    main()