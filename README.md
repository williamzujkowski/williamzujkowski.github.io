# William Zujkowski's Personal Website

A terminal-inspired personal website built with Python and [Textual](https://textual.textualize.io/), designed to work both as a TUI (Text User Interface) in the terminal and as a static website hosted on GitHub Pages.

## Features

- Home page with introduction and information
- Links page showing categorized links to resources, social profiles, and projects
- Blog page using Markdown for content
- Responsive design that works in both terminal and web browsers
- Configurable site-wide settings via TOML configuration
- Detailed logging with multiple log levels
- Built-in static site generation for GitHub Pages deployment

## Installation

```bash
# Clone the repository
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive Terminal Mode

Run the application interactively in your terminal:

```bash
# Run in development mode (default)
python main.py

# Set a specific environment (development or production)
python main.py --env production

# Set a specific log level
python main.py --log-level DEBUG
```

### Static Site Generation

Generate a static site for deployment to GitHub Pages:

```bash
python main.py --build --env production
```

This will create a `build` directory with static HTML, CSS, and JavaScript files that can be deployed to GitHub Pages.

## Configuration

The site is configured via the `site_config.toml` file. You can modify this file to customize:

- Site title and description
- Navigation links
- Blog settings
- Link categories and items
- Environment-specific settings

## Project Structure

- `main.py`: Main application entry point
- `site_config.toml`: Site configuration
- `styles.tcss`: Textual CSS styles
- `pages/`: Page modules
  - `home.py`: Home page
  - `links.py`: Links page
  - `blog.py`: Blog page
  - `placeholder.py`: Placeholder for future pages
- `utils/`: Utility modules
  - `navigation.py`: Navigation sidebar
  - `builder.py`: Static site builder
- `content/posts/`: Blog post markdown files
- `logs/`: Log files
- `build/`: Generated static site (when built)

## Dependencies

- Python 3.8+
- Textual
- Rich
- Tomli
- Tomli-w
- Markdown
- BeautifulSoup4

## License

MIT
