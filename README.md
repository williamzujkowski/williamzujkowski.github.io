# My Personal Website

A modern personal website built with [11ty](https://www.11ty.dev/), GitHub Actions, and GitHub Pages.

## Features

- 🚀 Fast static site using the 11ty static site generator
- 📱 Fully responsive design that works on all devices
- 🎨 Clean, modern interface with dark mode support
- 📝 Blog section with formatting and syntax highlighting
- 🖼️ Portfolio showcase for your projects
- 🔗 Curated links collection page
- 🤖 Automated deployment via GitHub Actions
- 🔒 Secure defaults and best practices

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (LTS version recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [Git](https://git-scm.com/)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/my-personal-website.git
   cd my-personal-website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Visit `http://localhost:8080` to see your site.

## Customization

### Site Configuration

Edit the `src/_data/site.js` file to update your site's information:

```javascript
module.exports = {
  title: "My Personal Website", // Your site title
  description: "A personal website for my projects, thoughts, and curated links", // Site description
  author: "Your Name", // Your name
  url: "https://your-username.github.io", // Your site URL
  // ...more configuration options
};
```

### Adding Content

#### Blog Posts

Create new blog posts in the `src/posts/` directory as Markdown files. Follow the naming convention `YYYY-MM-DD-title.md` and include the necessary frontmatter:

```markdown
---
title: Your Blog Post Title
description: A brief description of your post
date: 2025-03-01
tags:
  - tag1
  - tag2
---

Your post content goes here...
```

#### Projects

Add new projects in the `src/projects/` directory as Markdown files with frontmatter:

```markdown
---
title: Your Project Title
description: A brief description of your project
date: 2025-01-15
image: /assets/images/projects/your-project.jpg
tags:
  - tag1
  - tag2
---

Project content goes here...
```

#### Links

Update the `src/_data/links.json` file to add your curated links:

```json
{
  "categories": [
    {
      "name": "Category Name",
      "items": [
        {
          "title": "Link Title",
          "url": "https://example.com",
          "description": "Link description",
          "date": "2025-01-01"
        }
      ]
    }
  ]
}
```

### Styling

The main CSS file is located at `src/assets/css/style.css`. You can modify this file to change the site's appearance.

## Deployment

This site is set up to automatically deploy to GitHub Pages whenever you push changes to the `main` branch. The GitHub Actions workflow file is located at `.github/workflows/deploy.yml`.

To set up GitHub Pages deployment:

1. Push your repository to GitHub
2. Go to your repository settings
3. Under "Pages", select "GitHub Actions" as the source
4. The site will be available at `https://your-username.github.io`

## Adding Custom Domain

To use a custom domain:

1. Update the `url` field in `src/_data/site.js` with your domain
2. Create a file called `CNAME` in the `src` directory with your domain name
3. Update your DNS settings according to [GitHub's documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.