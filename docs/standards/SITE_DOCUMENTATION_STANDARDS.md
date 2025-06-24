# Site Documentation Standards

**Version:** 1.0.0  
**Last Updated:** 2024-01-24  
**Status:** Active  
**Standard Code:** SDS

---

## Table of Contents

1. [Overview](#overview)
2. [Documentation Structure](#documentation-structure)
3. [Content Guidelines](#content-guidelines)
4. [Metadata Requirements](#metadata-requirements)
5. [Cross-Reference System](#cross-reference-system)
6. [Version Control](#version-control)
7. [Implementation Checklist](#implementation-checklist)

---

## Overview

This standard defines how documentation is created and maintained for the williamzujkowski.github.io personal website. It implements the Knowledge Management Standards (KM) specifically adapted for a personal website context.

### Scope

- README files
- Code documentation
- Blog post formatting
- Page content structure
- AI-optimized documentation

### Prerequisites

- Understanding of Markdown
- Familiarity with Eleventy
- Knowledge of semantic HTML

---

## Documentation Structure

### [REQUIRED] File Organization

```
williamzujkowski.github.io/
├── README.md              # Project overview
├── CLAUDE.md             # AI assistant interface
├── MANIFEST.yaml         # Machine-readable metadata
├── docs/                 # Extended documentation
│   ├── guides/          # How-to guides
│   │   ├── CONTENT_GUIDE.md
│   │   └── DEVELOPMENT_GUIDE.md
│   ├── standards/       # Documentation standards
│   │   └── SITE_DOCUMENTATION_STANDARDS.md
│   └── examples/        # Code examples
└── src/                 # Content source files
```

### [REQUIRED] Document Types

1. **Technical Documentation**
   - README.md - Project overview
   - CLAUDE.md - AI interface
   - Guide documents - How-to instructions

2. **Content Documentation**
   - Blog posts - Markdown with frontmatter
   - Page content - Structured markdown
   - Code comments - Inline documentation

3. **Metadata Documentation**
   - MANIFEST.yaml - Machine-readable
   - Frontmatter - Post/page metadata
   - Config comments - Build settings

---

## Content Guidelines

### [REQUIRED] Blog Post Structure

```markdown
---
title: Post Title
date: 2024-01-24
description: SEO-friendly description
tags: [web-development, eleventy]
author: William Zujkowski
readingTime: 5 minutes
---

# Post Title

**Summary:** One-paragraph overview of the post content.

## Introduction
[Hook and context]

## Main Content
[Core information with examples]

## Conclusion
[Key takeaways]

## References
- [Related posts or external resources]
```

### [REQUIRED] Page Structure

```markdown
---
layout: page
title: Page Title
description: SEO description
permalink: /page-url/
lastUpdated: 2024-01-24
---

# Page Title

## Section 1
[Content organized in logical sections]

## Section 2
[Clear headings and subheadings]
```

### [RECOMMENDED] Writing Style

- **Tone:** Professional yet personable
- **Voice:** First person acceptable for blog posts
- **Length:** 500-2000 words for posts
- **Readability:** Grade 8-10 level

---

## Metadata Requirements

### [REQUIRED] Document Headers

Every documentation file must include:

```yaml
---
version: "1.0.0"
lastUpdated: "2024-01-24"
status: "active|draft|archived"
category: "guide|standard|reference"
---
```

### [REQUIRED] Frontmatter Schema

**Blog Posts:**
```yaml
title: string (required)
date: ISO-8601 (required)
description: string (required, 150-160 chars)
tags: array (optional)
author: string (optional, defaults to site.author)
image: string (optional, hero image)
readingTime: number (optional, in minutes)
```

**Pages:**
```yaml
layout: string (required)
title: string (required)
description: string (required)
permalink: string (required)
navigation: object (optional, menu placement)
```

### [RECOMMENDED] SEO Metadata

Include for better search visibility:
```yaml
seo:
  keywords: ["keyword1", "keyword2"]
  canonicalUrl: "https://williamzujkowski.github.io/..."
  ogImage: "/assets/images/og-image.jpg"
  twitterCard: "summary_large_image"
```

---

## Cross-Reference System

### [REQUIRED] Internal Links

Use relative paths for internal content:
```markdown
<!-- Good -->
See the [About page](/about/) for more information.
Read my post on [Eleventy basics](/posts/eleventy-basics/).

<!-- Avoid -->
See https://williamzujkowski.github.io/about/
```

### [REQUIRED] Related Content

Add related content sections:
```markdown
## Related Posts
- [Building with Eleventy](/posts/building-with-eleventy/)
- [Static Site Generators](/posts/static-site-generators/)

## See Also
- [GitHub Repository](https://github.com/williamzujkowski/williamzujkowski.github.io)
- [Eleventy Documentation](https://www.11ty.dev/)
```

### [RECOMMENDED] Tag System

Implement consistent tagging:
```yaml
tags:
  - web-development    # Technical category
  - eleventy          # Specific technology
  - tutorial          # Content type
  - beginner-friendly # Difficulty level
```

---

## Version Control

### [REQUIRED] Change Tracking

For significant documentation updates:

```markdown
## Changelog

### [1.1.0] - 2024-01-30
#### Added
- New section on advanced configuration
- Code examples for custom filters

#### Changed
- Updated installation instructions
- Clarified deployment process

#### Fixed
- Corrected typo in configuration example
```

### [RECOMMENDED] Update Notifications

For time-sensitive content:
```markdown
> **Last Updated:** January 24, 2024
> 
> **Note:** This guide reflects Eleventy v2.0.1. Check for updates
> if using a different version.
```

---

## Implementation Checklist

### Initial Setup
- [ ] Create docs/ directory structure
- [ ] Add CLAUDE.md for AI assistance
- [ ] Create MANIFEST.yaml
- [ ] Update README with KM standards

### Content Standards
- [ ] Define blog post template
- [ ] Create page template
- [ ] Set up frontmatter schemas
- [ ] Document writing guidelines

### Metadata Implementation
- [ ] Add version info to all docs
- [ ] Implement consistent frontmatter
- [ ] Set up SEO metadata
- [ ] Create tag taxonomy

### Cross-References
- [ ] Audit internal links
- [ ] Add related content sections
- [ ] Implement tag system
- [ ] Create content map

### Maintenance
- [ ] Set up change tracking
- [ ] Schedule content reviews
- [ ] Document update process
- [ ] Create validation scripts

---

## References

- [Knowledge Management Standards](.standards/docs/standards/KNOWLEDGE_MANAGEMENT_STANDARDS.md)
- [Eleventy Documentation](https://www.11ty.dev/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

---

## Quick Reference

### Essential Metadata
```yaml
# Minimum required
title: "Title"
date: 2024-01-24
description: "Description"

# Recommended additions
tags: [tag1, tag2]
author: "Name"
lastUpdated: 2024-01-24
```

### File Naming
```
# Blog posts
YYYY-MM-DD-post-title.md

# Pages
pagename.md

# Guides
GUIDE_NAME.md
```

### Link Format
```markdown
[Internal Page](/path/)
[Blog Post](/posts/post-title/)
[External](https://example.com)
```