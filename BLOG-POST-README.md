# Blog Post Automation System

We've created a streamlined process for adding new blog posts to the website with proper formatting, standardized metadata, and automatic scheduling.

## Features

- **Automated Conversion**: Transforms raw text or markdown files into properly formatted blog posts
- **Supports Multiple Formats**: 
  - Text files (.txt) with title on first line
  - Markdown files (.md) with H1 header, front matter, or filename as title
- **Intelligent Date Spacing**: Schedules posts 10-14 days apart from each other
- **Automated Tagging**: Suggests relevant tags based on content analysis
- **Image Selection**: Recommends appropriate feature images for each post
- **Code Formatting**: Preserves code blocks with proper syntax highlighting
- **ASCII Diagrams**: Supports ASCII art diagrams for technical illustrations
- **Markdown Enhancement**: Improves formatting with proper headers, lists, and links
- **Content Guidelines**: Provides detailed guidance for creating engaging technical content

## How It Works

1. **Write Content**: Create `.txt` or `.md` files in the `new_posts/` directory with your content
2. **Follow Guidelines**: Use `Prompts/blog-guidelines.md` for content structure best practices
3. **Run the Processor**: Use `npm run process:posts` to transform all new posts
4. **Posts Are Enhanced**: Posts get converted to proper markdown with all necessary frontmatter
5. **Automatic Scheduling**: Dates are assigned sequentially from the most recent post
6. **Original Files Preserved**: Processed source files move to `new_posts/processed/`

## Directory Structure

```
/
├── new_posts/               # Where you place raw posts
│   └── processed/           # Where processed raw posts are stored
├── Prompts/
│   ├── blogpost.prompt      # Complete prompt for generating blog posts
│   └── blog-guidelines.md   # Content guidelines for creating effective posts
├── src/
│   └── posts/               # Where the final formatted posts go
├── tools/
│   └── process-new-posts.js # The processing script
└── BLOG-WORKFLOW.md         # Detailed workflow instructions
```

## Sample Posts Created

The system has successfully processed these posts:

1. `2024-12-26-ai-learning-in-resource-constrained-environments.md` (13 days after previous post)
2. `2025-01-06-beyond-containers-the-future-of-application-deployment.md` (11 days after previous post)
3. `2025-01-19-designing-resilient-systems-for-an-uncertain-world.md` (13 days after previous post)

Each post includes:
- Proper frontmatter (title, date, layout, tags)
- Appropriate header image
- Enhanced formatting with proper header hierarchy
- Code blocks with syntax highlighting
- ASCII diagrams for technical concepts
- Improved bullet points and lists
- Reference links

## Content Guidelines

For detailed content guidelines, see `Prompts/blog-guidelines.md`. Key recommendations include:

- Target a reading time of 6-9 minutes (minimum 1,400 words, ideally 1,400-2,100 words)
- Include a header image and relevant images throughout
- Use analogies and real-world examples to simplify complex concepts
- Structure content with clear headings and logical organization
- Provide code examples with proper syntax highlighting
- Include trade-offs and limitations when presenting technologies
- End with a clear summary and further reading suggestions

## Getting Started

See `BLOG-WORKFLOW.md` for detailed instructions on how to use this system to create and manage blog posts.

Run this command to process new posts:

```bash
npm run process:posts
```

Then build the site to see your changes:

```bash
npm run build
```

## Using the Blog Post Prompt

The file `Prompts/blogpost.prompt` contains a comprehensive prompt for generating high-quality blog posts. This prompt can be used with AI assistants to help create structured content that follows our guidelines. It includes instructions for:

- Topic selection and audience targeting
- Content structure and formatting
- Visual enhancements and image selection
- Code integration and examples
- Citations and reference formatting

## Customization

The system can be customized by editing the `tools/process-new-posts.js` script:

- Change the date spacing between posts
- Add more tags to detect
- Add new image mappings for different topics
- Modify the enhancement logic for different formatting needs