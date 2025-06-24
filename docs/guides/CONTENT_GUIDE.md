# Content Creation Guide

**Version:** 1.0.0  
**Last Updated:** 2024-01-24  
**Status:** Active  
**Category:** Guide

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Blog Posts](#blog-posts)
3. [Static Pages](#static-pages)
4. [Images and Media](#images-and-media)
5. [SEO Best Practices](#seo-best-practices)
6. [Content Workflow](#content-workflow)

---

## Quick Start

### Creating Your First Post

1. Create a new file in `src/posts/`:
   ```bash
   touch src/posts/2024-01-24-my-first-post.md
   ```

2. Add frontmatter and content:
   ```markdown
   ---
   title: My First Post
   date: 2024-01-24
   description: Learning how to create content with Eleventy
   tags: [tutorial, eleventy]
   ---

   Your content here...
   ```

3. Preview locally:
   ```bash
   npm run serve
   ```

4. Visit http://localhost:8080/posts/my-first-post/

---

## Blog Posts

### [REQUIRED] File Structure

Location: `src/posts/`  
Format: Markdown (.md)  
Naming: `YYYY-MM-DD-post-title.md` (optional but recommended)

### [REQUIRED] Frontmatter

```yaml
---
title: "Your Post Title"          # Required
date: 2024-01-24                 # Required (YYYY-MM-DD)
description: "Brief description"  # Required (150-160 chars)
tags: [tag1, tag2]               # Optional
author: "Your Name"              # Optional (defaults to site.author)
image: "/assets/images/hero.jpg" # Optional
draft: false                     # Optional
---
```

### [RECOMMENDED] Post Template

```markdown
---
title: "Building a Personal Website with Eleventy"
date: 2024-01-24
description: "Learn how to create a fast, accessible personal website using Eleventy and GitHub Pages"
tags: [web-development, eleventy, tutorial]
---

**Reading time:** 5 minutes

## Introduction

Start with a hook that explains why readers should care about this topic.

## Prerequisites

- Basic HTML/CSS knowledge
- Node.js installed
- GitHub account

## Main Content

### Step 1: Setup

Detailed instructions with code examples:

```javascript
// Example code
module.exports = function(eleventyConfig) {
  // Configuration
};
```

### Step 2: Implementation

Continue with logical progression...

## Conclusion

Summarize key points and provide next steps.

## Resources

- [Official Eleventy Docs](https://www.11ty.dev/)
- [GitHub Repository](#)
```

### [RECOMMENDED] Writing Tips

1. **Start with an outline**
   - Introduction (why this matters)
   - Main points (3-5 sections)
   - Conclusion (key takeaways)

2. **Use clear headings**
   - H2 for main sections
   - H3 for subsections
   - H4 sparingly

3. **Include examples**
   - Code snippets
   - Screenshots
   - Real-world scenarios

4. **Optimize for scanning**
   - Short paragraphs (3-4 sentences)
   - Bullet points for lists
   - Bold key concepts

---

## Static Pages

### [REQUIRED] Page Structure

Location: `src/pages/`  
Format: Markdown (.md) or Nunjucks (.njk)

### [REQUIRED] Frontmatter

```yaml
---
layout: page                     # Required
title: "Page Title"             # Required  
description: "Page description" # Required
permalink: /custom-url/         # Required
navigation:                     # Optional
  order: 1
  label: "Nav Label"
---
```

### Common Pages

**About Page** (`src/pages/about.md`):
```markdown
---
layout: page
title: About
description: Learn more about William Zujkowski
permalink: /about/
---

# About Me

## Background

Your professional background...

## Skills

- Web Development
- Static Site Generators
- ...

## Contact

How to reach you...
```

**Projects Page** (`src/pages/projects.md`):
```markdown
---
layout: page
title: Projects
description: Featured projects and work
permalink: /projects/
---

# Projects

## Project Name

**Tech Stack:** Eleventy, CSS, JavaScript  
**Link:** [View Project](#)

Description of the project...
```

---

## Images and Media

### [REQUIRED] Image Organization

```
src/assets/images/
├── posts/          # Blog post images
├── pages/          # Page-specific images
├── og/             # Open Graph images
└── site/           # General site images
```

### [RECOMMENDED] Image Optimization

1. **Format Selection**
   - Photos: JPEG (quality 80-85)
   - Graphics: PNG or SVG
   - Animations: GIF or MP4

2. **Sizing Guidelines**
   - Hero images: 1200x630px (OG size)
   - Content images: 800px max width
   - Thumbnails: 400x300px

3. **Naming Convention**
   - Descriptive: `eleventy-build-process.png`
   - Not: `img1.png` or `screenshot.png`

### [RECOMMENDED] Image Usage

In Markdown:
```markdown
![Alt text describing the image](/assets/images/posts/image-name.jpg)
```

With caption:
```markdown
<figure>
  <img src="/assets/images/posts/image-name.jpg" alt="Alt text">
  <figcaption>Image caption goes here</figcaption>
</figure>
```

---

## SEO Best Practices

### [REQUIRED] On-Page SEO

1. **Title Optimization**
   - 50-60 characters
   - Include primary keyword
   - Compelling and clear

2. **Meta Descriptions**
   - 150-160 characters
   - Include call-to-action
   - Unique for each page

3. **URL Structure**
   - Use hyphens: `/my-blog-post/`
   - Keep short and descriptive
   - Avoid special characters

### [RECOMMENDED] Content SEO

1. **Heading Structure**
   - One H1 per page (usually the title)
   - Use H2-H6 hierarchically
   - Include keywords naturally

2. **Internal Linking**
   - Link to related posts
   - Use descriptive anchor text
   - Create topic clusters

3. **External Linking**
   - Link to authoritative sources
   - Use `rel="noopener"` for security
   - Open in same window by default

---

## Content Workflow

### [RECOMMENDED] Publishing Process

1. **Planning**
   - Research topic
   - Create outline
   - Gather resources

2. **Writing**
   - Draft in Markdown
   - Add code examples
   - Include images

3. **Review**
   - Check spelling/grammar
   - Verify code works
   - Test all links

4. **Optimization**
   - Add SEO metadata
   - Optimize images
   - Check mobile view

5. **Publishing**
   - Commit to Git
   - Push to main branch
   - Verify deployment

### [OPTIONAL] Content Calendar

Consider maintaining a simple content calendar:

```markdown
## 2024 Content Calendar

### January
- [x] Welcome post
- [ ] Eleventy tutorial
- [ ] GitHub Pages guide

### February
- [ ] CSS Custom Properties
- [ ] Accessibility basics
```

---

## Quick Reference

### Frontmatter Templates

**Blog Post:**
```yaml
---
title: ""
date: 2024-01-24
description: ""
tags: []
---
```

**Page:**
```yaml
---
layout: page
title: ""
description: ""
permalink: //
---
```

### Common Tags

- `tutorial` - How-to content
- `web-development` - General web dev
- `eleventy` - Eleventy-specific
- `css` - Styling topics
- `javascript` - JS content
- `personal` - Personal updates
- `project` - Project announcements

### Markdown Helpers

```markdown
**Bold text**
*Italic text*
[Link text](URL)
![Image alt](URL)
`inline code`
```code block```
> Blockquote
- Bullet point
1. Numbered list
```

---

## Related Documentation

- [Site Documentation Standards](../standards/SITE_DOCUMENTATION_STANDARDS.md)
- [Development Guide](DEVELOPMENT_GUIDE.md)
- [README.md](../../README.md)