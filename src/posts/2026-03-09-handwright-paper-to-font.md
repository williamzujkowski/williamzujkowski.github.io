---
title: "From Paper to Font File: Building an Open-Source Handwriting Digitizer"
date: 2026-03-09
description: "How Handwright turns a scanned worksheet into a custom .ttf font — OpenCV glyph extraction, contour vectorization, and fonttools assembly. Local-first, no cloud required."
tags: [python, opencv, projects, fonts, privacy]
author: William Zujkowski
---

I wanted to send a handwritten note to someone, but my actual handwriting is terrible. So I did what any reasonable person would do: I spent a weekend building a tool that digitizes handwriting into fonts.

[Handwright](https://github.com/williamzujkowski/handwright) is an open-source handwriting font generator. You fill in a worksheet template, scan or photograph it, upload it, and the system extracts your glyphs into a custom `.ttf` font file. You can also generate realistic handwritten messages using your font.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/handwright.png'); width: min(380px, 88%); aspect-ratio: 400/319; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">your handwriting, compiled</p>

## The Pipeline

The system has four stages, each with its own set of problems I didn't anticipate.

### Worksheet Generation

The system generates a printable PDF with guide boxes for every character — 26 uppercase, 26 lowercase, 10 digits, and 15 punctuation characters (with a further symbol set behind a flag). Each box has a faint baseline and cap height guide so your characters are consistently sized.

The template needs to be precise. If guide boxes are even slightly off-grid, the extraction stage misaligns. I went through three iterations of the template generator before the grid was reliable enough: the first version used HTML-to-PDF conversion which introduced sub-pixel rounding errors. Switching to direct PDF generation with `reportlab` fixed it.

### Glyph Extraction (OpenCV)

This is where most of the complexity lives. OpenCV processes the scanned image through several stages:

**Adaptive thresholding** handles uneven lighting — phone photos have shadows, desk lamp reflections, and color casts that simple binary thresholding can't handle. I use Gaussian adaptive thresholding — block size 51 when locating the page, 11 when pulling glyphs out of individual cells. The right value differs by scale, which took a while to work out.

**Contour detection** finds each character cell. The challenge is that the printed guide lines are thin but visible: they need to be treated as cell boundaries and not as part of the glyph. The worksheet solves this by construction rather than by vision — the cell geometry is fixed in millimetres, so once the page is deskewed against its printed alignment markers the cell boundaries are arithmetic, not a detection problem. Contours are then found within each computed cell.

**Perspective correction** handles skewed scans. If someone photographs the worksheet at an angle, the grid cells become trapezoids. The pipeline detects the four corners of the worksheet and applies a perspective warp to produce a flat, rectangular image before extraction.

**Individual glyph extraction** crops each character with consistent padding. The padding normalization took several attempts — too little and ascenders/descenders get clipped, too much and the font has excessive whitespace. I settled on 10% padding, applied isotropically. Per-character vertical padding tied to ascender height would be better and is not implemented.

Extraction fails on cells where handwriting runs well outside the guide box, or where two adjacent characters merge. Right now a failed cell passes its empty thresholded contents through rather than substituting a `.notdef` glyph, which is a gap worth closing — a missing character should look missing, not blank.

### Vectorization

Extracted glyphs are bitmap images. Fonts need vector outlines. Potrace converts raster glyph images into smooth SVG paths.

Vectorization goes through OpenCV's `approxPolyDP` — Ramer-Douglas-Peucker
polygon simplification on the extracted contour — and the resulting points are
emitted as straight `lineTo` segments.

That is worth being blunt about, because it is the biggest compromise in the
pipeline: **there are no Bézier curves in the output at all.** A handwritten
curve becomes a polyline dense enough to look curved at reading size and visibly
faceted if you scale it up. The epsilon on the simplification is the whole
quality knob — too tight and you carry paper-texture noise into the glyph, too
loose and thin strokes collapse.

Proper curve fitting (potrace does this well, and it is the obvious next step)
would fix it. It is on the list and it is not in the code.

### Font Assembly (fonttools)

The SVG paths are assembled into a TrueType font using fonttools. This is the most straightforward stage, but the details matter:

- **Glyph metrics**: Each glyph needs correct advance width (how far the cursor moves after typing the character). Right now every glyph is monospaced at the em width with a zero side bearing, which is the crudest thing that works. This works for most characters but produces too-loose spacing for narrow characters like `i` and `l`. A future version should use per-character kerning.

- **Character mapping**: The `cmap` table maps Unicode code points to glyphs. Standard Latin mapping is straightforward, but symbol characters (curly braces, tildes, at-signs) need explicit entries that are easy to miss.

- **Font metadata**: Name table entries (family name, version, license) are required for the font to work in all applications. Some older PDF renderers fail silently if the name table is incomplete.

The output is a standard `.ttf` file that works in any application — Word, Google Docs, Photoshop, web CSS `@font-face`. File size scales with glyph complexity — a polyline-heavy font is larger than a curve-fitted one would be.

## Why Local-First

Handwriting is personal data you cannot rotate. It is not a fingerprint — forensic handwriting comparison has been criticised on validity grounds for decades, and treating the two as equivalent overstates it. But it is distinctive, it is attached to you, and unlike a password you cannot issue yourself a new one. Uploading it to a cloud service means trusting that service with biometric data that can't be changed if it's compromised.

Handwright runs entirely locally. Docker Compose brings up the Next.js frontend and FastAPI backend on your machine. Your handwriting never leaves your computer. The tradeoff is you need Docker installed, which is a barrier for non-technical users. I'm considering a WebAssembly port of the OpenCV pipeline to eliminate the Docker requirement entirely.

## What Didn't Work

**Automatic kerning.** I tried generating kerning pairs automatically by analyzing common letter combinations (th, he, in, er, etc.) and measuring the visual gap. The results were inconsistent: it would produce tight kerning for "th" but loose kerning for "ty" because the algorithm couldn't account for glyph shape, only bounding boxes. Manual kerning tables would be better, but that's a significant UX problem for a tool meant to be zero-config.

**Handwriting variation.** Real handwriting varies — the same person writes the letter "a" slightly differently every time. A single glyph per character produces unnaturally uniform text. Adding variation (multiple glyphs per character, randomly selected) is on the roadmap but requires significant changes to the font assembly stage.

## The Stack

- **Frontend**: Next.js 16, TypeScript, Tailwind — handles worksheet display, image upload, font preview
- **Backend**: Python, FastAPI — runs OpenCV pipeline, serves generated fonts
- **Engine**: OpenCV (extraction), Pillow (image preprocessing), potrace (vectorization), fonttools (TTF generation)
- **Deployment**: Docker Compose — single `docker compose up` brings up everything

## Try It

Clone the repo at [github.com/williamzujkowski/handwright](https://github.com/williamzujkowski/handwright), run `docker compose up`, and point your browser at `localhost:3000`. Print the worksheet, fill it in, photograph it, and you'll have a working font file in under a minute.

## Sources

- [Handwright](https://github.com/williamzujkowski/handwright) — the project this post is about
