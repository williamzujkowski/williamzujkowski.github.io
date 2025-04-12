# Blog Post Creation Workflow

This guide explains how to create, process, and publish blog posts on the website using our optimized workflow system.

## Overview

Our blog workflow follows a streamlined process:

1. **Draft** - Write your content in markdown or plain text
2. **Process** - Use the automated tool to convert drafts into properly formatted posts
3. **Review** - Check and customize the generated posts
4. **Publish** - Include the posts in the site build

This approach separates content creation from technical formatting, allowing you to focus on writing quality content.

## Step-by-Step Guide

### 1. Create a Draft Post

Create a new file in the `new_posts/` directory using either format:

#### Option A: Markdown Format (Recommended)

Create a `.md` file with:
- Optional frontmatter for metadata
- H1 heading for the title
- Markdown-formatted content

**Example with frontmatter:**
```markdown
---
title: "Understanding Quantum Computing"
tags: quantum, computing, technology
---

# Understanding Quantum Computing

Quantum computing represents a fundamental shift in how we process information...
```

**Example with just H1 title:**
```markdown
# Understanding Quantum Computing

Quantum computing represents a fundamental shift in how we process information...
```

#### Option B: Simple Text Format

Create a `.txt` file with:
- First line: Post title
- Second line: Blank
- Remaining lines: Content

```
Understanding Quantum Computing

Quantum computing represents a fundamental shift in how we process information...
```

### 2. Format Your Content

Follow these basic formatting guidelines:

- Use `# Heading` for main title (level 1)
- Use `## Heading` for section titles (level 2)
- Use `### Heading` for subsections (level 3)
- Use `*italic*` or `_italic_` for italic text
- Use `**bold**` or `__bold__` for bold text
- Use `- item` or `* item` for bullet lists
- Use `1. item` for numbered lists
- Use `[link text](URL)` for links
- Use `![alt text](image-path.jpg)` for images
- Use `` `code` `` for inline code
- Use triple backticks for code blocks:

```javascript
function example() {
  console.log("This is example code");
}
```

### 3. Follow Content Guidelines

#### Length & Structure
- Write posts with a 6-9 minute reading time (1,400-2,100 words)
- Use clear headings and subheadings to organize content
- Include an introduction, main sections, and conclusion
- Keep paragraphs short (3-4 sentences) for better readability

#### Content Quality
- Start with a concise summary that introduces key concepts
- Include insights from recent developments (especially arXiv papers)
- Add relevant code samples or diagrams where appropriate
- Use analogies and real-world examples to explain complex concepts
- Link to reputable sources and provide proper citations
- Maintain a conversational but professional tone
- Include a call to action and suggested resources at the end

