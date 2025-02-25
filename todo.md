# TODO Checklist for 11ty-based Personal Website Redesign

This checklist outlines every task required to complete the project. Each task is broken down into small, manageable steps to ensure incremental progress with continuous testing and integration.

---

## 1. Repository & Project Initialization
- [ ] **Create Repository & Initialize Project**
  - [ ] Create a new repository on GitHub.
  - [ ] Clone the repository locally.
  - [ ] Run `npm init` to initialize a new Node.js project.
- [ ] **Install Dependencies**
  - [ ] Install 11ty: `npm install --save-dev @11ty/eleventy`
  - [ ] (Later) Add additional plugins and linters.
- [ ] **Set Up Directory Structure**
  - [ ] Create `/src` folder.
    - [ ] Create `/src/_data`
    - [ ] Create `/src/_includes`
      - [ ] Create `/src/_includes/layouts`
      - [ ] Create `/src/_includes/partials`
    - [ ] Create `/src/assets`
      - [ ] Create `/src/assets/css`
      - [ ] Create `/src/assets/js`
      - [ ] Create `/src/assets/images`
      - [ ] Create `/src/assets/fonts`
    - [ ] Create `/src/blog`
    - [ ] Create `/src/resume`
    - [ ] Create `/src/about`
    - [ ] Create `/src/links`
- [ ] **Create Core Files**
  - [ ] Create `.eleventy.js` at the root.
  - [ ] Create `README.md` with project overview.
  - [ ] Create a basic `.gitignore` (ignore `node_modules`, build artifacts, etc.).

---

## 2. 11ty Core Configuration & Global Data
- [ ] **Configure 11ty**
  - [ ] Write `.eleventy.js` to:
    - [ ] Set input and output directories.
    - [ ] Configure Nunjucks as the templating engine.
    - [ ] Define directories for layouts and includes.
- [ ] **Global Data File**
  - [ ] Create `/src/_data/site.yml` with:
    - [ ] Site metadata (title, tagline, description, baseUrl, language).
    - [ ] Social links (GitHub, Twitter, LinkedIn, etc.).
    - [ ] Theme settings (OKLCH colors, typography).
    - [ ] Navigation mapping.

---

## 3. Layouts & Template Foundation
- [ ] **Base Layout**
  - [ ] Create `/src/_includes/layouts/default.njk`:
    - [ ] Include HTML boilerplate.
    - [ ] Reference header and footer partials.
- [ ] **Header Partial**
  - [ ] Create `/src/_includes/partials/header.njk`:
    - [ ] Build a simple navigation bar using data from `site.yml`.
- [ ] **Footer Partial**
  - [ ] Create `/src/_includes/partials/footer.njk`:
    - [ ] Add basic copyright.

---

## 4. Core Pages Creation
- [ ] **About Page**
  - [ ] Create `/src/about/index.md` (or `.njk`) with:
    - [ ] YAML front matter (title, layout).
    - [ ] Brief biography placeholder.
- [ ] **Blog Index Page**
  - [ ] Create `/src/blog/index.njk` with:
    - [ ] Placeholder code to loop through blog posts.
- [ ] **Resume Page**
  - [ ] Create `/src/resume/index.md` with:
    - [ ] YAML front matter.
    - [ ] Basic resume content placeholder.
- [ ] **Curated Links Page**
  - [ ] Create `/src/links/index.njk` with:
    - [ ] Placeholder for displaying curated links.
- [ ] **Custom 404 Page**
  - [ ] Create `/src/404.njk` with:
    - [ ] A simple error message.
    - [ ] A link back to the homepage.

---

## 5. Blog Section Implementation
- [ ] **Sample Blog Post**
  - [ ] Create a Markdown file in `/src/blog/` (e.g., `post1.md`) with:
    - [ ] YAML front matter (title, date, categories, tags).
    - [ ] Sample content and placeholder for a Table of Contents.
