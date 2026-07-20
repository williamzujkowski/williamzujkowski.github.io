# Design Deviations

This site consumes [`remarque-tokens`](https://www.npmjs.com/package/remarque-tokens)
(v0.3.0) for the **core tier** — type scale, rhythm, spacing, content
widths, radius, motion, and base prose/typography machinery — via
`@import "remarque-tokens/core";` in `src/styles/global.css`. The
**palette tier** (fonts, colors, `--content-reading`) stays local, as
designed: overriding palette-tier tokens is *authored* customization, not
a fork (see "Token Tiers" in remarque's `REMARQUE.md`).

This document records every place this site's CSS differs from what the
package ships out of the box, and why — so a future audit doesn't
re-litigate a ratified decision as an accidental drift. Migration tracked
in issue #324; upstream tiering proposal in remarque#47 (ratified 6-1).

## 1. Core-tier token override

One core-tier token is deliberately overridden locally, in
`global.css`'s `/* ─── Core-tier deviations ─── */` block:

| Token | Core (`remarque-tokens/core`) | This site | Rationale |
|---|---|---|---|
| `--text-display` | `clamp(2.75rem, 5.5vw, 5rem)` (44–80px) | `clamp(2.25rem, 3.5vw, 3.5rem)` (36–56px) | Editorial restraint, ratified in issue #274 ("Phosphor broadsheet," 7-0): this site's display type deliberately reads smaller/less-fluid than the package default across the two-voice (serif/mono) system. |

Every other token this site previously hand-declared (~32 of them: full
type scale minus `--text-display`, all line-heights, all letter-spacing
except `--tracking-body` which core adds and this site didn't have, all
three font weights, `--space-1`…`--space-9`, `--content-standard`,
`--radius-sm`/`--radius-md`, all three motion tokens) was **byte-identical**
to core's value and has been deleted from `global.css` — core now supplies
it, with no shadowing duplicate left behind to rot out of sync.

## 2. Palette-tier tokens (sanctioned override surface, not deviations)

These stay local by design — palette tier is meant to be overridden:

- **Fonts**: Fraunces (display), Source Serif 4 (body), IBM Plex Mono
  (mono) — registered via Astro 6's Fonts API in `astro.config.mjs` and
  injected onto the root element by `<Font>` in `BaseLayout.astro`, so
  they are intentionally *not* redeclared as CSS custom properties in
  `global.css` (see the comment at the top of that file).
- **Colors**: "Palette B — Departure" (photosensitive ivory + ferric ink
  + radar green, light; CRT phosphor on black-green, dark) — both themes
  independently APCA/WCAG-audited (`pnpm audit`).
- **`--content-reading: 40rem`** — **this is NOT a deviation.** It is the
  sanctioned measure-compensation value for a Source Serif 4 body font,
  which remarque's own docs (`REMARQUE.md`'s "Measure Compensation"
  table) cite this site as the reference example for: core's palette
  default of 46rem is tuned for Inter (~70ch/line); the same width in a
  text serif runs ~86ch, well past comfortable, so this site measured its
  actual rendered text and landed on 40rem (~71ch/line at 17px Source
  Serif 4). Ratified alongside the rest of #274's measure/rhythm item.
  Per remarque#47's ratification notes, this flagship adoption — palette-
  tier-only overrides — *is* the acceptance test for the upstream tiering
  epic.

## 3. Fourth font slot: `--font-accent`

Core's font system is a strict three-slot model (display / body / mono).
This site adds a fourth, `--font-accent` (Shantell Sans, hand-lettered),
restricted by CI (`scripts/accent-font-audit.mjs`) to `.hand-note` only —
marginalia, never prose, nav, or meta. remarque#47 explicitly names this
site's fourth-slot precedent as the basis for the "optional accent/
marginalia slot" rule under consideration upstream.

## 4. Zine marginalia layer (`zine.css` / `theme-deck.css`)

Design-review ratified 7-0: hand-drawn geometry, masks, and scoped
texture over the Remarque system — body typography untouched, every
color still derives from theme tokens. Per the 2026-07-20 multi-agent
review's governance disposition, this layer stays **site-local by
design** (not a packaging candidate); `theme-deck.css` (14 terminal
palettes keyed on `[data-theme-deck]`) is slated to graduate into an
official upstream module, with this site becoming its first consumer
instead of its only home. Neither is adopted as a package dependency in
this migration.

Specific ratified deviations from a stock Remarque presentation, all
issue #274 ("Direction B," 7-0) unless noted:

- **Share links in post footers** (`.share-row` / `.share-label` in
  `PostLayout.astro`) — not part of core Remarque's prose machinery.
- **Zine border-radii** — `zine.css`'s squiggle-box radii (e.g.
  `255px 15px 225px 15px / 15px 225px 15px 255px` on `.callout`) vary
  per component so the wobble never reads as a uniform theme pack;
  deliberately not the flat `--radius-sm`/`--radius-md` scale.
  Design-review ratified 7-0 (zine layer).