#### Media
- Include at least one relevant image per major section
- Add meaningful alt text to all images for accessibility
- Only use images from copyright-free sources:
  - [Unsplash](https://unsplash.com/)
  - [Pexels](https://pexels.com/)
  - [Pixabay](https://pixabay.com/)
  - [Wikimedia Commons](https://commons.wikimedia.org/)

### 4. Process Your Post

Our system offers two processing options:

#### Enhanced Interactive Processor (Recommended)

```bash
npm run process:posts:enhanced
```

This provides a guided, interactive experience:
- You'll see a list of drafts available for processing
- Choose to process a single post or all drafts
- Preview the generated frontmatter before committing
- Confirm before writing files to their final destination

#### Batch Processing (For Multiple Posts)

```bash
npm run process:posts:batch
```

This processes all drafts automatically without confirmation, ideal for bulk processing.

#### Legacy Processor (Basic)

```bash
npm run process:posts
```

This runs the original processing script with fewer features.

### 5. What Happens During Processing

The processor performs these automated tasks:

- **Content Analysis** - Extracts title, body, and any existing metadata
- **SEO Optimization** - Generates descriptions and slugs for better search visibility
- **Smart Tagging** - Suggests relevant tags based on content analysis
- **Image Selection** - Chooses appropriate featured images based on content
- **Date Scheduling** - Sets publication dates spaced appropriately apart
- **Template Application** - Applies standardized formatting with proper sections
- **Cleanup** - Removes citation artifacts and fixes formatting issues
- **File Management** - Moves processed drafts to `new_posts/processed/`

### 6. Review and Customize

After processing:

1. Check the generated files in `src/posts/`
2. Make any manual adjustments needed:
   - Edit tags if the suggestions aren't perfect
   - Modify the description for better SEO
   - Change the featured image if desired
   - Add or refine code examples
   - Enhance visual elements or formatting

### 7. Publishing

After processing, posts will be automatically included in the site build:

```bash
npm run build
```

For development and preview:

```bash
npm run dev
```

## Post Features & Settings

### Frontmatter Options

Each post has these configurable settings in the frontmatter:

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

### Featured Images

#### Image Selection System

Posts automatically get relevant featured images based on:

1. Explicit `image` field in frontmatter (highest priority)
2. Tags that match known image categories
3. Keywords in the title and content
4. Default image (lowest priority)

#### Custom Images

To specify a custom image:

```yaml
---
title: My Blog Post
image: blog/custom/my-image.jpg 
image_alt: Description of my custom image
---
```

Paths should be relative to the `assets/images/` directory.

#### Available Image Categories

The system supports these image categories:

| Category | Topic | File Path |
|----------|-------|-----------|
| ai | Artificial Intelligence | blog/ai-blog.jpg |
| security | Cybersecurity | blog/security-blog.jpg |
| cloud | Cloud Computing | blog/cloud-blog.jpg |
| ethics | AI Ethics | blog/ethics-blog.jpg |
| transformer | Transformer Architecture | blog/transformer-blog.jpg |
| pizza | Pizza Calculator | blog/pizza-blog.jpg |
| cryptography | Encryption & Cryptography | blog/topics/cryptography.jpg |
| quantum | Quantum Computing | blog/topics/quantum.jpg |
| edge | Edge Computing | blog/topics/edge-computing.jpg |
| hpc | High-Performance Computing | blog/topics/hpc.jpg |
| rag | Retrieval Augmented Generation | blog/topics/rag.jpg |
| prompt | Prompt Engineering | blog/topics/prompt-engineering.jpg |
| containers | Container Technologies | blog/topics/containers.jpg |
| resilience | System Resilience | blog/topics/resilience.jpg |
| llm | Large Language Models | blog/topics/llm.jpg |

#### Adding New Image Categories

You can add new image categories in two ways:

##### Option 1: Automatic (Recommended)
1. Add tags to your blog posts
2. Run `npm run build:blog-images`
3. The system will automatically:
   - Extract all unique tags from your posts
   - Find appropriate images for each tag
   - Download images from free image sources
   - Update the configuration file

##### Option 2: Manual Configuration
1. Edit `src/_data/config/blog/images.json`
2. Add entries to both `image_mapping` and `keyword_mapping` sections
3. Run `npm run build:blog-images` to download sample images

The enhanced image downloader supports:
- Unsplash images (even without API key)
- Pixabay images (with API key)
- Pexels images (with API key)
- Custom predefined image URLs

### Tags

Common tags include:

- `posts` (automatically added to all posts)
- `security`
- `ai`
- `cloud`
- `devops`
- `programming`
- `architecture`
- `quantum`
- `cryptography`
- `edge`
- `hpc` 
- `rag`
- `prompt`
- `containers`
- `resilience`
- `llm`
- `ethics`

Use 3-5 relevant tags per post for better categorization.

## Tips for Great Blog Posts

### Content Strategy
- **Research First** - Read recent papers and established sources before writing
- **Unique Angle** - Offer perspectives not found elsewhere
- **Practical Value** - Include actionable takeaways readers can implement
- **Progressive Disclosure** - Start simple, then delve into complexity

### Enhancing Readability
- Use the "inverted pyramid" - most important information first
- Break up text with headings, lists, and visual elements
- Include code examples for technical concepts
- Add comparative tables for technology comparisons

### Technical Best Practices
- Include performance benchmarks where relevant
- Discuss trade-offs and limitations of approaches
- Provide complete code examples when possible
- Link to documentation and further resources

### SEO Optimization
- Use descriptive, keyword-rich titles
- Write meta descriptions that encourage clicks
- Include relevant keywords naturally in headings
- Link to related content on the site

## Troubleshooting

- **Images not showing**: Verify paths are correct relative to `assets/images/`
- **Formatting issues**: Check markdown syntax in your original post
- **Missing metadata**: Ensure frontmatter is properly formatted with no YAML errors
- **Date conflicts**: Edit post frontmatter to adjust publication dates
- **Processing errors**: Check the `new_posts/` directory structure and file formats

## Further Help

For more assistance:
- Check the [official Markdown guide](https://www.markdownguide.org/)
- Review [11ty documentation](https://www.11ty.dev/docs/) for template questions
- Visit [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/) for advanced formatting