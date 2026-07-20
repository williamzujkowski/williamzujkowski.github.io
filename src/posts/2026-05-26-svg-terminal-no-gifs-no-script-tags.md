---
title: "No GIFs, No Script Tags: How Far a Single SVG File Can Go"
date: 2026-05-26
description: "svg-terminal is an experiment in how much you can make one self-contained SVG do: type, blink, phone an API for live stats, and survive a renderer that assumes every SVG is hostile. 48 blocks, zero JavaScript, one wry aside about trusting my own config file."
tags: [svg, typescript, github, projects, security]
author: William Zujkowski
---

svg-terminal is what happens when you take the profile-README GIF genre personally and ask how much of it you could do without a GIF at all. Concretely: it's a CLI and GitHub Action that reads a YAML config and hands back one self-contained SVG — typing animation, blinking cursor, 48 pre-built blocks running from neofetch to a fake `rm -rf /` panic — that renders inside GitHub's `<img>` tag with no JavaScript anywhere in the file.

It was also my first real argument with a rendering sandbox built on the assumption that every SVG is a loaded weapon, which mostly taught me how much of "loaded weapon" it actually lets through.

## The one trick everything else stands on

An `<img src="terminal.svg">` on GitHub doesn't get parsed as a live DOM subtree. The browser renders it in one of two "secure" SVG processing modes, and because the SVG is animated, it lands in secure *animated* mode: scripting off, event handlers inert, external resources blocked, but declarative animation still runs. SMIL elements — `<animate>`, `<animateTransform>`, `<set>` — aren't script, so nothing in the img-sandbox model touches them. They're declarative markup, so secure animated mode renders them like any other element. Despite years of Chrome threatening to deprecate SMIL, it never actually happened — Chrome suspended the deprecation in 2016, and SMIL still ships in every major engine ([caniuse: SVG SMIL animation](https://caniuse.com/svg-smil); [SVG Integration spec, W3C](https://svgwg.org/specs/integration/)).

That gap is the entire project. The typing reveal, the cursor walk, and scroll-on-overflow are SMIL `<animate>` elements with `calcMode="discrete"`. Frame-cycling animations — spinners, a clock, dice — moved to CSS `@keyframes` a while back specifically so `prefers-reduced-motion` could clamp them, since CSS media queries have a hook into CSS animation and none into SMIL. That's also the honest gap in the reduced-motion story: the typing reveal and cursor walk still don't honor it, because there's no CSS lever to pull, and the docs say so instead of pretending otherwise. If that matters for your audience, `--static` renders one non-animated frame and calls it done.

## Forty-eight blocks and a live wire to the internet

Once the sandbox stopped being an obstacle, the actual work was making 48 blocks worth typing out. Some are useful — `neofetch`, `htop`, `build-badge` for tests/lint/coverage. Some exist because I found them funny and refused to feel bad about it: `sudo-sandwich` (the xkcd 149 callback), `fork-bomb` ("turn your laptop fan into a leaf blower"), a `who` block that lists ghost users named `debugger`, `coffee`, and `sanity`, and an `rm-rf` block that stages a dramatic fake wipe of `/` with running commentary, because half this genre is theatrical failure anyway.

Five of the blocks are live, not scripted-to-look-live: `weather` pulls from wttr.in, `quote` and `fun-fact` hit small public APIs, `github-languages` aggregates a user's repo languages into percentage bars, and `github-stats` fetches follower and repo counts straight from `api.github.com` at build time. That's the part of the experiment I actually care about — an SVG that's current the moment it was generated, sitting on your profile like a badge that refreshes itself on a cron schedule instead of going stale the day you made it:

```yaml
- block: github-stats
  config:
    username: your-github-username

- block: weather
  config:
    location: "Los Angeles"
    units: metric
```

Wire that into a GitHub Action on a schedule and the SVG on your profile page updates itself, commits itself, and never runs a line of JavaScript in a viewer's browser to do it. The animation was the flashy part. Getting a static image format to hold a live data feed without the usual liabilities of a live data feed — a script tag, a tracking pixel, a fetch call running in someone else's browser — is the part I keep being pleased with.

## Respecting the off switch

None of this is worth much if it's obnoxious to people who'd rather not watch a cursor blink. `prefers-reduced-motion` clamps every CSS-driven animation — the frame cycles, the fade-ins. It can't reach the SMIL-driven ones, for the reason above, so `--static` exists as the actual off switch: one frame, guaranteed motionless. Renderers that strip SMIL outright — social-card scrapers, npm's README renderer, some RSS readers — still see something readable, because the animated elements' static attribute values sit at the reveal's end state until a SMIL-capable viewer takes over. The one honest exception is the CSS frame-cycle blocks: strip their animation and they fall back to their *first* frame, not their last, so a spinner shows one static glyph instead of a settled result. Nobody's staring at a blank rectangle either way, which was the actual bar.

## And yes, I eventually had to stop trusting my own config file

Here's the smaller, less flattering story. Every block interpolates user config — `color`, `fontFamily`, theme values — straight into SVG attributes and inline `<style>` blocks. I'd been treating that as low-risk because it arrived as YAML instead of a web form, which is exactly the kind of reasoning that gets you an internal security audit finding `color: '" onmouseover="alert(1)" x="'` producing a working event-handler injection, and a font-family field breaking out of a `<style>` block to inject a live `<script>` tag. GitHub's own rendering path is defended by the sandbox described above, so none of that fired *there* — but svg-terminal's output also gets embedded via npm-readme renderers, raw file hosts, and static-site generators that don't apply the same restrictions. Safe on GitHub and unsafe everywhere else isn't safe, it's safe by accident.

The fix was unglamorous: a strict `zod` schema at config-load time, plus `escapeXml()` at every place a string actually becomes markup, so library consumers who skip the schema by building a config object programmatically still get caught at the emit site. Two layers because I'd already learned, the hard way, that one layer is a promise and two is a policy. The lesson generalizes past this one project — "it's just a config file" was never a security property, it was a feeling I had about the file extension.

## What this doesn't claim

The SMIL-survives-the-sandbox trick isn't novel; it falls straight out of the SVG spec's img-referencing rules, and other badge tools lean on the same behavior. What I like about svg-terminal is smaller and dumber than a technical insight: a file format everyone treats as a static picture turns out to have a typing cursor, a live API call, and a decent fake panic hiding inside it, if you're willing to read the spec instead of assuming `<img>` means "inert." Most of the fun was finding out where the assumption stopped being true.

## Sources

- [svg-terminal repository](https://github.com/williamzujkowski/svg-terminal)
- [svg-terminal SECURITY.md](https://github.com/williamzujkowski/svg-terminal/blob/main/SECURITY.md)
- [svg-terminal CHANGELOG](https://github.com/williamzujkowski/svg-terminal/blob/main/CHANGELOG.md)
- [SVG Integration specification, SVG Working Group (secure animated / secure static processing modes for `img`-referenced SVG)](https://svgwg.org/specs/integration/)
- [caniuse: SVG SMIL animation browser support](https://caniuse.com/svg-smil)
- [Chrome SMIL deprecation suspension, tracked in Fyrd/caniuse#4167](https://github.com/Fyrd/caniuse/issues/4167)
