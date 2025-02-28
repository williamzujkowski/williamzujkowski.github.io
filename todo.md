# Developer-Ready Specification for williamzujkowski.github.io

## Overview
A personal website for William Zujkowski built using GitHub, 11ty (Eleventy), GitHub Pages, and GitHub Actions. The site will employ Brutalist Web Design principles, emphasizing readability, simplicity, honesty, and performance.

## Primary Objectives
- A fun, aesthetically pleasing personal site.
- Showcase technical and non-technical blog content.
- Highlight personal projects.
- Curate and annotate interesting external links.
- Provide deeper insight into William’s personality and interests.

## Technology Stack
- **Static Site Generator:** 11ty (Eleventy)
- **Hosting & Deployment:** GitHub Pages
- **CI/CD:** GitHub Actions
- **CSS Framework:** Minimalist (e.g., Tachyons or Tailwind, aligned with Brutalist principles)
- **Fonts:**
  - Headings: Inter or IBM Plex Sans (sans-serif)
  - Body: Merriweather or IBM Plex Serif (serif)
- **Palette:** OKLCH-based blue and white
- **Dynamic Content:** API (NumbersAPI for daily historical facts)

## Website Structure

### Main Navigation
- Home
- Blog
- Projects
- Fun Links
- About

### Home Page
- Brief bio
- Profile photo
- Featured posts/projects (combination curated/automatic)
- Latest blog updates
- Quick links to main sections
- Dynamic daily historical fact fetched from NumbersAPI

### Blog Section
- Markdown-based content editing
- Metadata: tags/categories, publish dates, author (William), reading time estimates
- Brutalist typography and clear underlined links

### Projects Section
- Individual project cards
  - Project title
  - Screenshot/image
  - Brief project description
  - Links to live demo/source code (GitHub)

### Fun Links Section
- Categorized sections (bold headings)
- Bullet lists with concise annotations/explanations
- Links underlined clearly

### About Section
- Personal background, interests, professional journey, and skills
- Personal photos or illustrations
- Social media/contact links clearly underlined
- Whimsical, humorous, or personal anecdotes included

## SEO & Performance Optimization
### SEO
- Meta tags: Title, description, Open Graph tags
- Semantic HTML
- Human-readable URLs
- Sitemap.xml and robots.txt (auto-generated via 11ty)

### Performance
- Minimal JavaScript usage
- Optimized images (lazy loading, WebP)
- CDN utilization (GitHub Pages)
- Lightweight CSS framework
- Regular Lighthouse/PageSpeed audits

## Content Management
- Markdown files manually pushed to GitHub
- Structured directories:
  - `/blog`, `/projects`, `/fun-links`, `/about`
- Front-matter standardization and validation via GitHub Actions
- Branch strategy: `main` (production), feature branches (drafts/experiments)

## Backup & Maintenance
- Periodic repository backups (optional automated via GitHub Actions)
- Dependabot integration for dependency updates
- Regular broken link checking via GitHub Actions (lychee recommended)

## Analytics (Optional)
- Minimal, privacy-respecting analytics such as Plausible or GoatCounter

## Error Handling & Validation
- CI/CD GitHub Actions workflows must:
  - Validate Markdown front-matter
  - Check for broken internal/external links
  - Ensure images and assets are optimized correctly
  - Provide clear, actionable error messages

## Testing Plan
- Automated testing (GitHub Actions):
  - Markdown/front-matter validation
  - Link validation (lychee)
  - Image optimization checks
  - Lighthouse/PageSpeed performance metrics
- Manual testing:
  - Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
  - Mobile and responsive design testing
  - Accessibility checks (basic WCAG compliance: semantic HTML, readable contrast)

## Deployment Workflow
- Pushes to the `main` branch trigger automatic build/deployment via GitHub Actions
- Draft content managed via `draft: true` in Markdown front matter (excluded from production)

## Out of Scope
- GDPR/cookie compliance (no data collection)
- Extensive client-side JavaScript interactivity

## Developer Deliverables
- GitHub repository configured with 11ty project setup
- Clearly structured README.md with setup, build, deploy instructions
- Pre-configured GitHub Actions for validation, testing, deployment

---

# todo.md

## Initial Setup
- [ ] Initialize Eleventy (11ty) project structure
- [ ] Configure directories and basic layout structure
- [ ] Integrate CSS framework (Tachyons/Tailwind)
- [ ] Set up Brutalist typography and responsive layouts

## Content and Layout Implementation
- [ ] Build reusable templates for main navigation and page layouts
- [ ] Set up content directories (`/blog`, `/projects`, `/fun-links`, `/about`)
- [ ] Configure Markdown front-matter standards
- [ ] Populate Home page with bio, photo, featured content, and latest blog posts
- [ ] Integrate NumbersAPI for dynamic daily historical facts

## SEO and Performance
- [ ] Add SEO-friendly meta tags and Open Graph tags
- [ ] Implement sitemap.xml and robots.txt generation
- [ ] Configure image optimization and lazy loading
- [ ] Conduct initial Lighthouse/PageSpeed audits

## Advanced Sections
- [ ] Develop individual project cards with images, descriptions, and links
- [ ] Curate and annotate Fun Links content
- [ ] Complete About page with personal content and social/contact links

## CI/CD and Validation
- [ ] Set up GitHub Actions workflow for automatic deployments
- [ ] Implement Markdown and front-matter validation
- [ ] Add link validation and image optimization checks

## Testing and Maintenance
- [ ] Perform cross-browser compatibility and responsive testing
- [ ] Validate accessibility standards
- [ ] Set up regular dependency updates with Dependabot
- [ ] Schedule regular backups and broken link checks

---

**End of Specification**

