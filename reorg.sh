#!/bin/bash

# Script to reorganize the Eleventy project structure
# Created on March 1, 2025

# Create necessary directories if they don't exist
mkdir -p src/static/scss
mkdir -p src/blog
mkdir -p src/projects
mkdir -p src/fun-links
mkdir -p src/about
mkdir -p src/images
mkdir -p _includes
mkdir -p .github/workflows

# Move layout files to _includes
echo "Moving layout files to _includes..."
if [ -d "_includes/layouts" ]; then
  cp -r _includes/layouts/* _includes/
fi
if [ -f "_includes/layout.njk" ]; then
  cp _includes/layout.njk _includes/
fi

# Move content files to src
echo "Moving content files to src directory..."

# Move index.html to src
if [ -f "index.html" ]; then
  cp index.html src/
fi

# Move blog content
if [ -d "blog" ]; then
  cp -r blog/* src/blog/
fi

# Move projects content
if [ -d "projects" ]; then
  cp -r projects/* src/projects/
fi

# Move fun-links content
if [ -d "fun-links" ]; then
  cp -r fun-links/* src/fun-links/
fi

# Move about content
if [ -d "about" ]; then
  cp -r about/* src/about/
fi

# Create SCSS file if it doesn't exist
if [ ! -f "src/static/scss/main.scss" ]; then
  echo "Creating main.scss file..."
  cat > src/static/scss/main.scss << 'EOL'
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Merriweather:wght@400;700&display=swap');

body {
  font-family: 'Merriweather', serif;
  margin: 0;
  padding: 0;
  background-color: #ffffff;
  color: #000000;
}

header {
  background-color: #007acc;
  color: #ffffff;
  padding: 1rem;
}

nav ul {
  list-style-type: none;
  padding: 0;
}

nav ul li {
  display: inline;
  margin-right: 1rem;
}

a {
  text-decoration: underline;
  color: #007acc;
}

a:hover {
  color: #005fa3;
}

button {
  background-color: #007acc;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

button:hover {
  background-color: #005fa3;
}

footer {
  text-align: center;
  padding: 1rem;
  background-color: #f1f1f1;
}

h1 {
  color: #333;
  text-align: center;
  padding: 20px;
}
EOL
fi

# Create GitHub Actions workflows
echo "Creating GitHub Actions workflow files..."
cat > .github/workflows/build.yml << 'EOL'
name: Build PR

on:
  pull_request:
    branches: ['master']

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: ['20']

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install packages
        run: npm ci

      - name: Run npm build
        run: npm run build
EOL

cat > .github/workflows/build-and-deploy.yml << 'EOL'
name: Build and Deploy

on:
  push:
    branches: ['master']

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: ['20']

    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install packages
        run: npm ci

      - name: Run npm build
        run: npm run build:prod

      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          deploy_key: ${{ secrets.ACTIONS_DEPLOY_KEY }}
EOL

# Update .eleventy.js
echo "Updating .eleventy.js configuration..."
cat > .eleventy.js << 'EOL'
const eleventyImg = require("@11ty/eleventy-img");

module.exports = function(eleventyConfig) {
    eleventyConfig.addPlugin(eleventyImg);
    
    // Create collections for blog posts, projects, and fun links
    eleventyConfig.addCollection("blog", function(collectionApi) {
        return collectionApi.getFilteredByGlob("src/blog/*.md");
    });
    
    eleventyConfig.addCollection("projects", function(collectionApi) {
        return collectionApi.getFilteredByGlob("src/projects/*.md");
    });
    
    eleventyConfig.addCollection("funLinks", function(collectionApi) {
        return collectionApi.getFilteredByGlob("src/fun-links/*.md");
    });

    // Set up BrowserSync to refresh on CSS changes
    eleventyConfig.setBrowserSyncConfig({
        files: './public/static/**/*.css',
    });

    // Add passthrough copy for static files
    eleventyConfig.addPassthroughCopy("src/images");
    
    // Return configuration object
    return {
        dir: {
            input: "src",
            output: "public",
            includes: "../_includes"  // Looking one directory up from src
        }
    };
};
EOL

# Create empty .nojekyll file for GitHub Pages
touch .nojekyll

# Update package.json scripts
echo "Updating package.json scripts..."
# This is a bit complex to do in a shell script without a JSON parser
# So we'll recommend manual editing

echo "=========================="
echo "Directory structure has been reorganized!"
echo "=========================="
echo "Please run the following commands to install dependencies and start the development server:"
echo "npm install"
echo "npm run start"
echo ""
echo "IMPORTANT: Make sure to update your package.json scripts section with the following:"
echo '
"scripts": {
  "watch:sass": "sass src/static/scss:public/static/css --watch",
  "build:sass": "sass src/static/scss:public/static/css",
  "build:sass:prod": "sass src/static/scss:public/static/css --style compressed",
  "watch:eleventy": "eleventy --serve",
  "build:eleventy": "ELEVENTY_ENV=development eleventy",
  "build:eleventy:prod": "ELEVENTY_ENV=production eleventy",
  "start": "npm run watch:eleventy & npm run watch:sass",
  "build": "npm run build:eleventy & npm run build:sass",
  "build:prod": "npm run build:eleventy:prod & npm run build:sass:prod"
}'