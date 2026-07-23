# Design Deviations

This site consumes [`remarque-tokens`](https://www.npmjs.com/package/remarque-tokens)
(v0.5.0) for the **core tier** — type scale, rhythm, spacing, content
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

remarque#47 item 4, "One theme-switching convention," was ratified 3-0
and shipped in remarque-tokens **0.5.0**: the package's own palette now
keys dark mode on `[data-theme="dark"], :root.dark` (dual selector —
`[data-theme]` canonical, `:root.dark` a documented compatibility bridge,
"sunset target: 1.0"), and `remarque-audit` natively parses both
conventions (plus `html.dark`/`.dark`) with fixture tests for all three.
This site still authors its own palette on `:root.dark` / `:root.light`
only — by choice, not because the tooling can't see it anymore (see §6,
which is exactly the "cannot parse this site's convention" blocker that
0.5.0 removed) — so this remains the one place this site's selector
convention differs from the upstream default, not a case of the tooling
having no opinion on it.

## 6. Audit tooling: adopted at `remarque-audit@0.5.0`

**Resolved 2026-07-20** (was: "NOT yet adopted," blocked on remarque#47
item 4 — see the git history of this file for the original deferral
text). remarque-tokens 0.5.0's `remarque-audit` CLI natively parses this
site's `:root.dark` class convention (§5), which is what unblocked
adoption: the previous version's dark-theme extraction was built around
`[data-theme="dark"]` only and would have silently audited the wrong (or
no) dark-theme block against this site's actual CSS.

