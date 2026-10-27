#!/usr/bin/env bash
# Regenerates src/fonts/*.woff2 (issue #661). Usage: bash scripts/subset-fonts.sh
# Needs curl and uv. Sources: the exact Fontsource variable builds Astro used
# before (pinned below). Each output is the same face with unused axis range
# and unused glyphs removed; nothing is redrawn. See src/fonts/README.md.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=src/fonts; mkdir -p "$OUT"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/fonts.XXXXXX"); trap 'rm -rf "$WORK"' EXIT
CDN=https://cdn.jsdelivr.net/npm/@fontsource-variable
FR=fraunces@5.3.0; SS=source-serif-4@5.3.1; SH=shantell-sans@5.3.0
# Basic Latin, Latin-1, dotless i, OE, general punctuation, arrows, minus, euro, TM.
U="U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,U+2010-2027,U+2030-203A,U+2122,U+2190-2193,U+2212,U+20AC"
FT=(uvx --from fonttools --with brotli)
fetch() { curl -fsSL "$CDN/$1/files/$2" -o "$WORK/$2"; }
# fontTools tool, source file, output name, instancer axis pins, [unicodes]
make() {
  local src=$1 out=$2 unicodes=$3; shift 3
  "${FT[@]}" fonttools varLib.instancer "$WORK/$src" "$@" -o "$WORK/$out.ttf" >/dev/null
  "${FT[@]}" pyftsubset "$WORK/$out.ttf" --unicodes="$unicodes" --layout-features='*' \
    --flavor=woff2 --output-file="$OUT/$out.woff2"
}
# Fraunces: SOFT=0 / WONK=1 are the font's own defaults and the CSS never sets them.
# wght is NOT trimmed: re-basing the weight axis changed edge pixels (verified by screenshot diff).
fetch $FR fraunces-latin-full-normal.woff2; fetch $FR fraunces-latin-full-italic.woff2
make fraunces-latin-full-normal.woff2 fraunces-normal "$U" SOFT=0 WONK=1
make fraunces-latin-full-italic.woff2 fraunces-italic "$U" SOFT=0 WONK=1
# Source Serif 4: opsz kept (font-optical-sizing is auto), wght trimmed.
fetch $SS source-serif-4-latin-opsz-normal.woff2; fetch $SS source-serif-4-latin-opsz-italic.woff2
make source-serif-4-latin-opsz-normal.woff2 source-serif-4-normal "$U" wght=400:900
make source-serif-4-latin-opsz-italic.woff2 source-serif-4-italic "$U" wght=400:700
fetch $SS source-serif-4-greek-opsz-normal.woff2; fetch $SS source-serif-4-greek-opsz-italic.woff2
# Greek must declare the SAME weight range as latin: Chrome groups @font-face rules by
# (style, weight range), so a wider Greek range would shadow the latin face entirely.
G="U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF"
make source-serif-4-greek-opsz-normal.woff2 source-serif-4-greek-normal "$G" wght=400:900
make source-serif-4-greek-opsz-italic.woff2 source-serif-4-greek-italic "$G" wght=400:700
# Shantell Sans: one static instance at wght 400 (the only weight used); other axes at defaults.
fetch $SH shantell-sans-latin-full-normal.woff2
make shantell-sans-latin-full-normal.woff2 shantell-sans-400 "$U" wght=400 INFM=0 BNCE=0 SPAC=0
# OFL 1.1 texts travel with the derived files.
mkdir -p "$OUT/licenses"
for pkg in fraunces@5.3.0 source-serif-4@5.3.1 shantell-sans@5.3.0; do
  curl -fsSL "$CDN/$pkg/LICENSE" -o "$OUT/licenses/${pkg%@*}-OFL.txt"
done
ls -l "$OUT"/*.woff2
