# Theme System Documentation

> This document is part of the [website documentation](../README.md).

This document explains the theme system implementation and usage for William Zujkowski's personal website.

## Overview

The theme system uses OKLCH colors for perceptually uniform color palettes that work well across different devices and accessibility settings. The system is designed to be:

- **Flexible**: Easily create new themes with different color palettes
- **Maintainable**: Centralized configuration in JSON files
- **Compatible**: Works with Tailwind CSS utility classes
- **Accessible**: Better contrast and readability with OKLCH colors

## Components

The theme system consists of these key components:

1. **Configuration Files**:

   - `src/_data/config/theme.json`: Central theme configuration
   - `src/css/styles.css`: CSS variables and Tailwind integration

2. **JavaScript Utilities**:

   - `src/js/theme-utils.js`: Core functions for OKLCH colors
   - `src/js/theme-switcher.js`: Theme initialization and switching

3. **Tools**:
   - `tools/generate-theme.js`: CLI utility for theme generation

## Theme Configuration

A theme is defined in JSON with properties for colors, shadows, borders, and animations:

```json
{
  "name": "GitHub Dark",
  "description": "Dark theme inspired by GitHub's dark mode with OKLCH colors",
  "isDark": true,
  "version": "1.0.0",
  "colors": {
    "primaryHue": 145,
    "primaryChroma": 0.15,
    "primaryLightness": 0.56,

    "accentHue": 230,
    "accentChroma": 0.15,
    "accentLightness": 0.7,

    "backgroundColor": "oklch(0.16 0.02 250)",
    "surfaceColor": "oklch(0.20 0.02 250)",
    "borderColor": "oklch(0.30 0.02 250)",
    "grayLightColor": "oklch(0.25 0.02 250)",
    "textColor": "oklch(0.93 0.02 250)",
    "textSecondaryColor": "oklch(0.75 0.03 250)",
    "mutedColor": "oklch(0.65 0.02 250)",

    "successColor": "oklch(0.56 0.15 145)",
    "warningColor": "oklch(0.75 0.15 80)",
    "dangerColor": "oklch(0.65 0.15 25)",
    "infoColor": "oklch(0.70 0.15 230)"
  },
  "shadows": {
    "card": "0 0 0 1px oklch(0.30 0.02 250)",
    "elevated": "0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.1)"
  },
  "borders": {
    "radius": "6px",
    "width": "1px"
  },
  "animation": {
    "transition": "0.3s ease",
    "hover": "-translate-y-1"
  }
}
```

## Understanding OKLCH Colors

OKLCH is a perceptual color space with three components:

- **L**: Lightness (0 to 1)
- **C**: Chroma/saturation (typically 0 to 0.4)
- **H**: Hue (0 to 360)

Example: `oklch(0.56 0.15 145)` is a medium green

Benefits over hex/RGB:

- Better perceptual uniformity
- Improved contrast for accessibility
- More intuitive color manipulation
- Consistent saturation and lightness

## CSS Implementation

The theme is implemented in CSS through custom properties:

```css
:root {
  /* Primary color scale */
  --color-primary: oklch(0.56 0.15 145);
  --color-primary-50: oklch(0.92 0.05 145);
  /* ...other color variables... */

  /* UI colors */
  --color-background: oklch(0.16 0.02 250);
  --color-text: oklch(0.93 0.02 250);

  /* Other design tokens */
  --shadow-card: 0 0 0 1px var(--color-border);
  --border-radius: 6px;
  --transition: 0.3s ease;
}
```

## Using the Theme in Templates

The theme variables are available in Tailwind utility classes:

```html
<div class="bg-surface text-text border border-border rounded-github">
  <h2 class="text-accent">Styled Heading</h2>
  <p class="text-text-secondary">Secondary text with themed colors</p>
  <button class="bg-primary hover:bg-primary-600 text-white">Button</button>
</div>
```

## Creating a New Theme

Use the theme generator tool:

```bash
# Using npm script
npm run generate:theme -- --name "Ocean Blue" --primary-hue 220 --primary-chroma 0.15 --accent-hue 280

# Or directly with node
node scripts/styling/generate-theme.js --name "Ocean Blue" --primary-hue 220 --primary-chroma 0.15 --accent-hue 280
```

Or manually create a theme file by copying and modifying the existing one.

## Utility Functions

The `theme-utils.js` file provides several helpful functions:

```javascript
// Generate CSS variables from theme config
const variables = generateThemeVariables(themeConfig);

// Create an OKLCH color string
const color = generateOklchColor(220, 0.15, 0.7);

// Modify colors
const lighterColor = lighten("oklch(0.5 0.2 180)", 0.1);
const darkerColor = darken("oklch(0.5 0.2 180)", 0.1);
const moreSaturated = saturate("oklch(0.5 0.2 180)", 0.05);
const lessSaturated = desaturate("oklch(0.5 0.2 180)", 0.05);
```

## Extending the Theme System

To extend the theme system:

1. Add new variables to `theme.json`
2. Update `theme-utils.js` to handle the new variables
3. Add corresponding CSS variables in `styles.css`
4. Create Tailwind utilities in `tailwind.config.cjs`

## Future Improvements

Planned enhancements:

- Multiple theme support and switching
- User preference persistence
- Theme preview tool
- Dark/light mode variants of each theme
- Auto-generation of additional color variants

---

[Back to Documentation Home](../index.md) | [Guides](./)
