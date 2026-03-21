---
title: "From Paper to Font File: Building an Open-Source Handwriting Digitizer"
date: 2026-03-21
description: "How Handwright turns a scanned worksheet into a custom .ttf font — OpenCV glyph extraction, potrace vectorization, and fonttools assembly. Local-first, no cloud required."
tags: [python, opencv, projects, fonts, privacy]
author: William Zujkowski
---

I wanted to send a handwritten note to someone, but my actual handwriting is terrible. So I did what any reasonable person would do: I spent a weekend building a tool that digitizes handwriting into fonts.

[Handwright](https://github.com/williamzujkowski/handwright) is an open-source handwriting font generator. You fill in a worksheet template, scan or photograph it, upload it, and the system extracts your glyphs into a custom `.ttf` font file. You can also generate realistic handwritten messages in your font.

## How It Works

The pipeline has four stages:

### 1. Worksheet Generation

The system generates a printable worksheet with guide boxes for every character — uppercase, lowercase, digits, punctuation. You fill it in with a pen, then scan or photograph it.

### 2. Glyph Extraction (OpenCV)

OpenCV processes the scanned image:
- Adaptive thresholding to handle uneven lighting
- Contour detection to find each character cell
- Perspective correction for skewed scans
- Individual glyph extraction with padding normalization

This is where most of the complexity lives. Real-world scans are messy — shadows, wrinkles, slightly rotated pages. The extraction pipeline needs to be robust to all of that.

### 3. Vectorization (potrace)

Extracted glyphs are bitmap images. Fonts need vector outlines. Potrace converts raster glyph images into smooth SVG paths, with configurable smoothing parameters to balance accuracy against file size.

### 4. Font Assembly (fonttools)

The SVG paths are assembled into a TrueType font using fonttools. This sets up the glyph table, character mapping, kerning hints, and font metadata. The output is a standard `.ttf` file that works in any application.

## Why Local-First

Handwriting is biometric data. Uploading it to a cloud service means trusting that service with a unique identifier that's literally attached to your identity. Handwright runs entirely locally — Docker Compose brings up the Next.js frontend and FastAPI backend on your machine. Your handwriting never leaves your computer.

## The Stack

- **Frontend**: Next.js 15 + TypeScript + Tailwind
- **Backend**: Python + FastAPI
- **Engine**: OpenCV + Pillow + fonttools + potrace
- **Deployment**: Docker Compose (single `docker compose up`)

## Try It

The repo is at [github.com/williamzujkowski/handwright](https://github.com/williamzujkowski/handwright). Clone it, run `docker compose up`, and point your browser at `localhost:3000`. The worksheet template is generated in-browser.
