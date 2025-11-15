---
title: Accessibility & Formatting Standards
category: standards
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1200
load_when:
  - Creating content
  - Reviewing accessibility
  - Image management
dependencies: []
tags: [accessibility, wcag, a11y, formatting, mobile]
---

# Accessibility & Formatting Standards

## Module Metadata
- **Category:** standards
- **Priority:** MEDIUM
- **Load frequency:** All content operations
- **Dependencies:** None

## Purpose
This module defines WCAG AA accessibility standards, mobile optimization requirements, formatting best practices, and testing procedures to ensure all content is accessible to diverse audiences including those using assistive technologies.

## When to Load This Module
- **Creating content** - Apply accessibility from start
- **Reviewing accessibility** - Validate compliance
- **Image management** - Alt text requirements

## Quick Reference

| Standard | Requirement | Target | Validation |
|----------|-------------|--------|------------|
| Alt Text | All images have descriptive alt text | 100% | Manual review |
| Touch Targets | All interactive elements ≥44px | 100% | Mobile testing |
| Heading Hierarchy | Proper H1 → H2 → H3 structure | 100% | Linting |
| Mobile Responsive | Tested 375px-2560px | 100% | Device testing |
| WCAG Level | AA compliance | AA | Lighthouse audit |
| Keyboard Navigation | All features accessible via keyboard | 100% | Manual testing |

**Quick Test:**
```bash
# Run Lighthouse accessibility audit
npx lighthouse https://williamzujkowski.github.io/posts/[slug]/ --only-categories=accessibility
```

---

## Required Practices

### Descriptive Alt Text

**For all visual elements:**
- Convey the image's purpose and content
- Be concise (125 characters or less when possible)
- Include context relating to surrounding content
- Avoid redundancy with caption text

**Examples:**
- ✅ Good: "Diagram showing Claude-Flow's hierarchical swarm topology with queen and worker agents"
- ❌ Bad: "Image" or "Diagram"

### Clear Heading Hierarchy

**Proper H1 → H2 → H3 structure:**
- One H1 per page (post title)
- H2 for major sections
- H3 for subsections
- Never skip levels (H1 → H3)

### Simple Language

**Make content accessible to diverse audiences:**
- Explain technical jargon on first use
- Use plain language when possible
- Define acronyms and abbreviations
- Provide context for complex concepts

### Assistive Technology Compatibility

