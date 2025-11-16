#!/usr/bin/env -S uv run python3
"""
WCAG AAA Contrast Validator
Validates button and text color combinations for 7:1 minimum contrast ratio

Usage:
    uv run python scripts/validation/contrast-validator.py

Requirements:
    - Python 3.10+
    - No external dependencies (uses only stdlib)
"""

import math
import re
import sys
from pathlib import Path
from typing import Tuple, Dict, List
from dataclasses import dataclass

# Add lib directory to path for logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)


@dataclass
class ColorPair:
    """Color pair with foreground and background"""
    name: str
    foreground: str  # OKLCH or hex
    background: str  # OKLCH or hex
    context: str  # Button, link, text, etc.


def oklch_to_rgb(lightness: float, chroma: float, hue: float) -> Tuple[int, int, int]:
    """
    Convert OKLCH to RGB (simplified approximation)
    For accurate conversion, use a proper color library in production

    This is a simplified conversion for validation purposes.
    """
    # Convert hue to radians
    hue_rad = math.radians(hue)

    # Convert OKLCH to LAB
    a = chroma * math.cos(hue_rad)
    b = chroma * math.sin(hue_rad)
    L = lightness * 100

    # LAB to XYZ (D65 illuminant)
    y = (L + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    def lab_to_xyz(t):
        if t > 6/29:
            return t ** 3
        else:
            return 3 * (6/29)**2 * (t - 4/29)

    x = 0.95047 * lab_to_xyz(x)
    y = 1.00000 * lab_to_xyz(y)
    z = 1.08883 * lab_to_xyz(z)

    # XYZ to RGB (sRGB)
    r =  3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    b =  0.0557 * x - 0.2040 * y + 1.0570 * z

    def gamma_correction(c):
        if c <= 0.0031308:
            return 12.92 * c
        else:
            return 1.055 * (c ** (1/2.4)) - 0.055

    r = gamma_correction(r)
    g = gamma_correction(g)
    b = gamma_correction(b)

    # Clamp and convert to 0-255
    r = max(0, min(255, int(r * 255)))
    g = max(0, min(255, int(g * 255)))
    b = max(0, min(255, int(b * 255)))

    return (r, g, b)


def parse_oklch(oklch_str: str) -> Tuple[int, int, int]:
    """Parse OKLCH string like 'oklch(75% 0.19 50)' to RGB"""
    match = re.match(r'oklch\((\d+(?:\.\d+)?)%?\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\)', oklch_str)
    if not match:
        raise ValueError(f"Invalid OKLCH format: {oklch_str}")

    lightness = float(match.group(1)) / 100  # Convert percentage to 0-1
    chroma = float(match.group(2))
    hue = float(match.group(3))

    return oklch_to_rgb(lightness, chroma, hue)


def parse_hex(hex_str: str) -> Tuple[int, int, int]:
    """Parse hex color like '#FF5733' to RGB"""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Calculate relative luminance for WCAG contrast formula"""
    def linearize(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    R = linearize(r)
    G = linearize(g)
    B = linearize(b)

    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(color1: str, color2: str) -> float:
    """Calculate WCAG contrast ratio between two colors"""
    # Parse colors
    if color1.startswith('oklch'):
        rgb1 = parse_oklch(color1)
    elif color1.startswith('#'):
        rgb1 = parse_hex(color1)
    else:
        raise ValueError(f"Unsupported color format: {color1}")

    if color2.startswith('oklch'):
        rgb2 = parse_oklch(color2)
    elif color2.startswith('#'):
        rgb2 = parse_hex(color2)
    else:
        raise ValueError(f"Unsupported color format: {color2}")

    # Calculate luminance
    L1 = relative_luminance(rgb1)
    L2 = relative_luminance(rgb2)

    # Calculate contrast ratio
    lighter = max(L1, L2)
    darker = min(L1, L2)

    return (lighter + 0.05) / (darker + 0.05)


def validate_contrast(color_pairs: List[ColorPair]) -> None:
    """Validate contrast ratios for color pairs"""
    logger.info("=" * 80)
    logger.info("WCAG AAA CONTRAST VALIDATION (7:1 minimum for body text)")
    logger.info("=" * 80)
    logger.info("")

    results = []
    all_pass = True

    for pair in color_pairs:
        try:
            ratio = contrast_ratio(pair.foreground, pair.background)
            passes_aaa = ratio >= 7.0
            passes_aa = ratio >= 4.5

            status = "✅ PASS AAA" if passes_aaa else ("✅ PASS AA" if passes_aa else "❌ FAIL")

            results.append({
                'name': pair.name,
                'context': pair.context,
                'ratio': ratio,
                'passes_aaa': passes_aaa,
                'passes_aa': passes_aa,
                'status': status
            })

            if not passes_aaa:
                all_pass = False

            logger.info(f"{status:15} {pair.name:40} {ratio:5.2f}:1 ({pair.context})")
            logger.info(f"               FG: {pair.foreground}")
            logger.info(f"               BG: {pair.background}")
            logger.info("")

        except Exception as e:
            logger.error(f"❌ ERROR      {pair.name:40} - {str(e)}")
            logger.info("")
            all_pass = False

    logger.info("=" * 80)
    logger.info(f"TOTAL: {len(results)} color pairs tested")
    aaa_count = sum(1 for r in results if r['passes_aaa'])
    aa_count = sum(1 for r in results if r['passes_aa'] and not r['passes_aaa'])
    fail_count = sum(1 for r in results if not r['passes_aa'])

    logger.info(f"AAA (7:1+):  {aaa_count} pairs")
    logger.info(f"AA (4.5:1+): {aa_count} pairs")
    logger.info(f"FAIL:        {fail_count} pairs")
    logger.info("=" * 80)

    if all_pass:
        logger.info("✅ All color combinations meet WCAG AAA standards!")
    else:
        logger.warning("⚠️  Some color combinations need adjustment for AAA compliance.")
        logger.info("   Consider increasing contrast or using larger text (AA standard).")


def main():
    """Main validation function"""
    # Define color pairs from modern-design.css and theme-tokens.css
    color_pairs = [
        # Light mode buttons (UPDATED for AAA compliance)
        ColorPair(
            "Primary button (light)",
            "oklch(98% 0.01 25)",  # warm white text
            "oklch(45% 0.18 25)",  # darker burnt orange background (was 55%)
            "Button text"
        ),
        ColorPair(
            "Secondary button (light)",
            "oklch(98% 0.01 160)",  # cool white text
            "oklch(45% 0.15 160)",  # deep teal background (already compliant)
            "Button text"
        ),
        ColorPair(
            "Tertiary button (light)",
            "oklch(98% 0.01 320)",  # pink-white text
            "oklch(40% 0.20 320)",  # much darker deep rose background (was 50%)
            "Button text"
        ),

        # Dark mode buttons
        ColorPair(
            "Primary button (dark)",
            "oklch(15% 0.01 50)",  # very dark warm text
            "oklch(75% 0.19 50)",  # warm coral background
            "Button text"
        ),
        ColorPair(
            "Secondary button (dark)",
            "oklch(15% 0.01 110)",  # very dark cool text
            "oklch(80% 0.15 110)",  # bright lime background
            "Button text"
        ),
        ColorPair(
            "Tertiary button (dark)",
            "oklch(98% 0.01 340)",  # nearly white text
            "oklch(70% 0.20 340)",  # electric magenta background
            "Button text"
        ),

        # Light mode body text
        ColorPair(
            "Body text (light)",
            "oklch(25% 0.02 270)",  # rich charcoal text
            "oklch(98% 0.01 80)",  # warm off-white background
            "Body text"
        ),
        ColorPair(
            "Secondary text (light)",
            "oklch(45% 0.02 270)",  # medium gray text
            "oklch(98% 0.01 80)",  # warm off-white background
            "Secondary text"
        ),

        # Dark mode body text
        ColorPair(
            "Body text (dark)",
            "oklch(95% 0.01 270)",  # nearly white text
            "oklch(15% 0.02 270)",  # deep purple-black background
            "Body text"
        ),
        ColorPair(
            "Secondary text (dark)",
            "oklch(70% 0.02 270)",  # muted purple-gray text
            "oklch(15% 0.02 270)",  # deep purple-black background
            "Secondary text"
        ),

        # Links (UPDATED for AAA compliance)
        ColorPair(
            "Link (light)",
            "oklch(45% 0.18 25)",  # darker burnt orange link (was 55%)
            "oklch(98% 0.01 80)",  # warm off-white background
            "Link"
        ),
        ColorPair(
            "Link (dark)",
            "oklch(75% 0.19 50)",  # warm coral link
            "oklch(15% 0.02 270)",  # deep purple-black background
            "Link"
        ),
    ]

    validate_contrast(color_pairs)


if __name__ == "__main__":
    main()
