# Remarque — Field Notes

> Category: Editorial & Print
> The design system of williamzujkowski.github.io: remarque-tokens core with a local palette. Warm ivory paper, ferric red-black ink, one radar-green accent; in dark mode, CRT phosphor on black-green. Serif for human prose, mono for every machine surface. Flat, hairline-ruled, typography-first.

Package format: Open Design's design-system layout (`manifest.json` + `DESIGN.md` + `tokens.css`), described in [open-design/design-systems/README.md](https://github.com/nexu-io/open-design/blob/main/design-systems/README.md).

This describes a site that already exists; nothing here is a proposal. Every value traces to a file and line (Appendix C, as of commit `00f96b9`). Where the site disagrees with itself, Appendix B says so. If this file and the CSS disagree, the CSS wins: fix this file.

## 1. Visual Theme & Atmosphere

A technical broadsheet printed on slightly warm photographic paper, then annotated in the margins. Three layers, in order of authority:

1. **Remarque core** (`remarque-tokens` 0.26.0). Book typography: 17px body, 1.75 leading, a column of about 70 characters, borders instead of shadows, an 8px radius ceiling, near-invisible motion. Remarque's stated identity is "a modern technical publication", not an app dashboard (`RT/REMARQUE.md:23`).
2. **Palette B, "Departure"**. Ivory ground, ferric red-black ink, one radar-green accent, and an amber that appears only on hover. Dark mode is a different instrument, not an inversion.
3. **Zine marginalia**. Hand-drawn doodles, wobbly rules, a hand-lettered caption face and paper grain on the masthead and footer. It sits over the system, never touches body typography, and every mark is coloured by a token (`zine.css:1-6`).

**The two-voice rule** is the most recognisable trait. Serif carries what a person wrote. Mono carries what a machine would print: navigation, kickers, dates, tags, table headers, captions, TOC, breadcrumbs, footer (`global.css:380-422`). If a string is metadata, it is mono.

Fourteen palettes ship: light, dark and 12 terminal theme decks. Components survive all of them only by using tokens.

## 2. Color Palette & Roles

Values are oklch exactly as written in `astro-site/src/styles/global.css`. Hex is an sRGB conversion for convenience; the site's `theme-color` meta confirms both grounds (`BaseLayout.astro:200-205`). Contrast is against `--color-bg`.

### Light — photosensitive ivory, ferric ink, radar green

| Site token (OD alias) | oklch | ≈ hex | Role |
|---|---|---|---|
| `--color-bg` (`--bg`) | `0.95 0.015 75` | `#f5ede4` | Canvas. Never `#fff` |
| `--color-surface` (`--surface`), `--color-bg-subtle` | `0.93 0.015 75` | `#eee7dd` | Diagram nodes and tiers, dialogs, `.seq-note` |
| `--color-code-bg` | `0.92 0.015 75` | `#ebe3da` | `pre`, inline `code` |
| `--color-fg` (`--fg`) | `0.18 0.04 25` | `#200a08` | Body text, headings. Red-black, never neutral grey |
| `--color-fg-muted` (`--fg-2`) | `0.42 0.04 25` | `#614542` | 7.4:1. Excerpts, descriptions, blockquotes, doodle ink |
| `--color-muted` (`--muted`) | `0.52 0.03 25` | `#796360` | 4.8:1. Dates, captions, nav, chips |
| `--color-border` (`--border`) | `0.85 0.02 75` | `#d6ccc0` | **Decorative only** (<3:1). Rules, card edges, row separators |
| `--color-border-bold` | `0.62 0.02 25` | `#928280` | 3.2:1. Any boundary a reader must see: diagram nodes, chip hover, blockquote rule, kicker dots |
| `--color-accent` (`--accent`) | `0.48 0.15 140` | `#227008` | 5.3:1. Links, current section, focus outline, gate nodes |
| `--color-accent-hover` (`--accent-hover`) | `0.50 0.10 75` | `#845a0f` | 5.3:1. Amber; link hover only |
| `--color-selection-bg` | `0.88 0.10 140` | `#b5e8a9` | `::selection` |
| `--color-success` / `-warning` / `-error` | `0.50 0.12 145` / `0.52 0.105 85` / `0.52 0.12 25` | `#2f7434` / `#846305` / `#a34945` | Diagram states and validation only |

### Dark — CRT phosphor on black-green

