# Blog Post Content Guidelines

This document provides detailed guidelines for creating effective blog posts for [williamzujkowski.github.io](https://williamzujkowski.github.io). Use these guidelines alongside the workflow process described in `BLOG-WORKFLOW.md`.

## Audience

- **Target**: Craft content that appeals to technology enthusiasts.
- **Accessibility**: Begin with a concise summary to help beginners grasp key points.
- **Tone**: Maintain a conversational writing style to engage readers effectively.

## Topic Selection

- **Originality**: Ensure the subject matter hasn't been previously covered on the blog.
- **Clarity**: Define a clear objective (educate, tutorial, analyze developments).
- **Focus Areas**: Prioritize topics in AI, quantum computing, cybersecurity, cryptography, robotics, HPC, or science fiction.
- **Cutting-Edge Content**: Explore papers uploaded to arXiv within the last 30 days that align with focus areas:
  - Look for papers with high citation potential, novel methodologies, or breakthrough findings
  - Identify emerging trends, paradigm shifts, or unexpected connections between fields
  - Build upon existing literature while introducing new concepts or applications
  - Seek papers that bridge multiple disciplines for unique storytelling opportunities

## Content Development

### Structure

- Reading time: 6-9 minutes (minimum 1,400 words, ideally 1,400-2,100 words)
- Use clear hierarchical headings (H1 for title, H2 for sections, H3 for subsections)
- Organize with bullet points and numbered lists where appropriate

### Content Elements

- **Recent Developments**: Incorporate insights from recent advancements
- **Code Samples**: Include relevant code with proper formatting
- **Diagrams/Images**: Use visuals to explain complex concepts
- **Source Links**: Provide references to reputable sources
- **Security Details**: For vulnerabilities, include CVSS scores and mitigation strategies
- **Trade-offs**: Discuss limitations when presenting technologies
- **Examples**: Use analogies and real-world examples to simplify complex concepts

## Visual Guidelines

### Image Requirements

- Include a header image at the top of the post
- Add relevant images throughout (approximately one per major section)
- Ensure all visuals have descriptive alt text for accessibility

### Image Sources

Use images ONLY from these copyright-free websites:

- Unsplash (https://unsplash.com/)
- Pexels (https://www.pexels.com/)
- Pixabay (https://pixabay.com/)
- Wikimedia Commons (https://commons.wikimedia.org/)
- NASA Image Gallery (https://www.nasa.gov/multimedia/imagegallery/)
- StockSnap.io (https://stocksnap.io/)
- Kaboompics (https://kaboompics.com/)
- ISO Republic (https://isorepublic.com/)
- Burst by Shopify (https://burst.shopify.com/)
- Rawpixel (https://www.rawpixel.com/)

For each image, provide:

- Direct URL to the specific image
- Proper attribution if required by the source
- Descriptive alt text for accessibility
- Complete Markdown formatting

## Conclusion Structure

- **Summary**: Summarize main points and reinforce critical insights
- **Call to Action**: Encourage readers to apply knowledge or participate in discussions
- **Additional Resources**: Suggest relevant repositories or further reading materials

## Formatting Reference

### Code Blocks

````markdown
```javascript
function example() {
  console.log("This is example code");
}
```
````

### Images

```markdown
![Alt text describing the image](/assets/images/blog/image-name.jpg)
```

### Lists

```markdown
## Main Points

- First point
- Second point
  - Sub-point
  - Another sub-point
- Third point

1. First step
2. Second step
3. Third step
```

### Links

```markdown
[Descriptive link text](https://example.com)
```

## Process Integration

After writing content following these guidelines, use the post processing script described in `BLOG-WORKFLOW.md` to automatically format and integrate the post into the site structure.
