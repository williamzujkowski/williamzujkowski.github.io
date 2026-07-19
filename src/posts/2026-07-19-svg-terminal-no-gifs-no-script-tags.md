---
title: "No GIFs, No Script Tags: Building Animated Terminal SVGs for GitHub READMEs"
date: 2026-07-19
description: "svg-terminal turns a YAML config into a self-contained animated SVG that survives GitHub's sandboxed renderer. The interesting engineering problem isn't the animation. It's treating YAML as untrusted input."
tags: [typescript, svg, security, projects, github]
author: William Zujkowski
---

Profile READMEs are full of animated terminal demos, and almost all of them are GIFs. GIFs are heavy, they can't be edited without re-recording, and they can't respond to `prefers-reduced-motion`. I built [svg-terminal](https://github.com/williamzujkowski/svg-terminal) to replace that workflow: write a YAML config, get back one self-contained SVG file with typing animation, a blinking cursor, and 48 pre-built "blocks" (neofetch, htop, fake `rm -rf` panic, a live GitHub-stats card). No GIF. No JavaScript runtime. It has to render inside GitHub's `<img>` tag, which means it has to survive a rendering context that's actively hostile to almost everything an animated SVG normally does.

That constraint shaped the whole project. Getting animation past the sandbox turned out to be the easy part. Making the YAML front-end safe turned out to be the part that actually needed engineering discipline.

## What GitHub's SVG sandbox actually strips

When you embed an SVG with `<img src="terminal.svg">` on GitHub, the browser doesn't render it as a live DOM subtree. It renders it in what the SVG spec calls "secure static" mode: any SVG referenced as an image is required to have scripting disabled. `<script>` tags don't execute. `onclick`, `onload`, and every other event-handler attribute are inert. External resource fetches (fonts, `xlink:href` to remote assets) are blocked. That's a browser-level rule, not a GitHub-specific filter, and it's the same reason `<img src="malicious.svg">` doesn't pop an alert box no matter what's inside the file ([SVG Integration spec, W3C](https://svgwg.org/specs/integration/)).

Declarative animation is the exception. SMIL elements — `<animate>`, `<animateTransform>`, `<set>` — aren't script. They're markup, evaluated by the SVG renderer the same way a `<rect>` or a `<path>` is. Nothing in the img-sandbox model disables them, and despite periodic noise about Chrome deprecating SMIL, it never actually shipped: Chrome 45 deprecated SMIL in 2015, then suspended that deprecation in 2016, and SMIL still ships in every major engine as of this year ([caniuse: SVG SMIL animation](https://caniuse.com/svg-smil); [Chrome SMIL deprecation suspension, tracked in Fyrd/caniuse#4167](https://github.com/Fyrd/caniuse/issues/4167)). CSS animation survives the same sandbox for the same reason: it's declarative, not scripted.

That's the whole trick. svg-terminal's typing reveal, cursor walk, and scroll-on-overflow are SMIL `<animate>` elements with `calcMode="discrete"`. Frame-cycling animations (spinners, a clock, dice) moved to CSS `@keyframes` in v0.17, specifically so `@media (prefers-reduced-motion: reduce)` could clamp them. CSS media queries apply to CSS animations but have no equivalent hook into SMIL, which is why the typing reveal and cursor walk still don't honor reduced-motion, and the project's docs say so plainly rather than papering over it. If that's a problem for your audience, `--static` renders a single non-animated frame instead. No JavaScript is emitted at any point, which also means the output degrades gracefully: renderers that strip SMIL outright (social-card scrapers, npm's README renderer, some RSS readers) still see a fully-rendered final frame instead of a blank rectangle, because the static attribute values are the *end* state, held by a `<set>` element until SMIL takes over for viewers that support it.

## The actual attack surface: YAML in, SVG out

Once animation was solved, the remaining problem was more mundane and more dangerous: every block in svg-terminal takes user config and interpolates it into SVG attributes, `fill=` values, and inline `<style>` blocks. `color`, `fontFamily`, `titleFontFamily`, and every slot in a custom inline theme are strings that came from a YAML file and end up inside markup a browser parses. That's an injection surface no different in kind from a web form, and I initially treated it with less suspicion than I would a web form, because it "was just a YAML config." That was the actual mistake.

It showed up as three real bugs, not hypothetical ones. An internal security audit found that `color: '" onmouseover="alert(1)" x="'` on a block entry produced a working event-handler injection in the rendered SVG. The same shape worked through an inline theme's `colors.text` field. And `fontFamily: 'monospace; } </style><script>alert(1)</script>'` broke out of the `<style>` block entirely and injected a live `<script>` tag. GitHub's own rendering path is defended by the img-sandbox behavior described above, so none of these executed *there*. But svg-terminal's output isn't only consumed by GitHub. Library users embed it via npm-readme renderers, raw file hosts on custom domains, and static-site generators that inline the SVG directly into a page's DOM, none of which apply the same img-tag restrictions. An SVG that's safe when GitHub serves it and unsafe everywhere else isn't safe; it's safe by accident.

The fix is two layers, deliberately redundant:

```typescript
const ColorRefSchema = z.string().refine(
  (v: string) => HEX_COLOR_RE.test(v) || THEME_COLOR_NAMES.has(v),
  { message: 'color must be a hex string (#abc / #aabbcc) or a theme palette name' },
);
```

Every color and font-family field goes through a strict `zod` schema at config-load time, so a malicious value throws a clear error before it ever reaches the renderer. That's layer one, and it's the one that stops the attack for anyone using the CLI or the GitHub Action. But the schema only runs if the caller goes through `loadConfig`. Library consumers who build a `UserConfig` object programmatically can skip it entirely, so every one of those same values also gets `escapeXml()` applied at the actual SVG emit site, in `svg-generator.ts` and `line-renderer.ts`. Defense in depth here isn't decorative. It's the difference between "validated at the front door" and "validated at every place the string actually becomes markup." The second one is what protects a use case the first one doesn't cover.

The lesson generalizes past this project. "It's just a config file" is not a security property. YAML, JSON, TOML — the serialization format tells you nothing about whether the values inside it are trusted. Trust comes from who's allowed to write the file and what happens to the values afterward, and if the answer to the second question is "gets interpolated into something a browser or a shell parses," it needs the same schema-plus-escape treatment you'd give a web form, not a lighter one because it arrived as `.yml` instead of `?color=`.

## What this doesn't claim

svg-terminal is a small tool — two GitHub stars, mostly built for my own profile README and a handful of blocks I found funny (`fork-bomb`, `sudo-sandwich`). I'm not claiming the SMIL-survives-sandboxing trick is novel; it follows directly from the SVG spec's img-referencing rules, and plenty of other SVG-badge tools rely on the same behavior. What I am claiming, because I watched it happen in this codebase specifically, is that the YAML-config attack surface is easy to underweight precisely because it doesn't look like an attack surface, and that the fix (schema validation plus emit-site escaping, applied redundantly) is cheap enough that there's no excuse for skipping either layer.

## Sources

- [svg-terminal repository](https://github.com/williamzujkowski/svg-terminal)
- [svg-terminal SECURITY.md](https://github.com/williamzujkowski/svg-terminal/blob/main/SECURITY.md)
- [svg-terminal v0.17.1 security release notes (CHANGELOG)](https://github.com/williamzujkowski/svg-terminal/blob/main/CHANGELOG.md)
- [SVG Integration specification, SVG Working Group (secure static processing mode for `img`-referenced SVG)](https://svgwg.org/specs/integration/)
- [caniuse: SVG SMIL animation browser support](https://caniuse.com/svg-smil)
- [Chrome SMIL deprecation suspension, tracked in Fyrd/caniuse#4167](https://github.com/Fyrd/caniuse/issues/4167)