| Token | oklch | ≈ hex | Notes |
|---|---|---|---|
| `--color-bg` | `0.14 0.015 140` | `#060b05` | |
| `--color-surface`, `-bg-subtle`, `-code-bg` | `0.17 0.015 140` | `#0c110b` | one value, three names |
| `--color-fg` | `0.92 0.03 140` | `#daead7` | phosphor green |
| `--color-fg-muted` | `0.85 0.03 140` | `#c4d3c0` | 12.7:1 |
| `--color-muted` | `0.78 0.03 140` | `#aebcaa` | 10.0:1 |
| `--color-border` | `0.25 0.02 140` | `#1d241b` | decorative only |
| `--color-border-bold` | `0.60 0.03 140` | `#778574` | 5.1:1 |
| `--color-accent` | `0.82 0.17 140` | `#84de70` | 12.0:1 |
| `--color-accent-hover` | `0.78 0.15 75` | `#efa831` | amber |
| `--color-code-fg` | `0.88 0.03 140` | `#cdddca` | |
| `--color-selection-bg` | `0.30 0.08 140` | `#14370c` | chroma cut to 0.08 for sRGB gamut |
| success / warning / error | `0.61 0.11 145` / `0.62 0.11 85` / `0.62 0.11 26` | `#569459` / `#a4802b` / `#c06a63` | |

Scrim and shadow get heavier in dark mode (`0.72` and `0.8` alpha) because black at 50% over an L=0.14 ground does nothing (`global.css:164-169`).

### Rules

- **One accent.** Green is the only expressive hue; amber exists only as the hover colour of something green (`RT/REMARQUE.md:532`).
- **Links are accent.** Every prose link is green, underlined 1px at 0.2em offset. Outside links, use accent once per element at most: one kicker word, one `❯` glyph, one gate node.
- **Two borders, two jobs.** `--color-border` decorates. Anything that must be perceived as a boundary uses `--color-border-bold` (`RT/REMARQUE.md:492`).
- **State colours are for state**, and in diagrams always come with a border-style change so they survive colour-blindness and forced colours (`global.css:889-917`).
- **Syntax colours** are nine quiet ANSI-derived slots, each ≥4.5:1 on `--color-code-bg`, not derived from the accent (`global.css:101-109`).
- **Dataviz slots `--color-viz-1…6` are reserved**; no chart exists. A future chart must pair hue with shape, dash or a direct label (`global.css:267-269`).
- **No literal colours** in authored visuals, inline SVG included ([content-visuals.md](../../content-visuals.md), Shared Rules). The one sanctioned literal is print's black-on-white (`zine.css:135-138`).

### Theme decks

With no stored choice the system preference decides; a choice puts `class="dark"` or `class="light"` on the root, plus `data-theme-deck="<slug>"` for a deck (`BaseLayout.astro:247-265`). A deck overrides `--color-*` names only, for one of 12 themes: catppuccin-latte, catppuccin-mocha, dracula, github-light-default, gruvbox-dark-hard, gruvbox-light-hard, kanagawa-wave, nord, nord-light, rose-pine, solarized-dark-higher-contrast, tokyonight. They are generated and contrast-validated by `scripts/theme-deck/generate.py` (`theme-deck.css:1-4`). A component with one literal colour breaks in 13 of 14 palettes.

## 3. Typography Rules

### Faces

| Slot | Face | Fallbacks | Loaded | Role |
|---|---|---|---|---|
| `--font-display` | Fraunces | Georgia, "Times New Roman", serif | wght 100–900, roman + italic | h1, h2, nameplate, card and entry titles, ledes, drop caps, numerals |
| `--font-body` | Source Serif 4 | Georgia, serif | wght 200–900, roman + italic; `latin` + `greek` | Prose, h3/h4, diagram node text |
| `--font-mono` | IBM Plex Mono | ui-monospace, "Courier New", monospace | 400, 500, roman + italic | Every machine surface |
| `--font-accent` | Shantell Sans | "Comic Sans MS", cursive | 400–500 | `.hand-note` captions only; CI-enforced by `scripts/accent-font-audit.mjs` |

The Greek subset is required: posts use π, ε and μ in prose (`astro.config.mjs:360-363`). The site self-hosts through Astro's Fonts API, which injects hashed family names; mockups can load the same four families from Google Fonts.

### Scale

