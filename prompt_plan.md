Below is a detailed blueprint for the project, followed by a series of iterative, granular prompts designed to guide a code-generation LLM. Each prompt builds on the previous work, ensuring that every piece of code is integrated and thoroughly tested. The prompts are small enough to be implemented and tested safely but big enough to move the project forward incrementally.

---

## Step 1: Overall Blueprint

1. **Project Initialization & Setup**
   - Create the repository and initialize a Node.js project.
   - Set up the directory structure and install dependencies (11ty, plugins, linters, etc.).

2. **Core Configuration & Global Data**
   - Configure 11ty with a basic `.eleventy.js` file.
   - Create global site metadata and theme settings in `_data/site.yml`.

3. **Layout & Template Foundation**
   - Build the foundational Nunjucks layouts and partials (header, footer).
   - Create basic page templates for “About,” “Blog,” “Resume,” “Curated Links,” and “404.”

4. **Section-Specific Implementations**
   - **Blog:** Markdown posts with YAML front matter, pagination, TOC generation, social sharing, RSS feed.
   - **Resume:** A dedicated page with dynamic rendering from Markdown and structured data.
   - **About:** A single-page biography that adheres to Brutalist design.
   - **Curated Links:** A YAML/JSON data-driven page with client-side filtering.

5. **Styling & Asset Management**
   - Implement Brutalist design principles using custom CSS (OKLCH colors, strong typography).
   - Set up assets: images (with lazy-loading and modern formats), fonts, and minimal JavaScript for interactions.

6. **Plugin & Feature Integrations**
   - Configure eleventy plugins (eleventy-img, Prism, eleventy-plugin-rss, sitemap, navigation, etc.).

7. **Testing & Deployment Pipeline**
   - Write automated tests (accessibility, performance, link checking) and integrate them into GitHub Actions.
   - Create a GitHub Actions workflow for linting, building, testing, version tagging, and deploying to GitHub Pages.

8. **Documentation**
   - Create a detailed README with an overview, directory structure, local dev setup, and deployment instructions.

---

## Step 2: Iterative Breakdown into Chunks

The project will be built in the following iterative chunks:

1. **Repository & Project Initialization:**
   - Set up the repository, initialize Node.js, install 11ty, and create the basic folder structure.

2. **11ty Core Configuration & Global Data:**
   - Create `.eleventy.js` and `_data/site.yml` to configure the build process and global settings.

3. **Layouts & Partials Setup:**
   - Develop the base layout (`default.njk`) and common partials (header and footer).

4. **Core Pages Creation:**
   - Build basic pages for About, Blog index, Resume, Links, and the custom 404 page using Markdown/Nunjucks templates.

5. **Blog Section Implementation:**
   - Write initial Markdown blog posts with YAML front matter.
   - Integrate pagination, social sharing buttons, TOC generation, and the RSS plugin.

6. **Resume Section Implementation:**
   - Create a resume page that uses Markdown and structured JSON/YAML for data, rendered dynamically.

7. **Curated Links Section Implementation:**
   - Develop a YAML (or JSON) file for curated links.
   - Create a template to display and filter these links.

8. **Styling and Assets:**
   - Set up CSS files following Brutalist design principles and integrate OKLCH colors and typography.
   - Configure image optimization (lazy-loading, modern formats) and minimal JavaScript for any interactions.

9. **Plugin Integration & Additional Features:**
   - Wire up plugins (eleventy-img, Prism, sitemap, navigation, etc.) within the 11ty configuration.
  
10. **Testing, CI/CD, and Deployment:**
    - Develop and integrate tests (linters, pa11y, link checkers).
    - Create a GitHub Actions workflow for CI/CD and deployment to GitHub Pages.

11. **Final Integration & Documentation:**
    - Wire all components together.
    - Write documentation (README) to cover setup, usage, and further contributions.

---

## Step 3: Detailed Iterative Prompts for a Code-Generation LLM

Each prompt below is tagged as a text prompt in markdown. They are structured to be run in sequence so that every implementation builds on the previous work.

---

### Prompt 1: Repository & Project Initialization

```text
# Prompt 1: Repository & Project Initialization

Please create a detailed initial setup for our 11ty-based personal website project. The setup should include:
1. Initializing a new Node.js project (with package.json).
2. Installing necessary dependencies, including 11ty and any initial plugins.
3. Creating the following directory structure:
   ```
   /src
     /_data
     /_includes
       /layouts
       /partials
     /assets
       /css
       /js
       /images
       /fonts
     /blog
     /resume
     /about
     /links
   .eleventy.js
   README.md
   ```
4. Include a basic .gitignore to ignore node_modules and build artifacts.

Ensure that this initial setup is simple and includes commands where necessary, so that it can be run and tested immediately.
```

---

### Prompt 2: 11ty Core Configuration & Global Data

```text
# Prompt 2: 11ty Core Configuration & Global Data

Please create the 11ty configuration file (.eleventy.js) to use Nunjucks as the templating engine. The configuration should:
1. Specify the input and output directories.
2. Set the directories for layouts and includes.
3. Add any basic plugin integrations if needed.

Additionally, create a global data file at /src/_data/site.yml that includes site metadata (title, tagline, description, baseUrl, language), social links, and theme settings (colors in OKLCH, typography).

Provide the full content for both .eleventy.js and site.yml.
```

---

