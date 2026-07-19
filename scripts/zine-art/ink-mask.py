#!/usr/bin/env python3
"""Convert a generated ink drawing into a theme-recolorable alpha mask.

Takes black-ink-on-paper raster art (e.g. from `agy` image generation),
thresholds away paper texture/grid lines, crops to content, downscales,
and emits a grayscale+alpha PNG where ink = opaque. The site renders it
via `mask-image: url(...)` + `background: var(--color-fg|--color-accent)`,
so one asset repaints across all 14 palettes. PIL re-encode strips any
generator metadata (design-review condition).

Authoring-time tool only — never runs in CI (#282).

Usage: ink-mask.py IN.png OUT.png [--threshold 128] [--width 640] [--pad 12]
"""

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--threshold", type=int, default=128,
                    help="gray level below which a pixel counts as ink (0-255)")
    ap.add_argument("--width", type=int, default=640,
                    help="max output width in px")
    ap.add_argument("--pad", type=int, default=12,
                    help="padding around the content crop, in source px")
    args = ap.parse_args()

    gray = Image.open(args.src).convert("L")

    # Ink -> alpha: darker than threshold becomes opacity, scaled so soft
    # antialiased edges keep partial alpha instead of stair-stepping.
    alpha = gray.point(
        lambda v: 0 if v >= args.threshold else min(255, int((args.threshold - v) * 255 / args.threshold))
    )

    bbox = alpha.getbbox()
    if bbox is None:
        raise SystemExit("no ink found below threshold — lower --threshold?")
    pad = args.pad
    bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
            min(alpha.width, bbox[2] + pad), min(alpha.height, bbox[3] + pad))
    alpha = alpha.crop(bbox)

    if alpha.width > args.width:
        h = round(alpha.height * args.width / alpha.width)
        alpha = alpha.resize((args.width, h), Image.LANCZOS)

    # LA: luminance is irrelevant (mask uses alpha); keep it flat black.
    out = Image.merge("LA", (Image.new("L", alpha.size, 0), alpha))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.out, optimize=True)

    kb = args.out.stat().st_size / 1024
    print(f"{args.out} {out.size[0]}x{out.size[1]} {kb:.1f}KB")
    if kb > 60:
        raise SystemExit(f"over the 60KB budget ({kb:.1f}KB) — raise threshold or shrink width")


if __name__ == "__main__":
    main()
