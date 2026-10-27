# Trimmed font files (issue #661)

Derived from the Fontsource variable builds the site used before (same faces, same look). Nothing is redrawn: each file is the original with unused axes and glyphs removed.

Regenerate with `bash scripts/subset-fonts.sh` (needs `curl` and `uv`; uses fontTools `varLib.instancer` and `pyftsubset`, woff2 output, all OpenType layout features kept). Source versions are pinned in the script.

| File | Source | Change |
|---|---|---|
| `fraunces-normal/italic.woff2` | `@fontsource-variable/fraunces@5.3.0` latin `full` | SOFT pinned 0, WONK pinned 1 (the font's defaults; CSS never sets them); `opsz` and `wght` kept whole; glyph subset |
| `source-serif-4-normal/italic.woff2` | `@fontsource-variable/source-serif-4@5.3.1` latin `opsz` | `wght` trimmed to 400-900 / 400-700 (census of every built page: 400-900 normal, 400-600 italic); `opsz` kept; glyph subset |
| `source-serif-4-greek-*.woff2` | same, greek | `wght` trimmed to match the latin faces |
| `shantell-sans-400.woff2` | `@fontsource-variable/shantell-sans@5.3.0` latin `full` | static wght 400 instance (the only weight used); INFM/BNCE/SPAC at defaults; glyph subset |

Glyph subset (`unicode-range` in `astro.config.mjs` must match): Basic Latin, Latin-1, U+0131, U+0152-0153, U+2010-2027, U+2030-203A, U+2122, U+2190-2193, U+2212, U+20AC. Anything outside falls through to the next family in the stack, as it did before.

Two things that bite when changing this: Chrome groups `@font-face` rules by weight range, so Greek must declare the same range as latin or it shadows the latin face; and trimming Fraunces' `wght` axis shifted edge pixels in screenshots, so it is left whole.

Licences: all three families are SIL OFL 1.1; texts in `licenses/`. None reserves a font name. Adobe's own Source Serif release reserves "Source", but these files derive from the Google Fonts build that Fontsource ships, whose OFL (copied here from google/fonts `ofl/sourceserif4/OFL.txt`) has no Reserved Font Name, so subsetting it is permitted as-is.
