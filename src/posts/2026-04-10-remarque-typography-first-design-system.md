---
title: "Remarque: A Typography-First Design System for Technical Sites"
date: 2026-04-10
description: "Most developer sites look like SaaS dashboards. Remarque is the antidote — a design system rooted in book typography, 17px body text, 46rem reading columns, and the OKLCH color space. Self-hosted fonts, AI-native tokens, zero CDN dependencies."
tags: [design, typography, open-source, frontend, css]
image: https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=1200&h=630
imageAlt: "Open book with printed text and a fountain pen resting on the page"
author: William Zujkowski
---

Most developer sites look the same. Generic sans-serif at 16px. A sidebar with icon-heavy navigation. Gradient heroes. Syntax-highlighted code blocks with vaguely-too-dark backgrounds. The visual vocabulary of SaaS dashboards applied to every context, including ones that have nothing to do with SaaS.

I got tired of it. Not because there's anything wrong with those defaults individually — Tailwind's type scale is fine, system-ui renders adequately, 16px is industry-standard for a reason. But the cumulative effect of every technical site picking the same defaults is that they all blur into one dashboard, and none of them are actually good at the thing they're for: letting a reader focus on the text.

[Remarque](https://github.com/williamzujkowski/remarque) is my answer. A design system rooted in book typography, editorial design, and the quiet confidence of a well-made publication. The interface is the typography. Everything else is auxiliary.

## The three-font system

Remarque ships with exactly three fonts, each with a strict role:

| Role | Font | Used For |
|------|------|----------|
| Display | [Newsreader](https://fonts.google.com/specimen/Newsreader) | Page titles, hero headings, article titles. Never for body copy. |
| Body | [Inter](https://rsms.me/inter/) | Body text, UI labels, navigation, buttons. The workhorse. |
| Mono | [JetBrains Mono](https://www.jetbrains.com/lp/mono/) | Metadata, code, timestamps, labels. Never for headings. |

The strictness matters. A lot of design systems ship five or six fonts and leave the pairing decisions to the consumer, which produces chaos. Remarque's rule is that if you're putting text on a page, one of these three fonts is correct and the other two are wrong. Display for headings. Body for prose. Mono for anything numeric or structural. No overlap.

This is where most developer sites fall down. They use a sans-serif for headings and body because "sans-serif is clean." Clean in display contexts, sure. But a paragraph of sans-serif at reading sizes loses the character variation that makes serif body text comfortable for long-form reading. Newsreader specifically because it's a serif designed for UI and the web, not a print-era workhorse shoved into a web context.

## 17px body, 46rem column

The two numbers everything else derives from:

- **17px minimum body text.** One pixel above the industry default. The difference in reading comfort is immediate and the evidence for it is well-established — the Nielsen Norman Group's reading research and Matthew Butterick's [Practical Typography](https://practicaltypography.com/) both converge on 16-18px as the sweet spot for screen reading, and 17 is the round-number middle of that range.
- **46rem reading column.** About 70 characters per line at 17px Inter. That's the upper end of the 45-75 characters-per-line window that typography research has consistently pointed to since Bringhurst's *Elements of Typographic Style*.

These two numbers together define the reading experience. Every other layout decision is in service of them.

If you run Remarque in a browser at 100% zoom, a paragraph fills the column naturally. Your eye hits the end of a line and finds the next line without a saccade jump. Your hand doesn't reflexively reach for Cmd-+ to bump the text size. That's the test. If you're not reaching for the zoom, the design is working.

Contrast this with the typical SaaS dashboard design: 14px body, full-viewport-width columns, everything balanced to look good in a product screenshot. Readable for scanning, not for reading.

## OKLCH for color

All colors in Remarque are specified in the OKLCH color space. This isn't a vanity choice. It's a perceptual uniformity choice.

RGB and HSL are devices for specifying colors in a way that matches display hardware, not a way that matches how the human visual system perceives color. A 50% lightness in HSL looks different across hues — a 50% yellow is perceptually much brighter than a 50% blue. OKLCH fixes this. A 0.50 lightness value in OKLCH actually looks mid-brightness, regardless of hue.

In practice, this means:

- Building a color palette in OKLCH produces coherent-feeling colors without manual tuning.
- Dark mode and light mode use symmetric lightness values that actually feel symmetric.
- Accessibility contrast checks are more predictable because lightness correlates with perceived brightness.

Browser support for OKLCH is already universal in evergreen browsers. There's no fallback needed for anyone reading a modern technical site.

## Self-hosted fonts, strict CSP

Remarque's fonts are self-hosted. No Google Fonts CDN call. No `fonts.googleapis.com` domain in the network waterfall. Strict Content Security Policy that refuses third-party font origins.

This matters for three reasons:

1. **Privacy.** Google Fonts' GDPR posture has been [litigated in the EU](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation) and the privacy-preserving answer is self-hosting.
2. **Performance.** A cold-cache Google Fonts fetch adds ~200-400ms on typical connections. A self-hosted font served from the same origin is free after the first page load in a session.
3. **Resilience.** When `fonts.googleapis.com` has an outage (it happens), your site's typography is unaffected. Self-hosting decouples your render path from someone else's infrastructure.

The tradeoff is slightly larger initial bundle. Newsreader + Inter + JetBrains Mono subsetted to Latin + common punctuation runs about 180KB gzipped total for all weights and styles. A single Google Fonts CSS request plus the three font files it references is ~140KB. The 40KB delta is worth it.

## Page archetypes

Remarque isn't a collection of components. It's a collection of **page archetypes** — complete page templates for specific editorial contexts:

- **Article.** Hero heading, byline, 46rem body column, footnotes. The blog post archetype.
- **Project.** Project overview with metadata table, description, links. For portfolio-style pages.
- **Specimen.** The typography specimen page — every weight, every size, every pairing.
- **Tokens.** The design tokens reference page — every color, every spacing value, every type scale step.
- **Start.** The "getting started" archetype for tool landing pages.

Each archetype is a complete HTML + CSS + (minimal) JS template. Copy it, replace the content, done. No component composition, no framework lock-in, no decisions about what "the hero section" should look like — the archetype already made them.

This is where Remarque diverges from most design systems. Instead of giving you LEGO bricks and a reference manual, it gives you houses. The houses are well-designed, and if you want a different floor plan you edit the template. But the default is that you're writing content into a page that already looks good.

## AI-native design tokens

The design tokens ship as CSS custom properties in a structured file:

```css
:root {
  --rq-color-ink: oklch(0.18 0.02 250);
  --rq-color-paper: oklch(0.98 0.005 90);
  --rq-font-display: "Newsreader", Georgia, serif;
  --rq-font-body: "Inter", system-ui, sans-serif;
  --rq-font-mono: "JetBrains Mono", Menlo, monospace;
  --rq-size-body: 1.0625rem;  /* 17px */
  --rq-width-reading: 46rem;
  --rq-line-height-body: 1.7;
  /* ... */
}
```

The explicit naming convention (`--rq-color-ink`, not `--color-dark-gray-500`) gives AI coding assistants enough semantic context to make correct decisions without additional prompting. When Claude Code sees `--rq-color-ink`, it doesn't need to infer from context that this is body text color — the name says so.

This sounds trivial. In practice, design systems with terse token names (`--gray-500`, `--accent-3`) require explanatory documentation that AI tools don't always get in their context window. Semantic naming defers less meaning to the docs. Remarque's tokens file is readable as-is.

There's a [REMARQUE.md](https://github.com/williamzujkowski/remarque/blob/main/REMARQUE.md) in the repo that's specifically a specification for AI agents — rules, constraints, examples of correct vs. incorrect usage. Designed to be consumed by Cursor or Claude Code or Copilot with zero aesthetic drift between sessions.

## What "design system" even means here

Most "design systems" are component libraries. Headless UI primitives. Shadcn. Tailwind UI. These are fine tools for building SaaS dashboards, which is what most of them are designed for.

Remarque is deliberately not a component library. There's no `<Button variant="primary">` or `<Card elevation={2}>`. The things it ships are:

1. **Design tokens** (the CSS file).
2. **Page archetypes** (the templates).
3. **A type specimen** (the demo page).
4. **Documentation** (the start guide, the design decisions page).

You can use any of these independently. Drop the tokens into an existing project and get the typography palette without the archetypes. Use the Article archetype as a blog post template and ignore the tokens. Lift the color scheme and apply it to a Vue app. The pieces are composable without being coupled.

This matters because the cost of adopting a design system is usually locking into its component model. Remarque doesn't have a component model. It has opinions about typography and color and layout, expressed as the minimum primitives needed to apply them.

## Named for a reason

A remarque is a small mark or sketch in the margin of a print — a proof impression that signals the work's provenance without interrupting it. The name captures what the system is trying to do: be present as a well-made substrate for the content, not compete with it for attention.

Every decision in Remarque serves that goal. The three-font constraint prevents visual noise. The 17px/46rem rules optimize for reading. The self-hosted fonts eliminate rendering dependencies. The page archetypes get out of the way of the writing.

## What I'd tell a past-me

**Pick fewer fonts.** My first version had five. Dropping to three made every page look more coherent. If you can't describe each font's role in one sentence, you have too many.

**Commit to a reading width.** "Responsive" in most design systems means "fill whatever container." That's wrong for body text. 46rem is 46rem whether the viewport is 1920px or 1440px. Lines wider than ~75 characters become harder to read regardless of viewport.

**OKLCH early, not late.** Converting an RGB palette to OKLCH after the fact is painful. Starting in OKLCH and generating the fallbacks is easy. If you're starting a design system today, start in OKLCH.

**Write the AI specification separately.** [REMARQUE.md](https://github.com/williamzujkowski/remarque/blob/main/REMARQUE.md) didn't exist in the first few versions. Once it did, coherence across AI-assisted builds went up noticeably. Humans and AI agents want the same information but in different formats. Ship both.

## Numbers

| Metric | Value |
|--------|------:|
| Fonts | 3 (Newsreader, Inter, JetBrains Mono) |
| Body text size | 17px |
| Reading column width | 46rem |
| Color space | OKLCH |
| Color palette | 14 tokens (ink, paper, 5 accents, 7 neutrals) |
| Page archetypes | 5 (Article, Project, Specimen, Tokens, Start) |
| Total font weight (gzipped) | ~180KB across all weights |
| External dependencies at runtime | 0 |
| Google Fonts CDN calls | 0 |
| CSP directives for third-party fonts | `font-src 'self'` only |

## Try it

- [Live demo](https://williamzujkowski.github.io/remarque/) — reads at 17px body, 46rem column, as intended.
- [Type specimen](https://williamzujkowski.github.io/remarque/specimen/) — every weight, every pairing.
- [Design tokens reference](https://williamzujkowski.github.io/remarque/tokens/) — the CSS variables in one place.
- [Source](https://github.com/williamzujkowski/remarque) — Apache 2.0.

If you're building a technical site and the default Tailwind setup feels wrong but you can't name why, the answer is usually that it's a great SaaS dashboard design applied to a context that isn't a SaaS dashboard. Remarque is what I use instead.
