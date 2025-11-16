# Implementation Architecture for Website Redesign

**Status:** Draft - Architect Deliverable
**Version:** 1.0.0
**Date:** 2025-11-15
**Agent:** Architect (Hive Mind Swarm)

## Overview

This document provides the complete implementation architecture for transforming williamzujkowski.github.io into a modern, visually stunning website using OKLCH color space, advanced CSS features, and premium design patterns.

---

## 1. CSS Architecture

### 1.1 File Structure

```
src/assets/css/
├── main.css                  # Import orchestrator (existing)
├── tailwind.css              # Tailwind base (existing)
├── theme-tokens.css          # Design tokens - MAJOR REFACTOR
├── cybersecurity-effects.css # Visual effects - PRESERVE
├── enhancements.css          # Component styles - MAJOR REFACTOR
└── animations.css            # NEW - Animation system
```

### 1.2 Design Token Architecture (theme-tokens.css)

**Strategy:** Complete OKLCH migration with color-mix() support

```css
/* ========================================
   OKLCH COLOR SYSTEM - DARK MODE
   ======================================== */
:root.dark {
  /* Background Layers - Midnight Espresso */
  --oklch-bg-base: 15% 0.02 270;        /* Deep purple-black */
  --oklch-bg-surface: 20% 0.03 270;     /* Elevated cards */
  --oklch-bg-elevated: 25% 0.03 265;    /* Interactive elements */

  /* Accent Colors */
  --oklch-primary: 75% 0.19 50;         /* Warm coral/peach */
  --oklch-secondary: 80% 0.15 110;      /* Bright lime green */
  --oklch-tertiary: 70% 0.20 340;       /* Electric magenta */
  --oklch-success: 75% 0.15 145;        /* Mint green */
  --oklch-warning: 78% 0.18 85;         /* Golden yellow */

  /* Text Hierarchy */
  --oklch-text-primary: 95% 0.01 270;   /* Nearly white with purple hint */
  --oklch-text-secondary: 70% 0.02 270; /* Muted purple-gray */
  --oklch-text-tertiary: 55% 0.02 270;  /* Subtle gray */

  /* Button Text (AAA Contrast) */
  --oklch-btn-on-primary: 15% 0.01 50;  /* Very dark warm */
  --oklch-btn-on-secondary: 15% 0.01 110; /* Very dark cool */
  --oklch-btn-on-tertiary: 98% 0.01 340;  /* Nearly white */

  /* Convert to CSS color values */
  --color-bg-base: oklch(var(--oklch-bg-base));
  --color-bg-surface: oklch(var(--oklch-bg-surface));
  --color-bg-elevated: oklch(var(--oklch-bg-elevated));

  --color-primary: oklch(var(--oklch-primary));
  --color-secondary: oklch(var(--oklch-secondary));
  --color-tertiary: oklch(var(--oklch-tertiary));
  --color-success: oklch(var(--oklch-success));
  --color-warning: oklch(var(--oklch-warning));

  --color-text-primary: oklch(var(--oklch-text-primary));
  --color-text-secondary: oklch(var(--oklch-text-secondary));
  --color-text-tertiary: oklch(var(--oklch-text-tertiary));

  --color-btn-on-primary: oklch(var(--oklch-btn-on-primary));
  --color-btn-on-secondary: oklch(var(--oklch-btn-on-secondary));
  --color-btn-on-tertiary: oklch(var(--oklch-btn-on-tertiary));
}

/* ========================================
   OKLCH COLOR SYSTEM - LIGHT MODE
   ======================================== */
:root {
  /* Background Layers - Warm Canvas */
  --oklch-bg-base: 98% 0.01 80;         /* Warm off-white */
  --oklch-bg-surface: 95% 0.02 85;      /* Subtle cream */
  --oklch-bg-elevated: 100% 0 0;        /* Pure white */

  /* Accent Colors */
  --oklch-primary: 55% 0.18 25;         /* Burnt orange/terracotta */
  --oklch-secondary: 45% 0.15 160;      /* Deep teal */
  --oklch-tertiary: 50% 0.20 320;       /* Deep rose */
  --oklch-success: 50% 0.14 155;        /* Forest green */
  --oklch-warning: 55% 0.17 65;         /* Amber */

  /* Text Hierarchy */
  --oklch-text-primary: 25% 0.02 270;   /* Rich charcoal */
  --oklch-text-secondary: 45% 0.02 270; /* Medium gray */
  --oklch-text-tertiary: 60% 0.01 270;  /* Light gray */

  /* Button Text (AAA Contrast) */
  --oklch-btn-on-primary: 98% 0.01 25;  /* Warm white */
  --oklch-btn-on-secondary: 98% 0.01 160; /* Cool white */
  --oklch-btn-on-tertiary: 98% 0.01 320;  /* Pink-white */

  /* Convert to CSS color values */
  --color-bg-base: oklch(var(--oklch-bg-base));
  --color-bg-surface: oklch(var(--oklch-bg-surface));
  --color-bg-elevated: oklch(var(--oklch-bg-elevated));

  --color-primary: oklch(var(--oklch-primary));
  --color-secondary: oklch(var(--oklch-secondary));
  --color-tertiary: oklch(var(--oklch-tertiary));
  --color-success: oklch(var(--oklch-success));
  --color-warning: oklch(var(--oklch-warning));

  --color-text-primary: oklch(var(--oklch-text-primary));
  --color-text-secondary: oklch(var(--oklch-text-secondary));
  --color-text-tertiary: oklch(var(--oklch-text-tertiary));

  --color-btn-on-primary: oklch(var(--oklch-btn-on-primary));
  --color-btn-on-secondary: oklch(var(--oklch-btn-on-secondary));
  --color-btn-on-tertiary: oklch(var(--oklch-btn-on-tertiary));
}

/* ========================================
   COLOR-MIX UTILITIES
   ======================================== */
:root {
  /* Hover states using color-mix() */
  --color-primary-hover: color-mix(in oklch, var(--color-primary), white 10%);
  --color-secondary-hover: color-mix(in oklch, var(--color-secondary), white 10%);
  --color-tertiary-hover: color-mix(in oklch, var(--color-tertiary), white 10%);

  /* Active states */
  --color-primary-active: color-mix(in oklch, var(--color-primary), black 15%);
  --color-secondary-active: color-mix(in oklch, var(--color-secondary), black 15%);
  --color-tertiary-active: color-mix(in oklch, var(--color-tertiary), black 15%);

  /* Surface tints (subtle color overlays) */
  --surface-primary-tint: color-mix(in oklch, var(--color-bg-surface), var(--color-primary) 5%);
  --surface-secondary-tint: color-mix(in oklch, var(--color-bg-surface), var(--color-secondary) 5%);
}
```

