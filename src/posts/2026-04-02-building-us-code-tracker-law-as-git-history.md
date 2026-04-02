---
title: "Building US Code Tracker: Federal Law as Git History"
date: 2026-04-02
description: "How I built an end-to-end pipeline that converts the United States Code from XML into a Git-versioned, searchable static site with 53,000+ sections and inline case law annotations."
tags: [civic-tech, open-data, typescript, astro, git]
image: https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1200&h=630
imageAlt: "Law books on library shelves"
author: William Zujkowski
---

The [Office of the Law Revision Counsel](https://uscode.house.gov/) publishes the entire United States Code as XML. Over 230 release points going back to 2013, each tagged to a specific Public Law. The data is open, the format is documented, and nobody has built a good diff viewer for it.

So I did. [US Code Tracker](https://civic-source.github.io/us-code-tracker/) converts OLRC's XML into Git-versioned Markdown, layers on case law citations from [CourtListener](https://www.courtlistener.com/), and serves it as a static site with full-text search. Every statutory change is a Git commit. Every `git blame` line traces back to the Public Law that enacted it.

## The Core Insight

Law changes the same way code changes. A bill passes, the Statutes at Large get a new entry, and the Office of the Law Revision Counsel updates the affected title of the U.S. Code. The OLRC publishes these as discrete "release points." Tagged releases of the law's source code.

Git was built for exactly this kind of tracked, attributed, diffable text. The missing piece was a pipeline to get from OLRC's XML to a Git repository with clean commits.

## Architecture

The project is a [Turborepo](https://turbo.build/) monorepo with five packages and a web app:

```
us-code-tracker/
├── packages/
│   ├── types/          # Zod schemas (ReleasePoint, PrecedentAnnotation)
│   ├── fetcher/        # OLRC endpoint scraper + SHA-256 caching
│   ├── transformer/    # USLM XML → Markdown with legal list formatting
│   ├── annotator/      # CourtListener API → sidecar YAML case law
│   └── pipeline/       # End-to-end orchestrator
└── apps/web/           # Astro 6 + Svelte 5 static site
```

Each package does one thing. The pipeline runs them in sequence: fetch, transform, annotate, commit. A [weekly cron job](https://github.com/civic-source/us-code-tracker/blob/main/.github/workflows/sync-law.yml) keeps it current.

## Fetching 230 Release Points

The OLRC publishes release points at `uscode.house.gov/download/priorreleasepoints.htm`. Each one links to ZIP files containing USLM XML for all 54 titles. The fetcher scrapes this page, parses the Public Law number and date from each entry, and downloads the XML ZIPs.

SHA-256 hashing provides idempotency. If a release point's hash matches the last run, it's skipped. The weekly cron job only processes new releases.

The fetcher exposes a CLI for standalone use and ships structured metrics: download counts, cache hits, error rates, and per-release timing.

## Transforming USLM XML to Markdown

[USLM](https://github.com/usgpo/uslm) (United States Legislative Markup) is an XML schema designed for legislative text. It handles the nested structure of federal law: titles contain chapters, chapters contain sections, sections contain subsections labeled `(a)(1)(A)(i)` and so on.

The transformer maps this tree to Markdown files at `statutes/title-{N}/chapter-{N}/section-{N}.md`. Each file gets Zod-validated YAML frontmatter with the title number, section number, chapter, classification, and the Public Law it's current through.

The tricky part is preserving legal list indentation. Federal statutes nest four or five levels deep with a specific labeling scheme:

```
(a) Top-level subsection
    (1) Paragraph
        (A) Subparagraph
            (i) Clause
```

The transformer maps USLM's `<level>` nesting to Markdown indentation and calculates the correct depth from the marker format. Golden snapshot tests against Title 18 (Crimes and Criminal Procedure) catch any formatting drift.

## Sidecar Case Law Annotations

Federal statutes don't exist in isolation. Courts interpret them, narrow them, and occasionally strike them down. The annotator queries the [CourtListener API](https://www.courtlistener.com/api/) for cases citing each section, prioritizing Supreme Court and appellate decisions over district courts.

Annotations live in sidecar YAML files at `annotations/title-{N}/section-{N}.yaml`. They never touch the statutory Markdown, keeping the Git history of Congressional actions clean. The schema tracks case name, citation, court level, date, holding summary, and impact classification (interpretation, unconstitutional, narrowed, historical).

This separation matters. If you `git blame` a statute line, you see the Public Law that enacted it. Not annotation noise from the case law layer.

## The Static Site

The frontend is [Astro 6](https://astro.build/) with [Svelte 5](https://svelte.dev/) islands, styled with [Tailwind CSS](https://tailwindcss.com/) and the typography plugin. It builds 56,000+ pages from the Markdown content collections.

Key components:

- **Statute reader.** Prose-styled legal text at 19px with 72ch max-width. Serif font for body text, sans-serif for navigation. Designed for extended reading.
- **Diff viewer.** A Svelte component that shows inline green/red diffs between release points, grouped by Congress. Static diff manifests with GitHub API fallback.
- **Precedent drawer.** On wide viewports (1440px+), case law annotations display as a persistent third column alongside the statute text. On smaller screens, it becomes a slide-out overlay.
- **Search.** [Pagefind](https://pagefind.app/) indexes the entire corpus at build time. Debounced input with keyboard navigation.
- **Chapter index.** Large chapters (50+ sections) show an index by default with on-demand full-text loading. This avoids multi-megabyte page loads.

The color system uses a warm-paper light mode and deep-navy dark mode with [WCAG AA](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) contrast ratios verified across all text colors.

## What I Learned

**XML parsing is the easy part.** The USLM schema is well-documented and the [Cheerio](https://cheerio.js.org/) library handles it without drama. The hard part is formatting decisions: how to indent nested legal lists, when to insert paragraph breaks, how to handle repealed sections that still appear in the XML with `[Repealed]` in their heading.

**Git as a database works for this use case.** 230 tagged release points, 53 titles, clean commit messages linking to Public Laws. `git log --follow` on a section file shows its complete legislative history. The data repository ([civic-source/us-code](https://github.com/civic-source/us-code)) is separate from the pipeline code, which keeps both clean.

**Static sites can handle 56,000 pages.** Astro with `--max-old-space-size=8192` builds the full corpus. [Pagefind](https://pagefind.app/) handles search without a server. The only dynamic content is the diff viewer's GitHub API fallback, and even that has static manifests as the primary source.

**Case law enrichment is the differentiator.** OLRC publishes the text. Other sites like [Cornell LII](https://www.law.cornell.edu/uscode) publish the text with better formatting. What this project adds is the Git history layer and the CourtListener case law linkage. Two things that make the law not just readable but traceable.

## Numbers

| Metric | Value |
|--------|-------|
| Release points indexed | 230+ (2013-present) |
| Titles covered | 53 of 54 |
| Searchable sections | 53,000+ |
| Annotated sections (Title 18) | 47 |
| Test count | 267 passing |
| Build output | 56,239 static pages |
| Weekly sync | Sunday 2 AM ET via GitHub Actions |

## Try It

The site is live at [civic-source.github.io/us-code-tracker](https://civic-source.github.io/us-code-tracker/). Browse any title, search for a term, click through to a section, and check the diff viewer to see how the text changed between Public Laws.

The code is open source under the [civic-source](https://github.com/civic-source) organization:

- [us-code-tracker](https://github.com/civic-source/us-code-tracker) — Pipeline and web app
- [us-code](https://github.com/civic-source/us-code) — The Git-versioned statutory data

The data is CC0 public domain. The code is Apache 2.0.
