Below is the comprehensive developer-ready specification for your 11ty-based personal website redesign:

---

# Comprehensive Developer Specification for 11ty-based Personal Website Redesign

## 1. Project Overview

This project involves updating the current personal website (hosted on GitHub Pages and originally built with custom HTML, CSS, and JavaScript) to a modern, maintainable, and performant site built using [11ty](https://www.11ty.dev/) with Nunjucks templating. The redesign will adhere to Brutalist Web Design principles using an OKLCH color palette and strong, beautiful typography.

## 2. Goals & Objectives

- **Maintainability & Content Management:** Improve overall maintainability and ease of content updates.
- **Enhanced Templating & SEO:** Leverage 11ty’s templating features for streamlined development and improved SEO.
- **Performance Gains:** Optimize asset loading (e.g., lazy loading images, modern image formats, and font loading improvements) for fast performance.
- **Responsive Design:** Ensure a consistent, user-friendly experience on both desktop and mobile devices.

## 3. Website Sections & Features

### 3.1 Blog Section
- **Content Features:**
  - **Post Categorization & Tagging:** Organize posts by categories and tags.
  - **Pagination:** Enable multi-page navigation for older posts.
  - **Search Functionality:** Allow users to search through posts.
  - **Social Sharing:** Include social sharing buttons for individual posts.
  - **RSS Feed:** Generate an RSS feed for subscribers.
- **Technical Implementation:**
  - Store blog posts as Markdown files with YAML front matter.
  - Utilize eleventy-plugin-rss for feed generation.
  - Integrate an automatic Table of Contents generator for longer posts.

### 3.2 Resume Section
- **Content Features:**
  - Showcase work experience, skills, and projects.
  - Provide the resume in multiple formats: Markdown, JSON, and optionally a downloadable PDF.
- **Technical Implementation:**
  - Create a dedicated `/resume` folder with content organized in Markdown (with YAML front matter) and JSON/YAML files for structured data.
  - Use templating to render the resume dynamically.

### 3.3 About Me Page
- **Content Features:**
  - Personal biography including hobbies, interests, and other personal details to enhance approachability.
  - A design that is true to Brutalist principles—raw, minimal decoration, and a focus on content.
- **Technical Implementation:**
  - A single Markdown file or Nunjucks template under `/about` that outlines your personal story.

### 3.4 Curated Links Page
- **Content Features:**
  - Display links organized by categories with annotations and descriptions.
  - Provide client-side filtering (using 11ty’s native templating features wherever possible) for ease of navigation.
- **Technical Implementation:**
  - Store links data in a structured format (JSON or YAML) within the repository.
  - Use Nunjucks to generate a page that renders and filters the curated links.

## 4. Design & Styling

- **Brutalist Web Design Guidelines:**
  - **Content-First:** Minimal decoration, raw presentation of content.
  - **Interaction:** Only hyperlinks and buttons are interactive (underlined hyperlinks, traditional button styling).
  - **Responsive:** The design must render well on all screen sizes.
  - **Typography & Color:** Implement OKLCH color palettes and strong typography. Use custom CSS (or minimal resets) to ensure content readability.
- **Assets Optimization:**
  - Implement lazy-loading for images.
  - Serve images in modern formats (e.g., WebP) when supported.
  - Optimize font loading with best practices (e.g., preload key fonts, use font-display strategies).

## 5. Architecture & Technology Stack

- **Static Site Generator:** 11ty
- **Templating Engine:** Nunjucks
- **Project Structure (suggested):**
  ```
  /src
    /_data
      site.yml           # Global configuration file
    /_includes
      layouts/           # Base layouts (e.g., default.njk, post.njk)
      partials/          # Reusable snippets (e.g., header.njk, footer.njk)
    /assets
      /images            # Images and media (with lazy-loading considerations)
      /fonts             # Font files and related assets
      /css               # Custom styles (Brutalist design-focused)
      /js                # JavaScript enhancements (minimal, for interactions like filtering)
    /blog
      post1.md           # Markdown posts with YAML front matter (includes TOC, categories, tags)
      post2.md
    /resume
      index.md           # Resume content in Markdown; additional JSON/YAML files as needed
    /about
      index.md           # About me content
    /links
      links.yml          # Curated links data (categories, annotations, descriptions)
    404.njk              # Custom 404 error page template
  .eleventy.js           # 11ty configuration file
  package.json           # Project dependencies and scripts
  README.md              # Project documentation
  ```
- **Content Migration:**
  - Develop scripts or manual processes to convert existing HTML content into Markdown (for blog posts, about page, resume).
  - Ensure proper YAML front matter is added to all content files for metadata (dates, categories, tags, etc.).

## 6. Data Handling

- **Global Configuration File:**
  - Create `_data/site.yml` to centralize site metadata, theming, SEO defaults, and navigation settings.
  - Example keys:
    ```yaml
    title: "Your Personal Site"
    tagline: "A Modern Brutalist Web Experience"
    description: "A personal website showcasing my blog, resume, and curated links."
    baseUrl: "https://yourusername.github.io/"
    language: "en"
    social:
      github: "https://github.com/yourusername"
      twitter: "https://twitter.com/yourusername"
      linkedin: "https://linkedin.com/in/yourusername"
    theme:
      colors:
        primary: "oklch(50% 0.1 120)"   # Example OKLCH values; adjust as needed
        secondary: "oklch(40% 0.15 240)"
      typography:
        header: "Your chosen header font, fallback to system sans-serif"
        body: "Your chosen body font, fallback to system serif"
    seo:
      defaultMeta:
        ogType: "website"
        twitterCard: "summary"
    navigation:
      - title: "Blog"
        url: "/blog/"
      - title: "Resume"
        url: "/resume/"
      - title: "About"
        url: "/about/"
      - title: "Links"
        url: "/links/"
    ```
- **Content Formats:**
  - Blog posts, about page, and resume content in Markdown.
  - Curated links data in YAML (or JSON) for easy templating and filtering.

## 7. Plugins & Custom Filters

Include and configure the following 11ty plugins:

- **eleventy-img:** For image optimization and responsive image handling.
- **Prism:** For syntax highlighting in blog posts or code snippets.
- **Automatic Table of Contents Generator:** Use an existing plugin or create a custom filter for generating TOCs in Markdown posts.
- **eleventy-plugin-rss:** For generating an RSS feed from blog posts.
- **eleventy-plugin-sitemap:** For automatically generating a sitemap to improve SEO.
- **eleventy-navigation:** For managing navigation across the site.

*Additional Note:* All plugin configurations (if applicable) should be centralized in the 11ty configuration file (`.eleventy.js`) and referenced in your global configuration when needed.

## 8. Global Configuration

Centralize duplicative settings in the `_data/site.yml` file as detailed above. This file will provide defaults for:
- Site metadata and social links.
- Theming parameters (OKLCH colors, typography, spacing, breakpoints).
- SEO defaults (meta tags, Open Graph, Twitter cards).
- Navigation mapping.
- Any plugin-specific default options.

## 9. Deployment Pipeline & GitHub Actions Workflow

### Trigger & Steps:
- **Trigger:** Workflow runs on pushes to the `main` branch.
- **Steps:**
  1. **Checkout Code:** Pull repository code.
  2. **Dependency Caching:** Cache Node modules (or other dependencies) to improve build times.
  3. **Linting & Testing:**
     - Run linters for HTML, CSS, and JavaScript.
     - Execute automated accessibility and performance testing using [pa11y](https://pa11y.org/).
     - Run link-checking tools to ensure no broken links are present.
  4. **Build Site:** Run the 11ty build command.
  5. **Version Tagging:** Automatically tag releases based on commits or pull request merges.
  6. **Deploy:** Deploy the generated site to GitHub Pages.
  7. **Preview Deployments (Optional):** Configure preview builds for pull requests to allow review before merging.

### Additional Testing Steps:
- **Automated Accessibility & Performance Testing:** Integrate pa11y to ensure compliance with accessibility standards.
- **Link Checking:** Implement a step (using tools like `broken-link-checker` or similar) to validate all site links.
- **Version Tagging:** Use a GitHub Action to automate semantic versioning and tagging based on commit history.

## 10. Error Handling Strategy

- **Custom 404 Error Page:**
  - Develop a `404.njk` template that follows Brutalist Web Design guidelines.
  - Include a clear, friendly message and a prominent link back to the homepage.
  - Ensure minimal decoration and raw, honest typography consistent with the overall design.

## 11. Testing Plan

- **Accessibility & Performance:**
  - Run pa11y tests as part of the CI workflow to catch any accessibility issues.
  - Optionally integrate Lighthouse CI for additional performance metrics.
- **Link Validation:**
  - Incorporate automated link-checking to detect and flag broken links during builds.
- **Visual & Functional Testing:**
  - Test the site on multiple devices (desktop and mobile) and browsers.
  - Manually verify that interactive elements (navigation, filtering on curated links, etc.) work as expected.
- **Versioning:**
  - Confirm that version tagging reflects changes accurately, providing a clear history of releases.

## 12. Documentation

- **README.md:**
  - Provide an overview of the project, including the purpose, technology stack, and design philosophy.
  - Document the directory structure and file organization.
  - Outline local development setup instructions (e.g., installing dependencies, running the local dev server).
  - Detail the content migration process (how to convert existing content into Markdown/YAML).
  - Explain the GitHub Actions workflow and deployment steps.
  - Include guidelines on how to add new content or update configurations.

## 13. Additional Considerations

- **Content Migration:** Develop or document scripts/processes to migrate existing content (blog posts, resume details, and the about page) from static HTML into the new Markdown and YAML-based formats.
- **Performance:** Continually monitor build times and site performance, leveraging caching and optimization plugins as needed.
- **Scalability:** Ensure that the design and architecture allow for easy addition of new sections or features in the future.

---

This specification provides a complete blueprint—from architectural decisions and data handling to deployment and testing—that a developer can use to begin implementing your modern, Brutalist-inspired personal website using 11ty.