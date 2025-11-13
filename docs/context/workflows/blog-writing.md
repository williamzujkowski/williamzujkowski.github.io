---
title: Blog Writing Workflow
category: workflows
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 3500
load_when:
  - Creating new blog post
  - Editing existing post
  - Content review
dependencies:
  - core/nda-compliance
  - standards/humanization-standards
  - standards/citation-research
tags: [blog, writing, content, workflow]
---

# Blog Writing Workflow

## Module Metadata

**Category:** workflows
**Priority:** MEDIUM
**Load When:** Creating new blog posts, editing existing content, content review
**Dependencies:** core/nda-compliance, standards/humanization-standards, standards/citation-research
**Estimated Size:** ~3,500 tokens

---

## Purpose

This module provides the complete workflow for creating new blog posts from scratch, including recommended approaches, minimum standards, target audience definition, and pre-publication checklists.

---

## When to Load This Module

**Load this module when:**
- Creating new blog posts (AFTER blog-topic-summary.md)
- Need complete post workflow guidance
- Defining target audience for content
- Planning content structure
- Preparing for publication

**Skip this module if:**
- Haven't selected topic yet (load blog-topic-summary.md FIRST)
- Refining existing posts (use blog-transformation.md)
- Only validating content (use humanization-standards.md)

**IMPORTANT:** This module assumes you've already:
1. Loaded `blog-topic-summary.md` (or full blog-topic-selection.md)
2. Scored your topic (≥15/25)
3. Verified it fills a content gap or introduces new format
4. Passed NDA compliance check

If you haven't done these, **STOP** and load `blog-topic-summary.md` first.

---

## Quick Reference

**Recommended Workflow:**
1. Use Content Template (`docs/TEMPLATES/blog-post-writing-template.md`) for 80-90/100 baseline
2. Check topic diversity (different from last 5 posts)
3. Write 1,400-2,100 words (6-9 min read)
4. Ensure 90%+ citations with working hyperlinks
5. Add hero image + 1 per major section
6. Validate humanization score ≥75/100

---

## Recommended Workflow

**For NEW blog posts**, use the **Content Template** at `docs/TEMPLATES/blog-post-writing-template.md` to achieve 80-90/100 baseline scores on first draft. This proactive humanization approach is **50% faster** than reactive refinement.

**Template Validation Results:**
- Test post scored **90/100** (vs 50/100 unguided)
- All required patterns present: 8 first-person, 6 uncertainty, 22 trade-offs
- Time to baseline: 2.5 hours (vs 4-6 hours reactive)
- Full results: `docs/reports/phase-1-template-validation-report.md`

---

## Before You Write

**Check topic diversity:**
```bash
# List last 10 post topics
ls -t src/posts/*.md | head -10 | xargs grep "^tags:"
```

**Rules:**
- Different primary topic than last 5 posts
- No duplicate keywords in title
- Check overrepresented topics

**Why it matters:** Readers get bored. Variety keeps them coming back.

---

## Minimum Standards

- **Length:** 1,400-2,100 words (6-9 min read)
- **Citations:** 90%+ of claims sourced
- **Images:** Hero + 1 per major section
- **Code:** <25% of content

**Instant rejection criteria:**
- <1,400 words
- Made-up statistics
- No sources for technical claims
- Work/NDA violations

---

## Target Audience

### Primary & Secondary Audiences

- **Primary**: Technology enthusiasts with varying levels of expertise
- **Secondary**: Beginners seeking to understand complex technical concepts
- **Approach**: Begin with concise summaries to help beginners grasp key points, then dive deeper for advanced readers

### Focus Areas

Choose topics from these core domains:
- Artificial Intelligence and Machine Learning
- Quantum Computing
- Cybersecurity and Information Security
- Cryptography
- Robotics and Automation
- High-Performance Computing
- Science Fiction (technology implications)
- Homelab and Self-Hosted Solutions

### Diversity Requirements

- **Primary topic/category** must differ from the main topics of at least the **last 5 blog posts**
- **Analyze the most recent 10 posts** in `/src/posts/` to identify overrepresented topics
- **Prioritize topics** that haven't been the primary focus of any blog post in the last 2 months
- **Avoid repeating primary keywords** from recent post titles (check last 10 posts)

### Topic Research Strategy

To ensure content is cutting-edge and relevant:

1. **Explore Recent Research**: Search arXiv for papers uploaded within the last 30 days that align with blog focus areas
2. **Identify Breakthrough Papers**: Look for papers with:
   - High citation potential
   - Novel methodologies
   - Breakthrough findings
   - Emerging trends or paradigm shifts
   - Unexpected connections between fields
3. **Bridge Multiple Disciplines**: Papers that connect different domains often present unique storytelling opportunities
4. **Build on Existing Literature**: Select topics that introduce new concepts or applications while building on established knowledge

### Topic Objective Definition

