---
title: Blog Topic Selection - Quick Summary
category: workflows
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-13
estimated_tokens: 645
load_when:
  - Before creating new blog post (default)
  - Quick topic validation
dependencies:
  - core/nda-compliance
  - core/enforcement
tags: [blog, topic-selection, summary, quick-reference]
---

# Blog Topic Selection - Quick Summary

## Module Metadata

**Category:** workflows
**Priority:** MEDIUM (load by default before blog posts)
**Estimated Size:** ~645 tokens
**Full Module:** `docs/context/workflows/blog-topic-selection.md` (3,000 tokens)

**Load full module when:**
- Planning content calendar
- Detailed topic evaluation
- Quarterly content review
- Need comprehensive topic idea bank

---

## 🔴 Critical Content Gaps (MUST FILL)

**Severely Underrepresented (2-3 posts each, target 8-10):**
1. **Cloud Security & Architecture** - AWS/Azure/GCP, multi-cloud, serverless
2. **Container & Orchestration** - Docker/K8s security, RBAC, service mesh
3. **Monitoring & Observability** - Prometheus, Grafana, Loki, distributed tracing
4. **Python Security Automation** - Script walkthroughs, pytest, API integrations

**Missing Formats:**
- Multi-part series (0 → need some!)
- Tool comparisons (minimal → need more!)
- Failure stories (minimal → need more!)
- Beginner guides (few → need more!)

---

## Quick Go/No-Go Filter

**Before scoring, verify ALL:**
```
✅ Personal homelab experience? (not work/NDA)
✅ Can test/demo in my environment?
✅ Unique angle or deeper than existing content?
✅ Readers can reproduce?
✅ Passes NDA compliance check?
```

**If ANY answer is NO → Reject topic immediately**

---

## Scoring System (Minimum 15/25 to Proceed)

| Criteria | Must/Prefer | Score |
|----------|-------------|-------|
| **Personal Experience** | Must be 4+ | __/5 |
| **Audience Value** | Must be 3+ | __/5 |
| **Search Potential** | Nice to have 3+ | __/5 |
| **Evergreen Longevity** | Prefer 4+ | __/5 |
| **Unique Angle** | Must be 3+ | __/5 |
| **TOTAL** | **Minimum 15** | __/25 |

**Priority Levels:**
- **18-25 points:** HIGH PRIORITY - Write immediately
- **15-17 points:** MEDIUM PRIORITY - Add to calendar
- **<15 points:** LOW PRIORITY - Reconsider or reframe

---

## Content Mix Target: 75/25 Evergreen-Trending

**Monthly quota (4 posts/month):**
- Week 1: Deep technical guide (evergreen, gap-filler)
- Week 2: Practical implementation (evergreen, hands-on)
- Week 3: Tool review/comparison (evergreen, new format)
- Week 4: Trending topic OR failure story (mixed)

**If this month already has 1 trending post → this post must be evergreen**

---

## When to Load Full Module

**Load `blog-topic-selection.md` (full 3,000 tokens) when:**
- Need comprehensive topic idea bank (90+ ideas across 5 categories)
- Planning quarterly content themes
- Detailed gap-filling priority matrix
- Topic research validation workflow
- Monthly/quarterly content review

**This summary is sufficient for:**
- Quick topic validation before writing
- Scoring a single topic idea
- Checking current content gaps
- Verifying NDA compliance

---

## Cross-References

**Related Modules:**
- Full module: `docs/context/workflows/blog-topic-selection.md`
- Writing workflow: `docs/context/workflows/blog-writing.md`
- NDA compliance: `docs/context/core/nda-compliance.md`

**Strategy Documents:**
- Comprehensive strategy: `docs/strategy/blog-topic-strategy-2025.md` (3,040 words)
- Quick start guide: `docs/strategy/TOPIC_SELECTION_QUICK_START.md` (921 words)
