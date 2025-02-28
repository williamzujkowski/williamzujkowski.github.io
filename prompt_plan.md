Here's your structured, detailed, iterative blueprint, optimized for step-by-step implementation using a code-generation LLM. Each prompt is clearly defined, manageable in complexity, testable, and builds incrementally upon the last.

---

## Iterative Blueprint for williamzujkowski.github.io:

---

### Step 1: Initialize the Project with 11ty
```text
Generate the initial project structure using the Eleventy (11ty) static site generator, initializing it with npm. Set up a basic, clean folder structure:
- `/src` for source files
- `/src/_includes` for layouts and partials
- `/src/_data` for site-wide data
- `/public` as the output directory

Include an initial minimal README.md file with clear instructions for installing dependencies, running development servers, and building the site.

Test this step by building the initial project and confirming that a simple index page renders correctly in a local browser.
```

---

### Step 2: Implement Brutalist Typography and Layout
```text
Integrate the Tachyons CSS framework and the chosen fonts (Inter or IBM Plex Sans for headings, Merriweather or IBM Plex Serif for body). Configure CSS to match Brutalist Web Design principles:
- Minimal margins and padding
- Clear underlined hyperlinks
- Buttons clearly distinguished from hyperlinks
- Highly readable typography with clear font sizing and spacing

Test by rendering a simple placeholder home page, verifying the visual styling matches Brutalist guidelines and is fully responsive.
```

---

### Step 3: Build Basic Page Layout Templates
```text
Create reusable 11ty layout templates for Home, Blog, Projects, Fun Links, and About pages within `/src/_includes/layouts`.

Each layout should include:
- Semantic HTML structure
- Header navigation with clearly underlined links
- Footer with basic copyright
- Main content area structured for readability and clarity

Validate this step by generating dummy pages and manually reviewing layout consistency.
```

---

### Step 4: Implement Content Directories and Front Matter
```text
Set up structured content directories:
- `/src/blog`
- `/src/projects`
- `/src/fun-links`
- `/src/about`

Establish YAML front-matter conventions, including title, description, date, tags/categories, author, and draft status.

Use 11ty data files (`/src/_data`) to pull content into each section automatically.

Test by adding sample markdown files and confirming content renders correctly on local builds.
```

---

### Step 5: SEO and Performance Foundations
```text
Implement automatic SEO-friendly meta tags (title, description, Open Graph tags) using front matter data within the HTML head of each layout.

Set up sitemap.xml and robots.txt auto-generation using 11ty plugins.

Configure performance optimizations, such as image optimization (WebP format and lazy loading), using recommended 11ty image plugins.

Test performance using Lighthouse/PageSpeed and verify that the site scores highly for SEO and performance metrics.
```

---

### Step 6: Add Dynamic "Today in Obscure History" via NumbersAPI
```text
Integrate a simple JavaScript fetch to NumbersAPI to pull a dynamic historical fact based on the current date, displayed prominently on the Home page.

Implement basic JavaScript error handling, ensuring fallback content if API fails.

Test by confirming successful fetch and fallback scenarios on local builds.
```

---

### Step 7: Configure GitHub Actions CI/CD Pipeline
```text
Set up a GitHub Actions workflow for automated deployments:
- Triggered on pushes to the `main` branch
- Run npm install, build the 11ty site, and publish to GitHub Pages
- Include basic error notifications upon failure

Ensure this workflow runs smoothly by testing pushes to the repository and verifying automatic deployment to GitHub Pages.
```

---

### Step 8: Implement Content Validation and Error Handling via CI
```text
Extend the GitHub Actions workflow to include automated testing:
- Markdown front-matter validation
- Broken internal/external link checks using lychee
- Image optimization checks

Ensure clear actionable error messages are outputted if issues arise.

Test extensively with deliberate broken links, missing metadata, and large images to ensure robustness.
```

---

### Step 9: Integrate Featured Posts/Projects on Home Page
```text
Develop logic to display curated or recently published blog posts/projects prominently on the home page.

Implement data-driven selection, supporting a "featured" flag in markdown front matter for manual curation.

Test by marking content as featured and verifying correct display order and layout on local builds.
```

---

### Step 10: Finalize the Fun Links Section
```text
Create structured Fun Links markdown files with categories and annotated descriptions in front matter.

Render clearly delineated sections with bold headings, underlined links, and brief annotations.

Test by adding multiple categorized fun links and validating their correct rendering.
```

---

### Step 11: Complete the About Page
```text
Implement the About page with structured content:
- Narrative personal/professional background
- Photo/illustration integration
- Clear, semantic markup for readability
- Social media/contact links clearly underlined

Test visually for readability, responsiveness, and link functionality.
```

---

### Step 12: Final Integration and Comprehensive Testing
```text
Perform comprehensive integration testing:
- Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- Mobile and responsive design testing on various devices
- Validate accessibility (basic WCAG semantic HTML, contrast checks)
- Lighthouse and PageSpeed performance audits

Address any issues and ensure all site sections and features integrate smoothly and perform optimally.
```

---

## Preparation for LLM-driven TDD Prompts:

Each step above can now be converted into clearly defined prompts for a code-generation LLM. For example, starting with:

**Example prompt for step 1:**
```text
Generate code for initializing an Eleventy (11ty) project with a clean directory structure including `/src`, `/src/_includes`, `/src/_data`, and `/public`. Provide a clear README.md explaining setup, running the local server (`npm start`), and building the static site (`npm run build`). Include simple test instructions to verify the setup.
```

Follow this iterative, incremental pattern for all subsequent steps to generate robust, testable code for your personal website project.