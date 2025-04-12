# Blog Post Workflow

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

### Step 2: Content Guidelines

Follow these guidelines to create effective blog posts:

#### Audience
- Target technology enthusiasts while making content accessible to beginners
- Start with a concise summary that introduces key concepts

#### Topic Selection
- Check existing posts to avoid duplicating topics
- Define a clear objective (educate, tutorial, analyze developments)

#### Content Development
- Include insights from recent developments and personal experiences
- Enhance with relevant code samples, diagrams, or images
- Link to reputable sources for further reading
- For security topics, include CVSS scores and mitigation strategies

#### Formatting
- Use clear headings, subheadings, bullet points, and numbered lists
- Structure content for a reading time of 6-9 minutes (minimum 1,400 words, ideally 1,400-2,100 words)
- Use analogies and real-world examples to simplify complex concepts
- Maintain a conversational tone to engage readers

#### Visual Elements
- Include a header image at the top of the post
- Add relevant images throughout (approximately one per major section)
- Source images only from copyright-free websites like:
  - Unsplash, Pexels, Pixabay, Wikimedia Commons, NASA Image Gallery
- Provide alt text for all images for accessibility

#### Conclusion
- Summarize main points and reinforce critical insights
- Include a call to action for readers
- Suggest related resources, repositories, or further reading

### Step 3: Format Your Content (Optional)

While the conversion script handles basic formatting, you can enhance your drafts:

- Use standard Markdown formatting in your content
- Use # for main title (added automatically)
- Use ## for section headings
- Use * or - for bullet points
- Use `backticks` for inline code
- Use ```language for code blocks

### Step 4: Run the Conversion Process

You can choose between two processing options:

#### Standard Processor (Legacy)

```bash
npm run process:posts
```

#### Enhanced Interactive Processor (Recommended)

The enhanced processor offers more features and better control:

```bash
npm run process:posts:enhanced
```

Or run in batch mode (processes all posts without confirmation):

```bash
npm run process:posts:batch
```

The enhanced processor will:
- Extract title and content intelligently from various formats
- Generate comprehensive frontmatter with SEO metadata
- Set publication dates with smart spacing between posts
- Create SEO-friendly slugs from titles
- Suggest relevant tags based on comprehensive content analysis
- Select appropriate featured images using the image mapping system
- Auto-generate descriptions from content
- Clean up citation artifacts and formatting
- Convert to proper Markdown format with standardized templates
- Move processed files to `new_posts/processed/`
- Provide interactive confirmation before writing files

You'll be guided through the process with clear prompts and previews of changes.

### Step 5: Review and Customize

1. Check the generated files in `src/posts/`
2. Make any manual adjustments needed:
   - Edit tags if necessary
   - Replace suggested images
   - Add or modify code examples
   - Add diagrams or custom content

## Post Features

### Featured Images

Each blog post includes a featured image at the top. The system automatically selects an appropriate image based on the post tags, title keywords, or explicitly defined image in the frontmatter.

#### Automatic Image Selection

The system will attempt to find the most relevant image in this order:

1. If the post has `image` defined in its frontmatter, it will use that specific image
2. If the post has tags that match known image categories, it will use the corresponding image
3. If the post title contains specific keywords, it will map to the appropriate category
4. If no match is found, it will use the default blog image

#### Specifying Custom Images

To specify a custom image for a post, add the following to your frontmatter:

```yaml
---
title: My Blog Post
image: blog/custom/my-image.jpg 
image_alt: Description of my custom image
---
```

The image path should be relative to the `assets/images/` directory.

#### Available Image Categories

The system supports the following image categories:

- `ai`: Artificial Intelligence
- `security`: Cybersecurity
- `cloud`: Cloud Computing
- `ethics`: AI Ethics
- `transformer`: Transformer Architecture
- `pizza`: Pizza Calculator
- `cryptography`: Encryption and Cryptography
- `quantum`: Quantum Computing
- `edge`: Edge Computing
- `hpc`: High-Performance Computing
- `rag`: Retrieval Augmented Generation
- `prompt`: Prompt Engineering
- `containers`: Container Technologies
- `resilience`: System Resilience
- `llm`: Large Language Models

#### Adding New Image Categories

To add new image categories, edit the file at `src/_data/config/blog/images.json`. Add new entries to both the `image_mapping` and `keyword_mapping` sections.

Then download the corresponding images by running:

```bash
npm run build:blog-images
```

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
- Discuss trade-offs and limitations when presenting technologies
- Provide links to related articles or documentation at the end