Clearly define the post's objective:
- **Educational**: Teaching readers a new concept
- **Tutorial**: Providing step-by-step guidance
- **Insight**: Offering perspectives on recent developments
- **Analysis**: Examining trade-offs and implications
- **Experience Report**: Sharing lessons from personal projects

---

## Structure (5 Parts)

1. **Hook** (50 words): Grab attention with one strong sentence
2. **Context** (100 words): Why this matters now
3. **Main Content** (1,000-1,500 words): The substance
4. **Reflection** (150 words): What I learned
5. **Call to Action** (50 words): What readers should do

---

## Writing Rules

**Lead with the point:**
```markdown
❌ "While exploring various approaches to container orchestration..."
✅ "K3s cut my RAM usage by 75%. Here's how."
```

**Use bullets for lists:**
```markdown
✅ Three ways this failed:
   - OOM kills on 2GB nodes
   - etcd corruption after power loss
   - DNS resolution lag >5s
```

**One idea per paragraph:**
```markdown
✅ K3s uses SQLite instead of etcd. This matters for edge deployments.

   SQLite needs no quorum. Your cluster survives network partitions.
```

---

## Content Requirements

**Every post must include:**
- Opening hook (compelling story, question, or fact)
- Context setting (why this topic matters now)
- Core technical content with sources
- Personal experience (homelab experiments or research)
- Practical examples (code samples, diagrams, images)
- Security considerations (when relevant, CVSS 9.5+)
- Trade-offs and limitations (balanced analysis)
- Personal reflection (what this means to you)
- Conclusion (summarize main points)
- Call to action (encourage readers to apply knowledge)

**Content quality:**
- Analogies and real-world examples
- Balanced perspective (discuss trade-offs)
- Simple language with jargon explanations
- Conversational tone (see [writing-style.md](../standards/writing-style.md) for complete voice guidelines)
- Clear headings, bullet points, numbered lists