This site now runs `remarque-audit --palette src/styles/global.css --src
src/styles` as its **WCAG 2.x contrast + sRGB-gamut** check, wired via
`scripts/run-remarque-audit.mjs` (`pnpm audit:remarque`, part of `pnpm
audit` and the `remarque` CI job in `.github/workflows/audits.yml`). It
replaces the site's own former `scripts/contrast-audit.mjs`, which is
**deleted in full** — that script covered exactly the `:root` /
`:root.dark` fg/bg pairs remarque-audit's `CHECKS` table now covers
(confirmed line-for-line: `fg`, `fg-muted`, `muted`, `border-bold`,
`accent`, `accent-hover` against `bg`, both themes), had no coverage of
`theme-deck.css`'s 14 terminal palettes or anything else remarque-audit
doesn't also see, so nothing was trimmed-and-kept — the whole file's
job moved upstream. **Kept as-is**, not covered by remarque-audit and not
duplicative of it: `scripts/apca-audit.mjs` (APCA/WCAG 3 draft — upstream
has no APCA check, and this script is explicitly advisory-only, unlike
remarque-audit's hard-fail WCAG 2 checks), `scripts/typography-audit.mjs`
(whole-`src/` font-floor scan — broader scope than remarque-audit's
`--src src/styles`, and free of the false-positive issues below since it
already skips comment lines), `scripts/color-token-audit.mjs` (whole-`src/`
hardcoded-color scan that already excludes `--color-*` token-declaration
lines by shape rather than by filename, so it doesn't misfire on
`theme-deck.css`), and `scripts/accent-font-audit.mjs` (no upstream
equivalent at all).

One real fix came out of adopting the tool: dark-theme
`--color-selection-bg` was `oklch(0.30 0.10 140)`, which remarque-audit
correctly flagged as outside the sRGB gamut (its OKLCH→linear-sRGB
math clips the blue channel to -0.0007 at that L/C/H — independently
verified). Reduced chroma to `oklch(0.30 0.08 140)` (same hue and
lightness — still comfortably in gamut, blue channel now +0.0036);
`color-selection-fg`/`color-selection-bg` contrast is unaffected at
10.58:1 (floor is 4.5:1). This is a genuine, if minor, defect the site's
own former script never caught (`contrast-audit.mjs` and `apca-audit.mjs`
both only computed WCAG/APCA ratios — a gamut check was never part of
either).

### Accepted source-scan false positives (`scripts/remarque-audit-baseline.json`)

**Update 2026-07-23 (#375): the baseline is now EMPTY.** The 216 entries
documented below were false positives from `remarque-audit@0.5.0`. This site
bumped to `remarque-tokens@0.8.0` (#345), whose `--src` scan fixed them — it
strips comments before matching (killing the `#274`-in-a-comment hex false
positives) and correctly recognizes `global.css` as a token file (killing the
`oklch() literal` false positives) — so it emits **zero** source-scan findings
against the current CSS. This was verified to be a genuine clean result, not a
silently-disabled gate: a probe injecting a real hardcoded hex, a sub-13px
font-size, and a stray `oklch()` literal is still correctly caught and fails
the audit. Emptying the baseline also retires the line-number-keyed maintenance
trap (it previously had to be hand-remapped on any line-shifting CSS edit — see
#332/#334). The fail-closed mechanism is retained: any future real source-scan
finding now hits an empty baseline and blocks the build until hand-reviewed.
The original rationale is kept below for the historical record.

remarque-audit's `--src` scan (font floors, hardcoded colors) unconditionally
recurses `src/styles` and flags three categories of finding that are **not**
real defects, verified by hand against every flagged line:

1. **`oklch() literal outside token files`** on `global.css` and
   `theme-deck.css` (198 of 216 total findings). remarque-audit's
   `isTokenFile` allowlist only recognizes literal filenames ending in
   `tokens.css` / `tokens-core.css` / `tokens-palette.css` / `fonts.css` /
   `globals.css` / `pages/tokens.astro`. `global.css` (this site's actual
   `--palette` file — the tool is told, via `--palette`, that this file
   *is* the palette, but that fact isn't threaded through to the `--src`
   scan's file-type check) and `theme-deck.css` (a generated, build-time
   contrast-validated palette, see §4) don't match that list by name, even
   though both are 100% token declarations. This is judged to be an
   upstream limitation, not a site defect — see the PR that introduced
   this file for the full "upstream audit is wrong here" writeup.
2. **`hardcoded hex/rgb/hsl color`** on GitHub issue-number references in
   comments (e.g. `(issue #324)`, 11 instances across `global.css` /
   `zine.css`). remarque-audit's `--palette` parser strips comments before
   matching, but its `--src` source-scan does not, so `#324` matches the
   same regex as a 3-6 digit hex color. A real upstream regex gap.
3. **`statically unverifiable font-size (clamp/%)`** on 7 one-off display/
   hero `clamp()` sizes (`.site-nameplate-title`, `.site-nameplate-byline`,
   `.masthead-title`, `.landing-tagline`, `.lead-title`, `.entry-numeral`,
   `.entry-title`). Intentional fluid typography for display elements
   outside the standard `--text-*` scale, ratified under issue #274
   ("Phosphor broadsheet") — not a font-floor violation (every clamp()
   minimum is well above the 13px floor; this category exists to catch
   *unverifiable* sizes, and these have been manually verified instead).

None of these are weakened token values or silently-widened suppression:
`scripts/remarque-audit-baseline.json` is an exact `(file, line, category)`
allowlist, generated from and matching the current audit output 1:1. If
any flagged line moves — including these — the entry stops matching and
resurfaces as a real, blocking failure requiring re-review (fail-closed).
`scripts/run-remarque-audit.mjs` additionally hard-codes, independent of
the baseline file's contents, that CONTRAST and GAMUT failures (the
`--palette` checks) can never be suppressed — only `--src` source-scan
findings are eligible.

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

## 8. Syntax-highlighting palette (remarque-tokens 0.15.0)

Bumped `remarque-tokens` from 0.8.0 → 0.15.0 (issue: this migration) and
adopted the "Syntax Highlighting" section of `REMARQUE.md`: `astro.config.mjs`
now passes Shiki's `createCssVariablesTheme({ variablePrefix:
'--color-syntax-' })` as a single theme object (replacing the previous
`themes: { light: 'github-light', dark: 'github-dark' }` dual-theme vendor
config), and `global.css` adds the required `.astro-code` CSS bridge plus
the 9 `--color-syntax-*` palette-tier slots to all three palette blocks
(`:root`, `:root.dark`, the `@media (prefers-color-scheme: dark) :root:not(.light)`
block).

The 9 slots are copied from remarque-tokens' own default palette (ANSI-derived,
targeted at `--color-code-bg`, not this site's accent hue) rather than
re-derived from Palette B's green/ferric-red accent — per REMARQUE.md, a quiet
hue-spread syntax ramp is the intended look regardless of a site's own accent.
All 9 are audit-verified (`pnpm audit:remarque`) ≥ 4.5:1 against this site's
own `--color-code-bg` in both themes, not just trusted from upstream.

Three light-theme slots needed solving (upstream defaults are tuned against
remarque's own lighter `--color-code-bg`, `oklch(0.945 0.005 80)`; this site's
is `oklch(0.92 0.015 75)`, slightly darker):

| Slot | Upstream default | This site | Rationale |
|---|---|---|---|
| `--color-syntax-string` | `oklch(0.50 0.12 145)` (4.49:1 here) | `oklch(0.49 0.12 145)` (4.69:1) | Darkened to clear 4.5:1 against this site's code-bg |
| `--color-syntax-comment` | `oklch(0.52 0.01 80)` (4.35:1 here) | `oklch(0.505 0.01 80)` (4.63:1) | Same fix |
| `--color-syntax-punctuation` | `oklch(0.52 0.01 80)` (4.35:1 here) | `oklch(0.505 0.01 80)` (4.63:1) | Same source triple as comment, same fix |

All other 6 slots (`keyword`, `constant`, `function`, `type`, `variable`,
`link`) match the upstream default byte-for-byte in both themes and clear
4.5:1 unmodified. `node node_modules/remarque-tokens/scripts/drift-check.mjs`
correctly classifies all 3 solved values as palette-tier INFO (sanctioned
personalization), never FAIL.

Not extended to `theme-deck.css`'s 12 terminal palettes in this migration —
each deck defines its own `--color-code-bg`/`--color-code-fg` but none
currently overrides `--color-syntax-*`, so highlighted code under an active
theme-deck renders with this section's base-palette syntax colors (verified
non-broken, just not deck-tuned/contrast-audited per-deck). Tracked as a
follow-up, not a regression: `remarque-audit`'s CONTRAST check only ever ran
against the `--palette` file (`global.css`), not `theme-deck.css`, before this
change either.

## References

- Issue #324 (this migration)
- Issue #274 ("Phosphor broadsheet," Direction B, ratified 7-0)
- remarque#47 ("Layered token architecture," ratified 6-1) — Token
  Tiers doc: `remarque-tokens`'s `REMARQUE.md`
- remarque-tokens 0.5.0 `CHANGELOG.md` — "Theme-convention unification"
  (remarque#47 item 4, ratified 3-0), the release that unblocked §6
- Issue #283 (accent-font lint, `--font-accent` allowlist)