- **Decorative accent usage** — e.g. the 404 doodle's wandering path
  (`.doodle-wander`, reduced-motion-guarded — see next item) and the
  landing-issue-label's terminal prompt glyph (`❯`), both accent-colored,
  purely decorative.
- **6-entry front page** — `src/pages/index.astro`'s
  `posts.slice(0, 6)` lead + 5-entry split, not a Remarque default.
- **404 ambient animation** — `.lost-doodle .doodle-wander`'s
  `@keyframes zine-wander`, scoped inside
  `@media (prefers-reduced-motion: no-preference)` in `zine.css`, so it's
  fully inert for anyone with a reduced-motion preference (WCAG 2.3.3).
- **Pill tag chips** — `.chip` tag/filter chips (`PostCard.astro`,
  `tags/index.astro`) with small-caps typography and a token-driven
  border; a presentational choice layered on top of core's typography
  machinery, not part of it.

## 5. Theming attribute convention

This site keys themes on `:root.dark` / `:root.light` classes plus
`[data-theme-deck='<name>']` for the 12 terminal-theme deck (generated,
`theme-deck.css`). Upstream remarque-tokens keys on `[data-theme="dark"]`
/ `[data-theme="light"]` attributes (see `tokens-palette.css`'s "Manual
dark mode toggle support" block) and a bare `@media
(prefers-color-scheme: dark) :root { ... }` query.

This is remarque#47's item 4, "One theme-switching convention" — not yet
unified upstream. It's the reason this migration does **not** adopt the
imported core's own dark-tier declarations (core tier ships none — colors
are palette tier — so no conflict there) nor treat `[data-theme]` as a
target selector anywhere in this codebase.

## 6. Audit tooling: NOT yet adopted (`npx remarque-audit`)

remarque-tokens ships an `npx remarque-audit` CLI. This site does **not**
adopt it in this migration and keeps its own five local audit scripts
(`scripts/contrast-audit.mjs`, `apca-audit.mjs`, `typography-audit.mjs`,
`color-token-audit.mjs`, `accent-font-audit.mjs`, run via `pnpm audit`).

Reason: the upstream audit's dark-theme extraction is built around
`[data-theme="dark"]` (and/or a bare prefers-color-scheme media query on
`:root`) — see §5 above — and cannot parse this site's `:root.dark` /
`:root.light` class-based theming convention. Adopting it today would
either silently audit the wrong (or no) dark-theme block, or require
forking the audit script, defeating the point of consuming it. This is
explicitly blocked on remarque#47 item 4 (theme-attribute unification).
Tracked as a follow-up once upstream unifies the convention; until then,
the local scripts (which already parse this site's actual `:root` /
`:root.dark` blocks directly, per-property, and independently validate
both WCAG 2 and APCA/WCAG 3 draft contrast) remain CI's gate.

## 7. `html` base-reset neutralization

Core's base reset sets `html { font-family; font-size: 100%; line-height;
color; background-color: var(--color-bg); ... }`. Every property except
`background-color` is a no-op here — `body` already sets its own
`font-family`/`font-size`/`line-height`/`color` explicitly to the same
values, and nothing renders directly on `<html>`. `background-color`,
though, would newly paint the gutter beyond `body`'s
`max-width: var(--content-standard)` on wide viewports with
`var(--color-bg)`, replacing the browser's own `color-scheme`-aware
canvas default (white in light mode, UA dark in dark mode) — a real
rendering change. `global.css`'s own `html {}` rule (unchanged selector,
positioned after the `@import`, so it wins on equal specificity) adds an
explicit `background-color: transparent;` — background-color's own
initial value — to restore exactly the pre-migration appearance. See the
inline comment in `global.css` for the full reasoning.

## References

- Issue #324 (this migration)
- Issue #274 ("Phosphor broadsheet," Direction B, ratified 7-0)
- remarque#47 ("Layered token architecture," ratified 6-1) — Token
  Tiers doc: `remarque-tokens`'s `REMARQUE.md`
- Issue #283 (accent-font lint, `--font-accent` allowlist)
