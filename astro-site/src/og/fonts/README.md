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