| Remarque token (OD alias) | Value | Used for |
|---|---|---|
| `--text-micro` (`--text-xs`) | 0.8125rem (13px) | **The floor.** Kickers, eyebrows, counts, diagram labels |
| `--text-meta` (`--text-sm`) | 0.875rem (14px) | Nav, breadcrumbs, card meta, chips, figcaptions, `pre`, footer |
| `--text-body` (`--text-base`) | 1.0625rem (17px) | Body copy; never smaller for prose |
| `--text-body-lg` (`--text-lg`) | 1.1875rem (19px) | Post description, card titles, h3 |
| `--text-section` (`--text-xl`) | clamp(1.375rem, 2.25vw, 2rem) | h2 |
| `--text-title` (`--text-2xl`) | clamp(1.875rem, 3.5vw, 3rem) | Core token; no current page uses it |
| `--text-display` (`--text-3xl`) | clamp(2.25rem, 3.5vw, 3.5rem) | h1. Site override of core's 2.75–5rem |
| nameplate (`--text-4xl`) | clamp(2.25rem, 5.5vw, 4.25rem) | "*Field* Notes" masthead |

One-off fluid display sizes, all ratified under #274: `.lead-title` clamp(2.25rem, 4.5vw, 3.75rem), `.entry-title` clamp(1.5rem, 2.5vw, 1.875rem), `.entry-numeral` clamp(2rem, 4vw, 3rem), `.landing-tagline` clamp(1.25rem, 2.2vw, 1.625rem), `.masthead-title` clamp(3.5rem, 9vw, 7.5rem).

**Floor:** nothing renders below 0.8125rem. `astro-site/scripts/typography-audit.mjs` fails CI on any absolute size under 13px, `clamp()` minimums included (`:7`, `:32`). It exempts `em` and `%` sizes (`:8-10`), so the rendered size of relative and synthesized text is on you (Appendix B).

### Leading, tracking, weight

| Token | Value | Use |
|---|---|---|
| `--leading-display` | 1.05 | h1 |
| `--leading-title` (`--leading-tight`) | 1.15 | h3 |
| `--leading-section` | 1.2 | h2 |
| `--leading-body` | 1.75 | Prose |
| `--leading-meta` | 1.5 | Mono metadata |
| `--tracking-display` / `-title` | -0.02em / -0.015em | h1 / h2 and card titles (`.prose h2` is -0.01em, `global.css:1587`) |
| `--tracking-meta` / `-caps` | 0.02em / 0.06em | Mono metadata / uppercase labels |
| weights | 400 / 500 / 600 | h1 400, h2 500, h3, h4 and `strong` 600 |

Uppercase mono kickers track wider than the tokens: 0.12em (post, lead and entry kickers, issue label), 0.15em (masthead kicker, archive count), 0.08em (nav, archive stats) (`global.css:491-503`, `:1185-1195`, `:1242-1254`, `:1290-1301`, `:1474-1494`, `:1519-1528`).

### Typesetting details

- **Italic Fraunces as emphasis colour.** One word in Fraunces italic weight 300 in `--color-fg-muted`: "*Field* Notes" (`global.css:477-481`). The site's signature move.
- **Drop cap** on each post's first paragraph: Fraunces italic, 3.5em, line-height 0.85, floated (`global.css:800-809`). The landing lede has its own at 3.25em.
- **Numerals.** Prose uses `oldstyle-nums proportional-nums`; metadata (time, chips, card meta, breadcrumbs, code) uses `tabular-nums lining-nums` (`global.css:666`, `:1574-1579`). Never mix them in one context (`RT/REMARQUE.md:190-197`).
- **Headings** get `text-wrap: balance`, `font-optical-sizing: auto`, `font-synthesis: none` and discretionary ligatures; prose gets `text-wrap: pretty` and `hanging-punctuation: first last` (`global.css:665-673`, `:685-692`).
- **External links** in prose carry a small `↗` in `--color-muted` (`global.css:1552-1559`).
- **Caps labels.** Chips, post-card meta, section eyebrows and the TOC summary use `text-transform: uppercase` at `--text-micro` with `--tracking-caps`. Never `font-variant-caps: all-small-caps`: no subset font ships `smcp`/`c2sc`, so browsers synthesize them at about 0.75× and land below the 13px floor while the computed font-size still reads 14px.
- **Line breaks are spaces.** `compressHTML` is `true` (lossless), not Astro 7's default `'jsx'`, which follows React's rules and deletes the line break between text and an inline element on the next line ("via<a>"). `tests/e2e/reflow.spec.ts` fails on any word glued to a link (`astro.config.mjs`, `compressHTML`).

## 4. Component Stylings

Use the real class names when mocking site changes.

### Post header (`PostLayout.astro:54-89`; `global.css:541-564`)
Mono breadcrumb "Front / Dispatches" at `--text-meta` in `--color-muted`. Kicker: mono `--text-micro`, uppercase, 0.12em; section name in accent weight 500, then `·` in `--color-border-bold`, reading time, `·`, date. h1 at `--text-display`, Fraunces 400. Description at `--text-body-lg` in `--color-fg-muted`. Tag chips. All centred at `--content-reading`.

