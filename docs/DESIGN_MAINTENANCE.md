# Design System Maintenance Guide

**Version:** 1.0.0
**Last Updated:** 2025-11-15
**Purpose:** Future updates and maintenance procedures

## Overview

This guide covers maintenance procedures for the OKLCH-based design system, including adding colors, updating components, managing dark mode, and troubleshooting common issues.

## Adding New Colors

### Step 1: Define OKLCH Values

**Choose perceptually uniform values:**
```css
/* theme-tokens.css */
:root {
  /* Light mode */
  --clr-light-custom: oklch(60% 0.15 200);  /* L C H */

  /* Dark mode */
  --clr-dark-custom: oklch(70% 0.18 200);
}
```

**OKLCH parameters:**
- **L (Lightness):** 0-100% (50% = medium gray)
- **C (Chroma):** 0-0.4 (0 = grayscale, 0.4 = vivid)
- **H (Hue):** 0-360 degrees (0 = red, 120 = green, 240 = blue)

### Step 2: Add to Design System

**Update modern-design.css:**
```css
:root {
  /* Light mode active by default */
  --color-custom: var(--clr-light-custom);
}

.dark {
  /* Dark mode override */
  --color-custom: var(--clr-dark-custom);
}
```

### Step 3: Validate Contrast

**Test against backgrounds:**
```javascript
// Use browser DevTools
// 1. Inspect element with new color
// 2. Click color swatch in Styles panel
// 3. Check contrast ratio (✓✓ = AAA, ✓ = AA)

// Requirements:
// - Body text: 7:1 (AAA)
// - Large text: 4.5:1 (AA)
// - Button text: 7:1 (AAA)
```

**Manual calculation:**
```bash
# Use contrast checker
node scripts/accessibility/check-contrast.js --fg "oklch(60% 0.15 200)" --bg "oklch(98% 0.01 80)"

# Output: 6.2:1 (AA, not AAA)
# Adjust lightness to meet AAA: oklch(45% 0.15 200) → 8.1:1 ✓
```

### Step 4: Document Usage

**Add to DESIGN_SYSTEM.md:**
```markdown
### Custom Color

**Purpose:** [Describe use case]

**Light mode:** `oklch(45% 0.15 200)` (deep sky blue)
**Dark mode:** `oklch(70% 0.18 200)` (bright sky blue)

**Contrast ratios:**
- On light base: 8.1:1 (AAA) ✓
- On dark base: 9.2:1 (AAA) ✓

**Usage:**
```css
.custom-element {
  color: var(--color-custom);
}
```
```

## Updating Typography

### Adding a New Font

**Step 1: Obtain font files (WOFF2 format):**
```bash
# Self-hosted fonts in /public/fonts
/public/fonts/
  NewFont-Regular.woff2
  NewFont-Bold.woff2
  NewFont-Italic.woff2
```

**Step 2: Define @font-face:**
```css
/* theme-tokens.css or modern-design.css */
@font-face {
  font-family: 'NewFont';
  src: url('/fonts/NewFont-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'NewFont';
  src: url('/fonts/NewFont-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

**Step 3: Add to font stack:**
```css
:root {
  --font-custom: "NewFont", system-ui, sans-serif;
}

.text-custom {
  font-family: var(--font-custom);
}
```

**Step 4: Preload critical fonts:**
```html
<!-- base.njk -->
<link rel="preload" href="/fonts/NewFont-Regular.woff2" as="font" type="font/woff2" crossorigin>
```

### Adjusting Type Scale

**Current ratio:** 1.25 (Major Third)

**To change to 1.333 (Perfect Fourth):**
```css
:root {
  /* Recalculate each step */
  --text-xs: clamp(0.875rem, 0.8vw + 0.7rem, 1rem);      /* 14px base */
  --text-sm: clamp(1.167rem, 0.9vw + 0.9rem, 1.333rem);  /* 14px × 1.333 */
  --text-base: clamp(1.556rem, 1vw + 1.2rem, 1.778rem);  /* 14px × 1.333² */
  --text-lg: clamp(2.074rem, 1.2vw + 1.5rem, 2.369rem);  /* 14px × 1.333³ */
  --text-xl: clamp(2.765rem, 1.4vw + 1.9rem, 3.157rem);  /* 14px × 1.333⁴ */
  --text-2xl: clamp(3.686rem, 1.6vw + 2.4rem, 4.209rem); /* 14px × 1.333⁵ */
  --text-3xl: clamp(4.915rem, 1.8vw + 3rem, 5.610rem);   /* 14px × 1.333⁶ */
  --text-4xl: clamp(6.553rem, 2vw + 3.8rem, 7.478rem);   /* 14px × 1.333⁷ */
}
```

**Ratio reference:**
- 1.125 (Major Second) - Subtle
- 1.200 (Minor Third) - Balanced
- 1.250 (Major Third) - **Current**
- 1.333 (Perfect Fourth) - Bold
- 1.414 (Augmented Fourth) - Dramatic
- 1.500 (Perfect Fifth) - Very dramatic

## Managing Dark Mode

### Toggle Implementation

**Current implementation:**
```javascript
// base.njk or theme-toggle.js
function toggleTheme() {
  const html = document.documentElement;
  html.classList.add('theme-transitioning');
  html.classList.toggle('dark');

  const isDark = html.classList.contains('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');

  setTimeout(() => {
    html.classList.remove('theme-transitioning');
  }, 400);
}