### 1.3 Typography System

**Fonts:** Cabinet Grotesk, Geist, GeistMono, Fraunces (loaded via Google Fonts)

```css
/* Typography Scale - 1.25 ratio */
:root {
  --font-display: 'Cabinet Grotesk', -apple-system, sans-serif;
  --font-heading: 'Satoshi', 'General Sans', sans-serif;
  --font-body: 'Geist', 'DM Sans', sans-serif;
  --font-mono: 'GeistMono', 'Berkeley Mono', monospace;
  --font-feature: 'Fraunces', Georgia, serif;

  /* Type scale - 1.25 ratio from 14px base */
  --text-xs: 0.875rem;   /* 14px */
  --text-sm: 1.125rem;   /* 18px */
  --text-base: 1.375rem; /* 22px */
  --text-lg: 1.75rem;    /* 28px */
  --text-xl: 2.1875rem;  /* 35px */
  --text-2xl: 2.75rem;   /* 44px */
  --text-3xl: 3.4375rem; /* 55px */
  --text-4xl: 4.3125rem; /* 69px */

  /* Line heights */
  --leading-tight: 1.2;
  --leading-normal: 1.5;
  --leading-relaxed: 1.7;
  --leading-loose: 2.0;

  /* Font weights */
  --weight-normal: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
  --weight-extrabold: 800;
  --weight-black: 900;
}

/* Typography applications */
.text-display {
  font-family: var(--font-display);
  font-weight: var(--weight-black);
  font-size: var(--text-4xl);
  line-height: var(--leading-tight);
  letter-spacing: -0.02em;
}

.text-heading {
  font-family: var(--font-heading);
  font-weight: var(--weight-bold);
  line-height: var(--leading-normal);
}

.text-body {
  font-family: var(--font-body);
  font-weight: var(--weight-normal);
  line-height: var(--leading-relaxed);
}

.text-feature {
  font-family: var(--font-feature);
  font-weight: var(--weight-semibold);
  font-variation-settings: 'wght' 600;
}
```