### Prompt 3: Layouts & Partials Setup

```text
# Prompt 3: Layouts & Partials Setup

Please create the following template files using Nunjucks:
1. A base layout file at /src/_includes/layouts/default.njk that includes the HTML boilerplate, and references a header and footer partial.
2. A header partial (/src/_includes/partials/header.njk) that includes a simple navigation bar using the site navigation data from site.yml.
3. A footer partial (/src/_includes/partials/footer.njk) with a simple copyright.

Ensure that the header and footer are included in the default layout. Provide the complete content of these files.
```

---

### Prompt 4: Core Pages Creation

```text
# Prompt 4: Core Pages Creation

Please create the core pages for the site using Markdown (with YAML front matter) or Nunjucks templates. Create:
1. An About page (/src/about/index.md or .njk) with a brief biography.
2. A Blog index page (/src/blog/index.njk) that will list blog posts.
3. A Resume page (/src/resume/index.md) that will later render the resume content.
4. A Curated Links page (/src/links/index.njk) that will later display the curated links.
5. A custom 404 page (/src/404.njk).

Ensure each page has basic placeholder content and proper front matter for 11ty to process them.
```

---

### Prompt 5: Blog Section Implementation

```text
# Prompt 5: Blog Section Implementation

Please implement the initial functionality for the blog section:
1. Create a sample blog post in Markdown with YAML front matter (e.g., title, date, categories, tags) in /src/blog/.
2. Update the Blog index page to list blog posts using a Nunjucks template loop.
3. Integrate a basic pagination mechanism (if possible in this initial setup).
4. Include a placeholder for social sharing buttons.
5. Add configuration for the eleventy-plugin-rss to generate an RSS feed for the blog posts.

Provide the sample blog post file and the updated blog index template code.
```

---

### Prompt 6: Resume Section Implementation

```text
# Prompt 6: Resume Section Implementation

Please create the resume section:
1. Develop a resume page (/src/resume/index.md) with YAML front matter.
2. Include structured data (in Markdown and/or a referenced JSON/YAML file) that outlines work experience, skills, and projects.
3. Ensure that the resume page uses a Nunjucks layout to render the resume dynamically.

Provide the complete content for the resume page and any accompanying data file if used.
```

---

### Prompt 7: Curated Links Section Implementation

```text
# Prompt 7: Curated Links Section Implementation

Please create the curated links section:
1. Create a data file (e.g., /src/links/links.yml) that includes a sample list of links with categories, annotations, and descriptions.
2. Develop a Nunjucks template (/src/links/index.njk) that reads the links data and displays it in a list.
3. Add simple client-side filtering logic (or explain how templating can be used) so that links can be filtered by category.

Provide the content for the links data file and the template code.
```

---

### Prompt 8: Styling and Asset Setup

```text
# Prompt 8: Styling and Asset Setup

Please set up the styling for the site:
1. Create a CSS file at /src/assets/css/main.css that implements a Brutalist design with an OKLCH color palette and strong typography.
2. Add basic styles for layout (header, footer, content areas) and responsive design.
3. Include any necessary styles for lazy-loaded images and minimal JavaScript interactions if needed later.

Provide the full content for the main.css file.
```

---

### Prompt 9: Plugin Integration & Additional Features

```text
# Prompt 9: Plugin Integration & Additional Features

Please update the 11ty configuration (.eleventy.js) to integrate the following plugins:
1. eleventy-img for image optimization.
2. Prism for syntax highlighting.
3. eleventy-plugin-sitemap for generating a sitemap.
4. eleventy-navigation for managing the site navigation.
5. (Optional) A plugin or filter for generating a Table of Contents for long blog posts.

Provide the updated .eleventy.js content that includes these plugins and any necessary configuration.
```

---

### Prompt 10: Testing, CI/CD, and Deployment Setup

```text
# Prompt 10: Testing, CI/CD, and Deployment Setup

Please configure the project for testing and deployment:
1. Update package.json to include scripts for building the site, running linters, and executing accessibility (pa11y) and link-checking tests.
2. Create a GitHub Actions workflow file (e.g., .github/workflows/ci.yml) that:
   - Checks out the repository.
   - Caches dependencies.
   - Runs linting and testing steps.
   - Builds the site using 11ty.
   - Deploys the site to GitHub Pages on pushes to the main branch.
3. Ensure that the CI/CD pipeline is incremental, with tests running before any deployment.

Provide the full content for package.json scripts and the GitHub Actions workflow YAML.
```

---

### Prompt 11: Final Integration & Documentation

```text
# Prompt 11: Final Integration & Documentation

Please perform the final integration and write project documentation:
1. Wire all components together so that each section (About, Blog, Resume, Curated Links) uses the common layout and global data.
2. Run the 11ty development server to verify that all pages are rendered correctly.
3. Write a comprehensive README.md that includes:
   - An overview of the project.
   - Detailed instructions for local development and building the site.
   - Descriptions of the folder structure, technology stack, and design philosophy.
   - Guidelines for adding new content and updating configurations.
   - Information on the CI/CD workflow and testing procedures.

Provide the complete README.md content.
```

---

By following these iterative prompts, each stage of the project is built incrementally, tested early, and integrated properly with no orphaned code. This plan ensures a maintainable, performant, and modern website redesign using 11ty, adhering to best practices and Brutalist Web Design principles.