### Post card: archive, tags, related (`PostCard.astro:32-52`; `global.css:566-629`)
Grid `minmax(9rem, 14ch) 1fr`, gap `--space-6`, padding-block `--space-4`, 1px `--color-border` rule beneath, none on the last card. No box, fill or shadow. Left: mono `--text-meta` in `--color-muted`, date over reading time, 0.4em top padding to align with the title baseline. Right: Fraunces 400 title at `--text-body-lg`, line-height 1.25, no underline, accent on hover; excerpt in Source Serif `--text-body`, `--color-fg-muted`; chips. At ≤640px: one column, meta in a row.

### Landing (`index.astro:15-48`; `global.css:1177-1508`)
A broadsheet: a centred issue label (`❯` in accent, wobbly hairlines either side), a Fraunces tagline, a lead story with a large title and an italic weight-300 lede with its own drop cap, then a numbered list. Entry numerals are Fraunces italic 300 oldstyle figures in `--color-border-bold`, right-aligned in a 3.5–5rem gutter, accent on hover. Title links grow a 1px underline from the left via a background gradient, with a `text-decoration` fallback under forced colours (`global.css:1318-1347`).

### Chips and cards (`global.css:631-651`)
`.chip`: inline-flex, padding 0.2rem 0.6rem, mono `--text-meta`, 1px `--color-border`, `--radius-sm` (4px), `--color-muted`; hover turns text `--color-fg` and edge `--color-border-bold`. Rectangles, not pills. `.card` is the only boxed container: 1px border, `--radius-md`, padding `--space-5`, bold border on hover. Use it sparingly (`RT/REMARQUE.md:246`).

### Prose (`global.css:658-789`)
- Blockquote: 2px left rule in `--color-border-bold`, italic, `--color-fg-muted`; the zine layer hangs a hand-drawn quote mark in accent at 0.85 opacity in the left margin (`zine.css:72-88`).
- Inline code: `--color-code-bg`, 0.9em, `--radius-sm`. Blocks: `--color-code-bg`, 1px border, `--radius-md`, padding `--space-5`, mono `--text-meta`, line-height 1.6. `data-title` renders a mono `--text-micro` tab top-left.
- Tables: full width, 0.95rem; `th` mono semibold over a 2px border; `td` 1px border. Wrapped in `.scroll-wrap` for horizontal overflow.
- Images: 1px border, `--radius-sm`, never a shadow. Figcaptions: mono `--text-meta`, `--color-muted`, centred.
- Sidenotes and the TOC come from `remarque-tokens/essay`: in flow below 80rem, margin notes and a sticky right rail at ≥80rem (`RT/essay.css:200`, `:411`).

### Native diagrams ([content-visuals.md](../../content-visuals.md) owns the contracts)
Pick by the reader's question: process → `.flow`; layers or zones → `.arch`; actor exchange → `.seq`; matrix → Markdown table; dense graph → 2–3 views. Mermaid is legacy.
- **`.flow`** (`global.css:854-939`): a centred column of `--color-surface` nodes, 1.5px `--color-border-bold` edge, `--radius-md`, body serif 0.95rem weight 600; an `<i>` second line in mono 0.8125rem. CSS draws connectors; never type arrows. Variants: `.is-gate` dashed accent capsule, `.is-good` double 3px success, `.is-bad` dotted 2px error, `.is-warn` dashed 2px warning. `.flow-parallel` wraps; `.flow-branch` legs carry a mono uppercase label from `data-branch`.
- **`.arch`** (`global.css:947-995`): stacked `--color-surface` tiers with a 1px border and a mono uppercase `data-label`; chips are `--color-bg` boxes, 1.5px bold border, `--radius-sm`, 0.875rem weight 600. Variants `.is-primary`, `.is-guard`, `.is-warn`, `.is-bad`, `.is-good`. `.arch.is-stack` adds `↓` between tiers.
- **`.seq`** (`global.css:1002-1031`): ordered step cards with a mono counter; `.seq-note` italic on `--color-bg-subtle`; `.seq-label` a mono uppercase divider for alt/else/loop.
- Root `.flow`/`.arch` carry `role="group"` and `aria-label`; every `data-label` and `data-branch` is mirrored into an `aria-label`, because `::before` text is visual only. Under about 8 items per view.

