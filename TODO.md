# TODO: Website Improvements and Features

**Generated:** 2025-06-26  
**Last Updated:** 2025-06-26  
**Priority:** Organized by impact and effort

---

## ✅ Completed (Done!)

### High Priority Items
- [x] **Replace Generic Welcome Post** - Created "Building My Digital Garden with Eleventy" post
- [x] **Add Web App Manifest** - PWA support with manifest.json and SVG icons
- [x] **Fix Style Guide Page** - Already exists at `/style-guide/`
- [x] **Add lazy loading** - Already implemented via `lazyImages` filter

### Medium Priority Items  
- [x] **Add "Back to Top" Button** - Implemented with smooth scrolling and accessibility
- [x] **Fix 404 Page Search** - Added functional search to help users find content

### Low Priority Items
- [x] **Dynamic theme-color meta tags** - Changes based on dark/light mode

---

## 🚀 High Priority (Quick Wins)

### 1. Implement Image Optimization
- [ ] Install `@11ty/eleventy-img` plugin
- [ ] Create image shortcode for automatic optimization
- [ ] Generate multiple sizes and formats (webp, avif)
- [ ] Update existing images to use new shortcode
- **Impact:** Major performance improvement, better Core Web Vitals

### 2. Create Tag/Category Pages
- [ ] Generate pages for each tag dynamically  
- [ ] Template: `/tags/[tag-name]/` listing all posts with that tag
- [ ] Add tag list to sidebar or footer
- [ ] Update post template to link tags
- **Impact:** Better content discovery, improved SEO

---

## 📈 Medium Priority (Enhanced UX)

### 3. Add Related Posts
- [ ] Implement "Related Posts" section at end of blog posts
- [ ] Use tags/categories for relevance
- [ ] Show 3-5 related posts
- [ ] Consider using similarity algorithm
- **Impact:** Increased engagement, lower bounce rate

### 4. Add Reading Progress Indicator
- [ ] Thin progress bar at top of viewport for blog posts
- [ ] Shows reading progress through article
- [ ] Smooth animation, respects reduced motion
- **Impact:** Better user experience for long-form content

### 5. Implement Resource Hints
- [ ] Add preconnect for external domains (fonts, etc.)
- [ ] Add dns-prefetch for common resources
- [ ] Consider prefetch for likely next pages
- **Impact:** Faster page loads, better perceived performance

---

## 🔧 Low Priority (Nice to Have)

### 6. Progressive Web App Features
- [ ] Implement service worker for offline support
- [ ] Cache static assets and recent posts
- [ ] Show offline page when disconnected
- [ ] Add install prompt for mobile

### 7. Privacy & Analytics
- [ ] Create privacy policy page if adding analytics
- [ ] Consider privacy-focused analytics (Plausible, Fathom)
- [ ] Add `security.txt` file for security researchers

### 8. Enhanced Content Features
- [ ] Implement print styles for articles
- [ ] Add newsletter signup (ConvertKit, Buttondown)
- [ ] Consider comment system (Giscus, Utterances)
- [ ] Create RSS categories for different content types

### 9. Performance Optimizations
- [ ] Inline critical CSS
- [ ] Add Workbox for advanced caching strategies
- [ ] Optimize web fonts loading
- [ ] Implement image blur-up placeholders

### 10. Developer Experience
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
- [ ] "Local LLM Deployment: Privacy-First AI"
- [ ] "Ansible Playbooks for Security Automation"

### Page Additions
- [ ] `/now` - What you're currently focused on
- [ ] `/speaking` - Past and upcoming talks  
- [ ] `/projects/[project-name]` - Detailed project case studies
- [ ] `/security-tools` - Curated security tool recommendations

---

## 🎯 Implementation Notes

### Next Steps (Recommended Order):
1. **Image Optimization** - Biggest performance win remaining
2. **Tag Pages** - Improves navigation and SEO significantly  
3. **Related Posts** - Keeps visitors engaged longer
4. **Reading Progress** - Nice UX enhancement for blog posts

### Time Estimates:
- Image Optimization: 2-3 hours
- Tag Pages: 1-2 hours
- Related Posts: 1 hour
- Reading Progress: 30 minutes

---

## 📚 Standards to Reference

When implementing these improvements, refer to:
- **Performance:** `@load FE:performance + SEO:core-web-vitals`
- **PWA:** `@load FE:pwa + WD:mobile-first`
- **Accessibility:** `@load WD:accessibility + FE:accessibility`
- **SEO:** `@load SEO:technical + SEO:on-page`
- **Image Optimization:** `@load FE:images + SEO:images`

---

## 📊 Progress Tracking

**Completed:** 7 items ✅  
**Remaining High Priority:** 2 items  
**Remaining Medium Priority:** 3 items  
**Remaining Low Priority:** 5 items  

**Overall Progress:** ~35% of identified improvements completed

---

*Remember: Don't let perfect be the enemy of good. Ship incrementally!*