- [ ] **Blog Index Enhancements**
  - [ ] Update `/src/blog/index.njk`:
    - [ ] Use a Nunjucks loop to list blog posts.
    - [ ] Implement a basic pagination mechanism.
    - [ ] Add a placeholder for social sharing buttons.
- [ ] **RSS Feed Integration**
  - [ ] Configure eleventy-plugin-rss in `.eleventy.js` to generate an RSS feed.

---

## 6. Resume Section Implementation
- [ ] **Resume Content**
  - [ ] Update `/src/resume/index.md` with:
    - [ ] YAML front matter (title, layout).
    - [ ] Structured resume data (work experience, skills, projects).
- [ ] **Optional Structured Data File**
  - [ ] Create an accompanying JSON/YAML file if needed for additional resume data.
- [ ] **Dynamic Rendering**
  - [ ] Ensure the resume page uses Nunjucks for dynamic rendering.

---

## 7. Curated Links Section Implementation
- [ ] **Curated Links Data**
  - [ ] Create `/src/links/links.yml` (or JSON) with:
    - [ ] Sample links including categories, annotations, and descriptions.
- [ ] **Curated Links Template**
  - [ ] Update `/src/links/index.njk` to:
    - [ ] Read and render the links data.
    - [ ] Include basic client-side filtering logic or document templating-based filtering.

---

## 8. Styling and Asset Setup
- [ ] **Main CSS File**
  - [ ] Create `/src/assets/css/main.css` to:
    - [ ] Implement Brutalist design principles.
    - [ ] Use OKLCH color palette and strong typography.
    - [ ] Define layout styles for header, footer, and content areas.
    - [ ] Add responsive design media queries.
    - [ ] Style lazy-loaded images and prepare for minimal JavaScript interactions.
- [ ] **Organize Assets**
  - [ ] Place images, fonts, and any JavaScript files in their respective directories.

---

## 9. Plugin Integration & Additional Features
- [ ] **Update 11ty Configuration**
  - [ ] Integrate the following plugins in `.eleventy.js`:
    - [ ] `eleventy-img` for image optimization.
    - [ ] `Prism` for syntax highlighting.
    - [ ] `eleventy-plugin-sitemap` for generating a sitemap.
    - [ ] `eleventy-navigation` for managing site navigation.
    - [ ] (Optional) A plugin or custom filter for generating a Table of Contents.
- [ ] **Test Plugin Configurations**
  - [ ] Run the build process to verify plugin integrations.

---

## 10. Testing, CI/CD, and Deployment Setup
- [ ] **Package Scripts**
  - [ ] Update `package.json` to include scripts for:
    - [ ] Building the site.
    - [ ] Running linters (HTML, CSS, JavaScript).
    - [ ] Running accessibility tests (using pa11y).
    - [ ] Link-checking tests.
- [ ] **GitHub Actions Workflow**
  - [ ] Create `.github/workflows/ci.yml` to:
    - [ ] Checkout the repository.
    - [ ] Cache dependencies.
    - [ ] Run linting and testing steps.
    - [ ] Build the site using 11ty.
    - [ ] Deploy the site to GitHub Pages upon pushes to the `main` branch.

---

## 11. Final Integration & Documentation
- [ ] **Wiring Components Together**
  - [ ] Ensure all pages (About, Blog, Resume, Curated Links) use the common layout and global data.
  - [ ] Test navigation and page linking across the site.
- [ ] **Local Testing**
  - [ ] Run the 11ty development server.
  - [ ] Verify that every page renders correctly on various devices and browsers.
- [ ] **Documentation**
  - [ ] Update `README.md` with:
    - [ ] Project overview and design philosophy.
    - [ ] Detailed local development instructions.
    - [ ] Explanation of folder structure and technology stack.
    - [ ] Guidelines for adding new content and updating configurations.
    - [ ] Description of CI/CD workflow and testing procedures.
