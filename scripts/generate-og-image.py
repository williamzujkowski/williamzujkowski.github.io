#!/usr/bin/env python3
"""
Generate Open Graph images for social sharing
Creates 1200x630px images with title and site branding
"""

from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def create_og_image(title, output_path, subtitle=None):
    """Create an Open Graph image with the given title"""
    
    # Image dimensions (Facebook/Twitter recommended)
    width = 1200
    height = 630
    
    # Colors (matching site theme)
    bg_color = "#1a202c"  # Dark background
    primary_color = "#3b82f6"  # Blue accent
    text_color = "#f7fafc"  # Light text
    subtitle_color = "#cbd5e0"  # Muted text
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect
    for i in range(height):
        gradient_color = int(26 + (i/height) * 10)  # Subtle gradient
        draw.line([(0, i), (width, i)], fill=(gradient_color, 32, 44))
    
    # Add accent bar at top
    draw.rectangle([(0, 0), (width, 10)], fill=primary_color)
    
    # Try to load fonts (fallback to default if not found)
    try:
        # You may need to adjust font paths for your system
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()
    
    # Wrap title text
    wrapped_title = textwrap.fill(title, width=30)
    lines = wrapped_title.split('\n')
    
    # Calculate text position (centered)
    y_offset = (height - len(lines) * 70) // 2 - 50
    
    # Draw title
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset), line, font=title_font, fill=text_color)
        y_offset += 70
    
    # Draw subtitle if provided
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset + 20), subtitle, font=subtitle_font, fill=subtitle_color)
    
    # Add site branding at bottom
    brand_text = "williamzujkowski.github.io"
    bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, height - 60), brand_text, font=brand_font, fill=subtitle_color)
    
    # Add decorative elements
    # Left bracket
    draw.line([(100, 200), (100, 430)], fill=primary_color, width=4)
    draw.line([(100, 200), (150, 200)], fill=primary_color, width=4)
    draw.line([(100, 430), (150, 430)], fill=primary_color, width=4)
    
    # Right bracket
    draw.line([(width-100, 200), (width-100, 430)], fill=primary_color, width=4)
    draw.line([(width-100, 200), (width-150, 200)], fill=primary_color, width=4)
    draw.line([(width-100, 430), (width-150, 430)], fill=primary_color, width=4)
    
    # Save image
    img.save(output_path, 'PNG', optimize=True)
    print(f"Created: {output_path}")

def main():
    """Generate OG images for the site"""
    
    # Create output directory
    output_dir = "src/assets/images/og"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate default OG image
    create_og_image(
        "William Zujkowski",
        os.path.join(output_dir, "default-og.png"),
        "Security Engineer • Homelab Enthusiast • Lifelong Learner"
    )
    
    # Generate images for main pages
    pages = {
        "about-og.png": ("About Me", "Dad, Security Engineer, Technology Enthusiast"),
        "projects-og.png": ("Projects & Portfolio", "Security Tools and Personal Experiments"),
        "experience-og.png": ("Experience Timeline", "15+ Years in IT and Security"),
        "skills-og.png": ("Skills & Expertise", "From Infrastructure to AI/ML Security"),
        "contact-og.png": ("Let's Connect", "Get in Touch About Security and Technology"),
        "uses-og.png": ("My Setup", "Tools and Tech Stack"),
        "blog-og.png": ("Blog", "Security, Homelab, and Technical Writing")
    }
    
    for filename, (title, subtitle) in pages.items():
        create_og_image(title, os.path.join(output_dir, filename), subtitle)
    
    print(f"\nGenerated {len(pages) + 1} Open Graph images in {output_dir}")
    print("\nTo use these images, add to your page frontmatter:")
    print('image: "/assets/images/og/your-image.png"')

if __name__ == "__main__":
    main()