### 1.4 Spacing System

**Base unit:** 4px, modular scale

```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
  --space-24: 6rem;    /* 96px */
  --space-32: 8rem;    /* 128px */

  /* Semantic spacing */
  --section-padding-mobile: var(--space-12);  /* 48px */
  --section-padding-desktop: var(--space-24); /* 96px */
  --content-max-width: 1200px;
  --reading-width: 720px;
}
```

---

## 2. Component Architecture

### 2.1 Hero Section

**Design:** Animated gradient mesh background with floating geometric shapes

```css
/* Hero Component */
.hero {
  position: relative;
  min-height: 80vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  padding-block: var(--section-padding-desktop);
}

/* Animated gradient mesh background */
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 30%, var(--color-primary) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, var(--color-secondary) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, var(--color-tertiary) 0%, transparent 50%);
  background-size: 400% 400%;
  animation: gradientMesh 15s ease infinite;
  opacity: 0.15;
  filter: blur(60px);
}

@keyframes gradientMesh {
  0%, 100% { background-position: 0% 50%, 100% 50%, 50% 0%; }
  50% { background-position: 100% 50%, 0% 50%, 50% 100%; }
}

/* Floating geometric shapes */
.hero-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.hero-shape {
  position: absolute;
  background: var(--color-primary);
  opacity: 0.1;
  border-radius: 50%;
  filter: blur(20px);
  animation: float 20s ease-in-out infinite;
}

.hero-shape:nth-child(1) {
  width: 300px;
  height: 300px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.hero-shape:nth-child(2) {
  width: 200px;
  height: 200px;
  top: 60%;
  right: 15%;
  background: var(--color-secondary);
  animation-delay: 5s;
}

.hero-shape:nth-child(3) {
  width: 250px;
  height: 250px;
  bottom: 10%;
  left: 50%;
  background: var(--color-tertiary);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(30px, -30px) rotate(120deg); }
  66% { transform: translate(-30px, 30px) rotate(240deg); }
}

/* Hero headshot with parallax */
.hero-headshot {
  position: relative;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.hero-headshot:hover {
  transform: scale(1.05);
}

/* Typography treatments */
.hero-title {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: var(--weight-black);
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.03em;
  margin-bottom: var(--space-6);
}
```

### 2.2 Navigation Component

**Design:** Frosted glass effect with gradient border

```css
/* Navigation - Frosted glass */
.site-header {
  position: sticky;
  top: 0;
  backdrop-filter: blur(12px) saturate(180%);
  background: color-mix(in oklch, var(--color-bg-base), transparent 20%);
  border-bottom: 1px solid;
  border-image: linear-gradient(90deg,
    var(--color-primary) 0%,
    var(--color-secondary) 50%,
    var(--color-tertiary) 100%
  ) 1;
  z-index: 1000;
  transition: all 0.3s ease;
}

/* Nav links */
.nav-link {
  position: relative;
  padding: var(--space-2) var(--space-4);
  font-family: var(--font-heading);
  font-weight: var(--weight-semibold);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link:hover {
  color: var(--color-text-primary);
}

/* Active indicator - slide-in underline */
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: var(--color-primary);
  border-radius: 2px;
  transform: translateX(-50%);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}
```

### 2.3 Card Components

**Design:** Multi-layer shadows with gradient borders and hover effects

```css
/* Card base */
.card {
  background: var(--color-bg-surface);
  border-radius: 16px;
  border: 1px solid;
  border-image: linear-gradient(180deg,
    color-mix(in oklch, var(--color-primary), transparent 70%),
    transparent
  ) 1;
  box-shadow:
    0 4px 24px color-mix(in oklch, var(--color-bg-base), black 12%);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

/* Hover effect - lift and glow */
.card:hover {
  transform: translateY(-8px);
  box-shadow:
    0 8px 32px color-mix(in oklch, var(--color-bg-base), black 15%),
    0 0 40px color-mix(in oklch, var(--color-primary), transparent 70%);
}

/* Post card specific */
.post-card-image {
  aspect-ratio: 16 / 9;
  overflow: hidden;
  border-radius: 16px 16px 0 0;
}

.post-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover .post-card-image img {
  transform: scale(1.1);
}

/* Tag pills */
.tag-pill {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: color-mix(in oklch, var(--color-primary), transparent 85%);
  color: var(--color-primary);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.tag-pill:hover {
  background: color-mix(in oklch, var(--color-primary), transparent 70%);
  transform: scale(1.05);
}
```

