---
title: Blog Post Creation Template
category: templates
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 500
load_when:
  - Creating new blog posts
  - Needing post structure guidance
dependencies:
  - workflows/blog-writing
  - standards/humanization-standards
tags: [template, blog, post, creation]
---

# Blog Post Creation Template

## Module Metadata
- **Category:** templates
- **Priority:** LOW
- **Load frequency:** When creating new blog posts
- **Dependencies:** workflows/blog-writing, standards/humanization-standards

## Purpose

This module provides a complete template for creating new blog posts that meet all quality standards (humanization, citations, structure, metadata).

## When to Load This Module

- Creating new blog posts
- Needing structural guidance
- Ensuring all required elements are present

---

## Frontmatter Template

```yaml
---
title: "[50-60 character title with primary keywords]"
date: YYYY-MM-DD
description: "[150-160 character summary for SEO and social sharing]"
tags: [tag1, tag2, tag3, tag4, tag5]
author: "William Zujkowski"
images:
  hero:
    src: "/assets/images/blog/hero/YYYY-MM-DD-slug-hero.jpg"
    alt: "[Descriptive alt text for hero image]"
    caption: "[Optional caption for context]"
    width: 1200
    height: 630
  og:
    src: "/assets/images/blog/hero/YYYY-MM-DD-slug-og.jpg"
    alt: "[Open Graph image description]"
---
```

---

## Content Structure Template

```markdown
# [Title - H1 - Same as frontmatter title]

**BLUF (Bottom Line Up Front):**

[2-3 sentences: What this post covers and why it matters NOW]
[Include surprising fact or specific metric to hook readers]
[Quantify the impact or benefit immediately]

**Why it matters:** [One sentence with specific, quantified benefit or impact]

---

## [Section 1 Title - Problem/Context]

[Opening paragraph establishing the problem or context]

**Key points:**
- [Bullet point with specific metric or example]
- [Bullet point demonstrating personal experience: "I tested..."]
- [Bullet point with concrete measurement: "73% improvement"]
- [Bullet point with uncertainty marker: "This probably depends on..."]

[Brief prose paragraph with first-person narrative and trade-off]

**Example from my homelab:**
```[language]
# Essential 5-10 line code snippet
# With comments explaining key concepts
```

**Why it matters:** [Connect back to reader's benefit]

---

## [Section 2 Title - Solution/Approach]

[Personal narrative: "I tried 3 approaches..."]

### Approach 1: [Name]

**What I tested:**
- [Concrete measurements: "22.1GB VRAM", "147ms latency"]
- [Time investment: "Took 17 minutes to compile"]
- [Iteration count: "After 4 failed attempts"]

**Trade-offs:**
- **Pros:** [Specific benefits with measurements]
- **Cons:** [Honest limitations and costs]

**When to use:** [Context-dependent recommendation]

[Failure narrative: "The first fix made it worse..."]

### Approach 2: [Name]

[Repeat pattern for each approach tested]

---

## [Section 3 Title - Results/Lessons]

**What worked:**
- [Bullet with specific outcome]
- [Bullet with personal reflection]
- [Bullet with concrete metric]

**What didn't work:**
- [Honest failure story]
- [Lesson learned]
- [Trade-off acknowledged]

[Closing reflection paragraph with uncertainty marker]

---

## Key Takeaways

[3-5 actionable takeaways as bullets]
- [Takeaway 1 with specific metric]
- [Takeaway 2 with context]
- [Takeaway 3 with trade-off]

---

## Further Reading

### Official Documentation
- [Link Title](URL) - Brief description of resource

### Academic Research
- **[Paper Title](DOI or arXiv link)** (Year)
  - Author names
  - *Journal/Conference Name*
  - [Brief summary of relevant findings]

### Related Posts
- [Post Title](URL) - How it relates to this post

### Tools & Resources
- [Tool Name](URL) - What it does and why it's useful

---

## References

1. **[Citation Title](Hyperlink URL)** (Year)
   - Author/organization
   - *Publication/source*
   - [Brief context for citation]

2. **[Citation Title](Hyperlink URL)** (Year)
   - [Continue pattern...]

[Minimum 10 citations, all with working hyperlinks]
[Prioritize: arXiv, NIST, official docs, IEEE, ACM]
[Include DOI/arXiv links when available]
```

