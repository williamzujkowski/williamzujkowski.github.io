#!/usr/bin/env python3
"""
Remove Generic Hero Images from Blog Posts
Updates blog posts to remove duplicate hero images and improve content structure
"""

import os
import re
from pathlib import Path
import yaml

class BlogPostOptimizer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.posts_dir = self.base_path / "src" / "posts"
        self.hero_dir = self.base_path / "src" / "assets" / "images" / "blog" / "hero"
    
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
    
    def remove_hero_images(self, post_file: Path) -> bool:
        """Remove hero image references from a blog post"""
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter, post_content = self.parse_frontmatter(content)
            
            # Remove images section from frontmatter
            if 'images' in frontmatter:
                del frontmatter['images']
                
                # Rebuild the file content
                new_content = '---\n'
                new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
                new_content += '---\n'
                new_content += post_content
                
                # Write back to file
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ✅ Removed images from {post_file.name}")
                return True
            else:
                print(f"  ⏭️ No images in {post_file.name}")
                return False
            
        except Exception as e:
            print(f"  ❌ Error processing {post_file.name}: {e}")
            return False
    
    def delete_generic_hero_images(self):
        """Delete the generic hero image files"""
        print("\n🗑️ Removing generic hero image files...")
        
        if self.hero_dir.exists():
            image_files = list(self.hero_dir.glob("*.jpg")) + list(self.hero_dir.glob("*.png"))
            
            for img_file in image_files:
                try:
                    img_file.unlink()
                    print(f"  ✅ Deleted {img_file.name}")
                except Exception as e:
                    print(f"  ❌ Error deleting {img_file.name}: {e}")
            
            # Try to remove the directory if empty
            try:
                self.hero_dir.rmdir()
                print(f"  ✅ Removed empty hero directory")
            except:
                print(f"  ℹ️ Hero directory not empty or in use")
    
    def process_all_posts(self):
        """Process all blog posts to remove hero images"""
        print("🧹 Removing Generic Hero Images from Blog Posts")
        print("=" * 50)
        
        posts = list(self.posts_dir.glob('*.md'))
        print(f"Found {len(posts)} blog posts to process\n")
        
        updated_count = 0
        for post_file in sorted(posts):
            if self.remove_hero_images(post_file):
                updated_count += 1
        
        print("\n" + "=" * 50)
        print(f"✨ Processing complete!")
        print(f"   Updated: {updated_count} posts")
        print(f"   Unchanged: {len(posts) - updated_count} posts")
        
        # Delete the generic image files
        self.delete_generic_hero_images()
        
        print("\n📝 Summary:")
        print("• Removed hero image metadata from all blog posts")
        print("• Deleted generic hero image files")
        print("• Blog posts now load faster without duplicate images")
        print("\n🎯 Next Steps:")
        print("1. Posts will use text-based headers (cleaner, faster)")
        print("2. Add relevant images only where they add value")
        print("3. Focus on content quality over decorative images")

def main():
    """Main execution function"""
    optimizer = BlogPostOptimizer()
    optimizer.process_all_posts()

if __name__ == "__main__":
    main()