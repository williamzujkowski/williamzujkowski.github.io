# williamzujkowski.github.io

Personal website of William Zujkowski, built with [Eleventy](https://www.11ty.dev/) and hosted on GitHub Pages.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io

# Install dependencies
npm install

# Start development server
npm run serve
```

The site will be available at `http://localhost:8080/`

### Build for Production

```bash
npm run build
```

The static site will be generated in the `_site` directory.

## 📁 Project Structure

```
├── src/                    # Source files
│   ├── _includes/         # Templates and layouts
│   │   └── layouts/       # Page layouts
│   ├── _data/            # Global data files
│   ├── assets/           # CSS, JS, images
│   ├── pages/            # Static pages
│   ├── posts/            # Blog posts
│   └── index.njk         # Homepage
├── _site/                # Build output (git-ignored)
├── .eleventy.js          # Eleventy configuration
├── .github/workflows/    # GitHub Actions
├── .standards/           # Development standards (submodule)
└── package.json          # Dependencies
```

## 🛠️ Technologies

- **Static Site Generator**: Eleventy 2.0
- **Templating**: Nunjucks
- **Styling**: Vanilla CSS with CSS Custom Properties
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions
- **Standards**: Integrated via [standards repository](https://github.com/williamzujkowski/standards)

## 📝 Content Management

### Creating a New Post

1. Create a new Markdown file in `src/posts/`
2. Add front matter:

```yaml
---
title: Your Post Title
date: 2024-01-15
description: Brief description of your post
---
```

3. Write your content in Markdown
4. The post will automatically appear in the posts listing

### Adding a New Page

1. Create a new file in `src/pages/`
2. Use either Markdown (`.md`) or Nunjucks (`.njk`)
3. Set the layout and permalink in front matter

## 🚀 Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the `main` branch.

### Manual Deployment

1. Push changes to the `main` branch
2. GitHub Actions will build and deploy the site
3. View at https://williamzujkowski.github.io

## 🔧 Configuration

### Site Metadata

Edit `src/_data/site.json` to update:
- Site title
- Description
- Author information
- URL

### Eleventy Configuration

Modify `.eleventy.js` to:
- Add plugins
- Configure collections
- Set up filters
- Adjust build settings

## 📚 Standards Integration

This project follows the guidelines from the [standards repository](https://github.com/williamzujkowski/standards), which is included as a submodule at `.standards/`.

Key standards applied:
- Semantic HTML structure
- Accessible navigation
- Performance optimization
- Security best practices
- Automated testing and deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Live Site**: https://williamzujkowski.github.io
- **Standards**: https://github.com/williamzujkowski/standards
- **Eleventy Docs**: https://www.11ty.dev/docs/