**Humanization requirements:** For detailed edge case handling (career/NDA-sensitive posts, technical deep-dives, tutorials, security posts), see [humanization-standards.md](../standards/humanization-standards.md#edge-cases).

**Code integration:**
- Store samples in appropriate folders
- Include direct links in post
- Use syntax highlighting
- Add comments for clarity
- Keep examples concise (5-10 lines)

---

## Metadata and SEO

### Title Requirements

- **Uniqueness**: Search all existing posts in `/src/posts/` to ensure no duplicate or similar titles
- **Keyword Optimization**: Include primary and secondary keywords for SEO
- **Length**: Between 6-12 words
- **Engagement**: Descriptive and compelling
- **Keyword Diversity**: Avoid reusing primary keywords from last 10 post titles

### Required Metadata

- Publication date (YYYY-MM-DD format)
- Last updated date (if applicable)
- Description/summary (150-160 characters)
- Tags (4-8 relevant tags)
- Author information
- Image metadata (see Blog Image Standards section)

---

## Images

**Required:**
- Hero image (1200x630px)
- One image per major section
- All images have descriptive alt text

**Scripts:**
```bash
# Auto-generate hero images
python scripts/blog-images/generate-blog-hero-images.py

# Optimize all images
bash scripts/optimize-blog-images.sh
```

**Sources (copyright-free):**
- [Unsplash](https://unsplash.com/)
- [Pexels](https://www.pexels.com/)
- [Pixabay](https://pixabay.com/)
- [Wikimedia Commons](https://commons.wikimedia.org/)
- [NASA Image Gallery](https://www.nasa.gov/multimedia/imagegallery/)

**For each image:**
- Direct URL to specific image
- Proper attribution if required
- Descriptive alt text for accessibility
- Complete Markdown formatting
- Appropriate search terms

---

## Citations

**Every technical claim needs:**
- Primary source (paper, documentation)
- Working hyperlink
- Publication date

**Format:**
```markdown
[Kubernetes uses 2GB RAM minimum](https://kubernetes.io/docs/setup/) (2024)

**Research citation:**
"K3s reduces memory footprint by 50%" ([Rancher Labs, 2023](https://rancher.com/k3s-whitepaper))
```

**Why it matters:** No citations = no credibility.

**For complete citation standards, research platforms, and validation workflows:**
See [citation-research.md](../standards/citation-research.md)

**Further Exploration Section:**

At the end of each post, include:
- Links to related articles
- Official documentation
- Tutorials and guides
- Relevant public repositories
- Projects readers may find interesting

---

## Accessibility and Formatting

### Required Practices

- **Descriptive Alt Text**: For all visual elements
- **Clear Heading Hierarchy**: Proper H1 → H2 → H3 structure
- **Simple Language**: Make content accessible to diverse audiences
- **Assistive Technology**: Ensure compatibility with screen readers and other assistive tools
- **Mobile Optimization**: Test on various screen sizes (375px-2560px)

### Formatting Standards

- Clear headings and subheadings
- Bullet points for lists
- Numbered lists for sequential steps
- Code blocks with syntax highlighting
- White space for readability
- Short paragraphs (3-5 sentences)

---

## Pre-Publication Checklist

**Before submitting:**

- [ ] Topic diversity (different from last 5 posts)
- [ ] Title is unique
- [ ] 1,400+ words (6-9 min read)
- [ ] All claims have citations with working hyperlinks
- [ ] 3+ reputable sources per major point
- [ ] Hero image + section images
- [ ] Descriptive alt text on all images
- [ ] Code examples tested
- [ ] Links verified (no broken links)
- [ ] Mobile preview checked
- [ ] Accessibility requirements met
- [ ] NDA compliance (no work references)
- [ ] Personal experience included
- [ ] Call to action present
- [ ] Further reading section populated
- [ ] Metadata complete
- [ ] Trade-offs and limitations discussed
- [ ] Tone validation completed (Phase G)
- [ ] No AI tells (em dashes, "in conclusion," "leverage")
- [ ] Sentence rhythm varies (short/medium/long)
- [ ] At least one hesitation or reflection included
- [ ] Personal voice preserved in stories
- [ ] Concrete details added (timestamps, numbers)
- [ ] Grammar and spelling checked

---

## Cross-References

### Related Modules
- [nda-compliance.md](../core/nda-compliance.md) - Content boundaries and privacy
- [humanization-standards.md](../standards/humanization-standards.md) - Voice and tone validation
- [citation-research.md](../standards/citation-research.md) - Research verification protocols

### External References
- [docs/TEMPLATES/blog-post-writing-template.md](../../TEMPLATES/blog-post-writing-template.md) - Starter template
- [docs/guides/UNIFIED_HUMANIZATION_METHODOLOGY.md](../../guides/UNIFIED_HUMANIZATION_METHODOLOGY.md) - 7-phase methodology

---

## Examples

### Example 1: Topic Diversity Check

```bash
# Check last 10 post topics
ls -t src/posts/*.md | head -10 | xargs grep "^tags:"

# Output shows:
# tags: [AI, homelab, GPU]
# tags: [security, containers, docker]
# tags: [kubernetes, k3s, edge]
# ...

# NEW POST should avoid these primary topics
```

**Explanation:** Ensures variety and prevents topic fatigue.

### Example 2: Complete Blog Post Workflow

```bash
# 1. Use template for 90/100 baseline
cp docs/TEMPLATES/blog-post-writing-template.md src/posts/2025-11-01-new-post.md

# 2. Check topic diversity
ls -t src/posts/*.md | head -10 | xargs grep "^tags:"

# 3. Write content (1,400-2,100 words)

# 4. Generate hero image
python scripts/blog-images/generate-blog-hero-images.py

# 5. Validate humanization
python scripts/blog-content/humanization-validator.py --post src/posts/2025-11-01-new-post.md

# 6. Validate citations
python scripts/blog-research/check-citation-hyperlinks.py

# 7. Commit if ≥75/100 score
git add src/posts/2025-11-01-new-post.md
git commit -m "feat: add new blog post"
```

**Explanation:** End-to-end workflow from template to publication.

---

## Common Pitfalls

### Pitfall 1: Ignoring Topic Diversity
**Problem:** Writing 3 posts in a row about same topic
**Solution:** Check last 10 post tags before choosing topic
**Prevention:** Keep running list of varied topic ideas

### Pitfall 2: Missing Citations
**Problem:** Technical claims without reputable sources
**Solution:** Add citations as you write, not after
**Prevention:** Use research workflow early in writing process

### Pitfall 3: Skipping Template
**Problem:** First draft scores 50/100, requires 4-6 hours of refinement
**Solution:** Use blog-post-writing-template.md for 90/100 baseline
**Prevention:** ALWAYS start with template for new posts

---

## Validation

### How to Verify Compliance

**Checklist:**
- [ ] Topic different from last 5 posts
- [ ] 1,400-2,100 words
- [ ] 90%+ claims have working hyperlinks
- [ ] Hero image + section images present
- [ ] Humanization score ≥75/100
- [ ] All accessibility requirements met

**For complete validation workflow** (commands, expected output, score interpretation), see [humanization-standards.md](../standards/humanization-standards.md#validation).

**Quick validation:**
```bash
# Check word count
wc -w src/posts/[file].md

# Build test
npm run build
```

---

## Changelog

### Version 1.1.0 (2025-11-01)
- **Phase 2A Consolidation:** Replaced duplicate validation commands with cross-reference to humanization-standards.md
- Added cross-reference to writing-style.md for complete voice guidelines
- Added cross-reference to humanization-standards.md for edge case handling
- Token savings: ~300 tokens (3500 → 3200)

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md section "Blog Post Creation Guidelines"
- Complete workflow with all standards
- Pre-publication checklist integrated
- Examples and validation added

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Content Quality Team

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