### 2.4 Button Components

**Design:** Gradient backgrounds with scale and brightness transitions

```css
/* Primary button */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-8);
  font-family: var(--font-heading);
  font-weight: var(--weight-bold);
  font-size: var(--text-sm);
  letter-spacing: 0.025em;
  color: var(--color-btn-on-primary);
  background: linear-gradient(135deg,
    var(--color-primary),
    color-mix(in oklch, var(--color-primary), var(--color-secondary) 30%)
  );
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px color-mix(in oklch, var(--color-primary), transparent 60%);
}

.btn-primary:hover {
  transform: scale(1.02);
  filter: brightness(1.1);
  box-shadow: 0 6px 20px color-mix(in oklch, var(--color-primary), transparent 40%);
}

.btn-primary:active {
  transform: scale(0.98);
}

/* Icon animations */
.btn-primary svg {
  transition: transform 0.3s ease;
}

.btn-primary:hover svg {
  transform: translateX(4px);
}
```

---

## 3. Animation System

### 3.1 Core Animations

**File:** `src/assets/css/animations.css`

```css
/* ========================================
   SCROLL ANIMATIONS
   ======================================== */

/* Fade in on scroll */
.animate-on-scroll {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger animation for lists */
.stagger-item {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.stagger-item:nth-child(1) { transition-delay: 0ms; }
.stagger-item:nth-child(2) { transition-delay: 50ms; }
.stagger-item:nth-child(3) { transition-delay: 100ms; }
.stagger-item:nth-child(4) { transition-delay: 150ms; }
.stagger-item:nth-child(5) { transition-delay: 200ms; }
/* Continue pattern up to 20 items */

.stagger-item.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ========================================
   PAGE TRANSITIONS
   ======================================== */

.page-transition {
  animation: fadeSlideIn 0.6s ease-out;
}

@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========================================
   DARK MODE TRANSITION
   ======================================== */

html {
  transition: background-color 400ms ease, color 400ms ease;
}

* {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-duration: 400ms;
  transition-timing-function: ease;
}

/* Disable transitions during theme change for better performance */
html.theme-transitioning * {
  transition: none !important;
}

/* ========================================
   REDUCED MOTION SUPPORT
   ======================================== */

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .hero::before,
  .hero-shape {
    animation: none !important;
  }

  .animate-on-scroll,
  .stagger-item {
    opacity: 1 !important;
    transform: none !important;
  }
}
```

### 3.2 Interaction Observers

**File:** `src/assets/js/scroll-animations.js`

```javascript
// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Unobserve after animation to improve performance
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe all animated elements
document.querySelectorAll('.animate-on-scroll, .stagger-item').forEach(el => {
  observer.observe(el);
});

// Parallax effect for hero headshot
const heroHeadshot = document.querySelector('.hero-headshot');
if (heroHeadshot) {
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const rate = scrolled * 0.3;
    heroHeadshot.style.transform = `translateY(${rate}px)`;
  }, { passive: true });
}
```

---

## 4. Dark Mode Toggle

### 4.1 Toggle Component

```html
<!-- Dark mode toggle button -->
<button
  type="button"
  onclick="toggleTheme()"
  class="theme-toggle"
  aria-label="Toggle theme"
>
  <svg class="sun-icon" viewBox="0 0 24 24"><!-- Sun SVG --></svg>
  <svg class="moon-icon" viewBox="0 0 24 24"><!-- Moon SVG --></svg>
</button>
```

```css
.theme-toggle {
  position: relative;
  width: 44px;
  height: 44px;
  padding: var(--space-2);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-default);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px color-mix(in oklch, var(--color-primary), transparent 70%);
}

.sun-icon,
.moon-icon {
  width: 100%;
  height: 100%;
  transition: all 0.4s ease;
}

.dark .sun-icon {
  opacity: 0;
  transform: rotate(180deg) scale(0);
}

.dark .moon-icon {
  opacity: 1;
  transform: rotate(0deg) scale(1);
}

:not(.dark) .moon-icon {
  opacity: 0;
  transform: rotate(-180deg) scale(0);
}

:not(.dark) .sun-icon {
  opacity: 1;
  transform: rotate(0deg) scale(1);
}
```

