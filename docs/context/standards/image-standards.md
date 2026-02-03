---
title: Blog Image Standards
category: standards
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1500
load_when:
  - Creating blog posts with images
  - Managing hero images
  - Optimizing images
  - Image metadata updates
dependencies:
  - technical/image-automation
tags: [images, hero, optimization, accessibility, metadata]
---

# Blog Image Standards

## Module Metadata
- **Category:** standards
- **Priority:** MEDIUM
- **Load frequency:** Blog posts with images
- **Dependencies:** technical/image-automation (when implemented)

## Purpose
This module defines image management standards for blog posts, including directory structure, naming conventions, image requirements, automation workflows, and accessibility standards.

## When to Load This Module
- **Creating blog posts with images** - Proper metadata from start
- **Managing hero images** - Generation and optimization
- **Optimizing images** - Performance requirements
- **Image metadata updates** - Frontmatter standards

## Quick Reference

| Image Type | Dimensions | Max Size | Format | Purpose |
|------------|------------|----------|--------|---------|
| Hero | 1200x630px | 200KB | JPEG/PNG | Post header + og:image |
| Inline | 800px wide | 150KB | JPEG/PNG/WebP | Content illustration |
| Thumbnail | 200px wide | 50KB | JPEG | Previews |

**Required Automation:**
```bash
# Complete image pipeline for new post
uv run python scripts/blog-images/update-blog-images.py && \
uv run python scripts/blog-images/generate-blog-hero-images.py && \
bash scripts/optimize-blog-images.sh
```

---

## Image Management System

### Directory Structure

All blog images are organized in a hierarchical structure:

```
src/assets/images/blog/
├── hero/               # Hero images for post headers (1200x630px)
├── inline/             # Inline content images (800px wide)
├── diagrams/           # Technical diagrams and architecture visuals
├── infographics/       # Data visualizations and infographics
└── thumbnails/         # Small preview images (400x300px)
```

### Image Naming Convention

**Format:** `YYYY-MM-DD-post-slug-image-type.ext`

**Example:** `2025-08-07-nexus-agents-architecture-diagram.png`

---

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

### Responsive Variants

Each hero image should have:
- Original: 1200px wide
- Medium: 800px wide
- Small: 400px wide
- Thumbnail: 200px wide

---

## Blog Post Frontmatter

Every blog post MUST include comprehensive image metadata:

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
    width: 1200
    height: 630
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

---

## Automation Scripts

### 1. Update Blog Image Metadata

```bash
# Updates all blog posts with proper image metadata
uv run python scripts/blog-images/update-blog-images.py
```

**This script:**
- Scans all blog posts
- Generates appropriate image metadata
- Creates context-aware alt text
- Updates frontmatter automatically

### 2. Generate Hero Images

```bash
# Creates hero images for all blog posts
uv run python scripts/blog-images/generate-blog-hero-images.py
```

**Features:**
- Topic-based color schemes
- Pattern overlays (circuit, dots, lines, grid, waves)
- Automatic text layout
- Social media variants (og:image)

### 3. Optimize Images

```bash
# Optimizes images and creates responsive variants
bash scripts/optimize-blog-images.sh
```

**Performs:**
- JPEG optimization (85% quality)
- PNG compression
- Responsive variant generation
- WebP conversion (if tools available)

---

## Image Creation Workflow

### For New Blog Posts

1. **Write the post** with proper frontmatter (without images section)
2. **Run metadata update**: `uv run python scripts/blog-images/update-blog-images.py`
3. **Generate hero image**: `uv run python scripts/blog-images/generate-blog-hero-images.py`
4. **Optimize images**: `bash scripts/optimize-blog-images.sh`
5. **Review and customize** if needed

### For Existing Posts

1. **Update metadata**: `uv run python scripts/blog-images/update-blog-images.py`
2. **Generate missing images**: `uv run python scripts/blog-images/generate-blog-hero-images.py`
3. **Optimize all images**: `bash scripts/optimize-blog-images.sh`

---

## Accessibility Standards

### Alt Text Requirements

- **Be descriptive**: Convey the image's purpose and content
- **Be concise**: 125 characters or less when possible
- **Include context**: Relate to surrounding content
- **Avoid redundancy**: Don't repeat caption text

### Examples

- ✅ Good: "Diagram showing Claude-Flow's hierarchical swarm topology with queen and worker agents"
- ❌ Bad: "Image" or "Diagram"

---

## Visual Consistency

### Color Schemes by Topic

The image generator automatically selects colors based on content:

