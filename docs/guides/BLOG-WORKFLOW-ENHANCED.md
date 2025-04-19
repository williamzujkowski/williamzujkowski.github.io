# Enhanced Blog Workflow Guide

This document outlines the improved blog post creation workflow that streamlines the process of creating, formatting, and publishing blog posts on the website.

## 1. Blog Post Creation

### Option 1: Using Templates (Recommended)

The enhanced workflow uses templates to generate consistent, well-structured blog posts:

1. **Choose a template type**
   The system currently supports these template types:

   - `base` - General technology post
   - `cybersecurity` - Security-focused content
   - `ai-ml` - Artificial intelligence and machine learning
   - `cloud-computing` - Cloud technologies and services
   - `quantum-computing` - Quantum computing topics
   - `devops` - DevOps practices and tools

2. **Create a new post draft**
   Create a `.md` or `.txt` file in the `new_posts/` directory. The simplest approach is to use a `.txt` file with:

   - The title on the first line
   - The content in the rest of the file

   Example `new_posts/my-new-ai-post.txt`:

   ```
   Understanding Large Language Models and Their Applications

   In this post, we'll explore how large language models work and their practical applications in various industries.

   Modern language models like GPT-4, Claude, and others have demonstrated remarkable capabilities...
   ```

3. **Process the post**
   Run the enhanced post processor:

   ```bash
   npm run process:posts:enhanced
   ```

4. **Review and edit**
   The processor will:

   - Detect the most appropriate template based on content
   - Add suitable tags based on content analysis
   - Schedule the post with an appropriate future date
   - Format the post with proper frontmatter
   - Save the processed post to `src/posts/`
   - Move the original file to `new_posts/processed/`

5. **Final edits**
   Open the generated post in `src/posts/` and:
   - Review and refine the content
   - Check and adjust tags if needed
   - Verify the selected image is appropriate
   - Add any additional sections required

### Option 2: Manual Creation with Frontmatter

You can also manually create posts with custom frontmatter:

1. Create a new markdown file in `src/posts/` with the naming format: `YYYY-MM-DD-post-title.md`

2. Add the required frontmatter:

   ```markdown
   ---
   title: Your Post Title
   date: 2025-05-15
   description: A brief description of your post
   tags:
     - primary-tag
     - secondary-tag
   image: /assets/images/blog/your-image.jpg
   layout: post.njk
   ---

   Your post content here...
   ```

## 2. Images for Blog Posts

### Topic-Specific Images

The system includes pre-configured topic images located in:

```
assets/images/blog/topics/
```

These images are organized by topic:

- `ai-ml.jpg` - Artificial intelligence/machine learning
- `cloud-computing.jpg` - Cloud technologies
- `cybersecurity.jpg` - Security topics
- `devops.jpg` - DevOps content
- `quantum.jpg` - Quantum computing
- ...and more

### Using Images in Posts

Images are referenced in the frontmatter:

```yaml
image: /assets/images/blog/topics/cybersecurity.jpg
```

For custom images, place them in `assets/images/blog/` and reference accordingly.

### Image Best Practices

1. **Size and Dimensions**

   - Blog header images: 1600x900px (16:9 ratio)
   - Keep file sizes under 250KB for performance
   - Use JPG format for photographs
   - Use PNG for diagrams or images with transparency

2. **Alternative Text**
   Always provide descriptive alt text in your image shortcodes:
   ```njk
   {% image "path/to/image.jpg", "Descriptive alt text about the image", "100vw" %}
   ```

## 3. Tags and Categories

### Using Tags Effectively

Tags help categorize content and improve discoverability. The template system automatically suggests tags based on content analysis.

Common tags include:

- `cybersecurity`
- `artificial-intelligence`
- `machine-learning`
- `cloud-computing`
- `devops`
- `quantum-computing`
- `programming`
- `serverless`
- `blockchain`

Best practices:

- Use 3-5 tags per post
- Include one primary topic tag
- Add more specific subtopic tags
- Consider adding technology-specific tags (e.g., `kubernetes`, `aws`, `tensorflow`)

## 4. Publishing Process

1. **Preview your post**
   Run the development server to preview:

   ```bash
   npm run dev
   ```

   Visit `http://localhost:8082/blog/` to see your post.

2. **Commit and push**
   Once satisfied with your post:

   ```bash
   git add src/posts/your-new-post.md
   git commit -m "Add new blog post on [topic]"
   git push
   ```

3. **Deployment**
   The site will automatically rebuild and deploy after pushing to the repository.

## 5. Post Maintenance

### Updating Existing Posts

1. Find the post markdown file in `src/posts/`
2. Make your changes
3. Commit and push the changes

### Removing Posts

1. Move the post from `src/posts/` to `removed_posts/`
2. Commit and push the changes

## Command Reference

| Command                          | Description                                         |
| -------------------------------- | --------------------------------------------------- |
| `npm run process:posts:enhanced` | Process new posts with the enhanced template system |
| `npm run process:posts`          | Process posts with the original processor (legacy)  |
| `npm run dev`                    | Start the development server to preview posts       |
| `npm run build`                  | Build the site including all posts                  |