**Ensure compatibility with:**
- Screen readers (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation
- Voice control software
- Screen magnifiers

### Mobile Optimization

**Test on various screen sizes:**
- Minimum: 375px (iPhone SE)
- Standard: 390px-430px (modern phones)
- Tablet: 768px-1024px
- Desktop: 1280px-2560px

---

## Formatting Standards

### Clear Headings and Subheadings

Use semantic HTML heading tags:
```html
<h1>Post Title</h1>
<h2>Major Section</h2>
<h3>Subsection</h3>
```

### Bullet Points for Lists

**Unordered lists for non-sequential items:**
```markdown
- First item
- Second item
- Third item
```

### Numbered Lists for Sequential Steps

**Ordered lists for procedures:**
```markdown
1. First step
2. Second step
3. Third step
```

### Code Blocks with Syntax Highlighting

**Always specify language:**
```markdown
```python
# Python code example
def hello_world():
    print("Hello, World!")
```
```

### White Space for Readability

- Short paragraphs (3-5 sentences maximum)
- Line breaks between sections
- Margins around code blocks
- Padding around images

---

## WCAG Compliance

### Level AA Requirements

**Achieved standards:**
- Contrast ratio ≥4.5:1 for normal text
- Contrast ratio ≥3:1 for large text
- Touch targets ≥44x44px
- Text resizable to 200% without loss of functionality
- Keyboard accessible (all features)
- Focus indicators visible

### Testing Tools

```bash
# Lighthouse accessibility audit
npx lighthouse https://williamzujkowski.github.io/ --only-categories=accessibility

# axe-core CLI testing
npx axe https://williamzujkowski.github.io/

# pa11y CLI testing
npx pa11y https://williamzujkowski.github.io/
```

---

## Mobile Responsiveness

### Touch Target Requirements

**All interactive elements:**
- Minimum size: 44x44px (iOS Human Interface Guidelines)
- Minimum spacing: 8px between targets
- Large enough for average finger (16x16mm)

**Common interactive elements:**
- Navigation links
- Buttons
- Form inputs
- Checkboxes and radio buttons
- Carousel controls

### Responsive Breakpoints

**CSS breakpoints used:**
```css
/* Mobile: 375px-639px */
/* Tablet: 640px-1023px */
/* Desktop: 1024px+ */
```

### Testing Procedure

**Test on real devices:**
1. iPhone SE (375px) - Minimum mobile
2. iPhone 14 (390px) - Standard mobile
3. iPad (768px) - Tablet
4. MacBook (1440px) - Desktop

**Test in browser DevTools:**
- Chrome DevTools device mode
- Firefox Responsive Design Mode
- Safari Web Inspector

---

## Dark Mode Support

### Requirements

**Fully functional dark mode:**
- Automatic detection via `prefers-color-scheme`
- Manual toggle in UI
- Color contrast maintained in both modes
- Image adjustments for dark backgrounds

### Color Schemes

**Light Mode:**
- Background: #ffffff
- Text: #1f2937
- Accent: #3b82f6

**Dark Mode:**
- Background: #0f172a
- Text: #f1f5f9
- Accent: #60a5fa

---

## Keyboard Navigation

### Requirements

**All features accessible via keyboard:**
- Tab to navigate between elements
- Shift+Tab to navigate backwards
- Enter/Space to activate buttons
- Arrow keys for carousels/menus
- Escape to close modals

### Focus Indicators

**Visible focus states:**
- Outline or background color change
- 2px solid focus ring
- High contrast with background
- Never remove focus indicators with `outline-solid: none` without replacement

---

## Reading Progress

### Implementation

**Features:**
- Progress bar at top of post
- Percentage indicator
- Smooth animation
- Mobile-friendly
- Accessible (ARIA labels)

---

## Code Copy Buttons

### Requirements

**All code blocks have copy buttons:**
- Visible on hover/focus
- Accessible via keyboard
- Confirmation feedback (✓ icon)
- Screen reader announcements
- Mobile-friendly touch targets

---

## Cross-References

### Related Modules
- [standards/image-standards](image-standards.md) - Alt text requirements
- [workflows/blog-writing](../workflows/blog-writing.md) - Content formatting

### External References
- **WCAG 2.1 AA:** [w3.org/WAI/WCAG21/quickref/](https://www.w3.org/WAI/WCAG21/quickref/)
- **iOS HIG:** [developer.apple.com/design/human-interface-guidelines/](https://developer.apple.com/design/human-interface-guidelines/)

---

## Examples

### Example 1: Accessible Image with Alt Text

```html
<img
  src="/assets/images/blog/hero/2025-11-01-k3s-homelab-hero.jpg"
  alt="K3s cluster running on three Raspberry Pi 4 devices with LED indicators showing node status"
  width="1200"
  height="630"
  loading="lazy"
/>
```

**Analysis:** Descriptive alt text, dimensions specified, lazy loading for performance.

### Example 2: Proper Heading Hierarchy

```html
<h1>Building a Homelab K3s Cluster</h1>

<h2>Hardware Requirements</h2>
<p>Content about hardware...</p>

<h3>Raspberry Pi Setup</h3>
<p>Content about Raspberry Pi...</p>

<h3>Network Configuration</h3>
<p>Content about networking...</p>

<h2>Software Installation</h2>
<p>Content about software...</p>
```

**Analysis:** One H1, logical H2 sections, H3 subsections, no level skipping.

---

## Common Pitfalls

### Pitfall 1: Missing Alt Text
**Problem:** Images without alt text fail screen readers
**Solution:** Add descriptive alt text to all images
**Prevention:** Run image metadata updater: `python scripts/blog-images/update-blog-images.py`

### Pitfall 2: Small Touch Targets
**Problem:** Interactive elements <44px difficult to tap on mobile
**Solution:** Add padding to reach 44x44px minimum
**Prevention:** Test on real mobile devices before publishing

### Pitfall 3: Broken Heading Hierarchy
**Problem:** Skipping from H1 to H3 confuses screen readers
**Solution:** Always progress sequentially (H1 → H2 → H3)
**Prevention:** Use linting tools to validate heading structure

---

## Validation

### Pre-Publication Checklist

- [ ] All images have descriptive alt text
- [ ] Heading hierarchy is proper (H1 → H2 → H3)
- [ ] Touch targets are ≥44x44px
- [ ] Content tested on mobile (375px minimum)
- [ ] Lighthouse accessibility score ≥90
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Focus indicators visible
- [ ] Dark mode functional
- [ ] Code blocks have copy buttons
- [ ] Reading progress indicator works

### Validation Commands

```bash
# Lighthouse accessibility audit
npx lighthouse https://williamzujkowski.github.io/posts/[slug]/ --only-categories=accessibility --view

# axe-core validation
npx axe https://williamzujkowski.github.io/posts/[slug]/

# pa11y validation
npx pa11y https://williamzujkowski.github.io/posts/[slug]/
```

### Expected Output

```
Lighthouse Accessibility Audit
==============================
Score: 95/100

Passed Audits:
✓ [aria-*] attributes are valid
✓ [role] values are valid
✓ Alt text present on images
✓ Heading hierarchy proper
✓ Touch targets adequate size
✓ Contrast ratios sufficient
✓ Keyboard navigation works

Warnings:
⚠ Minor contrast issue on footer link (4.3:1, recommend ≥4.5:1)
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md v3.0.0
- WCAG AA standards documented
- Mobile responsiveness requirements defined
- Touch target minimums established
- Keyboard navigation requirements included
- Testing procedures documented

---

## Maintenance Notes

**Review Schedule:** Semi-annually
**Last Review:** 2025-11-01
**Next Review:** 2026-05-01
**Maintainer:** Accessibility compliance agent

**Update Triggers:**
- WCAG standards updated
- New assistive technology considerations
- Device landscape changes (new screen sizes)
- User feedback on accessibility issues

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
