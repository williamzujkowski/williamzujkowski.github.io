---
title: Blog Topic Selection - Enhanced with Research Posts
category: workflows
priority: MEDIUM
version: 2.0.0
last_updated: 2025-12-09
estimated_tokens: 850
load_when:
  - Before creating new blog post (default)
  - Quick topic validation
  - Research topic evaluation
dependencies:
  - core/nda-compliance
  - core/enforcement
tags: [blog, topic-selection, research, arxiv, theory, quick-reference]
---

# Blog Topic Selection - Enhanced with Research Posts

## Module Metadata

**Category:** workflows
**Priority:** MEDIUM (load by default before blog posts)
**Estimated Size:** ~850 tokens
**Full Module:** `docs/context/workflows/blog-topic-selection.md` (3,000 tokens)

**Load full module when:**
- Planning content calendar
- Detailed topic evaluation
- Quarterly content review
- Need comprehensive topic idea bank

---

## 📚 NEW: Research & Theory Posts

**Purpose:** Cover cutting-edge research from arXiv, cross-cutting theoretical developments, and emerging paradigms without requiring homelab implementation.

### Research Post Criteria

**MUST HAVE:**
- ✅ Based on recent papers (last 6 months preferred)
- ✅ Cross-cutting relevance (impacts multiple domains)
- ✅ Accessible explanation of complex concepts
- ✅ Clear "Why this matters" section
- ✅ Practical implications discussed

**NICE TO HAVE:**
- 📊 Visual diagrams explaining concepts
- 🔗 Links to 3+ high-quality papers
- 💡 Future predictions based on trends
- 🏗️ Potential applications in various fields

### Research Topic Scoring (15/25 minimum)

| Criteria | Weight | Score |
|----------|--------|-------|
| **Novelty & Timeliness** | High | __/5 |
| **Cross-Domain Impact** | High | __/5 |
| **Reader Accessibility** | High | __/5 |
| **Practical Relevance** | Medium | __/5 |
| **Future Potential** | Medium | __/5 |

### Good Research Topics

✅ **Ideal Examples:**
- "Mamba vs Transformers: Why State Space Models Might Replace Attention"
- "Quantum Error Correction Breakthrough: What Google's Willow Chip Means"
- "Diffusion Models Meet LLMs: The Convergence of Generation Paradigms"
- "Mechanistic Interpretability: Finally Understanding What Neural Networks Learn"

❌ **Avoid:**
- Pure reproductions of single papers
- Topics requiring PhD-level math without simplification
- Hype without substance
- Claims without citations

---

## 🔴 Critical Content Gaps (MUST FILL)

**Severely Underrepresented (2-3 posts each, target 8-10):**
1. **Cloud Security & Architecture** - AWS/Azure/GCP, multi-cloud, serverless
2. **Container & Orchestration** - Docker/K8s security, RBAC, service mesh
3. **Monitoring & Observability** - Prometheus, Grafana, Loki, distributed tracing
4. **Research & Theory** - arXiv papers, emerging paradigms, cross-cutting developments

**Missing Formats:**
- Multi-part series (0 → need some!)
- Tool comparisons (minimal → need more!)
- Failure stories (minimal → need more!)
- Research deep-dives (NEW → need 4-6!)

---

## Quick Go/No-Go Filter

### For Implementation Posts (Homelab/Tools)

**Before scoring, verify ALL:**
```
✅ Personal homelab experience? (not work/NDA)
✅ Can test/demo in my environment?
✅ Unique angle or deeper than existing content?
✅ Readers can reproduce?
✅ Passes NDA compliance check?
```

### For Research/Theory Posts

**Before scoring, verify ALL:**
```
✅ Based on credible sources (arXiv, conferences)?
✅ Can explain without excessive jargon?
✅ Cross-cutting relevance to multiple fields?
✅ Adds synthesis beyond source papers?
✅ Practical implications clear?
```

**If ANY answer is NO → Reject topic immediately**

---

## Scoring System (Minimum 15/25 to Proceed)

### Implementation Posts

| Criteria | Must/Prefer | Score |
|----------|-------------|-------|
| **Personal Experience** | Must be 4+ | __/5 |
| **Audience Value** | Must be 3+ | __/5 |
| **Search Potential** | Nice to have 3+ | __/5 |
| **Evergreen Longevity** | Prefer 4+ | __/5 |
| **Unique Angle** | Must be 3+ | __/5 |
| **TOTAL** | **Minimum 15** | __/25 |

### Research Posts

| Criteria | Must/Prefer | Score |
|----------|-------------|-------|
| **Source Quality** | Must be 4+ | __/5 |
| **Accessibility** | Must be 4+ | __/5 |
| **Cross-Domain Impact** | Must be 3+ | __/5 |
| **Timeliness** | Prefer 4+ | __/5 |
| **Practical Value** | Must be 3+ | __/5 |
| **TOTAL** | **Minimum 15** | __/25 |

**Priority Levels:**
- **18-25 points:** HIGH PRIORITY - Write immediately
- **15-17 points:** MEDIUM PRIORITY - Add to calendar
- **<15 points:** LOW PRIORITY - Reconsider or reframe

---

## Content Mix Target: 60/25/15 Implementation-Research-Meta

**Monthly quota (4 posts/month):**
- Week 1: Deep technical guide (implementation/homelab)
- Week 2: Research/theory post (arXiv synthesis)
- Week 3: Practical implementation (hands-on)
- Week 4: Tool review OR failure story OR meta topic

**Balance check:** If month has 2+ implementation → next must be research/theory

---

## Research Post Best Practices

### Structure Template

1. **Hook:** Why this research matters NOW
2. **Background:** Minimum context needed (no PhD required)
3. **Core Innovation:** What's actually new
4. **Visual Explanation:** Diagrams > equations
5. **Implications:** Real-world impact in 1-5 years
6. **Limitations:** Honest assessment
7. **Further Reading:** Curated paper list

### Writing Style for Research

- **Analogies over equations:** "Like a translator between languages"
- **Progressive disclosure:** Start simple, add depth
- **Practical framing:** "This could enable..."
- **Honest uncertainty:** "Researchers hypothesize..."
- **Clear attribution:** Every claim needs a citation

---

## When to Load Full Module

**Load `blog-topic-selection.md` (full 3,000 tokens) when:**
- Need comprehensive topic idea bank (90+ ideas)
- Planning quarterly content themes
- Detailed gap-filling priority matrix
- Topic research validation workflow
- Monthly/quarterly content review

**This summary is sufficient for:**
- Quick topic validation before writing
- Scoring a single topic idea
- Checking current content gaps
- Verifying NDA compliance
- Evaluating research topic potential

---

## Cross-References

**Related Modules:**
- Full module: `docs/context/workflows/blog-topic-selection.md`
- Writing workflow: `docs/context/workflows/blog-writing.md`
- NDA compliance: `docs/context/core/nda-compliance.md`
- Citation research: `docs/context/standards/citation-research.md`

**Strategy Documents:**
- Comprehensive strategy: `docs/strategy/blog-topic-strategy-2025.md`
- Research post guide: `docs/strategy/RESEARCH_POST_GUIDE.md` (NEW)