# Standards Quick Reference Guide

**Version:** 1.0.0  
**Last Updated:** 2024-01-24  
**Purpose:** Quick reference for applying standards to this Eleventy site

---

## 🚀 Getting Started with Standards

### Step 1: Understanding the Standards System

This project uses the comprehensive standards from the `.standards` submodule. The main entry point is:

**Standards Router:** [.standards/docs/core/CLAUDE.md](.standards/docs/core/CLAUDE.md)

### Step 2: Common Commands

```bash
# For AI assistants working on this site

# Site-specific navigation
@load CLAUDE.md                    # Load site documentation
@load content-management           # Learn about content structure

# Standards guidance
@load FE:*                        # Frontend standards
@load WD:*                        # Web design standards  
@load SEO:*                       # SEO standards
@load CONT:*                      # Content standards
@load GH:pages                    # GitHub Pages standards
```

---

## 📋 Task-Based Standards Loading

### Creating Content

```bash
# Writing a new blog post
@load CONT:writing + SEO:on-page + content-management

# Creating a new page
@load FE:architecture + WD:ux-patterns + templates

# Optimizing existing content
@load SEO:content + CONT:seo + performance-metrics
```

### Development Tasks

```bash
# Improving performance
@load FE:performance + SEO:core-web-vitals + WD:performance

# Enhancing accessibility
@load WD:accessibility + FE:accessibility + templates

# Setting up tooling
@load TOOL:javascript + GH:actions + CS:javascript
```

### Design & Styling

```bash
# Updating visual design
@load WD:visual-design + WD:typography + styling-architecture

# Implementing responsive design
@load FE:responsive + WD:responsive + CSS

# Adding dark mode
@load WD:theming + FE:theming + CSS
```

---

## 🎯 Priority Standards for Eleventy Sites

### Must-Have Standards

1. **Frontend Architecture** (`FE:architecture`)
   - Component organization
   - Performance optimization
   - Build configuration

2. **SEO Technical** (`SEO:technical`)
   - Meta tags
   - Sitemap
   - Structured data

3. **Content Structure** (`CONT:structure`)
   - Blog post format
   - Page organization
   - Content governance

4. **GitHub Pages** (`GH:pages`)
   - Deployment setup
   - Custom domain
   - CI/CD workflows

### Should-Have Standards

1. **Web Design** (`WD:visual-design`)
   - Typography system
   - Color architecture
   - Spacing guidelines

2. **Accessibility** (`WD:accessibility`)
   - WCAG compliance
   - Keyboard navigation
   - Screen reader support

3. **Performance** (`FE:performance`)
   - Core Web Vitals
   - Image optimization
   - Caching strategies

---

## 🔧 Implementation Examples

### Example 1: Optimizing Blog Post SEO

```bash
# Load relevant standards
@load SEO:on-page + CONT:seo + context:[eleventy-blog]

# Key implementations:
- Add structured data for articles
- Optimize meta descriptions (150-160 chars)
- Use proper heading hierarchy
- Internal linking strategy
```

### Example 2: Improving Site Performance

```bash
# Load performance standards
@load FE:performance + SEO:core-web-vitals + context:[static-site]

# Key implementations:
- Implement image lazy loading
- Minify CSS/HTML
- Add resource hints
- Optimize font loading
```

### Example 3: Enhancing Accessibility

```bash
# Load accessibility standards
@load WD:accessibility + FE:accessibility + context:[personal-website]

# Key implementations:
- Add ARIA labels
- Ensure color contrast ratios
- Test keyboard navigation
- Implement focus indicators
```

---

## 📚 Key Standards Files

### Primary Standards
- **Frontend:** `.standards/docs/standards/FRONTEND_MOBILE_STANDARDS.md`
- **Web Design:** `.standards/docs/standards/WEB_DESIGN_UX_STANDARDS.md`
- **SEO:** `.standards/docs/standards/SEO_WEB_MARKETING_STANDARDS.md`
- **Content:** `.standards/docs/standards/CONTENT_STANDARDS.md`
- **GitHub:** `.standards/docs/standards/GITHUB_PLATFORM_STANDARDS.md`

### Supporting Standards
- **Coding:** `.standards/docs/standards/CODING_STANDARDS.md`
- **Testing:** `.standards/docs/standards/TESTING_STANDARDS.md`
- **Security:** `.standards/docs/standards/SECURITY_STANDARDS.md`
- **Toolchain:** `.standards/docs/standards/TOOLCHAIN_STANDARDS.md`

---

## ✅ Validation Commands

```bash
# Validate KM standards implementation
npm run validate:km

# Check specific implementations
@validate against:[FE:architecture]
@validate against:[SEO:technical]
@validate against:[WD:accessibility]
```

---

## 🆘 Getting Help

1. **For comprehensive guidance:** Use the standards router at `.standards/docs/core/CLAUDE.md`
2. **For site-specific help:** Use `CLAUDE.md` in the root directory
3. **For implementation status:** Check `docs/STANDARDS_IMPLEMENTATION_CHECKLIST.md`

---

**Remember:** The standards are comprehensive guides. Focus on implementing the sections most relevant to your current task. Use progressive enhancement to add more standards compliance over time.