Transform https://williamzujkowski.github.io into a visually stunning, modern website that exemplifies exceptional design. Use OKLCH color space for perceptually uniform, accessible colors.

TYPOGRAPHY SYSTEM:
- Display/Headings: "Cabinet Grotesk" or "Satoshi" (700-900 weight) - modern, geometric
- Subheadings: "General Sans" or "Plus Jakarta Sans" (600-700 weight)
- Body: "Geist" or "DM Sans" (400-500 weight) with generous line-height (1.7)
- Monospace: "GeistMono" or "Berkeley Mono" for code
- Feature text: "Fraunces" (variable font, 600-700) for emphasized quotes
- Scale: 1.25 ratio (14px, 18px, 22px, 28px, 35px, 44px, 55px, 69px)

DARK MODE - "Midnight Espresso":
Background layers:
- Base: oklch(15% 0.02 270) - deep purple-black
- Surface: oklch(20% 0.03 270) - elevated cards
- Elevated: oklch(25% 0.03 265) - interactive elements

Accent colors:
- Primary (CTA/links): oklch(75% 0.19 50) - warm coral/peach
- Secondary: oklch(80% 0.15 110) - bright lime green  
- Tertiary: oklch(70% 0.20 340) - electric magenta
- Success: oklch(75% 0.15 145) - mint green
- Warning: oklch(78% 0.18 85) - golden yellow

Text:
- Primary: oklch(95% 0.01 270) - nearly white with purple hint
- Secondary: oklch(70% 0.02 270) - muted purple-gray
- Tertiary: oklch(55% 0.02 270) - subtle gray

Button text (ensure AAA contrast):
- On primary: oklch(15% 0.01 50) - very dark warm
- On secondary: oklch(15% 0.01 110) - very dark cool
- On tertiary: oklch(98% 0.01 340) - nearly white

LIGHT MODE - "Warm Canvas":
Background layers:
- Base: oklch(98% 0.01 80) - warm off-white
- Surface: oklch(95% 0.02 85) - subtle cream
- Elevated: oklch(100% 0 0) - pure white

Accent colors:
- Primary: oklch(55% 0.18 25) - burnt orange/terracotta
- Secondary: oklch(45% 0.15 160) - deep teal
- Tertiary: oklch(50% 0.20 320) - deep rose
- Success: oklch(50% 0.14 155) - forest green
- Warning: oklch(55% 0.17 65) - amber

Text:
- Primary: oklch(25% 0.02 270) - rich charcoal
- Secondary: oklch(45% 0.02 270) - medium gray
- Tertiary: oklch(60% 0.01 270) - light gray

Button text (ensure AAA contrast):
- On primary: oklch(98% 0.01 25) - warm white
- On secondary: oklch(98% 0.01 160) - cool white
- On tertiary: oklch(98% 0.01 320) - pink-white

MODERN DESIGN ELEMENTS:

Hero Section:
- Animated gradient mesh background (3-4 OKLCH colors blending)
- Large, bold typography with slight letter-spacing
- Subtle parallax scroll effect on headshot
- Floating geometric shapes with blur backdrop

Navigation:
- Frosted glass effect (backdrop-filter: blur(12px))
- Border with subtle gradient
- Active state: bold underline with primary color
- Smooth slide-in indicator on hover

Cards/Content Blocks:
- Rounded corners (16px-24px)
- Multi-layer shadows for depth:
  - Dark: 0 4px 24px oklch(15% 0.02 270 / 0.12)
  - Light: 0 4px 24px oklch(25% 0.02 270 / 0.08)
- Hover: Lift effect + glow with accent color
- Border: 1px gradient (top-to-bottom, subtle)

Buttons:
- Primary: Gradient background (2 shades of primary)
- Large padding (16px 32px), rounded (12px)
- Hover: Scale 1.02 + brightness increase
- Text: Bold (600-700 weight), letter-spacing: 0.025em
- Icon animations on hover
- Ensure 7:1 contrast ratio minimum

Typography Treatments:
- Gradient text for main heading (primary to secondary)
- Text shadow for depth on dark mode
- Emphasis words: Different color + weight
- Quote blocks: Oversized quotation marks, accent border-left

Post Cards:
- Image: Rounded top, aspect ratio 16:9
- Tag pills: Small, rounded, with accent backgrounds
- Date: Monospace font with tertiary color
- Hover: Image subtle zoom, card lift, accent color glow

Interactive States:
- Focus rings: 3px solid accent color with 2px offset
- Transitions: 200ms cubic-bezier(0.4, 0, 0.2, 1)
- Active states: Scale 0.98, brightness shift
- Loading states: Skeleton screens with shimmer

Backgrounds & Textures:
- Subtle noise texture (opacity 2-3%)
- Animated gradient orbs (blurred circles)
- Geometric patterns in hero/footer sections
- Radial gradients from accent colors (very subtle)

Spacing System:
- Base: 4px
- Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128
- Section padding: 96px (desktop), 48px (mobile)
- Content max-width: 1200px, reading width: 720px

ADVANCED FEATURES:
- Smooth scroll behavior
- Intersection observers for scroll animations
- Stagger animation for list items (50ms delay each)
- Page transitions (fade + slight slide)
- Dark mode toggle: Smooth color transitions (400ms)
- Reduced motion support (@prefers-reduced-motion)

CSS ARCHITECTURE:
- Custom properties for all colors in OKLCH
- Color-mix() for hover states and variants
- Logical properties (inline, block) for i18n
- Container queries for component adaptation
- Subgrid for complex layouts

ACCESSIBILITY:
- WCAG AAA for body text (7:1 contrast)
- WCAG AA for large text (4.5:1 contrast)
- Focus indicators on all interactive elements
- Keyboard navigation with visible focus states
- Screen reader optimizations (sr-only class)
- Color-blind friendly palette testing

INSPIRATION THEMES:
- Linear.app aesthetic (clean, modern, bold typography)
- Stripe.com (sophisticated gradients, precise spacing)
- Rauno.me (playful interactions, attention to detail)
- Vercel.com (minimalist, high-contrast, fast)
- Arc browser landing page (vibrant, gradient-heavy)

Create a design that feels premium, intentional, and memorable. Every element should have purpose and polish. The site should make visitors say "wow, this is beautifully designed."