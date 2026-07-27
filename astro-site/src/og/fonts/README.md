# OG card fonts

`FreeSans.ttf` / `FreeSansBold.ttf` are subsets (Latin + common punctuation,
~40KB each) of **GNU FreeFont** (https://www.gnu.org/software/freefont/),
licensed **GPLv3 with the font exception**, which permits embedding the font
in generated documents/images without affecting their license.

Used only at build time by `../card.ts` to rasterize per-post OG/social cards.
Regenerate a subset with:

```
pyftsubset FreeSansBold.ttf --unicodes="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-205E,U+2022,U+20AC,U+2122" --output-file=FreeSansBold.ttf
```

## ShantellSans.ttf (zine kicker, #283 "go maximal")

The site's `--font-accent` (Shantell Sans, used for `.hand-note` marginalia
in `src/styles/zine.css`) is loaded in the browser as a **variable** font via
Astro's Fontsource font provider (`astro.config.mjs`). **satori cannot render
variable fonts** — it needs a static-instance TTF, or the glyphs silently
fail to render (no error, just missing/fallback text).

`ShantellSans.ttf` is a static instance, sourced from Fontsource's
pre-instanced weight-500 static woff2 (not the `:vf` variable package),
converted to TTF and subsetted the same way as the FreeSans files above:

```bash
curl -o shantell-500.woff2 \
  https://cdn.jsdelivr.net/fontsource/fonts/shantell-sans@latest/latin-500-normal.woff2

python3 -c "
from fontTools.ttLib import TTFont
f = TTFont('shantell-500.woff2')
assert 'fvar' not in f, 'still variable — pick a different source'
f.flavor = None
f.save('shantell-500.ttf')
"

pyftsubset shantell-500.ttf \
  --unicodes="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-205E,U+2022,U+20AC,U+2122" \
  --layout-features='' --no-hinting \
  --output-file=ShantellSans.ttf
```

Licensed **SIL Open Font License 1.1** (Shantell Sans Project Authors,
https://github.com/arrowtype/shantell-sans), which permits embedding.

Only ASCII/Latin-1 punctuation is subsetted in, matching FreeSans — any
symbol outside that range (e.g. `✦`, U+2726) will render invisibly with no
build error. Check a codepoint before using it:

```bash
python3 -c "
from fontTools.ttLib import TTFont
print(0x2726 in TTFont('ShantellSans.ttf').getBestCmap())
"
```
