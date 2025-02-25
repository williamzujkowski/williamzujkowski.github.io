# Personal Website

A personal website built with [11ty](https://www.11ty.dev/).

## Features

- Blog
- Resume
- About page
- Links page

## Development

### Prerequisites

- Node.js (v14 or newer)
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
```

## License

MIT
