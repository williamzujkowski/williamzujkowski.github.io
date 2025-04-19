## Project Plan: Implementing CLAUDE.md Standards & Codebase Enhancements

**Goal:** Refactor the existing codebase to align with the standards outlined in `CLAUDE.md`, improve code organization, remove vestigial code, and enhance overall project manageability.

**Phase 1: Setup & Initial Cleanup (Foundation)**

1.  **Environment Setup & Verification:**
    - Ensure Node.js version 20+ and npm 10+ are used consistently[cite: 179].
    - Set up Python virtual environment and install dev dependencies (`pip install -e ".[dev]"`), although the primary stack seems Node.js based, `CLAUDE.md` mentions Python tooling[cite: 298]. Clarify if Python tooling (Black, isort, Flake8, Mypy, Pytest) is intended for Python scripts or if equivalent Node.js tools (e.g., Prettier, ESLint, Jest) should be used for JS/CSS/MD files[cite: 181, 298, 299].
    - Install and configure pre-commit hooks for automated style checks (either Python or JS tools)[cite: 298, 209].
2.  **Vestigial Code Removal:**
    - Review and remove files in `removed_posts/` if they are confirmed to be obsolete[cite: 15].
    - Delete backup files like `src/site.js.backup` and `src/site.json.backup`[cite: 16].
    - Audit `scripts/` and `tools/` directories for unused or outdated scripts, comparing against `docs/development/SCRIPTS.md`[cite: 241].
3.  **Basic Code Formatting:**
    - Run initial code formatting (e.g., Prettier for JS/CSS/MD, Black/isort if Python scripts exist) across the entire codebase to establish a baseline[cite: 209, 298].
4.  **Configuration Consolidation:**
    - Verify primary configuration files (`config/.eleventy.simple.cjs`, `config/postcss.config.cjs`, `config/tailwind.config.cjs`) are correctly referenced and used[cite: 179, 363].
    - Review the two Eleventy config files (`.eleventy.cjs` and `.eleventy.simple.cjs`) [cite: 14] – consolidate or clarify their distinct purposes (e.g., one for local dev, one for CI as suggested in `CLAUDE.md` [cite: 179]).
    - Examine `src/_data/config/` for potential consolidation of JSON files[cite: 15].

**Phase 2: Code Style & Structure Alignment**

1.  **File Naming Conventions:**
    - Audit all filenames; rename files to use kebab-case as specified[cite: 181].
    - Verify blog posts in `src/posts/` follow the `YYYY-MM-DD-title-with-hyphens.md` format[cite: 181].
2.  **Frontmatter Standardization:**
    - Review all posts and pages (`.md`, `.njk`) to ensure required frontmatter (title, date, layout, tags) is present[cite: 181].
    - Implement `eleventyNavigation` where appropriate for site navigation[cite: 181].
3.  **Template & Shortcode Usage:**
    - Replace manual image tags with the `{% image %}` shortcode, ensuring correct paths and descriptive alt text[cite: 181, 308].
    - Implement the `{% breadcrumbs page %}` shortcode on relevant pages[cite: 181].
4.  **Styling Implementation:**
    - Ensure styles primarily use Tailwind CSS utility classes[cite: 181], referencing `config/tailwind.config.cjs`[cite: 181].
    - Refactor custom CSS (`src/css/`) to follow the organizational structure outlined in `docs/development/CSS-ORGANIZATION.md` [cite: 194] or the optimized structure in `CSS-OPTIMIZATION.md`[cite: 189, 190], ensuring modularity (base, components, utilities).
    - Verify OKLCH color usage aligns with `docs/guides/THEME-SYSTEM.md`[cite: 316].
5.  **Markdown Formatting:**
    - Review markdown files (`.md`) for correct heading hierarchy (H1 for titles, H2/H3 for sections)[cite: 181].

**Phase 3: Documentation & Architecture**

1.  **Code Documentation:**
    - Add/update Google-style docstrings for public functions/methods/classes, especially in JavaScript (`src/js/`) and any Python scripts[cite: 211].
    - Add contextual comments for complex logic[cite: 211].
2.  **System Documentation:**
    - Review existing documentation in `docs/`[cite: 14].
    - Update or create architecture diagrams, data flow descriptions, and API documentation (if applicable) based on the current state[cite: 213].
    - Ensure `CLAUDE.md` itself is accurate and reflects any changes made[cite: 177].
3.  **Architectural Review:**
    - Analyze component boundaries and dependencies (e.g., between Eleventy, scripts, data sources)[cite: 215].
    - Refactor to improve separation of concerns (e.g., ensure data fetching logic is separated from presentation logic in templates)[cite: 215].
    - Review JavaScript organization against `docs/development/JS-ORGANIZATION.md`[cite: 214].
    - Review template structure against `docs/development/TEMPLATE-ORGANIZATION.md`[cite: 253].

**Phase 4: Security, Performance & Testing**

1.  **Security Hardening:**
    - Review input handling (e.g., search inputs, forms if any) for validation[cite: 220].
    - Check dependencies for known vulnerabilities (`npm audit`) and update them[cite: 243, 307].
    - Ensure sensitive information (API keys, etc., though none obvious in the snippet) is not hardcoded and handled securely[cite: 223].
2.  **Performance Optimization:**
    - Evaluate build times and identify bottlenecks.
    - Analyze asset sizes (CSS, JS, Images) and ensure optimization processes (`scripts/media/optimize-images.js`[cite: 249], `scripts/styling/optimize-css.js` [cite: 248]) are effective.
    - Assess data loading efficiency (review `scripts/data/smart-data-loader.js` usage [cite: 297]).
3.  **Testing Implementation:**
    - Implement or enhance the testing framework based on `docs/development/TESTING.md` [cite: 257] and the Testing Manifesto in `CLAUDE.md`[cite: 285].
    - Add unit tests for critical JavaScript utilities and build scripts[cite: 286].
    - Implement integration tests for the build process (`scripts/testing/verify-build.js` seems to exist)[cite: 1136].
    - Ensure template verification (`scripts/testing/verify-templates.js` seems to exist) is robust[cite: 1159].
    - Set up code coverage tracking and aim for defined targets (e.g., 85%+)[cite: 303].

**Phase 5: Final Review & Refinement**

1.  **End-to-End Build & Test:** Run the full build (`npm run build`) [cite: 179] and all tests (`npm test` or `pytest`) [cite: 179, 298] to ensure everything integrates correctly.
2.  **Code Review:** Conduct a final code review focusing on adherence to all `CLAUDE.md` standards.
3.  **Documentation Update:** Update all relevant documentation (`README.md`, `docs/`, `CLAUDE.md`) to reflect the final state of the project.
4.  **Cleanup:** Remove any temporary files, unused branches, or commented-out code.

**General Enhancements (Throughout the project):**

- **Scripting:** Improve clarity and maintainability of scripts in `scripts/` and `tools/`. Add comments and potentially consolidate related functionalities[cite: 15].
- **Error Handling:** Enhance error handling in build scripts and JavaScript components[cite: 230].
- **Organization:** Ensure the final directory structure is logical and follows the documented standards[cite: 180].

This plan provides a structured approach to aligning the codebase with the `CLAUDE.md` standards while improving its overall quality and maintainability. Remember to commit changes frequently with clear messages referencing the specific standard or task being addressed[cite: 246].
