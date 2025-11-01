---
title: Image Automation Workflow
category: technical
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1000
load_when:
  - Generating hero images
  - Optimizing images
  - Running image automation
dependencies:
  - standards/image-standards
tags: [images, automation, optimization, hero]
---

# Image Automation Workflow

This document describes the automated image generation, optimization, and metadata management workflow.

## Quick Commands

### Complete Image Pipeline

**When creating/editing blog posts:**
```bash
# 1. Update image metadata
python scripts/blog-images/update-blog-images.py

# 2. Generate hero images
python scripts/blog-images/generate-blog-hero-images.py

# 3. Optimize images
bash scripts/optimize-blog-images.sh
```

**Run all three in sequence** for new posts.

## Image Automation Scripts

### 1. Update Blog Image Metadata

**Script:** `scripts/blog-images/update-blog-images.py`

**Purpose:** Automatically add/update image metadata in blog post frontmatter.

**What it does:**
- Scans all blog posts for missing image metadata
- Generates appropriate image paths
- Creates context-aware alt text
- Updates frontmatter with complete image section

**Usage:**
```bash
# Update all posts
python scripts/blog-images/update-blog-images.py

# Update specific post
python scripts/blog-images/update-blog-images.py --post src/posts/2025-10-29-example.md

# Dry-run (preview changes)
python scripts/blog-images/update-blog-images.py --dry-run

# Validate existing metadata
python scripts/blog-images/update-blog-images.py --validate
```

**Generated metadata format:**
```yaml
images:
  hero:
    src: "/assets/images/blog/hero/YYYY-MM-DD-post-slug-hero.jpg"
    alt: "Descriptive alt text for hero image"
    caption: "Optional caption for context"
    width: 1200
    height: 630
  og:
    src: "/assets/images/blog/hero/YYYY-MM-DD-post-slug-og.jpg"
    alt: "Open Graph image description"
  inline:
    - src: "/assets/images/blog/inline/image1.png"
      alt: "Alt text for inline image 1"
      caption: "Caption for image 1"
```

### 2. Generate Hero Images

**Script:** `scripts/blog-images/generate-blog-hero-images.py`

**Purpose:** Create hero images for blog posts with topic-based styling.

**Features:**
- Topic-based color schemes (security, AI/ML, cloud, blockchain, etc.)
- Pattern overlays (circuit, dots, lines, grid, waves)
- Automatic text layout and typography
- Social media variants (og:image, Twitter cards)
- Responsive image generation

**Usage:**
```bash
# Generate for all posts
python scripts/blog-images/generate-blog-hero-images.py

# Generate for specific post
python scripts/blog-images/generate-blog-hero-images.py --post="YYYY-MM-DD-post-slug"

# Regenerate existing images
python scripts/blog-images/generate-blog-hero-images.py --force

# Preview without saving
python scripts/blog-images/generate-blog-hero-images.py --preview
```

