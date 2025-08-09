#!/usr/bin/env python3
"""
Add tech-related images to blog posts with proper attribution
Using Unsplash Source API (no key required) for relevant images
"""

from pathlib import Path
import yaml
import re

class TechImageAdder:
    def __init__(self):
        self.base_path = Path(".")
        self.posts_dir = self.base_path / "src" / "posts"
        
        # Map topics to Unsplash image URLs (curated high-quality tech images)
        self.image_mappings = {
            'security': {
                'url': 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=1920&q=80',
                'credit': 'Photo by Franck on Unsplash',
                'alt': 'Digital security concept with code and lock symbols'
            },
            'ai': {
                'url': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1920&q=80',
                'credit': 'Photo by Google DeepMind on Unsplash',
                'alt': 'Artificial intelligence and neural network visualization'
            },
            'cloud': {
                'url': 'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1920&q=80',
                'credit': 'Photo by C Dustin on Unsplash',
                'alt': 'Cloud computing infrastructure and servers'
            },
            'network': {
                'url': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1920&q=80',
                'credit': 'Photo by NASA on Unsplash',
                'alt': 'Network connections and data flow visualization'
            },
            'code': {
                'url': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1920&q=80',
                'credit': 'Photo by Arnold Francisca on Unsplash',
                'alt': 'Code on computer screen'
            },
            'data': {
                'url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1920&q=80',
                'credit': 'Photo by Luke Chesser on Unsplash',
                'alt': 'Data visualization and analytics dashboard'
            },
            'quantum': {
                'url': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1920&q=80',
                'credit': 'Photo by Zac Wolff on Unsplash',
                'alt': 'Quantum computing visualization'
            },
            'blockchain': {
                'url': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=1920&q=80',
                'credit': 'Photo by Shubham Dhage on Unsplash',
                'alt': 'Blockchain network visualization'
            }
        }
    
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
    
    def select_image_for_post(self, title: str, tags: list) -> dict:
        """Select appropriate image based on post content"""
        title_lower = title.lower()
        
        # Check for specific keywords
        if 'security' in title_lower or 'zero trust' in title_lower:
            return self.image_mappings['security']
        elif 'ai' in title_lower or 'llm' in title_lower or 'claude' in title_lower:
            return self.image_mappings['ai']
        elif 'cloud' in title_lower:
            return self.image_mappings['cloud']
        elif 'network' in title_lower or 'dns' in title_lower:
            return self.image_mappings['network']
        elif 'quantum' in title_lower:
            return self.image_mappings['quantum']
        elif 'blockchain' in title_lower:
            return self.image_mappings['blockchain']
        elif 'data' in title_lower or 'analytics' in title_lower:
            return self.image_mappings['data']
        
        # Check tags
        for tag in tags:
            tag_lower = tag.lower()
            if 'security' in tag_lower or 'crypto' in tag_lower:
                return self.image_mappings['security']
            elif 'ai' in tag_lower or 'ml' in tag_lower:
                return self.image_mappings['ai']
            elif 'cloud' in tag_lower:
                return self.image_mappings['cloud']
        
        # Default to code image
        return self.image_mappings['code']
    
    def add_image_to_post(self, post_file: Path):
        """Add an image to a blog post"""
        with open(post_file, 'r') as f:
            content = f.read()
        
        frontmatter, post_content = self.parse_frontmatter(content)
        
        # Skip if already has images
        if 'images' in frontmatter or '![' in post_content:
            print(f"  ⏭️ {post_file.name} already has images")
            return False
        
        title = frontmatter.get('title', '')
        tags = frontmatter.get('tags', [])
        
        # Select appropriate image
        image = self.select_image_for_post(title, tags)
        
        # Add image markdown after the first paragraph
        image_markdown = f"""

![{image['alt']}]({image['url']})
*{image['credit']}*

"""
        
        # Find insertion point (after first paragraph)
        first_para_end = post_content.find('\n\n')
        if first_para_end > 0:
            # Check if there's already a section header right after
            next_content = post_content[first_para_end:first_para_end+5]
            if next_content.strip().startswith('##'):
                # Insert before the section header
                post_content = post_content[:first_para_end] + image_markdown + post_content[first_para_end:]
            else:
                # Insert after the paragraph break
                post_content = post_content[:first_para_end+2] + image_markdown + post_content[first_para_end+2:]
        else:
            # Add at the beginning
            post_content = image_markdown + post_content
        
        # Save updated content
        new_content = '---\n'
        new_content += yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        new_content += '---\n'
        new_content += post_content
        
        with open(post_file, 'w') as f:
            f.write(new_content)
        
        print(f"  ✅ Added image to {post_file.name}")
        return True
    
    def process_key_posts(self):
        """Process key blog posts"""
        print("🖼️ Adding Tech Images to Blog Posts")
        print("=" * 50)
        
        # Key posts to update
        key_posts = [
            '2025-08-07-supercharging-development-claude-flow.md',
            '2024-08-27-zero-trust-security-principles.md',
            '2025-07-15-vulnerability-management-scale-open-source.md',
            '2025-07-01-ebpf-security-monitoring-practical-guide.md',
            '2025-06-25-local-llm-deployment-privacy-first.md',
            '2025-02-10-automating-home-network-security.md',
            '2024-10-10-blockchain-beyond-cryptocurrency.md',
            '2024-08-02-quantum-computing-leap-forward.md',
        ]
        
        updated = 0
        for post_name in key_posts:
            post_file = self.posts_dir / post_name
            if post_file.exists():
                if self.add_image_to_post(post_file):
                    updated += 1
            else:
                print(f"  ⚠️ {post_name} not found")
        
        print(f"\n✨ Added images to {updated} posts")
        print("\nImages are from Unsplash (free to use with attribution)")

def main():
    adder = TechImageAdder()
    adder.process_key_posts()

if __name__ == "__main__":
    main()