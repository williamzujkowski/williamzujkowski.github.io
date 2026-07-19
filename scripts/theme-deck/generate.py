#!/usr/bin/env python3
"""Generate the site's theme deck from the oklch-terminal-themes dataset.

Reads a clone of github.com/williamzujkowski/oklch-terminal-themes and emits:
  astro-site/src/data/theme-deck.json         (picker UI data)
  astro-site/src/data/theme-deck-attribution.json  (colophon credits)
  astro-site/src/styles/theme-deck.css        (generated token overrides)

Every emitted token value is a resolved oklch() literal validated against
WCAG contrast floors here, at generation time. A theme that cannot satisfy
the floors fails the run — nothing contrast-broken can ship.

Usage: python3 scripts/theme-deck/generate.py /path/to/oklch-terminal-themes
"""

import json
import math
import sys
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parents[2]

# Curated picks: popular + wcag-aaa, hand-selected for range and recognition.
# Classic solarized fails AAA (fg/bg 4.7 dark, 4.1 light) so the
# higher-contrast variant stands in; no AAA solarized-light exists.
CURATED = [
    "dracula",
    "nord",
    "catppuccin-mocha",
    "tokyonight",
    "gruvbox-dark-hard",
    "kanagawa-wave",
    "rose-pine",
    "solarized-dark-higher-contrast",
    "github-light-default",
    "gruvbox-light-hard",
    "catppuccin-latte",
    "nord-light",
]

# Compact display names where the upstream name is a mouthful.
DISPLAY_NAME = {
    "solarized-dark-higher-contrast": "Solarized Dark+",
    "github-light-default": "GitHub Light",
}

# A theme's characteristic accent hue, tried first (must still clear the
# contrast floor, else the chroma heuristic decides).
PREFERRED_ACCENT = {
    "dracula": ["purple", "brightPurple"],
    "nord": ["blue", "cyan", "brightBlue"],
    "catppuccin-mocha": ["purple", "blue", "brightPurple"],
    "tokyonight": ["blue", "cyan", "brightBlue"],
    "gruvbox-dark-hard": ["yellow", "brightYellow"],
    "kanagawa-wave": ["blue", "yellow", "brightBlue"],
    "rose-pine": ["purple", "red"],
    "solarized-dark-higher-contrast": ["blue", "cyan", "brightBlue"],
    "github-light-default": ["blue", "purple", "brightBlue"],
    "gruvbox-light-hard": ["red", "yellow"],
    "catppuccin-latte": ["purple", "blue"],
    "nord-light": ["blue", "cyan"],
}

ACCENT_CANDIDATES = [
    "blue", "cyan", "green", "purple", "red", "yellow",
    "brightBlue", "brightCyan", "brightGreen", "brightPurple", "brightRed", "brightYellow",
]

FG_ON_BG_FLOOR = 7.0      # AAA body text
ACCENT_FLOOR = 4.5        # links / interactive
MUTED_FLOOR = 4.5         # meta text is still text


# --- oklch -> sRGB (standard Björn Ottosson matrices) ---------------------