### 4.2 Toggle Logic

```javascript
function toggleTheme() {
  const html = document.documentElement;

  // Add transitioning class to prevent jarring color changes
  html.classList.add('theme-transitioning');

  // Toggle dark class
  html.classList.toggle('dark');

  // Save preference
  const isDark = html.classList.contains('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');

  // Update meta theme-color
  const themeColorMeta = document.querySelector('meta[name="theme-color"]');
  if (themeColorMeta) {
    themeColorMeta.content = isDark
      ? getComputedStyle(html).getPropertyValue('--color-bg-base').trim()
      : getComputedStyle(html).getPropertyValue('--color-bg-base').trim();
  }

  // Remove transitioning class after animation completes
  setTimeout(() => {
    html.classList.remove('theme-transitioning');
  }, 400);
}

// Initialize theme on page load
(function() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const shouldBeDark = savedTheme === 'dark' || (!savedTheme && prefersDark);

  if (shouldBeDark) {
    document.documentElement.classList.add('dark');
  }
})();
```

---

## 5. Accessibility Implementation

### 5.1 WCAG AAA Compliance

**Color Contrast:**
- Body text: 7:1 minimum (AAA)
- Large text: 4.5:1 minimum (AA)
- Button text on backgrounds: Validated against OKLCH values
- All interactive elements: Verified programmatically

**Contrast Validation Script:**

```javascript
// Color contrast validator for OKLCH
function validateContrast(foreground, background) {
  // Convert OKLCH to RGB for WCAG calculation
  const fgRGB = oklchToRgb(foreground);
  const bgRGB = oklchToRgb(background);

  const ratio = getContrastRatio(fgRGB, bgRGB);

  return {
    ratio,
    passAAA: ratio >= 7,
    passAA: ratio >= 4.5,
    passAALarge: ratio >= 3
  };
}

function getContrastRatio(rgb1, rgb2) {
  const l1 = getRelativeLuminance(rgb1);
  const l2 = getRelativeLuminance(rgb2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

function getRelativeLuminance({ r, g, b }) {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}
```

### 5.2 Focus Indicators

```css
/* Focus ring for all interactive elements */
:focus-visible {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Remove default outline */
:focus:not(:focus-visible) {
  outline: none;
}

/* Custom focus states for specific components */
.btn-primary:focus-visible {
  outline-color: var(--color-secondary);
  outline-width: 3px;
  outline-offset: 3px;
}

.nav-link:focus-visible {
  outline-offset: 4px;
}
```

### 5.3 Keyboard Navigation

```javascript
// Enhanced keyboard navigation
document.addEventListener('keydown', (e) => {
  // Tab key - show focus indicators
  if (e.key === 'Tab') {
    document.body.classList.add('keyboard-nav');
  }

  // Escape key - close modals/menus
  if (e.key === 'Escape') {
    closeAllModals();
  }
});

// Hide focus indicators on mouse click
document.addEventListener('mousedown', () => {
  document.body.classList.remove('keyboard-nav');
});

// Skip to main content
const skipLink = document.querySelector('.skip-to-main');
if (skipLink) {
  skipLink.addEventListener('click', (e) => {
    e.preventDefault();
    const main = document.querySelector('#main');
    main.focus();
    main.scrollIntoView({ behavior: 'smooth' });
  });
}
```

### 5.4 Screen Reader Optimizations

```css
/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  padding: var(--space-2);
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

---

## 6. Advanced CSS Features

### 6.1 Logical Properties (i18n Support)

```css
/* Use logical properties for internationalization */
.card {
  margin-block: var(--space-6);
  margin-inline: var(--space-4);
  padding-block: var(--space-8);
  padding-inline: var(--space-6);
  border-inline-start: 3px solid var(--color-primary);
}

.hero-title {
  margin-block-end: var(--space-6);
  text-align: start;
}

.nav-list {
  gap: var(--space-4);
  padding-inline-start: 0;
}
```

### 6.2 Container Queries

```css
/* Container query for card adaptation */
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: var(--space-4);
  }

  .post-card-image {
    border-radius: 16px 0 0 16px;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 300px 1fr;
  }
}
```

### 6.3 Subgrid for Complex Layouts

```css
/* Grid system with subgrid */
.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-6);
}

