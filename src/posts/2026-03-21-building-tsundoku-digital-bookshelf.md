---
title: "Building a 3,500-Book Digital Library with Astro and Six APIs"
date: 2026-03-21
description: "How I built Tsundoku — a curated digital bookshelf with multi-source enrichment, free reading links, and a static-site architecture that serves 3,500+ books without a database."
tags: [astro, svelte, python, projects, reading]
author: William Zujkowski
---

The Japanese word *tsundoku* (積ん読) describes the habit of acquiring books and letting them pile up unread. I have this problem. So I built a website for it.

[Tsundoku](https://github.com/williamzujkowski/tsundoku) is a curated digital bookshelf — 3,534 books across 29 categories, with search, reading progress tracking, author pages, and free reading links. It's a static site built with Astro 6 and Svelte 5, backed by a Python enrichment pipeline that pulls from six different APIs.

## The Problem

I wanted a single place to browse my reading list that wasn't a spreadsheet, wasn't Goodreads, and didn't require me to trust a third-party service with my reading habits. I also wanted free reading links — if a book is in the public domain, link directly to Project Gutenberg or LibriVox.

## The Architecture

The site has two halves:

**Python enrichment pipeline** — takes a CSV of book titles and ISBNs, then enriches each entry from:
- **Open Library** — metadata, covers, subjects, first publish dates
- **Google Books** — descriptions, page counts, additional ISBNs
- **Wikipedia** — author biographies and portraits
- **Project Gutenberg** — free ebook links for public domain works
- **LibriVox** — free audiobook links
- **HathiTrust/WorldCat** — copyright status verification

The pipeline handles deduplication, conflict resolution between sources, and outputs a clean JSON dataset.

**Astro static site** — generates pages for every book, author, and category at build time. No database, no API calls at runtime. The entire 3,500-book library is a static site that loads instantly.

## What I Learned

**Data quality is the hard problem.** Six APIs give six different opinions about the same book. Open Library says "The Art of War" was published in -500, Google Books says 2003 (the translation). Wikipedia has three different Sun Tzu pages. The enrichment pipeline spends more code on conflict resolution than on API calls.

**Static sites can handle surprisingly large datasets.** 3,534 book pages + 1,615 author pages + 29 category pages = 5,178 pages generated in under 30 seconds. Astro's content collections make this feel effortless.

**Free reading links are a killer feature.** About 40% of the books link to free, legal reading options. Seeing "Read free on Project Gutenberg" next to a classic you've been meaning to read removes the last bit of friction.

## Try It

The repo is at [github.com/williamzujkowski/tsundoku](https://github.com/williamzujkowski/tsundoku). The enrichment pipeline is reusable — if you have a CSV of books, you can build your own digital bookshelf.
