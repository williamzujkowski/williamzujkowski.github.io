# Contributing to William Zujkowski's Personal Website

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run any tests and ensure your code works as expected
5. Commit your changes: `git commit -m "Add your descriptive commit message"`
6. Push to your branch: `git push origin feature/your-feature-name`
7. Create a Pull Request against the main repository

## Development Setup

```bash
# Clone the repository
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io

# Install dependencies
npm install

# Run the application in development mode
npm run dev

# Or using the CLI utility
./scripts/bin/dev.sh serve
```

## Pull Request Guidelines

- Provide a clear description of the changes in your PR
- Include any relevant issue numbers in your PR description
- Make sure your code passes any existing tests
- Add tests for new features when applicable
- Update documentation if necessary

## Adding Blog Posts

### Option A: Automated Blog Post Processing

1. Create a file in the `new_posts/` directory using either:

   - A `.txt` file with the title on the first line
   - A `.md` file with an H1 header or front matter for the title

2. Run the processing script:

   ```bash
   # Using npm script
   npm run process:posts

   # Or using the CLI utility
   ./scripts/bin/content.sh blog:process
   ```

3. The script will format the post with proper frontmatter, schedule it appropriately, add tags, and place it in `src/posts/`.

### Option B: Manual Blog Post Creation

1. Create a new Markdown file in the `src/posts/` directory
2. Follow the naming convention: `YYYY-MM-DD-post-title.md`
3. Include frontmatter at the top of the file:
   ```
   ---
   title: Your Post Title
   date: YYYY-MM-DD
   description: A brief description of your post
   tags: ["tag1", "tag2"]
   image: /assets/images/blog/your-post-image.jpg
   ---
   ```
4. Write your content using Markdown

See [BLOG-WORKFLOW.md](docs/guides/BLOG-WORKFLOW.md) for more details.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