.post-card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 4;
}

.post-card-image { grid-row: 1; }
.post-card-tags { grid-row: 2; }
.post-card-title { grid-row: 3; }
.post-card-meta { grid-row: 4; }
```

---

## 7. Performance Optimizations

### 7.1 CSS Loading Strategy

```html
<!-- Critical CSS inline in <head> -->
<style>
  /* Critical above-the-fold styles */
  :root { /* Essential color tokens */ }
  .hero { /* Hero layout only */ }
</style>

<!-- Deferred non-critical CSS -->
<link rel="preload" href="/assets/css/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/assets/css/main.css"></noscript>
```

### 7.2 Animation Performance

```css
/* Use transform and opacity for animations (GPU-accelerated) */
.card {
  will-change: transform, opacity;
  transform: translateZ(0); /* Force GPU rendering */
}

/* Avoid animating expensive properties */
.card:hover {
  transform: translateY(-8px); /* ✅ Good - GPU */
  /* filter: brightness(1.1); ❌ Avoid - CPU intensive */
}
```

### 7.3 Font Loading Strategy

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/CabinetGrotesk-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/Geist-Regular.woff2" as="font" type="font/woff2" crossorigin>

<!-- Font display swap for performance -->
<style>
  @font-face {
    font-family: 'Cabinet Grotesk';
    src: url('/fonts/CabinetGrotesk-Bold.woff2') format('woff2');
    font-weight: 700-900;
    font-display: swap;
  }
</style>
```

---

## 8. Implementation Checklist

### Phase 1: Foundation (Coder 1)
- [ ] Migrate theme-tokens.css to OKLCH color system
- [ ] Update color variables in both dark and light modes
- [ ] Implement color-mix() utilities
- [ ] Add typography system with new font families
- [ ] Create spacing system

### Phase 2: Components (Coder 2)
- [ ] Build hero section with gradient mesh
- [ ] Create navigation with frosted glass effect
- [ ] Design card components with multi-layer shadows
- [ ] Implement button components with gradients
- [ ] Add tag pills and micro-interactions

### Phase 3: Animations (Coder 1)
- [ ] Create animations.css file
- [ ] Implement scroll animations
- [ ] Add stagger effects for lists
- [ ] Build page transitions
- [ ] Create dark mode toggle animation
- [ ] Write JavaScript for intersection observers

### Phase 4: Accessibility (Coder 2)
- [ ] Validate all color contrasts (WCAG AAA)
- [ ] Implement focus indicators
- [ ] Add keyboard navigation support
- [ ] Create screen reader optimizations
- [ ] Test reduced motion preferences

### Phase 5: Testing & Refinement
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsiveness (375px - 2560px)
- [ ] Accessibility audit (WAVE, axe DevTools)
- [ ] Performance testing (Lighthouse, WebPageTest)
- [ ] Color-blind palette testing

---

## 9. Dependencies & Resources

### Required Fonts
- Cabinet Grotesk (700-900) - Google Fonts or self-hosted
- Satoshi (600-700) - Self-hosted
- Geist (400-500) - Vercel CDN or self-hosted
- GeistMono (400-500) - Vercel CDN or self-hosted
- Fraunces (variable, 600-700) - Google Fonts

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Polyfills (if needed)
- OKLCH color space: None required (native support in modern browsers)
- Container queries: None required (native support in modern browsers)
- color-mix(): None required (native support in modern browsers)

---

## 10. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     VISUAL LAYER                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Hero     │  │ Navigation │  │   Cards    │            │
│  │  Section   │  │  Component │  │ Components │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│                   ANIMATION LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Scroll   │  │   Hover    │  │    Page    │            │
│  │ Animations │  │   Effects  │  │ Transitions│            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│                   DESIGN TOKENS                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   OKLCH    │  │ Typography │  │  Spacing   │            │
│  │   Colors   │  │   System   │  │   System   │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│                    CSS FOUNDATION                           │
│         Tailwind + Custom Properties + Utilities            │
└─────────────────────────────────────────────────────────────┘
```

---

**End of Architecture Document**

This architecture provides the complete blueprint for implementation. Coders should reference specific sections as needed and coordinate via shared memory for any clarifications.
