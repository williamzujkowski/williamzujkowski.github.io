# Blog Post Workflow

> This document is part of the [website documentation](../README.md).

This document outlines the process for creating and publishing new blog posts on the website.

## Overview

The blog workflow uses a two-stage process:

1. Draft posts in simple text or markdown format in the `new_posts/` directory
2. Process them automatically with the conversion script to create properly formatted posts

This approach makes it easy to focus on content first, then handle formatting and technical details automatically.

## Creating New Posts

### Step 1: Write Draft Content

You can use either of these formats:

#### Option A: Simple Text Format (.txt)

1. Create a new `.txt` file in the `new_posts/` directory
2. Use a simple format:
   - First line: Post title
   - Second line: Blank
   - Remaining lines: Post content

Example:

```
Understanding Quantum Computing

Quantum computing represents a fundamental shift in how we process information...
```

#### Option B: Markdown Format (.md)

1. Create a new `.md` file in the `new_posts/` directory
2. Use any of these formats:
   - Use an H1 header (`# Title`) for the title
   - Or use front matter with a title field
   - Or the script will use the filename as the title

Example with H1:

```markdown
# Understanding Quantum Computing

Quantum computing represents a fundamental shift in how we process information...
```

Example with front matter:

```markdown
---
title: Understanding Quantum Computing
---

Quantum computing represents a fundamental shift in how we process information...
```

### Step 2: Format Your Content (Optional)

While the conversion script handles basic formatting, you can enhance your drafts:

- Use standard Markdown formatting in your content
- Use # for main title (added automatically)
- Use ## for section headings
- Use \* or - for bullet points
- Use `backticks` for inline code
- Use ```language for code blocks

### Step 3: Run the Conversion Process

Run the post processing script:

```bash
# Using npm script
npm run process:posts

# Or using the CLI utility
./scripts/bin/content.sh blog:process

# Or directly with node
node scripts/content/blog/process-new-posts.js
```

This script will:

- Extract the title from the first line
- Generate appropriate frontmatter
- Set publication dates (spaced 10-14 days apart from the most recent post)
- Create slugs from titles
- Suggest relevant tags based on content
- Add appropriate feature images
- Convert to proper Markdown format
- Move processed files to `new_posts/processed/`

### Step 4: Review and Customize

1. Check the generated files in `src/posts/`
2. Make any manual adjustments needed:
   - Edit tags if necessary
   - Replace suggested images
   - Add or modify code examples
   - Add diagrams or custom content

## Post Features

### Images

The conversion process automatically suggests images based on content keywords. Available images include:

- `ai-blog.jpg` - For AI/ML topics
- `cloud-blog.jpg` - For cloud/infrastructure topics
- `ethics-blog.jpg` - For ethics/policy topics
- `security-blog.jpg` - For security/privacy topics
- `transformer-blog.jpg` - For transformer/LLM topics
- `tech-header.jpg` - Default technology header

To use a custom image, just replace the suggested image in the frontmatter.

### Tags

Common tags are automatically suggested based on content. These include:

- `posts` (added to all posts)
- `security`
- `ai`
- `cloud`
- `devops`
- `programming`
- `architecture`

### Code Blocks

Use standard Markdown code blocks with language specification:

```javascript
function example() {
  console.log("This is example code");
}
```

## Publishing

After processing, posts will be automatically included in the site build. Run:

```bash
npm run build
```

To see your changes live during development:

```bash
npm run dev
```

## Troubleshooting

- **Images not showing**: Make sure image paths are correct and images exist in `assets/images/blog/`
- **Formatting issues**: Check Markdown syntax in your original post
- **Dates too close**: Edit post frontmatter to adjust publication dates

## Adding New Images

To add new images to use with blog posts:

1. Add the image to `assets/images/blog/`
2. Reference it in your post using the correct path:

```markdown
![Alt text](/assets/images/blog/your-image.jpg)
```

## Best Practices

- Keep titles concise and descriptive
- Use section headings to organize content
- Include code examples where helpful
- Use images to break up text and illustrate concepts
- Keep paragraphs short for better readability
- Tag posts accurately for better categorization

---

[Back to Documentation Home](../index.md) | [Guides](./)
