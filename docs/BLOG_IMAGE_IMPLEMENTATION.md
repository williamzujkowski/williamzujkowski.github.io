# Blog Image Standards Implementation

## Directory Structure

All blog images are organized in a well-structured hierarchy:

```
src/assets/images/blog/
├── hero/               # Hero images for post headers (1200x630px)
├── inline/             # Inline content images (800px wide)
├── diagrams/           # Technical diagrams and architecture visuals
├── infographics/       # Data visualizations and infographics
└── thumbnails/         # Small preview images (400x300px)
```

## Image Naming Convention

All images follow a consistent naming pattern:
- Format: `YYYY-MM-DD-post-slug-image-type.ext`
- Example: `2025-08-07-claude-flow-architecture-diagram.png`

## Image Requirements

### Hero Images
- **Dimensions:** 1200x630px (16:9 ratio for social sharing)
- **Format:** JPEG for photos, PNG for graphics
- **Max file size:** 200KB (optimized)
- **Purpose:** Post header and og:image for social media

### Inline Images
- **Dimensions:** 800px wide (height variable)
- **Format:** JPEG/PNG/WebP
- **Max file size:** 150KB
- **Purpose:** Content illustration within posts

### Diagrams
- **Format:** SVG preferred, PNG fallback
- **Background:** Transparent or white
- **Text:** Minimum 14px when rendered
- **Purpose:** Technical explanations

### Infographics
- **Dimensions:** 800-1200px wide
- **Format:** PNG or SVG
- **Color scheme:** Consistent with site branding
- **Purpose:** Data visualization

## Frontmatter Image Metadata

Each blog post should include comprehensive image metadata:

```yaml
---
title: "Post Title"
date: YYYY-MM-DD
description: "Post description"
tags: [tag1, tag2]
author: "William Zujkowski"
images:
  hero:
    src: "/assets/images/blog/hero/YYYY-MM-DD-post-slug-hero.jpg"
    alt: "Descriptive alt text for hero image"
    caption: "Optional caption for context"
    credit: "Photo credit if applicable"
  og:
    src: "/assets/images/blog/hero/YYYY-MM-DD-post-slug-og.jpg"
    alt: "Open Graph image description"
  inline:
    - src: "/assets/images/blog/inline/image1.png"
      alt: "Alt text for inline image 1"
      caption: "Caption for image 1"
    - src: "/assets/images/blog/diagrams/diagram1.svg"
      alt: "Alt text for diagram"
      caption: "System architecture diagram"
---
```

## Accessibility Standards

### Alt Text Requirements
- **Be descriptive:** Convey the image's purpose and content
- **Be concise:** 125 characters or less when possible
- **Include context:** Relate to surrounding content
- **Avoid redundancy:** Don't repeat caption text

### Alt Text Examples
- ✅ Good: "Diagram showing Claude-Flow's hierarchical swarm topology with queen and worker agents"
- ❌ Bad: "Image" or "Diagram"

## Image Optimization

### Compression Guidelines
- **JPEG:** Quality 85% for photos
- **PNG:** Use pngquant for lossless compression
- **WebP:** Provide as alternative format
- **SVG:** Minify and optimize paths

### Responsive Images
```html
<picture>
  <source srcset="/assets/images/blog/hero/image.webp" type="image/webp">
  <source srcset="/assets/images/blog/hero/image.jpg" type="image/jpeg">
  <img src="/assets/images/blog/hero/image.jpg" 
       alt="Descriptive alt text"
       loading="lazy"
       width="1200"
       height="630">
</picture>
```

## Visual Consistency

### Color Palette
- Primary: #3B82F6 (Blue)
- Secondary: #10B981 (Green)
- Accent: #8B5CF6 (Purple)
- Neutral: #6B7280 (Gray)
- Background: #FFFFFF (White)
- Dark mode support required

### Typography in Images
- Font: System font stack or Inter
- Minimum size: 14px
- High contrast ratios (WCAG AA)
- Consistent heading hierarchy

## Implementation Checklist

For each blog post:
- [ ] Create hero image (1200x630px)
- [ ] Optimize all images (<200KB)
- [ ] Add comprehensive alt text
- [ ] Include image metadata in frontmatter
- [ ] Generate WebP alternatives
- [ ] Test responsive display
- [ ] Verify accessibility compliance
- [ ] Create social media variants

## Automation Scripts

### Image Optimization Script
```bash
# Optimize all blog images
for img in src/assets/images/blog/**/*.{jpg,jpeg,png}; do
  # Create WebP version
  cwebp -q 85 "$img" -o "${img%.*}.webp"
  
  # Optimize original
  if [[ $img == *.png ]]; then
    pngquant --quality=85-95 --ext=.png --force "$img"
  else
    jpegoptim --max=85 "$img"
  fi
done
```

### Generate Responsive Variants
```bash
# Create multiple sizes for responsive images
for img in src/assets/images/blog/hero/*.{jpg,png}; do
  basename="${img%.*}"
  
  # Create sizes
  convert "$img" -resize 1200x "$basename-1200.jpg"
  convert "$img" -resize 800x "$basename-800.jpg"
  convert "$img" -resize 400x "$basename-400.jpg"
done
```

## Social Media Image Templates

### Twitter/X Card
- Dimensions: 1200x675px
- Safe area: Central 1000x475px
- Text size: Minimum 24px

### LinkedIn
- Dimensions: 1200x627px
- Aspect ratio: 1.91:1

### Facebook
- Dimensions: 1200x630px
- Aspect ratio: 1.91:1

## Performance Metrics

Target metrics for image loading:
- **LCP (Largest Contentful Paint):** < 2.5s
- **Total image weight per page:** < 1MB
- **Hero image load time:** < 1s
- **Lazy loading:** All below-fold images

## Future Enhancements

1. **AI-Generated Alt Text:** Implement automatic alt text generation
2. **Dynamic Image CDN:** Use image transformation service
3. **AVIF Support:** Add next-gen image format
4. **Dark Mode Variants:** Automatic image adjustments
5. **Image Maps:** Interactive diagrams with clickable areas