### Zine marginalia (`zine.css`)
- **Doodles** (`.zine-doodle`, `zine.css:195-204`): an alpha-masked black PNG under 60 KB used as a mask over `background-color: var(--color-fg-muted)` (or accent with `--accent`), so one asset recolours across all palettes. Always `aria-hidden="true"`. After the intro, `width: min(240px, 62%)`, explicit `aspect-ratio`. The drawing carries a specific metaphor; never a stamped label.
- **Hand-note** (`zine.css:179-188`): Shantell Sans 1.05rem, line-height 1.45, `--color-fg-muted`, rotated -1.2deg. The only home of `--font-accent`.
- **Wobble rule** (`zine.css:40-68`): an SVG squiggle mask filled with `--color-border-bold`, replacing the masthead's straight bottom border and the issue-label hairlines.
- **Paper grain** (`zine.css:92-106`): procedural noise at 0.5 opacity, soft-light, on masthead and footer only. Never on reading surfaces; contrast CI cannot see composited texture.
- **Squiggle radii** (`zine.css:23-36`): `.series-nav`, `.deck-panel` and `pre[data-title]::before` use uneven elliptical radii. A ratified exception scoped to those three ([DESIGN-DEVIATIONS.md](../../../astro-site/DESIGN-DEVIATIONS.md) §4). Do not spread it.

### Masthead and footer (`global.css:424-539`, `:1033-1053`)
Centred nameplate: Fraunces italic light byline over "*Field* Notes" at the nameplate size, line-height 0.95, -0.03em. Below, a mono uppercase nav at `--text-meta`, 0.08em; the current page gets a Fraunces italic `§` in accent. Footer: mono `--text-meta`, `--color-muted`, centred, 44px link targets. Both carry grain; the masthead carries the wobble rule.

## 5. Layout Principles

- **One column.** `body` is capped at `--content-standard` (72rem) with 2rem × 1.5rem padding; nearly everything inside is centred at `--content-reading` (38rem: a median of 73 rendered characters per line of Source Serif 4 at 17px, measured, not derived from `ch`) so mono and serif edges line up (`global.css:318-325`, `:1156-1175`). The masthead is the one wider element (64rem).
- **Rhythm** from the spacing scale: h1 `--space-5` above / `--space-4` below; h2 `--space-7` above; h3 `--space-6`; `hr` `--space-7`; prose paragraphs 1.25em. A paragraph right after h2/h3 is pulled up to pair with it (`global.css:334-368`, `:702`, `:791-796`).
- **Spacing scale** (rem): 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 10, 12 for `--space-1…12` (`RT/tokens-core.css:49-60`). `--space-5` is 24px.
- **Density.** At most three distinct content sections above the fold (`RT/REMARQUE.md:258`). No hero banners, CTAs or feature grids. The front page shows six posts: one lead, five numbered entries.
- **Archetypes.** Posts: Remarque's Essay. Front page: Broadsheet. /about and /uses: the specimen list (`.uses-list`, `global.css:1055-1118`), a two-column `dl` with an italic Fraunces name and mono dates left, prose right.
- **Social images** are generated per post at `/og/<slug>.png`. Do not design hero images or add hero frontmatter.

## 6. Depth, Focus & Motion

**Depth.** Reading surfaces are flat. A 1px `--color-border` rule separates cards, `pre`, images and rows. Shadows exist only on floating UI: the theme-deck popover (`0 4px 16px var(--color-shadow)`, `ThemeDeck.astro:199`) and the search dialog (`0 25px 50px -12px` over a `--color-overlay` scrim, `Search.svelte:433-441`). "Quiet, subtle borders over shadows" (`RT/REMARQUE.md:237`).

**Radius.** `--radius-sm` 4px for chips, inline code, images, arch chips; `--radius-md` 8px for cards, `pre`, diagram nodes and tiers. 8px is the ceiling (`RT/tokens-core.css:70`). The `.flow` gate and branch labels use a literal `999px` capsule inside the diagram contract; it is not a token to reuse.

**Focus.** `outline: 2px solid var(--color-accent); outline-offset: 2px` on `:focus-visible` (`global.css:1136`). Use `outline`, not `box-shadow`: forced-colours mode removes shadows, and core pins the outline to `Highlight` there (`RT/tokens-core.css:275-278`). Inside a scroll container the ring is inset (`.remarque-toc-rail`, `global.css:1140`).

