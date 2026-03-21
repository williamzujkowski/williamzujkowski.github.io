---
title: "From Paper to Font File: Building an Open-Source Handwriting Digitizer"
date: 2026-03-09
description: "How Handwright turns a scanned worksheet into a custom .ttf font — OpenCV glyph extraction, potrace vectorization, and fonttools assembly. Local-first, no cloud required."
tags: [python, opencv, projects, fonts, privacy]
author: William Zujkowski
---

I wanted to send a handwritten note to someone, but my actual handwriting is terrible. So I did what any reasonable person would do: I spent a weekend building a tool that digitizes handwriting into fonts.

[Handwright](https://github.com/williamzujkowski/handwright) is an open-source handwriting font generator. You fill in a worksheet template, scan or photograph it, upload it, and the system extracts your glyphs into a custom `.ttf` font file. You can also generate realistic handwritten messages using your font.

## The Pipeline

The system has four stages, each with its own set of problems I didn't anticipate.

### Worksheet Generation

The system generates a printable PDF with guide boxes for every character — 26 uppercase, 26 lowercase, 10 digits, and about 30 punctuation/symbol characters. Each box has a faint baseline and cap height guide so your characters are consistently sized.

The template needs to be precise. If guide boxes are even slightly off-grid, the extraction stage misaligns. I went through three iterations of the template generator before the grid was reliable enough — the first version used HTML-to-PDF conversion which introduced sub-pixel rounding errors. Switching to direct PDF generation with `reportlab` fixed it.

### Glyph Extraction (OpenCV)

This is where most of the complexity lives. OpenCV processes the scanned image through several stages:

**Adaptive thresholding** handles uneven lighting — phone photos have shadows, desk lamp reflections, and color casts that simple binary thresholding can't handle. I use Gaussian adaptive thresholding with a block size of 31 pixels, tuned by trial and error on about 40 test scans.

**Contour detection** finds each character cell. The challenge is that the printed guide lines are thin but visible — they need to be detected as cell boundaries but not as part of the glyph. I solve this by detecting the grid first (Hough line transform), masking it out, then finding contours within each cell.

**Perspective correction** handles skewed scans. If someone photographs the worksheet at an angle, the grid cells become trapezoids. The pipeline detects the four corners of the worksheet and applies a perspective warp to produce a flat, rectangular image before extraction.

**Individual glyph extraction** crops each character with consistent padding. The padding normalization took several attempts — too little and ascenders/descenders get clipped, too much and the font has excessive whitespace. I settled on 15% padding on each side, with vertical padding adjusted based on detected ascender height.

The extraction fails gracefully on about 3% of cells — usually when someone's handwriting extends well outside the guide box or when two adjacent characters merge. Failed cells get a fallback to a default glyph rather than crashing the pipeline.

### Vectorization (potrace)

Extracted glyphs are bitmap images. Fonts need vector outlines. Potrace converts raster glyph images into smooth SVG paths.

The key parameter is `turdsize` (potrace's actual parameter name) — it controls the minimum area of features to keep. Too low and you get noise from paper texture. Too high and thin strokes disappear. I default to 2 for most characters but increase to 5 for punctuation marks, which tend to be small enough to trigger the noise filter at default settings.

Potrace also has an `alphamax` parameter controlling curve smoothness. Higher values produce smoother curves but can round off sharp corners that are part of someone's handwriting style. I keep it at 1.0 (the default), which preserves most stylistic details.

### Font Assembly (fonttools)

The SVG paths are assembled into a TrueType font using fonttools. This is the most straightforward stage, but the details matter:

- **Glyph metrics**: Each glyph needs correct advance width (how far the cursor moves after typing the character). I calculate this from the bounding box plus a fixed side bearing of 50 units. This works for most characters but produces too-loose spacing for narrow characters like `i` and `l`. A future version should use per-character kerning.

- **Character mapping**: The `cmap` table maps Unicode code points to glyphs. Standard Latin mapping is straightforward, but symbol characters (curly braces, tildes, at-signs) need explicit entries that are easy to miss.

- **Font metadata**: Name table entries (family name, version, license) are required for the font to work in all applications. Some older PDF renderers fail silently if the name table is incomplete.

The output is a standard `.ttf` file that works in any application — Word, Google Docs, Photoshop, web CSS `@font-face`. File sizes range from 30-80KB depending on glyph complexity.

## Why Local-First

Handwriting is biometric data. It's a unique identifier literally attached to your identity — your handwriting is as personal as your fingerprint in some forensic contexts. Uploading it to a cloud service means trusting that service with biometric data that can't be changed if it's compromised.

Handwright runs entirely locally. Docker Compose brings up the Next.js frontend and FastAPI backend on your machine. Your handwriting never leaves your computer. The tradeoff is you need Docker installed, which is a barrier for non-technical users. I'm considering a WebAssembly port of the OpenCV pipeline to eliminate the Docker requirement entirely.

## What Didn't Work

**Browser-based extraction.** My first attempt used TensorFlow.js to do glyph extraction in the browser. The model was accurate enough but painfully slow — 45 seconds per worksheet on a modern laptop. OpenCV on the server processes the same worksheet in under 2 seconds.

**Automatic kerning.** I tried generating kerning pairs automatically by analyzing common letter combinations (th, he, in, er, etc.) and measuring the visual gap. The results were inconsistent — it would produce tight kerning for "th" but loose kerning for "ty" because the algorithm couldn't account for glyph shape, only bounding boxes. Manual kerning tables would be better, but that's a significant UX problem for a tool meant to be zero-config.

**Handwriting variation.** Real handwriting varies — the same person writes the letter "a" slightly differently every time. A single glyph per character produces unnaturally uniform text. Adding variation (multiple glyphs per character, randomly selected) is on the roadmap but requires significant changes to the font assembly stage.

## The Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind — handles worksheet display, image upload, font preview
- **Backend**: Python, FastAPI — runs OpenCV pipeline, serves generated fonts
- **Engine**: OpenCV (extraction), Pillow (image preprocessing), potrace (vectorization), fonttools (TTF generation)
- **Deployment**: Docker Compose — single `docker compose up` brings up everything

## Try It

Clone the repo at [github.com/williamzujkowski/handwright](https://github.com/williamzujkowski/handwright), run `docker compose up`, and point your browser at `localhost:3000`. Print the worksheet, fill it in, photograph it, and you'll have a working font file in under a minute.
