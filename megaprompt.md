# Cloud.gov Personal Site Audit & Iteration — williamzujkowski.github.io

You are a Claude-Swarm conducting a full-stack UX/UI, a11y, performance, and content audit of **https://williamzujkowski.github.io/** (all pages, subpages, blog posts, assets). Your job: **find issues → fix them → re-review** until we reach **no known issues** under the criteria below.

## Hard Requirements
1) **Follow repo process**: obey **CLAUDE.md**, CODEOWNERS, CONTRIBUTING, and any repo standards (commit format, branches, PR templates, lint rules).
2) **Readability first**: both **light** and **dark** modes must be highly readable. No low-contrast text anywhere. Comfortable line length/height, clean hierarchy, sufficient spacing.
3) **Modern & consistent**: visual language (colors, spacing, UI states) is coherent across all pages. 
4) **Accessible**: aim for WCAG 2.2 AA or better. Keyboard-only must work cleanly; visible focus ring; proper semantics.
5) **Responsive**: mobile → tablet → desktop tested. No overflow, squished columns, or layout jumps.
6) **Performance**: target Lighthouse ≥ 90 across Performance, Accessibility, Best Practices, SEO.
7) **Content hygiene**: consistent frontmatter, headings, ToC behavior, code block styling, link style, image handling.

## Known Issues To Prioritize (P0/P1)
- **Dark mode header shows white background** → must match dark theme.
- **Global contrast issues** in dark mode (links, subtle text, muted borders).
- **Sizing / hierarchy** issues (headings too close to body, small subheads).
- **ToC appears at the bottom** of blog posts → move **to top** inside an **accessible accordion**.
- **Inconsistent hover/focus states** and occasional invisible focus rings.
- **Images not responsive/lazy-loaded** (profile and post images).
- **Post metadata inconsistencies** (frontmatter formatting, excerpt length).

## Roles (spawn as parallel agents)
- **Lead UX** (owns look/feel, hierarchy, spacing, IA)
- **A11y Auditor** (WCAG 2.2 AA, semantics, keyboard, focus)
- **Frontend Engineer** (Tailwind/11ty, theme tokens, components)
- **Perf Engineer** (Lighthouse/CLS/LCP/JS/CSS budgets, image pipeline)
- **Content QA** (frontmatter, MD hygiene, headings/ToC/links)
- **Link & Asset Checker** (broken links, 404s, missing alt, missing sizes)
- **Design QA** (visual consistency across pages)

## Process (repeat until clean)
1) Crawl all pages (site map, collections, blog index). Snapshot **light/dark** and **mobile/desktop**.
2) Run: Lighthouse (mobile/desktop), axe-core/Pa11y, link checker, html-validate, markdownlint.
3) Create **Issue Log**: each item = ID, URL(s), Severity (P0–P3), Finding, Evidence (screenshot/HTML/CSS), Fix proposal, Acceptance criteria.
4) Batch fixes in **small PRs** by category (theme tokens, components, content hygiene, performance).
5) Re-run audits and update Issue Log. No regressions allowed.

## Deliverables each iteration
- **Issue Log** (markdown table + per-issue details)
- **Diff summary** (what changed, why)
- **Before/After screenshots** (light/dark, mobile/desktop)
- **Scores** (Lighthouse + axe/Pa11y counts)
- **Open risks** (if any)

