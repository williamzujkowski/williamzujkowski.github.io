# Theme Customization Guide

This document explains how to customize the site's appearance using the OKLCH color theme system.

## Overview

The website now uses OKLCH color format for all colors, providing better perceptual uniformity and consistency across different displays. The theme system is built with CSS variables and configurable through a JSON configuration file.

## Theme Configuration

The theme is defined in the file: `/src/_data/config/theme.json`

### Example Configuration

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
    "accentLightness": 0.70,
    
    "backgroundColor": "oklch(0.16 0.02 250)",
    "surfaceColor": "oklch(0.20 0.02 250)",
    "borderColor": "oklch(0.30 0.02 250)",
    "textColor": "oklch(0.93 0.02 250)",
    "textSecondaryColor": "oklch(0.75 0.03 250)"
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

OKLCH is a perceptually uniform color space that represents colors with three values:

1. **Lightness** - A value from 0 (black) to 1 (white)
2. **Chroma** - Color saturation (intensity), typically from 0 to 0.4
3. **Hue** - The color angle around the color wheel (0-360 degrees)

### Benefits of OKLCH

- More perceptually uniform than RGB or HSL
- Better for creating accessible color palettes
- More predictable when creating color scales 
- Consistent across different displays

## Creating Themes Using the Generator

For convenience, a theme generator script is included to help you create new themes:

```bash
node tools/generate-theme.js --name "Ocean Blue" --primary-hue 220 --primary-chroma 0.15 --accent-hue 280
```

### Available Parameters

- `--name` - Theme name
- `--description` - Theme description
- `--primary-hue` - Primary color hue (0-360)
- `--primary-chroma` - Primary color chroma/saturation (0-0.4)
- `--primary-lightness` - Primary color lightness (0-1)
- `--accent-hue` - Accent color hue (0-360)
- `--accent-chroma` - Accent color chroma/saturation (0-0.4)
- `--accent-lightness` - Accent color lightness (0-1)
- `--background-color` - Complete OKLCH color for background
- `--surface-color` - Complete OKLCH color for surface elements
- `--border-color` - Complete OKLCH color for borders
- `--gray-light-color` - Complete OKLCH color for lighter gray elements
- `--text-color` - Complete OKLCH color for text
- `--text-secondary-color` - Complete OKLCH color for secondary text
- `--muted-color` - Complete OKLCH color for muted text
- `--success-color` - Complete OKLCH color for success states
- `--warning-color` - Complete OKLCH color for warning states
- `--danger-color` - Complete OKLCH color for error/danger states
- `--info-color` - Complete OKLCH color for information states

## Using Theme Colors in Templates

The theme colors are available as CSS variables and utility classes:

### CSS Variables

```css
:root {
  --color-primary: oklch(0.56 0.15 145);
  --color-accent: oklch(0.70 0.15 230);
  --color-background: oklch(0.16 0.02 250);
  /* and many more... */
}
```

### CSS Classes

```html
<div class="bg-primary text-white">Primary background with white text</div>
<div class="bg-accent-100 text-accent-900">Light accent background with dark accent text</div>
<div class="border-accent hover:border-primary">Border that changes on hover</div>
```

## Theme CSS Files

The theme system consists of these files:

- `/src/css/theme.css` - Defines CSS variables and utility classes
- `/src/js/theme-utils.js` - JavaScript utilities for generating colors
- `/src/js/theme-switcher.js` - Handles theme switching and initialization
- `/tools/generate-theme.js` - CLI tool for creating themes

## Color Palette

Each theme includes these color scales:

### Primary Color Scale

Used for buttons, links, and primary actions.

- `--color-primary` - Base primary color
- `--color-primary-50` through `--color-primary-950` - Complete scale from light to dark

### Accent Color Scale

Used for highlights, secondary buttons, and decorative elements.

- `--color-accent` - Base accent color
- `--color-accent-50` through `--color-accent-950` - Complete scale from light to dark

### UI Colors

- `--color-background` - Page background
- `--color-surface` - Card and component surfaces
- `--color-border` - Borders and dividers
- `--color-gray-light` - Light gray UI elements

### Text Colors

- `--color-text` - Main text
- `--color-text-secondary` - Secondary text (less emphasis)
- `--color-muted` - Muted text (least emphasis)

### Alert/Status Colors

- `--color-success` - Success messages and indicators
- `--color-warning` - Warning messages and indicators
- `--color-danger` - Error messages and danger actions
- `--color-info` - Information messages

## Best Practices

1. Always use the CSS variables or utility classes rather than hardcoded colors
2. For new UI components, follow the color usage conventions in existing components
3. Maintain sufficient contrast ratios for accessibility
4. Use the theme generator for creating consistent new themes
5. When creating color combinations, check their appearance in both light and dark modes

## Useful Resources

- [OKLCH Color Picker](https://oklch.com/)
- [Perceptually uniform color spaces](https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/)
- [A Guide to OKLCH Color](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)