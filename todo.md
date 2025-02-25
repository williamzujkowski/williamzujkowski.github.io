# TODO Checklist for 11ty-based Personal Website Redesign

This checklist outlines every task required to complete the project. Each task is broken down into small, manageable steps to ensure incremental progress with continuous testing and integration.

---

## 1. Repository & Project Initialization
- [x] **Create Repository & Initialize Project**
  - [x] Create a new repository on GitHub.
  - [x] Clone the repository locally.
  - [x] Run `npm init` to initialize a new Node.js project.
- [x] **Install Dependencies**
  - [x] Install 11ty: `npm install --save-dev @11ty/eleventy`
  - [x] (Later) Add additional plugins and linters.
- [x] **Set Up Directory Structure**
  - [x] Create `/src` folder.
    - [x] Create `/src/_data`
    - [x] Create `/src/_includes`
      - [x] Create `/src/_includes/layouts`
      - [x] Create `/src/_includes/partials`
    - [x] Create `/src/assets`
      - [x] Create `/src/assets/css`
      - [x] Create `/src/assets/js`
      - [x] Create `/src/assets/images`
      - [x] Create `/src/assets/fonts`
    - [x] Create `/src/blog`
    - [x] Create `/src/resume`
    - [x] Create `/src/about`
    - [x] Create `/src/links`
- [x] **Create Core Files**
  - [x] Create `.eleventy.js` at the root.
  - [x] Create `README.md` with project overview.
  - [x] Create a basic `.gitignore` (ignore `node_modules`, build artifacts, etc.).

---

## 2. 11ty Core Configuration & Global Data
- [x] **Configure 11ty**
  - [x] Write `.eleventy.js` to:
    - [x] Set input and output directories.
    - [x] Configure Nunjucks as the templating engine.
    - [x] Define directories for layouts and includes.
- [x] **Global Data File**
  - [x] Create `/src/_data/site.yml` with:
    - [x] Site metadata (title, tagline, description, baseUrl, language).
    - [x] Social links (GitHub, Twitter, LinkedIn, etc.).
    - [x] Theme settings (OKLCH colors, typography).
    - [x] Navigation mapping.

---

## 3. Layouts & Template Foundation
- [x] **Base Layout**
  - [x] Create `/src/_includes/layouts/default.njk`:
    - [x] Include HTML boilerplate.
    - [x] Reference header and footer partials.
- [x] **Header Partial**
  - [x] Create `/src/_includes/partials/header.njk`:
    - [x] Build a simple navigation bar using data from `site.yml`.
- [x] **Footer Partial**
  - [x] Create `/src/_includes/partials/footer.njk`:
    - [x] Add basic copyright.

---

## 4. Core Pages Creation
- [x] **About Page**
  - [x] Create `/src/about/index.md` (or `.njk`) with:
    - [x] YAML front matter (title, layout).
    - [x] Brief biography placeholder.
- [x] **Blog Index Page**
  - [x] Create `/src/blog/index.njk` with:
    - [x] Placeholder code to loop through blog posts.
- [x] **Resume Page**
  - [x] Create `/src/resume/index.md` with:
    - [x] YAML front matter.
    - [x] Basic resume content placeholder.
- [x] **Curated Links Page**
  - [x] Create `/src/links/index.njk` with:
    - [x] Placeholder for displaying curated links.
- [x] **Custom 404 Page**
  - [x] Create `/src/404.njk` with:
    - [x] A simple error message.
    - [x] A link back to the homepage.

---

## 5. Blog Section Implementation
- [x] **Sample Blog Post**
  - [x] Create a Markdown file in `/src/blog/` (e.g., `post1.md`) with:
    - [x] YAML front matter (title, date, categories, tags).
    - [x] Sample content and placeholder for a Table of Contents.
- [x] **Blog Index Enhancements**
  - [x] Update `/src/blog/index.njk`:
    - [x] Use a Nunjucks loop to list blog posts.
    - [x] Implement a basic pagination mechanism.
    - [x] Add a placeholder for social sharing buttons.
- [x] **RSS Feed Integration**
  - [x] Configure eleventy-plugin-rss in `.eleventy.js` to generate an RSS feed.

---

## 6. Resume Section Implementation
- [x] **Resume Content**
  - [x] Update `/src/resume/index.md` with:
    - [x] YAML front matter (title, layout).
    - [x] Structured resume data (work experience, skills, projects).
- [x] **Optional Structured Data File**
  - [x] Create an accompanying JSON/YAML file if needed for additional resume data.
- [x] **Dynamic Rendering**
  - [x] Ensure the resume page uses Nunjucks for dynamic rendering.

---

## 7. Curated Links Section Implementation
- [x] **Curated Links Data**
  - [x] Create `/src/links/links.yml` (or JSON) with:
    - [x] Sample links including categories, annotations, and descriptions.
- [x] **Curated Links Template**
  - [x] Update `/src/links/index.njk` to:
    - [x] Read and render the links data.
    - [x] Include basic client-side filtering logic or document templating-based filtering.

---

## 8. Styling and Asset Setup
- [x] **Main CSS File**
  - [x] Create `/src/assets/css/main.css` to:
    - [x] Implement Brutalist design principles.
    - [x] Use OKLCH color palette and strong typography.
    - [x] Define layout styles for header, footer, and content areas.
    - [x] Add responsive design media queries.
    - [x] Style lazy-loaded images and prepare for minimal JavaScript interactions.
- [x] **Organize Assets**
  - [x] Place images, fonts, and any JavaScript files in their respective directories.

---

## 9. Plugin Integration & Additional Features
- [x] **Update 11ty Configuration**
  - [x] Integrate the following plugins in `.eleventy.js`:
    - [x] `eleventy-img` for image optimization.
    - [x] `Prism` for syntax highlighting.
    - [x] `eleventy-plugin-sitemap` for generating a sitemap.
    - [x] `eleventy-navigation` for managing site navigation.
    - [x] (Optional) A plugin or custom filter for generating a Table of Contents.
- [x] **Test Plugin Configurations**
  - [x] Run the build process to verify plugin integrations.

---

## 10. Testing, CI/CD, and Deployment Setup
- [x] **Package Scripts**
  - [x] Update `package.json` to include scripts for:
    - [x] Building the site.
    - [x] Running linters (HTML, CSS, JavaScript).
    - [x] Running accessibility tests (using pa11y).
    - [x] Link-checking tests.
- [x] **GitHub Actions Workflow**
  - [x] Create `.github/workflows/deploy.yml` to:
    - [x] Checkout the repository.
    - [x] Cache dependencies.
    - [x] Run linting and testing steps.
    - [x] Build the site using 11ty.
    - [x] Deploy the site to GitHub Pages upon pushes to the `main` branch.

---

## 11. Final Integration & Documentation
- [x] **Wiring Components Together**
  - [x] Ensure all pages (About, Blog, Resume, Curated Links) use the common layout and global data.
  - [x] Test navigation and page linking across the site.
- [x] **Local Testing**
  - [x] Run the 11ty development server.
  - [x] Verify that every page renders correctly on various devices and browsers.
- [x] **Documentation**
  - [x] Update `README.md` with:
    - [x] Project overview and design philosophy.
    - [x] Detailed local development instructions.
    - [x] Explanation of folder structure and technology stack.
    - [x] Guidelines for adding new content and updating configurations.
    - [x] Description of CI/CD workflow and testing procedures.
