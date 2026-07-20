---
title: "3,584 Books, and the Website I Built Instead of Reading Any of Them"
date: 2026-02-23
description: "Tsundoku is a static bookshelf for the 3,584 books I own and haven't read — Astro 7, Svelte islands, six primary sources plus a Wikidata backstop, no database. Plus a documentation bug I found while checking my own numbers."
tags: [astro, svelte, python, projects, reading]
author: William Zujkowski
---

The Japanese word *tsundoku* (積ん読) describes the specific habit of buying books and letting them stack up unread. I have this problem badly enough that the fix, apparently, was to build software. [Tsundoku](https://github.com/williamzujkowski/tsundoku) is a curated digital bookshelf — 3,584 books across 28 categories, 1,649 authors — enriched from six primary sources plus a Wikidata backstop, and served as a static site with no database behind it. The README states the project's mission more honestly than I could: "because buying books and not reading them is a lifestyle." I'm not going to try to improve on that line. I'm just going to explain what I built.

It's Astro 7 up front, Svelte 5 for the handful of things that need to be interactive, and a Python enrichment pipeline behind the scenes that turns a spreadsheet row into a book page with a cover, a description, a copyright determination, and — where one exists — a legal way to read it for free. No database, no backend, no accounts. A build step runs, generates several thousand HTML files, and then gets out of the way.

## Why I Built This

I keep a running list of books I've read, want to read, or found interesting enough to write down. It's a spreadsheet, and somewhere past 3,500 rows it stopped being an organizational tool and started being a monument to intent. Goodreads was the obvious alternative, and I didn't want it: no interest in the social features, no interest in Amazon holding my reading history. I wanted something I controlled, plus a feature Goodreads doesn't bother with — surfacing free, legal reading options for anything already in the public domain.

The constraints were simple. No database, no backend, no hosting bill beyond a static file server. Everything gets built once, at compile time, and shipped as flat files.

## The Numbers, and a Documentation Bug I Found While Checking Them

The current shape of the collection: 3,584 books, sorted into 28 categories, by 1,649 authors, tagged across 35 genres, a count that will have grown again by the time anyone reads this. 971 of those books link to a free Project Gutenberg edition, 702 to a LibriVox audiobook, 127 to a digitized HathiTrust copy: free, legal reading without buying the same book again, which is apparently a personal growth area.

I ran `gh api` against the repo while fact-checking this post, and the GitHub description still doesn't match reality: "essential works across 42 categories," when the actual count is 28. It's sitting in full public view, on the first thing anyone sees before they click through. It's tracked now as [tsundoku#228](https://github.com/williamzujkowski/tsundoku/issues/228), and the fix is one line.

## Six Sources, One Book Record

The interesting part of Tsundoku was never the website. It's the pipeline that takes a title and author and turns them into forty-some structured fields. Six sources do the work:

**Open Library** is the backbone — DDC/LCC classification, subjects, ISBNs, page counts, first-publish years, cover art. Free, keyless, and it gets the easy cases right without complaint.

**Google Books** fills what Open Library misses: descriptions, alternate ISBNs, categories. It's also the pipeline's lowest-trusted source, which is a polite way of saying it's the fallback, not the authority.

**Wikipedia** supplies author bios and portraits over the REST API — third-party-edited text, so the pipeline trusts it less than anything structured.

**Project Gutenberg**, reached through the [Gutendex](https://gutendex.com/) API rather than a raw catalog dump, supplies free reading links for public-domain titles, gated on a matched author surname and a fuzzy title check, so "The Art of War" doesn't accidentally link to a cookbook with a similar name.

**LibriVox** does the same job for free audiobooks, over its own JSON API, with the identical author-then-title matching discipline.

**HathiTrust** looks up digitized copies by OCLC number first, ISBN second, and gives the pipeline a better rights signal than most book metadata bothers with.

A seventh source has quietly joined since I first wrote this post: **Wikidata**, queried by SPARQL for year corrections, original publishers, awards, series data, and — the one I didn't expect — a book's screen and stage adaptations, pulled via the "based on" property. The pipeline is still six primary sources, plus Wikidata as a backstop, because Wikidata arrived to reinforce the other six rather than replace one of them. The headline aged before the rewrite did.

## When Six Sources Disagree

Six sources means six opinions about the same fact, and the actual engineering problem here was never the API calls: it was arbitrating them. Every field the pipeline touches carries a rank. `manual` edits sit at 100 and nothing overwrites those. Wikidata's cross-link via a book's own Open Library ID sits at 85. Open Library's first-edition consensus sits at 80. Wikidata reached by fuzzy search instead of a hard ID match drops to 50, because fuzzy matches are noisier and the pipeline knows it. Google Books sits at 35. Wikipedia's bio text, being the field most likely to have been edited by someone with an opinion, sits at 30. Untouched legacy data defaults to 0, so any tagged source can correct it on the next pass.

A field only gets overwritten by a strictly higher rank than whatever's already recorded against it. No merge conflicts, no queue of records to eyeball by hand after every run — just a lookup table that already knows Wikidata beats Google Books, and nothing beats a human.

## No Database, and a Reading Tracker That's Just a CSV

The build reads every book and author as a JSON file in an Astro content collection, validates it against a Zod schema, and generates a page for each one — 3,584 book pages, 1,649 author pages, 28 category pages, at minimum. Svelte 5 covers the five things that need real interactivity: search, the book grid, a random-book button, a share button, and the light/dark toggle. Everything else is HTML that existed before a reader asked for it.

Search isn't Pagefind, despite what I claimed the first time I wrote this post. It's a hand-rolled `search-index.json`, generated at build time and fetched on demand by the search modal, so the site ships one JSON file instead of embedding 3,584 books into every page's markup. The random-book button gets its own, smaller sibling index — just URL slugs — so picking a random book doesn't mean downloading the full search index first. That's the kind of optimization you only bother making once someone notices the random button feels laggy for no obvious reason.

Reading progress isn't `localStorage` either, which is also what I claimed originally. It's a CSV file, `data/reading-status.csv`, that's the single source of truth, merged into each book's JSON at build time. There's no button in the UI for marking a book "currently reading." You edit a spreadsheet and redeploy. It's either the most honest reading tracker I've ever used or proof I'll build almost anything to avoid clicking a toggle. Possibly both.

## What I Got Wrong the First Time

One self-criticism from the original version of this post didn't survive contact with the current code. I said category assignment was manual — one person eyeballing 3,500-odd books into 29 buckets. It isn't anymore. `recategorize.py` derives a category from a book's DDC or LCC classification first, and only falls back to tag heuristics when neither exists. Running it against the full collection collapsed the taxonomy from 29 buckets to 28 — the classifier merged categories a human curator had kept separate out of habit rather than any DDC/LCC signal. A book can still only live in one category, but a human isn't the one drawing the lines anymore.

Cover image quality is the gap that didn't close. Not every book gets a high-resolution scan, and the fallback chain — Wikidata's image, then Wikipedia's, then Open Library's editions, then Google Books — sometimes runs out of good options before it runs out of sources. That part hasn't changed since the first draft, and I'm not going to pretend it has.

## Numbers

| Metric | Value |
|---|---:|
| Books | 3,584 |
| Categories | 28 |
| Authors | 1,649 |
| Genre tags | 35 |
| Free Project Gutenberg links | 971 |
| Free LibriVox audiobook links | 702 |
| Free HathiTrust links | 127 |
| Primary sources | 6 (plus Wikidata as a backstop) |
| Provenance ranks | 0 (legacy) to 100 (manual) |
| Tests gated in CI | 530 (70 Vitest, 460 pytest) |

The repo is at [github.com/williamzujkowski/tsundoku](https://github.com/williamzujkowski/tsundoku), MIT-licensed, and the enrichment pipeline is reusable if you've got your own spreadsheet problem. I have 3,584 books I haven't read and a website that can tell me exactly which ones. Whether that counts as progress is a separate discussion, and not one I'm equipped to win.

## Sources

- [williamzujkowski/tsundoku](https://github.com/williamzujkowski/tsundoku) — the project this post is about; README, scripts, and issue tracker
- [tsundoku#228](https://github.com/williamzujkowski/tsundoku/issues/228) — the "42 categories" vs. 28 documentation mismatch referenced above
- [Open Library Search API](https://openlibrary.org/dev/docs/api/search) — primary classification and metadata source
- [Gutendex](https://gutendex.com/) — REST API wrapping the Project Gutenberg catalog
- [LibriVox API](https://librivox.org/api/info) — free audiobook lookup
- [HathiTrust Bib API](https://www.hathitrust.org/data/bib-api-basics/) — digitized copy and rights lookup
- [Wikidata Query Service](https://query.wikidata.org/) — SPARQL enrichment for year corrections, awards, and adaptations