// Initialize on page load
(function() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const shouldBeDark = savedTheme === 'dark' || (!savedTheme && prefersDark);

  if (shouldBeDark) {
    document.documentElement.classList.add('dark');
  }
})();
```

### Adding Dark Mode to New Components

**Pattern:**
```css
.new-component {
  /* Light mode (default) */
  background: var(--clr-light-bg-surface);
  color: var(--clr-light-text-primary);
  border: 1px solid var(--clr-light-border-default);
}

.dark .new-component {
  /* Dark mode override */
  background: var(--clr-dark-bg-surface);
  color: var(--clr-dark-text-primary);
  border: 1px solid var(--clr-dark-border-default);
}
```

**Or use CSS custom properties:**
```css
:root {
  --component-bg: var(--clr-light-bg-surface);
  --component-text: var(--clr-light-text-primary);
}

.dark {
  --component-bg: var(--clr-dark-bg-surface);
  --component-text: var(--clr-dark-text-primary);
}

.new-component {
  background: var(--component-bg);
  color: var(--component-text);
}
```

### Smooth Transitions

**Global transitions:**
```css
html {
  transition: background-color 400ms ease, color 400ms ease;
}

* {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-duration: 400ms;
  transition-timing-function: ease;
}
```

**Disable during theme change:**
```css
html.theme-transitioning * {
  transition: none !important;
}
```

**Why:** Prevents jarring color flashes when toggling theme.

## Component Updates

### Modifying Existing Components

**Step 1: Locate component file:**
```bash
/src/_includes/components/
  hero-modern.njk
  nav-modern.njk
  post-card-modern.njk
  feature-card-modern.njk
