#!/usr/bin/env -S uv run python3
"""
SCRIPT: generate-blog-hero-images.py
PURPOSE: Generate Hero Images for Blog Posts
CATEGORY: blog_management
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Generate Hero Images for Blog Posts. This script is part of the blog management
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/generate-blog-hero-images.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/generate-blog-hero-images.py

    # With verbose output
    python scripts/generate-blog-hero-images.py --verbose

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

MANIFEST_REGISTRY: scripts/generate-blog-hero-images.py
"""

import os
import re
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import colorsys
import hashlib

class HeroImageGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.posts_dir = self.base_path / "src" / "posts"
        self.hero_dir = self.base_path / "src" / "assets" / "images" / "blog" / "hero"
        self.hero_dir.mkdir(parents=True, exist_ok=True)
        
        # Color schemes for different topics
        self.color_schemes = {
            'security': ['#1e3a8a', '#dc2626', '#0f172a'],  # Blue to red (security/warning)
            'ai': ['#7c3aed', '#ec4899', '#1e1b4b'],  # Purple to pink (AI/ML)
            'cloud': ['#0ea5e9', '#10b981', '#0c4a6e'],  # Sky blue to teal (cloud)
            'blockchain': ['#f59e0b', '#10b981', '#78350f'],  # Amber to emerald (blockchain)
            'quantum': ['#8b5cf6', '#3b82f6', '#1e1b4b'],  # Violet to blue (quantum)
            'devops': ['#10b981', '#3b82f6', '#064e3b'],  # Green to blue (DevOps)
            'network': ['#06b6d4', '#6366f1', '#083344'],  # Cyan to indigo (network)
            'database': ['#f97316', '#eab308', '#7c2d12'],  # Orange to yellow (data)
            'python': ['#3776ab', '#ffd343', '#1e3a5f'],  # Python blue and yellow
            'javascript': ['#f7df1e', '#323330', '#000000'],  # JavaScript yellow
            'default': ['#3b82f6', '#10b981', '#1e3a8a']  # Blue to green (default)
        }
        
        # Pattern overlays for visual interest
        self.patterns = {
            'dots': self.create_dots_pattern,
            'lines': self.create_lines_pattern,
            'grid': self.create_grid_pattern,
            'circuit': self.create_circuit_pattern,
            'waves': self.create_waves_pattern
        }
    
    def get_color_scheme(self, title: str, tags: list) -> tuple:
        """Determine color scheme based on post content"""
        combined_text = f"{title} {' '.join(tags)}".lower()
        
        # Check for keywords to determine color scheme
        for keyword, colors in self.color_schemes.items():
            if keyword in combined_text:
                return colors
        
        # Use hash of title for consistent but varied colors
        title_hash = hashlib.md5(title.encode()).hexdigest()
        scheme_keys = list(self.color_schemes.keys())
        selected = scheme_keys[int(title_hash[:2], 16) % len(scheme_keys)]
        return self.color_schemes[selected]
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient(self, size: tuple, colors: list) -> Image:
        """Create a gradient background"""
        width, height = size
        img = Image.new('RGB', size)
        draw = ImageDraw.Draw(img)
        
        # Convert hex colors to RGB
        rgb_colors = [self.hex_to_rgb(c) for c in colors[:2]]
        
        # Create gradient
        for y in range(height):
            # Calculate interpolation factor
            factor = y / height
            
            # Interpolate between colors
            r = int(rgb_colors[0][0] * (1 - factor) + rgb_colors[1][0] * factor)
            g = int(rgb_colors[0][1] * (1 - factor) + rgb_colors[1][1] * factor)
            b = int(rgb_colors[0][2] * (1 - factor) + rgb_colors[1][2] * factor)
            
            draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
        
        return img
    
    def create_dots_pattern(self, img: Image, color: tuple, opacity: int = 30) -> Image:
        """Add dots pattern overlay"""
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        dot_size = 4
        spacing = 30
        
        for x in range(0, img.width, spacing):
            for y in range(0, img.height, spacing):
                draw.ellipse(
                    [(x, y), (x + dot_size, y + dot_size)],
                    fill=(*color, opacity)
                )
        
        # Composite the overlay onto the image
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        return img.convert('RGB')
    
    def create_lines_pattern(self, img: Image, color: tuple, opacity: int = 20) -> Image:
        """Add diagonal lines pattern"""
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        spacing = 40
        for i in range(-img.height, img.width + img.height, spacing):
            draw.line(
                [(i, 0), (i + img.height, img.height)],
                fill=(*color, opacity),
                width=2
            )
        
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        return img.convert('RGB')
    
    def create_grid_pattern(self, img: Image, color: tuple, opacity: int = 20) -> Image:
        """Add grid pattern overlay"""
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        spacing = 50
        # Vertical lines
        for x in range(0, img.width, spacing):
            draw.line([(x, 0), (x, img.height)], fill=(*color, opacity), width=1)
        # Horizontal lines
        for y in range(0, img.height, spacing):
            draw.line([(0, y), (img.width, y)], fill=(*color, opacity), width=1)
        
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        return img.convert('RGB')
    
    def create_circuit_pattern(self, img: Image, color: tuple, opacity: int = 25) -> Image:
        """Add circuit board pattern"""
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Draw circuit-like paths
        import random
        random.seed(42)  # Consistent pattern
        
        for _ in range(20):
            x = random.randint(0, img.width)
            y = random.randint(0, img.height)
            
            # Draw a circuit path
            for _ in range(random.randint(3, 8)):
                next_x = x + random.choice([-50, 0, 50])
                next_y = y + random.choice([-50, 0, 50])
                
                if 0 <= next_x < img.width and 0 <= next_y < img.height:
                    draw.line([(x, y), (next_x, next_y)], fill=(*color, opacity), width=2)
                    # Add connection point
                    draw.ellipse(
                        [(next_x - 3, next_y - 3), (next_x + 3, next_y + 3)],
                        fill=(*color, opacity + 10)
                    )
                    x, y = next_x, next_y
        
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        return img.convert('RGB')
    
    def create_waves_pattern(self, img: Image, color: tuple, opacity: int = 20) -> Image:
        """Add wave pattern overlay"""
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        import math
        amplitude = 20
        frequency = 0.02
        
        for y in range(0, img.height, 30):
            points = []
            for x in range(img.width + 1):
                wave_y = y + amplitude * math.sin(x * frequency)
                points.append((x, wave_y))
            
            if len(points) > 1:
                draw.line(points, fill=(*color, opacity), width=2)
        
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        return img.convert('RGB')
    
    def wrap_text(self, text: str, max_width: int = 40) -> list:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def create_hero_image(self, title: str, date: str, tags: list, output_path: Path):
        """Generate a hero image for a blog post"""
        # Image dimensions
        width, height = 1200, 630
        
        # Get color scheme
        colors = self.get_color_scheme(title, tags)
        
        # Create gradient background
        img = self.create_gradient((width, height), colors)
        
        # Add pattern overlay based on content
        pattern_type = 'grid'  # Default pattern
        if any(tag in ['ai', 'machine-learning', 'llm'] for tag in tags):
            pattern_type = 'circuit'
        elif any(tag in ['cloud', 'devops'] for tag in tags):
            pattern_type = 'dots'
        elif any(tag in ['security', 'cybersecurity'] for tag in tags):
            pattern_type = 'lines'
        elif any(tag in ['network', 'infrastructure'] for tag in tags):
            pattern_type = 'waves'
        
        pattern_color = self.hex_to_rgb('#ffffff')
        img = self.patterns[pattern_type](img, pattern_color)
        
        # Add semi-transparent overlay for text readability
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Create text background area
        text_bg_height = 400
        text_bg_top = (height - text_bg_height) // 2
        draw.rectangle(
            [(100, text_bg_top), (width - 100, text_bg_top + text_bg_height)],
            fill=(0, 0, 0, 180)
        )
        
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        # Add text
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default if not available
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            date_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            tag_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            date_font = ImageFont.load_default()
            tag_font = ImageFont.load_default()
        
        # Wrap and draw title
        title_lines = self.wrap_text(title, max_width=35)
        y_offset = text_bg_top + 80
        
        for line in title_lines[:3]:  # Max 3 lines
            # Get text bbox for centering
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x_pos = (width - text_width) // 2
            
            draw.text(
                (x_pos, y_offset),
                line,
                fill=(255, 255, 255),
                font=title_font
            )
            y_offset += 60
        
        # Draw date
        y_offset += 30
        bbox = draw.textbbox((0, 0), date, font=date_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (width - text_width) // 2
        
        draw.text(
            (x_pos, y_offset),
            date,
            fill=(200, 200, 200),
            font=date_font
        )
        
        # Draw tags
        if tags:
            y_offset += 50
            tags_text = ' • '.join(tags[:5])  # Max 5 tags
            bbox = draw.textbbox((0, 0), tags_text, font=tag_font)
            text_width = bbox[2] - bbox[0]
            x_pos = (width - text_width) // 2
            
            draw.text(
                (x_pos, y_offset),
                tags_text,
                fill=(150, 200, 255),
                font=tag_font
            )
        
        # Add site branding
        branding = "williamzujkowski.github.io"
        bbox = draw.textbbox((0, 0), branding, font=tag_font)
        text_width = bbox[2] - bbox[0]
        draw.text(
            (width - text_width - 50, height - 50),
            branding,
            fill=(200, 200, 200),
            font=tag_font
        )
        
        # Save the image
        img.save(output_path, 'JPEG', quality=85, optimize=True)
        
        # Also create OG image variant (same for now)
        og_path = output_path.parent / output_path.name.replace('-hero.jpg', '-og.jpg')
        img.save(og_path, 'JPEG', quality=85, optimize=True)
    
    def process_all_posts(self):
        """Generate hero images for all blog posts"""
        print("🎨 Generating Hero Images for Blog Posts")
        print("=" * 50)
        
        # Load the blog image index
        index_path = self.base_path / "docs" / "blog-image-index.json"
        if index_path.exists():
            with open(index_path, 'r') as f:
                index = json.load(f)
        else:
            print("❌ Blog image index not found. Run update-blog-images.py first.")
            return
        
        generated_count = 0
        skipped_count = 0
        
        for post_file in sorted(self.posts_dir.glob('*.md')):
            # Parse post metadata
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            if content.startswith('---'):
                try:
                    _, fm, _ = content.split('---', 2)
                    import yaml
                    frontmatter = yaml.safe_load(fm)
                    
                    title = frontmatter.get('title', '')
                    date = str(frontmatter.get('date', ''))
                    tags = frontmatter.get('tags', [])
                    
                    # Generate output filename
                    filename = post_file.stem
                    hero_path = self.hero_dir / f"{filename}-hero.jpg"
                    
                    # Skip if already exists
                    if hero_path.exists():
                        print(f"  ⏭️  Skipping {filename} (already exists)")
                        skipped_count += 1
                        continue
                    
                    # Generate the image
                    self.create_hero_image(title, date, tags, hero_path)
                    print(f"  ✅ Generated {hero_path.name}")
                    generated_count += 1
                    
                except Exception as e:
                    print(f"  ❌ Error processing {post_file.name}: {e}")
        
        print("\n" + "=" * 50)
        print(f"✨ Hero image generation complete!")
        print(f"   Generated: {generated_count} images")
        print(f"   Skipped: {skipped_count} images")
        print(f"\n📁 Images saved to: {self.hero_dir}")

def main():
    """Main execution function"""
    # Check for required library
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow library not installed.")
        print("   Run: pip install Pillow")
        return
    
    generator = HeroImageGenerator()
    generator.process_all_posts()
    
    print("\n🎯 Next Steps:")
    print("1. Review generated images in src/assets/images/blog/hero/")
    print("2. Replace with custom images where desired")
    print("3. Optimize images for web delivery")
    print("4. Test responsive loading")

if __name__ == "__main__":
    main()