**Motion.** Nearly none. Hover and focus use `--motion-fast` (120ms), theme switches `--motion-normal` (180ms), easing `ease-out`. No scroll, entrance, stagger or parallax animation; nothing animates on a non-interactive element (`RT/REMARQUE.md:435-450`). A deliberate theme toggle crossfades colour properties briefly (`global.css:1613-1645`). The cross-document view transition runs only under `prefers-reduced-motion: no-preference` (`global.css:36-40`). Under `reduce`, core zeroes both duration tokens and a global rule clamps anything left (`global.css:1647-1653`). The one ambient animation is the 404 doodle's wander, also motion-gated, and it runs once for 4.8s; like the PizzaOps status pulse (2 × 2.4s), it stops within 5s, so WCAG 2.2.2 needs no pause control (`zine.css:217-229`, `tests/e2e/motion.spec.ts`). Transition named properties, never `all`.

## 7. Do's and Don'ts

### Do
- Mono for metadata, serif for prose. Every time.
- Keep rendered text at 0.8125rem or larger, diagram labels and captions included.
- Use `--content-reading` for anything in the article column.
- `--color-border-bold` for any border a reader needs to see; `--color-border` for decoration.
- Pair every state colour with a border style (double, dotted, dashed), and say the state in words.
- Use the existing diagram classes and their ARIA contract; split anything over ~8 items.
- Check new UI in light, dark and at least one theme deck, at 320px and desktop widths.

### Don't
- Hardcode a colour, including in inline SVG. Print is the only exception.
- Add a second accent hue, or use amber anywhere but a hover.
- Add shadows, decorative gradients, glassmorphism or `backdrop-filter` to content.
- Round anything past 8px or make generic pills.
- Use the hand-lettered face outside `.hand-note`.
- Use Fraunces for running text, or mono for headings or prose.
- Put grain on reading surfaces.
- Author a bare `z-index` (use `--z-*`, `RT/REMARQUE.md:454-470`) or a literal duration (use the motion tokens).
- Type arrows into `.flow` diagrams.
- Let anything scroll the page sideways.
- Stamp a word on a doodle to explain it. If it needs a label, it's the wrong drawing.

## 8. Responsive Behavior & Accessibility

| Breakpoint | What changes |
|---|---|
| ≤640px viewport | Body padding `--space-5` × `--space-4`; masthead tools centre below the nameplate; nav tightens gap and tracking but stays `--text-meta`; post cards and `.uses-row` go to one column (`global.css:531-539`, `:618-629`, `:1105-1118`, `:1150-1154`) |
| ≤640px container | `.entry-list` stacks numerals above titles at 1.5rem, via a container query on the list (`global.css:1498-1508`) |
| ≥80rem | Sidenotes move to the margin and the TOC becomes a sticky right rail; below, the TOC is a collapsed `<details>` (`RT/essay.css:200`, `:411`) |

**Reflow.** No page may scroll sideways at 320px. `body` sets `overflow-wrap: break-word` so a bare URL or long inline `code` breaks only when it cannot fit (`global.css:324`); `tests/e2e/reflow.spec.ts` checks every built page. Diagrams wrap (`flex-wrap`), never scroll; tables scroll inside `.scroll-wrap`; `pre` scrolls on its own.

**Accessibility floor**
- Body ≥17px; small text ≥14px; 13px is the absolute floor (`RT/REMARQUE.md:482-484`).
- Text ≥4.5:1 against `--color-bg` and `--color-surface`; functional borders ≥3:1. `remarque-audit` enforces this for the base palettes in CI.
- Touch targets ≥44×44px via `min-height`/padding: nav links, nameplate, footer links, archive link.
- Forced colours: diagram connectors and doodles fall back to `CanvasText`; gradient underlines to `text-decoration` (`global.css:1341-1360`).
- Print: forced light scheme, black on white, chrome hidden, external URLs appended, diagrams and code kept whole (`zine.css:108-175`).

## 9. Agent Prompt Guide

Paste `tokens.css` (both `:root` blocks, the dark blocks and the reduced-motion block) into the first `<style>`, then write component CSS against tokens only. Block 2 holds the site's native names, so site CSS such as the `.flow` rules pastes unchanged.

### Example prompts