## Implementation Guidance (11ty/Tailwind)
### Dark Mode Header
- Ensure header/container uses theme tokens and `dark:` variants. No hardcoded light backgrounds.
- Example (simplified):
  ```html
  <header class="bg-white/80 dark:bg-slate-900/80 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:supports-[backdrop-filter]:bg-slate-900/60 border-b border-slate-200/60 dark:border-slate-700">
    ...
  </header>
````

* Prefer design tokens (CSS variables set per theme) for colors, spacing, radii.

### Color Tokens (CSS variables)

```css
:root {
  --bg: #ffffff;
  --fg: #0f172a; /* slate-900 */
  --muted: #475569; /* slate-600 */
  --link: #2563eb; /* blue-600 */
  --link-hover: #1d4ed8; /* blue-700 */
  --border: #e2e8f0; /* slate-200 */
  --card: #ffffff;
}
:root.dark {
  --bg: #0b1220;      /* dark slate/blue-black */
  --fg: #e5e7eb;      /* slate-200 */
  --muted: #cbd5e1;   /* slate-300 */
  --link: #60a5fa;    /* blue-400 */
  --link-hover: #93c5fd; 
  --border: #1f2937;  /* slate-800 */
  --card: #0f172a;    /* slate-900 */
}
```

Bind tokens in Tailwind via `theme.extend.colors` or utility `var(--token)` classes.

### Contrast & Focus

* Enforce visible focus ring across all interactive controls:

  ```html
  <a class="underline decoration-transparent hover:decoration-current focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 dark:focus-visible:ring-blue-300 focus-visible:ring-offset-[var(--bg)]">Link</a>
  ```
* Use `focus-visible` and ensure offset contrasts in dark mode.

### Typography & Spacing

* Increase subhead size/weight and add spacing above sections:

  ```html
  <h2 class="mt-10 text-2xl font-semibold tracking-tight text-[var(--fg)]">...</h2>
  <p class="mt-4 leading-7 text-[var(--muted)]">...</p>
  ```
* Constrain line length: `prose prose-slate max-w-prose` (and `dark:prose-invert`).

### Blog ToC — Accessible Accordion at Top

* Generate ToC via markdown-it-anchor + markdown-it-toc-done-right or your current plugin.
* Render at top of article content inside `<details>` for progressive enhancement:

  ```html
  <nav aria-label="Table of contents" class="mb-6">
    <details class="group rounded-lg border border-[var(--border)] bg-[var(--card)] p-3">
      <summary class="cursor-pointer select-none font-medium text-[var(--fg)] focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 dark:focus-visible:ring-blue-300">
        Table of contents
      </summary>
      <div class="mt-3 prose prose-sm dark:prose-invert">
        <!-- Inject generated ToC markup here -->
        {{ content | toc }}
      </div>
    </details>
  </nav>
  ```
* If server-side ToC isn’t available globally, add a post layout hook to always include it when headings ≥ 2.

### Responsive Images (eleventy-img)

* Create a shortcode:

  ```js
  // .eleventy.js
  const Image = require("@11ty/eleventy-img");
  module.exports = function(eleventyConfig) {
    eleventyConfig.addNunjucksAsyncShortcode("img", async function(src, alt, sizes = "(min-width: 768px) 768px, 100vw") {
      let metadata = await Image(src, {
        widths: [320, 640, 960, 1280, 1920],
        formats: ["webp","jpeg"],
        urlPath: "/img/",
        outputDir: "./_site/img/",
      });
      let imageAttributes = { alt, sizes, loading: "lazy", decoding: "async" };
      return Image.generateHTML(metadata, imageAttributes);
    });
  };
  ```
* Replace `<img>` in templates/posts with `{% img "src/path.jpg", "Alt text" %}`.

### Frontmatter Baseline

```yaml
---
title: "Post Title"
description: "Short, human summary (≤160 chars)."
date: 2025-09-10
updated: 2025-09-23
tags: [post, category]
slug: post-title
draft: false
toc: true
canonical: https://williamzujkowski.github.io/posts/post-title/
image:
  src: /assets/post-title/cover.jpg
  alt: "Descriptive alt"
  width: 1280
  height: 720
seo:
  noindex: false