- **Security**: Blue to red gradient (#1e3a8a → #dc2626)
- **AI/ML**: Purple to pink (#7c3aed → #ec4899)
- **Cloud**: Sky blue to teal (#0ea5e9 → #10b981)
- **Blockchain**: Amber to emerald (#f59e0b → #10b981)
- **Quantum**: Violet to blue (#8b5cf6 → #3b82f6)
- **DevOps**: Green to blue (#10b981 → #3b82f6)
- **Python**: Python blue and yellow (#3776ab → #ffd343)
- **JavaScript**: JavaScript yellow (#f7df1e)

### Pattern Selection

Patterns are automatically chosen based on tags:

- **AI/ML posts**: Circuit pattern
- **Cloud/DevOps**: Dots pattern
- **Security**: Diagonal lines
- **Network**: Wave pattern
- **Default**: Grid pattern

---

## Image Optimization

### Performance Targets

- **LCP (Largest Contentful Paint)**: < 2.5s
- **Total image weight per page**: < 1MB
- **Hero image load time**: < 1s
- **Lazy loading**: All below-fold images

### Optimization Commands

```bash
# Install optimization tools
sudo apt-get install jpegoptim optipng webp imagemagick

# Optimize JPEGs
find src/assets/images/blog -name "*.jpg" -exec jpegoptim --max=85 --strip-all {} \;

# Optimize PNGs
find src/assets/images/blog -name "*.png" -exec optipng -o2 {} \;

# Create WebP versions
for img in src/assets/images/blog/**/*.jpg; do
  cwebp -q 85 "$img" -o "${img%.*}.webp"
done
```

---

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

---

## Cross-References

### Related Modules
- [technical/image-automation](../technical/image-automation.md) - Image script details (when implemented)
- [workflows/blog-writing](../workflows/blog-writing.md) - Blog post creation workflow
- [standards/accessibility](accessibility.md) - Accessibility requirements

### External References
- **Image Updater:** `scripts/blog-images/update-blog-images.py`
- **Hero Generator:** `scripts/blog-images/generate-blog-hero-images.py`
- **Optimizer:** `scripts/optimize-blog-images.sh`

---

## Examples

### Example 1: Complete Image Frontmatter

```yaml
images:
  hero:
    src: "/assets/images/blog/hero/2025-11-01-k3s-homelab-hero.jpg"
    alt: "K3s cluster running on three Raspberry Pi 4 devices with LED indicators showing node status"
    caption: "Homelab K3s setup: 3-node cluster on Raspberry Pi 4"
    width: 1200
    height: 630
  og:
    src: "/assets/images/blog/hero/2025-11-01-k3s-homelab-og.jpg"
    alt: "K3s homelab architecture diagram"
  inline:
    - src: "/assets/images/blog/diagrams/k3s-architecture.svg"
      alt: "Architecture diagram showing K3s control plane and worker nodes"
      caption: "K3s cluster topology with SQLite datastore"
```

**Analysis:** Descriptive alt text, proper paths, dimensions specified, captions add context without repeating alt text.

---

## Common Pitfalls

### Pitfall 1: Missing Alt Text
**Problem:** Images without alt text fail accessibility requirements
**Solution:** Run `update-blog-images.py` to auto-generate descriptive alt text
**Prevention:** Include alt text in frontmatter from creation

### Pitfall 2: Oversized Images
**Problem:** Large images slow page load, hurt Core Web Vitals
**Solution:** Run `optimize-blog-images.sh` before committing
**Prevention:** Check file sizes: hero <200KB, inline <150KB

### Pitfall 3: Broken Image Paths
**Problem:** Incorrect paths break images in production
**Solution:** Use absolute paths starting with `/assets/images/blog/`
**Prevention:** Run validation script before committing

---

## Validation

### Quality Checklist

Before publishing, ensure:
- [ ] Hero image exists and is optimized
- [ ] Image metadata in frontmatter is complete
- [ ] Alt text is descriptive and meaningful
- [ ] Responsive variants are generated
- [ ] File sizes are under limits
- [ ] Images load properly in development
- [ ] Social media preview works (og:image)

### Validation Commands

```bash
# Validate all image references
uv run python scripts/blog-images/update-blog-images.py --validate

# Check image statistics
find src/assets/images/blog -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.webp" \) | wc -l

# Generate image report
uv run python scripts/blog-images/update-blog-images.py --report > docs/image-report.md
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md v3.0.0
- Image management system documented
- Directory structure defined
- Automation workflows included
- Accessibility standards established
- Optimization targets set

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Image quality agent

**Update Triggers:**
- New image types added
- Optimization tools updated
- Accessibility standards change
- Performance targets adjust

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