1. **Post page.** "Mock a Field Notes post page with the Remarque tokens, light and dark side by side. Body max 72rem; everything else centred at `--content-reading`. Mono breadcrumb 'Front / Dispatches'. Kicker in mono `--text-micro`, uppercase, 0.12em: 'HOMELAB' in accent weight 500, `·` in `--color-border-bold`, '9 min read', `·`, date. H1 Fraunces 400 at `--text-display`. Description at `--text-body-lg` in `--color-fg-muted`. Three chips. Prose at 17px/1.75 with a Fraunces italic drop cap, one h2, one external link with `↗`, one blockquote, one titled code block. No shadows, no box around the article."
2. **Process diagram.** "Draw a homelab backup restore path as a `.flow` diagram using the class contract in DESIGN.md §4: `role="group"` and `aria-label` on the root; 'Nightly snapshot', a gate 'Checksum matches?', then a `.flow-branch` with `data-branch="Pass"` → `.is-good` 'Mount and verify' and `data-branch="Fail"` → `.is-bad` 'Alert, keep previous'. Mirror each `data-branch` into `aria-label`. No typed arrows. Every label ≥0.8125rem; reflow at 320px."
3. **Doodle and caption.** "After a post's intro, place a `div.zine-doodle` (`aria-hidden`, `--doodle` pointing at an alpha-masked PNG, `width: min(240px, 62%)`, explicit `aspect-ratio`) and a centred `.hand-note`. The post is about a firewall rule that silently allowed everything; the drawing carries that idea on its own, for example a bouncer holding the door open with the 'members only' sign facing the wrong way. Write three lowercase, deadpan captions under eight words."
4. **Theme stress test.** "Render the post card and an `.arch` diagram in light, `class="dark"`, and with the `nord` deck's `--color-*` values. Nothing may change but colour, and no element may carry a literal colour."

### Copy for mockups
Placeholder copy should sound like the blog ([AGENTS.md](../../../AGENTS.md), Writing Style): precise, dry, observational; understatement over enthusiasm; no exclamation marks or uplift. Technical examples come from the homelab; work references are time-buffered and never current (AGENTS.md, NDA Compliance).

### Review checklist
1. Is every metadata string mono and every prose string serif?
2. Does anything render below 0.8125rem, synthesized small caps and `em` sizes included?
3. Is there a colour that is not a token, or a hue besides green and its amber hover?
4. Any radius over 8px, or a shadow on a reading surface?
5. Do functional borders use `--color-border-bold`?
6. Does it hold in dark mode, one theme deck, and at 320px without sideways scroll?
7. Do diagrams carry the `role="group"` + `aria-label` contract?

## Appendix A — Token map

`tokens.css` has two `:root` blocks. Block 1 declares the 56 token names Open Design's schema expects, nothing else. Block 2 declares the site's native names (`--color-*`, `--text-meta`, `--space-7/9/10/11`, `--content-reading`, `--z-*`, `--font-accent`), aliasing block 1 where the value is shared.

| OD token | Bound to | Note |
|---|---|---|
| `--surface-warm` | `var(--surface)` | No third surface tier |
| `--fg-2` | `--color-fg-muted` | Secondary ink |
| `--meta` | `var(--muted)` | Meta and captions share one tier |
| `--border`, `--border-soft` | `--color-border` | Decorative. Interactive edges use `--color-border-bold` |
| `--accent-on` | `var(--bg)` | Text on an accent fill (`PizzaOps.svelte:466`); 5.3:1 light, 12.0:1 dark |
| `--accent-active` | `var(--accent)` | No `:active` colour state on the site |
| `--text-xs`…`--text-4xl` | micro … nameplate | `--text-xs` is the 13px floor |
| `--leading-tight` | 1.15 (`--leading-title`) | |
| `--space-5/6/8/12` | 1.5 / 2 / 4 / 12 rem | Remarque values by name |
| `--section-y-*` | 3rem | No viewport-dependent rhythm |
| `--radius-lg`, `--radius-pill` | 0.5rem | 8px ceiling |
| `--elev-raised` | `0 4px 16px` shadow colour | Popovers only |
| `--focus-ring` | 2px bg gap + 2px accent | Mirrors the outline; prefer `outline` |
| `--motion-base` | 180ms (`--motion-normal`) | |
| `--container-max` | 72rem (`--content-standard`) | Reading column is `--content-reading` |

## Appendix B — Open inconsistencies

Places where the site's own sources disagree. Follow the CSS.

1. **13px vs 14px for non-timestamp text.** `RT/REMARQUE.md:543` and `global.css:535-537` say 13px is for timestamps and 14px is the floor for other text. Kickers, eyebrows, archive counts, `.uses-meta`, `.series-position`, the `pre` title tab and every diagram label use 13px.
2. **Sub-floor relative size.** The external-link `↗` is 0.7em of 17px ≈ 11.9px. `typography-audit.mjs:8-10` exempts `em` on purpose, which contradicts "keep all visual text at 0.8125rem or larger" in content-visuals.md.
3. **999px capsules.** `.flow-node.is-gate` and `.flow-leg::before` use `border-radius: 999px` (`global.css:887`, `:934`) against the 8px ceiling.
4. **Functional border on surface.** `--color-border-bold` is 3.16:1 against `--color-bg` (`global.css:82`), but `.flow-node` draws it on `--color-surface` (`:874`), which computes to ≈2.99:1 in light mode, just under WCAG 1.4.11's 3:1. `remarque-audit` checks against `--color-bg` only.

