# Blog Post Quick Reference Guide

## 📝 Quick Start

1. **Create draft** in `new_posts/` directory (markdown or text)
2. **Process post** with `npm run process:posts:enhanced`
3. **Review output** in `src/posts/` directory
4. **Build site** with `npm run build`

## 🛠 Post Processing Options

| Command                          | Description                                        |
| -------------------------------- | -------------------------------------------------- |
| `npm run process:posts:enhanced` | Interactive processing with guidance (recommended) |
| `npm run process:posts:batch`    | Process all posts automatically                    |
| `npm run process:posts`          | Legacy processor (basic features)                  |

## 📋 Frontmatter Template

```yaml
---
title: "Post Title"
date: 2025-01-15
layout: post.njk
tags:
  - posts
  - category1
  - category2
description: "SEO-friendly description of the post content"
image: blog/topics/image-name.jpg
image_alt: "Description of the featured image"
---
```

## 📊 Content Guidelines

- **Length**: 6-9 minute read (1,400-2,100 words)
- **Format**: Clear headings, short paragraphs, code examples
- **Images**: At least one per major section (from free sources)
- **Structure**: Intro → Main content → Conclusion → Resources

## 🏷 Common Tags

- `posts` (automatic)
- `security`, `ai`, `cloud`, `devops`
- `programming`, `architecture`
- `quantum`, `cryptography`, `edge`
- `hpc`, `rag`, `prompt`, `containers`
- `resilience`, `llm`, `ethics`

## 🖼 Image Categories

| Category     | Topic                     | File Path                    |
| ------------ | ------------------------- | ---------------------------- |
| ai           | Artificial Intelligence   | blog/ai-blog.jpg             |
| security     | Cybersecurity             | blog/security-blog.jpg       |
| cloud        | Cloud Computing           | blog/cloud-blog.jpg          |
| ethics       | AI Ethics                 | blog/ethics-blog.jpg         |
| transformer  | Transformer Architecture  | blog/transformer-blog.jpg    |
| quantum      | Quantum Computing         | blog/topics/quantum.jpg      |
| cryptography | Encryption & Cryptography | blog/topics/cryptography.jpg |
| llm          | Large Language Models     | blog/topics/llm.jpg          |

_Update all image categories with: `npm run build:blog-images`_

## 📚 Markdown Cheatsheet

````markdown
# Heading 1

## Heading 2

### Heading 3

**Bold text**
_Italic text_

- Bullet point
- Another point
  - Sub-point

1. Numbered item
2. Another item

[Link text](https://example.com)

![Alt text](image-path.jpg)

`inline code`

```javascript
// Code block
function example() {
  return "Hello";
}
```
````

> Blockquote text

| Column 1 | Column 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |

```

## 🔎 For Details

See the comprehensive [BLOG-WORKFLOW.md](BLOG-WORKFLOW.md) for full documentation and instructions.

## 🧠 Using AI Assistance

The file `Prompts/blogpost.prompt` contains a comprehensive prompt for generating high-quality blog posts with AI assistants. It helps create structured content that follows our guidelines, including:

- Topic selection and audience targeting
- Content structure and formatting
- Visual enhancements and image selection
- Code integration and examples
- Research suggestions for latest developments

## 📁 Directory Structure

```

/
├── new_posts/ # Place draft posts here
│ └── processed/ # Processed drafts move here
├── Prompts/
│ ├── blogpost.prompt # AI prompt for generating posts
│ └── post-template.md # Standard post template
├── src/
│ └── posts/ # Final formatted posts
├── tools/
│ ├── process-new-posts.js # Legacy processor
│ └── enhanced-post-processor.js # New interactive processor
└── BLOG-WORKFLOW.md # Complete workflow documentation

```

```
