# William Zujkowski's Personal Website

A modern, minimalist personal website built with [11ty](https://www.11ty.dev/) and deployed to GitHub Pages.

## Features

- **Blog** - Share thoughts and tutorials on web development and technology
- **Resume** - Professional experience and skills
- **About** - Personal information and background
- **Links** - Curated collection of useful resources

## Technology Stack

- **Static Site Generator**: [11ty (Eleventy)](https://www.11ty.dev/)
- **Templating**: Nunjucks
- **Styling**: Custom CSS with OKLCH color space
- **Deployment**: GitHub Actions to GitHub Pages
- **Version Control**: Git

## Development

### Prerequisites

- Node.js (v18 or newer)
- npm

### Setup

1. Clone this repository
2. Install dependencies:

```bash
npm install
```

### Development Server

Start the development server:

```bash
npm start
```

This will start a local server at `http://localhost:8080`.

### Quality Assurance

Run the QA script to check for issues:

```bash
./qa.sh
```

### Build

Build the site for production:

```bash
npm run build
```

The built site will be in the `_site` directory.

## Project Structure

```
/src                  # Source files
  /_data              # Global data files
  /_includes          # Templates and partials
    /layouts          # Layout templates
    /partials         # Reusable components
  /assets             # Static assets
    /css              # Stylesheets
    /js               # JavaScript files
    /images           # Images
    /fonts            # Fonts
  /blog               # Blog posts
  /resume             # Resume page
  /about              # About page
  /links              # Links page
.eleventy.js          # 11ty configuration
.github/workflows     # GitHub Actions CI/CD configuration
```

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch.

## License

MIT