---

## Pre-Publication Checklist

**Content Requirements:**
- [ ] 1,400+ words (6-9 min read)
- [ ] BLUF with quantified impact
- [ ] 8+ first-person statements ("I tested", "I discovered")
- [ ] 6+ uncertainty phrases ("probably", "in my case", "YMMV")
- [ ] 15+ concrete measurements (numbers, percentages, time investments)
- [ ] 10+ trade-off discussions (pros/cons, context-dependent)
- [ ] 5+ failure narratives (honest mistakes and debugging stories)

**Citations:**
- [ ] 10+ citations with working hyperlinks
- [ ] All technical claims sourced
- [ ] Academic sources prioritized (arXiv, IEEE, ACM)
- [ ] DOI/arXiv links when available
- [ ] Inline citations + comprehensive References section

**Images:**
- [ ] Hero image present (1200x630px)
- [ ] Section images where appropriate
- [ ] Descriptive alt text on all images
- [ ] Proper attribution for external images

**Code & Technical:**
- [ ] Code ratio <25% of content
- [ ] Code examples tested and working
- [ ] Comments explain key concepts
- [ ] Link to GitHub gist for full implementations
- [ ] Mermaid diagrams for architecture

**Structure:**
- [ ] Clear heading hierarchy (H1 → H2 → H3)
- [ ] 60+ bullets for scannability
- [ ] 2-3 sentence prose transitions between sections
- [ ] "Why it matters" sections present
- [ ] Key takeaways section at end

**Validation:**
- [ ] Humanization score ≥75/100 (run validator)
- [ ] Zero AI tells (em dashes, semicolons, "in conclusion")
- [ ] NDA compliance (no work references)
- [ ] Build passes (`npm run build`)
- [ ] Links validated (no broken links)
- [ ] Mobile preview tested (375px screens)

---

## Automation Commands

```bash
# Update image metadata
python scripts/blog-images/update-blog-images.py

# Generate hero images
python scripts/blog-images/generate-blog-hero-images.py

# Optimize images
bash scripts/optimize-blog-images.sh

# Validate citations
python scripts/blog-research/research-validator.py --post src/posts/[file].md

# Check citation hyperlinks
python scripts/blog-research/check-citation-hyperlinks.py

# Validate humanization (MANDATORY before commit)
python scripts/blog-content/humanization-validator.py --post src/posts/[file].md

# Run build
npm run build
```

---

## Quick Reference: Required Elements

| Element | Minimum | Target |
|---------|---------|--------|
| Word count | 1,400 | 1,800 |
| Citations | 10 | 12+ |
| First-person | 8 | 10+ |
| Uncertainty | 6 | 8+ |
| Measurements | 15 | 20+ |
| Trade-offs | 10 | 15+ |
| Bullets | 60 | 80+ |
| Failure stories | 5 | 7+ |
| Humanization score | 75/100 | 90/100 |

---

## Common Mistakes to Avoid

❌ **Don't:**
- Start with "In this post, I will..."
- Use vague claims without sources
- Embed verbose code blocks (>30 lines)
- Omit trade-offs and limitations
- Write in perfect parallel structures (AI tell)
- Use em dashes or semicolons
- Include work references or NDA violations

✅ **Do:**
- Lead with BLUF (bottom line up front)
- Source every technical claim
- Link to gists for full code examples
- Acknowledge costs and context-dependencies
- Vary sentence rhythm and structure
- Use commas and periods
- Focus on homelab and personal projects

---

## Cross-References

**Related modules:**
- `workflows/blog-writing` - Complete blog post workflow
- `standards/humanization-standards` - Validation requirements
- `standards/citation-research` - Citation guidelines
- `standards/image-standards` - Image requirements

**Tools:**
- `scripts/blog-content/humanization-validator.py` - Humanization validation
- `scripts/blog-research/research-validator.py` - Citation validation
- `scripts/blog-images/update-blog-images.py` - Image automation

---

## Changelog
- 2025-11-01: Initial template creation based on proven patterns