```

**Step 2: Edit Nunjucks template:**
```njk
{# Example: Update hero heading text #}
<h1 class="text-display gradient-text-modern">
  {{ site.heroHeading | default("Your New Heading") }}
</h1>
```

**Step 3: Test changes:**
```bash
npm run dev
# Visit http://localhost:8080
# Verify component renders correctly
```

**Step 4: Update documentation:**
```markdown
<!-- MODERN_COMPONENTS_GUIDE.md -->
### Hero Section

**Customization:**
- Line 22: Main heading text (now uses site.heroHeading variable)
```

### Creating New Components

**Step 1: Create component file:**
```bash
# Follow naming convention: [component]-modern.njk
touch src/_includes/components/testimonial-modern.njk
```

**Step 2: Write Nunjucks template:**
```njk
{# testimonial-modern.njk #}
<blockquote class="modern-card testimonial">
  <div class="testimonial-content">
    <p class="text-body">{{ quote }}</p>
  </div>
  <footer class="testimonial-footer">
    <cite class="text-subheading">{{ author }}</cite>
    <span class="text-tertiary">{{ role }}</span>
  </footer>
</blockquote>
```

**Step 3: Add styles to modern-design.css:**
```css
/* Testimonial Component */
.testimonial {
  padding: var(--space-8);
  background: var(--clr-light-bg-elevated);
  border-left: 4px solid var(--clr-light-primary);
}

.dark .testimonial {
  background: var(--clr-dark-bg-elevated);
  border-left-color: var(--clr-dark-primary);
}

.testimonial-content {
  margin-bottom: var(--space-6);
  font-style: italic;
}

.testimonial-footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
```

**Step 4: Document usage:**
```markdown
<!-- MODERN_COMPONENTS_GUIDE.md -->
### Testimonial Card

**File:** `/src/_includes/components/testimonial-modern.njk`

**Usage:**
```njk
{% set quote = "This design system is fantastic!" %}
{% set author = "Jane Developer" %}
{% set role = "Senior Engineer" %}
{% include "components/testimonial-modern.njk" %}
```

**Features:**
- Left border accent (primary color)
- Italic quote text
- Author name and role
- Dark mode support
```
```

## Updating Spacing

### Global Spacing Changes

**Current scale:** 4px base unit

**To change base unit to 8px:**
```css
:root {
  --space-1: 0.5rem;    /* 8px */
  --space-2: 1rem;      /* 16px */
  --space-3: 1.5rem;    /* 24px */
  --space-4: 2rem;      /* 32px */
  --space-6: 3rem;      /* 48px */
  --space-8: 4rem;      /* 64px */
  --space-12: 6rem;     /* 96px */
  --space-16: 8rem;     /* 128px */
  --space-24: 12rem;    /* 192px */
  --space-32: 16rem;    /* 256px */
}
```

**Impact:** All components using spacing variables will scale proportionally.

### Component-Specific Spacing

**Pattern:**
```css
.custom-component {
  /* Don't hardcode values */
  padding: 24px;  /* ❌ */

  /* Use spacing variables */
  padding: var(--space-6);  /* ✅ 24px */
}
```

**Benefits:**
- Consistent spacing across all components
- Easy to adjust globally
- Maintains design system integrity

## Performance Optimization

### CSS Bundle Size

**Current bundle:**
- `modern-design.css`: 45KB uncompressed (7KB gzipped)
- `theme-tokens.css`: 15KB uncompressed (3KB gzipped)
- Total: ~60KB uncompressed (10KB gzipped)

**Optimization strategies:**

**1. Remove unused styles:**
```bash
# Use PurgeCSS (already configured in Tailwind)
npm run build

# Manual audit:
grep -r "class=\"unused-class\"" src/
# If not found, remove from modern-design.css
```

**2. Minify CSS:**
```bash
# Production build automatically minifies
npm run build

# Manual minification:
npx csso src/assets/css/modern-design.css -o dist/assets/css/modern-design.min.css
```

**3. Split critical CSS:**
```html
<!-- Inline critical above-the-fold styles -->
<style>
  :root { /* Essential tokens */ }
  .hero { /* Hero styles only */ }
</style>

<!-- Defer non-critical styles -->
<link rel="preload" href="/assets/css/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

### Animation Performance

**GPU-accelerated properties:**
```css
/* Good - GPU accelerated */
.element {
  transform: translateY(-4px);
  opacity: 0.9;
}

/* Avoid - CPU intensive */
.element {
  top: -4px;         /* Triggers layout */
  filter: blur(2px); /* Slow on mobile */
}
```

**Force GPU rendering:**
```css
.animated-element {
  will-change: transform, opacity;
  transform: translateZ(0);
}
```

**Remove will-change after animation:**
```javascript
element.addEventListener('animationend', () => {
  element.style.willChange = 'auto';
});
```

## Troubleshooting

### Colors Not Updating

**Symptoms:** New color variables not applying.

**Solutions:**
1. Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)
2. Verify CSS file imported in `main.css`
3. Check CSS custom property syntax: `var(--variable-name)`
4. Inspect element in DevTools → Computed styles

### Dark Mode Not Switching

**Symptoms:** Theme toggle doesn't change colors.

**Solutions:**
1. Check `.dark` class added to `<html>` element
2. Verify dark mode variables defined in CSS
3. Test localStorage: `localStorage.getItem('theme')`
4. Check transition class removed after 400ms

### Fonts Not Loading

**Symptoms:** System fonts used instead of custom fonts.

**Solutions:**
1. Verify font files exist in `/public/fonts`
2. Check @font-face `src` path is correct
3. Ensure WOFF2 format (best browser support)
4. Preload critical fonts in `<head>`
5. Check Network tab in DevTools (200 status for fonts)

### Focus Indicators Missing

**Symptoms:** No outline when tabbing through elements.

**Solutions:**
1. Check `:focus-visible` rule exists
2. Verify outline not set to `none`
3. Test with keyboard (Tab), not mouse
4. Inspect element in DevTools → Styles panel

### Animations Not Working

**Symptoms:** Gradient mesh static, no hover effects.

**Solutions:**
1. Check `@media (prefers-reduced-motion: reduce)` not active
2. Verify animation keyframes defined
3. Check element has `animation` property
4. Test in different browser (Safari vs Chrome)

## Version Control

### Git Workflow

**Creating a design update branch:**
```bash
# Create feature branch
git checkout -b design/update-color-palette

# Make changes
# - Edit theme-tokens.css
# - Update modern-design.css
# - Modify components as needed

# Stage changes
git add src/assets/css/theme-tokens.css
git add src/assets/css/modern-design.css

# Commit with descriptive message
git commit -m "feat(design): update primary color to burnt orange

- Adjust lightness for AAA contrast (55% → 52%)
- Update dark mode coral for consistency
- Verify all button text meets 7:1 contrast
- Test across light/dark modes"

# Push to remote
git push origin design/update-color-palette

# Create pull request
gh pr create --title "Update primary color palette" --body "..."
```

### Documenting Changes

**Update CHANGELOG.md:**
```markdown
## [1.1.0] - 2025-11-20

### Changed
- Updated primary color from oklch(55% 0.18 25) to oklch(52% 0.18 25) for better contrast
- Adjusted dark mode coral to oklch(73% 0.19 50) for consistency

### Fixed
- Button text on primary background now meets AAA contrast (7.2:1)

### Tested
- Light mode: 15.1:1 (AAA) ✓
- Dark mode: 14.8:1 (AAA) ✓
- All button combinations: 7.1:1+ (AAA) ✓
```

### Rollback Procedure

**If design update breaks site:**
```bash
# Option 1: Revert specific commit
git revert <commit-hash>
git push origin main

# Option 2: Reset to previous version
git reset --hard HEAD~1
git push origin main --force

# Option 3: Restore from backup
git checkout <previous-commit-hash> -- src/assets/css/
git commit -m "chore: restore previous design system"
git push origin main
```

## Testing Checklist

### Before Deploying Changes

**Visual regression:**
- [ ] Homepage renders correctly (light/dark modes)
- [ ] Blog post page layout intact
- [ ] Navigation frosted glass effect works
- [ ] Hero gradient mesh animates
- [ ] Card hover effects function
- [ ] Typography scales responsively (375px - 2560px)

**Accessibility:**
- [ ] Lighthouse score ≥95 (accessibility category)
- [ ] WAVE: Zero errors
- [ ] Contrast ratios meet AAA (7:1+ body text)
- [ ] Focus indicators visible on all interactive elements
- [ ] Keyboard navigation functional (Tab, Enter, Escape)
- [ ] Screen reader announces correctly (NVDA/VoiceOver)

**Performance:**
- [ ] Lighthouse score ≥90 (performance category)
- [ ] CSS bundle ≤15KB gzipped
- [ ] Fonts preloaded (check Network tab)
- [ ] No layout shifts (CLS <0.1)
- [ ] First Contentful Paint <2s

**Cross-browser:**
- [ ] Chrome 111+ (OKLCH support)
- [ ] Safari 15.4+ (OKLCH support)
- [ ] Firefox 113+ (OKLCH support)
- [ ] Mobile Safari (iOS 15.4+)
- [ ] Mobile Chrome (Android)

## Maintenance Schedule

**Monthly:**
- [ ] Audit contrast ratios (WAVE/axe DevTools)
- [ ] Check for broken styles (visual regression)
- [ ] Verify dark mode toggle works
- [ ] Test keyboard navigation
- [ ] Review CSS bundle size

**Quarterly:**
- [ ] Update font files if new versions available
- [ ] Review typography scale (still appropriate?)
- [ ] Audit unused CSS (PurgeCSS report)
- [ ] Check browser support (Can I Use)
- [ ] Update documentation (DESIGN_SYSTEM.md)

**Annually:**
- [ ] Full accessibility audit (WCAG 2.1 AAA)
- [ ] Performance audit (Lighthouse, WebPageTest)
- [ ] Cross-browser testing (latest versions)
- [ ] Review design trends (still modern?)
- [ ] Consider design system refresh

## References

**Internal docs:**
- DESIGN_SYSTEM.md - Complete color palette and component reference
- ACCESSIBILITY_GUIDE.md - WCAG compliance procedures
- MODERN_COMPONENTS_GUIDE.md - Component usage examples

**External resources:**
- OKLCH color picker: https://oklch.com/
- Contrast checker: https://webaim.org/resources/contrastchecker/
- Font display strategies: https://web.dev/font-display/
- CSS custom properties: https://developer.mozilla.org/en-US/docs/Web/CSS/--*

---

**Last updated:** 2025-11-15
**Maintained by:** William Zujkowski
**Next review:** 2025-12-15
