# TODO: Website Improvements and Features

**Generated:** 2025-06-26  
**Priority:** Organized by impact and effort

---

## 🚀 High Priority (Quick Wins)

### 1. Replace Generic Welcome Post
- [ ] Replace `src/posts/welcome.md` with meaningful content
- [ ] Consider: "My Journey into Security Engineering" or "Building This Site with Eleventy"
- [ ] Remove placeholder feel, add personal touch

### 2. Add Web App Manifest
- [ ] Create `src/manifest.json` for PWA support
- [ ] Include app name, icons, theme colors
- [ ] Add to `.eleventy.js` passthrough copy
- [ ] Link in base template: `<link rel="manifest" href="/manifest.json">`

### 3. Implement Image Optimization
- [ ] Install `@11ty/eleventy-img` plugin
- [ ] Create image shortcode for automatic optimization
- [ ] Generate multiple sizes and formats (webp, avif)
- [ ] Update existing images to use new shortcode

### 4. Fix Style Guide Page
- [ ] Create `src/pages/style-guide.md` (referenced in docs but missing)
- [ ] Document color palette, typography, components
- [ ] Add to navigation if appropriate

---

## 📈 Medium Priority (Enhanced UX)

### 5. Create Tag/Category Pages
- [ ] Generate pages for each tag dynamically
- [ ] Template: `/tags/[tag-name]/` listing all posts with that tag
- [ ] Add tag cloud or list to sidebar/footer
- [ ] Update post template to link tags

### 6. Add Related Posts
- [ ] Implement "Related Posts" section at end of blog posts
- [ ] Use tags/categories for relevance
- [ ] Show 3-5 related posts
- [ ] Consider using similarity algorithm

### 7. Enhance Image Loading
- [ ] Add `loading="lazy"` to all images
- [ ] Implement blur-up placeholders
- [ ] Add aspect ratio containers to prevent layout shift

### 8. Add "Back to Top" Button
- [ ] Create floating button for long pages
- [ ] Show after scrolling down 50%
- [ ] Smooth scroll animation
- [ ] Accessible implementation

### 9. Enhance 404 Page Search
- [ ] Replace "Coming Soon" with working search
- [ ] Reuse existing search.js functionality
- [ ] Help users find what they're looking for

---

## 🔧 Low Priority (Nice to Have)

### 10. Progressive Web App Features
- [ ] Implement service worker for offline support
- [ ] Cache static assets and recent posts
- [ ] Show offline page when disconnected
- [ ] Add install prompt for mobile

### 11. Privacy & Analytics
- [ ] Create privacy policy page if adding analytics
- [ ] Consider privacy-focused analytics (Plausible, Fathom)
- [ ] Add `security.txt` file for security researchers

### 12. Enhanced Content Features
- [ ] Add reading progress indicator bar
- [ ] Implement print styles for articles
- [ ] Add newsletter signup (ConvertKit, Buttondown)
- [ ] Consider comment system (Giscus, Utterances)

### 13. Performance Optimizations
- [ ] Inline critical CSS
- [ ] Implement resource hints (preconnect, prefetch)
- [ ] Add Workbox for advanced caching strategies
- [ ] Optimize web fonts loading

### 14. Developer Experience
- [ ] Add linting scripts (ESLint, Stylelint)
- [ ] Create component library/showcase
- [ ] Add git hooks for code quality
- [ ] Implement automated testing

---

## 📋 Content Ideas

### Blog Post Topics (based on your expertise)
- [ ] "Setting Up a Home Security Lab with Raspberry Pi"
- [ ] "Automating Security Workflows with Python"
- [ ] "My Favorite Open Source Security Tools"
- [ ] "Building a Personal Knowledge Management System"
- [ ] "Lessons Learned from Security Incident Response"

### Page Additions
- [ ] /now - What you're currently focused on
- [ ] /speaking - Past and upcoming talks
- [ ] /projects/[project-name] - Detailed project pages

---

## 🎯 Implementation Notes

1. **Start with High Priority items** - They provide the most value for least effort
2. **Image optimization** will significantly improve performance
3. **PWA features** enhance mobile experience but aren't critical
4. **Content is king** - Focus on writing quality posts over adding features

---

## 📚 Standards to Reference

When implementing these improvements, refer to:
- **Performance:** `@load FE:performance + SEO:core-web-vitals`
- **PWA:** `@load FE:pwa + WD:mobile-first`
- **Accessibility:** `@load WD:accessibility + FE:accessibility`
- **SEO:** `@load SEO:technical + SEO:on-page`

---

*Remember: Don't let perfect be the enemy of good. Ship incrementally!*