---
```

### Link Hygiene

* Absolute canonical where needed; ensure external links use `rel="noopener"` and have visible hover/focus.

### Lint & CI (suggested)

* **a11y**: `axe-core` or `pa11y-ci` against built site.
* **Links**: `linkinator` or `lychee`.
* **HTML**: `html-validate`.
* **MD**: `markdownlint`.
* **Images**: check for missing `alt`, width/height (or responsive sets), and oversized assets (> 250KB).

## Acceptance Criteria (stop conditions)

* Dark mode header/backgrounds are correct, no white blocks.
* No WCAG AA color contrast violations (spot checks + automated).
* ToC appears at top within accessible accordion on all posts with ≥ 2 headings.
* Lighthouse mobile & desktop ≥ 90 across all categories.
* Keyboard navigation & focus rings are consistent & visible.
* All images responsive + lazy-loaded; CLS stable.
* Frontmatter & metadata consistent across posts.
* No broken links. No console errors. No layout overflow.

## Reporting Format (every iteration)

1. **Scores**: Lighthouse (M/D), axe counts.
2. **Issue Log** (markdown table): ID | Severity | URL | Finding | Evidence | Fix | Status.
3. **Diff Summary**: PRs merged with highlights.
4. **Screenshots**: before/after light & dark, mobile & desktop.
5. **Open Items**: remaining issues + plan.

````

---

# ✅ Checklists (Operational)

## 1) Visual & Readability
- [ ] Header, nav, footer inherit theme tokens; no hardcoded light backgrounds in dark mode.
- [ ] Body text ≥ 16px, line-height ~1.6–1.8, max line length ~65–80ch.
- [ ] H1/H2/H3 hierarchy clearly distinct (+spacing above sections).
- [ ] Link/hover/focus states consistent and visible in light & dark.
- [ ] Spacing scale consistent (e.g., 4/8px steps or Tailwind scale).

## 2) Color & Contrast
- [ ] All text/interactive elements meet WCAG 2.2 AA contrast.
- [ ] Borders/dividers visible in dark mode.
- [ ] Accent colors harmonized; avoid neon on dark backgrounds unless high-contrast.

## 3) Layout & Responsive
- [ ] Mobile: no horizontal scroll; nav collapses cleanly; ToC accordion usable.
- [ ] Tablet/desktop grids align; gutters consistent.
- [ ] Cards: sufficient padding; consistent image aspect ratios; no cramped meta text.

## 4) Accessibility
- [ ] Proper landmarks: `header`, `nav`, `main`, `aside`, `footer`.
- [ ] Headings in order; no skipped levels for styling.
- [ ] Focus ring visible (`focus-visible`) for keyboard users.
- [ ] ToC in `<nav aria-label="Table of contents">` within `<details>`; summary is keyboard accessible.
- [ ] All images have informative `alt` (or empty alt for decorative).

## 5) Performance
- [ ] eleventy-img responsive sets; `loading="lazy"`, `decoding="async"`.
- [ ] No unoptimized hero images (budget each ≤ 250KB where reasonable).
- [ ] CSS/JS minimal; no unused heavy libs.
- [ ] Good LCP/CLS (no layout shifts on load).

## 6) Content Hygiene
- [ ] Frontmatter fields standard across posts.
- [ ] Titles, dates, slugs, canonicals consistent.
- [ ] ToC enabled where posts have ≥ 2 headings.
- [ ] Code blocks readable in both themes (check inline code contrast).

## 7) Tooling & Process
- [ ] CI runs pa11y/axe, link checker, markdownlint, html-validate.
- [ ] PRs small & themed; commit messages follow convention from CLAUDE.md.
- [ ] Screenshots attached to PRs (before/after).

---

# 🔍 Preliminary Review & Concrete Fixes

## Summary (my take)
- **Dark-mode header flashes/appears white**: background and border tokens not applied in dark mode, or a hardcoded light class is overriding. Fix with `dark:bg-*` and token-based colors on the header container; remove any inline or component-level hardcodes.
- **Contrast**: Link and muted text in dark mode need brighter tokens. Use `--link`/`--link-hover` and `--muted` per dark set above.
- **Hierarchy**: H2/H3 are too close to body text—boost size/weight and add `mt-10`/`mt-8` spacing.
- **ToC**: Currently at the bottom. Move to the top inside a `<details>` accordion (spec above) with a11y labels.
- **Focus rings**: Add `focus-visible:ring-2` across interactive elements and ensure ring contrasts on dark.
- **Cards & spacing**: Blog cards feel tight; increase padding (`p-5`/`p-6`), line-height for excerpts, and consistent meta spacing.
- **Images**: Make responsive with eleventy-img; lazy-load and provide multiple widths to drop LCP weight.
- **Metadata**: Normalize frontmatter (see template); ensure `toc: true` on posts that need it.

## Concrete Patches (ready to implement)

### 1) Header template (example)
```html
<header class="sticky top-0 z-40 border-b border-[var(--border)] bg-[var(--card)]/85 dark:bg-[var(--card)]/85 backdrop-blur supports-[backdrop-filter]:bg-[var(--card)]/60">
  <div class="mx-auto max-w-screen-lg px-4 py-3 flex items-center justify-between">
    <a href="/" class="font-semibold tracking-tight text-[var(--fg)] focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 dark:focus-visible:ring-blue-300">William Zujkowski</a>
    <nav class="flex items-center gap-4">
      <!-- nav links -->
      <a class="text-[var(--muted)] hover:text-[var(--fg)] underline decoration-transparent hover:decoration-current focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 dark:focus-visible:ring-blue-300 focus-visible:ring-offset-[var(--bg)]" href="/posts/">Posts</a>
      <a class="text-[var(--muted)] hover:text-[var(--fg)] underline decoration-transparent hover:decoration-current focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 dark:focus-visible:ring-blue-300 focus-visible:ring-offset-[var(--bg)]" href="/about/">About</a>
    </nav>
  </div>
</header>
````

### 2) Post layout — ToC at top in accordion

```njk
{% if toc and page.hasTOC %}
<nav aria-label="Table of contents" class="mb-6">
  <details class="group rounded-lg border border-[var(--border)] bg-[var(--card)] p-3">
    <summary class="cursor-pointer select-none font-medium text-[var(--fg)] focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 dark:focus-visible:ring-blue-300">
      Table of contents
    </summary>
    <div class="mt-3 prose prose-sm dark:prose-invert">
      {{ content | toc }}
    </div>
  </details>
</nav>
{% endif %}
```

### 3) Prose styling (tailwind typography)

```html
<article class="prose prose-slate dark:prose-invert prose-headings:scroll-mt-24 prose-a:underline prose-a:decoration-transparent hover:prose-a:decoration-current max-w-prose">
```