## Appendix C — Provenance

Paths are relative to the repository root at commit `00f96b9`. `G` = `astro-site/src/styles/global.css`; `RT/` = `astro-site/node_modules/remarque-tokens/` (0.26.0).

| Value(s) | Source |
|---|---|
| Light palette | `G:76-90` |
| Light syntax, state, dataviz | `G:101-109`, `:120-126`, `:134-139` |
| Link / focus / selection aliases | `G:154-157` |
| Dark palette | `G:161-182` |
| Dark syntax, state, dataviz | `G:186-214` |
| System-preference dark block | `G:225-285` |
| `--text-display` override | `G:55`; rationale `astro-site/DESIGN-DEVIATIONS.md` §1 |
| `--content-reading: 38rem` | `G:73`; `RT/REMARQUE.md` Measure Compensation |
| Type scale, leading, tracking, weights | `RT/tokens-core.css:21-27`, `:30-34`, `:37-41`, `:44-46` |
| Spacing, content widths, radius | `RT/tokens-core.css:49-60`, `:65-66`, `:69-71` |
| Motion, `--z-*`, reduced-motion zeroing | `RT/tokens-core.css:80-82`, `:92-98`, `:109-115` |
| Focus outline | `RT/tokens-core.css:244-248`; `G:1136` |
| Fonts and fallbacks | `astro-site/astro.config.mjs:339-386` |
| Nameplate size | `G:468-476` |
| Body width, padding, overflow-wrap | `G:318-325`; mobile `G:1151-1154` |
| Section rhythm 3rem | `G:349` (h2), `G:368` (hr) |
| `--accent-on` | `astro-site/src/components/PizzaOps.svelte:466` |
| `--elev-raised` | `astro-site/src/components/ThemeDeck.astro:199`; shadow colour `G:90`, `G:169` |
| Search dialog shadow, radius, scrim | `astro-site/src/components/Search.svelte:433-441` |
| Post header | `astro-site/src/layouts/PostLayout.astro:54-89`; `G:541-564` |
| Post card | `astro-site/src/components/PostCard.astro:32-52`; `G:566-629` |
| Chips, cards | `G:631-651`, `:1597-1606` |
| Prose rules, drop cap | `G:658-789`, `:800-809` |
| `.flow` / `.arch` / `.seq` | `G:854-939`, `:947-995`, `:1002-1031`; contracts `docs/content-visuals.md` |
| Masthead, nav, footer | `G:424-539`, `:1033-1053` |
| Specimen list | `G:1055-1118`; `astro-site/src/pages/about.astro:38` |
| Broadsheet landing | `G:1177-1508`; `astro-site/src/pages/index.astro:15-48` |
| Forced-colours fallbacks | `G:1341-1360` |
| Theme crossfade, view transition, reduced motion | `G:1613-1645`, `:36-40`, `:1647-1653` |
| Zine masks, squiggle radii, wobble, quote mark, grain | `astro-site/src/styles/zine.css:10-21`, `:23-36`, `:40-68`, `:72-88`, `:92-106` |
| Print | `zine.css:108-175` |
| `.hand-note`, `.zine-doodle`, 404 wander | `zine.css:179-188`, `:190-204`, `:217-229` |
| Theme decks (12) | `astro-site/src/styles/theme-deck.css`; `astro-site/src/data/theme-deck.json` |
| Theme selectors | `astro-site/src/layouts/BaseLayout.astro:247-265`; `astro-site/DESIGN-DEVIATIONS.md` §5 |
| `theme-color` hex | `BaseLayout.astro:200-205` |
| Sidenote / TOC breakpoint | `RT/essay.css:200`, `:411` |
| 13px floor enforcement | `astro-site/scripts/typography-audit.mjs:7-10`, `:32` |
| `compressHTML: true`, reflow test | `astro-site/astro.config.mjs` (`compressHTML`); `astro-site/tests/e2e/reflow.spec.ts` |
| Font-slot rules and deviations | `RT/REMARQUE.md:152-158`; `astro-site/DESIGN-DEVIATIONS.md` §3, §12 |
| Borders over shadows, cards, radius, images | `RT/REMARQUE.md:237`, `:246`, `:247`, `:267-270` |
| Motion, stacking | `RT/REMARQUE.md:435-450`, `:454-470` |
| Size floors, contrast | `RT/REMARQUE.md:482-492`, `:538-557` |
