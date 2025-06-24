# Content Creation Guide

**Version:** 2.0.0  
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

### Navigation Note

Blog posts automatically appear in the posts listing but are NOT added to the main navigation menu. To add pages to navigation, see [Static Pages](#static-pages) section.

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
eleventyNavigation:             # Required for menu inclusion
  key: Page Name                # Required - unique identifier
  title: Menu Title             # Optional - overrides page title in menu
  order: 5                      # Optional - controls menu order (lower = first)
  parent: Parent Page           # Optional - creates nested navigation
---
```

### [NEW] Navigation System

The site uses `eleventy-navigation` plugin for automatic menu generation:

1. **Basic Navigation Entry:**
   ```yaml
   eleventyNavigation:
     key: About          # Shows "About" in menu
   ```

2. **Custom Menu Title:**
   ```yaml
   eleventyNavigation:
     key: about-page
     title: About Me     # Shows "About Me" instead of page title
   ```

3. **Ordered Navigation:**
   ```yaml
   eleventyNavigation:
     key: Home
     order: 1           # First in menu
   ```

4. **Nested Navigation:**
   ```yaml
   eleventyNavigation:
     key: Team
     parent: About      # Appears under "About" in menu
     order: 2
   ```

### Common Pages

**About Page** (`src/pages/about.md`):
```markdown
---
layout: page
title: About
description: Learn more about William Zujkowski
permalink: /about/
eleventyNavigation:
  key: About
  order: 2
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
eleventyNavigation:
  key: Projects
  order: 3
---

# Projects

## Project Name

**Tech Stack:** Eleventy, CSS, JavaScript  
**Link:** [View Project](#)

Description of the project...
```

**Contact Page with Nested Navigation** (`src/pages/contact.md`):
```markdown
---
layout: page
title: Contact
description: Get in touch with me
permalink: /contact/
eleventyNavigation:
  key: Contact
  parent: About    # Nested under About
  order: 1
---

# Contact Me

Feel free to reach out...
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

## Styling with Tailwind CSS

### [NEW] Content Styling

The site uses Tailwind CSS with the Typography plugin for beautiful content styling:

1. **Prose Classes for Content**
   ```markdown
   All Markdown content is automatically wrapped in Tailwind's prose classes:
   - Light mode: `prose prose-lg prose-gray`
   - Dark mode: `prose-invert`
   - Responsive: `lg:prose-xl`
   ```

2. **Custom Components in Content**
   ```html
   <!-- Alert box -->
   <div class="rounded-lg bg-blue-50 dark:bg-blue-900/20 p-4 my-6">
     <p class="text-blue-800 dark:text-blue-200">
       💡 <strong>Tip:</strong> Your helpful information here
     </p>
   </div>

   <!-- Call-to-action button -->
   <a href="#" class="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
     Get Started
   </a>
   ```

3. **Code Block Styling**
   - Code blocks are automatically styled with syntax highlighting
   - Dark mode compatible
   - Scrollable for long lines

4. **Responsive Images**
   ```html
   <!-- Full-width responsive image -->
   <img src="/assets/images/hero.jpg" 
        alt="Description" 
        class="w-full h-auto rounded-lg shadow-lg">
   
   <!-- Centered image with max width -->
   <img src="/assets/images/diagram.png" 
        alt="Description" 
        class="mx-auto max-w-2xl h-auto">
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

**Page with Navigation:**
```yaml
---
layout: page
title: ""
description: ""
permalink: //
eleventyNavigation:
  key: ""
  order: 1
---
```

**Page without Navigation:**
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

---

## Changelog

### [2.0.0] - 2024-01-24
#### Added
- Navigation system documentation for eleventy-navigation plugin
- Tailwind CSS content styling section
- Examples of nested navigation
- Custom component examples for content
- Updated frontmatter templates with navigation

#### Changed
- All page examples now include eleventyNavigation configuration
- Added navigation note to blog posts section
- Updated version to 2.0.0

#### Technical Updates
- Pages require eleventyNavigation key for menu inclusion
- Support for hierarchical navigation with parent key
- Menu ordering with order property