Increase heading spacing via utility wrappers:

```css
.prose :is(h2){margin-top:2.5rem}
.prose :is(h3){margin-top:2rem}
```

### 4) Link & focus utilities (apply globally)

```css
a, button, [role="button"], [tabindex]:not([tabindex="-1"]) {
  outline: none;
}
:where(a, button, [role="button"], [tabindex]:not([tabindex="-1"])):focus-visible {
  box-shadow: 0 0 0 2px var(--link);
}
```

### 5) eleventy-img shortcode (as above) and template usage

```njk
{% img "/assets/profile.jpg", "Portrait of William Zujkowski" %}
```

### 6) Frontmatter enforcement (lint aid)

* Add a simple build-time check to ensure required frontmatter keys exist; fail build if missing (`eleventy-plugin-frontmatter-validation` or custom prebuild script).

### 7) CI tasks (package.json scripts sketch)

```json
{
  "scripts": {
    "build": "eleventy",
    "serve": "eleventy --serve",
    "lint:md": "markdownlint '**/*.md' --ignore node_modules",
    "lint:html": "html-validate '_site/**/*.html'",
    "check:links": "linkinator '_site' --recurse --skip 'mailto:,tel:'",
    "a11y": "pa11y-ci",
    "audit": "npm run build && npm run lint:md && npm run lint:html && npm run check:links && npm run a11y"
  }
}
```

---

# 📋 Issue Log Starter (you can paste into a tracking doc)

| ID          | Sev | URL          | Finding                              | Evidence                      | Proposed Fix                                                                      | Owner    | Status |
| ----------- | --- | ------------ | ------------------------------------ | ----------------------------- | --------------------------------------------------------------------------------- | -------- | ------ |
| UI-001      | P0  | /\* (global) | Dark header shows white in dark mode | Header bg hardcoded/overrides | Apply tokenized bg + `dark:` variants on header container; remove light hardcodes | Frontend | Open   |
| UI-002      | P0  | Posts/\*     | ToC at bottom                        | DOM order/screens             | Move ToC to top inside `<details>` accordion with a11y labels                     | Frontend | Open   |
| A11Y-003    | P0  | /\*          | Focus rings inconsistent/invisible   | Keyboard tab walkthrough      | Add `focus-visible` ring classes globally; test keyboard flow                     | A11y     | Open   |
| COLOR-004   | P1  | /\* dark     | Low contrast links/muted text        | axe/Pa11y report              | Adjust dark tokens (`--link`, `--muted`, borders)                                 | UX       | Open   |
| TYPE-005    | P1  | Posts/\*     | Weak heading hierarchy/spacing       | Visual review                 | Increase H2/H3 size/weight and section `mt-*` spacing                             | UX       | Open   |
| PERF-006    | P1  | /\*          | Unoptimized images                   | LH LCP/transfer size          | Use eleventy-img pipeline; lazy-load; multi-width                                 | Perf     | Open   |
| CONTENT-007 | P2  | Posts/\*     | Frontmatter inconsistencies          | diff across posts             | Enforce template; add validation; normalize                                       | Content  | Open   |
| UI-008      | P2  | Blog cards   | Tight spacing / meta cramped         | screenshots                   | Increase padding, adjust line-height, set consistent aspect ratios                | UX       | Open   |

---

# 🧪 Swarm Run Plan (how to iterate)

**Round 1 (Discovery & Baseline)**

* Crawl, snapshot, run Lighthouse (M/D), axe/Pa11y, link checker.
* Populate Issue Log with evidence.

**Round 2 (Theme & A11y)**

* Fix header/dark tokens, add focus rings, raise contrast, apply typography spacing.
* Merge PRs; re-run audits.

**Round 3 (ToC & Content Hygiene)**

* Implement ToC accordion in post layout. Normalize frontmatter across posts.
* Re-run a11y + link checks.

**Round 4 (Images & Performance)**

* eleventy-img migration for large/static images, lazy-load, width sets.
* Re-run Lighthouse; address CLS/LCP.

**Round 5 (Polish & QA)**

* Card spacing, hover states, small visual tweaks.
* Final pass; ensure no regressions.

**Exit when** acceptance criteria met (see prompt).

---

# 🧭 Opinionated Notes (why this set of changes)

* Dark-mode header + global tokens eliminate white flashes and “two-theme drift”. Use variables so future palette changes are trivial.
* ToC at top within `<details>` gives fast navigation without dominating the layout; progressive enhancement and keyboard-friendly.
* Focus rings: non-negotiable. Invisible focus is an accessibility fail and a UX smell.
* eleventy-img is low-effort, high-impact for performance. It typically bumps LH scores and reduces jank.
* Frontmatter normalization makes future automation (feeds, SEO, sitemaps, cross-links) predictable.


