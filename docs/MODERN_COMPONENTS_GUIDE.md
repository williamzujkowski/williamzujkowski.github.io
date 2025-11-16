# Modern Design Components - Usage Guide

**Version:** 1.0.0
**Date:** 2025-11-15
**Author:** Coder Agent #2

## Overview

This guide provides usage instructions for the modern design components implemented for the site redesign. All components follow the OKLCH color system and modern design principles outlined in `/redesign.md`.

## Component Catalog

### 1. Hero Section

**File:** `/src/_includes/components/hero-modern.njk`

**Usage:**
```njk
{% include "components/hero-modern.njk" %}
```

**Features:**
- Animated gradient mesh background
- Floating geometric shapes
- Parallax-ready profile image
- Stagger animations for child elements
- Responsive grid layout

**Customization:**
To customize content, edit the Nunjucks template directly. Key sections:
- Line 22: Main heading text
- Line 27: Description paragraph
- Line 33: CTA buttons (href and text)
- Line 47: Profile image path

---

### 2. Navigation (Frosted Glass)

**File:** `/src/_includes/components/nav-modern.njk`

**Usage:**
```njk
{% include "components/nav-modern.njk" %}
```

**Features:**
- Frosted glass effect with backdrop-filter
- Smooth active indicator animation
- Mobile-responsive with collapsible menu
- Dark mode toggle integrated

**Customization:**
- Requires `collections.all | eleventyNavigation` for menu items
- Expects `site.title` variable for logo
- Mobile menu toggles via `toggleMobileMenu()` function (already in base.njk)

---

### 3. Post Card

**File:** `/src/_includes/components/post-card-modern.njk`

**Usage:**
```njk
{% set post = postObject %}
{% include "components/post-card-modern.njk" %}
```

**Required Variables:**
- `post` - The post object with:
  - `post.data.title` - Post title
  - `post.data.description` - Post description
  - `post.date` - Publication date
  - `post.url` - Post URL
  - `post.data.image` (optional) - Featured image path
  - `post.data.tags` (optional) - Array of tags

**Example in Loop:**
```njk
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
  {% for post in collections.posts | reverse | limit(6) %}
    {% set post = post %}
    {% include "components/post-card-modern.njk" %}
  {% endfor %}
</div>
```

**Features:**
- 16:9 aspect ratio image
- Image zoom on hover
- Tag pills (max 3 shown, excluding "posts")
- Truncated description (3 lines)
- Lift + glow hover effect

---

### 4. Feature Card

**File:** `/src/_includes/components/feature-card-modern.njk`

**Usage:**
```njk
{% set icon = '<path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />' %}
{% set title = "Security Engineering" %}
{% set description = "Implementing Zero-Trust architectures for federal systems." %}
{% include "components/feature-card-modern.njk" %}
```

**Required Variables:**
- `icon` - SVG path data (as string)
- `title` - Card title
- `description` - Card description

**Example in Grid:**
```njk
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
  {% for feature in features %}
    {% set icon = feature.icon %}
    {% set title = feature.title %}
    {% set description = feature.description %}
    {% include "components/feature-card-modern.njk" %}
  {% endfor %}
</div>
```

**Features:**
- Gradient icon background (primary → secondary)
- Hover lift + glow effect
- Responsive padding and sizing

---

## CSS Classes Reference

### Typography

```css
.text-display       /* Display/heading font (Cabinet Grotesk/Satoshi) */
.text-subheading    /* Subheading font (General Sans/Plus Jakarta Sans) */
.text-body          /* Body font (Geist/DM Sans) with 1.7 line-height */
.text-feature       /* Feature/quote font (Fraunces variable) */
```

### Buttons

```css
.btn-modern                 /* Base button styles */
.btn-modern-primary         /* Gradient background button */
.btn-modern-secondary       /* Outline button with hover fill */
```

**Example:**
```html
<a href="/about/" class="btn-modern btn-modern-primary">
  Learn more
  <svg><!-- arrow icon --></svg>
</a>
```

### Cards

```css
.modern-card        /* Modern card with multi-layer shadows */
.post-card          /* Specialized post card component */
```

### Layout

```css
.hero-gradient-mesh     /* Hero section with animated gradient */
.nav-frosted           /* Frosted glass navigation */
.floating-shapes       /* Container for geometric shapes */
.floating-shape        /* Individual floating shape */
```

### Utilities