def oklch_to_linear_srgb(l, c, h):
    a = c * math.cos(math.radians(h))
    b = c * math.sin(math.radians(h))
    l_ = (l + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (l - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (l - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return tuple(min(1.0, max(0.0, v)) for v in (r, g, bl))


def luminance(lch):
    r, g, b = oklch_to_linear_srgb(*lch)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(lch1, lch2):
    y1, y2 = luminance(lch1), luminance(lch2)
    lighter, darker = max(y1, y2), min(y1, y2)
    return (lighter + 0.05) / (darker + 0.05)


def mix(lch_a, lch_b, share_a):
    """Approximate color-mix(in oklch, A share%, B) — linear l/c, shortest-arc hue."""
    la, ca, ha = lch_a
    lb, cb, hb = lch_b
    t = share_a
    dh = ((hb - ha + 180) % 360) - 180
    return (la * t + lb * (1 - t), ca * t + cb * (1 - t), (ha + dh * (1 - t)) % 360)


def css(lch):
    l, c, h = lch
    return f"oklch({l:.4f} {c:.4f} {h:.1f})"


def as_lch(color):
    o = color["oklch"]
    return (o["l"], o["c"], o["h"])


def find_mix_share(fg, bg, start_share, floor):
    """Smallest fg share >= start_share whose mix clears the contrast floor."""
    share = start_share
    while share <= 1.0:
        if contrast(mix(fg, bg, share), bg) >= floor:
            return share
        share += 0.05
    raise SystemExit(f"cannot reach contrast {floor} even at 100% fg")


def deepen(lch, fg, bg):
    """Mix a color toward fg until it clears the accent floor (keeps its hue)."""
    for share in range(0, 101, 5):
        candidate = mix(fg, lch, share / 100)
        if contrast(candidate, bg) >= ACCENT_FLOOR:
            return candidate
    return fg


def pick_accent(colors, bg, fg, slug):
    for slot in PREFERRED_ACCENT.get(slug, []):
        lch = as_lch(colors[slot])
        if contrast(lch, bg) >= ACCENT_FLOOR:
            others = [as_lch(colors[s]) for s in ACCENT_CANDIDATES
                      if s != slot and contrast(as_lch(colors[s]), bg) >= ACCENT_FLOOR]
            hover = max(others, key=lambda c: c[1]) if others else mix(fg, lch, 0.25)
            return lch, hover, slot
    scored = []
    for slot in ACCENT_CANDIDATES:
        lch = as_lch(colors[slot])
        ratio = contrast(lch, bg)
        if ratio >= ACCENT_FLOOR:
            scored.append((lch[1], ratio, slot, lch))  # chroma first: vivid over merely legible
    if not scored:
        # Light themes often have no AA-passing ANSI slot. Take the most
        # chromatic candidate and deepen it toward fg until it passes —
        # hue identity survives, the floor is guaranteed.
        best = max(ACCENT_CANDIDATES, key=lambda s: as_lch(colors[s])[1])
        lch = deepen(as_lch(colors[best]), fg, bg)
        return lch, mix(fg, lch, 0.25), f"{best} (deepened)"
    scored.sort(reverse=True)
    accent = scored[0]
    hover = next((s[3] for s in scored[1:] if s[2] != accent[2]), None)
    if hover is None:
        # Only one passing slot (e.g. catppuccin-latte): derive a hover shade
        # instead of duplicating the accent, which would kill :hover feedback.
        hover = mix(fg, accent[3], 0.25)
    return accent[3], hover, accent[2]


def build_theme(t):
    colors = t["colors"]
    bg = as_lch(colors["background"])
    fg = as_lch(colors["foreground"])

    if contrast(fg, bg) < FG_ON_BG_FLOOR:
        raise SystemExit(f"{t['slug']}: fg/bg {contrast(fg, bg):.2f} below AAA floor")

    accent, hover, accent_slot = pick_accent(colors, bg, fg, t["slug"])
    if css(accent) == css(hover):
        raise SystemExit(f"{t['slug']}: accent and accent-hover are identical")

    fg_muted = mix(fg, bg, find_mix_share(fg, bg, 0.70, MUTED_FLOOR))
    muted = mix(fg, bg, find_mix_share(fg, bg, 0.55, MUTED_FLOOR))

    selection = as_lch(colors["selection"])
    if contrast(fg, selection) < ACCENT_FLOOR:
        selection = mix(accent, bg, 0.25)  # dataset selection too close to fg — derive instead

    tokens = {
        "--color-bg": bg,
        "--color-bg-subtle": mix(fg, bg, 0.03),
        "--color-fg": fg,
        "--color-fg-muted": fg_muted,
        "--color-muted": muted,
        "--color-border": mix(fg, bg, 0.15),
        "--color-border-bold": mix(fg, bg, 0.40),
        "--color-surface": mix(fg, bg, 0.04),
        "--color-accent": accent,
        "--color-accent-hover": hover,
        "--color-code-bg": mix(fg, bg, 0.06),
        "--color-code-fg": fg,
        "--color-selection-bg": selection,
    }

    ansi = [css(as_lch(colors[s])) for s in
            ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")]

    return {
        "slug": t["slug"],
        "name": DISPLAY_NAME.get(t["slug"], t["name"]),
        "isDark": t["isDark"],
        "accentSlot": accent_slot,
        "tokens": {k: css(v) for k, v in tokens.items()},
        "swatches": {"bg": css(bg), "fg": css(fg), "accent": css(accent), "ansi": ansi},
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    dataset = Path(sys.argv[1]) / "data" / "themes.json"
    raw = json.loads(dataset.read_text())
    themes = raw["themes"] if isinstance(raw, dict) else raw
    by_slug = {t["slug"]: t for t in themes}

    missing = [s for s in CURATED if s not in by_slug]
    if missing:
        raise SystemExit(f"curated slugs missing from dataset: {missing}")

    built, attribution = [], []
    for slug in CURATED:
        t = by_slug[slug]
        built.append(build_theme(t))
        attribution.append({
            "slug": slug, "name": t["name"],
            "source": t["source"],
            # Upstream sourceUrls carry literal spaces (invalid URIs) —
            # percent-encode the path, keeping scheme/host/slashes intact.
            "sourceUrl": quote(t["sourceUrl"], safe=":/"),
        })

    data_dir = REPO_ROOT / "astro-site" / "src" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "theme-deck.json").write_text(json.dumps(built, indent=2) + "\n")
    (data_dir / "theme-deck-attribution.json").write_text(json.dumps(attribution, indent=2) + "\n")

    lines = [
        "/* GENERATED by scripts/theme-deck/generate.py — do not edit by hand.",
        " * Token values are resolved oklch() literals, contrast-validated at",
        " * generation time (fg/bg >= 7, accent & muted >= 4.5). */",
        "",
    ]
    for theme in built:
        s = theme["slug"]
        # .dark/.light variants outrank :root.dark and the prefers-color-scheme
        # block on specificity, so a picked deck theme wins in every mode.
        lines.append(
            f":root[data-theme-deck='{s}'],\n"
            f":root[data-theme-deck='{s}'].dark,\n"
            f":root[data-theme-deck='{s}'].light {{"
        )
        lines.append(f"  color-scheme: {'dark' if theme['isDark'] else 'light'};")
        for k, v in theme["tokens"].items():
            lines.append(f"  {k}: {v};")
        lines.append("}")
        lines.append("")
    (REPO_ROOT / "astro-site" / "src" / "styles" / "theme-deck.css").write_text("\n".join(lines))

    for theme in built:
        print(f"{theme['slug']:32} accent={theme['accentSlot']:12} ok")
    print(f"\n{len(built)} themes -> theme-deck.json / theme-deck.css / attribution.json")


if __name__ == "__main__":
    main()
