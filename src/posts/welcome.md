---
date: 2025-01-01
author: William Zujkowski
description: Build privacy-respecting sites with Eleventy—create fast, accessible static websites with zero tracking and excellent Core Web Vitals.
images:
  hero:
    alt: Building My Digital Garden with Eleventy - Hero Image
    caption: Visual representation of Building My Digital Garden with Eleventy
    height: 630
    src: /assets/images/blog/hero/welcome-hero.jpg
    width: 1200
  inline: []
  og:
    alt: Building My Digital Garden with Eleventy - Social Media Preview
    src: /assets/images/blog/hero/welcome-og.jpg
tags:
- web-development
- eleventy
- open-source
title: Building My Digital Garden with Eleventy
---
Welcome to my digital corner of the internet! After years of working in security engineering and incident response, I decided it was time to create a proper home for my thoughts, projects, and learnings. This site documents [my secure homelab journey](/posts/2025-04-24-building-secure-homelab-adventure/), development workflows, and technical experiments.

## The Journey to Eleventy

Like many engineers, I've had my share of personal websites over the years – from hand-coded HTML in the early days to various CMS platforms. But I wanted something different this time:

- **Complete control** over my content and how it's presented
- **Lightning-fast performance** without sacrificing functionality
- **Privacy-respecting** with no tracking scripts or third-party dependencies
- **Developer-friendly** workflow that gets out of my way

After evaluating options ranging from Next.js to Hugo, I landed on [Eleventy](https://www.11ty.dev/) Here's why:

## Why Eleventy Won Me Over

### 1. Simplicity Without Sacrificing Power
Eleventy generates static HTML with zero client-side JavaScript by default. What this means in practice is my site loads instantly, works on slow connections, and respects users' bandwidth. When I do need interactivity (like the dark mode toggle or search), I can add just what's necessary.

### 2. Data Cascade
One of Eleventy's killer features is its data cascade. I can define global data, directory data, and page-specific data that all merge intelligently. This made building features like automatic navigation and tag pages surprisingly straightforward.

### 3. Incredible Build Speed
My entire site builds in under 100ms. Coming from webpack-based tools, this feels like magic. Why it matters: fast builds mean I can iterate quickly and deploy confidently. Your mileage may vary depending on site complexity, but for my setup it's been consistently fast.

## What I've Built

This site is more than just a blog. It's:

- **A knowledge repository** – My [Resources](/resources/) page catalogs tools and references I've found invaluable
- **A professional portfolio** – The [About](/about/) section showcases my experience and projects
- **A learning platform** – Each blog post represents hours of research and hands-on experience
- **An experiment in web craft** – From the glass morphism effects to the responsive design, every detail is intentional

## Technical Highlights

Some features I'm particularly proud of:

- **Client-side search** that works offline and respects privacy
- **Automatic dark mode** that remembers your preference
- **Git-based timestamps** showing when content was last updated
- **Accessible navigation** with keyboard support and ARIA labels
- **Lightning performance** with perfect Lighthouse scores

## What's Coming Next

This site will evolve as I do. Expect content on:

- **Security engineering** – Real-world IR playbooks, security automation, and defensive strategies
- **AI and automation** – Practical applications of LLMs, local AI deployment, and ethical considerations. I'm particularly excited about [Claude Code with standardized workflows](/posts/2025-07-22-supercharging-claude-cli-with-standards/) and [Claude Flow for AI-powered development](/posts/2025-08-07-supercharging-development-claude-flow/).
- **Open source projects** – Tools I'm building and contributing to, including [my MCP standards server](/posts/2025-07-29-building-mcp-standards-server/)
- **Career insights** – Lessons learned from working in federal contracting and security operations

## The Open Source Advantage

This site is [open source on GitHub](https://github.com/williamzujkowski/williamzujkowski.github.io). Feel free to explore the code, learn from it, or even fork it for your own use. I believe in learning in public and sharing knowledge freely. For those interested in workflow optimization, my posts on [progressive context loading for LLM workflows](/posts/2025-10-17-progressive-context-loading-llm-workflows/) and [privacy-first AI lab deployment](/posts/2025-10-29-privacy-first-ai-lab-local-llms/) demonstrate how open-source tools enable sophisticated development setups.


## Let's Connect

I'm always interested in connecting with fellow engineers, security professionals, and anyone passionate about technology. You can find me on [GitHub](https://github.com/williamzujkowski) or reach out directly through my [contact page](/about/#contact).

Here's to building a better, faster, more accessible web – one static site at a time!

---

*Check out the [README](https://github.com/williamzujkowski/williamzujkowski.github.io) on GitHub. I've documented everything from the build process to the deployment pipeline.*