```css
.gradient-text-modern   /* Gradient text (primary → secondary) */
.quote-block           /* Styled quote with oversized quotation mark */
.tag-pill              /* Small pill-shaped tag */
.post-date             /* Monospace date styling */
.noise-texture         /* Subtle noise texture overlay */
.stagger-children      /* Stagger animation for child elements */
```

### Interactive States

```css
.transition-colors      /* Smooth color transitions */
.transition-transform   /* Smooth transform transitions */
.active-scale          /* Scale to 0.98 on click */
```

---

## CSS Custom Properties

### Typography Scale

```css
--text-xs      /* 14px (clamp responsive) */
--text-sm      /* 18px */
--text-base    /* 22px */
--text-lg      /* 28px */
--text-xl      /* 35px */
--text-2xl     /* 44px */
--text-3xl     /* 55px */
--text-4xl     /* 69px */
```

### Spacing

```css
--space-1      /* 4px */
--space-2      /* 8px */
--space-3      /* 12px */
--space-4      /* 16px */
--space-6      /* 24px */
--space-8      /* 32px */
--space-12     /* 48px */
--space-16     /* 64px */
--space-24     /* 96px */
--space-32     /* 128px */
```

### Colors (OKLCH)

**Light Mode:**
```css
--clr-light-bg-base           /* oklch(98% 0.01 80) */
--clr-light-bg-surface        /* oklch(95% 0.02 85) */
--clr-light-bg-elevated       /* oklch(100% 0 0) */

--clr-light-primary           /* oklch(55% 0.18 25) - burnt orange */
--clr-light-secondary         /* oklch(45% 0.15 160) - deep teal */
--clr-light-tertiary          /* oklch(50% 0.20 320) - deep rose */
--clr-light-success           /* oklch(50% 0.14 155) - forest green */
--clr-light-warning           /* oklch(55% 0.17 65) - amber */

--clr-light-text-primary      /* oklch(25% 0.02 270) - rich charcoal */
--clr-light-text-secondary    /* oklch(45% 0.02 270) - medium gray */
--clr-light-text-tertiary     /* oklch(60% 0.01 270) - light gray */
```

**Dark Mode:**
```css
--clr-dark-bg-base            /* oklch(15% 0.02 270) - purple-black */
--clr-dark-bg-surface         /* oklch(20% 0.03 270) - elevated */
--clr-dark-bg-elevated        /* oklch(25% 0.03 265) - interactive */

--clr-dark-primary            /* oklch(75% 0.19 50) - warm coral */
--clr-dark-secondary          /* oklch(80% 0.15 110) - bright lime */
--clr-dark-tertiary           /* oklch(70% 0.20 340) - electric magenta */
--clr-dark-success            /* oklch(75% 0.15 145) - mint green */
--clr-dark-warning            /* oklch(78% 0.18 85) - golden yellow */

--clr-dark-text-primary       /* oklch(95% 0.01 270) - nearly white */
--clr-dark-text-secondary     /* oklch(70% 0.02 270) - purple-gray */
--clr-dark-text-tertiary      /* oklch(55% 0.02 270) - subtle gray */
```

---

## Accessibility Features

All components include:

1. **Focus Indicators:**
   - 3px solid outline in primary color
   - 2px offset for clarity
   - Applied via `:focus-visible` (keyboard navigation only)

2. **Contrast Ratios:**
   - Body text: 7:1 minimum (AAA)
   - Large text: 4.5:1 minimum (AA)
   - Button text: 7:1 minimum (AAA)

3. **Reduced Motion:**
   - All animations respect `@prefers-reduced-motion: reduce`
   - Animations → 0.01ms duration when reduced motion preferred
   - Gradient mesh and floating shapes disabled

4. **Keyboard Navigation:**
   - All interactive elements focusable
   - Tab order follows logical flow
   - Skip links provided in base layout

5. **Semantic HTML:**
   - Proper heading hierarchy
   - ARIA labels on icons
   - Meaningful alt text on images

---

## Performance Considerations

### CSS Optimization

**Loaded via main.css:**
```css
/* Order matters for proper cascade */
1. tailwind.css        /* Base Tailwind */
2. theme-tokens.css    /* CSS custom properties */
3. modern-design.css   /* Modern design system */
4. cybersecurity-effects.css
5. enhancements.css
```

**File Size:**
- `modern-design.css`: ~45KB uncompressed (~7KB gzipped)
- Total CSS bundle: ~120KB uncompressed (~18KB gzipped)

### Animation Performance

**GPU-Accelerated:**
- All animations use `transform` and `opacity` only
- No layout thrashing (avoid width/height animations)
- `will-change` not used (modern browsers auto-optimize)