**Color schemes by topic:**
- **Security**: Blue to red gradient (#1e3a8a → #dc2626)
- **AI/ML**: Purple to pink (#7c3aed → #ec4899)
- **Cloud**: Sky blue to teal (#0ea5e9 → #10b981)
- **Blockchain**: Amber to emerald (#f59e0b → #10b981)
- **Quantum**: Violet to blue (#8b5cf6 → #3b82f6)
- **DevOps**: Green to blue (#10b981 → #3b82f6)
- **Python**: Python blue and yellow (#3776ab → #ffd343)
- **JavaScript**: JavaScript yellow (#f7df1e)

**Pattern selection:**
- **AI/ML posts**: Circuit pattern
- **Cloud/DevOps**: Dots pattern
- **Security**: Diagonal lines
- **Network**: Wave pattern
- **Default**: Grid pattern

### 3. Optimize Images

**Script:** `scripts/optimize-blog-images.sh`

**Purpose:** Optimize images and create responsive variants.

**What it does:**
- JPEG optimization (85% quality)
- PNG compression (lossless)
- Responsive variant generation (1200px, 800px, 400px, 200px)
- WebP conversion (if tools available)
- File size reduction

**Usage:**
```bash
# Optimize all images
bash scripts/optimize-blog-images.sh

# Force re-optimization
bash scripts/optimize-blog-images.sh --force

# Dry-run (show what would be optimized)
bash scripts/optimize-blog-images.sh --dry-run
```

**Optimization commands used:**
```bash
# JPEG optimization
find src/assets/images/blog -name "*.jpg" -exec jpegoptim --max=85 --strip-all {} \;

# PNG optimization
find src/assets/images/blog -name "*.png" -exec optipng -o2 {} \;

# WebP conversion
for img in src/assets/images/blog/**/*.jpg; do
  cwebp -q 85 "$img" -o "${img%.*}.webp"
done
```

### 4. Other Image Scripts

**Enhanced blog image search:**
```bash
python scripts/blog-images/enhanced-blog-image-search.py --query "quantum computing" --count 5
```

**Fetch stock images:**
```bash
python scripts/blog-images/fetch-stock-images.py --query "cybersecurity" --source "unsplash"
```

**Playwright image search (no API keys):**
```bash
python scripts/blog-images/playwright-image-search.py --query "AI visualization" --source "pexels"
```

## Image Workflow for New Posts

### Step-by-Step Process

**1. Write blog post** with proper frontmatter (without images section).

**2. Update metadata:**
```bash
python scripts/blog-images/update-blog-images.py
```

**3. Generate hero image:**
```bash
python scripts/blog-images/generate-blog-hero-images.py
```

**4. Optimize images:**
```bash
bash scripts/optimize-blog-images.sh
```

**5. Review and customize** (if needed):
- Check hero image appearance
- Verify alt text accuracy
- Adjust colors/patterns if desired

## Image Requirements

### Hero Images

- **Dimensions**: 1200x630px (16:9 ratio for social sharing)
- **Format**: JPEG for photos, PNG for graphics
- **Max file size**: 200KB (optimized)
- **Purpose**: Post header and og:image for social media

### Inline Images

- **Dimensions**: 800px wide (height variable)
- **Format**: JPEG/PNG/WebP
- **Max file size**: 150KB
- **Purpose**: Content illustration within posts

### Responsive Variants

Each hero image should have:
- **Original**: 1200px wide
- **Medium**: 800px wide
- **Small**: 400px wide
- **Thumbnail**: 200px wide

## Directory Structure

```
src/assets/images/blog/
├── hero/               # Hero images (1200x630px)
├── inline/             # Inline content images (800px wide)
├── diagrams/           # Technical diagrams
├── infographics/       # Data visualizations
└── thumbnails/         # Small previews (400x300px)
```

## Performance Targets

**Image optimization goals:**
- LCP (Largest Contentful Paint): <2.5s
- Total image weight per page: <1MB
- Hero image load time: <1s
- Lazy loading: All below-fold images

## Troubleshooting

### Missing Hero Images

**Generate for specific post:**
```bash
python scripts/blog-images/generate-blog-hero-images.py --post="YYYY-MM-DD-post-slug"
```

### Images Too Large

**Force re-optimization:**
```bash
bash scripts/optimize-blog-images.sh --force
```

### Broken Image Paths

**Validate all image references:**
```bash
python scripts/blog-images/update-blog-images.py --validate
```

**Check for 404s:**
```bash
# Start local server
npm run serve

# Check browser console for 404 errors
```

### Alt Text Not Descriptive

**Manually update frontmatter:**
```yaml
images:
  hero:
    alt: "More descriptive alt text explaining the image content"
```

## Best Practices

### When Creating Blog Posts

1. **Always run the update script** after creating a new post
2. **Generate hero images** for visual consistency
3. **Optimize images** before committing
4. **Test responsive loading** on different devices
5. **Verify alt text** is descriptive and accurate

### Image Selection Guidelines

1. **Hero images**: Should represent the post's main concept
2. **Inline images**: Break up text every 3-4 paragraphs
3. **Diagrams**: Use for technical explanations
4. **Infographics**: Summarize data or processes
5. **Screenshots**: Show actual interfaces when relevant

### Content-Image Alignment

- Place images near relevant text
- Use captions to provide context
- Ensure images enhance understanding
- Don't use decorative-only images

## Quality Checklist

Before publishing:
- [ ] Hero image exists and is optimized
- [ ] Image metadata in frontmatter is complete
- [ ] Alt text is descriptive and meaningful
- [ ] Responsive variants are generated
- [ ] File sizes are under limits
- [ ] Images load properly in development
- [ ] Social media preview works (og:image)

## Related Documentation

- **Image Standards**: `docs/context/standards/image-standards.md`
- **Accessibility**: `docs/context/standards/accessibility.md`
- **Blog Writing**: `docs/context/workflows/blog-writing.md`