**Backdrop-Filter:**
- May impact performance on low-end devices
- Consider disabling for older browsers:
  ```css
  @supports not (backdrop-filter: blur(12px)) {
    .nav-frosted {
      background: var(--clr-light-bg-base); /* Solid fallback */
    }
  }
  ```

### Container Queries

**Browser Support:**
- Chrome 105+, Safari 16+, Firefox 110+
- Fallback: Cards use fixed 16px border-radius on unsupported browsers
- Progressive enhancement approach

---

## Migration from Old Components

### Replacing Existing Hero

**Old (src/index.njk):**
```njk
<section class="relative isolate overflow-hidden bg-gradient-to-br...">
  <!-- Old hero content -->
</section>
```

**New:**
```njk
{% include "components/hero-modern.njk" %}
```

### Replacing Existing Navigation

**Old (src/_includes/layouts/base.njk):**
```njk
<header role="banner" class="site-header sticky top-0 z-50">
  <!-- Old nav content -->
</header>
```

**New:**
```njk
{% include "components/nav-modern.njk" %}
```

### Updating Post Cards

**Old:**
```njk
<article class="group card holo-card p-8">
  <!-- Old card content -->
</article>
```

**New:**
```njk
{% set post = postObject %}
{% include "components/post-card-modern.njk" %}
```

---

## Testing Checklist

Before deploying, verify:

- [ ] Hero gradient mesh animates smoothly
- [ ] Floating shapes don't interfere with text readability
- [ ] Navigation frosted glass effect renders correctly
- [ ] Active nav indicator animates on hover/click
- [ ] Post cards image zoom works on hover
- [ ] Tag pills truncate properly (max 3 shown)
- [ ] Button hover states (scale + brightness)
- [ ] Button icon animations (translateX on hover)
- [ ] Focus indicators visible on all interactive elements
- [ ] Dark mode toggle transitions smoothly (400ms)
- [ ] Reduced motion disables animations correctly
- [ ] Mobile menu collapses/expands properly
- [ ] Typography scales responsively (clamp values)
- [ ] Contrast ratios meet AAA standard (7:1 body, 4.5:1 large)
- [ ] Noise texture subtle (3% opacity)
- [ ] Stagger animations delay correctly (50ms increments)

---

## Browser Support

**Minimum Required:**
- Chrome 111+ (OKLCH support)
- Safari 15.4+ (OKLCH support)
- Firefox 113+ (OKLCH support)

**Features with Fallbacks Needed:**
- Backdrop-filter (frosted glass) → Solid background
- Container queries → Fixed breakpoints
- Color-mix() → Pre-calculated colors

**Not Supported:**
- Internet Explorer (any version)
- Older mobile browsers (<2023)

---

## Troubleshooting

### Gradient Not Animating

**Issue:** Hero gradient mesh appears static.

**Solution:**
1. Check if `@media (prefers-reduced-motion: reduce)` is active
2. Verify animation is not disabled in browser settings
3. Confirm `.hero-gradient-mesh::before` has `animation: gradient-shift 15s ease-in-out infinite;`

### Frosted Glass Not Working

**Issue:** Navigation appears solid instead of frosted.

**Solution:**
1. Check browser supports `backdrop-filter` (Chrome 76+, Safari 9+, Firefox 103+)
2. Verify GPU acceleration enabled (some browsers disable on low-end hardware)
3. Add fallback: `.nav-frosted { background: var(--clr-light-bg-base); }`

### Colors Look Wrong

**Issue:** OKLCH colors not rendering correctly.

**Solution:**
1. Verify browser version supports OKLCH (Chrome 111+, Safari 15.4+, Firefox 113+)
2. Check color-gamut support: `@media (color-gamut: p3) { /* P3 colors */ }`
3. Add RGB fallbacks for older browsers

### Focus Indicators Missing

**Issue:** No outline when tabbing through elements.

**Solution:**
1. Check if `:focus-visible` supported (all modern browsers)
2. Verify `*:focus-visible` rule in modern-design.css
3. Test with keyboard navigation (Tab key), not mouse clicks

---

## Additional Resources

- **Architect Specifications:** `/redesign.md`
- **Implementation Summary:** `/IMPLEMENTATION_SUMMARY_CODER2.md`
- **Color System:** OKLCH - https://oklch.com/
- **Typography:** Modern font stack with system fallbacks
- **Accessibility:** WCAG 2.1 Level AAA - https://www.w3.org/WAI/WCAG21/quickref/

---

**Last Updated:** 2025-11-15
**Component Version:** 1.0.0
**Status:** Ready for integration
